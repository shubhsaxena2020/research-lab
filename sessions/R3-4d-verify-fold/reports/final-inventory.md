# Final Inventory — R3-4d verify-fold cleanup lane

Generated 2026-11-18T23:13+05:30. Repo root: `C:\Users\shubh\research-lab`.

## 1. Stale pre-rename generated tables — removed

The prefix rename reordered table numbers to match appearance order. The canonical
generator/template set is `T1_prior_work`, `T2_audit`, `T3_per_rung`, `T4_hypotheses`,
`T5_arms`, `T6_frozen_vs_corrected`, `T7_ablations_corrected`. Nine old-name files
remained (six `.md` plus three `.tex` siblings); all nine were deleted and nothing else
under `05_paper/tables/generated/` was touched.

| # | deleted stale file | had `.tex` sibling? |
|---|--------------------|---------------------|
| 1 | `T1_per_rung.md` | yes — `T1_per_rung.tex` (also deleted) |
| 2 | `T2_hypotheses.md` | yes — `T2_hypotheses.tex` (also deleted) |
| 3 | `T3_audit.md` | yes — `T3_audit.tex` (also deleted) |
| 4 | `T4_frozen_vs_corrected.md` | no |
| 5 | `T6_ablations_corrected.md` | no |
| 6 | `T7_prior_work.md` | no |

`rm -v` confirmed all nine removals:

```
removed '05_paper/tables/generated/T1_per_rung.md'
removed '05_paper/tables/generated/T1_per_rung.tex'
removed '05_paper/tables/generated/T2_hypotheses.md'
removed '05_paper/tables/generated/T2_hypotheses.tex'
removed '05_paper/tables/generated/T3_audit.md'
removed '05_paper/tables/generated/T3_audit.tex'
removed '05_paper/tables/generated/T4_frozen_vs_corrected.md'
removed '05_paper/tables/generated/T6_ablations_corrected.md'
removed '05_paper/tables/generated/T7_prior_work.md'
```

Directory contents after cleanup (7 canonical files, no stale names):

```
T1_prior_work.md
T2_audit.md
T3_per_rung.md
T4_hypotheses.md
T5_arms.md
T6_frozen_vs_corrected.md
T7_ablations_corrected.md
```

### Reference check (done BEFORE deletion)

- `05_paper/template/draft_template.md` contains only new-name placeholders:
  `{{TABLE:T1_prior_work}}` (L132), `{{TABLE:T2_audit}}` (L244),
  `{{TABLE:T3_per_rung}}` (L259), `{{TABLE:T4_hypotheses}}` (L263),
  `{{TABLE:T5_arms}}` (L365), `{{TABLE:T6_frozen_vs_corrected}}` (L417),
  `{{TABLE:T7_ablations_corrected}}` (L421). No old-name placeholder.
- `05_paper/build_draft.py` resolves placeholder names dynamically from the template; it
  hardcodes no table names and contains no old-name reference.
- `04_experiments/src/make_paper_assets.py` L588–594 writes only new names.
- Repo-wide grep over all `*.py`, `*.sh`, `*.ps1` (excluding archived `runs/` snapshots):
  **zero** old-name matches.
- `05_paper/latex-build/**`: **zero** old-name matches.
- Historic old-name strings remain only as narrative prose (the rename description in
  `06_review/RESPONSE-LETTER-R3.md` L153–154 and round-1 reviewer prompts under
  `06_review/reviews/round1-c1/`). These are not placeholders or build references and
  were left untouched.

## 2. Final gates — re-run after cleanup, exact outputs

### `python 05_paper/build_draft.py` (rc=0)

```
wrote 05_paper/draft/paper.md from 7 tables (T1_prior_work, T2_audit, T3_per_rung, T4_hypotheses, T5_arms, T6_frozen_vs_corrected, T7_ablations_corrected); 61620 bytes; sha256 d81cc90ffe60
```

Draft sha256 before and after the rebuild was identical
(`d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500`) — the rebuild was
byte-for-byte reproducible and removed no other lane's content.

### `python tools/check_numbers.py --draft 05_paper/draft/paper.md` (rc=0)

```
509 number(s) in 1 file(s): 322 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
```

### `python tools/check_all.py` (rc=0, 600s timeout)

