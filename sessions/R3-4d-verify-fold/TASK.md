# TASK R3-4d — independently verify the fold and improve wording-only partials

Lane: R3-4d-verify-fold; main laptop; profile res-s4; created 2026-11-18.

## Context

R3-4c-fold completed and was committed as `533998b`. Claude Code verified that the generated draft SHA changed to `89e92e79`, `check_numbers.py` found 0 issues, draft rebuilding was reproducible, and preregistration/frozen results were untouched. A head audit found an overclaim: round-2 MF-14 is marked resolved, but the template does not place registered R4 band precision and frozen exploratory R4 precision beside corrected exploratory `12.53%`, and Section 5.2 is not restricted accordingly. MF-27 and MF-40 were spot-checked and appear supported. The response letter reports 23 resolved, 52 partial, and 11 deferred, summing to 86, while its apparent canonical inventory is 44 round-2 items plus 41 round-3 items. Reconcile this discrepancy explicitly; do not silently drop or duplicate an item.

The central requirement is independent evidence, not prior agents' summaries. For EVERY item the response letter currently calls resolved, a fresh verification subagent that did not make the claimed change must inspect the actual generated draft `05_paper/draft/paper.md` and quote exact text that implements that item's stated change. A table row may be quoted where the implementation is tabular. If supporting text is absent or incomplete, mark it MISSING and downgrade that item's verdict to partial with a precise reason. Complete `VERIFY-RESOLVED.md` with item ID, claim, exact draft quotation or MISSING, and final verdict. Quote the draft itself, not the response letter or a lane report. No verifier may verify a change they themselves wrote. Keep the round-3 pre-fold review status clear where relevant.

## Owned paths

Same integrator ownership as R3-4c, excluding the PDF build owned by R3-7c:

- `05_paper/template/**`
- `04_experiments/src/make_paper_assets.py`
- `04_experiments/RESULTS-INDEX.json`
- `05_paper/draft/**` (generated output only; never hand-edit `paper.md`)
- `05_paper/tables/**`
- `05_paper/figures/**`
- `06_review/**`
- `sessions/R3-4d-verify-fold/**`

Never write `05_paper/latex-build/**`; res-s1 owns it. Everything outside these paths is read-only. Never edit `04_experiments/results/**`, `04_experiments/runs/**`, `PREREGISTRATION.md` or its hash history. Do not commit or push.

## Deliverables

1. Inventory every response-letter entry, its canonical ID, claim, and current verdict. Expected round inventory is round-2 MF-1 through MF-44 and round-3 MF-1 through MF-41. Reconcile the stated 86 verdict total against the 85 expected item IDs and report any duplicate, orphan, or counting error.
2. Blindly verify every currently resolved claim using independent subagents who did not author the prior fold. Each entry in `sessions/R3-4d-verify-fold/VERIFY-RESOLVED.md` must give item ID, claim, exact quotation from `05_paper/draft/paper.md` or MISSING, and final verdict. Audit exact scope, denominators, run labels, caveats, and table values; keyword presence alone is not proof. Downgrade unsupported resolved verdicts to partial in `06_review/RESPONSE-LETTER-R3.md`, with a concrete reason. Do not upgrade a verdict unless the full claimed correction is present in the draft and independently verified.
3. Fix round-2 MF-14 in `05_paper/template/draft_template.md`: in the discussion of corrected exploratory R4's `12.53%`, place the existing registered band R4 `100.00%` and frozen exploratory R4 `84.71%` figures beside it, bound to existing result keys via `<!-- num:... -->` markers. Scope Section 5.2 to the measured corpus, feature stack, and gate; identify the corrected result as exploratory/post-hoc and do not imply it replaces the registered result. No new experiment or result value.
4. Fold PARTIAL items only when an honest wording, scope, terminology, or structure change can resolve or materially improve them without experiments or new evidence. Prioritize items with the greatest reviewer impact, especially repeated/persisted issues and clarity or claim-calibration risks. Any numeric wording must use an existing result key and the number marker mechanism. Leave evidence-dependent items partial/deferred and say why. Update each affected response-letter verdict and change description.
5. Rebuild only from the template with `python 05_paper/build_draft.py`; never edit `paper.md` directly. After every batch, record in `PROGRESS.md` and verify:
   - `python tools/check_numbers.py --draft 05_paper/draft/paper.md` reports 0 findings.
   - `python 05_paper/build_draft.py` run twice produces byte-identical generated draft content/hash.
   - `python tools/check_all.py` reports 4/4 PASS.
   Record commands and exact observed outputs after each batch. Do not claim a gate passed without rerunning it.

## Progress and integrity

Update `sessions/R3-4d-verify-fold/PROGRESS.md` after every batch. Put one report per subagent task in `reports/`. Verify all subagent claims by opening the report and checking the actual draft or rerunning its command. A writer must not be the verifier of the same change. Maximum three rework rounds per item. Last line may be `CARD COMPLETE` only when all required deliverables and gates pass; otherwise use `CARD BLOCKED: <specific reason>` only for a genuine blocker.

No model computation is expected. If a model job becomes necessary, follow `sessions/R3/COMMON.md` rule 6 exactly: GPU first, CPU torch only under its allowed fallback/spill conditions, and record device/reason. Do not restart the shared Hermes gateway. Do not touch res-s1 or any other project's profiles, processes, folders, or runner use.

## Batches

Every batch is one blocking `delegate_task` call with exactly three parallel tasks. First action after reading instructions must be that call. Each task must define one independent deliverable, exact owned write paths, inputs to read, proof command/check, and report path under this lane. The first batch partitions resolved entries among independent read-only auditors and includes inventory/count reconciliation. From batch two onward, one task independently reviews and re-runs/checks a previous batch output. Keep audit, template edits, and response-letter edits separated so no agent verifies its own change.
