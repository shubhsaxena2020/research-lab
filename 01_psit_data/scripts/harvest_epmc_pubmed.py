#!/usr/bin/env python
"""Europe PMC + PubMed harvest (affiliation-field search).

Both services support an exact-ish affiliation field query, which Crossref cannot do:
  Europe PMC:  AFF:"Pranveer Singh"
  PubMed:      PSIT[AD]
They cover the biomedical part of PSIT's output (PSIT College of Pharmacy is the
institution that exists in ROR, so most of its indexed output is biomedical).
This complements the Crossref/DOI backbone; it is NOT a substitute for it.

Usage: python 01_psit_data/scripts/harvest_epmc_pubmed.py
"""
import json
import os
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")
os.makedirs(RAW, exist_ok=True)
MAILTO = "shubh.saxena2020@gmail.com"
UA = {"User-Agent": "research-lab-psit/1.0 (mailto:%s)" % MAILTO}


def get(url, params, tries=3):
    delay = 10
    for a in range(1, tries + 1):
        r = requests.get(url, params=params, headers=UA, timeout=90)
        if r.status_code == 200:
            time.sleep(0.6)
            return r.json()
        print("  HTTP %s attempt %d" % (r.status_code, a))
        time.sleep(delay)
        delay *= 2
    raise SystemExit("failed: %s" % url)


def epmc():
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    out, seen, cursor, page = [], set(), "*", 0
    while cursor and page < 10:
        page += 1
        d = get(url, {"query": 'AFF:"Pranveer Singh" OR AFF:"PSIT"',
                      "format": "json", "pageSize": 1000,
                      "resultType": "core", "cursorMark": cursor})
        res = d.get("resultList", {}).get("result", [])
        print("[EPMC] page %d: %d (hitCount %s)" % (page, len(res), d.get("hitCount")))
        for it in res:
            k = (it.get("doi") or it.get("id") or "").lower()
            if k and k not in seen:
                seen.add(k)
                out.append(it)
        nc = d.get("nextCursorMark")
        if not res or not nc or nc == cursor:
            break
        cursor = nc
    with open(os.path.join(RAW, "europepmc.json"), "w", encoding="utf-8") as fh:
        json.dump({"retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "query": 'AFF:"Pranveer Singh" OR AFF:"PSIT"',
                   "records": out}, fh)
    print("[EPMC] %d unique records" % len(out))
    return out


def pubmed():
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    d = get(base + "esearch.fcgi", {"db": "pubmed", "term": 'PSIT[AD] OR "Pranveer Singh"[AD]',
                                    "retmax": 1000, "retmode": "json"})
    ids = d["esearchresult"].get("idlist", [])
    print("[PubMed] %d ids (count %s)" % (len(ids), d["esearchresult"].get("count")))
    recs = []
    for i in range(0, len(ids), 200):
        chunk = ids[i:i + 200]
        s = get(base + "esummary.fcgi", {"db": "pubmed", "id": ",".join(chunk),
                                         "retmode": "json"})
        for pid in chunk:
            r = s.get("result", {}).get(pid)
            if r:
                recs.append(r)
    with open(os.path.join(RAW, "pubmed.json"), "w", encoding="utf-8") as fh:
        json.dump({"retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "query": 'PSIT[AD] OR "Pranveer Singh"[AD]', "records": recs}, fh)
    print("[PubMed] %d summaries saved" % len(recs))
    return recs


if __name__ == "__main__":
    epmc()
    pubmed()
