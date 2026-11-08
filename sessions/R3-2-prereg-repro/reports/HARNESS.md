# HARNESS — provenance capture fix (R3-2)

## Changes

- `04_experiments/harness/runner.py`:
  - Added helper `git_diff(root)` capturing `git diff HEAD` + `git diff --cached` + untracked file list.
  - Added helper `git_preregistration_sha256(root)` computing SHA-256 of `04_experiments/PREREGISTRATION.md`.
  - `run()` now captures the diff, writes it to `artifacts/git_diff.patch`, `artifacts/git_diff.txt`, `artifacts/git-diff.patch`, `artifacts/git-diff.txt` and top-level copies of the same four names, and records meta keys: `git_diff`, `git_diff_sha256`, `git_diff_path`, `git_untracked`, `preregistration_sha256`, `preregistration_path`.
- Added `04_experiments/harness/tests/test_provenance.py` (3 tests).

## Why the frozen run's `preregistration_sha256` was `#`

`04_experiments/src/run_c1.py` read `(PREREGISTRATION.sha256).read_text().split()[0]`; the sha256 file's first token on each line is `#` (comment), so the recorded value was `#`. The harness now computes the hash directly from `PREREGISTRATION.md` via `git_preregistration_sha256`.

## Test result

Command: `python -m pytest 04_experiments/harness/tests -q`

Result: **75 passed** in 20.42s.
