#!/usr/bin/env python
"""S2b screening: dedupe OpenAlex hits, score against the two finalist slices, emit shortlists.

Input : 02_literature/staging/S2b-openalex-hits.jsonl
Output: 02_literature/staging/S2b-screen-C1.json   (family A / topic C1 candidates)
        02_literature/staging/S2b-screen-C3.json   (family D / topic C3 candidates)
        02_literature/staging/S2b-screen-report.txt

Scoring is deliberately dumb and transparent (word lists, printed so the counts can be audited);
it only decides what a human/agent then reads. Verdicts come later from reading, never from this.
"""
import csv
import json
import os
import re

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(LAB, "staging")
ROOT = os.path.dirname(LAB)

C1 = {
    "abstain": r"abstain|abstention|abstaining|refus|decline|defer|escalat|selective prediction|"
               r"answerab|unanswerab|sufficien|insufficien|when to answer|withhold|reject option",
    "retrieval": r"retriev|rag\b|retrieval-augmented|passage|evidence|bm25|dense|rerank|"
                 r"corpus|document set|context",
    "gate": r"threshold|gate|gating|calibrat|operating point|two-sided|band|dead zone|"
            r"risk-coverage|confidence",
    "hardness": r"hard negative|near-miss|negative sampl|difficulty|hardness|ladder|"
                r"perturb|misleading|false premise|unanswerable",
}
C3 = {
    "scam": r"spam|phish|smish|scam|fraud|abuse|malicious message|unsolicited",
    "prevalence": r"prevalence|base rate|class imbalance|imbalanc|prior shift|"
                  r"low prevalence|rare class|deployment|real-world distribution",
    "threshold": r"threshold|operating point|cost-sensitive|cost ratio|false positive|"
                 r"precision|alert|decision",
    "domain": r"sms|message|text message|whatsapp|code-mix|hinglish|india|indian|multilingual",
}


def load():
    rows, seen = [], set()
    with open(os.path.join(STAGE, "S2b-openalex-hits.jsonl"), encoding="utf-8") as f:
        for ln in f:
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if r["openalex_id"] in seen:
                continue
            seen.add(r["openalex_id"])
            rows.append(r)
    return rows


def score(row, spec):
    text = (row.get("title", "") + " " + row.get("abstract", "")).lower()
    hits = {}
    for k, pat in spec.items():
        hits[k] = len(set(re.findall(pat, text)))
    present = sum(1 for v in hits.values() if v)
    # weighted: title hits count double, must have >=3 of 4 concept groups
    t = row.get("title", "").lower()
    tb = sum(1 for pat in spec.values() if re.search(pat, t))
    s = present * 2 + tb * 3 + sum(min(v, 3) for v in hits.values())
    return s, present, tb, hits


def known_titles():
    p = os.path.join(LAB, "verified_citations.csv")
    out = set()
    if os.path.exists(p):
        with open(p, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                out.add(re.sub(r"[^a-z0-9]+", " ", (row.get("title") or "").lower()).strip())
    return out


def main():
    rows = load()
    known = known_titles()
    report = [f"unique OpenAlex works: {len(rows)}"]
    for name, spec, need in (("C1", C1, 3), ("C3", C3, 3)):
        cands = []
        for r in rows:
            s, present, tb, hits = score(r, spec)
            if present >= need and r.get("abstract"):
                r = dict(r)
                r["_score"], r["_present"], r["_titlehits"], r["_hits"] = s, present, tb, hits
                key = re.sub(r"[^a-z0-9]+", " ", r["title"].lower()).strip()
                r["_in_register"] = key in known
                cands.append(r)
        cands.sort(key=lambda r: (-r["_score"], -(r.get("cites") or 0)))
        with open(os.path.join(STAGE, f"S2b-screen-{name}.json"), "w", encoding="utf-8") as f:
            json.dump(cands, f, ensure_ascii=False, indent=1)
        report.append(f"{name}: {len(cands)} candidates pass the {need}-of-4 concept filter "
                      f"(of {len(rows)} works); top 40 written")
        for r in cands[:40]:
            report.append(f"  {r['_score']:>3} {'NEW' if not r['_in_register'] else 'reg'} "
                          f"{r.get('year')} | {r['title'][:105]} | {(r.get('venue') or '')[:45]}")
    with open(os.path.join(STAGE, "S2b-screen-report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report[:12]))
    print(f"... full report: 02_literature/staging/S2b-screen-report.txt")


if __name__ == "__main__":
    main()
