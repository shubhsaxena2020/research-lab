# S1 STUDENT DIGEST — what you have and what it means

For Shubh. One page. Each claim points at the file that proves it.

## 1. What exists now

Seven pages in `00_foundations/`, each opening with a 10-line "READ THIS FIRST" block — read those in order:
`WHAT-IS-A-PAPER` (anatomy, six paper types, novelty, reproducibility) → `HOW-TO-WRITE-ONE` (idea to submission, writing order, LaTeX, 20 mistakes, 2-week and 3-month plans) → `VENUES-AND-PUBLISHING` (arXiv, workshops vs conferences vs journals, blind review, fees, visas, predatory venues, UGC/Scopus/NIRF, 10 target venue types) → `ETHICS-AND-AI-USE` (authorship, plagiarism, and the *quoted* AI policies of arXiv, ACM, IEEE, NeurIPS, ICML, ACL, COPE) → `WHAT-A-PAPER-DOES-FOR-YOU` (honest effect on MCA/MS/PhD, scholarships, internships; your 18+ and year rules) → `GLOSSARY` (125 terms) → `READING-LIST` (15 verified resources).

Plus `01_psit_data/papers.csv`: **793 deduplicated PSIT-affiliated records**, 2007–2026, with the scripts that rebuild it.

## 2. Five facts to carry

- A paper is a claim plus evidence plus a way to check the evidence. Reviewers reject what they cannot check.
- Write **results first, introduction last**.
- arXiv is **not peer reviewed**; since 21 Jan 2026 you cannot self-endorse — you need prior authorship in the field or a personal endorser. A faculty co-author solves it. [VENUES §2]
- **UGC-CARE is discontinued** (UGC notice, 16 Jul 2025) and CORE stopped ranking journals in 2022. Most Indian advice you will hear is out of date. [VENUES §10]
- AI disclosure is now required in specific wording. ACM updated its rules in May 2026. [ETHICS §1]

## 3. What PSIT's public record shows

- 793 records; 24 papers in 2019 → 148 in 2025 → 234 in ten months of 2026. A large part of that last jump is one publisher family (Bentham) — a testable explanation, not a verdict. [ANALYSIS §2]
- **394 distinct venues for 793 papers.** Output is spread very thin; almost nobody holds a sustained line in one venue.
- 168 records (**21.2%**) touch AI/ML — and **0 of 168** appear in a named AI venue, by a scoped name match. [AI-RESEARCH §5.1]
- Median 1 citation, 40% uncited (partly an age effect — most of the corpus is 2024–2026).
- 507 author name strings, not disambiguated. Treat "top author" lists as approximate.

## 4. The two findings that shape your plan

1. **Three institutions are collapsed into one database node.** ROR has one record (`04v8v3741`) named "PSIT-Pharmacy", with the engineering name as an alias; OpenAlex has one node (1,412 works), also "Pharmacy". So PSIT-CHE output is counted under "Pharmacy" or under nothing — every quoted "PSIT publication count" is ambiguous. [README §2]
2. **Self-reported and database counts diverge, and the institute's own filing shows why.** In the NAAC SSR the UGC-CARE count reads 148/136/87/72/147 *before* NAAC's data validation and 37/21/18/17/24 *after* (p.89/95, in `raw/institute_docs/psit_naac_ssr.pdf`). No accusation needed: a "publication" in a brochure and in a database are different objects.

## 5. Where you can actually contribute

PSIT's AI work is applied, and its abstracts rarely show evaluation hygiene: of 108 AI abstracts, 3 mention a baseline and 0 mention a seed. A small, honest study — one of their questions, public data, a dumb baseline and a strong one, five seeds, mean ± spread — is publishable at a student workshop and teaches the whole craft. Three concrete shapes: [AI-RESEARCH §6].

## 6. What is still blocked

OpenAlex (shared budget exhausted, resets 00:00 UTC), Semantic Scholar and DBLP all returned HTTP 429 from this network. Evidence in `raw/*_unavailable.json`; `scripts/harvest_openalex.py` is ready. Nothing was invented to cover the gap.

## 7. Do these five things

1. Read `WHAT-IS-A-PAPER` then `HOW-TO-WRITE-ONE` (~80 min).
2. Start the one-line AI-use log from `ETHICS §5` today, not when you draft.
3. Skim `ANALYSIS §4–5` so you can say the venue and citation numbers out loud.
4. Send the email in `drafts/EMAIL-TO-PSIT-RnD-CELL.md` — after confirming the address, which is a placeholder because none is published; the Dean (Research & Innovation) is the right person.
5. During exams: nothing. Files are written so a later session resumes cold.

last_updated: 2026-11-03
