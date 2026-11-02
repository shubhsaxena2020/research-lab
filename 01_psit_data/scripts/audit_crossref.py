#!/usr/bin/env python
"""Audit the Crossref affiliation filter and the dataset's coverage.

Three questions, each answered by a computation rather than an opinion:

Q1 ATTRIBUTION - is every record's PSIT evidence traceable to a source?
   For each row we know which harvest contributed it (source column) and which
   affiliation strings matched. Split the corpus into: (a) Crossref-attributed,
   (b) Europe PMC/PubMed-only, (c) Crossref record with no PSIT author string.

Q2 FALSE POSITIVES - does the regex /PSIT|Pranveer Singh/ ever fire on a
   different institution? List every distinct matched affiliation string with
   its paper count and classify it by the words it contains (Kanpur / Pharmacy /
   Higher Education / other city).

Q3 RECALL - what does the filter miss? Take the most prolific PSIT author
   strings, search Crossref by author name, and check every DOI Crossref returns
   against our dataset. A paper by the same author WITH a PSIT affiliation that
   we do not have is a real miss; one without any PSIT string is not attributable
   and is reported separately.

Output: 01_psit_data/raw/crossref_audit.json
Run:    python 01_psit_data/scripts/audit_crossref.py
"""
import csv
import json
import os
import re
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")
PAPERS = os.path.join(ROOT, "papers.csv")
MAILTO = "shubh.saxena2020@gmail.com"
UA = {"User-Agent": "research-lab-psit/1.0 (mailto:%s)" % MAILTO}
PSIT_RE = re.compile(r"PSIT|Pranveer\s*Singh", re.I)


def load():
    with open(PAPERS, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def matched_strings(row):
    return [s.strip() for s in (row["affiliations"] or "").split("|")
            if PSIT_RE.search(s)]


def q1(rows):
    out = {"total": len(rows), "crossref_attributed": 0, "epmc_or_pubmed_only": 0,
           "crossref_no_psit_author_string": 0, "no_affiliation_text": 0,
           "epmc_only_examples": [], "crossref_no_psit_examples": []}
    for r in rows:
        has_cr = r["in_crossref"] == "True"
        has_psit_author = bool((r["psit_authors"] or "").strip())
        has_affil = bool((r["affiliations"] or "").strip())
        if has_cr and has_psit_author:
            out["crossref_attributed"] += 1
        elif not has_cr:
            out["epmc_or_pubmed_only"] += 1
            if len(out["epmc_only_examples"]) < 8:
                out["epmc_only_examples"].append(
                    {"doi": r["doi"], "title": r["title"][:90], "source": r["source"],
                     "year": r["year"]})
        elif has_cr and not has_psit_author:
            out["crossref_no_psit_author_string"] += 1
            if len(out["crossref_no_psit_examples"]) < 8:
                out["crossref_no_psit_examples"].append(
                    {"doi": r["doi"], "title": r["title"][:90],
                     "affil": (r["affiliations"] or "")[:160]})
        if not has_affil:
            out["no_affiliation_text"] += 1
    return out


def q2(rows):
    counts = {}
    for r in rows:
        for s in matched_strings(r):
            key = re.sub(r"\s+", " ", s)[:140]
            counts[key] = counts.get(key, 0) + 1
    classified = {"kanpur": 0, "pharmacy": 0, "higher_education": 0,
                  "no_city_word": 0, "non_kanpur_city": 0}
    other_cities = {"pune", "delhi", "mumbai", "noida", "lucknow", "agra", "jaipur",
                    "hyderabad", "chennai", "bangalore", "bengaluru", "indore",
                    "bhopal", "patna", "varanasi", "mathura", "ghaziabad", "meerut"}
    suspicious = []
    for s, c in sorted(counts.items(), key=lambda x: -x[1]):
        low = s.lower()
        if "kanpur" in low:
            classified["kanpur"] += c
        else:
            classified["no_city_word"] += c
            hit = [city for city in other_cities if city in low]
            if hit:
                classified["non_kanpur_city"] += c
                suspicious.append({"string": s, "papers": c, "other_city": hit})
        if "pharmac" in low:
            classified["pharmacy"] += c
        if "higher education" in low:
            classified["higher_education"] += c
    return {"distinct_matched_strings": len(counts), "by_paper": classified,
            "strings_with_another_city": suspicious[:20],
            "top_strings": [{"string": s, "papers": c}
                            for s, c in sorted(counts.items(), key=lambda x: -x[1])[:12]]}


def cr_author(name, rows_n, tries=3):
    """Crossref author search; returns items."""
    for a in range(tries):
        r = requests.get("https://api.crossref.org/works",
                         params={"query.author": name, "rows": 100,
                                 "select": "DOI,title,author,issued,container-title",
                                 "mailto": MAILTO}, headers=UA, timeout=60)
        if r.status_code == 200:
            time.sleep(1.0)
            return r.json()["message"]["items"]
        time.sleep(10 * (a + 1))
    return []


def q3(rows, top_authors):
    have = {r["doi"].strip().lower() for r in rows if r["doi"].strip()}
    out = {"probes": [], "new_with_psit_affiliation": 0,
           "new_without_psit_affiliation": 0, "unattributable_examples": [],
           "missed_examples": []}
    for name in top_authors:
        items = cr_author(name, len(have))
        new_missed, new_unattr, n_authored = [], [], 0
        for it in items:
            authors = it.get("author", []) or []
            if not any(name.split()[-1].lower() in
                       (x.get("family", "") or "").lower() for x in authors):
                continue
            n_authored += 1
            doi = (it.get("DOI") or "").lower()
            if not doi or doi in have:
                continue
            affs = [af.get("name", "") for x in authors for af in (x.get("affiliation") or [])]
            rec = {"doi": doi,
                   "title": ((it.get("title") or [""])[0])[:90],
                   "year": ((it.get("issued", {}).get("date-parts") or [[None]])[0][0]),
                   "has_psit_affil": any(PSIT_RE.search(a) for a in affs)}
            if rec["has_psit_affil"]:
                new_missed.append(rec)
            else:
                new_unattr.append(rec)
        out["new_with_psit_affiliation"] += len(new_missed)
        out["new_without_psit_affiliation"] += len(new_unattr)
        out["missed_examples"] += [{**r, "author_probe": name} for r in new_missed[:5]]
        out["unattributable_examples"] += [{**r, "author_probe": name} for r in new_unattr[:3]]
        out["probes"].append({"author": name, "crossref_items": len(items),
                              "authored_by_name": n_authored,
                              "already_in_dataset": n_authored - len(new_missed) - len(new_unattr),
                              "new_with_psit": len(new_missed),
                              "new_without_psit": len(new_unattr)})
    return out


def main():
    rows = load()
    # top authors by PSIT-affiliated paper count
    counts = {}
    for r in rows:
        for a in (r["psit_authors"] or "").split(";"):
            a = a.strip()
            if len(a) > 5:
                counts[a] = counts.get(a, 0) + 1
    top = [a for a, _ in sorted(counts.items(), key=lambda x: -x[1])[:3]]
    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "q1_attribution": q1(rows), "q2_false_positives": q2(rows),
              "q3_recall_probe": q3(rows, top)}
    with open(os.path.join(RAW, "crossref_audit.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps(report, indent=1)[:6000])


if __name__ == "__main__":
    main()
