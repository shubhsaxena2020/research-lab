# Codex orchestrator — pass 3 (2026-11-18 ~22:20 IST). Same rules as passes 1-2. Do this pass, report, exit. Budget ~100k tokens.

## Facts (verified by Claude Code)
- R3-4c-fold (res-s4) wrote CARD COMPLETE at 22:13. Committed + pushed as 533998b. Verified: draft sha 89e92e79 (changed),
  check_numbers 0 findings, build_draft reproducible, PREREGISTRATION and frozen results untouched.
- RESPONSE-LETTER-R3.md tally: 23 resolved, 52 partial, 11 deferred (86 entries); entries are not templated (median word
  Jaccard 0.10). But the template diff is only 42 lines, and a head spot-check found an OVERCLAIM: MF-14 is marked resolved,
  yet the draft does not put the registered R4 figure (band 100.00% / frozen exploratory 84.71%) beside the corrected 12.53%
  and section 5.2 is not restricted. MF-27 and MF-40 check out (MF-40 says eight tables; the draft has seven).
- res-s4 is now idle. res-s1 runs R3-7c-latex-citations (do not touch it). The other Claude session's leads on res-s2, res-s3,
  researcher must not be touched. Max 2 research-lab leads.
- Lesson from earlier projects: LLM per-row audits have been gamed (a reviewer listed distinct items without checking content).
  Verification must quote the actual draft text, checked by a different subagent than the one that made the change.

## Your tasks this pass
1. Write and launch the next res-s4 lane, R3-4d-verify-fold (budget 10800, runner, no double quotes in the prompt):
   a. Blind verification of every RESOLVED claim in RESPONSE-LETTER-R3.md: per item, a subagent that did not write it quotes the
      exact draft sentence(s) in 05_paper/draft/paper.md that implement the stated change, or downgrades the verdict to partial
      with the reason. Results table in sessions/R3-4d-verify-fold/VERIFY-RESOLVED.md (item, claim, quoted draft text or MISSING,
      final verdict). Fix MF-14 properly in the template (it is text-only: put the registered figures beside 12.53% and scope 5.2).
   b. Then fold PARTIAL items that need only wording/structure changes (no new experiments, no new numbers except existing
      result keys through num markers), biggest reviewer impact first; for each, update the letter verdict honestly.
   c. Gates (record in PROGRESS.md after every batch): check_numbers 0 findings, build_draft reproducible, tools/check_all.py
      4/4 PASS. Same OWNED paths as R3-4c; never write 05_paper/latex-build/**.
   d. Compute rule: COMMON.md rule 6 (GPU first). This lane should need no model compute; if it does, follow rule 6.
2. Append Checkpoint 8 to orchestration/HEAD-REVIEW.md, write sessions/R3/orch/REPORT-pass3.md, print the summary.
3. Name what you think the round should do after R3-4d and R3-7c (e.g. review round 4 on the verified draft), so Claude Code
   can plan the next wave; do not launch it.
