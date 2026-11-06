# Round comparison - 06_review/reviews/round1-c1 -> 06_review/reviews/round2-c1

- Generated: 2026-11-03T02:17:45Z
- Reviews: round 1 = 5, round 2 = 6
- Distinct must-fix items: round 1 = 12, round 2 = 44

> A **resolved** item means no round-2 reviewer raised it again. That is evidence,
> not proof: an item can disappear because the text moved, because a reviewer
> forgot it, or because the revision buried it. Pair every resolved row with a
> concrete change (file, diff, run id) in the response letter.

## Totals

| Metric | Round 1 | Round 2 | Delta |
|---|---:|---:|---:|
| Mean overall (1-10) | 4.00 | 4.67 | +0.67 |
| Median overall | 4 | 4.5 | +0.5 |
| Must-fix items (distinct) | 12 | 44 | +32 |
| Reject recommendations | 1 | 3 | +2 |
| Items resolved | - | 12 | |
| Items persisted | - | 0 | |
| Items new in round 2 | - | 44 | |

**Headline: 12 resolved, 0 persisted, 44 new.**

## Resolved (raised in round 1, not raised in round 2): 12

No round-2 reviewer re-raised these. Pair each one with the change that resolved it.

| # | Reviewers (round 1) | Claim | Evidence that was needed |
|---:|---|---|---|
| 1 | 1 (methodologist) | The gate can identify rung-0 items from construction artefacts, so the separation may not measure answerability. | Held-out AUROC and per-rung precision without rank features, plus a variant where every presented passage is the top-1 retrieved document. |
| 2 | 1 (methodologist) | No ablation isolates which retrieval features carry the result. | Per-rung abstain precision for leave-one-out variants: without overlap, without ranks, without the cross-encoder. |
| 3 | 1 (methodologist) | Rung 2 is reported at 68% of designed size with no exchangeability check. | Comparison of question length and answer type between the 273 kept and 127 dropped rung-2 dev questions. |
| 4 | 1 (statistician) | The exploratory per-rung precisions that carry the ladder claim have no uncertainty. | BCa intervals at the frozen seed for each exploratory per-rung precision and for the rung 1 minus rung 3 difference. |
| 5 | 1 (statistician) | Intervals ignore clustering of questions within articles. | A cluster bootstrap by article reported alongside the item bootstrap for the primary per-rung precisions. |
| 6 | 1 (statistician) | 'Matched abstain recall' is asserted but the matched test recalls are not shown. | A row reporting band recall and matched-single recall on the held-out half. |
| 7 | 1 (novelty_skeptic) | Title and abstract promise a hardness effect the confirmatory result refutes, while the real finding sits in a deviation log. | Either a title and abstract leading with the coverage-precision finding, or a second corpus showing the ladder effect at a non-degenerate operating point. |
| 8 | 1 (novelty_skeptic) | Prior work is named but not compared. | A table comparing this setup with the closest benchmark on data, metric, negative construction and reported operating point. |
| 9 | 1 (reproducibility_reviewer) | The draft references generated tables by path instead of including them, so the paper contains no results tables. | Tables inlined (or \input in LaTeX) with the generated content and no hand-edited cells. |
| 10 | 1 (reproducibility_reviewer) | The numbers audit does not pass on the draft, which is a hard gate in this project's own rules. | A zero-finding run of tools/check_numbers.py on the draft, or a per-finding justification. |
| 11 | 1 (clarity_reviewer) | The abstract's first reported numbers are the degenerate ones, so the finding is invisible to a skimming reader. | An abstract whose first quantitative sentence is the over-refusal figure and its consequence. |
| 12 | 1 (clarity_reviewer) | Four-decimal reporting overstates precision relative to the reported intervals. | Two decimals for rates and three for AUROC, consistent with Section 6's own rule. |

## Persisted (raised in both rounds): 0

Unaddressed or addressed without convincing the reviewer. Each needs a
decision: fix, or rebut with evidence.

_None._

## New in round 2: 44

Revision-induced problems (new claims, moved text, new experiments). Triage these before the next round.

