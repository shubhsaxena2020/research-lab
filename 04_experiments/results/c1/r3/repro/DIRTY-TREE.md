# DIRTY-TREE reconstruction — frozen C1 gate run

## Frozen run identity

- Run id: `20261103T022140Z_c1_gate_4cd9275`
- `meta.json`: `git_commit = "4cd9275"`, `git_dirty = true`
- Started: `2026-11-03T02:21:40Z`; finished: `2026-11-03T02:21:49Z`; duration `8.9096 s`
- Command: `python.exe 04_experiments/src/run_c1.py --check-repro 1`
- Config: `c1_gate`, seed `20261103`, `toy = false`
- Host/platform: `DESKTOP-4INP19J`, `Windows-10-10.0.26300-SP0`, Python `3.11.15`

## Base commit

- Commit: `4cd9275` (`4cd92756e6b9a9257aa0f4fa030cfa800b291cf9`)
- Commit timestamp: `2026-11-03T07:47:22+05:30`
- Commit message: `Final wind-down files`
- Current HEAD at reconstruction time: `76c6796` (`Round 3 setup: head checkpoint 5, ...`)
- The frozen run started about 4 minutes after the base commit (`07:51:40+05:30`).

## What `git_dirty = true` means here

`harness/runner.py:git_dirty()` runs `git status --porcelain` and records whether it is non-empty.
`.gitignore` ignores only `logs/`, `*.log`, `__pycache__/`, `.venv/`, and `ops/.nilabh_env`.
It does **not** ignore `04_experiments/runs/`, `04_experiments/results/`, data, or source files.
Run folders and results are tracked (`git ls-files` includes them), so a run creates tracked-path
additions/modifications and is dirty by construction.

## Likely dirty sources

Exact dirty patch is **not stored** by the frozen harness (MF-37). The reconstruction below is
bounded by evidence; it is not a complete file inventory.

1. **Generated run artifacts for this run** (certain to exist):
   - `04_experiments/runs/20261103T022140Z_c1_gate_4cd9275/{config,meta,results}.json`
   - `04_experiments/runs/20261103T022140Z_c1_gate_4cd9275/{stdout,stderr}.log`
   - `04_experiments/runs/20261103T022140Z_c1_gate_4cd9275/artifacts/`
   - These are untracked additions under a tracked parent and are sufficient by themselves to make
     `git status --porcelain` non-empty.
2. **Results-side outputs written by `run_c1.py`** (per its docstring and code):
   - `04_experiments/results/c1/audit.json`
   - `04_experiments/results/c1/predictions.csv`
   - `04_experiments/results/c1/results_full.json`
   - possibly `04_experiments/RESULTS-INDEX.json` (tracked; mtime `2026-11-03 07:49:05+05:30`,
     just before the run)
3. **Candidate uncommitted source/paper edits in the 4-minute commit-to-run window** (not provable):
   The later commit `1926b73` (`S3b leftovers...`, 2026-11-06) shows files that may have existed as
   uncommitted edits on 2026-11-03, including `04_experiments/src/make_claims_audit.py`,
   `04_experiments/src/make_paper_assets.py`, paper/template/review files, `ops/*.ps1`, and session
   `TASK.md` files. Their presence in the later commit is evidence of candidacy only, not proof that
   they were dirty during the frozen run.

## Code that produced the headline numbers

The headline metrics in `results.json` (for example `B2_dense_top1.pooled_precision = 0.7458`,
`band.auroc.r1 = 0.9995`, `band.over_refusal = 0.755`) were produced by the committed base code at
`4cd9275`, specifically:

- `04_experiments/src/run_c1.py`
- `04_experiments/src/features.py` (blob `6ebde4545ecc9a6d9d48798cdadb8e059fb8984e`)
- harness modules `audit.py`, `gate.py`, `runner.py`

The dense feature is **degenerate** in that committed `features.py`:

```python
present_text = [it["context"] for it in sitems]          # line 100
Pq = dense.encode(present_text, ...)                      # lines 101-103
...
d_order = np.argsort(-P @ Pq[k], kind="stable")          # line 132
cos = P @ Pq[k]                                          # line 133
```

`Pq` is the embedding of the **presented passage**, not the question. Therefore the presented passage
is compared with itself: `dense_presented == dense_top1` on all 3752 rows of
`04_experiments/data/features.csv`, and `dense_rank_log` is effectively rank 1. This makes the B2
baseline (`single threshold on dense_top1`) degenerate and collinear with `dense_presented`.

Evidence from the frozen data:

- `features.csv`: 3752 rows; `dense_presented == dense_top1` on all 3752 rows.
- Run result: `B2_dense_top1.pooled_precision = 0.7458` with `B1_bm25_top1.pooled_precision = 0.0169`.
- `features_meta.json`: `csv_sha256 = f9de87f699da1e73968dde27c5a55600c23c077ff9e5a446823e05abe0733cbb`.
- The committed `features.py` blob is identical in the worktree and in `HEAD`
  (`6ebde4545ecc9a6d9d48798cdadb8e059fb8984e`), so the degenerate code is part of the recorded commit,
  not an uncommitted edit.

Contrast with the later sensitivity analysis:

- `04_experiments/src/features_corrected.py` states that §4 specifies a question--passage cosine and
  that the frozen implementation instead encodes the presented passage.
- Its corrected output records `dense_query = "question"` and
  `frac_dense_presented_eq_dense_top1 = 0.1599`, versus `1.0` in the frozen data.

## File mtimes relevant to the reconstruction

- `04_experiments/src/features.py`: `2026-11-03 04:05:37+05:30`
- `04_experiments/data/features.csv`: `2026-11-03 04:32:22+05:30`
- `04_experiments/data/features_meta.json`: `2026-11-03 04:32:23+05:30`
- `04_experiments/RESULTS-INDEX.json`: `2026-11-03 07:49:05+05:30`
- Frozen run `meta.json`/`results.json`: `2026-11-03 07:51:49+05:30`
- Base commit `4cd9275`: `2026-11-03 07:47:22+05:30`

## Reconstruction steps

1. Read `04_experiments/runs/20261103T022140Z_c1_gate_4cd9275/meta.json` for commit, dirty flag,
   command, timestamps, and environment.
2. Confirm the base commit exists with `git rev-parse` / `git show 4cd9275`.
3. Use `git diff --stat 4cd9275 HEAD` only as a candidate list for later committed changes; it is not
   the frozen dirty patch.
4. Check `.gitignore` and `git ls-files` to establish that run folders/results are tracked and not ignored.
5. Inspect the run folder contents and `config.json`/`results.json`.
6. Inspect `features.py` at `4cd9275` and compare its blob to `HEAD` and the worktree.
7. Verify `features.csv` degeneracy counts and `features_meta.json` hash.
8. Compare with `features_corrected.py` to identify the intended question-as-query feature.

## Limits

- The harness stored only a boolean `git_dirty`, not `git status --porcelain`, a diff, or source hashes.
  No exact dirty patch can be reconstructed after the fact.
- The candidate uncommitted edits in the 4-minute window cannot be dated to the frozen run; they are
  inferred from later commits only.
- The run's generated artifacts are identifiable, but their exact contents at run time are what remains
  on disk; no independent snapshot of the dirty overlay exists.
- Therefore the recorded commit does not, by itself, identify the full executed code state. It does
  identify the degenerate dense-query implementation, because that code is present in the committed
  `features.py` and the feature CSV hash matches the committed implementation.
