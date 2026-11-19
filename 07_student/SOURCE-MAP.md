# SOURCE-MAP — R3-6b student pack

Lane: `R3-6b-student-pack`. Written 2026-11-19.

This is a mapping card, not a narrative. It lists **every** number the student pack may print, one row per
canonical claim ID from `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md`, with the exact file, the exact key
(or section and line numbers), the value as it is stored in that file, and the form a student document may
print. **If a number is not in this table, it does not go in the pack.**

Every row was produced by opening the named file with `json.load` (or reading the named Markdown at the named
lines) during this task. Nothing is copied from a brief.

**Coverage.** C01–C23 (23 numeric claim IDs) plus N1–N8 (8 fact IDs) = 31 claim IDs, written as **32 table
rows**, because C13 carries two independent groups of numbers that live in two different parts of the same
file (`denominators.held_out_common` for the item counts, top-level `seed` / `n_boot` for the resampling
config) and the "exact JSON key" column can only name one path per row. The second C13 row is labelled
`C13b` and is a **split of C13, not a new claim ID**: no ID was invented, renumbered, or merged.

**Rounding rule.** The `rounding` column is the *only* permitted rendering of that row's number. `stored
value` is what `json.load` returns, so a writer can see where the file itself already rounded (e.g. the flat
`mf10` keys store `0.2802`, while `mf10.agreement.kappa` stores `0.2801966292134831`). No writer may
re-derive, re-compute, or further re-round any number in this map.

---

## 1. The table

| ID | value as printed | rounding | source path (relative to repo root) | exact JSON key or file section+lines | stored value (exact, unrounded) | label/limit note |
|---|---|---|---|---|---|---|
| C01 | Cohen's κ between the two LLM labellers = 0.2802 | 4 dp (as the source publishes); 2 dp (0.28) **not** permitted | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.cohen_kappa_overall']` (line 246 — stored already rounded to 4 dp); full precision at `mf10.agreement.kappa` (line 86) | `0.2802` at the flat key; `0.2801966292134831` at `mf10.agreement.kappa` | exploratory/post-hoc repeated **LLM** judgement; **NOT human gold**. κ = modest agreement **beyond chance between these two labellers** — not accuracy, not agreement with a human, not evidence the labels are true. |
| C02 | observed (raw) agreement 0.59 — 59 of 100 items | 2 dp as a rate; integers for the counts | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.raw_agreement_po']` (line 243), `results['c1.r3_3b.mf10.n_agreed']` (line 244), `results['c1.r3_3b.mf10.n_items']` (line 236) | `0.59` / `59` / `100` | same 100 seeded rung-1–4 negatives as C01; raw (uncorrected) agreement — it is **not** κ. |
| C03 | chance-level agreement implied by the marginals ≈ 0.43 (43%) | 4 dp (0.4304); 2 dp (0.43) acceptable | **DERIVED — no source file** | **No stored key.** κ = (Po − Pe)/(1 − Pe) rearranged gives Pe = (Po − κ)/(1 − κ) with Po = C02 and κ = C01; **lead-computed**. Cross-check from `mf10.agreement.contingency` (the `agreement` block opens line 81; the `contingency` key is at line 87): Pe = (62×21 + 38×79)/10000 = 0.4304 | not stored; the derivation returns `0.4304` | **must be labelled "derived from C01 and C02"** wherever it appears. Lead-computed, not a file value; a writer may not re-derive it or print it as if it were in the JSON. |
| C04 | the two labellers disagreed on 41 of 100 items | integer | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.n_disagreed']` (line 245) | `41` | consistent with C02 (100 − 59); exploratory/post-hoc, LLM only. |
| C05 | labeller A called 62 items answerable; labeller B called 21 | integer | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.labeller_A_answerable_n']` (line 247), `results['c1.r3_3b.mf10.labeller_B_answerable_n']` (line 249) | `62` / `21` | the marginals that produce C03: high raw agreement with very different per-labeller rates is exactly why κ is low. |
| C06 | on the 41 disagreements the strict resolver decided 35 answerable, 6 not answerable, 0 ambiguous | integers | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.resolver_resolved_1_n']` (line 254), `…_0_n` (255), `…_ambiguous_n` (256); case total `results['c1.r3_3b.mf10.resolver_on_disagreements_n']` = 41 (line 253) | `35` / `6` / `0` (of `41`) | third LLM with a stricter rubric; still LLM judgement, **not human gold**. |
| C07 | final resolved label: 56 of 100 negatives answerable (56%) | integer; 0 dp or 2 dp for the share | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.resolved_answerable_n']` (line 251), `results['c1.r3_3b.mf10.resolved_answerable_share']` (line 252) | `56` / `0.56` | the resolved label is two labellers plus one resolver; a **judged** label, not ground truth. |
| C08 | per-rung κ: R1 = 0.0, R2 = 0.2991, R3 = 0.026, R4 = 0.1379 (25 items per rung) | 4 dp (as the source publishes); 25 as an integer | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `results['c1.r3_3b.mf10.rung1.kappa']` (line 259), `rung2.kappa` (265), `rung3.kappa` (271), `rung4.kappa` (277); per-rung n at `results['c1.r3_3b.mf10.n_items_by_rung']` (line 237). Full precision only in `mf10.per_rung.{1..4}.kappa` (lines 99, 107, 115, 123) | flat keys `0.0` / `0.2991` / `0.026` / `0.1379`; `mf10.per_rung` `0.0` / `0.29906542056074775` / `0.025974025974026038` / `0.13793103448275895`; counts `{'1': 25, '2': 25, '3': 25, '4': 25}` | 25 items per rung: per-rung κ is unstable and must never be quoted without "n = 25". The spread is **not** a hardness ordering. |
| C09 | the earlier R3-3 adjudication had κ 0.1975 and 5 of 100 (5%) resolved answerable | 4 dp; integer; 0 dp | `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `mf10.comparison_with_prior_llm_adjudication.prior_kappa`, `.prior_resolved_answerable_n`, `.prior_resolved_answerable_share` (block opens line 217) | `0.1975` / `5` / `0.05` | **cautious comparison only**: different labeller and resolver models and GPU-first provenance — not a like-for-like replication, and not a "κ improved" claim. |
| C10 | frozen-run held-out AUROC 0.9824, 95% CI [0.9776, 0.9867] | 4 dp (0.982 acceptable at 3 dp) | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `results['c1.r3_3b.mf17.frozen_heldout_auroc.point']` (line 1256), `.ci95_lo` (1255), `.ci95_hi` (1254) | `0.9823630831643002` / `0.9776211411662427` / `0.9866543835742593` | exploratory/post-hoc interval around a **frozen** point estimate; no model retrained, no frozen verdict revised. AUROC is threshold-free ranking — **not accuracy**, and on its own says nothing about how many questions the gate answers. |
| C11 | spec-corrected held-out AUROC 0.8738, 95% CI [0.8587, 0.8893] | 4 dp (0.874 acceptable at 3 dp) | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `results['c1.r3_3b.mf17.corrected_heldout_auroc.point']` (line 1180), `.ci95_lo` (1179), `.ci95_hi` (1178) | `0.8738488843813388` / `0.8586833140203312` / `0.8893003500532195` | spec-corrected exploratory (post-hoc, deviation D4); not a confirmatory result. |
| C12 | paired difference (frozen − corrected) 0.1085, 95% CI [0.0946, 0.1225]; the interval excludes zero | 4 dp | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `results['c1.r3_3b.mf17.paired_auroc_diff.diff']` (line 1397), `.ci95_lo` (1396), `.ci95_hi` (1395); `contains_zero` is **inside** the nested dict `results['c1.r3_3b.mf17.paired_auroc_diff']` (line 1380) | `0.10851419878296142` / `0.09458017350090517` / `0.12252082237972457` / `False` | there is **no** flat key ending `.contains_zero`; read the nested field. "Excludes zero" describes this interval — it is not a claim that the frozen run is better science. |
| C13 | 1,879 held-out items = 400 answerable (rung 0) + 1,479 negatives (rungs 1–4); 18 article clusters | integers (thousands separator when printed) | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `denominators.held_out_common.n_items`, `.n_positive_rung0`, `.n_negative_rungs1to4`, `.n_article_clusters` (block opens line 980) | `1879` / `400` / `1479` / `18` | the denominator every C10–C12 interval sits on; the 18 clusters are article titles, not items. |
| C13b | 10,000 item-level bootstrap resamples, seed 20261118 | integers | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | top-level `n_boot` (line 1053) and top-level `seed` (line 1660) — **not** under `denominators` | `10000` / `20261118` | **split of C13, not a new claim ID**: these two numbers are top-level file fields. Resampling is item-level; a cluster variant exists (`*_cluster` aliases) and must not be substituted. |
| C14 | lexical-surface gate on dev rung 1: AUROC 0.9762 | 4 dp (0.976 acceptable at 3 dp) | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `results['c1.r3_3b.mf7.gold_control.dev.r1.auroc_surface_lex']` (line 1896) | `0.9762` (the file itself stores only 4 dp) | exploratory/post-hoc control cell (dev × rung 1) out of a dev/test × R1–R4 grid; never a headline AUROC, and it is an audit AUROC, not the gate's. |
| C15 | adding the gold indicator gives AUROC 1.0 | 1 dp (1.000 acceptable) | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `results['c1.r3_3b.mf7.gold_control.dev.r1.auroc_plus_is_gold']` (line 1891) | `1.0` | **label-construction artefact, tautological**: in the registered items an answerable item always presents the gold paragraph and a negative never does. Not evidence the gate works, not evidence about rung hardness. |
| C16 | the gold indicator **alone**, oriented so that "answerable" scores higher, is AUROC 1.0; `is_gold` is a deterministic function of the label | 1 dp; boolean | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `results['c1.r3_3b.mf7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented']` (line 1889), `results['c1.r3_3b.mf7.gold_control.dev.r1.is_gold_deterministic_from_label']` (line 1906) | `1.0` / `True` | same column un-oriented is `auroc_is_gold_alone_raw` = `0.0` — an orientation artefact, **not** a second result. Always print the 1.0 with the word "tautological". |
| C17 | D3 (top-1 presented) pooled set: 655 hits, 145 misses of 800; lexical AUROC hit-vs-miss 0.7327 | integers; 4 dp | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `results['c1.r3_3b.mf7.d3_pooled.all.n_hit']` (line 1800), `.n_miss` (1801), `.auroc_surface_lex_hit_vs_miss` (1767); total `…all.n` = 800 | `655` / `145` / `0.7327` (total `800`) | **pooled rung = −1 only**. 0.7327 is hit-vs-miss discrimination — not abstain precision, not accuracy. |
| C18 | D3 split: dev 342 hits / 58 misses; test 313 hits / 87 misses | integers | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `results['c1.r3_3b.mf7.d3_pooled.dev.n_hit']` (line 1839), `.dev.n_miss` (1840), `.test.n_hit` (1887), `.test.n_miss` (1888) | `342` / `58` / `313` / `87` | split by dev/test, **not** by rung; still pooled rung = −1 inside each split. |
| C19 | there is no D3 per-rung R1–R3 estimate; D3 exists only as pooled rung = −1 hit/miss data | — (boolean and an integer) | `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `results['c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available']` (line 1848), `results['c1.r3_3b.mf7.d3_pooled.rungs_present_value']` (line 1849); prose `notes.d3_scope` (line 1757) | `False` / `-1` | **pooled rung = −1 only; no per-rung R1–R3 estimate exists and none may be quoted.** Do not compute one from the pooled file. |
| C20 | registered band, **frozen D1** run: R4 abstain precision **100.00%** | 2 dp percent | `04_experiments/results/c1/results_full.json` | `test.band_primary.per_rung.4.abstain_precision` — top-level `"test"` (line 489) → `"band_primary"` (490) → `"per_rung"` (495) → `"4"` (535) → `abstain_precision` (line 536) | `1.0` | **registered band (frozen, D1)** — the pre-registered operating point, and the arm H1 was registered on; it is saturated (see N2). |
| C21 | frozen **exploratory** band, as-run D1: R4 abstain precision **84.71%** | 2 dp percent | `04_experiments/results/c1/results_full.json` | `test.exploratory_band.per_rung.4.abstain_precision` — `"test"` (489) → `"exploratory_band"` (551) → `"per_rung"` (556) → `"4"` (596) → `abstain_precision` (line 597) | `0.8471` | **frozen exploratory (as-run, D1)**: the arm added by deviation D1. Never confirmatory, cannot rescue H1; do not present it as a clean operating point. |
| C22 | spec-corrected exploratory band, post-hoc **D4**: R4 abstain precision **12.53%** | 2 dp percent | `04_experiments/results/c1_corrected/results_full.json` | `test.exploratory_band.per_rung.4.abstain_precision` — `"test"` (line 392) → `"exploratory_band"` (454) → `"per_rung"` (459) → `"4"` (499) → `abstain_precision` (line 500) | `0.1253` | **spec-corrected exploratory (post-hoc, D4)** — the most honest picture of the gate's precision on corrected features, and it is *low*. Revises no frozen verdict. |
| C23 | the two runs' AUROCs (0.9824 vs 0.8738) are comparable even though their thresholds are not, because AUROC is threshold-free | 4 dp | `04_experiments/PREREGISTRATION.md` (the rule) plus the two AUROC rows | §10 **D4, item 3**, lines 262–264: "Thresholds are therefore not comparable between the two runs; AUROC is, because it is threshold-free." The numbers themselves are C10 and C11 | no stored value here (prose); the AUROCs are `0.9823630831643002` (C10) and `0.8738488843813388` (C11) | a **rule of comparison**, not a third measurement. Point at C10/C11 for the numbers; do not recompute their difference here (that is C12 = 0.1085). |
| N1 | H1's registered criterion: abstain precision non-increasing across rungs 1→4, **and** the rung-1 − rung-3 drop ≥ 15 points | 15 points as an integer | `04_experiments/PREREGISTRATION.md` | §1 "Question and hypotheses", **H1 (hardness monotonicity)**, lines 22–25 | n/a — criterion, not a measurement | frozen pre-registration text. Quote both limbs together; "≥ 15 points" alone is not H1, and it is a criterion, never a result. |
| N2 | at the registered operating point the fitted band is t_lo = 0.907, t_hi = 0.948 (single t = 0.939); 92.9% of dev items are refused below t_lo alone; dev over-refusal 0.755; "Every gate then reports abstain precision 1.00 in every rung, so H1 and H3 cannot be tested at that operating point" | thresholds 3 dp; 92.9% 1 dp; 0.755 3 dp | `04_experiments/PREREGISTRATION.md` | §10 deviation log, **D1**, heading line 165, paragraph lines 167–172 | n/a — prose | deviation text frozen 2026-11-03T05:27+05:30. This is the sentence that makes H1 **not exercisable**; it must accompany C20. |
| N3 | the exploratory arm "cannot rescue a hypothesis — the pre-registered verdict stands on the pre-registered gate" | — | `04_experiments/PREREGISTRATION.md` | §10 **D1, consequence 2**, lines 178–181 (quote at 180–181) | n/a — prose | the governing rule for every C21/C22 number: exploratory arms are reported, never promoted. |
| N4 | at the registered operating point the rung-1 − rung-3 comparison had no discordant pairs at all ("no discordant pairs (all differences zero)") | — | `04_experiments/results/c1/results_full.json` | `hypotheses.H1.sign_test.p_note` (line 364); companion fields in the same block: `n_eff` = 0, `p_value` = 1.0, `statistic` = null, `n_pairs` = 400 | string `"no discordant pairs (all differences zero)"` | the mechanical reason the sign test cannot reject: at precision 1.00 in every rung there is nothing to compare. Do not print a p-value as if a test ran. |
| N5 | all three R3-3b items are labelled exploratory / post-hoc and none revises a frozen verdict | — | `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` | header **lines 3–6**; the `**Label:**` line of each item — MF-17 lines 55–56, MF-10 lines 107–108, MF-7 lines 147–149 | n/a — prose | the label obligation that covers every C01–C19 row here. |
| N6 | R3-3b findings are **not yet in the draft** | — | `orchestration/HEAD-REVIEW.md` | **Checkpoint 11** (2026-11-19), line 94: "R3-3b values remain explicitly post-hoc and are not yet bound into the draft"; **Checkpoint 10** (2026-11-18), line 84: R3-3b "must not be bound by this lane" | n/a — prose | "not yet in the draft" is a factual status, not a hedge. Say it plainly. |
| N7 | MF-17's own limitation text: intervals are post-hoc/exploratory, no frozen verdict revised, and the gold-indicator column "is a label-construction artefact; its AUROC is not evidence about rung hardness" | — | `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `limitations` list (opens line 1045), **item 1** line 1046 and **item 5** line 1050; 5-item list, so 0-indexed `limitations[0]` and `limitations[4]` | `limitations[0]` = "All intervals are post-hoc/exploratory; no frozen verdict is revised."; `limitations[4]` = "The gold-indicator column is a label-construction artefact; its AUROC is not evidence about rung hardness." | the file's own words; quote them when the limit is stated in the pack rather than paraphrasing. |
| N8 | what Round 3 is: the round that answers all 44 round-2 must-fix items, keeping the honest negative-result framing | 44 as an integer | `sessions/R3/TRIAGE.md`, `orchestration/HEAD-REVIEW.md`, `sessions/R3/COMMON.md` | `sessions/R3/TRIAGE.md` **line 1** ("every round-2 must-fix item has exactly one owning lane") with the 44-row table MF-1…MF-44 (rows at lines 8–51); `HEAD-REVIEW.md` **Checkpoint 5**, line 46 ("Round 3 = answer all 44 round-2 must-fix items"); `COMMON.md` **§"What the project is"**, lines 6–11 | n/a — prose | 44 is a count of review items, not a result. |

