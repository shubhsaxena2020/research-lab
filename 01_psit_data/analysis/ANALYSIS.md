# PSIT research output: what the numbers actually say

**What this page is for.** This is the reading of the PSIT publication dataset: what the 793 records show, what they do not show, and where a judgement starts. The arithmetic lives in two scripts and the JSON files they write.

**How to read this page — measured vs interpretation.** Every *measured* sentence ends with a key in square brackets. `[key]` is a key in `analysis/numbers.json`, written by `scripts/analyze.py`. `[x: key]` is a key in `analysis/numbers_extra.json`, written by `scripts/analyze_extra.py`. Both run on `01_psit_data/papers.csv` (793 records, retrieved 2026-11-03). Every sentence that is judgement rather than measurement starts with **Interpretation:** or sits under a heading that says it is not measured; a sentence with no key and no label describes the method or a limitation. There are no hand-counted figures in this file: if a number is not in one of those two JSON files or in a script-generated table under `analysis/tables/`, it is not here.

---

## 1. Headline numbers

- **793 records** whose deposited affiliation text names PSIT or Pranveer Singh [n_records]. This counts papers carrying such an *affiliation string*, not papers proven to be written by PSIT people: 784 records carry at least one PSIT string [affiliation_buckets.records_with_psit_affil_string], out of 792 with any affiliation text at all [affiliation_buckets.records_with_affil_text_nonempty].
- **2007–2026** [year_min, year_max], with 2026 partial [year_2026_is_partial]: data retrieved 2026-11-03, so it covers about ten months.
- **168 AI/ML-related, 21.2%** [ai_related_total, ai_related_share_pct]. "AI-related" is a keyword rule on title/abstract, not a subject classification.
- **Median citations: 1** [citations_median], over the 792 records carrying a count [citation_records_with_count].
- **394 distinct venues** for 793 papers [distinct_venues], and 258 of those venues appear exactly once [venues_with_1_paper] (section 4).

---

## 2. Growth over time

`tables/papers-per-year.md` is the story in one column: 1–8 papers a year until 2018, then 24 (2019), 27 (2020), 35 (2021), 50 (2022), 74 (2023), 157 (2024), 148 (2025), 234 (2026, partial) [year_counts].

**The 2019 → 2025 multiple**, using two complete years: 148 / 24 = **6.17x** over six years, which compounds to 1.354, or about **+35% a year** [x: growth.ratio_2019_2025, x: growth.cagr_2019_2025, x: growth.implied_pct_per_year].

**Interpretation: four things could produce that curve, and this dataset separates only one of them.**

- **Genuine growth** — more faculty, more PhD scholars, publication pressure for promotion and for NIRF/NAAC reporting.
- **Publication incentives** — a rise concentrated in APC-charging journals looks identical in a paper count.
- **Metadata improvement** — affiliations were rarely deposited before ~2015, and the corpus was *built* by searching affiliation strings, so pre-2018 papers that never deposited one are invisible by construction.
- **Harvest-side bias** — a query is not a census; recent records match more completely.

Within the corpus, coverage looks even: 28 of the 28 records from 2007–2015 carry an affiliation string [x: early_year_affiliation.records, x: early_year_affiliation.records_with_nonempty_affiliation]. **Interpretation:** that evenness is exactly why the metadata artefact is easy to miss — the invisibility happens *before* the record enters the corpus, so no filter on the corpus can reveal it.

Only the second explanation is partly testable, and the test is measurable: 279 records (35.2%) sit in journals whose Crossref publisher string contains "Bentham" [x: bentham.records, x: bentham.share_pct], across 87 distinct titles [x: bentham.distinct_venues]. Within those, 54 are dated 2025 and 112 are dated 2026 [x: bentham.records_2025, x: bentham.records_2026] — a rise of 58 against a corpus rise of 86 over the same two years [x: bentham.delta_2025_2026, x: bentham.corpus_delta_2025_2026], which is 67.4% of the increase [x: bentham.share_of_2025_2026_increase_pct].

