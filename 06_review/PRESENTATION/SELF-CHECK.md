# Self-Check Quiz — Does the Answer Hold Up?

For Shubh. Read the paper first, then test yourself. Questions are in plain English and follow the paper in order. Try to answer without looking, then check the Answer Key at the end. Every answer is grounded in `05_paper/draft/paper.md`.

---

## Questions

**Q1. Abstract — What is the main result in one sentence?**
At the pre-registered operating point, what are the over-refusal rate, the answer rate, and the pooled precision? What did the three hypotheses do?

**Q2. §1 Introduction — What are H1, H2, and H3 exactly?**
State the three frozen hypotheses and the numeric criterion for each.

**Q3. §2 Related work — Why does the paper cite Abdumalikov et al.?**
What accuracy collapse was reported, and what is the lesson the paper takes from it?

**Q4. §3.1 Items — How were the ladder items built?**
Give the SQuAD v2 dev size, how many questions were sampled per half, the total item count, and what each rung R0–R4 presents. Why is R2 short?

**Q5. §3.2–§3.3 Features and gate — What does the gate see, and where did the thresholds land?**
How many features are there, what are the fitted band and single-threshold values, and why does the paper call the admit region degenerate?

**Q6. §3.4–§3.5 Audit and naming — What is the separability audit gate, and what naming correction was made?**
State the audit gate, the rebuild rule, and the difference between refusal rate and precision.

**Q7. §4.1 Audit results — What did the audit show?**
Give the six-feature AUROC for R1–R4 and the overlap-variant AUROC for R1–R3. What does the overlap number mean?

**Q8. §4.2 Registered operating point — Why are H1 and H3 refuted?**
Give the band refusal rates for R1–R4, the R1 minus R3 difference with its CI, the H3 difference, and the precision on R1 and R2.

**Q9. §4.3 Exploratory point — What changes when coverage is constrained?**
State the exploratory rule, the over-refusal and coverage, and the R1-to-R3 drop with its CI. Does it rescue any hypothesis?

**Q10. §4.4 R5 control — What was R5 built to test, and what happened?**
How was R5 built, what is its matching quality, and its exploratory refusal rate with CI?

**Q11. §4.5 Top-1 variant — What objection does this arm answer, and what did it find?**
State the hit rate, the detection AUROC, the refusal rates on hits vs misses, and the interpretation caveat.

**Q12. §4.6 Dense correction — What was the bug, and what changed when it was fixed?**
How was the dense query wrong, what was the degenerate rate, and what happened to held-out AUROC, R4 refusal, and H3?

**Q13. §4.7–§4.8 Robustness and second corpus — What checks were run, and what did they conclude?**
Cover: (a) is the short R2 rung biased? (b) does the reader-confidence baseline work? (c) does the second corpus transfer?

**Q14. §5 Discussion — What is the paper's main lesson for practitioners?**
State the coverage–precision lesson and what a retrieval-feature gate actually measures.

**Q15. §6–§8 Threats, disclosure, and reproduction — What are the limits and how do you reproduce this?**
Name at least three threats to validity, the AI-assistance disclosure line, and where the reproduction commands live.

---

## Answer Key

**A1. Abstract.**
The gate is a negative result: at the registered rule (maximise abstain recall subject to dev abstain precision 0.80) the gate over-refuses 75.50% of answerable questions, so it answers only 24.50%, and pooled precision is 83.03%. Per-rung refusal rate is 100.00% (R1), 99.64% (R2), 100.00% (R3), 100.00% (R4) — H1 refuted with R1 minus R3 = 0.00%, 95% CI [0.00%, 0.00%]; H3 refuted with difference 0.00%, CI [0.00%, 0.00%]; H2 degenerate with loss 0.07%. The useful output is the audit (see Q7) and the control arms.

**A2. §1 H1–H3.**
H1 hardness monotonicity: abstain precision (refusal rate) is non-increasing across rungs and falls by at least 15 points from R1 to R3. H2 operating-point transfer: the dev-fitted point loses at least 10 points of abstain precision at equal abstain recall on a disjoint held-out half and a second corpus. H3 two-sided beats one-sided: the two-threshold band beats the best single threshold on the same score by at least 5 points at matched abstain recall.

**A3. §2 Related work.**
Abdumalikov et al. (arXiv:2403.01461) train on random negative excerpts, then evaluate on high-semantic-overlap excerpts: accuracy falls from 98% to 1%. The paper's lesson: the negative sampler, not the gate, was doing most of the work in the earlier numbers. A gate measured only on random negatives would look finished.

