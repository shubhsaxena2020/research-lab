# Slides outline — "How Hard Are Your Negatives?"

Talk: 10–12 slides, ~12–15 minutes. Numbers copied from `05_paper/draft/paper.md` (draft as of 2026-11-08; may change in round 3). Marked quantities are the paper's reported values.

---

## Slide 1 — Title

**Title:** How Hard Are Your Negatives? A Pre-Registered Audit of Negative Ladders for Retrieval-Feature Abstention Gates, with a Negative Result

**Subtitle:** Shubh, PSIT, BCA first semester. AI disclosure: agents wrote analysis code, ran experiments, drafted sections and performed simulated review; human-directed (§7).

**Speaker notes:**
- Open with the one-line claim: "I built a gate that decides whether a retrieved passage supports an answer, and I measured how hard it looks under four kinds of negatives. The headline result is negative and specific."
- State up front that the contribution is the audit, not a new gate. (draft as of 2026-11-08; may change in round 3)

---

## Slide 2 — Problem

**Bullets:**
- A retrieval-augmented system that always answers sometimes answers from a passage that does not support the question.
- An abstention gate decides, before generation, whether to answer from the passage.
- Gates are built from retrieval signals (lexical, dense, reranker) and evaluated against a set of negatives usually described in one sentence.
- That sentence matters: Abdumalikov et al. (arXiv:2403.01461) report accuracy falling from 98% to 1% when random-negative training is tested on high-overlap excerpts. (draft as of 2026-11-08; may change in round 3)

**Speaker notes:**
- Explain "abstention gate" in plain words: a yes/no filter before the answer is generated.
- The Abdumalikov swing (98% → 1%) is the observation this whole paper is built on.
- Thesis: a gate measured only on random negatives looks finished; the negative sampler was doing most of the work. (draft as of 2026-11-08; may change in round 3)

---

## Slide 3 — Setup

**Bullets:**
- Corpus: SQuAD v2.0 dev — 35 articles, 1204 paragraphs, 11873 questions, 5928 answerable. Only answerable rows used. (draft as of 2026-11-08; may change in round 3)
- Articles split whole (never at paragraph level) into a dev half and a held-out half.
- Sample 400 answerable questions per half; each question presented with 5 passages (one per rung).
- 12 retrieval-side features per item (BM25 score/rank/top-1/top-5/margin; dense cosine equivalents; BM25–dense agreement; cross-encoder score; question–passage token overlap). (draft as of 2026-11-08; may change in round 3)
- Gate: logistic regression on standardised features, fitted on dev only. Operating rule: maximise dev abstain recall subject to dev abstain precision ≥ 0.80. (draft as of 2026-11-08; may change in round 3)

**Speaker notes:**
- Stress "article-disjoint": the held-out half contains articles the gate never saw, so transfer is a real test.
- The 0.80 precision target is the number a practitioner writes down; it is the registered rule. (draft as of 2026-11-08; may change in round 3)

---

## Slide 4 — The ladder

**Bullets:**
- R0 (answerable): the question's gold paragraph.
- R1 (negative): a uniformly sampled other paragraph from the same split.
- R2 (negative): a paragraph containing the question's highest-IDF content token.
- R3 (negative): the paragraph immediately before or after the gold paragraph.
- R4 (negative): the gold paragraph with its first answer span replaced by a same-surface-type value.
- Total 3752 items (1879 held out); R2 short at 273 dev / 280 held-out items because most questions have no content word appearing in another paragraph. (draft as of 2026-11-08; may change in round 3)

**Speaker notes:**
- The ladder changes one respect at a time: unrelated → topically anchored → adjacent → one span swapped.
- Each rung is a negative; answerable items are R0. The ladder varies construction, not just difficulty. (draft as of 2026-11-08; may change in round 3)

---

## Slide 5 — Separability audit (passes, says something uncomfortable)

**Bullets:**
- Hard gate before any result: a 6-feature surface classifier (chars, tokens, digit ratio, upper-case ratio, punctuation ratio, mean word length) must not tell a rung's negatives from answerable items (AUROC gate 0.750), 5-fold CV.
- Passes on all rungs: R1 0.506, R2 0.539, R3 0.488, R4 0.415, R5 0.721. (draft as of 2026-11-08; may change in round 3)
- Sensitivity variant adds question–passage overlap: R1 0.977, R2 0.889, R3 0.923, R4 0.408, R5 0.794. (draft as of 2026-11-08; may change in round 3)
- Conclusion: rungs are not formatting artefacts; they differ mainly in how much of the question the passage's words cover — exactly what a lexical retriever scores.

