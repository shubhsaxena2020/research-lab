# R3-2 — per-MF answers (MF-4, 24, 30, 31, 32, 33, 37)

Lane: R3-2 (pre-registration & reproducibility). Evidence files:
- `04_experiments/PREREGISTRATION.md` (now 293 lines; D1-D6)
- `04_experiments/PREREGISTRATION.sha256` (5 lines; tip 83d5b31f…)
- `04_experiments/results/c1/r3/repro/PREREG-AUDIT.md`
- `04_experiments/results/c1/r3/repro/DIRTY-TREE.md`
- `04_experiments/requirements-lock.txt` (pip freeze)
- `04_experiments/ENVIRONMENT.md`
- `04_experiments/REPRODUCE.md`
- `04_experiments/harness/runner.py` (git diff + prereg hash capture)

---

## MF-4 — D4 not in pre-registration hash chain / deviation log

Verdict: RESOLVED (with post-hoc disclosure). D4 was present in `PREREGISTRATION.md` (§10 D4, dated 2026-11-03T07:05) and in `.sha256` (line 4, 0b577228…) before round 3, but it was recorded after the corrected run existed (corrected mtimes 06:54 IST). R3-2 appended D5 (2026-11-08) stating this plainly and added a fifth hash line (tip 83d5b31f…). No earlier text edited.

Evidence: `PREREG-AUDIT.md` §D4 timing; `PREREGISTRATION.md` D5; `.sha256` line 5; on-disk sha256 = 83d5b31f… matches.

Proposed draft sentence (§8 / deviation section): "D4 is a post-hoc disclosure, not a strict pre-registered deviation: the corrected dense run's files carry mtimes of 06:54 IST on 2026-11-03, eleven minutes before the D4 section's timestamp (07:05 IST). It changes no verdict."

## MF-24 — overlap-augmented audit (0.977/0.889/0.923) not registered

Verdict: RESOLVED (declared exploratory). The six-features-plus-overlap variant is not a §8 stopping-rule procedure; §8's rule is defined on the six primary surface features only. R3-2 appended D6 (2026-11-08) declaring it an exploratory post-hoc sensitivity, with first-run timestamp (2026-11-03 05:25:24 IST, run 20261102T235524Z). It cannot trigger a rebuild or a stop.

Evidence: `PREREGISTRATION.md` D6; `audit.py` surface_features(with_lex=True); `results/c1/audit.json` auroc_with_lex_overlap.

Proposed draft sentence (§3.4 / §4.1): "The overlap-augmented AUROCs (0.977 / 0.889 / 0.923) are a post-hoc sensitivity of the six-feature audit, not a registered procedure; they do not trigger §8's rebuild rule, which is defined on the primary six features only."

## MF-30 — no requirements lockfile / model revisions

Verdict: RESOLVED. `04_experiments/requirements-lock.txt` written from `python -m pip freeze` (Hermes venv, Python 3.11.15). `04_experiments/ENVIRONMENT.md` records OS/CPU/Python/torch/bm25s and the three Hugging Face revisions from the local cache: BAAI/bge-small-en-v1.5 = 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a; cross-encoder/ms-marco-MiniLM-L-6-v2 = 233902d25c440f23af6f7d6e94d2946bac0bee0a; Qwen/Qwen2.5-0.5B-Instruct = 7ae557604adf67be50417f59c2c2f167def9a775.

Evidence: `requirements-lock.txt`, `ENVIRONMENT.md`, sha256 of lockfile a4982334… (see ENV report).

Proposed draft sentence (§8): "Environment: Python 3.11.15 on Windows 10 (build 26300), Intel64 Family 6 Model 197, 14 cores; torch 2.15.0+cpu, bm25s 0.3.16. Checkpoint revisions: BAAI/bge-small-en-v1.5@5c38ec7…, cross-encoder/ms-marco-MiniLM-L-6-v2@233902d…, Qwen/Qwen2.5-0.5B-Instruct@7ae5576…. Full pinned list: `04_experiments/requirements-lock.txt`."

## MF-31 — frozen run records preregistration_sha256 as '#'

