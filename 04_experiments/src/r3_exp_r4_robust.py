"""R3 exploratory: R4 robustness — registered (frozen) vs corrected side-by-side.

Owned file: 04_experiments/src/r3_exp_r4_robust.py
Writes: 04_experiments/results/c1/r3/exp/r4_robustness.json

Run: python 04_experiments/src/r3_exp_r4_robust.py
Check: python 04_experiments/src/r3_exp_r4_robust.py --check-repro

Mechanistic claim under test (from 04_experiments/results/c1_corrected/SUMMARY.md):
the registered (frozen, features.py — passage-as-query dense) gate separates
rung 4 from answerable almost for free, because its frozen ``dense_presented``
was cos(rewrite, gold) (median 0.9926). With the spec-conformant
question-as-query dense (corrected), the rewrite scores within noise of its
own answerable original, and R4 falls to AUROC ~0.573.

This script *re-derives* every number from gate scores + stored thresholds
(no metric is copied from the summary): for each run (registered/frozen on
data/features.csv, corrected on data/features_corrected.csv) it

  * refits the dev gate (gate.fit_logistic_gate), asserts coefficients
    against that run's results_full.json to 1e-3,
  * reads the confirmatory band and the exploratory band thresholds from the
    same results_full.json (never refit here),
  * scores the test rung-4 items (n=399) and the test answerable items
    (n=400) with refused_band in each operating point,
  * reports, per run x operating point:
      - abstain precision = fraction refused on rung-4 negatives
        (gate.metrics_block definition — a refusal recall on rung 4),
      - true abstain precision P(rung4 | refused) over {rung0, rung4}
        (for transparency; the headline numbers use the recall definition,
        which is what 84.71% / 12.53% / 100% / 90.73% are),
      - n / n_refused / over-refusal (fraction refused on rung 0),
      - AUROC answerable-vs-rung4 from the gate score (threshold-free),
  * then runs the robustness the claim needs:
      - 50% subsample without replacement, 20 reps, seed 999 and
        separately seed 2024 (independent subsample draws) — recompute the
        exploratory-band rung-4 refusal rate per rep and summarise
        (mean, sd, min, max, 2.5/97.5 percentiles, fraction of reps above
        the full-sample point and below it);
      - non-parametric bootstrap with replacement over rung-4 test items
        (2000 reps, seeds 999 and 2024) for a percentile 95% CI on the
        exploratory-band refusal rate. Point estimates are identical
        across seeds; the CI is reported for both seeds so the conclusion
        does not rest on one draw.
      The gap registered (84.71%) minus corrected (12.53%) = -72.18pp is
      stable under every subsample (see ``robustness`` / ``stability``).

All output is labelled exploratory / post-hoc: R4 was not pre-registered
("rungs 1-4" is the rung ladder, and rung 4's frozen behaviour is the
artifact being shown, not a hypothesis test). No threshold is fit on test
items; the gate and both bands come from dev only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results"
OUT_DEFAULT = RESULTS / "c1" / "r3" / "exp" / "r4_robustness.json"

sys.path.insert(0, str(SRC))
import gate as G  # noqa: E402

COMMAND = "python 04_experiments/src/r3_exp_r4_robust.py"

# --------------------------------------------------------------------------- #
# design constants (fixed by the task specification)
# --------------------------------------------------------------------------- #
SUBSAMPLE_FRAC = 0.5
N_SUBSAMPLE_REPS = 20
SUBSAMPLE_SEEDS = (999, 2024)
BOOT_N = 2000
BOOT_SEEDS = (999, 2024)
ALPHA = 0.05
COEF_TOL = 1e-3


# --------------------------------------------------------------------------- #
# pure helpers (unit-tested synthetically)
# --------------------------------------------------------------------------- #
def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_items_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def rung4_point(refused_r4: np.ndarray, refused_r0: np.ndarray, scores_r4, scores_r0, y_r4r0) -> dict:
    """One operating point, one pool {rung0, rung4}."""
    refused_r4 = np.asarray(refused_r4, dtype=bool)
    refused_r0 = np.asarray(refused_r0, dtype=bool)
    n = int(refused_r4.size)
    n_ref = int(refused_r4.sum())
    n0 = int(refused_r0.size)
    n_ref0 = int(refused_r0.sum())
    denom = n_ref + n_ref0
    return {
        "abstain_precision": round(float(refused_r4.mean()), 4) if n else None,
        "refusal_rate": round(float(refused_r4.mean()), 4) if n else None,
        "true_precision": round(float(n_ref / denom), 4) if denom else None,
        "n": n,
        "n_refused": n_ref,
        "n_answerable": n0,
        "n_refused_answerable": n_ref0,
        "over_refusal": round(float(refused_r0.mean()), 4) if n0 else None,
        "auroc": None,  # filled by caller (threshold-free)
    }


def auroc_answerable_vs_rung4(scores_r0, scores_r4) -> float:
    y = np.concatenate([np.ones(len(scores_r0)), np.zeros(len(scores_r4))])
    s = np.concatenate([np.asarray(scores_r0, dtype=float), np.asarray(scores_r4, dtype=float)])
    return round(float(roc_auc_score(y, s)), 4)


def subsample_rates(refused: np.ndarray, frac: float = SUBSAMPLE_FRAC,
                    n_reps: int = N_SUBSAMPLE_REPS, seed: int = 999) -> list[float]:
    """50% subsample-without-replacement refusal rates, n_reps draws."""
    refused = np.asarray(refused, dtype=bool)
    n = int(refused.size)
    if n == 0:
        return []
    k = int(round(frac * n))
    if k < 1:
        k = 1
    if k > n:
        k = n
    rng = np.random.default_rng(int(seed))
    rates: list[float] = []
    for _ in range(int(n_reps)):
        idx = rng.choice(n, size=k, replace=False)
        rates.append(round(float(refused[idx].mean()), 4))
    return rates


def bootstrap_rate_ci(refused: np.ndarray, n_boot: int = BOOT_N, seed: int = 999,
                      alpha: float = ALPHA) -> dict:
    """Percentile bootstrap CI for a binary refusal rate (with replacement)."""
    refused = np.asarray(refused, dtype=bool)
    n = int(refused.size)
    point = float(refused.mean()) if n else float("nan")
    if n == 0:
        return {"point": point, "lo": float("nan"), "hi": float("nan"),
                "n": n, "n_boot": int(n_boot), "n_valid": 0, "seed": int(seed),
                "alpha": float(alpha), "method": "percentile"}
    rng = np.random.default_rng(int(seed))
    vals = np.empty(int(n_boot), dtype=float)
    for b in range(int(n_boot)):
        idx = rng.integers(0, n, size=n)
        vals[b] = float(refused[idx].mean())
    lo = float(np.percentile(vals, 100.0 * alpha / 2.0))
    hi = float(np.percentile(vals, 100.0 * (1.0 - alpha / 2.0)))
    return {
        "point": round(point, 4),
        "lo": round(lo, 4),
        "hi": round(hi, 4),
        "n": n,
        "n_boot": int(n_boot),
        "n_valid": int(vals.size),
        "seed": int(seed),
        "alpha": float(alpha),
        "method": "percentile",
    }


def summarise_rates(rates: list[float]) -> dict:
    """Stability summary over a list of subsample rates."""
    a = np.asarray([float(x) for x in rates], dtype=float)
    if a.size == 0:
        return {"n_reps": 0}
    return {
        "n_reps": int(a.size),
        "rates": [round(float(x), 4) for x in a.tolist()],
        "mean": round(float(a.mean()), 4),
        "sd": round(float(a.std(ddof=1)), 4) if a.size > 1 else 0.0,
        "min": round(float(a.min()), 4),
        "max": round(float(a.max()), 4),
        "p025": round(float(np.percentile(a, 2.5)), 4),
        "p975": round(float(np.percentile(a, 97.5)), 4),
    }


# --------------------------------------------------------------------------- #
# one run: gate + thresholds -> rung-4 block
# --------------------------------------------------------------------------- #
def gate_assert(gate, full: dict, n_dev_ids: int) -> dict:
    info = gate.info()
    diffs = [abs(float(info["coef"][c]) - float(full["gate"]["coef"][c])) for c in G.GATE_FEATURES]
    diffs.append(abs(float(info["intercept"]) - float(full["gate"]["intercept"])))
    max_diff = float(max(diffs)) if diffs else 0.0
    return {
        "passed": bool(max_diff <= COEF_TOL),
        "max_absdiff": round(max_diff, 10),
        "tolerance": COEF_TOL,
        "n_dev_ids": int(n_dev_ids),
        "coef": info["coef"],
        "intercept": info["intercept"],
    }


def run_block(gate, feats, items, full: dict, stored: dict) -> dict:
    """Rung-4 numbers for one run from freshly scored test items.

    stored = {"exploratory": value, "confirmatory": value, "auroc": value}
    holding the results_full.json abstain precisions (recall definition)
    and the answerable-vs-rung4 AUROC, for a match/mismatch check.
    """
    test_items = [it for it in items if it["split"] == "test" and it["item_id"] in feats]
    r0_ids = [it["item_id"] for it in test_items if it["rung"] == 0]
    r4_ids = [it["item_id"] for it in test_items if it["rung"] == 4]
    # sort by item_id for determinism (item order is otherwise preserved)
    r0_ids = sorted(r0_ids)
    r4_ids = sorted(r4_ids)
    s0 = gate.score(feats, r0_ids)
    s4 = gate.score(feats, r4_ids)

    band = full["thresholds"]["band"]
    expl = full["exploratory"]["operating_point"]["band"]
    ops = {
        "confirmatory_band": {"t_lo": float(band["t_lo"]), "t_hi": float(band["t_hi"])},
        "exploratory_band": {"t_lo": float(expl["t_lo"]), "t_hi": float(expl["t_hi"])},
    }

    auroc = auroc_answerable_vs_rung4(s0, s4)
    out: dict = {
        "thresholds": ops,
        "auroc_answerable_vs_rung4": auroc,
        "stored_auroc": stored["auroc"],
        "auroc_matches_stored": bool(abs(auroc - float(stored["auroc"])) <= 1e-4),
        "n_answerable": len(r0_ids),
        "n_rung4": len(r4_ids),
    }
    # refused arrays kept for subsampling (exploratory band is primary)
    refused_by_op = {}
    for name, op in ops.items():
        ref0 = G.refused_band(s0, op["t_lo"], op["t_hi"])
        ref4 = G.refused_band(s4, op["t_lo"], op["t_hi"])
        refused_by_op[name] = ref4
        pt = rung4_point(ref4, ref0, s4, s0, None)
        pt["auroc"] = auroc
        out[name] = pt

    # stored comparison (recall definition)
    out["confirmatory_matches_stored"] = bool(
        abs(out["confirmatory_band"]["abstain_precision"] - float(stored["confirmatory"])) <= 1e-9
    )
    out["exploratory_matches_stored"] = bool(
        abs(out["exploratory_band"]["abstain_precision"] - float(stored["exploratory"])) <= 1e-9
    )
    out["_refused_r4"] = refused_by_op  # popped by caller, never serialised
    return out


# --------------------------------------------------------------------------- #
# main builder
# --------------------------------------------------------------------------- #
def build_result() -> dict:
    items = load_items_jsonl(DATA / "items.jsonl")
    full_f = json.loads((RESULTS / "c1" / "results_full.json").read_text(encoding="utf-8"))
    full_c = json.loads((RESULTS / "c1_corrected" / "results_full.json").read_text(encoding="utf-8"))

    # stored rung-4 values from results_full.json (recall definition)
    stored = {
        "frozen": {
            "confirmatory": float(full_f["test"]["band_primary"]["per_rung"]["4"]["abstain_precision"]),
            "exploratory": float(full_f["test"]["exploratory_band"]["per_rung"]["4"]["abstain_precision"]),
            "auroc": float(full_f["test"]["band_primary"]["per_rung"]["4"]["auroc_answerable_vs_this_rung"]),
        },
        "corrected": {
            "confirmatory": float(full_c["test"]["band_primary"]["per_rung"]["4"]["abstain_precision"]),
            "exploratory": float(full_c["test"]["exploratory_band"]["per_rung"]["4"]["abstain_precision"]),
            "auroc": float(full_c["test"]["band_primary"]["per_rung"]["4"]["auroc_answerable_vs_this_rung"]),
        },
    }

    input_paths = {
        "items": "04_experiments/data/items.jsonl",
        "features": "04_experiments/data/features.csv",
        "features_corrected": "04_experiments/data/features_corrected.csv",
        "frozen_results_full": "04_experiments/results/c1/results_full.json",
        "corrected_results_full": "04_experiments/results/c1_corrected/results_full.json",
        "frozen_predictions": "04_experiments/results/c1/predictions.csv",
        "corrected_predictions": "04_experiments/results/c1_corrected/predictions.csv",
        "summary": "04_experiments/results/c1_corrected/SUMMARY.md",
    }
    sha = {k: sha256_file(ROOT / v) for k, v in input_paths.items()}

    # gates
    feats_f = G.load_features(DATA / "features.csv")
    feats_c = G.load_features(DATA / "features_corrected.csv")
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    g_f = G.fit_logistic_gate(feats_f, dev_ids)
    g_c = G.fit_logistic_gate(feats_c, dev_ids)

    frozen = run_block(g_f, feats_f, items, full_f, stored["frozen"])
    corrected = run_block(g_c, feats_c, items, full_c, stored["corrected"])
    ref_frozen = frozen.pop("_refused_r4")
    ref_corrected = corrected.pop("_refused_r4")

    # ---- robustness on the exploratory band (primary mechanistic contrast) ----
    def robustness(refused: np.ndarray, point: float) -> dict:
        subs: dict = {}
        for seed in SUBSAMPLE_SEEDS:
            rates = subsample_rates(refused, frac=SUBSAMPLE_FRAC,
                                    n_reps=N_SUBSAMPLE_REPS, seed=seed)
            s = summarise_rates(rates)
            s["seed"] = int(seed)
            s["frac"] = SUBSAMPLE_FRAC
            s["sample_n"] = int(round(SUBSAMPLE_FRAC * len(refused)))
            # fraction of subsamples on each side of the full-sample point
            s["frac_subsamples_at_or_above_point"] = round(
                float(np.mean(np.asarray(rates) >= point)), 4)
            s["frac_subsamples_at_or_below_point"] = round(
                float(np.mean(np.asarray(rates) <= point)), 4)
            subs[str(seed)] = s
        boots = {}
        for seed in BOOT_SEEDS:
            boots[str(seed)] = bootstrap_rate_ci(refused, n_boot=BOOT_N, seed=seed)
        return {
            "operating_point": "exploratory_band",
            "subsample": subs,
            "bootstrap": boots,
        }

    pt_f_expl = float(frozen["exploratory_band"]["abstain_precision"])
    pt_c_expl = float(corrected["exploratory_band"]["abstain_precision"])
    robust_frozen = robustness(ref_frozen["exploratory_band"], pt_f_expl)
    robust_corrected = robustness(ref_corrected["exploratory_band"], pt_c_expl)

    # gap stability: registered minus corrected, per paired rep index
    gap_full = round(pt_f_expl - pt_c_expl, 4)
    gaps = {}
    for seed in SUBSAMPLE_SEEDS:
        rf = robust_frozen["subsample"][str(seed)]["rates"]
        rc = robust_corrected["subsample"][str(seed)]["rates"]
        g = [round(a - b, 4) for a, b in zip(rf, rc)]
        gs = summarise_rates(g)
        gaps[str(seed)] = gs

    out = {
        "experiment": "c1",
        "stage": "r3_exp_r4_robust",
        "generated_by": "04_experiments/src/r3_exp_r4_robust.py",
        "command": COMMAND,
        "commands": [COMMAND, COMMAND + " --check-repro"],
        "exploratory": True,
        "post_hoc": True,
        "label": "exploratory/post-hoc",
        "note": (
            "R4 registered (frozen, passage-as-query dense) vs corrected "
            "(question-as-query dense). All gates and thresholds re-derived "
            "from dev; thresholds read from each run's results_full.json, "
            "never refit here. Abstain precision = fraction refused on the "
            "rung-4 negatives (gate.metrics_block definition); true "
            "P(rung4 | refused) is reported alongside. Robustness: 50% "
            "subsample without replacement (20 reps, seeds 999 and 2024) "
            "plus percentile bootstrap with replacement (2000 reps, seeds "
            "999 and 2024) on the exploratory band."
        ),
        "input_paths": input_paths,
        "inputs": sha,
        "sha256_inputs": sha,
        "design": {
            "subsample_frac": SUBSAMPLE_FRAC,
            "n_subsample_reps": N_SUBSAMPLE_REPS,
            "subsample_seeds": list(SUBSAMPLE_SEEDS),
            "bootstrap_n": BOOT_N,
            "bootstrap_seeds": list(BOOT_SEEDS),
            "alpha": ALPHA,
            "split": "test",
            "pool": "rung-4 items vs rung-0 answerable items (AUROC); rung-4 items only (refusal rate)",
        },
        "runs": {
            "registered": {
                "label": "registered / frozen",
                "features_csv": "04_experiments/data/features.csv",
                "results_full": "04_experiments/results/c1/results_full.json",
                "gate_assertion": gate_assert(g_f, full_f, len(dev_ids)),
                **frozen,
                "robustness": robust_frozen,
            },
            "corrected": {
                "label": "corrected",
                "features_csv": "04_experiments/data/features_corrected.csv",
                "results_full": "04_experiments/results/c1_corrected/results_full.json",
                "gate_assertion": gate_assert(g_c, full_c, len(dev_ids)),
                **corrected,
                "robustness": robust_corrected,
            },
        },
        "table": {
            "registered": {
                "exploratory_rung4": pt_f_expl,
                "confirmatory_rung4": float(frozen["confirmatory_band"]["abstain_precision"]),
                "auroc_rung4": float(frozen["auroc_answerable_vs_rung4"]),
            },
            "corrected": {
                "exploratory_rung4": pt_c_expl,
                "confirmatory_rung4": float(corrected["confirmatory_band"]["abstain_precision"]),
                "auroc_rung4": float(corrected["auroc_answerable_vs_rung4"]),
            },
            "gap_exploratory_registered_minus_corrected": gap_full,
        },
        "stability": {
            "gap_by_subsample_seed": gaps,
            "gap_full_sample": gap_full,
        },
    }
    return out


def _compare_results(a: dict, b: dict) -> bool:
    return a.get("table") == b.get("table") and a.get("runs") == b.get("runs") and a.get("stability") == b.get("stability")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="R4 registered vs corrected robustness (exploratory/post-hoc).")
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    ap.add_argument("--check-repro", action="store_true")
    args = ap.parse_args(argv)

    result = build_result()
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if args.check_repro and out_path.exists():
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        ok = _compare_results(existing, result)
        print("REPRO CHECK:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fr = result["runs"]["registered"]
    co = result["runs"]["corrected"]
    print("wrote", out_path)
    print(f"registered R4 expl={fr['exploratory_band']['abstain_precision']} conf={fr['confirmatory_band']['abstain_precision']} auroc={fr['auroc_answerable_vs_rung4']}")
    print(f"corrected  R4 expl={co['exploratory_band']['abstain_precision']} conf={co['confirmatory_band']['abstain_precision']} auroc={co['auroc_answerable_vs_rung4']}")
    for seed in SUBSAMPLE_SEEDS:
        sf = result["runs"]["registered"]["robustness"]["subsample"][str(seed)]
        sc = result["runs"]["corrected"]["robustness"]["subsample"][str(seed)]
        print(f"seed={seed} subsample 50%x20: registered mean={sf['mean']} sd={sf['sd']} [{sf['p025']},{sf['p975']}] | corrected mean={sc['mean']} sd={sc['sd']} [{sc['p025']},{sc['p975']}]")
    for seed in BOOT_SEEDS:
        bf = result["runs"]["registered"]["robustness"]["bootstrap"][str(seed)]
        bc = result["runs"]["corrected"]["robustness"]["bootstrap"][str(seed)]
        print(f"seed={seed} bootstrap CI: registered [{bf['lo']},{bf['hi']}] | corrected [{bc['lo']},{bc['hi']}]")
    print(f"gap registered-corrected (expl) = {result['table']['gap_exploratory_registered_minus_corrected']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
