# R3-2 progress (pre-registration & reproducibility)

Batch 1 (4 parallel subagents):
- AUDIT: PREREG-AUDIT.md written; D5 + D6 appended to PREREGISTRATION.md; hash line appended (tip 83d5b31f…). Report: reports/AUDIT.md.
- HARNESS: runner.py now captures git diff (artifacts/git_diff.patch + top-level copies, meta git_diff/git_diff_sha256/git_untracked) and records PREREGISTRATION.md sha256 in meta. Tests: test_provenance.py 3 passed; full harness suite 75 passed. Report: reports/HARNESS.md.
- DIRTY-TREE: DIRTY-TREE.md written (commit 4cd9275, dirty, reconstruction limits). Report: reports/DIRTYTREE.md.
- ENV/REPRO: requirements-lock.txt, ENVIRONMENT.md, REPRODUCE.md written; cheap checks passed. Report: reports/ENV.md.

Deliverables:
- 04_experiments/results/c1/r3/repro/PREREG-AUDIT.md
- 04_experiments/results/c1/r3/repro/DIRTY-TREE.md
- 04_experiments/results/c1/r3/repro/ANSWERS.md
- 04_experiments/PREREGISTRATION.md (D5, D6 appended; append-only)
- 04_experiments/PREREGISTRATION.sha256 (5 lines, tip 83d5b31f…)
- 04_experiments/requirements-lock.txt
- 04_experiments/ENVIRONMENT.md
- 04_experiments/REPRODUCE.md
- 04_experiments/harness/runner.py (provenance capture)
- 04_experiments/harness/tests/test_provenance.py

Verification:
- sha256sum PREREGISTRATION.md == 83d5b31fe4f2eea66d8b39e269f2dc1a79a3b0be4a7420f95abea0f6de291ea0 (matches .sha256 tip)
- python -m pytest 04_experiments/harness/tests -q -> 75 passed
- No frozen result files modified; no git commits.

MF items addressed: 4, 24, 30, 31, 32, 33, 37 (see ANSWERS.md).

CARD COMPLETE
