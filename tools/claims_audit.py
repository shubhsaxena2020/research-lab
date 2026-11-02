#!/usr/bin/env python
"""claims_audit.py — mechanically verify that every abstract/introduction claim is backed.

RULES.md #5 says claims are calibrated; RULES.md #2 says every number comes from a result file.
This tool is the enforcement: each row of the claims-audit table names one claim, the evidence
file, the key inside it, the command that produced it, the printed value, and a human verdict.
The tool re-checks all of that from disk and refuses to take "verified: YES" on trust.

    python tools/claims_audit.py \
        --audit 06_review/CLAIMS-AUDIT.md \
        --draft 05_paper/draft/ \
        --index 04_experiments/RESULTS-INDEX.json \
        --citations 02_literature/verified_citations.csv

Per row:
    * evidence_file exists (relative to --root, or absolute);
    * evidence_key resolves inside that file
        - .json : dotted path, list indices as [i]  (e.g. "_meta.n", "paired.p_value")
        - .csv  : "column=value" row selector, optional "#column" to pick the value
                  (default value column: "status" if present, else the selector value)
        - .md/.txt : evidence_key is a literal phrase that must occur in the file
    * the stored value agrees with result_value
        numeric  : |stored - printed| <= tol * |stored|     (tol = index entry tolerance,
                   else 1% relative; a trailing "%" in result_value is converted)
        string   : case/whitespace-insensitive equality
        text file: a non-empty result_value must also occur in the file
    * any citation key cited by the row ([@key] or \\cite{key}) is in verified_citations.csv
      with status VERIFIED;
    * verified is exactly YES.

Across the draft (abstract + introduction of every .md/.tex under --draft):
    * every quantitative or comparative sentence (a digit, or a trigger word) must fuzzy-match
      a row's claim text; unmatched ones are reported UNCOVERED with file:line;
    * "state of the art" / "novel" / "first" must have a matching row whose evidence_file is
      02_literature/NOVELTY-CHECK.md, else NOVELTY_ROW_MISSING.

Matching rule (coverage): sentences and row claims are lowercased, citation markers and
punctuation are dropped, then scored max(Dice token overlap, containment). Containment counts
only when the shorter side has >= 5 tokens. Threshold COVERAGE_THRESHOLD = 0.80 — verbatim
claims score 1.00; a paraphrase of one clause usually lands 0.55-0.75 and is correctly rejected.

Rows whose claim_id starts with "EX-" are worked examples: they are skipped entirely (not
judged, not used for coverage), and counted separately in the output.

Exit codes: 0 every row verified and coverage complete, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import citation_schema  # noqa: E402  (shared one-schema mapping; see CONTRACTS §1)

REPO_ROOT = Path(__file__).resolve().parents[1]

COLUMNS = (
    "claim_id",
    "claim",
    "section",
    "evidence_file",
    "evidence_key",
    "command",
    "result_value",
    "verified",
    "limitation",
    "reviewer",
)
REQUIRED_FIELDS = (
    "claim_id",
    "claim",
    "section",
    "evidence_file",
    "evidence_key",
    "command",
    "result_value",
    "verified",
)

COVERAGE_THRESHOLD = 0.80
DEFAULT_REL_TOL = 0.01
NOVELTY_FILE = "NOVELTY-CHECK.md"

# A sentence is "quantitative or comparative" if it has a digit or one of these stems.
TRIGGER_STEMS = (
    "outperform",
    "improve",
    "reduc",
    "increas",
    "novel",
    "state-of-the-art",
    "state of the art",
    "first",
    "sota",
    "better than",
    "superior",
    "gain",
    "speedup",
    "faster",
    "cheaper",
)
NUM_RE = re.compile(r"(?<![A-Za-z])\d")
CITE_RE = re.compile(r"\[@([^\]]+)\]|\\cite[pt]?\{([^}]+)\}")
_WORD_RE = re.compile(r"[a-z][a-z0-9'\-]*")
# "novel"/"state of the art" are novelty claims wherever they appear. Bare "first" is not:
# "First, we load the data" is an enumeration, not a priority claim. Only flag "first" when
# it is used to claim priority (first to / first work / first paper ...).
FORBIDDEN_RE = re.compile(
    r"\bstate[- ]of[- ]the[- ]art\b|\bnovel\b"
    r"|\bfirst\s+(?:to|work|study|paper|approach|method|system)\b",
    re.IGNORECASE,
)


class AuditParseError(Exception):
    pass


# --------------------------------------------------------------------------- markdown table


def _ends_with_pipe(line: str) -> bool:
    s = line.rstrip()
    if not s.endswith("|"):
        return False
    n, i = 0, len(s) - 2
    while i >= 0 and s[i] == "\\":
        n += 1
        i -= 1
    return n % 2 == 0


def _split_row(line: str) -> List[str]:
    """Split a markdown table row on unescaped pipes, ignoring pipes inside `code spans`."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    cells: List[str] = []
    cur: List[str] = []
    in_code = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
            cur.append(ch)
            i += 1
            continue
        if ch == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    tail = "".join(cur).strip()
    if tail:
        cells.append(tail)
    return cells


