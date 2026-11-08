# ANSWERS — R3 exploratory (`c1/r3/exp`)

**Exploratory / post-hoc.** Every item below is exploratory unless the frozen
pre-registration already names it; none changes any pre-registered verdict.
Verdict = what the evidence supports for the MF item.
Full MF texts: `sessions/R3-3-experiments/TASK.md`; summaries in
`results/c1/r3/exp/adjudication/final_summary.md` (MF-10).

## MF-3 — R5/transfer under both runs, one table (re-derived)

Verdict: Done, exploratory. Frozen vs corrected: R5 exploratory 0.8925
(AUROC 0.9736) vs 0.9375 (AUROC 0.9728); transfer exploratory 0.855 @0.6402
vs 0.975 @0.7059; confirmatory transfer 0.985 vs 1.0.

Evidence: `both_runs.json` → `runs.{frozen,corrected}.rung5` /
`.transfer`, `all_match_stored = true` both runs (verified 10/10 in
`verify_batch1.json` → `both_runs`).

Command: `python 04_experiments/src/r3_exp_both_runs.py`
(`--check-repro` → REPRO CHECK: PASS).

Proposed draft sentence: "Re-derived under both runs, rung-5 exploratory
abstain precision is 0.8925 (frozen) versus 0.9375 (corrected), and transfer
is 0.855 @ AUROC 0.6402 versus 0.975 @ 0.7059; no number above was copied
from either summary."

## MF-6 — H2 verdict against the pre-registered rule (second corpus)

Verdict: Done, exploratory; frozen exploratory is **UNDEFINED**, everything
else REFUTED. Preregistered rule (PREREGISTRATION.md §1): SUPPORTED if the
drop is ≥ 10pp, REFUTED if within ±5pp — a 5–10pp drop is unclassified by
the rule, as is a gain steeper than −5pp. Frozen exploratory drop 7.25pp →
UNDEFINED (equal-recall check also fails, abs recall gap 7.25pp); corrected
exploratory −2.0pp → REFUTED (gain; equal-recall false); frozen confirmatory
1.5pp → REFUTED; corrected confirmatory 0.0pp → REFUTED. H2 carries no
p-value (Holm family is H1/H3 only).

Evidence: `h2_verdict.json` → `table`, `runs.*.*.verdict`,
`gap_interpretation` (`h2_verbatim` quoted from PREREGISTRATION.md §1);
verified 6/6 in `verify_batch1.json` → `h2_verdict`.

Command: `python 04_experiments/src/r3_exp_h2_verdict.py`
(`--check-repro` → REPRO CHECK: PASS).

Proposed draft sentence: "Against the preregistered H2 rule (≥ 10pp supported,
±5pp refuted), the frozen second-corpus drop of 7.25pp at the exploratory
operating point is unclassified rather than supportive; the corrected arm
gains 2.0pp and is refuted, and both confirmatory arms are refuted."

## MF-7 — "is this the gold paragraph" control

Verdict: Done, exploratory. Audit variant with gold-indicator control
(present-vs-absent gold paragraph); the control separates at AUROC 1.0 in all
8 dev/test × rung cells (shown to be a label-construction artefact, not a
substantive finding).

Evidence: `audit_twosided.json` → `gold_control` /
`gold_indicator_control`; verified 10/10 in `verify_batch1.json` →
`audit_twosided`.

Command: `python 04_experiments/src/r3_exp_audit_twosided.py`.

Proposed draft sentence: "A gold-paragraph indicator alone separates answerable
from negative at AUROC 1.0 in all eight dev/test by rung cells, so the
primary audit's separation partly reflects whether the passage is the gold
paragraph rather than rung hardness alone."

## MF-10 — answerability adjudication (100 negatives, two LLM labellers)

Verdict: Done, exploratory. 100 seeded negatives (25 per rung
1–4; 48 dev / 52 test). Cohen's κ = 0.1975 (observed agreement 0.74; 26
disagreements). Labeller A (qwen2.5:1.5b-instruct): 30/100 answerable;
labeller B (qwen3:1.7b): 6/100; neither used `ambiguous`. Confusion: both `0` = 69,
both `1` = 5, A=`1`/B=`0` = 25, A=`0`/B=`1` = 1 (one-directional: A is lax).
Per rung: rung 1 κ = 1.0 (0 disagreements); rung 2 κ = 0.359 (3); rung 3
κ = 0.359 (3); rung 4 κ = −0.055 (20/25 disagree). Third labeller
(qwen2.5:1.5b-instruct, strict rubric): resolved 5/100 (5%) answerable
(rung1 0%, rung2 4%, rung3 4%, rung4 12%); `resolve.csv` 100/100 filled.
Annotators are LLM agents per the TASK design, not human gold-standard
(disclosed in `adjudication.json`). Rung-0 positives were not sampled.

Evidence: `adjudication/label_A.csv`, `adjudication/label_B.csv`,
`adjudication/sample.csv`, `adjudication/resolve.csv` (100/100),
`adjudication/adjudication.json` (kappa 0.1975, resolved share 0.05),
`adjudication/rubric.md`; see `adjudication/final_summary.md`.

Command: `python 04_experiments/src/r3_exp_adjudicate.py --kappa`.

