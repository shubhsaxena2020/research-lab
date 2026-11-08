"""R3 exploratory: H2 operating-point transfer verdict (frozen + corrected).

Owned file: 04_experiments/src/r3_exp_h2_verdict.py
Writes: 04_experiments/results/c1/r3/exp/h2_verdict.json

Run: python 04_experiments/src/r3_exp_h2_verdict.py
Check: python 04_experiments/src/r3_exp_h2_verdict.py --check-repro

This is exploratory / post-hoc (D1.2 + D4). It does not change any
pre-registered verdict; it applies the preregistered H2 criterion to the
second-corpus drop already stored in transfer.json.

Definitions (PREREGISTRATION.md section 6):
- abstain precision = fraction refused on the rung's negatives; the same mean
  is named abstain recall. Hence recall(main rung3) == main rung3 precision
  and recall(transfer rung3) == transfer rung3 precision.
- over-refusal = fraction of rung-0 (answerable) items refused.
- drop = test rung3 abstain precision - transfer rung3 abstain precision,
  same gate, same thresholds (see drop_vs_test_rung3 in transfer.json).

H2 verdict rule (PREREGISTRATION.md section 1):
- SUPPORTED if drop >= 10pp
- REFUTED if drop is within +-5pp
- 5 < drop < 10 (and, symmetrically, drop < -5) is undefined: the preregistered
  binary rule does not classify it. This file reports it as UNDEFINED.
- H2 gets no p-value (D1.4): one side is the fitting half.
- The preregistered criterion is "at equal abstain recall"; the observed arms
  do NOT operate at equal recall (see equal_recall_check). Verdicts here are
  therefore precision-drop verdicts at frozen thresholds, not recall-matched.
- Corrected is D4 sensitivity analysis (exploratory); its confirmatory-band
  numbers cannot rescue or overturn the frozen confirmatory verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
RESULTS = ROOT / "04_experiments" / "results"
OUT_DEFAULT = RESULTS / "c1" / "r3" / "exp" / "h2_verdict.json"

sys.path.insert(0, str(SRC))

COMMAND = "python 04_experiments/src/r3_exp_h2_verdict.py"

# Preregistered H2 criterion (PREREGISTRATION.md section 1). Loss in points
# (100 * rate difference). SUPPORTED >= 10, REFUTED within +-5.
SUPPORTED_MIN_PP = 10.0
REFUTED_MAX_ABS_PP = 5.0

H2_VERBATIM = (
    "- **H2 (operating-point transfer).** The dev-fitted operating point, applied frozen to a\n"
    "  disjoint-article held-out half *and* to a second corpus, loses ≥ 10 points of abstain precision at\n"
    "  equal abstain recall relative to the dev figure.\n"
    "  *Refuted if* the loss is within ±5 points (i.e. it transfers), or if the second corpus is unavailable\n"
    "  (then H2 is reported as PARTIAL: within-corpus transfer only, and the second-corpus arm as NOT RUN)."
)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verdict_for_loss_pp(loss_pp: float) -> str:
    """Apply the preregistered binary rule; the 5-10 gap is UNDEFINED."""
    loss = float(loss_pp)
    if loss >= SUPPORTED_MIN_PP:
        return "SUPPORTED"
    if -REFUTED_MAX_ABS_PP <= loss <= REFUTED_MAX_ABS_PP:
        return "REFUTED"
    return "UNDEFINED"


def drop_pp(main_rung3: float, transfer_rung3: float) -> float:
    return round((float(main_rung3) - float(transfer_rung3)) * 100.0, 4)


def verdict_block(
    main_rung3: float,
    transfer_rung3: float,
    over_refusal_main: float,
    over_refusal_transfer: float,
    main_auroc: float | None = None,
    transfer_auroc: float | None = None,
    t_lo: float | None = None,
    t_hi: float | None = None,
) -> dict:
    loss_pp = drop_pp(main_rung3, transfer_rung3)
    verdict = verdict_for_loss_pp(loss_pp)
    # Per section 6, abstain recall == fraction refused on negatives ==
    # the rung-3 abstain precision itself.
    recall_main = round(float(main_rung3), 4)
    recall_transfer = round(float(transfer_rung3), 4)
    return {
        "main_test_rung3_precision": round(float(main_rung3), 4),
        "transfer_rung3_precision": round(float(transfer_rung3), 4),
        "main_recall_at_frozen_thresholds": recall_main,
        "transfer_recall_at_frozen_thresholds": recall_transfer,
        "recall_main_note": (
            "Per PREREGISTRATION.md section 6, abstain recall is the same mean as "
            "abstain precision (fraction refused on rung-3 negatives)."
        ),
        "over_refusal_main": round(float(over_refusal_main), 4),
        "over_refusal_transfer": round(float(over_refusal_transfer), 4),
        "drop_points": round(float(main_rung3) - float(transfer_rung3), 4),
        "drop_pp": round(loss_pp, 4),
        "direction": "loss" if loss_pp > 0 else ("gain" if loss_pp < 0 else "no_change"),
        "main_auroc_answerable_vs_rung3": (
            None if main_auroc is None else round(float(main_auroc), 4)
        ),
        "transfer_auroc_answerable_vs_rung3": (
            None if transfer_auroc is None else round(float(transfer_auroc), 4)
        ),
        "t_lo": None if t_lo is None else float(t_lo),
        "t_hi": None if t_hi is None else float(t_hi),
        "equal_recall_check": {
            "holds": bool(recall_main == recall_transfer),
            "abs_recall_gap_pp": round(abs(recall_main - recall_transfer) * 100.0, 4),
            "note": (
                "H2 requires equal abstain recall. equal_recall_check.holds reports "
                "whether this operating point meets it; the verdict is a "
                "frozen-threshold precision-drop verdict, not a recall-matched one "
                "unless holds is true."
            ),
        },
        "verdict": verdict,
        "criterion": "SUPPORTED if drop >= 10pp; REFUTED if drop within +-5pp; else UNDEFINED",
    }


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def build_result() -> dict:
    full_f = _load(RESULTS / "c1" / "results_full.json")
    full_c = _load(RESULTS / "c1_corrected" / "results_full.json")
    tr_f = _load(RESULTS / "c1" / "transfer.json")
    tr_c = _load(RESULTS / "c1_corrected" / "transfer.json")

    input_paths = {
        "frozen_results_full": "04_experiments/results/c1/results_full.json",
        "corrected_results_full": "04_experiments/results/c1_corrected/results_full.json",
        "frozen_transfer": "04_experiments/results/c1/transfer.json",
        "corrected_transfer": "04_experiments/results/c1_corrected/transfer.json",
    }

    def run_branch(full: dict, tr: dict) -> dict:
        drop = tr["drop_vs_test_rung3"]
        main_ref = tr["main_run_test_reference"]
        tr_ops = tr["transfer"]["operating_points"]
        thr = tr["thresholds"]
        # results_full cross-check sources (test rung3 + AUROC).
        test_band = full["test"]["band_primary"]
        test_expl = full["test"]["exploratory_band"]

        def auroc_from_full(test_obj: dict, rung: str = "3") -> float | None:
            try:
                return float(test_obj["per_rung"][rung]["auroc_answerable_vs_this_rung"])
            except (KeyError, TypeError, ValueError):
                return None

        branches = {}
        for key, ref_key, test_obj in (
            ("confirmatory", "band_primary", test_band),
            ("exploratory", "exploratory_band", test_expl),
        ):
            drop_key = (
                "confirmatory_band" if key == "confirmatory" else "exploratory_band"
            )
            main_prec = float(drop[drop_key]["test_rung3_precision"])
            transfer_prec = float(drop[drop_key]["transfer_rung3_precision"])
            # Stored drop check.
            stored_pp = float(drop[drop_key].get("drop_pp", drop_pp(main_prec, transfer_prec)))
            recomputed_pp = drop_pp(main_prec, transfer_prec)
            # Thresholds from transfer.json (same as results_full.json).
            t = thr[drop_key]
            blk = verdict_block(
                main_rung3=main_prec,
                transfer_rung3=transfer_prec,
                over_refusal_main=float(main_ref[ref_key]["over_refusal"]),
                over_refusal_transfer=float(
                    tr_ops[drop_key]["transfer_rung0_over_refusal"]
                ),
                main_auroc=auroc_from_full(test_obj),
                transfer_auroc=float(tr_ops[drop_key]["auroc_answerable_vs_rung3"]),
                t_lo=float(t["t_lo"]),
                t_hi=float(t["t_hi"]),
            )
            blk["stored_drop_pp"] = round(stored_pp, 4)
            blk["recomputed_drop_pp"] = round(recomputed_pp, 4)
            blk["stored_drop_matches"] = bool(
                abs(float(stored_pp) - float(recomputed_pp)) <= 1e-4
            )
            blk["main_ref_over_refusal_check"] = float(main_ref[ref_key]["over_refusal"])
            # results_full over-refusal check.
            blk["results_full_over_refusal"] = float(test_obj["over_refusal"])
            blk["results_full_over_refusal_matches"] = bool(
                abs(float(test_obj["over_refusal"]) - float(main_ref[ref_key]["over_refusal"]))
                <= 1e-4
            )
            blk["transfer_coverage"] = float(tr_ops[drop_key].get("coverage"))
            blk["transfer_ci95"] = tr_ops[drop_key].get("transfer_rung3_ci95")
            branches[key] = blk
        return branches

    frozen = run_branch(full_f, tr_f)
    corrected = run_branch(full_c, tr_c)

    gap_interpretation = {
        "h2_verbatim": H2_VERBATIM,
        "quote_source": "04_experiments/PREREGISTRATION.md section 1 (frozen; hash in PREREGISTRATION.sha256)",
        "supported_rule": "losses >= 10 points of abstain precision",
        "refuted_rule": "loss is within +-5 points (i.e. it transfers)",
        "gap_rule": (
            "The preregistered rule is binary and leaves (5, 10) points undefined: "
            "a 7.25pp drop is neither >= 10pp (not SUPPORTED) nor within +-5pp "
            "(not REFUTED). Symmetrically, a gain steeper than -5pp (loss < -5) "
            "is also not classified by the ±5 refutation rule. This file therefore "
            "reports UNDEFINED for such drops and does not treat them as support."
        ),
        "note": (
            "D1.4: H2 gets no p-value. Holm family is H1 and H3 only. "
            "The second-corpus construct differs from SQuAD (2WikiMultihopQA: no "
            "article grouping, shorter passages, multi-hop questions), so the "
            "second-corpus arm is a direction test only (see transfer.json "
            "construct_note)."
        ),
    }

    out = {
        "experiment": "c1",
        "stage": "r3_exp_h2_verdict",
        "generated_by": "04_experiments/src/r3_exp_h2_verdict.py",
        "command": COMMAND,
        "commands": [COMMAND, COMMAND + " --check-repro"],
        "exploratory": True,
        "post_hoc": True,
        "label": "exploratory/post-hoc",
        "note": (
            "Post-hoc application of the preregistered H2 criterion to the frozen "
            "and corrected second-corpus drops stored in transfer.json (D1.2 "
            "exploratory operating point, D4 corrected sensitivity analysis). "
            "The corrected confirmatory-band numbers are exploratory sensitivity "
            "only and cannot overturn the frozen confirmatory verdict."
        ),
        "h2_verbatim": H2_VERBATIM,
        "gap_interpretation": gap_interpretation,
        "input_paths": input_paths,
        "inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "sha256_inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "construct_note": tr_f.get("construct_note", "")[:500],
        "runs": {
            "frozen": {
                "label": "frozen (pre-registered gate; transfer.json frozen)",
                "confirmatory": frozen["confirmatory"],
                "exploratory": frozen["exploratory"],
            },
            "corrected": {
                "label": "corrected D4 sensitivity analysis (exploratory; cannot rescue H2)",
                "confirmatory": corrected["confirmatory"],
                "exploratory": corrected["exploratory"],
            },
        },
        "table": {
            "frozen": {
                "confirmatory_drop_pp": frozen["confirmatory"]["drop_pp"],
                "confirmatory_verdict": frozen["confirmatory"]["verdict"],
                "exploratory_drop_pp": frozen["exploratory"]["drop_pp"],
                "exploratory_verdict": frozen["exploratory"]["verdict"],
            },
            "corrected": {
                "confirmatory_drop_pp": corrected["confirmatory"]["drop_pp"],
                "confirmatory_verdict": corrected["confirmatory"]["verdict"],
                "exploratory_drop_pp": corrected["exploratory"]["drop_pp"],
                "exploratory_verdict": corrected["exploratory"]["verdict"],
            },
        },
    }
    return out


def _compare_results(a: dict, b: dict) -> bool:
    return (
        a.get("table") == b.get("table")
        and a.get("runs") == b.get("runs")
        and a.get("h2_verbatim") == b.get("h2_verbatim")
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="R3 exploratory H2 verdict.")
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
    out_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    for run_name in ("frozen", "corrected"):
        for op in ("confirmatory", "exploratory"):
            blk = result["runs"][run_name][op]
            print(
                f"{run_name} {op}: drop={blk['drop_pp']}pp "
                f"main={blk['main_test_rung3_precision']} "
                f"transfer={blk['transfer_rung3_precision']} "
                f"over_refusal main/transfer={blk['over_refusal_main']}/"
                f"{blk['over_refusal_transfer']} verdict={blk['verdict']}"
            )
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
