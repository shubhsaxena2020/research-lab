# PSIT research output: what this folder holds, and what it cannot tell you

**What this page is for.** One table of papers claiming a Pranveer Singh Institute of Technology (PSIT) affiliation, the scripts that built it, and the tables computed from it. Read this before quoting any number out of it. The finding that matters is not the paper count — it is that "PSIT" in the world's bibliographic databases means three institutions at once, and the surviving record is named "Pharmacy".

Retrieved 2026-11-03. Public data only; nothing came from behind a login.

## 1. What this folder contains

| File | What it is | Made by | Trust |
|---|---|---|---|
| `papers.csv` | 793 rows × 28 columns, one row per work | `build_dataset.py` | Medium — real metadata, regex affiliation filter |
| `build_report.json` | Row counts, per-source counts, dedupe rule | `build_dataset.py` | High |
| `analysis/numbers.json` | Every figure used in the write-ups, one key each | `analyze.py` | High, except one dead key (§4) |
| `analysis/tables/*.md`, `*.csv` | 10 tables: year, type, AI share, topics, venues, authors, citations, top-cited, affiliation vocabulary | `analyze.py` | High as arithmetic; labels are heuristics |
| `raw/crossref/*.json` | 17 cached Crossref pages, 1000 rows each | `harvest_crossref.py` | High — verbatim, re-runs read cache |
| `raw/crossref_merged.json` | 690 unique PSIT DOIs after the local regex | `harvest_crossref.py` | High |
| `raw/europepmc.json` | 283 records, affiliation-field query | `harvest_epmc_pubmed.py` | Medium — EPMC's affiliation parser is fuzzy (§2.6) |
| `raw/pubmed.json` | 280 MEDLINE summaries, `[AD]` query | same | Medium — no per-author affiliation saved |
| `raw/openalex_institution_I4405287327.json` | The one OpenAlex institution record we got | one call, then 429 | High in content, useless as a work list |
| `raw/ror_04v8v3741.json` | The ROR record, saved by this write-up | live call 2026-11-03 | High |
| `raw/s2_unavailable.json`, `raw/dblp_unavailable.json` | Proof of the 429 blocks | `enrich_s2_dblp.py --skip-s2` | Evidence, not data |
| `scripts/*.py` | 6 scripts, harvest → build → analyze | hand-written | High — every number reproduces |
| `COVERAGE-COMPARISON.md` and other `*.md` siblings here | Item B2 and later write-ups that read this dataset | written in this session, one file per item | High as argument; each quotes `numbers.json` |

## 2. The institutional identity question

### 2.1 Three entities, three websites

| Entity | What it is | Own site, checked 2026-11-03 |
|---|---|---|
| PSIT (engineering college), Bhauti, Kanpur | B.Tech, M.Tech, MBA, MCA — what most people mean by "PSIT" | `psit.ac.in`, title "Best Engineering College in Kanpur \| PSIT Kanpur" [4] |
| PSIT College of Higher Education (PSIT-CHE) | Where Shubh studies: the site lists two streams, Computer Applications (BCA) and Management (BBA) | `psitche.ac.in`, title "PSIT College of Higher Education" [5] |
| PSIT College of Pharmacy | PCI-approved B.Pharm, M.Pharm | `psitpharmacy.ac.in`, "PSIT Pharmacy … PCI-approved B.Pharm and M.Pharm" [6] |

Three domains, three front pages, three course catalogues: related, physically close, not the same institution. The engineering college's own homepage advertises "B.Tech, M.Tech, BCA, MCA, MBA, BBA & Pharmacy courses" [4], so the marketing blurs the boundary as well — expect no cleaner metadata.

### 2.2 ROR has exactly one record, and it is the Pharmacy

ROR (Research Organization Registry — the open institution-identifier register most scholarly tools build on) returns **one** result for "Pranveer": `ror.org/04v8v3741` [1]. Quoted from `raw/ror_04v8v3741.json`:

- display name: **"Pranveer Singh Institute of Technology (Pharmacy), Kanpur"**
- aliases: `PSIT-Pharmacy`, `PSIT-Pranveer Singh Institute of Technology, Pharmacy`, and — stare at this one — **`Pranveer Singh Institute of Technology, Kanpur`**
- `links` and `domains`: `psitpharmacy.ac.in`; `established` 2004; `types`: education; one location, Kanpur
- `external_ids`: empty (no GRID, no Wikidata, no ISNI)

