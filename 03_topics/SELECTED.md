# SELECTED — topic decision
S2 · 2026-11-03 · decides `03_topics/PROPOSAL.md` · **requires head approval before any experiment**

## Rank 1 — "How Hard Are Your Negatives? A Hardness Ladder for Retrieval-Feature Abstention Gates"
(candidate C1, 86/100 in `03_topics/CANDIDATES.md`; narrowed by `02_literature/NOVELTY-CHECK.md`)

One fixed small reader, one fixed corpus, four rungs of negative hardness, and a gate built only from
retrieval features with two dev-fitted thresholds (admit / refuse, dead zone between). Report abstain
precision, abstain recall and over-refusal rate at every rung, then test whether the operating point
transfers to a second corpus.

Why this one wins, in order of weight:

1. **Feasibility is measured, not assumed.** The laptop numbers this depends on already exist from S2:
   BM25 builds a 5,882-item index in 0.11 s and answers in 0.04 ms (recall@5 0.459); MiniLM embeds the
   corpus in 20 s at 600 MB; a cross-encoder rerank costs 361 ms/query and *loses* to plain BM25. The one
   expensive step is generation, and features are cached once and reused across all gate variants, so the
   3,200-item matrix is hours, not days.
2. **The personal edge is a measured pathology, not a hobby.** A gate that refused 47 of 82 answerable
   questions at precision 0.30 because its threshold sat outside the observed feature range is exactly
   what a two-sided band with a reported placement diagnostic repairs. No paper in the sweep reports that
   pathology; the student can speak to it from his own instrument.
3. **The failure mode is a legitimate result.** If the ladder shows no monotone hardness effect, or the
   band does not beat a single threshold, that is publishable as a negative result — the post-hoc
   calibration literature predicts it, so the null is informative rather than embarrassing.
4. **It needs no judge.** Every metric is computed from labels and arithmetic. There is no API bill and no
   judge-error confound to defend.

The honest deficit: `NOVELTY-CHECK.md` rates this **incremental**, not novel. Three 2026 papers hold the
gate, the ladder and the two-direction reporting separately (RINSE, GRAB-RAG, DeclineCraft). What is open
is their intersection with cheap retrieval-only features and a reported false-refusal column. That is a
workshop contribution and the proposal says so in its own "what we will NOT claim" section.

## Runner-up — "Operating Points, Not F1: A Small SMS Scam Detector at 0.1–1% Prevalence on Code-Mixed
Indian English" (candidate C3, 80/100)

Switch to this if, and only if, one of the following happens by day 3 of the C1 build:
- the rung-3 negatives turn out to be separable by surface features (the audit's AUROC > 0.75 rebuild
  rule fires twice), or
- the gate's abstain precision is flat across rungs, which removes the phenomenon the paper is about.

Why it is second and not first: its headline claim (base rates destroy precision) is already published in
another domain by arXiv:2610.41803, so our contribution is a domain transfer to an Indian code-mixed
corpus with a cost-ratio threshold. It is the lowest-variance path to *a* paper and the highest risk of
being called "just a classifier". It is also the strongest fallback because the artefact is a table that
cannot fail to exist once the threshold sweep runs.

## Demoted — memory staleness (C2, was 85/100)
`NOVELTY-PRESCAN.md` found three 2026 papers already occupying it, including one that separates "missed
the update" from "had it and did not use it" — the exact split C2 proposed. C2's novelty component was
scored before that scan existed. Re-scored at 8/25 it totals ~68/100. Do not start it. The lesson is
recorded here rather than quietly fixed: rubric scores are provisional until a novelty scan runs.

## Ranked table

| Rank | Topic | Score | Verdict |
|---:|---|---:|---|
| 1 | C1 hardness ladder for retrieval-feature abstention | 86 | Build this; incremental but defensible |
| 2 | C3 scam operating points at sub-1% prevalence | 80 | Fallback at day 3; lowest variance |
| 3 | C4 Hindi/Hinglish abstention transfer | 80→72 after scan | Result forecastable by 2026 prior work |
| 4 | C2 memory stale-hit rate | 85→~68 after scan | Occupied by three 2026 papers — do not start |
| 5 | C5 quantisation cliff at 1–3B | 61 | Measurement without a decision attached |

## What the head is being asked to approve
That the lab commits to C1 as the paper, with C3 held as the day-3 fallback and C2 abandoned. If
approved, write `TOPIC APPROVED` in `orchestration/HEAD-REVIEW.md`; S3 then pre-registers the protocol in
`04_experiments/` before running anything. Two conditions should be attached to any approval:

1. The novelty check must be completed against OpenAlex and Semantic Scholar before the draft's
   introduction claims any gap. The current check is one index deep and says so.
2. The negative-set separability audit is a gate, not an appendix: if the surface-only adversary exceeds
   AUROC 0.75 on any rung, that rung is rebuilt before any result is reported.
