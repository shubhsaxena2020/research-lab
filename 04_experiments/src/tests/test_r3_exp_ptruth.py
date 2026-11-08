"""Unit tests for r3_exp_ptruth pure functions. No Ollama calls."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import r3_exp_ptruth as P


def test_clip_context():
    assert P.clip_context("short", 100) == "short"
    long = "A" * 500 + "B" * 500
    clipped = P.clip_context(long, 200)
    assert len(clipped) <= 210
    assert clipped.startswith("A") and clipped.endswith("B")


def test_build_prompt_contains_passage_question_proposed_and_instruction():
    item = {
        "context": "The sky is blue.",
        "question": "What color is the sky?",
    }
    prompt = P.build_prompt(item, "blue")
    assert "Passage:\nThe sky is blue." in prompt
    assert "Question: What color is the sky?" in prompt
    assert "Proposed answer: blue" in prompt
    assert "Reply with only True or False." in prompt
    assert prompt.index("Passage:") < prompt.index("Question:") < prompt.index("Proposed answer:")


def test_find_true_false_logprobs():
    top = [
        {"token": "Answer", "logprob": -0.5},
        {"token": "True", "logprob": -0.1},
        {"token": "False", "logprob": -5.0},
    ]
    lp_t, lp_f = P.find_true_false_logprobs(top)
    assert lp_t == pytest.approx(-0.1)
    assert lp_f == pytest.approx(-5.0)


def test_find_true_false_logprobs_missing():
    top = [{"token": "Yes", "logprob": -0.1}]
    lp_t, lp_f = P.find_true_false_logprobs(top)
    assert lp_t is None
    assert lp_f is None


def test_ptruth_from_logprobs():
    # equal -> 0.5
    assert P.ptruth_from_logprobs(0.0, 0.0) == pytest.approx(0.5)
    # true much higher -> ~1
    p = P.ptruth_from_logprobs(0.0, -10.0)
    assert p is not None and p > 0.999
    # missing -> None
    assert P.ptruth_from_logprobs(None, -1.0) is None


def test_parse_ollama_response_lines():
    lines = [
        '{"logprobs":[{"token":"True","logprob":-0.1,"top_logprobs":[{"token":"True","logprob":-0.1},{"token":"False","logprob":-2.0}]}],"done":false}',
        '{"done":true}',
    ]
    lp_t, lp_f, first, err = P.parse_ollama_response_lines(lines)
    assert err is None
    assert lp_t == pytest.approx(-0.1)
    assert lp_f == pytest.approx(-2.0)
    assert first == "True"


def test_compute_auroc():
    labels = [1, 1, 0, 0]
    scores = [0.9, 0.8, 0.2, 0.1]
    assert P.compute_auroc(labels, scores) == pytest.approx(1.0)
    # tie
    assert P.compute_auroc([1, 0], [0.5, 0.5]) == pytest.approx(0.5)


def test_fit_threshold_basic():
    # 4 pos high scores, 4 neg low scores -> threshold separates, precision 1.0
    labels = [1, 1, 1, 1, 0, 0, 0, 0]
    scores = [0.9, 0.85, 0.8, 0.75, 0.2, 0.15, 0.1, 0.05]
    res = P.fit_threshold(scores, labels, target_precision=0.80)
    assert res["feasible"] is True
    assert res["abstain_precision"] >= 0.80
    assert res["threshold"] is not None
    # refusing low scores should catch all negatives
    assert res["abstain_recall"] == pytest.approx(1.0)


def test_build_worklist_filters_dev_with_features():
    items = [
        {"item_id": "dev:a:r0", "split": "dev", "label": 1, "rung": 0, "context": "c", "question": "q", "gold_answer": "a"},
        {"item_id": "test:b:r0", "split": "test", "label": 1, "rung": 0, "context": "c", "question": "q"},
        {"item_id": "dev:c:r0", "split": "dev", "label": 0, "rung": 1, "context": "c", "question": "q"},
    ]
    features = {"dev:a:r0": {"reader_answer": "ansA"}, "dev:c:r0": {"reader_answer": "NOT_ANSWERABLE"}}
    work = P.build_worklist(items, features)
    assert len(work) == 2
    assert work[0][1] == "ansA"
    assert work[1][1] == "NOT_ANSWERABLE"
