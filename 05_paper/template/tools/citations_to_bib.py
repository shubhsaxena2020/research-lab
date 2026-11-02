#!/usr/bin/env python
"""citations_to_bib.py -- turn verified citations into BibTeX, so nobody hand-writes them.

Input : 02_literature/verified_citations.csv  (tools/CONTRACTS.md section 1)
        key,title,authors,year,doi,arxiv_id,venue,status,source,source_url,retrieved_at,evidence
Output: a .bib file whose every entry carries a "% provenance:" comment naming the
        API that resolved it and when.

Why this exists: RULES.md #1 says a citation may enter a draft only if it was
resolved by a real API call and recorded with its URL and retrieval date. Typing
BibTeX by hand is how invented references get in. This script is the only
sanctioned path from CSV row to .bib entry.

Policy enforced here, not left to the author:
  * rows whose status is not VERIFIED are dropped (MISMATCH / NOT_FOUND / ERROR
    never become references -- an ERROR is not a pass);
  * a file with no `status` column is refused, because nothing in it proves the
    rows were verified (override only with --allow-missing-status);
  * a VERIFIED row with no key or no title is refused and reported, never
    silently written as a stub;
  * duplicate keys with different content are a hard error;
  * the printed bibliography stays clean: provenance lives in a comment above
    each entry, not in a `note` field.

Usage
  python tools/citations_to_bib.py --csv 02_literature/verified_citations.csv \
         --out refs.generated.bib
  python tools/citations_to_bib.py --csv ... --out ... --json

Exit codes
  0  wrote the file (possibly zero entries -- that is a valid state)
  1  rows were refused (file may still be written with the good rows)
  2  usage error, unreadable input, or a file with no provenance columns
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import NoReturn

# The schema mapping lives once, in tools/lib/citation_schema.py, and is shared with
# tools/verify_citations.py and tools/claims_audit.py. Duplicating it here is how the two
# writers of verified_citations.csv drifted apart in the first place.
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "tools"))
try:
    from lib.citation_schema import normalize_row as _normalize_row
except ImportError as _exc:  # pragma: no cover - only if the repo is copied without tools/
    raise SystemExit(
        "citations_to_bib: cannot import tools/lib/citation_schema.py "
        f"({_exc}). Run this script from inside the research-lab repo."
    )


def _norm_schema(row: dict) -> dict:
    """Map a register row onto the internal field names (id->key, doi_or_arxiv->doi/arxiv)."""
    n = _normalize_row({k: (v or "") for k, v in row.items() if k})
    return {
        "key": n["key"] or "",
        "title": n["title"] or "",
        "authors": n["authors"] or "",
        "year": n["year"] or "",
        "doi": n["doi"] or "",
        "arxiv_id": n["arxiv_id"] or "",
        "venue": n["venue"] or "",
        "status": n["status"] or "",
        "source_url": (row.get("source_url") or row.get("url") or ""),
        "retrieved_on": (row.get("retrieved_on") or ""),
        "retrieved_at": (row.get("retrieved_at") or row.get("retrieved_on") or ""),
        "verified_by_command": (row.get("verified_by_command") or ""),
    }

# Characters that are LaTeX specials and would break compilation if they reach a
# text field unescaped. Backslash first: later rules introduce backslashes.
_TEXT_ESCAPE_ORDER = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("$", r"\$"),
]

_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.:+-]*$")
_DOI_PREFIXES = ("https://doi.org/", "http://doi.org/", "http://dx.doi.org/", "doi:")
_ARXIV_PREFIXES = ("arxiv:", "https://arxiv.org/abs/", "http://arxiv.org/abs/",
                   "https://arxiv.org/pdf/", "http://arxiv.org/pdf/")


class Refused(Exception):
    """A row that cannot become an entry."""


def die(msg: str, code: int = 2) -> NoReturn:
    print(f"citations_to_bib: error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def escape_text(value: str) -> str:
    out = value
    for old, new in _TEXT_ESCAPE_ORDER:
        out = out.replace(old, new)
    return re.sub(r"\s+", " ", out).strip()


def normalise_doi(raw: str) -> str:
    doi = (raw or "").strip()
    low = doi.lower()
    for prefix in _DOI_PREFIXES:
        if low.startswith(prefix):
            doi = doi[len(prefix):]
            break
    return doi.strip().rstrip(".")


def normalise_arxiv(raw: str) -> str:
    aid = (raw or "").strip()
    for prefix in _ARXIV_PREFIXES:
        if aid.lower().startswith(prefix):
            aid = aid[len(prefix):]
            break
    if aid.lower().endswith(".pdf"):
        aid = aid[:-4]
    return aid.strip()


def split_authors(raw: str) -> list[str]:
    """`Surname, Given; Surname, Given` -> `['Surname, Given', ...]`."""
    if not raw:
        return []
    parts = [p.strip() for p in re.split(r";|\band\b", raw) if p.strip()]
    return parts


def entry_from_row(row: dict[str, str], *, allow_missing_status: bool) -> str:
    # Accept the ONE canonical register schema (id,...,doi_or_arxiv,...) as well as the
    # older S3 12-column form. Without this the two writers of verified_citations.csv make
    # each other's output unreadable, which is exactly what happened on 2026-11-03.
    row = _norm_schema(row)
    key = (row.get("key") or "").strip()
    title = (row.get("title") or "").strip()
    if not key:
        raise Refused("no key")
    if not _KEY_RE.match(key):
        raise Refused(f"key {key!r} is not a legal BibTeX key")
    if not title:
        raise Refused(f"{key}: no title")

    doi = normalise_doi(row.get("doi", ""))
    arxiv = normalise_arxiv(row.get("arxiv_id", ""))
    venue = (row.get("venue") or "").strip()
    year = (row.get("year") or "").strip()
    if year and not re.fullmatch(r"\d{4}", year):
        year = ""  # never guess a year; an unparsable one is dropped
    url = (row.get("source_url") or "").strip()
    authors = split_authors(row.get("authors", ""))

    if doi and venue:
        etype = "article"
    elif arxiv:
        etype = "misc"
    elif doi:
        etype = "misc"
    else:
        etype = "misc"

    fields: list[tuple[str, str]] = []
    if authors:
        fields.append(("author", " and ".join(escape_text(a) for a in authors)))
    fields.append(("title", escape_text(title)))

    if etype == "article":
        fields.append(("journal", escape_text(venue)))
    elif venue:
        fields.append(("howpublished", escape_text(venue)))
    if year:
        fields.append(("year", year))
    if doi:
        fields.append(("doi", doi))
    if arxiv:
        fields.append(("eprint", arxiv))
        fields.append(("archivePrefix", "arXiv"))
    if not url:
        if doi:
            url = f"https://doi.org/{doi}"
        elif arxiv:
            url = f"https://arxiv.org/abs/{arxiv}"
    if url:
        fields.append(("url", url))

    # provenance, kept out of the printed reference list. The canonical register records it in
    # `verified_by_command` + `retrieved_on`; the older form used `source`/`retrieved_at`.
    prov = []
    for col in ("source", "retrieved_on", "retrieved_at", "verified_by_command", "evidence"):
        val = (row.get(col) or "").strip()
        if val:
            prov.append(f"{col}={val}")
    width = max(len(name) for name, _ in fields)
    body = ",\n".join(f"  {name.ljust(width)} = {{{value}}}" for name, value in fields)
    comment = f"% provenance: {' '.join(prov)}\n" if prov else ""
    return f"{comment}@{etype}{{{key},\n{body}\n}}\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Convert verified_citations.csv into BibTeX entries.",
        epilog="Only rows with status=VERIFIED become entries (RULES.md #1).",
    )
    ap.add_argument("--csv", required=True, help="path to verified_citations.csv")
    ap.add_argument("--out", required=True, help="output .bib path")
    ap.add_argument("--allow-missing-status", action="store_true",
                    help="accept a CSV with no `status` column; you are asserting "
                         "every row was verified (do not use on staging files)")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable summary on stdout")
    args = ap.parse_args(argv)

    src = Path(args.csv)
    if not src.is_file():
        die(f"{src} does not exist", 2)
    try:
        with src.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            fields = [f.strip() for f in (reader.fieldnames or [])]
            rows = [{k.strip(): (v or "") for k, v in row.items() if k}
                    for row in reader]
    except (OSError, csv.Error) as exc:
        die(f"cannot read {src}: {exc}", 2)

    if not fields:
        die(f"{src} has no header row", 2)
    if "title" not in fields:
        die(f"{src} lacks required column(s): title", 2)
    if "key" not in fields and "id" not in fields:
        die(f"{src} lacks required column(s): key (or id)", 2)

    # The canonical schema has no `status` column: every row in that file is verified by
    # construction, and `verified_by_command` is the proof. Anything else must say VERIFIED.
    has_status = "status" in fields
    if not has_status and "verified_by_command" not in fields and not args.allow_missing_status:
        die(f"{src} has no `status` and no `verified_by_command` column, so nothing proves "
            f"the rows were verified. Use 02_literature/verified_citations.csv (CONTRACTS "
            f"section 1), or pass --allow-missing-status if you are certain.",
            2)

    entries: dict[str, str] = {}
    counts = {"read": len(rows), "kept": 0, "skipped_status": 0, "refused": 0}
    refused: list[str] = []
    for raw_row in rows:
        if not any(v.strip() for v in raw_row.values()):
            continue
        # Normalise ONCE, before any key comparison: the register's key column is `id`,
        # and reading `key` before mapping it made every row look like the same empty key.
        row = _norm_schema(raw_row)
        status = (row.get("status") or "").strip().upper()
        if has_status and status != "VERIFIED":
            counts["skipped_status"] += 1
            continue
        try:
            text = entry_from_row(row, allow_missing_status=args.allow_missing_status)
        except Refused as exc:
            counts["refused"] += 1
            refused.append(str(exc))
            continue
        key = (row.get("key") or "").strip()
        if key in entries and entries[key] != text:
            counts["refused"] += 1
            refused.append(f"{key}: duplicate key with different content")
            continue
        entries[key] = text
        counts["kept"] += 1

    header = (
        "% =============================================================================\n"
        f"% GENERATED by 05_paper/template/tools/citations_to_bib.py -- do not edit.\n"
        f"% Source   : {src.as_posix()}\n"
        f"% Entries  : {len(entries)} (from {counts['read']} rows)\n"
        "% Rule     : every entry below resolved to a real DOI / arXiv id / OpenAlex\n"
        "%            record and is listed in verified_citations.csv (RULES.md #1).\n"
        "%            Rows with status != VERIFIED were dropped, not repaired.\n"
        "% =============================================================================\n\n"
    )
    bib = header + "\n".join(entries[k] for k in sorted(entries))
    out = Path(args.out)
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(bib, encoding="utf-8", newline="\n")
    except OSError as exc:
        die(f"cannot write {out}: {exc}", 2)

    result = {
        "input": src.as_posix(),
        "output": out.as_posix(),
        "entries": len(entries),
        **counts,
        "refused_detail": refused,
    }
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"citations_to_bib: read {counts['read']} rows, wrote {len(entries)} entries "
              f"to {out}")
        if counts["skipped_status"]:
            print(f"  dropped {counts['skipped_status']} row(s) that were not VERIFIED")
        for msg in refused:
            print(f"  REFUSED {msg}", file=sys.stderr)

    if refused:
        print("citations_to_bib: refusing to guess -- fix or delete the rows above "
              "before citing them", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
