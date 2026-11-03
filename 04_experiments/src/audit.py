"""C1 — stage 2: surface-only separability audit (the hard gate in PREREGISTRATION.md §8a).

Question the audit answers: can a classifier that sees **only surface properties of the text** tell a
rung-k negative from an answerable item? If yes (AUROC > 0.75), the rung is not measuring hardness, it is
measuring formatting, and it must be rebuilt (§8a) or the run stops (§8b).

Two surface variants are reported:

* ``primary_6`` — the six features PREREGISTRATION.md §1 names: characters, tokens, digit ratio,
  upper-case ratio, punctuation ratio, mean word length. This variant decides pass/fail.
* ``with_lex_overlap`` — the same six plus question-passage token Jaccard and question length. Reported
  as a sensitivity analysis only, because lexical overlap between question and passage is the retrieval
  signal the gate itself uses (§4 lists ``lex_overlap`` as a *gate* feature, not a surface one); calling
  it "surface" would measure whether retrieval works, not whether a rung leaks its identity through
  formatting.

`length_match` implements the §8a rebuild: keep negatives whose passage length matches the answerable
length distribution, decile by decile (±10% of the decile median).
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

import numpy as np

SURFACE_6 = ["n_chars", "n_tokens", "digit_ratio", "upper_ratio", "punct_ratio", "mean_word_len"]
SURFACE_LEX = ["lex_jaccard", "q_len"]
AUROC_GATE = 0.75
MAX_REBUILDS = 2


def surface_features(items: list[dict], with_lex: bool = True) -> np.ndarray:
    out = []
    for it in items:
        ctx, q = it["context"], it["question"]
        toks = re.findall(r"\S+", ctx)
        qt = re.findall(r"[a-z0-9]+", q.lower())
        pt = re.findall(r"[a-z0-9]+", ctx.lower())
        row = [
            len(ctx),
            len(toks),
            sum(c.isdigit() for c in ctx) / max(1, len(ctx)),
            sum(c.isupper() for c in ctx) / max(1, len(ctx)),
            sum(not c.isalnum() and not c.isspace() for c in ctx) / max(1, len(ctx)),
            float(np.mean([len(t) for t in toks])) if toks else 0.0,
        ]
        if with_lex:
            row += [len(set(qt) & set(pt)) / max(1, len(set(qt))), len(q)]
        out.append(row)
    return np.asarray(out, dtype=float)


def _cv_auroc(X: np.ndarray, y: np.ndarray, seed: int) -> float:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    n_splits = int(min(5, y.sum(), (y == 0).sum()))
    if n_splits < 2:
        return float("nan")
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    oof = np.zeros(len(y), dtype=float)
    for tr, te in skf.split(X, y):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        clf.fit(X[tr], y[tr])
        oof[te] = clf.predict_proba(X[te])[:, 1]
    if y.min() == y.max():
        return float("nan")
    return float(roc_auc_score(y, oof))


def audit(items: list[dict], split: str = "dev", seed: int = 13,
          rebuilt: dict[int, int] | None = None) -> dict:
    """Per-rung surface separability. `rebuilt` maps rung -> rebuild passes already applied."""
    rebuilt = rebuilt or {}
    sel = [it for it in items if it["split"] == split]
    pos = [it for it in sel if it["rung"] == 0]
    Xp6 = surface_features(pos, with_lex=False)
    Xpl = surface_features(pos, with_lex=True)
    res = {"split": split, "gate_auroc": AUROC_GATE, "per_rung": {},
           "rebuilt_rungs": {str(k): v for k, v in rebuilt.items()},
           "n_answerable": len(pos), "primary_features": SURFACE_6,
           "sensitivity_features": SURFACE_6 + SURFACE_LEX}
    for r in (1, 2, 3, 4):
        neg = [it for it in sel if it["rung"] == r]
        if not neg:
            continue
        y = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))])
        auc6 = _cv_auroc(np.vstack([Xp6, surface_features(neg, with_lex=False)]), y, seed)
        aucl = _cv_auroc(np.vstack([Xpl, surface_features(neg, with_lex=True)]), y, seed)
        res["per_rung"][str(r)] = {
            "auroc_primary_6": round(auc6, 4),
            "auroc_with_lex_overlap": round(aucl, 4),
            "passes": bool(auc6 <= AUROC_GATE),
            "n_negatives": len(neg),
            "n_answerable": len(pos),
            "length_chars_neg_median": round(statistics.median(len(i["context"]) for i in neg), 1),
            "length_chars_pos_median": round(statistics.median(len(i["context"]) for i in pos), 1),
            "rebuilds_applied": int(rebuilt.get(r, 0)),
        }
    res["failing_rungs"] = [int(k) for k, v in res["per_rung"].items() if not v["passes"]]
    res["all_pass"] = not res["failing_rungs"]
    return res


def length_match(neg: list[dict], pos: list[dict], seed: int = 13) -> list[dict]:
    """§8a rebuild: keep negatives matching the answerable length distribution, decile by decile."""
    import random

    rng = random.Random(seed)
    plen = np.array([len(p["context"]) for p in pos], dtype=float)
    edges = np.percentile(plen, np.arange(0, 101, 10))
    keep: list[dict] = []
    for i in range(10):
        lo, hi = edges[i], edges[i + 1]
        bucket_pos = [p for p in pos if lo <= len(p["context"]) <= hi]
        if not bucket_pos:
            continue
        med = statistics.median(len(p["context"]) for p in bucket_pos)
        cands = [n for n in neg if abs(len(n["context"]) - med) <= 0.10 * med]
        rng.shuffle(cands)
        keep.extend(cands[:len(bucket_pos)])
    keep.sort(key=lambda x: x["item_id"])
    return keep


def audit_with_rebuild(items: list[dict], split: str = "dev", seed: int = 13) -> tuple[dict, dict]:
    """Audit; rebuild failing rungs up to MAX_REBUILDS times each; audit again.

    Returns (report, kept_ids_by_rung). A rung that still fails after MAX_REBUILDS is reported as
    contaminated; §8b (stop and fall back to C3) applies to the run as a whole.
    """
    report = audit(items, split=split, seed=seed)
    working = list(items)
    rebuilt_counts: dict[int, int] = {}
    for r in list(report["failing_rungs"]):
        for attempt in range(MAX_REBUILDS):
            sel = [it for it in working if it["split"] == split]
            pos = [it for it in sel if it["rung"] == 0]
            neg = [it for it in sel if it["rung"] == r]
            keep_ids = {n["item_id"] for n in length_match(neg, pos, seed=seed + attempt)}
            working = [it for it in working
                       if it["split"] != split or it["rung"] != r or it["item_id"] in keep_ids]
            rebuilt_counts[r] = attempt + 1
            report = audit(working, split=split, seed=seed, rebuilt=rebuilt_counts)
            if report["per_rung"][str(r)]["passes"]:
                break
    kept = {0: [it["item_id"] for it in working if it["split"] == split and it["rung"] == 0]}
    for rr in (1, 2, 3, 4):
        kept[rr] = [it["item_id"] for it in working if it["split"] == split and it["rung"] == rr]
    report["kept_counts"] = {str(k): len(v) for k, v in sorted(kept.items())}
    return report, kept


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Surface-only separability audit for C1 rungs.")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--with-rebuild", action="store_true")
    a = ap.parse_args()
    items = [json.loads(l) for l in
             open(Path(__file__).resolve().parents[2] / "04_experiments" / "data" / "items.jsonl",
                  encoding="utf-8") if l.strip()]
    if a.with_rebuild:
        rep, kept = audit_with_rebuild(items, split=a.split)
        print(json.dumps(rep, indent=2, sort_keys=True))
        print(json.dumps({str(k): len(v) for k, v in sorted(kept.items())}))
    else:
        print(json.dumps(audit(items, split=a.split), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
