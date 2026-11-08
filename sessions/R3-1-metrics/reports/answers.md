# R3-1 — per-MF answers (MF-1, 8, 9, 15, 16, 18, 19, 20, 21, 22, 29, 39, 43, 44)

Lane: R3-1 (metrics & statistics). Evidence files (read-only inputs + produced outputs):
- `04_experiments/results/c1/r3/metrics/DEFINITIONS.md`
- `04_experiments/results/c1/r3/metrics/metrics.json` (and `metrics.md`)
- `04_experiments/results/c1/r3/metrics/intervals.json` (and `intervals.md`)
- `04_experiments/results/c1/r3/metrics/h3.json`
- `04_experiments/results/c1/r3/metrics/rung2.json`
- `04_experiments/results/c1/results_full.json` (frozen thresholds, for MF-29)
- Verification reports: `sessions/R3-1-metrics/reports/verify_*.md`

Commands and seeds (reproduce all numbers below):
- `python 04_experiments/src/r3_metrics_core.py` — seed 20261103; writes `metrics.json`, `metrics.md`, `DEFINITIONS.md`.
- `python 04_experiments/src/r3_metrics_intervals.py` — seed 12345, N_BOOT 10000; writes `intervals.json`, `intervals.md`.
- `python 04_experiments/src/r3_metrics_h3.py` — config seed 20261103, bootstrap seed 12345, N_BOOT 10000; writes `h3.json`.
- `python 04_experiments/src/r3_metrics_rung2.py` — seed 12345, 10000 permutation draws; writes `rung2.json`.

Copy note: this file is duplicated verbatim at `sessions/R3-1-metrics/reports/answers.md`.

---

## MF-1 — quantity called abstain precision is a per-rung refusal rate

Verdict: Fixed.

Evidence: `metrics.json` → `definitions.refusal_rate_k`, `definitions.precision_k`; `runs.*.operating_points.band.per_rung.*` (`abstain_precision` vs `refusal_rate`); `DEFINITIONS.md`; `metrics.md`.

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "We distinguish the per-rung refusal rate P(refused | negative of rung k) from abstain precision P(negative | refused); for example, the frozen band's R2 cell has refusal rate 279/280 = 99.64% but abstain precision 279/(279+302) = 48.0%."

## MF-8 — paper never reports abstention precision

Verdict: Fixed.

Evidence: `metrics.json` → `runs.*.operating_points.band.per_rung.*.abstain_precision`, `pooled.pooled_abstain_precision`, `pooled.n_refused_negatives`, `pooled.n_refused_answerable`; `DEFINITIONS.md`.

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "Every precision figure is P(negative | refused) = refused negatives / all refusals, with the refusal count behind each cell; the frozen band pooled held-out value is 1478/1780 = 83.0% (corrected: 1441/1807 = 79.7%), and R2's 99.64% is its recall, not its precision."

## MF-9 — coverage denominator (four negatives per question) understates coverage

Verdict: Fixed (coverage population corrected; AURCC/abstention F1 not added this round).

Evidence: `metrics.json` → `runs.*.operating_points.band.coverage_item`, `coverage_question`, `coverage_question_n_answered`, `coverage_question_n_qids`; `metrics.md`.

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "Coverage is reported over both populations: item-level (admitted items / all items) and question-level (questions whose rung-0 item is not refused / 400): frozen band 5.27% / 24.50% (98/400); corrected band 3.83% / 8.50% (34/400)."

## MF-15 — table cells are refusal rates, not pooled precision

Verdict: Fixed.

Evidence: `metrics.json` → `runs.*.operating_points.band.pooled.pooled_abstain_precision`, `per_rung.*.abstain_precision`, `per_rung.*.refusal_rate`, `pooled.n_refused_negatives`, `pooled.n_refused_answerable`; `DEFINITIONS.md`.

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "Table 1 reports both quantities: the per-rung refusal rate (e.g. frozen R1 400/400) and the pooled abstain precision (frozen 1478/1780 = 83.0%; corrected 1441/1807 = 79.7%), so the 0.80 rule is checked against the pooled value, not the per-rung rate."

## MF-16 — zero-width CIs on H1/H3 are boundary artefacts; interval method mismatch

