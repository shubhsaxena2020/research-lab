# ANSWERS — R3-3b deferred analyses (MF-17, MF-10, MF-7)

Lane: R3-3b. All three items are **exploratory / post-hoc**; none revises a
frozen verdict. Result keys below are the exact bindable keys in each JSON's
top-level `results` object (verified by parsing the files). Prefix for every
key is `c1.r3_3b.<item>.`.

---

## MF-17 — post-hoc 95% AUROC intervals + paired difference (0.982 → 0.874)

**Evidence file:** `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json`
(`results` has 111 keys, all prefixed `c1.r3_3b.mf17.`; supporting top-level
fields `alignment_assertions`, `denominators`, `limitations`, `resampling`).

**Bindable result keys (`results[...]`):**

| key | value |
|---|---|
| `c1.r3_3b.mf17.frozen_heldout_auroc.point` | 0.9823630831643002 |
| `c1.r3_3b.mf17.frozen_heldout_auroc.ci95_lo` | 0.9776211411662427 |
| `c1.r3_3b.mf17.frozen_heldout_auroc.ci95_hi` | 0.9866543835742593 |
| `c1.r3_3b.mf17.corrected_heldout_auroc.point` | 0.8738488843813388 |
| `c1.r3_3b.mf17.corrected_heldout_auroc.ci95_lo` | 0.8586833140203312 |
| `c1.r3_3b.mf17.corrected_heldout_auroc.ci95_hi` | 0.8893003500532195 |
| `c1.r3_3b.mf17.paired_auroc_diff.diff` | 0.10851419878296142 |
| `c1.r3_3b.mf17.paired_auroc_diff.ci95_lo` | 0.09458017350090517 |
| `c1.r3_3b.mf17.paired_auroc_diff.ci95_hi` | 0.12252082237972457 |
| `c1.r3_3b.mf17.top1_auroc.point` | 0.9452829495795234 |
| `c1.r3_3b.mf17.transfer_auroc_frozen.point` | 0.6401749999999999 |
| `c1.r3_3b.mf17.transfer_auroc_corrected.point` | 0.7058749999999999 |
| `c1.r3_3b.mf17.audit_lex_overlap_auroc.point` | 0.9772812500000001 |
| `c1.r3_3b.mf17.gold_indicator_control_auroc.point` | 1.0 |

Nested (not flattened) field: `results['c1.r3_3b.mf17.paired_auroc_diff']['contains_zero'] = false`.
There is **no** flattened key ending in `.contains_zero`; the same nested field
also exists on `.paired_auroc_diff_ci`, `.paired_auroc_diff_cluster`, and
`.paired_diff_auroc`. Alias families with identical values also present:
`.frozen_held_out_auroc.*` / `.frozen_test_auroc.*`, `.corrected_held_out_auroc.*`
/ `.corrected_test_auroc.*`, `.paired_auroc_diff_ci.*` / `.paired_diff_auroc.*`,
and the `*_cluster` variants (article-title cluster resampling).

**Verdict / support limit:** Exploratory 95% percentile-bootstrap intervals
(item-level, 10,000 resamples, seed 20261118) around held-out AUROCs: frozen
0.9824 [0.9776, 0.9867], corrected 0.8738 [0.8587, 0.8893]. The paired
difference on the same 1,879 items is 0.1085 [0.0946, 0.1225] and **excludes
zero** (`contains_zero = false`). Held-out AUROCs use all test rows from
`band_score` in existing predictions; no model is retrained. The
gold-indicator control (AUROC 1.0) is a label-construction artefact, not
evidence about rung hardness. **No frozen verdict is revised.**

**Reproduce:** `python 04_experiments/src/r3_r3_3b_mf17.py`
(check: `python 04_experiments/src/r3_r3_3b_mf17.py --check-repro`).

**Label:** exploratory / post-hoc (`exploratory: true`, `post_hoc: true`,
`label: "exploratory/post-hoc"`).

---

## MF-10 — repeated LLM answerability adjudication (κ = 0.2802)

**Evidence file:** `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json`
(`results` has 40 keys; the `mf10` block holds run provenance and the prior-run
comparison).

**Bindable result keys (`results[...]`):**