**A4. §3.1 Items.**
SQuAD v2 dev: 35 articles, 1204 paragraphs, 11873 questions, of which 5928 are answerable. Articles are split whole into dev and held-out halves; 400 answerable questions per half are sampled, each with five passages: 3752 items total (1879 held out). R0 = gold paragraph; R1 = uniformly sampled other paragraph from same split pool; R2 = paragraph containing the question's highest-IDF content token; R3 = adjacent paragraph (before/after gold) in same article; R4 = gold paragraph with its first answer span replaced by a same-surface-type value. R2 is short (273 dev items) because most questions have no content word occurring in a paragraph other than their own; the rung is reported at true size, not topped up.

**A5. §3.2–§3.3 Gate.**
12 retrieval-side features: BM25 score and log-rank, corpus top-1 and mean-top-5, top-1/top-2 margin; same four for dense cosine; BM25–dense agreement on top doc; cross-encoder score; question–passage token overlap. Logistic regression on dev only. Fitted band is [0.9072, 0.9478], width 0.0406; single threshold is 0.9394. Degenerate because dev admit mass is only 6.03% and 92.95% of dev items are refused by the lower threshold alone — the upper threshold almost never binds, so the band and the single threshold are the same gate.

**A6. §3.4–§3.5 Audit and naming.**
Audit: logistic regression on 6 surface features (characters, tokens, digit ratio, upper-case ratio, punctuation ratio, mean word length) with 5-fold CV per rung. Gate AUROC is 0.750. Any rung above it is rebuilt by length-matched resampling at most twice; if two or more rungs still fail the run stops. Sensitivity variant adds question–passage overlap and question length. Naming correction: the pre-registration called P(refused | negative) "abstain precision" but that is a recall on the rung. The paper reports both, labelled: refusal rate = P(refused | negative) (quantity H1/H3 are stated over), precision = P(negative | refused) over the rung's items plus answerable items. Pooled precision is 83.03% at the registered point and 97.29% at the exploratory point.

**A7. §4.1 Audit.**
Six surface features: R1 0.506, R2 0.539, R3 0.488, R4 0.415 — no rung is separable, so the ladder is not a formatting artefact. With overlap added: R1 0.977, R2 0.889, R3 0.923 (R4 0.408; R5 0.721 surface, 0.794 with overlap). Meaning: the rungs differ mainly in question–passage word overlap, exactly what a lexical retriever scores. This predicts the main result before the gate is fitted. R4 is the exception because its passage IS the gold passage.

**A8. §4.2 Registered point.**
Band refusal: R1 100.00%, R2 99.64%, R3 100.00%, R4 100.00%. H1: R1 minus R3 = 0.00%, 95% CI [0.00%, 0.00%]; sequence is not non-increasing; 15-point criterion not met — refuted. H3: band vs recall-matched single = 0.00%, CI [0.00%, 0.00%]; over-refusal is worse for the band (75.50% vs 72.50%) — refuted. H2: dev-to-test loss is only 0.07%, so it transfers degenerately (a gate refusing 92.95% of dev on the lower threshold alone cannot fail to transfer). Precision of refusals is only 56.98% on R1 and 48.02% on R2 — most refusals are answerable questions. Dev precision at the fitted band is 83.69%, so the rule did what it was asked; what it was asked was not enough.

**A9. §4.3 Exploratory.**
Deviation D1: maximise dev recall subject to precision 0.80 AND dev over-refusal at most 0.10. It keeps over-refusal at 9.50% with coverage 25.44%. Per-rung refusal now falls: 99.75% (R1), 91.07% (R2), 92.75% (R3), 84.71% (R4), with precision 87.03–91.30%. R1-to-R3 drop is 7.00%, CI [4.50%, 9.75%] — real but about half the predicted 15 points, and not monotone (R2 below R3). R1-to-R4 is 15.04%. No hypothesis is rescued; the confirmatory verdict stands.

**A10. §4.4 R5.**
R5 tests whether overlap is the whole story: for each question, the candidate paragraph whose overlap with the question is closest to the gold paragraph's overlap (D2). Matching quality: mean absolute overlap difference 10.29% on held-out vs 42.08% for a random negative — closer than any other rung, but not exact. Result: R5 negatives are still refused at 89.25%, 95% CI [85.75%, 91.75%] at the exploratory point (100.00% at confirmatory band), AUROC 0.974. It sits between R2 (91.07%) and R4 (84.71%). Conclusion: matching one signal is not enough; R5 items also differ in length and other correlated signals. The surface audit is closest to its gate on this rung (0.721) without crossing it.

