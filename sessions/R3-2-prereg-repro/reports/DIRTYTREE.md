# R3-2 report: dirty-tree reconstruction (MF-37)

Primary deliverable: `04_experiments/results/c1/r3/repro/DIRTY-TREE.md`.

## Summary

- Frozen run `20261103T022140Z_c1_gate_4cd9275` records `git_commit = "4cd9275"` and `git_dirty = true`.
- The commit is `4cd9275` (`Final wind-down files`, 2026-11-03 07:47:22+05:30); the run started 07:51:40+05:30.
- `git_dirty` is a boolean only; no porcelain output, diff, or source hash was stored, so the exact dirty patch cannot be reconstructed.
- Runs and results are tracked and are not ignored by `.gitignore`, so generated run artifacts alone are sufficient to make the tree dirty.
- Likely dirty sources: the run folder, results/c1 outputs, RESULTS-INDEX.json, and possibly uncommitted source/paper edits in the 4-minute commit-to-run window.
- The headline numbers came from committed `features.py` at `4cd9275`, whose dense query is degenerate: `Pq = dense.encode(present_text)` compares the presented passage with itself, so `dense_presented == dense_top1` on all 3752 rows. Evidence includes run result `B2_dense_top1.pooled_precision = 0.7458` and `features_meta.json` hash `f9de87f6...`.
- `features.py` blob is identical in commit, HEAD, and worktree (`6ebde454...`), so the degeneracy is in the recorded commit rather than an uncommitted edit.

## Limits

No exact dirty diff exists; candidate uncommitted edits are inferred from later commits only. The recorded commit identifies the degenerate dense-query code but not the full executed overlay.
