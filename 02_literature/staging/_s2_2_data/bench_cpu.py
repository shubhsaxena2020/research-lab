"""S2-2: measure CPU cost + retrieval quality of standard baselines on LoCoMo.

Runs on the target laptop (CPU only). Writes results to s2_2_cpu_baselines.json.
Purpose: give the deep dive measured numbers instead of guesses.
"""
import json, os, time, statistics, sys

D = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(D, "locomo10.json")
OUT = os.path.join(D, "s2_2_cpu_baselines.json")
LIMIT_Q = int(os.environ.get("LIMIT_Q", "0"))  # 0 = all

def rss_mb():
    import psutil
    return psutil.Process().memory_info().rss / (1024.0 * 1024.0)

conv = json.load(open(DATA, encoding="utf-8"))

# build per-conversation corpus of turns
corpora = []
for c in conv:
    turns = []
    for k, v in c["conversation"].items():
        if k.startswith("session_") and isinstance(v, list) and not k.endswith("date_time"):
            for t in v:
                turns.append({"dia_id": t.get("dia_id"), "text": t.get("text", ""),
                              "speaker": t.get("speaker", "")})
    corpora.append({"turns": turns, "qa": c["qa"]})

res = {"n_conv": len(corpora), "n_turns": sum(len(c["turns"]) for c in corpora),
       "n_qa": sum(len(c["qa"]) for c in corpora)}

import numpy as np
import bm25s
from sentence_transformers import SentenceTransformer, CrossEncoder

# ---------------- BM25
t0 = time.time()
bm25_idx = []
for c in corpora:
    tok = bm25s.tokenize([t["text"] for t in c["turns"]], stopwords="en", stemmer=None)
    r = bm25s.BM25()
    r.index(tok)
    bm25_idx.append(r)
res["bm25_index_s"] = round(time.time() - t0, 2)
res["rss_after_bm25_mb"] = round(rss_mb(), 1)

def bm25_rank(ci, q, k=10):
    tok = bm25s.tokenize([q], stopwords="en", stemmer=None)
    idx, _ = bm25_idx[ci].retrieve(tok, k=k, show_progress=False)
    return idx[0].tolist()

# ---------------- dense
def dense_run(model_name, qlimit):
    t0 = time.time()
    m = SentenceTransformer(model_name, device="cpu")
    load_s = time.time() - t0
    emb = []
    t0 = time.time()
    for c in corpora:
        emb.append(m.encode([t["text"] for t in c["turns"]], batch_size=64,
                            convert_to_numpy=True, normalize_embeddings=True,
                            show_progress_bar=False))
    enc_s = time.time() - t0
    n = sum(len(e) for e in emb)
    out = {"load_s": round(load_s, 2), "encode_s": round(enc_s, 2),
           "turns_per_s": round(n / max(enc_s, 1e-9), 1),
           "params_m": round(sum(p.numel() for p in m.parameters()) / 1e6, 1),
           "dim": int(emb[0].shape[1]),
           "embed_bytes_per_turn": int(emb[0].nbytes / emb[0].shape[0]),
           "rss_mb": round(rss_mb(), 1)}
    # retrieval quality
    qlat = []
    hits5 = hits10 = tot = 0
    for ci, c in enumerate(corpora):
        qs = c["qa"][:qlimit] if qlimit else c["qa"]
        for q in qs:
            ev = q.get("evidence") or []
            if not ev:
                continue
            t0 = time.time()
            qv = m.encode([q["question"]], normalize_embeddings=True, show_progress_bar=False)
            sims = emb[ci] @ qv[0]
            top = np.argsort(-sims)[:10]
            qlat.append((time.time() - t0) * 1000)
            ids = [corpora[ci]["turns"][i]["dia_id"] for i in top]
            tot += 1
            hits5 += len(set(ev) & set(ids[:5])) > 0
            hits10 += len(set(ev) & set(ids)) > 0
    out.update({"recall@5": round(hits5 / tot, 4), "recall@10": round(hits10 / tot, 4),
                "n_eval_q": tot, "query_ms_mean": round(statistics.mean(qlat), 2),
                "query_ms_p95": round(sorted(qlat)[int(0.95 * len(qlat))], 2)})
    return out, m, emb

