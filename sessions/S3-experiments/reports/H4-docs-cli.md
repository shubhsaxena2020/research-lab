# H4 — documentation / CLI drift tests

**Status: DONE. One new file, 56 tests, 54 pass, 2 fail — and both failures are real
discrepancies in the documentation, not bugs in the test.** Nothing else in the repo was
written; the two failures are left red on purpose so the lead can choose which side to change
(§4, D1 and D2).

Built 2026-11-03 ~03:00–03:10 IST by subagent H4. Every command and output below was executed
on this machine and copy-pasted; nothing is reconstructed.

---

## 1. Files

| Path | Status | Lines |
|---|---|---:|
| `tools/tests/test_docs_and_cli.py` | **created (only file touched)** | 654 |

No tool, doc, fixture or existing test was modified. The two files under
`tools/tests/test_verify_citations_adversarial.py` / `tools/check_all.py` that appear in the
tree are other workers' work, not mine (§5).

## 2. What the file checks

Six rule groups, one test function (or one parametrised test) each, so a failure names the rule
that broke:

| # | Rule | Test(s) |
|---|---|---|
| 1 | every tool answers `--help`, exit 0, ≥5 non-empty lines naming itself or an `--option` | `test_tool_help_exits_zero[<15 tools>]`, plus `test_every_discovered_script_is_classified`, `test_library_allowlist_is_truthful` |
| 2 | bad usage exits 2 (CONTRACTS §6): missing required argument, and unknown flag | `test_exit_2_when_required_argument_missing[<11>]`, `test_exit_2_on_unknown_flag[<15>]` |
| 3 | every backticked repo path in `tools/README.md` + `tools/CONTRACTS.md` exists; every README table tool exists | `test_documented_paths_exist[2 docs]`, `test_allowlisted_absences_still_documented`, `test_readme_tool_table_entries_exist`, `test_readme_json_flag_claim` |
| 4 | CONTRACTS §1–§5 paths exist; §2 `results.json` example keys appear in a real run | `test_contracts_section_paths_exist`, `test_contracts_s2_results_json_keys_are_real`, `test_contracts_s1_verified_citations_columns` |
| 5 | toy banner on `toy/README.md` line 1; `"toy": true` in every toy/results JSON; no toy number in the paper tree | `test_toy_readme_starts_with_banner`, `test_toy_json_artefacts_carry_toy_true`, `test_paper_tree_has_no_toy_result_numbers` |
| 6 | Phase-2 gate is not self-releasing (`TOPIC APPROVED` as a whole line only) | `test_phase2_gate_is_not_self_releasing`, `test_approval_detector_rejects_a_mention` |

**Discovery by globbing, not hard-coding.** 18 scripts are found in six directories
(`tools`, `04_experiments/harness`, `04_experiments/toy`, `05_paper/template/{figures,tables,tools}`,
shallow `*.py` so `tools/lib`, `harness/tests`, `template/tests` are excluded). 15 are CLIs; 3 are
allowlisted libraries:

```
04_experiments/harness/stats.py     library: bootstrap CIs / paired tests; __main__ prints a sample
04_experiments/harness/tables.py    library: table builder; __main__ takes a summary path, not argparse
04_experiments/toy/task.py          library: toy fixture generator, imported by run_toy.py
```

Two guard tests keep the allowlists honest: `test_every_discovered_script_is_classified` fails if a
new script is neither in `CLI_SPEC` nor a library (this is how `tools/check_all.py`, added by a
parallel worker at 02:59, was picked up and covered without an edit); `test_library_allowlist_is_truthful`
asserts the three libraries still do **not** import `argparse`, so a library that grows a CLI
cannot keep its exemption.

**The Phase-2 trap.** `orchestration/HEAD-REVIEW.md:10` contains the string `TOPIC APPROVED`
inside a sentence and inside backticks:

```
- Topic decision is the head's. S2 delivers SELECTED.md + NOVELTY-CHECK.md; the head reads them,
  then writes `TOPIC APPROVED` (or a veto) here.
```

A `"TOPIC APPROVED" in text` check would read that as approval and unblock experiments. The test
compares `line.strip() == "TOPIC APPROVED"` instead, and `test_approval_detector_rejects_a_mention`
proves the detector: sentence mention → False, `pre-TOPIC APPROVED-post` → False, bare line and
`"TOPIC APPROVED\r\n"` → True. The gate is closed today (`03_topics/` is empty, `_gate_open()` False)
and the same test still passes if the head later lands `SELECTED.md` **and** a bare approval line.

## 3. Commands and real output

