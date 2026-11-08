# VERIFY-C — independent verification of MF-10 adjudication, ANSWERS.md, frozen-file integrity

**Exploratory / post-hoc.** This verification report is itself exploratory: every
number below is re-derived from the adjudication files in
`04_experiments/results/c1/r3/exp/adjudication/`. None of these outputs changes
any pre-registered verdict. Labellers are LLM agents, not human annotators.

## Verdicts

| Check | Result |
|---|---|
| MF-10: n=100, 25/rung rungs 1–4, seed 20261103 | **PASS** |
| MF-10: label_A 30/100 answerable | **PASS** |
| MF-10: label_B 6/100 answerable | **PASS** |
| MF-10: resolved 5/100 (5%) | **PASS** |
| MF-10: Cohen κ = 0.1975 | **PASS** |
| MF-10: disagreements = 26 | **PASS** |
| MF-10: per-rung shares | **PASS** (see §1; one disclosure inconsistency, §4) |
| pytest `test_r3_exp_adjudicate.py` | **PASS** (10 passed) |
| ANSWERS.md: 8 MFs × (verdict + evidence file/key + command + draft sentence) | **PASS** |
| No frozen files under `04_experiments/results/c1/` (excl. `r3/exp`) modified | **PASS** (see §3) |

## 1. MF-10 numbers — reproduced from files

Independent CSV recount (Python `csv` + `collections`, not the supplied JSON):

- `sample.csv`: 100 rows, rung counts **{1: 25, 2: 25, 3: 25, 4: 25}**, split
  **48 dev / 52 test**, 100 unique item_ids.
- Regeneration check: `r3_exp_adjudicate.sample_negatives` on the real
  `items.jsonl` (`SEED=20261103`, `RUNGS=(1,2,3,4)`, `N_PER_RUNG=25`) reproduces
  `sample.csv` **exactly, in order** (`PASS`, live-data test also asserts this).
- `label_A.csv`: 100 rows, labels {0: 70, 1: **30**} → 30/100 = 0.30. No `ambiguous`.
- `label_B.csv`: 100 rows, labels {0: 94, 1: **6**} → 6/100 = 0.06. No `ambiguous`.
- `resolve.csv`: 100 rows, labels {0: 95, 1: **5**} → 5/100 = 0.05. No `ambiguous`.
- ID sets identical across all four files; `resolve.csv` copies the agreed label
  on all 74 agreements (0 deviations), and resolves all 26 disagreements.
- Contingency from A/B: both 0 = 69, both 1 = 5, A1/B0 = **25**, A0/B1 = **1**.
  One-directional disagreement: A is far more lenient (25 of 26 splits).

### Kappa

```
$ python 04_experiments/src/r3_exp_adjudicate.py --kappa
n_common=100 disagreements=26 kappa=0.197530864197531
  rung 1: n=25 disagreements=0 kappa=1.0
  rung 2: n=25 disagreements=3 kappa=0.3589743589743595
  rung 3: n=25 disagreements=3 kappa=0.3589743589743595
  rung 4: n=25 disagreements=20 kappa=-0.05485232067510545
```

- Reported κ = 0.1975 — **PASS** (exact: 0.19753).
- po = 74/100 = 0.74; pe = 0.30×0.06 + 0.70×0.94 = 0.676 — matches
  `adjudication.json` (`po 0.74`, `pe 0.676`, `kappa 0.1975`, `n_agree 74`).
- Disagreements = **26** — **PASS**.

### Per-rung shares (recounted from CSVs vs `adjudication.json`)

| Rung | n | A | B | resolved |
|---|---|---|---|---|
| 1 | 25 | 0/25 = 0.0 | 0/25 = 0.0 | 0/25 = 0.0 |
| 2 | 25 | 4/25 = 0.16 | 1/25 = 0.04 | 1/25 = 0.04 |
| 3 | 25 | 4/25 = 0.16 | 1/25 = 0.04 | 1/25 = 0.04 |
| 4 | 25 | 22/25 = 0.88 | 4/25 = 0.16 | 3/25 = 0.12 |

All match `adjudication.json` `per_rung_answerable_shares` exactly — **PASS**.
Resolver outcomes on the 26 disagreements: 0 → `1`, 26 → `0` (by rung 2:3, 3:3,
4:20) — matches `resolver_outcomes_on_disagreements`.

