"""R3-3b MF-7: gold-indicator control and D3 pooled top-1 hit/miss sanity check.

Post-hoc / exploratory re-derivation from EXISTING item and feature data only.
No model is trained for the frozen pipeline and no prior result is modified.

Writes only:
  04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json

Run:
  python 04_experiments/src/r3_r3_3b_mf7.py

Estimands
---------
1. Gold-indicator control (audit_twosided.json analogue): for each dev/test split
   and rung R1-R4, compare answerable items (rung 0) with that rung's negatives
   using the eight surface+lexical columns from audit.surface_features, then add
   the binary `is_gold` indicator. `is_gold` is a construction/label artefact:
   in the pre-registered items an answerable item ALWAYS presents its gold
   paragraph and a rung 1-4 negative NEVER does. The resulting AUROC = 1.0 is
   tautological, not evidence that the gate measures answerability.
2. D3 sanity: items_top1.jsonl contains ONLY rung = -1 pooled top-1-presented
   items, where label = 1 means the BM25 rank-1 passage IS the gold paragraph
   ("hit") and label = 0 means "miss". There are NO D3 R1/R2/R3 observations in
   these files, so a D3 per-rung R1-R3 AUROC is NOT computed or claimed. The
   six-surface-plus-overlap audit is instead re-run on the pooled hit/miss
   contrast per split and across splits, plus a small feature-stack sanity
   comparison from features_top1.csv and a dev-fitted logistic gate on test.

Bootstrap: fixed seed 20261118, 10000 resamples, 2.5/97.5 percentiles, both
item-level and article-cluster (title) resampling. The stratified 5-fold OOF
logistic CV uses seed 12345 to match r3_exp_audit_twosided.py, so the recomputed
point AUROCs reproduce the prior R3-3 cells. The fast rank-sum bootstrap is checked against r3_exp_auroc_ci.bootstrap_auroc_ci (read-only) on a small
fixture, and the check result is recorded in the output JSON.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
OUT = ROOT / "04_experiments" / "results" / "c1" / "r3" / "R3-3b" / "mf7_gold_control.json"
sys.path.insert(0, str(SRC))

import audit as A  # noqa: E402  (read-only input)
import r3_exp_auroc_ci as CI  # noqa: E402  (read-only reference bootstrap)

SEED = 20261118
N_BOOT = 10000
AUDIT_CV_SEED = 12345  # matches r3_exp_audit_twosided.py SEED (audit.py default 13)
ALPHA = 0.05
COMMAND = "python 04_experiments/src/r3_r3_3b_mf7.py"
PREFIX = "c1.r3_3b.mf7."

INPUT_PATHS = {
    "items": "04_experiments/data/items.jsonl",
    "items_top1": "04_experiments/data/items_top1.jsonl",
    "features_top1": "04_experiments/data/features_top1.csv",
    "audit_py": "04_experiments/src/audit.py",
    "reference_audit_twosided_py": "04_experiments/src/r3_exp_audit_twosided.py",
    "reference_bootstrap_py": "04_experiments/src/r3_exp_auroc_ci.py",
}
D3_FEATURES = [
    "bm25_presented", "bm25_top1", "bm25_top5_mean", "bm25_margin",
    "dense_presented", "dense_top1", "dense_margin", "top1_agreement",
    "ce_presented", "lex_overlap",
]
NOTES = {
    "gold_indicator":
        "is_gold is a construction/label artefact: in the pre-registered items "
        "answerable (rung 0) items always present the gold paragraph and rung "
        "1-4 negatives never do, so is_gold is a deterministic function of the "
        "label. AUROC=1.0 with is_gold is tautological and cannot exculpate the "
        "gate; it quantifies the confound named by MF-7.",
    "d3_scope":
        "D3 (top1_presented) has ONLY rung=-1 pooled hit/miss observations in "
        "items_top1.jsonl / features_top1.csv. There are no D3 R1/R2/R3 items, "
        "so the requested D3 per-rung R1-R3 estimand is unavailable and is NOT "
        "claimed here. All D3 numbers below are pooled (rung=-1) hit-vs-miss.",
    "label": "exploratory / post-hoc; no frozen verdict is revised.",
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _auroc_from_ranks(scores: np.ndarray, y: np.ndarray) -> np.ndarray:
    """AUROC for a batch of resamples, using average ranks for ties.

    Equivalent to sklearn.metrics.roc_auc_score for each row; validated below.
    """
    ranks = rankdata(scores, axis=1, method="average")
    n_pos = y.sum(axis=1).astype(float)
    n_neg = y.shape[1] - n_pos
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (np.einsum("ij,ij->i", ranks, y) - n_pos * (n_pos + 1.0) / 2.0) / (n_pos * n_neg)
    return out


def _indices(y: np.ndarray, n_boot: int, seed: int,
             cluster_ids: np.ndarray | None):
    """Resample indices. Item level: (n_boot, n) array. Cluster level: list of
    per-replicate index arrays (clusters can have unequal sizes)."""
    rng = np.random.default_rng(int(seed))
    n = int(len(y))
    if cluster_ids is None:
        return rng.integers(0, n, size=(int(n_boot), n)), "percentile_item", None
    uniq = np.unique(cluster_ids)
    by_cluster = {c: np.where(cluster_ids == c)[0] for c in uniq}
    sampled = rng.choice(uniq, size=(int(n_boot), uniq.size), replace=True)
    return ([np.concatenate([by_cluster[c] for c in row]) for row in sampled],
            "percentile_cluster", int(uniq.size))


def _n_boot(idx) -> int:
    return int(len(idx)) if isinstance(idx, list) else int(idx.shape[0])


def _draws(scores: np.ndarray, y: np.ndarray, idx) -> np.ndarray:
    scores = np.asarray(scores, dtype=float)
    y = np.asarray(y, dtype=int)
    if isinstance(idx, list):
        return np.array([_auroc_from_ranks(scores[i][None, :], y[i][None, :])[0] for i in idx])
    return _auroc_from_ranks(scores[idx], y[idx])


def _percentiles(draws: np.ndarray) -> tuple[float, float]:
    valid = np.isfinite(draws)
    draws = draws[valid]
    if draws.size == 0:
        return float("nan"), float("nan")
    lo, hi = (float(v) for v in np.percentile(draws, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)]))
    return lo, hi


def _bootstrap_ci(y: np.ndarray, scores: np.ndarray, idx,
                  seed: int, level: str, n_clusters: int | None) -> dict:
    y = np.asarray(y, dtype=int)
    scores = np.asarray(scores, dtype=float)
    draws = _draws(scores, y, idx)
    lo, hi = _percentiles(draws)
    return {
        "point": float(roc_auc_score(y, scores)),
        "lo": round(lo, 4),
        "hi": round(hi, 4),
        "level": level,
        "method": "percentile",
        "n": int(len(y)),
        "n_positive": int((y == 1).sum()),
        "n_negative": int((y == 0).sum()),
        "n_boot": _n_boot(idx),
        "n_valid": int(np.isfinite(draws).sum()),
        "n_clusters": n_clusters,
        "seed": int(seed),
        "alpha": float(ALPHA),
        "post_hoc": True,
    }


def _bootstrap_paired_ci(y: np.ndarray, a: np.ndarray, b: np.ndarray, idx,
                         seed: int, level: str, n_clusters: int | None) -> dict:
    y = np.asarray(y, dtype=int)
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    draws = _draws(a, y, idx) - _draws(b, y, idx)
    lo, hi = _percentiles(draws)
    point = float(roc_auc_score(y, a) - roc_auc_score(y, b))
    return {
        "point": round(point, 4), "lo": round(lo, 4), "hi": round(hi, 4),
        "level": level, "method": "paired_percentile", "n": int(len(y)),
        "n_boot": _n_boot(idx), "n_valid": int(np.isfinite(draws).sum()),
        "n_clusters": n_clusters, "seed": int(seed), "alpha": float(ALPHA),
        "post_hoc": True,
    }


def _oof(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Five-fold stratified OOF logistic scores, matching the CV rule in
    r3_exp_audit_twosided.py (stratified 5-fold, shuffle, seed 12345)."""
    n_splits = int(min(5, int(y.sum()), int((y == 0).sum())))
    if n_splits < 2:
        raise ValueError("not enough observations per class for 5-fold OOF")
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=AUDIT_CV_SEED)
    oof = np.zeros(len(y), dtype=float)
    for tr, te in skf.split(X, y):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        clf.fit(X[tr], y[tr])
        oof[te] = clf.predict_proba(X[te])[:, 1]
    return oof


