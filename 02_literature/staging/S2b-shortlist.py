#!/usr/bin/env python
"""Second-pass triage: from the 387 C1 / 241 C3 screened candidates, keep only papers whose
title or abstract actually touches the SLICE, and write per-reader batch files.

Slice C1: two separate thresholds / a dead zone / a band on RETRIEVAL-side features, evaluated
          across negatives of differing hardness, reporting over-refusal (false refusal) too.
Slice C3: an operating-point table (precision / recall / alerts per N) at sub-1% prevalence with a
          threshold set from a cost ratio, ideally on code-mixed Indian English SMS.

This script only decides what a reader opens. It makes no verdicts.
"""
import json
import os
import re
import textwrap

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(LAB, "staging")
BATCH = os.path.join(STAGE, "S2b-batches")
os.makedirs(BATCH, exist_ok=True)

C1_SLICE = {
    "two_threshold": r"two threshold|two-threshold|dual threshold|dual-threshold|two sided|two-sided|"
                     r"dead zone|dead-zone|dead band|band of|uncertain(ty)? band|hysteresis|"
                     r"admit.{0,20}refus|refus.{0,20}admit|middle band|grey zone|gray zone",
    "retrieval_features": r"bm25|dense (similarity|retriev)|retrieval score|retrieval feature|"
                          r"similarity score|retriever score|rerank|retrieval confidence|"
                          r"top-?1 score|retrieval-side|retrieval signal",
    "over_refusal": r"false refus|over-?refus|false abstention|abstain precision|abstain recall|"
                    r"over-?abstention|unnecessary abstention|excessive abstention",
    "hardness_ladder": r"hard negative|near-?miss|negative (hardness|difficulty)|rung|ladder|"
                       r"stratified negative|graded difficulty|difficulty level|harder negatives|"
                       r"easy to hard",
}
C3_SLICE = {
    "operating_point": r"operating point|operating-point|alerts per|per 10,?000|alert volume|"
                       r"precision[- ]recall trade|alert budget|threshold sweep",
    "prevalence": r"prevalence|base rate|prior shift|sub-?1 ?%|0\.1 ?%|extreme(ly)? imbalanc|"
                  r"severe imbalanc|realistic (prevalence|mix)",
    "cost_ratio": r"cost (ratio|matrix|sensitive)|cost-sensitive threshold|asymmetric cost|"
                  r"misclassif.{0,20}cost|threshold.{0,30}cost",
    "indic": r"code-?mix|hinglish|indian english|india\b|indic|devanagari|hindi",
}


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def score(text, spec):
    hits = {k: bool(re.search(p, text, re.I)) for k, p in spec.items()}
    return sum(hits.values()), hits


def load(name):
    with open(os.path.join(STAGE, f"S2b-screen-{name}.json"), encoding="utf-8") as f:
        return json.load(f)


def pick(name, spec, need, cap=48):
    rows = load(name)
    keep = []
    for r in rows:
        text = (r.get("title") or "") + " \n " + (r.get("abstract") or "")
        s, hits = score(text, spec)
        if s >= need:
            r["_slice_hits"] = [k for k, v in hits.items() if v]
            r["_slice_score"] = s
            keep.append(r)
    keep.sort(key=lambda r: (-r["_slice_score"], -r.get("_score", 0), -(r.get("cites") or 0)))
    return keep[:cap]


def write_batch(path, rows, title):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        for i, r in enumerate(rows, 1):
            f.write(f"## {i}. {norm(r['title'])}\n")
            f.write(f"year={r.get('year')} | venue={norm(r.get('venue'))[:120]} | "
                    f"cites={r.get('cites')} | openalex={r.get('openalex_id')} | "
                    f"doi={r.get('doi') or '(none)'}\n")
            f.write(f"authors={norm(r.get('authors'))[:200]}\n")
            f.write(f"abstract: {textwrap.fill(norm(r.get('abstract'))[:1600], 110)}\n\n")
    return len(rows)


def main():
    c1 = pick("C1", C1_SLICE, 1, cap=40)
    c3 = pick("C3", C3_SLICE, 2, cap=32)
    json.dump(c1, open(os.path.join(STAGE, "S2b-shortlist-C1.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(c3, open(os.path.join(STAGE, "S2b-shortlist-C3.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    lines = [f"C1 shortlist (>=2 slice concepts in title/abstract): {len(c1)}",
             f"C3 shortlist: {len(c3)}"]
    for i in range(0, len(c1), 8):
        n = write_batch(os.path.join(BATCH, f"C1-part{1 + i // 8}.md"), c1[i:i + 8],
                        f"C1 slice candidates, part {1 + i // 8} of {1 + (len(c1) - 1) // 8}")
        lines.append(f"  C1-part{1 + i // 8}.md  {n} papers")
    for i in range(0, len(c3), 8):
        n = write_batch(os.path.join(BATCH, f"C3-part{1 + i // 8}.md"), c3[i:i + 8],
                        f"C3 slice candidates, part {1 + i // 8} of {1 + (len(c3) - 1) // 8}")
        lines.append(f"  C3-part{1 + i // 8}.md  {n} papers")
    print("\n".join(lines))
    for r in c1[:15]:
        print("C1", r["_slice_score"], r.get("year"), "|", r["title"][:95], "|", ",".join(r["_slice_hits"]))
    for r in c3[:12]:
        print("C3", r["_slice_score"], r.get("year"), "|", r["title"][:95], "|", ",".join(r["_slice_hits"]))


if __name__ == "__main__":
    main()
