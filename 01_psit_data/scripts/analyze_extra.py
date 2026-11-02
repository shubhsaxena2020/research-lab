#!/usr/bin/env python
"""Secondary counts for 01_psit_data/analysis/ANALYSIS.md -> analysis/numbers_extra.json

`analyze.py` produces the headline numbers. This script produces every other
figure the write-up quotes, so that no number in the document is a hand count.
Each key is a deterministic function of `papers.csv`; re-running on the same CSV
reproduces the JSON byte-for-byte apart from the `generated` timestamp.

Rules that matter for honesty:
- Every regex used for a count is written out as a string in the output under
  the `rules` block, so a reader can see exactly what was matched.
- Text proxies (review titles, "dataset" in abstracts) are crude: they count
  words, not content, and abstract coverage is only 604/793 records.
- Affiliation regexes look at *all* affiliation strings on a record, including
  co-authors' institutions that are not PSIT. A pharmacy department at another
  university therefore counts. That inflates the pharmacy and CS counts
  relative to "PSIT departments only" and is stated in the write-up.
- No network calls. No writes outside analysis/.
"""
import csv
import json
import os
import re
import statistics
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "papers.csv")
OUT = os.path.join(ROOT, "analysis")

# --- patterns, kept here so the write-up can quote them -------------------
RE_PHARMACY_AFFIL = r"pharmac"
RE_CS_AFFIL = r"computer science|computer application|information technology|\bCSE\b"
RE_REVIEW_TITLE = r"review|survey|overview|meta-?analysis"
RE_DATASET = r"\bdataset|\bdata set\b"
RE_EXPERIMENT = r"\bexperiment"
RE_WE_PROPOSE = r"\bwe propose"


