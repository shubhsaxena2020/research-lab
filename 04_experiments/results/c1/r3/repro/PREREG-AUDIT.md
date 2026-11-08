# PREREG-AUDIT — C1 pre-registration integrity (lane R3-2)

Scope: `04_experiments/PREREGISTRATION.md` + `04_experiments/PREREGISTRATION.sha256`, timestamps and verdicts.
No history edited: earlier sections §1–§8 and D1–D4 are untouched; D5 and D6 are appended at the end (see below).

## 1. Hash chain (current)

File: `04_experiments/PREREGISTRATION.sha256`

| line | label | hash (short) | recorded |
|---|---|---|---|
| 1 | frozen, no deviations | 0a85a6b1… | freeze 2026-11-03T03:59+05:30 |
| 2 | amended, D1 appended | db6c9781… | (D1 dated 2026-11-03T05:27+05:30) |
| 3 | amended, D2+D3 appended | c24a9e51… | commit b2d3055, 2026-11-03 07:47:05 +0530 |
| 4 | amended, D4 appended | 0b577228… | commit b2d3055, 2026-11-03 07:47:05 +0530 |
| 5 | amended, D5+D6 appended | 83d5b31f… | 2026-11-08 (this lane) |

Verification: `sha256sum 04_experiments/PREREGISTRATION.md` = `83d5b31fe4f2eea66d8b39e269f2dc1a79a3b0be4a7420f95abea0f6de291ea0`, equal to line 5. Lines 3–4 were both added in the same commit b2d3055 (07:47:05 +0530), after their section timestamps (D2/D3 05:58, D4 07:05).

## 2. D4 timing audit (MF-4 / MF-32)

- D4 section date in file: `2026-11-03T07:05+05:30`.
- Corrected run outputs (`results/c1_corrected/`) mtimes: 2026-11-03 06:54:23 IST (audit.json 06:54:22.94; predictions.csv 06:54:22.94; results_full.json 06:54; run_return.json 06:54; SUMMARY.md 06:54).
- Therefore D4 was recorded 11 minutes after the corrected run already existed.
- D4 hash line entered the chain in commit b2d3055 at 07:47:05 +0530 (~42 min after the D4 timestamp; ~53 min after the corrected run).
- Frozen run (`results/c1`, commit 4cd9275) started 2026-11-03T02:21:40Z = 07:51:40 IST, i.e. after both the corrected run and D4.

Verdict: D4 is a post-hoc disclosure, not a strictly pre-registered deviation. It does not change a pre-registered verdict (it is labelled exploratory, `c1_corrected`/`D4`), and the non-dense columns are byte-identical to the frozen CSV (spec_check.json). Appended D5 (2026-11-08) records this plainly.

## 3. Overlap-augmented audit (MF-24)

Numbers: `auroc_with_lex_overlap` = 0.9773 / 0.8886 / 0.9232 (dev rungs 1–3); test 0.9804 / 0.8644 / 0.9053. They appear in D2's motivation and in `audit.json`, but §4 lists `lex_overlap` as a gate feature and §8's stopping rule (§8a/§8b) is defined on the six primary surface features only (`n_chars, n_tokens, digit_ratio, upper_ratio, punct_ratio, mean_word_len`). `audit.py` labels the `with_lex` variant a sensitivity analysis; it was never a pre-registered procedure and cannot trigger a rebuild or a stop.

First-run evidence:
- First on-disk run containing these numbers: `20261102T235524Z_c1_gate_e20bc7f`, started 2026-11-02T23:55:24Z = 2026-11-03 05:25:24 IST (commit e20bc7f, git_dirty true). D2 was written at 2026-11-03T05:58+05:30, after that run.
- Earliest `results/.../audit.json` mtime: 2026-11-03 06:54:23 IST (`results/c1_corrected/audit.json`); `results/c1/audit.json` 07:51:48 IST.
- All rungs pass the primary-6 audit (AUROC <= 0.75) on both splits; no rebuild triggered by either variant.

Verdict: the overlap-augmented audit is an exploratory post-hoc sensitivity analysis, reported descriptively only. Appended D6 (2026-11-08) declares this in the deviation log.

## 4. Other integrity notes (context, not changed here)

- `run_c1.py` sets `preregistration_sha256` to the first whitespace token of `PREREGISTRATION.sha256`, i.e. `#` (MF-31). Reconstructed current-at-run-start hash for the frozen run: 0b577228ab234f5df9dc0d08da66b5b4a0ff5c3d563e6e487e0aa0d3b68c53f6 (D4 line), which was the tip of the chain at 2026-11-03 07:47:05 +0530 — after the frozen run started (07:51? note: frozen run started 07:51:40 IST, which is after the chain tip at 07:47, so the frozen run actually started after D4 was already in the chain). Wait: frozen run started 07:51:40 IST, chain tip (D4) at 07:47:05 IST, so at frozen-run start the chain tip was 0b577228… . Good.
- Frozen run came from a dirty tree (git_dirty true, commit 4cd9275); provenance reconstruction is in `DIRTY-TREE.md` (separate deliverable).

## 5. Append performed

- Added `### D5` and `### D6` to the end of `PREREGISTRATION.md` (append-only; earlier text untouched).
- Appended hash line to `PREREGISTRATION.sha256`: `83d5b31fe4f2eea66d8b39e269f2dc1a79a3b0be4a7420f95abea0f6de291ea0`.
- Verified: on-disk SHA-256 of `PREREGISTRATION.md` equals the appended line.