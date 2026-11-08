"""Unit tests for r3_exp_both_runs (synthetic + structure checks)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_exp_both_runs as M  # noqa: E402

OUT = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "both_runs.json"


def test_compute_point():
    scores = np.array([0.1, 0.2, 0.9, 0.95])
    pt = M.compute_point(scores, t_lo=0.3, t_hi=0.8)
    # refused = score<0.3 or >0.8 -> all 4
    assert pt["abstain_precision"] == pytest.approx(1.0)
    assert pt["n"] == 4
    assert pt["n_refused"] == 4
    pt2 = M.compute_point(np.array([0.5, 0.6]), t_lo=0.3, t_hi=0.8)
    assert pt2["abstain_precision"] == pytest.approx(0.0)
    assert pt2["n_refused"] == 0


def test_auroc():
    pos = np.array([0.9, 0.8])
    neg = np.array([0.1, 0.2])
    assert M.auroc_answerable_vs_neg(pos, neg) == pytest.approx(1.0, abs=1e-4)
    assert M.auroc_answerable_vs_neg(neg, pos) == pytest.approx(0.0, abs=1e-4)


def test_match_bool():
    assert M.match_bool(0.8925, 0.8925) is True
    assert M.match_bool(0.8925, 0.9000) is False
    assert M.match_bool(None, 0.5) is None


def test_table_values_match_expected_rederived():
    # Expected recomputed values (verified by running gate.fit_logistic_gate
    # on dev features and applying thresholds from results_full.json).
    data = M.build_result()
    tbl = data["table"]
    # frozen
    assert tbl["frozen"]["rung5_confirmatory_test"] == pytest.approx(1.0, abs=1e-9)
    assert tbl["frozen"]["rung5_exploratory_test"] == pytest.approx(0.8925, abs=1e-9)
    assert tbl["frozen"]["rung5_auroc"] == pytest.approx(0.9736, abs=1e-4)
    assert tbl["frozen"]["transfer_confirmatory_rung3"] == pytest.approx(0.985, abs=1e-9)
    assert tbl["frozen"]["transfer_exploratory_rung3"] == pytest.approx(0.855, abs=1e-9)
    assert tbl["frozen"]["transfer_auroc"] == pytest.approx(0.6402, abs=1e-4)
    # corrected
    assert tbl["corrected"]["rung5_confirmatory_test"] == pytest.approx(0.9975, abs=1e-9)
    assert tbl["corrected"]["rung5_exploratory_test"] == pytest.approx(0.9375, abs=1e-9)
    assert tbl["corrected"]["rung5_auroc"] == pytest.approx(0.9728, abs=1e-4)
    assert tbl["corrected"]["transfer_confirmatory_rung3"] == pytest.approx(1.0, abs=1e-9)
    assert tbl["corrected"]["transfer_exploratory_rung3"] == pytest.approx(0.975, abs=1e-9)
    assert tbl["corrected"]["transfer_auroc"] == pytest.approx(0.7059, abs=1e-4)


def test_comparison_matches_stored():
    data = M.build_result()
    for run_name in ("frozen", "corrected"):
        run = data["runs"][run_name]
        assert run["all_match_stored"] is True, run_name
        r5 = run["rung5"]
        assert r5["comparison"]["test"]["confirmatory_band"]["match"] is True
        assert r5["comparison"]["test"]["exploratory_band"]["match"] is True
        assert r5["comparison"]["auroc"]["match"] is True
        tr = run["transfer"]
        assert tr["operating_points"]["confirmatory_band"]["match_rung3_precision"] is True
        assert tr["operating_points"]["exploratory_band"]["match_rung3_precision"] is True
        assert tr["operating_points"]["confirmatory_band"]["match_auroc"] is True
        assert tr["operating_points"]["exploratory_band"]["match_auroc"] is True


def test_main_writes_json(tmp_path):
    out = tmp_path / "both_runs.json"
    assert M.main(argv=["--out", str(out)]) == 0
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["command"] == "python 04_experiments/src/r3_exp_both_runs.py"
    assert data["exploratory"] is True
    assert "table" in data
    assert "runs" in data and "frozen" in data["runs"] and "corrected" in data["runs"]
    assert "inputs" in data and "sha256_inputs" in data
    # threshold values from results_full.json
    f = data["runs"]["frozen"]["thresholds"]
    assert f["confirmatory_band"]["t_lo"] == pytest.approx(0.90722098925, abs=1e-12)
    assert f["exploratory_band"]["t_lo"] == pytest.approx(0.297426271744, abs=1e-12)
    c = data["runs"]["corrected"]["thresholds"]
    assert c["confirmatory_band"]["t_lo"] == pytest.approx(0.52318216643, abs=1e-12)
    assert c["exploratory_band"]["t_lo"] == pytest.approx(0.303228201895, abs=1e-12)
