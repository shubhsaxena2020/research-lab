# HEAD-REVIEW (Claude Code) — latest at 01:20 IST, 2026-11-03
Phase 2 (experiments) stays LOCKED. This file does not yet contain the approval line.

## Checkpoint 1 findings (spot-checked from disk, not from your reports)
- S1: 7 foundation docs exist (~36k words) — good volume, but (a) STATUS.md still says NOT STARTED: update it NOW and every 15 min (RULES.md #12); (b) `00_foundations/_tmp_ethics.md` is a stray temp file: delete it; (c) 36k words is too much for a first-semester student mid-exams: each doc needs a 10-line "READ THIS FIRST" summary at the top, and 06_review/STUDENT-DIGEST-S1.md must be <= 1 page. Priority next: B1-B6 (PSIT public data) — nothing is in 01_psit_data yet except empty folders.
- S1 link check: 13/14 sampled URLs resolve (the one 403 is a bot-blocking US State Dept page, fine). Link existence is NOT claim support: for the 20 most important claims (venue deadlines, eligibility rules, AI-use policies) quote the exact sentence from the source page and its URL in a `claims_evidence.md`.
- S2: good use of 7 parallel subagents. Remember every citation goes through verified_citations.csv before use; I will re-resolve a random 20 at the next checkpoint.
- S3: you are running Phase 1 mostly alone. USE `delegate_task` with up to 9 subagents: the 8 packages S3-1..S3-8 are independent, launch them as one batch. One owner per file.
## Standing decisions
- Topic decision is the head's. S2 delivers SELECTED.md + NOVELTY-CHECK.md; the head reads them, then writes `TOPIC APPROVED` (or a veto) here.
- Do not spend effort polishing prose before data/tools exist; correctness and traceability first.
