"""Tests for the ablation-table generator.

The fixtures are written to ``tmp_path`` so the tests never read or write a real
results file, and so a missing-metric check cannot pass by accident.
"""

import json

import pytest

import tables


def _summary(sig_accuracy=0.0312, sig_loss=0.42, **overrides):
    """Multi-metric summary in the CONTRACTS-section-4 generalised shape."""
    data = {
        "experiment": "ablation",
        "configs": ["baseline", "ours", "no_aux"],
        "metrics": ["accuracy", "loss"],
        "per_run": {
            "accuracy": {
                "baseline": [0.79, 0.80, 0.81, 0.79, 0.80],
                "ours": [0.90, 0.91, 0.92, 0.90, 0.91],
                "no_aux": [0.85, 0.86, 0.84, 0.85, 0.86],
            },
            "loss": {
                "baseline": [0.41, 0.42, 0.43, 0.42, 0.41],
                "ours": [0.30, 0.31, 0.32, 0.31, 0.30],
                "no_aux": [0.33, 0.34, 0.32, 0.33, 0.34],
            },
        },
        "stats": {
            "accuracy": {
                "baseline": {
                    "mean": 0.798,
                    "std": 0.0075,
                    "ci95": [0.790, 0.806],
                    "n": 5,
                    "ci_method": "bootstrap",
                    "n_boot": 10000,
                    "ci_seed": 12345,
                },
                "ours": {
                    "mean": 0.908,
                    "std": 0.0084,
                    "ci95": [0.900, 0.916],
                    "n": 5,
                    "ci_method": "bootstrap",
                    "n_boot": 10000,
                    "ci_seed": 12345,
                },
                "no_aux": {
                    "mean": 0.852,
                    "std": 0.0084,
                    "ci95": [0.844, 0.860],
                    "n": 5,
                    "ci_method": "bootstrap",
                    "n_boot": 10000,
                    "ci_seed": 12345,
                },
            },
            "loss": {
                "baseline": {"mean": 0.418, "std": 0.0084, "n": 5},
                "ours": {"mean": 0.308, "std": 0.0084, "n": 5},
                "no_aux": {"mean": 0.332, "std": 0.0084, "n": 5},
            },
        },
        "paired": {
            "accuracy": {
                "test": "wilcoxon",
                "p_value": sig_accuracy,
                "n_pairs": 5,
                "correction": {
                    "method": "holm",
                    "family_size": 2,
                    "p_adjusted": sig_accuracy,
                },
            },
            "loss": {
                "test": "wilcoxon",
                "p_value": sig_loss,
                "n_pairs": 5,
                "correction": {"method": "holm", "family_size": 2, "p_adjusted": sig_loss},
            },
        },
    }
    data.update(overrides)
    return data


@pytest.fixture()
def summary_file(tmp_path):
    p = tmp_path / "summary_ablation.json"
    p.write_text(json.dumps(_summary()), encoding="utf-8")
    return p


