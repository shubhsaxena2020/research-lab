# STATUS S3-experiments

last_update: 2026-11-03T03:41+05:30
state: **PHASE 1 COMPLETE, HARDENED AND VERIFIED.** PHASE 2 LOCKED — nothing topic-specific run.

## One command now proves the toolchain

    python tools/check_all.py
    -> 4/4 steps passed   (tools-tests 25.7s, harness-tests 8.8s, paper-tests 4.5s,
                           toy-pipeline 4.5s; total ~44s, exit 0)

    python -m pytest tools/tests 04_experiments/harness/tests 05_paper/template/tests -q
    -> 409 passed, 0 xfailed, 0 failed

`ops/check.sh` is the same thing as a shell one-liner for the day supervisor.

## Reality checked from disk after the gateway disconnect

I re-ran everything rather than trusting my own earlier report:

- `pytest` over the three suites -> **409 passed** (was 250 before hardening).
- `python 04_experiments/toy/run_pipeline.py` -> **12/12 steps behaved as expected**.
- `tools/`, `04_experiments/harness/`, `05_paper/template/` listed on disk: all inventory
  present (6 paper tools + 4 lib modules, 5 harness modules, 3 template stubs, 270-row
  citation register, 6 toy runs).

### Phase 2 gate — a `grep` here lies; read the line

`grep "TOPIC APPROVED" orchestration/HEAD-REVIEW.md` returns **one hit and it is not an
approval**. It is line 10, the standing-decisions sentence describing what the head *will*
write ("the head reads them, then writes `TOPIC APPROVED` (or a veto) here"). The file header
still says "Phase 2 (experiments) stays LOCKED. This file does not yet contain the approval
line", and `03_topics/` is empty. **LOCKED.** `tools/tests/test_docs_and_cli.py` now asserts
the gate by exact line match (`line.strip() == "TOPIC APPROVED"`), with a self-test proving a
mention inside a sentence does not count — so this trap cannot be re-entered by accident.

## Delivered S3-1 .. S3-8 (each with the test that proves it)

| Item | Path | Proof |
|---|---|---|
| S3-1 citation verifier | `tools/verify_citations.py`, `tools/lib/*` | 79 tests; live: 5 real papers VERIFIED, fabricated row NOT_FOUND |
| S3-2 number tracer | `tools/check_numbers.py` | 88 tests; clean draft 0 findings, tampered digit -> MISMATCH exit 1 |
| S3-3 paper template | `05_paper/template/` | 30 tests; figures/tables generated from results files only |
| S3-4 experiment harness | `04_experiments/harness/` | 72 tests; exact Wilcoxon/BCa cross-checked against scipy |
| S3-5 peer-review sim | `06_review/PEER-REVIEW-SIM.md`, `tools/simulate_review.py` | 9 tests; round1->round2 `compare` marks a fixed item resolved |
| S3-6 originality + disclosure | `06_review/ORIGINALITY.md`, `tools/originality_check.py` | 27 tests; planted 21-word copy caught |
| S3-7 claims audit | `06_review/CLAIMS-AUDIT-TEMPLATE.md`, `tools/claims_audit.py` | 16 tests; five failure modes each named |
| S3-8 student digest | `tools/make_digest.py` | 11 tests; gaps emitted as `[TO FILL]`, never invented |
| extra | `04_experiments/PROTOCOL-CHECKLIST.md`, `tools/check_all.py`, `ops/check.sh` | 22 tests; 4/4 steps |

## Hardening round (4 add-only subagents, reports in `sessions/S3-experiments/reports/H*.md`)

They were told to add tests only, never touch verified tool code, and to report bugs rather
than fix them. 8 genuine defects came back, each now **fixed by me and guarded by a
permanent (non-xfail) regression test**:

1. **`verified_citations.csv` had two writers and two schemas** — S2's 9-column register
   overwrote S3's 12-column output, so `citations_to_bib.py` exited 2 and `claims_audit.py`
   collapsed all 270 rows onto one empty key (no citation could ever read VERIFIED). Resolved
   by declaring S2's schema canonical, adding `tools/lib/citation_schema.py` as the single
   mapping, and pointing all three consumers at it. **Verified: 270/270 rows -> 270 BibTeX
   entries; 270 keys load as VERIFIED.**
