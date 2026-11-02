"""One citation-row schema, because two pipelines writing the same file is how integrity dies.

History (2026-11-03): S3 built `tools/verify_citations.py` writing a 12-column
`verified_citations.csv`. S2 built `02_literature/tools/verify_citations.py add` writing a
9-column register to the *same path* and populated it with 266 rows. Two writers, two
schemas, one file — which silently broke `citations_to_bib.py` and `claims_audit.py` (they
looked for a `key` column that no longer existed). The head's directive was to agree on one
canonical schema and one owner; this module is that agreement in code.

**Canonical on-disk schema (owned by S2's tool, written by S3's too):**

    id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command

`status` is not a column: the file contains only verified rows by construction. A row that
was not verified belongs in a report, never in this file (RULES.md #1).

`normalize_row()` maps either schema (the canonical one, or S3's older 12-column form and
its report JSON) onto the internal dict that every consumer uses, so a reader never has to
know which generation wrote the file.
"""

from __future__ import annotations

import re
from typing import Dict, List, Mapping, Optional

#: The exact column order written to 02_literature/verified_citations.csv.
CANONICAL_FIELDS: List[str] = [
    "id",
    "title",
    "authors",
    "year",
    "venue",
    "url",
    "doi_or_arxiv",
    "retrieved_on",
    "verified_by_command",
]

_INTERNAL = ("key", "title", "authors", "year", "doi", "arxiv_id", "venue", "status")


def _pick(row: Mapping[str, Optional[str]], *names: str) -> str:
    for n in names:
        v = row.get(n)
        if v is not None and str(v).strip():
            return str(v).strip()
    return ""


def _looks_like_arxiv(s: str) -> bool:
    return bool(
        re.match(r"(?i)^arxiv:", s)
        or re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", s)
        or re.fullmatch(r"[a-z\-]+/\d{7}(v\d+)?", s)
        or "arxiv.org/abs/" in s.lower()
    )


def _looks_like_doi(s: str) -> bool:
    return bool(re.match(r"(?i)^(https?://(dx\.)?doi\.org/|doi:)?10\.\d{4,9}/", s))


def normalize_row(row: Mapping[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """Map a row from either schema onto the internal citation dict.

    Returns keys: key, title, authors, year, doi, arxiv_id, venue, status.
    Never raises: an unrecognisable row comes back with empty fields and the caller decides.
    """
    key = _pick(row, "key", "id", "citekey")
    title = _pick(row, "title")
    authors = _pick(row, "authors")
    year = _pick(row, "year")
    venue = _pick(row, "venue", "journal", "booktitle")
    doi = _pick(row, "doi")
    arxiv_id = _pick(row, "arxiv_id", "eprint", "arxiv")
    status = _pick(row, "status").upper()

    # One file may hold the identifier in a single mixed column.
    mixed = _pick(row, "doi_or_arxiv", "doi_or_arxiv_id", "identifier", "id_or_doi")
    if mixed:
        if _looks_like_arxiv(mixed):
            arxiv_id = arxiv_id or mixed
        elif _looks_like_doi(mixed):
            doi = doi or mixed

    # Or the identifier may only appear inside the url column.
    url = _pick(row, "url", "source_url")
    if url:
        if not doi:
            m = re.search(r"doi\.org/(10\.[^\s]+)$", url)
            if m:
                doi = m.group(1)
        if not arxiv_id:
            m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s?#]+?)(?:\.pdf)?$", url)
            if m:
                arxiv_id = m.group(1)

    # The canonical schema has no status column because every row in it is verified.
    if not status:
        status = "VERIFIED" if _pick(row, "verified_by_command", "retrieved_on") else ""
    if not key:
        slug = re.sub(r"[^a-z0-9]+", "-", (title or "record").lower()).strip("-")
        key = (slug[:60] or "record")

    return {
        "key": key or None,
        "title": title or None,
        "authors": authors or None,
        "year": year or None,
        "doi": doi or None,
        "arxiv_id": arxiv_id or None,
        "venue": venue or None,
        "status": status or None,
    }


def identifier_for(row: Mapping[str, Optional[str]]) -> str:
    """The single string to put in the canonical `doi_or_arxiv` column."""
    doi = _pick(row, "doi")
    if doi:
        return doi
    arxiv = _pick(row, "arxiv_id", "eprint")
    if arxiv:
        return arxiv if re.match(r"(?i)^arxiv:", arxiv) else f"arXiv:{arxiv}"
    return _pick(row, "doi_or_arxiv")


def to_canonical_row(internal: Dict[str, Optional[str]], command: str) -> Dict[str, str]:
    """Build a canonical 9-column row from the internal dict + the command that verified it."""
    return {
        "id": internal.get("key") or "",
        "title": internal.get("title") or "",
        "authors": internal.get("authors") or "",
        "year": str(internal.get("year") or ""),
        "venue": internal.get("venue") or "",
        "url": internal.get("url") or internal.get("source_url") or "",
        "doi_or_arxiv": identifier_for(internal),
        "retrieved_on": (internal.get("retrieved_at") or "")[:10],
        "verified_by_command": command,
    }