**Interpretation:** one publisher family explaining two-thirds of the latest jump is consistent with a special-issue or commissioning push at that publisher. It is equally consistent with those authors simply choosing those journals. Publication metadata records where a paper appeared, not why.

**What this analysis cannot test.** Whether output or reporting rose (no denominator: faculty head-count, PhD enrolment). Whether APCs were paid (fees are not in Crossref metadata). Whether the 2024–2026 surge is behavioural or a deposit-timing effect — that needs the `published-print` / `published-online` / `created` date triple per record, which this harvest did not keep. The denominator needs the institute's NAAC/NIRF tables or an RTI request.

**The 2026 caveat, stated every time 2026 appears.** 234 papers [x: run_rate_2026.papers_2026] is more than any complete year, in ten months. Ten months at the 2025 rate would give 123.3 [x: run_rate_2026.expected_at_2025_rate], so 2026 is running at 1.9x the 2025 rate [x: run_rate_2026.ratio_vs_2025_rate]. **Interpretation: three readings are indistinguishable here** — real acceleration; Crossref assigning issued-year 2026 to articles online-first in late 2025 or printed in 2027; or a burst at one publisher (the Bentham +58 above). Do not plot 2026 beside complete years without that caveat.

---

## 3. Topics: pharmacy dominates, ML is the biggest single tag

`tables/topics.md` gives both columns — multi-label (every tag a paper carries) and primary (first rule that matched). Primary tags [topic_counts_primary]: untagged 167 (21.1%), pharmacy-drug-delivery 154 (19.4%), machine-learning 135 (17.0%), pharmacology-toxicology 120 (15.1%), medicine-clinical 99 (12.5%), security-crypto 37, networks-iot 28, and seven smaller tags summing to 53 [x: topic_primary_shares_pct.untagged, x: topic_primary_shares_pct.pharmacy-drug-delivery, x: topic_primary_shares_pct.machine-learning, x: topic_primary_shares_pct.pharmacology-toxicology, x: topic_primary_shares_pct.medicine-clinical].

Grouped, the three pharmacy/medicine tags are **373 primary papers, 47.0%**; the six computer-science-flavoured tags are **209, or 26.4%** [x: topic_groups_primary.pharmacy_medicine.papers, x: topic_groups_primary.pharmacy_medicine.share_pct, x: topic_groups_primary.computer_science_flavoured.papers, x: topic_groups_primary.computer_science_flavoured.share_pct].

Affiliation text points the same way: **402 records (50.7%)** name a pharmacy or pharmaceutical department somewhere in their affiliation strings, and **201 (25.3%)** name computer science, computer applications, information technology or CSE [x: affiliation_departments.pharmacy_named_records, x: affiliation_departments.pharmacy_share_pct, x: affiliation_departments.computer_science_named_records, x: affiliation_departments.computer_science_share_pct]. That regex reads *every* affiliation on the paper, including co-authors at other institutions, so it is not a count of PSIT departments [x: rules.affiliation_scope].

**Interpretation:** on publication volume this behaves like a pharmacy institution with an engineering wing, not the reverse. The word "behaves" is doing the work — the counts say where PSIT-named papers are published and who is named on them, not what the institute calls itself.

**The tags are keyword heuristics and they overlap.** A paper titled "machine learning in drug design" can carry both `pharmacy-drug-delivery` and `machine-learning`; the multi-label column sums to 1,192 tags over 793 papers [topic_counts_multilabel, x: topic_multilabel_total]. 167 papers (21.1%) matched no rule — mostly mathematics, physics, general engineering. Read every share as ±a few points and never compare a multi-label count with a primary count.

