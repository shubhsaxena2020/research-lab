"""Validation tests for ``stats.py``.

Every expected number below is either derived by hand in the comment above the
assertion or taken from a published exact table.  Where a value is a known
textbook result the source is named, because the paper's credibility depends on
this module being right rather than merely self-consistent.
"""

import math

import numpy as np
import pytest

import stats

MEAN = lambda xs: sum(xs) / len(xs)  # noqa: E731


# --------------------------------------------------------------------------
# bootstrap
# --------------------------------------------------------------------------
def test_bootstrap_brackets_mean_and_is_deterministic():
    sample = [0.79, 0.80, 0.81, 0.79, 0.80]
    a = stats.bootstrap_ci(sample, n_boot=4000, seed=7)
    b = stats.bootstrap_ci(sample, n_boot=4000, seed=7)
    m = MEAN(sample)
    assert a["lo"] <= m <= a["hi"]
    assert (a["lo"], a["hi"]) == (b["lo"], b["hi"])  # same seed -> same interval
    assert a["n_boot"] == 4000
    assert a["seed"] == 7
    assert a["method"] == "percentile"


def test_bootstrap_changes_with_a_different_seed():
    sample = [0.10, 0.40, 0.90, 0.55, 0.72, 0.33, 0.68]
    a = stats.bootstrap_ci(sample, n_boot=2000, seed=1)
    b = stats.bootstrap_ci(sample, n_boot=2000, seed=2)
    assert (a["lo"], a["hi"]) != (b["lo"], b["hi"])
    # both still bracket the point estimate
    m = MEAN(sample)
    assert a["lo"] <= m <= a["hi"] and b["lo"] <= m <= b["hi"]


def test_bca_differs_from_percentile_on_a_skewed_sample():
    # Right-skewed: six values near 1, two large outliers.  The percentile
    # interval is symmetric-ish around the bootstrap distribution; BCa shifts
    # both bounds upward because the bootstrap distribution is skewed (z0 > 0
    # here) -- that shift is the documented reason to prefer BCa for small n.
    skewed = [1.2, 1.3, 1.1, 1.4, 1.0, 8.0, 9.0, 1.5]
    pct = stats.bootstrap_ci(skewed, n_boot=8000, seed=12345, method="percentile")
    bca = stats.bootstrap_ci(skewed, n_boot=8000, seed=12345, method="bca")
    m = MEAN(skewed)
    assert pct["lo"] <= m <= pct["hi"]
    assert bca["lo"] <= m <= bca["hi"]
    assert bca["method"] == "bca"
    assert bca["lo"] != pct["lo"] or bca["hi"] != pct["hi"]
    assert bca["lo"] > pct["lo"]  # bias/skew correction pulls the lower bound up
    assert "bca_z0" in bca and "bca_acceleration" in bca
    # determinism holds for BCa too
    again = stats.bootstrap_ci(skewed, n_boot=8000, seed=12345, method="bca")
    assert (again["lo"], again["hi"]) == (bca["lo"], bca["hi"])


def test_bca_falls_back_to_percentile_on_zero_variance_sample():
    # Every observation identical: the bootstrap distribution is a point mass,
    # z0 is undefined (P(boot < theta) = 0), so BCa must say so and fall back.
    r = stats.bootstrap_ci([0.5] * 5, n_boot=500, method="bca")
    assert r["method"] == "percentile"
    assert "BCa undefined" in r["notes"]
    assert r["lo"] == r["hi"] == pytest.approx(0.5)


def test_bootstrap_rejects_bad_input():
    with pytest.raises(ValueError):
        stats.bootstrap_ci([1.0])
    with pytest.raises(ValueError):
        stats.bootstrap_ci([1.0, float("nan"), 2.0])
    with pytest.raises(ValueError):
        stats.bootstrap_ci([1.0, 2.0, 3.0], method="jackknife")