The bare engineering-college name, with no "(Pharmacy)" in it, is an alias *of the pharmacy record*. Any matcher seeing it resolves here, because there is no second record to resolve to.

### 2.3 OpenAlex has exactly one record, and it is also the Pharmacy

`I4405287327` [2], saved in `raw/`:

- `display_name`: "Pranveer Singh Institute of Technology (Pharmacy), Kanpur"
- `ror`: `https://ror.org/04v8v3741` — the same id; `homepage_url`: `psitpharmacy.ac.in`
- `works_count`: **1412**; `cited_by_count`: 25098; `h_index`: 52; `i10_index`: 530
- `display_name_alternatives` includes "PSIT-Pharmacy" and again "Pranveer Singh Institute of Technology, Kanpur"
- `counts_by_year`: 284 works (2026), 245 (2025), 224 (2024)

OpenAlex builds its institution list from ROR, so this is not a second observation — the same node through a second window. Both systems agree, and both are wrong about the engineering college and PSIT-CHE.

### 2.4 What this means for any "PSIT publication count"

1. **Any published PSIT count mixes the entities.** "PSIT has 1412 papers" (OpenAlex node, 2026-11-03) counts a node called "(Pharmacy)" that absorbs engineering papers through the alias. You cannot subtract your way out: the node does not record which entity each paper belongs to.
2. **A PSIT-CHE paper is very likely counted under "PSIT-Pharmacy", or under nothing at all.** What decides is the deposited string and the alias the matcher hit, not what the author meant.
3. **Our 793 and their 1412 are different measurements, neither authoritative** (793: numbers.json `n_records`). The 619-record gap is the finding: a count that differs by that much between two public sources is not well defined. Quote both, with node and date.
4. **Do not merge, do not split.** No evidence field supports a split. Report counts per string pattern and state the ambiguity.

### 2.5 How the strings actually appear

`affiliation_buckets` in `numbers.json` counts paper×affiliation-string pairs for strings matching `PSIT|Pranveer\s*Singh`. A paper can contribute more than one, so these are not shares of 793:

| Bucket | Pairs | Reading |
|---|---|---|
| `mentions_Pranveer` | **776** | The spelled-out name dominates |
| `mentions_kanpur` | **746** | Location nearly always present — and disambiguates nothing: all three are in Kanpur |
| `mentions_pharmacy` | **400** | Half the strings say "pharmacy" — hence the node's name |
| `mentions_PSIT_abbrev` | **342** | The bare abbreviation identifies nothing on its own |
| `mentions_higher_education` | **21** | **PSIT-CHE's entire visible footprint**: 21 strings, 21 different papers |
| `records_with_affil_text_nonempty` | `792` | rows whose `affiliations` cell is non-empty |
| `records_with_psit_affil_string` | `784` | rows with at least one affiliation string naming PSIT |

CHE is 21 of 793 records, about 2.6%. Trust these counts alone and you would conclude PSIT-CHE barely publishes — when you are measuring deposit habits. Distinct strings: **563** (`affiliation_strings_distinct`) across 856 matching pairs (computed from `papers.csv`).

**Eight verbatim strings**, copied character-for-character, missing spaces included:

| # | String as deposited | Paper | Year | DOI |
|---|---|---|---|---|
| 1 | `Pranveer Singh Institute of Technology` | A Resilient Bacterial Foraging Optimization Algorithm … | 2026 | 10.1109/ic-sit69723.2026.11735761 |
| 2 | `Pranveer Singh Institute of Technology,Department of Computer Science and Engineering,Kanpur,India` | A Graph-Based NLP for Threat Detection in Healthcare | 2026 | 10.1109/icisessc68634.2026.11542786 |
| 3 | `PSIT-Pranveer Singh Institute of Technology (Pharmacy), Kanpur, India` | The Intricacies of Polypharmacy and Drug Interactions … | 2026 | 10.2174/0113892002382047250930160449 |
| 4 | `Department of Pharmacy, Pranveer Singh Institute of Technology, Kanpur, India` | Antioxidant and Cytotoxic Activity of the Aporphine Alkaloid (Boldine) … | 2025 | 10.2174/0115734064358287250613065507 |
| 5 | `PSIT-Pranveer Singh Institute of Technology (Pharmacy), Kalpi Road, Bhauti, Kanpur-208020, India` | Dendrimers in Breast Cancer Management: A Review … | 2026 | 10.2174/0115734048432986260701072348 |
| 6 | `PSIT College of Higher Education` | Efficient Phishing URL Detection Using Minimal- Feature Machine Learning Models | 2026 | 10.1109/gtss68743.2026.11679599 |
| 7 | `PSIT College of Higher EducationKanpur, Computer Application, Kanpur, India` | Classification & Technological Analysis of Load Balancing in Cloud Computing | 2026 | 10.2174/0118722121358630241220044608 |
| 8 | `Department of Computer Applications, Pranveer Singh Institute of Technology, Kanpur, India` | An intelligent federated learning boosted cyberattack … | 2025 | 10.1038/s41598-025-96986-5 |

