# S1 STUDENT DIGEST — what you have now and what it means

One page, for Shubh. Everything below is backed by the files named in brackets.

## 1. What was built today

Seven foundation pages in `00_foundations/`, in the order you should read them:

1. `WHAT-IS-A-PAPER.md` — the parts of a paper, the six types, what "contribution" and "novelty" actually mean, what reproducibility is.
2. `HOW-TO-WRITE-ONE.md` — the workflow from idea to submission, the writing order that works, LaTeX, 20 common mistakes, a 2-week and a 3-month timeline.
3. `VENUES-AND-PUBLISHING.md` — arXiv, workshops vs conferences vs journals, CORE ranks, blind review, rebuttals, fees, visas, predatory venues, the Indian (UGC/Scopus/NIRF) angle, and 10 realistic target venue types.
4. `ETHICS-AND-AI-USE.md` — authorship, plagiarism, data ethics, and the *actual quoted* AI policies of arXiv, ACM, IEEE, NeurIPS, ICML, ACL and COPE.
5. `WHAT-A-PAPER-DOES-FOR-YOU.md` — the honest version: what a paper does and does not do for MCA/MS/PhD, scholarships, internships, GATE. Includes the 18+ and year-of-study rules that apply to you.
6. `GLOSSARY.md` — 125 terms, so no later document can lose you in jargon.
7. `READING-LIST.md` — 15 verified "how to read/write papers" resources, easiest first.

Plus a dataset: `01_psit_data/papers.csv`, **793 deduplicated records** with a PSIT affiliation string, 2007–2026, and the scripts that reproduce it.

Each of the seven pages now opens with a 10-line READ THIS FIRST block - read that first, in order.

## 2. Five facts worth carrying in your head

- A paper is not a report of work; it is a **claim plus evidence plus a way to check the evidence**. Reviewers reject work they cannot check.
- Write **results first, introduction last**. The intro is the last thing that becomes true.
- arXiv is **not peer reviewed**, and since 21 Jan 2026 a new submitter needs an institutional email *and* prior authorship in the field, or a personal endorser — you cannot self-endorse. A faculty co-author solves this. [VENUES-AND-PUBLISHING §2]
- **UGC-CARE is discontinued** (UGC notice, 16 Jul 2025), and CORE stopped ranking journals in 2022. Most Indian advice you will hear on this is out of date. [VENUES-AND-PUBLISHING §10]
- AI disclosure is now a real requirement with real wording. ACM moved it to the methods section in May 2026; NeurIPS, ICML and ACL all require it in specific places. [ETHICS-AND-AI-USE §1]

## 3. What PSIT's public record actually shows

- 793 records, growing from 24 in 2019 to 148 in 2025; 2026 already shows 234 in ten months. A large part of the 2025→2026 jump traces to one publisher family (Bentham), which is a testable explanation, not a verdict. [analysis/ANALYSIS.md §2]
- **394 distinct venues for 793 papers.** That is the structural fact: the output is spread extremely thin, so almost nobody at PSIT is building a sustained line in one venue.
- 168 records (**21.2%**) touch AI/ML by a strict keyword screen — but **none** appears in a recognised AI venue (ACL/NeurIPS/ICML/CVPR/AAAI/EMNLP). Verified by name match. [subfolder_ai_research/AI-RESEARCH-AT-PSIT.md]
- Median citations per paper: **1**; 40% have zero. (Partly an age effect: most of the corpus is 2024–2026.)
- 507 distinct PSIT-affiliated author name strings, undeduplicated — so "top author" lists are approximate.

## 4. The two findings that matter for your plan

1. **The three PSIT entities are collapsed into one record in the world's databases.** ROR has exactly one entry (`04v8v3741`), named "PSIT-Pharmacy", with the engineering name as an alias. OpenAlex has one institution node (1,412 works) also named "Pharmacy". So a paper by a PSIT-CHE author is counted under "Pharmacy" — or under nothing. Any single "PSIT publication count" is therefore ambiguous, including the ones you will hear quoted. [01_psit_data/README.md §2]
2. **Self-reported numbers and database numbers diverge, and the institute's own documents show why.** In the NAAC SSR, the UGC-CARE paper count reads 148/136/87/72/147 *before* NAAC's data validation and 37/21/18/17/24 *after* (page 89/95, verified in `raw/institute_docs/psit_naac_ssr.pdf`). Nobody needs to be accused of anything: the lesson is that a "publication" in a brochure and a "publication" in a database are different objects.

## 5. Where a student can actually contribute

The dataset points at one gap that suits a beginner: PSIT's AI work is *applied* — small local datasets, few baselines, almost no seeds reported (3 of 108 abstracts mention a baseline, 0 mention seeds). A careful, small, honest study that takes one such paper's question, uses public data, adds a dumb baseline and a strong baseline, five seeds, and mean±spread, is publishable at a student workshop and teaches you the whole craft. Three concrete shapes are in `subfolder_ai_research/AI-RESEARCH-AT-PSIT.md` §6.

## 6. What could not be done today (and why it is not a dead end)

OpenAlex, Semantic Scholar and DBLP all returned HTTP 429 from this network on 2026-11-03 (OpenAlex: shared free budget exhausted, resets 00:00 UTC). The evidence is saved in `01_psit_data/raw/*_unavailable.json` and the harvest scripts are written and ready: after midnight UTC, or with a free key from openalex.org/settings/api, `python 01_psit_data/scripts/harvest_openalex.py` completes the picture. Nothing was invented to cover the gap.

## 7. Next five things you personally should do

1. Read `WHAT-IS-A-PAPER.md` and `HOW-TO-WRITE-ONE.md` (about 80 minutes).
2. Read `ETHICS-AND-AI-USE.md` §5 and set up the one-line AI-use log it gives you. Start today, not when you have a draft.
3. Skim `analysis/ANALYSIS.md` §4–5 so you can explain the venue and citation numbers out loud.
4. Send the email in `drafts/EMAIL-TO-PSIT-RnD-CELL.md` — but first confirm the recipient address, which is a placeholder because no R&D cell address is published; the Dean (Research & Innovation) is the person to address.
5. Do the exam-period thing: nothing. This project resumes after exams; the files are written so a later session can pick up cold.

last_updated: 2026-11-03
