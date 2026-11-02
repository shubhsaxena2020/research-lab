# Status of research: what public data can and cannot tell us about PSIT

**What this page is for.** This is the honest map of the first folder of the project. It records what we could measure about PSIT's research output from public sources, how each number was produced, and which questions public data cannot answer at all. Any later draft that needs a PSIT number should take it from here, or from the result file named here, and never from memory.

Retrieval date for everything below: **2026-11-03** (IST). The harvest itself ran on 2026-11-02.

## 1. What is known

### 1.1 The dataset

| Item | Value | How it was obtained | Where it lives |
|---|---|---|---|
| Records | 793 | 3-source union deduplicated by normalised DOI, else by the first 90 characters of the normalised title; 460 duplicate rows merged | `01_psit_data/papers.csv` |
| From Crossref | 690 | `/works?query.affiliation=` for three query strings, then kept only if a deposited author affiliation string matched `/PSIT\|Pranveer\s*Singh/i` | `01_psit_data/raw/crossref/`, `01_psit_data/scripts/harvest_crossref.py` |
| From Europe PMC | 102 | Affiliation field query `AFF:"Pranveer Singh" OR AFF:"PSIT"` | `01_psit_data/raw/europepmc.json` |
| From PubMed only | 1 | `PSIT[AD] OR "Pranveer Singh"[AD]`, after removing records already in Europe PMC | `01_psit_data/raw/pubmed.json` |
| Years covered | 2007-2026 | Year field of each record; 773 of 793 (97.5%) fall in 2013-2026 | `01_psit_data/analysis/numbers.json` |
| 2026 records | 234 | Partial year: the harvest stopped on 2026-11-02, so 2026 is not a full year | `01_psit_data/analysis/numbers.json` |
| AI-related | 168 (21.2%) | Keyword screen on title + abstract (`AI_STRICT_RE` in `01_psit_data/scripts/build_dataset.py`); a heuristic, not a subject classification | `01_psit_data/analysis/numbers.json` |
| Distinct venues | 394, of which 258 have one paper | Unique value of the venue field (a venue is the journal or conference where a paper appeared) | `01_psit_data/analysis/tables/top-venues.md` |
| Distinct PSIT author name strings | 507 | Unique values in the `psit_authors` column, names longer than 3 characters, no disambiguation | `01_psit_data/analysis/tables/top-psit-authors.md` |
| Distinct affiliation strings | 563 | Unique deposited affiliation strings matching the PSIT pattern | `01_psit_data/analysis/tables/affiliation-vocabulary.md` |
| Citations | 5,476 total; mean 6.91; median 1; 40.3% uncited | `is-referenced-by-count` from Crossref at harvest time | `01_psit_data/analysis/tables/citation-distribution.md` |
| Document types | 599 journal articles, 132 conference papers, 44 book chapters, 15 preprints, 2 other, 1 edited book | Crossref `type` field | `01_psit_data/analysis/tables/document-types.md` |

The union is dominated by Crossref because Crossref is the DOI registration agency: it holds the affiliation text that authors and journals deposit. Europe PMC adds the biomedical and pharmacy journals that Crossref indexes thinly. PubMed added exactly one record that neither of the others had.

**793 is a floor, not a total.** Three things push the true figure up. Authors who wrote the institute's name in a form our pattern missed. Papers with no DOI and no PubMed record, which describes most Indian conference proceedings before about 2015. Deposits where the affiliation field is empty. In the other direction, a few records may not be PSIT at all, since the pattern could in principle match another institute; we opened the 19 pre-2013 rows by hand and the ones we checked name PSIT departments explicitly.

### 1.2 The shape of the output

- **Growth.** 24 records in 2019, 74 in 2023, 157 in 2024, 148 in 2025, 234 in the partial 2026. Roughly a tenfold rise in seven years.
- **Pharmacy carries the volume.** 400 of 793 records mention "pharmacy" in an affiliation string; 21 mention "higher education", which is the College of Higher Education. Topic tags (multi-label, so they sum past 793) give medicine-clinical 373, pharmacology-toxicology 217, pharmacy-drug-delivery 168, machine-learning 135, security-crypto 50.
- **The output is spread thin across venues.** 394 venues, 258 of them with a single paper. There is no house journal absorbing the output.
- **Citation profile.** Median 1, 40.3% never cited, mean 6.91, 90th percentile 16. Large teams: mean 5.61 authors per paper, 325 papers with six or more authors, only 19 single-author papers.

This is the profile of a teaching-intensive institute with active faculty: many papers, wide venue spread, short citation life, large pharmacy-style author teams. It is not the profile of a research institute with a few flagship groups.

### 1.3 What the institute itself publishes

