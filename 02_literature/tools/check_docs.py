#!/usr/bin/env python
"""Merge staging CSVs into the canonical verified_citations.csv and audit documents.

  merge   - dedupe all 02_literature/staging/S2-*-verified.csv -> 02_literature/verified_citations.csv
  audit   - for each literature .md: every reference must resolve to a canonical CSV row,
            and every in-text [n] must exist in that document's reference list.

Usage:
  python 02_literature/tools/check_docs.py merge
  python 02_literature/tools/check_docs.py audit
"""
from __future__ import annotations

import csv
import difflib
import glob
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIT = os.path.join(ROOT, "02_literature")
STAGING = os.path.join(LIT, "staging")
CANON = os.path.join(LIT, "verified_citations.csv")
FIELDS = ["id", "title", "authors", "year", "venue", "url", "doi_or_arxiv",
          "retrieved_on", "verified_by_command"]


def norm(s: str) -> str:
    s = (s or "").lower().replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def merge() -> None:
    seen: dict[str, dict] = {}
    per_file: Counter = Counter()
    files = sorted(glob.glob(os.path.join(STAGING, "S2-*-verified.csv")))
    for path in files:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("title"):
                    continue
                k = norm(row["title"])
                per_file[os.path.basename(path)] += 1
                if k in seen:
                    continue
                seen[k] = {c: (row.get(c) or "").strip() for c in FIELDS}
    # carry over legacy rows that used a different schema, if any
    legacy = os.path.join(LIT, "verified_citations.s1-legacy.csv")
    legacy_added = 0
    if os.path.exists(legacy):
        with open(legacy, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t = row.get("title", "")
                if not t or norm(t) in seen:
                    continue
                ax = row.get("arxiv_id", "")
                seen[norm(t)] = {
                    "id": re.sub(r"[^a-z0-9]+", "-", norm(t)[:60]).strip("-"),
                    "title": t,
                    "authors": row.get("authors", ""),
                    "year": row.get("year", ""),
                    "venue": row.get("venue", ""),
                    "url": (f"https://arxiv.org/abs/{ax}" if ax
                            else row.get("doi", "") and f"https://doi.org/{row['doi']}" or ""),
                    "doi_or_arxiv": f"arXiv:{ax}" if ax else row.get("doi", ""),
                    "retrieved_on": (row.get("retrieved_at", "") or "")[:10],
                    "verified_by_command": f"legacy s1 row ({row.get('source','')})",
                }
                legacy_added += 1
    rows = sorted(seen.values(), key=lambda r: (r["year"] or "0", norm(r["title"])))
    with open(CANON, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({"staging_files": per_file, "legacy_added": legacy_added,
                      "unique": len(rows)}, indent=1))


def _refs_section(text: str) -> list[str]:
    """Return reference lines from the bibliography section.

    Handles '## 7. References', '## 14. References', '### References', and both
    '12. Author. Title (2025)...' and '[12] Title (2025)...' numbering styles.
    """
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^#{1,3}\s*(?:[\d.]+\s*)?references?\b", ln.strip(), re.I):
            start = i
    if start is None:
        return []
    out = []
    for ln in lines[start + 1:]:
        s = ln.strip()
        if re.match(r"^#{1,3}\s", s) and not re.match(r"^(\[\d+\]|\d+\.)", s):
            break
        if re.match(r"^(\[\d{1,3}\]|\d{1,3}[.)])\s+\S", s):
            out.append(s)
    return out


def audit() -> None:
    with open(CANON, newline="", encoding="utf-8") as f:
        canon = [r["title"] for r in csv.DictReader(f)]
    cn = [(norm(t), t) for t in canon]
    docs = [os.path.join(LIT, "LANDSCAPE.md")] + sorted(
        glob.glob(os.path.join(LIT, "deep_dives", "*.md")))
    report = {}
    for doc in docs:
        text = open(doc, encoding="utf-8").read()
        refs = _refs_section(text)
        unmatched = []
        for r in refs:
            nr = norm(r)
            hits = [orig for n, orig in cn if n and n in nr]
            if hits:
                continue
            best, bs = None, 0.0
            for n, orig in cn:
                s = difflib.SequenceMatcher(None, n, nr[:len(n) + 40]).ratio()
                if s > bs:
                    best, bs = orig, s
            if bs < 0.72:
                unmatched.append((r[:110], round(bs, 2)))
        # in-text citation indices
        body = text[:text.find(refs[0])] if refs else text
        cited = set()
        for m in re.finditer(r"\[(\d{1,2}(?:\s*[,\-–]\s*\d{1,2})*)\]", body):
            for part in re.split(r"[,\s]+", m.group(1)):
                part = part.strip()
                if not part:
                    continue
                if re.match(r"^\d+[-–]\d+$", part):
                    a, b = re.split(r"[-–]", part)
                    cited.update(range(int(a), int(b) + 1))
                elif part.isdigit():
                    cited.add(int(part))
        n = len(refs)
        missing_idx = sorted(i for i in cited if i < 1 or i > n)
        uncited = sorted(set(range(1, n + 1)) - cited) if cited else []
        report[os.path.basename(doc)] = {
            "refs": n, "unmatched_refs": unmatched,
            "intext_max": max(cited) if cited else 0,
            "out_of_range": missing_idx,
            "uncited_refs": uncited[:20],
            "words": len(text.split()),
        }
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    {"merge": merge, "audit": audit}[sys.argv[1]]()
