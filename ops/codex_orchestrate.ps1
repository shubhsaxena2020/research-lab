param([Parameter(Mandatory)][int]$Round)
Set-Location C:\Users\shubh\research-lab
$prompt = @"
You are the ORCHESTRATOR of a 3-session research project in C:\Users\shubh\research-lab (read README.md and RULES.md first). Three Hermes sessions (S1 foundations+PSIT public data, S2 literature+topic selection, S3 paper pipeline+experiments) work in parallel; each updates sessions\S*\STATUS.md. Claude Code is the head; its decisions in orchestration\HEAD-REVIEW.md override yours.
This is orchestration round $Round. BUDGET RULES: one short run, no polling, no sleeping, no running experiments, no installing, no network crawling, finish in under 8 minutes. Read: the three STATUS.md files, directory listings (just names/sizes) of 00_foundations, 01_psit_data, 02_literature, 03_topics, 04_experiments, 05_paper, 06_review, and open at most 6 output files to spot-check quality (look for fabricated-looking citations, numbers without sources, vague filler, contradictions between sessions).
Write orchestration\DIRECTIVES.md (overwrite) with: (1) one-paragraph state of the project; (2) per session: what is on track, what is weak, the 3 highest-priority next actions for the next 60 minutes, anything to redo and why; (3) cross-session conflicts/dependencies (e.g. S3 needs S2's SELECTED.md); (4) integrity risks you saw, quoting file names; (5) a list of questions the head (Claude Code) should decide. Be specific and concise (under 90 lines). Do not edit any other file.
"@
$ts = Get-Date -Format 'yyyyMMdd-HHmm'
codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -m gpt-6-sol -c 'model_reasoning_effort="medium"' $prompt *> "logs\codex-round$Round-$ts.log"
