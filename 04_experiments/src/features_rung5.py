"""C1 — EXPLORATORY rung 5 features (PREREGISTRATION.md §10 D2).

Same twelve features, same pinned models, same math as `features.py` (§4), applied to the rung-5 items
built by `build_items_rung5.py`:

* retrieval runs over the item's own split pool, built by `features.split_pools()`;
* `bm25_rank_log` / `dense_rank_log` are log1p of the 1-based rank of the presented passage inside that
  pool (a rung-5 passage is always a real pool document, so `bm25_is_source_doc` is 0 everywhere);
* `ce_presented` is the cross-encoder score of the actual presented text.

Writes `data/features_rung5.csv` (header identical to `data/features.csv`) and
`data/features_rung5_meta.json` (timings + sha256). Deterministic; no randomness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import features as F  # noqa: E402  (import only; never modified)

DATA = ROOT / "04_experiments" / "data"
COLS = ["item_id", "split", "rung", "label", "bm25_presented", "bm25_rank_log", "bm25_top1",
        "bm25_top5_mean", "bm25_margin", "dense_presented", "dense_rank_log", "dense_top1",
        "dense_margin", "top1_agreement", "ce_presented", "lex_overlap", "bm25_is_source_doc"]


def load_items() -> list[dict]:
    with open(DATA / "items_rung5.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def extract(write: bool = True) -> dict:
    import bm25s
    from sentence_transformers import CrossEncoder, SentenceTransformer

    items = load_items()
    pools = F.split_pools()
    meta: dict = {"dense_model": F.DENSE_MODEL, "ce_model": F.CE_MODEL, "bm25": "bm25s",
                  "n_items": len(items), "pools": {s: len(p) for s, (p, _) in pools.items()},
                  "rung": 5, "label": "EXPLORATORY (D2)", "timings": {}}

    t0 = time.time()
    dense = SentenceTransformer(F.DENSE_MODEL, device="cpu")
    ce = CrossEncoder(F.CE_MODEL, device="cpu")
    meta["timings"]["model_load_s"] = round(time.time() - t0, 2)

    rows: dict[str, dict] = {}
    for split in ("dev", "test"):
        pool, _gold_of = pools[split]
        t0 = time.time()
        ret = bm25s.BM25()
        tok = bm25s.tokenize(pool, stopwords="en", show_progress=False)
        ret.index(tok, show_progress=False)
        meta.setdefault("bm25_params", {"k1": float(getattr(ret, "k1", -1)),
                                        "b": float(getattr(ret, "b", -1)),
                                        "method": getattr(ret, "method", "?")})
        P = dense.encode(pool, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
        pool_set = {c: i for i, c in enumerate(pool)}
        meta["timings"][f"{split}_index_s"] = round(time.time() - t0, 2)

        sitems = [it for it in items if it["split"] == split]
        present_text = [it["context"] for it in sitems]
        t0 = time.time()
        Pq = dense.encode(present_text, batch_size=64, normalize_embeddings=True,
                          show_progress_bar=False)
        meta["timings"][f"{split}_encode_presented_s"] = round(time.time() - t0, 2)

        t0 = time.time()
        ce_scores = ce.predict([(it["question"], it["context"][:4000]) for it in sitems],
                               batch_size=64, show_progress_bar=False)
        meta["timings"][f"{split}_ce_s"] = round(time.time() - t0, 2)

        t0 = time.time()
        Qt = bm25s.tokenize([it["question"] for it in sitems], stopwords="en",
                            show_progress=False)
        b_ids, b_scores = ret.retrieve(Qt, k=len(pool), show_progress=False)
        for k, it in enumerate(sitems):
            order = np.asarray(b_ids[k], dtype=int)
            srow = np.asarray(b_scores[k], dtype=float)
            top1 = float(srow[0])
            top2 = float(srow[1]) if len(srow) > 1 else 0.0
            top5 = float(np.mean(srow[:5]))
            doc_id = pool_set.get(it["context"])
            if doc_id is None:
                raise RuntimeError(f"rung-5 context not a pool document: {it['item_id']}")
            hit = np.flatnonzero(order == doc_id)
            pos = int(hit[0]) if hit.size else len(pool) - 1
            b_pres, b_rank = float(srow[pos]), float(pos + 1)

            cos = P @ Pq[k]
            d_order = np.argsort(-cos, kind="stable")
            d_top1 = float(cos.max())
            d_top2 = float(np.partition(cos, -2)[-2]) if len(cos) > 1 else 0.0
            d_rank = float(np.flatnonzero(d_order == doc_id)[0] + 1)
            d_pres = float(cos[doc_id])

            qset, pset = set(F.tokens(it["question"])), set(F.tokens(it["context"]))
            rows[it["item_id"]] = {
                "item_id": it["item_id"], "split": split, "rung": it["rung"],
                "label": it["label"],
                "bm25_presented": b_pres, "bm25_rank_log": float(np.log1p(b_rank)),
                "bm25_top1": top1, "bm25_top5_mean": top5, "bm25_margin": top1 - top2,
                "dense_presented": d_pres, "dense_rank_log": float(np.log1p(d_rank)),
                "dense_top1": d_top1, "dense_margin": d_top1 - d_top2,
                "top1_agreement": float(int(order[0] == d_order[0])),
                "ce_presented": float(ce_scores[k]),
                "lex_overlap": len(qset & pset) / max(1, len(qset)),
                "bm25_is_source_doc": 0.0,
            }
        meta["timings"][f"{split}_scoring_s"] = round(time.time() - t0, 2)

    if write:
        DATA.mkdir(parents=True, exist_ok=True)
        out = DATA / "features_rung5.csv"
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(",".join(COLS) + "\n")
            for it in items:
                r = rows[it["item_id"]]
                fh.write(",".join(r[c] if isinstance(r[c], str) else f"{r[c]:.10g}"
                                  for c in COLS) + "\n")
        meta["csv_sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
        (DATA / "features_rung5_meta.json").write_text(
            json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract C1 rung-5 retrieval-side features (D2).")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = extract(write=not a.no_write)
    if a.json:
        print(json.dumps(m, indent=2, sort_keys=True))
    else:
        print("rung5 features written", m.get("timings"), file=sys.stderr)


if __name__ == "__main__":
    main()