| # | Reviewers (round 1) | Claim | Evidence that was needed |
|---:|---|---|---|
| 1 | 1 (methodologist) | The quantity reported as abstain precision is a per-rung refusal rate, so the 100.00% headline and the 75.50% over-refusal beside it cannot both be read as precision. | Define abstain precision, over-refusal and coverage with explicit numerators/denominators; the R1 cell is 400/400 refusals while Section 3.3's constraint is P(negative\|refused) = 0.8369 at 1760/1873 dev refusals (results_full.json), and the pooled held-out value under that definition is 1478/1780 = 83.0%, not 99.93%. |
| 2 | 1 (methodologist) | Table 4 compares two runs at different dev-fitted operating points without saying so, and omits the corrected exploratory coverage row that would expose the difference. | Add the corrected thresholds ([0.5232, 0.5370] against [0.9072, 0.9478]) and the exploratory coverage row (25.44% to 39.60%, per c1_corrected/SUMMARY.md) to Table 4, or report R4 at matched coverage and state that the precision rows are not the same cut on two feature sets. |
| 3 | 1 (methodologist) | The abstract and Sections 4.4 and 4.8 mix frozen and corrected numbers inside single comparisons, so the control-arm conclusions come from the run the paper calls defective. | Report R5 and the transfer arm under both runs (R5 89.25% frozen against 93.75% corrected; transfer 85.50% at AUROC 0.640 frozen against 97.50% at 0.706 corrected), or label every mixed sentence with the run it comes from. |
| 4 | 1 (methodologist) | D4 is called a declared deviation but the pre-registration's hash chain and deviation log stop at D3, so the paper's most striking result rests on an unregistered re-analysis. | PREREGISTRATION.sha256 holds three hashes (frozen, D1, D2+D3) and Section 10 ends at D3; either add the D4 entry and hash, or stop calling it declared and stop recommending its numbers in Section 5.3. |
| 5 | 1 (methodologist) | H1 and H3 are labelled refuted although the paper's own argument is that the quantity is undefined at that operating point, which conflates 'criterion not met' with 'hypothesis false'. | Distinguish degenerate from refuted as Section 4.2 already does for H2, and reconcile a flat 'H1 refuted' with the exploratory arm's 7.00-point R1-R3 drop in H1's predicted direction (95% CI [4.50, 9.75]). |
| 6 | 1 (methodologist) | The second-corpus leg of H2 is never scored against the pre-registered criterion, and its 7.25-point drop lands in the undefined gap between the 5-point refutation band and the 10-point criterion. | Add an explicit H2 verdict for the second corpus, with the recall each arm operates at (over-refusal 57.50% there against 9.50% on the main corpus), and state what the pre-registered rule says about a 5-to-10-point loss. |
| 7 | 1 (methodologist) | The audit's 0.977 separates rungs from answerable items that are always the gold paragraph, so it cannot distinguish rung hardness from 'is this the gold paragraph'. | Re-run the six-surface-plus-overlap audit inside the D3 top-1-presented items, where rung 0 is not always gold, and report the R1-R3 AUROCs from that variant beside the current 0.977 / 0.889 / 0.923. |
| 8 | 1 (domain_expert) | Every figure labelled 'abstain precision' is the share of a rung's negatives refused, so the paper never reports abstention precision and its central claim about precision is untested. | Recompute as refusals of negatives / all refusals, per rung and pooled, report the refusal count behind each cell, and state the definition explicitly: R2's 99.64% is 279/280 (recall), while its precision is 279/(279+302) = 48.0%. |
| 9 | 1 (domain_expert) | Coverage is computed over items with four negatives per question, which understates the field's coverage by about a factor of five and inflates the paper's headline claim. | Coverage reported over questions (98 of 400 = 24.5%) alongside the item-level figure, and AURCC or abstention F1 added as the companion metrics the cited survey recommends. |
| 10 | 1 (domain_expert) | No negative in the study has an adjudicated answerability label, so 'negative' means 'not the gold paragraph' rather than 'does not answer the question'. | A two-annotator adjudication of a sample of at least 100 R2 and R3 passages for whether each supports the question, with instructions and Cohen's kappa reported, plus SQuAD 2.0's impossible rows as a human-labelled anchor rung. |
| 11 | 1 (domain_expert) | 'The ladder therefore varies the negative along one axis at a time' is contradicted by the paper's own length observation, so hardness is not identified with any single axis. | Per-rung length and overlap distributions, and one rung matched on both question overlap and passage length, to show the ordering survives when both are held constant. |
| 12 | 1 (domain_expert) | The reader-side baseline is a fluency proxy, not the P(True) baseline the paper says a reviewer expects, so its failure is not evidence about reader-side gating. | P(True) scores on the same 553 dev items with AUROC and a threshold, or the removal of the claim that reader-side confidence fails on this task. |
| 13 | 1 (domain_expert) | The separability audit is one-sided, so inverted separation at R4 is recorded as a pass. | A two-sided rule on \|AUROC - 0.5\| with confidence intervals, the audit table's split and n stated, and R4's 0.415 reported as separation in the reverse direction rather than as no separation. |
| 14 | 1 (domain_expert) | The mechanistic conclusion about R4 rests on one post-hoc exploratory cell while the registered analysis reports the opposite for that rung. | Either promote the D4 corrected run to the primary analysis in the title and abstract, or report the registered R4 value (100.00%) beside the exploratory 12.53% and restrict Section 5.2 to what the registered run supports. |
| 15 | 1 (statistician) | The values reported as abstain precision are refusal rates over each rung's negatives, not the pooled precision the 0.80 constraint was fitted to, so the table cannot be checked against the rule. | Give the formula for both quantities: Table 1's R1 is 400/400 and R2 is 279/280 (predictions.csv), while thresholds.band.dev_precision is 0.8369 at 1760/1873 dev refusals; the pooled held-out precision under the fitting definition is 1478/1780 = 83.0%. Report both, and correct 'identical on every rung' given R2 = 99.64%. |
| 16 | 1 (statistician) | Zero-width 95% intervals on H1 and H3 are presented as estimates when they are artefacts of a boundary proportion, and the stated interval method does not match the archive. | Report the discordant counts (H1 0 of 400 pairs, H3 0 of 1479) as the primary evidence and describe the interval as degenerate, and reconcile Section 3.5's 'BCa' with the 'percentile' method recorded for rungs 1, 3 and 4 in results_full.json. |
| 17 | 1 (statistician) | No AUROC in the paper carries an interval or a paired difference interval, including the 0.982-to-0.874 drop that the corrected run turns on. | A paired bootstrap 95% CI on the AUROC difference over the 1879 held-out items for 0.982 against 0.874, and intervals for the 0.945, 0.640 and 0.977 figures, with the number of articles (18) stated. |
| 18 | 1 (statistician) | The cluster bootstrap rests on 18 held-out articles, the two cells that carry H1 are zero-width and excluded from its comparable set, and its quoted minimum width ratio is wrong. | Report n_articles = 18 beside the cluster intervals, show the rung-1 and rung-3 cluster intervals rather than describing them, and correct 'width ratio as low as 0.851' to the archive's 0.4521 (stats_addendum.json, cluster_bootstrap). |
| 19 | 1 (statistician) | The corrected H3 comparison is not at matched abstain recall and its matched single violates the 0.80 precision constraint, so -2.23% is not the pre-registered test. | Report the corrected dev recalls (band 0.9898, matched single 0.9925) and the matched single's dev precision (0.7886), then re-match on recall and re-report the difference and its interval. |
| 20 | 1 (statistician) | The corrected exploratory arm reports 11.00% over-refusal against a declared cap of 0.10 with no statement of whether the declared rule was breached. | State whether the 'dev over-refusal at most 0.10' cap binds on dev or on the held-out half, and give the corrected dev over-refusal; if the reported 11.00% is a breach, note it or rebuild the arm under the cap. |
| 21 | 1 (statistician) | The equivalence claim that no single feature group carries the result is supported only by point estimates across eight subsets. | A paired bootstrap 95% CI on the held-out AUROC difference for all_12 against no_dense (0.874 against 0.862) and against dense_only (0.874 against 0.870) over the same 1879 items. |
| 22 | 1 (statistician) | The held-out rung-2 shortfall is never stated and the exchangeability check that Section 3.1 promises for both splits reports only dev figures. | Report the held-out split's kept and dropped counts (280 of 400) and the per-variable p-values for that half, alongside the dev 273/127 and its 0.052 minimum. |
| 23 | 1 (novelty_skeptic) | Table 7 compares this paper with two prior works and omits all five near neighbours that the project's own documented search marks as closest, including the work that occupies the separability finding. | Rows and a differentiating paragraph for N1 (arXiv:2502.07255), N2 (arXiv:2609.22056), N3 (doi:10.32604/cmc.2026.088937), N4 (arXiv:2609.32269) and N10, each stating what is varied and what is reported per rung, and what §4.1's audit adds beyond N4's surface-only adversary at AUROC 0.979; plus a pointer to the search record (84 OpenAlex and 91 arXiv queries, 2026-11-03) so a reader can see the search happened. |
| 24 | 1 (novelty_skeptic) | The paper's headline measurement - the overlap-augmented audit at 0.977/0.889/0.923 - is not defined anywhere in the frozen pre-registration and has no deviation entry, yet §3.4 presents it as part of the design. | Either the frozen §8 text that defines the six-features-plus-overlap-and-question-length variant, with its hash, or a dated §10 entry declaring it exploratory and the time it was first run; plus one sentence in §3.4 and §4.1 labelling it post hoc if it was computed after the gate results. |
| 25 | 1 (novelty_skeptic) | H1 is reported as REFUTED although the confirmatory operating point cannot exercise the criterion, so a measurement collapse is presented as evidence about negative hardness. | State in the abstract and §4.2 that at 5.27% coverage three rungs are at 100.00% and R2 at 279/280, that the CI [0.00, 0.00] is a boundary bootstrap, and report H1 as not testable at the registered point with the exploratory 7.00-point drop [4.50, 9.75] as the only measured ordering. |
| 26 | 1 (novelty_skeptic) | 'The ladder is a ladder of lexical overlap' states an identifiability result as a hardness ordering, and the paper's own rung precisions contradict the ordering. | Either a per-rung overlap statistic showing precision ordered by overlap magnitude, or a rewritten sentence saying only that overlap separates each rung from answerable items, with the R2 91.07 versus R3 92.75 inversion and R5 89.25 stated beside it. |
| 27 | 1 (novelty_skeptic) | Section 4.4 misstates where R5 falls in the ordering. | Correct 'between R2 and R3' to 'between R2 (91.07%) and R4 (84.71%)', or report the ordering statistic that puts R5 second of four. |
| 28 | 1 (novelty_skeptic) | Table 7's DeclineCraft row mischaracterises the cited benchmark and contradicts the paper's own description of it. | Rewrite the row from arXiv:2610.28340 (title and abstract: retrieval and parametric abstention measured jointly; reported quantity is Correct Abstention Rate per model and retrieval condition), removing 'several unanswerable classes' and 'retrieval and memory reported separately' unless a named section of the source supports them. |
| 29 | 1 (novelty_skeptic) | The matched-recall comparison that carries H3 is degenerate by construction because the matched single threshold is the band's own lower threshold. | Report that single_matched_recall.t = 0.90722098925 equals band.t_lo = 0.90722098925, so only the upper cut can differ, replace the claim that zero discordant pairs is 'not a binning artefact' with what the construction guarantees, and give the number of held-out items scoring above t_hi. |
| 30 | 1 (reproducibility_reviewer) | The artefact is unpinned: no requirements or lockfile exists, no library version appears in the paper, and the two model checkpoints are given without revisions. | A pinned requirements.txt or lockfile that regenerates the recorded environment, the two Hugging Face model revisions with weight hashes, and one sentence in §8 naming them, verified by rerunning features.py to features.csv with sha256 f9de87f6... (data/features_meta.json). |
| 31 | 1 (reproducibility_reviewer) | The frozen run records preregistration_sha256 as '#', so the run does not evidence which pre-registration text it executed. | Fix the parser to store c24a9e51... (or the hash actually in force at run time) in the results file, re-run, and quote the field value in §7. |
| 32 | 1 (reproducibility_reviewer) | The deviation log stops at D3 while §4.6 and §8 describe the corrected dense run as 'deviation D4'. | A dated §10 entry D4 recording when the corrected features were first run and whether that was before or after the frozen numbers were seen, plus a fourth hash in PREREGISTRATION.sha256; or drop the word 'deviation' and label the corrected analysis post hoc wherever it is cited. |
| 33 | 1 (reproducibility_reviewer) | §8 omits the commands that produce two reported results: the transfer item builder and the reader baseline. | Add 'python 04_experiments/src/build_transfer_items.py' before features_transfer.py and 'python 04_experiments/src/reader_logprob.py' before the script that consumes reader_features.csv, and state in §4.7 and §4.8 which file each number (n=553, AUROC 0.419; 400 transfer items) comes from. |
| 34 | 1 (reproducibility_reviewer) | Table 4 juxtaposes two runs whose fitted operating points differ, and the column header labels the frozen run as deviation D1. | Print the corrected thresholds beside the frozen ones ([0.9072, 0.9478] to [0.5232, 0.5370]) and mark the precision and coverage rows as different cuts with AUROC as the only threshold-free comparison, as c1_corrected/SUMMARY.md already does; retitle the column 'frozen run' since D1 is the exploratory operating point. |
| 35 | 1 (reproducibility_reviewer) | No table in the draft is numbered or captioned, so no 'Table N' reference can be resolved and three cross-references point at the wrong sections. | Number and caption every table in order of appearance and correct the references (audit table in §4.1, per-rung in §4.2, arms in §4.4, frozen-versus-corrected and ablations in §4.6, prior work in §2), plus the §4.2 '(§4.5)' and §2 '(§4.8)' section references; the generator prefixes T1-T7 do not match appearance order. |
| 36 | 1 (reproducibility_reviewer) | Table 7 is a hardcoded string in the table generator and carries no traceability markers, contradicting the title page's statement that every table is generated from a results file. | Generate Table 7 from a checked-in source (a prior-work CSV with a citation-id column) or amend the title-page sentence to say which tables are generated and which are hand-written, and add the five cited identifiers to the citation register so the citation checker covers them. |
| 37 | 1 (reproducibility_reviewer) | The frozen run was produced from a dirty working tree and no diff was stored, so the recorded commit does not identify the code that produced the headline numbers. | Re-run from a clean checkout at a recorded commit, or commit the diff and the post-diff source hashes so that commit plus patch identifies the executed code; state in §8 which of the two the reported numbers come from. |
| 38 | 1 (clarity_reviewer) | The abstract reports two headline numbers on different denominators in one sentence, so a reader cannot tell whether the gate answers one question in four or one in twenty. | Both figures restated over one population (coverage = questions answered / questions asked = 98/400 = 24.5%), and 'about one question in twenty' in Section 5.1 corrected or replaced by that number. |
| 39 | 1 (clarity_reviewer) | 'Abstain precision' is undefined and the reported cells are the per-rung refusal rate, not the precision of refusals. | A one-sentence definition with numerator and denominator, the number of refusals behind every cell, and the eight per-rung cells recomputed as (negatives refused)/(all refusals): the R2 cell becomes 279/(279+302) = 48.0%, not 99.64%. |
| 40 | 1 (clarity_reviewer) | No table is numbered or captioned, and the in-text table numbers do not resolve against the tables as printed. | Sequential numbers and self-contained captions (what is plotted, n, split, units) for all eight tables, with every in-text reference rewritten to the appearance order. |
| 41 | 1 (clarity_reviewer) | There is no figure anywhere in the draft, so the paper's central trade-off has no visual form and the abstract has no Figure 1 to be read against. | The generated figure asset already in 05_paper/figures/generated inlined in the draft with a caption (what is plotted, n, split, units), and, given the metric problem above, one panel plotting abstain precision and over-refusal against coverage with the registered operating point marked. |
| 42 | 1 (clarity_reviewer) | Two cross-references send the reader to the wrong section. | The dense-column pointer changed to Section 4.6 and the reader-baseline pointer changed to Section 4.7, checked against the section that actually reports each number. |
| 43 | 1 (clarity_reviewer) | The arm table names the wrong conditional for its 87.30% cell. | Both conditionals stated with their denominators: P(refused \| miss) = 63.22% and P(miss \| refused) = 87.30%, with the cell relabelled to say which one it reports. |
| 44 | 1 (clarity_reviewer) | The paper claims coverage is reported beside every precision figure, and it is not. | A coverage column added to all five arm rows, or the contribution and the related-work table narrowed to the two tables where the claim is true. |

## Per-persona overall score

| Persona | Round 1 | Round 2 | Delta |
|---|---:|---:|---:|
| methodologist | 4 | 5 | +1 |
| domain_expert | - | 4 | n/a |
| statistician | 4 | 5 | +1 |
| novelty_skeptic | 3 | 4 | +1 |
| reproducibility_reviewer | 5 | 6 | +1 |
| clarity_reviewer | 4 | 4 | +0 |

---

_Generated by `tools/simulate_review.py compare`. Simulation, not a venue
decision._
