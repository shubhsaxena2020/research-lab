"""Unit tests for r3_exp_h2_verdict (synthetic + stored-value checks)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_exp_h2_verdict as M  # noqa: E402

OUT = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "h2_verdict.json"


def test_verdict_for_loss_pp():
    assert M.verdict_for_loss_pp(10.0) == "SUPPORTED"
    assert M.verdict_for_loss_pp(15.0) == "SUPPORTED"
    assert M.verdict_for_loss_pp(5.0) == "REFUTED"
    assert M.verdict_for_loss_pp(-5.0) == "REFUTED"
    assert M.verdict_for_loss_pp(0.0) == "REFUTED"
    assert M.verdict_for_loss_pp(1.5) == "REFUTED"
    assert M.verdict_for_loss_pp(-2.0) == "REFUTED"
    # The 5-10 gap is undefined under the preregistered binary rule.
    assert M.verdict_for_loss_pp(7.25) == "UNDEFINED"
    assert M.verdict_for_loss_pp(6.0) == "UNDEFINED"
    assert M.verdict_for_loss_pp(9.99) == "UNDEFINED"
    # A gain steeper than -5 is likewise unclassified by the +/-5 rule.
    assert M.verdict_for_loss_pp(-6.0) == "UNDEFINED"


def test_drop_pp():
    assert M.drop_pp(0.9275, 0.855) == pytest.approx(7.25, abs=1e-9)
    assert M.drop_pp(0.955, 0.975) == pytest.approx(-2.0, abs=1e-9)
    assert M.drop_pp(1.0, 0.985) == pytest.approx(1.5, abs=1e-9)
    assert M.drop_pp(1.0, 1.0) == pytest.approx(0.0, abs=1e-9)


def test_verdict_block_flags_unequal_recall():
    blk = M.verdict_block(
        main_rung3=0.9275,
        transfer_rung3=0.855,
        over_refusal_main=0.095,
        over_refusal_transfer=0.575,
        main_auroc=0.9836,
        transfer_auroc=0.6402,
    )
    assert blk["verdict"] == "UNDEFINED"
    assert blk["drop_pp"] == pytest.approx(7.25, abs=1e-9)
    assert blk["main_recall_at_frozen_thresholds"] == pytest.approx(0.9275, abs=1e-9)
    assert blk["transfer_recall_at_frozen_thresholds"] == pytest.approx(0.855, abs=1e-9)
    assert blk["equal_recall_check"]["holds"] is False
    assert blk["equal_recall_check"]["abs_recall_gap_pp"] == pytest.approx(7.25, abs=1e-9)


def test_table_values_match_stored():
    data = M.build_result()
    tbl = data["table"]
    # frozen: confirmatory 1.5pp REFUTED; exploratory 7.25pp UNDEFINED
    assert tbl["frozen"]["confirmatory_drop_pp"] == pytest.approx(1.5, abs=1e-9)
    assert tbl["frozen"]["confirmatory_verdict"] == "REFUTED"
    assert tbl["frozen"]["exploratory_drop_pp"] == pytest.approx(7.25, abs=1e-9)
    assert tbl["frozen"]["exploratory_verdict"] == "UNDEFINED"
    # corrected: confirmatory 0.0pp REFUTED; exploratory -2.0pp (gain) REFUTED
    assert tbl["corrected"]["confirmatory_drop_pp"] == pytest.approx(0.0, abs=1e-9)
    assert tbl["corrected"]["confirmatory_verdict"] == "REFUTED"
    assert tbl["corrected"]["exploratory_drop_pp"] == pytest.approx(-2.0, abs=1e-9)
    assert tbl["corrected"]["exploratory_verdict"] == "REFUTED"


def test_recall_and_over_refusal_pairs():
    data = M.build_result()
    expected = {
        ("frozen", "confirmatory"): (1.0, 0.985, 0.755, 0.895, 0.6402),
        ("frozen", "exploratory"): (0.9275, 0.855, 0.095, 0.575, 0.6402),
        ("corrected", "confirmatory"): (1.0, 1.0, 0.915, 0.965, 0.7059),
        ("corrected", "exploratory"): (0.955, 0.975, 0.11, 0.7, 0.7059),
    }
    for (run_name, op), (main_p, tr_p, or_main, or_tr, tr_auroc) in expected.items():
        blk = data["runs"][run_name][op]
        assert blk["main_test_rung3_precision"] == pytest.approx(main_p, abs=1e-9)
        assert blk["transfer_rung3_precision"] == pytest.approx(tr_p, abs=1e-9)
        assert blk["main_recall_at_frozen_thresholds"] == pytest.approx(main_p, abs=1e-9)
        assert blk["transfer_recall_at_frozen_thresholds"] == pytest.approx(tr_p, abs=1e-9)
        assert blk["over_refusal_main"] == pytest.approx(or_main, abs=1e-9)
        assert blk["over_refusal_transfer"] == pytest.approx(or_tr, abs=1e-9)
        assert blk["transfer_auroc_answerable_vs_rung3"] == pytest.approx(tr_auroc, abs=1e-4)
        assert blk["stored_drop_matches"] is True
        assert blk["results_full_over_refusal_matches"] is True
    # Confirmatory frozen and corrected operate at (near-)equal recall; the
    # exploratory arms do not (gap 7.25pp frozen, 2pp corrected).
    assert data["runs"]["frozen"]["confirmatory"]["equal_recall_check"]["holds"] is False
    assert data["runs"]["corrected"]["confirmatory"]["equal_recall_check"]["holds"] is True


def test_verbatim_and_gap_interpretation():
    data = M.build_result()
    verbatim = data["h2_verbatim"]
    assert "loses ≥ 10 points of abstain precision at" in verbatim
    assert "equal abstain recall" in verbatim
    assert "Refuted if" in verbatim
    assert "within ±5 points" in verbatim
    assert data["gap_interpretation"]["h2_verbatim"] == verbatim
    assert "binary" in data["gap_interpretation"]["gap_rule"].lower()
    assert data["exploratory"] is True
    assert data["post_hoc"] is True


def test_main_writes_json(tmp_path):
    out = tmp_path / "h2_verdict.json"
    assert M.main(argv=["--out", str(out)]) == 0
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["command"] == "python 04_experiments/src/r3_exp_h2_verdict.py"
    assert data["exploratory"] is True
    assert data["post_hoc"] is True
    assert set(data["table"].keys()) == {"frozen", "corrected"}
    for run_name in ("frozen", "corrected"):
        for op in ("confirmatory", "exploratory"):
            blk = data["runs"][run_name][op]
            for field in (
                "main_test_rung3_precision",
                "transfer_rung3_precision",
                "main_recall_at_frozen_thresholds",
                "transfer_recall_at_frozen_thresholds",
                "over_refusal_main",
                "over_refusal_transfer",
                "drop_points",
                "drop_pp",
                "direction",
                "transfer_auroc_answerable_vs_rung3",
                "equal_recall_check",
                "verdict",
            ):
                assert field in blk, (run_name, op, field)
    assert data["inputs"] and data["sha256_inputs"]
