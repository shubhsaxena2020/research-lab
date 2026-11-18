# Aggregate simulated review - round 3

- Generated: 2026-11-18T15:46:42Z
- Source: `06_review/reviews/round3-c1`
- Draft: `05_paper/draft/paper.md` (sha256 `9194a481c8c0`)
- Reviews: 6 of 6 personas (methodologist, domain_expert, statistician, novelty_skeptic, reproducibility_reviewer, clarity_reviewer)

> **This is a simulation, not a real review.** The personas were written by the
> project, the reviews were filled in by the authors or an agent, and no venue or
> external reviewer was involved. Use it to find and track defects; do not read the
> scores as a prediction of acceptance.

## Scores

| Persona | Soundness (1-4) | Presentation (1-4) | Contribution (1-4) | Confidence (1-5) | Overall (1-10) | Decision |
|---|---:|---:|---:|---:|---:|---|
| methodologist | 2 | 3 | 3 | 4 | 5 | borderline |
| domain_expert | 3 | 3 | 3 | 4 | 6 | borderline |
| statistician | 3 | 3 | 3 | 4 | 6 | borderline |
| novelty_skeptic | 3 | 3 | 3 | 4 | 6 | borderline |
| reproducibility_reviewer | 2 | 3 | 3 | 4 | 5 | borderline |
| clarity_reviewer | 3 | 3 | 3 | 4 | 6 | borderline |
| **Mean (n=6)** | 2.67 | 3.00 | 3.00 | 4.00 | 5.67 | - |
| **Median** | 3 | 3 | 3 | 4 | 6 | - |

Overall: mean **5.67**, median **6**, range 5-6, sd 0.52 (n=6).

## Decision distribution

| Decision | Count | Personas |
|---|---:|---|
| reject | 0 | - |
| borderline | 6 | methodologist, domain_expert, statistician, novelty_skeptic, reproducibility_reviewer, clarity_reviewer |
| accept | 0 | - |

## Must-fix, ranked (41 distinct items from 41 raised)

Ranked by how many distinct personas raised the item, then by how often it was
raised. Near-identical wording is merged; the exact phrasings are kept below the
table so nothing is lost.

