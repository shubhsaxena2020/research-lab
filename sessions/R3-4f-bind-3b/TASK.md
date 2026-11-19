HEAD NOTE 2026-11-19 01:40 IST (Claude Code) - LAUNCH NOW: R3-4e-consistency was stopped by the head at 01:32 after 2 h 13 min with no files written (one subagent ended incomplete, one never wrote its report); it changed nothing in the draft (sha still d81cc90ffe60). There is no R3-4e evidence to wait for. Treat this card as launched after the R3-4e handoff.
Extra deliverable, narrow: fix the one known contradiction R3-4e was meant to catch. Table 4 and section 4.2 say the H1 criterion is not exercisable at the registered operating point, but section 4.6 still says H1 remains refuted. Make every H1 verdict statement in the paper (abstract, 4.2, Table 4, 4.6, discussion, conclusion) say the same thing, using the Table 4 wording, and update the MF-25 entry in the response letter. Do not run a whole-paper audit: grep for H1 and verdict wording only. Keep each subagent task small (one or two files, one claim group) so each finishes in well under 30 minutes.

# TASK R3-4f — bind verified R3-3b results into the paper

Lane: R3-4f-bind-3b; main laptop; profile res-s4; prepared 2026-11-19. **Do not launch this card until R3-4e-consistency has completed and Claude Code has independently verified its deliverables and gates.**

## Goal

After the R3-4e handoff, integrate the already-computed R3-3b deferred analyses for MF-17, MF-10, and MF-7 into the current draft and response letter. Use only existing R3-3b result files and exact keys. Preserve exploratory/post-hoc labels and all support limits. No new analyses, model calls, numbers, or changes to the frozen verdict/preregistration.

## Owned paths

- `05_paper/template/**` — update the relevant prose and marker bindings only.
- `04_experiments/RESULTS-INDEX.json` — add the R3-3b entries using the existing schema and exact evidence paths/keys.
- `05_paper/draft/**` — generated output only; rebuild from the template, never hand-edit `paper.md`.
- `05_paper/tables/**` and `05_paper/figures/**` — only if the existing paper asset generation requires refresh; avoid unrelated changes.
- `06_review/RESPONSE-LETTER-R3.md` — update the MF-17, MF-10, and MF-7 entries to accurately describe what is now integrated and what remains unsupported.
- `sessions/R3-4f-bind-3b/**` — lane progress and reports.

Read-only: all `04_experiments/results/**`, all `04_experiments/runs/**`, `PREREGISTRATION.md` and its hash history, and the completed R3-4e audit evidence. Never touch `05_paper/latex-build/**`. Do not commit, push, change branches, change the runner or Hermes configuration, or restart the gateway.

## Evidence and binding requirements

Use `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` as the navigation summary and bind only keys present in its cited JSON `results` objects. The three evidence files are `mf17_auroc_intervals.json`, `mf10_adjudication.json`, and `mf7_gold_control.json` under that directory.

- MF-17: report the post-hoc item-level held-out intervals and paired difference only with their exact result keys. State sample/resampling scope and that the paired difference excludes zero only for this exploratory analysis; it does not revise a frozen verdict. Keep article-cluster resampling distinct if mentioned. Do not call the values confirmatory.
- MF-10: report repeated LLM agreement (Cohen's kappa 0.2802; raw agreement 0.59; 41 disagreements in 100 items) with exact keys. State that the strict resolver marked 56/100 answerable. This is not human gold; the labellers/resolver are LLMs and comparison to the earlier run is not like-for-like.
- MF-7: explain that the is_gold AUROC of 1.0 is tautological because is_gold is deterministic from the label. State that D3 has only pooled rung=-1 hit/miss counts and no per-rung R1-R3 estimand. Do not frame AUROC 1.0 as model/gate performance or as exculpatory evidence.

Every numeric prose/table value must be bound with `<!-- num:exact.key -->value<!-- /num -->` and pass `tools/check_numbers.py`. Add only the exact result keys already present. Update the response-letter statuses and change descriptions for MF-17, MF-10, and MF-7; keep any remaining evidence gaps or caveats explicit. Preserve the existing MF-14 and H1 wording from R3-4e unless the 4e handoff itself explicitly revises it. Do not count the R3-3b analysis as a new confirmatory test.

## Required process and gates

Follow `ops/lead_protocol_r3.txt`. Each batch is one blocking `delegate_task` call with exactly three parallel tasks. The initial batch should independently handle the index/key mapping, paper-template integration, and response-letter revisions, with non-overlapping write paths. Later batches must include an independent review of the prior batch. Verify each report against actual source files and rerun its proof. Record every batch in `PROGRESS.md` and reports under this lane.

Before completion run and record exact outcomes:

1. `python tools/check_numbers.py --draft 05_paper/draft/paper.md` — zero findings.
2. `python 05_paper/build_draft.py` twice — byte-identical generated draft/hash.
3. `python tools/check_all.py` — 4/4 PASS.
4. Confirm every new number key exists in the correct result JSON and in RESULTS-INDEX, MF-17/MF-10/MF-7 response-letter entries match the draft, and no frozen/preregistration files changed.

Last line of `PROGRESS.md` must be `CARD COMPLETE` only if every deliverable and gate passes; otherwise record the exact incomplete state. No commits.
