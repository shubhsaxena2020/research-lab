#!/usr/bin/env python
"""Harvest PSIT works from OpenAlex. Writes raw JSON pages + a merged index.

Usage:  python 01_psit_data/scripts/harvest_openalex.py [--max-pages N]

Design notes
- One owner (this script) touches OpenAlex, so the shared daily budget is not
  blown by parallel agents. Every page is cached in 01_psit_data/raw/ so re-runs
  are free.
- Polite: descriptive User-Agent with mailto, 1 request/second, exponential
  backoff on 429/5xx (RULES.md rule 11).
- No credentials, no logins. Public API only.
"""
import json
import os
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")
os.makedirs(RAW, exist_ok=True)

MAILTO = "shubh.saxena2020@gmail.com"
UA = "research-lab-psit/1.0 (mailto:%s)" % MAILTO
BASE = "https://api.openalex.org"
INST_ID = "I4405287327"  # candidate: "Pranveer Singh Institute of Technology (Pharmacy), Kanpur"

SELECT = ",".join([
    "id", "doi", "title", "display_name", "publication_year", "publication_date",
    "type", "primary_location", "authorships", "cited_by_count", "open_access",
    "topics", "keywords", "language", "referenced_works_count", "is_retracted",
    "institutions_distinct_count", "countries_distinct_count", "ids",
])


def get(path, params, tries=4):
    """GET with backoff. Returns parsed JSON."""
    delay = 30
    for attempt in range(1, tries + 1):
        r = requests.get(BASE + path, params=params,
                         headers={"User-Agent": UA}, timeout=60)
        if r.status_code == 200:
            time.sleep(1.0)
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            print("  HTTP %s on attempt %d, sleeping %ds" % (r.status_code, attempt, delay))
            time.sleep(delay)
            delay *= 2
            continue
        raise SystemExit("Fatal HTTP %s for %s params=%s body=%s"
                         % (r.status_code, path, params, r.text[:300]))
    raise SystemExit("Gave up after %d attempts: %s" % (tries, path))


def harvest(tag, filt, max_pages=40):
    """Cursor-page one filter into raw/openalex_<tag>_pNNN.json. Returns works list."""
    works, seen, cursor, page = [], set(), "*", 0
    meta_first = None
    while cursor and page < max_pages:
        page += 1
        params = {"filter": filt, "per_page": 200, "cursor": cursor,
                  "select": SELECT, "mailto": MAILTO}
        d = get("/works", params)
        if meta_first is None:
            meta_first = d["meta"]
            print("[%s] reported count=%s" % (tag, d["meta"]["count"]))
        path = os.path.join(RAW, "openalex_%s_p%03d.json" % (tag, page))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh)
        for w in d["results"]:
            if w["id"] not in seen:
                seen.add(w["id"])
                works.append(w)
        print("  page %d: %d results (total %d)" % (page, len(d["results"]), len(works)))
        cursor = d["meta"].get("next_cursor")
        if not d["results"]:
            break
    return works, meta_first


def main():
    max_pages = 40
    if "--max-pages" in sys.argv:
        max_pages = int(sys.argv[sys.argv.index("--max-pages") + 1])

    # 1. The institution record itself
    inst_path = os.path.join(RAW, "openalex_institution_%s.json" % INST_ID)
    if not os.path.exists(inst_path):
        inst = get("/institutions/" + INST_ID, {"mailto": MAILTO})
        with open(inst_path, "w", encoding="utf-8") as fh:
            json.dump(inst, fh, indent=1)
        print("institution saved:", inst["display_name"], inst["works_count"])
    else:
        print("institution cached")

    # 2. Works attributed to that institution id
    works_inst, meta_inst = harvest("inst", "institutions.id:" + INST_ID, max_pages)

    # 3. Works whose raw affiliation string mentions PSIT / Pranveer Singh
    works_affil, meta_affil = [], None
    for tag, term in (("affil_psit", "PSIT"), ("affil_pranveer", "Pranveer Singh")):
        w, m = harvest(tag, "raw_affiliation_strings.search:%s" % term, max_pages)
        works_affil.extend(w)
        if meta_affil is None:
            meta_affil = {}
        meta_affil[term] = m["count"]

    # 4. Merge + index
    merged = {}
    for w in works_inst + works_affil:
        merged.setdefault(w["id"], w)
    out = os.path.join(RAW, "openalex_works_merged.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "mailto": MAILTO,
                   "institution_id": INST_ID,
                   "counts": {"institution_filter": meta_inst,
                              "affiliation_search": meta_affil,
                              "merged_unique": len(merged)},
                   "works": list(merged.values())}, fh)
    print("MERGED %d unique works -> %s" % (len(merged), out))


if __name__ == "__main__":
    main()