| key | value |
|---|---|
| `c1.r3_3b.mf10.cohen_kappa_overall` | 0.2802 |
| `c1.r3_3b.mf10.raw_agreement_po` | 0.59 |
| `c1.r3_3b.mf10.n_items` | 100 |
| `c1.r3_3b.mf10.n_agreed` | 59 |
| `c1.r3_3b.mf10.n_disagreed` | 41 |
| `c1.r3_3b.mf10.labeller_A_answerable_n` | 62 |
| `c1.r3_3b.mf10.labeller_B_answerable_n` | 21 |
| `c1.r3_3b.mf10.resolver_on_disagreements_n` | 41 |
| `c1.r3_3b.mf10.resolver_resolved_1_n` | 35 |
| `c1.r3_3b.mf10.resolver_resolved_0_n` | 6 |
| `c1.r3_3b.mf10.resolver_resolved_ambiguous_n` | 0 |
| `c1.r3_3b.mf10.resolved_answerable_n` | 56 |
| `c1.r3_3b.mf10.resolved_answerable_share` | 0.56 |
| `c1.r3_3b.mf10.rung1.kappa` | 0.0 |
| `c1.r3_3b.mf10.rung2.kappa` | 0.2991 |
| `c1.r3_3b.mf10.rung3.kappa` | 0.026 |
| `c1.r3_3b.mf10.rung4.kappa` | 0.1379 |

(Also `c1.r3_3b.mf10.rung{1..4}.{n, n_disagreed, A_answerable_n,
B_answerable_n, resolved_answerable_n}`, `c1.r3_3b.mf10.n_items_by_rung`,
`labeller_{A,B}_answerable_share`. Full-precision κ = 0.2801966292134831 is in
`mf10.agreement.kappa`.)

**Verdict / support limit:** Repeated LLM judgement on the existing 100 seeded
rung-1–4 negatives (two independent labellers A/B plus a strict resolver on
disagreements): Cohen's κ = 0.2802, observed agreement 0.59, **41
disagreements**, strict resolver resolved **56/100 (56%) answerable**. These are
**NOT human gold labels** (`mf10.exploratory_status`); compare **cautiously**
with the prior adjudication in `04_experiments/results/c1/r3/exp/adjudication/
adjudication.json` (prior κ = 0.1975, strict resolver 5/100 = 5%; see
`mf10.comparison_with_prior_llm_adjudication`) — different models, resolver and
GPU-first provenance, so the two runs are not directly interchangeable. No
frozen verdict is revised.

**Reproduce:** `python 04_experiments/src/r3_r3_3b_mf10.py`
(uses the existing sample; Ollama at 127.0.0.1:11434; resume supported).

**Label:** exploratory / post-hoc (`mf10.post_hoc_exploratory: true`,
`mf10.exploratory_status: "post-hoc / exploratory repeated LLM judgement; NOT human gold"`).

---

## MF-7 — gold-indicator control and D3 pooled hit/miss sanity check

**Evidence file:** `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json`
(`results` has 294 keys; supporting fields `notes`, `denominators`,
`bootstrap_validation`).

**Bindable result keys (`results[...]`):**

| key | value |
|---|---|
| `c1.r3_3b.mf7.gold_control.dev.r1.auroc_surface_lex` | 0.9762 |
| `c1.r3_3b.mf7.gold_control.dev.r1.auroc_plus_is_gold` | 1.0 |
| `c1.r3_3b.mf7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented` | 1.0 |
| `c1.r3_3b.mf7.gold_control.dev.r1.is_gold_deterministic_from_label` | true |
| `c1.r3_3b.mf7.d3_pooled.all.n_hit` | 655 |
| `c1.r3_3b.mf7.d3_pooled.all.n_miss` | 145 |
| `c1.r3_3b.mf7.d3_pooled.all.auroc_surface_lex_hit_vs_miss` | 0.7327 |
| `c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available` | false |
| `c1.r3_3b.mf7.d3_pooled.rungs_present_value` | -1 |

Same gold-control pattern (`auroc_plus_is_gold = 1.0`,
`is_gold_deterministic_from_label = true`) across dev/test × rungs R1–R4;
D3 splits: `d3_pooled.dev.n_hit = 342`, `.n_miss = 58`; `d3_pooled.test.n_hit =
313`, `.n_miss = 87`.

**Verdict / support limit:** The gold indicator is a **construction artefact**:
`is_gold` is a deterministic function of the label (answerable always presents
the gold paragraph, negatives never do), so AUROC = 1.0 is **tautological** and
cannot exculpate the gate. D3 (top1_presented) has **only rung = −1 pooled**
hit/miss observations (655/145 all); there is **no D3 per-rung R1–R3 estimand**
(`per_rung_R1_R3_estimand_available = false`) — all D3 numbers are pooled. No
frozen verdict is revised.

**Reproduce:** `python 04_experiments/src/r3_r3_3b_mf7.py`.

**Label:** exploratory / post-hoc (`exploratory: true`, `post_hoc: true`,
`label: "exploratory/post-hoc"`, `lane: "R3-3b-deferred-analyses"`;
`notes.label: "exploratory / post-hoc; no frozen verdict is revised."`).
