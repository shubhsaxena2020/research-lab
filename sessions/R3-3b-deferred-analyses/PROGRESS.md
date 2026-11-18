# R3-3b-deferred-analyses — PROGRESS

Owner: res-s1. Workdir: C:/Users/shubh/research-lab. All reported numbers are post-hoc/exploratory and live only under `04_experiments/results/c1/r3/R3-3b/`.

## Batch 1 — first blocking delegate_task (3 parallel tasks)

Dispatched exactly three tasks: MF-17, MF-10, MF-7 (2026-11-18). All returned completed.

### MF-17
- Script: `04_experiments/src/r3_r3_3b_mf17.py`
- JSON: `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json`
- Reports: `04_experiments/results/c1/r3/R3-3b/MF-17.md`; `sessions/R3-3b-deferred-analyses/reports/mf17.md`
- Child reported: seed 20261118, n_boot 10000, 111 prefixed flat keys, alignment id_sets_equal/labels_equal/rungs_equal true, 1879 common test items, 18 article clusters, REPRO CHECK PASS.
- Lead verification: JSON parses; top-level seed=20261118, n_boot=10000, label=exploratory/post-hoc; 111 flat keys; spot-checked frozen 0.9824 item CI [0.9776,0.9867], corrected 0.8738 [0.8587,0.8893], paired diff 0.1085 [0.0946,0.1225] excludes zero; top1 0.9453; transfer frozen 0.6402/corrected 0.7059; lexical audit 0.9773; gold-indicator controls flagged as artefacts. `--check-repro` launched in background (proc_21afbf9af4b0) because full recomputation exceeds 420 s.

### MF-10
- Script: `04_experiments/src/r3_r3_3b_mf10.py`
- JSON+labels+raw: `mf10_adjudication.json`, `mf10_label_A.csv`, `mf10_label_B.csv`, `mf10_resolve.csv`, `mf10_raw_responses.jsonl`, `mf10_rubric.md` under R3-3b.
- Reports: `MF-10.md`; `reports/mf10.md`
- Child reported: used sample.csv exactly (no resample), 100 items, 25/rung; Ollama 127.0.0.1:11434, qwen2.5:1.5b-instruct (A) + qwen3:1.7b (B/resolver), Ollama 0.40.16, llamacpp, Intel Arc 130T iGPU Vulkan, no CPU fallback; kappa 0.2802, po 0.59, 41 disagreements, resolved 56/100 answerable.
- Lead verification: re-ran script (resume path, 241 raw records unchanged); independently recomputed kappa=0.2801966292134831, A=62/100, B=21/100, resolver 56/100, resolver agrees with A on all 59 agreements and resolved 35/41 disagreements to 1. JSON has 40 prefixed result keys and GPU/model provenance.

### MF-7
- Script: `04_experiments/src/r3_r3_3b_mf7.py`
- JSON: `mf7_gold_control.json`; Reports: `MF-7.md`; `reports/mf7.md`
- Child reported: gold-indicator control per split/rung plus D3 pooled hit/miss sanity; bootstrap 20261118, 10000 resamples; CV/gate seed 12345; 294 prefixed keys; scope guard says no D3 R1–R3 estimand.
- Lead verification: re-ran script successfully; JSON parses; guard `per_rung_R1_R3_estimand_available=false`, `rungs_present_value=-1`; dev R1 base 0.9762, dev R4 base 0.4047, pooled D3 655 hits / 145 misses; bootstrap cross-check against `r3_exp_auroc_ci` reported max_abs_diff 0.0.

## Ownership / safety observed
- New files only under `04_experiments/src/r3_r3_3b_*.py`, `04_experiments/results/c1/r3/R3-3b/**`, `sessions/R3-3b-deferred-analyses/**`.
- No edits to draft/template/review/results-index/prereg/frozen/prior R3 results by this lane; no commits or pushes; provider/Hermes config untouched.
- Pre-existing dirty files in git status belong to other lanes and were not touched here.

## Batch 2 — independent verification and deliverables (3 parallel tasks)

- Independent review: `sessions/R3-3b-deferred-analyses/reports/batch2-review.md` — overall PASS, zero mismatches. Re-ran MF-10 and MF-7 scripts (byte-identical outputs); recomputed MF-17 point AUROCs (frozen 0.982363083164300, corrected 0.873848884381339, paired diff 0.108514198782961; absdiff 0 vs JSON); verified seed 20261118, n_boot 10000, 111 prefixed keys, kappa 0.2801966292134831, 241 raw records, MF-7 guard false/-1 and 655/145 pooled.
- ANSWERS.md: `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` created with 41 distinct dotted keys checked against the three JSON `results` objects; verdict/support limits and commands included.
- Ownership audit: `sessions/R3-3b-deferred-analyses/reports/batch2-ownership.md` — all lane output confined to the three owned path families; no frozen path written; no R3-3b commit or push. Anomaly: HEAD advanced from 88d6b57 to `ea82291ae66fc7bbbbc32d54b3014e7297cb3126` by another lane (R3-4d), which also committed the three R3-3b source scripts; this lane did not commit or push. Pre-existing other-lane dirty state untouched.
- MF-17 `--check-repro` background process (proc_21afbf9af4b0) exited 0 with exact output `REPRO CHECK: PASS | all compared sections match`.

## Final verification (lead)
- Deliverables present: `MF-17.md`, `MF-10.md`, `MF-7.md`, `ANSWERS.md`, three JSON result files, label/raw/provenance files for MF-10, three scripts `r3_r3_3b_{mf17,mf10,mf7}.py`, and five reports (three item reports + batch2 review + ownership).
- All new numbers exist only under `04_experiments/results/c1/r3/R3-3b/`; scripts only under `04_experiments/src/r3_r3_3b_*.py`; lane files only under `sessions/R3-3b-deferred-analyses/**`.
- MF-10 GPU/model provenance observed in `mf10_adjudication.json`: Ollama 0.40.16, 127.0.0.1:11434, llamacpp, Intel Arc 130T iGPU Vulkan, model digests and size_vram recorded, CPU fallback reason null.
- No draft/template/review/results-index/preregistration/frozen/prior-R3 artifact was edited by this lane; no commits or pushes by this lane.

CARD COMPLETE
