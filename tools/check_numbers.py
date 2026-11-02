#!/usr/bin/env python
"""check_numbers.py — prove that every number in the draft came out of a results file.

WHY THIS EXISTS (RULES.md #2)
-----------------------------
A number in a paper that cannot be traced back to a logged run is either a typo or an
invention. Both are fatal, and neither is visible by reading: "0.812" looks exactly as
plausible as "0.821". This tool is the door every number has to walk through. It reads the
draft, finds every numeric token, and lets it pass only if

  (a) the author wrapped it in a traceability marker   (marked AND matching), or
  (b) the number is provably not a result              (exempt, by a named narrow rule).

Everything else is a finding, printed with file:line:col and the surrounding sentence so a
human can fix it in seconds without re-reading the paper.

THE TWO MARKER SYNTAXES
-----------------------
Markdown — the number is wrapped, so the marker cannot drift onto a neighbour:

    Our baseline reaches <!-- num:main.accuracy.baseline -->0.812<!-- /num --> test accuracy.

LaTeX — the marker is a comment on the line directly above the number, or a trailing
comment on the same line after the number (LaTeX cannot wrap a number in a comment):

    % num:main.accuracy.baseline
    0.812 & 0.790 & 0.781 \\

    0.812 \\  % num:main.accuracy.baseline

The id must exist in 04_experiments/RESULTS-INDEX.json (CONTRACTS.md §3). The printed value
must equal the value stored at `key` (a dotted path such as `accuracy` or `_meta.n`) inside
`file`. Percentages are the same number: storing 0.812 and printing `81.2%` is a MATCH, and
the evidence says so explicitly.

WHY A TOLERANCE AT ALL
----------------------
Stored 0.812345 printed as "0.812" is not a different result, it is the same result rounded
to three places. So a printed value is accepted when

    |printed - stored|  <=  max(entry tolerance, tolerance*|stored|, half of the last
                               decimal place printed)

Half of the last printed decimal place for "0.812" is 0.0005 — that is exactly how far
"0.812" may be from the true value and still be a correct 3-decimal rounding. Anything
outside that window is a real disagreement (0.912 vs stored 0.812 fails, as it must).

WHAT IS *NOT* A RESULT (exemptions, deliberately narrow)
--------------------------------------------------------
Years 1900–2100, section/figure/table/equation/algorithm numbers, citation numbers `[12]`,
DOIs, arXiv ids, URLs and file paths, ISO dates, page/line numbers, LaTeX ref/label/cite
keys and command arguments, LaTeX dimensions (`11pt`, `0.9\\textwidth`), markdown list
markers, and numbers named explicitly by an `--exempt` config file. Each rule is listed in
RULE_DOC below and printed in the report, so an exemption can never hide silently. Extra
patterns from the config file only exempt a number when the pattern's match actually covers
that number's characters, so a pattern that matches elsewhere on the line does nothing.

USAGE
-----
    python tools/check_numbers.py --draft 05_paper/draft/
    python tools/check_numbers.py --draft 05_paper/draft/main.md --json
    python tools/check_numbers.py --draft 05_paper/draft/ --allow-toy --out /tmp/audit.md
    python tools/check_numbers.py --draft d/ --index other.json --exempt my.json

Exit codes (CONTRACTS.md §6): 0 every number accounted for, 1 findings, 2 usage error.
Offline by design: this tool never makes a network call.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from bisect import bisect_right
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INDEX = REPO_ROOT / "04_experiments" / "RESULTS-INDEX.json"
DEFAULT_OUT = REPO_ROOT / "06_review" / "audits" / "numbers-audit.md"
DEFAULT_EXEMPT = REPO_ROOT / "04_experiments" / "config" / "exempt_numbers.json"

# A number whose index entry lives under this path is a TOY number: the pipeline is a
# labelled dry run, never a result (CONTRACTS.md §5). It is only accepted with --allow-toy.
TOY_PATH_MARKER = "04_experiments/toy/"

DRAFT_SUFFIXES = (".md", ".markdown", ".tex")
SKIP_DIRS = {".git", "__pycache__", "node_modules", "_tmp", ".pytest_cache"}

STATUS_MATCH = "MATCH"
STATUS_EXEMPT = "EXEMPT"
STATUS_UNTRACEABLE = "UNTRACEABLE"
STATUS_MISMATCH = "MISMATCH"
STATUS_DANGLING = "DANGLING_MARKER"
STATUS_INDEX_ERROR = "INDEX_ERROR"
STATUS_UNBOUND = "UNBOUND_MARKER"

# Statuses that make the run fail. A marker that wraps nothing is included: it usually
# means someone deleted the number and left the receipt, and a stale receipt is how a
# wrong number gets waved through later.
FINDING_STATUSES = {
    STATUS_UNTRACEABLE,
    STATUS_MISMATCH,
    STATUS_DANGLING,
    STATUS_INDEX_ERROR,
    STATUS_UNBOUND,
}


class UsageError(Exception):
    """Bad input (missing draft, unreadable index, malformed config) -> exit code 2."""


# --------------------------------------------------------------------------- rules

# One line of documentation per exemption rule: printed in the report, so the reader can
# see exactly why each number was let through. Narrow, named, and visible.
RULE_DOC: Dict[str, str] = {
    "year": "a bare 4-digit integer 1900-2100 (a calendar year, not a measurement)",
    "section_number": "numbering of a Markdown heading ('## 3.1 Method') or after §",
    "float_prefix": "number right after Figure/Table/Eq./Section/Algorithm/... (a label)",
    "page_line": "number after p./pp./page/line, including ranges (12-14)",
    "list_marker": "ordered-list numbering ('1.', '2)') at the start of a line",
    "citation_number": "bracketed citation numbers: [12], [3, 5], [12-14]",
    "doi": "digits inside a DOI (10.xxxx/...)",
    "arxiv_id": "arXiv identifier (arXiv:1706.03762)",
    "url": "digits inside an http(s):// or www. URL",
    "file_path": "digits inside a file path (fig/plot3.pdf)",
    "iso_date": "ISO date 2026-11-03",
    "footnote_marker": "markdown footnote reference [^1]",
    "latex_command_arg": "argument of \\ref \\label \\cite \\includegraphics \\begin ...",
    "latex_dimension": "LaTeX length: 11pt, 0.9\\textwidth, width=0.5\\linewidth",
    "identifier_attached": "digit glued to a name (GPT-4, ResNet-50, v2, L2)",
    "config_exempt": "number covered by a pattern in the --exempt config file",
}

# A numeric token: optional sign, digits with optional thousands separators, optional
# decimal part, optional exponent, optional %/x suffix. The lookbehind stops us from
# matching the tail of an identifier (ResNet50) or the middle of a version (v1.2.3);
# such glued digits are identifiers, not measurements.
NUMBER_RE = re.compile(
    r"""
    (?<![\w.])                                       # not glued to a word or a previous dot
    (?P<sign>[+\-\u2212\u00b1])?                     # + - (unicode minus) or +/- sign
    (?P<num>(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)
    (?P<exp>[eE][+\-]?\d+)?                          # 3e-4, 1.5E-3
    (?P<suffix>%|[x\u00d7])?                         # 12.3%   3.5x   3.5×
    """,
    re.VERBOSE,
)

PERCENT_WORD_RE = re.compile(r"\s?(?:percent\b|per\s+cent\b|pct\b)", re.I)

# Bracketed citation numbers. Integer lists/ranges only: "[0.812]" is not a citation.
CITATION_BRACKET_RE = re.compile(
    r"\[\s*\d+(?:\s*[-\u2013\u2014]\s*\d+)*(?:\s*,\s*\d+(?:\s*[-\u2013\u2014]\s*\d+)*)*\s*\]"
)

LATEX_ARG_CMDS = (
    "ref|eqref|autoref|cref|Cref|label|pageref|nameref|cite[a-zA-Z]*|bibitem|"
    "includegraphics|url|href|input|include|begin|end|bibliography|bibliographystyle|"
    "usepackage|documentclass|hspace|vspace|setlength|rule|multicolumn|multirow"
)
LATEX_ARG_RE = re.compile(
    r"\\(?:" + LATEX_ARG_CMDS + r")\*?(?:\[[^\]\n]*\])?\{[^{}\n]*\}"
)

# Things that are identifiers rather than measurements. Any token inside one of these
# spans is exempt; the span is recorded with its rule name for the report.
PROTECTED_PATTERNS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("url", re.compile(r"(?:https?://|www\.)[^\s<>\"'`)\]}]+")),
    ("doi", re.compile(r"\b10\.\d{4,9}/[^\s,;\"'<>)\]]+")),
    ("arxiv_id", re.compile(r"\barXiv[:\s]\s?\d{4}\.\d{4,5}(?:v\d+)?", re.I)),
    ("iso_date", re.compile(r"\b\d{4}-\d{2}-\d{2}\b")),
    ("citation_number", CITATION_BRACKET_RE),
    ("footnote_marker", re.compile(r"\[\^\d+\]")),
    (
        "file_path",
        re.compile(r"(?:[\w.\-]+/)+[\w.\-]+\.(?:png|jpe?g|pdf|svg|py|json|tex|md|csv|txt)\b"),
    ),
]

FLOAT_PREFIX_RE = re.compile(
    # The leading \b matters: without it "Ch\.?" matches the end of "reach ", and a metric
    # after any word ending in "ch" would be silently exempted as a chapter number.
    r"\b(?:Figure|Fig\.?|Figures|Figs\.?|Table|Tab\.?|Tables|Tabs\.?|Equation|Eq\.?|Eqs\.?|"
    r"Section|Sec\.?|Secs\.?|\u00a7+|\u00a7\u00a7|Appendix|App\.?|Algorithm|Alg\.?|"
    r"Listing|Chapter|Ch\.?|Step|Theorem|Thm\.?|Lemma|Definition|Def\.?|Remark|"
    r"Footnote|Panel|Column|Row)\s*~?\s*\(?\s*$",
    re.I,
)

# Range continuation: "pp. 12-14", "Figures 2-4", "Eqs. 3, 5-7".
RANGE_PREFIX_RE = re.compile(r"\d+\s*[-\u2013\u2014]\s*$")
PAGE_LINE_PREFIX_RE = re.compile(
    r"\b(?:p\.|pp\.|page|pages|line|lines)\s*~?\s*(?:\d+\s*[-\u2013\u2014]\s*)?$",
    re.I,
)

MD_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
MD_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s+)?\d{1,3}(?:\.\d{1,3})*[.)](?=\s)")

LATEX_DIM_SUFFIX_RE = re.compile(
    r"^\s*(?:pt|mm|cm|in|em|ex|bp|pc|sp|px|ms|s|min|GB|MB|KB)\b|"
    r"^\s*\\(?:textwidth|linewidth|columnwidth|textheight|baselineskip|tabcolsep)\b"
)
LATEX_DIM_PREFIX_RE = re.compile(r"(?:width|height|scale|angle)\s*=\s*$", re.I)

# "GPT-4", "ResNet-50": the digit hangs off a name, so it is part of the name.
IDENTIFIER_PREFIX_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]*)*[-_]?$")


# --------------------------------------------------------------------------- data


@dataclass
class Token:
    """One numeric token found in the draft, with enough geometry to print it precisely.

    Line and column are 1-based because that is what editors and `file:line:col` readers
    expect; offsets are 0-based byte-ish positions into the analysed text.
    """

    path: str          # path relative to the repo root, as shown to the human
    line: int
    col: int
    start: int
    end: int
    text: str
    value: Decimal     # numeric value normalised to "fraction" units (81.2% -> 0.812)
    half_ulp: Decimal  # half of the last printed decimal place, in the same units
    raw_value: Decimal  # the number exactly as printed (81.2 for "81.2%")
    percent: bool
    context: str
    status: str = ""
    rule: str = ""        # exemption rule or marker id
    reason: str = ""
    stored: Optional[Decimal] = None
    evidence: str = ""
    marker_id: str = ""


@dataclass
class Marker:
    """A `num:` traceability marker and the token(s) it is supposed to be vouching for."""

    marker_id: str
    line: int
    col: int
    start: int
    end: int
    style: str                     # "md" wrapped, "md-open", "tex-above", "tex-inline"
    bound: List[Token] = field(default_factory=list)


@dataclass
class IndexEntry:
    entry_id: str
    file: str
    key: str
    tolerance: Decimal
    description: str = ""
    run_id: str = ""
    resolved: Optional[Path] = None
    toy: bool = False   # entry is flagged `"toy": true` in the index


# --------------------------------------------------------------------------- helpers


def rel(path: Path) -> str:
    """Path as the human should see it: relative to the repo root when possible."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except (ValueError, OSError):
        return path.as_posix()


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def make_context(text: str, start: int, end: int, width: int = 60) -> str:
    """~`width` characters either side of the token, whitespace collapsed onto one line.

    Why collapse: the report is a table, and a context that contains newlines or runs of
    indentation is unreadable there. The token stays intact in the middle.
    """
    left = text[max(0, start - width):start]
    right = text[end:end + width]
    left = re.sub(r"\s+", " ", left)
    right = re.sub(r"\s+", " ", right)
    return (("\u2026" if start - width > 0 else "") + left + text[start:end] + right
            + ("\u2026" if end + width < len(text) else ""))


def line_starts(text: str) -> List[int]:
    starts = [0]
    for m in re.finditer(r"\n", text):
        starts.append(m.end())
    return starts


def pos_to_line_col(starts: Sequence[int], pos: int) -> Tuple[int, int]:
    """(1-based line, 1-based column) for a 0-based offset."""
    i = bisect_right(starts, pos) - 1
    if i < 0:
        i = 0
    return i + 1, pos - starts[i] + 1


def line_bounds(starts: Sequence[int], text_len: int, idx: int) -> Tuple[int, int]:
    """(start, end) offsets of the 0-based line number `idx`."""
    start = starts[idx]
    end = starts[idx + 1] - 1 if idx + 1 < len(starts) else text_len
    return start, end


# --------------------------------------------------------------------------- parsing


def parse_number(match: "re.Match[str]") -> Optional[Tuple[Decimal, Decimal, Decimal, bool]]:
    """Turn a NUMBER_RE match into (value, raw_value, half_ulp, percent).

    `value` is what we compare against the results file: "81.2%" becomes 0.812, because the
    stored metric is a fraction. `half_ulp` is half of the last decimal place *as printed*,
    also in fraction units, so "81.2%" gets 0.0005 and "0.8123" gets 0.00005.
    """
    raw = match.group("num").replace(",", "")
    if match.group("exp"):
        raw += match.group("exp")
    try:
        exact = Decimal(raw)
    except InvalidOperation:
        return None
    suffix = match.group("suffix") or ""
    percent = suffix == "%"
    if not percent:
        after = match.string[match.end():match.end() + 10]
        percent = bool(PERCENT_WORD_RE.match(after))
    # Decimal keeps the printed precision, including trailing zeros ("1.50" -> -2), which
    # is exactly the information we need for the rounding window. Floats would lose it.
    exponent = exact.as_tuple().exponent
    if not isinstance(exponent, int):  # 'n'/'N'/'F' cannot happen after the regex, but be safe
        return None
    half_ulp = Decimal(5) * (Decimal(10) ** (exponent - 1))
    if percent:
        value = exact / Decimal(100)
        half_ulp = half_ulp / Decimal(100)
    else:
        value = exact
    sign = match.group("sign") or ""
    if sign in ("-", "\u2212"):
        value, exact = -value, -exact
    return value, exact, half_ulp, percent


def comment_spans(text: str, kind: str) -> List[Tuple[int, int, str]]:
    """Every comment region: HTML comments in Markdown, `%` to end-of-line in LaTeX.

    Comments are blanked before the number scan. Without that, the id inside
    `<!-- num:main.accuracy.baseline -->` would itself look like a number ("1" in a name
    like "table1.p1") and get audited. Blanking (rather than deleting) keeps every offset
    in the file identical, so reported line/column numbers still match the editor.
    """
    spans: List[Tuple[int, int, str]] = []
    if kind == "md":
        for m in re.finditer(r"<!--.*?-->", text, re.S):
            spans.append((m.start(), m.end(), m.group(0)))
    else:
        # `\%` is a literal percent sign, not the start of a comment.
        for m in re.finditer(r"(?<!\\)%[^\n]*", text):
            spans.append((m.start(), m.end(), m.group(0)))
    return spans


def blank(text: str, spans: Iterable[Tuple[int, int, str]]) -> str:
    chars = list(text)
    for start, end, _ in spans:
        for i in range(start, end):
            if chars[i] not in "\r\n":
                chars[i] = " "
    return "".join(chars)


def scan_tokens(text: str, masked: str, path: str, width: int = 60) -> List[Token]:
    """All numeric tokens in the file, in reading order."""
    starts = line_starts(text)
    tokens: List[Token] = []
    for m in NUMBER_RE.finditer(masked):
        parsed = parse_number(m)
        if parsed is None:
            continue
        value, raw_value, half_ulp, percent = parsed
        line, col = pos_to_line_col(starts, m.start())
        tokens.append(
            Token(
                path=path,
                line=line,
                col=col,
                start=m.start(),
                end=m.end(),
                text=text[m.start():m.end()],
                value=value,
                half_ulp=half_ulp,
                raw_value=raw_value,
                percent=percent,
                context=make_context(text, m.start(), m.end(), width),
            )
        )
    return tokens


def find_markers(
    text: str, kind: str, spans: List[Tuple[int, int, str]], starts: Sequence[int]
) -> List[Marker]:
    """Collect `num:` markers, remembering whether they were wrapped or dangling-open.

    Markdown: `<!-- num:ID --> ... <!-- /num -->` is a wrapped pair. A `num:` comment with
    no closing tag binds the next number on the same or following lines (that is how the
    LaTeX form reads, and it keeps hand-written drafts usable); if there is no number after
    it, it binds the nearest number before it on the same line (a table cell).
    LaTeX: `% num:ID` binds the nearest number before it on its own line (trailing comment),
    or else the first number on the next non-blank, non-comment line.
    """
    markers: List[Marker] = []
    open_re = re.compile(r"<!--\s*num:\s*([A-Za-z0-9_.\-/]+)\s*-->")
    close_re = re.compile(r"<!--\s*/num\s*-->")

    if kind == "md":
        # Walk the comment spans in order and pair open/close tags. Pairing by order (not
        # by regex nesting) is enough because HTML comments cannot nest.
        pending: Optional[Marker] = None
        for start, end, raw in spans:
            m_open = open_re.match(raw)
            if m_open:
                line, col = pos_to_line_col(starts, start)
                pending = Marker(m_open.group(1), line, col, start, start + len(raw), "md-open")
                markers.append(pending)
                continue
            if close_re.match(raw):
                if pending is not None:
                    pending.style = "md"
                    pending.end = start  # the wrapped span ends where the closing tag starts
                    pending = None
                continue
        # The stored `end` for an unclosed marker stays at the tag end; binding handles it.
    else:
        tex_re = re.compile(r"^\s*%\s*num:\s*([A-Za-z0-9_.\-/]+)\s*$")
        for start, end, raw in spans:
            m = tex_re.match(raw)
            if not m:
                continue
            line, col = pos_to_line_col(starts, start)
            markers.append(Marker(m.group(1), line, col, start, end, "tex-raw"))
    return markers


def bind_markers(markers: List[Marker], tokens: List[Token], starts: Sequence[int]) -> None:
    """Attach each marker to the token(s) it vouches for. Fills `Marker.bound` in place."""
    by_line: Dict[int, List[Token]] = {}
    for t in tokens:
        by_line.setdefault(t.line, []).append(t)

    for mk in markers:
        if mk.style == "md":
            # Everything strictly inside the wrapped span belongs to this marker.
            mk.bound = [t for t in tokens if t.start >= mk.start and t.end <= mk.end]
            if not mk.bound:
                mk.style = "md-open"  # empty pair: treat like a bare marker for binding
        if mk.style == "md-open":
            after = [t for t in tokens if t.start >= mk.end]
            if after and after[0].start - mk.end <= 200 and after[0].line <= mk.line + 1:
                mk.bound = [after[0]]
                continue
            before = [t for t in by_line.get(mk.line, []) if t.end <= mk.start]
            mk.bound = before[-1:] if before else []
        elif mk.style == "tex-raw":
            on_line = [t for t in by_line.get(mk.line, []) if t.end <= mk.start]
            if on_line:
                # Trailing comment: the nearest number on the left is the annotated one.
                mk.bound = [on_line[-1]]
                mk.style = "tex-inline"
                continue
            # Otherwise look at the next line that has content and is not a comment.
            n_lines = len(starts)
            for idx in range(mk.line, min(mk.line + 4, n_lines)):  # mk.line is 1-based -> idx is the next line
                cand = [t for t in by_line.get(idx + 1, [])]
                if cand:
                    mk.bound = [cand[0]]
                    mk.style = "tex-above"
                    break


# --------------------------------------------------------------------------- index


def load_index(path: Path) -> Dict[str, IndexEntry]:
    """Read RESULTS-INDEX.json (CONTRACTS.md §3) into id -> entry, resolving each file.

    `file` is documented as relative to the repo root. Small drafts and the test fixtures
    keep their index next to their results, so when the repo-root reading does not exist we
    fall back to "relative to the index file's directory" — one documented fallback, tried
    only when the first path is missing, never a guess about which file was meant.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise UsageError(f"no such results index: {path}")
    except (json.JSONDecodeError, UnicodeDecodeError) as err:
        raise UsageError(f"results index is not valid JSON: {path}: {err}")

    entries_raw = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries_raw, list):
        raise UsageError(f"results index has no 'entries' list: {path}")

    out: Dict[str, IndexEntry] = {}
    for i, raw in enumerate(entries_raw, 1):
        if not isinstance(raw, dict):
            raise UsageError(f"index entry #{i} is not an object")
        for required in ("id", "file", "key"):
            if not isinstance(raw.get(required), str) or not raw[required]:
                raise UsageError(f"index entry #{i} is missing {required!r}")
        tol_raw = raw.get("tolerance", 0.0)
        try:
            tol = Decimal(str(tol_raw))
        except InvalidOperation:
            raise UsageError(f"index entry {raw['id']!r} has a non-numeric tolerance")
        entry = IndexEntry(
            entry_id=raw["id"],
            file=raw["file"],
            key=raw["key"],
            tolerance=tol,
            description=str(raw.get("description") or ""),
            run_id=str(raw.get("run_id") or ""),
            toy=raw.get("toy") is True,
        )
        as_root = (REPO_ROOT / entry.file)
        as_local = (path.parent / entry.file)
        entry.resolved = as_root if as_root.exists() else (as_local if as_local.exists() else as_root)
        out[entry.entry_id] = entry
    return out


def lookup_value(entry: IndexEntry) -> Tuple[Optional[Decimal], str, bool]:
    """Read `key` (dotted path) out of the entry's file.

    Returns (value, error_message, toy_file). `toy_file` is True when the results file itself
    carries the `"toy": true` marker, so a toy run cannot slip in just because it was copied
    to 04_experiments/results/summary_toy.json instead of staying under 04_experiments/toy/.
    """
    path = entry.resolved
    if path is None or not path.exists():
        return None, f"index entry {entry.entry_id!r} points at a missing file: {entry.file}", False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as err:
        return None, f"cannot read results file {rel(path)}: {err}", False
    toy_file = isinstance(data, dict) and data.get("toy") is True
    node = data
    for part in entry.key.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return None, f"key {entry.key!r} not found in {rel(path)}", toy_file
    if isinstance(node, bool) or node is None:
        return None, f"key {entry.key!r} in {rel(path)} is not a number ({node!r})", toy_file
    if isinstance(node, (int, float)):
        # str() on a float is repr()-shortest in Python 3, so 0.812 -> Decimal("0.812")
        # instead of the 0.8119999999999999 that binary floating point actually stores.
        return Decimal(str(node)), "", toy_file
    if isinstance(node, str):
        try:
            return Decimal(node.strip()), "", toy_file
        except InvalidOperation:
            return None, f"key {entry.key!r} in {rel(path)} is not numeric ({node!r})", toy_file
    return None, f"key {entry.key!r} in {rel(path)} is not a scalar", toy_file


# --------------------------------------------------------------------------- classify


def proportion_span(pos: int, spans: List[Tuple[int, int, str]]) -> Optional[str]:
    for start, end, rule in spans:
        if start <= pos < end:
            return rule
    return None


def protected_spans(masked: str, kind: str) -> List[Tuple[int, int, str]]:
    spans: List[Tuple[int, int, str]] = []
    for rule, pattern in PROTECTED_PATTERNS:
        for m in pattern.finditer(masked):
            spans.append((m.start(), m.end(), rule))
    if kind == "tex":
        for m in LATEX_ARG_RE.finditer(masked):
            spans.append((m.start(), m.end(), "latex_command_arg"))
    return spans


def exempt_rule(
    tok: Token,
    text: str,
    kind: str,
    spans: List[Tuple[int, int, str]],
    config_patterns: Sequence["re.Pattern[str]"],
) -> Optional[str]:
    """Name the narrow rule that makes this token not-a-result, or None.

    Order matters only in that the cheapest and most specific checks come first; every rule
    is meant to be tight enough that two of them never disagree.
    """
    hit = proportion_span(tok.start, spans)
    if hit:
        return hit

    line_start = text.rfind("\n", 0, tok.start) + 1
    line_end = text.find("\n", tok.end)
    if line_end < 0:
        line_end = len(text)
    line = text[line_start:line_end]
    prefix = text[max(line_start, tok.start - 40):tok.start]
    suffix = text[tok.end:line_end]

    # Years: a bare 4-digit integer in 1900..2100 with no decimal, sign, comma or suffix.
    if (
        re.fullmatch(r"\d{4}", tok.text)
        and tok.value == tok.raw_value
        and 1900 <= int(tok.raw_value) <= 2100
        and not tok.percent
    ):
        return "year"

    # Markdown heading numbering, and "§ 3.2" anywhere. The prefix has to include the token
    # itself ("## 4.1 Training" -> "4.1"), hence the +len(tok.text).
    heading = MD_HEADING_RE.match(line)
    if heading:
        in_heading = line[heading.end(): tok.end - line_start]
        if re.fullmatch(r"\s*(?:[A-Z]\.)?\d+(?:\.\d+)*\.?", in_heading):
            return "section_number"
    if re.search(r"\u00a7{1,2}\s*~?\s*$", prefix):
        return "section_number"

    # Ordered-list numbering at the start of a line.
    lm = MD_LIST_MARKER_RE.match(line)
    if lm and tok.start - line_start < lm.end():
        return "list_marker"

    # Figure/Table/Eq./Section labels, including ranges ("Figures 2-4", "pp. 12-14").
    if FLOAT_PREFIX_RE.search(prefix):
        return "float_prefix"
    range_hit = RANGE_PREFIX_RE.search(prefix)
    if range_hit:
        # "Figures 2-4": the tail of the prefix before the dash is a label, so this number
        # is the far end of a label range, not a measurement.
        head = prefix[: range_hit.start()]
        if FLOAT_PREFIX_RE.search(head):
            return "float_prefix"
        if PAGE_LINE_PREFIX_RE.search(head):
            return "page_line"

    if PAGE_LINE_PREFIX_RE.search(prefix):
        return "page_line"

    if kind == "tex":
        if LATEX_DIM_SUFFIX_RE.search(suffix) or LATEX_DIM_PREFIX_RE.search(prefix):
            return "latex_dimension"

    # "GPT-4", "ResNet-50", "v2": the digit is part of a name, and the name is not a number.
    m = IDENTIFIER_PREFIX_RE.search(prefix)
    if m and not tok.percent:
        tail = m.group(0)
        if tail.endswith(("-", "_")) or (m.end() == len(prefix) and tail[-1:].isalpha()):
            return "identifier_attached"

    # Explicit, documented config patterns. A pattern only exempts a number when its match
    # actually covers the number's characters — a pattern matching elsewhere on the line
    # does nothing, which is what keeps these narrow.
    for pattern in config_patterns:
        for m in pattern.finditer(line):
            if line_start + m.start() <= tok.start and line_start + m.end() >= tok.end:
                return "config_exempt"
    return None


# --------------------------------------------------------------------------- compare


def format_dec(d: Decimal) -> str:
    """Plain decimal string, no exponent, no trailing '.' — for reports."""
    s = format(d, "f")
    return s


def compare(tok: Token, entry: IndexEntry, stored: Decimal) -> Tuple[bool, str]:
    """Is the printed number the stored number? Returns (ok, evidence_string).

    The printed value is compared in "fraction" units (81.2% -> 0.812). Two readings are
    accepted for a percentage: the stored metric is a fraction (the normal case, CONTRACTS.md
    §2), or the stored metric is itself already in percent units (81.2). The evidence says
    which reading was used, so nobody has to guess later.

    The allowed slack is the largest of: the entry's tolerance read as absolute, the entry's
    tolerance read as relative (CONTRACTS.md §3 calls it relative), and half of the last
    decimal place printed — the rounding window. Never more than that.
    """
    tol = entry.tolerance
    tol_abs = abs(tol)
    tol_rel = abs(tol) * abs(stored)
    readings: List[Tuple[Decimal, Decimal, str]] = [(tok.value, tok.half_ulp, "fraction")]
    if tok.percent:
        # Alternative reading: the results file stores 81.2 rather than 0.812.
        readings.append((tok.raw_value, tok.half_ulp * Decimal(100), "percent"))

    best_reason = ""
    for printed, half_ulp, reading in readings:
        allowed = max(tol_abs, tol_rel, half_ulp)
        diff = abs(printed - stored)
        if diff <= allowed + Decimal("1e-12"):
            bits = [f"printed {tok.text!r} vs stored {format_dec(stored)}"]
            if tok.percent and reading == "fraction":
                bits.append(
                    f"percentage form: {format_dec(tok.raw_value)}/100 = {format_dec(printed)}, "
                    f"so {tok.text!r} is the same number as {format_dec(stored)}"
                )
            elif tok.percent and reading == "percent":
                bits.append("stored value is already in percent units")
            bits.append(
                f"diff {format_dec(diff)} <= allowed {format_dec(allowed)} "
                f"(half last decimal {format_dec(half_ulp)}, entry tolerance {format_dec(tol)})"
            )
            return True, "; ".join(bits)
        best_reason = (
            f"printed {tok.text!r} = {format_dec(printed)} but stored is {format_dec(stored)} "
            f"({entry.entry_id} = {entry.key} in {entry.file}); diff {format_dec(diff)} > "
            f"allowed {format_dec(max(tol_abs, tol_rel, half_ulp))}"
        )
    return False, best_reason


# --------------------------------------------------------------------------- audit


def iter_draft_files(draft: Path) -> List[Path]:
    if draft.is_file():
        if draft.suffix.lower() not in DRAFT_SUFFIXES:
            raise UsageError(
                f"{draft} is not a draft file (expected one of {', '.join(DRAFT_SUFFIXES)})"
            )
        return [draft]
    if not draft.is_dir():
        raise UsageError(f"no such draft file or directory: {draft}")
    files = []
    for p in sorted(draft.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in DRAFT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(draft).parts[:-1]):
            continue
        files.append(p)
    if not files:
        raise UsageError(f"no .md/.tex files found under {draft}")
    return files


def audit_file(
    path: Path,
    index: Dict[str, IndexEntry],
    config_patterns: Sequence["re.Pattern[str]"],
    allow_toy: bool,
    width: int,
) -> Tuple[List[Token], List[Marker]]:
    """Audit one draft file. Returns its tokens (with status filled in) and its markers."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as err:
        raise UsageError(f"{rel(path)} is not valid UTF-8: {err}")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    kind = "tex" if path.suffix.lower() == ".tex" else "md"

    spans = comment_spans(text, kind)
    masked = blank(text, spans)
    starts = line_starts(text)

    tokens = scan_tokens(text, masked, rel(path), width)
    markers = find_markers(text, kind, spans, starts)
    bind_markers(markers, tokens, starts)

    # marker id -> tokens it covers, plus which token is "first" for mismatch reporting
    covered: Dict[int, Marker] = {}
    for mk in markers:
        for t in mk.bound:
            covered[id(t)] = mk

    prot = protected_spans(masked, kind)

    for tok in tokens:
        mk = covered.get(id(tok))
        if mk is not None:
            tok.marker_id = mk.marker_id
            entry = index.get(mk.marker_id)
            if entry is None:
                tok.status = STATUS_DANGLING
                tok.reason = (
                    f"marker '{mk.marker_id}' is not in the results index — the number has "
                    f"no results file behind it"
                )
                continue
            stored, err, toy_file = lookup_value(entry)
            if stored is None:
                tok.status = STATUS_INDEX_ERROR
                tok.reason = f"index entry '{mk.marker_id}' is unusable: {err}"
                continue
            tok.stored = stored
            ok, evidence = compare(tok, entry, stored)
            tok.evidence = evidence
            if not ok:
                tok.status = STATUS_MISMATCH
                tok.reason = evidence
                continue
            is_toy = entry.toy or toy_file or TOY_PATH_MARKER in entry.file.replace("\\", "/")
            if is_toy and not allow_toy:
                tok.status = STATUS_UNTRACEABLE
                tok.reason = (
                    f"value comes from the toy pipeline ({entry.file}); toy output is labelled "
                    f"TOY, not a result (CONTRACTS.md §5). Pass --allow-toy only when "
                    f"deliberately demoing the pipeline"
                )
                continue
            tok.status = STATUS_MATCH
            tok.rule = mk.marker_id
            tok.reason = evidence
            continue

        rule = exempt_rule(tok, text, kind, prot, config_patterns)
        if rule:
            tok.status = STATUS_EXEMPT
            tok.rule = rule
            tok.reason = RULE_DOC.get(rule, rule)
            continue

        tok.status = STATUS_UNTRACEABLE
        tok.reason = (
            "no num: marker and no exemption rule matched — add "
            "<!-- num:<id> --> around it (or `% num:<id>` above it in LaTeX) with an entry "
            "in RESULTS-INDEX.json, or name it in the --exempt config"
        )

    # Markers that vouch for nothing. Usually a deleted number with a leftover receipt.
    for mk in markers:
        if not mk.bound:
            tokens.append(
                Token(
                    path=rel(path),
                    line=mk.line,
                    col=mk.col,
                    start=mk.start,
                    end=mk.end,
                    text="",
                    value=Decimal(0),
                    half_ulp=Decimal(0),
                    raw_value=Decimal(0),
                    percent=False,
                    context=make_context(text, mk.start, mk.end, width),
                    status=STATUS_UNBOUND,
                    rule=mk.marker_id,
                    reason=f"marker '{mk.marker_id}' wraps no number — delete it or mark the number",
                )
            )
    return tokens, markers


def audit(
    draft: Path,
    index_path: Path,
    exempt_path: Optional[Path],
    allow_toy: bool = False,
    width: int = 60,
) -> dict:
    """Run the whole audit and return the JSON-able report (see write_json/report_md)."""
    files = iter_draft_files(draft)
    index = load_index(index_path)
    patterns, pattern_source = load_exempt(exempt_path)

    all_tokens: List[Token] = []
    for f in files:
        toks, _ = audit_file(f, index, patterns, allow_toy, width)
        all_tokens.extend(toks)

    all_tokens.sort(key=lambda t: (t.path, t.line, t.col))
    findings = [t for t in all_tokens if t.status in FINDING_STATUSES]
    matches = [t for t in all_tokens if t.status == STATUS_MATCH]
    exempt = [t for t in all_tokens if t.status == STATUS_EXEMPT]

    rule_counts: Dict[str, int] = {}
    rule_examples: Dict[str, str] = {}
    for t in exempt:
        rule_counts[t.rule] = rule_counts.get(t.rule, 0) + 1
        rule_examples.setdefault(t.rule, t.text)

    return {
        "tool": "check_numbers",
        "version": 1,
        "generated_at": now_iso(),
        "draft": rel(draft),
        "index": rel(index_path),
        "exempt_config": rel(exempt_path) if exempt_path else None,
        "exempt_patterns": pattern_source,
        "allow_toy": bool(allow_toy),
        "files": [rel(f) for f in files],
        "n_files": len(files),
        "n_tokens": len(all_tokens),
        "n_matched": len(matches),
        "n_exempt": len(exempt),
        "n_findings": len(findings),
        "n_markers": sum(1 for t in all_tokens if t.marker_id),
        "counts": {
            s: sum(1 for t in all_tokens if t.status == s)
            for s in (
                STATUS_MATCH,
                STATUS_EXEMPT,
                STATUS_UNTRACEABLE,
                STATUS_MISMATCH,
                STATUS_DANGLING,
                STATUS_INDEX_ERROR,
                STATUS_UNBOUND,
            )
        },
        "exemptions": [
            {"rule": r, "count": c, "example": rule_examples.get(r, ""),
             "meaning": RULE_DOC.get(r, r)}
            for r, c in sorted(rule_counts.items())
        ],
        "findings": [token_dict(t) for t in findings],
        "matches": [token_dict(t) for t in matches],
        "ok": not findings,
    }


def token_dict(t: Token) -> dict:
    return {
        "file": t.path,
        "line": t.line,
        "col": t.col,
        "token": t.text,
        "status": t.status,
        "marker_id": t.marker_id or t.rule or "",
        "stored": format_dec(t.stored) if t.stored is not None else None,
        "reason": t.reason,
        "evidence": t.evidence,
        "context": t.context,
    }


def load_exempt(path: Optional[Path]) -> Tuple[List["re.Pattern[str]"], List[str]]:
    """Compile the `--exempt` config. Missing default config is fine; a broken one is not.

    The file is either a JSON list of regex strings, or an object with a "patterns" list
    (the shipped default is the object form so it can carry its own documentation). Each
    pattern is compiled up front: a bad regex in a config file must fail loudly at startup,
    not silently exempt nothing.
    """
    if path is None:
        return [], []
    if not path.exists():
        # The default file may legitimately be absent in a fresh checkout; an explicit
        # --exempt that does not exist is a typo and must not pass silently.
        if path == DEFAULT_EXEMPT:
            return [], []
        raise UsageError(f"no such exempt config: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as err:
        raise UsageError(f"exempt config is not valid JSON: {path}: {err}")
    if isinstance(data, dict):
        raw_patterns = data.get("patterns")
        if not isinstance(raw_patterns, list):
            raise UsageError(f'exempt config object needs a "patterns" list: {path}')
    elif isinstance(data, list):
        raw_patterns = data
    else:
        raise UsageError(f"exempt config must be a JSON list or an object with 'patterns': {path}")

    compiled: List["re.Pattern[str]"] = []
    for i, item in enumerate(raw_patterns, 1):
        if not isinstance(item, str) or not item:
            raise UsageError(f"exempt config pattern #{i} is not a non-empty string: {path}")
        try:
            compiled.append(re.compile(item))
        except re.error as err:
            raise UsageError(f"exempt config pattern #{i} is not a valid regex: {err}")
    return compiled, [p.pattern for p in compiled]


# --------------------------------------------------------------------------- outputs


def write_json(report: dict, path: Optional[Path]) -> None:
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False)
    if path is None:
        print(text)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def write_report_md(report: dict, path: Path) -> None:
    c = report["counts"]
    verdict = "**PASS**" if report["ok"] else "**FAIL**"
    draft_path = str(report["draft"]).replace("\\", "/")
    is_paper = "05_paper/draft" in draft_path
    scope = (
        "a PAPER draft: this PASS can be quoted as evidence that the draft's numbers are "
        "traceable"
        if is_paper
        else "NOT a paper draft (fixture / toy / template path): a PASS here says the tool "
        "works, NOT that any draft passed its audit"
    )
    lines = [
        "# Numbers audit",
        "",
        f"> **Scope: {scope}.**", 
        f"> Audited path: `{report['draft']}`",
        "",
        f"Draft: `{report['draft']}`  ",
        f"Index: `{report['index']}`  ",
        f"Generated: {report['generated_at']}  ",
        f"Toy numbers allowed: {report['allow_toy']}",
        "",
        f"{verdict} — {report['n_findings']} finding(s) over {report['n_files']} file(s).",
        "",
        "| scanned | matched | exempt | untraceable | mismatch | dangling | index error | "
        "unbound |",
        "|---|---|---|---|---|---|---|---|",
        f"| {report['n_tokens']} | {c['MATCH']} | {c['EXEMPT']} | {c['UNTRACEABLE']} | "
        f"{c['MISMATCH']} | {c['DANGLING_MARKER']} | {c['INDEX_ERROR']} | "
        f"{c['UNBOUND_MARKER']} |",
        "",
    ]

    if report["findings"]:
        lines += [
            "## Findings",
            "",
            "| # | where | token | status | why |",
            "|---|-------|-------|--------|-----|",
        ]
        for i, f in enumerate(report["findings"], 1):
            why = (f["reason"] or "").replace("|", "/").replace("\n", " ")
            where = f"`{f['file']}:{f['line']}:{f['col']}`"
            lines.append(f"| {i} | {where} | `{f['token'] or '-'}` | **{f['status']}** | {why} |")
        lines += ["", "### Where they are", ""]
        for f in report["findings"]:
            lines.append(f"- `{f['file']}:{f['line']}:{f['col']}` **{f['status']}** "
                         f"`{f['token'] or '-'}` — {f['reason']}")
            lines.append(f"  > {f['context']}")
        lines.append("")
    else:
        lines += ["## Findings", "", "None. Every numeric token is marked-and-matching or exempt.", ""]

    if report["matches"]:
        lines += [
            "## Matched numbers",
            "",
            "| where | printed | marker | stored | evidence |",
            "|-------|---------|--------|--------|----------|",
        ]
        for m in report["matches"]:
            ev = (m["evidence"] or "").replace("|", "/")
            lines.append(
                f"| `{m['file']}:{m['line']}` | `{m['token']}` | `{m['marker_id']}` | "
                f"`{m['stored']}` | {ev} |"
            )
        lines.append("")

    if report["exemptions"]:
        lines += [
            "## Exemptions used",
            "",
            "| rule | count | example | why it is not a result |",
            "|------|-------|---------|------------------------|",
        ]
        for e in report["exemptions"]:
            lines.append(
                f"| `{e['rule']}` | {e['count']} | `{e['example']}` | "
                f"{(e['meaning'] or '').replace('|', '/')} |"
            )
        lines.append("")

    lines += [
        "## Rules this run applied",
        "",
        "Exemptions are narrow by construction: each rule below is a named, fixed pattern in "
        "`tools/check_numbers.py` (or a pattern you supplied via `--exempt`). No catch-all.",
        "",
    ]
    for rule, meaning in RULE_DOC.items():
        lines.append(f"- `{rule}` — {meaning}")
    if report["exempt_patterns"]:
        lines += ["", f"Extra patterns from `{report['exempt_config']}`:", ""]
        for p in report["exempt_patterns"]:
            lines.append(f"- `{p}`")
    lines += [
        "",
        "A number passes only if it is inside a `num:` marker whose id is in the results "
        "index and whose stored value matches (percentages allowed, rounding allowed up to "
        "half of the last printed decimal place), or if one of the rules above applies. "
        "Everything else must be fixed before the draft is called done (RULES.md #2).",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="check_numbers.py",
        description="Prove every number in a draft traces to a results file (RULES.md #2).",
        epilog="Exit codes: 0 clean, 1 findings, 2 usage error.",
    )
    ap.add_argument("--draft", type=Path, required=True,
                    help="draft file (.md/.tex) or directory to scan (e.g. 05_paper/draft/)")
    ap.add_argument("--index", type=Path, default=DEFAULT_INDEX,
                    help=f"results index (default: {rel(DEFAULT_INDEX)})")
    ap.add_argument("--exempt", type=Path, default=DEFAULT_EXEMPT,
                    help=f"JSON list of extra exemption regexes (default: {rel(DEFAULT_EXEMPT)})")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"Markdown report path (default: {rel(DEFAULT_OUT)})")
    ap.add_argument("--no-write", action="store_true", help="do not write the Markdown report")
    ap.add_argument("--json", action="store_true", help="print the report as JSON to stdout")
    ap.add_argument("--json-out", type=Path, default=None, help="also write the JSON report here")
    ap.add_argument("--allow-toy", action="store_true",
                    help="accept numbers whose index entry lives under 04_experiments/toy/")
    ap.add_argument("--context", type=int, default=60,
                    help="characters of context to show either side of a token (default 60)")
    ap.add_argument("--quiet", action="store_true", help="no human-readable stdout summary")
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.context < 0:
        print("error: --context must be >= 0", file=sys.stderr)
        return 2

    try:
        report = audit(
            draft=args.draft,
            index_path=args.index,
            exempt_path=args.exempt,
            allow_toy=args.allow_toy,
            width=args.context,
        )
    except UsageError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2

    if not args.no_write:
        write_report_md(report, args.out)
    if args.json_out:
        write_json(report, args.json_out)
    if args.json:
        write_json(report, None)

    if not args.quiet:
        c = report["counts"]
        print(
            f"{report['n_tokens']} number(s) in {report['n_files']} file(s): "
            f"{c['MATCH']} matched, {c['EXEMPT']} exempt, {report['n_findings']} finding(s)",
            file=sys.stderr,
        )
        for f in report["findings"][:20]:
            print(f"  {f['file']}:{f['line']}:{f['col']}  {f['status']:<16} {f['token'] or '-'}",
                  file=sys.stderr)
        if len(report["findings"]) > 20:
            print(f"  ... and {len(report['findings']) - 20} more (see the report)",
                  file=sys.stderr)
        if not args.no_write:
            print(f"report -> {args.out}", file=sys.stderr)
        print("PASS — every number is accounted for" if report["ok"] else "FAIL — findings above",
              file=sys.stderr)

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