**Is the AI share rising?** Up sharply, then flat [ai_by_year]: 0 of 43 papers in 2007–2018 [x: ai_before_2019.papers, x: ai_before_2019.ai_related]; 4.2% in 2019; 0% in 2020; 17.1% in 2021; 24.0% in 2022; 28.4% in 2023; 21.0% in 2024; 22.3% in 2025; 26.5% in 2026 (partial). **Interpretation:** the honest reading is not "AI is growing fast" but that AI work went from near zero before 2019 to about a quarter of output by 2021–2023, and has sat between 21% and 27% since. The absolute count rose (6 in 2019 to 62 in 2026) because the whole corpus grew. The 2020 zero — 0 of 27 — is a warning about single-year keyword counts at this scale.

The AI tag is also narrow: `machine-learning` carries 135 primary papers, but `nlp` 7 and `computer-vision` 3 [topic_counts_primary]. **Interpretation:** PSIT's "AI" is machine learning applied to something else — drug delivery, optical networks, IoT — rather than NLP or vision research.

---

## 4. Venues: 394 venues for 793 papers

- 394 distinct venue strings [distinct_venues].
- 258 of them (65.5%) published exactly one PSIT paper [x: venue_concentration.venues_with_1_paper, x: venue_concentration.venues_with_1_paper_share_pct]; those 258 hold 32.5% of all papers [x: venue_concentration.share_of_papers_in_1_paper_venues_pct].
- The top 10 venues hold 119 papers, 15.0% [x: venue_concentration.top10_papers, x: venue_concentration.top10_share_pct]; the largest holds 23, or 2.9% [x: venue_concentration.largest_venue_papers, x: venue_concentration.largest_venue_share_pct]. No venue carries 3% of output.

**Interpretation (not measured):** this pattern is what you would expect if many individual faculty place papers wherever they can, rather than a few research groups with preferred outlets. Publication metadata cannot test that: it holds no faculty head-count, teaching load, submission history or rejection record. A teaching-intensive institution would produce this pattern; so would a young research institution with a large faculty and no shared lab. **Whether PSIT is teaching-heavy is not something this dataset can establish** — that needs AICTE or NIRF faculty-student data, which this analysis does not have.

Document types [type_counts]: journal-article 599 (75.5%), proceedings-article 132 (16.6%), book-chapter 44 (5.5%), posted-content (preprints) 15 (1.9%), other 2, edited-book 1 [x: type_shares_pct.journal-article, x: type_shares_pct.proceedings-article, x: type_shares_pct.book-chapter, x: type_shares_pct.posted-content].

First ten venues from `tables/top-venues.md`: Journal of Optical Communications 23; Current Drug Therapy 13; Current Diabetes Reviews 13; Current Traditional Medicine 13; Current Topics in Medicinal Chemistry 12; International Journal of Drug Delivery Technology 10; Scientific reports 9; Journal of Biomaterials Science, Polymer Edition 9; Chinese journal of applied physiology 9; Current Chemical Biology 8.