1–2 are the engineering college writing its own name unqualified. 3–5 are unambiguously Pharmacy (parenthetical, Kalpi Road, PIN 208020). 6–7 are PSIT-CHE — 7 has lost a space where the publisher concatenated two fields, a reminder that this text is machine-assembled. 8 is the ambiguous case: "Department of Computer Applications" under the plain institute name. BCA is a CHE programme [5]; the string names the engineering college. Which did the author mean? The string cannot tell you.

### 2.6 Rows we could not confirm

Nine of 793 rows (1.1%, computed from `papers.csv`) carry no PSIT or Pranveer string in their deposited affiliations: five Chitkara/Amity papers and three Rajasthan university papers returned by Europe PMC's `AFF:` search, plus one PubMed-only row with no affiliation saved. Either a PSIT co-author exists but the index kept another author's string, or the match was loose. Treat them as **unverified** — too few to move a percentage in §3 by half a point, but do not cite one without opening the paper.

## 3. How the dataset was built

**Step 1, Crossref.** `harvest_crossref.py` pages `api.crossref.org/works` with three quoted `query.affiliation` phrases: `"Pranveer"`, `"PSIT"`, `"PSIT Kanpur"`. Crossref reported 645 results for `"Pranveer"` — all 645 scanned, 636 kept; 278 for `"PSIT"` — 278 kept; 18,651 for `"PSIT Kanpur"`, of which the first 3,000 (the relevance-ranked head) yielded 2. After DOI dedupe: **690** unique PSIT DOIs.

The honest limitation starts here: `query.affiliation` is a **relevance-ranked free-text search, not a filter**. `"PSIT"` returning 278 hits that all match is luck, not design. The real filter is the local regex `PSIT|Pranveer\s*Singh` over every deposited affiliation string; a hit that fails is dropped. So a real PSIT paper ranked outside the head of `"PSIT Kanpur"` is never seen — the phrase list matters more than the ranking.

**Step 2, Europe PMC.** `harvest_epmc_pubmed.py` runs `AFF:"Pranveer Singh" OR AFF:"PSIT"`, storing 283 records — a true affiliation-field query, which Crossref cannot do.

**Step 3, PubMed.** The same script runs `PSIT[AD] OR "Pranveer Singh"[AD]`, storing 280 summaries. These carry no per-author affiliation, so they contribute identity only.

**Step 4, merge and dedupe.** `build_dataset.py` deduplicates on the normalised DOI (lowercase, strip `https://doi.org/`, strip trailing punctuation), falling back to the normalised title (lowercase, non-alphanumerics removed, first 90 characters) when no DOI exists. Log: 690 Crossref + 102 Europe PMC + 1 PubMed new records, **460 duplicates merged away** (`build_report.json`: `new_per_source`, `merged_dupes`). Overlap: 509 Crossref-only, 4 Europe PMC-only, 1 PubMed-only, 279 in two or more sources.

**The limitation that matters most:** only *deposited* affiliation strings are visible. Where a publisher recorded none — common in older proceedings, some Indian journals, and any paper whose corresponding author left the field blank — the paper is **invisible**, however often it was published. Absence here is not absence from PSIT's output, and that bites hardest on PSIT-CHE, whose 21 strings are a fraction of its real output.

Mechanically, `affiliations` is truncated at **1200 characters** per record (`" | ".join(sorted(affils))[:1200]`), so on papers with long co-author lists the PSIT string can be cut — one plausible cause of the 9 rows in §2.6.

## 4. Data dictionary for `papers.csv`

