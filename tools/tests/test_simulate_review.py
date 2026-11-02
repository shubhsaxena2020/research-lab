"""Tests for tools/simulate_review.py.

Run from the repo root:  python -m pytest tools/tests/test_simulate_review.py -q

These tests drive the real CLI in a subprocess, so they exercise argument
parsing, YAML reading, validation messages and file output - not just helpers.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "simulate_review.py"

PERSONAS = [
    "methodologist",
    "domain_expert",
    "statistician",
    "novelty_skeptic",
    "reproducibility_reviewer",
    "clarity_reviewer",
]

DRAFT = """# Introduction

DRAFT_SENTINEL_ABC123

Large language models are increasingly used to summarise student feedback, and
prior work reports gains over keyword baselines. We study whether a retrieval
augmented summariser improves faithfulness on a public corpus of 4,120 comments.

Our contribution is a two-stage pipeline that retrieves exemplars before
summarising. We compare against a keyword baseline and report a 6.2 point gain
on ROUGE-L in Table 2. We did not run the pipeline with more than one seed.
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )


def combined(proc: subprocess.CompletedProcess) -> str:
    return (proc.stdout or "") + (proc.stderr or "")


def base_review(persona: str, **overrides) -> dict:
    doc = {
        "persona": persona,
        "summary": (
            "The draft claims a retrieval pipeline improves faithfulness, but the "
            "evidence is a single-seed comparison on one corpus. I would need an "
            "interval and a second corpus before believing the size of the gain."
        ),
        "strengths": ["The problem statement in Section 1 is specific and checkable."],
        "weaknesses": ["Table 2 reports a single run per condition with no interval."],
        "questions": ["How many independent runs produced the 6.2 point gain?"],
        "soundness": 2,
        "presentation": 3,
        "contribution": 2,
        "confidence": 4,
        "overall": 4,
        "decision": "reject",
        "must_fix": [
            {
                "claim": "No confidence intervals are reported for the main metric.",
                "where": "Table 2",
                "evidence_needed": "A paired bootstrap 95% CI over at least 5 seeds.",
            }
        ],
    }
    doc.update(overrides)
    return doc