Verdict: Fixed.

Evidence: `intervals.json` → `H1`, `H3`, `interval_method_check` (paper_stated_method = "bca", archive_per_rung_method, mismatch = true, mismatched_rungs = ["1","3","4"]); `intervals.md`.

Reproduce: `python 04_experiments/src/r3_metrics_intervals.py` (seed 12345, N_BOOT 10000).

Proposed draft sentence: "The zero-width H1 and H3 intervals are boundary artefacts of 0 discordant pairs out of 400 and 1479; exact Clopper-Pearson upper bounds are 0.0092 and 0.0025 (Wilson 0.0095 and 0.0026). Section 3.5 states BCa, but the archive records percentile for rungs 1, 3 and 4 and BCa only for rung 2."

## MF-18 — cluster bootstrap: 18 articles, zero-width cells, wrong min width ratio

Verdict: Fixed.

Evidence: `intervals.json` → `cluster_bootstrap` (`n_articles_test` = 18, `n_articles_verified` = true, `rung1_cluster_ci95`, `rung3_cluster_ci95`, `min_width_ratio_archive` = 0.4521, `min_width_ratio_note`); `intervals.md`.

Reproduce: `python 04_experiments/src/r3_metrics_intervals.py` (seed 12345, N_BOOT 10000).

Proposed draft sentence: "The cluster bootstrap rests on 18 held-out articles; the rung-1 and rung-3 cluster intervals are [1.00, 1.00], and the smallest finite width ratio in the archive is 0.4521 (confirmatory rung 2), not 0.851."

## MF-19 — corrected H3 not at matched recall; matched single violates 0.80

Verdict: Fixed (documented: no precision-compliant threshold exists; re-matched on recall).

Evidence: `h3.json` → `dev_recalls` (band_dev_recall = 0.9898, matched_single_dev_recall = 0.9925, matched_single_dev_precision = 0.7886); `constrained_search` (constrained_threshold_exists = false, max_feasible_recall = 0.975560, closest_feasible_threshold.t = 0.587260); `re_matched_recall` (threshold = 0.620811, dev_recall = 0.989817, dev_precision = 0.792391, heldout_abstain_precision = 0.991210, difference = -0.0169, CI [-0.0264, -0.0074]); `original_matched_grid`.

Reproduce: `python 04_experiments/src/r3_metrics_h3.py` (config seed 20261103, bootstrap seed 12345).

Proposed draft sentence: "On the corrected run the band (dev recall 0.9898) and the matched single (0.9925) are not at matched recall and the matched single's dev precision is 0.7886, below 0.80; no precision-compliant single threshold reaches the band's recall (best 0.9756 at t = 0.587260). Re-matching on recall (t = 0.620811) gives held-out precision 0.9912 versus the band's 0.9743, difference -0.0169, 95% CI [-0.0264, -0.0074]."

## MF-20 — corrected arm 11.00% over-refusal versus declared 0.10 cap

Verdict: Fixed (statement; breach on held-out half noted).

Evidence: `h3.json` → `over_refusal_arm.corrected_exploratory_band` (`cap_binds_on` = "dev (fit_band_constrained enforces dev over-refusal <= cap during threshold search)", `dev_over_refusal` = 0.095, `held_out_over_refusal` = 0.11, `breached_on_dev` = false, `breached_on_held_out` = true).

Reproduce: `python 04_experiments/src/r3_metrics_h3.py` (config seed 20261103, bootstrap seed 12345).

Proposed draft sentence: "The declared 0.10 over-refusal cap binds on dev by construction: the corrected arm's dev over-refusal is 0.0950 (not breached), but its held-out over-refusal is 0.1100, which exceeds the cap."

## MF-21 — "no single feature group carries the result" supported only by point estimates

Verdict: Claim narrowed.

Evidence: `intervals.json` → `equivalence` (`all_12_auroc` = 0.8738, `no_dense_auroc` = 0.8623, `dense_only_auroc` = 0.8695, `all_12_vs_no_dense` diff = 0.0116, CI [0.0038, 0.0196], contains_zero = false; `all_12_vs_dense_only` diff = 0.0043, CI [-0.0078, 0.0161], contains_zero = true; `reading`).

