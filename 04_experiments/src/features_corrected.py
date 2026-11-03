"""C1 — SENSITIVITY ANALYSIS: spec-conformant retrieval features (question as the dense query).

Why this file exists
--------------------
`features.py` encodes the *presented passage* as the dense query (line 102:
`Pq = dense.encode(present_text)`) and then scores `P @ Pq[k]`, i.e. the presented passage is compared
with itself. The consequence, measured from the written CSV by `eval_transfer.dense_degeneracy()`:
`dense_presented == 1.0` and `dense_rank_log == log1p(1)` on every row of rungs 0-3, `dense_presented`
is exactly `dense_top1`, and the B2 baseline (`single threshold on dense_top1`) therefore degenerates —
the gate's dense coefficients are collinear (`dense_presented` and `dense_top1` received the identical
coefficient 5.9181 in `results/c1/results_full.json`).

PREREGISTRATION.md §4 specifies `dense_presented (bge-small-en-v1.5 cosine)` for a *question*--passage
pair, so the frozen implementation does not compute the feature the pre-registration names. This module
computes it as specified and nothing else:

    dense_presented  = cosine(emb(question), emb(presented passage))
    dense_rank_log   = log1p(1-based rank of the presented passage among all pool documents,
                             ranked by cosine to the QUESTION)
    dense_top1       = max cosine over the pool (to the question)
    dense_margin     = top1 - top2
    top1_agreement   = 1 iff BM25 rank-1 document id == dense rank-1 document id

Everything else — BM25 (score/rank/top1/top5/margin, the split pool, the rung-4 source-document
inheritance), the cross-encoder score and `lex_overlap` — is copied line-for-line from
`features.py`/`features_transfer.py`, and the writing format (header order, `%.10g`) is identical, so the
three CSVs are drop-in replacements for `features.csv`, `features_rung5.csv`, `features_transfer.csv`.

Rung-4 rows (a rewrite of the gold paragraph, not a pool document): `dense_presented` is computed
directly as `cosine(emb(question), emb(rewrite))` — the quantity §4 names — while the presented
passage's dense *rank*, `dense_top1` and `dense_margin` are taken from its source gold document inside
the pool, exactly as `features.py` inherits the source id for the BM25 terms. `bm25_is_source_doc`
stays 1 on those rows so the approximation is auditable.

This file does not modify `features.py`, `features_rung5.py`, `features_transfer.py` or anything in
`results/c1/`. It is a declared sensitivity analysis, not the frozen run.

Outputs
-------
04_experiments/data/features_corrected.csv           (items.jsonl)
04_experiments/data/features_corrected_rung5.csv     (items_rung5.jsonl)
04_experiments/data/features_corrected_transfer.csv  (transfer_items.jsonl)
04_experiments/data/features_corrected_meta.json     (timings, pool sizes, sha256s, degeneracy check)

Run: python 04_experiments/src/features_corrected.py [--dataset all|main|rung5|transfer]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RAW_SQUAD = DATA / "raw" / "dev-v2.0.json"
RAW_2WIKI = DATA / "raw" / "2wiki" / "2wikimultihop_dev.json"

sys.path.insert(0, str(SRC))
import features as F  # noqa: E402  (imported, never modified: pool definition + pinned models)

DENSE_MODEL = F.DENSE_MODEL          # "BAAI/bge-small-en-v1.5"
CE_MODEL = F.CE_MODEL                # "cross-encoder/ms-marco-MiniLM-L-6-v2"

COLS = ["item_id", "split", "rung", "label", "bm25_presented", "bm25_rank_log", "bm25_top1",
        "bm25_top5_mean", "bm25_margin", "dense_presented", "dense_rank_log", "dense_top1",
        "dense_margin", "top1_agreement", "ce_presented", "lex_overlap", "bm25_is_source_doc"]

WS = re.compile(r"\s+")

DATASETS = {
    "main": {"items": DATA / "items.jsonl", "out": DATA / "features_corrected.csv",
             "pools": "squad", "label": "main (rungs 0-4)"},
    "rung5": {"items": DATA / "items_rung5.jsonl", "out": DATA / "features_corrected_rung5.csv",
              "pools": "squad", "label": "EXPLORATORY rung 5 (D2)"},
    "transfer": {"items": DATA / "transfer_items.jsonl",
                 "out": DATA / "features_corrected_transfer.csv",
                 "pools": "2wiki", "label": "transfer arm (H2 second corpus)"},
}
META_OUT = DATA / "features_corrected_meta.json"


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def para_text(sentences) -> str:
    """Identical to features_transfer.para_text, so presented text matches the pool exactly."""
    return WS.sub(" ", " ".join(s.strip() for s in sentences)).strip()


def two_wiki_pool(items: list[dict]) -> tuple[list[str], dict]:
    """Copy of features_transfer.build_pool: union of the source questions' 2Wiki paragraphs."""
    qids: list[str] = []
    for it in items:
        if it["qid"] not in qids:
            qids.append(it["qid"])
    by_id = {}
    for rec in json.loads(RAW_2WIKI.read_text(encoding="utf-8")):
        by_id[rec["_id"]] = rec
    missing = [q for q in qids if q not in by_id]
    if missing:
        raise RuntimeError(f"{len(missing)} qids not found in {RAW_2WIKI}: {missing[:3]}")

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
            "n_pool_documents": len(pool), "n_duplicate_texts_dropped": n_paras - len(pool)}
    return pool, info