def _norm_header(cell: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", cell.strip().strip("*").lower()).strip("_")


def parse_audit_table(text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    lines = text.splitlines()
    header_idx = None
    for idx, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        cells = {_norm_header(c) for c in _split_row(line)}
        # a documentation table may also mention claim_id, so require most of the real columns
        if "claim_id" in cells and len([c for c in REQUIRED_FIELDS if c in cells]) >= 4:
            header_idx = idx
            break
    if header_idx is None:
        raise AuditParseError("no markdown table with a 'claim_id' column found")

    header = [_norm_header(c) for c in _split_row(lines[header_idx])]
    missing = [c for c in REQUIRED_FIELDS if c not in header]
    if missing:
        raise AuditParseError(f"table is missing required column(s): {', '.join(missing)}")
    pos = {name: i for i, name in enumerate(header) if name}

    warnings: List[str] = []
    rows: List[Dict[str, Any]] = []
    i = header_idx + 1
    if i < len(lines) and re.fullmatch(r"[|\s:=-]+", lines[i].strip()):
        i += 1

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s.startswith("|"):
            break
        start_line = i + 1
        buf = s
        truncated = False
        while not _ends_with_pipe(buf):
            j = i + 1
            if j >= len(lines):
                break
            nxt = lines[j].strip()
            if not nxt:
                break
            if nxt.startswith("|") or nxt.startswith("#"):
                truncated = True
                break
            buf = buf + " " + nxt
            i = j
        cells = _split_row(buf)
        i += 1
        if not cells or all(re.fullmatch(r"[-: ]*", c) for c in cells):
            continue
        if truncated:
            warnings.append(f"line {start_line}: row does not end with '|'; stopped at next table line")
        if len(cells) > len(header):
            # almost always an unescaped pipe inside the (long) claim cell: re-join it
            extra = len(cells) - len(header)
            cells = cells[:1] + [" | ".join(cells[1 : 2 + extra])] + cells[2 + extra :]
            warnings.append(f"line {start_line}: {extra} extra cell(s) merged back into 'claim'")
        if len(cells) < len(header):
            cells = cells + [""] * (len(header) - len(cells))
        row: Dict[str, Any] = {"_line": start_line}
        for name, col in pos.items():
            row[name] = cells[col].strip()
        rows.append(row)
    return rows, warnings


# --------------------------------------------------------------------------- evidence lookup


def _resolve_dotted(obj: Any, path: str) -> Tuple[bool, Any]:
    parts: List[Any] = []
    for m in re.finditer(r"([^.\[\]]+)|\[(\d+)\]", path):
        parts.append(int(m.group(2)) if m.group(2) is not None else m.group(1))
    if not parts:
        return False, None
    cur = obj
    for part in parts:
        if isinstance(part, int):
            if not isinstance(cur, list) or part >= len(cur):
                return False, None
            cur = cur[part]
        else:
            if not isinstance(cur, dict) or part not in cur:
                return False, None
            cur = cur[part]
    return True, cur


def _resolve_csv(path: Path, selector: str) -> Tuple[bool, Any, str]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if not fieldnames:
        return False, None, "csv has no header"
    value_col = None
    if "#" in selector:
        selector, value_col = selector.split("#", 1)
    if "=" in selector:
        col, wanted = selector.split("=", 1)
    else:
        col, wanted = fieldnames[0], selector
    col = col.strip()
    wanted = wanted.strip()
    hits = [r for r in rows if (r.get(col) or "").strip() == wanted]
    if not hits:
        return False, None, f"no row where {col} == {wanted!r}"
    if value_col:
        if value_col not in fieldnames:
            return False, None, f"no column {value_col!r}"
        return True, hits[0].get(value_col), ""
    if "status" in fieldnames:
        return True, hits[0].get("status"), ""
    return True, wanted, ""


def _fmt(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def _looks_numeric(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _parse_printed(text: str) -> Optional[Tuple[float, bool]]:
    t = text.strip().strip("`\"'")
    pct = t.endswith("%")
    t = t.replace(",", "").replace("±", " ").replace("~", " ")
    m = re.search(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", t)
    if not m:
        return None
    try:
        return float(m.group(0)), pct
    except ValueError:
        return None


def _norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ")).strip().lower()


def compare_values(stored: Any, printed: str, tol: float) -> Tuple[bool, str]:
    printed = (printed or "").strip()
    if not printed:
        return True, "no result_value to compare"
    if _looks_numeric(stored):
        parsed = _parse_printed(printed)
        if parsed is None:
            return False, f"result_value {printed!r} is not numeric but stored value is {_fmt(stored)}"
        num, pct = parsed
        if pct and abs(float(stored)) <= 1.0 and abs(num) > 1.0:
            num = num / 100.0
        diff = abs(float(stored) - num)
        limit = max(tol * abs(float(stored)), 1e-12)
        ok = diff <= limit
        return ok, (
            f"stored {_fmt(stored)} vs printed {num:g}: diff {diff:g} "
            f"{'<=' if ok else '>'} tol {limit:g}"
        )
    stored_str = _fmt(stored)
    ok = _norm_text(stored_str) == _norm_text(printed)
    return ok, f"stored {stored_str!r} vs printed {printed!r} ({'equal' if ok else 'differ'})"


def _evidence_tolerance(index: Dict[str, Any], evidence_file: str, key: str) -> Optional[float]:
    want_file = _norm_rel(evidence_file)
    for entry in index.get("entries", []):
        if _norm_rel(str(entry.get("file", ""))) == want_file and str(entry.get("key", "")) == key:
            tol = entry.get("tolerance")
            if isinstance(tol, (int, float)):
                return float(tol)
    return None


def _norm_rel(p: str) -> str:
    return str(p).replace("\\", "/").lstrip("./").lower()


# --------------------------------------------------------------------------- draft reading


def _md_sections(text: str) -> List[Tuple[str, str, int]]:
    heads = [
        (m.start(), m.end(), m.group(2).strip())
        for m in re.finditer(r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", text)
    ]
    out = []
    for idx, (start, end, title) in enumerate(heads):
        body_end = heads[idx + 1][0] if idx + 1 < len(heads) else len(text)
        out.append((title, text[end:body_end], end))
    return out


def _tex_sections(text: str) -> List[Tuple[str, str, int]]:
    out: List[Tuple[str, str, int]] = []
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S)
    if m:
        out.append(("Abstract", m.group(1), m.start(1)))
    heads = [(mm.start(), mm.end(), mm.group(1)) for mm in re.finditer(r"\\section\*?\{([^}]*)\}", text)]
    for idx, (start, end, title) in enumerate(heads):
        body_end = heads[idx + 1][0] if idx + 1 < len(heads) else len(text)
        out.append((title, text[end:body_end], end))
    return out


def _section_kind(title: str) -> Optional[str]:
    t = _norm_text(title)
    t = re.sub(r"^[0-9ivx]+[.)]?\s+", "", t)
    if "abstract" in t:
        return "abstract"
    if t.startswith("introduction") or t == "intro":
        return "intro"
    return None


def _split_sentences(text: str) -> List[Tuple[int, int, str]]:
    """Sentence spans, with decimal points and 'Fig. 2' style abbreviations left intact."""
    bounds: List[Tuple[int, int]] = []
    start = 0
    for m in re.finditer(r"[.!?]", text):
        i = m.start()
        if i > 0 and text[i - 1].isdigit() and i + 1 < len(text) and text[i + 1].isdigit():
            continue  # decimal point (0.812), not a sentence break
        j = i + 1
        while j < len(text) and text[j] in "\"')]":
            j += 1
        if j >= len(text) or not text[j].isspace():
            continue
        k = j
        while k < len(text) and text[k].isspace():
            k += 1
        if k >= len(text):
            break
        nxt = text[k]
        if not (nxt.isupper() or nxt.isdigit() or nxt in "([\""):
            continue
        bounds.append((start, k))
        start = k
    bounds.append((start, len(text)))
    out = []
    for s, e in bounds:
        chunk = text[s:e]
        if chunk.strip():
            lead = len(chunk) - len(chunk.lstrip())
            out.append((s + lead, e, chunk.strip()))
    return out


def _line_of(text: str, line_starts: List[int], offset: int) -> int:
    return bisect.bisect_right(line_starts, offset)


def _trigger(text: str) -> Optional[str]:
    # a citation key like [@vaswani2017] carries a year but is not a quantitative claim
    cleaned = re.sub(r"\[@[^\]]*\]|\\cite[pt]?\{[^}]*\}", " ", text)
    low = cleaned.lower()
    m = NUM_RE.search(cleaned)
    if m:
        return f"number {m.group(0)!r}"
    # Match stems on WORD PREFIXES, never as raw substrings: a naive `stem in low`
    # flags the sentence "we compare A against B" because "against" contains "gain",
    # which turns every comparison sentence into an uncovered claim. Prefix matching
    # still catches gain/gains/gained and outperform/outperforms.
    words = _WORD_RE.findall(low)
    for stem in TRIGGER_STEMS:
        if " " in stem or "-" in stem:
            if re.search(r"(?<![a-z0-9])" + re.escape(stem) + r"(?![a-z0-9])", low):
                return f"word {stem!r}"
        else:
            for w in words:
                if w.startswith(stem):
                    return f"word {stem!r}"
    return None


def _tokens(s: str) -> List[str]:
    s = re.sub(r"\[@[^\]]*\]|\\cite[pt]?\{[^}]*\}", " ", s)
    s = re.sub(r"[`*_#>~]", " ", s.lower())
    s = re.sub(r"[^a-z0-9.%\s-]", " ", s)
    return [t for t in s.split() if t.strip(".-")]


def similarity(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    inter = len(sa & sb)
    dice = 2.0 * inter / (len(sa) + len(sb))
    cont = inter / min(len(sa), len(sb)) if min(len(sa), len(sb)) >= 5 else 0.0
    return max(dice, cont)


def collect_draft_claims(draft: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    files: List[Path] = []
    if draft.is_dir():
        for pat in ("*.md", "*.tex", "*.markdown"):
            files.extend(sorted(draft.rglob(pat)))
    else:
        files = [draft]
    claims: List[Dict[str, Any]] = []
    warnings: List[str] = []
    kinds_seen = set()
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:  # pragma: no cover - unreadable file
            warnings.append(f"{path}: {exc}")
            continue
        sections = _tex_sections(text) if path.suffix.lower() == ".tex" else _md_sections(text)
        line_starts = [0] + [m.end() for m in re.finditer(r"\n", text)]
        for title, body, offset in sections:
            kind = _section_kind(title)
            if kind is None:
                continue
            kinds_seen.add(kind)
            for s, _e, sentence in _split_sentences(body):
                reason = _trigger(sentence)
                if reason is None:
                    continue
                claims.append(
                    {
                        "file": str(path),
                        "line": _line_of(text, line_starts, offset + s),
                        "section": kind,
                        "text": sentence,
                        "why": reason,
                    }
                )
    if "abstract" not in kinds_seen:
        warnings.append("no abstract section found in the draft")
    if "intro" not in kinds_seen:
        warnings.append("no introduction section found in the draft")
    return claims, warnings


# --------------------------------------------------------------------------- citations


def load_verified_keys(path: Path) -> Dict[str, str]:
    """key -> status, from either register schema (see tools/lib/citation_schema.py).

    The canonical file has no `status` column because every row in it is verified; a row
    whose only provenance is `verified_by_command` therefore counts as VERIFIED. Before this
    normalisation, the canonical file collapsed to a single empty key and *no* citation could
    ever read VERIFIED, which would have blocked every paper claim.
    """
    with path.open(encoding="utf-8-sig", newline="") as fh:
        out: Dict[str, str] = {}
        for row in csv.DictReader(fh):
            n = citation_schema.normalize_row({k: (v or "") for k, v in row.items() if k})
            key = (n["key"] or "").strip()
            if not key:
                continue
            out[key] = (n["status"] or "").strip().upper()
        return out


def keys_in(text: str) -> List[str]:
    out: List[str] = []
    for m in CITE_RE.finditer(text or ""):
        chunk = m.group(1) or m.group(2) or ""
        for part in re.split(r"[;,]", chunk):
            part = part.strip().lstrip("@")
            if part:
                out.append(part)
    return out


# --------------------------------------------------------------------------- audit


def audit(
    audit_path: Path,
    draft: Path,
    index_path: Path,
    citations_path: Path,
    root: Path,
) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []

    def add(code: str, detail: str, row_id: Optional[str] = None, file: Optional[str] = None, line: Optional[int] = None):
        findings.append({"code": code, "row_id": row_id, "detail": detail, "file": file, "line": line})

    text = audit_path.read_text(encoding="utf-8")
    rows, warnings = parse_audit_table(text)
    for w in warnings:
        add("TABLE_WARNING", w, file=str(audit_path))

    index = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(index, dict) or "entries" not in index:
        raise AuditParseError(f"{index_path} is not a RESULTS-INDEX.json (needs an 'entries' list)")
    verified = load_verified_keys(citations_path)

    checked: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    seen_ids: Dict[str, int] = {}
    judged_claims: List[Dict[str, Any]] = []

    for row in rows:
        rid = (row.get("claim_id") or "").strip()
        if rid.upper().startswith("EX-"):
            row["_status"] = "SKIP"
            row["_findings"] = []
            skipped.append(row)
            continue
        if not rid:
            add("ROW_MISSING_FIELD", "row has no claim_id", row_id="(blank)", file=str(audit_path), line=row["_line"])
            continue
        if rid in seen_ids:
            add("ROW_DUPLICATE_ID", f"claim_id {rid} already used on line {seen_ids[rid]}",
                row_id=rid, file=str(audit_path), line=row["_line"])
        else:
            seen_ids[rid] = row["_line"]

        row_findings: List[str] = []

        def fail(code: str, detail: str):
            row_findings.append(code)
            add(code, detail, row_id=rid, file=str(audit_path), line=row["_line"])

        for field in REQUIRED_FIELDS:
            if not (row.get(field) or "").strip():
                fail("ROW_MISSING_FIELD", f"required field '{field}' is empty")

        verified_flag = (row.get("verified") or "").strip().upper()
        if verified_flag != "YES":
            fail("ROW_NOT_VERIFIED", f"verified={row.get('verified')!r}; must be YES")

        ev_file = (row.get("evidence_file") or "").strip().strip("`")
        ev_key = (row.get("evidence_key") or "").strip().strip("`")
        result_value = (row.get("result_value") or "").strip()
        stored: Any = None
        resolved = False
        value_checked = False

        if ev_file:
            p = Path(ev_file)
            candidates = [p] if p.is_absolute() else [root / ev_file, audit_path.parent / ev_file]
            path = next((c for c in candidates if c.exists()), None)
            if path is None:
                fail("ROW_MISSING_FILE", f"evidence_file not found: {ev_file}")
            else:
                suffix = path.suffix.lower()
                if suffix == ".json":
                    if not ev_key:
                        fail("ROW_MISSING_FIELD", "evidence_key empty for a JSON evidence file")
                    else:
                        try:
                            data = json.loads(path.read_text(encoding="utf-8"))
                        except (OSError, json.JSONDecodeError) as exc:
                            fail("ROW_BAD_EVIDENCE", f"cannot read JSON {ev_file}: {exc}")
                            data = None
                        if data is not None:
                            ok, stored = _resolve_dotted(data, ev_key)
                            if not ok:
                                fail("ROW_KEY_MISSING", f"key {ev_key!r} does not resolve in {ev_file}")
                            else:
                                resolved = True
                elif suffix == ".csv":
                    try:
                        ok, stored, why = _resolve_csv(path, ev_key)
                    except OSError as exc:  # pragma: no cover
                        ok, stored, why = False, None, str(exc)
                    if not ok:
                        fail("ROW_KEY_MISSING", f"{ev_key!r} not resolvable in {ev_file}: {why}")
                    else:
                        resolved = True
                elif suffix in (".md", ".markdown", ".txt"):
                    body = path.read_text(encoding="utf-8")
                    if ev_key and _norm_text(ev_key) not in _norm_text(body):
                        fail("ROW_KEY_MISSING", f"phrase {ev_key!r} not found in {ev_file}")
                    elif not ev_key:
                        fail("ROW_MISSING_FIELD", "evidence_key empty for a text evidence file")
                    else:
                        resolved = True
                        stored = ev_key
                        if result_value and _norm_text(result_value) not in _norm_text(body):
                            fail("ROW_VALUE_MISMATCH", f"result_value {result_value!r} not found in {ev_file}")
                            resolved = False
                        value_checked = True
                else:
                    fail("ROW_BAD_EVIDENCE", f"unsupported evidence file type: {ev_file}")

        if resolved and not value_checked:
            tol = _evidence_tolerance(index, ev_file, ev_key)
            if tol is None:
                tol = DEFAULT_REL_TOL
            ok, detail = compare_values(stored, result_value, tol)
            if not ok:
                fail("ROW_VALUE_MISMATCH", detail)
            row["_value_detail"] = detail
            row["_stored"] = stored

        for ck in keys_in(row.get("claim", "")) + keys_in(ev_key):
            status = verified.get(ck)
            if status is None:
                fail("ROW_CITATION_UNVERIFIED", f"citation key {ck!r} is not in verified_citations.csv")
            elif status != "VERIFIED":
                fail("ROW_CITATION_UNVERIFIED", f"citation key {ck!r} has status {status}")

        row["_status"] = "PASS" if not row_findings else "FAIL"
        row["_findings"] = row_findings
        checked.append(row)
        judged_claims.append({"id": rid, "claim": row.get("claim", ""), "file": row.get("evidence_file", "")})

    # ---- coverage of the draft
    draft_claims, draft_warnings = collect_draft_claims(draft)
    for w in draft_warnings:
        add("DRAFT_STRUCTURE", w, file=str(draft))
    coverage: List[Dict[str, Any]] = []
    for claim in draft_claims:
        best: Optional[Dict[str, Any]] = None
        best_score = 0.0
        for jc in judged_claims:
            sc = similarity(claim["text"], jc["claim"])
            if sc > best_score:
                best_score, best = sc, jc
        covered = best is not None and best_score >= COVERAGE_THRESHOLD
        if not covered:
            section_label = {"abstract": "abstract", "intro": "introduction"}.get(
                claim["section"], claim["section"]
            )
            add(
                "UNCOVERED",
                f"no row covers this {section_label} claim ({claim['why']}): {claim['text'][:120]!r}",
                file=claim["file"],
                line=claim["line"],
            )
        claim["covered_by"] = best["id"] if covered and best else None
        claim["score"] = round(best_score, 3)
        coverage.append(claim)

        # forbidden unverified language must point at the novelty check
        if FORBIDDEN_RE.search(claim["text"]):
            if re.match(r"\s*first\s*,", claim["text"], re.IGNORECASE):
                continue  # enumerative "First, we ..." is not a novelty claim
            novelty_rows = [
                jc for jc in judged_claims if Path(jc["file"]).name.lower() == NOVELTY_FILE.lower()
            ]
            best_n = None
            best_n_score = 0.0
            for jc in novelty_rows:
                sc = similarity(claim["text"], jc["claim"])
                if sc > best_n_score:
                    best_n_score, best_n = sc, jc
            if best_n is None or best_n_score < COVERAGE_THRESHOLD:
                hit_match = FORBIDDEN_RE.search(claim["text"])
                hit = hit_match.group(0) if hit_match else "unverified claim"
                add(
                    "NOVELTY_ROW_MISSING",
                    f"{hit!r} used without a row whose evidence_file is 02_literature/{NOVELTY_FILE}: "
                    f"{claim['text'][:120]!r}",
                    file=claim["file"],
                    line=claim["line"],
                )

    n_fail_rows = sum(1 for r in checked if r["_status"] != "PASS")
    n_uncovered = sum(1 for f in findings if f["code"] == "UNCOVERED")
    blocking = [f for f in findings if f["code"] != "TABLE_WARNING"]
    ok = not blocking and n_uncovered == 0

    return {
        "audit_file": str(audit_path),
        "draft": str(draft),
        "index": str(index_path),
        "citations": str(citations_path),
        "n_rows": len(rows),
        "n_rows_checked": len(checked),
        "n_rows_skipped_examples": len(skipped),
        "n_rows_failed": n_fail_rows,
        "n_draft_claims": len(draft_claims),
        "n_covered": sum(1 for c in coverage if c["covered_by"]),
        "n_uncovered": n_uncovered,
        "rows": [
            {
                "claim_id": r.get("claim_id"),
                "section": r.get("section"),
                "evidence_file": r.get("evidence_file"),
                "evidence_key": r.get("evidence_key"),
                "result_value": r.get("result_value"),
                "stored_value": _fmt(r["_stored"]) if "_stored" in r else None,
                "verified": r.get("verified"),
                "status": r.get("_status"),
                "findings": r.get("_findings", []),
            }
            for r in rows
        ],
        "coverage": coverage,
        "findings": findings,
        "ok": ok,
        "exit_code": 0 if ok else 1,
    }


# --------------------------------------------------------------------------- rendering


def render_markdown(result: Dict[str, Any]) -> str:
    out: List[str] = []
    out.append(f"## Claims audit verdict — `{Path(result['audit_file']).name}`")
    out.append("")
    out.append(
        f"Rows: {result['n_rows']} ({result['n_rows_checked']} checked, "
        f"{result['n_rows_skipped_examples']} EX- examples skipped). "
        f"Draft claims needing evidence: {result['n_draft_claims']} "
        f"({result['n_covered']} covered, {result['n_uncovered']} uncovered)."
    )
    out.append("")
    out.append("| claim_id | section | evidence | printed | stored | verified | verdict |")
    out.append("|---|---|---|---|---|---|---|")
    for row in result["rows"]:
        ev = f"{Path(str(row['evidence_file'])).name} :: {row['evidence_key']}"
        stored = "" if row["stored_value"] is None else row["stored_value"]
        out.append(
            "| {id} | {sec} | {ev} | {res} | {sto} | {ver} | {stat} |".format(
                id=row["claim_id"],
                sec=row["section"],
                ev=ev,
                res=row["result_value"],
                sto=stored,
                ver=row["verified"],
                stat={"PASS": "✅ PASS", "FAIL": "❌ FAIL", "SKIP": "— skip (example)"}.get(
                    row["status"], row["status"]
                ),
            )
        )
    out.append("")
    if result["findings"]:
        out.append("### Findings")
        out.append("")
        for f in result["findings"]:
            loc = ""
            if f.get("file"):
                loc = f" — {f['file']}" + (f":{f['line']}" if f.get("line") else "")
            rid = f" `{f['row_id']}`" if f.get("row_id") else ""
            out.append(f"- **{f['code']}**{rid}: {f['detail']}{loc}")
        out.append("")
    else:
        out.append("### Findings")
        out.append("")
        out.append("None. Every checked row verifies and every quantitative/comparative claim is bound.")
        out.append("")
    out.append(f"**Verdict: {'PASS' if result['ok'] else 'BLOCKED'}** (exit {result['exit_code']})")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- CLI


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="claims_audit.py",
        description="Verify that every abstract/introduction claim is bound to real evidence.",
        epilog=(
            "Exit 0 = every row verified and coverage complete; 1 = findings; 2 = usage error. "
            f"Coverage fuzzy-match threshold: {COVERAGE_THRESHOLD} (Dice token overlap / containment). "
            "A sentence needs a row when it contains a digit or a comparative stem "
            "(outperform, improve, reduc, increas, novel, state-of-the-art, first, sota, "
            "better than, superior, gain, speedup, faster, cheaper)."
        ),
    )
    p.add_argument("--audit", required=True, type=Path, help="claims-audit markdown table")
    p.add_argument("--draft", required=True, type=Path, help="draft directory (or a single .md/.tex)")
    p.add_argument("--index", required=True, type=Path, help="04_experiments/RESULTS-INDEX.json")
    p.add_argument("--citations", required=True, type=Path, help="02_literature/verified_citations.csv")
    p.add_argument("--root", type=Path, default=REPO_ROOT, help="repo root for relative paths (default: repo root)")
    p.add_argument("--json", action="store_true", help="print machine-readable JSON to stdout")
    p.add_argument("--out", type=Path, help="also write the markdown verdict to this path")
    return p


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    for label, path in (
        ("--audit", args.audit),
        ("--draft", args.draft),
        ("--index", args.index),
        ("--citations", args.citations),
    ):
        if not path.exists():
            parser.error(f"{label} does not exist: {path}")

    try:
        result = audit(args.audit, args.draft, args.index, args.citations, args.root)
    except AuditParseError as exc:
        parser.error(str(exc))
        return 2  # unreachable, argparse exits

    md = render_markdown(result)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(md)
    return int(result["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
