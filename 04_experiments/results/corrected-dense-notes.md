# Corrected dense features — declared sensitivity analysis (not the pre-registered run)

Every number below is read from `04_experiments/data/features_corrected_meta.json`, `04_experiments/data/features*.csv`, `04_experiments/results/c1/*.json` or `04_experiments/results/c1_corrected/*.json` by `04_experiments/src/eval_corrected.py`, which wrote this file. Nothing in `results/c1/` and no pre-existing `src/` file was modified.

## 1. The defect

`04_experiments/src/features.py:102` sets the dense *query* to the presented passage:

```python
Pq = dense.encode(present_text, batch_size=64, normalize_embeddings=True, ...)
```

and then scores `P @ Pq[k]`, i.e. the presented passage against itself. PREREGISTRATION.md §4 defines `dense_presented` as a `bge-small-en-v1.5 cosine` (a question–passage quantity), so the frozen implementation computes a different feature from the one it is named after. Measured consequences in the frozen CSV:

| rung | frozen `dense_presented` (min / median / max) | distinct `dense_rank_log` values |
|---|---|---|
| 0 | 1.0000 / 1.0000 / 1.0000 | 1 |
| 1 | 1.0000 / 1.0000 / 1.0000 | 1 |
| 2 | 1.0000 / 1.0000 / 1.0000 | 1 |
| 3 | 1.0000 / 1.0000 / 1.0000 | 1 |
| 4 | 0.8979 / 0.9926 / 0.9999 | 1 |

Rungs 0–3 are exactly 1.0 by construction (the passage is compared with itself); `dense_rank_log` is `log1p(1)` on every row. Rung 4 is the exception and the leak: a rewrite is not a pool document, so `features.py` falls back to `cos[doc_id]` of the *source gold* paragraph, i.e. cos(rewrite, gold) — median 0.9926 there. That column therefore separates `presented == gold` (rungs 0–3) from `presented == rewrite` (rung 4) for free, and its frozen gate coefficient was 5.9181 — identical to `dense_top1`'s 5.9181, the collinearity signature of a constant feature that is non-constant only on rung 4.

## 2. What the corrected module does

`04_experiments/src/features_corrected.py` changes the dense block and nothing else:

* `dense_presented` = cosine(emb(question), emb(presented passage));
* `dense_rank_log` = log1p(1-based rank of the presented passage among all pool documents, ranked by cosine **to the question**);
* `dense_top1` / `dense_margin` = max / max−second-max of the question's cosines over the pool;
* `top1_agreement` = 1 iff the BM25 rank-1 document id equals the dense rank-1 document id.

Rung-4 rows (a rewrite, not a pool document): `dense_presented` = cosine(question, rewrite) — the quantity §4 names — while rank/top1/margin are taken from its source gold document, exactly as `features.py` inherits the source id for BM25 (see the comment in `score_group`). `bm25_is_source_doc` stays 1 on those rows.

Unchanged: the split pools (imported from `features.split_pools()`), BM25 score/rank/top1/top5/margin, the cross-encoder score, `lex_overlap`, the CSV header and the `%.10g` formatting. Verified cell-by-cell against the frozen CSVs: every non-dense column is byte-identical (0 differing cells across 3,752 / 800 / 400 rows).

| file | rows | pools | sha256 |
|---|---|---|---|
| `04_experiments/data/features_corrected.csv` | 3752 | {'dev': 608, 'test': 596} | `1d7f1b3aa1623416…` |
| `04_experiments/data/features_corrected_rung5.csv` | 800 | {'dev': 608, 'test': 596} | `1c5ff749385fe902…` |
| `04_experiments/data/features_corrected_transfer.csv` | 400 | {'transfer': 1459} | `8bde677cbf860e22…` |

After the change `dense_presented` takes 3731 distinct values on the main items (0 rows at 1.0) and `dense_rank_log` takes 527.

## 3. Integrity checks (all pass; the script aborts otherwise)