# --------------------------------------------------------------------------
# Wilcoxon signed-rank: exact distribution
# --------------------------------------------------------------------------
def test_wilcoxon_exact_n6_all_positive_is_2_over_64():
    """n = 6, all differences positive -> W+ = 1+2+3+4+5+6 = 21.

    The exact null distribution has 2^6 = 64 equally likely sign assignments.
    P(W+ >= 21) = 1/64 (only the all-positive assignment reaches 21), and
    P(W+ <= 21) = 1, so the two-sided exact p = 2 * (1/64) = 0.03125.
    This is the textbook exact value for the smallest all-positive case
    (Siegel & Castellan 1988, Table H; also scipy.stats.wilcoxon(method='exact')).
    """
    r = stats.wilcoxon_signed_rank([1, 2, 3, 4, 5, 6], [0] * 6)
    assert r["statistic"] == pytest.approx(21.0)
    assert r["p_value"] == pytest.approx(2 / 64, abs=1e-12)
    assert r["p_value"] == pytest.approx(0.03125, abs=1e-12)
    assert "exact" in r["method_detail"]
    assert r["n_eff"] == 6


def test_wilcoxon_exact_one_small_negative_is_4_over_64():
    """One negative difference carrying rank 1 -> W+ = 21 - 1 = 20.

    # {subsets of {1..6} summing to 20} = 1 (drop rank 1) and summing to 21 = 1,
    # so P(W+ >= 20) = 2/64 and P(W+ <= 20) = 63/64.
    Two-sided exact p = 2 * min(63/64, 2/64) = 4/64 = 0.0625.
    """
    r = stats.wilcoxon_signed_rank([-0.5, 2, 3, 4, 5, 6], [0] * 6)
    assert r["statistic"] == pytest.approx(20.0)
    assert r["p_value"] == pytest.approx(4 / 64, abs=1e-12)
    assert r["p_value"] == pytest.approx(0.0625, abs=1e-12)


def test_wilcoxon_exact_n9_all_positive_is_2_over_512():
    """n = 9: W+ = 45 = 9*10/2, only one of 2^9 = 512 assignments is as extreme."""
    r = stats.wilcoxon_signed_rank([1, 2, 3, 4, 5, 6, 7, 8, 9], [0] * 9)
    assert r["statistic"] == pytest.approx(45.0)
    assert r["p_value"] == pytest.approx(2 / 512, abs=1e-12)


def test_wilcoxon_dp_matches_full_enumeration_without_ties():
    """The DP count and the 2^n sign-flip enumeration must agree exactly."""
    d = np.array([1.0, -2.5, 3.0, 4.5, -5.0, 6.5, 7.0])
    p_dp = stats.wilcoxon_signed_rank(d, np.zeros_like(d))["p_value"]
    ranks = stats._ranks(np.abs(d))
    p_enum = stats._wilcoxon_exact_signflip(d, ranks)
    assert p_dp == pytest.approx(p_enum, abs=1e-12)


def test_wilcoxon_with_ties_uses_exact_enumeration():
    # Three tied pairs (all positive): 2^6 = 64 assignments, and only the
    # all-positive one has |T| as large as the observed T, so p = 2/64.
    r = stats.wilcoxon_signed_rank([1, 1, 2, 2, 3, 3], [0] * 6)
    assert r["ties"] is True
    assert "sign-flip" in r["method_detail"]
    assert r["p_value"] == pytest.approx(2 / 64, abs=1e-12)


def test_wilcoxon_drops_zeros_and_reports_them():
    # 5 pairs, one exactly zero -> n_eff = 4, all four non-zero differences
    # negative, so W+ = 0 and the exact two-sided p = 2 * P(W+ = 0)
    # = 2 * (1/16) = 0.125.
    r = stats.wilcoxon_signed_rank([1, 2, 3, 4, 5], [1, 3, 4, 5, 6])
    assert r["n_pairs"] == 5
    assert r["n_zero"] == 1
    assert r["n_eff"] == 4
    assert r["statistic"] == pytest.approx(0.0)
    assert r["p_value"] == pytest.approx(2 / 16, abs=1e-12)


def test_wilcoxon_normal_approximation_above_twenty():
    r = stats.wilcoxon_signed_rank(
        np.arange(1, 22, dtype=float), np.zeros(21)
    )
    assert "normal approximation" in r["method_detail"]
    # Hand value: W+ = 231, mu = 21*22/4 = 115.5,
    # var = 21*22*43/24 = 827.75, sigma = 28.7706,
    # z = 115.5/28.7706 = 4.0145, two-sided p = 2*(1-Phi(4.0145)) ~ 5.96e-5.
    assert r["p_value"] == pytest.approx(5.96e-5, rel=2e-3)