793 rows, 28 columns. `build_dataset.py` writes 23; `enrich_s2_dblp.py` appends five `s2`/`oa_pdf_url` columns, empty because Semantic Scholar was blocked.

| Column | Type — meaning | Known weakness |
|---|---|---|
| `title` | text — work title | Publisher markup occasionally leaks |
| `year` | int — issued year (Crossref, else EPMC `pubYear`, else PubMed date) | Online-first vs print can differ by one; 1 row empty; **2026 partial** (`year_2026_is_partial`) — 234 papers for 10 months |
| `doi` | text — normalised lowercase DOI | 1 row has none |
| `venue` | text — journal/proceedings as deposited | Not normalised: 394 distinct, 258 with a single paper |
| `type` | text — Crossref type (`journal-article` 599, `proceedings-article` 132, `book-chapter` 44, `posted-content` 15, `other` 2, `edited-book` 1) | EPMC/PubMed rows forced to `journal-article`, so reliable only for Crossref rows |
| `authors` | text — all names, `"; "`-joined | No ORCID disambiguation: 2237 distinct strings ≠ 2237 people |
| `psit_authors` | text — names whose **own** affiliation string matched PSIT | Needs that author's affiliation to be deposited; Crossref sometimes attaches one string to all authors, sometimes none. 507 distinct strings, 27 with 10+ papers |
| `n_authors` | int — author count | Missing author entries deflate it |
| `cited_by` | int — Crossref `is-referenced-by-count` (EPMC `citedByCount` for 4 rows) | **Crossref only**: a lower bound, not comparable with OpenAlex or Scopus. Total 5476, mean 6.91, median 1.0, 40.3% at zero |
| `topics` | text — `";"`-joined tags from 13 regex rules (`TOPIC_RULES`) | **Keyword heuristic, not a classification.** 167 rows untagged |
| `ai_related` | text — `yes`/`no` from a strict AI/ML term list over title+abstract | Under-counts work that uses ML without naming it. 168 yes (21.2%) |
| `open_access` | text — intended OA status | **Empty** (S2 blocked). Do not report an OA share |
| `publisher` | text — Crossref publisher | Empty for 103 rows (EPMC/PubMed-only) |
| `issn` | text — `";"`-joined ISSNs | Sometimes print and electronic, sometimes neither |
| `url` | text — DOI link, or an EPMC/PubMed article URL | Not a landing-page guarantee |
| `source` | text — `+`-joined provenance (509 crossref, 181 crossref+europepmc+pubmed, 98 europepmc+pubmed, 4 europepmc, 1 pubmed) | — |
| `in_crossref`, `in_europepmc`, `in_pubmed` | text — `True`/`False` | Capitalised Python booleans: filter `== "True"` |
| `affiliations` | text — **all** affiliation strings, `" \| "`-joined, sorted, cut at 1200 chars | Author→affiliation mapping is **lost** in the join; truncation can cut the PSIT string; this is the column §2 rests on |
| `subject_terms` | text — Crossref `subject` | **Empty for all rows**; Crossref has effectively retired it |
| `abstract` | text — abstract, tags stripped, cut at 4000 chars | Only 604 of 793 rows have one, which is why `topics` and `ai_related` miss papers |
| `query` | text — harvest query that first found it | A record found twice keeps only the first |
| `in_s2`, `s2_citation_count`, `s2_venue`, `s2_fields`, `oa_pdf_url` | text — intended S2 enrichment | **All empty / `not-checked`** |

**Fixed after review (2026-11-03, 04:20 IST).** An earlier `numbers.json` carried `affiliation_buckets.records_with_affil_string` = `0`, a key `analyze.py` initialised and never incremented. It was replaced by two explicitly named counts, `records_with_affil_text_nonempty` = **792** and `records_with_psit_affil_string` = **784**; the script was re-run and no other figure changed (793 records, 168 AI-related, 394 venues, median 1 citation). Every key was cross-checked against `papers.csv` for this write-up.

## 5. Reproducing

From the repo root, Python 3.11. Raw pages are cached, so re-runs are free until you add `--fresh`.