def _validate_bootstrap() -> dict:
    """Cross-check the fast rank bootstrap against the read-only reference."""
    rng = np.random.default_rng(7)
    y = np.array([0] * 20 + [1] * 20, dtype=int)
    s = np.round(rng.random(len(y)), 2)
    clusters = np.array([f"c{i // 5}" for i in range(len(y))])
    checks = {}
    for level, cl in (("item", None), ("cluster", clusters)):
        ref = CI.bootstrap_auroc_ci(y, s, n_boot=200, seed=SEED, cluster_ids=cl)
        idx, _, ncl = _indices(y, 200, SEED, cl)
        fast = _bootstrap_ci(y, s, idx, SEED, level, ncl)
        ref_lo, ref_hi = round(ref["lo"], 4), round(ref["hi"], 4)
        checks[level] = {
            "reference_module": "04_experiments/src/r3_exp_auroc_ci.py",
            "n_boot_check": 200,
            "reference_lo": ref_lo, "reference_hi": ref_hi,
            "fast_lo": fast["lo"], "fast_hi": fast["hi"],
            "max_abs_diff": round(max(abs(ref_lo - fast["lo"]),
                                      abs(ref_hi - fast["hi"])), 8),
            "pass": bool(abs(ref_lo - fast["lo"]) < 1e-8 and
                         abs(ref_hi - fast["hi"]) < 1e-8),
        }
    return checks


