# Round comparison - 06_review/reviews/round2-c1 -> 06_review/reviews/round3-c1 / current draft

- Generated: 2026-11-18 (regenerated with real round-3 scores and decisions)
- Reviews: round 2 = 6 personas (mean overall 4.67/10, 3 reject / 3 borderline / 0 accept, 44 must-fix); round 3 = 6 personas (mean overall 5.67/10, 0 reject / 6 borderline / 0 accept, 41 must-fix)
- Distinct must-fix items: round 2 = 44, round 3 = 41
- Draft under revision: `05_paper/draft/paper.md` (round-3 draft sha256 `9194a481c8c0`)
- Round-3 sources: `06_review/reviews/round3-c1/AGGREGATE.md`, `06_review/reviews/round3-c1/INGEST.md`

> **Timing note (R3-4c-fold).** Round 3 reviewed the *pre-fold* draft (sha256 `9194a481c8c0`). All fold edits made in R3-4c-fold are *post-review*: they do not invalidate the round-3 scores, which remain diagnostics on the pre-fold draft. No new review round was run.

> Round 3 is now ingested (6/6 personas, none missing). Real scores and decisions above.
> "Resolved / Partial / Deferred" below describe the current draft against the
> round-2 must-fix list (unchanged: 18 / 21 / 5). "Persisted" and "New in round 3"
> classify the 41 round-3 must-fix items against round-2 themes.

## Totals

| Metric | Round 2 | Round 3 | Delta |
|---|---:|---:|---:|
| Mean overall (1-10) | 4.67 | 5.67 | +1.00 |
| Reject / borderline / accept | 3 / 3 / 0 | 0 / 6 / 0 | -3 reject, +3 borderline |
| Must-fix items (distinct) | 44 | 41 | -3 |
| Resolved (draft contains change) | - | 18 | - |
| Partial (evidence exists, draft incomplete/stale) | - | 21 | - |
| Deferred (evidence exists, not folded) | - | 5 | - |
| Persisted (raised again in round 3) | - | 22 | - |
| New in round 3 | - | 19 | - |

**Headline: mean rose from 4.67 to 5.67; all six personas now borderline (0 rejects); 22 of 41 round-3 must-fix items overlap round-2 themes, 19 are new.**

## Per-persona overall score

| Persona | Round 2 overall | Round 2 decision | Round 3 overall | Round 3 decision |
|---|---:|---|---:|---|
| methodologist | 5 | borderline | 5 | borderline |
| domain_expert | 4 | reject | 6 | borderline |
| statistician | 5 | borderline | 6 | borderline |
| novelty_skeptic | 4 | reject | 6 | borderline |
| reproducibility_reviewer | 6 | borderline | 5 | borderline |
| clarity_reviewer | 4 | reject | 6 | borderline |
| **Mean** | **4.67** | - | **5.67** | - |

Round-2 detail: soundness 2.17, presentation 2.67, contribution 2.33, confidence 4.00.
Round-3 detail: soundness 2.67, presentation 3.00, contribution 3.00, confidence 4.00.

## Resolved in current draft (18)

These items have the change visible in `05_paper/draft/paper.md` with the section evidence below.
Round-3 confirmation (reviewer not re-raising) is still outstanding for all of them.

