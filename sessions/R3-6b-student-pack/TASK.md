# TASK R3-6b — refresh the student pack for the current Round 3 state

Lane: R3-6b-student-pack; main laptop; profile res-s1; created 2026-11-19.

## Goal

Prepare a short, plain-English student pack for a first-semester BCA student. Explain what Round 3 changed, what the new R3-3b analyses show, what those results can and cannot mean, and the current H1/MF-14 caveats. Every numerical claim must be traceable to an exact source file and result key or an explicitly identified source-file fact. Mark every R3-3b finding exploratory/post-hoc and state that these findings are not yet in the draft.

## Ownership and exclusions

Write only these paths:

- `07_student/**` — create this new folder; do not use or modify `06_review/**`.
- `sessions/R3-6b-student-pack/**` — this lane's progress and reports.

R3-4e-consistency on res-s4 owns `05_paper/template/**`, `05_paper/draft/**`, `05_paper/tables/**`, `05_paper/figures/**`, `04_experiments/RESULTS-INDEX.json`, and `06_review/**`. Do not write, move, or rename any of those paths. Do not bind the R3-3b results into the paper. Do not commit, push, change branches, touch the frozen run or preregistration, edit the Hermes runner/configuration, or restart the gateway.

Read-only source inputs include `RULES.md`, `sessions/R3/COMMON.md`, `orchestration/HEAD-REVIEW.md` checkpoints 9-10, `sessions/R3-4e-consistency/TASK.md`, `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` and its cited JSON files, `sessions/R3-4d-verify-fold/PROGRESS.md`, and the relevant original result records cited there. Treat the live R3-4e paths as unavailable for this lane; use checkpoint/task records for the state of that work.

## Deliverables

1. `07_student/ROUND3-DIGEST.md`: at most about two pages, explaining in simple language what changed in Round 3 and the R3-3b findings. Preserve the limits precisely: post-hoc/exploratory, not human gold, no frozen verdict revised, and not yet in the draft. Explain Cohen's kappa 0.2802 as modest agreement beyond chance in this particular two-LLM setup, not accuracy or proof the labels are true. Explain MF-7's gold-indicator AUROC 1.0 as a construction/label artefact and D3 as pooled rung=-1 data without per-rung R1-R3 estimates. Explain H1 as not exercisable at the registered operating point; do not call it confirmed or refuted based on exploratory evidence. Explain MF-14's registered versus exploratory comparison only from checked, cited evidence.
2. `07_student/VIVA-QA.md`: short viva questions and plain answers covering MF-14, why H1 is not exercisable, what kappa 0.2802 means, what the gold-indicator result means, and claims the student must not make. Keep answers understandable to a first-semester BCA student.
3. `07_student/SOURCE-MAP.md`: map every numeric claim in the digest and viva answers to the exact source path and JSON result key (or the precise source-file section/table for non-result facts). Include the exact value represented and its rounding. No unsupported numbers.
4. Lane progress and one report per subagent task under `sessions/R3-6b-student-pack/`; report exact files/checks and any unresolved source gaps.

## Required batching

Use `ops/lead_protocol_r3.txt`. Every batch is one blocking `delegate_task` call with exactly three parallel tasks. Batch 1: one writer for the digest, one writer for viva Q&A, and one writer for the source map; keep their write paths separate. Batch 2: an independent reviewer must check every number in both student documents against the source file/key and report mismatches; the other two tasks independently review plain-language accuracy/support limits and required-topic completeness. Reviewers are read-only and write only their lane reports. Lead must open all reports and independently check every numeric mapping before completion. Continue only if corrections are required, using batches of exactly three tasks and an independent re-review.

Use commands/checks appropriate to Markdown. Confirm all output paths are within the two owned roots. Do not claim completion unless all numbers are source-checked and the language preserves the stated limitations. Last line of `PROGRESS.md` must be `CARD COMPLETE` only when complete, otherwise state the exact unfinished work.
