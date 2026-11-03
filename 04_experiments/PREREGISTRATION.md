# PRE-REGISTRATION — C1 "How Hard Are Your Negatives?"

    status:      FROZEN
    frozen_at:   2026-11-03T03:59+05:30
    author:      S3 (FORGE/Hermes) for Shubh (PSIT, BCA sem 1)
    supersedes:  03_topics/PROPOSAL.md where the two differ (differences are listed in §9)
    gate:        orchestration/HEAD-REVIEW.md Checkpoint 3 line `TOPIC APPROVED` (verified by
                 tools/tests/test_docs_and_cli.py by exact line match, not by grep)

Everything below is fixed before the first result-producing run. The hash in `PREREGISTRATION.sha256`
covers this file byte-for-byte. Any change after the freeze is a **deviation**, appended to §10 with a
timestamp and a reason, never an edit to §1–§8. Numbers in this file that come from measurements are
marked `[pilot]` and are not result values.

## 1. Question and hypotheses

For a fixed passage corpus (SQuAD 2.0 dev) and a fixed question set, does an abstention gate built
**only** from retrieval-side features, with two dev-fitted thresholds (refuse below `t_lo`, refuse above
`t_hi`, admit inside the band), hold its abstain precision across a ladder of four increasing negative
hardness rungs — and does its operating point transfer to items it was not fitted on?

- **H1 (hardness monotonicity).** Abstain precision on the held-out half is non-increasing across rungs
  1→4, and the drop from rung 1 to rung 3 is ≥ 15 points.
  *Refuted if* the rung-1 minus rung-3 paired difference has a 95% CI containing 0, or if the observed
  sequence is not non-increasing, or if the drop is < 15 points.
- **H2 (operating-point transfer).** The dev-fitted operating point, applied frozen to a
  disjoint-article held-out half *and* to a second corpus, loses ≥ 10 points of abstain precision at
  equal abstain recall relative to the dev figure.
  *Refuted if* the loss is within ±5 points (i.e. it transfers), or if the second corpus is unavailable
  (then H2 is reported as PARTIAL: within-corpus transfer only, and the second-corpus arm as NOT RUN).
- **H3 (two-sided beats one-sided).** The band gate beats the best single-threshold gate built on the
  same score, by ≥ 5 points of abstain precision at matched abstain recall on the held-out half.
  *Refuted if* the paired bootstrap 95% CI of the difference contains 0, or the gain is < 5 points.

## 2. Data (public only)

- **SQuAD 2.0 dev**, `dev-v2.0.json`, 35 articles / 1,204 paragraphs / 11,873 questions (5,928
  answerable, 5,945 impossible), licence CC BY-SA 4.0.
  URL `https://raw.githubusercontent.com/rajpurkar/SQuAD-explorer/master/dataset/dev-v2.0.json`
  sha256 `80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8`, retrieved 2026-11-03.
  **Only the `is_impossible: false` rows are used**; the impossible rows are not part of this study
  (they are a different kind of negative and are recorded here as out of scope).
- **Second corpus (H2 arm 2): 2WikiMultihopQA dev**, if and only if it can be fetched from a public
  mirror without authentication during the run window. Recorded as NOT RUN otherwise, with the reason.
- No private or scraped data. The student's private memory-system evaluation is **not** used and no
  figure from it appears anywhere; at most one disclosed anecdote sentence with no numbers (head
  condition 4).

## 3. Items — 4,000, paired by question

Split articles first (whole articles, never split): 17 articles = dev, 18 = test, chosen by
`SPLIT_SEED` from the 35 article titles sorted lexicographically. Sample 400 answerable questions from
dev articles and 400 from test articles (`DATA_SEED`, uniform without replacement within the article
set). Each sampled question generates **five** items that share the question:

| rung | label | presented passage |
|---|---|---|
| 0 | answerable | the question's gold paragraph (`P_gold`) |
| 1 | negative (random) | a uniformly sampled paragraph ≠ `P_gold` from the same split's paragraph pool |
| 2 | negative (same-entity) | a paragraph ≠ `P_gold` containing the question's **highest-IDF content token** (IDF over the split's paragraph pool; stopwords and `?`-marks excluded); sampled uniformly among such paragraphs |
| 3 | negative (near-miss) | the paragraph immediately before or after `P_gold` in the same article (side by `DATA_SEED`); if `P_gold` is at an article boundary the other side is used; if the article has one paragraph the item is dropped |
| 4 | negative (premise violation) | `P_gold` with the first gold answer span replaced by a **same-surface-type** value taken from another answer span in the same article (types: `year`, `number`, `date`, `name`, `other`); items with no same-type candidate are dropped |

