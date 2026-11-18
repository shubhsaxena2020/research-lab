# PROGRESS — R3-4c-fold (integrator)

Lane: R3-4c-fold; main laptop; profile res-s4. Completed 2026-11-18.

## Batch 1 (delegate_task, 3 parallel tasks) — completed

### Task 1 — verify (rebuild + gates + coverage)
Report: `sessions/R3-4c-fold/reports/batch1-task1-verify.md`.
- `python 05_paper/build_draft.py` → sha256 `69e0d0790788` (baseline `3934ce7f56a0`; changed).
- `python tools/check_numbers.py --draft 05_paper/draft/paper.md` → 0 findings (503 numbers, 318 matched, 185 exempt).
- `python tools/check_all.py --timeout 580` → 4/4 PASS (tools-tests, harness-tests, paper-tests, toy-pipeline).
- Response letter counts: 44 round-2 (`^## MF-`) + 41 round-3 (`^### R3-MF-`).
- COMPARE contains `9194a481c8c0` (2 matches) and `post-review` (1 match).

### Task 2 — fold round-3 clarity items
Report: `sessions/R3-4c-fold/reports/batch1-task2-fold-clarity.md`.
Changed lines in `05_paper/template/draft_template.md`: 17, 33-36, 39-40, 43, 50, 175, 214, 275, 358.
- MF-4: six recorded hashes D1–D6 (front matter).
- R3-MF-35: surface features "in the expected direction"; R4 inverted separation of equal magnitude.
- R3-MF-36: R5 sits below R2 (not between R2 and R3).
- R3-MF-37: over-refusal vs per-rung precision wording clarified.
- R3-MF-39: 'abstain recall' defined as the refusal rate.
- R3-MF-40: closing generalisation scoped to corpus/feature stack/gate family.
- R3-MF-41: Figure 1 caption spec-corrected bands deferred to §4.6.
- R3-MF-38: Table 5 caption explains the 'Abstain precision' header.
- MF-24: "post-hoc" sensitivity analysis labelled.
- MF-22: held-out R2 counts (280 kept) added.
- MF-31/MF-37: in-force hash + dirty-tree disclosure.
- MF-1: refusal rate vs precision definition in Abstract/§3.3.
Rebuild: sha `89e92e7990a4`; check_numbers 0 findings (505 numbers, 318 matched, 187 exempt).

### Task 3 — strengthen response letter
Report: `sessions/R3-4c-fold/reports/batch1-task3-letter.md`.
- `06_review/RESPONSE-LETTER-R3.md`: 44 round-2 + 41 round-3 entries; generic 'Fold status:' placeholders removed (0 remaining). Each R3-MF item now carries a concrete verdict and evidence-based reason (resolved/partial/deferred), distinguishing pre-fold round-3 observation from post-fold changes.

## Additional fold edits (lead)
- `04_experiments/src/make_paper_assets.py`: Table 2 H1/H3 verdict changed from "REFUTED" to "criterion not exercisable (see §4.2)" (MF-5, MF-25).
- `06_review/reviews/COMPARE-round2-round3.md`: added timing note that round 3 reviewed the pre-fold draft (sha `9194a481c8c0`) and that fold edits are post-review; no new review round run.
- `05_paper/template/draft_template.md`: front matter corrected to six hashes D1–D6; §4.6 post-hoc labelling; §4.7 held-out R2 counts; §8 hash/dirty-tree disclosure.

## Final gates (verified 2026-11-18)
- Draft SHA: `89e92e7990a4` (changed from baseline `3934ce7f56a0`).
- `python tools/check_numbers.py --draft 05_paper/draft/paper.md` → 0 findings, exit 0.
- `python tools/check_all.py --timeout 580` → 4/4 PASS (tools-tests, harness-tests, paper-tests, toy-pipeline), exit 0.
- Response letter: 44 round-2 + 41 round-3 entries, 0 generic placeholders.
- COMPARE: contains `9194a481c8c0` and `post-review`.

## Unresolved items (remain partial/deferred with documented reasons)
Round-2 deferred (5): MF-7 (gold-paragraph control audit), MF-10 (adjudication of negatives), MF-17 (AUROC intervals), MF-23 (five nearest neighbours in Table 7), MF-28 (DeclineCraft row). Evidence exists (R3-3/R3-5); folding requires new index entries and new experiments beyond this lane's scope; documented in the response letter with reasons.
Round-3 new items (19): addressed where evidence permits (clarity/terminology folded); items needing new experiments or lockfile/citation changes remain partial/deferred with reasons in the response letter.

## Next steps
- R3-7b (latex build) consumes the updated draft; this lane did not touch `05_paper/latex-build/**`.
- Head commits at checkpoint. No git commits/pushes made by this lane.

CARD COMPLETE