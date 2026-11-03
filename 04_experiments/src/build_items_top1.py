"""C1 — exploratory 'top-1 presented' variant, stage 1: build the items (D3).

    python 04_experiments/src/build_items_top1.py            # write data/items_top1.jsonl
    python 04_experiments/src/build_items_top1.py --no-write  # hit rates only

PREREGISTRATION.md §10 D3 fixes this variant before any of its numbers exist: for every sampled
question (items.jsonl rows with rung == 0, 400 per split) the presented passage is the BM25 rank-1
paragraph retrieved from that split's own pool, and the label is 1 if that paragraph *is* the
question's gold paragraph, 0 otherwise. So the population is retrieval hits and retrieval misses; it
is not a hardness rung and `rung = -1` marks it as outside the ladder.

The pool construction is imported from `features.split_pools()` rather than re-implemented, so a
paragraph can never enter the wrong split's index (dev and test article sets are disjoint).

The hit rate written to features_top1_meta.json is a number the paper cites (it is the label
prevalence of this variant), so it is computed here from the emitted rows, never estimated.
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
SRC = ROOT / "04_experiments" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import features as F  # noqa: E402  (read-only reuse: tokens, load_items, split_pools)

DATA = F.DATA
ITEMS_OUT = DATA / "items_top1.jsonl"
META_OUT = DATA / "features_top1_meta.json"
VARIANT = "top1_presented"
RUNG = -1


def _merge_meta(block: dict) -> dict:
    meta: dict = {}
    if META_OUT.exists():
        meta = json.loads(META_OUT.read_text(encoding="utf-8"))
    meta.update(block)
    META_OUT.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return meta


def build(write: bool = True) -> dict:
    import bm25s

    base = [it for it in F.load_items() if it["rung"] == 0]
    pools = F.split_pools()
    rows: list[dict] = []
    per_split: dict[str, dict] = {}
    timings: dict[str, float] = {}

    for split in ("dev", "test"):
        pool, gold_of = pools[split]
        pool_set = {c: i for i, c in enumerate(pool)}
        questions = [it for it in base if it["split"] == split]
        qids = [it["qid"] for it in questions]

        t0 = time.time()
        ret = bm25s.BM25()
        ret.index(bm25s.tokenize(pool, stopwords="en", show_progress=False), show_progress=False)
        timings[f"{split}_index_s"] = round(time.time() - t0, 2)
        bm25_params = {"k1": float(getattr(ret, "k1", -1)), "b": float(getattr(ret, "b", -1)),
                       "method": getattr(ret, "method", "?")}

        # k = pool size so the gold paragraph's rank is readable for the diagnostic counters; the
        # ordering is identical to a k=1 retrieve (same scores, same tie-breaking).
        t0 = time.time()
        Qt = bm25s.tokenize([it["question"] for it in questions], stopwords="en", show_progress=False)
        b_ids, b_scores = ret.retrieve(Qt, k=len(pool), show_progress=False)
        timings[f"{split}_retrieve_s"] = round(time.time() - t0, 2)

        gold_ranks: list[int] = []
        for k, it in enumerate(questions):
            if it["qid"] not in gold_of:
                raise RuntimeError(f"qid {it['qid']} has no gold paragraph in SQuAD dev")
            order = np.asarray(b_ids[k], dtype=int)
            top_idx = int(order[0])
            top_text = pool[top_idx]
            gold_text = gold_of[it["qid"]]
            is_gold = int(top_text == gold_text)

            # where the gold paragraph sits in the BM25 ranking (diagnostic only, not a feature)
            gold_id = pool_set.get(gold_text)
            if gold_id is None:  # cannot happen for a sampled dev question; fail loudly, don't guess
                raise RuntimeError(f"gold paragraph of {it['qid']} not in the {split} pool")
            gold_ranks.append(int(np.flatnonzero(order == gold_id)[0]) + 1)

            rows.append({
                "item_id": f"{split}:{it['qid']}:top1",
                "split": split, "qid": it["qid"], "title": it["title"],
                "question": it["question"], "context": top_text,
                "rung": RUNG, "variant": VARIANT, "label": is_gold,
                "gold_answer": it["gold_answer"], "n_context_chars": len(top_text),
                "is_gold": is_gold,
            })

        mine = [r for r in rows if r["split"] == split]
        hits = int(sum(r["is_gold"] for r in mine))
        rk = sorted(gold_ranks)
        per_split[split] = {
            "n_questions": len(questions), "n_items": len(mine),
            "n_hits": hits, "n_misses": len(mine) - hits,
            "hit_rate": round(hits / len(mine), 6),
            "gold_rank_median": rk[len(rk) // 2],
            "gold_rank_mean": round(float(np.mean(rk)), 3),
            "gold_rank_leq1": sum(1 for r in rk if r <= 1),
            "gold_rank_leq5": sum(1 for r in rk if r <= 5),
            "gold_rank_leq10": sum(1 for r in rk if r <= 10),
            "bm25_params": bm25_params,
            "pool_size": len(pool),
            "distinct_top1_docs": len({r["context"] for r in mine}),
            "mean_n_context_chars": round(float(np.mean([r["n_context_chars"] for r in mine])), 1),
        }

    block = {
        "variant": VARIANT,
        "label_rule": "label = 1 iff the BM25 rank-1 paragraph text equals the question's gold paragraph",
        "rung": RUNG,
        "bm25": {"library": "bm25s", "stopwords": "en", "k1_b": "library defaults",
                 "k1": per_split["dev"]["bm25_params"]["k1"], "b": per_split["dev"]["bm25_params"]["b"]},
        "items": per_split,
        "items_timings_s": timings,
    }

    if write:
        DATA.mkdir(parents=True, exist_ok=True)
        with open(ITEMS_OUT, "w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
        block["items_sha256"] = hashlib.sha256(ITEMS_OUT.read_bytes()).hexdigest()
        block["n_items_total"] = len(rows)
        _merge_meta(block)
    return block


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the top-1-presented variant items (D3).")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    b = build(write=not a.no_write)
    for s, d in b["items"].items():
        print(f"{s}: n={d['n_items']} hits={d['n_hits']} misses={d['n_misses']} "
              f"hit_rate={d['hit_rate']:.4f} pool={d['pool_size']}", file=sys.stderr)
    print(json.dumps({"items": {s: {k: v for k, v in d.items() if k != "bm25_params"}
                                for s, d in b["items"].items()},
                      "items_sha256": b.get("items_sha256")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