Totals: 800 answerable + 800 per rung = 4,000 items (2,000 dev, 2,000 test). Dropped rung items are
counted and reported; the design is **not** topped up after the freeze (a rung with fewer than 700
usable items is reported as such, not re-sampled).

## 4. Features

Fitted on dev only; nothing is recomputed on test.

**Retrieval-side (the gate's allowed inputs):** `bm25_presented`, `bm25_rank_presented` (log1p),
`bm25_top1`, `bm25_top5_mean`, `bm25_margin` (top1−top2), `dense_presented` (bge-small-en-v1.5 cosine),
`dense_rank_presented` (log1p), `dense_top1`, `dense_margin`, `top1_agreement` (0/1), `ce_presented`
(cross-encoder/ms-marco-MiniLM-L-6-v2 score of the presented passage), `lex_overlap` (|q∩p| / |q|).

**Reader-side (baseline B4 and the ablation only, never inside the primary gate):**
`reader_mean_logprob` = mean token log-probability of the reader's greedy answer (≤ 16 tokens) to the
question *given the presented passage*.

Models, pinned: `BAAI/bge-small-en-v1.5` (33.4M), `cross-encoder/ms-marco-MiniLM-L-6-v2` (22.7M),
BM25 via `bm25s 0.3.16` (k1/b defaults, English stopwords), reader = `Qwen/Qwen2.5-0.5B-Instruct`
(reported as a *small* reader; a 1.5B+ reader is future work per §9).

## 5. Gates

Logistic regression (L2, `C=1.0`, `lbfgs`, `max_iter=1000`, `class_weight=None`) on the 12
retrieval-side features, standardised with dev mean/std, fitted on the dev half only. Score
`s = P(answerable | x)`.

- **Band (primary):** admit iff `t_lo ≤ s ≤ t_hi`; refuse otherwise.
- **Single (B3):** admit iff `s ≥ t`; refuse otherwise.
- Thresholds come from a grid over dev quantiles 1..99 (100 candidate values), chosen to maximise
  abstain recall on dev subject to abstain precision ≥ 0.80; ties broken by the higher threshold
  (single) or the wider band (band). Both are constrained to `[min(s_dev), max(s_dev)]`.
- **B1:** single threshold on `bm25_top1`. **B2:** single threshold on `dense_top1`, same rule.
- **B4:** single threshold on `reader_mean_logprob`, same rule. If the reader cannot be loaded, B4 is
  NOT RUN and says why; it is never replaced by a proxy.

**Placement diagnostic (a reported quantity, not a hypothesis):** for each fitted threshold, whether it
lies inside or outside the observed dev score range, and the admit-region mass on dev.

## 6. Metrics

Per rung on the held-out half, with negatives of that rung as the positives of "refused":
**abstain precision** = P(negative | refused) estimated on the rung's own items (mean of the refusal
indicator over that rung's negatives), **abstain recall** (same mean, named separately for clarity),
**over-refusal** = fraction of rung-0 items refused, and **coverage**. Secondary: AUROC of each gate
within each rung, coverage at 0.80 precision. No number is reported beyond the precision its interval
supports (2 decimals for rates, 3 for AUROC).

## 7. Statistics (fixed now)

- 10,000-resample **BCa** bootstrap, `BOOT_SEED=12345`, item-level resampling, paired by question for
  every comparison (the paired difference vector is `d_i = refused_i(A) − refused_i(B)`).
- Paired significance: **exact sign test** for binary paired indicators; Wilcoxon signed-rank only for
  continuous paired differences (`lex_overlap`, reader logprob). Two-sided, α = 0.05.
- **Holm** correction across the three primary hypothesis tests {H1, H2, H3}; per-rung descriptive
  intervals are *not* corrected and are labelled descriptive.
- Effect size: Cliff's delta for paired binary indicators, Cohen's d for continuous.
- Nothing is claimed from a difference whose interval contains 0.

## 8. Sample size, seeds, stopping rules

- Sizes fixed in §3 (400 questions per split × 5 items). Rationale: at 400 negatives per rung the
  binomial SE of a 0.80 precision is ≈ 2.0 points, so a 5-point H3 margin is ≈ 2.5 SE and a 15-point
  H1 drop is ≈ 5 SE — enough to detect the stated effects, not enough to chase 1-point differences.
- Seeds: `DATA_SEED=20261103`, `SPLIT_SEED=7`, `CV_SEED=13`, `BOOT_SEED=12345`. Reruns must reproduce
  every metric to 1e-9 (`--check-repro`).
- **Stopping / rebuild rules (hard):** (a) if the surface-only separability AUROC exceeds **0.75** on
  any rung, that rung is rebuilt by length-matched resampling (±10% of the rung-0 length deciles) and
  re-audited; at most **two** rebuilds per rung; (b) if more than **two** rungs still exceed 0.75 after
  their rebuilds, the run stops, the audit is reported as the finding, and the topic goes to the C3
  fallback (head condition 2 + SELECTED.md); (c) if a rung ends with < 700 items it is reported with its
  true n and the shortfall, not topped up.
- **What counts as failure:** every stated refutation in §1. A refuted hypothesis is reported as a
  refuted hypothesis; the paper is not rewritten to hide it. Wall-clock failure (no result by the end
  of the window) is reported as NOT DONE, never as a result.

## 9. Deviations from `03_topics/PROPOSAL.md` (declared before any run)

1. **Item arithmetic.** The proposal says "3,200 items: 800 answerable and 800 in each of four rungs",
   which is 4,000 by addition. We fix 4,000 (800 + 4×800) and say so; the 3,200 figure was an
   arithmetic slip.
2. **Pool size.** The proposal calls 11,873 "the SQuAD 2.0 dev paragraph pool". 11,873 is the number of
   *questions*; the dev pool is 1,204 paragraphs. Corrected here.
3. **Item-centring on the presented passage.** The proposal says features are "top-1 and mean top-5
   BM25 / dense". Read literally, the gate would score the corpus, not the passage it is being asked to
   answer from — so it could not distinguish a hard negative from a gold paragraph at all. We therefore
   make the presented passage first-class: its own score and rank, plus the corpus-level top-1, margin
   and agreement terms. The corpus-index-contamination variant (rungs as index composition) is listed
   as future work, not run.
4. **Reader.** The proposal's 1.5B reader is not run in this window (CPU-only laptop, shared, no GPU);
   B4 uses `Qwen2.5-0.5B-Instruct` and is labelled a *small* reader. Consequently the reader-side
   ablation is a lower bound on what a bigger reader's confidence signal would give, and the paper says
   so.
5. **Second corpus.** H2's second arm depends on a public 2WikiMultihopQA mirror being reachable; it is
   pre-declared as possibly NOT RUN rather than silently substituted by a different corpus.
6. **Length matching.** The proposal's "±10% per decile" is implemented as the *rebuild* procedure in
   §8(a), not as an up-front filter, because up-front matching would change the rung definitions
   themselves.

## 10. Deviation log (append only)

### D1 — 2026-11-03T05:27+05:30 — confirmatory thresholds are degenerate; exploratory constrained arm added

Observed before any number was written into a draft: with the pre-registered rule (maximise abstain
recall subject to dev abstain precision >= 0.80) the fitted band is t_lo=0.907, t_hi=0.948 and the fitted
single threshold t=0.939, which refuse 92.9% of dev items below t_lo alone — dev over-refusal is 0.755 on
the held-out half. Every gate then reports abstain precision 1.00 in every rung, so H1 and H3 cannot be
tested at that operating point: the thresholds sit in the saturated region where precision is bought with
coverage.

Consequences, fixed now and not later:

1. The confirmatory analysis stays exactly as pre-registered and its result is whatever it is. It is
   reported as REFUTED/UNSUPPORTED, not re-fitted.
2. A second, EXPLORATORY operating point is added: maximise dev abstain recall subject to dev abstain
   precision >= 0.80 AND dev over-refusal <= 0.10. It is labelled exploratory_* in every file and table,
   it is never described as confirmatory, and it cannot rescue a hypothesis — the pre-registered verdict
   stands on the pre-registered gate.
3. H2's second corpus was fetched after the freeze (2WikiMultihopQA dev, Apache-2.0, sha256 and every
   request logged in 04_experiments/data/TRANSFER-DATA.md; 400 transfer items built in
   transfer_items.jsonl). The second arm is run only if the remaining window allows it; otherwise it is
   reported NOT RUN with the data and the builder committed, and the paper's H2 verdict rests on the
   within-corpus arm alone. Its construct differs from the SQuAD rungs (2Wiki has no article grouping),
   so if it runs it is a direction test only.
