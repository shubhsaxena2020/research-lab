# Codex orchestrator — pass 6 (fresh session, 2026-11-19 ~00:05 IST). Do this pass, report, exit. Budget ~70k tokens.

You orchestrate the research-lab paper (C:\Users\shubh\research-lab); Claude Code verifies, commits and resumes you.
Read first: RULES.md, sessions/R3/COMMON.md, orchestration/HEAD-REVIEW.md checkpoints 9-10, sessions/R3-4e-consistency/TASK.md,
04_experiments/results/c1/r3/R3-3b/ANSWERS.md. Do not poll or wait on leads.

## Hard constraints (unchanged)
- Max 2 research-lab leads: res-s4 (running R3-4e-consistency since 23:19; it owns 05_paper/template/**, 05_paper/draft/**,
  05_paper/tables/**, 05_paper/figures/**, RESULTS-INDEX.json and 06_review/**; do not touch) and res-s1 (idle now).
  Never use res-s2, res-s3 or researcher (another Claude session). Never restart/kill the gateway or edit
  ops/hermes_runner.ps1. Launch via the runner like earlier lanes, budget 5400, PROMPT without double quotes, exactly 3
  subagents per batch, model already configured. Leads and you never commit.
- Integrity: frozen run and PREREGISTRATION immutable; new numbers only from result files; post-hoc labelled.

## State (verified by Claude Code)
- Pushed 17239f6: R3-3b complete (MF-17 AUROC intervals, MF-10 GPU LLM adjudication kappa 0.280, MF-7 control).
  Head recomputed kappa from the label CSVs and matched the AUROC points. Nothing is bound into the draft yet.
- R3-4e is still working and owns the draft, so binding R3-3b must wait for R3-4e to finish.

## Task
1. Give res-s1 useful work that writes NONE of R3-4e's paths. Default: R3-6b-student-pack — refresh the student
   materials for the current state (06_review is R3-4e's, so write a NEW folder 07_student/ instead): a short digest of what
   changed in round 3 and what the new R3-3b numbers mean (copied exactly from R3-3b JSON/ANSWERS.md, marked post-hoc and
   'not yet in the draft'), an updated viva Q&A covering MF-14, H1 not exercisable, kappa 0.280 meaning, and what NOT to
   claim; plain English for a first-semester BCA student; every number traced to a file. A reviewer subagent checks every
   number against its source. Choose differently only if clearly better and inside the constraints.
2. ALSO write, but do NOT launch, the card sessions/R3-4f-bind-3b/TASK.md (+ PROMPT-R3.txt) for after R3-4e: bind the R3-3b
   results into the draft via RESULTS-INDEX + num markers, update the MF-17/MF-10/MF-7 letter entries, gates as R3-4d.
3. Append Checkpoint 11 to HEAD-REVIEW.md, write sessions/R3/orch/REPORT-pass6.md, print a short summary.
