# TASK R3-4e — whole-paper consistency audit

Lane: R3-4e-consistency; main laptop; profile res-s4; created 2026-11-18.

## Objective
Audit the current generated paper end to end. Reconcile each hypothesis verdict (H1/H2/H3), every headline number, and every substantive claim repeated across the abstract, introduction, methods, results, tables, discussion, conclusion, and limitations. Correct contradictions in the template using existing evidence only. Update the response letter when an item verdict or description changes. Deliver `CONSISTENCY.md` with claim groups, all locations, agreed wording/value, and edits made.

Known issue requiring resolution: Table 4 and §4.2 say H1 is not exercisable at the registered operating point, but §4.6 says H1 remains refuted. MF-25 is only partly done. Do not assume which verdict is correct; read the registered criterion, results, and response-letter claim, then use precise wording that distinguishes registered-point testability from exploratory evidence. Check H2 and H3 similarly for repeated verdict drift.

## Owned paths
- `05_paper/template/**`
- `04_experiments/src/make_paper_assets.py` (only if needed to preserve generated consistency; prefer template-only edits)
- `04_experiments/RESULTS-INDEX.json` (read-only unless essential and authorized by existing keys; do not add results)
- `05_paper/draft/**` (generated output only; never hand-edit `paper.md`)
- `05_paper/tables/**`
- `05_paper/figures/**`
- `06_review/**`
- `sessions/R3-4e-consistency/**`

Never write `05_paper/latex-build/**`, any `04_experiments/results/**` or `04_experiments/runs/**`, `PREREGISTRATION.md` or its hash history, or paths owned by R3-3b. Do not commit, push, change branches, edit the runner, or restart the Hermes gateway. Do not use or bind any pending R3-3b results.

## Required work
1. Split the paper into thirds by section ranges. First batch is exactly three independent subagents, one read-only auditor per third. Each reports repeated claims, locations, exact current wording/values, discrepancies with evidence, and suggested agreed wording. Include claims that cross third boundaries by listing them in both relevant reports. The lead reconciles overlaps.
2. Audit all H1/H2/H3 statements and verdicts, headline numeric claims, and every material repeated claim. Trace numeric values to existing results keys and source rows. Any numeric text changed in the template must retain or use an existing `<!-- num:key -->` marker. No new numeric result or key.
3. Fix contradictions in `05_paper/template/draft_template.md` only; rebuild with `python 05_paper/build_draft.py`. Update `06_review/RESPONSE-LETTER-R3.md` only where the corrected verdict or item description requires it. Preserve the 85 canonical item inventory and report any verdict tally change.
4. Create `sessions/R3-4e-consistency/CONSISTENCY.md` listing every claim group, all locations (section/table and line references), agreed wording/value, evidence/result keys, and exactly what changed. Mark groups with no changes as checked/consistent. Include the final H1/H2/H3 verdict wording in one concise table.
5. Use subsequent batches of exactly three tasks. From batch two onward, one subagent must independently re-check the previous batch's audit or edits and run its specified proof. The independent reviewer cannot verify edits they authored. Continue until the review and all gates pass.
6. Record every batch and exact checks in `PROGRESS.md`. Before completion run:
   - `python tools/check_numbers.py --draft 05_paper/draft/paper.md` — 0 findings.
   - `python 05_paper/build_draft.py` twice — byte-identical generated draft content/hash.
   - `python tools/check_all.py` — 4/4 PASS.
   Verify the response-letter inventory/tally if changed. Record exact output and draft SHA. Last line of PROGRESS.md must be `CARD COMPLETE` only if every deliverable and gate passes; otherwise report the specific incomplete state.

No new experiments or simulated review. Do not use R3-3b output, which a separate lane will integrate later. Do not poll or wait on any other lead.