The NAAC Self Study Report (SSR) is the richest public document, and it is internally inconsistent [5]. Page numbers below are from the 95-page PDF.

| Claim | Value | Page |
|---|---|---|
| Grants received from government / non-government entities | "Rs. 7.3 crores" | p. 5 |
| Named projects | Rs. 5.85 crore from DST UP, Rs. 1.15 crore from MSME, Rs. 12.5 lakh from CST | p. 42 |
| Patents | "a count of 60 patents published and applied for put together in the last 5 years" | p. 42 |
| Patents (highlights box) | "Over 65 patents" | p. 85 |
| Government-funded projects (highlights box) | "10+ ... worth Rs.1.1 Crores" | p. 85 |
| Annual publications | "Around 200 annual research publications during 2022-23" | p. 85 |
| UGC-CARE papers, 2018-19 to 2022-23, **before** NAAC data validation | 147, 72, 87, 136, 148 = 590 | p. 89 |
| Same metric, **after** NAAC data validation | 24, 17, 18, 21, 37 = 117 | p. 89 |

Four different funding totals appear across one document and one website: Rs. 1.1 crore, Rs. 7.3 crore, the Rs. 7.13 crore sum of the three named projects, and on the homepage today Rs. 4.03 crore of DST NIDHI support plus Rs. 1.15 crore from MSME plus Rs. 90 lakh for an AICTE IDEA Lab [7]. Each may be true for its own window and scheme, but none can be used as a baseline without asking which window that is.

The validation table on p. 89 of the same report is the clearest warning in the whole exercise [5]. The institute's first submission claimed 590 UGC-CARE papers over five years; after NAAC's data validation the same claim became 117. Neither number is a lie, but neither is the same object as "papers in Crossref", and a student quoting either without the other would mislead.

### 1.4 The rules the institute has published

The research policy (office circular PSIT/2021-22/40, 28 January 2022) pays faculty cash rewards [6]: Rs. 30,000 for a first-authored SCI paper, Rs. 15,000 for ESCI, Rs. 10,000 for Scopus, Rs. 5,000 for a published patent, Rs. 20,000 for a granted patent, a share of sanctioned project amounts, and Rs. 70,000 on a completed PhD guidance. Two consequences matter here.

First, the policy is written for faculty only. It has no clause about students, which is why "does PSIT have a student research policy?" is an open question and not a lookup. Second, the policy fixes the affiliation format as "Pranveer Singh Institute of Technology, Kanpur". That is why this exact string is the most common one (35 records), while departments that add their own line produce the other 562 variants.

## 2. What is unknown or unavailable, and why

The point of this section is the mechanism. "Not found" is not an explanation; each item below is missing for a specific structural reason.

### 2.1 Papers under review, accepted, or in press

Not public by definition. A manuscript under review exists only in an editor's system and the authors' files; there is no registry, and journals do not publish submission queues. A paper "in press" appears publicly only when the publisher assigns a DOI, at which point it enters Crossref and our data. So the gap between what PSIT faculty have written and what we can see is structurally invisible, and no amount of searching closes it. Only the R&D cell can answer it, which is what the email draft is for.

### 2.2 Ongoing projects, project monitoring, and any research MIS

Internal systems. Project monitoring exists to track spending and compliance, not to be read: it is a spreadsheet or a dashboard behind a staff login. The public filing formats we could see ask for counts and a few illustrative cases rather than a register [5], so the list itself never leaves the office. We cannot see, and should not try to see, anything behind a login.

### 2.3 Funded project details

Aggregates only, and even those disagree (section 1.3). The mechanism is in the paperwork: a sanction letter is addressed to the institution and filed with it, while the public NAAC format asks for the number of projects and the amount received [5], which is exactly the level at which the SSR answers. PI names, durations and deliverables surface only on departmental pages, and inconsistently.

### 2.4 Patents

Partially public, and only by hand. We checked accessibility today rather than assuming it:

- `https://iprsearch.ipindia.gov.in/PublicSearch/` loaded on 2026-11-03 (HTTP 200) [10]. It offers search fields for Applicant, Inventor and Application Number, with Published and Granted filters. It is not behind a login, but the page contains a captcha (the string "Captcha" appears 20 times in the HTML).
- **We did not solve the captcha and did not run a search.** This project therefore holds no patent count of its own. A person can do it in about ten minutes by searching the applicant name "Pranveer Singh Institute of Technology".
- The institute's own Research & Innovation section lists a "Patent Published" page [9]. We could not retrieve its contents today (the extractor returned no text for it), so it is listed as UNCERTAIN, not as evidence.

The two institute claims (60 patents published and applied for over five years, p. 42; "over 65 patents", p. 85) mix filed and granted, which are very different things. A filed patent is a pending application; a granted patent is an enforceable right. Any comparison must say which one it counts.

