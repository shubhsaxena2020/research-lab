"""Unit tests for the B4 reader-confidence baseline. No model is loaded; runs in seconds."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reader_logprob as R  # noqa: E402

ITEM = {
    "item_id": "dev:abc:r0",
    "context": "A problem is regarded as inherently difficult if its solution requires significant "
               "resources, whatever the algorithm used.",
    "question": "What makes a problem inherently difficult?",
    "label": 1,
    "rung": 0,
}


# ---------------------------------------------------------------- prompt building
def test_build_messages_has_system_rule_and_passage_then_question():
    msgs = R.build_messages(ITEM)
    assert [m["role"] for m in msgs] == ["system", "user"]
    assert R.NOT_ANSWERABLE in msgs[0]["content"]
    assert "answer from the passage" in msgs[0]["content"].lower() or "only the passage" in msgs[0]["content"].lower()
    user = msgs[1]["content"]
    assert ITEM["context"] in user
    assert ITEM["question"] in user
    # passage must come before the question, per PREREGISTRATION §4
    assert user.index(ITEM["context"]) < user.index(ITEM["question"])
    # the gold answer must never leak into the prompt
    assert "significant resources" in user  # from context only
    assert "gold" not in user.lower()


def test_build_messages_never_includes_label_or_gold_fields():
    it = dict(ITEM, gold_answer="resources", anchor_token="significant", replacement="tiny")
    user = R.build_messages(it)[1]["content"]
    assert "resources" in user  # present via context
    for leaked in ("anchor_token", "replacement", "label"):
        assert leaked not in user


def test_clip_context_keeps_short_text_and_bounds_long_text():
    assert R.clip_context("short", 100) == "short"
    long = "A" * 500 + "B" * 500
    clipped = R.clip_context(long, 200)
    assert len(clipped) <= 210
    assert clipped.startswith("A") and clipped.endswith("B")


def test_render_prompt_uses_chat_template_with_generation_prompt():
    class FakeTok:
        def __init__(self):
            self.calls = []

        def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False):
            self.calls.append((messages, tokenize, add_generation_prompt))
            return "<|im_start|>system\n" + messages[0]["content"] + "<|im_end|>\n" + messages[1]["content"]

    tok = FakeTok()
    out = R.render_prompt(tok, ITEM)
    assert tok.calls and tok.calls[0][1] is False and tok.calls[0][2] is True
    assert ITEM["question"] in out and R.NOT_ANSWERABLE in out


# ---------------------------------------------------------------- logprob aggregation
def test_uniform_logits_give_negative_log_vocab_size():
    logits = [[0.0, 0.0, 0.0]]
    (lp,) = R.token_logprobs_from_logits(logits, [1])
    assert lp == pytest.approx(-1.0986122886681098)  # -log(3)


def test_logprobs_match_hand_computed_log_softmax():
    import math

    logits = [[1.0, 2.0, 3.0]]
    got = R.token_logprobs_from_logits(logits, [2])[0]
    lse = math.log(math.exp(1) + math.exp(2) + math.exp(3))
    assert got == pytest.approx(3.0 - lse)
    assert got < 0.0


def test_token_logprobs_are_negative_and_row_aligned():
    logits = [[0.0, 5.0, 0.0], [3.0, 0.0, 0.0]]
    lps = R.token_logprobs_from_logits(logits, [1, 0])
    assert len(lps) == 2
    assert all(v < 0 for v in lps)
    assert lps[0] > lps[1]  # high logit at the chosen id -> higher (less negative) logprob


def test_summarize_is_mean_over_generated_tokens_only():
    mean, n = R.summarize_logprobs([-0.5, -1.5])
    assert (mean, n) == (-1.0, 2)


def test_summarize_refuses_empty_sequence():
    with pytest.raises(ValueError):
        R.summarize_logprobs([])


def test_generation_length_stops_at_eos_and_padding():
    assert R.generation_length([10, 11, 2, 99, 99], pad_id=0, eos_id=2) == 3  # eos counted, pad not
    assert R.generation_length([10, 11, 0, 0], pad_id=0, eos_id=2) == 2
    assert R.generation_length([10, 11], pad_id=0, eos_id=2) == 2
    assert R.generation_length([0, 0], pad_id=0, eos_id=2) == 0  # nothing generated
    assert R.generation_length([], pad_id=0, eos_id=2) == 0


def test_generation_length_pad_equals_eos_stops_at_first_stop_token():
    # when pad == eos, the first stop token is the EOS and counts once; the rest is padding
    assert R.generation_length([7, 9, 9], pad_id=9, eos_id=9) == 2
    assert R.generation_length([9, 9, 9], pad_id=9, eos_id=9) == 1


def test_score_rows_from_batch_reads_per_row_scores_and_excludes_padding():
    torch = pytest.importorskip("torch")
    # batch of 2, 3 decoding steps; row 1 finishes at step 1 (eos) then pads
    step_logits = [torch.zeros(2, 12) for _ in range(3)]  # vocab 12, uniform -> -log(12)
    gen_ids = torch.tensor([[1, 2, 3], [1, 9, 9]])  # eos id = 9, pad id = 9
    rows = R.score_rows_from_batch(
        step_logits, gen_ids, pad_id=9, eos_id=9, decode=lambda ids: " ".join(map(str, ids))
    )
    assert rows[0]["n_tokens"] == 3
    assert rows[0]["mean_logprob"] == pytest.approx(-2.4849066497880004)  # -log(12)
    assert rows[1]["n_tokens"] == 2  # token "1" then EOS; the trailing pad is never averaged
    assert rows[1]["answer"] == "1 9"


def test_score_rows_from_batch_marks_padding_at_position_zero_as_none():
    torch = pytest.importorskip("torch")
    # first id is pad -> nothing was generated for this row
    rows = R.score_rows_from_batch(
        [torch.zeros(1, 12)], torch.tensor([[0]]), pad_id=0, eos_id=9, decode=lambda ids: ""
    )
    assert rows == [None]


# ---------------------------------------------------------------- CSV schema / resume
def test_format_row_is_four_fields_and_collapses_newlines():
    row = R.format_row("dev:x:r0", "a\nb  c", -0.123456789, 7)
    assert len(row) == len(R.CSV_HEADER) == 4
    assert row[1] == "a b c"
    assert row[2] == "-0.123457"
    assert row[3] == "7"


def test_append_rows_writes_header_once_and_survives_commas(tmp_path):
    p = tmp_path / "reader_features.csv"
    R.append_rows(p, R.CSV_HEADER, [R.format_row("a", "x, y", -1.0, 2)])
    R.append_rows(p, R.CSV_HEADER, [R.format_row("b", "z", -2.0, 3)])
    lines = p.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0].split(",") == R.CSV_HEADER
    assert len(lines) == 3
    with open(p, newline="", encoding="utf-8") as fh:
        recs = list(csv.DictReader(fh))
    assert [r["item_id"] for r in recs] == ["a", "b"]
    assert recs[0]["reader_answer"] == "x, y"
    assert float(recs[0]["reader_mean_logprob"]) == -1.0


def test_read_existing_ids_roundtrip_and_tolerates_truncated_last_line(tmp_path):
    p = tmp_path / "reader_features.csv"
    R.append_rows(p, R.CSV_HEADER, [R.format_row("a", "x", -1.0, 2), R.format_row("b", "y", -2.0, 3)])
    assert R.read_existing_ids(p) == {"a", "b"}
    # simulate a kill mid-write: half a row appended
    with open(p, "a", encoding="utf-8") as fh:
        fh.write('c,"unterminated')
    assert R.read_existing_ids(p) == {"a", "b"}


def test_read_existing_ids_missing_file_is_empty(tmp_path):
    assert R.read_existing_ids(tmp_path / "nope.csv") == set()


def test_read_existing_ids_rejects_foreign_schema(tmp_path):
    p = tmp_path / "other.csv"
    p.write_text("item_id,bm25_top1\nx,1.0\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        R.read_existing_ids(p)


def test_resume_skips_scored_items_and_keeps_order(tmp_path):
    items = [{"item_id": f"i{k}", "context": "c", "question": "q"} for k in range(5)]
    p = tmp_path / "reader_features.csv"
    R.append_rows(p, R.CSV_HEADER, [R.format_row("i0", "a", -1.0, 1), R.format_row("i2", "b", -1.0, 1)])
    done = R.read_existing_ids(p)
    todo = [it for it in items if it["item_id"] not in done]
    assert [it["item_id"] for it in todo] == ["i1", "i3", "i4"]
