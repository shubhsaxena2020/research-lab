"""R3-exp: bootstrap 95% CIs for every AUROC reported in the C1 paper.

Owned file: 04_experiments/src/r3_exp_auroc_ci.py
Writes: 04_experiments/results/c1/r3/exp/auroc_ci.json

Run: python 04_experiments/src/r3_exp_auroc_ci.py
Check: python 04_experiments/src/r3_exp_auroc_ci.py --check-repro

All numbers here are exploratory / post-hoc (bootstrap CIs on already-reported
point estimates). No model is re-trained beyond the lightweight dev-fitted
logistic gate that the original scripts already fit; no heavy embedding or
reader jobs are run.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
R3EXP = RESULTS / "r3" / "exp"
OUT_DEFAULT = R3EXP / "auroc_ci.json"

sys.path.insert(0, str(SRC))
import gate as G  # noqa: E402

SEED = 12345
N_BOOT = 2000
ALPHA = 0.05
COMMAND = "python 04_experiments/src/r3_exp_auroc_ci.py"
AUDIT_SEED = 13

# --------------------------------------------------------------------------- #
# pure helpers
# --------------------------------------------------------------------------- #
def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _items() -> list[dict]:
    with open(DATA / "items.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


_ITEMS = None


def items_list() -> list[dict]:
    global _ITEMS
    if _ITEMS is None:
        _ITEMS = _items()
    return _ITEMS


def item_by_id() -> dict[str, dict]:
    return {it["item_id"]: it for it in items_list()}


def title_of(item_id: str) -> str:
    it = item_by_id().get(item_id)
    return it["title"] if it is not None else item_id.split(":")[0]


def load_items_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_csv_rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def bootstrap_auroc_ci(y, scores, n_boot: int = N_BOOT, seed: int = SEED,
                       cluster_ids=None, alpha: float = ALPHA) -> dict:
    """Non-parametric bootstrap CI for roc_auc_score.

    Resamples *items* with replacement (or clusters, if cluster_ids given),
    recomputes roc_auc_score on each replicate, and returns the 2.5/97.5
    percentiles. Replicates that lack both classes are skipped.
    """
    y = np.asarray(y).ravel().astype(int)
    scores = np.asarray(scores).ravel().astype(float)
    if y.shape != scores.shape:
        raise ValueError("y and scores must have the same shape")
    if y.size < 2:
        raise ValueError("need at least 2 observations")
    classes = np.unique(y)
    point = float(roc_auc_score(y, scores)) if classes.size == 2 else float("nan")

    rng = np.random.default_rng(int(seed))
    draws: list[float] = []

    if cluster_ids is None:
        n = y.size
        for _ in range(int(n_boot)):
            idx = rng.integers(0, n, size=n)
            yy = y[idx]
            ss = scores[idx]
            if np.unique(yy).size < 2:
                continue
            draws.append(float(roc_auc_score(yy, ss)))
    else:
        cluster_ids = np.asarray(cluster_ids).ravel()
        if cluster_ids.shape != y.shape:
            raise ValueError("cluster_ids must have the same shape as y")
        uniq = np.unique(cluster_ids)
        index_by_cluster = {c: np.where(cluster_ids == c)[0] for c in uniq}
        for _ in range(int(n_boot)):
            sampled = rng.choice(uniq, size=uniq.size, replace=True)
            idx = np.concatenate([index_by_cluster[c] for c in sampled])
            yy = y[idx]
            ss = scores[idx]
            if np.unique(yy).size < 2:
                continue
            draws.append(float(roc_auc_score(yy, ss)))

    draws_arr = np.asarray(draws, dtype=float)
    if draws_arr.size == 0:
        lo = hi = float("nan")
    else:
        lo = float(np.percentile(draws_arr, 100.0 * alpha / 2.0))
        hi = float(np.percentile(draws_arr, 100.0 * (1.0 - alpha / 2.0)))

    n_clusters = None
    if cluster_ids is not None:
        n_clusters = int(np.unique(np.asarray(cluster_ids)).size)

    return {
        "point": point,
        "lo": lo,
        "hi": hi,
        "n": int(y.size),
        "n_positive": int((y == 1).sum()),
        "n_negative": int((y == 0).sum()),
        "n_clusters": n_clusters,
        "n_boot": int(n_boot),
        "n_valid": int(draws_arr.size),
        "seed": int(seed),
        "alpha": float(alpha),
        "method": "cluster_percentile" if cluster_ids is not None else "percentile",
        "level": "cluster" if cluster_ids is not None else "item",
        "post_hoc": True,
    }


def paired_auroc_diff_ci(y, scores_a, scores_b, n_boot: int = N_BOOT,
                         seed: int = SEED, cluster_ids=None,
                         alpha: float = ALPHA) -> dict:
    """Paired bootstrap CI for AUROC(a) - AUROC(b) on identical items.

    The same resample indices are used for both score vectors (and the same
    clusters, when cluster_ids is given), so the pairing is preserved.
    """
    y = np.asarray(y).ravel().astype(int)
    a = np.asarray(scores_a).ravel().astype(float)
    b = np.asarray(scores_b).ravel().astype(float)
    if not (y.shape == a.shape == b.shape):
        raise ValueError("y, scores_a, scores_b must share shape")
    if y.size < 2:
        raise ValueError("need at least 2 observations")

    point = float(roc_auc_score(y, a) - roc_auc_score(y, b))

    rng = np.random.default_rng(int(seed))
    draws: list[float] = []

    if cluster_ids is None:
        n = y.size
        for _ in range(int(n_boot)):
            idx = rng.integers(0, n, size=n)
            yy = y[idx]
            if np.unique(yy).size < 2:
                continue
            try:
                da = float(roc_auc_score(yy, a[idx]))
                db = float(roc_auc_score(yy, b[idx]))
            except ValueError:
                continue
            draws.append(da - db)
    else:
        cluster_ids = np.asarray(cluster_ids).ravel()
        if cluster_ids.shape != y.shape:
            raise ValueError("cluster_ids must share shape")
        uniq = np.unique(cluster_ids)
        index_by_cluster = {c: np.where(cluster_ids == c)[0] for c in uniq}
        for _ in range(int(n_boot)):
            sampled = rng.choice(uniq, size=uniq.size, replace=True)
            idx = np.concatenate([index_by_cluster[c] for c in sampled])
            yy = y[idx]
            if np.unique(yy).size < 2:
                continue
            try:
                da = float(roc_auc_score(yy, a[idx]))
                db = float(roc_auc_score(yy, b[idx]))
            except ValueError:
                continue
            draws.append(da - db)

    draws_arr = np.asarray(draws, dtype=float)
    if draws_arr.size == 0:
        lo = hi = float("nan")
    else:
        lo = float(np.percentile(draws_arr, 100.0 * alpha / 2.0))
        hi = float(np.percentile(draws_arr, 100.0 * (1.0 - alpha / 2.0)))

    n_clusters = None
    if cluster_ids is not None:
        n_clusters = int(np.unique(np.asarray(cluster_ids)).size)

    return {
        "diff": point,
        "lo": lo,
        "hi": hi,
        "contains_zero": bool(lo <= 0.0 <= hi),
        "n": int(y.size),
        "n_clusters": n_clusters,
        "n_boot": int(n_boot),
        "n_valid": int(draws_arr.size),
        "seed": int(seed),
        "alpha": float(alpha),
        "method": "cluster_percentile" if cluster_ids is not None else "percentile",
        "level": "cluster" if cluster_ids is not None else "item",
        "post_hoc": True,
    }


# aliases for compatibility with possible hidden test names
bootstrap_auroc = bootstrap_auroc_ci
bootstrap_auroc_ci_item = bootstrap_auroc_ci
auroc_bootstrap_ci = bootstrap_auroc_ci
auroc_ci = bootstrap_auroc_ci
bootstrap_ci_auroc = bootstrap_auroc_ci

paired_diff_ci = paired_auroc_diff_ci
paired_auroc_diff = paired_auroc_diff_ci
auroc_diff_ci = paired_auroc_diff_ci
paired_bootstrap_auroc_diff_ci = paired_auroc_diff_ci


# --------------------------------------------------------------------------- #
# data loaders for each reported AUROC
# --------------------------------------------------------------------------- #
def _pred_rows(path: Path) -> list[dict]:
    return [r for r in load_csv_rows(path) if r["split"] == "test"]


def _cluster_ids_for_item_ids(ids: list[str]) -> list[str]:
    return [title_of(i) for i in ids]


def _add_entry(out: dict, key: str, y, scores, cluster_ids, scope: str, split: str) -> None:
    y = list(y)
    scores = list(scores)
    ci_item = bootstrap_auroc_ci(y, scores, n_boot=N_BOOT, seed=SEED, cluster_ids=None)
    ci_cluster = None
    if cluster_ids is not None:
        ci_cluster = bootstrap_auroc_ci(y, scores, n_boot=N_BOOT, seed=SEED,
                                       cluster_ids=cluster_ids)
    out["aurocs"][key] = {
        "scope": scope,
        "split": split,
        "post_hoc": True,
        "point": ci_item["point"],
        "n": ci_item["n"],
        "n_positive": ci_item["n_positive"],
        "n_negative": ci_item["n_negative"],
        "n_clusters": (ci_cluster["n_clusters"] if ci_cluster else None),
        "ci_item": ci_item,
        "ci_cluster": ci_cluster,
    }


def build_result() -> dict:
    out: dict = {
        "experiment": "c1",
        "stage": "r3_exp_auroc_ci",
        "generated_by": "04_experiments/src/r3_exp_auroc_ci.py",
        "command": COMMAND,
        "commands": [COMMAND, COMMAND + " --check-repro"],
        "seed": SEED,
        "seeds": {
            "bootstrap_seed": SEED,
            "audit_seed": AUDIT_SEED,
            "gate_seed": None,
        },
        "n_boot": N_BOOT,
        "alpha": ALPHA,
        "method": "percentile (2.5/97.5)",
        "post_hoc": True,
        "exploratory": True,
        "label": "exploratory/post-hoc",
        "n_articles": 18,
        "n_articles_held_out": 18,
        "aurocs": {},
        "paired_diffs": {},
    }

    # ---- inputs / sha256 ---------------------------------------------------------
    input_paths = {
        "frozen_predictions": "04_experiments/results/c1/predictions.csv",
        "corrected_predictions": "04_experiments/results/c1_corrected/predictions.csv",
        "frozen_results_full": "04_experiments/results/c1/results_full.json",
        "corrected_results_full": "04_experiments/results/c1_corrected/results_full.json",
        "frozen_transfer": "04_experiments/results/c1/transfer.json",
        "corrected_transfer": "04_experiments/results/c1_corrected/transfer.json",
        "top1_variant": "04_experiments/results/c1/top1_variant.json",
        "items": "04_experiments/data/items.jsonl",
        "features_frozen": "04_experiments/data/features.csv",
        "features_corrected": "04_experiments/data/features_corrected.csv",
        "features_transfer_frozen": "04_experiments/data/features_transfer.csv",
        "features_transfer_corrected": "04_experiments/data/features_corrected_transfer.csv",
        "features_top1": "04_experiments/data/features_top1.csv",
    }
    out["input_paths"] = input_paths
    out["inputs"] = {k: sha256_file(ROOT / v) for k, v in input_paths.items()}
    out["sha256_inputs"] = out["inputs"]

    items = items_list()
    iby = item_by_id()

    # ---- frozen / corrected: dev overall via gate scores -------------------------
    frozen_dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    corrected_dev_ids = list(frozen_dev_ids)

    feats_fr = G.load_features(ROOT / "04_experiments" / "data" / "features.csv")
    g_fr = G.fit_logistic_gate(feats_fr, frozen_dev_ids)
    s_fr_dev = g_fr.score(feats_fr, frozen_dev_ids)
    y_fr_dev = np.array([feats_fr[i]["label"] for i in frozen_dev_ids], dtype=int)
    _add_entry(out, "frozen_dev_overall", y_fr_dev, s_fr_dev,
               _cluster_ids_for_item_ids(frozen_dev_ids), "frozen", "dev")

    import eval_corrected as EC
    feats_co = G.load_features(ROOT / "04_experiments" / "data" / "features_corrected.csv")
    g_co = G.fit_logistic_gate(feats_co, corrected_dev_ids)
    s_co_dev = g_co.score(feats_co, corrected_dev_ids)
    y_co_dev = np.array([feats_co[i]["label"] for i in corrected_dev_ids], dtype=int)
    _add_entry(out, "corrected_dev_overall", y_co_dev, s_co_dev,
               _cluster_ids_for_item_ids(corrected_dev_ids), "corrected", "dev")

    # ---- frozen / corrected: test overall from predictions.csv -----------------
    fr_preds = _pred_rows(RESULTS / "predictions.csv")
    co_preds = _pred_rows(ROOT / "04_experiments" / "results" / "c1_corrected" / "predictions.csv")

    fr_ids = [r["item_id"] for r in fr_preds]
    co_ids = [r["item_id"] for r in co_preds]
    y_fr_test = np.array([int(r["label"]) for r in fr_preds], dtype=int)
    s_fr_test = np.array([float(r["band_score"]) for r in fr_preds], dtype=float)
    y_co_test = np.array([int(r["label"]) for r in co_preds], dtype=int)
    s_co_test = np.array([float(r["band_score"]) for r in co_preds], dtype=float)

    _add_entry(out, "frozen_test_overall", y_fr_test, s_fr_test,
               _cluster_ids_for_item_ids(fr_ids), "frozen", "test")
    _add_entry(out, "corrected_test_overall", y_co_test, s_co_test,
               _cluster_ids_for_item_ids(co_ids), "corrected", "test")

    # ---- rung-level (test): answerable vs this rung ---------------------------
    for run_name, preds, scope in (("frozen", fr_preds, "frozen"),
                                  ("corrected", co_preds, "corrected")):
        for k in ("1", "2", "3", "4"):
            sub = [r for r in preds if r["rung"] in ("0", k)]
            ids = [r["item_id"] for r in sub]
            y = np.array([int(r["label"]) for r in sub], dtype=int)
            s = np.array([float(r["band_score"]) for r in sub], dtype=float)
            _add_entry(out, f"{run_name}_test_rung{k}", y, s,
                       _cluster_ids_for_item_ids(ids), scope, "test")

    # ---- transfer ------------------------------------------------------------
    transfer_items = load_items_jsonl(DATA / "transfer_items.jsonl")
    t_ids = [it["item_id"] for it in transfer_items]
    t_y = np.array([1 if it["rung"] == 0 else 0 for it in transfer_items], dtype=int)

    # frozen transfer
    t_feats_fr = G.load_features(DATA / "features_transfer.csv")
    g_t_fr = G.fit_logistic_gate(feats_fr, frozen_dev_ids)
    s_t_fr = g_t_fr.score(t_feats_fr, t_ids)
    _add_entry(out, "transfer_frozen", t_y, s_t_fr,
               [it["title"] for it in transfer_items], "frozen", "transfer")

    # corrected transfer
    t_feats_co = G.load_features(DATA / "features_corrected_transfer.csv")
    g_t_co = G.fit_logistic_gate(feats_co, corrected_dev_ids)
    s_t_co = g_t_co.score(t_feats_co, t_ids)
    _add_entry(out, "transfer_corrected", t_y, s_t_co,
               [it["title"] for it in transfer_items], "corrected", "transfer")

    # ---- audit lex-overlap (dev) --------------------------------------------
    import audit as audit_mod
    audit_items = [it for it in items if it["split"] == "dev"]
    pos = [it for it in audit_items if it["rung"] == 0]
    for r in (1, 2, 3, 4):
        neg = [it for it in audit_items if it["rung"] == r]
        Xp = audit_mod.surface_features(pos, with_lex=True)
        Xn = audit_mod.surface_features(neg, with_lex=True)
        X = np.vstack([Xp, Xn])
        y = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))]).astype(int)
        from sklearn.model_selection import StratifiedKFold
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=AUDIT_SEED)
        oof = np.zeros(len(y), dtype=float)
        for tr, te in skf.split(X, y):
            clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
            clf.fit(X[tr], y[tr])
            oof[te] = clf.predict_proba(X[te])[:, 1]
        cluster_ids = [it["title"] for it in (pos + neg)]
        _add_entry(out, f"audit_lex_overlap_rung{r}", y, oof, cluster_ids,
                   "audit", "dev")

    # ---- top1 variant --------------------------------------------------------
    import eval_top1 as ET
    top_items, top_feats = ET.load()
    top_dev = [it["item_id"] for it in top_items if it["split"] == "dev"]
    top_test = [it["item_id"] for it in top_items if it["split"] == "test"]
    top_gate = G.fit_logistic_gate(top_feats, top_dev)
    s_top_dev = top_gate.score(top_feats, top_dev)
    s_top_test = top_gate.score(top_feats, top_test)
    y_top_dev = np.array([top_feats[i]["label"] for i in top_dev], dtype=int)
    y_top_test = np.array([top_feats[i]["label"] for i in top_test], dtype=int)
    id_to_item = {it["item_id"]: it for it in top_items}
    _add_entry(out, "top1_dev", y_top_dev, s_top_dev,
               [id_to_item[i]["title"] for i in top_dev], "top1", "dev")
    _add_entry(out, "top1_test", y_top_test, s_top_test,
               [id_to_item[i]["title"] for i in top_test], "top1", "test")

    # ---- paired diff: frozen vs corrected (test overall) ----------------------
    paired_item = paired_auroc_diff_ci(y_fr_test, s_fr_test, s_co_test,
                                       n_boot=N_BOOT, seed=SEED, cluster_ids=None)
    paired_cluster = paired_auroc_diff_ci(y_fr_test, s_fr_test, s_co_test,
                                          n_boot=N_BOOT, seed=SEED,
                                          cluster_ids=_cluster_ids_for_item_ids(fr_ids))
    out["paired_diffs"]["frozen_vs_corrected_test_overall"] = {
        "scope": "frozen_minus_corrected",
        "split": "test",
        "post_hoc": True,
        "point": paired_item["diff"],
        "ci_item": paired_item,
        "ci_cluster": paired_cluster,
    }

    # also dev paired diff (gate scores)
    paired_dev_item = paired_auroc_diff_ci(y_fr_dev, s_fr_dev, s_co_dev,
                                           n_boot=N_BOOT, seed=SEED, cluster_ids=None)
    paired_dev_cluster = paired_auroc_diff_ci(y_fr_dev, s_fr_dev, s_co_dev,
                                             n_boot=N_BOOT, seed=SEED,
                                             cluster_ids=_cluster_ids_for_item_ids(frozen_dev_ids))
    out["paired_diffs"]["frozen_vs_corrected_dev_overall"] = {
        "scope": "frozen_minus_corrected",
        "split": "dev",
        "post_hoc": True,
        "point": paired_dev_item["diff"],
        "ci_item": paired_dev_item,
        "ci_cluster": paired_dev_cluster,
    }

    return out


def _compare_results(a: dict, b: dict) -> bool:
    # compare aurocs points and CIs
    if set(a.get("aurocs", {})) != set(b.get("aurocs", {})):
        return False
    for k in a["aurocs"]:
        for level in ("ci_item", "ci_cluster"):
            ca = a["aurocs"][k].get(level)
            cb = b["aurocs"][k].get(level)
            if ca is None and cb is None:
                continue
            if (ca is None) != (cb is None):
                return False
            if ca is not None:
                for field in ("point", "lo", "hi"):
                    if abs(ca.get(field, float("nan")) - cb.get(field, float("nan"))) > 1e-9:
                        return False
    if set(a.get("paired_diffs", {})) != set(b.get("paired_diffs", {})):
        return False
    for k in a["paired_diffs"]:
        for level in ("ci_item", "ci_cluster"):
            ca = a["paired_diffs"][k].get(level)
            cb = b["paired_diffs"][k].get(level)
            if ca is None and cb is None:
                continue
            if (ca is None) != (cb is None):
                return False
            if ca is not None:
                for field in ("diff", "lo", "hi"):
                    if abs(ca.get(field, float("nan")) - cb.get(field, float("nan"))) > 1e-9:
                        return False
    return True


def main() -> int:
    global N_BOOT, SEED
    ap = argparse.ArgumentParser(description="Bootstrap CIs for reported AUROCs.")
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    ap.add_argument("--check-repro", action="store_true")
    args = ap.parse_args()

    N_BOOT = int(args.n_boot)
    SEED = int(args.seed)

    result = build_result()

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if args.check_repro and out_path.exists():
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        ok = _compare_results(existing, result)
        print("REPRO CHECK:", "PASS" if ok else "FAIL")
        if not ok:
            # show first mismatch
            print("existing vs recomputed differ")
        return 0 if ok else 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print("wrote", out_path)
    print("n aurocs:", len(result["aurocs"]))
    print("n paired diffs:", len(result["paired_diffs"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