Reproduce: `python 04_experiments/src/r3_metrics_intervals.py` (seed 12345, N_BOOT 10000).

Proposed draft sentence: "Feature-group ablation: all_12 AUROC 0.8738 versus no_dense 0.8623, paired difference 0.0116, 95% CI [0.0038, 0.0196] (excludes zero), but versus dense_only 0.8695 the difference is 0.0043, 95% CI [-0.0078, 0.0161] (includes zero); the 'no single feature group carries the result' wording should therefore be narrowed to the dense group."

## MF-22 — held-out rung-2 shortfall; exchangeability for both splits

Verdict: Fixed.

Evidence: `rung2.json` → `shortfall`, `splits.dev` (`n_kept` = 273, `n_dropped` = 127, `share_kept` = 0.6825), `splits.test` (`n_kept` = 280, `n_dropped` = 120, `share_kept` = 0.7), `exchangeability.splits.dev/test.variables.*.p_value`, `min_p` (value = 0.052366, variable = "dev/q_chars"), `significant_at_0.05` = [].

Reproduce: `python 04_experiments/src/r3_metrics_rung2.py` (seed 12345, 10000 permutation draws).

Proposed draft sentence: "Rung 2 keeps 273 of 400 dev questions (127 dropped) and 280 of 400 held-out questions (120 dropped); kept versus dropped exchangeability p-values are all above 0.05 in both splits (smallest 0.052, dev q_chars)."

## MF-29 — matched-recall comparison degenerate by construction

Verdict: Fixed (frozen degeneracy documented; corrected run is not degenerate).

Evidence: `04_experiments/results/c1/results_full.json` → `thresholds.single_matched_recall.t` = 0.90722098925 equals `thresholds.band.t_lo` = 0.90722098925; `h3.json` → `degenerate_check` (`single_matched_recall_t` = 0.636224300244, `band_t_lo` = 0.52318216643, `equal` = false, `band_t_hi` = 0.537011889113, `n_heldout_above_t_hi` = 222); `h3.json` report and `h3.md`.

Reproduce: frozen equality from `results_full.json`; corrected-run check via `python 04_experiments/src/r3_metrics_h3.py` (config seed 20261103, bootstrap seed 12345).

Proposed draft sentence: "In the frozen run single_matched_recall.t = 0.90722098925 equals band.t_lo = 0.90722098925, so only the upper cut can differ; in the corrected run this equality no longer holds (0.636224 versus 0.523182), and 222 held-out items score above t_hi = 0.537012."

## MF-39 — "abstain precision" undefined; cells are per-rung refusal rate

Verdict: Fixed.

Evidence: `DEFINITIONS.md`; `metrics.json` → `definitions.pooled_precision`, `definitions.precision_k`, `definitions.refusal_rate_k`, `definitions.coverage_item`, `definitions.coverage_question`.

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "Abstain precision is defined as P(negative | refused) = refused negatives / all refusals, with numerator and denominator stated; the per-rung refusal rate P(refused | negative of rung k) is reported separately."

## MF-43 — arm table names the wrong conditional for the 87.30% cell

Verdict: Fixed.

Evidence: `metrics.json` → `top1` (`refuse_miss` = 0.6322, `n_misses` = 87, `n_refused_misses` = 55; `precision_miss_given_refused` = 0.8730, `n_refused` = 63); `metrics.md` (Top-1 section).

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "The top-1 arm reports both conditionals: P(refused | miss) = 63.22% (55/87) and P(miss | refused) = 87.30% (55/63); the 87.30% cell is the latter."

## MF-44 — coverage column for all five arm rows

Verdict: Fixed.

Evidence: `metrics.json` → `arms.frozen.*` and `arms.corrected.*` (`coverage` for all five arms); `metrics.md` (Arms table).

Reproduce: `python 04_experiments/src/r3_metrics_core.py` (seed 20261103).

Proposed draft sentence: "Coverage is reported beside every arm row for both runs (for example frozen band_primary 0.0527 item-level / 0.2450 question-level; corrected exploratory_band 0.3960 / 0.8900)."
