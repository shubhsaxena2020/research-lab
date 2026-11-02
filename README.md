# research-lab — Shubh's AI research-paper project (separate from ai-memory-core)

Goal: within 1-2 weeks of daily 3-7 hour agent sessions, produce ONE genuinely good, honest, reproducible AI research paper that Shubh
(BCA sem 1, PSIT CHE) understands end to end and can present and defend.

Head: Claude Code (reviews, verifies, decides). Orchestrator: Codex (gpt-6-sol, medium effort, 3 short runs per day session).
Workers: 3 Hermes sessions (profiles res-s1, res-s2, res-s3), each with up to 9 concurrent subagents, model nilabh/Deepseek-v4.1-Flash via 9Router.

Folders
- 00_foundations/   what research papers are, how to write/publish them, what they mean for a BCA student (S1)
- 01_psit_data/     PUBLIC data about PSIT research output + subfolder_ai_research/ (S1, then S2)
- 02_literature/    surveys, verified_citations.csv, gap analysis (S2)
- 03_topics/        candidate topics, scoring, SELECTED.md, PROPOSAL.md (S2, approved by head)
- 04_experiments/   pre-registered protocol, code, raw results (S3)
- 05_paper/         LaTeX/Markdown draft, figures, tables, references (S3)
- 06_review/        simulated peer reviews, claims audit, originality checks, STUDENT-DIGEST (all)
- orchestration/    Codex directives + head (Claude) reviews
- sessions/*/       each session's PROMPT.md, STATUS.md, BACKLOG.md (resumable: every day continues from these)
