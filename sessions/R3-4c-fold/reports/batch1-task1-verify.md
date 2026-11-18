# R3-4c-fold verification — batch1 task1 (rebuild + gates + coverage)

Date: 2026-11-18 (IST). Repo root: `C:/Users/shubh/research-lab`. Python: Hermes venv
`C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe` (3.11.15).
No template or response-letter edits made; no commits, no new experiments, no writes to
`05_paper/latex-build/**`. Only outputs written were the normal ones from the build/check
commands (`05_paper/draft/paper.md`, `06_review/audits/numbers-audit.md`) plus this report.

## 1. Rebuild — draft SHA

Command:
```
python 05_paper/build_draft.py
```
Output (verbatim):
```
wrote 05_paper/draft/paper.md from 7 tables (T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T5_arms, T4_frozen_vs_corrected, T6_ablations_corrected); 59975 bytes; sha256 69e0d0790788
```
Recorded printed draft sha256 (12 hex chars as printed): **`69e0d0790788`**

## 2. Numeric gate — check_numbers

Command:
```
python tools/check_numbers.py --draft 05_paper/draft/paper.md
```
Output (verbatim):
```
503 number(s) in 1 file(s): 318 matched, 185 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
```
Finding count: **0** (target 0 — PASS). Exit code 0.

## 3. Toolchain gate — check_all

Command (shell timeout 590 s; per-step timeout 580 s; terminal foreground timeout raised to 600 s):
```
timeout 590 python tools/check_all.py --timeout 580
```
Result table (verbatim):
```
step           command                                           exit  duration  result
---------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   0     36.4s     PASS
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     2m09.8s   PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     5.7s      PASS
toy-pipeline   python 04_experiments/toy/run_pipeline.py         0     26.7s     PASS
---------------------------------------------------------------------------------------
4/4 steps passed
```
Steps passed: **4/4** (target 4/4 — PASS). Exit code 0.
Note: two earlier attempts used the terminal tool's default 180 s foreground timeout and were
cut off mid-run (exit 124) before the toy-pipeline step completed; the successful run above set
the terminal foreground timeout to 600 s. The internal `timeout 590` never fired.

## 4. Response-letter coverage

Commands:
```
grep -c '^## MF-' 06_review/RESPONSE-LETTER-R3.md
grep -c '^### R3-MF-' 06_review/RESPONSE-LETTER-R3.md
```
Results:
- `^## MF-` count = **44** (target 44 — PASS) → r2_entries = 44
- `^### R3-MF-` count = **41** (target 41 — PASS) → r3_entries = 41

## 5. Round2→round3 comparison content

Commands:
```
grep -c '9194a481c8c0' 06_review/reviews/COMPARE-round2-round3.md
grep -c 'post-review' 06_review/reviews/COMPARE-round2-round3.md
```
Results: `9194a481c8c0` = **2** matches; `post-review` = **1** match. Both present (PASS).
Context lines:
- line 6: "Draft under revision: `05_paper/draft/paper.md` (round-3 draft sha256 `9194a481c8c0`)"
- line 9: "**Timing note (R3-4c-fold).** Round 3 reviewed the *pre-fold* draft (sha256 `9194a481c8c0`). All fold edits made in R3-4c-fold are *post-review*: they do not invalidate the round-3 scores, which remain diagnostics on the pre-fold draft. No new review round was run."

## 6. SHA change vs baseline

Baseline draft sha (before this lane): `3934ce7f56a0`
Current printed draft sha: `69e0d0790788`
Different: **YES** (PASS). Note the round-3 review reference sha `9194a481c8c0` is the separate
pre-fold draft identifier recorded in the comparison, not the current built draft.

## Verdict

All six checks pass: rebuild sha `69e0d0790788` differs from baseline; check_numbers 0 findings;
check_all 4/4 steps passed; response letter has 44 round-2 and 41 round-3 entries; comparison
contains both `9194a481c8c0` and `post-review`. No issues remain from this verification.
