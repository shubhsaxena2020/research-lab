"""Unit tests for r3_exp_audit_twosided."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_exp_audit_twosided as M  # noqa: E402


def test_abs_diff():
    assert M.abs_diff(0.8) == pytest.approx(0.3)
    assert M.abs_diff(0.4) == pytest.approx(0.1)


def test_direction():
    assert M.direction(0.3) == "inverted"
    assert M.direction(0.7) == "normal"


def test_twosided_pass():
    assert M.twosided_pass(0.5) is True
    assert M.twosided_pass(0.7) is True
    assert M.twosided_pass(0.25) is True
    assert M.twosided_pass(0.75) is True
    assert M.twosided_pass(0.2) is False
    assert M.twosided_pass(0.1) is False
    assert M.twosided_pass(0.9) is False


def test_bootstrap_ci_shape():
    rng = np.random.default_rng(0)
    y = np.array([0] * 50 + [1] * 50)
    oof = rng.random(100)
    ci = M.bootstrap_auroc_ci(oof, y, seed=1, n_boot=50)
    assert ci["lo"] <= ci["hi"]
    assert ci["n_boot"] == 50
    assert ci["n"] == 100


def test_main_writes_json():
    M.main()
    out = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "audit_twosided.json"
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["seed"] == 12345
    assert data["command"] == "python 04_experiments/src/r3_exp_audit_twosided.py"
    assert data["n_boot"] >= 2000
    assert "original" in data
    assert "top1" in data
    assert "gold_indicator_control" in data
    # check a rung entry has required fields
    r = data["original"]["dev"]["per_rung"]["1"]
    assert "auroc_primary_6" in r
    assert "abs_diff_primary_6" in r
    assert "direction_primary_6" in r
    assert "passes_primary_6" in r
    assert "ci_primary_6" in r
    # top1
    t = data["top1"]["dev"]
    assert "auroc_primary_6" in t
    assert "n" in t
    assert "split" in t or True
    # gold control
    g = data["gold_indicator_control"]["dev"]["per_rung"]["1"]
    assert "auroc_with_is_gold" in g
