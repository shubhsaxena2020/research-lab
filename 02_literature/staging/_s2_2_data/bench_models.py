"""S2-2 part 2: embedding-model and reranker cost on the target CPU laptop."""
import json, os, time, statistics, psutil
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

D = os.path.dirname(os.path.abspath(__file__))
conv = json.load(open(os.path.join(D, "locomo10.json"), encoding="utf-8"))
texts = []
for c in conv[:3]:
    for k, v in c["conversation"].items():
        if k.startswith("session_") and isinstance(v, list) and not k.endswith("date_time"):
            texts += [t.get("text", "") for t in v]
texts = texts[:1500]
queries = [q["question"] for c in conv[:3] for q in c["qa"]][:40]
print("n_texts", len(texts), "n_queries", len(queries), flush=True)

out = {}
for name in ["intfloat/e5-small-v2", "thenlper/gte-small"]:
    try:
        t0 = time.time(); m = SentenceTransformer(name, device="cpu"); load = time.time() - t0
        t0 = time.time()
        m.encode(texts, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
        enc = time.time() - t0
        out[name] = {"params_m": round(sum(p.numel() for p in m.parameters()) / 1e6, 1),
                     "dim": int(m.get_sentence_embedding_dimension()),
                     "load_s": round(load, 1), "texts_per_s": round(len(texts) / enc, 1),
                     "rss_mb": round(psutil.Process().memory_info().rss / 2**20, 1)}
        print(name, out[name], flush=True)
    except Exception as e:
        out[name] = {"error": str(e)[:200]}
        print("ERR", name, e, flush=True)

for name in ["cross-encoder/ms-marco-MiniLM-L-12-v2"]:
    try:
        t0 = time.time(); ce = CrossEncoder(name, device="cpu", max_length=256); load = time.time() - t0
        lat = []
        for q in queries[:20]:
            pairs = [(q, t) for t in texts[:20]]
            t0 = time.time(); ce.predict(pairs, batch_size=16, show_progress_bar=False)
            lat.append((time.time() - t0) * 1000)
        out[name] = {"params_m": round(sum(p.numel() for p in ce.model.parameters()) / 1e6, 1),
                     "load_s": round(load, 1), "rerank20_ms_mean": round(statistics.mean(lat), 1),
                     "per_pair_ms": round(statistics.mean(lat) / 20, 2),
                     "rss_mb": round(psutil.Process().memory_info().rss / 2**20, 1)}
        print(name, out[name], flush=True)
    except Exception as e:
        out[name] = {"error": str(e)[:200]}
        print("ERR", name, e, flush=True)

json.dump(out, open(os.path.join(D, "s2_2_cpu_models.json"), "w"), indent=2)
