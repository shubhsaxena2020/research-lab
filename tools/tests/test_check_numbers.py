#!/usr/bin/env python
"""Unit tests for tools/check_numbers.py.

The tool exists to make "every number traces to a results file" checkable rather than
hopeful, so these tests are organised around what it must *refuse* to do:

  * refuse a marked number whose printed value disagrees with the stored one (MISMATCH),
  * refuse an unmarked number even when the right value exists in the index (UNTRACEABLE),
  * refuse a marker whose id is not in the index (DANGLING_MARKER),
  * refuse toy-path numbers unless --allow-toy is given,
  * and, just as important, *not* cry wolf on the years, citation numbers, DOIs, arXiv ids,
    figure/table refs and dates that fill a real paragraph.

Fixtures live in tools/tests/fixtures/checknums/<case>/ next to their own index.json, so
each case is a tiny self-contained repo.

Run:  python -m pytest tools/tests/test_check_numbers.py -q
"""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import check_numbers as cn  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "checknums"
SCRIPT = TOOLS / "check_numbers.py"


def case(name: str) -> Path:
    return FIX / name


def run(draft: Path, index: Path | None = None, extra=(), write: bool = False) -> tuple[int, dict]:
    """Run main() in-process and return (exit_code, parsed JSON report)."""
    argv = [
        "--draft", str(draft),
        "--index", str(index if index is not None else draft / "index.json"),
        "--json", "--quiet",
        *extra,
    ]
    if not write:
        argv.append("--no-write")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cn.main(argv)
    out = buf.getvalue()
    if not out.strip():
        # main() only prints JSON on --json; an empty stdout means it failed before audit.
        return code, {}
    return code, json.loads(out)


def findings(report: dict) -> list[dict]:
    return report.get("findings", [])


def statuses(report: dict) -> list[str]:
    return [f["status"] for f in findings(report)]


# --------------------------------------------------------------------------- clean cases


class CleanDraftTests(unittest.TestCase):
    """A correct draft must pass, including one full of things that only look like numbers."""

    def test_realistic_markdown_passes(self):
        """Every number marked -> zero findings, and no UNTRACEABLE anywhere."""
        code, rep = run(case("good"))
        self.assertEqual(findings(rep), [], f"unexpected findings: {findings(rep)}")
        self.assertEqual(code, 0)
        self.assertTrue(rep["ok"])
        self.assertGreaterEqual(rep["n_tokens"], 30, "the fixture must exercise a real paragraph")
        self.assertEqual(rep["counts"]["UNTRACEABLE"], 0)
        self.assertEqual(rep["counts"]["MISMATCH"], 0)

    def test_realistic_latex_passes(self):
        """LaTeX markers: a `% num:id` comment above the number and a trailing one after it."""
        code, rep = run(case("latex"))
        self.assertEqual(findings(rep), [], f"unexpected findings: {findings(rep)}")
        self.assertEqual(code, 0)
        # The .tex fixture uses both marker styles; both must have bound.
        styles = {m["marker_id"] for m in rep["matches"]}
        self.assertIn("main.accuracy.baseline", styles)
        self.assertIn("main.accuracy.ours", styles)

    def test_years_and_citations_are_not_flagged(self):
        """A paragraph of only exempt forms (years, [12], DOI, arXiv, refs) must be silent.

        This is the anti-false-positive test: if this fails, the tool is unusable, because
        every real paragraph contains years and citation numbers.
        """
        code, rep = run(case("exempt_only"))
        self.assertEqual(findings(rep), [], f"unexpected findings: {findings(rep)}")
        self.assertEqual(code, 0)
        self.assertEqual(rep["n_matched"], 0, "this fixture has no marked numbers")
        self.assertGreater(rep["n_exempt"], 10, "the fixture must contain many exempt forms")
        rules = {e["rule"] for e in rep["exemptions"]}
        for expected in ("year", "citation_number", "doi", "arxiv_id", "float_prefix",
                         "page_line", "url"):
            self.assertIn(expected, rules, f"rule {expected} never fired: {sorted(rules)}")