def test_wilcoxon_matches_scipy_when_available():
    scipy_stats = pytest.importorskip("scipy.stats")
    rng = np.random.default_rng(0)
    for d in (
        np.array([1.0, 2, 3, 4, 5, 6]),
        np.array([0.3, -1.2, 2.0, 2.4, -0.1, 3.3, 1.7]),
    ):
        ours = stats.wilcoxon_signed_rank(d, np.zeros_like(d))
        theirs = scipy_stats.wilcoxon(d, method="exact")
        assert ours["p_value"] == pytest.approx(theirs.pvalue, abs=1e-12)
    big = rng.normal(0.4, 1.0, size=25)
    ours = stats.wilcoxon_signed_rank(big, np.zeros_like(big))
    theirs = scipy_stats.wilcoxon(big, method="approx", correction=False)
    assert ours["p_value"] == pytest.approx(theirs.pvalue, rel=1e-9)
    # tie correction must match too (rounded data -> mid-ranks)
    tied = np.round(rng.normal(0.6, 1.0, size=30), 1)
    ours = stats.wilcoxon_signed_rank(tied, np.zeros_like(tied))
    theirs = scipy_stats.wilcoxon(tied, method="approx", correction=False)
    assert ours["p_value"] == pytest.approx(theirs.pvalue, rel=1e-9)


def test_bca_matches_scipy_when_available():
    scipy_stats = pytest.importorskip("scipy.stats")
    x = np.array([0.79, 0.80, 0.81, 0.79, 0.80, 0.82])
    ours = stats.bootstrap_ci(x, n_boot=40000, seed=5, method="bca")
    ref = scipy_stats.bootstrap(
        (x,),
        np.mean,
        n_resamples=40000,
        method="BCa",
        random_state=np.random.default_rng(5),
    )
    lo, hi = ref.confidence_interval
    width = ours["hi"] - ours["lo"]
    # Same estimator, different RNG stream -> bounds agree to Monte-Carlo error.
    assert ours["lo"] == pytest.approx(lo, abs=0.01 * width)
    assert ours["hi"] == pytest.approx(hi, abs=0.02 * width)


# --------------------------------------------------------------------------
# sign test
# --------------------------------------------------------------------------
def test_sign_test_obvious_case():
    # 9 of 10 pairs positive.  p = 2*P(X <= 1), X ~ Bin(10, 0.5)
    #   = 2*(C(10,0) + C(10,1)) / 2^10 = 2*11/1024 = 22/1024 = 0.021484375
    a = [1.0] * 9 + [-1.0]
    b = [0.0] * 10
    r = stats.sign_test(a, b)
    assert r["n_pos"] == 9 and r["n_neg"] == 1
    assert r["p_value"] == pytest.approx(22 / 1024, abs=1e-12)
    assert r["p_value"] == pytest.approx(0.021484375, abs=1e-12)


def test_sign_test_symmetric_case_is_one():
    # 5 positive / 5 negative, no zeros (zeros would be dropped):
    # p = 2*P(X <= 5) = 2*638/1024 = 1.246 -> capped at 1.0, exactly.
    r = stats.sign_test([1, 1, 1, 1, 1, -1, -1, -1, -1, -1], [0] * 10)
    assert r["n_pos"] == 5 and r["n_neg"] == 5
    assert r["p_value"] == pytest.approx(1.0, abs=1e-12)


# --------------------------------------------------------------------------
# effect sizes
# --------------------------------------------------------------------------
def test_cohens_d_hand_computed_pooled_sd():
    # a = 1..5, b = 2..6.  mean_a = 3, mean_b = 4.
    # s_a^2 = s_b^2 = 2.5 (ddof=1), so s_pooled = sqrt(2.5) = 1.5811388...
    # d = (3 - 4) / 1.5811388 = -0.6324555...
    a = [1, 2, 3, 4, 5]
    b = [2, 3, 4, 5, 6]
    r = stats.effect_size(a, b, kind="cohens_d", n_boot=500, seed=1)
    assert r["name"] == "cohens_d"
    assert r["pooled_sd"] == pytest.approx(math.sqrt(2.5), rel=1e-12)
    assert r["value"] == pytest.approx(-1 / math.sqrt(2.5), rel=1e-12)
    assert r["value"] == pytest.approx(-0.6324555320336759, rel=1e-12)
    # |d| = 0.63 lies in [0.5, 0.8) -> "medium" by Cohen's thresholds.
    assert "medium" in r["interpretation"]
    assert r["ci95"][0] <= r["value"] <= r["ci95"][1]


