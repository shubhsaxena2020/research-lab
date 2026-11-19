# CLAIM INVENTORY (canonical) — R3-6b student pack

Written by the LEAD after parsing each source file with `python`/`json.load` on 2026-11-19.
Every row below was printed from the file named in the `source` column; nothing is copied from a brief.
All three student files (ROUND3-DIGEST.md, VIVA-QA.md, SOURCE-MAP.md) MUST use these exact IDs.
Do not invent IDs, do not renumber, do not add numbers that are not in this table.

Paths are relative to `C:\Users\shubh\research-lab`.

- `MF10` = `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` (sha256 2324d8605534…)
- `MF17` = `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` (sha256 07c3a0f8a54f…)
- `MF7`  = `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` (sha256 0728d92714d0…)
- `C1`   = `04_experiments/results/c1/results_full.json` (frozen, D1)
- `C1C`  = `04_experiments/results/c1_corrected/results_full.json` (spec-corrected, exploratory, D4)
- `ANS`  = `04_experiments/results/c1/r3/R3-3b/ANSWERS.md`
- `PREREG` = `04_experiments/PREREGISTRATION.md`
- `HEAD` = `orchestration/HEAD-REVIEW.md`

In `key` columns, `results[…]` means the top-level `results` object of that JSON.

## A. MF-10 — repeated LLM answerability adjudication (post-hoc / exploratory)

| ID | Claim (as it may appear) | source | key | exact value | rounding |
|---|---|---|---|---|---|
| C01 | Cohen's kappa between the two LLM labellers = 0.2802 | MF10 | `results['c1.r3_3b.mf10.cohen_kappa_overall']` (full precision also `mf10.agreement.kappa`) | 0.2802 (0.2801966292134831) | 4 dp / 3 dp |
| C02 | observed (raw) agreement 0.59, i.e. 59 of 100 items | MF10 | `results['c1.r3_3b.mf10.raw_agreement_po']`, `…['c1.r3_3b.mf10.n_agreed']`, `…['c1.r3_3b.mf10.n_items']` | 0.59; 59; 100 | 2 dp; integer |
| C03 | chance-level agreement implied by the marginals is about 0.43 (43%) | DERIVED from C01+C02 by kappa = (Po − Pe)/(1 − Pe); lead-computed 0.4304 | — (derived, not a stored key; must be labelled "derived from C01 and C02") | 0.4304 | 2 dp |
| C04 | the two labellers disagreed on 41 of 100 items | MF10 | `results['c1.r3_3b.mf10.n_disagreed']` | 41 | integer |
| C05 | labeller A called 62 items answerable, labeller B called 21 | MF10 | `results['c1.r3_3b.mf10.labeller_A_answerable_n']`, `…['c1.r3_3b.mf10.labeller_B_answerable_n']` | 62; 21 | integer |
| C06 | on the 41 disagreements the strict resolver decided 35 answerable, 6 not answerable, 0 ambiguous | MF10 | `results['c1.r3_3b.mf10.resolver_resolved_1_n']`, `…_0_n`, `…_ambiguous_n` | 35; 6; 0 | integer |
| C07 | final resolved label: 56 of 100 negatives answerable (56%) | MF10 | `results['c1.r3_3b.mf10.resolved_answerable_n']`, `…['c1.r3_3b.mf10.resolved_answerable_share']` | 56; 0.56 | integer; 0 dp / 2 dp |
| C08 | per-rung kappa: R1 = 0.0, R2 = 0.2991, R3 = 0.026, R4 = 0.1379 (25 items per rung) | MF10 | `results['c1.r3_3b.mf10.rung1.kappa']` … `rung4.kappa`; `…mf10.n_items_by_rung` | 0.0; 0.2991; 0.026; 0.1379; 25 each | 4 dp; integer |
| C09 | the earlier R3-3 adjudication had kappa 0.1975 and 5 of 100 (5%) resolved answerable | MF10 | `mf10.comparison_with_prior_llm_adjudication.prior_kappa`, `.prior_resolved_answerable_n`, `.prior_resolved_answerable_share` | 0.1975; 5; 0.05 | 4 dp; integer; 0 dp |

Support limit for A (must accompany any of C01–C09): these are LLM judgements, **NOT human gold**
(`mf10.exploratory_status` = "post-hoc / exploratory repeated LLM judgement; NOT human gold"), post-hoc,
and they revise no frozen verdict. The two runs used different resolver models and different provenance,
so C09 is a cautious comparison only, not a like-for-like replication.

## B. MF-17 — post-hoc AUROC intervals and the paired difference

