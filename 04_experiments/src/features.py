"""C1 — stage 3: retrieval-side feature extraction (BM25, dense cosine, cross-encoder).

Writes `04_experiments/data/features.csv` + `features_meta.json`. Deterministic: no randomness at all,
models pinned in PREREGISTRATION.md §4.

Design notes that belong in the paper's methods:

* Retrieval runs over the item's own *split* pool (dev articles and test articles never share a pool),
  so no test paragraph can be retrieved while fitting on dev.
* The presented passage is scored directly: `bm25_presented`/`bm25_rank_presented` are the BM25 score
  and rank of the presented passage inside the split pool. A rung-4 passage is a *rewritten* gold
  passage and is therefore not a corpus document; it inherits the source paragraph's id and the
  `bm25_is_source_doc` flag is 1 for those rows (the rewrite is one short span, so the score it would
  have is within a token or two of its source; the flag makes the approximation auditable).
* Dense and cross-encoder features are computed on the actual presented text in every rung.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_experiments" / "data"
RAW = DATA / "raw" / "dev-v2.0.json"

DENSE_MODEL = "BAAI/bge-small-en-v1.5"
CE_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
BM25_K1, BM25_B = None, None  # bm25s defaults; recorded from the object into meta


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def load_items() -> list[dict]:
    with open(DATA / "items.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def split_pools() -> dict[str, tuple[list[str], dict[str, str]]]:
    """split -> (pool paragraphs, qid -> gold paragraph).

    Pools are built by *article title* only, the same rule the split used, so a paragraph can never sit
    in the other split's pool.
    """
    data = json.loads(RAW.read_text(encoding="utf-8"))["data"]
    split_by_title: dict[str, str] = {}
    for it in load_items():
        split_by_title.setdefault(it["title"], it["split"])
    pools: dict[str, list[str]] = {"dev": [], "test": []}
    gold: dict[str, str] = {}
    for art in data:
        s = split_by_title.get(art["title"])
        for p in art["paragraphs"]:
            for q in p["qas"]:
                gold[q["id"]] = p["context"]
            if s:
                pools[s].append(p["context"])
    missing = [t for t in split_by_title if t not in {a["title"] for a in data}]
    if missing:
        raise RuntimeError(f"titles not in SQuAD dev: {missing}")
    return {s: (p, gold) for s, p in pools.items()}


def extract(write: bool = True) -> dict:
    import bm25s
    from sentence_transformers import CrossEncoder, SentenceTransformer

    items = load_items()
    pools = split_pools()
    meta: dict = {"dense_model": DENSE_MODEL, "ce_model": CE_MODEL, "bm25": "bm25s",
                  "n_items": len(items), "pools": {s: len(p) for s, (p, _) in pools.items()},
                  "timings": {}}

    t0 = time.time()
    dense = SentenceTransformer(DENSE_MODEL, device="cpu")
    ce = CrossEncoder(CE_MODEL, device="cpu")
    meta["timings"]["model_load_s"] = round(time.time() - t0, 2)

    rows: dict[str, dict] = {}
    for split, (pool, gold_of) in pools.items():
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
            is_src = 0
            doc_id = pool_set.get(it["context"])
            if doc_id is None:  # rung 4 rewrite: inherit the source gold paragraph's id
                doc_id = pool_set.get(gold_of[it["qid"]])
                is_src = 1
            if doc_id is not None:
                hit = np.flatnonzero(order == doc_id)
                pos = int(hit[0]) if hit.size else len(pool) - 1  # a doc always appears with k=n
                b_pres, b_rank = float(srow[pos]), float(pos + 1)
            else:
                b_pres, b_rank = float("nan"), float("nan")
            d_order = np.argsort(-P @ Pq[k], kind="stable")
            cos = P @ Pq[k]
            d_top1 = float(cos.max())
            d_top2 = float(np.partition(cos, -2)[-2]) if len(cos) > 1 else 0.0
            d_rank = float(np.flatnonzero(d_order == doc_id)[0] + 1) if doc_id is not None else float("nan")
            d_pres = float(cos[doc_id]) if doc_id is not None else float(np.dot(
                Pq[k], dense.encode([it["context"]], normalize_embeddings=True,
                                    show_progress_bar=False)[0]))

            qset, pset = set(tokens(it["question"])), set(tokens(it["context"]))
            rows[it["item_id"]] = {
                "item_id": it["item_id"], "split": split, "rung": it["rung"],
                "label": it["label"],
                "bm25_presented": b_pres, "bm25_rank_log": float(np.log1p(b_rank)),
                "bm25_top1": top1, "bm25_top5_mean": top5, "bm25_margin": top1 - top2,
                "dense_presented": d_pres, "dense_rank_log": float(np.log1p(d_rank)),
                "dense_top1": d_top1, "dense_margin": d_top1 - d_top2,
                "top1_agreement": float(int(order[0] == np.argsort(-cos, kind="stable")[0])),
                "ce_presented": float(ce_scores[k]), "lex_overlap": len(qset & pset) / max(1, len(qset)),
                "bm25_is_source_doc": float(is_src),
            }
        meta["timings"][f"{split}_scoring_s"] = round(time.time() - t0, 2)

    cols = ["item_id", "split", "rung", "label", "bm25_presented", "bm25_rank_log", "bm25_top1",
            "bm25_top5_mean", "bm25_margin", "dense_presented", "dense_rank_log", "dense_top1",
            "dense_margin", "top1_agreement", "ce_presented", "lex_overlap", "bm25_is_source_doc"]
    if write:
        DATA.mkdir(parents=True, exist_ok=True)
        out = DATA / "features.csv"
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(",".join(cols) + "\n")
            for it in items:
                r = rows[it["item_id"]]
                fh.write(",".join(r[c] if isinstance(r[c], str) else f"{r[c]:.10g}"
                                  for c in cols) + "\n")
        meta["csv_sha256"] = __import__("hashlib").sha256(out.read_bytes()).hexdigest()
        (DATA / "features_meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n",
                                                 encoding="utf-8")
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract C1 retrieval-side features.")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = extract(write=not a.no_write)
    if a.json:
        print(json.dumps(m, indent=2, sort_keys=True))
    else:
        print("features written", m.get("timings"), file=sys.stderr)


if __name__ == "__main__":
    main()