2. **False VERIFIED from title containment** — a survey titled "<real title>? A Survey ..."
   scored 0.95 and verified as the target paper, putting a wrong DOI in the register. The
   subtitle lift is now bounded (<=4 extra words, and none of survey/review/benchmark/
   correction/...). Five targeted cases behave correctly.
3. `0.50%` matched a stored `0.5` (100x error) via the percent-units fallback — the fallback is
   now only available when the stored value cannot be a fraction (`|stored| > 1`).
4. Two stacked `% num:` markers both bound to the first number, so the second marker's claim
   was never compared — binding is now exclusive and order-preserving.
5. `12.3 %` (space before the sign) parsed as `12.3` -> false MISMATCH on correct typography.
6. European `1.234,56` split into `1.234` + `56`, letting the integer part "match" a value
   1000x smaller.
7. Bare equation numbers `(1)` / `(2.1)` were reported UNTRACEABLE although the tool's own
   RULE_DOC promised they were exempt.
8. `parse_crossref` kept only the first *character* of a string title, and raised
   `AttributeError` on a dict `author`, killing a whole batch. Malformed API shapes now fail
   closed (NOT_FOUND, never VERIFIED).

Docs corrected to match reality: CONTRACTS §1 rewritten around the one canonical schema (plus
an addendum §7 recording these lessons), and `tools/README.md`'s "--json on all of them"
claim scoped to the six tools that actually have the flag.

## Response to Codex DIRECTIVES

1. *finish Phase 1 interfaces, bounded unit checks, record commands in STATUS* — done above.
2. *align citation contracts with S2's register, one canonical schema and owner* — done, and
   this is now the single biggest integrity fix of the session (item 1 above). Owner: S2 writes
   the file, S3 reads it via `tools/lib/citation_schema.py` and writes the same columns.
3. *topic-agnostic protocol checklist + paper/review handoff* — `04_experiments/PROTOCOL-CHECKLIST.md`,
   `06_review/PEER-REVIEW-SIM.md`, `06_review/templates/META-REVIEW.md`.
4. *label numbers-audit.md as a fixture audit* — default output is now
   `06_review/audits/numbers-audit.md` and every report opens with a scope line ("NOT a paper
   draft ... a PASS here says the tool works, NOT that any draft passed").
5. *replace the template's AI/data provenance assurance with a TODO* — done in
   `05_paper/template/main.tex`.

## Environment facts (carry forward)

- `pandas`, `matplotlib`, `scikit-learn`, `scipy`, `bibtexparser` are **not** installed.
- OpenAlex and Semantic Scholar answer `429` here (`Retry-After: 15859`); Crossref, arXiv,
  DataCite are healthy. An exhausted host is skipped for the whole run, not retried.
- MSYS does not translate paths for native python: pass `C:/...`, never `/c/...`.
- `git_dirty: true` in every `meta.json` is honest — S1/S2 write in this tree, so **nothing was
  committed**.

## Honest gaps

- No LaTeX installed: no template has ever been compiled; brace/environment checks only.
- `02_literature/sources/` is empty, so the originality gate has not run on a real draft.
- `05_paper/draft/` is empty; the toy draft is the only end-to-end evidence.
- `tools/simulate_review.py` has no `--json` (documented, not claimed).
- `04_experiments/results/` holds only `summary_toy.json`; `aggregate` writes summaries but
  does not copy per-run results there, although CONTRACTS §3 implies it does — noted by the
  docs test, left as a documented discrepancy rather than silently changed.

## Next session, in order

1. Re-read `orchestration/HEAD-REVIEW.md` for a *standalone* `TOPIC APPROVED` line, then turn
   `PROTOCOL-CHECKLIST.md` into `04_experiments/PROTOCOL.md` and freeze its hash.
2. Deposit source PDFs in `02_literature/sources/`, convert with `pdftotext -layout`.
3. Run `python tools/check_all.py` before and after any change; it is 44 seconds.