# --------------------------------------------------------------------------- #
# result builders
# --------------------------------------------------------------------------- #
def gold_control(items: list[dict], results: dict, details: dict) -> None:
    details["gold_indicator_control"] = {}
    for split in ("dev", "test"):
        sel = [it for it in items if it["split"] == split]
        pos = [it for it in sel if it["rung"] == 0]
        assert pos and all(int(it["label"]) == 1 for it in pos), "answerable rung check"
        details["gold_indicator_control"][split] = {}
        for rung in (1, 2, 3, 4):
            neg = [it for it in sel if it["rung"] == rung]
            if not neg:
                continue
            assert all(int(it["label"]) == 0 for it in neg), "negative rung check"
            X = np.vstack([A.surface_features(pos, with_lex=True),
                           A.surface_features(neg, with_lex=True)])
            # audit.py convention: negative item = positive class (y=1)
            y = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))]).astype(int)
            is_gold = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))]).astype(float)
            Xg = np.column_stack([X, is_gold])
            clusters = np.array([it["title"] for it in pos + neg])
            base, plus = _oof(X, y), _oof(Xg, y)
            base_auc = float(roc_auc_score(y, base))
            plus_auc = float(roc_auc_score(y, plus))
            alone_raw = float(roc_auc_score(y, is_gold))
            alone_oriented = float(roc_auc_score(1 - y, is_gold))
            per = {
                "split": split, "rung": rung,
                "n_answerable": len(pos), "n_negatives": len(neg), "n": len(y),
                "y_convention": "1 = rung negative, 0 = answerable (audit.py)",
                "auroc_surface_lex": round(base_auc, 4),
                "auroc_plus_is_gold": round(plus_auc, 4),
                "auroc_is_gold_alone_raw": round(alone_raw, 4),
                "auroc_is_gold_alone_answerable_oriented": round(alone_oriented, 4),
                "delta_auroc_plus_minus_base": round(plus_auc - base_auc, 4),
                "is_gold_deterministic_from_label": True,
            }
            for level, cl in (("item", None), ("cluster", clusters)):
                idx, _, ncl = _indices(y, N_BOOT, SEED, cl)
                cb = _bootstrap_ci(y, base, idx, SEED, level, ncl)
                cp = _bootstrap_ci(y, plus, idx, SEED, level, ncl)
                cd = _bootstrap_paired_ci(y, plus, base, idx, SEED, level, ncl)
                per[f"ci_{level}"] = {"base": cb, "plus_is_gold": cp, "delta": cd}
                stem = f"gold_control.{split}.r{rung}"
                pre = PREFIX + stem
                results[f"{pre}.auroc_surface_lex_ci_{level}_lo"] = cb["lo"]
                results[f"{pre}.auroc_surface_lex_ci_{level}_hi"] = cb["hi"]
                results[f"{pre}.auroc_plus_is_gold_ci_{level}_lo"] = cp["lo"]
                results[f"{pre}.auroc_plus_is_gold_ci_{level}_hi"] = cp["hi"]
                results[f"{pre}.delta_auroc_ci_{level}_lo"] = cd["lo"]
                results[f"{pre}.delta_auroc_ci_{level}_hi"] = cd["hi"]
            details["gold_indicator_control"][split][str(rung)] = per
            pre = PREFIX + f"gold_control.{split}.r{rung}"
            results[f"{pre}.n_answerable"] = len(pos)
            results[f"{pre}.n_negatives"] = len(neg)
            results[f"{pre}.n"] = len(y)
            results[f"{pre}.auroc_surface_lex"] = round(base_auc, 4)
            results[f"{pre}.auroc_plus_is_gold"] = round(plus_auc, 4)
            results[f"{pre}.auroc_is_gold_alone_raw"] = round(alone_raw, 4)
            results[f"{pre}.auroc_is_gold_alone_answerable_oriented"] = round(alone_oriented, 4)
            results[f"{pre}.delta_auroc_plus_minus_base"] = round(plus_auc - base_auc, 4)
            results[f"{pre}.is_gold_deterministic_from_label"] = True


