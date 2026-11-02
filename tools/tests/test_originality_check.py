#!/usr/bin/env python
"""Offline tests for tools/originality_check.py.

Everything here runs locally with no network. The properties that matter:

  1. A long verbatim run copied from a source is caught as UNQUOTED and fails the run
     (exit 1).
  2. The same run inside quotation marks is classified QUOTED and does not fail it.
  3. A short coincidence (6 words, n=8) is not flagged -- the tool must not cry wolf.
  4. LaTeX \\citep keys and % comments never manufacture a phantom overlap, and LaTeX
     command arguments are still counted as text.
  5. A CRLF corpus file matches an LF draft (Windows line endings are not a bug report).
  6. Exit codes 0 / 1 / 2 are what tools/CONTRACTS.md §6 says they are.

Run:  python -m pytest tools/tests -q
      python tools/tests/test_originality_check.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import originality_check as oc                     # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "originality"
CORPUS = FIX / "corpus"
CORPUS_CRLF = FIX / "corpus_crlf"
SCRIPT = TOOLS / "originality_check.py"

# The run the fixtures share between draft and corpus (11 words).
SHARED = "encodes each document into a dense vector and compares candidate passages"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def run_json(*args: str) -> tuple[int, dict]:
    proc = run(*args, "--json")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:  # pragma: no cover - would mean the CLI is broken
        raise AssertionError(f"stdout was not JSON:\n{proc.stdout}\n{proc.stderr}")
    return proc.returncode, payload


class TestSharedRunClassification(unittest.TestCase):
    def test_identical_ten_word_run_is_unquoted_and_fails(self):
        code, rep = run_json("--draft", str(FIX / "draft_identical.md"),
                             "--corpus", str(CORPUS))
        self.assertEqual(code, 1, "a 11-word verbatim run must exit 1")
        self.assertEqual(rep["summary"]["verdict"], "FAIL")
        self.assertEqual(rep["summary"]["n_unquoted"], 1)
        self.assertEqual(rep["summary"]["n_quoted"], 0)
        hit = rep["hits"][0]
        self.assertEqual(hit["status"], "UNQUOTED")
        self.assertGreaterEqual(hit["length"], 10)
        self.assertIn("encodes each document into a dense vector", hit["text"])
        self.assertEqual(hit["quoted_words"], 0)
        self.assertEqual(rep["draft"], str(FIX / "draft_identical.md"))
        # Location and context are present and non-empty.
        self.assertGreaterEqual(hit["draft_line"], 1)
        self.assertGreaterEqual(hit["source_line"], 1)
        self.assertIn("dense vector", hit["draft_context"])
        self.assertIn("dense vector", hit["source_context"])

    def test_quoted_run_is_quoted_and_does_not_fail(self):
        code, rep = run_json("--draft", str(FIX / "draft_quoted.md"),
                             "--corpus", str(CORPUS), "--quote-budget", "0.9")
        self.assertEqual(code, 0, "a properly quoted run must not exit 1")
        self.assertEqual(rep["summary"]["verdict"], "PASS")
        self.assertEqual(rep["summary"]["n_unquoted"], 0)
        self.assertEqual(rep["summary"]["n_hits"], 1)
        hit = rep["hits"][0]
        self.assertEqual(hit["status"], "QUOTED")
        self.assertEqual(hit["quoted_words"], hit["length"])
        self.assertTrue(hit["text"].startswith("encodes each document"))
        # The quotation audit saw the quote and found its [@smith2020] marker.
        self.assertEqual(len(rep["quotes"]), 1)
        self.assertTrue(rep["quotes"][0]["cited"])
        self.assertEqual(rep["quotes"][0]["words"], 11)

    def test_wrapped_quote_is_still_quoted(self):
        p = FIX / "_tmp_wrapped_quote.md"
        p.write_text(
            "# Method\n\n"
            '[@smith2020] reports that the system "encodes each document into a dense vector\n'
            'and compares candidate passages" during indexing.\n\n'
            "We reuse the same threshold search but log every candidate value.\n",
            encoding="utf-8",
        )
        try:
            code, rep = run_json("--draft", str(p), "--corpus", str(CORPUS),
                                 "--quote-budget", "0.9")
            self.assertEqual(code, 0)
            self.assertEqual(rep["summary"]["n_unquoted"], 0)
            self.assertEqual(rep["summary"]["n_quoted"], 1)
            self.assertEqual(rep["hits"][0]["status"], "QUOTED")
        finally:
            p.unlink()

    def test_six_word_coincidence_not_flagged(self):
        code, rep = run_json("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(CORPUS), "--n", "8")
        self.assertEqual(code, 0)
        self.assertEqual(rep["summary"]["n_hits"], 0,
                         "6 shared words with n=8 must not be reported")
        self.assertEqual(rep["summary"]["longest_unquoted"], 0)

    def test_same_six_words_flagged_when_threshold_lowered(self):
        # Sanity check that the negative test above is negative for the right reason:
        # with n=6 the same passage IS found.
        code, rep = run_json("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(CORPUS), "--n", "6")
        self.assertEqual(code, 1)
        self.assertEqual(rep["hits"][0]["length"], 6)
        self.assertIn("compares candidate passages", rep["hits"][0]["text"])


class TestLatexHandling(unittest.TestCase):
    def test_citep_and_percent_comment_create_no_phantom_overlap(self):
        code, rep = run_json("--draft", str(FIX / "draft_tex.tex"),
                             "--corpus", str(CORPUS))
        self.assertEqual(code, 0)
        self.assertEqual(rep["summary"]["n_hits"], 0,
                         "% comments and \\citep keys must not be analysed as prose")
        # The comment carried 13 corpus words; if it leaked, draft_words would show it.
        draft = oc.prepare(FIX / "draft_tex.tex", drop_references=True)
        self.assertNotIn("smith2020", draft.tokens, "\\citep key leaked into the tokens")
        self.assertNotIn("encodes", draft.tokens, "% comment leaked into the tokens")

    def test_latex_arguments_are_kept_as_text(self):
        draft = oc.prepare(FIX / "draft_tex.tex", drop_references=True)
        self.assertIn("per", draft.tokens)
        self.assertIn("notes", draft.tokens)
        self.assertIn("method", draft.tokens)          # \section{Method}
        self.assertIn("per-item", " ".join(draft.text.split()))
        # The citation became a non-word sentinel, not a token.
        self.assertNotIn("cite", draft.tokens)

    def test_tex_quote_marks_are_detected(self):
        p = FIX / "_tmp_texquote.tex"
        p.write_text("She wrote, ``a short borrowed clause goes here'' in her notes.\n",
                     encoding="utf-8")
        try:
            draft = oc.prepare(p)
            self.assertEqual(len(draft.quotes), 1)
            self.assertIn("borrowed clause", draft.quotes[0].text)
        finally:
            p.unlink()

    def test_escaped_percent_survives(self):
        self.assertEqual(oc.strip_tex_comment(r"growth of 42\% overall % note"), "growth of 42\\% overall ")
        self.assertEqual(oc.strip_tex_comment("plain text % everything after is gone"),
                         "plain text ")


class TestLineEndings(unittest.TestCase):
    def test_crlf_corpus_matches_lf_draft(self):
        raw = (CORPUS_CRLF / "paper_crlf.txt").read_bytes()
        self.assertIn(b"\r\n", raw, "fixture must actually use CRLF")
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""), "fixture must be pure CRLF")

        code, rep = run_json("--draft", str(FIX / "draft_crlf.md"),
                             "--corpus", str(CORPUS_CRLF))
        self.assertEqual(code, 1)
        self.assertEqual(rep["summary"]["n_unquoted"], 1)
        self.assertEqual(rep["hits"][0]["length"], 19)
        self.assertNotIn("\r", rep["hits"][0]["text"])

    def test_crlf_draft_matches_crlf_corpus(self):
        p = FIX / "_tmp_crlf_draft.md"
        p.write_bytes(b"# Note\r\n\r\nGradient accumulation splits a large batch into micro "
                       b"batches and averages the resulting parameter updates.\r\n")
        try:
            code, rep = run_json("--draft", str(p), "--corpus", str(CORPUS_CRLF))
            self.assertEqual(code, 1)
            self.assertGreaterEqual(rep["hits"][0]["length"], 8)
        finally:
            p.unlink()


class TestScopeControl(unittest.TestCase):
    def test_reference_section_is_ignored(self):
        p = FIX / "_tmp_refs.md"
        p.write_text(
            "# Results\n\nWe report the tuned threshold and its effect on recall.\n\n"
            "## References\n\n"
            "Smith, J. (2020). A paper whose abstract states that the proposed retrieval "
            "pipeline encodes each document into a dense vector and compares candidate "
            "passages with a cosine similarity threshold. Venue.\n",
            encoding="utf-8",
        )
        try:
            code, rep = run_json("--draft", str(p), "--corpus", str(CORPUS))
            self.assertEqual(code, 0, "the draft's own bibliography is not the author's prose")
            self.assertEqual(rep["summary"]["n_hits"], 0)
        finally:
            p.unlink()

    def test_longest_run_reported_once_not_every_window(self):
        words = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi "
                 "omicron pi rho sigma tau upsilon").split()
        run20 = " ".join(words)
        self.assertEqual(len(words), 20)

        corpus = FIX / "_tmp_corpus_max"
        corpus.mkdir(exist_ok=True)
        draft = FIX / "_tmp_draft_max.md"
        (corpus / "src.txt").write_text(
            f"Opening sentence here. {run20} followed by unrelated closing words.\n",
            encoding="utf-8")
        draft.write_text(f"# Test\n\nAnother opening. {run20} and then more text.\n",
                         encoding="utf-8")
        try:
            code, rep = run_json("--draft", str(draft), "--corpus", str(corpus))
            self.assertEqual(code, 1)
            self.assertEqual(len(rep["hits"]), 1,
                             "a 20-word copy is one hit, not 13 sliding windows")
            self.assertEqual(rep["hits"][0]["length"], 20)
        finally:
            draft.unlink()
            for f in corpus.iterdir():
                f.unlink()
            corpus.rmdir()

    def test_json_is_utf8_and_reports_caveat(self):
        code, rep = run_json("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(CORPUS))
        self.assertEqual(code, 0)
        self.assertIn("Not a plagiarism detector", rep["summary"]["caveat"])
        self.assertEqual(rep["corpus"]["n_files"], 1)
        self.assertTrue(rep["generated_at"].endswith("Z"))

    def test_markdown_report_written(self):
        out = FIX / "_tmp_report.md"
        try:
            proc = run("--draft", str(FIX / "draft_identical.md"),
                       "--corpus", str(CORPUS), "--out", str(out))
            self.assertEqual(proc.returncode, 1)
            text = out.read_text(encoding="utf-8")
            self.assertIn("## Verdict: **FAIL**", text)
            self.assertIn("## Quotation audit", text)
            self.assertIn("## Hits", text)
            self.assertIn("Not a plagiarism detector", text)
        finally:
            if out.exists():
                out.unlink()


class TestQuotationAudit(unittest.TestCase):
    QUOTED = ('One reviewer wrote "the quarterly budget review meeting moved to Thursday '
              'afternoon because the projector in the main hall was broken again"')

    def _draft(self, body: str) -> Path:
        p = FIX / "_tmp_quote_audit.md"
        p.write_text(f"# Notes\n\n{body}\n\nShort note follows.\n", encoding="utf-8")
        return p

    def test_uncited_quote_is_reported_and_only_strict_mode_fails(self):
        draft = self._draft(self.QUOTED + " before the deadline.")
        try:
            code, rep = run_json("--draft", str(draft), "--corpus", str(CORPUS),
                                 "--quote-budget", "0.9")
            self.assertEqual(code, 0, "quote findings alone do not change the default exit code")
            self.assertEqual(rep["summary"]["n_uncited_quotes"], 1)
            self.assertEqual(rep["summary"]["n_unquoted"], 0)

            strict = run("--draft", str(draft), "--corpus", str(CORPUS),
                         "--quote-budget", "0.9", "--strict-quotes")
            self.assertEqual(strict.returncode, 1, "--strict-quotes must fail on an uncited quote")
        finally:
            draft.unlink()

    def test_cited_quote_passes_strict_mode(self):
        draft = self._draft(self.QUOTED + " [@doe2021].")
        try:
            strict = run("--draft", str(draft), "--corpus", str(CORPUS),
                         "--quote-budget", "0.9", "--strict-quotes")
            self.assertEqual(strict.returncode, 0, strict.stdout + strict.stderr)
        finally:
            draft.unlink()

    def test_quote_budget_overrun_fails_strict_mode_and_reports_ratio(self):
        draft = self._draft(self.QUOTED + " [@doe2021].")
        try:
            code, rep = run_json("--draft", str(draft), "--corpus", str(CORPUS))
            ratio = rep["summary"]["quote_ratio"]
            self.assertGreater(ratio, 0.02)
            self.assertEqual(rep["summary"]["quoted_words"], 19)
            self.assertTrue(any("budget" in f for f in rep["summary"]["quote_findings"]))
            self.assertEqual(code, 0)

            strict = run("--draft", str(draft), "--corpus", str(CORPUS), "--strict-quotes")
            self.assertEqual(strict.returncode, 1)
        finally:
            draft.unlink()

    def test_quote_ratio_is_quoted_words_over_draft_words(self):
        draft = self._draft(self.QUOTED + " [@doe2021].")
        try:
            _, rep = run_json("--draft", str(draft), "--corpus", str(CORPUS))
            self.assertAlmostEqual(
                rep["summary"]["quote_ratio"],
                rep["summary"]["quoted_words"] / rep["draft_words"], places=6)
        finally:
            draft.unlink()


class TestExitCodes(unittest.TestCase):
    def test_pass_is_zero(self):
        self.assertEqual(run("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(CORPUS)).returncode, 0)

    def test_findings_is_one(self):
        self.assertEqual(run("--draft", str(FIX / "draft_identical.md"),
                             "--corpus", str(CORPUS)).returncode, 1)

    def test_missing_draft_is_two(self):
        proc = run("--draft", str(FIX / "does_not_exist.md"), "--corpus", str(CORPUS))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("draft not found", proc.stderr)

    def test_unsupported_extension_is_two(self):
        p = FIX / "_tmp_draft.rst"
        p.write_text("Some text.\n", encoding="utf-8")
        try:
            proc = run("--draft", str(p), "--corpus", str(CORPUS))
            self.assertEqual(proc.returncode, 2)
            self.assertIn("unsupported draft type", proc.stderr)
        finally:
            p.unlink()

    def test_bad_parameters_are_two(self):
        self.assertEqual(run("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(CORPUS), "--n", "2").returncode, 2)
        self.assertEqual(run("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(CORPUS), "--n", "8",
                             "--min-words", "4").returncode, 2)
        self.assertEqual(run("--draft", str(FIX / "draft_short.md"),
                             "--corpus", str(FIX / "no_such_dir")).returncode, 2)

    def test_empty_corpus_is_usage_error(self):
        empty = FIX / "_tmp_empty_corpus"
        empty.mkdir(exist_ok=True)
        try:
            proc = run("--draft", str(FIX / "draft_short.md"), "--corpus", str(empty))
            self.assertEqual(proc.returncode, 2)
            self.assertIn("no .txt/.md files", proc.stderr)
        finally:
            empty.rmdir()

    def test_corpus_read_recursively(self):
        nested = FIX / "_tmp_nested"
        (nested / "sub").mkdir(parents=True, exist_ok=True)
        (nested / "sub" / "deep.txt").write_text(
            (CORPUS / "paper_a.txt").read_text(encoding="utf-8"), encoding="utf-8")
        try:
            code, rep = run_json("--draft", str(FIX / "draft_identical.md"),
                                 "--corpus", str(nested))
            self.assertEqual(code, 1)
            self.assertEqual(rep["corpus"]["n_files"], 1)
            self.assertEqual(rep["hits"][0]["length"], 18)
        finally:
            (nested / "sub" / "deep.txt").unlink()
            (nested / "sub").rmdir()
            nested.rmdir()

    def test_help_works(self):
        proc = run("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--draft", proc.stdout)
        self.assertIn("--corpus", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
