"""C1 — EXPLORATORY rung 5 (overlap-matched negatives), PREREGISTRATION.md §10 D2.

For each sampled answerable question (the rung-0 rows of `data/items.jsonl`), compute

    lex_overlap(p) = |set(tokens(q)) & set(tokens(p))| / |set(tokens(q))|
    tokens(text)   = re.findall("[a-z0-9]+", text.lower())

for every paragraph `p` of that split's pool (built exactly as `features.split_pools()` builds it) and
for the gold paragraph, then choose the candidate `p != P_gold` whose `lex_overlap` is closest to
`lex_overlap(P_gold)` in absolute value. Candidates tied within 1e-12 are broken with
`random.Random("20261103:<qid>:5")`.

Writes `04_experiments/data/items_rung5.jsonl`. One row per question per split (400 + 400), keys =
the `items.jsonl` key set plus `overlap_target`, `overlap_chosen`, `overlap_absdiff`.

This builds items only; it produces no result. Rung 5 is exploratory (D2) and is never part of H1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import features as F  # noqa: E402  (import only; never modified)

DATA = ROOT / "04_experiments" / "data"
OUT = DATA / "items_rung5.jsonl"

DATA_SEED = 20261103
RUNG = 5
TIE_EPS = 1e-12


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def lex_overlap(qset: set[str], text: str) -> float:
    return len(qset & set(tokens(text))) / max(1, len(qset))


def build(verbose: bool = True) -> dict:
    items = F.load_items()
    pools = F.split_pools()  # split -> (pool paragraphs, qid -> gold paragraph)
    rung0 = [it for it in items if it["rung"] == 0]
    rows: list[dict] = []
    for split in ("dev", "test"):
        pool, gold_of = pools[split]
        qs = [it for it in rung0 if it["split"] == split]
        for it in qs:
            qset = set(tokens(it["question"]))
            gold = gold_of[it["qid"]]
            target = lex_overlap(qset, gold)
            best: list[tuple[float, str]] = []
            best_diff = None
            for p in pool:
                if p == gold:
                    continue
                d = abs(lex_overlap(qset, p) - target)
                if best_diff is None or d < best_diff - TIE_EPS:
                    best_diff, best = d, [(d, p)]
                elif abs(d - best_diff) <= TIE_EPS:
                    best.append((d, p))
            if not best:
                raise RuntimeError(f"no candidate for {split}:{it['qid']}")
            rng = random.Random(f"{DATA_SEED}:{it['qid']}:{RUNG}")
            chosen = rng.choice([p for _, p in best])
            chosen_diff = abs(lex_overlap(qset, chosen) - target)
            rows.append({
                "item_id": f"{split}:{it['qid']}:r5",
                "split": split, "qid": it["qid"], "title": it["title"], "rung": RUNG,
                "label": 0, "question": it["question"], "context": chosen,
                "gold_answer": None, "n_context_chars": len(chosen),
                "anchor_token": None, "replacement": None,
                "overlap_target": target, "overlap_chosen": lex_overlap(qset, chosen),
                "overlap_absdiff": chosen_diff,
                "_n_tied": len(best),
            })
    rows.sort(key=lambda r: (r["split"], r["qid"]))
    n_tied = [r.pop("_n_tied") for r in rows]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    blob = OUT.read_bytes()
    sha = hashlib.sha256(blob).hexdigest()

    summary = {"path": str(OUT.relative_to(ROOT)), "n_rows": len(rows), "sha256": sha,
               "per_split": {}}
    for split in ("dev", "test"):
        vals = [r["overlap_absdiff"] for r in rows if r["split"] == split]
        summary["per_split"][split] = {
            "n": len(vals),
            "mean_overlap_absdiff": statistics.fmean(vals),
            "median_overlap_absdiff": statistics.median(vals),
            "max_overlap_absdiff": max(vals),
            "n_exact_ties_resolved_randomly": sum(1 for r, t in zip(rows, n_tied)
                                                 if r["split"] == split and t > 1),
        }
    if verbose:
        print(json.dumps(summary, indent=2, sort_keys=True), file=sys.stderr)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Build C1 exploratory rung 5 (D2).")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    s = build(verbose=not a.quiet)
    if a.json:
        print(json.dumps(s, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