| Rank | Reviewers (n) | Claim | Evidence needed |
|---:|---:|---|---|
| 1 | 1 (methodologist) | The rung-separability headline (0.977 AUROC) is computed against answerable items that always present the gold paragraph, so it cannot separate rung hardness from gold-paragraph identity. | Re-run the six-surface-plus-overlap audit inside the D3 top-1-presented items, where rung 0 is not always gold, and report R1-R3 AUROCs beside the current 0.977 / 0.889 / 0.923. |
|  |  | _Where:_ Section 4.1, Table 2 |  |
| 2 | 1 (methodologist) | The corrected run that carries the R4 collapse (12.53% refusal, 0.874 AUROC) is labelled a declared deviation although the pre-registration hash chain stops at D3. | PREREGISTRATION.sha256 records three hashes (frozen, D1, D2+D3) and Section 1 ends the deviation list at D3; either add the D4 hash or stop calling it declared and stop recommending its numbers in Section 5.3. |
|  |  | _Where:_ Section 1, Section 4.6, Section 5.3 |  |
| 3 | 1 (methodologist) | Table 6 compares the frozen and corrected bands at different dev-fitted operating points and omits the corrected exploratory coverage row. | Add the corrected thresholds ([0.5232, 0.5370] against [0.9072, 0.9478]) and the exploratory coverage row (25.44% to 39.60%) to Table 6, or report R4 at matched coverage and state that the precision rows are not the same cut on two feature sets. |
|  |  | _Where:_ Section 4.6, Table 6 |  |
| 4 | 1 (methodologist) | H1 and H3 are verdicted REFUTED in Table 4 while the text calls them 'criterion not exercisable at this operating point', conflating 'criterion not met' with 'hypothesis false'. | Distinguish degenerate from refuted as Section 4.2 already does for H2, and reconcile a flat 'H1 refuted' with the exploratory arm's 7.00-point R1-R3 drop in the predicted direction (95% CI [4.50, 9.75]). |
|  |  | _Where:_ Abstract, Table 4, Section 4.2 |  |
| 5 | 1 (methodologist) | The abstract mixes frozen and corrected numbers in one comparison, quoting R5 at 89.25% (frozen) and R4 at 12.53% (corrected) in the same sentence. | Label every mixed number with its run, or report both R5 and R4 under the same run (frozen exploratory R4 84.71%; corrected exploratory R5 93.75%). |
|  |  | _Where:_ Abstract, Sections 4.4 and 4.6 |  |
| 6 | 1 (methodologist) | Table 7's leave-one-group-out ablations refit the threshold per subset and vary feature count with group size, confounding a group's contribution with model capacity. | Add a control that holds feature count fixed (e.g. replace the removed group with permuted features of the same dimension) and report held-out AUROC and over-refusal, or state that the ablation is descriptive. |
|  |  | _Where:_ Section 4.6, Table 7 |  |
| 7 | 1 (methodologist) | Held-out R2 has n=280 of 400 and the exchangeability check reports only the dev split while claiming coverage of 'either split'. | Report the held-out kept/dropped counts and their p-values beside the dev 273/127 split (smallest p=0.052), or restrict the exchangeability claim to dev. |
|  |  | _Where:_ Sections 3.1 and 4.7 |  |
| 8 | 1 (methodologist) | Whether the IDF used to anchor rung R2 was computed within each split pool or over the full corpus is not stated, leaving a possible leakage path in item construction. | State whether R2's highest-IDF content token was selected using within-split or corpus-wide IDF and whether any held-out article contributed to that statistic. |
|  |  | _Where:_ Sections 3.1 and 3.2 |  |
| 9 | 1 (domain_expert) | The study never evaluates on SQuAD v2.0's own unanswerable questions, which are the field's standard construct for unanswerability. | Either run the ladder on the 5945 SQuAD v2.0 dev unanswerable questions or state and justify why constructed negatives substitute for them. |
|  |  | _Where:_ Section 3.1, 'Only the answerable rows are used' |  |
| 10 | 1 (domain_expert) | Rung R4 labels are produced by automatic span substitution with no human verification or agreement statistic. | A label-quality audit of R4 reporting how many of N substituted items are genuinely unanswerable, or a reframing of R4 as answer-substituted rather than unanswerable. |
|  |  | _Where:_ Section 3.1 table, R4 row; section 5.4 |  |
| 11 | 1 (domain_expert) | The field-standard answerability baseline (a fine-tuned reader with a no-answer threshold) is absent. | Add a fine-tuned SQuAD 2.0 answerability classifier baseline (or justify scoping the comparison to retrieval features only) and report whether the gate survives. |
|  |  | _Where:_ Section 2, 'Model confidence as a gate'; section 4.2 baselines B1 and B2 |  |
| 12 | 1 (domain_expert) | No field companion metric is reported: SQuAD-style F1/EM or selective-prediction risk at coverage (AURC) is missing. | Report selective risk at the registered coverage and an AURC, or justify the metric choice against the field standard. |
|  |  | _Where:_ Sections 4.2-4.3, Tables 3-4 |  |
| 13 | 1 (domain_expert) | The sampling procedure for the 400 answerable questions per half and the article counts per split are not stated. | State whether sampling is random or stratified, by article, and report the number of articles per split. |
|  |  | _Where:_ Section 3.1 |  |
| 14 | 1 (domain_expert) | Related work does not engage the answerability-detection or selective-classification literature that already studied this problem. | Add at least one body of work (e.g. SQuAD 2.0 answerability baselines or El-Yaniv and Wiener on selective classification) and state what the paper argues against it. |
|  |  | _Where:_ Section 2 |  |
| 15 | 1 (statistician) | Headline over-refusal and coverage rates are reported without uncertainty. | Paired bootstrap 95% CIs on over-refusal and coverage at the registered and exploratory operating points, over the 400 held-out answerable items. |
|  |  | _Where:_ Section 4.2 and Figure 2 |  |
| 16 | 1 (statistician) | AUROC comparisons across runs and ablations rest on point estimates with no interval. | Bootstrap 95% CIs on dev and held-out AUROC for the frozen and corrected runs, and on at least the all_12, no_dense and lex_overlap_only ablation AUROCs. |
|  |  | _Where:_ Section 4.6, Tables 6 and 7 |  |
| 17 | 1 (statistician) | The reader baseline AUROC is computed on a non-random 553-item subset with no interval. | The selection rule and denominator for the 553 items, a bootstrap 95% CI on the 0.419 AUROC, and a comparison of subset difficulty to the full dev half. |
|  |  | _Where:_ Section 4.7 |  |
| 18 | 1 (statistician) | The cluster bootstrap uses only 17 dev and 18 test articles. | Report the cluster count, and either a wild-cluster or t(G minus 1) interval, or justify article-level resampling with so few clusters. |
|  |  | _Where:_ Section 4.7 |  |
| 19 | 1 (statistician) | Table 5 control arms omit sample sizes and several intervals. | Add n per arm and replace 'not informative' with intervals or a stated reason. |
|  |  | _Where:_ Sections 4.4 to 4.5, Table 5 |  |
| 20 | 1 (statistician) | Exploratory per-rung precisions in Table 3 lack per-cell intervals. | BCa 95% CIs for each exploratory per-rung precision at the frozen seed. |
|  |  | _Where:_ Section 4.3, Table 3 |  |
| 21 | 1 (novelty_skeptic) | The draft claims novelty for the ladder and audit but contains no documented novelty search (queries, databases, date, results). | An appendix or section listing search queries, databases searched, date, and counts of candidate papers found and excluded. |
|  |  | _Where:_ §2, §9 (no search record present) |  |
| 22 | 1 (novelty_skeptic) | The delta over the closest prior work (Abdumalikov et al., arXiv:2403.01461) is never stated as a single sentence without adjectives. | One sentence of the form 'Compared to Abdumalikov et al., this paper adds <delta>' placed in §1 or §2, where the delta is a mechanism or design change rather than more rungs. |
|  |  | _Where:_ §1 contribution bullets; §2; Table 1 |  |
| 23 | 1 (novelty_skeptic) | Related work may omit the obvious competing line: primary selective-classification / coverage-risk literature is represented only by a survey. | Either cite primary selective-classification (coverage-risk / reject-option) work or state explicitly why it is out of scope for a retrieval-feature gate. |
|  |  | _Where:_ §2 |  |
| 24 | 1 (novelty_skeptic) | The 'audit as hard gate' is presented as an instrument contribution but is a standard surface-leakage check; no evidence shows the ladder + audit + controls combination is non-obvious. | An ablation or argument showing which design component (rungs, audit, controls) is necessary for the verdict, beyond the feature-level ablations in Table 7. |
|  |  | _Where:_ §1 (second bullet); §3.4 |  |
| 25 | 1 (novelty_skeptic) | Concurrent work DeclineCraft is dismissed as 'complementary rather than nested' without stating whether its negative taxonomy subsumes any rung. | A sentence stating what DeclineCraft's negative classes are and which of R1-R4 they do or do not cover. |
|  |  | _Where:_ §2, Table 1 |  |
| 26 | 1 (novelty_skeptic) | Citation hygiene defects: Ho et al. arXiv:2011.01079 resolves to an unrelated paper, and the abstention survey entry lacks authors. | Corrected/verified identifiers and full author lists in the reference list. |
|  |  | _Where:_ §9 |  |
| 27 | 1 (reproducibility_reviewer) | The article-disjoint dev/held-out split and the per-rung item sampling have no stated seed, so the 1873/1879 item sets cannot be regenerated. | The integer seed(s) for article splitting and for the 400-question sampling per split, plus the committed split file path and sha256 and the sampling script's RNG call. |
|  |  | _Where:_ §3.1, §8 (build_items.py, 'seeds fixed') |  |
| 28 | 1 (reproducibility_reviewer) | No lockfile or pinned requirements are shipped; library and interpreter versions live only in an unspecified session status file. | A requirements.txt or lockfile with exact pins committed in the repo, plus OS, CPU/GPU model and count, driver/CUDA versions, and the Python interpreter version recorded in §8. |
|  |  | _Where:_ §8, final paragraph |  |
| 29 | 1 (reproducibility_reviewer) | Headline numbers are bound to RESULTS-INDEX.json but no run id or output file is given, so a rerun cannot be checked against the reported value. | For each table, the run id or results JSON path and the command that produced it, listed beside the command in §8. |
|  |  | _Where:_ §8 command block; Abstract; Tables 3-7 |  |
| 30 | 1 (reproducibility_reviewer) | The code licence is not stated even though data licences are, so the artifact's release terms are undefined. | A LICENSE file in the repository root and a one-line licence statement in §7 naming it. |
|  |  | _Where:_ §7 |  |
| 31 | 1 (reproducibility_reviewer) | The frozen run records its pre-registration hash as a single '#' character, so the freeze cannot be audited from the paper's reported line. | The corrected hash-reading line (or the four hashes from PREREGISTRATION.sha256 printed in §8) and a re-run showing the recorded hash matches. |
|  |  | _Where:_ §8, penultimate paragraph |  |
| 32 | 1 (reproducibility_reviewer) | Logistic-regression and gate hyperparameters are unspecified. | The exact model configuration (penalty, C, solver, max_iter, standardisation) and threshold-search procedure as committed in gate.py, quoted in §3.3. |
|  |  | _Where:_ §3.3, §3.4 |  |
| 33 | 1 (reproducibility_reviewer) | No smoke test or minimum configuration is provided, and the full run's resource needs are unstated, so a reviewer cannot check the artifact in minutes. | A documented smoke-test command on a small config (single CPU, under ten minutes) and the hardware requirement for the full run. |
|  |  | _Where:_ §8 |  |
| 34 | 1 (reproducibility_reviewer) | R4's answer-span replacement rule and the reader model used for the §4.7 baseline are unnamed, so those two results cannot be reproduced. | The type-matching rule and any inspected examples for R4 substitutions, and the reader model name and version, in §3.1 and §4.7 respectively. |
|  |  | _Where:_ §3.1, §4.7 |  |
| 35 | 1 (clarity_reviewer) | The abstract states that six surface features 'separate no rung' while reporting R4 AUROC 0.415, which the paper itself calls separation of equal magnitude with the sign flipped. | Section 3.4 and Table 2 reporting R4 AUROC 0.415 and its inverted separation, with the 0.750 one-sided gate. |
|  |  | _Where:_ Abstract, Table 2 |  |
| 36 | 1 (clarity_reviewer) | The abstract places overlap-matched R5 (89.25%) between R2 (91.07%) and R3 (92.75%), but 89.25% is below R2. | Table 3 R2 91.07% and R3 92.75%; Table 5 R5 89.25% and Section 4.4's ordering between R2 and R4. |
|  |  | _Where:_ Abstract |  |
| 37 | 1 (clarity_reviewer) | The abstract conflates over-refusal (75.50%) with per-rung precision (56.98% on R1), incorrectly summarising R1's refusals as 'mostly answerable'. | Table 3: R1 precision 56.98% (majority negatives) and over-refusal 75.50% (answerable questions refused). |
|  |  | _Where:_ Abstract |  |
| 38 | 1 (clarity_reviewer) | Table 5's column header 'Abstain precision' is used for refusal rates and P(miss \| refused), contradicting its own caption. | Table 5 caption 'Precision is reported for the main ladder only (Table 3)' alongside the 'Abstain precision' header. |
|  |  | _Where:_ Section 4.4, Table 5 |  |
| 39 | 1 (clarity_reviewer) | The undefined term 'abstain recall' appears in the abstract and Section 3.3, while Section 3.5 defines only refusal rate and precision. | Section 3.5 naming correction, which does not define abstain recall. |
|  |  | _Where:_ Abstract, Section 3.3 |  |
| 40 | 1 (clarity_reviewer) | The abstract's closing generalisations exceed the paper's stated scope of one corpus family, one feature stack and one gate family. | Section 1's scope disclaimer ('We claim neither priority nor generality beyond...'). |
|  |  | _Where:_ Abstract, final sentence |  |
| 41 | 1 (clarity_reviewer) | Figure 1's caption in Section 4.2 references spec-corrected bands before the correction is introduced in Section 4.6. | Figure 1 caption mentioning spec-corrected bands; correction introduced in Section 4.6. |
|  |  | _Where:_ Section 4.2, Figure 1 |  |