def test_hedges_g_correction():
    # g = d * (1 - 3/(4*(n1+n2)-9)) = d * (1 - 3/31) for n1 = n2 = 5.
    a = [1, 2, 3, 4, 5]
    b = [2, 3, 4, 5, 6]
    d = stats.cohens_d(a, b, n_boot=200, seed=1)["value"]
    g = stats.effect_size(a, b, kind="hedges_g", n_boot=200, seed=1)
    assert g["name"] == "hedges_g"
    assert g["value"] == pytest.approx(d * (1 - 3 / 31), rel=1e-12)
    assert abs(g["value"]) < abs(d)


def test_cliffs_delta_separable_is_one():
    # Every value in a exceeds every value in b: (#gt - #lt)/(n1*n2) = 1.
    r = stats.effect_size([5, 6, 7], [1, 2, 3], kind="cliffs_delta", n_boot=200)
    assert r["name"] == "cliffs_delta"
    assert r["value"] == pytest.approx(1.0, abs=1e-12)
    assert "large" in r["interpretation"]


def test_cliffs_delta_hand_computed_mid_case():
    # a = [2, 4], b = [1, 3].  Pairs: (2>1) +, (2>3) -, (4>1) +, (4>3) +
    # #gt = 3, #lt = 1, n1*n2 = 4 -> delta = (3-1)/4 = 0.5
    r = stats.cliffs_delta([2, 4], [1, 3], n_boot=200)
    assert r["value"] == pytest.approx(0.5, abs=1e-12)


def test_relative_improvement_and_ci():
    # mean_a = 0.80, mean_b = 0.90 -> +12.5% relative to baseline.
    a = [0.78, 0.79, 0.80, 0.81, 0.82]
    b = [0.88, 0.89, 0.90, 0.91, 0.92]
    r = stats.effect_size(a, b, kind="relative_improvement", n_boot=1000, seed=3)
    assert r["name"] == "relative_improvement_pct"
    assert r["value"] == pytest.approx(12.5, rel=1e-12)
    assert r["ci95"][0] <= 12.5 <= r["ci95"][1]
    assert r["n_boot"] == 1000 and r["seed"] == 3


def test_effect_size_requires_a_named_kind():
    with pytest.raises(ValueError):
        stats.effect_size([1, 2, 3], [2, 3, 4], kind="eta_squared")


# --------------------------------------------------------------------------
# multiple comparisons
# --------------------------------------------------------------------------
def test_holm_known_values():
    """Holm on (0.01, 0.02, 0.03), m = 3.

    Raw step-down products: 3*0.01 = 0.03, 2*0.02 = 0.04, 1*0.03 = 0.03.
    Holm's adjusted p-values must be monotonically non-decreasing in the sorted
    order (R's p.adjust and statsmodels both enforce this with a running
    maximum), so the third value is lifted to 0.04: [0.03, 0.04, 0.04].
    Returning the raw 0.03 would claim the weakest test is more significant
    than a stronger one -- incoherent, and not what any reference
    implementation reports.
    """
    r = stats.holm([0.01, 0.02, 0.03])
    assert r["method"] == "holm"
    assert r["family_size"] == 3
    assert r["p_adjusted"] == pytest.approx([0.03, 0.04, 0.04], abs=1e-12)


def test_holm_is_order_invariant_and_monotone():
    r = stats.holm([0.03, 0.01, 0.02])
    assert r["p_adjusted"] == pytest.approx([0.04, 0.03, 0.04], abs=1e-12)
    adj = np.asarray(r["p_adjusted"])
    assert np.all(adj >= np.asarray(r["p_raw"]) - 1e-15)
    order = np.argsort(r["p_raw"])
    assert np.all(np.diff(adj[order]) >= -1e-15)


def test_holm_four_values_hand_computed():
    """m = 4, p = (0.01, 0.04, 0.03, 0.005) in input order.

    Sorted: 0.005, 0.01, 0.03, 0.04.
    Products: 4*.005 = 0.02, 3*.01 = 0.03, 2*.03 = 0.06, 1*.04 = 0.04.
    Running max: 0.02, 0.03, 0.06, 0.06.  Back to input order:
    p=0.01 -> 0.03, p=0.04 -> 0.06, p=0.03 -> 0.06, p=0.005 -> 0.02.
    """
    r = stats.holm([0.01, 0.04, 0.03, 0.005])
    assert r["p_adjusted"] == pytest.approx([0.03, 0.06, 0.06, 0.02], abs=1e-12)


