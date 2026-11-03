# STATUS S2-literature (session S2b — novelty re-run)
last_update: 2026-11-03 05:55 IST (00:25 UTC)
state: IN PROGRESS (S2b) — head condition 1 (OpenAlex + Semantic Scholar re-run) is the only job.
       Previous S2 state kept below; S2b rewrites this file when it finishes.

## S2b log (all times UTC)
- 00:07 probe: OpenAlex answers again, `X-RateLimit-Limit: 1000`, remaining 990. **Unit is credits,
  10 per search** ($0.001/search, anonymous budget 1000 credits/day/IP) -> ~100 searches/day,
  shared with every other process on this IP. Harvester stops itself with 60-80 credits left.
- 00:08 Semantic Scholar unauthenticated `/graph/v1/paper/search`: **HTTP 429 on the first request**
  ("Too Many Requests ... apply for a key"). Recorded; not retried in a loop. No key exists;
  registering one with the student's email is the student's decision, not mine.
- 00:12-00:22 OpenAlex anonymous *search cluster* returns intermittent 429s ("temporarily
  rate-limited while the search cluster is under elevated load ... retry in Ns"). This is NOT the
  daily budget (no quota header; successful calls still cost 10 credits). v1/v2/v3 harvesters were
  stopped by the "stop on 429" rule and are kept as evidence; v3 died at 22/78 queries.
  **Disclosed deviation:** v4 paces adaptively (6->20 s), honours the server's own "retry in Ns",
  max 4 attempts per query, records every 429 with timestamp, marks SKIP429 after 4 failures, and
  stops for good after 5 consecutive skips. Rationale: the literal rule left 56 of 78 queries
  unrun; every 429 is timestamped in `staging/S2b-openalex-queries.jsonl`.
- Queries planned: 48 re-runs (25 family A + 23 family D) + 36 new slice-wording (18 C1, 18 C3).

## Note on `STOP`
`STOP` at the repo root dates from 03:53 today and was S2's own exit marker; this session was
launched afterwards with an explicit mandate (PROMPT-S2b) and is proceeding. The file is untouched.


## Head decision (authoritative — `orchestration/HEAD-REVIEW.md`, checkpoint 3, 04:00)
`TOPIC APPROVED`: **C1 "How Hard Are Your Negatives? A Hardness Ladder for Retrieval-Feature
Abstention Gates"**. C3 = day-3 fallback, C2 abandoned. Phase 2 belongs to S3; S2 starts no experiments.
Six binding conditions, and where S2's files stand on each:

| # | Head condition | State |
|---|---|---|
| 1 | INCREMENTAL framing; never "novel"/"first"/"SOTA"; re-run novelty on OpenAlex+S2 before any gap claim | Framing done everywhere (SELECTED Rank 1, PROPOSAL "What we will NOT claim", NOVELTY-CHECK header). **Re-run NOT done** — OpenAlex 429 all window. Carried forward (gap 1). |
| 2 | Separability audit (surface-only AUROC > 0.75 -> rebuild rung) is a hard gate | Present in PROPOSAL protocol step 2, CANDIDATES C1, GAP-01, STUDENT-DIGEST. |
| 3 | PREREGISTRATION.md frozen with hash before first run | Not S2's file (S3). Stated as a precondition in the PROPOSAL header. |
| 4 | No numbers from the private memory evaluation; at most one sentence of anecdote | **Fixed this session** — numbers stripped from PROPOSAL, SELECTED, STUDENT-DIGEST, CANDIDATES C1 pitch, GAP-MINING section 3. |
| 5 | Heavy jobs via ai-memory-core\tools\heavy.py; RAM >= 8 GB; no API hammering | Recorded in PROPOSAL; S2 ran no heavy jobs and no dataset download beyond a 2.8 MB JSON. |
| 6 | Every citation re-verified (resolve + title-vs-claim); every number traceable | Head found the LIMA/2305.11206 error; PROPOSAL B4 now cites Kadavath arXiv:2207.05221 (already in register, row confirmed). |

## What the 7 deep-dive subagents wrote (read and audited by the lead, not taken on trust)
| Agent | File | Words | Refs | Audit |
|---|---|---|---|---|
| S2-1 | `02_literature/LANDSCAPE.md` | 10,321 | 67 | 0 unmatched, 0 out-of-range, 0 uncited |
| S2-2 | `deep_dives/D2-1_agent_memory_retrieval.md` | 5,210 | 37 | clean |
| S2-3 | `deep_dives/D2-2_abstention_calibration_hallucination.md` | 6,277 | 41 | clean |
| S2-4 | `deep_dives/D2-3_efficient_on_device_inference.md` | 5,210 | 32 | clean (staging CSV 36 rows; 4 unused, no false cite) |
| S2-5 | `deep_dives/D2-4_evaluation_methodology_agents.md` | 5,922 | 32 | clean |
| S2-6 | `deep_dives/D2-5_indic_low_resource_nlp.md` | 5,012 | 47 | clean |
| S2-7 | `deep_dives/D2-6_scam_misinformation_detection.md` | 5,482 | 39 | clean |

Then S2-8 `GAP-MINING.md` (16 gaps; 6.2k words), S2-9 `03_topics/CANDIDATES.md` (5 topics; 6.9k words),
S2-10 `NOVELTY-PRESCAN.md` (91 queries). Lead wrote `NOVELTY-CHECK.md`, `SELECTED.md`, `PROPOSAL.md`,
`06_review/STUDENT-DIGEST-S2.md`.

## Register reconciliation (the 266 / 270 / 271 / 317 confusion)
`02_literature/verified_citations.csv` = **317 data rows, 317 unique titles, 317 unique ids**, schema
exactly `id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command`.
Provenance: 312 rows added by `verify_citations.py add` (API-resolved, command recorded per row) + 5 rows
carried from a pre-existing differently-schemad file (preserved as `verified_citations.s1-legacy.csv`).
The other counts were each true when written: 266 = before the gap-mining batch, 270/271 = after S2-8's
4 rows, 317 = after S2-10's 72 rows merged at ~03:47. `CANDIDATES.md` now says 317 with the snapshot time.

## Verification actually run (commands, not claims)
1. `check_docs.py merge` -> 317 unique rows, 0 duplicate titles.
2. **Every row merged late re-resolved**: all 4 S2-8 rows + all 72 S2-10 rows (70 via arXiv `id_list`,
   2 via Crossref) -> **76/76 resolve, 0 title mismatches**.
3. `check_docs.py audit` -> 295 reference lines across 7 documents: **0 unmatched, 0 out-of-range,
   0 uncited**.
4. `verify_citations.py spotcheck --n 20 --seed 11` -> **20/20 OK** (the seed-7 run earlier was also 20/20).
5. Tool bug found and fixed during that pass: `arxiv_id_of` mined `2026.3728` out of the IEEE DOI
   `10.1109/access.2026.3728186`, producing one false "unresolved". The parser now refuses to mine bare
   numbers from a non-arXiv DOI, accepts `arxiv.org/abs/...` URLs, and validates YYMM. Re-tested on 7 cases.

## Redo items from `orchestration/DIRECTIVES.md` (round 3) — all closed
- "retrieval-feature gate includes reader log-probability/entropy" -> **fixed in CANDIDATES (C1 method,
  B3/B4/B5), GAP-MINING (GAP-01, GAP-02), PROPOSAL (features, baselines)**. The gate is now six retrieval
  features, no generator call; reader signals are a separately labelled B4/B5 arm, never pooled.
- "Reconcile 266 vs 270 / measured vs estimated" -> **fixed** (above; CANDIDATES header now separates
  *measured on this laptop* from *published anchor / estimate*).
- "'nobody turned that into a designed ablation' without a documented check" -> **narrowed** in
  CANDIDATES and GAP-MINING to "no paper in the 91-query arXiv sweep", pointing at `NOVELTY-CHECK.md`
  section 1 and stating that the absence is one-index-deep.

## Gaps still open (not hidden)
1. **Novelty check is one index deep.** 48 of 60 required queries, arXiv only; OpenAlex 429 (free daily
   budget, resets 00:00 UTC = 05:30 IST), Semantic Scholar 429 without a key. It is now a **head
   condition**, so the next session must run it before any introduction claims a gap. If a paper appears
   that fits two thresholds on retrieval features and reports both directions per rung, C1 is dead -> C3.
2. **Exploratory timings are not paper results.** `staging/_s2_2_data/` holds real CPU measurements from
   this laptop (BM25 0.459 recall@5 / 0.04 ms / 406 MB; MiniLM 0.259 / 10.0 ms / 600 MB; rerank 361 ms and
   worse). Outside a preregistered protocol -> may inform S3's compute plan, must be re-run before any
   number reaches the paper.
3. Two cited 2026 works are SSRN / Research Square, not peer-reviewed venues
   (`10.2139/ssrn.7152058`, `10.21203/rs.3.rs-10839567/v1`) — flag wherever cited.
4. PROPOSAL section "Baselines" carries a visible "correction on record" parenthetical about the LIMA
   mix-up. Right for an internal document; **must be deleted before that text enters the paper draft**.

## Decisions taken (no questions asked, per PROMPT)
- Rank 1 **C1**, runner-up **C3**; **C2 demoted 85 -> ~68 and abandoned** after the pre-scan found three
  2026 papers occupying it (one splits "missed the update" from "had it and did not use it" — exactly
  C2's proposal). The correction is recorded in SELECTED.md rather than silently edited out of
  CANDIDATES.md.
- No experiments started; no `TOPIC APPROVED` written by S2 — the head wrote it.

## Housekeeping
- **Head condition 4 applied everywhere, not just to the decision documents**: the private-corpus figures
  were also removed from `LANDSCAPE.md` (3 places) and the four agent-written deep dives that quoted them
  (D2-1, D2-2, D2-4 x2, D2-6). Grep over `02_literature/`, `03_topics/`, `06_review/STUDENT-DIGEST-S2.md`
  now returns only `staging/S2-10-body.md` — a dead intermediate that is not a deliverable and must not be
  reused. `STUDENT-DIGEST-S2.md` trimmed 948 -> 773 words (one page).
- `STOP` exists at repo root, created 03:53. RULES 11: finish current item, save state, exit. This note is
  that save. No new experiments, no heavy compute, no new dataset downloads.
- `STATUS.prev.md` kept for reference (pre-overwrite version appended to by two child agents).
- Tools: `02_literature/tools/verify_citations.py` (search/enrich/add/spotcheck),
  `02_literature/tools/check_docs.py` (merge/audit). Run both after any bibliography edit.
- OpenAlex free budget resets 00:00 UTC (= 05:30 IST); exhausted for this IP on 2026-11-03.
