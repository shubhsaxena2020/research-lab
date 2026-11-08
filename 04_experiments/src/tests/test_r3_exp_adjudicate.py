"""Unit tests for r3_exp_adjudicate (synthetic + live-data checks).

Synthetic half covers the pure helpers (stratified sampling, Cohen's
kappa, agreement report). Live half runs the sampler on the real
items.jsonl and asserts the 25-per-rung / 100-total / negatives-only
invariants and that the deterministic sample reproduces; it also checks
that --kappa refuses to compute on the blank label templates.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import r3_exp_adjudicate as M  # noqa: E402

ITEMS = M.load_items_jsonl(M.ITEMS_PATH)


def _synthetic_items():
    items = []
    for rung in (1, 2, 3, 4):
        for i in range(40):
            items.append({
                "item_id": f"synth:r{rung}:{i:03d}",
                "label": 0,
                "rung": rung,
                "split": "dev",
                "question": "q?",
                "context": "ctx",
                "gold_answer": None,
            })
    # positives / wrong labels must never be sampled
    for rung in (0, 1, 2, 3, 4):
        for i in range(5):
            items.append({
                "item_id": f"synth:pos:r{rung}:{i}",
                "label": 1,
                "rung": rung,
                "split": "dev",
                "question": "q?",
                "context": "ctx",
                "gold_answer": "ans",
            })
    return items


# ---------- sampling (synthetic) ----------
def test_sample_stratified_25_per_rung_and_negatives_only():
    drawn = M.sample_negatives(_synthetic_items())
    counts = {}
    for it in drawn:
        counts[it["rung"]] = counts.get(it["rung"], 0) + 1
        assert it["label"] == 0 and it["rung"] >= 1
    assert counts == {1: 25, 2: 25, 3: 25, 4: 25}
    assert len(drawn) == 100

    # deterministic and order-invariant (sorted by item_id internally)
    drawn2 = M.sample_negatives(list(reversed(_synthetic_items())))
    assert [it["item_id"] for it in drawn] == [it["item_id"] for it in drawn2]

    # different seed -> different draw in general
    drawn3 = M.sample_negatives(_synthetic_items(), seed=1)
    assert [it["item_id"] for it in drawn] != [it["item_id"] for it in drawn3]


def test_sample_raises_when_stratum_too_small():
    items = [it for it in _synthetic_items() if not (it["rung"] == 3 and int(it["item_id"].split(":")[-1]) < 30)]
    with pytest.raises(ValueError, match="rung 3"):
        M.sample_negatives(items)


# ---------- kappa (synthetic) ----------
def test_kappa_identical_and_chance():
    assert M.cohens_kappa(["1", "0", "1"], ["1", "0", "1"]) == pytest.approx(1.0)
    # booleans: the classic 2x2 table [[a,b],[c,d]] = [[10,5],[5,10]] -> kappa = 1/3
    a = ["1"] * 15 + ["0"] * 15
    b = ["1"] * 10 + ["0"] * 5 + ["1"] * 5 + ["0"] * 10
    assert M.cohens_kappa(a, b) == pytest.approx(1 / 3)
    assert M.cohens_kappa([], []) is None
    with pytest.raises(ValueError, match="differ in length"):
        M.cohens_kappa(["1"], ["1", "0"])


def test_agreement_report_per_rung():
    a = {"i1": "1", "i2": "0", "i3": "1", "i4": "0"}
    b = {"i1": "1", "i2": "1", "i3": "0", "i4": "0"}
    rung = {"i1": 1, "i2": 2, "i3": 2, "i4": 2}
    rep = M.agreement_report(a, b, rung_by_id=rung)
    assert rep["n_common"] == 4
    assert rep["n_disagreed"] == 2
    assert rep["disagreements"] == ["i2", "i3"]
    assert rep["per_rung"]["1"]["kappa"] == pytest.approx(1.0)
    assert rep["per_rung"]["2"]["n_disagreed"] == 2


# ---------- live data ----------
def test_live_sample_invariants_and_repro():
    drawn = M.sample_negatives(ITEMS)
    assert len(drawn) == 100
    counts = {r: sum(1 for it in drawn if it["rung"] == r) for r in (1, 2, 3, 4)}
    assert counts == {1: 25, 2: 25, 3: 25, 4: 25}
    assert all(it["label"] == 0 and it["rung"] >= 1 for it in drawn)
    assert len({it["item_id"] for it in drawn}) == 100
    assert drawn == M.sample_negatives(ITEMS)  # same seed -> same rows
    assert M.SEED == 20261103
    assert M.RUNGS == (1, 2, 3, 4) and M.N_PER_RUNG == 25


def test_live_build_sample_schema(tmp_path):
    rows = M.build_sample(ITEMS)
    assert list(rows[0].keys()) == M.SAMPLE_COLUMNS
    assert len(rows) == 100
    sample_ids = {it["item_id"] for it in ITEMS}
    assert all(r["item_id"] in sample_ids for r in rows)


def test_create_sample_writes_outputs(tmp_path):
    rows = M.create_sample(tmp_path)
    assert len(rows) == 100
    for name in ("sample.csv", "rubric.md", "label_A.csv", "label_B.csv", "resolve.csv"):
        assert (tmp_path / name).is_file(), name

    with open(tmp_path / "sample.csv", newline="", encoding="utf-8") as fh:
        assert next(csv.reader(fh)) == M.SAMPLE_COLUMNS
    sample_ids = [r["item_id"] for r in rows]

    for name in ("label_A.csv", "label_B.csv", "resolve.csv"):
        with open(tmp_path / name, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert reader.fieldnames == ["item_id", "label", "notes"]
            template = list(reader)
            assert [r["item_id"] for r in template] == sample_ids
            assert all(r["label"] == "" and r["notes"] == "" for r in template)

    rubric = (tmp_path / "rubric.md").read_text(encoding="utf-8")
    for token in ("answerable", "not answerable", "ambiguous", "resolve.csv", "LLM"):
        assert token in rubric, token

    # repro: running again in a second dir gives the identical sample
    other = tmp_path / "again"
    rows2 = M.create_sample(other)
    assert rows2 == rows


def test_kappa_from_dir_blank_templates_fail(tmp_path):
    M.create_sample(tmp_path)
    with pytest.raises(ValueError, match="unlabelled"):
        M.kappa_from_dir(tmp_path)


def test_kappa_from_dir_perfect_agreement(tmp_path):
    M.create_sample(tmp_path)
    for name in ("label_A.csv", "label_B.csv"):
        path = tmp_path / name
        with open(path, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["item_id", "label", "notes"])
            writer.writeheader()
            writer.writerows({"item_id": r["item_id"], "label": "0", "notes": ""} for r in rows)
    rep = M.kappa_from_dir(tmp_path)
    assert rep["kappa"] == pytest.approx(1.0)
    assert rep["n_common"] == 100 and rep["n_disagreed"] == 0
    assert rep["per_rung"]["1"]["kappa"] == pytest.approx(1.0)


def test_production_outputs_exist():
    # the committed adjudication pack (results/c1/r3/exp/adjudication/)
    assert (M.OUT_DIR / "sample.csv").is_file()
    assert (M.OUT_DIR / "rubric.md").is_file()
    for name in ("label_A.csv", "label_B.csv", "resolve.csv"):
        with open(M.OUT_DIR / name, newline="", encoding="utf-8") as fh:
            header = next(csv.reader(fh))
        assert header == ["item_id", "label", "notes"]
