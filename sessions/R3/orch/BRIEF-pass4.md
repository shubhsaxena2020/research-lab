# Codex orchestrator — pass 4 (fresh session, 2026-11-18 ~22:30 IST). Do this pass, report, exit. Budget ~80k tokens.

You are the ORCHESTRATOR of the research-lab paper (C:\Users\shubh\research-lab). Claude Code is the coordinator: it watches
leads for free, verifies their work and commits; it resumes you at checkpoints. Do not poll or wait on leads. First read:
RULES.md, sessions/R3/COMMON.md (rule 6 = GPU first for any model compute), orchestration/HEAD-REVIEW.md checkpoints 5-8,
sessions/R3-4d-verify-fold/TASK.md, 06_review/RESPONSE-LETTER-R3.md (the deferred items), sessions/R3-4c-fold/PROGRESS.md.

## Hard constraints
- At most 2 research-lab Hermes leads: res-s4 (now running R3-4d-verify-fold, do not touch) and res-s1 (idle). Never use
  res-s2, res-s3 or researcher: another Claude session (AI Kaushal research) runs leads there. Never restart or kill the
  shared Hermes gateway; never kill processes by image name. Never edit ops/hermes_runner.ps1 (the other session uses it).
- Model nilabh/Deepseek-v4.1-Flash via 9Router (already configured; do not edit Hermes configs). Exactly 3 parallel subagents.
- Launch via the runner exactly like sessions/R3-4d-verify-fold was launched (see HEAD-REVIEW checkpoint 8 / earlier passes);
  PROMPT files must contain no double-quote characters. Leads never commit; you do not commit; Claude Code commits.
- Integrity: frozen run and PREREGISTRATION immutable; new numbers only from new result files under
  04_experiments/results/c1/r3/<lane>/, labelled post-hoc/exploratory; no fabrication.

## State (verified by Claude Code)
- Pushed: 533998b (R3-4c fold), ce0674e (R3-7c citations + reliable build), 88d6b57 (cache untracked).
- R3-7c verified: build.ps1 exit 0, 11 citations / 7 bib keys, reference list present, 0 overfull, labels unique.
- R3-4d (res-s4, started 22:19) owns the draft/template, RESULTS-INDEX, 06_review/**; it is verifying the 23 resolved
  claims and folding wording-only partials.

## Task
1. Pick the best next lane for res-s1 that does NOT write any R3-4d-owned path. Default: R3-3b-deferred-analyses —
   produce the evidence for deferred items that need analysis rather than wording, from EXISTING predictions/data only:
   MF-17 AUROC bootstrap intervals, MF-10 adjudication of a sample of >= 100 negatives (an LLM judge may be used; follow
   COMMON.md rule 6: GPU first via Ollama on 127.0.0.1 or the 9Router API, record the device/model), MF-7 gold-paragraph
   control audit if feasible. Outputs: results under 04_experiments/results/c1/r3/R3-3b/, a report per item with the exact
   result keys the integrator should bind, and ANSWERS.md mapping item -> evidence. No draft edits.
   Choose differently if the response letter shows a better use, but stay within the constraints.
2. Write sessions/<LANE>/TASK.md + PROMPT-R3.txt, launch on res-s1 (budget 10800), confirm the hermes.exe -p res-s1 PID.
3. Append Checkpoint 9 to HEAD-REVIEW.md, write sessions/R3/orch/REPORT-pass4.md, print a short summary and your new
   Codex session id.