**Checked by hand on 2026-11-03** (publisher's own page, opened and read):

1. **Journal of Optical Communications** — De Gruyter, since 1980, four issues a year, guided-wave optical communications; its coverage list includes Scopus and it reports CiteScore 6.9 (2024) [1]. A real, indexed specialist journal, and the most common outlet here. Of its 23 papers, 17 are dated 2025–2026 [x: top_venue_group.papers_2025_2026], and one author string, "Keshav Kumar", appears on 12 of the 23 [x: top_venue_group.keshav_kumar_papers_in_venue], or 16 across the whole corpus [x: top_venue_group.keshav_kumar_papers_corpus]; the papers are AI-for-optical-network work. **Interpretation:** one coherent programme explains the top venue, not scattered submissions — but that is read from author overlap, not from any statement by the authors.
2. **Current Drug Therapy** — Bentham Science; publisher states Impact Factor 0.7, CiteScore 1.0, "Indexed in: Scopus, ESCI, JCR" [2]. Note that ESCI is Web of Science's *Emerging Sources* tier, not SCIE — "in Web of Science" can mean entry level.
3. **Scientific Reports** — Springer Nature, fully open access, indexed in Web of Science, Scopus, DOAJ per the publisher; 2025 impact factor 4.9 [3]. The most internationally conventional venue in the top ten.
4. **Research Journal of Pharmacy and Technology** — A and V Publication, India, monthly; the journal's own site lists Scopus, ProQuest, CAS and Google Scholar [4]. Articles are marked "Closed Access" on the site.
5. **Advances in Computational Intelligence and Robotics** — not a journal but an IGI Global *book series* (publisher from Crossref metadata; the series page rate-limited me, so its description is UNCERTAIN). All 8 records are book chapters.

**Not verified, marked as such:** International Journal of Drug Delivery Technology (Crossref publisher "Dr. Yashwant Research Labs Pvt. Ltd."; site not opened); the Chinese journal of applied physiology (a Chinese-language physiology journal — nine PSIT papers there is odd on its face and I could not establish why); Journal of Biomaterials Science, Polymer Edition (Informa/Taylor & Francis per metadata only). No judgement here rests on a journal's name.

The "Current …" pattern deserves naming. **Measured:** 279 records (35.2%) sit in Bentham journals across 87 distinct titles [x: bentham.records, x: bentham.share_pct, x: bentham.distinct_venues], and many of those titles begin "A Comprehensive Review on …" or "A Detailed Insight into …". **Interpretation (not measured):** that title shape is the narrative review — a summary assembled from existing literature, needing no new data and no ethics approval, which is a format one author can produce repeatedly. Whether any individual paper in that set is a thin summary is a question about its text, and nothing here reads the text. This page makes **no cost claim**: no APC or fee is recorded in Crossref metadata, so it does not rank publication types by cost. It says only which format requires no data collection and no ethics approval.

---

## 5. Citation distribution: median 1, and a mean you should not quote

From `tables/citation-distribution.md` [citations_total, citations_mean, citations_median, citations_zero_share_pct, citations_p50, citations_p75, citations_p90, citations_p95, citations_p99]: 792 records with a count, 5,476 citations, mean 6.91, **median 1**, **40.3% at zero**, percentiles p50 = 1, p75 = 6, p90 = 16, p95 = 26, p99 = 86, max 702 [x: citation_concentration.max].

The mean is 6.9 and the median is 1; the gap is arithmetic, not opinion. The single most-cited paper (702 citations) holds 12.8% of all citations; the top three hold 19.3%; the top five hold 23.1% [x: citation_concentration.top1_share_pct, x: citation_concentration.top3_share_pct, x: citation_concentration.top5_share_pct]. **Interpretation:** "average 6.9 citations per paper" describes almost no paper in this corpus. Quote the median and the zero share.

**Why Crossref counts are a floor.** `is-referenced-by-count` counts only citations from DOI-registered works whose publishers deposit reference lists. Books, theses, non-DOI Indian journals and many conference papers are invisible, so Google Scholar and Scopus will both show higher counts for the same paper. Zero means "no DOI-registered work cites this", not "nobody cites this".

**Age matters more than anything else.** 539 records (68.0%) are dated 2024–2026 [x: year_cohorts.cohort_2024_2026.records, x: year_cohorts.cohort_2024_2026.share_of_corpus_pct]:

| period | records | median cites | mean | share with zero |
|---|---|---|---|---|
| 2007–2023 | 252 | 5 | 14.96 | 18.7% |
| 2024–2026 | 539 | 0 | 3.17 | 50.3% |

[Table values: x: year_cohorts.cohort_2007_2023.* and x: year_cohorts.cohort_2024_2026.*]

**Interpretation:** "median 1" mostly says *the corpus is young*. Papers old enough to be cited have a median of 5. Any claim that PSIT papers are rarely cited must fix the cohort age, and even then the Crossref floor applies.

**Reading `tables/top-cited.md` plainly.** The top is not AI and not engineering: number one, 702 citations, is "Drug delivery systems: An updated review" (2012, *International Journal of Pharmaceutical Investigation*), a pharmacy review that became a standard citation; two and three are also 2010–2012 pharmacy reviews (212, 143). Only from rank four does current work appear — a 2024 DFT study of a halide double perovskite (104), "Explainable AI for Industry 5.0" (99), federated learning for the Internet of Medical Things (76). The top three records hold 19.3% of all visible citations [x: citation_concentration.top3_share_pct]. Two DOIs resolve against doi.org [5], so the table is not corrupted. **Interpretation:** it is a *most-cited* list, not a *best* list; three old reviews at the top say more about how citations accumulate around a standard reference than about the institution.

---

## 6. Authors and collaboration

2,237 distinct author strings overall, **507 carrying a PSIT affiliation** [distinct_authors_all, distinct_psit_authors]; **27 of those appear on 10+ papers** — 5.3% of the 507 strings [authors_with_10plus, x: collaboration_shares.authors_10plus_share_of_psit_strings_pct]. Median authors per paper **5**, mean 5.61 [authors_per_paper_median, authors_per_paper_mean]; 325 papers (41.0%) have six or more [papers_6plus_authors, x: collaboration_shares.papers_6plus_share_pct]; **19 are single-author** (2.4%) [single_author_papers, x: collaboration_shares.single_author_share_pct].

The distribution is top-heavy at the string level: "Pranay Wal" appears on 170 papers — 21.4% of the corpus — and "Ankita Wal" on 119 [x: named_authors.pranay_wal_papers, x: named_authors.pranay_wal_share_pct, x: named_authors.ankita_wal_papers]; in 2026 alone, "Pranay Wal" is on 56 of the 234 [x: named_authors.pranay_wal_papers_2026]. **Interpretation:** with a median of five authors and 2.4% solo papers, this is a co-authorship culture in which a small number of names carry much of the volume.

**Name-string disambiguation is the weakest link in this section.** Everything above counts strings, not people. One person is written "Pranay Wal", "Wal P", "P. Wal" — the table shows "Wal P" on 22 papers and "Wal A" on 10, almost certainly the same two people, so the true totals are higher than shown while the 507 distinct strings overcounts actual humans. The opposite error also runs: Indian names have high homonym rates, so a common surname plus initials ("Keshav Kumar", "Rahul Singh") can merge two people into one row, and initials-only deposits ("A.K. Tiwari") cannot be resolved at all. Author order also varies by field, so "first author" is not a proxy for who did the work. Per-person claims need ORCIDs or OpenAlex author IDs; this dataset has neither.

---

## 7. Open access and indexing: mostly unknowable from here

**Open access: not determined.** The `open_access` column is empty for all 793 rows because Semantic Scholar — the planned source for OA status and PDF links — was unavailable on the harvest day. The `s2_*` and `oa_pdf_url` columns are empty for the same reason. Nothing on this page is an OA statistic.

**Indexing: not determined at scale.** Scopus and Web of Science are subscription products with no public "is this ISSN indexed" API. Indexing was not inferred from journal names — the mistake that makes a literature review look naive. What can be reported is only what four publishers state on their own pages: Journal of Optical Communications lists Scopus [1]; Current Drug Therapy lists Scopus, ESCI, JCR [2]; Scientific Reports lists Web of Science and Scopus [3]; Research Journal of Pharmacy and Technology lists Scopus [4]. For the other ~390 venues: **UNAVAILABLE**.

**DBLP: never checked.** [in_dblp_yes] = 0 and [in_dblp_checked] = 0, so the absence of DBLP records proves nothing.

Only 604 records (76.2%) carry an abstract [x: abstract_coverage.records_with_abstract, x: abstract_coverage.share_pct], so every abstract-based rule — including the topic tags in section 3 — is blind for a quarter of the corpus, unevenly across years and publishers.

---

## 8. Five things this analysis can establish, and six it cannot

**Can establish (measured):** (1) the size and shape of PSIT's DOI-registered output — 793 records, 75.5% journal articles, 16.6% conference papers [n_records, type_counts]; (2) a roughly six-fold rise between 2019 and 2025, 24 to 148 a year [year_counts, x: growth.ratio_2019_2025]; (3) that the disciplinary centre of gravity is pharmacy, not computer science — 47.0% of papers carry a primary pharmacy/medicine tag, and 50.7% name a pharmacy department in their affiliation text [x: topic_groups_primary.pharmacy_medicine.share_pct, x: affiliation_departments.pharmacy_share_pct]; (4) extreme venue fragmentation — 394 venues, 65.5% used once [distinct_venues, venues_with_1_paper]; (5) a young, low-citation corpus — median 1, 40.3% at zero, mean 6.91 driven by a few old reviews [citations_median, citations_zero_share_pct, citations_mean].

**Cannot establish:**

1. **Whether output or reporting is rising.** Settled by: faculty head-count and PhD enrolment per year, from NAAC/NIRF submissions or an RTI request.
2. **Whether PSIT is teaching-intensive, and how large its faculty is.** Settled by: AICTE approval data or the institute's NIRF submission. No publication metadata can supply it.
3. **Scopus/WoS coverage of most venues.** Settled by: a Scopus/WoS subscription, or the institute's own indexed-publication list cross-checked by ISSN and year.
4. **Open-access share and APC spend.** Settled by: Semantic Scholar or Unpaywall for OA status; the journals' APC pages plus author or institution records for money paid.
5. **Quality, novelty, or whether peer review was real.** Settled by: full-text reading of a sample under a coding protocol — e.g. 60 papers, two coders, "does this report an experiment with data and a baseline".
6. **Who actually did the work, including students.** Settled by: ORCIDs, author-contribution statements, and the institute's internal project records, which are not public.

---

## 9. So what for a BCA student

**Interpretation — this whole section is judgement, not measurement.** It rests on the counts above, but none of it is a key in either JSON file.

**Measured starting point.** 129 titles (16.3%) contain "review", "survey", "overview" or "meta-analysis" [x: text_proxies.review_title_records, x: text_proxies.review_title_share_pct]; of the 604 records with abstracts, 30 (5.0%) mention a dataset, 72 (11.9%) an experiment, and 10 (1.7%) say "we propose" [x: text_proxies.abstract_dataset_pct, x: text_proxies.abstract_experiment_pct, x: text_proxies.abstract_we_propose_pct]. Inside the AI subset (109 abstracts), 29 mention a dataset (26.6%) [x: text_proxies.ai_abstracts, x: text_proxies.ai_abstract_dataset, x: text_proxies.ai_abstract_dataset_pct]. These are single-keyword proxies that undercount: an abstract can describe an experiment without ever using the word.

**Interpretation:** the output reads as review-heavy and experiment-light, and those proxies are the only evidence for that reading.

**Interpretation:** volume is high and the median citation is 1. An institute publishing 148 papers a year across 394 venues, with 40% never cited, is producing countable output faster than readable output. If that reading holds, it is an opening: one well-executed, reproducible study with public data and code is likely to be cited more than one more narrative review.

**Interpretation:** the AI work is narrow — 168 papers [ai_related_total], but only 7 primary NLP and 3 primary computer-vision tags [topic_counts_primary]. The optical-networks strand looks like one group's programme in a Scopus-indexed journal [1], which is a template rather than a closed door.

**Interpretation:** three realistic entry points for someone with Python and no lab. A **replication or benchmark study** on a public dataset in a domain PSIT already publishes in — hard to dismiss, and cited by people who need the baseline. A **systematic review with a registered protocol and reproducible search**, which is what most existing reviews here are not. A **small tooling or dataset contribution** in one of these applied areas. All three need a supervisor and public data; this page makes no claim about what any of them costs.

**Interpretation:** what the data does not support is the comforting story that any publication is a good publication. With 394 venues and a median of one citation, venue choice and study design each carry weight that a publication count hides.

---

## Appendix: where every number comes from

- `scripts/analyze.py` → `analysis/numbers.json` plus `analysis/tables/*.md`: record counts, years, types, AI share, topic tags, venues, authors, citations, affiliation buckets, DBLP flags.
- `scripts/analyze_extra.py` → `analysis/numbers_extra.json`: everything else this page quotes — the 2019→2025 multiple, early-year affiliation coverage, the Bentham cluster and its 2025→2026 delta, the 2026 run-rate, topic and affiliation groups, type and topic shares, venue concentration, the top venue's author overlap, citation concentration, year cohorts, named-author counts, abstract coverage and the text proxies.

`numbers_extra.json` also stores the exact regexes it used, under `rules`, so a reader can check what "pharmacy department" or "mentions a dataset" meant. Re-running both scripts on the same `papers.csv` reproduces every figure above; only the `generated` timestamp changes.

`numbers.json` has two wrinkles, neither changing a headline: (i) `year_counts` sums to 792 while `n_records` is 793 — one Europe PMC record has no issued year and no DOI; (ii) `citation_records_with_count` is 792 for the same reason. The affiliation counts come in two kinds and are named for it: `affiliation_buckets.mentions_Pranveer` = 776 and its siblings count *strings*, so a string count can exceed the paper count, while the record-level keys are `affiliation_buckets.records_with_affil_text_nonempty` = **792** (records with any deposited affiliation text) and `affiliation_buckets.records_with_psit_affil_string` = **784** (records with at least one string naming PSIT). Both are counted per record in `analyze.py`.

---

## Sources

1. De Gruyter, *Journal of Optical Communications* — scope, coverage list, CiteScore. https://www.degruyterbrill.com/journal/key/joc/html — retrieved 2026-11-03.
2. Bentham Science, *Current Drug Therapy* — impact factor, indexing statement. https://www.benthamscience.com/journals/current-drug-therapy — retrieved 2026-11-03.
3. Nature Portfolio, *About Scientific Reports* — scope, open access, indexing, metrics. https://www.nature.com/srep/about — retrieved 2026-11-03.
4. A and V Publications, *Research Journal of Pharmacy and Technology* — publisher, frequency, indexing. https://rjptonline.org/ — retrieved 2026-11-03.
5. DOI resolver spot check: `10.4103/2230-973x.96920` and `10.1109/ojia.2024.3399057` both returned HTTP 302 to a publisher site, 2026-11-03. Dataset: `01_psit_data/papers.csv`, built by `01_psit_data/scripts/build_dataset.py`, analysed by `01_psit_data/scripts/analyze.py` and `01_psit_data/scripts/analyze_extra.py`.

## How confident is this?

- **Solid:** all counts, shares, percentiles and year totals — deterministic functions of `papers.csv`, reproducible by re-running `analyze.py` and `analyze_extra.py`; the four venue descriptions read on the publishers' own pages.
- **Solid but conditional:** topics, AI share, review share — keyword rules on titles and abstracts, with a quarter of records lacking abstracts and the exact regexes published in `numbers_extra.json`.
- **UNCERTAIN — the 2026 figure:** 234 papers in ten months, ~1.9x the 2025 run-rate; genuine growth and issued-year assignment cannot be separated without Crossref print/online dates. Never cite 2026 without the partial-year marker.
- **UNCERTAIN — indexing and open access:** only four venues verified from publisher pages; `open_access` is empty for all 793 rows because Semantic Scholar was down.
- **UNCERTAIN — author counts:** 507 distinct PSIT author *strings*, not people; no ORCIDs.
- **Interpretation, not finding:** that the Bentham "Current …" cluster reflects volume-oriented, review-heavy publishing. The counts are solid; the motive is inferred.
- **NOT MEASURED — institutional character:** "teaching-heavy", faculty size and research intensity are absent from publication metadata. The venue pattern is a shape, not proof, and section 4 says so where it appears.

last_updated: 2026-11-03
