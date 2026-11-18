# R3-3b — Batch 2 ownership / no-frozen-change / no-commit audit

Owner: res-s1. Workdir: `C:/Users/shubh/research-lab`.
Scope of this audit: confirm the R3-3b lane wrote only paths it owns, did not touch frozen paths, and did not advance HEAD.

## Commands run and exact observed output

All commands were run from `C:/Users/shubh/research-lab` (`pwd` -> `/c/Users/shubh/research-lab`), exit code 0.

### CMD1 — `git status --short`

```
 M orchestration/HEAD-REVIEW.md
?? 04_experiments/results/c1/r3/R3-3b/
?? sessions/R3-3b-deferred-analyses/
?? sessions/R3-4e-consistency/
?? sessions/R3/orch/BRIEF-pass5.md
?? sessions/R3/orch/LAST-pass5.txt
?? sessions/R3/orch/REPORT-pass5.md
```

### CMD2 — `git log -1 --format=%H`

```
ea82291ae66fc7bbbbc32d54b3014e7297cb3126
```

### CMD3 — `find 04_experiments/src -maxdepth 1 -name 'r3_r3_3b_*.py' -printf '%p\n'`

```
04_experiments/src/r3_r3_3b_mf10.py
04_experiments/src/r3_r3_3b_mf17.py
04_experiments/src/r3_r3_3b_mf7.py
```

### CMD4 — `find 04_experiments/results/c1/r3/R3-3b -type f -printf '%p\n' | sort`

```
04_experiments/results/c1/r3/R3-3b/MF-10.md
04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json
04_experiments/results/c1/r3/R3-3b/mf10_label_A.csv
04_experiments/results/c1/r3/R3-3b/mf10_label_B.csv
04_experiments/results/c1/r3/R3-3b/mf10_raw_responses.jsonl
04_experiments/results/c1/r3/R3-3b/mf10_resolve.csv
04_experiments/results/c1/r3/R3-3b/mf10_rubric.md
04_experiments/results/c1/r3/R3-3b/MF-17.md
04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json
04_experiments/results/c1/r3/R3-3b/MF-7.md
04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json
```

### CMD5 — `find sessions/R3-3b-deferred-analyses -type f -printf '%p\n' | sort`

```
sessions/R3-3b-deferred-analyses/PROGRESS.md
sessions/R3-3b-deferred-analyses/PROMPT-R3.txt
sessions/R3-3b-deferred-analyses/reports/mf10.md
sessions/R3-3b-deferred-analyses/reports/mf17.md
sessions/R3-3b-deferred-analyses/reports/mf7.md
sessions/R3-3b-deferred-analyses/run.log
sessions/R3-3b-deferred-analyses/STATUS.txt
sessions/R3-3b-deferred-analyses/TASK.md
```

This includes the file this audit itself writes: `sessions/R3-3b-deferred-analyses/reports/batch2-ownership.md`.

### Supporting probes

- `git reflog -8` (top two entries):
  ```
  ea82291 HEAD@{0}: commit: R3-4d: blind verification of resolved claims, MF-14 fixed, wording-only partials folded
  88d6b57 HEAD@{1}: commit: Untrack Tectonic font cache under latex-build and gitignore it
  ```
- `git cat-file -t 88d6b57` -> `commit` (baseline exists in history, one commit behind current HEAD).
- `git ls-files '04_experiments/src/r3_r3_3b_*.py'` -> all three source files are tracked and clean; `git check-ignore` -> none ignored.
- `git log --oneline --diff-filter=A -- '04_experiments/src/r3_r3_3b_*.py'` ->
  `ea82291 R3-4d: blind verification of resolved claims, MF-14 fixed, wording-only partials folded`
- `git status --short -- <all frozen paths>` -> **empty output** (all frozen paths clean).
- Frozen-path existence: `05_paper/template`, `05_paper/draft`, `06_review`, `04_experiments/RESULTS-INDEX.json`, `04_experiments/results/c1/predictions.csv`, `04_experiments/results/c1/transfer.json`, `04_experiments/results/c1/audit.json`, `04_experiments/runs` all EXISTS; `PREREGISTRATION.md` MISSING from the working tree.
- `git diff --stat` -> only `orchestration/HEAD-REVIEW.md | 8 ++++++++` (pre-existing, other lane).
- `grep -rn "CARD COMPLETE" sessions/R3-3b-deferred-analyses`:
  - `PROGRESS.md:35` — inside the `## Next` section as a future action: "close PROGRESS with CARD COMPLETE".
  - `run.log:37` — mirror of the same future-action line.
  - `TASK.md:35` — instruction: "Do not say CARD COMPLETE until all reports and gates are independently checked...".
  No line asserts the card is complete.

