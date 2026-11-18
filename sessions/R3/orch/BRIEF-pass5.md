# Codex orchestrator — pass 5 (fresh session, 2026-11-18 ~23:25 IST). Do this pass, report, exit. Budget ~70k tokens.

You orchestrate the research-lab paper (C:\Users\shubh\research-lab); Claude Code verifies, commits and resumes you at
checkpoints. Read first: RULES.md, sessions/R3/COMMON.md, orchestration/HEAD-REVIEW.md checkpoints 8-9,
sessions/R3-4d-verify-fold/PROGRESS.md and VERIFY-RESOLVED.md. Do not poll or wait on leads.

## Hard constraints (unchanged)
- Max 2 research-lab leads: res-s4 (idle now) and res-s1 (running R3-3b-deferred-analyses; do not touch). Never use res-s2,
  res-s3 or researcher (another Claude session runs a wave there now). Never restart/kill the gateway or edit
  ops/hermes_runner.ps1. Launch via the runner like earlier lanes; budget 7200; PROMPT without double quotes; exactly 3
  subagents per batch; model nilabh/Deepseek-v4.1-Flash already configured. Leads and you never commit.
- Integrity: frozen run and PREREGISTRATION immutable; no new numbers except existing result keys through num markers.

## State (verified by Claude Code, pushed ea82291)
- R3-4d complete: letter 28 resolved / 46 partial / 11 deferred; MF-14 genuinely fixed; draft d81cc90f; gates pass.
- Head found an internal CONTRADICTION: Table 4 and section 4.2 say the H1 criterion is not exercisable at the registered
  operating point, while section 4.6 still says H1 remains refuted. MF-25 is therefore only partly done.
- R3-3b (res-s1) is producing MF-17/MF-10/MF-7 evidence under 04_experiments/results/c1/r3/R3-3b/; it will be integrated
  by a LATER lane, so this lane must not bind those results.

## Task
1. Write and launch R3-4e-consistency on res-s4: a whole-paper consistency audit of the CURRENT draft — every hypothesis
   verdict (H1/H2/H3), every headline number and every claim stated in more than one place (abstract, intro, results,
   tables, discussion, conclusion, limitations) must agree in wording and value; fix contradictions in the template only
   (owned paths as R3-4d); update the response letter where a verdict changes; gates as R3-4d (check_numbers 0 findings,
   build_draft reproducible, check_all 4/4). Three subagents split the paper into thirds, a reviewer subagent re-checks.
   Report CONSISTENCY.md: each claim group, its locations, the agreed wording, and what was changed.
2. Append Checkpoint 10 to HEAD-REVIEW.md, write sessions/R3/orch/REPORT-pass5.md, print a short summary.