```
$ time python -m pytest tools/tests/test_docs_and_cli.py -q
FAILED tools/tests/test_docs_and_cli.py::test_readme_json_flag_claim - Assert...
FAILED tools/tests/test_docs_and_cli.py::test_contracts_s1_verified_citations_columns
2 failed, 54 passed in 7.92s
real    0m8.1s
```

Fast, offline, nothing executed beyond `--help` and argument-parse errors: no network, no toy
pipeline, no compilation, no LaTeX, no matplotlib. Slowest test 0.32 s
(`test_tool_help_exits_zero[tools/verify_citations.py]`). `python -m pytest tools/tests
--collect-only -q` → `307 tests collected`, no import/collection clash with the existing suite.

Evidence for the two failures:

```
$ python 05_paper/template/tools/citations_to_bib.py --csv 02_literature/verified_citations.csv \
      --out "$TMPDIR/h4-evidence/test.bib"
citations_to_bib: error: 02_literature\verified_citations.csv lacks required column(s): key
$ echo $?
2

$ python 05_paper/template/tools/citations_to_bib.py \
      --csv 02_literature/verified_citations.s1-legacy.csv --out "$TMPDIR/h4-evidence/legacy.bib"
citations_to_bib: read 5 rows, wrote 5 entries to \tmp\h4-evidence\legacy.bib   # exit 0

# what claims_audit.py builds from the same file (claims_audit.py:519 logic)
rows: 266 map size: 1 keys sample: ['']
lookup 'vaswani2017' -> None
any VERIFIED -> False

$ python tools/simulate_review.py --help | grep -- --json     # no output
```

## 4. Discrepancies found

### D1 — FAILING TEST. `02_literature/verified_citations.csv` does not have the CONTRACTS §1 columns

* Doc: `tools/CONTRACTS.md:29` "Output `02_literature/verified_citations.csv` — ONLY rows with
  status `VERIFIED`:" and `tools/CONTRACTS.md:32`
  `key,title,authors,year,doi,arxiv_id,venue,status,source,source_url,retrieved_at,evidence`.
* Disk: `02_literature/verified_citations.csv:1`
  `id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command`.
  Absent from disk: `key, doi, arxiv_id, status, source, source_url, retrieved_at, evidence`.
  Undocumented on disk: `id, url, doi_or_arxiv, retrieved_on, verified_by_command`.
* Cause: the file is written by a **different, same-named tool** —
  `02_literature/tools/verify_citations.py add` (`CSV_FIELDS`, line 50) — which appends to the
  contract path in its own 9-column shape. `tools/verify_citations.py` writes the contract shape
  (`VERIFIED_FIELDS`, line 672) and would overwrite it. The contract shape survives only in
  `02_literature/verified_citations.s1-legacy.csv`.
* Consequence, measured: `citations_to_bib.py` exits 2 on the live file (quote above);
  `claims_audit.py` collapses all 266 rows onto the empty key, so **no citation can ever read as
  `VERIFIED`** — the citation gate is currently unusable in the fail-closed direction.
* One-line fix, doc side: change §1 to the 9-column schema **and** update `citations_to_bib.py`
  (`status`→`verified_by_command`) and `claims_audit.py:519` (`key`→`id`).
* One-line fix, data side: regenerate the file in the contract shape
  (`python tools/verify_citations.py --csv <input.csv> --online`) and move S2's appends to
  `02_literature/staging/`.

### D2 — FAILING TEST. README claims `--json` on every tool; `simulate_review.py` has none

* Doc: `tools/README.md:5` "findings / 2 = usage error, and `--json` on all of them."
* Tool: `python tools/simulate_review.py --help` lists only `-h` and `--version`; none of the four
  subcommands (`pack`, `ingest`, `aggregate`, `compare`) defines `--json`; `grep -- "--json"
  tools/simulate_review.py` → no match.
* One-line fix, doc side: "...and `--json` on the five report-emitting tools (`simulate_review.py`
  writes YAML/Markdown instead)."
* One-line fix, tool side: add `--json` to the four subparsers.

### D3 — allowlisted. `02_literature/citations.csv` is documented as an input and does not exist

`tools/README.md:13` runs `--csv 02_literature/citations.csv`; `CONTRACTS.md:9` names it the input.
It does not exist anywhere in the repo, so the documented command exits 2 today
(`error: no such file: ...\02_literature\citations.csv`). S2 stages citations under
`02_literature/staging/*.csv` instead. Not asserted (it is an author input, not a tool output) —
recorded in `AUTHOR_INPUT_ALLOWLIST` with that reason.
Fix: commit the input CSV at the contract path, or write the README run column as
`--csv <your citations.csv>` and point §1 at `02_literature/staging/`.

