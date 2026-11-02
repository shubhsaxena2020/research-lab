# Coverage comparison: what six indexes can see of PSIT's research

**What this page is for.** Item B2 asked for a cross-check of OpenAlex against Semantic Scholar, Crossref and DBLP. All three refused today (HTTP 429; evidence in `01_psit_data/raw/`), so this page measures what we could get — Crossref, Europe PMC, PubMed — and records what the blocked three can and cannot do. Every count is either read from a file produced in this session or labelled as a single probe reading.

## 1. The finding

The union of the three sources that answered is **793 deduplicated records** (`build_report.json: rows_written`). Crossref contributed **690**, Europe PMC added **102** the others did not have, PubMed added **1**. Of the 793, **509 exist only in Crossref** (`build_report.json: source_overlap.crossref_only`), 279 appear in two or more sources, 4 only in Europe PMC. A Crossref-only study would have found 690 of 793 — about 87% — and missed 103, mostly biomedical; a Europe PMC-only study would have found 283 and missed 510. "PSIT's output" changes by a factor of nearly three with the index. A single index is a biased subset, not a sample of the truth, and the bias has to be measured.

## 2. Source by source

| Source | Affiliation search? | Records contributed | Unique to this source | Covers well | Misses |
|---|---|---|---|---|---|
| Crossref | Free-text relevance query (`query.affiliation`), not a filter | 690 | 509 | DOI journal articles with deposited affiliations; the only source with conference papers, chapters and preprints | Non-depositing publishers; non-DOI literature; anything below the page cap |
| Europe PMC | Exact field search `AFF:"..."` | 283 found, 102 new | 4 | Biomedical journals in MEDLINE/PMC | Engineering, CS, management; books; conference papers |
| PubMed | Exact field search `[AD]` | 280 found, 1 new | 1 | MEDLINE-indexed biomedicine | Everything non-biomedical; nearly a subset of Europe PMC |
| Semantic Scholar | No affiliation field in the Graph API | 0 (blocked) | 0 | Citation counts, fields, OA links for known DOIs | Cannot discover papers |
| DBLP | No affiliation field (author/title only) | 0 (blocked) | 0 | Precise CS venue metadata | Cannot discover; only confirms known titles |
| OpenAlex | Yes — real affiliation disambiguation | 0 harvested (blocked) | 0 | Institution-level attribution, concepts, citation counts | Not measured today; see the three numbers below |

### Crossref

`query.affiliation` is documented as "Query contributor affiliations" [1] — a relevance-ranked free-text query, not a filter. The harvest numbers show what that means: `"PSIT Kanpur"` reported **18,651** results, we scanned 3,000 and kept **2**; `"Pranveer"` reported 645 and kept 636; `"PSIT"` reported 278 and kept 278 (`crossref_merged.json: stats`). The real filtering was a local regex over deposited affiliation strings (`PSIT|Pranveer\s*Singh`), giving **690 unique DOIs** from `/works` [2].

Crossref is the broadest source here: 599 journal articles, 132 conference papers, 44 book chapters, 15 preprints, 2 other — every non-journal type came from Crossref (`papers.csv: type`). But 258 of the 394 distinct venues appear exactly once (`analysis/numbers.json`): its venue coverage is a long tail, not a census.

Its blind spot is structural: no deposited affiliation string, no match, however many queries you run. *"Isolated flavonoids from Ficus racemosa stem bark…"* (`10.1016/j.jep.2016.02.004`, *J. Ethnopharmacology*, 2016) is in PubMed and in our table but not in the Crossref set, though it has a DOI — Crossref knows the DOI but had no affiliation text to match.

### Europe PMC

`AFF:"Pranveer Singh" OR AFF:"PSIT"` is a real constraint, not a ranking hint [3]. It returned **283** hits and 283 unique records (`logs/harvest_epmc.log`), contributing **102** records Crossref lacked and 4 no other source has.

All 283 rows are journal articles (`papers.csv: type`): it sees the biomedical part of PSIT's output — largely the pharmacy campus — and nothing else. The 132 conference papers, 44 book chapters and 15 preprints are entirely outside it.

### PubMed

The `[AD]` tag searches affiliation [4]; `PSIT[AD] OR "Pranveer Singh"[AD]` returned **280** ids (`logs/harvest_epmc.log`). Of those, **279 also appear in Europe PMC**; exactly **1** was new (`build_report.json: new_per_source.pubmed`). Expected: Europe PMC indexes MEDLINE, so the same records arrive through both doors in different wrappers. The exception is the *Ficus racemosa* paper; why Europe PMC missed it is not visible in the cached records, so it stays unverified. PubMed adds almost nothing once Europe PMC is in the build — but "almost" is doing real work: one paper in 280.

