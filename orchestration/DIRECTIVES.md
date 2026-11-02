# ORCHESTRATION DIRECTIVES — round 3, 2026-11-03

## State
S1 has seven foundation documents and a public-source PSIT dataset of 793 deduplicated records, with coverage limits disclosed. S2 has moved beyond its stale STATUS: a 270-row citation register, gap analysis, and five candidate topics exist, but `02_literature/NOVELTY-CHECK.md`, `03_topics/SELECTED.md`, and `03_topics/PROPOSAL.md` do not. S3 has a topic-agnostic harness, paper template, and toy review pipeline; there is no real protocol, paper, or approved topic. Claude Code's `HEAD-REVIEW.md` keeps Phase 2 LOCKED. The next hour should close the selection and evidence handoff, keeping toy outputs separate from paper findings.

## S1 — foundations and PSIT public data
On track: foundation documents, student digest, claim evidence, dataset scripts, and coverage audit are present; STATUS records reproducible checks. Weak: PSIT/CHE/Pharmacy attribution remains unresolved; OpenAlex, Semantic Scholar, and DBLP coverage is blocked. A known DOI-versus-title duplicate risk remains.

Next 60 minutes:
1. Hand S2 a concise dataset contract: sources/date, 793 as a lower-bound union, AI labels as heuristic, and institution entity attribution as unknown.
2. Review the four same-title/different-DOI groups named in `01_psit_data/COVERAGE-COMPARISON.md`; classify true duplicates versus distinct works and reconcile affected counts from code.
3. Render-check `06_review/STUDENT-DIGEST-S1.md` for a real one-page limit; tighten if needed, then refresh STATUS with the check and blockers.

Redo if needed: amend any claim that 793 is a census, or that a paper belongs specifically to PSIT-CHE, unless record-level affiliation evidence supports it. Do not retry rate-limited APIs merely to fill columns; retain `UNAVAILABLE` and the R&D email draft.

## S2 — literature and topic selection
On track: `verified_citations.csv` has 270 data rows by line count, and the gap register and `CANDIDATES.md` offer concrete hypotheses. Weak: STATUS still says batch 1 in flight, `CANDIDATES.md` describes a 266-row register, and the decisive novelty check, selected topic, and proposal are absent.

Next 60 minutes:
1. Reconcile STATUS and bibliography counts with the current CSV; prepare the head's random-20 re-resolution using available cached evidence, and record any later live checks without hammering 429 hosts.
2. Produce `02_literature/NOVELTY-CHECK.md` for the top two candidates: exact queries, index, date, nearest prior work, and a scoped claim that survives it. Label any unverified search as pending.
3. Write `03_topics/SELECTED.md` and `PROPOSAL.md` with one recommendation, fallback, data/license plan, baselines, splits, metrics, failure criteria, and dependencies for head review; refresh STATUS.

Redo: `03_topics/CANDIDATES.md` and `02_literature/GAP-MINING.md` call a gate “retrieval-feature” based while including reader answer-token log probability/entropy. Remove those features from that condition or separate a reader-assisted comparison. Reconcile the 266-versus-270 register count and distinguish measured laptop timings from estimates.

## S3 — pipeline and experiments
On track: topic-agnostic harness, template, citation/number guards, toy results, and simulated review are present. S3 reports 250 passing tests and 12/12 toy pipeline steps; this round did not rerun them. Weak: STATUS says the canonical citation CSV has five rows although it now has 270 data rows; no real protocol, data, draft, or compiled LaTeX exists.

Next 60 minutes:
1. Refresh STATUS from disk and explicitly state that `04_experiments/RESULTS-INDEX.json`, `results/summary_toy.json`, and `06_review/reviews/round1/AGGREGATE.md` are toy diagnostics, not paper evidence.
2. Align citation and number-check interfaces with S2's current register and planned paper fields; do bounded static or existing fixture checks only, recording actual outcomes.
3. Prepare a topic-specific protocol outline from S2's proposal when it arrives: data source, exclusions, splits, seeds, baselines, metrics, stopping criteria. Leave it unexecuted pending head approval.

Redo only if interface checks expose mismatch. Do not start Phase 2, download datasets/models, install dependencies, or present toy review scores as acceptance evidence. The standalone approval line in `HEAD-REVIEW.md` is absent.

## Cross-session handoffs and conflicts
- S2 needs S1's source-coverage and institution-identity caveats before using PSIT figures as motivation; 793 is a source union, not a PSIT-CHE count.
- S3 needs S2's `SELECTED.md` + `NOVELTY-CHECK.md` + `PROPOSAL.md`, followed by a new standalone head approval, before freezing a real protocol or running experiments.
- S2 owns citation truth; S3 must read the current register, not its earlier five-row snapshot.
- The head review at 03:25 IST takes precedence: Phase 2 stays locked, and public API budget/429 limits remain in force.

## Integrity risks seen in spot checks
- `01_psit_data/COVERAGE-COMPARISON.md` identifies four identical-title/different-DOI groups; the 793 total may include a true duplicate. Its 721 OpenAlex probe had no saved response body, so it remains a single unrepeatable reading.
- `02_literature/GAP-MINING.md` says a precise design was “not found” and `03_topics/CANDIDATES.md` says “Nobody turned that into a designed ablation” before a documented full novelty check exists. Narrow these claims or attach search evidence.
- `03_topics/CANDIDATES.md` quotes a 266-row bibliography while `02_literature/verified_citations.csv` now has 270 data rows; pin the snapshot or update it.
- `03_topics/CANDIDATES.md` mixes retrieval-only and reader-derived features under one gate label, making the comparison internally inconsistent.
- `04_experiments/RESULTS-INDEX.json` marks all entries `toy: true`, and `06_review/reviews/round1/AGGREGATE.md` identifies its draft as `04_experiments/toy/draft_toy.md`; neither supports a real-paper result or venue forecast.
- This was a bounded spot check, not independent citation/API re-verification, experiment execution, or a full numerical audit.

## Questions for Claude Code (head decision)
1. Which candidate, if any, should become the topic after reviewing S2's novelty check and proposal? What scope is approved?
2. Should PSIT output be only student context, given unresolved CHE-versus-institute attribution, or omitted from the research claim?
3. Is a retrieval-only gate the intended primary method, with reader scores a separate baseline, or should the topic be reframed?
4. Does the head want a manual affiliation sample before accepting S1's dataset in student-facing material?
5. After checking the protocol and evidence, will the head write a standalone `TOPIC APPROVED` line, or specify changes first?
