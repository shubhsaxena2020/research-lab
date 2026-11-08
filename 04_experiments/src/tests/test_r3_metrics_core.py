"""Targeted tests for r3_metrics_core (R3-1)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_metrics_core as M  # noqa: E402

METRICS_DIR = ROOT / "04_experiments" / "results" / "c1" / "r3" / "metrics"


def test_handmade_10row_fixture_metrics():
    # 2 answerable rung-0 items + 8 negatives across rungs 1-4 (2 qids x 5 rungs).
    rows = [
        {"qid": "Q1", "rung": "0", "refused": "0"},
        {"qid": "Q1", "rung": "1", "refused": "1"},
        {"qid": "Q1", "rung": "2", "refused": "0"},
        {"qid": "Q1", "rung": "3", "refused": "1"},
        {"qid": "Q1", "rung": "4", "refused": "1"},
        {"qid": "Q2", "rung": "0", "refused": "1"},
        {"qid": "Q2", "rung": "1", "refused": "1"},
        {"qid": "Q2", "rung": "2", "refused": "1"},
        {"qid": "Q2", "rung": "3", "refused": "0"},
        {"qid": "Q2", "rung": "4", "refused": "1"},
    ]
    col = "refused"

    # Hand-computed inputs.
    n_refused_answerable = 1  # Q2 rung-0
    n_refused_by_rung = {"1": 2, "2": 1, "3": 1, "4": 2}
    n_by_rung = {"1": 2, "2": 2, "3": 2, "4": 2}
    total_refused_neg = 6
    total_items = 10
    total_refused = 7

    point = M.compute_point(rows, col)

    # refusal_rate (answerable / over-refusal)
    assert point["answerable"]["refusal_rate"] == pytest.approx(
        M.refusal_rate_k(n_refused_answerable, 2)
    )
    assert point["answerable"]["refusal_rate"] == pytest.approx(0.5)

    # per-rung refusal_rate and precision
    for k in ("1", "2", "3", "4"):
        assert point["per_rung"][k]["refusal_rate"] == pytest.approx(
            M.refusal_rate_k(n_refused_by_rung[k], n_by_rung[k])
        )
        assert point["per_rung"][k]["abstain_precision"] == pytest.approx(
            M.precision_k(n_refused_by_rung[k], n_refused_answerable)
        )

    assert point["per_rung"]["1"]["refusal_rate"] == pytest.approx(1.0)
    assert point["per_rung"]["1"]["abstain_precision"] == pytest.approx(2 / 3)
    assert point["per_rung"]["2"]["refusal_rate"] == pytest.approx(0.5)
    assert point["per_rung"]["2"]["abstain_precision"] == pytest.approx(0.5)
    assert point["per_rung"]["3"]["refusal_rate"] == pytest.approx(0.5)
    assert point["per_rung"]["3"]["abstain_precision"] == pytest.approx(0.5)
    assert point["per_rung"]["4"]["refusal_rate"] == pytest.approx(1.0)
    assert point["per_rung"]["4"]["abstain_precision"] == pytest.approx(2 / 3)

    # pooled precision
    assert point["pooled"]["pooled_abstain_precision"] == pytest.approx(
        M.pooled_precision(total_refused_neg, n_refused_answerable)
    )
    assert point["pooled"]["pooled_abstain_precision"] == pytest.approx(6 / 7)

    # coverage_item
    refused_flags = [1 if r[col] == "1" else 0 for r in rows]
    assert point["coverage_item"] == pytest.approx(M.coverage_item(refused_flags))
    assert point["coverage_item"] == pytest.approx(1.0 - total_refused / total_items)
    assert point["coverage_item"] == pytest.approx(0.3)

    # coverage_question
    cq, n_answered, n_qids = M.coverage_question(rows, col)
    assert point["coverage_question"] == pytest.approx(cq)
    assert point["coverage_question_n_answered"] == n_answered
    assert point["coverage_question_n_qids"] == n_qids
    assert cq == pytest.approx(0.5)
    assert n_answered == 1
    assert n_qids == 2


def test_definitions_md_required_definitions_present():
    defs_path = METRICS_DIR / "DEFINITIONS.md"
    assert defs_path.is_file(), f"missing {defs_path}"
    text = defs_path.read_text(encoding="utf-8").lower()
    for term in (
        "abstain precision",
        "refusal rate",
        "over-refusal",
        "coverage",
        "abstain recall",
    ):
        assert term in text, f"required definition missing: {term}"


def test_metrics_json_frozen_and_corrected():
    metrics_path = METRICS_DIR / "metrics.json"
    assert metrics_path.is_file(), f"missing {metrics_path}"
    data = json.loads(metrics_path.read_text(encoding="utf-8"))

    # Support both {"runs": {"frozen":..., "corrected":...}} and top-level keys.
    if "runs" in data and isinstance(data["runs"], dict):
        frozen = data["runs"].get("frozen")
        corrected = data["runs"].get("corrected")
    else:
        frozen = data.get("frozen")
        corrected = data.get("corrected")

    assert frozen is not None, "metrics.json missing frozen run"
    assert corrected is not None, "metrics.json missing corrected run"

    for run in (frozen, corrected):
        # operating points may be nested under operating_points
        if "operating_points" in run and isinstance(run["operating_points"], dict):
            points = run["operating_points"]
        elif "operating points" in run:
            points = run["operating points"]
        else:
            points = run
        assert isinstance(points, dict) and points, "no operating points found"
        for name, point in points.items():
            if not isinstance(point, dict):
                continue
            if "per_rung" not in point:
                continue
            per_rung = point["per_rung"]
            assert isinstance(per_rung, dict) and per_rung, f"empty per_rung in {name}"
            for rung, vals in per_rung.items():
                assert "refusal_rate" in vals, f"missing refusal_rate for rung {rung}"
                assert "abstain_precision" in vals, f"missing precision for rung {rung}"