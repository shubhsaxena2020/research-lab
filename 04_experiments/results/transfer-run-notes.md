# Transfer arm (H2, second corpus: 2WikiMultihopQA dev) — run notes

Run date: 2026-11-03 (IST). CPU only, `python` 3.11.15. No randomness in this arm: the item builder's
seed (20261103) was fixed earlier, feature extraction is deterministic, and both thresholds are *read*
from `results/c1/results_full.json`, never refitted.

## 1. What was run

```
python 04_experiments/src/features_transfer.py      # -> data/features_transfer.csv + features_transfer_meta.json
python 04_experiments/src/eval_transfer.py          # -> results/c1/transfer.json
```

`features_transfer.csv` sha256 `f7c70b07edae77a3126a39d04addb1753e85717ab83c43b9c2d706141dbe8582`
`transfer.json` sha256 `690278824756a208309e10a65f7cf231fb26b67cf5ab0a104d1069c985d3d614`

## 2. Feature extraction (identical maths to `features.py`)

* Pinned models, same as the main run: `BAAI/bge-small-en-v1.5`, `cross-encoder/ms-marco-MiniLM-L-6-v2`,
  `bm25s` with `stopwords="en"` (k1=1.5, b=0.75, lucene — read off the object into the meta file).
* **Pool** (the analogue of the split pool): union of every `[title, [sentences]]` paragraph in the
  `context` of the 200 source questions, deduplicated by exact text — 2,000 paragraphs before
  deduplication, **1,459 pool documents** after (541 duplicate texts dropped). Recorded in
  `features_transfer_meta.json` under `pool`.
* 400 rows (200 rung 0, 200 rung 3), 12 gate features + `bm25_is_source_doc`; header is byte-identical
  to `data/features.csv`. Every presented passage *is* a pool document (0 misses asserted, so
  `bm25_is_source_doc = 0` everywhere and no rung-4-style source-doc inheritance applies).
* Presented passage lengths: median 352 chars (rung 0), 287 (rung 3), 311.5 overall.
* Timings: model load 4.1 s, index+encode 118.6 s, presented encode 32.5 s, cross-encoder 14.0 s.

## 3. Gate check before any transfer number

Re-fitted the logistic gate on exactly the main run's dev ids (`items.jsonl` order, `split=="dev"`,
n = 1,873). Coefficients vs `results_full.json ['gate']`: **max |Δ| = 4.29e-05** (intercept 2.1e-06),
tolerance 1e-3 → **PASS**. `eval_transfer.py` exits non-zero and writes nothing if this fails.

Thresholds used, read not recomputed:

| operating point | t_lo | t_hi | source |
|---|---|---|---|
| confirmatory band | 0.907221 | 0.947839 | `results_full.json ['thresholds']['band']` |
| exploratory band (D1.2) | 0.297426 | 0.947839 | `results_full.json ['exploratory']['operating_point']['band']` |

## 4. Results — 400 transfer items (200 answerable / 200 rung 3)

| operating point | transfer rung-3 abstain precision | BCa 95% CI | n | transfer rung-0 over-refusal | coverage | refused | AUROC(answerable vs rung 3) |
|---|---|---|---|---|---|---|---|
| confirmatory band | 0.9850 | [0.950, 0.995] | 200 | 0.8950 | 0.0600 | 376/400 | 0.6402 |
| exploratory band | 0.8550 | [0.795, 0.895] | 200 | 0.5750 | 0.2850 | 286/400 | 0.6402 |

Main-run held-out reference and the drop (same gate, same thresholds; drop = test rung 3 minus
transfer rung 3):

| operating point | test rung-1 prec. | test rung-3 prec. | transfer rung-3 prec. | drop |
|---|---|---|---|---|
| confirmatory band | 1.0000 | 1.0000 | 0.9850 | 1.50 pp |
| exploratory band | 0.9975 | 0.9275 | 0.8550 | 7.25 pp |

Score distribution on transfer: median 0.084 (rung 0: 0.178, rung 3: 0.058), max 0.951.
93.8% of transfer items fall below the confirmatory `t_lo`, 71.3% below the exploratory `t_lo`.

### The confirmatory number is degenerate — say so

0.985 rung-3 precision at the confirmatory band is bought almost entirely with refusals: **89.5% of
answerable (rung-0) items are refused**, coverage is 6.0%, and only 3 of 200 rung-3 items are admitted.
At that operating point the gate is close to "refuse everything", so the 1.50 pp "drop" is not
evidence that the operating point transfers; it is the same saturation that PREREGISTRATION §10 D1
recorded on the main run (dev over-refusal 0.755), reproduced on a second corpus. The informative
number in this arm is the discrimination collapse: **AUROC(answerable vs rung 3) = 0.640 on 2Wiki
against 0.9836 on the SQuAD test half** — the frozen feature stack barely separates answerable from
near-miss items once the corpus changes. Abstain precision stays high only because the gate refuses
the answerable items too.