@pytest.fixture()
def null_file(tmp_path):
    """Same numbers, but neither metric's winner is significant."""
    p = tmp_path / "summary_null.json"
    p.write_text(json.dumps(_summary(sig_accuracy=0.42, sig_loss=0.61)), encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def test_md_renders_all_cells_with_n(summary_file):
    text, warnings = tables.ablation_table(
        summary_file, ["accuracy", "loss"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert "| config | accuracy | loss |" in text
    assert "0.7980 ± 0.0075 (n=5)" in text
    assert "0.9080" in text and "0.4180" in text
    for cfg in ("baseline", "ours", "no_aux"):
        assert f"| {cfg} |" in text
    # direction was inferred from the names, and that is reported, not hidden
    assert any("direction inferred" in w for w in warnings)


def test_tex_emits_booktabs_rules(summary_file):
    text, _ = tables.ablation_table(
        summary_file,
        ["accuracy", "loss"],
        ["baseline", "ours", "no_aux"],
        fmt="tex",
        caption="Ablation study",
        label="tab:ablation",
    )
    assert r"\toprule" in text
    assert r"\midrule" in text
    assert r"\bottomrule" in text
    assert r"\begin{tabular}{lcc}" in text
    assert r"\end{tabular}" in text
    assert r"\caption{Ablation study}" in text
    assert r"\label{tab:ablation}" in text
    # underscores in config/metric names must be escaped for LaTeX
    assert r"no\_aux" in text


def test_contract_single_metric_shape(tmp_path):
    single = {
        "experiment": "main",
        "configs": ["baseline", "ours"],
        "metric": "accuracy",
        "n_seeds": 5,
        "seeds": [0, 1, 2, 3, 4],
        "per_run": {
            "baseline": [0.79, 0.80, 0.81, 0.79, 0.80],
            "ours": [0.90, 0.91, 0.92, 0.90, 0.91],
        },
        "stats": {
            "baseline": {
                "mean": 0.798,
                "std": 0.0075,
                "n": 5,
                "ci95": [0.790, 0.806],
                "ci_method": "bootstrap",
                "n_boot": 10000,
                "ci_seed": 12345,
            },
            "ours": {
                "mean": 0.908,
                "std": 0.0084,
                "n": 5,
                "ci95": [0.900, 0.916],
                "ci_method": "bootstrap",
                "n_boot": 10000,
                "ci_seed": 12345,
            },
        },
        "paired": {"test": "wilcoxon", "p_value": 0.0312, "n_pairs": 5},
    }
    p = tmp_path / "summary_main.json"
    p.write_text(json.dumps(single), encoding="utf-8")
    text, _ = tables.ablation_table(p, ["accuracy"], ["baseline", "ours"], fmt="md")
    assert "0.7980 ± 0.0075 (n=5)" in text
    assert "**0.9080" in text  # significant, so bolded
    ci, _ = tables.ablation_table(
        p, ["accuracy"], ["baseline", "ours"], fmt="md", dispersion="ci"
    )
    assert "[0.7900, 0.8060]" in ci
    # CONTRACTS section 4: an interval must carry n_boot and ci_seed
    assert "seed 12345" in ci and "resamples" in ci


# --------------------------------------------------------------------------
# bolding follows the paired test
# --------------------------------------------------------------------------
def test_significant_case_bolds_the_winner(summary_file):
    md, _ = tables.ablation_table(
        summary_file, ["accuracy"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert "**0.9080 ± 0.0084**" in md
    assert "bold marks the best config" in md

    tex, _ = tables.ablation_table(
        summary_file, ["accuracy"], ["baseline", "ours", "no_aux"], fmt="tex"
    )
    assert r"\textbf{$0.9080 \pm 0.0084$}" in tex


def test_non_significant_case_does_not_bold(null_file):
    md, _ = tables.ablation_table(
        null_file, ["accuracy", "loss"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert "**" not in md  # nothing bolded anywhere
    assert "not statistically significant" in md
    # and the table still carries the numbers (no silent suppression)
    assert "0.9080" in md and "0.3080" in md

    tex, _ = tables.ablation_table(
        null_file, ["accuracy", "loss"], ["baseline", "ours", "no_aux"], fmt="tex"
    )
    assert r"\textbf{" not in tex


def test_lower_is_better_metric_picks_the_smallest(summary_file):
    # loss: ours 0.308 < no_aux 0.332 < baseline 0.418.  p=0.42 -> no bold,
    # but the footnote must name `ours` as the winner, proving direction was used.
    md, _ = tables.ablation_table(
        summary_file, ["loss"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert "between ours and no_aux" in md
    assert "**0.3080" not in md


def test_no_paired_block_means_no_bold(tmp_path):
    data = _summary()
    del data["paired"]
    p = tmp_path / "summary_nopaired.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    md, warnings = tables.ablation_table(
        p, ["accuracy"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert "**" not in md
    assert any("no paired test" in w for w in warnings)
    assert "not bolded" in md


def test_paired_test_for_other_configs_is_not_used(tmp_path):
    data = _summary()
    data["paired"]["accuracy"]["configs"] = ["baseline", "no_aux"]  # not best vs second
    p = tmp_path / "summary_wrongpair.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    md, warnings = tables.ablation_table(
        p, ["accuracy"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert "**" not in md
    assert any("not ours vs no_aux" in w for w in warnings)


# --------------------------------------------------------------------------
# refusal instead of placeholders
# --------------------------------------------------------------------------
def test_missing_metric_raises_with_available_names(summary_file):
    with pytest.raises(ValueError) as exc:
        tables.ablation_table(summary_file, ["f1_macro"], ["baseline"], fmt="md")
    msg = str(exc.value)
    assert "f1_macro" in msg
    assert "available metrics" in msg
    assert "accuracy" in msg


def test_missing_config_raises(summary_file):
    with pytest.raises(ValueError) as exc:
        tables.ablation_table(summary_file, ["accuracy"], ["baseline", "ghost"], fmt="md")
    assert "ghost" in str(exc.value)
    assert "no data for metric" in str(exc.value)


def test_missing_stats_and_values_raises(tmp_path):
    data = _summary()
    data["stats"]["accuracy"]["ours"] = {}  # no mean, and per_run is ignored? no:
    data["per_run"]["accuracy"]["ours"] = []  # no values either
    p = tmp_path / "summary_broken.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        tables.ablation_table(p, ["accuracy"], ["baseline", "ours"], fmt="md")
    assert "refusing" in str(exc.value)


def test_missing_file_raises(tmp_path):
    with pytest.raises(ValueError):
        tables.ablation_table(tmp_path / "nope.json", ["accuracy"], ["baseline"])


def test_bad_fmt_raises(summary_file):
    with pytest.raises(ValueError):
        tables.ablation_table(summary_file, ["accuracy"], ["baseline"], fmt="csv")


def test_small_n_warns(tmp_path):
    data = _summary()
    data["per_run"]["accuracy"]["ours"] = [0.90, 0.91, 0.92]
    data["stats"]["accuracy"]["ours"] = {"mean": 0.91, "std": 0.01, "n": 3}
    p = tmp_path / "summary_small.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    _, warnings = tables.ablation_table(
        p, ["accuracy"], ["baseline", "ours", "no_aux"], fmt="md"
    )
    assert any("n=3 < 5" in w for w in warnings)
