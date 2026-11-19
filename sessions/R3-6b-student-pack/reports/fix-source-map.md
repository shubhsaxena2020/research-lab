# Fix report — `07_student/SOURCE-MAP.md` (batch 2 corrections)

Editor: correction pass, 2026-11-19. File owned and written: `07_student/SOURCE-MAP.md`.
Report written: `sessions/R3-6b-student-pack/reports/fix-source-map.md`. Nothing else touched.

Inputs: `reports/review-numbers.md` (finding 2: C21 `per_rung` hop),
`reports/review-complete.md` (gap 5: `C13b` absent from the inventory), and the lead's update to
`sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` line 48, which now lists `C13b` as an accepted split of C13.

## Verdict

All three corrections applied. Every line number cited in the table and in §2 now resolves to the text it
claims, and every stored-value cell matches `json.load`. No stored value was wrong, so no value changed.

## Changes made (3)

1. **C21 row, `per_rung` hop: `(561)` → `(556)`.** Line 561 is `"hi": 1.0,` (the upper bound of rung 1's
   `ci95`); line 556 is `      "per_rung": {`. The four neighbouring hops — `"test"` 489,
   `"exploratory_band"` 551, `"4"` 596, `abstain_precision` 597 — were re-checked and are correct.
2. **C03 row, cross-check parenthetical sharpened.** It read "`mf10.agreement.contingency` (block opens line 81)".
   Line 81 is the `"agreement": {` block; the `contingency` key itself is at line 87 (verified). The cell now
   says so explicitly, so the cited line matches the named key rather than its parent.