### 2.5 Scopus and Web of Science counts for the institution

Subscription databases with no free affiliation-level query. Scopus's public content page describes coverage but publishes no per-institution publication counts [13]; the affiliation query normally runs inside an institutional subscription, and exporting its result is a licensed act. Web of Science has no public equivalent at all. Our 793 records cannot be converted into a "Scopus-indexed" count: Crossref does not carry indexing status, and the SSR's own 3.3.1 metric counts UGC-CARE journals, a third and different list [5].

### 2.6 Author-level disambiguation

507 name strings are not 507 people. "Pranay Wal" (170 records) and "Ankita Wal" (119) are probably two individuals; "Gaurav Tiwari" (38) and "Ruchi Tiwari" (36) could each be more than one person, and spelling variants split a single person across rows. Turning strings into people needs an external key: an ORCID iD on the paper, or an institutional staff ID. We did not check ORCID coverage, so this is the next step if any claim about a named individual is needed. Until then, treat the author table as approximate, as its own header says.

### 2.7 Three APIs that were blocked from this network on 2026-11-03

This is an access limitation of one laptop on one day, not a fact about PSIT.

| API | What happened | Evidence file |
|---|---|---|
| OpenAlex | HTTP 429, "Insufficient budget ... $0 remaining; resets at midnight UTC". One institution record was retrieved before the budget ran out | Error text in `sessions/S1-foundations/STATUS.md`; the single record in `01_psit_data/raw/openalex_institution_I4405287327.json` |
| Semantic Scholar | HTTP 429 on both the single and batch endpoints | `01_psit_data/raw/s2_unavailable.json` |
| DBLP | HTTP 429 and connection resets; it is also title/author search only, not affiliation searchable | `01_psit_data/raw/dblp_unavailable.json` |

Consequence: the comparison of coverage between OpenAlex, Semantic Scholar, DBLP and Crossref is incomplete. Our numbers describe Crossref plus Europe PMC plus PubMed. Re-running `01_psit_data/scripts/harvest_openalex.py` after 00:00 UTC, or with a free API key, would close most of the gap.

## 3. Can public data answer the question?

| Question | Can public data answer it? | How | Confidence |
|---|---|---|---|
| How many papers has PSIT published? | Partly | Crossref + Europe PMC + PubMed union, 793 records, affiliation-string rule stated | Medium. A floor, not a total |
| How many per year, and is it growing? | Yes, approximately | Year field of the same union | Medium-high from 2019 on; 2026 is partial |
| How much of it is AI-related? | Approximately | Keyword screen on title + abstract, 168 records (21.2%) | Medium-low. The screen includes IoT and data mining, so it is a loose upper bound |
| Which departments publish? | Partly | Only where the department appears in the affiliation string | Medium-low. Pharmacy-heavy; CSE and ECE visible; CHE almost invisible (21 records) |
| How many papers are Scopus or WoS indexed? | No | Subscription databases; no public affiliation query | None |
| How many patents filed or granted? | Partly, by hand only | IPO public search with captcha; institute claims 60 / 65, filed and granted mixed | Low |
| Which funded projects, with agency, amount, PI? | No for details | Aggregates only, and they disagree | Low |
| Papers under review or in press | No | Not public by definition | None |
| Does a student research policy exist? | Partly | The published policy covers faculty only; absence of a student clause is suggestive, not proof | Medium |
| Who works on machine learning at PSIT? | Partly | Author strings plus department pages; no disambiguation | Low-medium |
| Do faculty supervise undergraduate projects? | No | Needs the R&D cell or a mentor conversation | None |
| What is the citation impact? | Approximately | Crossref cited-by counts at harvest time | Medium-low. Crossref counts run below Scopus and Google Scholar |

## 4. The three names problem

PSIT is at least three institutions wearing one name, and the identifiers do not separate them. ROR returns exactly one record for the query "PSIT", `ror.org/04v8v3741` [4], and it is the pharmacy one: its label is "Pranveer Singh Institute of Technology (Pharmacy), Kanpur", its website is psitpharmacy.ac.in, and its alias list also contains the generic string "Pranveer Singh Institute of Technology, Kanpur", which is why the engineering campus's papers are absorbed into the pharmacy record. OpenAlex inherits that decision: institution `I4405287327` carries the same pharmacy name and reports 1,412 works, 25,098 citations and an h-index of 52 (h-index: the number h such that h papers have at least h citations each), while our Crossref union finds 793 records, and nothing in public data says how much of the 1,412 is engineering, how much pharmacy, and how much the College of Higher Education. Any single "PSIT publication count" is therefore a statement about a name-matching rule rather than about an institution, and must always name the rule.