## Rebuttal tracker seed

Copy this into the response tracker. Every item must end as a change (with the
file or diff) or a rebuttal (with a citation or result) - never as silence.

- [ ] **MF-1** (1 reviewer(s): methodologist) The rung-separability headline (0.977 AUROC) is computed against answerable items that always present the gold paragraph, so it cannot separate rung hardness from gold-paragraph identity.  
      evidence to supply: Re-run the six-surface-plus-overlap audit inside the D3 top-1-presented items, where rung 0 is not always gold, and report R1-R3 AUROCs beside the current 0.977 / 0.889 / 0.923.
- [ ] **MF-2** (1 reviewer(s): methodologist) The corrected run that carries the R4 collapse (12.53% refusal, 0.874 AUROC) is labelled a declared deviation although the pre-registration hash chain stops at D3.  
      evidence to supply: PREREGISTRATION.sha256 records three hashes (frozen, D1, D2+D3) and Section 1 ends the deviation list at D3; either add the D4 hash or stop calling it declared and stop recommending its numbers in Section 5.3.
- [ ] **MF-3** (1 reviewer(s): methodologist) Table 6 compares the frozen and corrected bands at different dev-fitted operating points and omits the corrected exploratory coverage row.  
      evidence to supply: Add the corrected thresholds ([0.5232, 0.5370] against [0.9072, 0.9478]) and the exploratory coverage row (25.44% to 39.60%) to Table 6, or report R4 at matched coverage and state that the precision rows are not the same cut on two feature sets.
