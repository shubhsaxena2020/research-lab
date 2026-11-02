#!/usr/bin/env python
"""Crossref backbone harvest for PSIT affiliation records.

Why Crossref first: OpenAlex's anonymous daily budget for this network's IP was
exhausted at 2026-11-03T01:50Z (HTTP 429, "$0 remaining; resets at midnight UTC"),
so the OpenAlex path is cached-but-unavailable today. Crossref is the DOI
registration agency, needs no key, and carries deposited author affiliation
strings - i.e. the primary evidence of "this paper claims a PSIT affiliation".

Method
- For each query string, page /works?query.affiliation=... with a cursor, 1000 rows/page.
- query.affiliation is a relevance-ranked free-text query, NOT an exact filter, so
  every returned item is re-checked locally: keep it only if some author affiliation
  string matches AFFIL_RE.
- Dedupe by DOI. Cache every page in raw/crossref/.

Usage: python 01_psit_data/scripts/harvest_crossref.py [--max-pages N] [--fresh]
"""
import json
import os
import re
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw", "crossref")
os.makedirs(RAW, exist_ok=True)

MAILTO = "shubh.saxena2020@gmail.com"
UA = "research-lab-psit/1.0 (mailto:%s)" % MAILTO
API = "https://api.crossref.org/works"

# A paper counts as PSIT-affiliated only if a deposited affiliation string says so.
AFFIL_RE = re.compile(r"PSIT|Pranveer\s*Singh", re.I)

QUERIES = [
    '"Pranveer"',      # 645 reported, 641/1000 matched locally -> near-pure set
    '"PSIT"',          # 278 reported, all matched
    '"PSIT Kanpur"',   # fuzzy (18k reported); first 1-2k rows are relevance-ranked
]

SELECT = ",".join([
    "DOI", "title", "author", "container-title", "issued", "published-print",
    "published-online", "type", "is-referenced-by-count", "abstract", "subject",
    "publisher", "ISSN", "URL", "link", "short-container-title", "volume", "page",
])


def get(params, tries=4):
    delay = 20
    for attempt in range(1, tries + 1):
        r = requests.get(API, params=params, headers={"User-Agent": UA}, timeout=90)
        if r.status_code == 200:
            time.sleep(1.0)
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            print("  HTTP %s attempt %d, sleeping %ds" % (r.status_code, attempt, delay))
            time.sleep(delay)
            delay *= 2
            continue
        raise SystemExit("Fatal HTTP %s: %s" % (r.status_code, r.text[:300]))
    raise SystemExit("Gave up: %s" % params)


def affil_strings(item):
    out = []
    for a in item.get("author", []) or []:
        for af in a.get("affiliation", []) or []:
            n = (af.get("name") or "").strip()
            if n:
                out.append(n)
    return out


def is_psit(item):
    return any(AFFIL_RE.search(s) for s in affil_strings(item))


def harvest_query(q, max_pages):
    tag = re.sub(r"[^a-z0-9]+", "_", q.lower()).strip("_")
    kept, seen_doi, scanned, cursor, page = [], set(), 0, "*", 0
    total = None
    while cursor and page < max_pages:
        page += 1
        path = os.path.join(RAW, "crossref_%s_p%02d.json" % (tag, page))
        if os.path.exists(path):
            d = json.load(open(path, encoding="utf-8"))
            print("[%s] page %d from cache" % (tag, page))
        else:
            params = {"query.affiliation": q, "rows": 1000, "cursor": cursor,
                      "select": SELECT, "mailto": MAILTO}
            d = get(params)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(d, fh)
        msg = d["message"]
        if total is None:
            total = msg.get("total-results")
            print("[%s] Crossref reports %s results for this query string" % (tag, total))
        items = msg.get("items", [])
        scanned += len(items)
        for it in items:
            if is_psit(it):
                doi = (it.get("DOI") or "").lower()
                if doi and doi not in seen_doi:
                    seen_doi.add(doi)
                    it["_affil_strings"] = affil_strings(it)
                    it["_query"] = q
                    kept.append(it)
        print("  page %d: scanned %d, kept %d (running total %d)"
              % (page, len(items), len(kept), len(kept)))
        cursor = msg.get("next-cursor")
        if not items:
            break
    return kept, total, scanned


def main():
    max_pages = 3
    if "--max-pages" in sys.argv:
        max_pages = int(sys.argv[sys.argv.index("--max-pages") + 1])

    by_doi, stats = {}, {}
    for q in QUERIES:
        kept, total, scanned = harvest_query(q, max_pages)
        stats[q] = {"crossref_total_results": total, "items_scanned": scanned,
                    "kept_psit": len(kept)}
        for it in kept:
            by_doi.setdefault((it.get("DOI") or "").lower(), it)

    out = {"retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "source": "Crossref REST API /works?query.affiliation",
           "mailto": MAILTO, "affil_regex": AFFIL_RE.pattern,
           "queries": QUERIES, "stats": stats, "unique_dois": len(by_doi),
           "items": list(by_doi.values())}
    p = os.path.join(ROOT, "raw", "crossref_merged.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh)
    print(json.dumps(stats, indent=1))
    print("UNIQUE PSIT DOIs: %d -> %s" % (len(by_doi), p))


if __name__ == "__main__":
    main()