def write_review(directory: Path, doc: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{doc['persona']}.review.yaml"
    path.write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    return path


def ranked_rows(aggregate_text: str):
    """Data rows of the ranked must-fix table (not the _Where_ continuation rows)."""
    section = aggregate_text.split("## Must-fix, ranked", 1)[1]
    section = section.split("### Alternate wordings", 1)[0]
    rows = []
    for line in section.splitlines():
        if line.startswith("| ") and len(line) > 2 and line[2].isdigit():
            rows.append(line)
    return rows


# --------------------------------------------------------------------------
# pack
# --------------------------------------------------------------------------

def test_pack_creates_six_persona_prompts_with_name_and_draft(tmp_path):
    draft = tmp_path / "intro.md"
    draft.write_text(DRAFT, encoding="utf-8")
    out = tmp_path / "round1"

    proc = run("pack", "--draft", str(draft), "--round", "1", "--out", str(out))
    assert proc.returncode == 0, combined(proc)

    prompts = sorted(out.glob("*.PROMPT.md"))
    assert len(prompts) == 6, [p.name for p in prompts]
    assert [p.name for p in prompts] == sorted(f"{p}.PROMPT.md" for p in PERSONAS)

    for persona in PERSONAS:
        text = (out / f"{persona}.PROMPT.md").read_text(encoding="utf-8")
        assert f"persona: {persona}" in text
        assert f"round 1 - persona: {persona}" in text
        assert "DRAFT_SENTINEL_ABC123" in text
        # the output schema must be present in every pack
        for field in ("must_fix", "soundness", "presentation", "contribution",
                      "confidence", "overall", "decision"):
            assert f"{field}:" in text, (persona, field)
        assert "DRAFT-BEGIN" in text and "DRAFT-END" in text

    manifest = json.loads((out / "_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["round"] == 1
    assert len(manifest["prompts"]) == 6
    assert manifest["draft_sha256"] == hashlib.sha256(
        DRAFT.encode("utf-8")).hexdigest()
    assert "does not generate reviews" in manifest["note"]
    # pack must not pretend a review exists
    assert not list(out.glob("*.review.yaml"))


def test_pack_refuses_ambiguous_delimiter_in_draft(tmp_path):
    draft = tmp_path / "bad.md"
    draft.write_text("text with DRAFT-BEGIN marker inside", encoding="utf-8")
    proc = run("pack", "--draft", str(draft), "--out", str(tmp_path / "o"))
    assert proc.returncode != 0
    assert "DRAFT-BEGIN" in combined(proc)


# --------------------------------------------------------------------------
# ingest
# --------------------------------------------------------------------------

def test_ingest_accepts_valid_review(tmp_path):
    reviews = tmp_path / "round1"
    write_review(reviews, base_review("statistician"))

    proc = run("ingest", "--dir", str(reviews))
    assert proc.returncode == 0, combined(proc)
    assert "1 review(s) valid" in proc.stdout
    assert "statistician.review.yaml" in (reviews / "INGEST.md").read_text(encoding="utf-8")
    assert (reviews / "_ingest.json").is_file()


def test_ingest_rejects_score_out_of_range_and_names_the_file(tmp_path):
    reviews = tmp_path / "round1"
    write_review(reviews, base_review("statistician", soundness=7))

    proc = run("ingest", "--dir", str(reviews))
    assert proc.returncode == 1
    msg = combined(proc)
    assert "statistician.review.yaml" in msg
    assert "soundness" in msg
    assert "out of range 1-4" in msg
    assert "1 review(s) valid" not in proc.stdout


def test_ingest_rejects_missing_field_and_names_the_file(tmp_path):
    reviews = tmp_path / "round1"
    doc = base_review("methodologist")
    doc.pop("confidence")
    write_review(reviews, doc)

    proc = run("ingest", "--dir", str(reviews))
    assert proc.returncode == 1
    msg = combined(proc)
    assert "methodologist.review.yaml" in msg
    assert "field 'confidence': missing required field" in msg


def test_ingest_rejects_bad_decision_and_missing_must_fix_evidence(tmp_path):
    reviews = tmp_path / "round1"
    doc = base_review("clarity_reviewer", decision="major revision",
                      must_fix=[{"claim": "Abstract overclaims robustness."}])
    write_review(reviews, doc)

    proc = run("ingest", "--dir", str(reviews))
    assert proc.returncode == 1
    msg = combined(proc)
    assert "clarity_reviewer.review.yaml" in msg
    assert "decision" in msg
    assert "must_fix[0].evidence_needed" in msg


# --------------------------------------------------------------------------
# aggregate
# --------------------------------------------------------------------------

def test_aggregate_ranks_item_raised_by_three_and_dedupes_wording(tmp_path):
    reviews = tmp_path / "round1"
    write_review(reviews, base_review(
        "statistician",
        must_fix=[{
            "claim": "No confidence intervals are reported for the main metric.",
            "where": "Table 2",
            "evidence_needed": "Paired bootstrap 95% CI over at least 5 seeds.",
        }],
    ))
    write_review(reviews, base_review(
        "methodologist",
        must_fix=[{
            "claim": "The paper reports no confidence intervals for its main metric.",
            "where": "Section 5, Table 2",
            "evidence_needed": "Report the interval for the 6.2 point difference.",
        }],
    ))
    write_review(reviews, base_review(
        "reproducibility_reviewer",
        must_fix=[{
            "claim": "Confidence intervals are missing from Table 2.",
            "where": "Table 2",
            "evidence_needed": "Five-seed runs with a reported interval.",
        }],
    ))
    write_review(reviews, base_review(
        "domain_expert",
        must_fix=[{
            "claim": "Seeds are not reported for any experiment.",
            "where": "Section 4",
            "evidence_needed": "A seed table and the exact command per run.",
        }],
    ))

    out = reviews / "AGGREGATE.md"
    proc = run("aggregate", "--dir", str(reviews), "--out", str(out))
    assert proc.returncode == 0, combined(proc)
    text = out.read_text(encoding="utf-8")

    rows = ranked_rows(text)
    assert len(rows) == 2, rows
    assert rows[0].startswith("| 1 | 3 ("), rows[0]
    assert all(p in rows[0] for p in
               ["statistician", "methodologist", "reproducibility_reviewer"])
    assert "confidence interval" in rows[0].lower()
    assert rows[1].startswith("| 2 | 1 (")
    assert "seeds" in rows[1].lower()
    # one merged item, not three rows with three phrasings
    assert "### Alternate wordings" in text
    assert sum("confidence interval" in r.lower() for r in rows) == 1

    # scores and decision distribution are present
    assert "**Mean (n=4)**" in text
    assert "Median" in text
    assert "## Decision distribution" in text
    assert "reject | 4 |" in text


# --------------------------------------------------------------------------
# compare
# --------------------------------------------------------------------------

def test_compare_reports_item_present_in_round1_and_absent_in_round2_as_resolved(tmp_path):
    r1 = tmp_path / "round1"
    r2 = tmp_path / "round2"
    write_review(r1, base_review("statistician"))
    write_review(r1, base_review(
        "reproducibility_reviewer",
        must_fix=[{
            "claim": "Seeds are not reported for any experiment.",
            "where": "Section 4",
            "evidence_needed": "A seed table and the exact command per run.",
        }],
    ))
    # round 2: the CI item is gone, the seed item persists with the same wording
    write_review(r2, base_review(
        "statistician",
        weaknesses=["The abstract overclaims robustness."],
        must_fix=[{
            "claim": "The abstract overclaims robustness.",
            "where": "Abstract",
            "evidence_needed": "Either drop 'robust' or add a robustness experiment.",
        }],
        overall=6,
        decision="borderline",
    ))
    write_review(r2, base_review(
        "reproducibility_reviewer",
        must_fix=[{
            "claim": "Seeds are not reported for any experiment.",
            "where": "Section 4",
            "evidence_needed": "A seed table and the exact command per run.",
        }],
    ))

    proc = run("compare", "--round1", str(r1), "--round2", str(r2))
    assert proc.returncode == 0, combined(proc)
    text = proc.stdout

    assert "## Resolved (raised in round 1, not raised in round 2): 1" in text
    resolved_block = text.split("## Resolved", 1)[1].split("## Persisted", 1)[0]
    assert "confidence interval" in resolved_block.lower()

    assert "## Persisted (raised in both rounds): 1" in text
    persisted_block = text.split("## Persisted", 1)[1].split("## New in round 2", 1)[0]
    assert "seeds are not reported" in persisted_block.lower()

    assert "1 resolved, 1 persisted, 1 new" in text
    new_block = text.split("## New in round 2", 1)[1]
    assert "overclaims robustness" in new_block.lower()
    assert "| Mean overall (1-10) |" in text


def test_compare_refuses_invalid_round(tmp_path):
    r1 = tmp_path / "round1"
    r2 = tmp_path / "round2"
    write_review(r1, base_review("statistician"))
    write_review(r2, base_review("statistician", overall=99, decision="accept"))

    proc = run("compare", "--round1", str(r1), "--round2", str(r2))
    assert proc.returncode == 1
    assert "statistician.review.yaml" in combined(proc)
    assert "overall" in combined(proc)
