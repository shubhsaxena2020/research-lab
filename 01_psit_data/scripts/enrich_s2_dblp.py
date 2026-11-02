#!/usr/bin/env python
"""Semantic Scholar enrichment + DBLP presence check.

Semantic Scholar's Graph API has no affiliation filter (verified 2026-11-03:
/graph/v1/paper/search matches title+abstract only), so it cannot *discover*
PSIT papers. What it can do is tell us, per DOI, whether S2 indexes the work,
its citation count, its field labels and its open-access PDF status. That is the
coverage comparison B2 asks for, done honestly.

DBLP likewise has no affiliation search, but it is precise about CS venues, so we
look each likely-CS title up and record whether DBLP knows it and under which venue.

Usage: python 01_psit_data/scripts/enrich_s2_dblp.py [--dblp-cap N]
"""
import csv
import json
import os
import re
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")
PAPERS = os.path.join(ROOT, "papers.csv")
MAILTO = "shubh.saxena2020@gmail.com"
UA = {"User-Agent": "research-lab-psit/1.0 (mailto:%s)" % MAILTO}

S2_FIELDS = ("citationCount,influentialCitationCount,venue,year,publicationVenue,"
             "fieldsOfStudy,s2FieldsOfStudy,openAccessPdf,externalIds,isOpenAccess,"
             "publicationTypes,referenceCount")


def s2_batch(ids, tries=5):
    delay = 20
    for a in range(1, tries + 1):
        r = requests.post("https://api.semanticscholar.org/graph/v1/paper/batch",
                          params={"fields": S2_FIELDS}, json={"ids": ids},
                          headers=UA, timeout=120)
        if r.status_code == 200:
            time.sleep(3.0)
            return r.json()
        print("  S2 HTTP %s attempt %d, sleeping %ds" % (r.status_code, a, delay))
        time.sleep(delay)
        delay = min(delay * 2, 120)
    print("  S2 gave up on a batch of %d" % len(ids))
    return [None] * len(ids)