**C13b is not a new claim ID.** It is an accepted split of C13 — the resampling config (`n_boot`, `seed`) lives at the
top level of `mf17_auroc_intervals.json`, not under `denominators` — and `CLAIM-INVENTORY.md` now lists `C13b` as an
accepted split of C13, so this row resolves against the inventory.

---

## 2. How to read a JSON key

The R3-3b evidence files and the two `results_full.json` files use **different key styles**, and the same
number often appears under several names. Read the `exact JSON key` column literally: the key listed there is
the canonical one for that claim.

1. **`mf10`, `mf17`, `mf7`: one flat dict of literal dotted strings.** `json.load(f)['results']` returns a
   single object whose keys *contain dots*. `results['c1.r3_3b.mf17.frozen_heldout_auroc.point']` is **one
   key**, not four nested dicts — do not try to walk it with four `[...]` lookups.
2. **One mixed case: C12.** `results['c1.r3_3b.mf17.paired_auroc_diff']` is a *nested dict* stored under a
   dot-named key, so read `results['c1.r3_3b.mf17.paired_auroc_diff']['contains_zero']`. **There is no flat
   key ending `.contains_zero`.**
3. **Alias families.** The same values also sit under `frozen_held_out_auroc.*` / `frozen_test_auroc.*`,
   `corrected_held_out_auroc.*` / `corrected_test_auroc.*`, `paired_auroc_diff_ci.*` / `paired_diff_auroc.*`,
   and the `*_cluster` (article-title cluster resampling) variants. `mf10` carries per-rung κ twice: the flat
   `rung{n}.kappa` key is **rounded to 4 dp**, `mf10.per_rung.{n}.kappa` is **full precision**. Cite the
   column's key; never mix an item-level and a `_cluster` number in one sentence.