### D4 — allowlisted. `06_review/CLAIMS-AUDIT.md` does not exist

`tools/README.md:15` example. Only `06_review/CLAIMS-AUDIT-TEMPLATE.md` exists.
Fix: copy the template to `CLAIMS-AUDIT.md` when the first draft exists, or use the template path
in the example.

### D5 — allowlisted. `05_paper/draft/method.md` does not exist

`tools/README.md:18` example; `05_paper/draft/` does not exist at all (only `05_paper/template/`).
Expected while Phase 2 is locked. Fix: none needed now; the allowlist entry should be deleted when
drafting starts (the staleness test only checks the path is still *mentioned*, so it will not
silently persist).

### D6 — judgement call. `04_experiments/harness/tables.py --help` exits 1 with a traceback

```
$ python 04_experiments/harness/tables.py --help
Traceback (most recent call last):
  File "...\04_experiments\harness\tables.py", line 687, in <module>
    print(ablation_table(sys.argv[1], sys.argv[2:], None)[0])
exit=1
```

`CONTRACTS.md:159` says "Every tool: `python tools/<tool>.py --help` works". `tables.py` has no
argparse — its `__main__` is a manual smoke hook that treats `argv[1]` as a summary path — so I
classified it as a library, not a tool (documented in `LIBRARY_MODULES`). If the lead considers it
a tool, §6 is violated and the fix is to give it a real `argparse` CLI (or delete the `__main__`
hook so `--help` is unambiguous).
* Doc-side alternative: scope §6 to "every script with a CLI" and name `stats.py`/`tables.py` as
  import-only.

### D7 — reported only, not asserted. CONTRACTS §3 says `aggregate` copies run results into `results/`

`CONTRACTS.md:120-121`: "Files under `04_experiments/results/` are the *aggregated* per-experiment
results, copied from `runs/<run_id>/results.json` by the harness (`aggregate` command)."
`aggregate.py` writes exactly one file per experiment — `results/summary_<experiment>.json`
(`summary_path`, line 490) — and copies nothing; all 9 entries in `RESULTS-INDEX.json` point at
`results/summary_toy.json` or `harness/configs/*.json`, never at a `results/<config>.json`. The
`main_baseline.json` in the §3 example is therefore a file nothing produces.
Not asserted because it sits inside a schema example rather than a backticked normative path (see
§5); worth a one-line doc fix: "`results/` holds `summary_<experiment>.json`; per-run results stay
in `runs/<run_id>/results.json`."

## 5. Limitations

* **Static only.** The suite proves the docs match the *interfaces* and the *files on disk*. It
  cannot prove a tool does what its help says, and it never feeds real data to a tool — that is
  what `tools/tests/test_*.py` and `04_experiments/harness/tests/` are for. `--help` and
  `--definitely-not-a-real-flag` are the only invocations, chosen because they cannot write,
  download or run anything.
* **Path parsing sees only single-backtick spans.** Paths inside fenced JSON examples
  (`04_experiments/results/main_baseline.json`, `.../table_main.md`) are deliberately not
  asserted; `<placeholders>` are skipped. This is why D7 is reported rather than tested. Widening
  the parser would make every illustrative name in a schema example a test failure.
* **Allowlists are permission slips.** Two tests limit the damage: an entry must still be mentioned
  in the docs, and library exemptions must still have no `argparse`. But an entry can still be
  *wrong* (e.g. claiming a file is tool-generated when nothing generates it) and only a human
  reading the comment will catch that.
* **`results/` toy rule is phase-aware by design.** Today every JSON under `results/` must carry
  `"toy": true`. Once the gate opens, the rule narrows to toy-named files, because a real
  `summary_<experiment>.json` is legitimate then. The behaviour is in the test docstring; if the
  head approves a topic this test changes meaning, which is intended but worth knowing.
* **Concurrent workers.** `tools/check_all.py` (H3) appeared at 02:59 while I was writing, and
  `tools/tests/test_verify_citations_adversarial.py` at ~03:05; the repo also has ~129 uncommitted
  paths from S1/S2 activity. The glob picked `check_all.py` up automatically. Anything a parallel
  worker changes in the docs or in `verified_citations.csv` will move these results — re-run before
  quoting.
* **Windows specifics:** subprocesses run with the pytest interpreter, `encoding="utf-8",
  errors="replace"`; `\r\n` is tolerated (`line.strip()`), and `\tmp` in the quoted output is the
  MSYS spelling of the scratch dir.