Proposed draft sentence: "In a seeded sample of 100 rung 1–4 negatives, two
independent LLM labellers agreed on whether the passage contains an answer
with κ = 0.20 (labeller A 30/100, labeller B 6/100; 20 of 26 disagreements
on rung 4); a third labeller resolved 5/100 (5%) of sampled negatives as
answerable (rung4 12%)."

## MF-12 — P(True)-style reader baseline (Kadavath et al.), 553 dev items

Verdict: Done, exploratory; **failure is not informative about reader-side
gating** (model and design differ from the paper's). AUROC 0.2317
answerable-vs-negative (inverted; reverse-direction 0.7683); the 0.80
threshold rule is infeasible (feasible = false, n_refused = 0). Reader is
`qwen2.5:1.5b-instruct` via Ollama `/api/generate` logprobs — not the
paper's pinned `Qwen/Qwen2.5-0.5B-Instruct`.

Evidence: `ptruth_summary.json` → `auroc_answerable_vs_negative`,
`threshold_080_rule.feasible`, `model_differs_from_paper_reader`;
`COMPUTE.md` (logprob support, top_logprobs ≤ 20); `ptruth_scores.csv`
(553 rows); verified 4/4 in `verify_batch1.json` → `ptruth`.

Command: `python 04_experiments/src/r3_exp_ptruth.py`.

Proposed draft sentence: "A P(True)-style reader baseline (qwen2.5:1.5b-instruct
via Ollama, not the paper's Qwen2.5-0.5B reader) achieves AUROC 0.232 in the
answerable-versus-negative direction (0.768 reversed) on 553 dev items, and
the 0.80 threshold rule is infeasible, so we do not treat the reader-side
baseline's failure as evidence about reader-side gating."

## MF-13 — two-sided separability audit (R4 inversion explicit)

Verdict: Done, exploratory. Two-sided rule |AUROC − 0.5| ≤ 0.25. R4 primary_6
dev AUROC 0.407 (inverted, passes); R4 with_lex dev 0.4047 (inverted,
passes). R1–R3 with_lex dev 0.9762 / 0.8901 / 0.9235 fail two-sided as
expected. Top-1-presented: primary 0.504 / 0.571, with_lex 0.716 / 0.738
(both pass).

Evidence: `audit_twosided.json` → `pass_rule`, `dev.per_rung`,
`gold_control`; verified 10/10 + 6/6 in `verify_batch1.json` →
`audit_twosided`, `audit_twosided_supporting`.

Command: `python 04_experiments/src/r3_exp_audit_twosided.py`.

Proposed draft sentence: "Under a two-sided separability rule (|AUROC − 0.5| ≤
0.25), rung 4 is inverted on the primary_6 audit (dev AUROC 0.407) while
rungs 1–3 separate strongly with the lex feature (0.976, 0.890, 0.924), so
rungs are not uniformly unordered only under the primary feature set."

## MF-14 — R4 registered vs post-hoc cell, side by side + robustness

Verdict: Done, exploratory. Registered (frozen) exploratory 0.8471 vs
corrected 0.1253; AUROC 0.9681 vs 0.5730; gap 0.7218, stable across 50%
subsamples (20 reps, seeds 999/2024) and percentile-bootstrap CIs
(registered [0.815, 0.885], corrected [0.093, 0.158]). Confirmatory 1.0 vs
0.9073. The mechanistic conclusion therefore rests on the registered
(passage-as-query) cell and collapses under the spec-conformant
(question-as-query) rewrite — the paper should say so.

Evidence: `r4_robustness.json` → `table`, `runs.*.exploratory_band`,
`robustness`, `stability`; verified 6/6 in `verify_batch1.json` →
`r4_robustness`.

Command: `python 04_experiments/src/r3_exp_r4_robust.py`
(`--check-repro` → REPRO CHECK: PASS).

Proposed draft sentence: "Rung-4 exploratory abstain precision is 0.8471
under the registered passage-as-query analysis but 0.1253 under the
spec-conformant question-as-query analysis (AUROC 0.9681 vs 0.5730), robust
to 50% subsampling and bootstrap (gap 0.72 in both), so the rung-4 mechanism
is reported as a property of the registered feature construction."

## MF-17 — AUROC intervals + paired difference (0.982 → 0.874)

Verdict: Done, exploratory. Frozen test AUROC 0.9824, 95% CI [0.9774, 0.9869];
corrected test AUROC 0.8738, 95% CI [0.8585, 0.8887]; paired difference on
identical items 0.1085, CI [0.0950, 0.1227] (excludes zero). Plugin
percentile + item-level bootstrap, 2000 resamples, seed 12345. 20 AUROCs
carried; n_articles held-out = 18. `verify_batch1.json` → `auroc_ci` (8/8)
includes `paired_point_equals_auroc_difference` (point = 0.9824 − 0.8738,
item CI [0.095, 0.123]).

Evidence: `auroc_ci.json` → `aurocs.*.{point,ci_item}`, `paired_diffs`;
verified 8/8 in `verify_batch1.json` → `auroc_ci`.

Command: `python 04_experiments/src/r3_exp_auroc_ci.py`
(`--check-repro` → REPRO CHECK: PASS).

Proposed draft sentence: "The frozen-to-corrected test AUROC drop (0.9824,
95% CI [0.977, 0.987] to 0.8738, [0.859, 0.889]) is 0.109 on identical items
(paired 95% CI [0.095, 0.123], excluding zero), from 2000-resample bootstrap
(seed 12345), reported as exploratory/post-hoc."
