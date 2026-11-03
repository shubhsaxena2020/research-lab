"""C1 — exploratory 'top-1 presented' variant, stage 2: the twelve gate features (D3).

    python 04_experiments/src/features_top1.py

Writes `04_experiments/data/features_top1.csv` and merges a `features` block into
`04_experiments/data/features_top1_meta.json`.

The twelve features, the two models and the arithmetic are the ones in `gate.GATE_FEATURES` /
`features.py`; only the *presented passage* changes: it is always the BM25 rank-1 document.

`bm25_rank_log` is constant here, at `log1p(1) = 0.6931` (not 0 — log1p(1) is ln 2), for every row,
because the presented passage is by construction the rank-1 document. The column is kept so the
feature vector is literally the same twelve columns; a constant column contributes nothing to the
fitted logistic score, which is exactly why the paper's no-rank ablation exists.
`dense_rank_log` is the dense rank of that same BM25-top-1 document and does vary.

DENSE MATH — a deliberate, declared departure from the frozen `features.py`. There, `Pq` is
`dense.encode(present_text)`, i.e. the *presented passage* is encoded as the query, so
`dense_presented = cos(passage, passage) = 1.0`, `dense_top1 = 1.0` and `dense_rank_log = log1p(1)`
for every corpus-document row. Those three columns of `features.csv` are therefore degenerate
(constant), which contradicts PREREGISTRATION §4 ("dense_presented (bge-small-en-v1.5 cosine)" of the
presented passage *for the question*). Reproducing that literally here would make
`dense_presented` a constant 1.0 and the reverse-direction check (AUROC of `dense_presented` alone)
exactly 0.5 by construction — a number about an encoding bug, not about retrieval. So this script
encodes the **question** as the query, which is what §4 describes, and records the frozen column's
degeneracy in `frozen_dense_columns_are_degenerate` so the discrepancy is auditable from the meta
file. `features.py` is not modified (it is outside this variant's ownership); see the run notes.

Because the presented passage is always a pool document, its dense vector is read from the pool matrix
(the same encode call `features.py` makes for the pool), not re-encoded — same numbers, no drift.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import features as F  # noqa: E402  (tokens, split_pools)
import gate as G  # noqa: E402  (GATE_FEATURES — the definition of "the same twelve features")

DATA = F.DATA
ITEMS_IN = DATA / "items_top1.jsonl"
CSV_OUT = DATA / "features_top1.csv"
META_OUT = DATA / "features_top1_meta.json"
COLS = ["item_id", "split", "rung", "label"] + list(G.GATE_FEATURES)


def load_top1_items() -> list[dict]:
    with open(ITEMS_IN, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _merge_meta(block: dict) -> dict:
    meta: dict = {}
    if META_OUT.exists():
        meta = json.loads(META_OUT.read_text(encoding="utf-8"))
    meta.update(block)
    META_OUT.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return meta


def extract(write: bool = True) -> dict:
    import bm25s
    from sentence_transformers import CrossEncoder, SentenceTransformer

    items = load_top1_items()
    pools = F.split_pools()
    meta: dict = {"n_items": len(items), "features": list(G.GATE_FEATURES),
                  "dense_model": F.DENSE_MODEL, "ce_model": F.CE_MODEL,
                  "timings": {}}

    t0 = time.time()
    dense = SentenceTransformer(F.DENSE_MODEL, device="cpu")
    ce = CrossEncoder(F.CE_MODEL, device="cpu")
    meta["timings"]["model_load_s"] = round(time.time() - t0, 2)

    rows: dict[str, dict] = {}
    for split, (pool, _gold_of) in pools.items():
        sitems = [it for it in items if it["split"] == split]
        if not sitems:
            continue
        pool_set = {c: i for i, c in enumerate(pool)}

        t0 = time.time()
        ret = bm25s.BM25()
        ret.index(bm25s.tokenize(pool, stopwords="en", show_progress=False), show_progress=False)
        P = dense.encode(pool, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
        meta["timings"][f"{split}_index_s"] = round(time.time() - t0, 2)

        # the presented passage is always a corpus document here; fail loudly if that ever breaks
        missing = [it["item_id"] for it in sitems if it["context"] not in pool_set]
        if missing:
            raise RuntimeError(f"{len(missing)} presented passages are not pool documents: {missing[:3]}")

        t0 = time.time()
        Pq = dense.encode([it["question"] for it in sitems], batch_size=64,
                          normalize_embeddings=True, show_progress_bar=False)
        meta["timings"][f"{split}_encode_questions_s"] = round(time.time() - t0, 2)

        t0 = time.time()
        ce_scores = ce.predict([(it["question"], it["context"][:4000]) for it in sitems],
                               batch_size=64, show_progress_bar=False)
        meta["timings"][f"{split}_ce_s"] = round(time.time() - t0, 2)

        t0 = time.time()
        Qt = bm25s.tokenize([it["question"] for it in sitems], stopwords="en", show_progress=False)
        b_ids, b_scores = ret.retrieve(Qt, k=len(pool), show_progress=False)
        for k, it in enumerate(sitems):
            order = np.asarray(b_ids[k], dtype=int)
            srow = np.asarray(b_scores[k], dtype=float)
            top1 = float(srow[0])
            top2 = float(srow[1]) if len(srow) > 1 else 0.0
            top5 = float(np.mean(srow[:5]))

            doc_id = pool_set[it["context"]]           # == order[0] by construction
            if int(order[0]) != doc_id:
                raise RuntimeError(f"{it['item_id']}: presented doc is not the BM25 rank-1 doc")
            b_pres, b_rank = float(srow[0]), 1.0

            cos = P @ Pq[k]
            d_order = np.argsort(-cos, kind="stable")
            d_top1 = float(cos.max())
            d_top2 = float(np.partition(cos, -2)[-2]) if len(cos) > 1 else 0.0
            d_rank = float(np.flatnonzero(d_order == doc_id)[0] + 1)
            d_pres = float(cos[doc_id])

            qset, pset = set(F.tokens(it["question"])), set(F.tokens(it["context"]))
            rows[it["item_id"]] = {
                "item_id": it["item_id"], "split": split, "rung": int(it["rung"]),
                "label": int(it["label"]),
                "bm25_presented": b_pres, "bm25_rank_log": float(np.log1p(b_rank)),
                "bm25_top1": top1, "bm25_top5_mean": top5, "bm25_margin": top1 - top2,
                "dense_presented": d_pres, "dense_rank_log": float(np.log1p(d_rank)),
                "dense_top1": d_top1, "dense_margin": d_top1 - d_top2,
                "top1_agreement": float(int(int(order[0]) == int(d_order[0]))),
                "ce_presented": float(ce_scores[k]),
                "lex_overlap": len(qset & pset) / max(1, len(qset)),
            }
        meta["timings"][f"{split}_scoring_s"] = round(time.time() - t0, 2)

    # ---- consistency check against the frozen run's rung-0 rows -----------------------
    # For a retrieval HIT the presented passage is the gold paragraph, so BM25 score, cross-encoder
    # score and lexical overlap must equal the rung-0 row of features.csv (same passage, same question,
    # same models). dense_presented is excluded on purpose: the frozen column is degenerate (below), so
    # agreement there would certify the bug, not the arithmetic. Cross-encoder scores differ at ~1e-5
    # because the frozen run batched all 1,873 dev pairs together and this one batches 400 — float
    # non-determinism of the same model on the same pair, not a different model.
    check = {"n_compared": 0, "max_abs_diff": {}, "compared_features": ["bm25_presented",
                                                                      "ce_presented", "lex_overlap"],
             "excluded": {"dense_presented": "frozen column degenerate; see frozen_dense_columns_are_degenerate"}}
    frozen_dense: dict = {}
    try:
        frozen = G.load_features()
        for it in items:
            if not it["is_gold"]:
                continue
            ref_id = f"{it['split']}:{it['qid']}:r0"
            if ref_id not in frozen:
                continue
            check["n_compared"] += 1
            for c in ("bm25_presented", "ce_presented", "lex_overlap"):
                d = abs(rows[it["item_id"]][c] - frozen[ref_id][c])
                check["max_abs_diff"][c] = max(check["max_abs_diff"].get(c, 0.0), d)
        check["max_abs_diff"] = {k: round(v, 9) for k, v in check["max_abs_diff"].items()}
        check["tolerance"] = {"bm25_presented": 1e-6, "ce_presented": 1e-4, "lex_overlap": 0.0}
        check["passed"] = bool(all(check["max_abs_diff"][c] <= check["tolerance"][c]
                                   for c in check["max_abs_diff"]))

        # the frozen dense block, read straight from features.csv
        by_rung: dict[str, list[float]] = {}
        for iid, rec in frozen.items():
            by_rung.setdefault(str(rec["rung"]), []).append(rec["dense_presented"])
        frozen_dense = {
            "source": "04_experiments/data/features.csv columns dense_presented / dense_top1 / dense_rank_log",
            "per_rung_dense_presented": {r: {"n": len(v), "mean": round(float(np.mean(v)), 6),
                                             "min": round(float(np.min(v)), 6),
                                             "max": round(float(np.max(v)), 6),
                                             "sd": round(float(np.std(v)), 6)}
                                         for r, v in sorted(by_rung.items())},
            "fraction_within_1e-3_of_1.0": round(float(np.mean([abs(x - 1.0) <= 1e-3
                                                                for v in by_rung.values() for x in v])), 6),
            "cause": ("features.py encodes present_text as the dense query (Pq = encode(present_text)), "
                      "so cos(presented, presented) = 1.0; dense_rank_log is then log1p(1) = 0.6931 "
                      "and dense_top1 = 1.0 for every corpus-document row"),
            "consequence": ("three of the twelve frozen gate columns carry no question-passage signal; "
                            "the dense block reduces to dense_margin (a passage-distinctiveness term)"),
        }
    except FileNotFoundError:
        check["status"] = "features.csv absent; check skipped"

    meta["consistency_check_vs_frozen_rung0"] = check
    meta["frozen_dense_columns_are_degenerate"] = frozen_dense
    meta["dense_math"] = {
        "used_here": "query = question; dense_presented = cos(question, presented passage)",
        "reason": "PREREGISTRATION.md §4 defines the feature this way; the frozen code does not",
        "literal_frozen_math_would_give": "dense_presented = 1.0 constant, AUROC 0.5 by construction",
    }
    meta["constant_by_construction"] = {
        "bm25_rank_log": sorted({round(r["bm25_rank_log"], 12) for r in rows.values()}),
        "note": ("log1p(1) = 0.6931 for every row: the presented passage is the BM25 rank-1 document. "
                 "Kept in the vector; contributes nothing to the fitted score."),
    }
    meta["feature_ranges"] = {c: {"min": round(float(np.min([r[c] for r in rows.values()])), 6),
                                  "max": round(float(np.max([r[c] for r in rows.values()])), 6),
                                  "sd": round(float(np.std([r[c] for r in rows.values()])), 6)}
                              for c in G.GATE_FEATURES}

    if write:
        with open(CSV_OUT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(",".join(COLS) + "\n")
            for it in items:
                r = rows[it["item_id"]]
                fh.write(",".join(r[c] if isinstance(r[c], str) else f"{r[c]:.10g}"
                                  for c in COLS) + "\n")
        meta["csv_sha256"] = hashlib.sha256(CSV_OUT.read_bytes()).hexdigest()
        _merge_meta({"features": meta})
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract top-1-presented variant features (D3).")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    m = extract(write=not a.no_write)
    print(json.dumps({k: m[k] for k in ("n_items", "timings", "consistency_check_vs_frozen_rung0",
                                        "constant_by_construction") if k in m},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
