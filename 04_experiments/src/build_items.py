"""C1 — stage 1: article split, question sampling, and the four negative rungs.

Reads only `04_experiments/data/raw/dev-v2.0.json` (SQuAD 2.0 dev, CC BY-SA 4.0) and writes
`04_experiments/data/items.jsonl` + `04_experiments/data/item_stats.json`.

Every rung definition is the one frozen in 04_experiments/PREREGISTRATION.md §3. RNGs are seeded from
`f"{DATA_SEED}:{qid}:{rung}"` so a single item is reproducible without replaying the whole file.

Nothing here is a result: it builds the item set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "04_experiments" / "data" / "raw" / "dev-v2.0.json"
OUT_DIR = ROOT / "04_experiments" / "data"

DATA_SEED = 20261103
SPLIT_SEED = 7
N_ANSWERABLE_PER_SPLIT = 400
RUNGS = (0, 1, 2, 3, 4)

STOP = set(
    """a an the of in on at to for from by with without into onto over under about above below
    and or but if then than that this these those there here it its is are was were be been being
    do does did done have has had having not no nor so such as which who whom whose what when where
    why how many much more most other some any each both few several own same too very can could
    will would shall should may might must i you he she they we them him her his their our your my
    me us also according used using""".split()
)

MONTHS = set(
    """january february march april may june july august september october november december
    jan feb mar apr jun jul aug sep sept oct nov dec""".split()
)


def norm_tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower())]


def content_tokens(text: str) -> list[str]:
    return [t for t in norm_tokens(text) if t not in STOP and len(t) > 1]


def answer_type(value: str) -> str:
    v = value.strip()
    low = v.lower().strip(".,;:")
    if low in MONTHS or any(m in low.split() for m in MONTHS):
        return "date"
    if re.fullmatch(r"1[0-9]{3}|20[0-9]{2}", low):
        return "year"
    if re.fullmatch(r"[\d][\d,\.]*", low) or re.search(r"\d", low):
        return "number"
    if v[:1].isupper() and re.fullmatch(r"[A-Za-z][A-Za-z'’\.\- ]*", v):
        return "name"
    return "other"


def load_squad(path: Path = RAW) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))["data"]
    return [
        {"title": a["title"], "paragraphs": [p["context"] for p in a["paragraphs"]],
         "paras": a["paragraphs"]}
        for a in data
    ]


def split_articles(articles: list[dict], seed: int = SPLIT_SEED) -> dict[str, list[dict]]:
    titles = sorted(a["title"] for a in articles)
    rng = random.Random(seed)
    rng.shuffle(titles)
    n_dev = 17
    dev_t = set(titles[:n_dev])
    by_title = {a["title"]: a for a in articles}
    return {
        "dev": [by_title[t] for t in titles if t in dev_t],
        "test": [by_title[t] for t in titles if t not in dev_t],
    }


def idf_table(paragraphs: list[str]) -> dict[str, float]:
    df: Counter[str] = Counter()
    for p in paragraphs:
        df.update(set(content_tokens(p)))
    n = max(1, len(paragraphs))
    return {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}


def pick_questions(articles: list[dict], n: int) -> list[dict]:
    pool = []
    for a in articles:
        for pi, p in enumerate(a["paras"]):
            for q in p["qas"]:
                if q["is_impossible"] or not q["answers"]:
                    continue
                pool.append({"qid": q["id"], "question": q["question"], "title": a["title"],
                             "para_idx": pi, "gold": p["context"],
                             "answers": [x["text"] for x in q["answers"]],
                             "answer_starts": [x["answer_start"] for x in q["answers"]]})
    pool.sort(key=lambda x: x["qid"])
    rng = random.Random(f"{DATA_SEED}:sample:{n}")
    return rng.sample(pool, min(n, len(pool)))


def make_rungs(item: dict, article: dict, pool: list[str], idf: dict[str, float]) -> list[dict]:
    rng1 = random.Random(f"{DATA_SEED}:{item['qid']}:1")
    rng3 = random.Random(f"{DATA_SEED}:{item['qid']}:3")
    rng4 = random.Random(f"{DATA_SEED}:{item['qid']}:4")
    gold = item["gold"]
    out = []

    # rung 0 — answerable, gold paragraph presented
    out.append({"rung": 0, "label": 1, "context": gold, "dropped": None})

    # rung 1 — random paragraph, never the gold one
    others = [p for p in pool if p != gold]
    out.append({"rung": 1, "label": 0, "context": rng1.choice(others), "dropped": None})

    # rung 2 — a paragraph sharing the question's highest-IDF content token
    toks = [t for t in content_tokens(item["question"]) if t in idf]
    if toks:
        anchor = max(toks, key=lambda t: (idf[t], t))
        cands = [p for p in pool if p != gold and anchor in set(norm_tokens(p))]
    else:
        anchor, cands = None, []
    if cands:
        out.append({"rung": 2, "label": 0, "context": rng1.choice(cands), "dropped": None,
                    "anchor": anchor, "n_candidates": len(cands)})
    else:
        out.append({"rung": 2, "label": 0, "context": None, "dropped": "no_anchor_candidate"})

    # rung 3 — contiguous near-miss inside the same article
    paras = article["paragraphs"]
    idxs = [i for i, p in enumerate(paras) if p == gold]
    if idxs:
        pi = idxs[0]
        order = [pi - 1, pi + 1] if rng3.random() < 0.5 else [pi + 1, pi - 1]
        side = [paras[j] for j in order if 0 <= j < len(paras) and paras[j] != gold]
        if side:
            out.append({"rung": 3, "label": 0, "context": side[0], "dropped": None})
        else:
            out.append({"rung": 3, "label": 0, "context": None, "dropped": "single_paragraph_article"})
    else:
        out.append({"rung": 3, "label": 0, "context": None, "dropped": "gold_not_found_in_article"})

    # rung 4 — premise violation: gold paragraph with the first answer span swapped for a
    # same-surface-type value drawn from another answer span in the same article
    cands_by_type: dict[str, list[str]] = {}
    for p in article["paras"]:
        for q in p["qas"]:
            for a in q["answers"]:
                v = a["text"].strip()
                if not v or v == item["answers"][0]:
                    continue
                cands_by_type.setdefault(answer_type(v), []).append(v)
    start = item["answer_starts"][0]
    gold_ans = item["answers"][0]
    rendered = None
    repl = None
    if 0 <= start < len(gold) and gold[start:start + len(gold_ans)].lower() == gold_ans.lower():
        t = answer_type(gold_ans)
        pool_vals = sorted(set(cands_by_type.get(t, [])))
        if pool_vals:
            repl = rng4.choice(pool_vals)
            if repl.lower() != gold_ans.lower():
                rendered = gold[:start] + repl + gold[start + len(gold_ans):]
    if rendered:
        out.append({"rung": 4, "label": 0, "context": rendered, "dropped": None,
                    "replacement": repl, "answer_type": answer_type(gold_ans)})
    else:
        out.append({"rung": 4, "label": 0, "context": None, "dropped": "no_same_type_replacement"})
    return out


def build(verbose: bool = True) -> dict:
    articles = load_squad()
    splits = split_articles(articles)
    items, stats = [], {"per_split": {}, "generated_by": "04_experiments/src/build_items.py",
                        "data_seed": DATA_SEED, "split_seed": SPLIT_SEED}
    for name, arts in splits.items():
        pool = [p for a in arts for p in a["paragraphs"]]
        idf = idf_table(pool)
        qs = pick_questions(arts, N_ANSWERABLE_PER_SPLIT)
        per_rung = Counter()
        drops = Counter()
        for it in qs:
            art = next(a for a in arts if a["title"] == it["title"])
            for r in make_rungs(it, art, pool, idf):
                if r["context"] is None:
                    drops[f"rung{r['rung']}:{r['dropped']}"] += 1
                    continue
                items.append({
                    "item_id": f"{name}:{it['qid']}:r{r['rung']}",
                    "split": name, "qid": it["qid"], "title": it["title"], "rung": r["rung"],
                    "label": r["label"], "question": it["question"], "context": r["context"],
                    "gold_answer": it["answers"][0] if r["rung"] in (0, 4) else None,
                    "n_context_chars": len(r["context"]),
                    "anchor_token": r.get("anchor"), "replacement": r.get("replacement"),
                })
                per_rung[r["rung"]] += 1
        stats["per_split"][name] = {
            "n_articles": len(arts), "n_paragraphs": len(pool),
            "n_answerable_available": sum(1 for a in arts for p in a["paras"] for q in p["qas"]
                                          if not q["is_impossible"]),
            "n_questions_sampled": len(qs),
            "items_per_rung": {str(k): per_rung[k] for k in sorted(per_rung)},
            "n_items": sum(per_rung.values()),
            "drops": dict(sorted(drops.items())),
        }
        if verbose:
            print(name, stats["per_split"][name], file=sys.stderr)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items.sort(key=lambda x: (x["split"], x["qid"], x["rung"]))
    with open(OUT_DIR / "items.jsonl", "w", encoding="utf-8", newline="\n") as fh:
        for it in items:
            fh.write(json.dumps(it, sort_keys=True, ensure_ascii=False) + "\n")
    blob = (OUT_DIR / "items.jsonl").read_bytes()
    stats.update({"n_items_total": len(items), "sha256_items_jsonl": hashlib.sha256(blob).hexdigest(),
                  "inputs": {"dev_v2.0.json": hashlib.sha256(RAW.read_bytes()).hexdigest()},
                  "length_chars": {}})
    for r in RUNGS:
        vals = [it["n_context_chars"] for it in items if it["rung"] == r]
        stats["length_chars"][str(r)] = {
            "n": len(vals),
            "median": round(statistics.median(vals), 1) if vals else None,
            "mean": round(statistics.fmean(vals), 1) if vals else None,
            "min": min(vals) if vals else None, "max": max(vals) if vals else None,
        }
    (OUT_DIR / "item_stats.json").write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n",
                                             encoding="utf-8")
    return stats


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the C1 negative-hardness ladder items.")
    ap.add_argument("--json", action="store_true", help="print the stats JSON to stdout")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    s = build(verbose=not a.quiet)
    if a.json:
        print(json.dumps(s, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