# BM25 quality (same protocol)
def bm25_quality(qlimit):
    qlat = []
    hits5 = hits10 = tot = 0
    for ci, c in enumerate(corpora):
        qs = c["qa"][:qlimit] if qlimit else c["qa"]
        tok = bm25s.tokenize([q["question"] for q in qs], stopwords="en", stemmer=None)
        t0 = time.time()
        idxs, _ = bm25_idx[ci].retrieve(tok, k=10, show_progress=False)
        dt = (time.time() - t0) * 1000 / max(len(qs), 1)
        for j, q in enumerate(qs):
            ev = q.get("evidence") or []
            if not ev:
                continue
            tot += 1
            qlat.append(dt)
            ids = [corpora[ci]["turns"][i]["dia_id"] for i in idxs[j].tolist()]
            hits5 += len(set(ev) & set(ids[:5])) > 0
            hits10 += len(set(ev) & set(ids)) > 0
    return {"recall@5": round(hits5 / tot, 4), "recall@10": round(hits10 / tot, 4),
            "n_eval_q": tot, "query_ms_mean": round(statistics.mean(qlat), 2)}

res["bm25"] = bm25_quality(LIMIT_Q)
print("bm25 done", res["bm25"], flush=True)

for name in ["sentence-transformers/all-MiniLM-L6-v2", "BAAI/bge-small-en-v1.5"]:
    o, m, emb = dense_run(name, LIMIT_Q)
    res[name] = o
    print(name, o, flush=True)
    # hybrid RRF + cross-encoder on a subset
    if name.endswith("MiniLM-L6-v2"):
        ce_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
        t0 = time.time()
        ce = CrossEncoder(ce_name, device="cpu", max_length=512)
        res["ce_load_s"] = round(time.time() - t0, 2)
        res["ce_params_m"] = round(sum(p.numel() for p in ce.model.parameters()) / 1e6, 1)
        # RRF( bm25, dense ) recall, and CE rerank of dense top-50
        hits5 = hits10 = tot = 0
        rr_hits5 = 0
        ce_lat = []
        ce_q = 0
        for ci, c in enumerate(corpora):
            qs = c["qa"][:LIMIT_Q] if LIMIT_Q else c["qa"]
            for q in qs:
                ev = q.get("evidence") or []
                if not ev:
                    continue
                tot += 1
                qv = m.encode([q["question"]], normalize_embeddings=True, show_progress_bar=False)
                sims = emb[ci] @ qv[0]
                dtop = np.argsort(-sims)[:50]
                bt = bm25_rank(ci, q["question"], k=50)
                # RRF
                score = {}
                for r, i in enumerate(dtop.tolist()):
                    score[i] = score.get(i, 0) + 1 / (60 + r + 1)
                for r, i in enumerate(bt):
                    score[i] = score.get(i, 0) + 1 / (60 + r + 1)
                fused = [i for i, _ in sorted(score.items(), key=lambda x: -x[1])][:10]
                ids = [corpora[ci]["turns"][i]["dia_id"] for i in fused]
                rr_hits5 += len(set(ev) & set(ids[:5])) > 0
                hits10 += len(set(ev) & set(ids)) > 0
                if ce_q < 200:  # cap CE queries for time
                    t0 = time.time()
                    pairs = [(q["question"], corpora[ci]["turns"][i]["text"]) for i in dtop]
                    sc = ce.predict(pairs, batch_size=32, show_progress_bar=False)
                    ce_lat.append((time.time() - t0) * 1000)
                    ce_top = [dtop[i] for i in np.argsort(-sc)[:5]]
                    cids = [corpora[ci]["turns"][i]["dia_id"] for i in ce_top]
                    ce_q += 1
                    hits5 += len(set(ev) & set(cids)) > 0
        res["rrf_bm25_dense"] = {"recall@5": round(rr_hits5 / tot, 4),
                                 "recall@10": round(hits10 / tot, 4), "n_eval_q": tot}
        res["ce_rerank_dense50"] = {"recall@5": round(hits5 / max(ce_q, 1), 4),
                                    "n_eval_q": ce_q,
                                    "rerank50_ms_mean": round(statistics.mean(ce_lat), 1)}
        print("hybrid+ce", res["rrf_bm25_dense"], res["ce_rerank_dense50"], flush=True)

res["rss_peak_mb"] = round(rss_mb(), 1)
json.dump(res, open(OUT, "w"), indent=2)
print(json.dumps(res, indent=2)[:2000])