```bash
python 01_psit_data/scripts/harvest_crossref.py --max-pages 3
#  -> raw/crossref/*.json, raw/crossref_merged.json
#     expect 645/636, 278/278, 3000 scanned/2 kept, 690 unique DOIs
python 01_psit_data/scripts/harvest_epmc_pubmed.py
#  -> raw/europepmc.json (283), raw/pubmed.json (280)
python 01_psit_data/scripts/build_dataset.py
#  -> papers.csv (793), build_report.json (690 + 102 + 1, 460 merged)
python 01_psit_data/scripts/analyze.py
#  -> analysis/numbers.json, analysis/tables/*.md|.csv
python 01_psit_data/scripts/harvest_openalex.py --max-pages 1   # 429 until 00:00 UTC
python 01_psit_data/scripts/enrich_s2_dblp.py --skip-s2         # records the 429s
```

Steps 1–4 take about a minute from cache, a few cold (scripts sleep 1s between Crossref calls, per RULES.md rule 8). Sanity checks: 793 rows; `n_records` 793; `citations_total` 5476; `distinct_psit_authors` 507. Different counts after a fresh harvest are normal — Crossref grows — but then regenerate every number with `analyze.py`, never by hand.

## 6. What is not here, and why

- **OpenAlex work-level data** (topics, per-work OA, author ids, its 1412-work list): HTTP 429, daily budget exhausted from this network on 2026-11-03. `harvest_openalex.py` re-runs after the reset.
- **Semantic Scholar fields** (independent citation counts, `fieldsOfStudy`, OA PDFs): 429 on both endpoints (`raw/s2_unavailable.json`). Hence the empty `open_access`.
- **DBLP venue typing:** 429 / connection reset, and DBLP has no affiliation search. `in_dblp_yes: 0` with `in_dblp_checked: 0` means **not measured**, never "not in DBLP".
- **Scopus / Web of Science indexing, JCR quartiles:** subscription data; do not infer indexing from a journal name.
- **Patents and funded projects:** other registries (IP India / InPASS, funders); item B3 covers institute-published figures.
- **Papers under review, "ongoing" projects, internal monitoring:** not public by definition. RULES.md rule 7 — record UNAVAILABLE, ask the R&D cell.
- **PSIT-CHE as its own institution:** not fixable by searching harder. A CHE-only count needs author-level and departmental evidence, and must say so.

## Sources

1. ROR API record `04v8v3741` — https://api.ror.org/v2/organizations/04v8v3741 (retrieved 2026-11-03; saved as `raw/ror_04v8v3741.json`). Query `?query=Pranveer` returned `number_of_results: 1`.
2. OpenAlex institution `I4405287327` — https://api.openalex.org/institutions/I4405287327 (saved 2026-11-03 in `raw/`; work-level queries returned 429 that day).
3. Crossref REST API, `/works` with `query.affiliation` — https://api.crossref.org/works (2026-11-02/03; responses cached in `raw/crossref/`).
4. PSIT Kanpur — https://www.psit.ac.in/ (retrieved 2026-11-03; "Best Engineering College in Kanpur | PSIT Kanpur").
5. PSIT College of Higher Education — https://psitche.ac.in/ (retrieved 2026-11-03).
6. PSIT Pharmacy — https://psitpharmacy.ac.in/ (retrieved 2026-11-03; description names "PSIT College of Pharmacy", PCI-approved B.Pharm/M.Pharm).
7. Europe PMC REST API — https://europepmc.org/RestfulWebService (2026-11-02; 283 records).
8. NCBI E-utilities, `[AD]` field — https://www.ncbi.nlm.nih.gov/books/NBK25499/ (2026-11-02; 280 records).

## How confident is this?

- **Solid:** inventory, row and source counts, dedupe rule, and every `numbers.json` key quoted — re-read and re-checked against `papers.csv`.
- **Solid:** the ROR and website evidence, fetched live 2026-11-03; ROR saved verbatim, all three domains HTTP 200 with distinct titles.
- **Solid:** 21 strings name PSIT College of Higher Education — enumerated individually, one per paper.
- **UNCERTAIN:** that OpenAlex holds *exactly one* PSIT institution. One record and its ROR mapping verified, but an OpenAlex institution search was impossible (429), so a second, unreferenced node cannot be ruled out. It would change a count, not the argument.
- **UNCERTAIN:** how much PSIT-CHE output is missing. 21 is a floor, not an estimate; there is no denominator, because the missing papers are invisible by construction.
- **UNCERTAIN:** whether the 9 rows in §2.6 are real PSIT papers with truncated metadata or false positives. Flagged, not resolved.

last_updated: 2026-11-03