```
$ python -m pytest 04_experiments/src/tests/test_r3_exp_adjudicate.py -q
..........   [100%]
10 passed in 0.30s
```

## 2. ANSWERS.md completeness (8 MFs)

File: `04_experiments/results/c1/r3/exp/ANSWERS.md`. Programmatic check that
every `## MF-<n>` section contains all four required fields:

| MF | Present | Verdict | Evidence file/key | Command | Draft sentence |
|---|---|---|---|---|---|
| MF-3 | yes | yes | yes (`both_runs.json`) | yes | yes |
| MF-6 | yes | yes | yes (`h2_verdict.json`) | yes | yes |
| MF-7 | yes | yes | yes (`audit_twosided.json`) | yes | yes |
| MF-10 | yes | yes | yes (5 adjudication files) | yes | yes |
| MF-12 | yes | yes | yes (`ptruth_summary.json`, `COMPUTE.md`) | yes | yes |
| MF-13 | yes | yes | yes (`audit_twosided.json`) | yes | yes |
| MF-14 | yes | yes | yes (`r4_robustness.json`) | yes | yes |
| MF-17 | yes | yes | yes (`auroc_ci.json`) | yes | yes |

**8/8 MFs — PASS.** (MF-10's evidence line names the five adjudication CSV/JSON
files; MF-17's draft sentence is present and closed with its reported CI.)

## 3. Frozen-file integrity under `04_experiments/results/c1/`

```
$ git -C 'C:/Users/shubh/research-lab' status --porcelain -- 04_experiments/results/c1/
?? 04_experiments/results/c1/r3/
```

- The only entry under `results/c1/` is `?? 04_experiments/results/c1/r3/` —
  untracked, i.e. the wholly new R3 exploratory tree owned by this lane.
- **No tracked file under `04_experiments/results/c1/` (excluding `r3/exp`)
  shows as modified** (`M ` / ` A ` / ` D `): none. Frozen files
  (`results_full.json`, `predictions.csv`, `ablations.json`, `rung5.json`,
  `transfer.json`, etc.) are intact.
- Note (outside lane scope, for context only): `git status` does show `M` on
  `04_experiments/PREREGISTRATION.md`, `RESULTS-INDEX.json`, `harness/runner.py`,
  etc. — none of which live under `results/c1/`. Not a violation of the MF-10 /
  ANSWERS check.

**PASS.**

## 4. Disclosure check — LLM annotators (one inconsistency flagged)

- `adjudication.json` `disclosure.labellers`:
  - A: `qwen2.5:1.5b (as recorded upstream)` — **but** `ANSWERS.md` MF-10 § and
    `final_summary.md` say A = `qwen2.5:1.5b-instruct`.
  - B: `qwen3:1.7b (as recorded upstream)` — consistent with `ANSWERS.md` / `final_summary.md`.
  - Resolver: `qwen2.5:1.5b-instruct`, strict rubric, Ollama — consistent across
    `adjudication.json`, `resolve.csv` notes, and `_resolver_tmp/resolver_raw.json`
    (model field = `qwen2.5:1.5b-instruct`, prompt requires a verbatim span).
- The `"(as recorded upstream)"` qualifier appears only in `adjudication.json`;
  the precise A figure (`qwen2.5:1.5b-instruct`) is asserted in `ANSWERS.md` /
  `final_summary.md` without an upstream source in this file pack. **FAIL (minor,
  disclosure consistency only)**: the A model name differs between files. The
  task-delegated names — A `qwen2.5:1.5b-instruct`, B `qwen3:1.7b`, resolver
  `qwen2.5:1.5b-instruct` (strict) — match `ANSWERS.md` / `final_summary.md` /
  `resolver_raw.json`; only `adjudication.json` uses the looser upstream string.
  Recommend reconciling the one string; no number changes.

## 5. Commands run

- `python 04_experiments/src/r3_exp_adjudicate.py --kappa`
- `python -m pytest 04_experiments/src/tests/test_r3_exp_adjudicate.py -q`
- `git -C 'C:/Users/shubh/research-lab' status --porcelain`
- Recount script over the four CSVs + `adjudication.json`; seed-reproduction
  check via `sample_negatives()`; ANSWERS.md section/field scan.

All findings are exploratory / post-hoc and use no human gold standard; any
contradiction with the source dataset requires human adjudication.