### Semantic Scholar

The Graph API's paper search takes free text matching title and abstract; it has no affiliation parameter [5] (`enrich_s2_dblp.py` header). The docs page would not open today — same 429 — so that claim is UNCERTAIN in the strict sense. It hardly matters: **we could not query Semantic Scholar at all** (`raw/s2_unavailable.json`, HTTP **429** at `2026-11-02T20:29:03Z`). All 793 rows carry `in_s2 = not-checked`.

Given a DOI it returns citation count, venue, field labels and an OA PDF link — useful for B4, useless for finding a paper whose affiliation nobody indexed.

### DBLP

DBLP has no affiliation field; it searches authors and titles [6]. It also refused every request: `raw/dblp_unavailable.json` records `2026-11-02T20:31:06Z`, two probes both ending in `RemoteDisconnected` — a bot challenge from this network. Even when reachable it cannot answer "what did PSIT publish"; it only confirms that a known title is indexed, and under which venue.

### OpenAlex — the three numbers

OpenAlex is the only index here with real affiliation disambiguation: it stores raw affiliation strings, assigns works to institution entities, and exposes `raw_affiliation_strings.search` as a filter [7]. It is also the source we could not harvest. Three numbers are in play, and they measure different things.

| Number | What it counts | Where it comes from |
|---|---|---|
| **721** | works whose raw affiliation string contains "PSIT" | one probe reading at 01:20 IST, 2026-11-03 (19:50 UTC, 2026-11-02) |
| **793** | our deduplicated union of Crossref + Europe PMC + PubMed | `build_report.json: rows_written` |
| **1412** | works assigned to institution `I4405287327` | `raw/openalex_institution_I4405287327.json: works_count` |

**721** is a `meta.count` from `/works?filter=raw_affiliation_strings.search:PSIT`. It is a single reading, not a harvest: the response body was not saved, and every later call returned 429 — `logs/harvest_openalex.log` shows four backoff attempts (30, 60, 120, 240 s) then "Gave up". It cannot be re-read today. Treat it as one number from one response, with no results page behind it.

**793** is our union: a regex over full affiliation strings matching "PSIT" or "Pranveer Singh", across three sources, after 460 merges. It stops where the page caps stopped — the `"PSIT Kanpur"` query alone reported 18,651 results and we read 3,000. So 793 is a floor, not a census.

**1412** is the institution node's own count [9]. The node is named "Pranveer Singh Institute of Technology (Pharmacy), Kanpur" (ROR `04v8v3741`), but its alternative names include the plain institute name — so it may mix the pharmacy campus with the main institute, or cover only one. `works_count` counts what disambiguation assigned to the entity, including works whose raw affiliation string never says "PSIT".

They cannot be reconciled without OpenAlex access. 721 is *smaller* than 793, impossible if OpenAlex saw everything we saw: 636 records were kept from the "Pranveer" query, whose strings spell out the institute's name without the acronym, and a "PSIT"-only search misses them. Conversely 1412 is 619 larger than 793, and nothing in our data says whether those 619 are pharmacy-campus papers, books and non-DOI items, or works whose affiliation Crossref never received. Separating those needs the work lists and their intersections; we have neither. OpenAlex probably sees more than we do, but the gap is not 1412 − 793.

## 3. Deduplication

The rule is fixed in `build_dataset.py` and quoted in `build_report.json`: **normalised DOI first; else normalised title[:90]**. A DOI is lowercased, stripped of `https://doi.org/`, `http://dx.doi.org/`, a leading `doi:` and trailing punctuation. Without a DOI, the title loses HTML tags and every non-alphanumeric character, is lowercased, and is cut to 90 characters.

The build read 1,253 source records (690 + 283 + 280) and wrote 793 rows: **460 merges** (`build_report.json: new_per_source.merged_dupes`). All 460 were keyed on DOI — only one row has no DOI (a Europe PMC Frontiers review) — so the title fallback never fired. The rule exists but is untested here.

Three real merges, all from `papers.csv`:

1. `10.1002/cphc.202500019` (*ChemPhysChem*, 2025). Crossref has "Diels–Alder … Information‐Theoretic" with an en dash and a Unicode hyphen; Europe PMC has ASCII "Diels-Alder … Information-Theoretic." plus a full stop. DOIs matched, so one row, `source = crossref+europepmc+pubmed`.
2. `10.1039/d6ra05311d` (*RSC Advances*, 2026). "structure–function" in Crossref, "structure-function" in Europe PMC. Same DOI, one row.
3. `10.1021/acs.molpharmaceut.5c00556` (*Molecular Pharmaceutics*, 2025). Europe PMC's title ends with a period, Crossref's does not. Same DOI, one row.

String comparison would have failed on all three; the 460 merges would have become 460 duplicate rows.

The residual risk is not hypothetical. Four groups with identical normalised titles but different DOIs survived:

- `10.3389/freae.2026.1833533` and a Europe PMC row with no DOI — the same review of epigenetic modifiers, one keyed `doi:`, one `title:`, so they never met.
- `10.25258/ijddt.16.11s.95` and `10.25258/ijddt.16.13s.2` — the same nanoemulgel paper, two DOIs from one journal, almost certainly a special-issue duplicate.
- `10.4018/978-1-6684-3666-0.ch040` (2022) and `10.4018/978-1-7998-2795-5.ch008` (2021) — one chapter title in two edited books.
- Two "Foreword" chapters with different DOIs — probably different front matter, indistinguishable by title.

Two risks remain unquantified. The 15 `posted-content` rows may later appear as journal articles with different DOIs, which the rule will not merge; the 793 may double-count at that boundary. Hyphenation or a dropped subtitle also breaks the 90-character title match.

## 4. What a better study would need

**A full OpenAlex harvest.** 1,412 works at 200 per page is 8 pages, plus about 8 for the two affiliation searches — roughly 16 requests. At 10 requests per second without a key, or 30 with a free one [8], that is seconds of network time; the real cost is an hour of dedupe against the 793. Zero rupees, one evening, and the 721/793/1412 puzzle becomes an answer.

**Institution disambiguation.** Establish which OpenAlex entity is which campus before counting. The node is titled "(Pharmacy)" but also carries the plain institute name, so 1,412 may be one campus or both. Half a day with the works list.

**ORCID for authors.** `analysis/numbers.json` reports 507 distinct PSIT author name strings — strings, not people. Linking the 30 most prolific authors to ORCID iDs would cover most of the output and fix "same person, two spellings"; the API is free, the work half a day.

**Scopus or Web of Science.** Neither is free, and they are the only reliable way to talk about venue indexing, which is what NIRF and NAAC reporting uses. PSIT's library may subscribe; if not, this needs a collaborator elsewhere. Cost: a subscription the project cannot buy, plus two to five days of waiting. UNCERTAIN: we have not asked.

**A manual audit.** Draw 100 random rows, open each DOI landing page, check that at least one author is really at PSIT. Two minutes each is three to four hours, and it turns "793 records" into "793 records, of which X% verified". Without it precision is unknown; the regex accepts a paper whose only "PSIT" sits in a co-author's address.

## 5. Re-running the blocked parts

The OpenAlex budget resets at 00:00 UTC (05:30 IST). Then run `python 01_psit_data/scripts/harvest_openalex.py`, or pass a free key from https://openalex.org/settings/api [10] through `get()` — the script authenticates only with `mailto`, so a key is a one-line change. It caches the institution record but re-fetches every works page, so a second run spends budget again; add the page-cache check `harvest_crossref.py` has first.

Semantic Scholar needs a free key; `enrich_s2_dblp.py` then fills `in_s2`, `s2_citation_count` and `oa_pdf_url` for all 793 DOIs, but discovers nothing new. DBLP needs a polite User-Agent and about one request per second — a convention, not a quoted limit, since its FAQ sits behind a bot check here.

## 6. Audit of the filter and of coverage (run 2026-11-03, after head checkpoint 2)

Script: `scripts/audit_crossref.py` -> `raw/crossref_audit.json`. Three questions, three computations. Nothing here is estimated.

**Q1 - Is every record's PSIT evidence traceable to a source?** Of 793 records: **690** carry a PSIT author-affiliation string deposited in Crossref, **103** come only from Europe PMC/PubMed, **0** are Crossref records lacking a PSIT author string, and **1** has no affiliation text at all. The head's checkpoint-2 anomaly (2 of 12 sampled records had title and year right but no PSIT string in Crossref) is therefore explained by the Europe PMC route, not by a bad filter: Europe PMC indexes the publisher's affiliation even where the Crossref deposit omits it. Example: `10.1038/s41598-025-11075-x` (source `europepmc+pubmed`).

