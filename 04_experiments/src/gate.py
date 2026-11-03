"""C1 — stage 4: gates, dev-fitted thresholds, held-out evaluation, statistics.

Implements PREREGISTRATION.md §5-§8.

Integrity rules encoded here, not just documented:

* the logistic gate and every threshold are fitted on the dev half only;
* the single threshold that H3 compares against is chosen so that **dev** abstain recall matches the
  band's dev abstain recall — matching on test would be test-set tuning;
* all intervals are item-level bootstrap CIs with the frozen `BOOT_SEED`, and all comparisons are paired
  by item;
* nothing is computed from the test half except the reported evaluation numbers.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
HARNESS = ROOT / "04_experiments" / "harness"

GATE_FEATURES = ["bm25_presented", "bm25_rank_log", "bm25_top1", "bm25_top5_mean", "bm25_margin",
                 "dense_presented", "dense_rank_log", "dense_top1", "dense_margin",
                 "top1_agreement", "ce_presented", "lex_overlap"]
READER_FEATURE = "reader_mean_logprob"
TARGET_PRECISION = 0.80
N_BOOT = 10000
BOOT_SEED = 12345


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #
def load_items() -> list[dict]:
    with open(DATA / "items.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_features(path: Path | None = None) -> dict[str, dict]:
    path = path or DATA / "features.csv"
    out: dict[str, dict] = {}
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            rec = {"item_id": row["item_id"], "split": row["split"], "rung": int(row["rung"]),
                   "label": int(row["label"])}
            for c in GATE_FEATURES:
                rec[c] = float(row[c])
            out[row["item_id"]] = rec
    return out


def load_reader(path: Path | None = None) -> dict[str, float]:
    path = path or DATA / "reader_features.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["item_id"]: float(r[READER_FEATURE]) for r in csv.DictReader(fh)
                if r.get(READER_FEATURE) not in ("", "nan", "None", None)}


# --------------------------------------------------------------------------- #
# the logistic gate
# --------------------------------------------------------------------------- #
class LogisticGate:
    """Logistic gate on standardised retrieval features, fitted on dev only."""

    def __init__(self, clf, mu, sd, features=GATE_FEATURES):
        self.clf, self.mu, self.sd, self.features = clf, mu, sd, list(features)

    def score(self, feats: dict[str, dict], ids: list[str]) -> np.ndarray:
        X = np.asarray([[feats[i][c] for c in self.features] for i in ids], dtype=float)
        return self.clf.predict_proba((X - self.mu) / self.sd)[:, 1]

    def info(self) -> dict:
        return {"coef": {c: round(float(w), 4) for c, w in zip(self.features, self.clf.coef_[0])},
                "intercept": round(float(self.clf.intercept_[0]), 4),
                "feature_sds": {c: round(float(s), 4) for c, s in zip(self.features, self.sd)}}


def fit_logistic_gate(feats: dict[str, dict], ids: list[str], features=None) -> LogisticGate:
    from sklearn.linear_model import LogisticRegression

    features = list(features or GATE_FEATURES)
    X = np.asarray([[feats[i][c] for c in features] for i in ids], dtype=float)
    y = np.asarray([feats[i]["label"] for i in ids], dtype=int)
    mu, sd = X.mean(0), X.std(0)
    sd = np.where(sd == 0, 1.0, sd)
    clf = LogisticRegression(C=1.0, max_iter=1000, solver="lbfgs", class_weight=None)
    clf.fit((X - mu) / sd, y)
    return LogisticGate(clf, mu, sd, features)


# --------------------------------------------------------------------------- #
# thresholds (dev only)
# --------------------------------------------------------------------------- #
def _grid(values: np.ndarray) -> np.ndarray:
    return np.unique(np.round(np.percentile(values, np.arange(1, 100)), 12))


def _prec_rec(refused: np.ndarray, y: np.ndarray) -> tuple[float, float, int]:
    n_ref = int(refused.sum())
    if n_ref == 0:
        return 0.0, 0.0, 0
    tp = int(refused[y == 0].sum())
    return tp / n_ref, tp / max(1, int((y == 0).sum())), n_ref


def fit_single_threshold(score: np.ndarray, y: np.ndarray) -> dict:
    """Maximise abstain recall s.t. dev abstain precision >= TARGET; tie-break higher threshold."""
    best = None
    for t in _grid(score):
        prec, rec, n_ref = _prec_rec(score < t, y)
        if n_ref == 0:
            continue
        key = (prec >= TARGET_PRECISION, rec, float(t))
        if best is None or key > best[0]:
            best = (key, float(t), prec, rec, n_ref)
    if best is None:
        return {"t": float("nan"), "feasible": False, "dev_precision": float("nan"),
                "dev_recall": float("nan"), "dev_n_refused": 0}
    return {"t": best[1], "feasible": bool(best[0][0]), "dev_precision": round(best[2], 4),
            "dev_recall": round(best[3], 4), "dev_n_refused": best[4]}


def fit_band_thresholds(score: np.ndarray, y: np.ndarray) -> dict:
    """Maximise abstain recall s.t. dev abstain precision >= TARGET; tie-break the wider band."""
    grid = _grid(score)
    best = None
    for i, lo in enumerate(grid):
        for hi in grid[i:]:
            prec, rec, n_ref = _prec_rec((score < lo) | (score > hi), y)
            if n_ref == 0:
                continue
            key = (prec >= TARGET_PRECISION, rec, float(hi - lo))
            if best is None or key > best[0]:
                best = (key, float(lo), float(hi), prec, rec, n_ref)
    if best is None:
        return {"t_lo": float("nan"), "t_hi": float("nan"), "feasible": False,
                "dev_precision": float("nan"), "dev_recall": float("nan"), "dev_n_refused": 0}
    return {"t_lo": best[1], "t_hi": best[2], "feasible": bool(best[0][0]),
            "dev_precision": round(best[3], 4), "dev_recall": round(best[4], 4),
            "dev_n_refused": best[5], "band_width": round(best[2] - best[1], 6)}


def match_single_to_recall(score: np.ndarray, y: np.ndarray, target_recall: float) -> dict:
    """Single threshold whose dev abstain recall is closest to `target_recall` (used by H3)."""
    best = None
    for t in _grid(score):
        prec, rec, n_ref = _prec_rec(score < t, y)
        if n_ref == 0:
            continue
        key = (abs(rec - target_recall), float(t))
        if best is None or key < best[0]:
            best = (key, float(t), prec, rec, n_ref)
    if best is None:
        return {"t": float("nan")}
    return {"t": best[1], "dev_precision": round(best[2], 4), "dev_recall": round(best[3], 4),
            "dev_n_refused": best[4]}


def fit_single_constrained(score: np.ndarray, y: np.ndarray, max_over_refusal: float) -> dict:
    """Exploratory: max dev abstain recall s.t. precision >= TARGET *and* dev over-refusal <= cap.

    Added after the confirmatory thresholds turned out degenerate (they refuse ~94% of items). It is
    labelled exploratory everywhere it is reported, it never replaces the pre-registered gate, and the
    constraint is recorded in PREREGISTRATION.md §10 before any of its numbers are written down.
    """
    best = None
    pos = y == 1
    for t in _grid(score):
        refused = score < t
        prec, rec, n_ref = _prec_rec(refused, y)
        if n_ref == 0:
            continue
        over = float(refused[pos].mean())
        key = (over <= max_over_refusal, prec >= TARGET_PRECISION, rec, float(t))
        if best is None or key > best[0]:
            best = (key, float(t), prec, rec, n_ref, over)
    if best is None:
        return {"t": float("nan"), "feasible": False}
    return {"t": best[1], "feasible": bool(best[0][0] and best[0][1]),
            "dev_precision": round(best[2], 4), "dev_recall": round(best[3], 4),
            "dev_n_refused": best[4], "dev_over_refusal": round(best[5], 4),
            "max_over_refusal": max_over_refusal}


def fit_band_constrained(score: np.ndarray, y: np.ndarray, max_over_refusal: float) -> dict:
    """Exploratory band version of `fit_single_constrained` (same constraint, wider region)."""
    grid = _grid(score)
    pos = y == 1
    best = None
    for i, lo in enumerate(grid):
        for hi in grid[i:]:
            refused = (score < lo) | (score > hi)
            prec, rec, n_ref = _prec_rec(refused, y)
            if n_ref == 0:
                continue
            over = float(refused[pos].mean())
            key = (over <= max_over_refusal, prec >= TARGET_PRECISION, rec, float(hi - lo))
            if best is None or key > best[0]:
                best = (key, float(lo), float(hi), prec, rec, n_ref, over)
    if best is None:
        return {"t_lo": float("nan"), "t_hi": float("nan"), "feasible": False}
    return {"t_lo": best[1], "t_hi": best[2], "feasible": bool(best[0][0] and best[0][1]),
            "dev_precision": round(best[3], 4), "dev_recall": round(best[4], 4),
            "dev_n_refused": best[5], "dev_over_refusal": round(best[6], 4),
            "max_over_refusal": max_over_refusal}


def refused_band(s: np.ndarray, t_lo: float, t_hi: float) -> np.ndarray:
    return (s < t_lo) | (s > t_hi)


def refused_single(s: np.ndarray, t: float) -> np.ndarray:
    return s < t


# --------------------------------------------------------------------------- #
# statistics
# --------------------------------------------------------------------------- #
def _stats():
    import sys

    if str(HARNESS) not in sys.path:
        sys.path.insert(0, str(HARNESS))
    import stats  # noqa: E402  (04_experiments/harness/stats.py)
    return stats


def ci_mean(values, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    st = _stats()
    x = np.asarray(values, dtype=float)
    if x.size < 2:
        return {"lo": None, "hi": None, "n": int(x.size)}
    r = st.bootstrap_ci(x, statistic=np.mean, n_boot=n_boot, seed=seed, method="bca")
    return {"lo": round(float(r["lo"]), 4), "hi": round(float(r["hi"]), 4),
            "method": r.get("method"), "n_boot": n_boot, "seed": seed, "n": int(x.size)}


def boot_precision_diff(ref_a: np.ndarray, ref_b: np.ndarray, negative_mask: np.ndarray,
                        n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """Paired item-level bootstrap of precision(A) - precision(B) over the same negative items.

    Precision here is the mean refusal indicator over negatives, so the difference is a difference of
    two means on the same resampled items — the pairing is preserved by construction.
    """
    rng = np.random.default_rng(seed)
    a = np.asarray(ref_a, dtype=float)[negative_mask]
    b = np.asarray(ref_b, dtype=float)[negative_mask]
    n = a.size
    if n == 0:
        return {"diff": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}
    obs = float(a.mean() - b.mean())
    draws = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        draws[i] = a[idx].mean() - b[idx].mean()
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return {"diff": round(obs, 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "n": int(n), "n_boot": n_boot, "seed": seed,
            "method": "paired percentile bootstrap over negative items",
            "contains_zero": bool(lo <= 0 <= hi)}


def paired_sign(ref_a: np.ndarray, ref_b: np.ndarray, mask: np.ndarray) -> dict:
    st = _stats()
    a, b = np.asarray(ref_a, float)[mask], np.asarray(ref_b, float)[mask]
    if a.size == 0:
        return {"test": "sign", "p_value": None, "n_pairs": 0}
    r = st.sign_test(a, b, alpha=0.05)
    p = r.get("p_value")
    return {"test": r.get("test", "sign_exact"), "statistic": r.get("statistic"),
            "p_value": (round(float(p), 6) if p is not None else 1.0),
            "p_note": (None if p is not None else "no discordant pairs (all differences zero)"),
            "n_pairs": int(r.get("n_pairs") or a.size), "n_eff": r.get("n_eff")}


def holm(pvals: dict[str, float]) -> dict:
    st = _stats()
    keys = list(pvals)
    out = st.holm([pvals[k] for k in keys])
    adj = out.get("p_adjusted", out.get("adjusted", None))
    return {"family": keys, "raw": {k: pvals[k] for k in keys},
            "adjusted": dict(zip(keys, adj)) if adj is not None else out,
            "alpha": 0.05, "method": "holm"}


# --------------------------------------------------------------------------- #
# metrics
# --------------------------------------------------------------------------- #
def metrics_block(ref: np.ndarray, items: list[dict], scores: np.ndarray, name: str) -> dict:
    """Per-rung abstain precision / recall / over-refusal / AUROC for one gate on one split."""
    from sklearn.metrics import roc_auc_score

    is_neg = np.array([it["rung"] > 0 for it in items])
    is_pos = ~is_neg
    out = {"gate": name, "n_items": int(len(items)),
           "pooled_abstain_precision": round(float(ref[is_neg].mean()), 4),
           "over_refusal": round(float(ref[is_pos].mean()), 4),
           "coverage": round(float(1.0 - ref.mean()), 4), "per_rung": {}}
    for r in (1, 2, 3, 4):
        m = np.array([it["rung"] == r for it in items])
        if not m.any():
            continue
        y = np.concatenate([np.ones(int(is_pos.sum())), np.zeros(int(m.sum()))])  # 1 = answerable
        s = np.concatenate([scores[is_pos], scores[m]])
        auc = float(roc_auc_score(y, s)) if len(np.unique(y)) == 2 else float("nan")
        out["per_rung"][str(r)] = {
            "abstain_precision": round(float(ref[m].mean()), 4),
            "n": int(m.sum()),
            "auroc_answerable_vs_this_rung": round(auc, 4),
            "ci95": ci_mean(ref[m]),
        }
    return out
