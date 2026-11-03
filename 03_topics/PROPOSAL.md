# PROPOSAL (2 pages)

## Title
**How Hard Are Your Negatives? A Hardness Ladder for Retrieval-Feature Abstention Gates**

Author: Shubh (PSIT, BCA sem 1). Lead: FORGE/Hermes, S2. Status: awaiting head approval
(`orchestration/HEAD-REVIEW.md`). Target: workshop / student track / arXiv preprint. No experiments have
been run; `04_experiments/PREREGISTRATION.md` must exist before the first one.

## Question
For a fixed 1.5B reader over a fixed passage corpus, does a gate built **only** from retrieval features,
with two thresholds fitted on a dev split (one to admit an answer, one to refuse, a dead zone between),
hold its abstain precision across a ladder of increasing negative hardness — and does its operating point
transfer to a corpus it was not fitted on?

The narrow claim behind the question: abstention gates are usually evaluated on one kind of negative
question, and the literature's own evidence says the choice of negative is worth up to 97 points of
accuracy (98% on random negatives, 1% on high-overlap negatives, same model — arXiv:2403.01461). Nobody
turned that into a designed ablation with a two-sided policy and a reported false-refusal rate.

## Hypotheses (each falsifiable, each with a stated refutation)
- **H1.** Abstain precision falls monotonically with rung hardness, and the drop from rung 1 to rung 3 is
  ≥15 points. Refuted by a flat or non-monotone curve.
- **H2.** A dev-fitted operating point loses ≥10 points of abstain precision on a second corpus at equal
  coverage. Refuted if transfer is within ±5 points.
- **H3.** A two-sided band (admit / dead zone / refuse) beats the best single-threshold gate by ≥5 points
  of abstain precision at matched abstain recall. Refuted if the paired bootstrap interval contains zero.

## Protocol outline
1. **Items — 3,200.** 800 answerable questions and 800 in each of four negative rungs, all built over the
   SQuAD 2.0 dev paragraph pool (11,873 rows, CC BY-SA 4.0).
   - Rung 1 *random*: a uniformly sampled non-gold paragraph.
   - Rung 2 *same-entity*: a paragraph containing the question's subject entity, not the answer.
   - Rung 3 *same-topic near-miss*: the paragraph immediately before or after the gold paragraph in the
     same article — contiguous sections, maximal lexical overlap, the condition that produced the 98%→1%
     collapse.
   - Rung 4 *premise violation*: the gold paragraph with the answer span replaced by a same-type value
     from the same article, so the passage asserts something false and refusal is correct.
2. **Separability audit (a gate, not an appendix).** Passage lengths matched within ±10% per decile across
   rungs; a surface-only logistic regression on six surface features trained per rung, AUROC reported for
   every rung. **Any rung above 0.75 is rebuilt before any result is reported.** Rung 4 also gets a
   paraphrase pass so no template survives.
3. **Features (retrieval-side only, cached once).** top-1 and mean top-5 BM25, top-1 and mean top-5 dense
   cosine (bge-small-en-v1.5, 33.4M), BM25/dense top-1 agreement, cross-encoder rerank score of top-1
   (22.7M). **Six retrieval features, no generator call.** The reader's own answer-token log-probability
   and answer entropy are deliberately NOT in the gate: they are computed only for the separate
   reader-assisted arm (B4/B5), so that "retrieval-only" means exactly what it says and the comparison
   between a retrieval gate and an "ask the model how sure it is" gate is a between-arms comparison, not a
   feature ablation inside one model. §Directives 2026-11-03 flagged the earlier mixed definition; this is
   the fix.
4. **Gate.** Logistic regression on the six retrieval features, fitted on a dev half; two thresholds
   grid-searched for a target abstain precision of 0.80, with the admissible band constrained to the
   observed dev feature range. Report where the fitted thresholds sit relative to that range — this is the
   diagnostic for the pathology that motivates the paper.
5. **Evaluation.** Held-out half, per rung. Then the frozen operating point is applied untouched to 800
   items from 2WikiMultihopQA (400 answerable, 400 rung-3 style) for the transfer test.

## Baselines
- **B1** single threshold on max BM25 — what most deployed systems actually do.
- **B2** single threshold on max dense cosine.
- **B3** logistic regression on the six retrieval features with **one** threshold (the ablation that
  isolates "two-sided" from "more features").