- [ ] **MF-4** (1 reviewer(s): methodologist) H1 and H3 are verdicted REFUTED in Table 4 while the text calls them 'criterion not exercisable at this operating point', conflating 'criterion not met' with 'hypothesis false'.  
      evidence to supply: Distinguish degenerate from refuted as Section 4.2 already does for H2, and reconcile a flat 'H1 refuted' with the exploratory arm's 7.00-point R1-R3 drop in the predicted direction (95% CI [4.50, 9.75]).
- [ ] **MF-5** (1 reviewer(s): methodologist) The abstract mixes frozen and corrected numbers in one comparison, quoting R5 at 89.25% (frozen) and R4 at 12.53% (corrected) in the same sentence.  
      evidence to supply: Label every mixed number with its run, or report both R5 and R4 under the same run (frozen exploratory R4 84.71%; corrected exploratory R5 93.75%).
- [ ] **MF-6** (1 reviewer(s): methodologist) Table 7's leave-one-group-out ablations refit the threshold per subset and vary feature count with group size, confounding a group's contribution with model capacity.  
      evidence to supply: Add a control that holds feature count fixed (e.g. replace the removed group with permuted features of the same dimension) and report held-out AUROC and over-refusal, or state that the ablation is descriptive.
- [ ] **MF-7** (1 reviewer(s): methodologist) Held-out R2 has n=280 of 400 and the exchangeability check reports only the dev split while claiming coverage of 'either split'.  
      evidence to supply: Report the held-out kept/dropped counts and their p-values beside the dev 273/127 split (smallest p=0.052), or restrict the exchangeability claim to dev.