def test_bh_known_values():
    """BH on (0.01, 0.02, 0.03), m = 3.

    Sorted descending: i=3 -> 3/3*0.03 = 0.03; i=2 -> 3/2*0.02 = 0.03;
    i=1 -> 3/1*0.01 = 0.03.  Running minimum from the top leaves all at 0.03.
    """
    r = stats.benjamini_hochberg([0.01, 0.02, 0.03])
    assert r["method"] == "benjamini-hochberg"
    assert r["family_size"] == 3
    assert r["p_adjusted"] == pytest.approx([0.03, 0.03, 0.03], abs=1e-12)


def test_bh_six_values_hand_computed():
    """m = 6, ascending p = 0.001, 0.008, 0.039, 0.041, 0.042, 0.06.

    Products 6/i * p_i: 0.006, 0.024, 0.078, 0.0615, 0.0504, 0.06.
    Running minimum from the largest: 0.06, 0.0504, 0.0504, 0.0504, 0.024, 0.006
    -> adjusted = [0.006, 0.024, 0.0504, 0.0504, 0.0504, 0.06].
    """
    p = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06]
    r = stats.benjamini_hochberg(p)
    assert r["p_adjusted"] == pytest.approx(
        [0.006, 0.024, 0.0504, 0.0504, 0.0504, 0.06], abs=1e-12
    )


def test_bh_matches_scipy_when_available():
    scipy_stats = pytest.importorskip("scipy.stats")
    p = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.2]
    r = stats.benjamini_hochberg(p)
    assert r["p_adjusted"] == pytest.approx(
        list(scipy_stats.false_discovery_control(p)), abs=1e-12
    )


def test_corrections_reject_bad_pvalues():
    for fn in (stats.holm, stats.benjamini_hochberg):
        with pytest.raises(ValueError):
            fn([])
        with pytest.raises(ValueError):
            fn([0.5, 1.2])
        with pytest.raises(ValueError):
            fn([0.5, float("nan")])


# --------------------------------------------------------------------------
# dispatcher behaviour: no fake p-values
# --------------------------------------------------------------------------
def test_all_zero_differences_returns_no_test_not_p_one():
    r = stats.paired_test([0.8, 0.8, 0.8], [0.8, 0.8, 0.8])
    assert r["test"] == "none"
    assert r["p_value"] is None
    assert r["statistic"] is None
    assert "no test possible" in r["notes"]
    assert r["n_zero"] == r["n_pairs"] == 3


def test_auto_picks_wilcoxon_at_six_pairs_and_sign_test_below():
    a = [1, 2, 3, 4, 5, 6]
    b = [0] * 6
    assert stats.paired_test(a, b)["test"] == "wilcoxon"
    r = stats.paired_test([1, 2, 3, 4, 5], [0] * 5)
    assert r["test"] == "sign_test"
    assert "n_eff=5 < 6" in r["notes"]


def test_paired_test_records_correction_provenance():
    r = stats.paired_test(
        [1, 2, 3, 4, 5, 6], [0] * 6, correction="holm", family_size=4
    )
    assert r["correction"] == {"method": "holm", "family_size": 4}
    assert "UNADJUSTED" in r["correction_note"]


def test_paired_test_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        stats.paired_test([1, 2, 3], [1, 2])


def test_summarise_hand_computed():
    r = stats.summarise([1, 2, 3, 4, 5])
    assert r["mean"] == pytest.approx(3.0)
    assert r["std"] == pytest.approx(math.sqrt(2.5))  # ddof=1
    assert r["median"] == pytest.approx(3.0)
    assert r["n"] == 5
    assert r["note"] == ""  # n = 5 is at the reporting threshold


def test_summarise_warns_below_five():
    r = stats.summarise([0.70, 0.72, 0.74, 0.76])
    assert r["n"] == 4
    assert r["std"] == pytest.approx(0.02582, rel=1e-3)
    assert "n=4" in r["note"] and "unreliable" in r["note"]


def test_summarise_single_value_has_no_sd():
    r = stats.summarise([0.9])
    assert math.isnan(r["std"])
    assert "n < 2" in r["note"]