```
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 4 step(s), timeout 600s per step

.. tools-tests: python -m pytest tools/tests -q
   -> PASS in 34.0s
.. harness-tests: python -m pytest 04_experiments/harness/tests -q
   -> PASS in 30.3s
.. paper-tests: python -m pytest 05_paper/template/tests -q
   -> PASS in 7.4s
.. toy-pipeline: python 04_experiments/toy/run_pipeline.py
   -> PASS in 11.5s

step           command                                           exit  duration  result
---------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   0     34.0s     PASS
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     30.3s     PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     7.4s     PASS
toy-pipeline   python 04_experiments/toy/run_pipeline.py         0     11.5s     PASS
---------------------------------------------------------------------------------------
4/4 steps passed
```

**All three gates PASS.**

## 3. Response-letter canonical ID inventory

Parsed `06_review/RESPONSE-LETTER-R3.md` with a regex over `##`/`###` item headings
(round 2 uses `## MF-n`, round 3 uses `### R3-MF-n`) and the single `Verdict:` line in
each item block. Parser: `parse_letter.py` in this profile's scratch dir.

```
round-2 MF: count=44 expected=44 range=1..44
  duplicates=[] missing=[] extra=[]
  EXACT_MATCH=True
round-3 R3-MF: count=41 expected=41 range=1..41
  duplicates=[] missing=[] extra=[]
  EXACT_MATCH=True
total canonical headers=85 unique=85
verdict tally: {'partial': 46, 'resolved': 28, 'deferred': 11}
sum: 85
TALLY_MATCH= True
  deferred: got 11, expected 11
  partial: got 46, expected 46
  resolved: got 28, expected 28
```

Conclusion: canonical IDs are exactly round-2 `MF-1..MF-44` and round-3
`R3-MF-1..R3-MF-41`, 85 distinct IDs, no gaps, no duplicates, no extras. Verdict tally
is exactly **28 resolved / 46 partial / 11 deferred = 85**, matching the letter's own
header line. Every item block has exactly one `Verdict:` line (no warnings).

## 4. `git status --short` — latex-build untouched by this lane

`git status --short -- 05_paper/latex-build/` returns **0 entries** (all files there are
tracked and clean); no `M`, `A`, `D`, or `??` entry appeared under that path at any point
in this lane. Its newest file mtimes predate this lane's start (latest `body.tex` at
22:23:39 on 2026-11-18, versus lane work at 23:05+). **Confirmed: nothing under
`05_paper/latex-build/**` was modified by this lane.**

Full `git status --short` after the lane (23:13 IST, condensed to tracked changes):

```
 M 04_experiments/RESULTS-INDEX.json
 M 04_experiments/results/summary_toy.json
 M 04_experiments/src/make_paper_assets.py
 M 04_experiments/toy/toy_runs.json
 M 05_paper/draft/paper.md
 D 05_paper/tables/generated/T1_per_rung.md
 D 05_paper/tables/generated/T1_per_rung.tex
 D 05_paper/tables/generated/T2_hypotheses.md
 D 05_paper/tables/generated/T2_hypotheses.tex
 D 05_paper/tables/generated/T3_audit.md
 D 05_paper/tables/generated/T3_audit.tex
 D 05_paper/tables/generated/T4_frozen_vs_corrected.md
 D 05_paper/tables/generated/T6_ablations_corrected.md
 D 05_paper/tables/generated/T7_prior_work.md
 M 05_paper/template/draft_template.md
 M 06_review/RESPONSE-LETTER-R3.md
 M 06_review/audits/numbers-audit.md
 M orchestration/HEAD-REVIEW.md
 M sessions/R3-7c-latex-citations/STATUS.txt
```

The nine `D` lines are the intended stale-table deletions — the only tracked changes
attributable to this lane. All other `M` entries pre-existed the lane. Untracked
entries are unchanged except for new `04_experiments/runs/20261118T1741*_toy_*` directories
produced by the mandated `check_all.py` toy-pipeline gate. Gate side effects also include
`06_review/audits/numbers-audit.md` (rewritten by the mandated `check_numbers.py` run) and
`05_paper/draft/paper.md` (rewritten byte-identically by the mandated `build_draft.py` run).

## 5. Files created / modified by this lane

- Deleted: the nine stale generated-table files listed in §1 only.
- Created: `sessions/R3-4d-verify-fold/reports/final-inventory.md` (this report).
- No edits to template, generator, letter, `VERIFY-RESOLVED.md`, or `05_paper/latex-build/**`.
