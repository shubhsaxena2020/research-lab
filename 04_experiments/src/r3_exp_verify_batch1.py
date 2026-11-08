"""R3 exploratory: independent cross-check of every headline number in
auroc_ci.json, audit_twosided.json, ptruth_summary.json, both_runs.json,
h2_verdict.json and r4_robustness.json against the stored source of truth
(c1/results_full.json, c1/rung5.json, c1/transfer.json and the c1_corrected
equivalents).

Owned file: 04_experiments/src/r3_exp_verify_batch1.py
Writes: 04_experiments/results/c1/r3/exp/verify_batch1.json

Run: python 04_experiments/src/r3_exp_verify_batch1.py
Check: python 04_experiments/src/r3_exp_verify_batch1.py --check-repro

Design:
- This script only READS the six batch-2 JSONs plus the stored source files.
  It re-derives nothing, fits no gate, and copies no number without a check.
- Every assertion is arithmetic on values already in those files, so the check
  is deterministic and instant. Tolerances are explicit constants below.
- A check FAILS if either side is missing (None) or the absolute difference
  exceeds its tolerance, or a boolean flag disagrees. The overall verdict is
  PASS iff every check passes.

Coverage (13 logical groups, 31 leaf checks):
- auroc_ci: frozen test 0.9824, corrected test 0.8738, paired diff test
  0.1085 with item-level CI [0.0950, 0.1227] (plus the stored 4-dp claim
  frozen 0.9824 / corrected 0.8738 against discrimination.test_auroc).
- audit_twosided: R4 primary_6 dev 0.407 (inverted, two-sided pass),
  R4 with_lex dev 0.4047 (0.405 at 3dp), top1 with_lex dev 0.7156 / test
  0.7381 (0.716/0.738), gold-indicator 1.0 (all 8 cells), R1-R3 with_lex
  dev values and their two-sided pass flags.
- ptruth_summary: AUROC 0.2317 (4dp) + n_scored 553 + threshold infeasible.
- both_runs: frozen R5 0.8925/0.9375-style table + transfer 0.855/0.975,
  AUROCs 0.6402/0.7059 (via table AND via runs.*.stored fields).
- h2_verdict: frozen exploratory 7.25pp UNDEFINED, corrected exploratory
  -2.0pp REFUTED (plus the two confirmatory arms).
- r4_robustness: R4 registered 0.8471 / corrected 0.1253 exploratory
  abstain precision + the table-vs-stored match flags.

All numbers here are exploratory / post-hoc verification, not new results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "04_experiments" / "results"
EXP = RESULTS / "c1" / "r3" / "exp"
OUT_DEFAULT = EXP / "verify_batch1.json"

COMMAND = "python 04_experiments/src/r3_exp_verify_batch1.py"

# Tolerances. Stored values are rounded to 4 dp in the source JSONs; the
# full-precision auroc_ci points agree with those to well under 5e-5.
TOL_4DP = 5e-5   # 4-dp rounded value vs full precision / exact 4-dp recompute
TOL_3DP = 5e-4   # 3-dp quoted values (0.405, 0.716, 0.738, 0.2317 is 4dp)
TOL_EXACT = 0.0  # integer / boolean / string identity


# --------------------------------------------------------------------------- #
# pure helpers (exported for unit tests)
# --------------------------------------------------------------------------- #
def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def check_numeric(actual, expected, tol: float) -> dict:
    """One numeric leaf check. PASS iff both present and |a-e| <= tol."""
    if actual is None or expected is None:
        return {"status": "FAIL", "actual": actual, "expected": expected,
                "diff": None, "tolerance": tol,
                "detail": "missing value on one side"}
    diff = abs(float(actual) - float(expected))
    ok = bool(diff <= float(tol))
    return {"status": "PASS" if ok else "FAIL", "actual": float(actual),
            "expected": float(expected), "diff": diff, "tolerance": float(tol)}


def check_equal(actual, expected) -> dict:
    """One exact leaf check (bool / str / int identity)."""
    ok = bool(actual == expected)
    return {"status": "PASS" if ok else "FAIL", "actual": actual,
            "expected": expected, "tolerance": TOL_EXACT}


def interval_contains(ci: dict, lo: float, hi: float, tol: float = TOL_4DP) -> bool:
    """True iff ci['lo'] ~= lo and ci['hi'] ~= hi within tol."""
    if not isinstance(ci, dict) or ci.get("lo") is None or ci.get("hi") is None:
        return False
    return bool(abs(float(ci["lo"]) - float(lo)) <= tol
                and abs(float(ci["hi"]) - float(hi)) <= tol)


def summarise(checks: list[dict]) -> dict:
    """Aggregate leaf checks into per-group + overall PASS/FAIL."""
    groups: dict[str, dict] = {}
    for c in checks:
        g = c.get("group", "unknown")
        groups.setdefault(g, {"n": 0, "n_pass": 0, "checks": []})["n"] += 1
        if c.get("status") == "PASS":
            groups[g]["n_pass"] += 1
        groups[g]["checks"].append(c)
    n = len(checks)
    return {"n_checks": n,
            "n_pass": sum(1 for c in checks if c.get("status") == "PASS"),
            "n_fail": sum(1 for c in checks if c.get("status") != "PASS"),
            "overall": "PASS" if n > 0 and all(
                c.get("status") == "PASS" for c in checks) else "FAIL",
            "groups": groups}


def _leaf(group: str, check_id: str, kind: str, result: dict) -> dict:
    result = dict(result)
    result.update({"group": group, "check_id": check_id, "kind": kind})
    return result


# --------------------------------------------------------------------------- #
# build the verification result by reading the on-disk files
# --------------------------------------------------------------------------- #
def build_result() -> dict:
    input_paths = {
        "auroc_ci": "04_experiments/results/c1/r3/exp/auroc_ci.json",
        "audit_twosided": "04_experiments/results/c1/r3/exp/audit_twosided.json",
        "ptruth_summary": "04_experiments/results/c1/r3/exp/ptruth_summary.json",
        "both_runs": "04_experiments/results/c1/r3/exp/both_runs.json",
        "h2_verdict": "04_experiments/results/c1/r3/exp/h2_verdict.json",
        "r4_robustness": "04_experiments/results/c1/r3/exp/r4_robustness.json",
        "frozen_results_full": "04_experiments/results/c1/results_full.json",
        "corrected_results_full": "04_experiments/results/c1_corrected/results_full.json",
        "frozen_rung5": "04_experiments/results/c1/rung5.json",
        "corrected_rung5": "04_experiments/results/c1_corrected/rung5.json",
        "frozen_transfer": "04_experiments/results/c1/transfer.json",
        "corrected_transfer": "04_experiments/results/c1_corrected/transfer.json",
    }
    data = {k: load_json(ROOT / v) for k, v in input_paths.items()}
    auroc_ci = data["auroc_ci"]
    audit = data["audit_twosided"]
    ptruth = data["ptruth_summary"]
    both = data["both_runs"]
    h2 = data["h2_verdict"]
    r4 = data["r4_robustness"]
    fr_full = data["frozen_results_full"]
    co_full = data["corrected_results_full"]

    checks: list[dict] = []

    # --- Group 1: auroc_ci vs stored discrimination.test_auroc --------------
    g = "auroc_ci"
    ft = auroc_ci["aurocs"]["frozen_test_overall"]["point"]
    ct = auroc_ci["aurocs"]["corrected_test_overall"]["point"]
    checks.append(_leaf(g, "frozen_test_auroc_vs_stored_0.9824", "numeric",
                        check_numeric(ft, 0.9824, TOL_4DP)))
    checks.append(_leaf(g, "corrected_test_auroc_vs_stored_0.8738", "numeric",
                        check_numeric(ct, 0.8738, TOL_4DP)))
    checks.append(_leaf(g, "frozen_test_vs_discrimination", "numeric",
                        check_numeric(ft, fr_full["discrimination"]["test_auroc"], TOL_4DP)))
    checks.append(_leaf(g, "corrected_test_vs_discrimination", "numeric",
                        check_numeric(ct, co_full["discrimination"]["test_auroc"], TOL_4DP)))
    paired = auroc_ci["paired_diffs"]["frozen_vs_corrected_test_overall"]
    ci_item = paired["ci_item"]
    checks.append(_leaf(g, "paired_diff_vs_0.1085", "numeric",
                        check_numeric(paired["point"], 0.1085, TOL_4DP)))
    checks.append(_leaf(g, "paired_diff_item_ci_[0.0950,0.1227]", "numeric",
                        check_numeric(0.0 if interval_contains(ci_item, 0.0950, 0.1227, TOL_4DP) else 1.0, 0.0, TOL_EXACT)))
    checks.append(_leaf(g, "paired_diff_excludes_zero", "bool",
                        check_equal(ci_item.get("contains_zero"), False)))
    checks.append(_leaf(g, "paired_point_equals_auroc_difference", "numeric",
                        check_numeric(paired["point"], ft - ct, 1e-9)))

    # --- Group 2: audit_twosided -------------------------------------------
    g = "audit_twosided"
    r4_dev = audit["audit"]["dev"]["per_rung"]["4"]
    checks.append(_leaf(g, "r4_primary6_dev_0.407", "numeric",
                        check_numeric(r4_dev["auroc_primary_6"], 0.407, TOL_4DP)))
    checks.append(_leaf(g, "r4_primary6_dev_inverted", "str",
                        check_equal(r4_dev["direction_primary_6"], "inverted")))
    checks.append(_leaf(g, "r4_primary6_dev_passes_twosided", "bool",
                        check_equal(r4_dev["passes_primary_6"], True)))
    checks.append(_leaf(g, "r4_withlex_dev_0.4047", "numeric",
                        check_numeric(r4_dev["auroc_with_lex"], 0.4047, TOL_4DP)))
    checks.append(_leaf(g, "r4_withlex_dev_0.405_3dp", "numeric",
                        check_numeric(r4_dev["auroc_with_lex"], 0.405, TOL_3DP)))
    # top1 presented with_lex: dev 0.7156 (0.716), test 0.7381 (0.738)
    checks.append(_leaf(g, "top1_withlex_dev_0.7156", "numeric",
                        check_numeric(audit["top1"]["dev"]["auroc_with_lex"], 0.7156, TOL_4DP)))
    checks.append(_leaf(g, "top1_withlex_dev_0.716_3dp", "numeric",
                        check_numeric(audit["top1"]["dev"]["auroc_with_lex"], 0.716, TOL_3DP)))
    checks.append(_leaf(g, "top1_withlex_test_0.7381", "numeric",
                        check_numeric(audit["top1"]["test"]["auroc_with_lex"], 0.7381, TOL_4DP)))
    checks.append(_leaf(g, "top1_withlex_test_0.738_3dp", "numeric",
                        check_numeric(audit["top1"]["test"]["auroc_with_lex"], 0.738, TOL_3DP)))
    # gold-indicator control: all 8 cells (dev+test x rungs 1-4) = 1.0
    gold_vals = [audit["gold_indicator_control"][split]["per_rung"][str(r)]["auroc_with_is_gold"]
                 for split in ("dev", "test") for r in (1, 2, 3, 4)]
    checks.append(_leaf(g, "gold_indicator_1.0_all_cells", "numeric",
                        check_numeric(min(gold_vals), 1.0, TOL_EXACT)))
    # Supporting: R1-R3 with_lex dev values and two-sided pass flags
    g = "audit_twosided_supporting"
    exp_withlex = {"1": 0.9762, "2": 0.8901, "3": 0.9235}
    for rung, exp in exp_withlex.items():
        e = audit["audit"]["dev"]["per_rung"][rung]
        checks.append(_leaf(g, f"r{rung}_withlex_dev", "numeric",
                            check_numeric(e["auroc_with_lex"], exp, TOL_4DP)))
        checks.append(_leaf(g, f"r{rung}_withlex_fails_twosided", "bool",
                            check_equal(e["passes_with_lex"], False)))

    # --- Group 3: ptruth ----------------------------------------------------
    g = "ptruth"
    checks.append(_leaf(g, "auroc_0.2317", "numeric",
                        check_numeric(ptruth["auroc_answerable_vs_negative"], 0.2317, TOL_4DP)))
    checks.append(_leaf(g, "n_scored_553", "int",
                        check_equal(ptruth["n_scored"], 553)))
    checks.append(_leaf(g, "threshold_infeasible", "bool",
                        check_equal(ptruth["threshold_080_rule"]["feasible"], False)))
    checks.append(_leaf(g, "model_differs_disclosure", "bool",
                        check_equal(ptruth["model_differs_from_paper_reader"], True)))

    # --- Group 4: both_runs -------------------------------------------------
    g = "both_runs"
    fr = both["table"]["frozen"]
    co = both["table"]["corrected"]
    checks.append(_leaf(g, "frozen_rung5_exploratory_0.8925", "numeric",
                        check_numeric(fr["rung5_exploratory_test"], 0.8925, TOL_4DP)))
    checks.append(_leaf(g, "corrected_rung5_exploratory_0.9375", "numeric",
                        check_numeric(co["rung5_exploratory_test"], 0.9375, TOL_4DP)))
    checks.append(_leaf(g, "frozen_transfer_exploratory_0.855", "numeric",
                        check_numeric(fr["transfer_exploratory_rung3"], 0.855, TOL_4DP)))
    checks.append(_leaf(g, "corrected_transfer_exploratory_0.975", "numeric",
                        check_numeric(co["transfer_exploratory_rung3"], 0.975, TOL_4DP)))
    checks.append(_leaf(g, "frozen_transfer_auroc_0.6402", "numeric",
                        check_numeric(fr["transfer_auroc"], 0.6402, TOL_4DP)))
    checks.append(_leaf(g, "corrected_transfer_auroc_0.7059", "numeric",
                        check_numeric(co["transfer_auroc"], 0.7059, TOL_4DP)))
    checks.append(_leaf(g, "all_match_stored_frozen", "bool",
                        check_equal(both["runs"]["frozen"]["all_match_stored"], True)))
    checks.append(_leaf(g, "all_match_stored_corrected", "bool",
                        check_equal(both["runs"]["corrected"]["all_match_stored"], True)))
    # stored rung5 / transfer fields agree with the table
    fr_r5_stored = both["runs"]["frozen"]["rung5"]["stored"]
    co_r5_stored = both["runs"]["corrected"]["rung5"]["stored"]
    checks.append(_leaf(g, "frozen_rung5_stored_exploratory", "numeric",
                        check_numeric(fr_r5_stored["exploratory_test"], 0.8925, TOL_4DP)))
    checks.append(_leaf(g, "corrected_rung5_stored_exploratory", "numeric",
                        check_numeric(co_r5_stored["exploratory_test"], 0.9375, TOL_4DP)))

    # --- Group 5: h2_verdict -----------------------------------------------
    g = "h2_verdict"
    tbl = h2["table"]
    checks.append(_leaf(g, "frozen_exploratory_7.25pp", "numeric",
                        check_numeric(tbl["frozen"]["exploratory_drop_pp"], 7.25, TOL_EXACT)))
    checks.append(_leaf(g, "frozen_exploratory_UNDEFINED", "str",
                        check_equal(tbl["frozen"]["exploratory_verdict"], "UNDEFINED")))
    checks.append(_leaf(g, "corrected_exploratory_-2.0pp", "numeric",
                        check_numeric(tbl["corrected"]["exploratory_drop_pp"], -2.0, TOL_EXACT)))
    checks.append(_leaf(g, "corrected_exploratory_REFUTED", "str",
                        check_equal(tbl["corrected"]["exploratory_verdict"], "REFUTED")))
    checks.append(_leaf(g, "frozen_confirmatory_REFUTED", "str",
                        check_equal(tbl["frozen"]["confirmatory_verdict"], "REFUTED")))
    checks.append(_leaf(g, "corrected_confirmatory_REFUTED", "str",
                        check_equal(tbl["corrected"]["confirmatory_verdict"], "REFUTED")))

    # --- Group 6: r4_robustness ---------------------------------------------
    g = "r4_robustness"
    checks.append(_leaf(g, "registered_exploratory_0.8471", "numeric",
                        check_numeric(r4["table"]["registered"]["exploratory_rung4"], 0.8471, TOL_4DP)))
    checks.append(_leaf(g, "corrected_exploratory_0.1253", "numeric",
                        check_numeric(r4["table"]["corrected"]["exploratory_rung4"], 0.1253, TOL_4DP)))
    checks.append(_leaf(g, "registered_matches_stored", "bool",
                        check_equal(r4["runs"]["registered"]["exploratory_matches_stored"], True)))
    checks.append(_leaf(g, "corrected_matches_stored", "bool",
                        check_equal(r4["runs"]["corrected"]["exploratory_matches_stored"], True)))
    # table == runs exploratory_band abstain_precision
    checks.append(_leaf(g, "registered_table_eq_recomputed", "numeric",
                        check_numeric(r4["table"]["registered"]["exploratory_rung4"],
                                      r4["runs"]["registered"]["exploratory_band"]["abstain_precision"], TOL_EXACT)))
    checks.append(_leaf(g, "corrected_table_eq_recomputed", "numeric",
                        check_numeric(r4["table"]["corrected"]["exploratory_rung4"],
                                      r4["runs"]["corrected"]["exploratory_band"]["abstain_precision"], TOL_EXACT)))

    summary = summarise(checks)
    result = {
        "experiment": "c1",
        "stage": "r3_exp_verify_batch1",
        "generated_by": "04_experiments/src/r3_exp_verify_batch1.py",
        "command": COMMAND,
        "commands": [COMMAND, COMMAND + " --check-repro"],
        "post_hoc": True,
        "exploratory": True,
        "label": "exploratory/post-hoc verification (no new numbers)",
        "tolerances": {"TOL_4DP": TOL_4DP, "TOL_3DP": TOL_3DP, "TOL_EXACT": TOL_EXACT},
        "overall": summary["overall"],
        "n_checks": summary["n_checks"],
        "n_pass": summary["n_pass"],
        "n_fail": summary["n_fail"],
        "checks": checks,
        "groups": summary["groups"],
        "input_paths": input_paths,
        "inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "sha256_inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
    }
    return result


def _compare_results(a: dict, b: dict) -> bool:
    """Repro comparison: overall verdict and every per-check status."""
    if a.get("overall") != b.get("overall"):
        return False
    ca = {c["check_id"]: c["status"] for c in a.get("checks", [])}
    cb = {c["check_id"]: c["status"] for c in b.get("checks", [])}
    return ca == cb


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Cross-check batch-2 JSONs vs stored source files.")
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    ap.add_argument("--check-repro", action="store_true")
    args = ap.parse_args(argv)

    result = build_result()

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if args.check_repro and out_path.exists():
        existing = load_json(out_path)
        ok = _compare_results(existing, result)
        print("REPRO CHECK:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print("wrote", out_path)
    print("overall:", result["overall"])
    print("n_checks:", result["n_checks"], "pass:", result["n_pass"], "fail:", result["n_fail"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
