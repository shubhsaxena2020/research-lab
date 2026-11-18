# Batch 2 independent review — R3-3b deferred analyses (MF-17, MF-10, MF-7)

Reviewer: independent subagent. All checks below were executed against the live
workspace `C:/Users/shubh/research-lab`; nothing was taken from the subagent
reports on trust. Exact observed values are recorded.

Method / safety notes:
- MF-10 and MF-7 were actually re-run. Before re-running, every file in
  `04_experiments/results/c1/r3/R3-3b/` was copied to a scratch backup; after the
  re-runs, all outputs were byte-compared and the originals (content **and**
  mtimes) restored. Final state of every result file is unchanged.
- MF-17 `--check-repro` was **not** run, per instruction (the lead has a
  background process for it). MF-17 was verified by parsing the JSON and
  independently recomputing point AUROCs with `sklearn.roc_auc_score`.

---

## MF-17 — `mf17_auroc_intervals.json`

| # | Check | Expected | Observed | Result |
|---|---|---|---|---|
| 1 | seed | 20261118 | `20261118` | PASS |
| 2 | n_boot | >= 10000 | `10000` | PASS |
| 3 | post_hoc | true | `True` | PASS |
| 4 | flat result key count | 111 | `111` | PASS |
| 5 | all flat keys prefixed `c1.r3_3b.mf17.` | yes | `all prefixed = True` (0 non-prefixed) | PASS |
| 6 | alpha | 0.05 | `0.05` | PASS |

Independent point-AUROC recomputation from the two `predictions.csv` files
(`results/c1/predictions.csv`, `results/c1_corrected/predictions.csv`), test rows,
common item ids, `band_score` as score, `label` as y, `sklearn.metrics.roc_auc_score`
(sklearn 1.9.1):

- common held-out items: **1879** (matches JSON alignment assertion).
- frozen: recomputed `0.982363083164300` vs JSON
  `...frozen_held_out_auroc.point = 0.982363083164300`; abs diff `0.000e+00`.
- corrected: recomputed `0.873848884381339` vs JSON
  `...corrected_held_out_auroc.point = 0.873848884381339`; abs diff `0.000e+00`.
- paired diff (frozen − corrected): recomputed `0.108514198782961` vs JSON
  `...paired_auroc_diff.diff = 0.108514198782961`; abs diff `0.000e+00`.
- JSON point difference `pt_f − pt_c = 0.108514198782961` equals the paired-diff
  value; abs diff `0.000e+00` (tolerance 1e-9). PASS.

Note on key naming: the paired-difference scalar is stored as `...paired_auroc_diff.diff`
(not `.point`), unlike the AUROC scalars. This is internally consistent and does
not affect any numeric claim; recording it here as an observation, not a mismatch.

Extra check: every nested result dict carrying `n_valid` shows `n_valid = 10000`
(27 such entries; no other value observed). PASS.

Report table spot checks all matched the JSON points: top1 `0.9452829495795234`,
transfer frozen `0.6401749999999999`, transfer corrected `0.7058749999999999`,
lexical audit `0.9772812500000001`, gold-indicator+lexical `1.0`. PASS.

## MF-10 — `r3_r3_3b_mf10.py` re-run + label recomputation

Re-run command: `python 04_experiments/src/r3_r3_3b_mf10.py` (resume path, Ollama
0.40.16 reachable at 127.0.0.1:11434). Exit code **0**. Observed stdout (verbatim):

```
DONE
n=100 agreed=59 disagreed=41 kappa=0.2801966292134831
A_answerable=62 B_answerable=21 resolved=56
  rung 1: n=25 disagreed=6 kappa=0.0
  rung 2: n=25 disagreed=9 kappa=0.29906542056074775
  rung 3: n=25 disagreed=18 kappa=0.025974025974026038
  rung 4: n=25 disagreed=8 kappa=0.13793103448275895
raw records: 241
```

This matches the subagent report's quoted stdout exactly. PASS.

| # | Check | Expected | Observed | Result |
|---|---|---|---|---|
| 1 | Cohen kappa from the two label CSVs via `r3_exp_adjudicate.cohens_kappa` | 0.2801966292134831 | `0.2801966292134831` (abs diff `0.000e+00`) | PASS |
| 2 | raw records | 241 | `241` (A=100, B=100, resolver=41) | PASS |
| 3 | label rows A / B / resolve | 100 / 100 / 100 | `100 / 100 / 100` | PASS |

Determinism: after the re-run, `mf10_label_A.csv`, `mf10_label_B.csv`,
`mf10_resolve.csv`, `mf10_adjudication.json`, `mf10_rubric.md`,
`mf10_raw_responses.jsonl`, `MF-10.md` were all byte-identical to the pre-run
backup (sha256 e.g. label A `d1691669...`, adjudication `2324d860...`). PASS.

Additional consistency: adjudication JSON stores `cohen_kappa_overall = 0.2802`
(rounded display) with `n_agreed = 59`, `n_disagreed = 41`, `raw_agreement_po = 0.59`,
rung kappas `0.0 / 0.2991 / 0.026 / 0.1379` — all consistent with the recomputed
full-precision values. PASS.

## MF-7 — `r3_r3_3b_mf7.py` re-run + JSON assertions

Re-run command: `python 04_experiments/src/r3_r3_3b_mf7.py`. Exit code **0**.
Observed stdout reported `n_result_keys: 294`, `seed: 20261118`, `n_boot: 10000`,
and bootstrap validation PASS for both levels (`item` and `cluster`,
`max_abs_diff: 0.0`, `n_boot_check: 200`, reference module
`04_experiments/src/r3_exp_auroc_ci.py`). PASS.

| # | Check | Expected | Observed | Result |
|---|---|---|---|---|
| 1 | scope guard `per_rung_R1_R3_estimand_available` | false | `False` | PASS |
| 2 | scope guard `rungs_present_value` | -1 | `-1` | PASS |
| 3 | flat result key count | 294 | `294` | PASS |
| 4 | all keys prefixed `c1.r3_3b.mf7.` | yes | `True` | PASS |
| 5 | pooled (rung=-1) hit / miss | 655 / 145 | `n_hit=655`, `n_miss=145` (`n=800`, `hit_rate=0.8187`) | PASS |
| 6 | seed / n_boot / post_hoc | 20261118 / 10000 / true | `20261118 / 10000 / True` | PASS |

Determinism: `mf7_gold_control.json` and `MF-7.md` were byte-identical to the
pre-run backup (sha256 `0728d927...` and `4eef149f...`). PASS.

Extra spot checks (all PASS): dev pooled 342/58 and test pooled 313/87 hits/misses;
gold control base AUROCs dev `0.9762 / 0.8901 / 0.9235 / 0.4047` and test
`0.9794 / 0.8614 / 0.9059 / 0.4332` reproduce the values quoted in the report;
`auroc_plus_is_gold = 1.0` with CI `[1.0, 1.0]` in all 8 dev/test × R1–R4 cells;
`is_gold` alone raw AUROC `0.0`, answerable-oriented `1.0`.

---

## Summary

- All requested checks for MF-17, MF-10 and MF-7: **PASS** (no FAIL).
- Mismatches found: **none**. The only non-conformity noted is the cosmetic
  `.diff` vs `.point` key name for the MF-17 paired difference; all numbers agree.
- Re-runs were deterministic: all regenerated result files were byte-identical to
  their originals, which were restored with original mtimes. No result file was
  left modified.
- Only file written in the repo: this report. Scratch verification scripts and
  backups live under the Hermes scratch dir, outside the repository.
- Not run (per instruction): MF-17 `--check-repro` (lead's background process).
