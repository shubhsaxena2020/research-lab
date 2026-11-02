"""Minimal BibTeX reader — no third-party dependency (bibtexparser is not installed).

Scope: the subset of BibTeX that appears in real drafts. It is deliberately tolerant, not
complete: a malformed entry is skipped with a warning rather than crashing the run, because a
citation checker that dies on one bad brace is useless.

Supported: @type{key, field = {value}, field = "value", field = 2020, @string-free.
Not supported (and not needed here): @string macros, crossref inheritance, \LaTeX in values
beyond brace stripping.
"""

from __future__ import annotations

import re
from typing import Dict, Iterator, List, Tuple

_ENTRY_START = re.compile(r"@(\w+)\s*\{", re.IGNORECASE)


def _read_braced(text: str, i: int, open_ch: str = "{", close_ch: str = "}") -> Tuple[str, int]:
    """Read a balanced {...} or "..." field value starting at i (pointing at the opener)."""
    if text[i] == '"':
        j = i + 1
        out = []
        while j < len(text):
            if text[j] == "\\" and j + 1 < len(text):
                out.append(text[j : j + 2])
                j += 2
                continue
            if text[j] == '"':
                return "".join(out), j + 1
            out.append(text[j])
            j += 1
        raise ValueError("unterminated quoted value")
    depth = 0
    j = i
    out = []
    while j < len(text):
        ch = text[j]
        if ch == "{":
            depth += 1
            if depth > 1:
                out.append(ch)
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(out), j + 1
            out.append(ch)
        else:
            out.append(ch)
        j += 1
    raise ValueError("unterminated braced value")


def _clean(value: str) -> str:
    v = value.strip()
    v = re.sub(r"\s+", " ", v)
    return v


def parse_bibtex(text: str) -> List[Dict[str, str]]:
    """Return a list of {key, type, field: value} dicts."""
    entries: List[Dict[str, str]] = []
    pos = 0
    while True:
        m = _ENTRY_START.search(text, pos)
        if not m:
            break
        etype = m.group(1).lower()
        i = m.end()  # just after '{'
        # entry key up to first comma
        comma = text.find(",", i)
        if comma < 0:
            break
        key = text[i:comma].strip()
        i = comma + 1
        fields: Dict[str, str] = {}
        while i < len(text):
            # skip whitespace and commas
            while i < len(text) and text[i] in " \t\r\n,":
                i += 1
            if i >= len(text):
                break
            if text[i] == "}":       # end of entry
                i += 1
                break
            if text[i] == "@":       # start of next entry, entry was unterminated
                break
            eq = text.find("=", i)
            if eq < 0:
                i = len(text)
                break
            name = text[i:eq].strip().lower()
            if not re.fullmatch(r"[a-z0-9_\-]+", name or ""):
                # not a field: skip to next comma to resynchronise
                nxt = text.find(",", i)
                i = nxt + 1 if nxt > 0 else len(text)
                continue
            j = eq + 1
            while j < len(text) and text[j] in " \t\r\n":
                j += 1
            try:
                if j < len(text) and text[j] in "{":
                    val, i = _read_braced(text, j, "{", "}")
                elif j < len(text) and text[j] == '"':
                    val, i = _read_braced(text, j)
                else:
                    # bare token: 2020, 10.1000/xyz
                    k = j
                    while k < len(text) and text[k] not in ",\n}":
                        k += 1
                    val, i = text[j:k], k
            except ValueError:
                break
            fields[name] = _clean(val)
        if key:
            fields["key"] = key
            fields["_type"] = etype
            entries.append(fields)
        pos = max(i, m.end())
    return entries


def bibtex_to_records(text: str) -> List[Dict[str, str]]:
    """Map BibTeX entries onto the citation CSV schema (tools/CONTRACTS.md §1)."""
    out = []
    for e in parse_bibtex(text):
        if e.get("_type") in ("comment", "preamble", "string"):
            continue
        authors = e.get("author", "") or e.get("editor", "")
        authors = re.sub(r"\s+and\s+", "; ", authors)
        arxiv = (e.get("eprint") or e.get("arxivid") or e.get("arxiv_id") or "").strip()
        if not arxiv:
            url = e.get("url", "")
            m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s]+?)(?:\.pdf)?$", url)
            if m:
                arxiv = m.group(1)
        out.append(
            {
                "key": e.get("key", ""),
                "title": e.get("title", ""),
                "authors": authors,
                "year": (e.get("year", "") or "").strip(),
                "doi": e.get("doi", ""),
                "arxiv_id": arxiv,
                "venue": e.get("journal", "") or e.get("booktitle", "") or e.get("publisher", ""),
            }
        )
    return out
