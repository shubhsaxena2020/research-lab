"""B6: build the AI-subset tables from 01_psit_data/papers.csv.

Run from repo root:  python 01_psit_data/scripts/ai_subset_tables.py
Writes CSVs into 01_psit_data/subfolder_ai_research/ and prints the summary
numbers quoted in AI-RESEARCH-AT-PSIT.md. Deterministic (no sampling).
"""
import collections
import csv
import os
import statistics

SRC = "01_psit_data/papers.csv"
OUT = "01_psit_data/subfolder_ai_research"

# Recognised AI venues we check for by name only (no API calls).
AI_VENUE_NAMES = [
    "neurips", "neural information processing", "icml",
    "international conference on machine learning", "acl",
    "association for computational linguistics", "cvpr",
    "computer vision and pattern recognition", "aaai", "emnlp", "iclr",
    "ijcai", "eccv", "kdd", "sigir", "interspeech", "miccai", "eacl", "naacl",
]
REVIEW_WORDS = ("review", "survey", "overview", "insight", "systematic",
                "perspective", "meta-analysis", "advances in", "recent")


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    ai = [r for r in rows if r["ai_related"] == "yes"]
    os.makedirs(OUT, exist_ok=True)

    # ---- 40 most recent (year desc, then original file order) ----
    recent = sorted(ai, key=lambda r: -int(r["year"]))[:40]
    with open(f"{OUT}/table_ai_recent40.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "title", "venue", "psit_authors", "doi"])
        for r in recent:
            w.writerow([r["year"], r["title"], r["venue"].replace("&amp;", "&"),
                        r["psit_authors"], r["doi"]])

    # ---- topics inside the AI subset (multi-label) ----
    tc = collections.Counter()
    for r in ai:
        for t in r["topics"].split(";"):
            if t.strip():
                tc[t.strip()] += 1
    with open(f"{OUT}/table_ai_topics.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["topic", "ai_papers", "share_of_168_pct"])
        for t, c in tc.most_common():
            w.writerow([t, c, round(100 * c / len(ai), 1)])

    # ---- authors inside the AI subset (name variants left as published) ----
    ac = collections.Counter()
    for r in ai:
        for a in r["psit_authors"].split(";"):
            if a.strip():
                ac[a.strip()] += 1
    with open(f"{OUT}/table_ai_authors.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["psit_author_as_published", "ai_papers"])
        for a, c in ac.most_common(30):
            w.writerow([a, c])

    # ---- venues ----
    vc = collections.Counter((r["venue"] or "(none recorded)").replace("&amp;", "&").strip()
                             for r in ai)
    with open(f"{OUT}/table_ai_venues.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["venue", "ai_papers"])
        for v, c in vc.most_common(15):
            w.writerow([v, c])

    # ---- summary numbers ----
    cit = sorted(int(float(r["cited_by"])) for r in ai if r["cited_by"] not in ("", "None"))

    def q(p):
        i = p * (len(cit) - 1)
        lo = int(i)
        return cit[lo] if i == lo else (cit[lo] + cit[lo + 1]) / 2

    rev = [r for r in ai if any(w in r["title"].lower() for w in REVIEW_WORDS)]
    conf = [r for r in ai if "conference" in r["venue"].lower()
            or "proceedings" in r["venue"].lower()]
    hits = [r for r in ai if any(t in (r["venue"] + " " + r["title"]).lower()
                                 for t in AI_VENUE_NAMES)]
    print(f"n_ai={len(ai)} of {len(rows)} ({100*len(ai)/len(rows):.1f}%)")
    print("by_year:", dict(sorted(collections.Counter(r["year"] for r in ai).items())))
    print("by_type:", dict(collections.Counter(r["type"] for r in ai)))
    print(f"review_titles={len(rev)} ({100*len(rev)/len(ai):.1f}%)")
    print(f"conference_named_venue={len(conf)} ({100*len(conf)/len(ai):.1f}%)")
    print(f"no_abstract={sum(1 for r in ai if len(r['abstract'].strip()) < 50)}")
    print(f"distinct_venues={len(vc)}; venues_with_1_paper={sum(1 for c in vc.values() if c==1)}")
    print(f"single_machine-learning_tag={sum(1 for r in ai if r['topics'].strip()=='machine-learning')}")
    print(f"cite_mean={statistics.mean(cit):.2f} q25={q(.25)} median={q(.5)} q75={q(.75)} "
          f"p90={q(.9)} max={max(cit)} zero={sum(1 for c in cit if c==0)}")
    print(f"distinct_psit_authors={len(ac)}")
    print(f"recognised_ai_venue_name_matches={len(hits)}")
    for h in hits:
        print("   HIT:", h["venue"], "|", h["title"][:70])


if __name__ == "__main__":
    main()
