# TASK R3-1 — metrics & statistics (main laptop, profile res-s1)

Goal: give the paper correct, clearly defined metrics and honest uncertainty, answering MF-1, 8, 9, 15, 16, 18, 19, 20,
21, 22, 29, 39, 43, 44 (read each item's full text + "evidence to supply" in `06_review/reviews/round2-c1/AGGREGATE.md`).

OWNED (write only these): `04_experiments/src/r3_metrics_*.py`, `04_experiments/src/tests/test_r3_metrics_*.py`,
`04_experiments/results/c1/r3/metrics/**`, `sessions/R3-1-metrics/**`.
READ-ONLY: everything else (frozen results, predictions.csv, results_full.json, rung5.json, transfer.json, top1_*.json,
stats_addendum.json, the corrected-run outputs, the draft).

Deliverables
1. `results/c1/r3/metrics/DEFINITIONS.md` — one-sentence definitions with numerator/denominator for: abstain precision
   P(negative | refused), per-rung refusal rate P(refused | negative of rung k), over-refusal P(refused | answerable),
   coverage = questions answered / questions asked (state the population explicitly, MF-9/38), abstain recall.
2. `results/c1/r3/metrics/metrics.json` (+ `.md` table) recomputed from the frozen predictions for BOTH the frozen and the
   corrected (D4) runs: per-rung refusal rate AND per-rung abstain precision (e.g. R2 = 279/(279+302) per MF-39), pooled
   precision, coverage, counts (n refused, n per cell) for every cell; all five arm rows with coverage (MF-44); both
   conditionals for the top-1 arm, P(refused|miss) and P(miss|refused) (MF-43).
3. Intervals: replace zero-width boundary intervals with an exact/Wilson or Clopper-Pearson interval and say why (MF-16);
   check the interval method stated in the paper against the archive and report any mismatch; cluster bootstrap by article
   with the number of clusters stated and the correct min/max width ratio (MF-18); equivalence/interval support for "no single
   feature group carries the result" across the eight subsets, or a recommended narrower wording (MF-21).
4. H3 at genuinely matched abstain recall and a matched single threshold that satisfies the 0.80 constraint, or a documented
   statement that no such threshold exists (MF-19, MF-29); explicit statement whether the corrected arm's 11.00% over-refusal
   breached the declared 0.10 cap (MF-20); held-out rung-2 shortfall + exchangeability check on BOTH splits (MF-22).
5. `results/c1/r3/metrics/ANSWERS.md` — per MF item: verdict (fixed / rebutted / claim narrowed), the evidence file + key,
   the command that reproduces it, and the exact sentence(s) you propose the integrator puts in the draft.
6. Targeted tests for every new script (at least: definitions on a hand-made 10-row fixture give hand-computed values).

Batch plan suggestion (you decide): batch 1 = {definitions+recompute script, interval methods, H3 matched-recall, rung-2
exchangeability}; batch 2 = {review+retest batch 1, cluster bootstrap, feature-group equivalence, arm-table conditionals};
batch 3 = {review, ANSWERS.md, tests}. Tell R3-4 nothing directly: ANSWERS.md is the hand-off.