| # | Reviewer (round 2) | Claim (short) | Draft evidence |
|---:|---|---|---|
| MF-1 | methodologist | abstain precision = refusal rate | §3.5 defines refusal rate P(refused\|negative) vs precision P(negative\|refused); Abstract pooled 83.03%; §4.2 gives R1 56.98%, R2 48.02% |
| MF-2 | methodologist | Table 4 two runs, different operating points | Table 6 prints frozen vs corrected thresholds 0.9072/0.9478 vs 0.5232/0.5370 and exploratory coverage 25.44% -> 39.60%; AUROC flagged as only threshold-free row |
| MF-8 | domain_expert | never reports abstention precision | Table 3 reports per-rung precision + pooled (1478/1780 = 83.03%); §3.5 states definition with counts |
| MF-11 | domain_expert | one axis at a time contradicted | §3.1 rewritten "one respect at a time — but not in only one respect"; R5 overlap matching mean_absdiff 10.29% vs random 42.08% |
| MF-14 | domain_expert | R4 conclusion on one post-hoc cell | Table 6 reports registered 84.71% beside corrected 12.53% for R4; §5.2 restricted to corrected-run reading |
| MF-15 | statistician | cells are refusal rates, not pooled precision | §3.5 + Table 3 note give both formulas with counts (R1 400/400, R2 279/280; dev precision 0.8369 at 1760/1873; pooled 83.03%) |
| MF-20 | statistician | 11.00% over-refusal vs 0.10 cap | §4.6 states cap binds on dev (0.095, not breached) and held-out 0.11 breaches it — breach reported, not hidden |
| MF-26 | novelty_skeptic | ladder of lexical overlap = ordering | Abstract/§4.1/§5.2 rewritten to "overlap separates each rung" with R2 91.07% vs R3 92.75% inversion and R5 89.25% stated |
| MF-27 | novelty_skeptic | §4.4 R5 ordering misstated | §4.4 now "between R2 (91.07%) and R4 (84.71%)" |
| MF-33 | reproducibility_reviewer | §8 omits transfer/reader commands | §8 lists `build_transfer_items.py` and `reader_logprob.py` before their consumers |
| MF-34 | reproducibility_reviewer | Table 4 header labels frozen as D1 | Table 6 columns "Frozen run" / "Spec-corrected (D4)" with both threshold pairs printed |
| MF-35 | reproducibility_reviewer | no numbered/captioned tables; refs wrong | Tables 1–7 numbered + captioned in appearance order; §4.2 "(§4.5)" and §2 "(§4.8)" refs corrected |
| MF-38 | clarity_reviewer | abstract mixes denominators | Abstract now one population: 24.50% of questions asked (98/400); §5.1 "about one question in four (24.50%)" |
| MF-39 | clarity_reviewer | abstain precision undefined | §3.5 one-sentence definition with numerator/denominator; R2 279/(279+302) = 48.02% |
| MF-40 | clarity_reviewer | tables unnumbered/uncaptioned | All seven tables sequentially numbered with self-contained captions; in-text refs rewritten |
| MF-41 | clarity_reviewer | no figure in draft | Figure 1 (F1_abstain_precision_by_rung.svg) + Figure 2 (F2_precision_overrefusal_vs_coverage.svg) inlined with captions |
| MF-42 | clarity_reviewer | two wrong cross-references | Dense-column pointer -> §4.6, reader-baseline pointer -> §4.7 (checked against reporting sections) |
| MF-43 | clarity_reviewer | arm table wrong conditional | §4.5 + Table 5 give both: P(refused\|miss) = 63.22% (55/87) and P(miss\|refused) = 87.30% (55/63) |

## Partial (21) — evidence exists, draft incomplete or stale

| # | Reviewer (round 2) | What's done | What's still missing in draft |
|---:|---|---|---|
| MF-3 | methodologist | Frozen R5/transfer labelled by run in §4.4/§4.8 | Corrected R5 93.75% and transfer 97.50% at AUROC 0.706 (in `both_runs.json`) are NOT in draft; draft only cites frozen |
| MF-4 | methodologist | D4 in `PREREGISTRATION.md` §10 + 5-line hash chain (tip 83d5b31f) | Draft front-matter still says "three recorded hashes … D1–D3"; D5 post-hoc timing not quoted in draft |
| MF-5 | methodologist | Abstract/§4.2 prose now "criterion not exercisable …" with exploratory 7.00pt [4.50, 9.75] | Table 4 verdict column still prints "REFUTED" for H1/H3 — prose/table inconsistent |
| MF-6 | methodologist | §4.8 gives explicit "inconclusive by the registered rule" + 7.25pt drop | Corrected arm (−2.0pt REFUTED) and per-arm recalls (57.50% vs 9.50%) not in draft; "inconclusive" ≠ verbatim UNDEFINED |
| MF-9 | domain_expert | Question-level coverage 24.50% (98/400) in Abstract/§5.1 | AURCC / abstention F1 not added (metrics ANSWERS: "not added this round"); item-level 5.27% only in Table 6 |
| MF-12 | domain_expert | §4.7 narrows fluency-proxy claim ("do not use it to rank gates") | New P(True)-style result (AUROC 0.232 inverted, 0.80 infeasible) not folded; model difference not stated in draft |
| MF-13 | domain_expert | §3.4 notes audit is one-sided, R4 0.415 reported as reverse separation | No two-sided |AUROC−0.5| rule with CIs; new audit values (R4 0.407, top-1 0.504/0.571) not in draft |
| MF-16 | statistician | §3.6 flags zero-width intervals as boundary, not certainty | Discordant counts (0/400, 0/1479), Clopper-Pearson/Wilson bounds, BCa-vs-percentile reconciliation not in draft |
| MF-18 | statistician | §4.7 gives width ratios 0.45 / 1.17 (corrected from 0.851) | n_articles = 18 not stated; rung-1/rung-3 cluster intervals [1.00, 1.00] not shown |
| MF-19 | statistician | §4.6 notes corrected matched single's dev precision < 0.80 (descriptive, not a retest) | Corrected recalls (0.9898/0.9925), dev precision 0.7886, re-matched diff −0.0169 [−0.0264, −0.0074] not in draft |
| MF-21 | statistician | §4.6 adds "point estimates without intervals cannot establish equivalence" caveat | Paired CIs (all_12 vs no_dense 0.0116 [0.0038, 0.0196] excludes zero!) not folded; last sentence still claims "No single group carries" — contradicted by evidence |
| MF-22 | statistician | §4.7 gives dev 273/127 and min p = 0.052 | Held-out 280/120 counts and per-variable p-values for that half not in draft |
| MF-24 | novelty_skeptic | D6 declares overlap audit exploratory; §3.4 labels it "sensitivity variant" | Draft never says "post hoc"; first-run time 2026-11-03 05:25 IST not quoted |
| MF-25 | novelty_skeptic | Abstract/§4.2 state 5.27% coverage, 279/280, boundary CI, exploratory 7.00pt | Same Table 4 "REFUTED" inconsistency as MF-5 |
| MF-29 | novelty_skeptic | §4.2 states single_matched = band_t_lo to five decimals (frozen degeneracy) | "not a binning artefact" claim retained; corrected non-degeneracy (0.636 vs 0.523, 222 items above t_hi) not in draft |
| MF-30 | reproducibility_reviewer | `requirements-lock.txt` + `ENVIRONMENT.md` exist with HF revisions | Draft §8 still prints "There is no lockfile" — false; needs correction |
| MF-31 | reproducibility_reviewer | §8 explains the `#` bug (whitespace token of comment line) | In-force hash at run time (0b577228…) not quoted; harness fix not cited in draft |
| MF-32 | reproducibility_reviewer | Log now D1–D6; 5-line chain | Draft front-matter stale (see MF-4); D5/D6 timing not quoted |
| MF-36 | reproducibility_reviewer | `table_prior_work()` now reads `table7_data.json` (mechanism built) | Data file still 3 rows (three neighbours only); five cited IDs not in table (register itself is covered) |
| MF-37 | reproducibility_reviewer | `DIRTY-TREE.md` reconstruction + future `git_diff.patch` storage | Draft §8 silent on dirty tree / diff — not disclosed to readers |
| MF-44 | clarity_reviewer | Figure 2 + §5.1 state coverage beside precision | Table 5 still has no coverage column; claim only partially true for arm rows |