### Observation: the dense half of the gate is degenerate by construction

Measured from the written CSVs (not inferred): in `data/features.csv`, `dense_presented == dense_top1`
for **all 3,752 rows**, `dense_rank_log` takes **one** distinct value, and `dense_presented` is exactly
1.0 for **every** row of rungs 0–3 and for none of rung 4. The cause is in `features.py`: the dense "query" is
the encoding of the presented passage itself (`Pq = dense.encode(present_text)`, then `P @ Pq[k]`), so
the passage is scored against itself. The dense terms therefore carry no question-conditioned retrieval
signal — in the main run they separate only rung 4 (the rewrite), and in this transfer arm they are
constant (`frac_dense_presented_eq_1 = 1.0`, one distinct `dense_rank_log` over 400 rows), contributing
nothing. **The 0.640 transfer AUROC is therefore a BM25 + cross-encoder + lex_overlap result, not a
retrieval-stack result.** This arm reuses `features.py`'s maths exactly as instructed and does not
modify it (out of scope); the observation is recorded in `transfer.json
['feature_observation_dense_degenerate']` so the owner of `features.py` can decide what to do. It does
not change any main-run number: the gate was fitted on those same features.

### Direction, not magnitude

This is a **direction test only**. Three construct differences forbid reading the drop as an estimate
of the same quantity: (1) 2Wiki has no article grouping — `context` is a set of independent Wikipedia
articles, so rung 3 is another paragraph from the same question's article set, not a same-document
neighbour; (2) shorter passages — corpus median paragraph 203 chars vs 711.5 for SQuAD 2.0 dev
(measured over 125,760 and 1,204 paragraphs respectively), presented transfer median 311.5 chars;
(3) multi-hop question types (compositional / comparison / bridge-comparison / inference) versus
single-paragraph extractive SQuAD questions. The retrieval pool is also different in kind (1,459
documents from 200 questions' article sets, not a split-wide pool). The same text is stored in
`transfer.json ['construct_note']`.

## 5. Citation resolution (the draft's reference was wrong)

The register row `S3-2wiki` in `02_literature/citations_s3.csv` pointed at arXiv 2011.01079, which the
arXiv API resolves to "Establishing the first hidden-charm pentaquark with strangeness" (hep-ph) — not
this dataset. Resolution performed here, both responses cached under `02_literature/raw/`:

* `crossref_2wiki_ho2020.json` (sha256 `d9e22e03…`) — Crossref
  `works?query.bibliographic=Constructing+A+Multi-hop+QA+Dataset+for+Comprehensive+Evaluation+of+Reasoning+Steps&rows=5`
  returns DOI `10.18653/v1/2020.coling-main.580` as hit 0, *Proceedings of the 28th International
  Conference on Computational Linguistics*, pp. 6609–6625, 2020.
* `acl_2020.coling-main.580.html` / `.bib` (sha256 `0ef31251…` / `8973fe2f…`) — ACL Anthology page and
  BibTeX; `https://doi.org/10.18653/v1/2020.coling-main.580` → HTTP 302 →
  `https://www.aclweb.org/anthology/2020.coling-main.580`.
* **Title-vs-claim check (passed).** The ACL Anthology abstract contains the sentence: *"In this study,
  we present a new multi-hop QA dataset, called 2WikiMultiHopQA, which uses structured and unstructured
  data."* That is the claim the draft needs (this paper introduces the dataset), so the row was added.
* Author list discrepancy: the brief lists five authors including Nagata, but **both Crossref and the
  ACL Anthology BibTeX list four** — Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, Akiko Aizawa. The
  register records the four verified authors; no fifth author was invented.
* One row appended to `02_literature/verified_citations.csv` (317 → 318 rows, no duplicate ids). The
  stale `citations_s3.csv` row is **not** mine to edit and still carries arXiv:2011.01079 — flagged
  here so whoever owns that file can fix or drop it.

## 6. Verification performed

* `eval_transfer.py` recomputes precision/over-refusal/coverage/AUROC from the written CSV; a separate
  throwaway script re-derived all four from `features_transfer.csv` + the refitted gate and matched the
  stored values exactly (AUROC 0.640175 vs stored 0.6402 — rounding to 4 dp).
* Pool coverage assertion: 0 of 400 presented passages missing from the pool (script raises otherwise).
* Item count assertions: 400 unique ids, 200 per rung, feature rows ⊇ item ids.

## 7. Open items / not done here

* No p-value for this arm (PREREGISTRATION §10 D1.4 — H2 compares a held-out number with a
  fitting-half number). None was computed.
* Only rungs 0 and 3 exist in the transfer arm; no rungs 1, 2, 4, so no monotonicity statement is made
  for this corpus.
* The draft/paper files were not touched (forbidden for this task), so any H2 sentence in
  `05_paper/**` that still cites arXiv 2011.01079 remains wrong until its owner updates it.