def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def main():
    with open(PAPERS, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    N = len(rows)
    out = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_file": "01_psit_data/papers.csv",
        "n_records": N,
        "rules": {
            "pharmacy_affiliation_regex": RE_PHARMACY_AFFIL,
            "cs_affiliation_regex": RE_CS_AFFIL,
            "review_title_regex": RE_REVIEW_TITLE,
            "abstract_dataset_regex": RE_DATASET,
            "abstract_experiment_regex": RE_EXPERIMENT,
            "abstract_we_propose_regex": RE_WE_PROPOSE,
            "affiliation_scope": "all affiliation strings on a record, not only PSIT's",
        },
    }

    def year(r):
        try:
            return int(r["year"])
        except (TypeError, ValueError):
            return None

    def cites(r):
        try:
            return int(float(r["cited_by"]))
        except (TypeError, ValueError):
            return None

    def aff(r):
        return r["affiliations"] or ""

    def in_range(r, lo, hi):
        y = year(r)
        return y is not None and lo <= y <= hi

    # --- growth ---------------------------------------------------------
    yc = Counter(year(r) for r in rows if year(r))
    y2019, y2025 = yc[2019], yc[2025]
    ratio = y2025 / y2019
    out["growth"] = {
        "papers_2019": y2019,
        "papers_2025": y2025,
        "ratio_2019_2025": round(ratio, 2),
        "cagr_2019_2025": round(ratio ** (1 / 6.0), 3),
        "implied_pct_per_year": round(100 * (ratio ** (1 / 6.0) - 1), 1),
    }

    # --- early-year affiliation coverage ---------------------------------
    early = [r for r in rows if in_range(r, 2007, 2015)]
    out["early_year_affiliation"] = {
        "years": "2007-2015",
        "records": len(early),
        "records_with_nonempty_affiliation": sum(1 for r in early if aff(r).strip()),
        "share_pct": pct(sum(1 for r in early if aff(r).strip()), len(early)),
    }

    # --- Bentham cluster -------------------------------------------------
    bent = [r for r in rows if "bentham" in (r["publisher"] or "").lower()]
    b25 = sum(1 for r in bent if year(r) == 2025)
    b26 = sum(1 for r in bent if year(r) == 2026)
    total_delta = yc[2026] - yc[2025]
    out["bentham"] = {
        "records": len(bent),
        "share_pct": pct(len(bent), N),
        "distinct_venues": len({(r["venue"] or "").strip()[:90] for r in bent if (r["venue"] or "").strip()}),
        "records_2025": b25,
        "records_2026": b26,
        "delta_2025_2026": b26 - b25,
        "corpus_delta_2025_2026": total_delta,
        "share_of_2025_2026_increase_pct": pct(b26 - b25, total_delta),
        "publisher_match": "publisher string contains 'bentham' (case-insensitive)",
    }

    # --- 2026 run-rate ---------------------------------------------------
    months = 10  # retrieved 2026-11-03: Jan-Oct
    expected = yc[2025] * months / 12.0
    out["run_rate_2026"] = {
        "papers_2026": yc[2026],
        "months_elapsed": months,
        "expected_at_2025_rate": round(expected, 1),
        "ratio_vs_2025_rate": round(yc[2026] / expected, 2),
        "formula": "papers_2026 / (papers_2025 * months_elapsed / 12)",
    }

    # --- topic groups (primary tags) -------------------------------------
    prim = Counter()
    for r in rows:
        tags = [t for t in (r["topics"] or "").split(";") if t and t != "untagged"]
        prim[tags[0] if tags else "untagged"] += 1
    pharm_tags = ["medicine-clinical", "pharmacology-toxicology", "pharmacy-drug-delivery"]
    cs_tags = ["machine-learning", "security-crypto", "networks-iot", "nlp",
               "data-engineering", "computer-vision"]
    ph = sum(prim.get(t, 0) for t in pharm_tags)
    cs = sum(prim.get(t, 0) for t in cs_tags)
    out["topic_groups_primary"] = {
        "pharmacy_medicine": {"tags": pharm_tags, "papers": ph, "share_pct": pct(ph, N)},
        "computer_science_flavoured": {"tags": cs_tags, "papers": cs, "share_pct": pct(cs, N)},
        "note": "primary tag = first matching keyword rule; groups are not exhaustive",
    }

    # --- affiliation department groups (record level) --------------------
    ph_rec = sum(1 for r in rows if re.search(RE_PHARMACY_AFFIL, aff(r), re.I))
    cs_rec = sum(1 for r in rows if re.search(RE_CS_AFFIL, aff(r), re.I))
    out["affiliation_departments"] = {
        "pharmacy_named_records": ph_rec,
        "pharmacy_share_pct": pct(ph_rec, N),
        "computer_science_named_records": cs_rec,
        "computer_science_share_pct": pct(cs_rec, N),
        "note": "any affiliation string on the paper, including non-PSIT co-authors'",
    }

    # --- shares quoted in the write-up ------------------------------------
    types = Counter(r["type"] or "unknown" for r in rows)
    out["type_shares_pct"] = {t: pct(c, N) for t, c in types.most_common()}
    out["topic_primary_shares_pct"] = {t: pct(c, N) for t, c in prim.most_common()}
    out["topic_multilabel_total"] = sum(
        len([t for t in (r["topics"] or "").split(";") if t and t != "untagged"]) for r in rows)
    out["collaboration_shares"] = {
        "papers_6plus": sum(1 for r in rows if (r["n_authors"] or "").isdigit() and int(r["n_authors"]) >= 6),
        "papers_6plus_share_pct": pct(sum(1 for r in rows if (r["n_authors"] or "").isdigit()
                                          and int(r["n_authors"]) >= 6), N),
        "single_author_papers": sum(1 for r in rows if (r["n_authors"] or "").isdigit()
                                    and int(r["n_authors"]) == 1),
        "single_author_share_pct": pct(sum(1 for r in rows if (r["n_authors"] or "").isdigit()
                                          and int(r["n_authors"]) == 1), N),
    }
    psit_strings = set()
    psit_string_counts = Counter()
    for r in rows:
        for a in (r["psit_authors"] or "").split(";"):
            a = a.strip()
            if a and len(a) > 3:
                psit_strings.add(a)
                psit_string_counts[a] += 1
    ten_plus = sum(1 for c in psit_string_counts.values() if c >= 10)
    out["collaboration_shares"]["authors_10plus"] = ten_plus
    out["collaboration_shares"]["authors_10plus_share_of_psit_strings_pct"] = pct(ten_plus, len(psit_strings))

    # --- AI before 2019 ---------------------------------------------------
    pre = [r for r in rows if in_range(r, 2007, 2018)]
    out["ai_before_2019"] = {
        "papers": len(pre),
        "ai_related": sum(1 for r in pre if r["ai_related"] == "yes"),
    }

    # --- venue concentration ---------------------------------------------
    venues = Counter((r["venue"] or "").strip()[:90] for r in rows if (r["venue"] or "").strip())
    top10 = venues.most_common(10)
    top10_n = sum(c for _, c in top10)
    largest_name, largest_n = venues.most_common(1)[0]
    out["venue_concentration"] = {
        "distinct_venues": len(venues),
        "venues_with_1_paper": sum(1 for c in venues.values() if c == 1),
        "venues_with_1_paper_share_pct": pct(sum(1 for c in venues.values() if c == 1), len(venues)),
        "papers_in_1_paper_venues": sum(c for c in venues.values() if c == 1),
        "share_of_papers_in_1_paper_venues_pct": pct(sum(c for c in venues.values() if c == 1), N),
        "top10_papers": top10_n,
        "top10_share_pct": pct(top10_n, N),
        "largest_venue": largest_name,
        "largest_venue_papers": largest_n,
        "largest_venue_share_pct": pct(largest_n, N),
    }

    # --- the top venue's author concentration ----------------------------
    joc = [r for r in rows if "Optical Communications" in (r["venue"] or "")]
    kk_venue = sum(1 for r in joc if "Keshav Kumar" in (r["psit_authors"] or ""))
    kk_all = sum(1 for r in rows if "Keshav Kumar" in (r["psit_authors"] or ""))
    out["top_venue_group"] = {
        "venue": "Journal of Optical Communications",
        "papers": len(joc),
        "papers_2025_2026": sum(1 for r in joc if year(r) in (2025, 2026)),
        "keshav_kumar_papers_in_venue": kk_venue,
        "keshav_kumar_papers_corpus": kk_all,
    }

    # --- citation concentration ------------------------------------------
    c = sorted([x for x in (cites(r) for r in rows) if x is not None], reverse=True)
    tot = sum(c)
    out["citation_concentration"] = {
        "total": tot,
        "top1_share_pct": pct(c[0], tot),
        "top3_share_pct": pct(sum(c[:3]), tot),
        "top5_share_pct": pct(sum(c[:5]), tot),
        "max": c[0],
    }

    # --- age cohorts ------------------------------------------------------
    cohorts = {}
    for label, lo, hi in (("cohort_2007_2023", 2007, 2023), ("cohort_2024_2026", 2024, 2026)):
        sub = [x for x in (cites(r) for r in rows if in_range(r, lo, hi)) if x is not None]
        cohorts[label] = {
            "records": len(sub),
            "share_of_corpus_pct": pct(len(sub), N),
            "median": statistics.median(sub),
            "mean": round(statistics.mean(sub), 2),
            "zero_share_pct": pct(sum(1 for x in sub if x == 0), len(sub)),
        }
    out["year_cohorts"] = cohorts

    # --- named authors ----------------------------------------------------
    wal = [r for r in rows if "Pranay Wal" in (r["psit_authors"] or "")]
    wal_a = [r for r in rows if "Ankita Wal" in (r["psit_authors"] or "")]
    out["named_authors"] = {
        "pranay_wal_papers": len(wal),
        "pranay_wal_share_pct": pct(len(wal), N),
        "pranay_wal_papers_2026": sum(1 for r in wal if year(r) == 2026),
        "ankita_wal_papers": len(wal_a),
        "note": "name strings, not disambiguated people",
    }

    # --- abstract coverage and text proxies -------------------------------
    ab = [r for r in rows if (r["abstract"] or "").strip()]
    n_ab = len(ab)

    def has(pat, r):
        return bool(re.search(pat, r["abstract"] or "", re.I))

    review_titles = sum(1 for r in rows if re.search(RE_REVIEW_TITLE, r["title"] or "", re.I))
    ai_ab = [r for r in ab if r["ai_related"] == "yes"]
    out["abstract_coverage"] = {
        "records_with_abstract": n_ab,
        "share_pct": pct(n_ab, N),
    }
    out["text_proxies"] = {
        "review_title_records": review_titles,
        "review_title_share_pct": pct(review_titles, N),
        "abstracts": n_ab,
        "abstract_dataset": sum(1 for r in ab if has(RE_DATASET, r)),
        "abstract_dataset_pct": pct(sum(1 for r in ab if has(RE_DATASET, r)), n_ab),
        "abstract_experiment": sum(1 for r in ab if has(RE_EXPERIMENT, r)),
        "abstract_experiment_pct": pct(sum(1 for r in ab if has(RE_EXPERIMENT, r)), n_ab),
        "abstract_we_propose": sum(1 for r in ab if has(RE_WE_PROPOSE, r)),
        "abstract_we_propose_pct": pct(sum(1 for r in ab if has(RE_WE_PROPOSE, r)), n_ab),
        "ai_abstracts": len(ai_ab),
        "ai_abstract_dataset": sum(1 for r in ai_ab if has(RE_DATASET, r)),
        "ai_abstract_dataset_pct": pct(sum(1 for r in ai_ab if has(RE_DATASET, r)), len(ai_ab)),
        "note": "single-keyword proxies on titles/abstracts; they undercount and are not a content analysis",
    }

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "numbers_extra.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: out[k] for k in ("growth", "bentham", "run_rate_2026",
                                         "venue_concentration", "text_proxies")}, indent=1))
    print("wrote", os.path.join(OUT, "numbers_extra.json"))


if __name__ == "__main__":
    main()