3. **One sentence added under the table on `C13b`** (per the lead's decision): `C13b` is an accepted split of
   C13, the resampling config (`n_boot`, `seed`) lives at the top level of `mf17_auroc_intervals.json` rather
   than under `denominators`, and `CLAIM-INVENTORY.md` now lists it. `C13b` was **not** renamed or removed.

Structure, §2, §3 hashes and §4 "Known exclusions" are unchanged — including the 90.73% ban and the statement
that only C03 is derived (both re-asserted mechanically below).

## (a) C20/C21/C22 path resolution

Snippet (run from the repo root):

```python
import json
c1  = json.load(open("04_experiments/results/c1/results_full.json"))
c1c = json.load(open("04_experiments/results/c1_corrected/results_full.json"))
print("C20 c1  test.band_primary.per_rung['4'].abstain_precision        =",
      c1["test"]["band_primary"]["per_rung"]["4"]["abstain_precision"])
print("C21 c1  test.exploratory_band.per_rung['4'].abstain_precision    =",
      c1["test"]["exploratory_band"]["per_rung"]["4"]["abstain_precision"])
print("C22 c1c test.exploratory_band.per_rung['4'].abstain_precision    =",
      c1c["test"]["exploratory_band"]["per_rung"]["4"]["abstain_precision"])
print("EXCL c1c test.band_primary.per_rung['4'].abstain_precision       =",
      c1c["test"]["band_primary"]["per_rung"]["4"]["abstain_precision"])
```

Output:

```
C20 c1  test.band_primary.per_rung['4'].abstain_precision        = 1.0
C21 c1  test.exploratory_band.per_rung['4'].abstain_precision    = 0.8471
C22 c1c test.exploratory_band.per_rung['4'].abstain_precision    = 0.1253
EXCL c1c test.band_primary.per_rung['4'].abstain_precision       = 0.9073
```

Line-level confirmation of the four hops, verbatim from the file (1-based):

```
C20 c1/results_full.json                          489 |   "test": {
C20 c1/results_full.json                          490 |     "band_primary": {
C20 c1/results_full.json                          495 |       "per_rung": {
C20 c1/results_full.json                          535 |         "4": {
C20 c1/results_full.json                          536 |           "abstain_precision": 1.0,
C21 c1/results_full.json                          551 |     "exploratory_band": {
C21 c1/results_full.json                          556 |       "per_rung": {
C21 c1/results_full.json                          596 |         "4": {
C21 c1/results_full.json                          597 |           "abstain_precision": 0.8471,
C22 c1_corrected/results_full.json                392 |   "test": {
C22 c1_corrected/results_full.json                454 |     "exploratory_band": {
C22 c1_corrected/results_full.json                459 |       "per_rung": {
C22 c1_corrected/results_full.json                499 |         "4": {
C22 c1_corrected/results_full.json                500 |           "abstain_precision": 0.1253,
```

## (b) Every cited line number, with the text found

112 line citations across 10 files, all opened at the cited 1-based line. `FIXED` marks the one citation
that was wrong in the file as reviewed; everything else was already correct and is listed so the check is
auditable rather than asserted.

| row | hop | file | line | text found (truncated) | status |
|---|---|---|---|---|---|
| C01 | `flat` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 246 | `"c1.r3_3b.mf10.cohen_kappa_overall": 0.2802,` | OK |
| C01 | `full` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 86 | `"kappa": 0.2801966292134831,` | OK |
| C02 | `raw` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 243 | `"c1.r3_3b.mf10.raw_agreement_po": 0.59,` | OK |
| C02 | `n_agreed` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 244 | `"c1.r3_3b.mf10.n_agreed": 59,` | OK |
| C02 | `n_items` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 236 | `"c1.r3_3b.mf10.n_items": 100,` | OK |
| C03 | `agreement_blk` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 81 | `"agreement": {` | OK |
| C03 | `contingency_key` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 87 | `"contingency": {` | OK |
| C04 | `n_disagreed` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 245 | `"c1.r3_3b.mf10.n_disagreed": 41,` | OK |
| C05 | `A` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 247 | `"c1.r3_3b.mf10.labeller_A_answerable_n": 62,` | OK |
| C05 | `B` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 249 | `"c1.r3_3b.mf10.labeller_B_answerable_n": 21,` | OK |
| C06 | `resolved_1` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 254 | `"c1.r3_3b.mf10.resolver_resolved_1_n": 35,` | OK |
| C06 | `resolved_0` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 255 | `"c1.r3_3b.mf10.resolver_resolved_0_n": 6,` | OK |
| C06 | `ambiguous` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 256 | `"c1.r3_3b.mf10.resolver_resolved_ambiguous_n": 0,` | OK |
| C06 | `total` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 253 | `"c1.r3_3b.mf10.resolver_on_disagreements_n": 41,` | OK |
| C07 | `n` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 251 | `"c1.r3_3b.mf10.resolved_answerable_n": 56,` | OK |
| C07 | `share` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 252 | `"c1.r3_3b.mf10.resolved_answerable_share": 0.56,` | OK |
| C08 | `r1` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 259 | `"c1.r3_3b.mf10.rung1.kappa": 0.0,` | OK |
| C08 | `r2` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 265 | `"c1.r3_3b.mf10.rung2.kappa": 0.2991,` | OK |
| C08 | `r3` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 271 | `"c1.r3_3b.mf10.rung3.kappa": 0.026,` | OK |
| C08 | `r4` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 277 | `"c1.r3_3b.mf10.rung4.kappa": 0.1379,` | OK |
| C08 | `n_by_rung` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 237 | `"c1.r3_3b.mf10.n_items_by_rung": {` | OK |
| C08 | `pr1` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 99 | `"kappa": 0.0,` | OK |
| C08 | `pr2` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 107 | `"kappa": 0.29906542056074775,` | OK |
| C08 | `pr3` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 115 | `"kappa": 0.025974025974026038,` | OK |
| C08 | `pr4` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 123 | `"kappa": 0.13793103448275895,` | OK |
| C09 | `block` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 217 | `"comparison_with_prior_llm_adjudication": {` | OK |
| S2 | `exploratory_status` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 6 | `"exploratory_status": "post-hoc / exploratory repeated LLM judgement; NOT human gold",` | OK |
| S2 | `agreement` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 81 | `"agreement": {` | OK |
| S2 | `per_rung` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 95 | `"per_rung": {` | OK |
| S2 | `resolved` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 151 | `"resolved": {` | OK |
| S2 | `disagreement_resolution` | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | 177 | `"disagreement_resolution": {` | OK |
| C10 | `point` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1256 | `"c1.r3_3b.mf17.frozen_heldout_auroc.point": 0.9823630831643002,` | OK |
| C10 | `lo` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1255 | `"c1.r3_3b.mf17.frozen_heldout_auroc.ci95_lo": 0.9776211411662427,` | OK |
| C10 | `hi` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1254 | `"c1.r3_3b.mf17.frozen_heldout_auroc.ci95_hi": 0.9866543835742593,` | OK |
| C11 | `point` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1180 | `"c1.r3_3b.mf17.corrected_heldout_auroc.point": 0.8738488843813388,` | OK |
| C11 | `lo` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1179 | `"c1.r3_3b.mf17.corrected_heldout_auroc.ci95_lo": 0.8586833140203312,` | OK |
| C11 | `hi` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1178 | `"c1.r3_3b.mf17.corrected_heldout_auroc.ci95_hi": 0.8893003500532195,` | OK |
| C12 | `diff` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1397 | `"c1.r3_3b.mf17.paired_auroc_diff.diff": 0.10851419878296142,` | OK |
| C12 | `lo` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1396 | `"c1.r3_3b.mf17.paired_auroc_diff.ci95_lo": 0.09458017350090517,` | OK |
| C12 | `hi` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1395 | `"c1.r3_3b.mf17.paired_auroc_diff.ci95_hi": 0.12252082237972457,` | OK |
| C12 | `nested` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1380 | `"c1.r3_3b.mf17.paired_auroc_diff": {` | OK |
| C13 | `denoms` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 980 | `"held_out_common": {` | OK |
| C13b | `n_boot` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1053 | `"n_boot": 10000,` | OK |
| C13b | `seed` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1660 | `"seed": 20261118,` | OK |
| N7 | `lim_opens` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1045 | `"limitations": [` | OK |
| N7 | `item1` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1046 | `"All intervals are post-hoc/exploratory; no frozen verdict is revised.",` | OK |
| N7 | `item5` | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | 1050 | `"The gold-indicator column is a label-construction artefact; its AUROC is not evidence about rung hardness."` | OK |
| C14 | `surface_lex` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1896 | `"c1.r3_3b.mf7.gold_control.dev.r1.auroc_surface_lex": 0.9762,` | OK |
| C15 | `plus_is_gold` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1891 | `"c1.r3_3b.mf7.gold_control.dev.r1.auroc_plus_is_gold": 1.0,` | OK |
| C16 | `is_gold_alone` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1889 | `"c1.r3_3b.mf7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented": 1.0,` | OK |
| C16 | `deterministic` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1906 | `"c1.r3_3b.mf7.gold_control.dev.r1.is_gold_deterministic_from_label": true,` | OK |
| C17 | `n_hit` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1800 | `"c1.r3_3b.mf7.d3_pooled.all.n_hit": 655,` | OK |
| C17 | `n_miss` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1801 | `"c1.r3_3b.mf7.d3_pooled.all.n_miss": 145,` | OK |
| C17 | `auroc` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1767 | `"c1.r3_3b.mf7.d3_pooled.all.auroc_surface_lex_hit_vs_miss": 0.7327,` | OK |
| C18 | `dev_hit` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1839 | `"c1.r3_3b.mf7.d3_pooled.dev.n_hit": 342,` | OK |
| C18 | `dev_miss` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1840 | `"c1.r3_3b.mf7.d3_pooled.dev.n_miss": 58,` | OK |
| C18 | `test_hit` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1887 | `"c1.r3_3b.mf7.d3_pooled.test.n_hit": 313,` | OK |
| C18 | `test_miss` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1888 | `"c1.r3_3b.mf7.d3_pooled.test.n_miss": 87,` | OK |
| C19 | `estimand` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1848 | `"c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available": false,` | OK |
| C19 | `rungs_present` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1849 | `"c1.r3_3b.mf7.d3_pooled.rungs_present_value": -1,` | OK |
| C19 | `note` | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | 1757 | `"d3_scope": "D3 (top1_presented) has ONLY rung=-1 pooled hit/miss observations in items_top1.jsonl / features_…` | OK |
| C20 | `test` | `04_experiments/results/c1/results_full.json` | 489 | `"test": {` | OK |
| C20 | `band_primary` | `04_experiments/results/c1/results_full.json` | 490 | `"band_primary": {` | OK |
| C20 | `per_rung` | `04_experiments/results/c1/results_full.json` | 495 | `"per_rung": {` | OK |
| C20 | `rung4` | `04_experiments/results/c1/results_full.json` | 535 | `"4": {` | OK |
| C20 | `abstain_precision` | `04_experiments/results/c1/results_full.json` | 536 | `"abstain_precision": 1.0,` | OK |
| C21 | `test` | `04_experiments/results/c1/results_full.json` | 489 | `"test": {` | OK |
| C21 | `exploratory_band` | `04_experiments/results/c1/results_full.json` | 551 | `"exploratory_band": {` | OK |
| C21 | `per_rung` | `04_experiments/results/c1/results_full.json` | 556 | `"per_rung": {` | FIXED |
| C21 | `rung4` | `04_experiments/results/c1/results_full.json` | 596 | `"4": {` | OK |
| C21 | `abstain_precision` | `04_experiments/results/c1/results_full.json` | 597 | `"abstain_precision": 0.8471,` | OK |
| N4 | `p_note` | `04_experiments/results/c1/results_full.json` | 364 | `"p_note": "no discordant pairs (all differences zero)",` | OK |
| S2 | `ablation_no_rank_test` | `04_experiments/results/c1/results_full.json` | 19 | `"test": {` | OK |
| C22 | `test` | `04_experiments/results/c1_corrected/results_full.json` | 392 | `"test": {` | OK |
| C22 | `exploratory_band` | `04_experiments/results/c1_corrected/results_full.json` | 454 | `"exploratory_band": {` | OK |
| C22 | `per_rung` | `04_experiments/results/c1_corrected/results_full.json` | 459 | `"per_rung": {` | OK |
| C22 | `rung4` | `04_experiments/results/c1_corrected/results_full.json` | 499 | `"4": {` | OK |
| C22 | `abstain_precision` | `04_experiments/results/c1_corrected/results_full.json` | 500 | `"abstain_precision": 0.1253,` | OK |
| EXCL | `90.73` | `04_experiments/results/c1_corrected/results_full.json` | 439 | `"abstain_precision": 0.9073,` | OK |
| C23 | `262_item3` | `04_experiments/PREREGISTRATION.md` | 262 | `3. **The corrected analysis refits the two thresholds** on corrected dev scores, because the score` | OK |
| C23 | `263_quote` | `04_experiments/PREREGISTRATION.md` | 263 | `distribution changes. Thresholds are therefore not comparable between the two runs; AUROC is, because` | OK |
| C23 | `264` | `04_experiments/PREREGISTRATION.md` | 264 | `it is threshold-free. Table 4 of the paper reports both and says this.` | OK |
| N1 | `22_h1` | `04_experiments/PREREGISTRATION.md` | 22 | `- **H1 (hardness monotonicity).** Abstain precision on the held-out half is non-increasing across rungs` | OK |
| N1 | `23` | `04_experiments/PREREGISTRATION.md` | 23 | `1→4, and the drop from rung 1 to rung 3 is ≥ 15 points.` | OK |
| N1 | `24` | `04_experiments/PREREGISTRATION.md` | 24 | `*Refuted if* the rung-1 minus rung-3 paired difference has a 95% CI containing 0, or if the observed` | OK |
| N1 | `25` | `04_experiments/PREREGISTRATION.md` | 25 | `sequence is not non-increasing, or if the drop is < 15 points.` | OK |
| N2 | `heading` | `04_experiments/PREREGISTRATION.md` | 165 | `### D1 — 2026-11-03T05:27+05:30 — confirmatory thresholds are degenerate; exploratory constrained arm added` | OK |
| N2 | `167` | `04_experiments/PREREGISTRATION.md` | 167 | `Observed before any number was written into a draft: with the pre-registered rule (maximise abstain` | OK |
| N2 | `172` | `04_experiments/PREREGISTRATION.md` | 172 | `coverage.` | OK |
| N3 | `178` | `04_experiments/PREREGISTRATION.md` | 178 | `2. A second, EXPLORATORY operating point is added: maximise dev abstain recall subject to dev abstain` | OK |
| N3 | `180` | `04_experiments/PREREGISTRATION.md` | 180 | `it is never described as confirmatory, and it cannot rescue a hypothesis — the pre-registered verdict` | OK |
| N3 | `181` | `04_experiments/PREREGISTRATION.md` | 181 | `stands on the pre-registered gate.` | OK |
| N5 | `hdr3` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 3 | `Lane: R3-3b. All three items are **exploratory / post-hoc**; none revises a` | OK |
| N5 | `hdr6` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 6 | `key is `c1.r3_3b.<item>.`.` | OK |
| N5 | `mf17_55` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 55 | `**Label:** exploratory / post-hoc (`exploratory: true`, `post_hoc: true`,` | OK |
| N5 | `mf17_56` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 56 | ``label: "exploratory/post-hoc"`).` | OK |
| N5 | `mf10_107` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 107 | `**Label:** exploratory / post-hoc (`mf10.post_hoc_exploratory: true`,` | OK |
| N5 | `mf10_108` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 108 | ``mf10.exploratory_status: "post-hoc / exploratory repeated LLM judgement; NOT human gold"`).` | OK |
| N5 | `mf7_147` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 147 | `**Label:** exploratory / post-hoc (`exploratory: true`, `post_hoc: true`,` | OK |
| N5 | `mf7_149` | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | 149 | ``notes.label: "exploratory / post-hoc; no frozen verdict is revised."`).` | OK |
| N6 | `cp11` | `orchestration/HEAD-REVIEW.md` | 94 | `Prepared but did not launch `sessions/R3-4f-bind-3b/`. It is gated on R3-4e completion and independent head ve…` | OK |
| N6 | `cp10` | `orchestration/HEAD-REVIEW.md` | 84 | `R3-4d was verified complete and pushed as `ea82291`; its current evidence is recorded in `sessions/R3-4d-verif…` | OK |
| N8 | `triage1` | `sessions/R3/TRIAGE.md` | 1 | `# ROUND 3 TRIAGE — every round-2 must-fix item has exactly one owning lane` | OK |
| N8 | `triage8` | `sessions/R3/TRIAGE.md` | 8 | `\| 1 \| "abstain precision" is a per-rung refusal rate; define numerators/denominators \| R3-1 (+I) \|` | OK |
| N8 | `triage51` | `sessions/R3/TRIAGE.md` | 51 | `\| 44 \| coverage column for all five arm rows, or narrow the claim \| R3-1 (+I) \|` | OK |
| N8 | `head46` | `orchestration/HEAD-REVIEW.md` | 46 | `- Round 3 = answer all 44 round-2 must-fix items (06_review/reviews/round2-c1/AGGREGATE.md), plus the S3 stude…` | OK |
| N8 | `cp5hdr` | `orchestration/HEAD-REVIEW.md` | 42 | `## Checkpoint 5 — ROUND 3 START — 2026-11-08 (head)` | OK |
| N6 | `cp11hdr` | `orchestration/HEAD-REVIEW.md` | 90 | `## Checkpoint 11 — R3-6b student pack launched; R3-4f handoff prepared — 2026-11-19` | OK |
| N6 | `cp10hdr` | `orchestration/HEAD-REVIEW.md` | 82 | `## Checkpoint 10 — R3-4e whole-paper consistency audit — 2026-11-18` | OK |
| N1 | `s1hdr` | `04_experiments/PREREGISTRATION.md` | 15 | `## 1. Question and hypotheses` | OK |
| N8 | `common6` | `sessions/R3/COMMON.md` | 6 | `## What the project is` | OK |
| N8 | `common11` | `sessions/R3/COMMON.md` | 11 | `Round 3 answers every one of them: fix with evidence, or rebut with evidence. Never hide a weakness; narrow th…` | OK |

Totals: **112 checked, 1 fixed, 0 unresolved.**

## (c) Stored-value re-check

69 values re-read with `json.load` against the `stored value` cells (C01–C23 plus C13b, the five run labels,
the N2/N4 companions, the N7 `limitations` list and the 0.9073 exclusion). **0 mismatches.** Arithmetic
cross-checks re-run: C03 derives `0.4304` from `(0.59 − κ)/(1 − κ)` and from marginals
`(62×21 + 38×79)/10000 = 4304/10000 = 0.4304`; back-substitution returns `0.2801966292134831`, identical to the
stored κ. C10 − C11 = `0.1085141987829614` = stored `paired_auroc_diff.diff`.

## (d) Row count and git scope

```
$ grep -c '^| C\|^| N' 07_student/SOURCE-MAP.md      # run before the first edit
32
$ grep -c '^| C\|^| N' 07_student/SOURCE-MAP.md      # run after the last edit
32
$ grep -c '^| C'  07_student/SOURCE-MAP.md
24
$ grep -c '^| N'  07_student/SOURCE-MAP.md
8
```

Row IDs after the edit: C01–C23 (23) + C13b + N1–N8 (8) = 32. No row added, removed, reordered or renamed;
the only changes inside the table are the C21 hop number and the C03 parenthetical.

Mechanical re-assertion of §4: `90.73%` present as a banned value, `Only C03 is derived` present, and no
`over_refusal` / `cap` row was introduced (the map still carries no cap claim for C21/C22).

```
$ git status --short 07_student/
?? 07_student/
```

`07_student/` is untracked as a whole, so the edit shows only as the directory entry; nothing under
`05_paper/**`, `06_review/**`, `04_experiments/**` was written by this pass.

## Scratch scripts

`C:/Users/shubh/AppData/Local/hermes/profiles/res-s1/cache/scratch/sm_check.py` (line resolver, 112 citations) and `sm_values.py` (69 `json.load` value comparisons).
