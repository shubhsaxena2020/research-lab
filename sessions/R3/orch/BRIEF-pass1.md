# Codex orchestrator brief — research-lab round 3, pass 1 (2026-11-18 ~21:30 IST)

You are the ORCHESTRATOR (head) of the research-lab paper project in C:\Users\shubh\research-lab. Claude Code is the
coordinator: it watches the Hermes leads for free and will resume this Codex session at checkpoints (a lead finishes,
stalls or deviates). Do NOT poll, sleep-wait or loop on lead progress yourself. Do this pass, write your report, and exit.
Token budget for this pass: about 150k. Read RULES.md, sessions/R3/COMMON.md, orchestration/HEAD-REVIEW.md first.

## Hard constraints (owner instructions)
- At most 2 Hermes sessions at a time on this laptop: profiles res-s4 and res-s1 only. Laptop 2 is offline; do not use it.
- Hermes model: nilabh/Deepseek-v4.1-Flash via 9Router for leads and subagents. Do not edit any Hermes config.
- Every lead batch = ONE delegate_task call with EXACTLY 3 parallel tasks (ops/lead_protocol_r3.txt already says this).
- Launch leads ONLY through the runner, from PowerShell, for example:
  Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','C:\Users\shubh\research-lab\ops\hermes_runner.ps1','-HermesProfile','res-s4','-Workdir','C:\Users\shubh\research-lab','-OutDir','C:\Users\shubh\research-lab\sessions\<LANE>','-PromptFile','C:\Users\shubh\research-lab\sessions\<LANE>\PROMPT-R3.txt','-Budget','10800'
  PROMPT files must contain NO double-quote characters (PowerShell 5.1 splits the argument at them and Hermes exits 2).
  A prompt = contents of ops/lead_protocol_r3.txt + a paragraph pointing at COMMON.md and the lane TASK.md
  (copy the pattern of sessions/R3-4b-review/PROMPT-R3.txt).
- Never kill processes by image name; only by PID. Never touch the shared Hermes gateway process.
- Leads never commit. You do not commit or push either: Claude Code verifies and commits.
- Integrity: no fabricated numbers; new numbers only from result files via the <!-- num: --> mechanism; post-hoc work labelled.

## Verified state (by Claude Code, 21:25)
- Checkpoint fa6db32 is pushed. Its message and sessions/R3-4b-review/TASK.md wrongly say the 11-08 round-3 prompt packs were
  stale. They were NOT: tools/simulate_review.py hashes the draft after newline normalisation; 9194a481 (tool) and e346271e
  (sha256sum of bytes) are the SAME draft. Record this correction in HEAD-REVIEW.md.
- res-s1 (lane R3-7b-latex-main) is RUNNING: Tectonic 0.17.0 installed in tools/tectonic/, build.ps1 and ENGINE.md edited,
  PDFs rebuilt. It has not created PROGRESS.md yet. Leave it running; only read its state.
- res-s4 (lane R3-4b-review) was STOPPED by Claude Code at 21:22 because it skipped deliverable 1:
  it never folded the 21 PARTIAL + 5 DEFERRED items (draft_template.md unchanged, draft sha unchanged). It did add
  RESULTS-INDEX entries, re-packed round 3 and wrote all 6 persona reviews + INGEST + AGGREGATE in 06_review/reviews/round3-c1/
  (mean 5.67/10, 6 borderline; round 2 was 4.67 with 3 rejects). The reviews look genuinely independent (word-set Jaccard
  between reviews <= 0.27, one subagent per persona reading its own PROMPT.md). They are a valid round-3 review of the
  CURRENT draft, i.e. before the folding work.
- Hermes write_file refuses to overwrite a file that changed since the agent last read it (twice today on
  COMPARE-round2-round3.md). Leads must re-read a file right before editing it and prefer the patch tool. PROGRESS.md
  of R3-4b stayed frozen after batch 0.
- check_all 4/4 PASS and check_numbers 0 findings on the current draft.

## Your tasks this pass
1. Skim the round-3 AGGREGATE.md and two review yamls; list the round-3 must-fix items that are new or persisted.
2. Write a new lane card sessions/R3-4c-fold/TASK.md (+ PROMPT-R3.txt, no double quotes) for res-s4: fold the 21 partial +
   5 deferred round-2 items AND the round-3 must-fix items into 05_paper/template/draft_template.md, rebuild the draft,
   then regenerate COMPARE-round2-round3.md (real round-3 scores, labelled as a review of the pre-fold draft) and
   RESPONSE-LETTER-R3.md (all 44 + round-3 items, verdict + concrete change). Gates the lead must meet and record in
   PROGRESS.md (updated after EVERY batch): draft sha changed, check_numbers 0 findings, tools/check_all.py 4/4 PASS.
   Tell it the editing rule above. Do NOT run another review round in this lane (that is the next pass, after Claude Code
   verifies the fold). Same OWNED paths as R3-4b, excluding 05_paper/latex-build/** which res-s1 owns.
3. Launch res-s4 on that lane with the runner (budget 10800). Confirm a hermes.exe -p res-s4 process exists.
4. Append Checkpoint 6 to orchestration/HEAD-REVIEW.md: Codex is orchestrator from 2026-11-18; the stale-pack correction;
   why R3-4b was stopped; the R3-4c plan.
5. Write sessions/R3/orch/REPORT-pass1.md: what you read, decided, wrote and launched, open risks, and what Claude Code
   should watch for before resuming you. Print the same summary as your final message.
