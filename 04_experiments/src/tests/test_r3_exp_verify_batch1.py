"""Unit tests for r3_exp_verify_batch1.

Two halves:
- synthetic: the pure check helpers (check_numeric, check_equal,
  interval_contains, summarise) on hand-built values;
- live: M.build_result() in-process, asserting every headline check passes
  against the committed on-disk files (auroc_ci / audit_twosided /
  ptruth_summary / both_runs / h2_verdict / r4_robustness vs the stored
  c1 + c1_corrected results_full.json, rung5.json and transfer.json).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_exp_verify_batch1 as M  # noqa: E402

OUT = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "verify_batch1.json"


# ---------- pure helpers (synthetic) ----------
def test_check_numeric_pass_and_fail():
    ok = M.check_numeric(0.98236, 0.9824, M.TOL_4DP)
    assert ok["status"] == "PASS"
    assert ok["diff"] <= M.TOL_4DP
    bad = M.check_numeric(0.5, 0.9, M.TOL_4DP)
    assert bad["status"] == "FAIL"
    miss = M.check_numeric(None, 0.5, M.TOL_4DP)
    assert miss["status"] == "FAIL"
    assert miss["diff"] is None


def test_check_numeric_exact():
    assert M.check_numeric(0.8925, 0.8925, M.TOL_EXACT)["status"] == "PASS"
    assert M.check_numeric(0.8925, 0.8926, M.TOL_EXACT)["status"] == "FAIL"


def test_check_equal():
    assert M.check_equal(True, True)["status"] == "PASS"
    assert M.check_equal(True, False)["status"] == "FAIL"
    assert M.check_equal("UNDEFINED", "UNDEFINED")["status"] == "PASS"
    assert M.check_equal(553, 553)["status"] == "PASS"
    assert M.check_equal(553, 552)["status"] == "FAIL"


def test_interval_contains():
    ci = {"lo": 0.0950, "hi": 0.1227}
    assert M.interval_contains(ci, 0.0950, 0.1227, M.TOL_4DP) is True
    assert M.interval_contains(ci, 0.10, 0.12, M.TOL_4DP) is False
    assert M.interval_contains({"lo": None, "hi": 0.12}, 0.095, 0.1227) is False
    assert M.interval_contains({}, 0.095, 0.1227) is False


def test_summarise():
    checks = [
        {"group": "a", "status": "PASS"},
        {"group": "a", "status": "PASS"},
        {"group": "b", "status": "FAIL"},
    ]
    s = M.summarise(checks)
    assert s["n_checks"] == 3 and s["n_pass"] == 2 and s["n_fail"] == 1
    assert s["overall"] == "FAIL"
    assert s["groups"]["a"]["n_pass"] == 2
    allp = M.summarise([{"group": "a", "status": "PASS"}])
    assert allp["overall"] == "PASS"


# ---------- live data (in-process re-check) ----------
def test_overall_pass_and_count():
    res = M.build_result()
    assert res["overall"] == "PASS", [
        c for c in res["checks"] if c["status"] != "PASS"]
    assert res["n_fail"] == 0
    assert res["n_checks"] >= 31
    assert res["n_pass"] == res["n_checks"]


@pytest.mark.parametrize("check_id,expected", [
    ("frozen_test_auroc_vs_stored_0.9824", 0.9824),
    ("corrected_test_auroc_vs_stored_0.8738", 0.8738),
    ("paired_diff_vs_0.1085", 0.1085),
    ("r4_primary6_dev_0.407", 0.407),
    ("top1_withlex_dev_0.7156", 0.7156),
    ("top1_withlex_test_0.7381", 0.7381),
    ("gold_indicator_1.0_all_cells", 1.0),
    ("auroc_0.2317", 0.2317),
    ("frozen_rung5_exploratory_0.8925", 0.8925),
    ("corrected_rung5_exploratory_0.9375", 0.9375),
    ("frozen_transfer_exploratory_0.855", 0.855),
    ("corrected_transfer_exploratory_0.975", 0.975),
    ("frozen_transfer_auroc_0.6402", 0.6402),
    ("corrected_transfer_auroc_0.7059", 0.7059),
    ("frozen_exploratory_7.25pp", 7.25),
    ("corrected_exploratory_-2.0pp", -2.0),
    ("registered_exploratory_0.8471", 0.8471),
    ("corrected_exploratory_0.1253", 0.1253),
])
def test_headline_checks(check_id, expected):
    res = M.build_result()
    by_id = {c["check_id"]: c for c in res["checks"]}
    assert by_id[check_id]["status"] == "PASS", by_id[check_id]
    assert by_id[check_id]["expected"] == pytest.approx(expected)


def test_h2_verdict_strings():
    res = M.build_result()
    by_id = {c["check_id"]: c for c in res["checks"]}
    assert by_id["frozen_exploratory_UNDEFINED"]["status"] == "PASS"
    assert by_id["corrected_exploratory_REFUTED"]["status"] == "PASS"
    assert by_id["frozen_confirmatory_REFUTED"]["status"] == "PASS"
    assert by_id["corrected_confirmatory_REFUTED"]["status"] == "PASS"


def test_main_writes_json(tmp_path):
    out = tmp_path / "verify_batch1.json"
    assert M.main(argv=["--out", str(out)]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["overall"] == "PASS"
    assert data["command"] == "python 04_experiments/src/r3_exp_verify_batch1.py"
    assert "checks" in data and len(data["checks"]) >= 31
    assert "inputs" in data and "sha256_inputs" in data
