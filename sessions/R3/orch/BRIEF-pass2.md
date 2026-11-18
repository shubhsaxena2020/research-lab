# Codex orchestrator — pass 2 (2026-11-18 ~21:50 IST). Same rules as pass 1. Do this pass, report, exit. Budget ~100k tokens.

## New facts since pass 1 (verified by Claude Code)
- R3-7b-latex-main (res-s1) wrote CARD COMPLETE. Verified: Tectonic 0.17.0 in tools/tectonic (gitignored), build.ps1 no longer
  hardcodes the laptop-2 path, 0 overfull boxes, no ?? references, test_md2tex.py PASS (317 numbers). Problems found by Claude Code:
  (a) the build is flaky on this laptop: Windows Defender/indexer briefly memory-maps freshly written files, so truncating refs.bib
      or a PDF fails with Errno 22 / os error 1224. Claude Code added retry loops in build.ps1 (citations step 5 tries, tectonic 4
      tries on os error 1224 only); the ACL PDF rebuilt at 21:34 but the article PDF still failed in that run.
  (b) the bibliography is EMPTY: md2tex.py never turns the draft's citations into \cite keys, so refs.bib (342 entries) is unused.
  (c) label fig:main-accuracy is defined 3 times in body.tex.
- The old R3-4b lead kept running inside the shared gateway after its client was killed; it obeyed a cancellation note and
  ended at 21:34 with CARD BLOCKED. Killing hermes.exe does not stop a lead; only its turn ending or a gateway restart does.
- R3-4c-fold (res-s4) is running (started 21:25).
- Owner compute rule updated in sessions/R3/COMMON.md rule 6 (= ai-memory-core decision D10): GPU first for every model job
  (Ollama embeddings/generation on Vulkan, or ONNX DirectML via the ai-memory-core venv interpreter), CPU torch only as fallback
  or spill when GPU 3D load >= 90%; never swap a pre-registered model to reach the GPU. Ollama embed on GPU verified.
- res-s1 and res-s4 profiles now carry 14 MCP servers + Claude skill dirs, but MCP tools only attach after the shared gateway
  restarts (planned between waves, coordinated with the other session). Until then leads have built-in tools + skills only.
- ANOTHER Claude session (InMobi AI Kaushal hackathon research, C:\Users\shubh\Projects\ai-kaushal-research) runs 3 Hermes leads
  on res-s2, res-s3, researcher, uses research-lab\ops\hermes_runner.ps1 read-only, and also uses Codex luna. Never touch its
  profiles, its folder, the runner script, or the gateway. Keep research-lab at 2 leads max (res-s1, res-s4).

## Your tasks this pass
1. Decide the next lane for the now-idle res-s1 so two sessions keep running. Default proposal: R3-7c-latex-citations —
   make the build reliable on this laptop (finish the retry fix; consider writing to a temp file then os.replace with retries),
   implement citation conversion in md2tex.py (draft citation markers -> \cite keys present in refs.bib; report any citation with
   no bib entry instead of inventing one), fix the duplicate figure label, rebuild both PDFs, re-run test_md2tex.py and the PDF
   checks, update BUILD-REPORT.md. OWNED: 05_paper/latex-build/** and its lane folder only; it must not edit the draft or
   template (R3-4c owns them) — if citation markers in the draft are inconsistent, it lists them in its report for R3-4c.
   Change the plan if you see a better use of res-s1, but stay inside research-lab and the rules.
2. Write sessions/<LANE>/TASK.md + PROMPT-R3.txt (no double quotes), launch it on res-s1 via the runner (budget 10800), confirm
   the process. Do not touch res-s4.
3. Append a short Checkpoint 7 to orchestration/HEAD-REVIEW.md, write sessions/R3/orch/REPORT-pass2.md, print the summary.
