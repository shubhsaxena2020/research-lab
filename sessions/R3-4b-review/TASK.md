# HEAD ORDER 2026-11-18 21:30 IST - LANE R3-4b IS CANCELLED. If you are the R3-4b lead or one of its subagents: STOP NOW. Do not edit any more files. Lane R3-4c-fold (a new res-s4 session) has taken over this work. Write the line CARD BLOCKED: lane cancelled by head as the last line of this file and end your turn.

# TASK R3-4b — finish the round-3 fixes, then run review round 3 for real (MAIN laptop, profile res-s4)

Context (head, 2026-11-18): R3-4 stopped on 2026-11-08 after its first batch. Its honest status is in
`06_review/reviews/COMPARE-round2-round3.md`: of the 44 round-2 must-fix items, 18 are resolved in the draft,
21 are partial and 5 are deferred. Round-3 reviews were NEVER run: `06_review/reviews/round3-c1/` holds only
prompt packs, and they were packed against an older draft (sha 9194a481; current draft is e346271e), so they are stale.
Laptop 2 is offline; only two Hermes sessions run (you and R3-7b, which owns `05_paper/latex-build/**`).

OWNED: `05_paper/template/**`, `04_experiments/src/make_paper_assets.py`, `04_experiments/RESULTS-INDEX.json`,
`05_paper/draft/**`, `05_paper/tables/**`, `05_paper/figures/**`, `06_review/**`, `sessions/R3-4b-review/**`.
Everything else is read-only. Never edit the frozen run, PREREGISTRATION.md, or results outside results/c1/r3/.

Deliverables, in order
1. Fold the 21 PARTIAL and 5 DEFERRED items into the draft. For each, use the evidence the R3-1/2/3/5 lanes already
   produced (their reports and ANSWERS files) and the row in COMPARE-round2-round3.md / RESPONSE-LETTER-R3.md.
   Edit `05_paper/template/draft_template.md` (never paper.md by hand), rebuild with `python 05_paper/build_draft.py`,
   then `python tools/check_numbers.py --draft 05_paper/draft/paper.md` must report 0 findings. New numbers come only
   from result files via the existing `<!-- num: -->` marker mechanism. If an item cannot be done honestly, say so in
   RESPONSE-LETTER-R3.md and keep it partial; do not paper over it.
2. Re-pack round 3 against the NEW draft: `python tools/simulate_review.py pack ...` into `06_review/reviews/round3-c1/`
   (replace the stale packs; read the tool's --help and how round2-c1 was produced).
3. Write the six persona reviews: each subagent reads exactly one `<persona>.PROMPT.md` and writes the matching
   `<persona>.review.yaml` in the format the prompt demands, as that reviewer, independently and critically (two batches
   of 3 personas). Then run ingest and aggregate so `AGGREGATE.md` exists.
4. Regenerate `06_review/reviews/COMPARE-round2-round3.md` with real round-3 scores and decisions (like
   COMPARE-round1-round2.md) and update `06_review/RESPONSE-LETTER-R3.md` so every one of the 44 items has a final verdict
   plus the concrete change (section, file, result key).
5. Final checks: `python tools/check_all.py` 4/4 PASS and check_numbers 0 findings. Record the outputs in PROGRESS.md.
Batches of exactly 3 subagents; from the second batch on, one task reviews the previous batch.
