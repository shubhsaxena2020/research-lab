# Rung 5 run notes — EXPLORATORY (D2), overlap-matched negatives

Everything here is exploratory per `PREREGISTRATION.md` §10 D2. Rung 5 is not part of H1, cannot
rescue H1, and no sentence reporting it may call it confirmatory.

## Commands (run from `C:\Users\shubh\research-lab`)

```
python 04_experiments/src/build_items_rung5.py --json      # items_rung5.jsonl
python 04_experiments/src/features_rung5.py                # features_rung5.csv + _meta.json
python 04_experiments/src/eval_rung5.py                    # results/c1/rung5.json
```

Runtimes on this laptop (CPU, shared): build 13.4 s; features 4 m 16.9 s wall (model load 3.47 s,
dev index 75.54 s, dev dense-encode 43.93 s, dev cross-encoder 24.61 s, test index 47.37 s, test
dense-encode 33.31 s, test cross-encoder 16.84 s); eval 3.89 s (gate refit 2.70 s, audit 0.87 s).

## Files written (sha256 of the two data files as written)

| file | n | sha256 |
|---|---|---|
| `data/items_rung5.jsonl` | 800 rows (400 dev + 400 test) | `48d5bc9edee13701084e94c417d279b1c197d396214e7d512e547014f0c073c1` |
| `data/features_rung5.csv` | 800 rows + header, header identical to `features.csv` | `5dab233176e8e2e745095859e877e0e93d1a0a866a6514ec93eeeb787caa2a33` |

The builder is deterministic: rerunning it produced the same sha256. Rerunning `eval_rung5.py`
reproduced every reported figure exactly (0.8925, CI [0.8575, 0.9175], AUROC 0.9736, dev audit
0.7208). Item keys are exactly the
`items.jsonl` key set plus `overlap_target`, `overlap_chosen`, `overlap_absdiff`; every chosen
passage is a real pool document (`bm25_is_source_doc` = 0 on all 800 rows), never the gold paragraph,
and always from the item's own split pool (608 dev / 596 test paragraphs).

## Did the matching work?

Yes, with a systematic one-directional residue:

| split | mean overlap(gold) | mean overlap(chosen) | mean absdiff | median absdiff | max absdiff | rung-1 random contrast |
|---|---|---|---|---|---|---|
| dev | 0.6676 | 0.5538 | 0.1138 | 0.0909 | 0.60 | 0.4328 |
| test | 0.6644 | 0.5628 | 0.1029 | 0.0909 | 0.50 | 0.4208 |

Median absdiff is 0.0909 on both splits — about one token, since the median question has 10 distinct
tokens on dev and 9 on test — and
the rung-1 random negative sits 0.42–0.43 away, so the search does what D2 asked. Two honest caveats:

1. **The residual is one-sided.** `lex_overlap` is discrete (`k/|q|`) and the pool has far more
   low-overlap paragraphs than high-overlap ones, so the closest available candidate is usually
   *below* the gold overlap: mean chosen 0.554–0.563 against mean target 0.665–0.668. Rung 5 is
   "as close as the pool allows", not "matched". 41.5% (dev) / 45.8% (test) of items are exact
   matches; the rest carry a real gap.
2. **Ties are common** — 285/400 dev and 282/400 test items had more than one candidate at the
   minimum distance and were resolved by `random.Random("20261103:<qid>:5")`, as D2 specifies.

## Frozen gate

`eval_rung5.py` refits `gate.fit_logistic_gate` on the 1,873 dev ids of rungs 0–4 and asserts every
coefficient and the intercept against `results_full.json['gate']` within 1e-3. **Passed**, max
absdiff 0.0 (intercept −6.2862). Thresholds read, never refit: confirmatory band
`[0.907221, 0.947839]`; exploratory band `[0.297426, 0.947839]`.

## Numbers (test split, n = 400 rung-5 items)

| operating point | rung 5 abstain precision | BCa 95% CI | rungs 1–4 reference |
|---|---|---|---|
| confirmatory band | 1.0000 | [1.0000, 1.0000] (percentile fallback) | 1.0000 / 0.9964 / 1.0000 / 1.0000 |
| exploratory band | 0.8925 | [0.8575, 0.9175] | 0.9975 / 0.9107 / 0.9275 / 0.8471 |

AUROC(answerable test rung 0 vs rung 5) = **0.9736**; reference 0.9995 / 0.9764 / 0.9836 / 0.9681 for
rungs 1–4. Dev rung 5, same frozen gate: 1.0000 confirmatory, 0.9325 [0.9025, 0.9525] exploratory.

Surface separability audit (5-fold CV, seed 13, `audit.surface_features` + `audit._cv_auroc`):

| rung | dev primary-6 | dev +lex/q_len | test primary-6 |
|---|---|---|---|
| 5 | 0.7208 | 0.7936 | 0.6651 |
| 1 | 0.5063 | 0.9773 | 0.5199 |
| 2 | 0.5392 | 0.8886 | 0.5867 |
| 3 | 0.4881 | 0.9232 | 0.4895 |
| 4 | 0.4151 | 0.4082 | 0.4259 |

## Surprises (reported, not smoothed)

- **Rung 5 is not the hardest rung.** At the exploratory operating point it scores 0.8925, i.e.
  *above* rung 4 (0.8471) and just under rung 2 (0.9107); its AUROC 0.9736 sits between rung 4
  (0.9681) and rung 2 (0.9764). Matching overlap did not defeat the gate — the remaining ~0.10
  overlap gap plus the dense/cross-encoder signal is enough to keep separation at ~0.97.
- **Rung 5 has the largest surface signature of any rung** (dev 0.7208, test 0.6651 vs 0.42–0.59 for
  rungs 1–4), driven by length: median 995.5 chars (dev) / 902.0 (test) against 723 / 711 for the
  answerable items. Long paragraphs are exactly the ones with enough distinct tokens to match a high
  gold overlap, so overlap-matching selects long passages. It still passes the §8a gate (≤ 0.75) on
  both splits, but the dev margin is only 0.029 — this is the closest any rung has come to the
  stopping rule, and it should be said in the paper rather than left in the file.
- **Overlap-driven identifiability fell but did not vanish**: with `lex_jaccard` + `q_len` added,
  rungs 1–3 are 0.98/0.89/0.92 on dev, while rung 5 is 0.7936 dev / 0.7537 test. So D2's premise
  ("if the rungs differ mainly in overlap…") holds only partly: about half the excess separability
  goes away, the rest survives as the one-token residual and the length shift.
- **The confirmatory band is degenerate again on rung 5** (all 400 refused, CI [1,1], reported with
  the harness's documented percentile fallback because BCa is undefined at zero variance). Mean
  rung-5 gate score is 0.1016, an order of magnitude below `t_lo` = 0.9072. Nothing about H1/H3
  changes; this is the same D1 pathology, now with a fifth rung.
- No item was dropped: 800/800 questions produced a rung-5 candidate, so the rung has the full
  400 negatives per split and needs no shortfall note.
