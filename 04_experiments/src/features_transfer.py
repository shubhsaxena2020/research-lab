"""C1 — H2 second-corpus arm: retrieval-side features for the 400 transfer items.

Writes `04_experiments/data/features_transfer.csv` + `features_transfer_meta.json`.
Deterministic: no randomness at all, same pinned models as `features.py`.

The only difference from `features.py` is the *pool*. The dev/test arms each have one
paragraph pool built from that split's articles. 2WikiMultihopQA has no split-level
corpus in this study, so the analogue is the union of every `[title, [sentences]]`
paragraph in the `context` of the 200 source questions the transfer items were built
from, deduplicated by exact text. Every presented passage in the transfer arm is a
pool document (rung 0 = a supporting paragraph, rung 3 = another paragraph from the
same question's context set), so `bm25_is_source_doc` is 0 for all 400 rows and no
source-doc inheritance is needed.

Feature maths is copied line-for-line from `features.py` (BM25 score/rank of the
presented passage in the pool, corpus top-1/top-5/margin, dense cosine/rank/top-1/
margin, BM25-vs-dense top-1 agreement, cross-encoder score, lexical overlap).

Run: python 04_experiments/src/features_transfer.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_experiments" / "data"
ITEMS = DATA / "transfer_items.jsonl"
RAW = DATA / "raw" / "2wiki" / "2wikimultihop_dev.json"

DENSE_MODEL = "BAAI/bge-small-en-v1.5"
CE_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

COLS = ["item_id", "split", "rung", "label", "bm25_presented", "bm25_rank_log", "bm25_top1",
        "bm25_top5_mean", "bm25_margin", "dense_presented", "dense_rank_log", "dense_top1",
        "dense_margin", "top1_agreement", "ce_presented", "lex_overlap", "bm25_is_source_doc"]

WS = re.compile(r"\s+")


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def para_text(sentences) -> str:
    """Identical to build_transfer_items.para_text, so presented text matches the pool exactly."""
    return WS.sub(" ", " ".join(s.strip() for s in sentences)).strip()


def load_items() -> list[dict]:
    with open(ITEMS, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def build_pool(items: list[dict]) -> tuple[list[str], dict]:
    """Union of the paragraphs of every source question's 2Wiki `context`, dedup by exact text."""
    qids: list[str] = []
    for it in items:
        if it["qid"] not in qids:
            qids.append(it["qid"])
    by_id = {}
    for rec in json.loads(RAW.read_text(encoding="utf-8")):
        by_id[rec["_id"]] = rec
    missing = [q for q in qids if q not in by_id]
    if missing:
        raise RuntimeError(f"{len(missing)} qids not found in {RAW}: {missing[:3]}")

    pool: list[str] = []
    seen: set[str] = set()
    n_paras = 0
    for q in qids:
        for _title, sentences in by_id[q]["context"]:
            n_paras += 1
            txt = para_text(sentences)
            if txt and txt not in seen:
                seen.add(txt)
                pool.append(txt)
    info = {"n_qids": len(qids), "n_paragraphs_before_dedup": n_paras,
            "n_pool_documents": len(pool),
            "n_duplicate_texts_dropped": n_paras - len(pool)}
    return pool, info


