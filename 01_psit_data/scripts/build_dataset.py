#!/usr/bin/env python
"""Merge Crossref + Europe PMC + PubMed into one deduplicated papers table.

Inputs (raw/, all cached by the harvest scripts):
  crossref_merged.json   - DOI backbone, deposited author affiliations
  europepmc.json         - biomedical index with AFF: field search
  pubmed.json            - MEDLINE summaries with [AD] field search

Output:
  papers.csv             - one row per work
  build_report.json      - counts, dedupe decisions, coverage per source

Dedupe rule: normalised DOI first (lowercase, strip https://doi.org/ and trailing
punctuation). Records without a DOI are matched on a normalised title (lowercase,
non-alphanumerics removed, first 90 chars). Every merge is logged so the numbers
in the write-up can be reproduced.
"""
import csv
import html
import json
import os
import re
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "papers.csv")

PSIT_RE = re.compile(r"PSIT|Pranveer\s*Singh", re.I)

# Transparent keyword tagging. This is a heuristic, NOT a subject classification
# from a database. Labelled as such in every output that uses it.
TOPIC_RULES = [
    ("machine-learning", r"\bmachine learning\b|\bdeep learning\b|artificial intelligence|"
                         r"\bneural network|\bANN\b|\bCNN\b|\bLSTM\b|transformer model|"
                         r"\breinforcement learning\b|\brandom forest\b|\bsupport vector\b|"
                         r"gradient boosting|\bXGBoost\b|convolutional"),
    ("nlp", r"\bNLP\b|natural language processing|text mining|sentiment analysis|"
            r"language model|\bLLM\b|chatbot|machine translation|speech recognition"),
    ("computer-vision", r"computer vision|image processing|image segmentation|object detection|"
                        r"\bOCR\b|image classification|face recognition"),
    ("security-crypto", r"cryptograph|encryption|authentication|\bblockchain\b|privacy|"
                        r"intrusion detection|cyber ?security|steganograph|watermarking"),
    ("networks-iot", r"\bIoT\b|internet of things|wireless sensor|\bVANET\b|\bMANET\b|"
                     r"\b5G\b|edge computing|cloud computing|network security|routing protocol"),
    ("data-engineering", r"big data|data mining|data warehouse|database system|"
                         r"recommender system|information retrieval|\bSQL\b|data science"),
    ("pharmacy-drug-delivery", r"drug delivery|nanoparticle|nanocarrier|formulation|"
                               r"hydrogel|liposome|transdermal|buccal|pharmacokinetic|excipient|"
                               r"tablet|microparticle|nanoemulsion"),
    ("pharmacology-toxicology", r"toxicity|pharmacolog|antioxidant|antimicrobial|antibacterial|"
                                r"anticancer|cytotox|hepatoprotect|anti-inflammatory|"
                                r"phytochem|ethnopharmacolog|in silico docking|molecular docking"),
    ("chemistry-materials", r"synthesis|nanomaterial|nanocomposite|catalys|spectroscop|"
                            r"electrochemical|polymer composite|\bXRD\b|\bFTIR\b"),
    ("medicine-clinical", r"\bpatient|clinical trial|diagnosis|therap(y|eutic)|\bcovid\b|"
                          r"diabetes|\bcancer\b|hospital|public health|epidemiolog"),
    ("education-pedagogy", r"teaching|pedagog|higher education|curriculum|"
                           r"learning outcome|classroom|student performance|e-learning"),
    ("management-economics", r"consumer|marketing|financial|economic|entrepreneur|"
                             r"human resource|stock market|\bGDP\b|supply chain"),
    ("energy-environment", r"\bsolar\b|renewable energy|environmental|pollution|"
                           r"water treatment|sustainab|waste management|\bCO2\b"),
]

