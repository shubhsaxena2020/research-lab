# H3 — `check_all.py`: one command that proves the toolchain

date: 2026-11-03
status: **DONE, verified by three real runs** (full, `--fast`, timeout demo) on this machine.

## Why

Before this, proving the lab still worked meant remembering eleven things in the right order:

```
python -m pytest tools/tests -q
python -m pytest 04_experiments/harness/tests -q
python -m pytest 05_paper/template/tests -q
python 04_experiments/toy/run_pipeline.py
```

...plus which flags, from which directory, and — if something hung — how long to wait before
believing it. That is the kind of memory that fails at 2am and produces "I thought the tests
passed". Now:

```
sh ops/check.sh
```

## Files (all new; nothing existing was touched)

| Path | What it is |
|---|---|
| `tools/check_all.py` | The runner. 4 steps, one table, honest exit codes. |
| `ops/check.sh` | POSIX `sh` wrapper: `#!/bin/sh`, `set -eu`, cds to the repo root, `exec python tools/check_all.py "$@"`. |
| `tools/tests/test_check_all.py` | 22 tests for `--list`, `--only` validation, `--json`, table formatting, timeout-as-FAIL, missing-suite-as-FAIL, and root resolution from a foreign cwd. |
| `sessions/S3-experiments/reports/H3-check-all.md` | This report. |

`git status --porcelain -- tools ops sessions` shows exactly three new untracked files
(`tools/check_all.py`, `ops/check.sh`, `tools/tests/test_check_all.py`); no existing tool,
test, CONTRACTS.md or RULES.md was modified.

## What it runs

| # | step | command | why it is a step of its own |
|---|---|---|---|
| 1 | `tools-tests` | `python -m pytest tools/tests -q` | all six integrity tools + `lib/` |
| 2 | `harness-tests` | `python -m pytest 04_experiments/harness/tests -q` | runner, lock, stats, tables |
| 3 | `paper-tests` | `python -m pytest 05_paper/template/tests -q` | LaTeX/Markdown template |
| 4 | `toy-pipeline` | `python 04_experiments/toy/run_pipeline.py` | 12 end-to-end guards wiring tools → draft → review → paper |

Each is a separate `subprocess` invocation (`sys.executable`, `cwd=<repo root>`), so a crash
in one cannot poison the next, and each gets a per-step timeout.

## Real output (pasted, not paraphrased)

### `python tools/check_all.py --list` — run from `C:\Users\shubh`, not the repo

```
repo root: C:\Users\shubh\research-lab
 1. tools-tests    python -m pytest tools/tests -q
 2. harness-tests  python -m pytest 04_experiments/harness/tests -q
 3. paper-tests    python -m pytest 05_paper/template/tests -q
 4. toy-pipeline   python 04_experiments/toy/run_pipeline.py  [skipped by --fast]
4 step(s) in order; --fast skips toy-pipeline
```

exit 0. (The `[skipped by --fast]` note is a label on the toy row, not a skip in this run —
`--list` runs nothing at all.)

### `python tools/check_all.py --fast` — the 30-second sanity check

```
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 3 step(s), timeout 600s per step

.. tools-tests: python -m pytest tools/tests -q
   -> PASS in 17.3s
.. harness-tests: python -m pytest 04_experiments/harness/tests -q
   -> PASS in 7.9s
.. paper-tests: python -m pytest 05_paper/template/tests -q
   -> PASS in 4.0s

step           command                                           exit  duration  result
---------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   0     17.3s     PASS
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     7.9s      PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     4.0s      PASS
---------------------------------------------------------------------------------------
3/3 steps passed
```

exit 0.

### `python tools/check_all.py` — the full run, all four steps

```
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 4 step(s), timeout 600s per step

.. tools-tests: python -m pytest tools/tests -q
   -> PASS in 16.1s
.. harness-tests: python -m pytest 04_experiments/harness/tests -q
   -> PASS in 8.5s
.. paper-tests: python -m pytest 05_paper/template/tests -q
   -> PASS in 4.2s
.. toy-pipeline: python 04_experiments/toy/run_pipeline.py
   -> PASS in 4.9s

step           command                                           exit  duration  result
---------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   0     16.1s     PASS
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     8.5s      PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     4.2s      PASS
toy-pipeline   python 04_experiments/toy/run_pipeline.py         0     4.9s      PASS
---------------------------------------------------------------------------------------
4/4 steps passed
```