* Item ids and order identical to the frozen run: 3752 rows, n_dev = 1873, n_test = 1879, per-rung counts identical, `predictions.csv` item order identical.
* Surface audit byte-identical (it reads only item text): dev primary-6 AUROC r1=0.5063 / r2=0.5392 / r3=0.4881 / r4=0.4151 — same as frozen.
* The main analysis is `run_c1.analyse` itself (only `gate.load_features` and `gate.RESULTS` re-pointed), so every metric comes from the frozen code path.
* Rung-5 and transfer refits reproduce `c1_corrected/results_full.json['gate']` (max |Δcoef| = 3.9e-05, tolerance 1e-3).
* Independent spot recomputation of two rows (one rung 0, one rung 4) outside this script reproduced `dense_presented` and `dense_rank_log` to 6 decimal places.
* Max |Δcoef| between the frozen and corrected gates: 7.422 (largest on `dense_top1`, 7.422).

## 4. What changes (see `SUMMARY.md` for the full table)

* Threshold-free discrimination falls: dev AUROC 0.9879 → 0.887, test AUROC 0.9824 → 0.8738. Almost all of the loss is rung 4: AUROC(answerable vs rung 4) 0.9681 → 0.573, while rungs 1–3 barely move (0.9995 → 0.9992, 0.9764 → 0.9694, 0.9836 → 0.9817).
* Rung 4 is no longer refused: exploratory-band precision 0.8471 → 0.1253 (coverage 0.2544 → 0.396), confirmatory-band precision 1.0 → 0.9073. A rewritten gold passage is, to retrieval-side features built on the question, simply its own answerable original.
* The confirmatory operating point stays degenerate and gets worse: over-refusal 0.755 → 0.915, coverage 0.0527 → 0.0383, pooled precision 0.9993 → 0.9743.
* H3 stops being exactly zero: band − matched-single 0.0 (CI [0.0, 0.0]) → -0.0223 (CI [-0.0311, -0.0135]). Verdict unchanged (unsupported: the criterion is +0.05 in favour of the band and the sign is now negative).
* B2 (`dense_top1`) becomes a real score: pooled precision 0.7458 → 0.9973, but at coverage 0.2773 → 0.0027 and over-refusal 0.6375 → 0.9975 — precision bought with coverage, the D1 pattern.
* Rung 5 (EXPLORATORY) exploratory-band precision 0.8925 → 0.9375, AUROC(r0 vs r5) 0.9736 → 0.9728.
* Transfer: rung-3 precision 0.985 → 1.0 (confirmatory) and 0.855 → 0.975 (exploratory); AUROC(answerable vs rung 3) 0.6402 → 0.7059.

## 5. What this does and does not license

* It does **not** change a pre-registered verdict: H1 and H3 are unsupported and H2 refuted in both runs (see `SUMMARY.md`). The frozen run stands as the pre-registered result.
* It **does** change how rung 4 may be described. Any statement that the gate detects rewritten gold passages is, on §4-conformant features, not supported: the detector was reading a passage-against-passage rewrite-fidelity cosine that §4 never specified and that no deployed gate could compute (it needs the gold paragraph).
* The rung-5 and transfer arms here use the **corrected** gate and thresholds, so their numbers are not comparable cell-for-cell with `results/c1/rung5.json` / `transfer.json`; the reply string for H2's second corpus inside `results_full.json` still says NOT RUN because `run_c1.py` hard-codes it and was not modified — the transfer arm lives in `transfer.json`, as in the frozen run.
* `dense_top1` / `dense_margin` depend only on the question, so they cannot separate two items that share a question; the within-question separation in this design comes from BM25, the cross-encoder, `dense_presented` and `dense_rank_log`.

## 6. Provenance

```
python 04_experiments/src/features_corrected.py --dataset all     # 3 CSVs + meta
python 04_experiments/src/eval_corrected.py                       # main + rung5 + transfer + summary
```

Timings (CPU, `sentence-transformers`): model load 3.57 s, main index 21.95 + 21.13 s, main cross-encoder 34.74 + 35.2 s, total 157.75 s (all three files).