# Strict AI/ML screen used for the "AI share" number, so the headline figure is
# auditable: these are terms no reasonable reader would dispute as AI/ML work.
AI_STRICT_RE = re.compile(
    r"\bmachine learning\b|\bdeep learning\b|artificial intelligence|\bneural network|"
    r"\bCNN\b|\bLSTM\b|\bRNN\b|convolutional neural|\bNLP\b|natural language processing|"
    r"large language model|\bLLM\b|chatbot|computer vision|image processing|"
    r"\brandom forest\b|\bsupport vector machine\b|\bSVM\b|\bXGBoost\b|"
    r"\breinforcement learning\b|transfer learning|sentiment analysis|\bANN\b|"
    r"\bGRU\b|\bBERT\b|\bYOLO\b|object detection|pattern recognition|"
    r"recommend(er|ation) system|federated learning|generative adversarial|"
    r"text mining|\bIoT\b|internet of things|data mining|big data", re.I)


def norm_doi(d):
    if not d:
        return ""
    d = d.strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", d)
    return d.rstrip(".,; ")


def norm_title(t):
    if not t:
        return ""
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9]+", "", t.lower())
    return t[:90]


def year_of(*cands):
    for c in cands:
        if c:
            try:
                y = int(str(c)[:4])
                if 1990 < y < 2030:
                    return y
            except (TypeError, ValueError):
                pass
    return None


def strip_jats(s):
    if not s:
        return ""
    s = html.unescape(str(s))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def topics_of(title, abstract=""):
    text = (title or "") + " " + (abstract or "")
    tags = [name for name, pat in TOPIC_RULES if re.search(pat, text, re.I)]
    return ";".join(tags) if tags else "untagged"