4. H2 gets NO p-value. It compares two point estimates where one side is the fitting half, so a
   significance test would be theatre. Holm's family is therefore the two tests H1 and H3 (m = 2), not
   three, and this is the declared reason.
5. The reader baseline B4 covers 553 dev items only (CPU time cap). It is reported as a dev-only
   exploratory check with its own n, never as a held-out result.

None of these five changes alters an item, a feature, a model, a seed or the confirmatory gate.

### D2 — 2026-11-03T05:58+05:30 — exploratory rung 5 (overlap-matched negatives)

Requested by the head (HEAD-REVIEW Checkpoint 4, item 2) and declared **before** any of its numbers were
computed. Motivation: the §8 sensitivity audit shows that adding question–passage overlap to the six
surface features makes rungs 1–3 almost perfectly identifiable (0.9773 / 0.8886 / 0.9232 on dev). If the
rungs differ mainly in overlap, then a negative built to *match* the gold paragraph's overlap should be
indistinguishable from an answerable item by any overlap-driven signal, and a retrieval-only gate should
lose whatever separation overlap was buying.

Definition, fixed now:

- **Rung 5 (negative, overlap-matched).** For each sampled answerable question, compute
  `lex_overlap(p) = |tokens(q) ∩ tokens(p)| / |tokens(q)|` for the gold paragraph `P_gold`, then choose
  the candidate paragraph `p ≠ P_gold` from the same split's pool whose `lex_overlap` is closest to
  `lex_overlap(P_gold)` (absolute difference; ties broken by `random.Random("20261103:<qid>:5")`).
  The item records `overlap_target`, `overlap_chosen` and `overlap_absdiff`.