4. **`results_full.json` is genuinely nested.** `test.band_primary.per_rung.4.abstain_precision` is a real
   path: `['test']['band_primary']['per_rung']['4']['abstain_precision']`, and the rung key is the **string**
   `"4"`. These files also contain *other* `"test"` blocks (e.g. inside `ablation_no_rank`, line 19), so a
   naive grep for `"test"` lands on the wrong one — the line numbers here point at the top-level block
   (line 489 in `c1`, line 392 in `c1_corrected`).
5. **`mf10` has a second, non-flat block also called `mf10`.** Run provenance — labeller models, the
   `exploratory_status` string (line 6), `agreement` (line 81), `per_rung` (line 95), `resolved` (line 151),
   `disagreement_resolution` (line 177), `comparison_with_prior_llm_adjudication` (line 217) — lives at the
   top level, **outside** `results`. C01, C03 and C09 need it.

## 3. Paths and hashes

The three R3-3b JSON files this map was checked against, with their sha256:

| file | sha256 (first 12) | full sha256 |
|---|---|---|
| `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `2324d8605534` | `2324d8605534defe245d37a1b8924e4a07c29dca0784b8b37aa2fae5d271c3b1` |
| `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `07c3a0f8a54f` | `07c3a0f8a54fc70c466bd8d26af59e0b424f62207217c06014c383ebb3158883` |
| `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `0728d92714d0` | `0728d92714d0a209a3ea9a99a2ad81d747d844b529cc2b96315da5e0238b1952` |

Also cited above, for completeness (not in the inventory's hash list):

| file | sha256 (first 12) |
|---|---|
| `04_experiments/results/c1/results_full.json` (frozen, D1) | `e4cf65cb0b2b` |
| `04_experiments/results/c1_corrected/results_full.json` (spec-corrected, D4) | `936ce0b89e22` |

Line numbers in the table are 1-based and refer to these exact bytes. If a file changes, this map is stale
and must be re-checked before any number is printed.

## 4. Known exclusions

- **90.73% is deliberately not used anywhere in the student pack.**
  `04_experiments/results/c1_corrected/results_full.json` → `test.band_primary.per_rung.4.abstain_precision`
  (line 439) stores `0.9073`. It is the spec-corrected **registered** band. Quoting it would force a fourth
  operating point into a two-page digest and a beginner viva answer, and its label (registered threshold
  rule re-fitted on corrected features) fits neither run label the pack uses. Do not introduce it, do not
  footnote it, do not mention it in passing.
- **No number in this map may be re-derived or re-rounded by a writer.** The `value as printed` column is the
  only permitted rendering. A writer may not compute a percentage from a share, a difference from two AUROCs
  (that is C12, and it is stored), a percentage-point change, an average across rungs, or a "nicer" rounded
  form such as 0.28 for κ or 84.7% for C21.
- **Only C03 is derived**, and wherever it appears it must be labelled "derived from C01 and C02".
- **No per-rung D3 number exists** (C19). A "D3 by rung" table would be fabricated.
- **No frozen value is presented here as an R3-3b finding**, and no frozen verdict is revised by any row in
  this map (N5, N6, N7).
- Symbols and words, not numbers, carry the limits: "exploratory / post-hoc", "not human gold",
  "tautological", "not yet in the draft", "not exercisable at the registered operating point". A limit stated
  only as a number is not a limit.