| ID | Claim (as it may appear) | source | key | exact value | rounding |
|---|---|---|---|---|---|
| C10 | frozen-run held-out AUROC 0.9824, 95% CI [0.9776, 0.9867] | MF17 | `results['c1.r3_3b.mf17.frozen_heldout_auroc.point']`, `.ci95_lo`, `.ci95_hi` | 0.9823630831643002; 0.9776211411662427; 0.9866543835742593 | 4 dp / 3 dp |
| C11 | spec-corrected held-out AUROC 0.8738, 95% CI [0.8587, 0.8893] | MF17 | `results['c1.r3_3b.mf17.corrected_heldout_auroc.point']`, `.ci95_lo`, `.ci95_hi` | 0.8738488843813388; 0.8586833140203312; 0.8893003500532195 | 4 dp / 3 dp |
| C12 | paired difference (frozen − corrected) 0.1085, 95% CI [0.0946, 0.1225], interval excludes zero | MF17 | `results['c1.r3_3b.mf17.paired_auroc_diff.diff']`, `.ci95_lo`, `.ci95_hi`; nested `results['c1.r3_3b.mf17.paired_auroc_diff']['contains_zero']` | 0.10851419878296142; 0.09458017350090517; 0.12252082237972457; false | 4 dp |
| C13 | intervals use 1,879 held-out items (400 answerable at rung 0 + 1,479 negatives across rungs 1–4), 18 article clusters, 10,000 item-level percentile bootstrap resamples, seed 20261118 | MF17 | `denominators.held_out_common`; top-level `seed`; top-level `n_boot` | 1,879; 400; 1,479; 18; 10,000; 20261118 | integer |
| C13b | (accepted split of C13, **not** a new claim) 10,000 item-level bootstrap resamples, seed 20261118 | MF17 | top-level `n_boot`, top-level `seed` — not under `denominators` | 10000; 20261118 | integer |

Support limit for B: post-hoc / exploratory (`exploratory: true`, `post_hoc: true`); no model retrained;
no frozen verdict revised. An AUROC is threshold-free and ranks items; it is not an accuracy and says
nothing on its own about how many questions the gate answers.

## C. MF-7 — gold-indicator control and D3 pooled hit/miss

| ID | Claim (as it may appear) | source | key | exact value | rounding |
|---|---|---|---|---|---|
| C14 | lexical-surface gate on dev rung 1: AUROC 0.9762 | MF7 | `results['c1.r3_3b.mf7.gold_control.dev.r1.auroc_surface_lex']` | 0.9762 | 4 dp |
| C15 | adding the gold indicator gives AUROC 1.0 | MF7 | `results['c1.r3_3b.mf7.gold_control.dev.r1.auroc_plus_is_gold']` | 1.0 | 1 dp |
| C16 | the gold indicator *alone*, oriented so that "answerable" scores higher, is AUROC 1.0; `is_gold` is a deterministic function of the label | MF7 | `results['c1.r3_3b.mf7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented']`, `…dev.r1.is_gold_deterministic_from_label` | 1.0; true | 1 dp; boolean |
| C17 | the D3 (top-1 presented) pooled set: 655 hits, 145 misses of 800; lexical AUROC hit-vs-miss 0.7327 | MF7 | `results['c1.r3_3b.mf7.d3_pooled.all.n_hit']`, `.n_miss`, `.n`, `.auroc_surface_lex_hit_vs_miss` | 655; 145; 800; 0.7327 | integer; 4 dp |
| C18 | D3 split: dev 342 hits / 58 misses, test 313 hits / 87 misses | MF7 | `results['c1.r3_3b.mf7.d3_pooled.dev.n_hit']`, `.dev.n_miss`, `.test.n_hit`, `.test.n_miss` | 342; 58; 313; 87 | integer |
| C19 | there is no D3 per-rung R1–R3 estimate; D3 exists only as pooled rung = −1 hit/miss data | MF7 | `results['c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available']` (false), `results['c1.r3_3b.mf7.d3_pooled.rungs_present_value']` (−1); prose `notes.d3_scope` | false; −1 | — |

Support limit for C: C15 and C16 are a **construction / label artefact**, not evidence about rung
hardness and not evidence that the gate works — in the registered items an answerable item always
presents the gold paragraph and a negative never does, so `is_gold` restates the label. C17–C19 are
pooled (rung = −1) only; no per-rung R1–R3 D3 numbers exist and none may be quoted.

## D. MF-14 — registered versus exploratory R4 abstain precision (run labels are binding)

