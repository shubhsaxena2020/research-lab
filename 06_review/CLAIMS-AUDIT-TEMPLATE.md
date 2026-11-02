# CLAIMS AUDIT — template

**Binding rule (read before writing a single row).**

1. Every claim in the abstract and every claim in the introduction gets **exactly one row**.
   One claim, one row: no row means the claim **cannot ship**.
2. A row whose `verified` is anything other than `YES` **blocks the draft**. Not "warn", not
   "fix later" — the draft does not leave the repo.
3. A row is only `YES` when a reviewer has re-run the command and seen the printed value come
   out of the evidence file named in the same row. `YES` is a signature, not an opinion.
4. Numbers are copied from the evidence file, never retyped from memory. If the number changes,
   the row changes and the reviewer signs again.
5. `state of the art`, `novel`, `first` require a row whose `evidence_file` is
   `02_literature/NOVELTY-CHECK.md` (RULES.md #5). Without one, the sentence is deleted.

`tools/claims_audit.py` mechanically enforces rows 1-5 for the claims it can detect: anything
containing a digit or a comparative word (`outperforms`, `improves`, `reduces`, `increases`,
`novel`, `state-of-the-art`, `first`, plus the stems documented in `--help`). The remaining
claims are qualitative and are enforced by the reviewer reading the table against the draft —
the tool says so rather than pretending to understand prose.

Copy this file to `06_review/CLAIMS-AUDIT.md` for the draft you are auditing (one file per
draft version), keep the table, delete the examples.

```
python tools/claims_audit.py \
    --audit 06_review/CLAIMS-AUDIT.md \
    --draft 05_paper/draft/ \
    --index 04_experiments/RESULTS-INDEX.json \
    --citations 02_literature/verified_citations.csv
```

Exit 0 = every row verifies and coverage is complete. Exit 1 = findings (a row fails, or a
draft claim has no row). Exit 2 = usage error. `--json` prints the same verdict machine-readably.

---

## Columns

| column | required | what goes in it |
|---|---|---|
| `claim_id` | yes | Stable id, `C-01`, `C-02`, ... Rows starting `EX-` are worked examples and are **skipped** by the validator. |
| `claim` | yes | The sentence **verbatim from the draft**, in double quotes. Do not paraphrase: coverage matching is textual. |
| `section` | yes | `Abstract` or `Introduction` (free text is allowed; these two are the audited sections). |
| `evidence_file` | yes | Path from the repo root to the file the number came from, e.g. `04_experiments/results/main_baseline.json`. Must exist. |
| `evidence_key` | yes | Where inside that file: a dotted JSON path (`accuracy`, `_meta.n`, `paired.p_value`), `column=value` for a CSV (`key=vaswani2017`), or a literal phrase for `.md`/`.txt`. |
| `command` | yes | The command that produced the file, runnable from the repo root. Must include the seed/config. |
| `result_value` | yes | The value as it is printed in the draft (`0.812`, `1,000`, `14.2`, `VERIFIED`). A trailing `%` is converted, so `86.5%` matches `0.865`. |
| `verified` | yes | `YES` only after a reviewer re-ran the row. Anything else blocks the draft. |
| `limitation` | recommended | What the number does **not** support: single seed, one dataset, CPU-only timing, small n. This is what stops a claim from overreaching. |
| `reviewer` | recommended | Initials of the person who ran the command. |

Values are compared with tolerance: the `tolerance` on the matching `RESULTS-INDEX.json` entry
is used as a **relative** tolerance; when the index has no entry (or no tolerance) the default
is 1% relative. `0.031` passes against a stored `0.0312`; `0.900` does not pass against `0.865`.

Forbidden in this table: a row with an empty `command`, a row whose `result_value` was copied
from another row, a row pointing at a file that a later run overwrote, and a `YES` written by
the person who wrote the claim without re-running it.

---

## Worked examples (marked EX-, skipped by the validator)

**These are not real claims.** They show how a row is shaped. The validator skips them, so a
template file full of EX- rows reports "0 checked, N examples skipped" instead of judging them.

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| EX-001 | "The baseline reaches 0.812 accuracy on the 1,000-query held-out split." | Abstract | 04_experiments/results/main_baseline.json | accuracy | python 04_experiments/harness/run.py --config configs/baseline.json --seed 0 | 0.812 | YES | single seed for this number; 5-seed spread is a separate row | SS |
| EX-002 | "Our reranker improves accuracy to 0.865 on the same held-out split,
a gain of 5.3 points over the baseline." | Abstract | 04_experiments/results/main_ours.json | accuracy | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 0.865 | YES | gain is computed from EX-001; same split and preprocessing | SS |
| EX-003 | "Across 5 seeds the improvement is stable." | Abstract | 04_experiments/results/summary_main.json | n_seeds | python 04_experiments/harness/aggregate.py --experiment main | 5 | YES | n=5 is small; CI95 is [0.862, 0.868] | SS |
| EX-004 | "The Holm-corrected p-value is 0.031 for the baseline/ours comparison." | Abstract | 04_experiments/results/summary_main.json | paired.p_value | python 04_experiments/harness/aggregate.py --experiment main | 0.031 | YES | family of 3 comparisons, Holm \| not Bonferroni | SS |
| EX-005 | "To our knowledge this is the first audit that binds every abstract claim to a stored result." | Abstract | 02_literature/NOVELTY-CHECK.md | audit claim binding | `grep -in "audit" 02_literature/NOVELTY-CHECK.md` | no prior audit binds every abstract claim | YES | two search queries only; no full-text screening of hits | SS |
| EX-006 | "Prior work reports strong ranking results on standard benchmarks [@vaswani2017]." | Introduction | 02_literature/verified_citations.csv | key=vaswani2017 | python tools/verify_citations.py --csv 02_literature/citations.csv --online | VERIFIED | YES | citation supports the survey claim, not a head-to-head rerun | SS |

Two formatting notes, both exercised above and accepted by the parser: a cell may be **wrapped
over several physical lines** (EX-002 above is continued on its second line; the lines are
joined with a space), and a literal pipe inside a cell must be **escaped** (`\|`, see EX-004) or
placed inside backticks.

---

## Worked example of a claim that fails the audit

A row that looks complete and still fails. The claim is quantitative, the file exists, and the
row carries a value — but that value came from a different run, and the reviewer marked it NO.

```
| C-07 | "Our reranker is 9.8 ms per query, 12% faster than the baseline." | Introduction | 04_experiments/results/main_ours.json | latency_ms | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 9.8 | NO | timing on CPU only | SS |
```

Captured output (`tools/tests/fixtures/claims/audit_value_mismatch.md`, same failure shape):

```
| V2 | "our reranker raises this to 0.865" | main_ours.json :: accuracy | 0.900 | 0.865 | YES | ❌ FAIL |

### Findings

- **ROW_VALUE_MISMATCH** `V2`: stored 0.865 vs printed 0.9: diff 0.035 > tol 0.0004325 — audit_value_mismatch.md:8

**Verdict: BLOCKED** (exit 1)
```

What the reviewer does next, in order: re-run the command; if the file really holds `0.865`,
fix the draft sentence to `0.865` and set `verified` back to `YES` **after** re-running; if the
file holds `0.900`, the draft was right and the evidence file is stale — regenerate it, update
the `RESULTS-INDEX.json` entry, then re-audit. Never edit `result_value` to match the draft.

Second failure mode, no row at all: a draft sentence *"Our reranker improves accuracy by 5.3
points over the baseline."* in the introduction with no matching row produces

```
- **UNCOVERED**: no row covers this introduction claim (number '5'): 'Our reranker improves accuracy by 5.3 points over the baseline.' — 05_paper/draft/paper.md:9
```

Third, the language rule: *"Our reranker is state of the art on the public benchmark."* with no
row pointing at `02_literature/NOVELTY-CHECK.md` produces `NOVELTY_ROW_MISSING` at the exact
`file:line`, and the sentence is deleted or softened to what was measured.

---

## Review procedure

1. Copy this template to `06_review/CLAIMS-AUDIT.md`.
2. For each abstract/introduction sentence, add one row. Quote it verbatim. Split a sentence
   that prints two numbers into two rows — one row binds one number.
3. Run the command in the `command` column yourself. Paste the value you saw. Add the limitation
   you would have to admit if a reviewer asked "on what, how many runs?".
4. `python tools/claims_audit.py ...` — fix every finding, re-run until exit 0.
5. Sign `reviewer` only then. The draft may be shared only when the audit exits 0 **and** a
   second person has spot-checked three rows of their choosing (RULES.md #14).

## Known limits of the mechanical check

- Coverage is textual: a claim reworded instead of quoted will be reported `UNCOVERED` even if a
  row exists. That is deliberate — the binding rule says verbatim.
- Matching threshold is 0.80 (Dice token overlap, or containment when the shorter side has at
  least 5 tokens). Claims sharing boilerplate ("we evaluate ... on ... queries") can score high
  on the wrong row; the reviewer must eyeball each `covered_by`.
- Numbers inside a claim are not individually reconciled: the row binds the sentence, and the
  reviewer confirms every printed number in it. Splitting multi-number sentences keeps this
  honest.
- A row can name a real file with a real key and still describe the wrong experiment. The
  `command`, `limitation` and a second reader are the defence; the tool cannot know intent.
- `.md`/`.txt` evidence is checked by phrase presence only — used for `NOVELTY-CHECK.md` and
  review notes, not for numbers.
