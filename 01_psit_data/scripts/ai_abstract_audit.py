"""Counted evidence for two sentences in subfolder_ai_research/AI-RESEARCH-AT-PSIT.md.

1. The "no recognised AI venue" claim: a name match on the `venue` column of the
   168 records where ai_related=='yes'.
2. The "evaluation discipline" claim: how often abstracts mention a baseline, a
   random seed, a spread, a significance test, an ablation, etc.

Both are COUNTED, not judged. The script prints the numbers quoted in the document
and writes the same numbers to 01_psit_data/raw/ai_abstract_audit.json, so the
document and its evidence file can be compared mechanically.

No network calls, no sampling, no randomness: sorting and counting only.

Run from the repo root:   python 01_psit_data/scripts/ai_abstract_audit.py
"""
import csv
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "01_psit_data" / "papers.csv"
OUT = ROOT / "01_psit_data" / "raw" / "ai_abstract_audit.json"

RETRIEVED = "2026-11-03"
MIN_ABSTRACT_CHARS = 200   # below this an "abstract" is usually a fragment
NO_ABSTRACT_CHARS = 50     # below this the field is empty or a stub

# Venue names we look for. Whole-token, case-insensitive: "ACL" must not match
# "Oracle", "KDD" must not match inside another word.
VENUE_NAMES = [
    "ACL", "NeurIPS", "NIPS", "ICML", "CVPR", "AAAI", "EMNLP", "ICLR", "KDD",
    "SIGIR", "IJCAI", "ICCV", "ECCV", "NAACL", "WSDM", "CIKM", "TKDE", "TNNLS",
    "Pattern Recognition", "Neural Networks", "Expert Systems with Applications",
]
VENUE_RX = re.compile(
    r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(v) for v in VENUE_NAMES) + r")(?![A-Za-z0-9])",
    re.IGNORECASE,
)

