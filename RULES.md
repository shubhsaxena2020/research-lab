# RULES (all sessions, all subagents; non-negotiable)

## Integrity (this is what makes the paper presentable)
1. NO fabricated anything. Every citation must be verified to exist (resolve DOI / arXiv id / OpenAlex id with a real API call) and recorded in 02_literature/verified_citations.csv
   with the URL and retrieval date BEFORE it may appear in any draft. A citation you cannot verify is dropped, never "approximately" cited.
2. Every number, table, figure in any draft comes from a result file produced by code in 04_experiments/ with fixed seeds, committed command, and logged output. No invented results,
   no "expected" numbers, no results from a different run than the one cited. Negative results are reported as negative.
3. Original wording only: summarize in your own words, quote sparingly with quotation marks and citation. Never paste paper text. Run the originality procedure in 06_review/ORIGINALITY.md before any draft is called done.
4. The paper must disclose AI assistance (tools used and for what) following the target venue's policy. The student is the responsible author: the STUDENT-DIGEST must let Shubh explain every section.
5. Claims are calibrated: say what was measured, on what, how many runs; never claim "state of the art" / "novel" without a documented novelty check (02_literature/NOVELTY-CHECK.md with search queries and results).
6. Public data only for experiments. No private chats, no personal files, no scraped data that breaks a site's terms. The user's own projects may inspire a topic but their private data is never used or published.

## Sources & access
7. PSIT data: PUBLIC sources only (OpenAlex, Semantic Scholar, Crossref, DBLP, the institute's own public website, arXiv). Do NOT log in anywhere, guess credentials, scrape behind logins, or bypass terms of service
   (e.g. do not scrape Google Scholar). Internal facts (papers "ongoing", "under review", "under surveillance/monitoring") are NOT public: record them as UNAVAILABLE and draft an email to the PSIT R&D cell instead.
8. Respect APIs: polite rate limits, a descriptive User-Agent with mailto shubh.saxena2020@gmail.com, cache responses in 01_psit_data/raw/.

## Operations
9. Write only inside C:\Users\shubh\research-lab. Never touch ai-memory-core\, Second Brain, Ollama models, other processes, other Hermes profiles, git remotes (local commits only), scheduled tasks.
10. No secrets in files/logs. No unbounded loops: every loop has a cap/timeout. Heavy compute (model training, big downloads >1 GB) only one at a time: use ops\heavy_lock.py semantics (create ops\HEAVY.lock, remove when done); this laptop is shared with another build.
11. API etiquette on 429/timeouts: exponential backoff (30 s, 60 s, 120 s), do not hammer. If work\STOP (research-lab\STOP) exists, finish current item, save state, exit.
12. Save state constantly: update your session STATUS.md after every meaningful step and at least every 15 minutes; keep BACKLOG.md checkboxes truthful. Sessions die; the next day resumes from these files.
13. Read orchestration\DIRECTIVES.md (from the Codex orchestrator) at start and about every 30 minutes; follow it unless it contradicts RULES.md. Read orchestration\HEAD-REVIEW.md (Claude Code) likewise: head decisions override.
14. Verify, don't trust: when a subagent reports, open the file, run the command, check the numbers. Max 3 rework rounds per item. Quote evidence. Failing / not-done is reported as such.