def enrich(skip_s2=False):
    rows = list(csv.DictReader(open(PAPERS, encoding="utf-8")))
    if skip_s2:
        # Evidence of the block, kept so the write-up can cite it instead of guessing.
        try:
            probe = requests.get(
                "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature14539",
                params={"fields": "citationCount"}, headers=UA, timeout=30)
            evidence = {"http_status": probe.status_code, "body": probe.text[:300],
                        "checked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        except Exception as e:  # noqa: BLE001
            evidence = {"error": str(e)[:200]}
        with open(os.path.join(RAW, "s2_unavailable.json"), "w", encoding="utf-8") as fh:
            json.dump(evidence, fh, indent=1)
        for r in rows:
            r["in_s2"] = "not-checked"
            r["s2_citation_count"] = ""
            r["s2_venue"] = ""
            r["s2_fields"] = ""
            r["oa_pdf_url"] = ""
            if "open_access" not in r:
                r["open_access"] = ""
        cols = list(rows[0].keys())
        with open(PAPERS, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print("S2 skipped (see raw/s2_unavailable.json); %d rows carry in_s2=not-checked" % len(rows))
        return rows
    dois = [r["doi"].strip().lower() for r in rows if r["doi"].strip()]
    ids = ["DOI:" + d for d in dois]
    cache = os.path.join(RAW, "s2_batch.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as fh:
            results = json.load(fh)["results"]
        print("S2 cache loaded: %d results" % len(results))
    else:
        results = []
        for i in range(0, len(ids), 400):
            chunk = ids[i:i + 400]
            print("S2 batch %d/%d (%d ids)" % (i // 400 + 1, (len(ids) + 399) // 400, len(chunk)))
            results.extend(s2_batch(chunk))
        with open(cache, "w", encoding="utf-8") as fh:
            json.dump({"retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       "ids": ids, "results": results}, fh)

    s2_by_doi = {}
    for doi, res in zip(dois, results):
        if res:
            s2_by_doi[doi] = res
    print("S2 matched %d of %d DOIs" % (len(s2_by_doi), len(dois)))

    n_in = 0
    for r in rows:
        d = r["doi"].strip().lower()
        s = s2_by_doi.get(d)
        if s:
            n_in += 1
            r["in_s2"] = "yes"
            r["s2_citation_count"] = s.get("citationCount", "")
            r["s2_influential_citations"] = s.get("influentialCitationCount", "")
            r["s2_venue"] = (s.get("venue") or "")[:120]
            r["open_access"] = "yes" if s.get("isOpenAccess") else "no"
            pdf = (s.get("openAccessPdf") or {}).get("url", "")
            r["oa_pdf_url"] = pdf
            fs = ";".join(s.get("fieldsOfStudy") or [])
            r["s2_fields"] = fs
        else:
            r["in_s2"] = "no"
            r["s2_citation_count"] = ""
            r["s2_influential_citations"] = ""
            r["s2_venue"] = ""
            r["oa_pdf_url"] = ""
            r["s2_fields"] = ""

    cols = list(rows[0].keys())
    with open(PAPERS, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("papers.csv updated; in_s2 = %d / %d" % (n_in, len(rows)))
    return rows


def dblp(rows, cap=200):
    """Look up likely-CS titles in DBLP. Records presence + venue key."""
    cache_path = os.path.join(RAW, "dblp_lookup.json")
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as fh:
            cache = json.load(fh).get("lookups", {})

    def likely_cs(r):
        t = (r.get("topics") or "") + " " + (r.get("venue") or "")
        return bool(re.search(r"machine-learning|nlp|computer-vision|security-crypto|"
                              r"networks-iot|data-engineering", t)) or \
            (r.get("type") == "proceedings-article")

    todo = [r for r in rows if likely_cs(r) and r["title"] and r["title"] not in cache]
    print("DBLP: %d candidate titles, %d cached, looking up %d (cap %d)"
          % (len([r for r in rows if likely_cs(r)]), len(cache), min(len(todo), cap), cap))
    for r in todo[:cap]:
        q = re.sub(r"[^A-Za-z0-9 ]+", " ", r["title"])[:120]
        try:
            resp = requests.get("https://dblp.org/search/publ/api",
                                params={"q": q, "format": "json", "h": 3},
                                headers=UA, timeout=45)
            hits = resp.json().get("result", {}).get("hits", {}).get("hit", [])
            best = None
            for h in hits:
                info = h.get("info", {})
                t1 = re.sub(r"[^a-z0-9]", "", (info.get("title", "")).lower())
                t2 = re.sub(r"[^a-z0-9]", "", r["title"].lower())
                if t1[:60] and (t1[:60] in t2 or t2[:60] in t1):
                    best = {"venue": info.get("venue", ""), "key": info.get("key", ""),
                            "type": info.get("type", ""), "year": info.get("year", ""),
                            "doi": info.get("doi", "")}
                    break
            cache[r["title"]] = best
        except Exception as e:  # noqa: BLE001 - network flake must not kill the run
            print("  dblp error:", str(e)[:80])
            cache[r["title"]] = None
        time.sleep(1.1)

    with open(cache_path, "w", encoding="utf-8") as fh:
        json.dump({"retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "lookups": cache}, fh)
    hit = sum(1 for v in cache.values() if v)
    print("DBLP: %d/%d looked-up titles found" % (hit, len([v for v in cache.values() if v is not None])))

    by_title = {r["title"]: r for r in rows}
    for t, v in cache.items():
        if t in by_title:
            by_title[t]["in_dblp"] = "yes" if v else "no"
            by_title[t]["dblp_venue"] = (v or {}).get("venue", "")
    cols = list(rows[0].keys())
    if "in_dblp" in cols:
        with open(PAPERS, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    cap = 200
    if "--dblp-cap" in sys.argv:
        cap = int(sys.argv[sys.argv.index("--dblp-cap") + 1])
    rows = enrich(skip_s2="--skip-s2" in sys.argv)
    dblp(rows, cap)
