#!/usr/bin/env python
"""Tests for tools/claims_audit.py.

The point of the tool is to be hard to fool, so every failure mode gets its own fixture and
its own test: a missing evidence file, a printed number that disagrees with the stored value,
a row the reviewer marked NO, a draft claim with no row, and forbidden language with no
novelty check. The valid fixture must pass cleanly, and the worked examples (EX-) must be
skipped rather than judged — otherwise the template's own examples would block every draft.

Run:  python -m pytest tools/tests/test_claims_audit.py -q
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
TOOLS = TESTS.parent
REPO_ROOT = TOOLS.parent
FIX = TESTS / "fixtures" / "claims"
TOOL = TOOLS / "claims_audit.py"

INDEX = FIX / "RESULTS-INDEX.json"
CITATIONS = FIX / "verified_citations.csv"


def run(audit: str, draft: str, *extra: str) -> tuple[subprocess.CompletedProcess, dict]:
    """Run the CLI, return (completed process, parsed --json payload)."""
    cmd = [
        sys.executable,
        str(TOOL),
        "--audit",
        str(FIX / audit),
        "--draft",
        str(FIX / draft),
        "--index",
        str(INDEX),
        "--citations",
        str(CITATIONS),
        "--root",
        str(REPO_ROOT),
        "--json",
    ]
    cmd.extend(extra)
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    payload = {}
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:  # pragma: no cover - would be a real defect
            pytest.fail(f"stdout is not JSON:\n{proc.stdout[:2000]}\nstderr:\n{proc.stderr[:2000]}")
    return proc, payload


def codes(payload: dict) -> list[str]:
    return [f["code"] for f in payload["findings"]]


def finding(payload: dict, code: str) -> dict:
    hits = [f for f in payload["findings"] if f["code"] == code]
    assert hits, f"expected a {code} finding, got {codes(payload)}"
    return hits[0]


# --------------------------------------------------------------------------- the happy path


def test_valid_audit_passes():
    proc, out = run("audit_valid.md", "draft")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["ok"] is True and out["exit_code"] == 0
    assert out["findings"] == []
    assert out["n_rows"] == 10
    assert out["n_rows_checked"] == 9
    assert out["n_rows_skipped_examples"] == 1
    assert out["n_rows_failed"] == 0
    # 4 abstract sentences + 1 quantitative introduction sentence
    assert out["n_draft_claims"] == 5
    assert out["n_uncovered"] == 0
    assert all(r["status"] == "PASS" for r in out["rows"] if not r["claim_id"].startswith("EX-"))


def test_tolerance_comes_from_the_index_entry():
    """A5 prints 0.031 for a stored 0.0312; the index declares 0.0 tolerance, so 1% relative applies."""
    _, out = run("audit_valid.md", "draft")
    row = next(r for r in out["rows"] if r["claim_id"] == "A5")
    assert row["status"] == "PASS"
    assert row["stored_value"] == "0.0312"


def test_markdown_table_parses_wrapped_and_escaped_cells():
    sys.path.insert(0, str(TOOLS))
    import claims_audit  # noqa: PLC0415

    rows, _warnings = claims_audit.parse_audit_table((FIX / "audit_valid.md").read_text(encoding="utf-8"))
    by_id = {r["claim_id"]: r for r in rows}
    # A8's claim is wrapped over two physical lines and must be joined into one cell
    assert "14.2 ms mean latency per query" in by_id["A8"]["claim"]
    assert by_id["A8"]["claim"].startswith('"On the same held-out queries')
    # A5's limitation contains an escaped pipe and must stay a single cell
    assert by_id["A5"]["limitation"] == "family of 3 comparisons, Holm | not Bonferroni"
    # A6's command contains a pipe inside a code span; the row must still have 10 columns
    assert "grep" in by_id["A6"]["command"] and "audit" in by_id["A6"]["command"]
    assert all(len(r) == 11 for r in rows)  # 10 columns + _line


def test_shipped_template_parses_and_only_has_example_rows():
    """Guards the deliverable: 06_review/CLAIMS-AUDIT-TEMPLATE.md must stay machine-readable."""
    sys.path.insert(0, str(TOOLS))
    import claims_audit  # noqa: PLC0415

    rows, _warnings = claims_audit.parse_audit_table(
        (REPO_ROOT / "06_review" / "CLAIMS-AUDIT-TEMPLATE.md").read_text(encoding="utf-8")
    )
    assert len(rows) == 6
    assert all(r["claim_id"].startswith("EX-") for r in rows)
    assert all(r["evidence_key"] and r["command"] for r in rows)
    # the wrapped EX-002 row must survive as one row, not two
    ex2 = next(r for r in rows if r["claim_id"] == "EX-002")
    assert "a gain of 5.3 points" in ex2["claim"]
    assert len(ex2) == 11


# --------------------------------------------------------------------------- row-level failures


def test_missing_evidence_file_fails_and_names_the_row():
    proc, out = run("audit_missing_file.md", "draft_min")
    assert proc.returncode == 1
    f = finding(out, "ROW_MISSING_FILE")
    assert f["row_id"] == "M2"
    assert "main_ours_missing.json" in f["detail"]
    assert f["file"].endswith("audit_missing_file.md")
    status = {r["claim_id"]: r["status"] for r in out["rows"]}
    assert status["M1"] == "PASS" and status["M2"] == "FAIL"
    assert out["ok"] is False


def test_value_disagreement_with_stored_result_fails():
    proc, out = run("audit_value_mismatch.md", "draft_min")
    assert proc.returncode == 1
    f = finding(out, "ROW_VALUE_MISMATCH")
    assert f["row_id"] == "V2"
    assert "0.865" in f["detail"] and "0.9" in f["detail"]
    status = {r["claim_id"]: r["status"] for r in out["rows"]}
    assert status["V2"] == "FAIL" and status["V1"] == "PASS"


def test_row_marked_not_verified_fails():
    proc, out = run("audit_verified_no.md", "draft_min")
    assert proc.returncode == 1
    f = finding(out, "ROW_NOT_VERIFIED")
    assert f["row_id"] == "N2"
    assert "NO" in f["detail"]
    status = {r["claim_id"]: r["status"] for r in out["rows"]}
    assert status["N1"] == "PASS" and status["N2"] == "FAIL"


# --------------------------------------------------------------------------- coverage


def test_uncovered_quantitative_intro_claim_is_reported_with_file_and_line():
    proc, out = run("audit_uncovered.md", "draft_uncovered")
    assert proc.returncode == 1
    f = finding(out, "UNCOVERED")
    assert f["file"].replace("\\", "/").endswith("draft_uncovered/paper.md")
    assert f["line"] == 9, f"expected the introduction sentence on line 9, got {f['line']}"
    assert "5.3" in f["detail"]
    assert "5.3" in f["detail"] and "introduction" in f["detail"].lower()
    assert out["n_uncovered"] == 1
    assert out["n_covered"] == 1


def test_state_of_the_art_without_a_novelty_row_fails():
    proc, out = run("audit_sota.md", "draft_sota")
    assert proc.returncode == 1
    f = finding(out, "NOVELTY_ROW_MISSING")
    assert "state of the art" in f["detail"].lower()
    assert f["file"].replace("\\", "/").endswith("draft_sota/paper.md")
    assert f["line"] == 5
    # the row itself is sound: this is a coverage/rule failure, not a broken evidence link
    assert out["n_rows_failed"] == 0
    assert "UNCOVERED" not in codes(out)


# --------------------------------------------------------------------------- examples are inert


def test_example_rows_are_skipped_not_judged():
    proc, out = run("audit_examples_only.md", "draft_min")
    assert proc.returncode == 1  # only because the draft claim is uncovered
    assert out["n_rows_skipped_examples"] == 2
    assert {r["status"] for r in out["rows"]} == {"SKIP"}
    # deliberately broken examples: a missing file, a missing key, verified=MAYBE.
    # If any of them were judged these codes would appear.
    assert set(codes(out)) == {"UNCOVERED"}
    assert all(f.get("row_id") is None for f in out["findings"])


# --------------------------------------------------------------------------- citations, CLI


def test_citation_key_must_be_verified(tmp_path: Path):
    audit = tmp_path / "audit_bad_citation.md"
    audit.write_text(
        "\n".join(
            [
                "| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |",
                "|---|---|---|---|---|---|---|---|---|---|",
                '| C1 | "The baseline reaches 0.812 accuracy, as shown before [@nosuchkey2024]." | Abstract '
                "| tools/tests/fixtures/claims/results/main_baseline.json | accuracy "
                "| python 04_experiments/harness/run.py --config configs/baseline.json --seed 0 "
                "| 0.812 | YES | none | SS |",
                '| C2 | "our reranker raises this to 0.865" | Abstract '
                "| tools/tests/fixtures/claims/results/main_ours.json | accuracy "
                "| python 04_experiments/harness/run.py --config configs/main.json --seed 0 "
                "| 0.865 | YES | none | SS |",
                "",
            ]
        ),
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(TOOL),
        "--audit",
        str(audit),
        "--draft",
        str(FIX / "draft_min"),
        "--index",
        str(INDEX),
        "--citations",
        str(CITATIONS),
        "--root",
        str(REPO_ROOT),
        "--json",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert proc.returncode == 1
    out = json.loads(proc.stdout)
    f = finding(out, "ROW_CITATION_UNVERIFIED")
    assert f["row_id"] == "C1" and "nosuchkey2024" in f["detail"]
    # the MISMATCH-status row in the CSV is not VERIFIED either
    assert "fake2019" not in json.dumps(out)


def test_usage_errors_exit_2(tmp_path: Path):
    missing_index = [
        sys.executable,
        str(TOOL),
        "--audit",
        str(FIX / "audit_valid.md"),
        "--draft",
        str(FIX / "draft"),
        "--index",
        str(tmp_path / "nope.json"),
        "--citations",
        str(CITATIONS),
    ]
    proc = subprocess.run(missing_index, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert proc.returncode == 2
    assert "does not exist" in proc.stderr

    no_args = subprocess.run(
        [sys.executable, str(TOOL)], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    assert no_args.returncode == 2


def test_help_works():
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    assert proc.returncode == 0
    assert "claims-audit" in proc.stdout.lower() or "--audit" in proc.stdout


def test_markdown_verdict_is_written_with_out_flag(tmp_path: Path):
    target = tmp_path / "verdict.md"
    proc, _ = run("audit_valid.md", "draft", "--out", str(target))
    assert proc.returncode == 0
    text = target.read_text(encoding="utf-8")
    assert "Claims audit verdict" in text
    assert "| A1 |" in text
    assert "PASS" in text


# --- regression: trigger stems must match WORDS, not substrings -------------------------
def test_stem_gain_does_not_match_against():
    """'we compare A against B' is not a comparative claim.

    A naive `stem in text` matched 'gain' inside 'against', which made every comparison
    sentence an UNCOVERED claim. Prefix matching on tokenised words fixes that.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("claims_audit_mod", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod._trigger("We compare a baseline against a treatment.") is None
    assert mod._trigger("We compare our model against the baseline, a gain of 2 points.")  # has a number
    assert mod._trigger("Our model gains accuracy over the baseline.") == "word 'gain'"
    assert mod._trigger("It outperforms the baseline.") == "word 'outperform'"


def test_forbidden_first_requires_a_priority_claim():
    import importlib.util

    spec = importlib.util.spec_from_file_location("claims_audit_mod2", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.FORBIDDEN_RE.search("First, we load the data.") is None
    assert mod.FORBIDDEN_RE.search("This is the first work to study X.") is not None
    assert mod.FORBIDDEN_RE.search("The first experiment failed.") is None
    assert mod.FORBIDDEN_RE.search("a novel method") is not None
