# MF-10 — answerability adjudication: final summary

**Exploratory / post-hoc.** All R3-exp outputs are exploratory unless the frozen
pre-registration already names them. This file summarises the adjudication
sample and labels only; it does not change any pre-registered verdict.

## Design

- Item: does a rung 1–4 "negative" passage actually contain an answer to its
  question (TASK R3-3 deliverable 8)? Judged from the passage alone, per
  `rubric.md`; labels `1` = answerable, `0` = not answerable,
  `ambiguous` = partial/indirect/contradictory.
- Sample: `sample.csv`, 100 seeded negatives — 25 from each of rungs 1, 2, 3, 4
  (`random.Random(20261103)`; 48 dev / 52 test). Rung-0 positives were NOT
  sampled as controls, so this kappa does not estimate any false-unanswerable
  rate on answerable items (`r3_exp_adjudicate.py` docstring).
- Annotators: two independent labellers, A and B; labels are LLM-agent output
  per the TASK design, not human gold-standard labels. Model name, version,
  (models/prompts recorded in `adjudication.json` disclosure + 
  `_resolver_tmp/resolver_raw.json`). `resolve.csv` (third, resolving
  annotator) is 100/100 filled: `adjudication.json` reports the resolved
  share 5/100 (5%) answerable, with per-rung resolved shares rung1 0%,
  rung2 4%, rung3 4%, rung4 12% (qwen2.5:1.5b-instruct, strict rubric).

## Key numbers (`--kappa`)

- **Cohen's kappa = 0.1975** (n = 100 overlap; observed agreement 0.74,
  chance-corrected expected 0.676; 26 disagreements). Reproduced independently
  from `label_A.csv` / `label_B.csv`.
- **Labeller A: 30/100 "answerable" (`1`); labeller B: 6/100.** Neither used
  `ambiguous`.
- Confusion (A,B): both `0` = 69, both `1` = 5, A=`1`/B=`0` = 25, A=`0`/B=`1` = 1.
  The disagreement is one-directional: A is far more lenient (25 of 26 splits).
- Per rung: rung 1 — κ = 1.0 (0 disagreements); rung 2 — κ = 0.359 (3);
  rung 3 — κ = 0.359 (3); rung 4 — κ = −0.055 (20 of 25 disagree).

## Reading

- With the third labeller (strict rubric, qwen2.5:1.5b-instruct via Ollama),
  5/100 (5%) of sampled negatives answer the question (per-rung resolved:
  rung1 0%, rung2 4%, rung3 4%, rung4 12%). Pre-resolution range was 5–31%; the
  resolved point estimate is 5% with the kappa caveat above.
- Disagreement concentrates on rung 4 (κ ≈ 0): rung-4 "negatives" are the
  contested ones, which is exactly where the paper's mechanistic story is
  thinnest (see MF-14). Rung 1 is uncontested.
- Because the labellers are LLMs (not human adjudicators) and n = 25 per rung,
  this is a contamination warning, not a corrected denominator.

## Reproduce

`python 04_experiments/src/r3_exp_adjudicate.py --kappa`
