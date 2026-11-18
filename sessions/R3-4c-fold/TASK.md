# TASK R3-4c — fold round-2 and round-3 review findings into the draft

Lane: R3-4c-fold; main laptop; profile res-s4; created 2026-11-18.

## Context and evidence boundary

R3-4b-review was stopped because it did not perform deliverable 1: it did not fold the 21 PARTIAL and 5 DEFERRED round-2 items into the template. `05_paper/template/draft_template.md` and the draft hash remained unchanged. It did create six independent persona reviews, an INGEST, and an AGGREGATE in `06_review/reviews/round3-c1/`. Those are a valid simulated round-3 review of the pre-fold draft. The round-3 scores are diagnostics, not venue predictions. Do not run another review round in this lane.

The round-3 aggregate reports six borderline decisions, mean 5.67/10, and 41 distinct must-fix items. `06_review/reviews/COMPARE-round2-round3.md` classifies 22 as persisted themes and 19 as new. Round-3 review content and scores refer to the pre-fold draft. Keep that timing explicit in the regenerated comparison, even after the draft changes.

The current draft is generated only from `05_paper/template/draft_template.md` using `python 05_paper/build_draft.py`. Do not edit `paper.md` directly. Every numeric statement added to the paper must use existing result-file evidence and the `<!-- num:... -->` mechanism. Do not invent numbers or run new experiments. If evidence cannot support a requested resolution, describe the limitation and leave it partial/deferred.

Hermes `write_file` may refuse to overwrite a changed file. Re-read every target file immediately before editing and prefer the patch tool.

## Owned paths

Same as R3-4b-review, except this lane owns the integrator work and explicitly excludes the LaTeX build:

- `05_paper/template/**`
- `04_experiments/src/make_paper_assets.py`
- `04_experiments/RESULTS-INDEX.json`
- `05_paper/draft/**`
- `05_paper/tables/**`
- `05_paper/figures/**`
- `06_review/**`
- `sessions/R3-4c-fold/**`

Do not write `05_paper/latex-build/**`; R3-7b owns it. Everything outside the owned paths is read-only. Preserve frozen run files and all existing results. Do not commit or push.

## Deliverables

1. Fold the 21 PARTIAL and 5 DEFERRED round-2 items listed in `06_review/reviews/COMPARE-round2-round3.md` into the template where the existing evidence permits. Also address all 41 round-3 must-fix items from `06_review/reviews/round3-c1/AGGREGATE.md`: the 22 persisted themes and 19 new findings. For each item, make a supported correction, narrow/rebut with evidence, or state why it remains partial/deferred. Do not conceal negative, inconclusive, or post-hoc evidence. Use the already-produced lane ANSWERS/reports and result files; no new experiment runs.
2. Rebuild with `python 05_paper/build_draft.py`. Run `python tools/check_numbers.py --draft 05_paper/draft/paper.md`; target is 0 findings. A draft SHA change from the verified baseline is required.
3. Regenerate `06_review/reviews/COMPARE-round2-round3.md` with the real round-3 scores and decisions from the existing `INGEST.md` and `AGGREGATE.md`. Label clearly that round 3 reviewed the pre-fold draft (sha `9194a481c8c0`) and that the fold is post-review. Do not repack prompts, regenerate persona reviews, ingest, or aggregate another review.
4. Update `06_review/RESPONSE-LETTER-R3.md` so all 44 round-2 items and all 41 round-3 items have a final verdict and a concrete change or evidence-based reason they remain unresolved. Include section, file, and result key when applicable. Distinguish the pre-fold round-3 observation from changes made after that review.
5. Run `python tools/check_all.py`; target is 4/4 PASS. Record commands, outputs, draft hash change, unresolved items, and next steps in `PROGRESS.md`.

## Progress and gates

Create/update `sessions/R3-4c-fold/PROGRESS.md` after every batch with completed work, file-and-command evidence, values, and next action. Verify subagent claims yourself. Maximum three rework rounds per item. The final line may be `CARD COMPLETE` only when all achievable deliverables and gates are done; otherwise end with `CARD BLOCKED: <specific reason>` only for a genuine blocker. Do not report completion when a gate failed.

Required gates before completion:

- Draft SHA changed from baseline.
- `python tools/check_numbers.py --draft 05_paper/draft/paper.md` reports 0 findings.
- `python tools/check_all.py` reports 4/4 PASS.

## Batches

Every lead batch is exactly one `delegate_task` call with exactly three parallel tasks. First action after reading the instructions must be that call. Each task must have one independent deliverable, exact owned write paths, input files to read, a proving command/check, and a report path under `sessions/R3-4c-fold/reports/`. From batch two onward, one task must independently review and re-run/check the previous batch output. Update PROGRESS after each batch. Never leave subagents running after ending a turn.