## Confirmations

**(a) New source files — CONFIRMED (with provenance note).** The only R3-3b source files present are exactly the three `r3_r3_3b_*.py` files listed by CMD3. No other file under `04_experiments/src` appears as new or modified in `git status --short`. They are tracked (not ignored) and clean. Provenance note: all three were added by commit `ea82291` (see `--diff-filter=A`), whose reflog message attributes it to the R3-4d lane, not to this lane; this lane made no commit.

**(b) New result/report files under the two owned folders — CONFIRMED.** CMD4 lists 11 files, all under `04_experiments/results/c1/r3/R3-3b/`; CMD5 lists the session files, all under `sessions/R3-3b-deferred-analyses/`. No result or report file written by this lane appears outside those two folders. All other untracked entries in CMD1 (`sessions/R3-4e-consistency/`, `sessions/R3/orch/BRIEF-pass5.md`, `sessions/R3/orch/LAST-pass5.txt`, `sessions/R3/orch/REPORT-pass5.md`) belong to other lanes and were not touched here.

**(c) HEAD commit — ANOMALY: expected `88d6b57...`, observed `ea82291ae66fc7bbbbc32d54b3014e7297cb3126`.** HEAD is one commit ahead of the `88d6b57` baseline stated in the task. Reflog shows the intervening commit `ea82291` is an R3-4d lane commit ("R3-4d: blind verification..."). There is no R3-3b commit in the reflog and no commit/push was made by this lane; the HEAD advance is attributable to another lane. Exact observed HEAD: `ea82291ae66fc7bbbbc32d54b3014e7297cb3126`. Baseline `88d6b57` is present in history at `HEAD@{1}`.

**(d) Frozen paths — CONFIRMED untouched.** `git status --short -- <frozen paths>` returned empty: no file under `05_paper/template`, `05_paper/draft`, `06_review`, `04_experiments/RESULTS-INDEX.json`, `04_experiments/results/c1/{predictions.csv,transfer.json,audit.json}`, or `04_experiments/runs` is modified or untracked. `PREREGISTRATION.md` does not exist in the working tree, so it cannot have been written. The only tracked modification in the whole repo is `orchestration/HEAD-REVIEW.md` (+8 lines), a pre-existing other-lane change that this lane did not touch; likewise the other untracked paths in CMD1 belong to other lanes.

**(e) PROGRESS.md — CONFIRMED present, no CARD COMPLETE.** `sessions/R3-3b-deferred-analyses/PROGRESS.md` exists. The string "CARD COMPLETE" occurs only as a future action in its `## Next` section, as a mirror in `run.log`, and as a prohibition in `TASK.md`. No completion marker has been written.

## Anomalies / exceptions to record

1. HEAD is `ea82291ae66fc7bbbbc32d54b3014e7297cb3126`, not the expected `88d6b57...`; the extra commit is R3-4d's, not R3-3b's. No R3-3b commit or push occurred.
2. The three R3-3b source scripts were added in that R3-4d commit (`ea82291`), so they are tracked/clean rather than showing as untracked new files in `git status`.
3. `PREREGISTRATION.md` is absent from the working tree (listed as a frozen path to protect, but not present).
4. Pre-existing other-lane dirty state (`orchestration/HEAD-REVIEW.md`, `sessions/R3-4e-consistency/`, `sessions/R3/orch/*`) is visible in git status and was not modified by this lane.

## Verdict

Ownership holds: every file this lane produced is under `04_experiments/src/r3_r3_3b_*.py`, `04_experiments/results/c1/r3/R3-3b/**`, or `sessions/R3-3b-deferred-analyses/**`. No frozen path was written, no commit or push was made by this lane, and PROGRESS.md has no CARD COMPLETE. The HEAD mismatch is attributable to a different lane's commit and is not a violation by R3-3b.
