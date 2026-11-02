#!/usr/bin/env python
"""Adversarial edge-case tests for tools/check_numbers.py (companion to test_check_numbers.py).

Where the existing suite proves the tool's *contract* on well-formed fixtures, this file
attacks the edges: number spellings the tokeniser has to survive, the rounding window's
boundary, marker placement that a careless author will get wrong, structural numbers that
fill a real paragraph, broken index entries, and file-level oddities (CRLF, BOM, tabs,
empty files, directory scans).

Two deliberate rule choices are asserted here and explained in the test that makes them,
because a reviewer will otherwise ask "why is that the expected answer?":

  * ROUNDING. The tool's documented window is *half of the last decimal place printed*
    (0.0005 for "0.871"), never a fixed number of decimals. So 0.871 is NOT an acceptable
    rendering of a stored 0.8703706667: the correctly rounded 3dp form is 0.870, and
    accepting 0.871 would need an arbitrary tolerance the index never declared. An entry
    that *does* declare tolerance 0.001 accepts it, which is the supported escape hatch.

  * LaTeX MARKER + BLANK LINE. The tool documents "the first number on the next non-blank,
    non-comment line", so a blank line does not sever a `% num:id` marker. That is asserted
    as documented behaviour; the dangerous half of the same rule (how far a marker may
    reach) is pinned separately: it must not bind a number more than four lines away.

Every test builds its own tiny repo under pytest's tmp_path: a draft, an index.json, a
results file and an (empty) exempt config, so nothing here touches 05_paper/draft/ or the
repo's real 04_experiments/. `--exempt` points at the empty local config on purpose, so the
shipped exemption list cannot mask a tokeniser bug.

Run:  python -m pytest tools/tests/test_check_numbers_adversarial.py -q
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
from decimal import Decimal
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import check_numbers as cn  # noqa: E402

DEFAULT_ENTRIES = [{"id": "a", "file": "main.json", "key": "v"}]
DEFAULT_RESULTS = {"main.json": {"v": 0.5}}


# --------------------------------------------------------------------------- harness


def _prepare(root: Path, entries, results) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.json").write_text(
        json.dumps({"version": 1, "entries": entries}, ensure_ascii=False), encoding="utf-8"
    )
    # An empty local exempt config: these tests must fail on the tool's own rules only.
    (root / "exempt.json").write_text("[]", encoding="utf-8")
    for fname, payload in results.items():
        p = root / fname
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return root


def _run(draft: Path, root: Path, extra=()) -> tuple[int, dict]:
    argv = [
        "--draft", str(draft),
        "--index", str(root / "index.json"),
        "--exempt", str(root / "exempt.json"),
        "--json", "--quiet", "--no-write",
        *extra,
    ]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cn.main(argv)
    out = buf.getvalue()
    return code, (json.loads(out) if out.strip() else {})


def audit(root, text: str, results=None, entries=None, name: str = "draft.md", extra=()):
    """Write one draft + its index/results under `root` and return (exit_code, report)."""
    root = Path(root)
    _prepare(root, DEFAULT_ENTRIES if entries is None else entries,
             DEFAULT_RESULTS if results is None else results)
    draft = root / name
    draft.parent.mkdir(parents=True, exist_ok=True)
    # newline="" keeps "\r\n" literal so the CRLF test really writes CRLF on Windows.
    draft.write_text(text, encoding="utf-8", newline="")
    return _run(draft, root, extra)


def audit_dir(root, files: dict, results=None, entries=None, extra=()):
    """Write a directory of drafts (keys are relative paths) and audit the directory."""
    root = Path(root)
    _prepare(root, DEFAULT_ENTRIES if entries is None else entries,
             DEFAULT_RESULTS if results is None else results)
    for rel_name, text in files.items():
        p = root / rel_name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="")
    return _run(root, root, extra)


def statuses(rep: dict) -> list[str]:
    return [f["status"] for f in rep.get("findings", [])]


def bad_tokens(rep: dict) -> list[str]:
    return [f["token"] for f in rep.get("findings", [])]


def matched_ids(rep: dict) -> set[str]:
    return {m["marker_id"] for m in rep.get("matches", [])}


# --------------------------------------------------------------------------- 1. formats


class TestNumberFormats:
    """Every spelling below is a number a real draft contains; the tool must read it."""

    def test_scientific_notation_lowercase_matches(self, tmp_path):
        code, rep = audit(
            tmp_path / "lower", "Learning rate <!-- num:a -->1.2e-3<!-- /num --> was used.\n",
            results={"main.json": {"v": 0.0012}},
        )
        assert code == 0, (
            "1.2e-3 must parse as 0.0012 and match a stored 0.0012; if this fails, every "
            "scientific-notation hyper-parameter in a draft is a false finding."
        )
        assert rep["n_matched"] == 1, "the token must be MATCHed, not exempted or flagged"

    def test_scientific_notation_uppercase_with_plus_exponent_matches(self, tmp_path):
        code, rep = audit(
            tmp_path / "upper", "We processed <!-- num:a -->3E+05<!-- /num --> rows.\n",
            results={"main.json": {"v": 300000}},
        )
        assert code == 0, (
            "3E+05 must parse as 300000; if this fails, an uppercase exponent is read as a "
            "truncated number (3) and a correct draft is flagged."
        )
        assert rep["n_matched"] == 1, "the uppercase-exponent token must match its stored value"

    def test_unicode_minus_is_a_negative_number(self, tmp_path):
        code, rep = audit(
            tmp_path / "minus",
            "Drop: <!-- num:a -->\u22120.5<!-- /num --> vs gain <!-- num:b -->0.5<!-- /num -->.\n",
            entries=[{"id": "a", "file": "main.json", "key": "drop"},
                     {"id": "b", "file": "main.json", "key": "gain"}],
            results={"main.json": {"drop": -0.5, "gain": 0.5}},
        )
        assert code == 0, (
            "U+2212 MINUS SIGN must be read as a sign: if this fails, '\u22120.5' is compared "
            "as +0.5 (or as an exempt token), so a sign error in a draft goes unreported."
        )
        assert matched_ids(rep) == {"a", "b"}, "both the negative and the positive token must match"

    def test_thousands_separator_is_one_number(self, tmp_path):
        code, rep = audit(
            tmp_path / "thousands", "Corpus: <!-- num:a -->1,234,567<!-- /num --> tokens.\n",
            results={"main.json": {"v": 1234567}},
        )
        assert code == 0, (
            "1,234,567 must be a single token equal to 1234567; if this fails, comma-grouped "
            "corpus sizes are split into fragments and cannot be traced."
        )
        assert rep["n_tokens"] == 1, "a grouped integer must not be scanned as several tokens"

    def test_european_thousands_separator_is_not_silently_truncated(self):
        text = "Value 1.234,56 here."
        toks = cn.scan_tokens(text, cn.blank(text, []), "x")
        assert [t.value for t in toks] == [Decimal("1234.56")], (
            "If this fails, the European form '1.234,56' is being tokenised as '1.234' plus "
            "'56'. A marker around '1.234' then MATCHes a stored 1.234 while the page reads "
            "1.234,56 -- a factor-1000 error reported as traced evidence, which is the exact "
            "failure this tool exists to prevent."
        )

    def test_leading_plus_and_multiplier_suffix_are_the_same_number(self, tmp_path):
        code_plus, rep_plus = audit(
            tmp_path / "plus", "Gain of <!-- num:a -->+0.5<!-- /num --> points.\n",
            results={"main.json": {"v": 0.5}},
        )
        code_x, rep_x = audit(
            tmp_path / "times", "Runs <!-- num:a -->0.5x<!-- /num --> faster.\n",
            results={"main.json": {"v": 0.5}},
        )
        assert code_plus == 0, (
            "A leading '+' is a sign, not a different number: if this fails, '+0.5' is read as "
            "text plus 0.5 and a correct draft is flagged."
        )
        assert code_x == 0, (
            "The 'x' in '0.5x' is a multiplier suffix, not part of the value: if this fails, "
            "'0.5x' is compared as 0.5 followed by garbage, or the suffix is dropped into the "
            "next token."
        )
        assert rep_plus["n_matched"] == 1 and rep_x["n_matched"] == 1, (
            "both spellings must be MATCHed against the stored 0.5"
        )

    def test_percent_without_space_matches_a_fraction(self, tmp_path):
        code, rep = audit(
            tmp_path / "pct", "Accuracy <!-- num:a -->12.3%<!-- /num --> on test.\n",
            results={"main.json": {"v": 0.123}},
        )
        assert code == 0, (
            "12.3% is the same number as a stored 0.123; if this fails, percentages no longer "
            "match fractional metrics and every results table is unreadable to the tool."
        )
        assert "percentage" in rep["matches"][0]["evidence"].lower(), (
            "the evidence must say the match was made in percentage form, so a reader can see "
            "why 12.3 and 0.123 were treated as equal"
        )

    def test_percent_with_a_space_before_the_sign_matches(self, tmp_path):
        code, rep = audit(
            tmp_path / "pct_space", "Accuracy <!-- num:a -->12.3 %<!-- /num --> on test.\n",
            results={"main.json": {"v": 0.123}},
        )
        assert code == 0, (
            "If this fails, a typographic space before '%' (12.3 %) makes the token plain "
            "12.3, compared against 0.123 -> MISMATCH. LaTeX and house styles routinely put a "
            "thin space before %, so this produces a false finding on a correct draft, and the "
            "author's only fix is to change the typography."
        )
        assert rep["n_findings"] == 0, "a space before the percent sign must not create a finding"

    def test_p_value_and_sample_size_are_measured_numbers(self, tmp_path):
        code_bad, rep_bad = audit(
            tmp_path / "p_unmarked", "The effect is significant (p<0.001).\n",
            results={"main.json": {"v": 0.001}},
        )
        code_ok, rep_ok = audit(
            tmp_path / "p_marked", "The effect is significant (p < <!-- num:a -->0.001<!-- /num -->).\n",
            results={"main.json": {"v": 0.001}},
        )
        code_n, rep_n = audit(
            tmp_path / "n", "We sampled n=<!-- num:a -->150<!-- /num --> items.\n",
            results={"main.json": {"v": 150}},
        )
        assert code_bad == 1 and statuses(rep_bad) == ["UNTRACEABLE"], (
            "An unmarked p-value must be a finding: if this fails, a p-value can be typed into "
            "a draft without a results file behind it, which is precisely how a made-up "
            "significance claim gets past review."
        )
        assert code_ok == 0, (
            "A marked p-value must match its stored 0.001; if this fails, p-values cannot be "
            "traced at all and authors will be tempted to exempt them wholesale."
        )
        assert code_n == 0, (
            "n=150 must be traceable like any other number; if this fails, sample sizes -- the "
            "one number every claim about statistical power depends on -- cannot be marked."
        )

    def test_range_endpoints_are_two_separate_numbers(self, tmp_path):
        code, rep = audit(
            tmp_path / "range",
            "CI <!-- num:a -->0.80<!-- /num -->-<!-- num:b -->0.85<!-- /num --> on test.\n",
            entries=[{"id": "a", "file": "main.json", "key": "lo"},
                     {"id": "b", "file": "main.json", "key": "hi"}],
            results={"main.json": {"lo": 0.80, "hi": 0.85}},
        )
        assert code == 0, (
            "Both ends of a range need their own marker and value: if this fails, a CI printed "
            "as '0.80-0.85' cannot be traced even when both endpoints are in the index."
        )
        code_one, rep_one = audit(
            tmp_path / "range_half",
            "CI from <!-- num:a -->0.80<!-- /num --> to 0.85 on test.\n",
            results={"main.json": {"v": 0.80}},
        )
        assert code_one == 1 and "0.85" in bad_tokens(rep_one), (
            "The far end of a range is a real number, not a label: if this fails, marking the "
            "lower bound silently vouches for the upper bound too."
        )

    def test_approximately_prefix_is_not_an_exemption(self, tmp_path):
        code, rep = audit(
            tmp_path / "tilde", "About ~<!-- num:a -->0.9<!-- /num --> of runs.\n",
            results={"main.json": {"v": 0.9}},
        )
        assert code == 0, (
            "'~0.9' is still 0.9 and must match; if this fails, an approximation marker is "
            "either swallowed into the token or treated as a label."
        )
        code_bare, rep_bare = audit(
            tmp_path / "tilde_bare", "About ~0.9 of runs.\n", results={"main.json": {"v": 0.9}},
        )
        assert code_bare == 1, (
            "'~' is not an exemption rule: if this fails, prefixing a number with '~' launders "
            "it past the audit, which is a one-character bypass of RULES.md #2."
        )

    def test_a_fraction_is_not_silently_exempted(self, tmp_path):
        code, rep = audit(tmp_path / "frac", "About 1/3 of the runs diverged.\n")
        assert code == 1, (
            "A fraction is not in the exemption list: if this passes, '1/3' is being exempted "
            "as a file path or a list marker, and any number can hide behind a slash."
        )
        assert sorted(bad_tokens(rep)) == ["1", "3"], (
            "Both digits of '1/3' must be reported as untraceable; if only one is, the other is "
            "being exempted by a rule that does not fit."
        )


# --------------------------------------------------------------------------- 2. rounding


class TestRoundingTolerance:
    """The window is half the last printed decimal place -- not 'close enough'."""

    def test_four_decimal_rounding_of_a_long_stored_value_matches(self, tmp_path):
        code, rep = audit(
            tmp_path / "4dp", "Score <!-- num:a -->0.8704<!-- /num --> overall.\n",
            results={"main.json": {"v": 0.8703706667}},
        )
        assert code == 0, (
            "0.8704 is the correct 4dp rounding of 0.8703706667; if this fails, the rounding "
            "window is narrower than half a unit in the last place and correctly rounded "
            "numbers are flagged."
        )

    def test_two_decimal_rounding_of_the_same_value_matches(self, tmp_path):
        code, rep = audit(
            tmp_path / "2dp", "Score <!-- num:a -->0.87<!-- /num --> overall.\n",
            results={"main.json": {"v": 0.8703706667}},
        )
        assert code == 0, (
            "0.87 is a correct 2dp rounding; if this fails, the window does not widen when "
            "fewer decimals are printed, so authors are forced to print more precision than "
            "the paper needs."
        )

    def test_three_decimal_0_871_is_not_a_rounding_of_0_87037(self, tmp_path):
        code, rep = audit(
            tmp_path / "3dp", "Score <!-- num:a -->0.871<!-- /num --> overall.\n",
            results={"main.json": {"v": 0.8703706667}},
        )
        assert code == 1 and statuses(rep) == ["MISMATCH"], (
            "Asserted rule: the window is half of the last PRINTED decimal (0.0005 for 3dp), "
            "not a fixed 4dp or 2dp tolerance. 0.8703706667 rounds to 0.870 at 3dp and 0.87 at "
            "2dp, so 0.871 is not a correct rounding at any precision -- if this passes, a "
            "transposed digit is accepted as rounding noise."
        )
        code_tol, rep_tol = audit(
            tmp_path / "3dp_tol", "Score <!-- num:a -->0.871<!-- /num --> overall.\n",
            entries=[{"id": "a", "file": "main.json", "key": "v", "tolerance": 0.001}],
            results={"main.json": {"v": 0.8703706667}},
        )
        assert code_tol == 0, (
            "A wider window must be an explicit, per-entry decision: with tolerance 0.001 in "
            "the index, 0.871 is within 0.00063 and must be accepted. If this fails, there is "
            "no supported way to declare a looser tolerance."
        )

    def test_half_printed_as_fifty_percent_matches(self, tmp_path):
        code, rep = audit(
            tmp_path / "half", "Half the runs <!-- num:a -->50%<!-- /num --> converged.\n",
            results={"main.json": {"v": 0.5}},
        )
        assert code == 0, (
            "50% is 0.5; if this fails, a fraction stored as 0.5 cannot be printed as a "
            "percentage, which is how half of every results table is written."
        )
        assert "percentage" in rep["matches"][0]["evidence"].lower(), (
            "the evidence must name the percentage reading, so the match is auditable later"
        )

    def test_zero_point_five_zero_percent_is_not_one_half(self, tmp_path):
        code, rep = audit(
            tmp_path / "tiny", "Only <!-- num:a -->0.50%<!-- /num --> of runs diverged.\n",
            results={"main.json": {"v": 0.5}},
        )
        assert code == 1, (
            "If this passes, '0.50%' (= 0.005) is accepted as the stored 0.5 because the "
            "percent-units fallback compares the printed 0.50 against 0.5 directly. A draft "
            "that says '0.50% of runs diverged' against a stored 0.5 divergence rate is wrong "
            "by 100x, yet the tool reports it as MATCH with 'stored value is already in "
            "percent units' as evidence. The fallback must not fire when it contradicts the "
            "fraction reading of the same token."
        )


# --------------------------------------------------------------------------- 3. placement


class TestMarkerPlacement:
    """A marker must bind the number it was written for -- and never a different one."""

    def test_markdown_marker_on_the_line_above_binds_the_next_number(self, tmp_path):
        code, rep = audit(
            tmp_path / "above", "Score:\n<!-- num:a -->\n0.812 on test.\n",
            results={"main.json": {"v": 0.812}},
        )
        assert code == 0, (
            "An unclosed `<!-- num:id -->` on its own line is the hand-written Markdown form "
            "and must bind the next number; if this fails, authors must use the wrapped form "
            "or their numbers are all untraceable."
        )
        assert rep["n_matched"] == 1, "the number on the next line must be MATCHed"

    def test_markdown_marker_after_the_number_on_the_same_line_binds_it(self, tmp_path):
        code, rep = audit(
            tmp_path / "trailing", "Score: 0.812 <!-- num:a -->\n",
            results={"main.json": {"v": 0.812}},
        )
        assert code == 0, (
            "A trailing marker on the same line must bind the number to its left (table-cell "
            "style); if this fails, numbers written before their marker are flagged."
        )
        assert rep["n_matched"] == 1, "the preceding number must be MATCHed, not left untraceable"

    def test_latex_marker_reaches_the_next_nonblank_line(self, tmp_path):
        code, rep = audit(
            tmp_path / "blank", "% num:a\n\n0.812 \\\\\n",
            results={"main.json": {"v": 0.812}}, name="draft.tex",
        )
        assert code == 0, (
            "Documented contract: a `% num:id` binds the first number on the next non-blank, "
            "non-comment line, so one blank line does not sever it. If this fails, ordinary "
            "LaTeX layout (comment, blank line, table) produces UNBOUND_MARKER noise."
        )
        assert rep["n_matched"] == 1, "the number after the blank line must be MATCHed"

    def test_latex_marker_never_reaches_past_four_lines(self, tmp_path):
        code, rep = audit(
            tmp_path / "far", "% num:a\nprose one\nprose two\nprose three\nprose four\n0.812 \\\\\n",
            results={"main.json": {"v": 0.812}}, name="draft.tex",
        )
        assert code == 1, (
            "A marker five lines above a number must not bind it: if this passes, a marker "
            "left over from a deleted sentence silently vouches for an unrelated number a "
            "paragraph later, and the audit reports a match nobody intended."
        )
        assert set(statuses(rep)) == {"UNBOUND_MARKER", "UNTRACEABLE"}, (
            "the orphan marker must be reported AND the number must be reported: if only one "
            "appears, the failure is half-silent (either a stale receipt or an unmarked number)"
        )

    def test_two_markers_bind_two_numbers_in_one_table_row(self, tmp_path):
        code, rep = audit(
            tmp_path / "row", "% num:a\n0.812 & 0.790 \\\\  % num:b\n",
            entries=[{"id": "a", "file": "main.json", "key": "va"},
                     {"id": "b", "file": "main.json", "key": "vb"}],
            results={"main.json": {"va": 0.812, "vb": 0.790}}, name="draft.tex",
        )
        assert code == 0, (
            "The standard LaTeX table pattern -- marker above the row for cell 1, trailing "
            "marker for cell 2 -- must bind each number to its own id. If this fails, only one "
            "cell per row can be traced."
        )
        assert matched_ids(rep) == {"a", "b"}, (
            "each marker must own a different number; if one id is missing from the matches, "
            "the second marker bound the first cell and the other cell went unchecked"
        )

    def test_stacked_markers_do_not_silently_discard_one(self, tmp_path):
        code, rep = audit(
            tmp_path / "stacked", "% num:a\n% num:b\n0.812 \\\\\n",
            entries=[{"id": "a", "file": "main.json", "key": "bad"},
                     {"id": "b", "file": "main.json", "key": "v"}],
            results={"main.json": {"bad": 0.9, "v": 0.812}}, name="draft.tex",
        )
        assert code == 1, (
            "If this passes, two markers stacked above one number are both bound to it, the "
            "later one overwrites the earlier in the token->marker map, and the earlier marker "
            "is neither checked nor reported as UNBOUND_MARKER. A marker claiming 0.9 "
            "disappears while the number passes against 0.812 -- a stale or wrong marker is "
            "exactly the thing this tool is supposed to catch."
        )
        assert "a" in matched_ids(rep) or any("a" == f.get("marker_id") for f in rep["findings"]), (
            "marker 'a' must either be checked against the number or reported; it must not "
            "vanish from the audit"
        )

    def test_marker_with_trailing_whitespace_still_binds(self, tmp_path):
        code_md, rep_md = audit(
            tmp_path / "ws_md", "<!-- num:a   -->0.812<!-- /num   -->\n",
            results={"main.json": {"v": 0.812}},
        )
        code_tex, rep_tex = audit(
            tmp_path / "ws_tex", "% num:a   \n0.812 \\\\\n",
            results={"main.json": {"v": 0.812}}, name="draft.tex",
        )
        assert code_md == 0, (
            "Trailing whitespace inside a Markdown marker is an editor artefact, not a "
            "different marker; if this fails, a formatter reflow silently untraces numbers."
        )
        assert code_tex == 0, (
            "Trailing whitespace after `% num:id` must be tolerated; if this fails, editors "
            "that trim/strip inconsistently break the LaTeX marker form."
        )

    def test_two_line_html_comment_marker_is_reported_not_silently_ignored(self, tmp_path):
        code, rep = audit(
            tmp_path / "multiline", "Score:\n<!--\nnum:a\n-->\n0.5 here.\n",
            results={"main.json": {"v": 0.5}},
        )
        assert code == 1, (
            "A marker written inside a comment that spans several lines cannot bind the number "
            "below it (the comment ends two lines above). The tool must say so; if this passes, "
            "the marker is either accepted as vouching for a distant number or dropped without "
            "a word, and the author believes the number is traced."
        )
        assert "UNBOUND_MARKER" in statuses(rep), (
            "the unbound marker must be named in the findings, so the author knows to fix the "
            "marker rather than the number"
        )
        assert rep["n_matched"] == 0, (
            "nothing may be reported as MATCH here: a two-line comment must not silently bind "
            "a number it does not wrap"
        )


# --------------------------------------------------------------------------- 4. structural


class TestStructuralNumbers:
    """Numbers that are structure, not results. False positives here make the tool unusable."""

    def test_structural_numbering_produces_no_findings(self, tmp_path):
        text = (
            "## 3. Results\n\n"
            "See Figure 2 and Table 3 in Section 4.1; refs [12] and [12, 15].\n"
            "We ran from 2020-2024; doi 10.1000/xyz; arXiv:1706.03762; version v2.1.3.\n"
            "Results at https://example.org/a/12345/b?id=7 were reused.\n"
        )
        code, rep = audit(tmp_path, text, results={"main.json": {"v": 0.5}})
        assert rep["findings"] == [], (
            "If this fails, a paragraph of ordinary scholarly apparatus (heading number, "
            "Figure/Table/Section refs, citations, a year range, a DOI, an arXiv id, a version "
            "string, a URL) is reported as untraceable numbers -- the tool would be unusable "
            "on any real paper. Findings: %r" % (rep["findings"],)
        )
        assert code == 0, "a draft containing only structural numbers must exit 0"
        rules = {e["rule"] for e in rep["exemptions"]}
        expected = {"section_number", "float_prefix", "citation_number", "year", "doi",
                    "arxiv_id", "url"}
        assert expected <= rules, (
            "each structural form must be excused by its own named rule, not by one catch-all: "
            "missing %r from %r" % (sorted(expected - rules), sorted(rules))
        )
        assert rep["n_matched"] == 0, "no structural number may be reported as a traced result"

    def test_bare_equation_number_is_not_a_result(self, tmp_path):
        code, rep = audit(tmp_path / "eq", "The loss in (1) is minimised over the batch.\n")
        assert code == 0, (
            "If this fails, a bare equation number '(1)' is reported as an untraceable result. "
            "The tool's own docstring lists 'equation numbers' among the exemptions and "
            "RULE_DOC promises equation numbering is exempt; only the 'Equation (1)' spelling "
            "works, so a draft that cross-references equations as '(1)' cannot pass."
        )
        assert rep["n_matched"] == 0, "an equation number must be exempt, never 'matched'"

    def test_comments_are_not_scanned_in_either_dialect(self, tmp_path):
        code_md, rep_md = audit(
            tmp_path / "html", "Text.\n<!-- see 0.912 and 12 for details -->\nDone.\n",
            results={"main.json": {"v": 0.912}},
        )
        code_tex, rep_tex = audit(
            tmp_path / "pct_comment", "% baseline reached 12.3% accuracy\nDone.\n",
            results={"main.json": {"v": 0.123}}, name="draft.tex",
        )
        assert code_md == 0 and rep_md["n_tokens"] == 0, (
            "An HTML comment is not printed text: if this fails, numbers inside an author's "
            "TODO comment are audited as claims (and a commented-out 0.912 becomes a finding "
            "or, worse, a match)."
        )
        assert code_tex == 0 and rep_tex["n_tokens"] == 0, (
            "A LaTeX `%` comment is not printed text: if this fails, a commented-out "
            "percentage is audited, so drafts fail on text the reader never sees."
        )

    def test_percent_marker_lookalike_in_a_code_block_does_not_vouch(self, tmp_path):
        text = (
            "Example usage:\n\n"
            "```latex\n"
            "% num:a\n"
            "0.812\n"
            "```\n\n"
            "End.\n"
        )
        code, rep = audit(tmp_path, text, results={"main.json": {"v": 0.812}})
        assert rep["n_matched"] == 0, (
            "If this fails, a `% num:id` line inside a Markdown code block is being treated as "
            "a LaTeX marker and vouches for the example number -- a documentation snippet can "
            "then launder a number into a passing audit."
        )
        assert rep["n_markers"] == 0, (
            "no marker may be created from inside a fenced code block; if one is, the block's "
            "contents are being parsed as draft prose"
        )
        assert code == 1 and "0.812" in bad_tokens(rep), (
            "the example number itself is still a number in the file and must be reported "
            "(failing safe). If it is silently exempt, a real number inside a code block would "
            "also disappear from the audit."
        )


# --------------------------------------------------------------------------- 5. integrity


class TestMarkerIntegrity:
    """A marker is only as good as the index entry behind it."""

    def test_marker_pointing_at_a_missing_results_file_is_index_error(self, tmp_path):
        code, rep = audit(
            tmp_path, "<!-- num:a -->0.5<!-- /num -->\n",
            entries=[{"id": "a", "file": "missing.json", "key": "v"}],
            results={"main.json": {"v": 0.5}},
        )
        assert code == 1 and statuses(rep) == ["INDEX_ERROR"], (
            "If this fails, a marker whose results file was deleted or renamed is reported as "
            "something other than INDEX_ERROR (or not at all), so the number looks traced "
            "while the evidence behind it does not exist."
        )
        assert "missing.json" in rep["findings"][0]["reason"], (
            "the finding must name the missing file, otherwise the author cannot tell which "
            "entry to repair"
        )

    def test_marker_pointing_at_a_json_object_is_index_error(self, tmp_path):
        code, rep = audit(
            tmp_path, "<!-- num:a -->0.5<!-- /num -->\n",
            results={"main.json": {"v": {"mean": 0.5}}},
        )
        assert code == 1 and statuses(rep) == ["INDEX_ERROR"], (
            "A key that resolves to an object has no single value to compare: if this fails, "
            "the tool either crashes or compares against a repr, and a table of metrics could "
            "pass on a value nobody chose."
        )
        assert "not a scalar" in rep["findings"][0]["reason"], (
            "the reason must say the key is not a scalar, so the author knows to point the "
            "entry at a leaf (v.mean) instead"
        )

    def test_string_and_float_stored_values_both_match(self, tmp_path):
        code, rep = audit(
            tmp_path,
            "Str <!-- num:a -->0.812<!-- /num --> and float <!-- num:b -->0.812<!-- /num -->.\n",
            entries=[{"id": "a", "file": "strings.json", "key": "v"},
                     {"id": "b", "file": "floats.json", "key": "v"}],
            results={"strings.json": {"v": "0.812"}, "floats.json": {"v": 0.812}},
        )
        assert code == 0, (
            "A numeric string in a results file is the same number as a float (CONTRACTS §2 "
            "allows str leaves); if this fails, hand-written or CSV-derived results files "
            "produce INDEX_ERROR on correct drafts."
        )
        assert rep["n_matched"] == 2, "both the string- and float-backed markers must MATCH"

    def test_null_stored_value_is_index_error_not_a_match(self, tmp_path):
        code, rep = audit(
            tmp_path, "<!-- num:a -->0.5<!-- /num -->\n",
            results={"main.json": {"v": None}},
        )
        assert code == 1 and statuses(rep) == ["INDEX_ERROR"], (
            "If this fails, a metric that was never computed (null) is treated as comparable. "
            "A missing measurement must be an error, never a silent pass -- that is how an "
            "unrun experiment ends up in a table."
        )

    def test_same_marker_id_twice_with_the_same_value_passes(self, tmp_path):
        code, rep = audit(
            tmp_path,
            "Test <!-- num:a -->0.812<!-- /num --> and dev <!-- num:a -->0.812<!-- /num -->.\n",
            results={"main.json": {"v": 0.812}},
        )
        assert code == 0, (
            "Reusing one id for two printings of the same stored value is legitimate (the same "
            "metric quoted twice); if this fails, authors are forced to duplicate index entries."
        )
        assert rep["n_matched"] == 2, "both occurrences must be MATCHed independently"

    def test_same_marker_id_twice_with_different_values_flags_one(self, tmp_path):
        code, rep = audit(
            tmp_path,
            "Test <!-- num:a -->0.812<!-- /num --> but dev <!-- num:a -->0.912<!-- /num -->.\n",
            results={"main.json": {"v": 0.812}},
        )
        assert code == 1, (
            "If this passes, one id can be reused for two different numbers and the wrong one "
            "is never reported -- a duplicated marker would launder a typo."
        )
        assert "0.912" in bad_tokens(rep), (
            "the occurrence that disagrees with the stored value must be the one reported; if "
            "the other one is reported, the finding points the author at the wrong sentence"
        )
        assert rep["n_matched"] == 1, "the agreeing occurrence must still MATCH"

    def test_toy_entry_with_a_wrong_value_reports_mismatch(self, tmp_path):
        entries = [{"id": "a", "file": "main.json", "key": "v", "toy": True}]
        code_bare, rep_bare = audit(
            tmp_path / "toy_bare", "<!-- num:a -->0.9<!-- /num -->\n",
            entries=entries, results={"main.json": {"v": 0.5}},
        )
        code_toy, rep_toy = audit(
            tmp_path / "toy_allowed", "<!-- num:a -->0.9<!-- /num -->\n",
            entries=entries, results={"main.json": {"v": 0.5}}, extra=("--allow-toy",),
        )
        assert code_bare == 1 and statuses(rep_bare) == ["MISMATCH"], (
            "A value disagreement must be reported as MISMATCH even for a toy entry: if it is "
            "reported as UNTRACEABLE/toy, the author 'fixes' it by adding --allow-toy and the "
            "wrong number then passes."
        )
        assert code_toy == 1 and statuses(rep_toy) == ["MISMATCH"], (
            "--allow-toy must relax only the toy provenance rule, never the value comparison: "
            "if this passes, a demo flag turns the audit into a rubber stamp."
        )


# --------------------------------------------------------------------------- 6. files


class TestFileHandling:
    """Encodings and layouts a real submission collects: CRLF, BOM, tabs, empties."""

    def test_si_unit_number_still_needs_a_marker(self, tmp_path):
        code_bad, rep_bad = audit(
            tmp_path / "si_bare", "Width \\SI{0.812}{} of the beam.\n",
            results={"main.json": {"v": 0.812}}, name="draft.tex",
        )
        code_ok, rep_ok = audit(
            tmp_path / "si_marked", "% num:a\n\\SI{0.812}{} of the beam.\n",
            results={"main.json": {"v": 0.812}}, name="draft.tex",
        )
        assert code_bad == 1 and "0.812" in bad_tokens(rep_bad), (
            "A number typeset by \\SI (siunitx) is printed text, so it must be traced like any "
            "other number; if this is silently exempt as a LaTeX command argument, the most "
            "common way to print a measurement in LaTeX bypasses the audit entirely."
        )
        assert code_ok == 0 and rep_ok["n_matched"] == 1, (
            "a `% num:id` above a \\SI line must bind the number inside the braces; if this "
            "fails, siunitx users cannot trace measurements at all"
        )

    def test_crlf_line_endings_preserve_values_and_line_numbers(self, tmp_path):
        text = "Line one.\r\nScore <!-- num:a -->0.812<!-- /num --> here.\r\nLine three.\r\n"
        code, rep = audit(tmp_path, text, results={"main.json": {"v": 0.812}})
        assert code == 0 and rep["n_matched"] == 1, (
            "CRLF (the default on Windows) must not break the marker: if this fails, every "
            "draft saved by a Windows editor fails the audit."
        )
        assert rep["matches"][0]["line"] == 2, (
            "the reported line must still be 2: if it is off by one, findings point the author "
            "at the wrong line and the report is useless"
        )
        assert rep["matches"][0]["token"] == "0.812", (
            "a stray CR must not be swallowed into the token text"
        )

    def test_utf8_bom_does_not_break_the_first_marker(self, tmp_path):
        code_md, rep_md = audit(
            tmp_path / "bom_md", "\ufeffScore: <!-- num:a -->0.5<!-- /num -->.\n",
        )
        code_tex, rep_tex = audit(
            tmp_path / "bom_tex", "\ufeff% num:a\n0.812 \\\\\n",
            results={"main.json": {"v": 0.812}}, name="draft.tex",
        )
        assert code_md == 0, (
            "A UTF-8 BOM at the start of a Markdown file must not hide the first marker; if "
            "this fails, the first number of every BOM-encoded file is untraceable."
        )
        assert code_tex == 0, (
            "A BOM before a `% num:id` line must not stop it matching; if this fails, LaTeX "
            "files saved by Windows tools cannot be audited."
        )

    def test_tabs_do_not_change_binding_or_columns(self, tmp_path):
        code, rep = audit(
            tmp_path, "\tScore:\t<!-- num:a -->0.5<!-- /num -->\n",
        )
        assert code == 0 and rep["n_matched"] == 1, (
            "Tabs are ordinary whitespace; if this fails, indented (tab-based) drafts cannot "
            "be audited and authors are pushed to reformat their source to satisfy the tool."
        )

    def test_empty_file_exits_zero_with_no_tokens(self, tmp_path):
        code_md, rep_md = audit(tmp_path / "empty_md", "")
        code_tex, rep_tex = audit(tmp_path / "empty_tex", "", name="draft.tex")
        for label, code, rep in (("markdown", code_md, rep_md), ("latex", code_tex, rep_tex)):
            assert code == 0, (
                "An empty %s draft has nothing to trace and must exit 0; if this fails, the "
                "tool crashes or reports a finding on a file that has no content." % label
            )
            assert rep["n_tokens"] == 0, (
                "an empty %s draft must scan zero tokens; a non-zero count means the reader "
                "invented content" % label
            )

    def test_directory_scan_audits_every_markdown_file_including_readme(self, tmp_path):
        code, rep = audit_dir(
            tmp_path,
            {
                "sub/sec.md": "Good <!-- num:a -->0.5<!-- /num -->\n",
                "sub/README.md": "# Notes\n\nWe once saw 0.912 in a log.\n",
                "sub/__pycache__/ignored.md": "0.777\n",
            },
        )
        assert rep["n_files"] == 2, (
            "Documented contract: a directory draft is scanned recursively for every .md/.tex "
            "file, skipping only VCS/cache dirs (SKIP_DIRS). If n_files is not 2, either the "
            "skip-list changed or README.md stopped being scanned -- note the consequence: a "
            "README placed under the draft directory is treated as a draft."
        )
        assert code == 1 and any(f["file"].endswith("README.md") for f in rep["findings"]), (
            "If this fails, a non-draft README's number is either silently skipped (so the "
            "scan is not the documented full scan) or the finding does not name the file. "
            "Either way the documented rule is: put drafts in a directory that contains only "
            "drafts, because every .md there is audited."
        )
        assert not any("__pycache__" in f["file"] for f in rep["findings"]), (
            "files under SKIP_DIRS must never be audited; if one is, build artefacts produce "
            "phantom findings"
        )
