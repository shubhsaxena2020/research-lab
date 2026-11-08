"""Unit tests for r3_metrics_rung2 (MF-22)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_metrics_rung2 as M  # noqa: E402


def test_shortfall_counts():
    items = M.load_items()
    import stats_addendum as SA
    ex = SA.exchangeability(items)
    assert ex["splits"]["test"]["n_kept"] == 280
    assert ex["splits"]["test"]["n_dropped"] == 120
    assert ex["splits"]["dev"]["n_kept"] == 273
    assert ex["splits"]["dev"]["n_dropped"] == 127


def test_json_written_with_required_keys(tmp_path, monkeypatch):
    # run main in-process; it writes to canonical paths
    M.main()
    out = ROOT / "04_experiments" / "results" / "c1" / "r3" / "metrics" / "rung2.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["n_kept"] == 280
    assert data["n_dropped"] == 120
    assert set(data["p_values"]["dev"]) == {"q_chars", "q_tokens", "gold_chars", "n_paragraphs", "answer_type"}
    assert set(data["p_values"]["test"]) == {"q_chars", "q_tokens", "gold_chars", "n_paragraphs", "answer_type"}
    assert "verdict" in data
    assert data["command"] == "python 04_experiments/src/r3_metrics_rung2.py"
    assert data["seed"] == 12345
    assert "inputs" in data