# What an evaluation-hygiene sentence would need. Each entry is one concept with
# the word forms a writer would plausibly use; the regex is deliberately literal.
TERMS = {
    "baseline": r"\bbaselines?\b",
    "random seed": r"\bseeds?\b|random_state|fixed random",
    "spread (std dev or plus-minus)": r"standard deviation|\bstd\.?\b|±",
    "significance test": r"statistical(?:ly)? significan|p-value|p\s*[<=]\s*0\.0[15]",
    "ablation": r"\bablation",
    "confidence interval": r"confidence interval",
    "cross-validation": r"cross[-\s]validation",
    "dataset": r"\bdatasets?\b",
    "accuracy": r"\baccuracy\b",
    "reproducibility (any 'reproduc-')": r"reproduc",
}
EVAL_MARKERS = ["baseline", "random seed", "spread (std dev or plus-minus)",
                "significance test", "ablation"]


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    ai = [r for r in rows if r["ai_related"] == "yes"]
    venues = [(r["venue"] or "").replace("&amp;", "&").strip() for r in ai]
    abstracts = [(r["abstract"] or "").strip() for r in ai]
    audited = [a for a in abstracts if len(a) >= MIN_ABSTRACT_CHARS]

    # ---- 1. venue name match ----
    venue_hits = [(v, r["title"]) for v, r in zip(venues, ai) if VENUE_RX.search(v)]
    distinct_venues = len(set(venues))
    no_venue = sum(1 for v in venues if not v)

    # ---- 2. abstract term counts ----
    counts = {}
    for label, pattern in TERMS.items():
        rx = re.compile(pattern, re.IGNORECASE)
        n = sum(1 for a in audited if rx.search(a))
        counts[label] = {"n": n, "share_of_audited_pct": round(100 * n / len(audited), 1),
                         "regex": pattern}

    eval_rx = re.compile("|".join(TERMS[m] for m in EVAL_MARKERS), re.IGNORECASE)
    n_any_marker = sum(1 for a in audited if eval_rx.search(a))

    # ---- 3. citation split (needed because zero shares differ sharply by year) ----
    def cite_stats(rs):
        c = sorted(int(float(r["cited_by"] or 0)) for r in rs)
        z = sum(1 for x in c if x == 0)
        return {"n": len(c), "zero_citations": z, "zero_pct": round(100 * z / len(c), 1),
                "mean": round(statistics.mean(c), 2), "median": statistics.median(c)}

    citation_split = {
        "field": "cited_by, as deposited by Crossref / Europe PMC",
        "all_ai": cite_stats(ai),
        "by_year": {y: cite_stats([r for r in ai if r["year"] == y])
                    for y in sorted({r["year"] for r in ai})},
        "pooled_2023_2024": cite_stats([r for r in ai if r["year"] in ("2023", "2024")]),
    }

    result = {
        "generated": RETRIEVED,
        "source": "01_psit_data/papers.csv",
        "subset": {"filter": "ai_related == 'yes'", "n_records": len(ai),
                   "n_all_records": len(rows)},
        "venue_name_match": {
            "field": "venue",
            "names_searched": VENUE_NAMES,
            "n_distinct_venue_strings": distinct_venues,
            "n_records_with_blank_venue": no_venue,
            "n_records_matched": len(venue_hits),
            "matches": [{"venue": v, "title": t} for v, t in venue_hits],
            "method_limits": [
                "string match on the deposited venue value, not on a publisher page",
                "an unnamed workshop of a top conference is missed",
                "a differently abbreviated or renamed venue is missed",
                "the dataset is a Crossref + Europe PMC + PubMed union, not a census",
            ],
        },
        "abstract_audit": {
            "min_chars_for_audit": MIN_ABSTRACT_CHARS,
            "n_audited": len(audited),
            "n_no_abstract_below_50_chars": sum(1 for a in abstracts if len(a) < NO_ABSTRACT_CHARS),
            "n_between_50_and_199_chars": sum(
                1 for a in abstracts if NO_ABSTRACT_CHARS <= len(a) < MIN_ABSTRACT_CHARS),
            "term_counts": counts,
            "n_with_any_eval_marker": n_any_marker,
            "eval_marker_definition": EVAL_MARKERS,
            "proxy_caveat": ("Abstracts are a lossy summary. A paper can fix seeds and "
                             "report spreads in its methods section without saying so in the "
                             "abstract, so these counts describe abstract text, not practice. "
                             "No full text was read."),
        },
        "citation_split": citation_split,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- console summary ----
    print(f"subset: {len(ai)} of {len(rows)} records with ai_related=='yes'")
    print(f"venue strings: {distinct_venues} distinct, {no_venue} blank")
    print(f"venue name matches: {len(venue_hits)} of {len(ai)} records")
    print(f"abstracts audited (>= {MIN_ABSTRACT_CHARS} chars): {len(audited)} of {len(ai)}")
    print(f"  no abstract (< {NO_ABSTRACT_CHARS} chars): "
          f"{result['abstract_audit']['n_no_abstract_below_50_chars']}")
    for label, c in counts.items():
        print(f"  {label:<34} {c['n']:>3} of {len(audited)} ({c['share_of_audited_pct']}%)")
    print(f"  {'any of ' + str(len(EVAL_MARKERS)) + ' eval markers':<34} "
          f"{n_any_marker:>3} of {len(audited)} "
          f"({round(100 * n_any_marker / len(audited), 1)}%)")
    print("zero-citation share by year:")
    for y, s in citation_split["by_year"].items():
        print(f"  {y}: {s['zero_citations']:>3} of {s['n']:>3} ({s['zero_pct']}%) "
              f"median={s['median']}")
    s = citation_split["pooled_2023_2024"]
    print(f"  2023-24 pooled: {s['zero_citations']} of {s['n']} ({s['zero_pct']}%) "
          f"mean={s['mean']} median={s['median']}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