- **B4** reader-assisted arm: the reader's own answer-token log-probability as the gate, i.e. "ask the model
  how sure it is" (Kadavath et al., *Language Models (Mostly) Know What They Know*, arXiv:2207.05221).
  Labelled **reader-assisted** everywhere; it is a separate arm, not a feature of the retrieval gate.
  (Correction on record: the earlier draft cited arXiv:2305.11206, which is LIMA and does not support this
  claim. The ID resolved; the title did not match the sentence. Caught by head review 2026-11-03.)
- **B5** reader-assisted two-sided band: B3's six retrieval features **plus** log-probability and entropy,
  two thresholds. Reported only to answer "does adding the model's own confidence help a two-sided band?",
  and never pooled with the retrieval-only results.
Every baseline is run on the same cached features, same items, same seeds.

## Metrics and statistics
Primary: **abstain precision** TP/(TP+FP) with "refused a negative" as positive, **abstain recall**, and
**over-refusal rate** on answerable items. Secondary: AUROC of each gate within each rung; coverage at
fixed precision; ECE of the gate itself. All comparisons paired by item, 10,000-resample bootstrap with
the seed, resampling order and quantile rule fixed in the preregistration; Holm correction across the
per-rung family of tests. Nothing is reported to more precision than the interval supports.

## Timeline (agent-assisted build; student polishes after)
- **Day 1** corpus + 3,200 items built; separability audit run; rung rebuilds if needed.
- **Day 2** feature extraction end to end, cached; timing log committed.
- **Day 3** gate fitted, thresholds swept, held-out evaluated; **go/no-go against C3 fallback**.
- **Day 4** transfer corpus; refit-vs-freeze comparison.
- **Day 5** baselines B1–B4 + ablations; bootstrap intervals.
- **Day 6** figures, table of results, negative results written as they are.
- **Day 7** internal review (ARGUS pass), preregistration check, claims audit vs `verified_citations.csv`.
Then 2–3 weeks of student rewriting, defence rehearsal, and the venue submission.

## Risks
1. **Negatives too easy** → the paper is a restatement of arXiv:2403.01461. Mitigation: the 0.75 AUROC
   audit is a hard gate, plus length matching and, if needed, an adversarial rebuild that keeps only
   items the audit cannot separate.
2. **A 1.5B reader is too weak, so every gate looks the same** (floor effect). Mitigation: run the whole
   protocol a second time through the dev-time API on a strong model for a 400-item subsample; if the
   ordering of gates changes, that is a finding, and it is reported.
3. **Transfer fails for a boring reason** (different corpus → different feature scale). Mitigation:
   report both frozen and refit-on-transfer numbers, and state that the frozen number is the one the
   hypothesis is about.
4. **Reviewer: "this is RINSE plus GRAB-RAG"**. Mitigation: the paper's contribution is stated as a
   measurement with a number in the abstract, not as a new method; the related-work section names both and
   says exactly what is added (a band, retrieval-only signals, a false-refusal column, a placement
   diagnostic).

## What we will NOT claim
- Not "novel". `NOVELTY-CHECK.md` rates this **incremental** on a one-index sweep; the claim is "nobody
  published this exact measurement", not "nobody thought of it".
- Not state of the art, not better than RINSE or GRAB-RAG — different signals, different object.
- Not a general result about abstention. One reader family, one corpus family, English, passage-level.
- No claim about frontier models: the API run is a robustness check on 400 items, not a benchmark entry.
- No claim that the ladder's rungs are ordered by "difficulty" in any absolute sense — only that they are
  ordered by construction and audited for surface separability.
- No numbers from the student's private memory-system evaluation. Its held-out set was contaminated, so it
  is at most one sentence of motivation, quoted without figures, and never a result, a dataset or a
  reproduced pathology. Everything measured here comes from public data.

## Disclosure
Code, prompts, model IDs, seeds and raw outputs are committed under `04_experiments/`. AI assistance
(agent-written code and analysis, human-directed) is disclosed per the target venue's policy; the student
is the responsible author and can explain every section — see `06_review/STUDENT-DIGEST-S2.md`.