Verdict: RESOLVED (root cause + harness fix + reconstructed link). Bug: `run_c1.py` line 271 read `(PREREGISTRATION.sha256).read_text().split()[0]`, whose first token is the comment marker `#`. Fix in the harness: `runner.git_preregistration_sha256(root)` computes the sha256 of `PREREGISTRATION.md` directly and `run()` stores it in `meta["preregistration_sha256"]` (plus `preregistration_path`). Frozen run did not use the harness's value (it read the file); the value that was in force at run time is 0b577228ab234f5df9dc0d08da66b5b4a0ff5c3d563e6e487e0aa0d3b68c53f6 (D4 line), because the frozen run started 07:51:40 IST, after the b2d3055 commit (07:47:05 IST) that added the D4 hash. Earlier hashes in force before that commit: frozen 0a85a6b1…, D1 db6c9781…, D2+D3 c24a9e51….

Evidence: `run_c1.py:271`; `PREREG-AUDIT.md`; `runs/20261103T022140Z_c1_gate_4cd9275/meta.json` git_commit 4cd9275, git_dirty true, started_at 02:21:40Z.

Proposed draft sentence (§7): "The frozen run's `preregistration_sha256` field reads `#` because `run_c1.py` parsed the first whitespace token of the hash log; the hash in force at run time was 0b577228… (D4). The harness now records the sha256 of `PREREGISTRATION.md` directly."

## MF-32 — deviation log stops at D3 while text says D4

Verdict: RESOLVED. D4 is present (§10 D4, dated 2026-11-03T07:05) and the fourth hash line (0b577228…) exists. D5 (2026-11-08) additionally clarifies that D4 was recorded after the corrected run existed, so "deviation" is retained only with that post-hoc caveat. D6 (2026-11-08) adds the overlap audit disclosure.

Evidence: `PREREGISTRATION.md` tail (D5, D6); `.sha256` 5 lines; tip 83d5b31f….

Proposed draft sentence (§8): "The deviation log now runs D1–D6; D4 and D5 disclose post-hoc timing (corrected run 06:54 IST, D4 07:05 IST); D6 declares the overlap-augmented audit exploratory."

## MF-33 — §8 omits commands for transfer item builder and reader baseline

Verdict: RESOLVED. `04_experiments/REPRODUCE.md` lists the full ordered command sequence, including `python 04_experiments/src/build_transfer_items.py` before `features_transfer.py` and `python 04_experiments/src/reader_logprob.py` before the reader baseline consumption. Heavy experiment commands are marked "not re-run (would overwrite immutable frozen outputs)"; cheap checks (`--help`, pytest) were run and passed.

Evidence: `REPRODUCE.md`; `reports/ENV.md`.

Proposed draft sentence (§4.7 / §4.8): "Transfer items: `build_transfer_items.py` then `features_transfer.py` (400 items, sha256 2ae0ce0c…). Reader baseline: `reader_logprob.py` over 553 dev items (AUROC 0.419)."

## MF-37 — frozen run from dirty tree, no diff stored

Verdict: PARTIALLY RESOLVED (honest reconstruction + future fix). The frozen run (commit 4cd9275, git_dirty true) has no stored diff; `runs/20261103T022140Z_c1_gate_4cd9275/meta.json` records only commit + dirty flag. Reconstruction in `DIRTY-TREE.md`: the run started 07:51:40 IST (after b2d3055 at 07:47:05); `04_experiments/runs/` and `results/` are tracked, so dirty state likely includes generated run artifacts plus any uncommitted src edits; the degenerate dense code (`features.py`, Pq = presented passage) is present in commit 4cd9275 and evidenced by `results/c1` degeneracy (78.70% rows). Exact patch cannot be recovered. Future runs now store the diff via `runner.git_diff()` written to `artifacts/git_diff.patch` (and top-level copies) plus `meta["git_diff"]` / `git_diff_sha256` / `git_untracked`.

Evidence: `DIRTY-TREE.md`; `harness/runner.py`; `tests/test_provenance.py` (3 passed); full harness suite 75 passed.

Proposed draft sentence (§8): "The frozen run (commit 4cd9275) was produced from a dirty working tree with no stored diff; commit plus the degenerate-features evidence identifies the executed code. From round 3 onward every run stores `artifacts/git_diff.patch` and its sha256 in `meta.json`."