- [ ] **MF-8** (1 reviewer(s): methodologist) Whether the IDF used to anchor rung R2 was computed within each split pool or over the full corpus is not stated, leaving a possible leakage path in item construction.  
      evidence to supply: State whether R2's highest-IDF content token was selected using within-split or corpus-wide IDF and whether any held-out article contributed to that statistic.
- [ ] **MF-9** (1 reviewer(s): domain_expert) The study never evaluates on SQuAD v2.0's own unanswerable questions, which are the field's standard construct for unanswerability.  
      evidence to supply: Either run the ladder on the 5945 SQuAD v2.0 dev unanswerable questions or state and justify why constructed negatives substitute for them.
- [ ] **MF-10** (1 reviewer(s): domain_expert) Rung R4 labels are produced by automatic span substitution with no human verification or agreement statistic.  
      evidence to supply: A label-quality audit of R4 reporting how many of N substituted items are genuinely unanswerable, or a reframing of R4 as answer-substituted rather than unanswerable.
- [ ] **MF-11** (1 reviewer(s): domain_expert) The field-standard answerability baseline (a fine-tuned reader with a no-answer threshold) is absent.  
      evidence to supply: Add a fine-tuned SQuAD 2.0 answerability classifier baseline (or justify scoping the comparison to retrieval features only) and report whether the gate survives.
- [ ] **MF-12** (1 reviewer(s): domain_expert) No field companion metric is reported: SQuAD-style F1/EM or selective-prediction risk at coverage (AURC) is missing.  
      evidence to supply: Report selective risk at the registered coverage and an AURC, or justify the metric choice against the field standard.
- [ ] **MF-13** (1 reviewer(s): domain_expert) The sampling procedure for the 400 answerable questions per half and the article counts per split are not stated.  
      evidence to supply: State whether sampling is random or stratified, by article, and report the number of articles per split.
- [ ] **MF-14** (1 reviewer(s): domain_expert) Related work does not engage the answerability-detection or selective-classification literature that already studied this problem.  
      evidence to supply: Add at least one body of work (e.g. SQuAD 2.0 answerability baselines or El-Yaniv and Wiener on selective classification) and state what the paper argues against it.