def d3_pooled(items_top1: list[dict], feat_rows: list[dict],
              results: dict, details: dict) -> None:
    assert set(int(it["rung"]) for it in items_top1) == {-1}, "D3 must be rung=-1 only"
    assert set(int(r["rung"]) for r in feat_rows) == {-1}, "D3 features must be rung=-1 only"
    assert len(items_top1) == len(feat_rows), "top1 item/feature count mismatch"
    for it, row in zip(items_top1, feat_rows):
        assert it["item_id"] == row["item_id"], "top1 item-id alignment mismatch"
        assert int(it["label"]) == int(row["label"]), "top1 label mismatch"
        assert int(it["is_gold"]) == int(it["label"]), "top1 is_gold/label mismatch"
    details["d3_pooled"] = {
        "scope": "rung=-1 pooled hit/miss only",
        "rungs_present": [-1],
        "per_rung_R1_R3_estimand_available": False,
        "estimand": "label=1 hit (BM25 rank-1 is gold), label=0 miss; pooled over all D3 items",
    }
    results[PREFIX + "d3_pooled.per_rung_R1_R3_estimand_available"] = False
    results[PREFIX + "d3_pooled.rungs_present_value"] = -1

    id_to_item = {it["item_id"]: it for it in items_top1}
    for scope in ("dev", "test", "all"):
        sel = [it for it in items_top1 if scope == "all" or it["split"] == scope]
        rows = [r for r in feat_rows if scope == "all" or r["split"] == scope]
        y = np.array([int(it["label"]) for it in sel], dtype=int)
        clusters = np.array([it["title"] for it in sel])
        n_hit, n_miss = int((y == 1).sum()), int((y == 0).sum())
        stem = f"d3_pooled.{scope}"
        pre = PREFIX + stem
        results[f"{pre}.n"] = len(sel)
        results[f"{pre}.n_hit"] = n_hit
        results[f"{pre}.n_miss"] = n_miss
        results[f"{pre}.hit_rate"] = round(n_hit / len(sel), 4)
        per: dict = {
            "scope": scope, "n": len(sel), "n_hit": n_hit, "n_miss": n_miss,
            "hit_rate": round(n_hit / len(sel), 4), "rungs": [-1],
        }
        # six-surface-plus-overlap audit on the pooled hit/miss contrast
        X = A.surface_features(sel, with_lex=True)
        oof = _oof(X, y)
        auc = float(roc_auc_score(y, oof))
        per["surface_lex_auroc"] = round(auc, 4)
        results[f"{pre}.auroc_surface_lex_hit_vs_miss"] = round(auc, 4)
        for level, cl in (("item", None), ("cluster", clusters)):
            idx, _, ncl = _indices(y, N_BOOT, SEED, cl)
            ci = _bootstrap_ci(y, oof, idx, SEED, level, ncl)
            per[f"surface_lex_ci_{level}"] = ci
            results[f"{pre}.auroc_surface_lex_ci_{level}_lo"] = ci["lo"]
            results[f"{pre}.auroc_surface_lex_ci_{level}_hi"] = ci["hi"]
        # single-feature sanity comparison from features_top1.csv
        per["feature_aurocs"] = {}
        idx_item, _, _ = _indices(y, N_BOOT, SEED, None)
        for name in D3_FEATURES:
            x = np.array([float(r[name]) for r in rows], dtype=float)
            a = float(roc_auc_score(y, x))
            ci = _bootstrap_ci(y, x, idx_item, SEED, "item", None)
            per["feature_aurocs"][name] = {"auroc": round(a, 4), "ci_item": ci}
            results[f"{pre}.feature_{name}_auroc"] = round(a, 4)
            results[f"{pre}.feature_{name}_ci_item_lo"] = ci["lo"]
            results[f"{pre}.feature_{name}_ci_item_hi"] = ci["hi"]
        details["d3_pooled"][scope] = per

    # dev-fitted logistic gate on the feature file, evaluated on held-out test;
    # definition recorded here explicitly (not the frozen paper gate).
    dev_rows = [r for r in feat_rows if r["split"] == "dev"]
    test_rows = [r for r in feat_rows if r["split"] == "test"]
    Xd = np.array([[float(r[f]) for f in D3_FEATURES] for r in dev_rows], dtype=float)
    Xt = np.array([[float(r[f]) for f in D3_FEATURES] for r in test_rows], dtype=float)
    yd = np.array([int(r["label"]) for r in dev_rows], dtype=int)
    yt = np.array([int(r["label"]) for r in test_rows], dtype=int)
    gate = make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=2000, random_state=AUDIT_CV_SEED))
    gate.fit(Xd, yd)
    s_t = gate.predict_proba(Xt)[:, 1]
    auc_t = float(roc_auc_score(yt, s_t))
    clusters_t = np.array([id_to_item[r["item_id"]]["title"] for r in test_rows])
    per_gate = {
        "definition": "standardized logistic regression on the ten D3_FEATURES, "
                      "fitted on dev rows of features_top1.csv, scored on test rows",
        "n_dev_fit": len(dev_rows), "n_test": len(test_rows),
        "n_test_hit": int((yt == 1).sum()), "n_test_miss": int((yt == 0).sum()),
        "auroc": round(auc_t, 4), "features": list(D3_FEATURES),
        "random_state": AUDIT_CV_SEED,
    }
    for level, cl in (("item", None), ("cluster", clusters_t)):
        idx, _, ncl = _indices(yt, N_BOOT, SEED, cl)
        ci = _bootstrap_ci(yt, s_t, idx, SEED, level, ncl)
        per_gate[f"ci_{level}"] = ci
        pre = PREFIX + "d3_pooled.dev_fit_gate.test"
        results[f"{pre}.auroc_hit_vs_miss_ci_{level}_lo"] = ci["lo"]
        results[f"{pre}.auroc_hit_vs_miss_ci_{level}_hi"] = ci["hi"]
    results[PREFIX + "d3_pooled.dev_fit_gate.test.auroc_hit_vs_miss"] = round(auc_t, 4)
    results[PREFIX + "d3_pooled.dev_fit_gate.test.n_dev_fit"] = len(dev_rows)
    results[PREFIX + "d3_pooled.dev_fit_gate.test.n_test"] = len(test_rows)
    details["d3_pooled"]["dev_fit_gate_test"] = per_gate