## Deferred (5) — evidence exists, nothing in draft

| # | Reviewer (round 2) | Evidence file (exists) | Draft status |
|---:|---|---|---|
| MF-7 | methodologist | `04_experiments/results/c1/r3/exp/audit_twosided.json` gold_control AUROC 1.0 (label artefact) | No gold-paragraph control in §3.4/§4.1; no D3-top-1 audit R1–R3 |
| MF-10 | domain_expert | `04_experiments/results/c1/r3/exp/adjudication/` (100 items, κ = 0.1975, 5% resolved answerable) | No adjudication section in draft (§3.1/§6 silent); SQuAD impossible anchor not added |
| MF-17 | statistician | `04_experiments/results/c1/r3/exp/auroc_ci.json` (0.9824 [0.9774, 0.9869] vs 0.8738 [0.8585, 0.8887], paired 0.1085 [0.095, 0.123]) + `intervals.json` auroc_intervals | §3.6 explicitly says "AUROC itself carries no interval" — new intervals not folded |
| MF-23 | novelty_skeptic | `02_literature/related-work-r3/table7.json` (12 rows incl. N1 arXiv:2502.07255, N2 2609.22056, N3 doi:10.32604/cmc.2026.088937, N4 2609.32269, N10 doi:10.5281/zenodo.20547014) + `NOVELTY-R3.md` search record (18 OpenAlex + prior 91 arXiv) | Draft Table 1 still 3 rows; no differentiating paragraph; no search-record pointer |
| MF-28 | novelty_skeptic | `02_literature/related-work-r3/table7.json` DeclineCraft row (CAR + Answerable Attempt Rate, arXiv:2610.28340) | Draft Table 1 DeclineCraft row still "several unanswerable classes / retrieval and memory reported separately" |

## Persisted (raised again in round 3) — 22 items

Round-3 must-fix items whose theme overlaps a round-2 must-fix item.

