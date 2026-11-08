"""Unit tests for r3_metrics_intervals (MF-16, MF-18, MF-21)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_metrics_intervals as M


@pytest.fixture(scope="module")
def intervals_data():
    M.main()
    out = ROOT / "04_experiments" / "results" / "c1" / "r3" / "metrics" / "intervals.json"
    return json.loads(out.read_text(encoding="utf-8"))


def test_clopper_pearson_upper_0_of_400():
    ci = M.clopper_pearson(0, 400)
    assert ci["lo"] == 0.0
    assert ci["hi"] == 0.0092
    assert ci["method"] == "clopper_pearson_exact_binomial"


def test_clopper_pearson_upper_0_of_1479():
    ci = M.clopper_pearson(0, 1479)
    assert ci["lo"] == 0.0
    assert ci["hi"] == 0.0025
    assert ci["method"] == "clopper_pearson_exact_binomial"


def test_clopper_pearson_upper_independent_scipy():
    from scipy.stats import binomtest

    hi_400 = binomtest(0, 400).proportion_ci(confidence_level=0.95, method="exact").high
    hi_1479 = binomtest(0, 1479).proportion_ci(confidence_level=0.95, method="exact").high
    assert round(float(hi_400), 4) == 0.0092
    assert round(float(hi_1479), 4) == 0.0025


def test_method_mismatch_detection(intervals_data):
    mc = intervals_data["interval_method_check"]
    assert mc["mismatch"] is True
    assert mc["mismatched_rungs"] == ["1", "3", "4"]
    assert mc["paper_stated_method"] == "bca"
    assert mc["archive_per_rung_method"]["2"] == "bca"


def test_equivalence_ci_contains_excludes_zero(intervals_data):
    eq = intervals_data["equivalence"]
    nodense = eq["all_12_vs_no_dense"]
    denseonly = eq["all_12_vs_dense_only"]
    frozen = eq["frozen_vs_corrected"]

    assert nodense["contains_zero"] is False
    assert not (nodense["lo"] <= 0 <= nodense["hi"])

    assert denseonly["contains_zero"] is True
    assert denseonly["lo"] <= 0 <= denseonly["hi"]

    assert frozen["contains_zero"] is False
    assert not (frozen["lo"] <= 0 <= frozen["hi"])


def test_main_writes_required_keys(intervals_data):
    d = intervals_data
    assert d["command"] == "python 04_experiments/src/r3_metrics_intervals.py"
    assert d["seed"] == 12345
    assert "inputs" in d
    assert d["H1"]["clopper_pearson"]["hi"] == 0.0092
    assert d["H3"]["clopper_pearson"]["hi"] == 0.0025
    assert "interval_method_check" in d
    assert "equivalence" in d