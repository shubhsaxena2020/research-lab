# ROUND 3 — shared rules for all seven lead sessions (2026-11-08)

Read first, in this order: `RULES.md` (non-negotiable), `orchestration/HEAD-REVIEW.md` (Checkpoint 5 is the latest),
this file, `sessions/R3/TRIAGE.md`, then your own `TASK.md`. `orchestration/DIRECTIVES.md` is superseded for round 3.

## What the project is
One honest, reproducible workshop-level paper: `05_paper/draft/paper.md` (generated from
`05_paper/template/draft_template.md` by `05_paper/build_draft.py`). Title: "How Hard Are Your Negatives? A
Pre-Registered Audit of Negative Ladders for Retrieval-Feature Abstention Gates, with a Negative Result".
Round-2 simulated review: mean 4.67/10, 3 rejects, 44 must-fix items (`06_review/reviews/round2-c1/AGGREGATE.md`).
Round 3 answers every one of them: fix with evidence, or rebut with evidence. Never hide a weakness; narrow the claim instead.

## Hard rules for round 3 (on top of RULES.md)
1. **Frozen run is immutable.** Never refit thresholds of the frozen confirmatory run, never overwrite or delete any
   existing file in `04_experiments/results/`, `04_experiments/runs/`, `PREREGISTRATION.md` history. New numbers go
   ONLY in new files under `04_experiments/results/c1/r3/<your-lane>/` produced by NEW scripts
   `04_experiments/src/r3_<lane>_*.py` with fixed seeds. Every result file records the exact command, seed, inputs' sha256.
2. **File ownership.** Write only the paths your TASK.md lists as OWNED. Everything else is read-only for you. If you need a
   change in a file you do not own, write a request in `sessions/R3/REQUESTS.md` (append one line: date, your lane, file,
   what, why) and continue with something else.
3. **No git commits, no git push, no branch changes.** The head (Claude Code) commits at checkpoints.
4. **Post-hoc is labelled post-hoc.** Anything not in the frozen pre-registration is "exploratory" or a declared deviation,
   in so many words. Never back-date a deviation.
5. **Numbers:** two decimals for rates, three for AUROC. Every number you put in prose for the draft must point to a
   results-file key (the integrator binds it with `<!-- num:... -->` markers and `tools/check_numbers.py` must PASS).
6. **Compute: GPU first, then CPU, gently.** This laptop's Arc 130T iGPU is reached through Ollama (Vulkan, already
   enabled, http://127.0.0.1:11434). Any local LLM generation/scoring: try the Ollama route first; if it cannot give what
   is needed (e.g. token log-probabilities), fall back to CPU torch with `torch.set_num_threads(4)` and the heavy lock
   (`ops/HEAVY.lock` semantics in RULES.md #10). Only one heavy job at a time on the whole laptop. Never while free RAM < 8 GB.
   Embedding/BM25 passes are minutes; do not parallelise them across subagents.
7. **Public APIs** (OpenAlex, Crossref, arXiv, Semantic Scholar): cache in `02_literature/raw/`, polite rate (<=1 req/s),
   User-Agent with mailto shubh.saxena2020@gmail.com, back off 30/60/120 s on 429. Do not sign up for keys.
8. **Python:** inside Hermes, `python` is the Hermes venv (3.11, torch CPU, bm25s, sentence-transformers, sklearn,
   scipy). matplotlib/pandas are absent: emit SVG from code. Tests: `python -m pytest <targeted path> -q`.
9. **Progress:** your lane folder holds `PROGRESS.md` (update after every batch: what was done, evidence = file + command +
   value, what is next) and `reports/` (one report per subagent task). Verify every subagent claim yourself by opening the
   file / re-running the command before marking it done (RULES.md #14). Max 3 rework rounds per item.
10. **Finish marker:** last line of `PROGRESS.md` = `CARD COMPLETE` or `CARD BLOCKED: <reason>` only when truly finished.
11. If `research-lab/STOP` exists: finish the current batch, save state, write `CARD BLOCKED: STOP file`, exit.

## Lanes
| Lane | Where | Profile | Owns (summary) |
|---|---|---|---|
| R3-1 metrics & statistics | main | res-s1 | r3_metrics_* scripts + results/c1/r3/metrics/ |
| R3-2 pre-registration & reproducibility | main | res-s2 | PREREGISTRATION amendment, lockfile, harness provenance |
| R3-3 new experiments | main | res-s3 | r3_exp_* scripts + results/c1/r3/exp/ |
| R3-4 integrator | main | res-s4 | draft template, paper assets, RESULTS-INDEX, 06_review/ |
| R3-5 related work & novelty | laptop 2 | res-s5 | 02_literature/related-work-r3/ |
| R3-6 student digest & presentation | laptop 2 | res-s6 | 06_review/STUDENT-DIGEST-S3.md, 06_review/PRESENTATION/ |
| R3-7 LaTeX / PDF build | laptop 2 | res-s7 | 05_paper/latex-build/ |