**A11. §4.5 Top-1 variant.**
Objection: answerable items always show the gold paragraph while negatives never do, so the gate may read "is this the document retrieval found" rather than answerability. Variant D3: every item presents the BM25 rank-1 paragraph, labelled answerable only if it is the gold paragraph. Hit rate is 78.25% on held-out. The same stack detects retrieval correctness at AUROC 0.945, refuses 63.22% of misses and 2.56% of hits, and P(miss | refused) = 87.30%. Caveat: the label IS retrieval correctness here, so "detects misses" and "detects unanswerable" coincide. It confirms the mechanism and does not exculpate the gate.

**A12. §4.6 Dense bug.**
Bug: the dense query was the presented passage itself, not the question, so `dense_presented` and `dense_top1` were identical, dense cosine was exactly 1 on 78.70% of as-run rows (all R0–R3, none of R4), and `dense_rank_log` was constant. The gate had ten informative columns, not twelve. Fix (D4, sensitivity analysis): re-implement question-to-passage cosine per §3.2. Changes: held-out AUROC falls 0.982 → 0.874 (dev 0.988 → 0.887); exploratory R4 refusal collapses to 12.53% while R1–R3 stay in the nineties; confirmatory verdicts do not change (H1 still 0.00%); H3 becomes −2.23%, CI [−3.11%, −1.35%] (band worse than single); dense baseline B2 goes from 74.58% pooled (artefact, constant score) to 99.73% pooled at 0.27% coverage (real score, degenerate point). Ablations: no single group carries the result; removing dense costs 0.874 → 0.862, overlap alone reaches 0.811.

**A13. §4.7–§4.8 Robustness and second corpus.**
(a) R2 bias: of 400 sampled questions, 273 kept an R2 item, 127 did not. No variable (question length, answer surface type, gold paragraph length, article size) differs at 5% in either split; smallest p = 0.052 on dev question length. R2 describes the sampled set, with the caveat several p-values sit between 5–10%. Article-clustered intervals leave every verdict unchanged.
(b) Reader baseline fails: n = 553 dev items, mean generated-token log-probability AUROC 0.419 (worse than chance). A refusal string emitted at near-certainty scores as high confidence, so mean log-probability measures fluency, not evidential support. Reported as exploratory only.
(c) Second corpus (multi-hop, 400 items): confirmatory 98.50% precision at 89.50% over-refusal (same degeneracy, uninformative); exploratory 85.50%, CI [79.50%, 89.50%], a drop of 7.25 points vs main R3. AUROC falls 0.982 → 0.640. H2's second arm is inconclusive by the registered rule (5–10 point loss has no verdict). Reading: operating-point transfer survives, discrimination transfer does not — direction only.

**A14. §5 Discussion.**
A precision target without a coverage constraint is not a specification: the registered rule produced a gate answering about one question in four (24.50%) with refusals only 83.03% true negatives. Any paper reporting abstention without over-refusal and coverage beside it is reporting a choice about how often to refuse. Retrieval-feature gates measure match between passage and question and likelihood the passage is the retrieved document; on paragraph-substituted negatives those move with answerability, but when they come apart (R4: passage matches perfectly, one span wrong) the gate has nothing to work with. The rung that changes what the passage says must be in the ladder or the ladder measures the wrong thing. The corrected run should be carried forward, not the frozen one.

**A15. §6–§8 Limits, disclosure, reproduction.**
Threats (any three): one corpus family/language/English passage-level QA, one feature stack, one gate family; gold paragraph shown for answerables (part of discrimination is retrieval-found-the-gold); R2 incomplete (273 dev / 280 held-out vs 400 sampled); R4 substitutions automatic and sometimes ungrammatical; second-corpus arm is a direction test with a different construct; reader baseline covers only 553 dev items; gate fitted on 1873 dev items (no corpus-level uncertainty); frozen dense block was degenerate — needs a fresh pre-registered replication with corrected features.
Disclosure: public data only (SQuAD v2.0 dev share-alike; multi-hop corpus Apache), student is responsible author, AI agents wrote analysis code, ran experiments, drafted sections, and performed the simulated review (labelled as simulation, not a venue decision).
Reproduction: commands are in §8 of the paper, starting with `build_items.py`, `features.py`, `run_c1.py`, then the corrected and control-arm scripts, ending with `make_paper_assets.py`, `build_draft.py`, and `tools/check_numbers.py --draft 05_paper/draft/paper.md`.

---

*End of quiz. Score yourself honestly: if you cannot explain Q6 (naming), Q8 (why the ladder disappears), and Q12 (the dense bug) without re-reading, re-read those sections before the viva.*