- [ ] **MF-15** (1 reviewer(s): statistician) Headline over-refusal and coverage rates are reported without uncertainty.  
      evidence to supply: Paired bootstrap 95% CIs on over-refusal and coverage at the registered and exploratory operating points, over the 400 held-out answerable items.
- [ ] **MF-16** (1 reviewer(s): statistician) AUROC comparisons across runs and ablations rest on point estimates with no interval.  
      evidence to supply: Bootstrap 95% CIs on dev and held-out AUROC for the frozen and corrected runs, and on at least the all_12, no_dense and lex_overlap_only ablation AUROCs.
- [ ] **MF-17** (1 reviewer(s): statistician) The reader baseline AUROC is computed on a non-random 553-item subset with no interval.  
      evidence to supply: The selection rule and denominator for the 553 items, a bootstrap 95% CI on the 0.419 AUROC, and a comparison of subset difficulty to the full dev half.
- [ ] **MF-18** (1 reviewer(s): statistician) The cluster bootstrap uses only 17 dev and 18 test articles.  
      evidence to supply: Report the cluster count, and either a wild-cluster or t(G minus 1) interval, or justify article-level resampling with so few clusters.
- [ ] **MF-19** (1 reviewer(s): statistician) Table 5 control arms omit sample sizes and several intervals.  
      evidence to supply: Add n per arm and replace 'not informative' with intervals or a stated reason.
- [ ] **MF-20** (1 reviewer(s): statistician) Exploratory per-rung precisions in Table 3 lack per-cell intervals.  
      evidence to supply: BCa 95% CIs for each exploratory per-rung precision at the frozen seed.
- [ ] **MF-21** (1 reviewer(s): novelty_skeptic) The draft claims novelty for the ladder and audit but contains no documented novelty search (queries, databases, date, results).  
      evidence to supply: An appendix or section listing search queries, databases searched, date, and counts of candidate papers found and excluded.
- [ ] **MF-22** (1 reviewer(s): novelty_skeptic) The delta over the closest prior work (Abdumalikov et al., arXiv:2403.01461) is never stated as a single sentence without adjectives.  
      evidence to supply: One sentence of the form 'Compared to Abdumalikov et al., this paper adds <delta>' placed in §1 or §2, where the delta is a mechanism or design change rather than more rungs.
- [ ] **MF-23** (1 reviewer(s): novelty_skeptic) Related work may omit the obvious competing line: primary selective-classification / coverage-risk literature is represented only by a survey.  
      evidence to supply: Either cite primary selective-classification (coverage-risk / reject-option) work or state explicitly why it is out of scope for a retrieval-feature gate.
- [ ] **MF-24** (1 reviewer(s): novelty_skeptic) The 'audit as hard gate' is presented as an instrument contribution but is a standard surface-leakage check; no evidence shows the ladder + audit + controls combination is non-obvious.  
      evidence to supply: An ablation or argument showing which design component (rungs, audit, controls) is necessary for the verdict, beyond the feature-level ablations in Table 7.
- [ ] **MF-25** (1 reviewer(s): novelty_skeptic) Concurrent work DeclineCraft is dismissed as 'complementary rather than nested' without stating whether its negative taxonomy subsumes any rung.  
      evidence to supply: A sentence stating what DeclineCraft's negative classes are and which of R1-R4 they do or do not cover.
- [ ] **MF-26** (1 reviewer(s): novelty_skeptic) Citation hygiene defects: Ho et al. arXiv:2011.01079 resolves to an unrelated paper, and the abstention survey entry lacks authors.  
      evidence to supply: Corrected/verified identifiers and full author lists in the reference list.
- [ ] **MF-27** (1 reviewer(s): reproducibility_reviewer) The article-disjoint dev/held-out split and the per-rung item sampling have no stated seed, so the 1873/1879 item sets cannot be regenerated.  
      evidence to supply: The integer seed(s) for article splitting and for the 400-question sampling per split, plus the committed split file path and sha256 and the sampling script's RNG call.
- [ ] **MF-28** (1 reviewer(s): reproducibility_reviewer) No lockfile or pinned requirements are shipped; library and interpreter versions live only in an unspecified session status file.  
      evidence to supply: A requirements.txt or lockfile with exact pins committed in the repo, plus OS, CPU/GPU model and count, driver/CUDA versions, and the Python interpreter version recorded in §8.