**exit 0, whole toolchain green in ~34 s.** Tests behind that table: 264 + 72 + 30 = 366
collected at that moment (22 of the 264 are this report's `test_check_all.py`). The toy
pipeline reports its own `12/12 steps behaved as expected` internally; the runner only cares
that it exits 0.

### State at hand-off — the tree moved under this work, and the runner said so

Minutes after that green run, another session began writing in the same working tree
(`tools/tests/test_docs_and_cli.py` appeared at 03:05:59, `test_check_numbers_adversarial.py`
alongside it) and `02_literature/verified_citations.csv` on disk carries S2's 9-column schema
(`id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command`). Re-running
the same command immediately after gave, unedited:

```
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 4 step(s), timeout 600s per step

.. tools-tests: python -m pytest tools/tests -q
   -> FAIL (exit 1) in 23.2s
.. harness-tests: python -m pytest 04_experiments/harness/tests -q
   -> PASS in 7.8s
.. paper-tests: python -m pytest 05_paper/template/tests -q
   -> PASS in 4.0s
.. toy-pipeline: python 04_experiments/toy/run_pipeline.py
   -> PASS in 3.8s

step           command                                           exit  duration  result
----------------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   1     23.2s     FAIL (exit 1)
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     7.8s      PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     4.0s      PASS
toy-pipeline   python 04_experiments/toy/run_pipeline.py         0     3.8s      PASS
----------------------------------------------------------------------------------------------
3/4 steps passed
```

exit 1. The single failure is
`tools/tests/test_docs_and_cli.py::test_contracts_s1_verified_citations_columns`:

```
FAILED tools/tests/test_docs_and_cli.py::test_contracts_s1_verified_citations_columns
1 failed, 297 passed, 8 xfailed in 22.51s
```

That test compares CONTRACTS.md §1 against `02_literature/verified_citations.csv` and finds
the documented 12 columns vs the 9 on disk (`documented but absent: key, doi, arxiv_id,
status, source, source_url, retrieved_at, evidence`). **This is not a `check_all.py` defect
and not caused by anything in this report:** none of the four new files touch that CSV,
that test, or CONTRACTS.md, and the failure reproduces with
`python -m pytest tools/tests/test_docs_and_cli.py::test_contracts_s1_verified_citations_columns`
alone. It is the S2/S3 contract collision the test itself names, and fixing it means either
regenerating the CSV in the §1 schema or amending §1 — a decision for the owner of those
files, both of which this task was told not to modify.

Two useful facts follow from this episode, which is the best evidence available that the
runner is worth having:

- it caught, within one command, a cross-tool regression no test suite owner would notice
  in isolation (each suite's *own* green run says nothing about the other's schema);
- `check_all.py` itself satisfies the new cross-tool CLI contract that the concurrent session
  added — `test_tool_help_exits_zero`, `test_exit_2_on_unknown_flag`,
  `test_exit_2_when_required_argument_missing`, `test_every_discovered_script_is_classified`:
  `42 passed`. The runner is registered there as `required: []`, `base: []` under the
  comment "runs the whole toolchain; never invoke without a flag", which is exactly the
  contract implemented here (no required args; unknown flag → exit 2 before any step runs).

### The timeout path, demonstrated for real — `--only toy-pipeline --timeout 1`

```
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 1 step(s), timeout 1s per step

.. toy-pipeline: python 04_experiments/toy/run_pipeline.py
   -> FAIL (timeout 1s) in 1.0s


failed step output (last 25 lines each):

--- toy-pipeline: FAIL (timeout 1s) ---
(no output captured)

step          command                                    exit  duration  result
------------------------------------------------------------------------------------------
toy-pipeline  python 04_experiments/toy/run_pipeline.py  -     1.0s      FAIL (timeout 1s)
------------------------------------------------------------------------------------------
0/1 steps passed
```

**exit 1.** A step that is killed at 1.0 s of a 5 s job is reported as `FAIL (timeout 1s)`,
`exit` is `-`, and the count line says `0/1 steps passed`. It can never read as a pass.

### `--json` (machine-readable, pure JSON on stdout)

```
python tools/check_all.py --json --only paper-tests
-> passed=1 / total=1  ok=True  steps=['paper-tests']  result='PASS'
```

Shape: `{root, python, generated_at, fast, timeout_s, passed, total, ok, steps:[{step,
command, exit_code, duration_s, result, passed, timed_out, output_tail?}]}`. `output_tail`
appears only on failures. `--json --list` emits the step plan without running anything.

### Usage error — `--only no-such-step`

```
usage: check_all.py [-h] [--fast] [--list] [--only NAME] [--json]
                    [--timeout SECONDS]
check_all.py: error: argument --only: invalid choice: 'no-such-step' (choose from
'tools-tests', 'harness-tests', 'paper-tests', 'toy-pipeline')
```

exit 2. The valid names are in the message, so nobody has to read the source to recover.

## Design decisions that matter

1. **Timeout is a FAIL, not a pass or a skip.** `subprocess.run(timeout=...)` kills the
   child; the result string contains `timeout` so it cannot be confused with a real exit
   code. Default 600 s per step — generous enough for the 80 s suite from STATUS.md, short
   enough that a wedged pytest cannot consume a whole session.
2. **A missing suite/script is a FAIL.** `Step.requires` is checked first: `pytest` on a
   deleted directory would otherwise return exit 4 and, if somebody "fixed" that to be
   tolerated, "no tests found" would read as "all good". Message: `FAIL (missing <path>)`.
3. **Read-only, verified.** The runner writes no report, no log, no cache. It runs pytest
   with `-p no:cacheprovider` and exports `PYTHONDONTWRITEBYTECODE=1`, so checking the tree
   does not dirty the tree. Verified by fingerprinting every `*.pyc`, `CACHEDIR.TAG` and
   `.pytest_cache` entry under `tools/`, `04_experiments/`, `05_paper/` before and after a
   `--fast` run: `diff` = 0 lines. `.pytest_cache` still carries its 00:53 timestamp from
   before this work.
4. **cwd-independent.** `ROOT = Path(__file__).resolve().parents[1]`; every child runs with
   `cwd=ROOT`, and displayed commands are repo-relative. Verified by `--list` from
   `C:\Users\shubh` and from `/tmp`.
5. **Exit codes follow CONTRACTS.md §6**: 0 all pass, 1 any fail, 2 usage. An empty step
   list returns 2 (`no steps run` is not success).
6. **Failure diagnosis, not just marks.** Failing steps print their last 25 lines of
   captured output under the table, so a red run is actionable without a second command.
   Passing runs stay quiet (`pytest -q` output is captured, not echoed).

## Test strategy (the recursion trap)

`check_all.py` runs `pytest tools/tests`; the test file lives in `tools/tests`. Any test
that invoked the runner in run mode would re-collect itself and fork-bomb pytest. So
`tools/tests/test_check_all.py` only calls the runner as a **subprocess** for `--list`,
`--list --json`, and argument-error cases — all of which exit before executing a step — and
tests everything else by calling the functions directly:

| Test class | Proves |
|---|---|
| `TestStepDiscovery` | exactly the 4 required steps, in order; `--fast` drops only the toy; each pytest step targets its own directory; `-q` + `no:cacheprovider` present |
| `TestCliWithoutRunning` | `--list` exits 0 and names all four in order; unknown `--only` exits 2 naming all valid choices; `--only toy-pipeline --fast` exits 2 with "conflict"; `--timeout 0/-5/abc` exits 2; `--list --json` parses and preserves names/indexes; root resolves from `tmp_path` |
| `TestTableFormatting` | five required columns; PASS and FAIL rows distinguishable (and exit code visible); timeout row says FAIL+timeout and not PASS; `41.8s` and `1m35.0s` renderings; final line `4/4 steps passed` |
| `TestRunStepSemantics` | exit 0 → PASS; exit 3 → `FAIL (exit 3)`; a 30 s sleep with `timeout=1` is killed in <20 s, `timed_out=True`, `exit_code=None`, never passed; missing path → `FAIL (missing ...)`; `overall_exit` = 0/1/2 |
| `TestJsonResultShape` | the documented JSON keys, and no `output_tail` on a pass |

22 tests, ~2.7 s — fast enough that the suite it protects is not slowed by its own watchdog.

## Limitations (stated so nobody over-trusts a green run)

- **Green means the plumbing is intact, not that the paper is right.** It proves the tests
  pass and the toy pipeline's 12 guards still behave. `05_paper/draft/` is still empty, so
  no real draft has ever been through the number/citation/claims gates.
- **`--fast` is not the toolchain.** It skips the only end-to-end path (the toy pipeline),
  which is precisely where cross-tool breakage shows up. Use it as a smoke test, not as
  proof.
- **Timeout kills the direct child only.** `subprocess.run` terminates the process it
  started; on Windows a grandchild launched by that process is not guaranteed to die. No
  step launches grandchildren today, but a future step that does could leave an orphan.
- **No per-test detail in the table.** `pytest -q` output is captured to keep the table
  readable; on a failure you see the last 25 lines only. Re-run the single suite or
  `--only <step>` for the full log.
- **Nothing live is checked.** No network: `verify_citations.py --online` is not exercised
  here, so a broken API path would still show a green table. Offline-by-default is the
  contract, not an oversight.
- **Capacity limits** are on timings measured on this machine today (34 s full run); a
  slower disk or first-run import cost can push it up, hence the 600 s default rather than
  a tight one.
- **`--only` is an exact (case-sensitive) name match** (argparse `choices`, so a typo
  exits 2 rather than silently matching something else). It does not accept prefixes.
- **A red `tools-tests` is not automatically your bug.** This tree is shared with other
  sessions working in parallel; the runner reports the state of the tree at the moment it
  ran, and that state can change between two invocations a minute apart (observed: 4/4 →
  3/4 → back to a single failure as another session edited tests). Read the failing test
  name before assuming the change you just made is the cause.
- The runner does not enable `--strict-markers`/`-W error`; test-suite hygiene is the test
  suites' business, not the watchdog's.

## Next session, in one line

`sh ops/check.sh` before you believe anything, and `sh ops/check.sh --fast` while iterating.
If it is green, the eleven commands still work and you can spend the session on the paper.