| Entity | Website | What it is | Identifier found |
|---|---|---|---|
| PSIT (engineering) | psit.ac.in | Pranveer Singh Institute of Technology, founded 2004, AICTE-approved, AKTU-affiliated, college code 164 | No ROR record of its own found |
| PSIT-CHE | psitche.ac.in | PSIT College of Higher Education, college code KN162; the BCA/BBA side, where Shubh studies | No ROR record found |
| PSIT-Pharmacy | psitpharmacy.ac.in | PSIT (Pharmacy), the pharmacy institute | ROR `04v8v3741` = OpenAlex `I4405287327` |

## Sources

1. `01_psit_data/papers.csv` and `01_psit_data/build_report.json` — the 793-row dataset and its build log (690 Crossref + 102 Europe PMC + 1 PubMed, 460 merges). Local result files, retrieved 2026-11-03.
2. `01_psit_data/analysis/numbers.json` and `01_psit_data/analysis/tables/*.md` — every count in section 1, produced by `01_psit_data/scripts/analyze.py`. Local result files, retrieved 2026-11-03.
3. `01_psit_data/raw/openalex_institution_I4405287327.json` — OpenAlex institution record, `https://api.openalex.org/institutions/I4405287327`, retrieved 2026-11-02.
4. ROR record `04v8v3741` via `https://api.ror.org/v2/organizations/04v8v3741`, and the search `https://api.ror.org/v2/organizations?query=PSIT` (one result for "PSIT"), retrieved 2026-11-03. The human page is `https://ror.org/04v8v3741`.
5. PSIT, *Self Study Report* (NAAC, 95 pp., generated 09-10-2024), `https://www.psit.ac.in/QIF/ssr/ssr.pdf`, retrieved 2026-11-03. Claims cited from pp. 5, 42, 85, 89.
6. PSIT, *Policy to Enhance Research Activities in the Institute*, office circular PSIT/2021-22/40, 28 January 2022, `https://www.psit.ac.in/QIF/cr6/6.2.1/Policies/Policy%20to%20Enhance%20Research%20Activities%20in%20the%20Institute.pdf`, retrieved 2026-11-03.
7. PSIT homepage, `https://www.psit.ac.in/` (DST NIDHI Rs. 4.03 crore, MSME Rs. 1.15 crore, AICTE IDEA Lab Rs. 90 lakh), retrieved 2026-11-03.
8. PSIT Contact page, `https://www.psit.ac.in/contact-us/` (address, toll-free number, admission@psit.ac.in), retrieved 2026-11-03.
9. PSIT Research and Innovation, `https://www.psit.ac.in/research_and_innovation/research_center` (lists Research Center, Research Publications, Patent Published, Noteworthy Projects), retrieved 2026-11-03.
10. Intellectual Property India public search, `https://iprsearch.ipindia.gov.in/PublicSearch/` (HTTP 200, captcha present, search not run), checked 2026-11-03.
11. EACE-2026 conference page, `https://www.psit.ac.in/eace2026/` (Prof. Brijesh Kumar Chaurasia listed as Dean-Research & Innovation), retrieved 2026-11-03.
12. PSIT College of Higher Education, `https://psitche.ac.in/` (college code KN162), retrieved 2026-11-03.
13. Elsevier, *Scopus content*, `https://www.elsevier.com/products/scopus/content` (describes coverage; no institution-level counts), retrieved 2026-11-03.

## How confident is this?

- **Solid.** The record count and its composition: the build log and the dataset are in the repo and the harvest scripts can be re-run. The year, venue, type and citation distributions are direct tallies of that file.
- **Solid.** The identifier facts: one ROR record for "PSIT", named Pharmacy, with the generic Kanpur name as an alias; one OpenAlex institution with the same name and 1,412 works.
- **Solid.** The institute's published figures and their inconsistency, quoted with page numbers from the SSR, and the faculty-only scope of the 2022 research policy.
- **UNCERTAIN.** 793 is a floor. Undeposited affiliations, missing DOIs and name variants all hide records; the 21.2% AI share is a keyword heuristic that includes IoT and data mining.
- **UNCERTAIN.** Patent numbers. We verified that the IPO search page loads and needs a captcha, and we did not run a search; the institute's "Patent Published" page could not be read today.
- **UNCERTAIN.** Everything about coverage relative to OpenAlex, Semantic Scholar and DBLP, because all three APIs refused this network on 2026-11-03. That is a temporary access limit, not a finding about PSIT.
- **Note on the brief.** The task description said "years 2013-2026"; the dataset actually runs 2007-2026, with 773 of 793 records in 2013-2026. The earlier 19 are real PSIT papers, mostly pharmacy, and were kept.

last_updated: 2026-11-03