- [ ] **MF-29** (1 reviewer(s): reproducibility_reviewer) Headline numbers are bound to RESULTS-INDEX.json but no run id or output file is given, so a rerun cannot be checked against the reported value.  
      evidence to supply: For each table, the run id or results JSON path and the command that produced it, listed beside the command in §8.
- [ ] **MF-30** (1 reviewer(s): reproducibility_reviewer) The code licence is not stated even though data licences are, so the artifact's release terms are undefined.  
      evidence to supply: A LICENSE file in the repository root and a one-line licence statement in §7 naming it.
- [ ] **MF-31** (1 reviewer(s): reproducibility_reviewer) The frozen run records its pre-registration hash as a single '#' character, so the freeze cannot be audited from the paper's reported line.  
      evidence to supply: The corrected hash-reading line (or the four hashes from PREREGISTRATION.sha256 printed in §8) and a re-run showing the recorded hash matches.
- [ ] **MF-32** (1 reviewer(s): reproducibility_reviewer) Logistic-regression and gate hyperparameters are unspecified.  
      evidence to supply: The exact model configuration (penalty, C, solver, max_iter, standardisation) and threshold-search procedure as committed in gate.py, quoted in §3.3.
- [ ] **MF-33** (1 reviewer(s): reproducibility_reviewer) No smoke test or minimum configuration is provided, and the full run's resource needs are unstated, so a reviewer cannot check the artifact in minutes.  
      evidence to supply: A documented smoke-test command on a small config (single CPU, under ten minutes) and the hardware requirement for the full run.
- [ ] **MF-34** (1 reviewer(s): reproducibility_reviewer) R4's answer-span replacement rule and the reader model used for the §4.7 baseline are unnamed, so those two results cannot be reproduced.  
      evidence to supply: The type-matching rule and any inspected examples for R4 substitutions, and the reader model name and version, in §3.1 and §4.7 respectively.
- [ ] **MF-35** (1 reviewer(s): clarity_reviewer) The abstract states that six surface features 'separate no rung' while reporting R4 AUROC 0.415, which the paper itself calls separation of equal magnitude with the sign flipped.  
      evidence to supply: Section 3.4 and Table 2 reporting R4 AUROC 0.415 and its inverted separation, with the 0.750 one-sided gate.
- [ ] **MF-36** (1 reviewer(s): clarity_reviewer) The abstract places overlap-matched R5 (89.25%) between R2 (91.07%) and R3 (92.75%), but 89.25% is below R2.  
      evidence to supply: Table 3 R2 91.07% and R3 92.75%; Table 5 R5 89.25% and Section 4.4's ordering between R2 and R4.
- [ ] **MF-37** (1 reviewer(s): clarity_reviewer) The abstract conflates over-refusal (75.50%) with per-rung precision (56.98% on R1), incorrectly summarising R1's refusals as 'mostly answerable'.  
      evidence to supply: Table 3: R1 precision 56.98% (majority negatives) and over-refusal 75.50% (answerable questions refused).
- [ ] **MF-38** (1 reviewer(s): clarity_reviewer) Table 5's column header 'Abstain precision' is used for refusal rates and P(miss | refused), contradicting its own caption.  
      evidence to supply: Table 5 caption 'Precision is reported for the main ladder only (Table 3)' alongside the 'Abstain precision' header.
- [ ] **MF-39** (1 reviewer(s): clarity_reviewer) The undefined term 'abstain recall' appears in the abstract and Section 3.3, while Section 3.5 defines only refusal rate and precision.  
      evidence to supply: Section 3.5 naming correction, which does not define abstain recall.
- [ ] **MF-40** (1 reviewer(s): clarity_reviewer) The abstract's closing generalisations exceed the paper's stated scope of one corpus family, one feature stack and one gate family.  
      evidence to supply: Section 1's scope disclaimer ('We claim neither priority nor generality beyond...').
- [ ] **MF-41** (1 reviewer(s): clarity_reviewer) Figure 1's caption in Section 4.2 references spec-corrected bands before the correction is introduced in Section 4.6.  
      evidence to supply: Figure 1 caption mentioning spec-corrected bands; correction introduced in Section 4.6.

---

_Generated by `tools/simulate_review.py aggregate`. Scores are diagnostics for
revision, not a venue decision._