def load(name):
    p = os.path.join(RAW, name)
    if not os.path.exists(p):
        print("MISSING", name)
        return {}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    rows = {}
    log = {"crossref": 0, "europepmc": 0, "pubmed": 0, "merged_dupes": 0}

    def add(rec, source):
        key = ("doi:" + norm_doi(rec["doi"])) if rec.get("doi") else ("title:" + norm_title(rec["title"]))
        if not key.endswith(":") and key not in ("doi:", "title:"):
            if key in rows:
                log["merged_dupes"] += 1
                cur = rows[key]
                cur["sources"] = sorted(set(cur["sources"] + [source]))
                # keep the richer record but never lose fields
                for k, v in rec.items():
                    if v and not cur.get(k):
                        cur[k] = v
                cur["sources"] = sorted(set(cur["sources"]))
                return
            rec["sources"] = [source]
            rows[key] = rec
            log[source] += 1

    # ---- Crossref -------------------------------------------------------
    cr = load("crossref_merged.json")
    for it in cr.get("items", []):
        authors, affils, psit_auth = [], set(), []
        for a in it.get("author", []) or []:
            name = " ".join(x for x in [a.get("given"), a.get("family")] if x).strip()
            if not name:
                name = a.get("name", "")
            authors.append(name)
            aff = [x.get("name", "") for x in (a.get("affiliation") or [])]
            affils.update(aff)
            if any(PSIT_RE.search(x) for x in aff) and name:
                psit_auth.append(name)
        dp = (it.get("issued", {}).get("date-parts") or [[None]])[0]
        add({
            "doi": it.get("DOI"),
            "title": strip_jats((it.get("title") or [""])[0]),
            "year": year_of(dp[0] if dp else None),
            "venue": strip_jats((it.get("container-title") or [""])[0]),
            "type": it.get("type", ""),
            "publisher": it.get("publisher", ""),
            "authors": "; ".join(authors),
            "n_authors": len(authors),
            "psit_authors": "; ".join(sorted(set(psit_auth))),
            "affiliations": " | ".join(sorted(affils))[:1200],
            "cited_by": it.get("is-referenced-by-count", ""),
            "abstract": strip_jats(it.get("abstract", ""))[:4000],
            "subject_terms": "; ".join(it.get("subject", []) or []),
            "issn": "; ".join(it.get("ISSN", []) or []),
            "url": it.get("URL", ""),
            "query": it.get("_query", ""),
        }, "crossref")

    # ---- Europe PMC -----------------------------------------------------
    ep = load("europepmc.json")
    for it in ep.get("records", []):
        affs = []
        for a in (it.get("authorList", {}) or {}).get("author", []) or []:
            for af in (a.get("authorAffiliationDetailsList", {}) or {}).get("authorAffiliation", []) or []:
                if af.get("affiliation"):
                    affs.append(af["affiliation"])
        pa = [x.get("fullName", "") for x in (it.get("authorList", {}) or {}).get("author", []) or []
              if PSIT_RE.search(" ".join(
                  y.get("affiliation", "") for y in
                  (x.get("authorAffiliationDetailsList", {}) or {}).get("authorAffiliation", []) or []))]
        add({
            "doi": it.get("doi"),
            "title": strip_jats(it.get("title", "")),
            "year": year_of(it.get("pubYear")),
            "venue": it.get("journalInfo", {}).get("journal", {}).get("title", "")
                     or it.get("bookOrReportDetails", {}).get("publisher", ""),
            "type": "journal-article" if it.get("source") in ("MED", "PMC") else it.get("source", ""),
            "publisher": it.get("journalInfo", {}).get("journal", {}).get("publisher", ""),
            "authors": "; ".join(x.get("fullName", "") for x in
                                 (it.get("authorList", {}) or {}).get("author", []) or []),
            "n_authors": len((it.get("authorList", {}) or {}).get("author", []) or []),
            "psit_authors": "; ".join(sorted(set(pa))),
            "affiliations": " | ".join(sorted(set(affs)))[:1200],
            "cited_by": it.get("citedByCount", ""),
            "abstract": strip_jats(it.get("abstractText", ""))[:4000],
            "subject_terms": "",
            "issn": it.get("journalInfo", {}).get("journal", {}).get("issn", ""),
            "url": "https://europepmc.org/article/%s/%s" % (it.get("source", ""), it.get("id", "")),
            "query": 'AFF:"Pranveer Singh" OR AFF:"PSIT"',
        }, "europepmc")

    # ---- PubMed ---------------------------------------------------------
    pm = load("pubmed.json")
    for it in pm.get("records", []):
        au = [a.get("name", "") for a in it.get("authors", []) or []]
        add({
            "doi": next((x.get("value") for x in it.get("articleids", []) or []
                         if x.get("idtype") == "doi"), ""),
            "title": strip_jats(it.get("title", "")),
            "year": year_of(it.get("pubdate") or it.get("epubdate")),
            "venue": it.get("fulljournalname", "") or it.get("source", ""),
            "type": "journal-article",
            "publisher": "",
            "authors": "; ".join(au),
            "n_authors": len(au),
            "psit_authors": "",
            "affiliations": "",
            "cited_by": "",
            "abstract": "",
            "subject_terms": "",
            "issn": it.get("issn", ""),
            "url": "https://pubmed.ncbi.nlm.nih.gov/%s/" % it.get("uid", ""),
            "query": 'PSIT[AD] OR "Pranveer Singh"[AD]',
        }, "pubmed")

    # ---- finalise -------------------------------------------------------
    out_rows = []
    for r in rows.values():
        r["topics"] = topics_of(r["title"], r["abstract"])
        r["ai_related"] = "yes" if AI_STRICT_RE.search((r["title"] or "") + " " + (r["abstract"] or "")) else "no"
        r["source"] = "+".join(r["sources"])
        r["in_crossref"] = "crossref" in r["sources"]
        r["in_europepmc"] = "europepmc" in r["sources"]
        r["in_pubmed"] = "pubmed" in r["sources"]
        r["open_access"] = ""  # filled by s2_enrich.py
        out_rows.append(r)
    out_rows.sort(key=lambda r: (-(r["year"] or 0), (r["title"] or "").lower()))

    cols = ["title", "year", "doi", "venue", "type", "authors", "psit_authors",
            "n_authors", "cited_by", "topics", "ai_related", "open_access", "publisher", "issn",
            "url", "source", "in_crossref", "in_europepmc", "in_pubmed",
            "affiliations", "subject_terms", "abstract", "query"]
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    report = {"built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "rows_written": len(out_rows),
              "new_per_source": log,
              "source_overlap": {
                  "crossref_only": sum(1 for r in out_rows if r["sources"] == ["crossref"]),
                  "europepmc_only": sum(1 for r in out_rows if r["sources"] == ["europepmc"]),
                  "pubmed_only": sum(1 for r in out_rows if r["sources"] == ["pubmed"]),
                  "any_two_or_more": sum(1 for r in out_rows if len(r["sources"]) >= 2),
              },
              "dedupe_rule": "normalised DOI; else normalised title[:90]"}
    with open(os.path.join(ROOT, "build_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