| R3 # | Reviewer | Round-3 claim (short) | Overlaps round-2 |
|---:|---|---|---|
| 1 | methodologist | rung-separability headline (0.977) computed vs answerable items that always present gold paragraph | MF-7 |
| 2 | methodologist | corrected run labelled declared deviation although hash chain stops at D3 | MF-4, MF-32 |
| 3 | methodologist | Table 6 compares frozen/corrected at different dev-fitted operating points; omits corrected exploratory coverage row | MF-2, MF-34 |
| 4 | methodologist | H1/H3 verdicted REFUTED while text calls criterion not exercisable | MF-5, MF-25 |
| 5 | methodologist | abstract mixes frozen and corrected numbers in one comparison (R5 89.25 frozen, R4 12.53 corrected) | MF-3 |
| 7 | methodologist | held-out R2 n=280 of 400; exchangeability check reports only dev split | MF-22 |
| 9 | domain_expert | study never evaluates on SQuAD v2.0's own unanswerable questions | MF-10 |
| 11 | domain_expert | field-standard answerability baseline (fine-tuned reader) absent | MF-12 |
| 12 | domain_expert | no field companion metric (SQuAD F1/EM or AURC) | MF-9 |
| 15 | statistician | headline over-refusal/coverage reported without uncertainty | MF-16, MF-17 |
| 16 | statistician | AUROC comparisons across runs/ablations rest on point estimates | MF-17, MF-21 |
| 17 | statistician | reader baseline AUROC on non-random 553-item subset, no interval | MF-17, MF-22 |
| 18 | statistician | cluster bootstrap uses only 17 dev / 18 test articles | MF-18 |
| 20 | statistician | exploratory per-rung precisions in Table 3 lack per-cell intervals | MF-16 |
| 21 | novelty_skeptic | draft claims novelty but contains no documented novelty search | MF-23 |
| 25 | novelty_skeptic | DeclineCraft dismissed without stating whether its taxonomy subsumes any rung | MF-28 |
| 31 | reproducibility_reviewer | frozen run records pre-registration hash as '#' | MF-31 |
| 35 | clarity_reviewer | abstract states six surface features 'separate no rung' while reporting R4 AUROC 0.415 | MF-13, MF-26 |
| 36 | clarity_reviewer | abstract places overlap-matched R5 (89.25%) between R2 (91.07%) and R3 (92.75%) | MF-27 |
| 37 | clarity_reviewer | abstract conflates over-refusal (75.50%) with per-rung precision (56.98% R1) | MF-38, MF-39 |
| 38 | clarity_reviewer | Table 5 header 'Abstain precision' used for refusal rates and P(miss\|refused) | MF-39, MF-43 |
| 39 | clarity_reviewer | undefined term 'abstain recall' appears in abstract/§3.3 | MF-39 |

## New in round 3 — 19 items

Round-3 must-fix items not overlapping a round-2 theme.

| R3 # | Reviewer | Claim (short) |
|---:|---|---|
| 6 | methodologist | Table 7 leave-one-group-out ablations refit threshold per subset, confounding group contribution with model capacity |
| 8 | methodologist | whether IDF anchoring R2 was computed within split or corpus-wide is unstated (leakage path) |
| 10 | domain_expert | R4 labels produced by automatic span substitution with no human verification or agreement statistic |
| 13 | domain_expert | sampling procedure for the 400 answerable questions per half and article counts per split not stated |
| 14 | domain_expert | related work does not engage answerability-detection / selective-classification literature |
| 19 | statistician | Table 5 control arms omit sample sizes and several intervals |
| 22 | novelty_skeptic | delta over closest prior work (Abdumalikov et al.) never stated as a single sentence |
| 23 | novelty_skeptic | related work may omit primary selective-classification / coverage-risk literature |
| 24 | novelty_skeptic | 'audit as hard gate' presented as instrument contribution but is a standard surface-leakage check |
| 26 | novelty_skeptic | citation hygiene defects (Ho et al. arXiv:2011.01079 resolves to unrelated paper; survey entry lacks authors) |
| 27 | reproducibility_reviewer | article-disjoint split and per-rung sampling have no stated seed |
| 28 | reproducibility_reviewer | no lockfile or pinned requirements shipped |
| 29 | reproducibility_reviewer | headline numbers bound to RESULTS-INDEX.json but no run id or output file given |
| 30 | reproducibility_reviewer | code licence not stated |
| 32 | reproducibility_reviewer | logistic-regression and gate hyperparameters unspecified |
| 33 | reproducibility_reviewer | no smoke test or minimum configuration; full run resource needs unstated |
| 34 | reproducibility_reviewer | R4 answer-span replacement rule and reader model for §4.7 baseline unnamed |
| 40 | clarity_reviewer | abstract's closing generalisations exceed stated scope (one corpus family, one feature stack, one gate family) |
| 41 | clarity_reviewer | Figure 1 caption references spec-corrected bands before correction introduced in §4.6 |

---

_Type: round2-vs-round3 comparison with real round-3 scores/decisions (INGEST.md, AGGREGATE.md). "Resolved/Partial/Deferred" describe the current draft against the round-2 must-fix list; "Persisted/New" classify round-3 must-fix items._