def score_group(sitems: list[dict], pool: list[str], gold_of: dict[str, str], dense, ce,
                tag: str, meta: dict) -> dict[str, dict]:
    """BM25 + corrected dense + cross-encoder for one pool. Maths of BM25/CE/lex is features.py's."""
    import bm25s

    t0 = time.time()
    ret = bm25s.BM25()
    tok = bm25s.tokenize(pool, stopwords="en", show_progress=False)
    ret.index(tok, show_progress=False)
    meta.setdefault("bm25_params", {"k1": float(getattr(ret, "k1", -1)),
                                    "b": float(getattr(ret, "b", -1)),
                                    "method": getattr(ret, "method", "?")})
    P = dense.encode(pool, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    pool_set = {c: i for i, c in enumerate(pool)}
    meta["timings"][f"{tag}_index_s"] = round(time.time() - t0, 2)

    # ---- the only changed block: the dense QUERY is the question, not the passage --------------
    t0 = time.time()
    Q = dense.encode([it["question"] for it in sitems], batch_size=64, normalize_embeddings=True,
                     show_progress_bar=False)
    cos_all = Q @ P.T                       # (n_items, n_pool) cosine(question, pool doc)
    meta["timings"][f"{tag}_encode_questions_s"] = round(time.time() - t0, 2)

    # rung-4 rewrites are not pool documents: embed them so dense_presented = cos(question, rewrite)
    rewrite_idx = [k for k, it in enumerate(sitems)
                   if pool_set.get(it["context"]) is None and gold_of.get(it["qid"]) in pool_set]
    rewrite_cos: dict[int, float] = {}
    if rewrite_idx:
        t0 = time.time()
        Rw = dense.encode([sitems[k]["context"] for k in rewrite_idx], batch_size=64,
                          normalize_embeddings=True, show_progress_bar=False)
        for j, k in enumerate(rewrite_idx):
            rewrite_cos[k] = float(np.dot(Q[k], Rw[j]))
        meta["timings"][f"{tag}_encode_rewrites_s"] = round(time.time() - t0, 2)
        meta[f"{tag}_n_rewrite_rows"] = len(rewrite_idx)

    t0 = time.time()
    ce_scores = ce.predict([(it["question"], it["context"][:4000]) for it in sitems],
                           batch_size=64, show_progress_bar=False)
    meta["timings"][f"{tag}_ce_s"] = round(time.time() - t0, 2)

    t0 = time.time()
    Qt = bm25s.tokenize([it["question"] for it in sitems], stopwords="en", show_progress=False)
    b_ids, b_scores = ret.retrieve(Qt, k=len(pool), show_progress=False)
    rows: dict[str, dict] = {}
    for k, it in enumerate(sitems):
        order = np.asarray(b_ids[k], dtype=int)
        srow = np.asarray(b_scores[k], dtype=float)
        top1 = float(srow[0])
        top2 = float(srow[1]) if len(srow) > 1 else 0.0
        top5 = float(np.mean(srow[:5]))
        is_src = 0
        doc_id = pool_set.get(it["context"])
        if doc_id is None:  # rung 4 rewrite: inherit the source gold paragraph's id
            doc_id = pool_set.get(gold_of.get(it["qid"], ""))
            is_src = 1
        if doc_id is not None:
            hit = np.flatnonzero(order == doc_id)
            pos = int(hit[0]) if hit.size else len(pool) - 1  # a doc always appears with k=n
            b_pres, b_rank = float(srow[pos]), float(pos + 1)
        else:
            b_pres, b_rank = float("nan"), float("nan")

        cos = cos_all[k]
        d_order = np.argsort(-cos, kind="stable")
        d_top1 = float(cos.max())
        d_top2 = float(np.partition(cos, -2)[-2]) if len(cos) > 1 else 0.0
        d_rank = float(np.flatnonzero(d_order == doc_id)[0] + 1) if doc_id is not None else float("nan")
        if doc_id is not None and is_src == 0:
            d_pres = float(cos[doc_id])                 # cos(question, presented pool document)
        elif k in rewrite_cos:
            d_pres = rewrite_cos[k]                     # cos(question, rewrite) — §4 quantity
        else:
            d_pres = float("nan")

        qset, pset = set(tokens(it["question"])), set(tokens(it["context"]))
        rows[it["item_id"]] = {
            "item_id": it["item_id"], "split": it["split"], "rung": it["rung"],
            "label": it["label"],
            "bm25_presented": b_pres, "bm25_rank_log": float(np.log1p(b_rank)),
            "bm25_top1": top1, "bm25_top5_mean": top5, "bm25_margin": top1 - top2,
            "dense_presented": d_pres, "dense_rank_log": float(np.log1p(d_rank)),
            "dense_top1": d_top1, "dense_margin": d_top1 - d_top2,
            "top1_agreement": float(int(order[0] == d_order[0])),
            "ce_presented": float(ce_scores[k]), "lex_overlap": len(qset & pset) / max(1, len(qset)),
            "bm25_is_source_doc": float(is_src),
        }
    meta["timings"][f"{tag}_scoring_s"] = round(time.time() - t0, 2)
    return rows


def degeneracy_check(rows: dict[str, dict]) -> dict:
    """Measured proof the corrected dense block is no longer self-scoring."""
    vals = np.asarray([r["dense_presented"] for r in rows.values()], dtype=float)
    ranks = np.asarray([r["dense_rank_log"] for r in rows.values()], dtype=float)
    top1 = np.asarray([r["dense_top1"] for r in rows.values()], dtype=float)
    return {"n_rows": len(rows),
            "frac_dense_presented_eq_1": round(float(np.mean(np.abs(vals - 1.0) <= 1e-6)), 4),
            "frac_dense_presented_eq_dense_top1": round(float(np.mean(np.abs(vals - top1) <= 1e-9)), 4),
            "n_distinct_dense_presented": int(len(np.unique(np.round(vals, 10)))),
            "n_distinct_dense_rank_log": int(len(np.unique(np.round(ranks, 10)))),
            "n_distinct_dense_top1": int(len(np.unique(np.round(top1, 10)))),
            "n_nan_dense_presented": int(np.isnan(vals).sum())}


def extract(dataset: str, dense, ce, write: bool = True) -> dict:
    spec = DATASETS[dataset]
    items = load_jsonl(spec["items"])
    meta: dict = {"dataset": dataset, "label": spec["label"], "dense_model": DENSE_MODEL,
                  "ce_model": CE_MODEL, "bm25": "bm25s", "n_items": len(items),
                  "source_items": str(spec["items"].relative_to(ROOT)).replace("\\", "/"),
                  "output_csv": str(spec["out"].relative_to(ROOT)).replace("\\", "/"),
                  "dense_query": "question", "dense_block": (
                      "dense_presented/rank_log/top1/margin are cosines to the QUESTION; BM25, "
                      "cross-encoder and lex_overlap unchanged from features.py"),
                  "timings": {}, "pool_sizes": {}}

    rows: dict[str, dict] = {}
    if spec["pools"] == "squad":
        pools = F.split_pools()   # identical pools as features.py (imported, not copied)
        for split, (pool, gold_of) in pools.items():
            sitems = [it for it in items if it["split"] == split]
            if not sitems:
                continue
            meta["pool_sizes"][split] = len(pool)
            rows.update(score_group(sitems, pool, gold_of, dense, ce, split, meta))
    else:
        pool, pool_info = two_wiki_pool(items)
        meta["pool_sizes"]["transfer"] = len(pool)
        meta["pool"] = pool_info
        rows.update(score_group(items, pool, {}, dense, ce, "transfer", meta))

    missing = [it["item_id"] for it in items if it["item_id"] not in rows]
    if missing:
        raise RuntimeError(f"{len(missing)} items without features, e.g. {missing[:3]}")
    meta["degeneracy_check"] = degeneracy_check(rows)
    order = [it["item_id"] for it in items]
    meta["row_order_sha256"] = hashlib.sha256(
        ("\n".join(order) + "\n").encode("utf-8")).hexdigest()

    if write:
        spec["out"].parent.mkdir(parents=True, exist_ok=True)
        with open(spec["out"], "w", encoding="utf-8", newline="\n") as fh:
            fh.write(",".join(COLS) + "\n")
            for it in items:
                r = rows[it["item_id"]]
                fh.write(",".join(r[c] if isinstance(r[c], str) else f"{r[c]:.10g}"
                                  for c in COLS) + "\n")
        meta["csv_sha256"] = hashlib.sha256(spec["out"].read_bytes()).hexdigest()
        meta["csv_bytes"] = spec["out"].stat().st_size
    meta["item_file_sha256"] = hashlib.sha256(spec["items"].read_bytes()).hexdigest()
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Spec-conformant (question-query) C1 features.")
    ap.add_argument("--dataset", default="all", choices=["all", *DATASETS])
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    from sentence_transformers import CrossEncoder, SentenceTransformer

    t0 = time.time()
    dense = SentenceTransformer(DENSE_MODEL, device="cpu")
    ce = CrossEncoder(CE_MODEL, device="cpu")
    load_s = round(time.time() - t0, 2)

    names = list(DATASETS) if a.dataset == "all" else [a.dataset]
    all_meta: dict = {}
    if META_OUT.exists() and a.dataset != "all":
        all_meta = json.loads(META_OUT.read_text(encoding="utf-8")).get("datasets", {})
    for name in names:
        m = extract(name, dense, ce, write=not a.no_write)
        m["timings"]["model_load_s"] = load_s
        m["timings"]["total_s"] = round(time.time() - t0, 2)
        all_meta[name] = m
        print(f"[{name}] n={m['n_items']} pools={m['pool_sizes']} "
              f"degeneracy={m['degeneracy_check']}", file=sys.stderr)

    payload = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "python": sys.version.split()[0], "numpy": np.__version__,
               "note": ("Sensitivity analysis: dense features use the QUESTION as query "
                        "(PREREGISTRATION.md §4), unlike features.py which encodes the presented "
                        "passage. Nothing in results/c1/ is touched."),
               "datasets": all_meta}
    if not a.no_write:
        META_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True) if a.json
          else f"wrote {len(names)} corrected feature files; meta -> {META_OUT}")


if __name__ == "__main__":
    main()
