# STUDENT DIGEST — S3 (what we built, what failed)



## 1. What we built

One corpus, one question set, one feature extractor, one fitting procedure.
Corpus: SQuAD v2.0 dev, split by whole article into dev and held-out halves; 400 answerable questions per half.
Each question shown with 5 passages, one per rung:
R0 gold paragraph; R1 random other paragraph; R2 paragraph with the question's highest-IDF content token; R3 the adjacent paragraph; R4 gold paragraph with first answer span replaced by a same-surface-type value.
That gives 3752 items (1879 held out) (draft as of 2026-11-08; may change in round 3).
[paper §3.1]

Gate: logistic regression on 12 standardised retrieval features, fitted on dev only.
Operating points fitted on dev: band [0.9072, 0.9478] and single threshold 0.9394, both maximising dev abstain recall subject to dev abstain precision 0.80 (draft as of 2026-11-08; may change in round 3).
[paper §3.2, §3.3]

Separability audit before any result: logistic regression on 6 surface features with 5-fold CV per rung; any rung above AUROC 0.750 (draft as of 2026-11-08; may change in round 3) is rebuilt; sensitivity variant adds question-passage overlap.
[paper §3.4]

Three hypotheses frozen before any result run: H1 hardness monotonicity, H2 transfer, H3 two-sided beats one-sided.
[paper §1, §3]

## 2. What we measured

Audit: on 6 surface features no rung separates from answerable items (AUROC 0.506, 0.539, 0.488, 0.415) (draft as of 2026-11-08; may change in round 3).
Add question-passage overlap and Rung 1 is almost perfectly identifiable (0.977) (draft as of 2026-11-08; may change in round 3); Rung 4 is 0.408 (draft as of 2026-11-08; may change in round 3).
[paper §4.1, Table 3]

Registered point: band refuses 100.00%, 99.64%, 100.00%, 100.00% of Rungs 1-4 (draft as of 2026-11-08; may change in round 3), refuses 75.50% of answerable questions (draft as of 2026-11-08; may change in round 3), answers 24.50% (draft as of 2026-11-08; may change in round 3).
Pooled precision of refusals 83.03% (draft as of 2026-11-08; may change in round 3); per-rung precision 56.98% (Rung 1) and 48.02% (Rung 2) (draft as of 2026-11-08; may change in round 3).
[paper §4.2, Table 1]

H1 refuted: Rung 1 minus Rung 3 = 0.00%, CI [0.00%, 0.00%] (draft as of 2026-11-08; may change in round 3).
H3 refuted: band minus matched single = 0.00%, CI [0.00%, 0.00%] (draft as of 2026-11-08; may change in round 3).
H2 degenerate: dev-to-test loss 0.07% (draft as of 2026-11-08; may change in round 3); 92.95% of dev items refused by the lower threshold alone (draft as of 2026-11-08; may change in round 3).
[paper §4.2, Table 2]

Exploratory, coverage-capped (D1): over-refusal 9.50%, coverage 25.44% (draft as of 2026-11-08; may change in round 3); Rung 1 to Rung 3 drop 7.00%, CI [4.50%, 9.75%] (draft as of 2026-11-08; may change in round 3).
[paper §4.3]

## 3. What failed and why that is still a result

The registered rule produced a gate that refuses 75.50% of answerable questions (draft as of 2026-11-08; may change in round 3) and answers only 24.50% (draft as of 2026-11-08; may change in round 3).
The ladder's refusal rate saturated near 100% on every rung, so H1 could not be tested as intended.
H3's band was identical to its own lower threshold.
H2's "transfer" was trivial: a gate refusing 92.95% of dev items on its lower threshold alone (draft as of 2026-11-08; may change in round 3) cannot fail to transfer.

Why this is still a result: the audit shows the rungs differ mainly in question-passage overlap (0.977 with overlap added) (draft as of 2026-11-08; may change in round 3), which is exactly what a lexical retriever scores.
So the ladder measured overlap, not answerability.
The over-refusal number (75.50%) (draft as of 2026-11-08; may change in round 3) makes the precision figure (83.03%) (draft as of 2026-11-08; may change in round 3) interpretable.
A precision target without a coverage constraint is not a specification.
[paper §4.2, §4.1, §5.1]

The paper's contribution is the instrument and the measurement of that pathology, not a better gate.
[paper §1, §5]

## 4. What the 12.53% swapped-answer (Rung 4) finding means

Rung 4 replaces one answer span inside the gold passage, so the passage still matches the question but the answer is wrong.
In the frozen run the dense block was degenerate: the dense query was the passage itself, so dense_presented and dense_top1 were always identical, and the dense cosine was exactly one on 78.70% of rows (draft as of 2026-11-08; may change in round 3).
That hid the failure.

After correction (question-to-passage cosine), Rung 4's exploratory refusal falls to 12.53% (draft as of 2026-11-08; may change in round 3), and held-out AUROC falls from 0.982 to 0.874 (draft as of 2026-11-08; may change in round 3).
Rungs 1-3 stay in the nineties (99.75%, 92.86%, 95.50%) (draft as of 2026-11-08; may change in round 3).
So the gate cannot detect a passage that matches the question but carries a wrong answer span; that is the failure mode it should have, and the frozen run hid it.
The corrected run is the one to carry forward.
[paper §4.6, Table 4; §5.3]

## 5. What the paper does NOT claim

- It does not claim a new gate or better abstention performance; it claims an audit and a measurement of a pathology.
  [paper §1, §5]
- It does not claim the two-threshold idea is new; a 2025 paper (arXiv:2502.07255) already does two thresholds.
  [STUDENT-DIGEST-S2]
- It does not claim generality beyond one corpus family, one language, passage-level question answering, one feature stack, one gate family.
  [paper §6, item 1]
- It does not claim the frozen run's AUROC 0.982 (draft as of 2026-11-08; may change in round 3) is real; it discloses the dense defect and reports both runs.
  [paper §4.6, §5.3]
- It does not claim H1, H2, or H3 are supported; all three are refuted or degenerate.
  [paper §4.2, Table 2]
- It does not claim the corrected run is a fresh pre-registered replication; it is a declared sensitivity analysis (deviation D4).
  [paper §4.6]


