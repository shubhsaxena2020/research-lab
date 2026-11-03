#!/usr/bin/env python
"""Phrase sweep over every cached OpenAlex work + build the citation-claim file.

Part 1 counts, per exact slice phrase, how many of the 3681 unique works contain it in
title+abstract, and prints the matches so each can be eyeballed. This is the check that answers
"does anyone already use this wording", not a relevance ranking.

Part 2 writes 02_literature/staging/S2b-claims.jsonl for verify_citations.py add.
"""
import json
import os
import re

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(LAB, "staging")

PHRASES_C1 = ["two threshold", "two-threshold", "dual threshold", "dead zone", "dead-zone",
              "dead band", "grey zone", "uncertainty band", "admit and refuse", "admit/refuse",
              "false refusal", "over-refusal rate", "abstain precision", "abstain recall",
              "negative hardness", "hardness ladder", "per rung", "retrieval-side feature",
              "retrieval-only feature", "threshold placement", "outside the observed range"]
PHRASES_C3 = ["alerts per", "per 10,000", "per 10000", "operating point", "cost ratio",
              "cost-sensitive threshold", "base rate", "0.1% prevalence", "1% prevalence",
              "code-mixed", "hinglish", "indian english"]

# papers this session will cite as new closest-prior-work rows (openalex id -> why)
CLAIMS = [
    "W7134924609",  # Confidence Gate Theorem
    "W7222995872",  # Training Negatives Still Matter
    None,           # Predictable Failure in Multi-Hop Retrieval (fill by title)
]


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


def sweep(rows, phrases, label):
    print(f"\n=== {label}: {len(rows)} works scanned ===")
    out = []
    for p in phrases:
        pat = re.compile(re.escape(p).replace(r"\ ", r"[\s\-]"), re.I)
        hits = [r for r in rows if pat.search((r.get("title") or "") + " " + (r.get("abstract") or ""))]
        out.append((p, len(hits)))
        print(f"{len(hits):>4}  {p}")
        for r in hits[:4]:
            print(f"        - {r.get('year')} {re.sub(chr(10), ' ', r['title'])[:100]}")
    return out


def main():
    rows = load()
    c1 = sweep(rows, PHRASES_C1, "C1 slice wording")
    c3 = sweep(rows, PHRASES_C3, "C3 slice wording")
    json.dump({"C1": c1, "C3": c3, "corpus": len(rows)},
              open(os.path.join(STAGE, "S2b-phrase-sweep.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
