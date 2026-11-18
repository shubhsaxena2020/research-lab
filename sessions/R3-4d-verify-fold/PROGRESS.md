# R3-4d-verify-fold PROGRESS

## Setup verified
- Workdir C:\Users\shubh\research-lab; owned paths per TASK.md; no writes to 05_paper/latex-build/**.
- Baseline gates at session start:
  - `python tools/check_numbers.py --draft 05_paper/draft/paper.md` -> 505 numbers, 318 matched, 187 exempt, 0 findings, PASS.
  - `python tools/check_all.py` -> 4/4 steps PASS (tools-tests, harness-tests, paper-tests, toy-pipeline).
  - Draft sha256 at start: 89e92e7990a451ff49ac14f11d016bf8b44d4b85906d0bba64f6d9cc3b7a9ca8.
  - git HEAD 88d6b57 (R3-7c merged); no commits made by this lane.

## Batch 1 — independent audit of all 23 currently-resolved claims + inventory
Delegate call with exactly 3 parallel read-only auditors. Reports:
- reports/audit-A.md (MF-1,2,8,11,14,15,20,26)
- reports/audit-B.md (MF-27,33,34,35,38,39,40,41 + inventory)
- reports/audit-C.md (MF-42,43,R3-MF-3,36,37,38,39)

Lead verification (opened all three reports; spot-checked draft directly):
- MF-14: draft lines 450/456 have "Band abstain precision, R4 | 100.00% | 90.73%" and "Exploratory precision, R4 | 84.71% | 12.53%"; §5.2 lines 581-590 are not scoped to the measured corpus/feature stack/gate and do not mark the corrected result exploratory/post-hoc. Confirms head audit: MF-14 overclaimed -> must fix.
- R3-MF-39: draft lines 17, 179, 218 still contain 'abstain recall' -> not implemented as claimed.
- Inventory parser (lead, executed): round 2 = 18 resolved / 21 partial / 5 deferred (44); round 3 = 5 resolved / 30 partial / 6 deferred (41); total 85. Letter header says 23/52/11=86 -> counting error: partial count should be 51, not 52; no duplicate or orphan IDs.

Audit outcomes (23 resolutions tested):
- Fully supported (13): MF-2, MF-26 (A); MF-27, MF-33, MF-34, MF-38, MF-41 (B); MF-42, MF-43, R3-MF-3, R3-MF-36, R3-MF-37, R3-MF-38 (C).
- Downgrade to partial (10): MF-1, MF-8, MF-11, MF-14, MF-15, MF-20 (A); MF-35, MF-39, MF-40 (B); R3-MF-39 (C). Reasons: missing exact fractions/denominators per cell, absent per-rung length/overlap distributions, MF-14 unsupported placement + unscoped §5.2, generator prefix misalignment / table-count mismatch, and retained 'abstain recall' term.

Also noted for the next batch: several items marked partial are already implemented in the current draft (MF-4/MF-25/R3-MF-2: six hashes; MF-5/R3-MF-4: H1/H3 verdict column already 'criterion not exercisable'; MF-30/R3-MF-28: no stale 'no lockfile' sentence). These must be upgraded only after independent re-quotation in batch 2.

## Batch 2 — review of batch 1 + MF-14 template fix + verdict downgrades
Three parallel tasks: (1) independent reviewer re-checked batch-1 evidence (reports/review-batch1.md) — confirmed all 10 downgrades and the 85-item inventory, found no verdict-changing mismatches; (2) MF-14 template fix (reports/mf14-fix.md); (3) VERIFY-RESOLVED.md + response-letter downgrades (reports/verify-consolidate.md).

Lead verification after batch 2:
- Opened template: abstract and §4.6 now place registered band R4 `c1.band.precision.r4.run` 100.00%, frozen exploratory R4 `c1.expl.precision.r4.run` 84.71%, beside corrected exploratory R4 `c1.expl.precision.r4.corr` 12.53%, each with num markers and run labels; §5.2 scoped to measured corpus/feature stack/gate and marks corrected result exploratory/post-hoc (D4), not replacing registered result. No new keys.
- Draft sha after rebuild: `1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0`. Subagent reported two builds byte-identical (both 61306 bytes, same sha).
- `python tools/check_numbers.py --draft 05_paper/draft/paper.md` -> 509 numbers, 322 matched, 187 exempt, 0 findings, PASS (reported; lead will re-run at final gates).
- `VERIFY-RESOLVED.md` exists with 23 rows, 13 resolved / 10 partial; response letter re-parsed by lead: 13 resolved / 61 partial / 11 deferred = 85; header documents the 86->85 counting correction and the ten downgrades.
- Lead moved two reports mistakenly written to repo-root `reports/` into this lane's `reports/` and removed the stray root folder.

Next: batch 3 = (1) independent review/re-run of batch-2 outputs, (2) wording/structure folds of high-impact partials with existing support, (3) response-letter updates for items already implemented in the current draft plus folded items.

## Batch 3 — review of batch 2 + wording/structure folds + verdict upgrades
Three parallel tasks: (1) reports/review-batch2.md — all four batch-2 claims confirmed, no mismatches; gates re-run by reviewer (build byte-identical sha 1679b75f..., check_numbers 0 findings, check_all 4/4 PASS). (2) reports/folds-batch3.md — four folds landed: removed all 5 'abstain recall' occurrences (R3-MF-39); MF-29 construction-degeneracy wording; MF-13 two-sided |AUROC − chance| note (no new number); MF-35 generator/template table prefixes renamed to appearance order T1_prior_work…T7_ablations_corrected. (3) reports/letter-upgrades-batch3.md — 15 verdicts upgraded to resolved; tally 13/61/11 -> 28/46/11=85. Writer flagged four folds as pending because it ran before the parallel fold writer finished; batch-4 review confirmed the folds landed, so the flag is stale documentation only.

Lead verification: draft sha advanced to d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500; `grep -c 'abstain recall' paper.md` = 0; two-sided note at L206; degeneracy wording at L543-544; template placeholders and generated tables in new order; letter re-parsed to 28/46/11=85. Lead re-ran: build (61620 bytes, sha d81cc90ffe60, identical across two builds), check_numbers (509 numbers, 322 matched, 187 exempt, 0 findings, PASS), check_all (4/4 PASS).

## Batch 4 — final review, VERIFY-RESOLVED finalization, cleanup and inventory
Three parallel tasks: (1) reports/review-batch3.md — all folds landed, MF-14 intact, tally 28/46/11; only stale PENDING note in letter-upgrades report. (2) reports/verify-finalize.md — appended 'Post-fold status' section to VERIFY-RESOLVED.md with all 23 originally-resolved items; final 23-item tally 17 resolved, 6 partial, 0 deferred (MF-14, MF-35, MF-40, R3-MF-39 upgraded; MF-1, MF-8, MF-11, MF-15, MF-20, MF-39 remain partial with reasons). (3) reports/final-inventory.md — deleted 9 stale pre-rename generated table files; re-gates PASS; canonical IDs exactly round-2 MF-1..44 + round-3 R3-MF-1..41 (85, no gaps/duplicates); git status shows no 05_paper/latex-build/** changes.

Lead final verification: sha d81cc90ffe60... unchanged after cleanup; check_numbers 509/322/187/0 PASS; check_all 4/4 PASS (tools 37.5s, harness 34.9s, paper 5.0s, toy 11.1s); letter tally 28 resolved / 46 partial / 11 deferred = 85; no STOP file; no commits made; 05_paper/latex-build/** untouched.

Deliverables complete: VERIFY-RESOLVED.md with exact draft quotations for all 23 originally resolved items + post-fold status; MF-14 fixed with existing registered keys/markers and §5.2 scoped; wording/structure partials folded with existing support; 86-vs-85 tally reconciled as a counting error (85 canonical IDs, 51 pre-downgrade partials, not 52); all gates PASS with observed values recorded.

CARD COMPLETE