| ID | Claim (as it may appear) | source | key | exact value | rounding |
|---|---|---|---|---|---|
| C20 | registered band, frozen D1 run: R4 abstain precision 100.00% | C1 | `test.band_primary.per_rung.4.abstain_precision` (= `c1.band.precision.r4.run`) | 1.0 | 100.00% |
| C21 | frozen exploratory band, as-run D1: R4 abstain precision 84.71% | C1 | `test.exploratory_band.per_rung.4.abstain_precision` (= `c1.expl.precision.r4.run`) | 0.8471 | 84.71% |
| C22 | spec-corrected exploratory band, post-hoc D4: R4 abstain precision 12.53% | C1C | `test.exploratory_band.per_rung.4.abstain_precision` (= `c1.expl.precision.r4.corr`) | 0.1253 | 12.53% |
| C23 | the two runs' AUROCs are comparable (0.9824 vs 0.8738) even though their thresholds are not, because AUROC is threshold-free | PREREG §10 D4 item 3; C10/C11 values | PREREG lines "Thresholds are therefore not comparable between the two runs; AUROC is, because it is threshold-free" | 0.9824; 0.8738 | 4 dp |

Deliberately **not** used in the student pack: 90.73% (`C1C test.band_primary.per_rung.4.abstain_precision`),
so that no writer has to label a third operating point. Do not introduce it.

Support limit for D: C20 is the registered (frozen) number; C21 is exploratory and was the arm added by
deviation D1 — it may never be presented as the registered or confirmatory number, and it may not be
described as "clean". C22 is post-hoc deviation D4 and the most honest picture of the gate's precision on
corrected features. Over-refusal figures (9.50% on the as-run exploratory arm, 11.00% on the spec-corrected
arm, both held-out) are **not** part of this pack's claim set: no writer may assert a cap breach or cap
compliance for C21/C22, because those keys are deliberately not in this inventory. None of C20–C22 revises
a frozen verdict, and none is yet in the draft (N6).

## E. Non-result facts (cite the precise section/line, not a JSON key)

| ID | Fact | source | where exactly |
|---|---|---|---|
| N1 | H1's registered criterion: abstain precision non-increasing across rungs 1→4, and the rung-1 minus rung-3 drop ≥ 15 points | PREREG | §1 "H1 (hardness monotonicity)", lines 22–25 |
| N2 | At the registered operating point the fitted band is t_lo = 0.907, t_hi = 0.948 (single t = 0.939); 92.9% of dev items are refused below t_lo alone; dev over-refusal 0.755; "Every gate then reports abstain precision 1.00 in every rung, so H1 and H3 cannot be tested at that operating point" | PREREG | §10 D1, lines 165–172 |
| N3 | The exploratory arm "cannot rescue a hypothesis — the pre-registered verdict stands on the pre-registered gate" | PREREG | §10 D1, consequence 2 |
| N4 | At the registered operating point the rung-1 − rung-3 comparison had no discordant pairs at all ("no discordant pairs (all differences zero)") | C1 | `hypotheses.H1.sign_test.p_note` |
| N5 | All three R3-3b items are labelled exploratory / post-hoc and none revises a frozen verdict; the MF-10 labels are explicitly **not human gold** | ANS; MF10 | ANS header (lines 3–6) and the "Label:" line of each item; `mf10.exploratory_status` = "post-hoc / exploratory repeated LLM judgement; NOT human gold" |
| N6 | R3-3b findings are not yet in the draft | HEAD | Checkpoint 11 (2026-11-19): "R3-3b values remain explicitly post-hoc and are not yet bound into the draft"; Checkpoint 10: R3-3b "must not be bound by this lane" |
| N7 | MF-17's own limitation text: intervals are post-hoc/exploratory, no frozen verdict revised, no model retrained, and the gold-indicator column "is a label-construction artefact; its AUROC is not evidence about rung hardness" | MF17 | `limitations` list, items 1, 2 and 5 |
| N8 | What Round 3 is: the round that answers all 44 round-2 must-fix items, keeping the honest negative-result framing | HEAD / TRIAGE | `sessions/R3/TRIAGE.md` header ("every round-2 must-fix item has exactly one owning lane"; 44 rows MF-1…MF-44); HEAD Checkpoint 5 ("Round 3 = answer all 44 round-2 must-fix items"); `sessions/R3/COMMON.md` §"What the project is" |

## F. Required framing sentences (verbatim obligations, not numbers)

1. Every R3-3b finding is **exploratory / post-hoc** and **not yet in the draft**.
2. κ = 0.2802 is **modest agreement beyond chance between these two LLM labellers** — not accuracy,
   not agreement with a human, not a measure of whether the labels are true.
3. The gold-indicator AUROC of 1.0 is **tautological**: the indicator is a deterministic function of the
   label.
4. D3 is **pooled rung = −1** hit/miss data and has **no per-rung R1–R3 estimate**.
5. H1 was **not exercisable at the registered operating point**; it must not be called confirmed or
   refuted on the strength of any exploratory ordering.
6. MF-14 must be given with its run labels: registered band (frozen, D1) / frozen exploratory (as-run,
   D1) / spec-corrected exploratory (post-hoc, D4).
7. No frozen verdict is revised by anything in this pack.