**Q2 - Does the regex fire on a different institution (false positives)?** The 793 records contain **583 distinct matched affiliation strings**. By paper-match: 746 mention Kanpur, 400 mention Pharmacy, 21 mention Higher Education, and **5 name another city - all Lucknow, and all in strings that read "Pranveer Singh Institute of Technology, Dr. APJ Abdul Kalam Technical University, Lucknow"**, i.e. PSIT plus its affiliating university, not a different PSIT. **No false positive was found.** Honest limit: this classifier reads city and institution words, and only the top 12 strings were read by eye; it is not a line-by-line reading of all 583.

**Q3 - What does the filter miss (recall)?** The three most prolific PSIT author strings were probed with Crossref `query.author` (top 100 relevance-ranked items each): 99, 98 and 100 items authored by the named person; 46, 41 and 13 already in our dataset; **new items carrying a PSIT affiliation string: 0**; new items without any PSIT string: **197** (the same people publishing from other affiliations). So no PSIT-attributed paper surfaced that we lack. Limits: Crossref returned at most 100 items per author and ranks them by relevance, so this is a bounded probe, not a census; and a paper whose publisher deposited no affiliation is invisible to this method whether we look or not.

**What the audit does not settle.** Publishers that deposit no affiliation strings at all (invisible to both Crossref and this regex); books, book chapters and regional conference proceedings that never reached Crossref; and the 1,412 works on the OpenAlex institution node, which still cannot be reconciled without an OpenAlex harvest.

## Sources

1. Crossref REST API documentation, `query.affiliation` — https://github.com/CrossRef/rest-api-doc — retrieved 2026-11-03.
2. Crossref `/works` endpoint — https://api.crossref.org/works — retrieved 2026-11-03; responses in `01_psit_data/raw/crossref/`.
3. Europe PMC REST search, `AFF:` field — https://www.ebi.ac.uk/europepmc/webservices/rest/search — retrieved 2026-11-03; response in `raw/europepmc.json`.
4. PubMed Help, Affiliation `[ad]` tag — https://pubmed.ncbi.nlm.nih.gov/help/ — retrieved 2026-11-03.
5. Semantic Scholar Graph API docs — https://api.semanticscholar.org/api-docs/graph — NOT retrieved: HTTP 429, 2026-11-03.
6. DBLP, "How to use the dblp search API" — https://dblp.org/faq/How+to+use+the+dblp+search+API.html — NOT retrieved: bot challenge, 2026-11-03.
7. OpenAlex docs, filter works (`raw_affiliation_strings.search`) — https://docs.openalex.org/api-entities/works/filter-works — retrieved 2026-11-03.
8. OpenAlex docs, rate limits and authentication — https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication — retrieved 2026-11-03.
9. OpenAlex institution `I4405287327` — https://api.openalex.org/institutions/I4405287327 — cached at `raw/openalex_institution_I4405287327.json` (`updated_date` 2026-11-01), retrieved 2026-11-03.
10. OpenAlex API key settings — https://openalex.org/settings/api — retrieved 2026-11-03.

## How confident is this?

- **Solid.** The 690 / 102 / 1 split, the 509 Crossref-only count, the 460 merges and the 793 total come from `build_report.json`, and `papers.csv` reproduces them (690 + 283 + 280 = 1,253; 1,253 − 793 = 460). Crossref's query behaviour is measured, not assumed: 18,651 reported and 2 kept for `"PSIT Kanpur"` (`crossref_merged.json: stats`).
- **Solid.** The 1,412 figure, institution name and ROR id are copied from the cached OpenAlex record.
- **UNCERTAIN.** The 721 is one probe reading with no saved body and no results page; it cannot be re-checked today and must never be quoted as "OpenAlex has 721 PSIT papers".
- **UNCERTAIN.** Semantic Scholar's and DBLP's search behaviour rests on their API design and our scripts, not a docs page we could load; certain only that neither was queried successfully.
- **PARTLY MEASURED (2026-11-03).** Precision was audited in §6: 583 distinct matched strings, no match to another institution, the only non-Kanpur hits being PSIT's affiliating university (AKTU Lucknow). Recall was probed on the three most prolific authors: 0 missed PSIT-attributed papers within a 100-item-per-author window. Whether the 1,412 OpenAlex works cover both campuses remains unresolved.

last_updated: 2026-11-03
