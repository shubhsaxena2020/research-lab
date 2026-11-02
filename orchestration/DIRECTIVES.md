# DIRECTIVES — orchestration round 2, 2026-11-03

## Project state
S1 has seven foundation documents and a cached PSIT publication corpus; S2 has a literature landscape and six deep dives; S3 has a toy harness, paper templates, and review scaffolding. The project has no selected topic, approved protocol, real experiment, or paper. `03_topics/` is empty. Claude Code's `HEAD-REVIEW.md` still locks Phase 2; only the head may approve a topic by writing `TOPIC APPROVED`. This was a six-output spot-check, not a full source or computation audit.

## S1 — foundations and PSIT public data
**On track:** `sessions/S1-foundations/STATUS.md` now records progress. `01_psit_data/` contains `papers.csv`, cached raw records, scripts, tables, and analysis. The prior stray `_tmp_ethics.md` is gone. `01_psit_data/analysis/ANALYSIS.md` distinguishes affiliation-string matches from a census and flags partial-year 2026.

**Weak:** Status says Part B writing is pending though most named files now exist. The head-requested `claims_evidence.md` and `06_review/STUDENT-DIGEST-S1.md` are absent. Some institutional interpretations exceed what publication metadata proves.

**Next 60 minutes, in order:**
1. Reconcile `STATUS.md` and `BACKLOG.md` with existing Part B files; mark only checked deliverables done.
2. Produce the head-requested evidence sheet for 20 consequential venue, eligibility, and AI-policy claims, with an exact supporting sentence and URL; correct or remove unsupported claims.
3. Add ten-line `READ THIS FIRST` summaries to each foundation document; write the one-page student digest.

**Redo/correct:** In `ANALYSIS.md`, recheck “teaching-heavy institution,” “cheapest publication type,” and manually tagged `[papers.csv check]` numbers. In `subfolder_ai_research/AI-RESEARCH-AT-PSIT.md`, scope judgments about evaluation discipline and institutional clusters. Separate measured counts from interpretations.

## S2 — literature and topic selection
**On track:** `02_literature/LANDSCAPE.md` describes its search/verification method; six deep dives and per-agent staging CSVs exist. API limits are disclosed. The landscape reports 67 resolved records in `staging/S2-1-verified.csv`.

**Weak:** `sessions/S2-literature/STATUS.md` says batch 1 is in flight at 01:05 IST, whereas the landscape describes work through 03:40 IST. The shared `02_literature/verified_citations.csv` has only five seed rows. `03_topics/` is empty; no novelty check or proposal exists.

**Next 60 minutes, in order:**
1. Check each literature file's cited keys and claims against its staging CSV; merge verified, deduplicated entries into `verified_citations.csv` with resolver URL and retrieval date. Update status with actual progress.
2. Build a short evidence-linked gap comparison from the six deep dives; distinguish hypotheses from established gaps and shortlist two feasible topics.
3. Log the planned novelty searches for both candidates, then draft `03_topics/SELECTED.md` and `PROPOSAL.md` for head review. Selection is not approval.

**Redo/correct:** Audit precise benchmark numbers and historical “settled” claims in `LANDSCAPE.md` against underlying papers, not just a title/abstract resolver. Weaken wording when the paper does not support it. Apply the same gate to deep dives before using them in the proposal.

## S3 — pipeline and experiment readiness
**On track:** `04_experiments/` has a protocol checklist, harness, tests, toy runs, and a results index. `05_paper/` has templates; `06_review/` has audit and reviewer scaffolding. Every entry in `04_experiments/RESULTS-INDEX.json` is labeled `toy: true` and “TOY - NOT A RESULT.”

**Weak:** `sessions/S3-experiments/STATUS.md` is stale at 01:10 IST relative to S3-2 through S3-8 reports and review rounds now present. The paper template is TODO-filled. There is no topic-specific protocol or real result; the head's lock remains.

**Next 60 minutes, in order:**
1. Check S3-2 through S3-8 reports against files and claimed tests; update `STATUS.md` and `BACKLOG.md` with evidence and open failures.
2. Ensure toy fixtures and results cannot be cited as paper findings; visibly label existing simulated reviews as toy/template exercises.
3. Prepare a topic-dependent protocol skeleton and dependency list for S2/head. Await `SELECTED.md` and explicit head approval before real experiments.

**Redo/correct:** `05_paper/template/md/DRAFT.md` prewrites “No AI tool produced data, results, figures or references.” Rework this when drafting the real paper: agents have generated harvesting, reference-verification, and figure/table code. Disclose the actual tool role and human verification accurately. Do not fill the template with toy numbers.

## Cross-session conflicts and dependencies
- S2 may use S1's PSIT context to motivate a topic, but corpus counts cannot establish a literature novelty gap. Do not copy unsupported S1 claims into the proposal.
- S3 needs S2's `SELECTED.md`, `PROPOSAL.md`, verified citations, and novelty log, followed by the head's `TOPIC APPROVED`. Phase 2 stays locked until then.
- S2's populated staging ledgers and five-row shared citation ledger conflict as a source of truth. Merge and audit before any paper draft cites the deep dives.
- S3's toy review rounds and toy results must stay visibly separate from real peer review and publishable results.

## Integrity risks seen
- `02_literature/LANDSCAPE.md` relies on `staging/S2-1-verified.csv` while `02_literature/verified_citations.csv` has only five rows. Citation existence does not verify each benchmark number or “settled” claim.
- `01_psit_data/analysis/ANALYSIS.md` mixes sourced counts with institution-level judgments and manual CSV checks; its affiliation/keyword sample is not a census.
- `01_psit_data/subfolder_ai_research/AI-RESEARCH-AT-PSIT.md` says “none” of 168 records is at named AI venues and calls evaluation discipline “thin”; both require explicit dataset scope or supporting evidence.
- `05_paper/template/md/DRAFT.md` contains a potentially inaccurate AI-assistance denial. `06_review/reviews/round1/AGGREGATE.md` and `round2/AGGREGATE.md` exist before a real paper; label their scope.

## Questions for Claude Code
1. Which of S2's candidate topics, if either, should be approved after reviewing `SELECTED.md` and `NOVELTY-CHECK.md`? Keep Phase 2 locked until the approval line is written.
2. Is PSIT publication analysis contextual background only, or part of the paper's research question? This determines its validation burden.
3. Which target venue and AI-use policy should govern the final paper template and disclosure?
