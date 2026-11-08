"""Unit tests for r3_exp_r4_robust (synthetic + live-data checks).

Synthetic half covers the pure helpers (rung-4 point, subsample, bootstrap
CI, rate summary). Live half runs M.build_result() in-process and asserts
the headline table against the stored results_full.json values
(84.71% vs 12.53% exploratory, 100% vs 90.73% confirmatory,
AUROC 0.9681 vs 0.5730) and the robustness design constants
(50% x 20 reps, seeds 999/2024).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_exp_r4_robust as M  # noqa: E402

OUT = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "r4_robustness.json"


# ---------- pure helpers (synthetic) ----------
def test_rung4_point_separation():
    # all refused except one answerable → high recall, high true precision
    pt = M.rung4_point(np.array([True] * 10), np.array([True]), None, None, None)
    assert pt["abstain_precision"] == pytest.approx(1.0)
    assert pt["true_precision"] == pytest.approx(0.9091, abs=1e-4)
    assert pt["n"] == 10 and pt["n_refused"] == 10

    pt2 = M.rung4_point(np.array([False, True]), np.array([False]), None, None, None)
    assert pt2["abstain_precision"] == pytest.approx(0.5)
    assert pt2["true_precision"] == pytest.approx(1.0)  # 1 refused rung4, 0 refused answerable


def test_auroc_helper():
    pos = np.array([0.9, 0.8, 0.7])
    neg = np.array([0.1, 0.2, 0.3])
    assert M.auroc_answerable_vs_rung4(pos, neg) == pytest.approx(1.0, abs=1e-4)
    assert M.auroc_answerable_vs_rung4(neg, pos) == pytest.approx(0.0, abs=1e-4)


def test_subsample_rates_deterministic_and_sized():
    refused = np.array([True] * 50 + [False] * 50)
    a = M.subsample_rates(refused, frac=0.5, n_reps=20, seed=999)
    b = M.subsample_rates(refused, frac=0.5, n_reps=20, seed=999)
    assert a == b
    assert len(a) == 20
    # half subsample of a 50/50 mix concentrates near 0.5
    assert all(0.3 <= r <= 0.7 for r in a)

    c = M.subsample_rates(refused, frac=0.5, n_reps=20, seed=2024)
    assert c != a  # different seed → different draw in general


def test_bootstrap_ci_shape_and_point():
    refused = np.array([True] * 80 + [False] * 20)
    ci = M.bootstrap_rate_ci(refused, n_boot=500, seed=999)
    assert ci["point"] == pytest.approx(0.8)
    assert ci["lo"] <= 0.8 <= ci["hi"]
    assert ci["n_boot"] == 500 and ci["n"] == 100
    assert ci["method"] == "percentile" and ci["seed"] == 999

    # deterministic across seeds at the point; LO/HI may differ
    ci2 = M.bootstrap_rate_ci(refused, n_boot=500, seed=999)
    assert ci["lo"] == ci2["lo"] and ci["hi"] == ci2["hi"]


def test_summarise_rates():
    s = M.summarise_rates([0.1, 0.2, 0.3])
    assert s["n_reps"] == 3
    assert s["mean"] == pytest.approx(0.2)
    assert s["min"] == pytest.approx(0.1) and s["max"] == pytest.approx(0.3)
    assert s["sd"] == pytest.approx(0.1)


# ---------- live data (in-process re-derivation) ----------
def test_table_values_match_stored():
    data = M.build_result()
    tbl = data["table"]
    # SUMMARY: registered 84.71% / corrected 12.53% exploratory,
    # registered 100% / corrected 90.73% confirmatory, AUROC 0.9681 / 0.5730
    assert tbl["registered"]["exploratory_rung4"] == pytest.approx(0.8471, abs=1e-9)
    assert tbl["corrected"]["exploratory_rung4"] == pytest.approx(0.1253, abs=1e-9)
    assert tbl["registered"]["confirmatory_rung4"] == pytest.approx(1.0, abs=1e-9)
    assert tbl["corrected"]["confirmatory_rung4"] == pytest.approx(0.9073, abs=1e-9)
    assert tbl["registered"]["auroc_rung4"] == pytest.approx(0.9681, abs=1e-4)
    assert tbl["corrected"]["auroc_rung4"] == pytest.approx(0.5730, abs=1e-4)
    assert tbl["gap_exploratory_registered_minus_corrected"] == pytest.approx(
        0.8471 - 0.1253, abs=1e-9)

    for run in ("registered", "corrected"):
        r = data["runs"][run]
        assert r["gate_assertion"]["passed"] is True
        assert r["confirmatory_matches_stored"] is True
        assert r["exploratory_matches_stored"] is True
        assert r["auroc_matches_stored"] is True
        assert r["n_answerable"] == 400
        assert r["n_rung4"] == 399

    assert data["exploratory"] is True
    assert data["post_hoc"] is True
    assert data["label"] == "exploratory/post-hoc"
    assert data["command"] == "python 04_experiments/src/r3_exp_r4_robust.py"
    assert "inputs" in data and "sha256_inputs" in data


def test_robustness_design_and_stability():
    data = M.build_result()
    d = data["design"]
    assert d["subsample_frac"] == pytest.approx(0.5)
    assert d["n_subsample_reps"] == 20
    assert d["subsample_seeds"] == [999, 2024]
    assert d["bootstrap_n"] == 2000
    assert d["bootstrap_seeds"] == [999, 2024]

    for run in ("registered", "corrected"):
        rob = data["runs"][run]["robustness"]
        assert rob["operating_point"] == "exploratory_band"
        for seed in ("999", "2024"):
            s = rob["subsample"][seed]
            assert s["n_reps"] == 20
            assert len(s["rates"]) == 20
            assert s["frac"] == pytest.approx(0.5)
            assert s["sample_n"] == 200 or s["sample_n"] == 199  # round(0.5*399)=200
            # mean close to full-sample point (subsample is unbiased)
            point = data["runs"][run]["exploratory_band"]["abstain_precision"]
            assert abs(s["mean"] - point) < 0.05
        for seed in ("999", "2024"):
            b = rob["bootstrap"][seed]
            assert b["n_boot"] == 2000
            assert b["lo"] <= b["point"] <= b["hi"]

    # gap stays large and positive in every subsample (both seeds)
    for seed in ("999", "2024"):
        g = data["stability"]["gap_by_subsample_seed"][seed]
        assert g["n_reps"] == 20
        assert g["min"] > 0.4  # worst subsample still far above zero
        assert g["mean"] == pytest.approx(0.8471 - 0.1253, abs=0.05)
    assert data["stability"]["gap_full_sample"] == pytest.approx(0.8471 - 0.1253, abs=1e-9)


def test_main_writes_json():
    M.main(argv=[])
    assert OUT.exists()
    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["command"] == "python 04_experiments/src/r3_exp_r4_robust.py"
    assert data["exploratory"] is True
    assert "table" in data and "runs" in data and "stability" in data
    assert "registered" in data["runs"] and "corrected" in data["runs"]
    # thresholds read from results_full.json, not refit here
    f = data["runs"]["registered"]["thresholds"]
    assert f["confirmatory_band"]["t_lo"] == pytest.approx(0.90722098925, abs=1e-12)
    assert f["exploratory_band"]["t_lo"] == pytest.approx(0.297426271744, abs=1e-12)
    c = data["runs"]["corrected"]["thresholds"]
    assert c["confirmatory_band"]["t_lo"] == pytest.approx(0.52318216643, abs=1e-12)
    assert c["exploratory_band"]["t_lo"] == pytest.approx(0.303228201895, abs=1e-12)
