"""Unit tests for the R3-exp AUROC bootstrap CIs.

Synthetic data only; no heavy model jobs. Tests cover the pure bootstrap
helpers: single AUROC CI and the paired differences CI.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import r3_exp_auroc_ci as M


def _synth(n_pos=50, n_neg=50, rng_seed=12345):
    rng = np.random.default_rng(rng_seed)
    y = np.concatenate([np.ones(n_pos, dtype=int), np.zeros(n_neg, dtype=int)])
    # positives get higher scores with overlap
    scores = np.concatenate([rng.normal(1.0, 0.5, n_pos), rng.normal(0.0, 0.5, n_neg)])
    return y, scores


# ---------- single bootstrap AUROC CI ----------
def test_bootstrap_auroc_ci_perfect_separation_near_one():
    y = np.concatenate([np.ones(30, dtype=int), np.zeros(30, dtype=int)])
    scores = np.concatenate([np.linspace(2, 3, 30), np.linspace(0, 1, 30)])
    out = M.bootstrap_auroc_ci(y, scores, n_boot=500, seed=12345)
    assert abs(out["point"] - 1.0) < 1e-9
    assert out["lo"] <= 1.0 <= out["hi"] or abs(out["point"] - 1.0) < 1e-9
    assert out["n"] == 60
    assert out["n_boot"] == 500
    assert out["seed"] == 12345
    assert out["method"] == "percentile"
    assert out["level"] == "item"
    assert out["post_hoc"] is True


def test_bootstrap_auroc_ci_random_scores_around_half():
    y, scores = _synth(n_pos=200, n_neg=200)
    out = M.bootstrap_auroc_ci(y, scores, n_boot=500, seed=12345)
    # strong signal in _synth: point well above 0.5, near 0.9
    assert 0.8 <= out["point"] <= 0.99
    assert out["lo"] <= out["hi"]
    assert out["hi"] - out["lo"] > 0.0

    # null scores (same distribution) -> AUROC near 0.5
    rng = np.random.default_rng(12345)
    y0 = np.concatenate([np.ones(200, dtype=int), np.zeros(200, dtype=int)])
    s0 = rng.standard_normal(400)
    out0 = M.bootstrap_auroc_ci(y0, s0, n_boot=500, seed=12345)
    assert abs(out0["point"] - 0.5) < 0.1


def test_bootstrap_auroc_ci_deterministic_same_seed():
    y, scores = _synth(n_pos=60, n_neg=60)
    a = M.bootstrap_auroc_ci(y, scores, n_boot=400, seed=12345)
    b = M.bootstrap_auroc_ci(y, scores, n_boot=400, seed=12345)
    assert a["point"] == b["point"]
    assert a["lo"] == b["lo"]
    assert a["hi"] == b["hi"]


def test_bootstrap_auroc_ci_cluster_level():
    rng = np.random.default_rng(12345)
    y = np.concatenate([np.ones(20, dtype=int), np.zeros(20, dtype=int)])
    scores = np.concatenate([rng.normal(1.0, 0.3, 20), rng.normal(0.0, 0.3, 20)])
    clusters = np.concatenate([["c1"] * 20, ["c2"] * 20])
    out = M.bootstrap_auroc_ci(y, scores, n_boot=300, seed=12345, cluster_ids=clusters)
    assert out["level"] == "cluster"
    assert out["method"] == "cluster_percentile"
    assert out["n_clusters"] == 2
    assert "lo" in out and "hi" in out


# ---------- paired diff CI ----------
def test_paired_diff_identical_scores_contains_zero():
    y, scores = _synth(n_pos=80, n_neg=80)
    out = M.paired_auroc_diff_ci(y, scores, scores, n_boot=1000, seed=12345)
    assert out["diff"] == 0.0
    assert out["lo"] == 0.0
    assert out["hi"] == 0.0
    assert out["contains_zero"] is True


def test_paired_diff_better_scores_positive_point():
    y, _ = _synth(n_pos=50, n_neg=50)
    rng = np.random.default_rng(12345)
    a = np.concatenate([rng.normal(1.0, 0.4, 50), rng.normal(0.0, 0.4, 50)])
    b = np.concatenate([rng.normal(0.3, 0.9, 50), rng.normal(0.2, 0.9, 50)])
    out = M.paired_auroc_diff_ci(y, a, b, n_boot=1000, seed=12345)
    assert out["diff"] > 0.0
    assert out["n"] == 100
    assert out["n_boot"] == 1000
    assert out["seed"] == 12345
    assert out["lo"] <= out["hi"]


def test_paired_diff_cluster_level():
    rng = np.random.default_rng(12345)
    y = np.concatenate([np.ones(25, dtype=int), np.zeros(25, dtype=int)])
    a = np.concatenate([rng.normal(1.0, 0.3, 25), rng.normal(0.0, 0.3, 25)])
    b = np.concatenate([rng.normal(1.0, 0.3, 25), rng.normal(0.0, 0.3, 25)])
    clusters = np.concatenate([["x"] * 25, ["y"] * 25])
    out = M.paired_auroc_diff_ci(y, a, b, n_boot=300, seed=12345, cluster_ids=clusters)
    assert out["level"] == "cluster"
    assert out["n_clusters"] == 2
