# Top-1-presented run notes — EXPLORATORY (D3), answers review item MF-1

Everything here is exploratory per `PREREGISTRATION.md` §10 D3, declared before any of its numbers
were computed. This variant is not part of H1/H2/H3, cannot rescue any of them, and nothing in
`05_paper/**` was touched. Every number below is read from `results/c1/top1_variant.json`,
`data/features_top1_meta.json` or the two data files.

**What the variant does.** The ladder's answerable items always present the gold paragraph and its
negatives never do, so the gate could be reading "is this the retrieved document" instead of
answerability (the first review round's top must-fix item, MF-1). This variant changes only the
*presentation*: for each of the 400 sampled questions per split, the presented passage is the BM25
rank-1 paragraph from that split's own pool, and the label is 1 iff that paragraph **is** the gold
paragraph. The population is therefore retrieval hits and retrieval misses; `rung = -1`,
`variant = "top1_presented"`.

## Commands (run from `C:\Users\shubh\research-lab`)

```
python 04_experiments/src/build_items_top1.py     # data/items_top1.jsonl
python 04_experiments/src/features_top1.py        # data/features_top1.csv + features_top1_meta.json
python 04_experiments/src/eval_top1.py            # results/c1/top1_variant.json
```

Runtimes on this laptop (CPU, shared, `ops/HEAVY.lock` held during the two model passes and removed
after): build 3.9 s (BM25 index 0.15 s dev / 0.08 s test); features 96 s (model load 3.4 s, dev pool
encode + index 25.0 s, test 23.8 s, question encode 1.4 / 1.7 s, cross-encoder 9.2 / 8.8 s); eval
~4 s.

## Files written

| file | n | sha256 |
|---|---|---|
| `data/items_top1.jsonl` | 800 rows (400 dev + 400 test) | `a586606d6ec23b10f86c9104e343e77ccc2fc03130feb0bc5cb014a39f42ed55` |
| `data/features_top1.csv` | 800 rows + header, header = `item_id,split,rung,label` + the 12 `gate.GATE_FEATURES` | `3d22e100c1991ed63b3155ef6f0f66a873377d410ce0b9d629346ed4185e4a5c` |
| `results/c1/top1_variant.json` | every number cited here | `299c3e0569b4cef98342ac57930ce2b12398f00a7810a5b4bb80df7af7b65117` |

Determinism: rebuilding the items reproduced the same sha256; rerunning `features_top1.py` reproduced
the CSV **byte-identically** (same sha256); rerunning `eval_top1.py` reproduced
`top1_variant.json` byte-identically. No RNG is used anywhere in this variant except the bootstrap
(`BOOT_SEED = 12345`).

Item rows carry `item_id, split, qid, title, question, context, rung, variant, label, gold_answer,
n_context_chars, is_gold`. `eval_top1.py` re-verifies them against `data/raw/dev-v2.0.json` and
`data/items.jsonl` before computing anything (13 checks, all pass: 800 rows, 400/split, every
`label == (context == gold paragraph)`, qid sets identical to the rung-0 qid sets, no NaN in the
feature matrix, `bm25_rank_log` constant, `dense_presented` varying).

## Hit rate (the number the paper will cite)

| split | pool | n | hits | misses | hit rate | gold rank ≤5 | ≤10 | mean gold rank |
|---|---|---|---|---|---|---|---|---|
| dev | 608 | 400 | 342 | 58 | **0.8550** | 383 | 389 | 4.83 |
| test | 596 | 400 | 313 | 87 | **0.7825** | 381 | 388 | 3.11 |

So the label prevalence is 0.855 on dev and 0.783 on test, against 0.213 answerable prevalence in the
ladder's own 5-item blocks. The dev pool is the easier one: the same 400-question design lands 7.3
points higher there, which is why every dev-fitted operating point loses something on test.

## Features

The twelve columns are `gate.GATE_FEATURES` in the same order, same models (`BAAI/bge-small-en-v1.5`,
`cross-encoder/ms-marco-MiniLM-L-6-v2`), same arithmetic as `features.py`.

- **`bm25_rank_log` is constant at 0.6931 by construction** (log1p(1) = ln 2, *not* 0 — the task
  description's "log1p(1)=0" is an arithmetic slip). The column is kept so the vector is literally the
  same twelve features; a constant column contributes nothing to the fitted score. This is precisely
  the situation the paper's no-rank ablation was built to probe, and here it is forced rather than
  chosen.
- `dense_rank_log` still varies (the dense rank of the same BM25-top-1 document, 1…608), so the dense
  block is not entirely inert.
- Consistency check against the frozen run: for the 655 retrieval hits the presented passage *is* the
  gold paragraph, so BM25 score, cross-encoder score and lexical overlap must equal the `r0` row of
  `features.csv`. They do — max abs diff 5e-9 (BM25, float32), 3.8e-6 (cross-encoder, different batch
  composition), 0.0 (overlap).

### ⚠ The frozen dense block is degenerate — found while checking the above

`features.py` line 100–102 encodes `present_text` (the presented passage) as the dense *query*
(`Pq = dense.encode(present_text)`), not the question. The consequence in `features.csv`:

| rung | n | mean `dense_presented` | sd | `dense_rank_log` |
|---|---|---|---|---|
| 0 | 800 | 1.000000 | ~0 | 0.6931 (all rows) |
| 1 | 800 | 1.000000 | ~0 | 0.6931 |
| 2 | 553 | 1.000000 | ~0 | 0.6931 |
| 3 | 800 | 1.000000 | ~0 | 0.6931 |
| 4 | 799 | 0.9878 | 0.009 | 0.6931 |

i.e. `dense_presented` = cos(passage, passage) = 1, `dense_top1` = 1, `dense_rank_log` = log1p(1) for
every corpus-document row; the rung-4 rewrites are the only rows that differ, and only because they are
not pool documents. The fitted gate's coefficients show it: `dense_presented` and `dense_top1` get
the *identical* coefficient 5.9181 to four decimals (they are the same column twice), on sds of 0.0093
and 0.0093; `dense_rank_log`'s sd is 0.0, so standardisation replaces it with 1 and the column is a
constant. Of the twelve pre-registered features, three carry no question–passage dense signal at all;
the dense block reduces to `dense_margin` (a passage-distinctiveness term). Baseline B2 (`dense_top1`)
is likewise a constant score.

This is a bug in files this variant does not own (`features.py`, and the same line is in
`features_rung5.py` / `features_transfer.py`), so it is **not fixed here** and no frozen result is
altered. It needs a head decision, because re-running `features.py` with the question as the query
would change every dense-dependent number in `results_full.json` (gate coefficients, AUROCs, B2, the
no-rank ablation, rung 5, transfer). For this variant I compute the dense features the way
PREREGISTRATION §4 describes (question as query, cosine to the presented passage) and record the
frozen column's degeneracy in `features_top1_meta.json → frozen_dense_columns_are_degenerate`. Using
the literal frozen math here would have made `dense_presented` a constant 1.0 and the
reverse-direction check below exactly 0.5 by construction — a fact about an encoding bug, not about
retrieval.

## Gate and operating points (fitted on dev only, 400 items, 342 hits / 58 misses)

Logistic regression, same §5 estimator (L2, C=1.0, lbfgs, max_iter=1000, standardised with dev
mean/std) on the twelve features. New fit because the population and prevalence differ (D3).

- dev AUROC 0.9696, **test AUROC 0.9453** (P(score_hit > score_miss), n = 313 hits vs 87 misses).
- `gate.fit_band_thresholds` (target dev abstain precision 0.80): **t_lo = 0.532266, t_hi = 0.999990**
  — dev refusal rate on misses 0.7414, dev P(miss | refused) 0.8269, dev over-refusal 0.0263, dev
  coverage 0.8700.
- `gate.fit_band_constrained` (dev over-refusal cap 0.10): **the same band**. The precision-only rule
  already refuses only 2.6% of dev hits, so the extra constraint is not binding here. The two
  operating points coincide, which is worth saying out loud rather than presenting two identical rows
  as two results.

Test-split evaluation (n = 400: 313 hits, 87 misses):

| operating point | refused (all) | misses refused | hits refused | P(miss \| refused) | coverage |
|---|---|---|---|---|---|
| band, target precision 0.80 | 63 | 55/87 = **0.6322** [0.5172, 0.7241] | 8/313 = **0.0256** [0.0096, 0.0447] | **0.8730** [0.7681, 0.9394] | 0.8425 |
| band, over-refusal cap 0.10 | 63 | 0.6322 [0.5172, 0.7241] | 0.0256 [0.0096, 0.0447] | 0.8730 [0.7681, 0.9394] | 0.8425 |

All intervals are BCa, 10 000 resamples, `BOOT_SEED = 12345`, item-level. For reference, refusing
everything would give P(miss | refused) = 0.2175; the gate's 0.8730 is the same quantity conditional on
refusal.

Two different quantities both get called "abstain precision" and they are not interchangeable here:

- `refusal_rate_misses` = P(refused | miss) — the fraction of retrieval misses refused. This is the
  definition the task asked for and the one PREREGISTRATION §6's parenthetical encodes ("mean of the
  refusal indicator over that rung's negatives"), and it is what `gate.metrics_block` computes.
- `precision_miss_given_refused` = P(miss | refused) — what a user of the gate actually experiences.
  This is what the words "abstain precision" usually mean.

Both are in the JSON under those names; the paper should pick one and label it, because at the
confirmatory operating point the two differ by 0.17 (see the flag at the end).

## Hit vs miss refusal — the number that matters

At the dev-fitted band on test: **the gate refuses 63.2% of retrieval misses and 2.6% of retrieval
hits**, a ratio of ~25×, paired stratified bootstrap difference (hits − misses) = **−0.6066**
[−0.7082, −0.5019], 10 000 resamples, seed 12345.

So on this population the gate behaves as a *retrieval-correctness detector*: it is far more likely to
refuse the passage BM25 got wrong than the passage BM25 got right. It is not a good one — 37% of
retrieval misses are still admitted at 0.84 coverage, and 8 hits are refused — but the direction and
the size of the asymmetry are unambiguous.

## Reverse direction: does the 12-feature stack beat one cosine?

Test AUROC of each feature alone on the same 400 items (no fitting):

| feature | test AUROC | dev AUROC |
|---|---|---|
| `bm25_margin` | 0.8961 | 0.8983 |
| `ce_presented` | 0.8448 | 0.8928 |
| `bm25_presented` (= `bm25_top1`) | 0.7884 | 0.8133 |
| `top1_agreement` | 0.7863 | 0.8502 |
| `lex_overlap` | 0.6913 | 0.7329 |
| **`dense_presented` (raw bge cosine)** | **0.6760** | 0.7901 |
| `dense_margin` | 0.6592 | 0.7163 |
| `bm25_top5_mean` | 0.5950 | 0.6255 |
| `dense_top1` | 0.5055 | 0.5961 |
| `dense_rank_log` | 0.1809 | 0.1003 |
| `bm25_rank_log` | 0.5000 (constant) | 0.5000 |

The stack (0.9453) adds 4.9 points of AUROC over the best single feature (`bm25_margin`, 0.8961) and
26.9 points over one cosine (0.6760). That is a real gain, but read what it is built from: BM25 margin, cross-encoder relevance and
BM25/dense top-1 agreement — all retrieval-quality signals. None of them is evidence about whether the
passage *answers* the question.

## Does this support or undercut "the gate reads retrieval correctness, not answerability"?

**It supports the first half and cannot test the second.** In this variant the label *is* retrieval
correctness, so a high AUROC is expected of any retrieval-quality feature and cannot be evidence
*against* the objection; what the variant adds is that the same stack reaches 0.945 on hit-vs-miss and
refuses misses 25× more often than hits, i.e. the signal the original design leaned on is present and
strong. It provides no evidence that the gate detects answerability independently of retrieval, because
every item here is either "gold paragraph retrieved" (answerable) or "gold paragraph not retrieved"
(unanswerable from what is shown) — the two readings coincide item-for-item. Net: confirming for the
paper's limitation, not exculpatory. It does not rescue the ladder from MF-1; the honest sentence for
§6 limitation 2 is that the confound was tested and the feature stack demonstrably tracks retrieval
correctness.

## Caveats a reviewer will raise

1. **n is small on the miss side** (58 dev, 87 test). The refusal-rate interval on misses is ±10
   points; the AUROC interval is not reported and would be wide. Do not quote 0.9453 to three decimals
   without saying n = 87.
2. **Dev is an easier pool than test** (hit rate 0.855 vs 0.783). The dev-fitted band's miss-refusal
   rate drops from 0.7414 (dev) to 0.6322 (test) while its conditional precision *rises* from 0.8269 to
   0.8730 — because test has proportionally more misses to find. Neither number is a transfer result;
   they are two different populations.
3. **The band is effectively one-sided.** `t_hi = 0.99999` refuses 4 dev items and nothing meaningful
   on test; the "band" here is a low threshold at 0.532. Calling it a two-sided band would be
   misleading.
4. **`t_hi` sits at the top of the dev score range**, so the upper arm is unconstrained in practice.
5. **The label is text equality**, so a duplicate paragraph elsewhere in the pool counts as a hit only
   if it is the gold text; 301 dev / 275 test distinct top-1 documents for 400 questions means many
   questions share a top-1 paragraph, which is expected (one paragraph per article, several questions
   per paragraph).
6. **Nothing here is confirmatory** and no hypothesis is claimed. It is one exploratory measurement on
   800 items.

## Two flags for the head (outside this variant's ownership; not fixed)

1. **Dense block degenerate** (above): `features.py` encodes the presented passage as the dense query,
   so `dense_presented`, `dense_top1` and `dense_rank_log` are constant in `features.csv`. This affects
   every dense-dependent number in `results_full.json` (gate coefficients, AUROCs, B2, the no-rank
   ablation, rung 5, transfer). Fixing it means re-running features and everything downstream; that is
   a head decision, not a subagent edit.
2. **"Abstain precision" is reported as recall.** `gate.metrics_block` sets
   `pooled_abstain_precision = ref[is_neg].mean()`, i.e. P(refused | negative). PREREGISTRATION §6's
   parenthetical defines it that way, so the code follows the protocol — but the *name* is the other
   conditional. Computed from `results/c1/predictions.csv` (derived here, not a pipeline number):
   confirmatory band reports 0.9993 where P(miss | refused) is 0.8303; exploratory band reports 0.9216
   where P(miss | refused) is 0.9729. The paper should rename or report both before a reviewer does it
   for them.