# --------------------------------------------------------------------------- failure cases


class FailureModeTests(unittest.TestCase):
    """Each failure mode has its own fixture, so a regression names itself."""

    def test_tampered_value_is_mismatch(self):
        """Printed 0.912 against stored 0.812 is not a rounding difference."""
        code, rep = run(case("tampered"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["MISMATCH"])
        f = findings(rep)[0]
        self.assertEqual(f["token"], "0.912")
        self.assertEqual(f["stored"], "0.812")
        self.assertEqual(f["line"], 3)
        self.assertIn("0.912", f["reason"])

    def test_unmarked_number_is_untraceable(self):
        """0.910 exists in the index, but with no marker nothing ties the sentence to it."""
        code, rep = run(case("unmarked"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["UNTRACEABLE"])
        f = findings(rep)[0]
        self.assertEqual(f["token"], "0.910")
        self.assertEqual(f["line"], 3)
        self.assertEqual(f["col"], 19)
        self.assertIn("marker", f["reason"])

    def test_marker_with_absent_id_is_dangling(self):
        code, rep = run(case("dangling"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["DANGLING_MARKER"])
        self.assertIn("main.accuracy.missing", findings(rep)[0]["reason"])

    def test_marker_wrapping_nothing_is_unbound(self):
        """A leftover marker is a receipt with no purchase: it must not pass silently."""
        code, rep = run(case("unbound"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["UNBOUND_MARKER"])

    def test_rounding_window_is_not_a_free_pass(self):
        """Stored 0.8124: 0.812 is a faithful rounding, 0.813 is not (diff 0.0006)."""
        code, rep = run(case("rounding"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["MISMATCH"])
        self.assertEqual(findings(rep)[0]["token"], "0.813")
        self.assertEqual(rep["n_matched"], 1, "0.812 must have matched")

    def test_entry_tolerance_is_honoured(self):
        """A declared tolerance of 0.01 lets a two-decimal 0.82 stand for 0.812."""
        code, rep = run(case("tolerance"))
        self.assertEqual(findings(rep), [])
        self.assertEqual(code, 0)


# --------------------------------------------------------------------------- percentages


class PercentageTests(unittest.TestCase):
    def test_percentage_form_of_a_fraction_passes(self):
        code, rep = run(case("percent"))
        self.assertEqual(findings(rep), [], f"unexpected findings: {findings(rep)}")
        self.assertEqual(code, 0)
        self.assertEqual(rep["n_matched"], 2, "both '81.2%' and '81.2 per cent' count")
        for m in rep["matches"]:
            self.assertIn("percentage", m["evidence"].lower())
            self.assertIn("0.812", m["evidence"])

    def test_percentage_does_not_launder_a_wrong_value(self):
        """91.2% of 0.812 is still a different number; the percentage form must not hide it."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "draft.md").write_text(
                "Baseline: <!-- num:a -->91.2%<!-- /num -->\n", encoding="utf-8"
            )
            (tmp / "index.json").write_text(json.dumps({
                "version": 1,
                "entries": [{"id": "a", "file": "main.json", "key": "accuracy"}],
            }), encoding="utf-8")
            (tmp / "main.json").write_text('{"accuracy": 0.812}', encoding="utf-8")
            code, rep = run(tmp)
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["MISMATCH"])


# --------------------------------------------------------------------------- toy


class ToyTests(unittest.TestCase):
    """Toy numbers are labelled TOY and must never be mistaken for results (CONTRACTS §5)."""

    def test_toy_number_rejected_without_flag(self):
        code, rep = run(case("toy"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["UNTRACEABLE"])
        self.assertIn("toy", findings(rep)[0]["reason"].lower())

    def test_toy_number_accepted_with_flag(self):
        code, rep = run(case("toy"), extra=("--allow-toy",))
        self.assertEqual(findings(rep), [], f"unexpected findings: {findings(rep)}")
        self.assertEqual(code, 0)
        self.assertTrue(rep["allow_toy"])

    def test_toy_flagged_in_the_index_is_rejected(self):
        """The real index marks toy entries with `"toy": true`; that flag alone must stop them."""
        code, rep = run(case("toy_flag"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["UNTRACEABLE"])
        self.assertIn("toy", findings(rep)[0]["reason"].lower())
        code, rep = run(case("toy_flag"), extra=("--allow-toy",))
        self.assertEqual(code, 0)
        self.assertEqual(findings(rep), [])

    def test_toy_flagged_in_the_results_file_is_rejected(self):
        """A toy run copied to results/summary_toy.json still says `"toy": true` inside."""
        code, rep = run(case("toy_file"))
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["UNTRACEABLE"])
        code, rep = run(case("toy_file"), extra=("--allow-toy",))
        self.assertEqual(code, 0)
        self.assertEqual(findings(rep), [])


# --------------------------------------------------------------------------- exit codes


class ExitCodeTests(unittest.TestCase):
    """0 = clean, 1 = findings, 2 = usage error. Checked through the real CLI process."""

    def cli(self, *args: str) -> int:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True, text=True, timeout=120,
        )
        return proc.returncode

    def test_cli_exit_0_on_clean(self):
        d = case("good")
        self.assertEqual(self.cli("--draft", str(d), "--index", str(d / "index.json"),
                                  "--no-write", "--quiet"), 0)

    def test_cli_exit_1_on_findings(self):
        d = case("tampered")
        self.assertEqual(self.cli("--draft", str(d), "--index", str(d / "index.json"),
                                  "--no-write", "--quiet"), 1)

    def test_cli_exit_2_on_missing_draft(self):
        self.assertEqual(self.cli("--draft", str(FIX / "does-not-exist"),
                                  "--no-write", "--quiet"), 2)

    def test_cli_exit_2_on_missing_index(self):
        d = case("good")
        self.assertEqual(self.cli("--draft", str(d), "--index", str(FIX / "no-index.json"),
                                  "--no-write", "--quiet"), 2)

    def test_exit_2_on_bad_index_json(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "draft.md").write_text("no numbers here\n", encoding="utf-8")
            (tmp / "index.json").write_text("{not json", encoding="utf-8")
            code, _ = run(tmp)
        self.assertEqual(code, 2)

    def test_exit_2_on_bad_exempt_regex(self):
        d = case("good")
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "exempt.json"
            bad.write_text(json.dumps(["[unclosed"]), encoding="utf-8")
            code, _ = run(d, extra=("--exempt", str(bad)))
        self.assertEqual(code, 2)

    def test_exit_2_on_explicit_missing_exempt_config(self):
        """An explicitly requested --exempt that does not exist is a typo, not 'no patterns'."""
        d = case("good")
        code, _ = run(d, extra=("--exempt", str(FIX / "nope.json")))
        self.assertEqual(code, 2)

    def test_exit_2_on_unsupported_file_type(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "notes.txt").write_text("0.5\n", encoding="utf-8")
            code, _ = run(tmp)
        self.assertEqual(code, 2)


# --------------------------------------------------------------------------- report


class ReportTests(unittest.TestCase):
    def test_markdown_report_is_written(self):
        d = case("tampered")
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "audit.md"
            code, _ = run(d, extra=("--out", str(out)), write=True)
            self.assertEqual(code, 1)
            self.assertTrue(out.exists(), "the report file was not written")
            text = out.read_text(encoding="utf-8")
        self.assertIn("FAIL", text)
        self.assertIn("MISMATCH", text)
        self.assertIn("0.912", text)
        self.assertIn("draft.md:3", text)
        self.assertIn("Rules this run applied", text)

    def test_json_shape_and_ordering(self):
        code, rep = run(case("good"))
        for key in ("draft", "index", "n_tokens", "n_matched", "n_exempt", "n_findings",
                    "counts", "findings", "matches", "exemptions", "ok", "generated_at"):
            self.assertIn(key, rep, f"missing key {key}")
        self.assertEqual(rep["tool"], "check_numbers")
        self.assertEqual(rep["n_files"], 1)
        self.assertTrue(rep["files"][0].endswith("paper.md"))

    def test_context_window_is_about_120_chars(self):
        code, rep = run(case("tampered"))
        f = findings(rep)[0]
        self.assertIn("0.912", f["context"])
        self.assertLessEqual(len(f["context"]), 60 + len(f["token"]) + 60 + 2)
        self.assertNotIn("\n", f["context"], "context must be one line for the report table")

    def test_multiple_files_in_a_directory(self):
        """A directory draft is scanned across every .md/.tex file it contains."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "index.json").write_text(json.dumps({
                "version": 1,
                "entries": [{"id": "a", "file": "main.json", "key": "accuracy"}],
            }), encoding="utf-8")
            (tmp / "main.json").write_text('{"accuracy": 0.5}', encoding="utf-8")
            (tmp / "sec1.md").write_text("Good: <!-- num:a -->0.5<!-- /num -->\n",
                                         encoding="utf-8")
            (tmp / "sub").mkdir()
            (tmp / "sub" / "sec2.tex").write_text(
                "Good: 0.5 % num:a\n", encoding="utf-8")
            code, rep = run(tmp)
            self.assertEqual(rep["n_files"], 2)
            self.assertEqual(findings(rep), [])
            self.assertEqual(code, 0)


# --------------------------------------------------------------------------- units


class NumberParsingTests(unittest.TestCase):
    """The tokeniser is where false negatives are born, so it is tested directly."""

    def parse(self, text: str):
        m = cn.NUMBER_RE.search(text)
        self.assertIsNotNone(m, f"no token found in {text!r}")
        return cn.parse_number(m)

    def test_plain_decimal(self):
        value, raw, half, pct = self.parse("accuracy 0.812 overall")
        self.assertEqual(value, Decimal("0.812"))
        self.assertEqual(half, Decimal("0.0005"))
        self.assertFalse(pct)

    def test_percent(self):
        value, raw, half, pct = self.parse("12.3%")
        self.assertEqual(value, Decimal("0.123"))
        self.assertEqual(half, Decimal("0.0005"))
        self.assertTrue(pct)

    def test_thousands_separator(self):
        value, raw, half, pct = self.parse("1,234 examples")
        self.assertEqual(value, Decimal("1234"))
        self.assertEqual(raw, Decimal("1234"))

    def test_multiplier_suffix(self):
        value, raw, half, pct = self.parse("3.5x faster")
        self.assertEqual(value, Decimal("3.5"))
        self.assertFalse(pct)

    def test_signed(self):
        value, _, _, _ = self.parse("+2.1 points")
        self.assertEqual(value, Decimal("2.1"))
        value, _, _, _ = self.parse("-0.5 points")
        self.assertEqual(value, Decimal("-0.5"))

    def test_scientific_notation(self):
        value, raw, half, pct = self.parse("lr 3e-4")
        self.assertEqual(raw, Decimal("3e-4"))
        # Precision of 3e-4 comes from the exponent, not from how many digits are typed.
        self.assertEqual(half, Decimal("0.00005"))

    def test_glued_identifier_is_not_a_number(self):
        """'ResNet50' contains no measurement; the lookbehind must skip it."""
        self.assertIsNone(cn.NUMBER_RE.search("ResNet50"))


class ExemptionTests(unittest.TestCase):
    """Each rule is narrow. If a rule starts swallowing real numbers, these fail."""

    def rule_for(self, text: str, needle: str = "") -> str | None:
        kind = "tex" if "\\" in text else "md"
        spans = cn.comment_spans(text, kind)
        masked = cn.blank(text, spans)
        starts = cn.line_starts(text)
        toks = cn.scan_tokens(text, masked, "x", 60)
        target = None
        for t in toks:
            if not needle or t.text == needle:
                target = t
                break
        self.assertIsNotNone(target, f"no token found in {text!r}")
        return cn.exempt_rule(target, text, kind, cn.protected_spans(masked, kind), [])

    def test_year_is_exempt(self):
        self.assertEqual(self.rule_for("Published in 2019 by us.", "2019"), "year")

    def test_metric_is_not_exempt(self):
        """The whole point: 0.910 next to ordinary prose is not exempt, it is a finding."""
        self.assertIsNone(self.rule_for("We reach 0.910 accuracy.", "0.910"))

    def test_out_of_range_four_digit_number_is_not_a_year(self):
        self.assertIsNone(self.rule_for("We keep 1850 examples.", "1850"))

    def test_citation_number_is_exempt(self):
        self.assertEqual(self.rule_for("As shown before [12, 15].", "12"), "citation_number")

    def test_figure_reference_is_exempt(self):
        self.assertEqual(self.rule_for("See Figure 3 for details.", "3"), "float_prefix")

    def test_page_number_is_exempt(self):
        self.assertEqual(self.rule_for("See p. 42 of the appendix.", "42"), "page_line")

    def test_doi_is_exempt(self):
        self.assertEqual(
            self.rule_for("doi:10.18653/v1/n19-1423 here", "10.18653"), "doi"
        )

    def test_latex_ref_key_is_exempt(self):
        self.assertEqual(self.rule_for("see \\ref{fig:2} here", "2"), "latex_command_arg")

    def test_latex_dimension_is_exempt(self):
        self.assertEqual(
            self.rule_for("\\documentclass[11pt]{article}", "11"), "latex_command_arg"
        )
        self.assertEqual(
            self.rule_for("width=0.5\\linewidth", "0.5"), "latex_dimension"
        )

    def test_config_pattern_only_exempts_what_it_covers(self):
        """A config pattern for a learning rate must not excuse other numbers on the line."""
        text = "learning rate 3e-4 and accuracy 0.910 were logged."
        kind = "md"
        spans = cn.comment_spans(text, kind)
        masked = cn.blank(text, spans)
        toks = cn.scan_tokens(text, masked, "x", 60)
        patterns, _ = cn.load_exempt(cn.DEFAULT_EXEMPT)
        self.assertTrue(patterns, "the shipped exempt config must have patterns")
        prot = cn.protected_spans(masked, kind)
        got = {t.text: cn.exempt_rule(t, text, kind, prot, patterns) for t in toks}
        self.assertEqual(got.get("3e-4"), "config_exempt")
        self.assertIsNone(got.get("0.910"), "the metric on the same line must still be audited")


class MarkerBindingTests(unittest.TestCase):
    def test_unclosed_marker_binds_next_number(self):
        """Hand-written `<!-- num:id -->` without a closing tag still binds one number."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "draft.md").write_text(
                "Score: <!-- num:a -->0.5 here.\n", encoding="utf-8")
            (tmp / "index.json").write_text(json.dumps({
                "version": 1,
                "entries": [{"id": "a", "file": "main.json", "key": "accuracy"}],
            }), encoding="utf-8")
            (tmp / "main.json").write_text('{"accuracy": 0.5}', encoding="utf-8")
            code, rep = run(tmp)
        self.assertEqual(findings(rep), [])
        self.assertEqual(code, 0)

    def test_marker_bound_to_a_year_still_checked(self):
        """A marker wins over an exemption: marking a number means 'prove this one'."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "draft.md").write_text(
                "Released in <!-- num:a -->1999<!-- /num -->.\n", encoding="utf-8")
            (tmp / "index.json").write_text(json.dumps({
                "version": 1,
                "entries": [{"id": "a", "file": "main.json", "key": "year"}],
            }), encoding="utf-8")
            (tmp / "main.json").write_text('{"year": 2001}', encoding="utf-8")
            code, rep = run(tmp)
        self.assertEqual(code, 1)
        self.assertEqual(statuses(rep), ["MISMATCH"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