def extract(write: bool = True) -> dict:
    import bm25s
    from sentence_transformers import CrossEncoder, SentenceTransformer

    items = load_items()
    pool, pool_info = build_pool(items)
    meta: dict = {"dense_model": DENSE_MODEL, "ce_model": CE_MODEL, "bm25": "bm25s",
                  "bm25_stopwords": "en", "n_items": len(items), "pool": pool_info,
                  "pool_definition": ("union of every [title,[sentences]] paragraph in the "
                                      "context of the 200 source 2Wiki questions, dedup by "
                                      "exact text; analogue of the split pool in features.py"),
                  "source_items": str(ITEMS.relative_to(ROOT)).replace("\\", "/"),
                  "source_corpus": str(RAW.relative_to(ROOT)).replace("\\", "/"),
                  "timings": {}}

    t0 = time.time()
    dense = SentenceTransformer(DENSE_MODEL, device="cpu")
    ce = CrossEncoder(CE_MODEL, device="cpu")
    meta["timings"]["model_load_s"] = round(time.time() - t0, 2)

    t0 = time.time()
    ret = bm25s.BM25()
    tok = bm25s.tokenize(pool, stopwords="en", show_progress=False)
    ret.index(tok, show_progress=False)
    meta["bm25_params"] = {"k1": float(getattr(ret, "k1", -1)),
                           "b": float(getattr(ret, "b", -1)),
                           "method": getattr(ret, "method", "?")}
    P = dense.encode(pool, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    pool_set = {c: i for i, c in enumerate(pool)}
    meta["timings"]["index_s"] = round(time.time() - t0, 2)

    present_text = [it["context"] for it in items]
    t0 = time.time()
    Pq = dense.encode(present_text, batch_size=64, normalize_embeddings=True,
                      show_progress_bar=False)
    meta["timings"]["encode_presented_s"] = round(time.time() - t0, 2)

    t0 = time.time()
    ce_scores = ce.predict([(it["question"], it["context"][:4000]) for it in items],
                           batch_size=64, show_progress_bar=False)
    meta["timings"]["ce_s"] = round(time.time() - t0, 2)

    t0 = time.time()
    Qt = bm25s.tokenize([it["question"] for it in items], stopwords="en", show_progress=False)
    b_ids, b_scores = ret.retrieve(Qt, k=len(pool), show_progress=False)

    rows: dict[str, dict] = {}
    n_missing_doc = 0
    for k, it in enumerate(items):
        order = np.asarray(b_ids[k], dtype=int)
        srow = np.asarray(b_scores[k], dtype=float)
        top1 = float(srow[0])
        top2 = float(srow[1]) if len(srow) > 1 else 0.0
        top5 = float(np.mean(srow[:5]))
        doc_id = pool_set.get(it["context"])
        if doc_id is None:  # every transfer passage is a pool document; flag if that ever breaks
            n_missing_doc += 1
            b_pres = b_rank = float("nan")
        else:
            hit = np.flatnonzero(order == doc_id)
            pos = int(hit[0]) if hit.size else len(pool) - 1  # a doc always appears with k=n
            b_pres, b_rank = float(srow[pos]), float(pos + 1)

        cos = P @ Pq[k]
        d_order = np.argsort(-cos, kind="stable")
        d_top1 = float(cos.max())
        d_top2 = float(np.partition(cos, -2)[-2]) if len(cos) > 1 else 0.0
        d_rank = float(np.flatnonzero(d_order == doc_id)[0] + 1) if doc_id is not None else float("nan")
        d_pres = float(cos[doc_id]) if doc_id is not None else float("nan")

        qset, pset = set(tokens(it["question"])), set(tokens(it["context"]))
        rows[it["item_id"]] = {
            "item_id": it["item_id"], "split": it["split"], "rung": it["rung"],
            "label": it["label"],
            "bm25_presented": b_pres, "bm25_rank_log": float(np.log1p(b_rank)),
            "bm25_top1": top1, "bm25_top5_mean": top5, "bm25_margin": top1 - top2,
            "dense_presented": d_pres, "dense_rank_log": float(np.log1p(d_rank)),
            "dense_top1": d_top1, "dense_margin": d_top1 - d_top2,
            "top1_agreement": float(int(order[0] == np.argsort(-cos, kind="stable")[0])),
            "ce_presented": float(ce_scores[k]), "lex_overlap": len(qset & pset) / max(1, len(qset)),
            "bm25_is_source_doc": 0.0,
        }
    meta["timings"]["scoring_s"] = round(time.time() - t0, 2)
    meta["n_presented_not_in_pool"] = n_missing_doc
    if n_missing_doc:
        raise RuntimeError(f"{n_missing_doc} presented passages not found in the pool")

    l0 = [it["n_context_chars"] for it in items if it["rung"] == 0]
    l3 = [it["n_context_chars"] for it in items if it["rung"] == 3]
    meta["presented_chars"] = {"rung0_median": statistics.median(l0),
                              "rung3_median": statistics.median(l3),
                              "all_median": statistics.median(l0 + l3)}
    meta["n_per_rung"] = {str(r): sum(1 for it in items if it["rung"] == r) for r in (0, 3)}

    if write:
        DATA.mkdir(parents=True, exist_ok=True)
        out = DATA / "features_transfer.csv"
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(",".join(COLS) + "\n")
            for it in items:
                r = rows[it["item_id"]]
                fh.write(",".join(r[c] if isinstance(r[c], str) else f"{r[c]:.10g}"
                                  for c in COLS) + "\n")
        meta["csv_sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
        (DATA / "features_transfer_meta.json").write_text(
            json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract transfer-arm retrieval features.")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = extract(write=not a.no_write)
    if a.json:
        print(json.dumps(m, indent=2, sort_keys=True))
    else:
        print("features_transfer written", m.get("timings"), file=sys.stderr)
        print(json.dumps(m["pool"], sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    main()
