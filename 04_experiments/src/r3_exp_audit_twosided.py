"""R3 exploratory: two-sided separability audit (MF-7 / MF-13).

Two-sided rule: a rung PASSES when |AUROC - 0.5| <= 0.25 (AUROC in [0.25, 0.75]).
Inverted separation (AUROC < 0.5) is reported as a direction rather than as a
pass under a one-sided rule.

Outputs:
  04_experiments/results/c1/r3/exp/audit_twosided.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
OUT_DIR = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp"
OUT_JSON = OUT_DIR / "audit_twosided.json"

sys.path.insert(0, str(SRC))
import audit as A  # noqa: E402

SEED = 12345
N_BOOT = 2000
COMMAND = "python 04_experiments/src/r3_exp_audit_twosided.py"
GATE = 0.25


def load_items(path: Path = DATA / "items.jsonl") -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_top1_items(path: Path = DATA / "items_top1.jsonl") -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def abs_diff(auroc: float) -> float:
    return float(abs(float(auroc) - 0.5))


def direction(auroc: float) -> str:
    return "inverted" if float(auroc) < 0.5 else "normal"


def twosided_pass(auroc: float, tol: float = GATE) -> bool:
    return bool(abs(float(auroc) - 0.5) <= float(tol))


# aliases
abs_auroc_diff = abs_diff
is_inverted = lambda a: float(a) < 0.5


def oof_scores(X: np.ndarray, y: np.ndarray, seed: int = SEED) -> np.ndarray | None:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    y = np.asarray(y).astype(int)
    X = np.asarray(X, dtype=float)
    n_splits = int(min(5, int(y.sum()), int((y == 0).sum())))
    if n_splits < 2 or len(np.unique(y)) < 2:
        return None
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    oof = np.zeros(len(y), dtype=float)
    for tr, te in skf.split(X, y):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        clf.fit(X[tr], y[tr])
        oof[te] = clf.predict_proba(X[te])[:, 1]
    return oof


def bootstrap_auroc_ci(oof: np.ndarray, y: np.ndarray, seed: int = SEED,
                       n_boot: int = N_BOOT) -> dict:
    from sklearn.metrics import roc_auc_score

    y = np.asarray(y).astype(int)
    oof = np.asarray(oof, dtype=float)
    n = int(len(y))
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(int(n_boot)):
        idx = rng.integers(0, n, n)
        if len(np.unique(y[idx])) < 2:
            continue
        try:
            vals.append(float(roc_auc_score(y[idx], oof[idx])))
        except Exception:
            continue
    vals = np.asarray(vals, dtype=float)
    if vals.size == 0:
        return {"lo": None, "hi": None, "method": "percentile", "n_boot": int(n_boot),
                "n_valid": 0, "seed": int(seed), "n": n}
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return {"lo": round(float(lo), 4), "hi": round(float(hi), 4), "method": "percentile",
            "n_boot": int(n_boot), "n_valid": int(vals.size), "seed": int(seed), "n": n}


def _point_auroc(X, y, seed=SEED):
    oof = oof_scores(X, y, seed)
    if oof is None:
        return None, None
    from sklearn.metrics import roc_auc_score
    try:
        auc = float(roc_auc_score(y, oof))
    except Exception:
        auc = None
    return auc, oof


def _entry_for_rung(pos_items, neg_items, seed=SEED, n_boot=N_BOOT, with_lex=False):
    Xp = A.surface_features(pos_items, with_lex=with_lex)
    Xn = A.surface_features(neg_items, with_lex=with_lex)
    X = np.vstack([Xp, Xn])
    y = np.concatenate([np.zeros(len(pos_items)), np.ones(len(neg_items))]).astype(int)
    auc, oof = _point_auroc(X, y, seed)
    ci = bootstrap_auroc_ci(oof, y, seed=seed, n_boot=n_boot) if oof is not None else None
    return {
        "n": int(len(y)),
        "n_answerable": int(len(pos_items)),
        "n_negatives": int(len(neg_items)),
        "auroc": None if auc is None else round(float(auc), 4),
        "abs_diff": None if auc is None else round(abs(float(auc) - 0.5), 4),
        "direction": None if auc is None else ("inverted" if float(auc) < 0.5 else "normal"),
        "passes": None if auc is None else bool(abs(float(auc) - 0.5) <= GATE),
        "ci": ci,
        "oof_point": None if auc is None else round(float(auc), 4),
    }


def run_original(items, split, seed=SEED, n_boot=N_BOOT):
    sel = [it for it in items if it["split"] == split]
    pos = [it for it in sel if it["rung"] == 0]
    out = {"split": split, "n_answerable": len(pos), "seed": seed, "n_boot": n_boot}
    per_rung = {}
    for r in (1, 2, 3, 4):
        neg = [it for it in sel if it["rung"] == r]
        if not neg:
            continue
        e6 = _entry_for_rung(pos, neg, seed=seed, n_boot=n_boot, with_lex=False)
        el = _entry_for_rung(pos, neg, seed=seed, n_boot=n_boot, with_lex=True)
        # flatten with variant suffixes
        per_rung[str(r)] = {
            "split": split,
            "seed": seed,
            "n": e6["n"],
            "n_answerable": e6["n_answerable"],
            "n_negatives": e6["n_negatives"],
            "auroc_primary_6": e6["auroc"],
            "abs_diff_primary_6": e6["abs_diff"],
            "direction_primary_6": e6["direction"],
            "passes_primary_6": e6["passes"],
            "ci_primary_6": e6["ci"],
            "auroc_with_lex": el["auroc"],
            "abs_diff_with_lex": el["abs_diff"],
            "direction_with_lex": el["direction"],
            "passes_with_lex": el["passes"],
            "ci_with_lex": el["ci"],
            # aliases
            "auroc_primary": e6["auroc"],
            "primary_6": e6["auroc"],
            "with_lex": el["auroc"],
        }
    out["per_rung"] = per_rung
    out["rungs"] = list(per_rung.keys())
    return out


def run_top1(items_top1, split, seed=SEED, n_boot=N_BOOT):
    sel = [it for it in items_top1 if it["split"] == split]
    y = np.array([int(it.get("label", 0)) for it in sel], dtype=int)
    X6 = A.surface_features(sel, with_lex=False)
    Xl = A.surface_features(sel, with_lex=True)
    def _single(X, y):
        auc, oof = _point_auroc(X, y, seed)
        ci = bootstrap_auroc_ci(oof, y, seed=seed, n_boot=n_boot) if oof is not None else None
        return {
            "auroc": None if auc is None else round(float(auc), 4),
            "abs_diff": None if auc is None else round(abs(float(auc) - 0.5), 4),
            "direction": None if auc is None else ("inverted" if float(auc) < 0.5 else "normal"),
            "passes": None if auc is None else bool(abs(float(auc) - 0.5) <= GATE),
            "ci": ci,
        }
    r6 = _single(X6, y)
    rl = _single(Xl, y)
    n_hit = int((y == 1).sum())
    n_miss = int((y == 0).sum())
    return {
        "split": split,
        "seed": seed,
        "n_boot": n_boot,
        "n": int(len(sel)),
        "n_hit": n_hit,
        "n_miss": n_miss,
        "auroc_primary_6": r6["auroc"],
        "abs_diff_primary_6": r6["abs_diff"],
        "direction_primary_6": r6["direction"],
        "passes_primary_6": r6["passes"],
        "ci_primary_6": r6["ci"],
        "auroc_with_lex": rl["auroc"],
        "abs_diff_with_lex": rl["abs_diff"],
        "direction_with_lex": rl["direction"],
        "passes_with_lex": rl["passes"],
        "ci_with_lex": rl["ci"],
    }


def run_gold_control(items, split, seed=SEED, n_boot=N_BOOT):
    sel = [it for it in items if it["split"] == split]
    pos = [it for it in sel if it["rung"] == 0]
    out = {"split": split, "seed": seed, "n_boot": n_boot, "per_rung": {}}
    for r in (1, 2, 3, 4):
        neg = [it for it in sel if it["rung"] == r]
        if not neg:
            continue
        # is_gold binary: 1 for gold (pos), 0 for neg
        is_gold = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
        # surface features + is_gold
        Xp = A.surface_features(pos, with_lex=True)
        Xn = A.surface_features(neg, with_lex=True)
        X = np.vstack([Xp, Xn])
        Xg = np.column_stack([X, is_gold])
        y = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))]).astype(int)
        auc_base, _ = _point_auroc(X, y, seed)
        auc_gold, _ = _point_auroc(Xg, y, seed)
        # is_gold alone
        try:
            from sklearn.metrics import roc_auc_score
            auc_alone = float(roc_auc_score(y, is_gold))
        except Exception:
            auc_alone = None
        out["per_rung"][str(r)] = {
            "split": split,
            "seed": seed,
            "n": int(len(y)),
            "n_answerable": int(len(pos)),
            "n_negatives": int(len(neg)),
            "auroc_with_lex": None if auc_base is None else round(float(auc_base), 4),
            "auroc_with_is_gold": None if auc_gold is None else round(float(auc_gold), 4),
            "auroc_is_gold_alone": None if auc_alone is None else round(float(auc_alone), 4),
            "abs_diff_with_is_gold": None if auc_gold is None else round(abs(float(auc_gold) - 0.5), 4),
            "direction_with_is_gold": None if auc_gold is None else ("inverted" if float(auc_gold) < 0.5 else "normal"),
            "passes_with_is_gold": None if auc_gold is None else bool(abs(float(auc_gold) - 0.5) <= GATE),
        }
    return out


def main() -> None:
    items = load_items()
    top1 = load_top1_items()

    original = {}
    for split in ("dev", "test"):
        original[split] = run_original(items, split, seed=SEED, n_boot=N_BOOT)

    top1_out = {}
    for split in ("dev", "test"):
        top1_out[split] = run_top1(top1, split, seed=SEED, n_boot=N_BOOT)

    gold_out = {}
    for split in ("dev", "test"):
        gold_out[split] = run_gold_control(items, split, seed=SEED, n_boot=N_BOOT)

    result = {
        "generated_by": "04_experiments/src/r3_exp_audit_twosided.py",
        "command": COMMAND,
        "seed": SEED,
        "n_boot": N_BOOT,
        "threshold": GATE,
        "pass_rule": "|AUROC - 0.5| <= 0.25",
        "exploratory_post_hoc": True,
        "n": len(items),
        "n_top1": len(top1),
        "splits": ["dev", "test"],
        "rungs": [1, 2, 3, 4],
        "original": original,
        "top1": top1_out,
        "gold_indicator_control": gold_out,
        # aliases
        "twosided_audit": original,
        "audit": original,
        "top1_presented": top1_out,
        "gold_control": gold_out,
        "dev": original["dev"],
        "test": original["test"],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(OUT_JSON), "seed": SEED, "n_boot": N_BOOT}, indent=2))


if __name__ == "__main__":
    main()