def build_result() -> dict:
    items = load_jsonl(ROOT / INPUT_PATHS["items"])
    top1 = load_jsonl(ROOT / INPUT_PATHS["items_top1"])
    feats = load_csv(ROOT / INPUT_PATHS["features_top1"])
    results: dict = {}
    details: dict = {}
    gold_control(items, results, details)
    d3_pooled(top1, feats, results, details)
    validation = _validate_bootstrap()
    out = {
        "experiment": "c1",
        "lane": "R3-3b-deferred-analyses",
        "item": "MF-7",
        "generated_by": "04_experiments/src/r3_r3_3b_mf7.py",
        "command": COMMAND,
        "commands": [COMMAND],
        "seed": SEED,
        "seeds": {
            "bootstrap": SEED,
            "audit_cv": AUDIT_CV_SEED,  # r3_exp_audit_twosided.py; audit.py default is 13
            "audit_py_default_cv_seed": 13,
            "gate_logistic_random_state": AUDIT_CV_SEED,
        },
        "n_boot": N_BOOT,
        "bootstrap_method": "non-parametric percentile bootstrap, 2.5/97.5; item-level and article-title-cluster resampling",
        "alpha": ALPHA,
        "post_hoc": True,
        "exploratory": True,
        "label": "exploratory/post-hoc",
        "notes": NOTES,
        "input_paths": INPUT_PATHS,
        "sha256_inputs": {k: sha256_file(ROOT / v) for k, v in INPUT_PATHS.items()},
        "denominators": {
            "items_total": len(items),
            "items_top1_total": len(top1),
            "features_top1_rows": len(feats),
            "gold_control": {
                s: {str(r): {
                    "n_answerable": sum(1 for it in items if it["split"] == s and it["rung"] == 0),
                    "n_negatives": sum(1 for it in items if it["split"] == s and it["rung"] == r),
                } for r in (1, 2, 3, 4)} for s in ("dev", "test")
            },
            "d3_pooled": {
                s: {
                    "n_hit": sum(1 for it in top1 if it["label"] == 1 and (s == "all" or it["split"] == s)),
                    "n_miss": sum(1 for it in top1 if it["label"] == 0 and (s == "all" or it["split"] == s)),
                } for s in ("dev", "test", "all")
            },
        },
        "bootstrap_validation": validation,
        "results": results,
        "details": details,
    }
    assert all(v["pass"] for v in validation.values()), "bootstrap cross-check failed"
    return out


def main() -> None:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "wrote": str(OUT),
        "seed": SEED, "n_boot": N_BOOT,
        "n_result_keys": len(result["results"]),
        "bootstrap_validation": result["bootstrap_validation"],
    }, indent=2))


if __name__ == "__main__":
    main()
