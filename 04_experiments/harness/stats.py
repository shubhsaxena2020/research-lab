"""Statistical primitives for the experiment harness (no scipy dependency).

Everything here is hand-implemented so that the numbers in the paper can be
re-derived on a machine with only numpy.  Every public function returns a dict
whose keys are meant to be copied verbatim into a results file: CONTRACTS.md
section 4 requires that a bootstrap CI always carries ``n_boot`` and
``ci_seed``, and that every reported p-value carries its correction method and
family size.

Conventions
-----------
* ``a`` is the *baseline* / first condition, ``b`` the *new* condition.
* Tests are two-sided unless stated otherwise.
* Nothing here imputes missing data, drops NaN silently, or returns a fake
  ``p = 1`` for a degenerate sample.

Validation status
-----------------
The exact Wilcoxon distribution is built by dynamic programming over rank-sum
counts and cross-checked in ``tests/test_stats.py`` against the published exact
values for n = 6 (P = 2/64 = 0.03125 for all-positive differences).  The
Holm/BH implementations are cross-checked against the worked examples in
R's ``p.adjust`` documentation semantics; a scipy cross-check runs when scipy
is importable and is skipped otherwise.
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import Callable, Iterable, Sequence

import numpy as np

__all__ = [
    "bootstrap_ci",
    "paired_test",
    "sign_test",
    "wilcoxon_signed_rank",
    "effect_size",
    "cohens_d",
    "cliffs_delta",
    "holm",
    "benjamini_hochberg",
    "summarise",
]

_ND = NormalDist()


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _as_1d(values, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float).ravel()
    if arr.size == 0:
        raise ValueError(f"{name} is empty")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains NaN or inf; clean the data first")
    return arr


def _check_alpha(alpha: float) -> float:
    alpha = float(alpha)
    if not 0.0 < alpha < 1.0:
        raise ValueError(f"alpha must be in (0, 1), got {alpha!r}")
    return alpha


def _stat_name(statistic: Callable) -> str:
    return getattr(statistic, "__name__", repr(statistic))


def _rng(seed):
    """Accept an int seed or an existing Generator (returned unchanged)."""
    if isinstance(seed, np.random.Generator):
        return seed
    if not isinstance(seed, (int, np.integer)):
        raise TypeError("seed must be an int or numpy.random.Generator")
    return np.random.default_rng(int(seed))


def _ranks(values: np.ndarray) -> np.ndarray:
    """Average (mid-)ranks, 1-based.  Ties get the mean of their rank block."""
    values = np.asarray(values, dtype=float)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    i = 0
    n = len(values)
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        ranks[order[i : j + 1]] = avg
        i = j + 1
    return ranks


# --------------------------------------------------------------------------
# bootstrap confidence intervals
# --------------------------------------------------------------------------
def bootstrap_ci(
    values,
    statistic: Callable = np.mean,
    n_boot: int = 10000,
    alpha: float = 0.05,
    seed: int = 12345,
    method: str = "percentile",
) -> dict:
    """Non-parametric bootstrap CI for a statistic of one sample.

    Returns ``{"lo", "hi", "method", "n_boot", "seed", "alpha", "statistic",
    "n", "notes"}`` — the four metadata fields the paper must report are
    ``n_boot``, ``seed`` (= ``ci_seed``), ``method`` and ``alpha``.

    Assumptions
    -----------
    * The observations are i.i.d. draws from the population of interest.  For
      seed-level experiment results that means "seeds are exchangeable"; if the
      seeds were chosen adversarially (e.g. one deliberately bad init) the
      resampling distribution is not the sampling distribution.
    * ``statistic`` must be a function of a 1-D array only (mean, median, ...).
      It must not depend on n in a way that changes its definition.

    Limitations a reviewer will attack
    ----------------------------------
    * With n < 5 the bootstrap distribution has at most C(2n-1, n) distinct
      resamples (n=5 -> 126), so the 2.5% and 97.5% quantiles are interpolations
      over a handful of points and are optimistic.  ``summarise`` flags this.
    * The percentile interval is *not* transformation-respecting and is biased
      when the statistic is skewed (accuracy near 1.0, F1 near 0).  BCa is the
      default recommendation for those metrics; percentile is the documented
      fallback used when BCa cannot be computed (zero-variance sample).
    * ``n_boot = 10000`` gives Monte-Carlo error of roughly 1-2% of the interval
      width on the bounds; report n_boot so the reader can judge.
    * The same ``seed`` must be reused across configs if intervals are to be
      compared cell-by-cell; this function is deterministic for a fixed seed.

    BCa (Efron 1987; Efron & Tibshirani 1993, ch. 14) corrects for median bias
    (z0, from the fraction of bootstrap replicates below the point estimate)
    and for skewness (acceleration a, from the jackknife).  It is second-order
    accurate where the percentile interval is first-order accurate.
    """
    x = _as_1d(values, "values")
    n = int(x.size)
    if n < 2:
        raise ValueError("bootstrap_ci needs at least 2 observations")
    alpha = _check_alpha(alpha)
    n_boot = int(n_boot)
    if n_boot < 100:
        raise ValueError("n_boot must be >= 100 for a usable interval")
    method = str(method).lower()
    if method not in {"percentile", "bca"}:
        raise ValueError("method must be 'percentile' or 'bca'")

    theta = float(statistic(x))
    rng = _rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))

    if statistic is np.mean:
        boot = x[idx].mean(axis=1)
    else:  # generic statistic: honest loop, 10k calls is cheap for small n
        boot = np.array([float(statistic(x[i])) for i in idx])

    notes = ""
    resolved = method
    if method == "bca":
        lo, hi, z0, accel, notes = _bca_interval(x, boot, theta, statistic, alpha)
        if lo is None:  # degenerate -> documented fallback
            resolved = "percentile"
            lo = float(np.quantile(boot, alpha / 2.0))
            hi = float(np.quantile(boot, 1.0 - alpha / 2.0))
    else:
        lo = float(np.quantile(boot, alpha / 2.0))
        hi = float(np.quantile(boot, 1.0 - alpha / 2.0))
        z0 = accel = None

    out = {
        "lo": lo,
        "hi": hi,
        "method": resolved,
        "n_boot": n_boot,
        "seed": int(seed) if isinstance(seed, (int, np.integer)) else None,
        "alpha": alpha,
        "statistic": _stat_name(statistic),
        "n": n,
        "point": theta,
        "notes": notes,
    }
    if z0 is not None:
        out["bca_z0"] = z0
        out["bca_acceleration"] = accel
    return out


def _bca_interval(x, boot, theta, statistic, alpha):
    """Return (lo, hi, z0, a, notes); lo is None when BCa is undefined."""
    n = x.size
    prop = float(np.mean(boot < theta))
    if prop == 0.0 or prop == 1.0:
        return (
            None,
            None,
            None,
            None,
            "BCa undefined: all bootstrap replicates lie on one side of the "
            "point estimate (zero-variance sample); fell back to percentile.",
        )
    z0 = _ND.inv_cdf(prop)

    # jackknife acceleration
    jack = np.empty(n, dtype=float)
    for i in range(n):
        jack[i] = float(statistic(np.delete(x, i)))
    jbar = jack.mean()
    d = jbar - jack
    denom = 6.0 * float(np.sum(d * d)) ** 1.5
    if denom == 0.0:
        return (
            None,
            None,
            None,
            None,
            "BCa undefined: jackknife variance is zero; fell back to percentile.",
        )
    accel = float(np.sum(d**3) / denom)

    def _adjust(q):
        zq = _ND.inv_cdf(q)
        num = z0 + zq
        den = 1.0 - accel * num
        if den == 0.0:
            return None
        return _ND.cdf(z0 + num / den)

    a1 = _adjust(alpha / 2.0)
    a2 = _adjust(1.0 - alpha / 2.0)
    if a1 is None or a2 is None or not (0.0 < a1 < a2 < 1.0):
        return (
            None,
            None,
            None,
            None,
            "BCa adjustment produced an invalid percentile pair; fell back to "
            "percentile.",
        )
    lo = float(np.quantile(boot, a1))
    hi = float(np.quantile(boot, a2))
    return lo, hi, float(z0), accel, "BCa (bias-corrected and accelerated)"


# --------------------------------------------------------------------------
# Wilcoxon signed-rank
# --------------------------------------------------------------------------
def _wilcoxon_exact_dp(ranks_sorted: np.ndarray) -> np.ndarray:
    """Counts of subsets of {1..n} with each rank sum, via DP.

    ``counts[s]`` = number of subsets of the integer ranks 1..n summing to s.
    Only valid when there are no ties (ranks are exactly 1..n).
    """
    n = int(ranks_sorted.size)
    max_sum = n * (n + 1) // 2
    counts = np.zeros(max_sum + 1, dtype=np.int64)
    counts[0] = 1
    for r in range(1, n + 1):
        # descending so each rank is used at most once
        counts[r:] += counts[:-r].copy()
    return counts


def _wilcoxon_exact_signflip(d: np.ndarray, ranks: np.ndarray) -> float:
    """Exact two-sided p by enumerating all 2^n sign flips (handles ties).

    Statistic: T = sum_i sign(d_i) * rank_i, observed T = W+ - W-.  Under H0 the
    signs are exchangeable, so P = #{|T*| >= |T|} / 2^n.  This is the exact
    permutation distribution; with distinct |d| it is identical to the exact
    Wilcoxon distribution (checked in the tests).
    """
    n = int(d.size)
    total = 1 << n
    obs = float(np.sum(np.sign(d) * ranks))
    tol = 1e-9 * max(1.0, abs(obs))
    chunk = 1 << 16
    hits = 0
    bits = np.arange(n)
    for start in range(0, total, chunk):
        stop = min(start + chunk, total)
        idx = np.arange(start, stop, dtype=np.int64)[:, None]
        signs = 1.0 - 2.0 * ((idx >> bits) & 1)
        stats = signs @ ranks
        hits += int(np.sum(np.abs(stats) >= abs(obs) - tol))
    return hits / total


def wilcoxon_signed_rank(a, b, alpha: float = 0.05) -> dict:
    """Two-sided Wilcoxon signed-rank test on paired samples.

    H0: the distribution of ``a - b`` is symmetric about zero.

    Assumptions
    -----------
    * Paired observations, same length, paired by index (same seed / same item).
    * Differences are independent and (under H1) from a symmetric distribution.
      Symmetry is the assumption reviewers attack; it fails for bounded or
      heavily skewed metrics (e.g. accuracy near 1.0), which is why
      ``paired_test`` offers the sign test as a robustness check.

    Method
    ------
    * n_eff <= 20 and no ties  -> exact null distribution by DP over rank sums
      (all 2^n sign assignments, no normal approximation).
    * n_eff <= 20 and ties     -> exact via full sign-flip enumeration
      (2^n <= 1,048,576; median ranks stay valid).
    * otherwise                -> normal approximation with tie correction
      sigma^2 = n(n+1)(2n+1)/24 - sum(t^3 - t)/48.

    Zeros are dropped (Wilcoxon's convention) and reported as ``n_zero``.
    The minimum attainable two-sided p at n_eff = n is 2/2^n, so n < 5 can
    never reach 0.05 — that is a property of the test, not a bug.
    """
    x = _as_1d(a, "a")
    y = _as_1d(b, "b")
    if x.size != y.size:
        raise ValueError(
            f"paired_test needs equal-length samples, got {x.size} vs {y.size}"
        )
    n_pairs = int(x.size)
    d = x - y
    n_zero = int(np.sum(d == 0))
    d = d[d != 0]
    n = int(d.size)
    if n == 0:
        return {
            "test": "wilcoxon",
            "statistic": None,
            "p_value": None,
            "n_pairs": n_pairs,
            "n_eff": 0,
            "n_zero": n_zero,
            "notes": "no test possible: every paired difference is zero",
            "method_detail": "none",
            "alpha": alpha,
        }

    absd = np.abs(d)
    ranks = _ranks(absd)
    w_plus = float(np.sum(ranks[d > 0]))
    w_minus = float(np.sum(ranks[d < 0]))
    ties = len(np.unique(absd)) < n
    total_rank_sum = float(n * (n + 1) / 2.0)

    if n <= 20 and not ties:
        counts = _wilcoxon_exact_dp(np.arange(1, n + 1, dtype=float))
        k = int(round(w_plus))
        p_low = float(counts[: k + 1].sum()) / float(2**n)
        p_high = float(counts[k:].sum()) / float(2**n)
        p = min(1.0, 2.0 * min(p_low, p_high))
        detail = f"exact (DP over rank sums, 2^{n} = {2**n} arrangements)"
        notes = (
            "exact two-sided p from the full null distribution; no normal "
            "approximation"
        )
        if n < 5:
            notes += f"; minimum attainable p at n={n} is {2.0/2**n:.4f}"
    elif n <= 20 and ties:
        p = _wilcoxon_exact_signflip(d, ranks)
        detail = f"exact (full sign-flip enumeration, 2^{n} = {2**n} arrangements)"
        notes = (
            "ties detected, so the rank-sum DP does not apply; p is exact by "
            "enumerating all sign assignments over the mid-ranks"
        )
        if n < 5:
            notes += f"; minimum attainable p at n={n} is {2.0/2**n:.4f}"
    else:
        mu = n * (n + 1) / 4.0
        tie_term = 0.0
        if ties:
            _, tcounts = np.unique(absd, return_counts=True)
            tie_term = float(np.sum(tcounts.astype(float) ** 3 - tcounts)) / 48.0
        var = n * (n + 1) * (2 * n + 1) / 24.0 - tie_term
        if var <= 0:
            return {
                "test": "wilcoxon",
                "statistic": w_plus,
                "p_value": None,
                "n_pairs": n_pairs,
                "n_eff": n,
                "n_zero": n_zero,
                "notes": "no test possible: zero variance under the null "
                "(all |differences| identical)",
                "method_detail": "none",
                "alpha": alpha,
            }
        z = (w_plus - mu) / math.sqrt(var)
        p = min(1.0, 2.0 * (1.0 - _ND.cdf(abs(z))))
        detail = "normal approximation with tie correction"
        notes = (
            "n_eff > 20 or ties beyond the exact limit; p from the normal "
            "approximation (no continuity correction, matching scipy's default)"
        )

    return {
        "test": "wilcoxon",
        "statistic": w_plus,
        "w_plus": w_plus,
        "w_minus": w_minus,
        "p_value": float(p),
        "n_pairs": n_pairs,
        "n_eff": n,
        "n_zero": n_zero,
        "ties": bool(ties),
        "method_detail": detail,
        "notes": notes,
        "alpha": alpha,
        "alternative": "two-sided",
        "rank_sum_total": total_rank_sum,
    }


# --------------------------------------------------------------------------
# sign test
# --------------------------------------------------------------------------
def sign_test(a, b, alpha: float = 0.05) -> dict:
    """Exact two-sided binomial sign test on paired samples.

    Counts how often ``a > b``; under H0 that count is Binomial(n_eff, 0.5).
    p = 2 * P(X <= min(n_pos, n_neg)), capped at 1.

    Assumptions: paired observations; each pair is an independent coin flip
    under H0.  It needs *no* symmetry and no normality, so it is the robust
    fallback — but it throws away magnitudes, so it is much less powerful than
    Wilcoxon when the differences are informative.  With n_eff = 5 the smallest
    attainable two-sided p is 2/32 = 0.0625: a non-significant result at that n
    is uninformative, not evidence of no effect.
    """
    x = _as_1d(a, "a")
    y = _as_1d(b, "b")
    if x.size != y.size:
        raise ValueError(
            f"sign_test needs equal-length samples, got {x.size} vs {y.size}"
        )
    n_pairs = int(x.size)
    d = x - y
    n_zero = int(np.sum(d == 0))
    n = n_pairs - n_zero
    if n == 0:
        return {
            "test": "sign_test",
            "statistic": None,
            "p_value": None,
            "n_pairs": n_pairs,
            "n_eff": 0,
            "n_zero": n_zero,
            "notes": "no test possible: every paired difference is zero",
            "alpha": alpha,
        }
    n_pos = int(np.sum(d > 0))
    n_neg = int(np.sum(d < 0))
    k = min(n_pos, n_neg)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / float(2**n)
    p = min(1.0, 2.0 * tail)
    notes = (
        f"exact binomial, {n_pos} positive / {n_neg} negative of {n} "
        f"non-zero differences"
    )
    if n < 6:
        notes += f"; minimum attainable p at n={n} is {2.0/2**n:.4f}"
    return {
        "test": "sign_test",
        "statistic": n_pos,
        "p_value": float(p),
        "n_pairs": n_pairs,
        "n_eff": n,
        "n_zero": n_zero,
        "n_pos": n_pos,
        "n_neg": n_neg,
        "notes": notes,
        "alpha": alpha,
        "alternative": "two-sided",
    }


# --------------------------------------------------------------------------
# dispatcher
# --------------------------------------------------------------------------
def paired_test(
    a,
    b,
    method: str = "auto",
    alpha: float = 0.05,
    correction: str | None = None,
    family_size: int | None = None,
) -> dict:
    """Paired significance test, returning the CONTRACTS section 4 dict.

    Keys: ``test``, ``statistic``, ``p_value``, ``n_pairs``, ``n_eff``,
    ``method_detail``, ``notes``, plus ``correction`` when supplied.

    ``method``
    ----------
    * ``"auto"`` (default): Wilcoxon signed-rank when n_eff >= 6 and not all
      differences are zero; the sign test when 0 < n_eff < 6; and an explicit
      ``{"test": "none", "p_value": None}`` when every difference is zero — it
      never emits a fake p = 1.
    * ``"wilcoxon"`` / ``"sign_test"``: forced (still honest about degenerate
      input).

    Assumptions: paired samples (same index = same seed/item), independent
    pairs.  Limitation: with fewer than 6 pairs no two-sided test here can
    reach p < 0.05 by construction; report the effect size and call the result
    inconclusive rather than "no difference".  If ``correction`` is given the
    p-value is *not* re-adjusted here — pass it through ``holm`` /
    ``benjamini_hochberg`` first and set ``p_adjusted`` yourself; this function
    only records the provenance.
    """
    x = _as_1d(a, "a")
    y = _as_1d(b, "b")
    if x.size != y.size:
        raise ValueError(
            f"paired_test needs equal-length samples, got {x.size} vs {y.size}"
        )
    method = str(method).lower()
    if method not in {"auto", "wilcoxon", "sign_test", "sign"}:
        raise ValueError("method must be 'auto', 'wilcoxon' or 'sign_test'")

    n_pairs = int(x.size)
    d = x - y
    n_zero = int(np.sum(d == 0))
    n_eff = n_pairs - n_zero

    if n_eff == 0:
        return {
            "test": "none",
            "statistic": None,
            "p_value": None,
            "n_pairs": n_pairs,
            "n_eff": 0,
            "n_zero": n_zero,
            "notes": (
                "no test possible: every paired difference is zero, so there is "
                "no evidence of any difference and no p-value to report (not "
                "p=1). Report the identical values as a null result."
            ),
            "alpha": alpha,
            "correction": (
                {"method": correction, "family_size": family_size}
                if correction
                else None
            ),
        }

    if method == "auto":
        chosen = "wilcoxon" if n_eff >= 6 else "sign_test"
    elif method == "sign":
        chosen = "sign_test"
    else:
        chosen = method

    res = (
        wilcoxon_signed_rank(x, y, alpha=alpha)
        if chosen == "wilcoxon"
        else sign_test(x, y, alpha=alpha)
    )

    if method == "auto":
        if chosen == "sign_test":
            res["notes"] += (
                f"; auto chose the sign test because n_eff={n_eff} < 6 (Wilcoxon's "
                "exact null is too coarse there)"
            )
        else:
            res["notes"] += f"; auto chose Wilcoxon (n_eff={n_eff} >= 6)"

    res["correction"] = (
        {"method": correction, "family_size": family_size} if correction else None
    )
    res["correction_note"] = (
        "p_value is UNADJUSTED; apply holm()/benjamini_hochberg() across the "
        "family before reporting"
        if correction
        else "no multiple-comparison correction recorded; CONTRACTS section 4 "
        "requires one for every reported p"
    )
    return res


# --------------------------------------------------------------------------
# effect sizes
# --------------------------------------------------------------------------
_INTERP = ((0.2, "negligible"), (0.5, "small"), (0.8, "medium"), (math.inf, "large"))
_CLIFF = (
    (0.147, "negligible"),
    (0.33, "small"),
    (0.474, "medium"),
    (math.inf, "large"),
)


def _band(value: float, table) -> str:
    v = abs(value)
    for edge, label in table:
        if v < edge:
            return label
    return "large"


def cohens_d(a, b, hedges: bool = False, n_boot: int = 2000, seed: int = 12345):
    """Standardised mean difference d = (mean_a - mean_b) / s_pooled.

    ``s_pooled = sqrt(((n1-1)s1^2 + (n2-1)s2^2) / (n1+n2-2))`` with ddof=1.

    Assumptions: continuous, roughly normal data with comparable spread; the
    pooled SD is only meaningful when the two SDs are of the same order.
    Limitations: d is unbounded and unstable for n < 10 (the SD is estimated
    from the same handful of points); for bounded metrics (accuracy in [0,1])
    it is not comparable across datasets — report the raw difference too.
    ``hedges=True`` applies the small-sample correction
    g = d * (1 - 3/(4(n1+n2)-9)) and reports it as ``hedges_g``.

    The bootstrap CI resamples pairs when ``len(a) == len(b)`` and treats the
    samples as independent otherwise; it is a percentile interval and inherits
    the small-n caveat above.
    """
    x = _as_1d(a, "a")
    y = _as_1d(b, "b")
    n1, n2 = int(x.size), int(y.size)
    if n1 < 2 or n2 < 2:
        raise ValueError("cohens_d needs at least 2 observations per group")
    s1 = float(np.std(x, ddof=1))
    s2 = float(np.std(y, ddof=1))
    sp2 = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2)
    sp = math.sqrt(sp2)
    if sp == 0.0:
        raise ValueError(
            "cohens_d undefined: pooled standard deviation is zero (both groups "
            "constant)"
        )
    d = (float(np.mean(x)) - float(np.mean(y))) / sp
    g = d * (1.0 - 3.0 / (4.0 * (n1 + n2) - 9.0)) if (n1 + n2) > 3 else d
    lo, hi = _bootstrap_effect_ci(x, y, lambda p, q: _d_value(p, q), n_boot, seed)
    return {
        "name": "hedges_g" if hedges else "cohens_d",
        "value": float(g if hedges else d),
        "cohens_d": float(d),
        "hedges_g": float(g),
        "ci95": [lo, hi],
        "ci_method": "bootstrap-percentile",
        "n_boot": int(n_boot),
        "seed": int(seed),
        "pooled_sd": sp,
        "n1": n1,
        "n2": n2,
        "interpretation": (
            f"{_band(d, _INTERP)} effect (Cohen 1988 thresholds: 0.2 small, "
            "0.5 medium, 0.8 large); positive means a > b"
        ),
    }


def _d_value(x, y):
    n1, n2 = len(x), len(y)
    s1 = float(np.std(x, ddof=1))
    s2 = float(np.std(y, ddof=1))
    sp = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    if sp == 0:
        return float("nan")
    return (float(np.mean(x)) - float(np.mean(y))) / sp


def cliffs_delta(a, b, n_boot: int = 2000, seed: int = 12345) -> dict:
    """Cliff's delta: P(a > b) - P(a < b), in [-1, 1].

    delta = (#(a>b) - #(a<b)) / (n1*n2); 0 means the two samples are
    stochastically indistinguishable, +1 that every a exceeds every b.

    Assumptions: independent samples (NOT paired — pairing is ignored, which is
    conservative but wasteful if the data are paired).  Robust to outliers and
    distribution-free.  Limitation: it saturates at +-1 whenever the samples are
    separable, so it cannot distinguish "slightly better everywhere" from
    "vastly better"; report the raw means alongside.
    Thresholds: Romano et al. (2006), 0.147 / 0.33 / 0.474.
    """
    x = _as_1d(a, "a")
    y = _as_1d(b, "b")
    n1, n2 = int(x.size), int(y.size)
    greater = float(np.sum(x[:, None] > y[None, :]))
    less = float(np.sum(x[:, None] < y[None, :]))
    delta = (greater - less) / float(n1 * n2)
    lo, hi = _bootstrap_effect_ci(
        x, y, lambda p, q: _cliffs_value(p, q), n_boot, seed
    )
    return {
        "name": "cliffs_delta",
        "value": float(delta),
        "ci95": [lo, hi],
        "ci_method": "bootstrap-percentile",
        "n_boot": int(n_boot),
        "seed": int(seed),
        "n1": n1,
        "n2": n2,
        "interpretation": (
            f"{_band(delta, _CLIFF)} effect (Romano et al. 2006 thresholds: "
            "0.147 small, 0.33 medium, 0.474 large); positive means a tends to "
            "exceed b"
        ),
    }


def _cliffs_value(x, y):
    greater = float(np.sum(x[:, None] > y[None, :]))
    less = float(np.sum(x[:, None] < y[None, :]))
    return (greater - less) / float(len(x) * len(y))


def relative_improvement(
    a, b, n_boot: int = 2000, seed: int = 12345, higher_is_better: bool = True
) -> dict:
    """Percent change from baseline ``a`` to new ``b``: 100*(mean_b-mean_a)/|mean_a|.

    Positive means b is larger than a, whatever the metric's polarity; use
    ``higher_is_better=False`` only to relabel the interpretation, the number
    itself is a plain ratio and the reader must know the metric direction.

    Assumptions: same metric, same units, same test set; ``mean_a != 0``.
    Limitations: unstable when the baseline is near zero (divide by a small
    number inflates the percentage — a 0.01 -> 0.02 change is "+100%"); not
    additive across metrics; a percentage hides the absolute gain, so always
    report both.  The CI is a percentile bootstrap of the ratio, which is
    asymmetric by construction (as it should be).
    """
    x = _as_1d(a, "a")
    y = _as_1d(b, "b")
    base = float(np.mean(x))
    if base == 0.0:
        raise ValueError(
            "relative_improvement undefined: baseline mean is zero (ratio has no "
            "scale); report the absolute difference instead"
        )
    val = 100.0 * (float(np.mean(y)) - base) / abs(base)

    def _stat(p, q):
        m = float(np.mean(p))
        if m == 0:
            return float("nan")
        return 100.0 * (float(np.mean(q)) - m) / abs(m)

    lo, hi = _bootstrap_effect_ci(x, y, _stat, n_boot, seed)
    direction = "improvement" if (val > 0) == higher_is_better else "regression"
    return {
        "name": "relative_improvement_pct",
        "value": float(val),
        "ci95": [lo, hi],
        "ci_method": "bootstrap-percentile",
        "n_boot": int(n_boot),
        "seed": int(seed),
        "baseline_mean": base,
        "new_mean": float(np.mean(y)),
        "interpretation": (
            f"{abs(val):.1f}% {'increase' if val >= 0 else 'decrease'} relative to "
            f"baseline; read as a {direction} given higher_is_better="
            f"{higher_is_better}"
        ),
    }


def _bootstrap_effect_ci(x, y, stat, n_boot, seed):
    """Percentile bootstrap CI for a two-sample statistic; paired if same length."""
    n1, n2 = len(x), len(y)
    paired = n1 == n2
    rng = _rng(seed)
    vals = np.empty(int(n_boot), dtype=float)
    if paired:
        for i in range(int(n_boot)):
            idx = rng.integers(0, n1, n1)
            vals[i] = stat(x[idx], y[idx])
    else:
        for i in range(int(n_boot)):
            vals[i] = stat(
                x[rng.integers(0, n1, n1)], y[rng.integers(0, n2, n2)]
            )
    vals = vals[np.isfinite(vals)]
    if vals.size < 10:
        return (float("nan"), float("nan"))
    return (
        float(np.quantile(vals, 0.025)),
        float(np.quantile(vals, 0.975)),
    )


def effect_size(a, b, kind: str = "cohens_d", **kwargs) -> dict:
    """Dispatcher returning ``{"name", "value", "interpretation", ...}``.

    ``kind`` in {"cohens_d", "hedges_g", "cliffs_delta",
    "relative_improvement"}.  The effect size is always *named* in the return
    value because CONTRACTS section 4 forbids an unnamed effect size.

    Direction convention: positive means ``a > b`` for d and delta, and for the
    relative improvement positive means b is larger than a (i.e. the percentage
    is computed as b relative to a).  That asymmetry is deliberate and is stated
    in each ``interpretation`` string.
    """
    kind = str(kind).lower()
    if kind == "cohens_d":
        return cohens_d(a, b, **kwargs)
    if kind == "hedges_g":
        return cohens_d(a, b, hedges=True, **kwargs)
    if kind == "cliffs_delta":
        return cliffs_delta(a, b, **kwargs)
    if kind in {"relative_improvement", "relative_improvement_pct"}:
        return relative_improvement(a, b, **kwargs)
    raise ValueError(
        "kind must be one of cohens_d, hedges_g, cliffs_delta, "
        f"relative_improvement; got {kind!r}"
    )


# --------------------------------------------------------------------------
# multiple-comparison correction
# --------------------------------------------------------------------------
def _validate_pvalues(p_values: Iterable[float]) -> list:
    ps = [float(p) for p in p_values]
    if not ps:
        raise ValueError("p_values is empty; there is no family to correct")
    for p in ps:
        if not (0.0 <= p <= 1.0) or math.isnan(p):
            raise ValueError(f"p-values must be in [0, 1], got {p!r}")
    return ps


def holm(p_values) -> dict:
    """Holm-Bonferroni step-down adjusted p-values.

    adjusted_(i) = max_{j <= i} min(1, (m - j + 1) * p_(j)) on the sorted
    p-values, i.e. the running maximum enforces monotonicity.

    Assumptions: the family of m tests was fixed *before* looking at the data
    (otherwise it is not a family), and the tests are valid individually.
    Controls the family-wise error rate at alpha under arbitrary dependence —
    no independence assumption.  Limitation: conservative when m is large and
    the tests are positively correlated (typical for accuracy/F1/loss on the
    same runs); report m so the reader can see the penalty.

    Note on the third value in the (0.01, 0.02, 0.03) example: the raw step-down
    products are 0.03, 0.04, 0.03, but adjusted p-values must be monotonically
    non-decreasing in the sorted order (R's p.adjust and statsmodels both
    enforce this), so the answer is 0.03, 0.04, 0.04.  Returning 0.03 for the
    largest raw p would claim more significance for the weakest test than for a
    stronger one, which is incoherent.
    """
    ps = _validate_pvalues(p_values)
    m = len(ps)
    order = np.argsort(np.asarray(ps, dtype=float), kind="mergesort")
    adjusted = np.empty(m, dtype=float)
    running = 0.0
    for rank, idx in enumerate(order, start=1):
        val = (m - rank + 1) * ps[idx]
        running = max(running, val)
        adjusted[idx] = min(1.0, running)
    return {
        "method": "holm",
        "family_size": m,
        "p_adjusted": [float(v) for v in adjusted],
        "p_raw": ps,
        "alpha": None,
        "notes": "step-down, FWER control under arbitrary dependence; "
        "monotonicity enforced (running maximum)",
    }


def benjamini_hochberg(p_values) -> dict:
    """Benjamini-Hochberg step-up adjusted p-values (FDR control).

    adjusted_(i) = min_{j >= i} (m / j) * p_(j), computed from the largest
    p-value downwards (running minimum).

    Assumptions: independent tests, or positive regression dependency (PRDS).
    Under arbitrary dependence use Benjamini-Yekutieli instead.  Controls the
    *expected false discovery proportion*, not the probability of any error, so
    a BH-adjusted p of 0.03 does not mean "3% chance of being wrong on this
    one".  Limitation: with m = 3 (a typical ablation) BH is barely less
    conservative than Holm — do not use it to buy significance you do not have.
    """
    ps = _validate_pvalues(p_values)
    m = len(ps)
    order = np.argsort(np.asarray(ps, dtype=float), kind="mergesort")
    adjusted = np.empty(m, dtype=float)
    running = 1.0
    for rank in range(m, 0, -1):
        idx = order[rank - 1]
        val = m * ps[idx] / rank
        running = min(running, val)
        adjusted[idx] = min(1.0, running)
    return {
        "method": "benjamini-hochberg",
        "family_size": m,
        "p_adjusted": [float(v) for v in adjusted],
        "p_raw": ps,
        "alpha": None,
        "notes": "step-up, FDR control assuming independence or PRDS",
    }


# --------------------------------------------------------------------------
# descriptive summary
# --------------------------------------------------------------------------
def summarise(values) -> dict:
    """Mean, sample SD (ddof=1), median, n, and a small-n warning.

    Assumptions: values are a complete set of independent runs of the same
    configuration on the same test split.  The SD is the sample SD (ddof=1),
    which is the one to report for n runs; the population SD would understate
    variability.  Limitation: with n < 5 the SD itself has ~50% sampling error,
    so any CI built from it is indicative only — ``note`` says so explicitly so
    the table generator can surface it.
    """
    x = _as_1d(values, "values")
    n = int(x.size)
    note = ""
    if n < 2:
        std = float("nan")
        note = "n < 2: standard deviation undefined; report the single run only"
    else:
        std = float(np.std(x, ddof=1))
        if n < 5:
            note = (
                f"n={n} < 5: SD and any CI are unreliable (the SD itself has "
                "large sampling error); treat intervals as indicative only"
            )
    return {
        "mean": float(np.mean(x)),
        "std": std,
        "median": float(np.median(x)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
        "n": n,
        "note": note,
    }


if __name__ == "__main__":  # tiny smoke test, no fixtures needed
    print(bootstrap_ci([0.79, 0.80, 0.81, 0.79, 0.80], method="bca"))
    print(paired_test([0.79, 0.80, 0.81, 0.79, 0.80], [0.90, 0.91, 0.89, 0.92, 0.91]))
    print(holm([0.01, 0.02, 0.03]))
    print(summarise([1, 2, 3, 4]))