**Speaker notes:**
- 0.977 on R1 is the paper's most transferable single measurement: the rungs differ in lexical overlap.
- R4 is the exception (0.408) because its passage is the gold passage. (draft as of 2026-11-08; may change in round 3)

---

## Slide 6 — Result at the registered operating point

**Bullets:**
- Band refuses 100.00% / 99.64% / 100.00% / 100.00% of R1–R4 negatives. (draft as of 2026-11-08; may change in round 3)
- Over-refusal 75.50% of answerable questions; answers only 24.50% of questions asked. (draft as of 2026-11-08; may change in round 3)
- Pooled precision of refusals 83.03%. Per-rung precision of refusals: R1 56.98%, R2 48.02%. (draft as of 2026-11-08; may change in round 3)
- Fitted band [0.9072, 0.9478], width 0.0406; single threshold 0.9394; dev admit mass 6.03%; 92.95% of dev items refused by the lower threshold alone. (draft as of 2026-11-08; may change in round 3)

**Speaker notes:**
- Read Table 1: refusal rate saturates near 100% on every rung, so the ladder "disappears."
- The band's refusals are mostly answerable questions, not negatives. (draft as of 2026-11-08; may change in round 3)

---

## Slide 7 — Why it is negative (hypotheses refuted)

**Bullets:**
- H1 hardness monotonicity (criterion ≥15 points, non-increasing): R1−R3 = 0.00%, 95% CI [0.00%, 0.00%]. REFUTED. (draft as of 2026-11-08; may change in round 3)
- H2 transfer (loss ≥10 points): dev-to-held-out loss 0.07%. REFUTED-as-transferring, degenerately. (draft as of 2026-11-08; may change in round 3)
- H3 two-sided beats one-sided (≥5 points): difference 0.00%, 95% CI [0.00%, 0.00%]. REFUTED. (draft as of 2026-11-08; may change in round 3)
- Cause: a precision target with no coverage constraint is satisfied by refusing almost everything; the admissible region is degenerate.
- Dev precision at the fitted band 83.69% — the rule did exactly what it was asked; what it was asked was not enough.

**Speaker notes:**
- The two-sided band equals its own lower threshold to five decimals; the upper threshold never binds.
- A gate that refuses 92.95% of dev items on its lower threshold alone cannot fail to transfer. (draft as of 2026-11-08; may change in round 3)

---

## Slide 8 — Coverage-constrained point (exploratory)

**Bullets:**
- Second operating point (deviation D1): maximise dev recall subject to precision ≥0.80 and dev over-refusal ≤0.10.
- Over-refusal 9.50%, coverage 25.44%. (draft as of 2026-11-08; may change in round 3)
- Per-rung refusal rate now falls: R1 99.75%, R2 91.07%, R3 92.75%, R4 84.71%; precision of refusals 87.03–91.30% in every rung. (draft as of 2026-11-08; may change in round 3)
- R1−R3 drop 7.00% (95% CI [4.50%, 9.75%]) — real, but about half the pre-registered 15-point criterion, and not monotone (R2 < R3). R1−R4 15.04%. (draft as of 2026-11-08; may change in round 3)
- Conclusion: the ladder is not invisible; it is bought out by coverage at the registered point.

**Speaker notes:**
- This rescues no hypothesis; the confirmatory verdict stands.
- Exploratory numbers are descriptive, not confirmatory. (draft as of 2026-11-08; may change in round 3)

---

## Slide 9 — Swapped-answer finding (R4)

**Bullets:**
- R4 replaces one answer span inside the gold passage; the passage still matches the question perfectly, but the answer is wrong.
- As-run (frozen) gate hid this: dense block degenerate (dense query was the passage itself; dense cosine = 1 on 78.70% of rows). (draft as of 2026-11-08; may change in round 3)
- Spec-corrected re-implementation (question-to-passage cosine): held-out AUROC 0.982 → 0.874; R4 exploratory refusal 84.71% → 12.53%. (draft as of 2026-11-08; may change in round 3)
- R1–R3 stay in the nineties (99.75 / 92.86 / 95.50); R4 collapses to 12.53%. (draft as of 2026-11-08; may change in round 3)
- Interpretation: a feature set scoring how well a passage matches a question has nothing to work with when the passage matches perfectly and one span is wrong — which is exactly the failure mode an abstention gate should have.

