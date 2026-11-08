"""Unit tests for r3_metrics_h3 (MF-19, MF-20, MF-29)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_metrics_h3 as M
import gate as G


@pytest.fixture(scope="module")
def h3_data():
    rc = M.main()
    assert rc == 0
    out = ROOT / "04_experiments" / "results" / "c1" / "r3" / "metrics" / "h3.json"
    return json.loads(out.read_text(encoding="utf-8"))


def test_degenerate_equality_check_false(h3_data):
    deg = h3_data["degenerate_check"]
    assert deg["equal"] is False
    assert deg["single_matched_recall_t"] != deg["band_t_lo"]


def test_constrained_search_returns_no_feasible_threshold(h3_data):
    cs = h3_data["constrained_search"]
    assert cs["constrained_threshold_exists"] is False
    assert cs["max_feasible_recall"] < cs["target_recall"]


def test_degenerate_equality_independent():
    items = [it for it in M.load_items()
             if it["item_id"] in G.load_features(ROOT / "04_experiments" / "data" / "features_corrected.csv")]
    feats = G.load_features(ROOT / "04_experiments" / "data" / "features_corrected.csv")
    items = [it for it in items if it["item_id"] in feats]
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    y_dev = np.asarray([feats[i]["label"] for i in dev_ids], dtype=int)
    gate = G.fit_logistic_gate(feats, dev_ids)
    s_dev = gate.score(feats, dev_ids)
    band = G.fit_band_thresholds(s_dev, y_dev)
    matched = G.match_single_to_recall(s_dev, y_dev, float(band["dev_recall"]))
    assert matched["t"] != band["t_lo"]


def test_constrained_search_independent():
    items = [it for it in M.load_items()
             if it["item_id"] in G.load_features(ROOT / "04_experiments" / "data" / "features_corrected.csv")]
    feats = G.load_features(ROOT / "04_experiments" / "data" / "features_corrected.csv")
    items = [it for it in items if it["item_id"] in feats]
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    y_dev = np.asarray([feats[i]["label"] for i in dev_ids], dtype=int)
    gate = G.fit_logistic_gate(feats, dev_ids)
    s_dev = gate.score(feats, dev_ids)
    band = G.fit_band_thresholds(s_dev, y_dev)
    target_recall = float(band["dev_recall"])
    neg_dev = int((y_dev == 0).sum())
    feasible = []
    for t in sorted(set(s_dev.tolist())):
        refused = s_dev < t
        nref = int(refused.sum())
        if nref == 0:
            continue
        tp = int(refused[y_dev == 0].sum())
        prec = tp / nref
        rec = tp / max(1, neg_dev)
        if prec >= 0.80 and rec >= target_recall:
            feasible.append(float(t))
    assert feasible == []


def test_main_writes_required_keys(h3_data):
    d = h3_data
    assert d["command"] == "python 04_experiments/src/r3_metrics_h3.py"
    assert d["seed"] == 12345
    assert "constrained_search" in d
    assert "degenerate_check" in d
    assert d["constrained_search"]["constrained_threshold_exists"] is False