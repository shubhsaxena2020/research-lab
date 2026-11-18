# TASK R3-3b — deferred analyses from existing data

Lane: R3-3b-deferred-analyses; main laptop; profile res-s1; created 2026-11-18.

## Goal

Produce independent, reproducible post-hoc evidence for round-2 deferred items MF-7, MF-10, and MF-17 from existing predictions, labels, feature files, and passages only. Existing R3-3 artifacts already contain related results; treat them as comparison evidence, not as output from this lane. Do not replace or modify any prior result.

## Owned paths

- `04_experiments/src/r3_r3_3b_*.py` — new lane scripts only.
- `04_experiments/results/c1/r3/R3-3b/**` — all new result files, item reports, and ANSWERS.md.
- `sessions/R3-3b-deferred-analyses/**` — PROGRESS.md and reports.

Everything else is read-only. In particular, do not touch any R3-4d-owned path: `05_paper/template/**`, `05_paper/draft/**`, `05_paper/tables/**`, `05_paper/figures/**`, `06_review/**`, `04_experiments/RESULTS-INDEX.json`, or `04_experiments/src/make_paper_assets.py`. Never modify existing files under `04_experiments/results/**`, `04_experiments/runs/**`, `PREREGISTRATION.md`, or its hash history. No git commits, pushes, branch changes, Hermes configuration changes, gateway restart, or edits to `ops/hermes_runner.ps1`.

## Required first action and batching

Follow `ops/lead_protocol_r3.txt`. Your first action must be one blocking `delegate_task` call with exactly three parallel tasks, one each for MF-17, MF-10, and MF-7. Each task must state its exact owned write paths, read-only inputs, proof command, and report path under this lane's `reports/`. On later batches, include an independent review/re-run of prior work. Do not write any other paths.

## Analyses

1. **MF-17 AUROC intervals.** Recompute from existing per-item predictions, using fixed seed 20261118 and at least 10,000 bootstrap resamples. Assert item-id alignment before any paired difference. Report 95% intervals for the response-letter estimands: frozen and corrected held-out AUROC and their paired difference over the common held-out items; top-1 AUROC; transfer AUROC; and the gold-indicator/lexical audit AUROC. Give denominators, bootstrap method, input paths and sha256, exact command, seed, and post-hoc/exploratory label. Preserve any distinction between item and article-cluster resampling. Do not call these confirmatory or revise a frozen verdict.
2. **MF-10 answerability adjudication.** Use the existing seeded 100-item negative sample at `04_experiments/results/c1/r3/exp/adjudication/sample.csv`; do not resample. Obtain two independent labels per item and a resolver label for disagreements under a written rubric. Use the GPU-first route in COMMON.md rule 6: prefer local Ollama at `http://127.0.0.1:11434`, never localhost; record exact model/version, backend, available GPU device, prompts/rubric, and reason if any computation falls back to CPU. Do not call the result human gold. Report raw agreement, Cohen kappa, disagreement counts and resolution, and item counts by rung. Label this repeated LLM judgement post-hoc/exploratory and compare it cautiously with the earlier LLM adjudication. Preserve all raw model responses needed to audit labels; redact secrets.
3. **MF-7 gold-paragraph control.** Recompute the existing gold-indicator control from the existing item/features data and, if feasible from the same files, the D3 pooled top-1 hit/miss sanity comparison. Clearly state that the gold indicator is a construction/label artefact and that D3 has rung=-1 pooled hit/miss data, not per-rung R1-R3 observations. Do not claim the unavailable D3 per-rung estimand. Record command, fixed seed if used, input paths and hashes, denominators, and post-hoc/exploratory status.

## Deliverables

- New result files only under `04_experiments/results/c1/r3/R3-3b/`.
- `MF-17.md`, `MF-10.md`, and `MF-7.md`, each with the item, design, result, limitations, evidence file, exact JSON result keys an integrator can bind, and reproducibility command.
- `ANSWERS.md` mapping every item to its evidence, keys, and verdict/support limit.
- One report per subagent task under `sessions/R3-3b-deferred-analyses/reports/`.
- `PROGRESS.md` updated after each batch with commands and exact observed outcomes.

Use explicit result keys under a `results` object, prefixed `c1.r3_3b.mf17`, `c1.r3_3b.mf10`, or `c1.r3_3b.mf7`. Every numeric result file must record exact command, fixed seed, input SHA-256 values, and exploratory/post-hoc status. No draft edits. Do not say CARD COMPLETE until all reports and gates are independently checked; otherwise report the specific incomplete item.

## Verification

Independently open every subagent report and check its outputs and claims. Re-run the targeted scripts or proof commands. Confirm all writes stay within owned paths, all newly reported numbers are generated in new files under `R3-3b/`, no frozen/preregistration artifacts changed, and MF-10 records GPU/model provenance. Do not claim verification without observed output.