**Speaker notes:**
- This is the paper's central constructive finding: the rung that changes what the passage says (not how much it overlaps) breaks the gate.
- Report both runs; the frozen run is the registered result, the corrected run is the one worth carrying forward. (draft as of 2026-11-08; may change in round 3)

---

## Slide 10 — Controls

**Bullets:**
- R5 (overlap-matched negative, exploratory): refused at 89.25% (95% CI [85.75%, 91.75%]); AUROC 0.974. Matching overlap is not enough to hide a paragraph drawn from elsewhere. (draft as of 2026-11-08; may change in round 3)
- Top-1 presented (hit rate 78.25%): AUROC 0.945; refuses 63.22% of misses and 2.56% of hits; P(miss | refused) = 87.30%. A good retrieval-correctness detector — but the label is retrieval correctness, so "detects misses" and "detects unanswerable" coincide. (draft as of 2026-11-08; may change in round 3)
- Second corpus: confirmatory point 98.50% precision at 89.50% over-refusal (same degeneracy); exploratory 85.50% (95% CI [79.50%, 89.50%]); AUROC 0.640. Direction only. (draft as of 2026-11-08; may change in round 3)

**Speaker notes:**
- Three controls agree on one description: the features measure how well the passage matches the question and how likely it is to be the document retrieval wanted.
- Matching one signal (overlap) is not enough; the gate catches correlated signals. (draft as of 2026-11-08; may change in round 3)

---

## Slide 11 — Limitations

**Bullets:**
- One corpus family, one language, passage-level QA, one feature stack, one gate family. (draft as of 2026-11-08; may change in round 3)
- Answerable items present the gold paragraph, so part of discrimination measures whether retrieval found the gold paragraph (§4.5 quantifies it). (draft as of 2026-11-08; may change in round 3)
- R2 incomplete: 273 dev / 280 held-out items vs 400 sampled; exchangeability check p = 0.052 on dev question length. (draft as of 2026-11-08; may change in round 3)
- R4 substitutions are automatic and sometimes ungrammatical.
- Reader-confidence baseline (mean generated-token log-probability) AUROC 0.419 on 553 dev items — worse than chance; reports fluency, not support. (draft as of 2026-11-08; may change in round 3)
- Gate fitted on 1873 dev items; uncertainty reflects item/article resampling, not corpus-level uncertainty. (draft as of 2026-11-08; may change in round 3)
- Second-corpus arm is a direction test with a different construct (no article grouping, shorter passages, multi-hop questions); its confirmatory point is degenerate. (draft as of 2026-11-08; may change in round 3)
- Frozen run's dense block degenerate; both runs reported; neither substitutes for a fresh pre-registered replication.

**Speaker notes:**
- Be honest about what the paper does not claim: no generality beyond one corpus family and one feature stack.
- The gate is fitted on 1873 dev items, so intervals do not capture corpus-level uncertainty.
- The second-corpus arm is a direction test with a different construct, not a generality claim. (draft as of 2026-11-08; may change in round 3)

---

## Slide 12 — What I learned + AI-use disclosure

**Bullets — what I learned:**
- An abstention precision is not interpretable without its coverage and over-refusal beside it.
- A negative-ladder result is not interpretable without an overlap control.
- A precision target without a coverage constraint can be satisfied by refusing almost everything.
- Report implementation defects in the text; do not quietly refit.

**Bullets — AI-use disclosure:**
- Language-model agents wrote analysis code, ran the experiments, drafted sections and performed a simulated review; the simulated review is labelled as a simulation, not a venue decision. (draft as of 2026-11-08; may change in round 3)
- The student directed the work, holds the author position, and is expected to explain every section; `06_review/STUDENT-DIGEST-S3.md` and `06_review/CLAIMS-AUDIT.md` exist for that.
- Public data only (SQuAD v2.0 dev, share-alike; multi-hop corpus dev, Apache); no private or scraped data.

**Speaker notes:**
- Close on responsibility: "I am the responsible author; I can explain every section."
- If asked "did you write this yourself?" answer truthfully: agents assisted code, experiments, drafting and a simulated review; I directed, checked, and own every claim and number. (draft as of 2026-11-08; may change in round 3)