- Rung 5 is built for **both** splits (dev and test), reusing exactly the 400 sampled questions per split
  that rungs 0–4 use, so items are paired by question.
- The gate is **not refitted for rung 5**. The frozen model is re-fitted from the same dev rows (rungs
  0–4) and its coefficients are checked against `results_full.json` before use; the confirmatory and
  exploratory thresholds are read from that file, not recomputed.
- Rung 5 is analysed with (a) the surface audit's six features and (b) the same six plus overlap, so the
  audit can be compared rung-by-rung.
- Rung 5 is **exploratory**: it is not part of H1, it cannot rescue H1, and it is labelled `EXPLORATORY`
  in every file, table and sentence that reports it.

### D3 — 2026-11-03T05:58+05:30 — exploratory "top-1 presented" variant

Declared before its numbers. The first review round's top must-fix item (MF-1) is that answerable items
always present the gold paragraph while negatives do not, so the gate may be reading "is this the
retrieved document" rather than answerability. The pre-registered design cannot answer that. This variant
changes the *presentation*, not the hypothesis:

- For every sampled question in both splits, the presented passage is the **BM25 top-1 retrieved
  paragraph** for that question, taken from the item's own split pool. Label is 1 if that paragraph is
  the question's gold paragraph and 0 otherwise (i.e. the item is a retrieval hit or a retrieval miss).
- The twelve features are computed exactly as in §4, with the presented passage being that top-1
  document. Rung-5-style records carry `rung = -1` and `variant = "top1_presented"`.
- A gate fitted on this variant cannot be the frozen gate (different item population and label
  prevalence), so a fresh logistic gate is fitted on the dev half and evaluated on the test half. This is
  a **new measurement, exploratory by construction**, and is reported only as "what the same feature
  stack does when the presented passage is always the retrieved one".
- It changes no rung definition, no feature, no model, no seed, and no confirmatory result.

### D4 — 2026-11-03T07:05+05:30 — the dense block was degenerate; a spec-conformant re-implementation is added

Found while answering review round 1, by two readers of the code working separately, and recorded here
before any of its numbers were written into a draft.

`features.py` set the dense query to the presented passage itself (`Pq = dense.encode(present_text)`)
rather than to the question. Consequently `dense_presented` and `dense_top1` were both identically 1.0 and
`dense_rank_log` was constant on every row of rungs R0–R3 (78.70% of all rows; the remaining rows are the
rung-4 rewrites). The gate therefore had ten informative columns rather than twelve, and baseline B2 — a
threshold on `dense_top1` — was a threshold on a constant.

Consequences, fixed now and not later:

1. **The pre-registered analysis is not refitted and not replaced.** `results/c1/results_full.json` and
   everything downstream of it remain exactly as produced from the frozen code; the hash chain in
   `PREREGISTRATION.sha256` still covers the file above this paragraph.
2. **A spec-conformant implementation is added**: `features_corrected.py` computes the §4 feature as a
   question-to-passage cosine (question as query), for the main items, the R5 items and the transfer
   items. `eval_corrected.py` re-runs the *whole* analysis through the same code path
   (`run_c1.analyse` with the features file swapped) and writes to `results/c1_corrected/`. It asserts
   that the item ids, order and per-rung counts are unchanged, and every non-dense column is byte-identical
   to the frozen CSV.
3. **The corrected analysis refits the two thresholds** on corrected dev scores, because the score
   distribution changes. Thresholds are therefore not comparable between the two runs; AUROC is, because
   it is threshold-free. Table 4 of the paper reports both and says this.
4. **The corrected run is exploratory.** It is labelled `c1_corrected` and `D4` everywhere it appears. It
   cannot rescue a hypothesis and it does not change a pre-registered verdict; it changes what we believe
   the gate is measuring, which is stated in §4.6 and §5.2 of the paper.
5. This deviation is also the reason the paper reports leave-one-group-out ablations on the corrected
   features (`ablation_corrected.py`) rather than on the frozen ones: an ablation of a degenerate column
   would have been uninterpretable.
