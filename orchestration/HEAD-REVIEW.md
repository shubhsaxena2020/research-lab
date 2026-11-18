# HEAD-REVIEW (Claude Code) — latest at 01:20 IST, 2026-11-03
Phase 2 (experiments) stays LOCKED. This file does not yet contain the approval line.

## Checkpoint 1 findings (spot-checked from disk, not from your reports)
- S1: 7 foundation docs exist (~36k words) — good volume, but (a) STATUS.md still says NOT STARTED: update it NOW and every 15 min (RULES.md #12); (b) `00_foundations/_tmp_ethics.md` is a stray temp file: delete it; (c) 36k words is too much for a first-semester student mid-exams: each doc needs a 10-line "READ THIS FIRST" summary at the top, and 06_review/STUDENT-DIGEST-S1.md must be <= 1 page. Priority next: B1-B6 (PSIT public data) — nothing is in 01_psit_data yet except empty folders.
- S1 link check: 13/14 sampled URLs resolve (the one 403 is a bot-blocking US State Dept page, fine). Link existence is NOT claim support: for the 20 most important claims (venue deadlines, eligibility rules, AI-use policies) quote the exact sentence from the source page and its URL in a `claims_evidence.md`.
- S2: good use of 7 parallel subagents. Remember every citation goes through verified_citations.csv before use; I will re-resolve a random 20 at the next checkpoint.
- S3: you are running Phase 1 mostly alone. USE `delegate_task` with up to 9 subagents: the 8 packages S3-1..S3-8 are independent, launch them as one batch. One owner per file.
## Standing decisions
- Topic decision is the head's. S2 delivers SELECTED.md + NOVELTY-CHECK.md; the head reads them, then writes `TOPIC APPROVED` (or a veto) here.
- Do not spend effort polishing prose before data/tools exist; correctness and traceability first.

## Checkpoint 2 — 03:25 IST (head, independent checks)
- S1 PSIT dataset: re-verified 12 random records against Crossref directly: 10/12 exact (title + PSIT affiliation + year); 2/12 title/year match but PSIT not in Crossref's deposited affiliation (probably the Europe PMC route — NOT confirmed). The "793 is a floor" framing is correct and honest. NAAC-SSR inconsistency table (590 vs 117 UGC-CARE papers) is the most valuable finding for the student; keep it prominent.
- OpenAlex/Semantic Scholar/Crossref/DBLP rate limits were hit by our own sessions (OpenAlex free daily budget shows $0 for this IP until 00:00 UTC). Do NOT hammer public APIs again; cache and back off. Do NOT sign up for API keys with the student's email — that is the student's decision.
- S3: Phase 1 reported complete; keep Phase 2 locked. S2: 271 verified citations, CANDIDATES.md exists; waiting for NOVELTY-CHECK.md + SELECTED.md + PROPOSAL.md. I will review them and decide the topic myself.

## Checkpoint 3 — TOPIC DECISION — 04:00 IST 2026-11-03 (head)
Reviewed 03_topics/SELECTED.md, PROPOSAL.md, 02_literature/NOVELTY-CHECK.md in full.
Independent check: resolved 16 of the arXiv IDs the proposal/novelty case rests on against the arXiv API: 15/16 exist with matching titles and dates (all 2026 papers real).
1 error found and fixed by the head: B4's citation arXiv:2305.11206 is LIMA (alignment), NOT the confidence-baseline paper; replaced by Kadavath et al. arXiv:2207.05221 (verified). Add 2207.05221 to verified_citations.csv. Lesson for all sessions: an ID that resolves is not proof it supports the sentence — check title against claim.

TOPIC APPROVED

Approved topic: C1 "How Hard Are Your Negatives? A Hardness Ladder for Retrieval-Feature Abstention Gates". C3 (scam operating points) is the day-3 fallback exactly as SELECTED.md states; C2 abandoned.
Conditions (binding on S3 and any later session):
1. Honest framing everywhere: INCREMENTAL / workshop-level measurement paper. Never write "novel", "first", or "state of the art". NOVELTY-CHECK is one index deep (arXiv only): before the introduction claims any gap, re-run against OpenAlex (budget resets 00:00 UTC = 05:30 IST) and Semantic Scholar, plus >=15 slice-wording queries per finalist. If a paper appears that fits two thresholds on retrieval features and reports both directions per rung, C1 is dead -> move to C3.
2. The separability audit (surface-only AUROC > 0.75 on any rung -> rebuild that rung) is a hard gate before any result is reported.
3. Pre-registration first: 04_experiments/PREREGISTRATION.md frozen with a hash BEFORE the first run; deviations logged.
4. The "47 of 82 refused" figure comes from the student's PRIVATE memory-system evaluation, whose held-out set was contaminated; do NOT present it as a result or a dataset. At most one sentence, as an unmeasured motivating anecdote, no numbers from that corpus. All experiments use public data only (SQuAD 2.0 dev, 2WikiMultihopQA).
5. Compute: all heavy jobs through C:\Users\shubh\ai-memory-core\tools\heavy.py (shared lock with the memory build — the laptop is shared) and never while free RAM < 8 GB. No OpenAlex/Semantic Scholar hammering; cache responses.
6. Every citation re-verified (resolve + title-vs-claim) before it enters a draft; every number traceable (tools\check_numbers.py).

## Checkpoint 4 — 06:05 IST (head, after reading S3's Phase-2 report and checking the artefacts)
Verified: prereg hash frozen 03:59 before any real run (toy runs only before); deviation D1 appended openly (hash 0a85a6b1.. -> db6c9781..); ablation_no_rank.json is genuine (dev AUROC 0.9875 vs 0.9879 main; 10 vs 12 features; different thresholds — the equal 4-decimal TEST AUROC 0.9824 is a coincidence, not a bug).
STOP file (created by the day timer 03:51/03:53) removed by the head at 06:00; S2b and S3 may run.
RESULT: H1 refuted (precision 1.0 on all rungs), H3 refuted, H2 degenerate. SELECTED.md named "abstain precision flat across rungs" as the trigger to fall back to C3. That trigger HAS FIRED. Head decision:
- Do NOT silently switch and do NOT hide it. Keep C1 but REFRAME it as an honest negative-result / benchmark-audit paper: "negatives built by paragraph substitution are trivially separable (surface features alone ~0.5 AUROC, but adding question-passage overlap gives 0.89-0.98), so retrieval-feature gates look perfect on them" — with the audit procedure as the contribution. This is legitimate only if stated plainly as a negative result in title/abstract (workshop negative-results tracks, arXiv).
- C3 (scam operating points) stays documented as the alternative if the student prefers a positive-result paper; the decision is the student's to confirm.
Next work for S3 (S3b), in priority order: (1) tools\check_numbers.py must PASS on the draft (26 findings: fix or index every number; no exemptions that hide real numbers); (2) exploratory rung 5 "overlap-matched negatives" (negatives chosen to match answerable items' question-passage overlap) as a DECLARED exploratory deviation — does any retrieval-only gate survive when overlap is controlled?; (3) H2 transfer: extract features for the 400 2WikiMultihopQA items, run the FROZEN operating point; resolve the correct citation for 2WikiMultihopQA (Ho et al., COLING 2020 — resolve it properly; arXiv 2011.01079 is NOT it); (4) review round 2, answer all 12 must-fix items or rebut with evidence; (5) originality check (deposit sources), fix draft to say NEGATIVE RESULT honestly. Never claim more than measured.

## Checkpoint 5 — ROUND 3 START — 2026-11-08 (head)
Owner decisions (Shubh, 2026-11-08): keep C1 as the honest negative-result / audit paper (C3 stays documented, not started);
all Hermes on `nilabh/Deepseek-v4.1-Flash` via 9Router; 7 lead sessions (4 main laptop, 3 laptop 2), each running
at least 3 parallel subagents per batch.
- Round 3 = answer all 44 round-2 must-fix items (06_review/reviews/round2-c1/AGGREGATE.md), plus the S3 student digest,
  related-work/novelty refresh and a real PDF build. Lane cards: sessions/R3-*/TASK.md; triage: sessions/R3/TRIAGE.md;
  shared rules: sessions/R3/COMMON.md.
- orchestration/DIRECTIVES.md (Codex, 2026-11-03) is SUPERSEDED for round 3. Follow RULES.md, this file, COMMON.md, your TASK.md.
- Frozen confirmatory run is immutable: never refit, never overwrite any existing file in 04_experiments/results/ or runs/.
  New numbers go in new files under 04_experiments/results/c1/r3/<lane>/.
- No lead commits to git. The head commits at checkpoints.

## Checkpoint 6 — Codex orchestration and R3-4c fold — 2026-11-18

Codex is orchestrating the research-lab paper pass from 2026-11-18; Claude Code coordinates checkpoint resumes. Laptop 2 is offline. Only Hermes profiles res-s4 and res-s1 may run, using the configured nilabh/Deepseek-v4.1-Flash route. The res-s1 R3-7b-latex-main lane is running and owns `05_paper/latex-build/**`; leave it untouched.

Correction to the prior checkpoint: the 11-08 round-3 prompt packs were not stale. `tools/simulate_review.py` hashes the draft after newline normalization; tool hash `9194a481` and byte hash `e346271e` identify the same draft. The six persona reviews, INGEST, and AGGREGATE in `06_review/reviews/round3-c1/` are a valid simulated review of that pre-fold draft. Round-3 scores must remain labelled as pre-fold scores.

R3-4b-review was stopped because it skipped deliverable 1: it did not fold the 21 partial and 5 deferred round-2 items into `05_paper/template/draft_template.md`; the template and draft hash were unchanged. Its review outputs are retained as valid review evidence. Round-3 aggregate: six borderline, mean 5.67/10, 41 distinct must-fix items (22 persisted themes, 19 new).

R3-4c-fold plan: res-s4 will use existing evidence to fold the 26 remaining round-2 items and the 41 round-3 must-fix items where support permits; mark unsupported items honestly unresolved; rebuild the generated draft; regenerate the round comparison with an explicit pre-fold label and update the response letter for both rounds. Do not run another review round or new experiments. Required gates are a changed draft SHA, `check_numbers.py` at 0 findings, and `check_all.py` at 4/4 PASS. R3-4c excludes `05_paper/latex-build/**`.

## Checkpoint 7 — R3-7c LaTeX citations — 2026-11-18

R3-7b is complete. Claude Code verified the main-laptop Tectonic build, but identified transient Windows file-mapping failures, no emitted citations despite a populated `refs.bib`, and three duplicate `fig:main-accuracy` labels. R3-7c-latex-citations is assigned to the now-idle res-s1, owning only `05_paper/latex-build/**` and its lane folder. It will add bounded transient-error handling / safe output promotion, map explicit draft DOI/arXiv markers only to existing BibTeX keys, preserve and report unmatched markers, make figure labels unique, rebuild both PDFs, run converter/PDF checks, and update BUILD-REPORT. It must not edit the draft/template owned by res-s4. Do not restart the shared gateway or touch the separate InMobi research project; research-lab remains capped at res-s1 and res-s4. Updated round-3 compute policy is GPU first for model jobs; no model work is planned in this TeX lane.

## Checkpoint 8 — R3-4d independent fold verification — 2026-11-18

R3-4c completed and was committed as `533998b`; Claude Code verified draft SHA `89e92e79`, zero number findings, reproducible build, and unchanged preregistration/frozen results. R3-4d is assigned to res-s4 to independently quote draft evidence for every resolved response-letter item, reconcile the reported 86 verdicts against 44 round-2 plus 41 round-3 IDs, fix MF-14 in the template using existing result keys, and fold only wording/structure partials with existing evidence. Per-batch gates: zero number findings, byte-identical draft across two builds, and check_all 4/4 PASS. R3-4d must not touch `05_paper/latex-build/**`; res-s1 is running R3-7c. No new experiments or review round in this lane.

After R3-4d and R3-7c finish and are independently checked, the proposed next wave is a fresh simulated review round 4 packed against the verified final draft SHA. This is a recommendation only, not launched here.

## Checkpoint 9 — R3-3b deferred analyses launched — 2026-11-18

Claude Code verified R3-7c (`ce0674e`) and reported the res-s1 profile idle. res-s1 is assigned to `R3-3b-deferred-analyses` for fresh post-hoc analyses from existing data addressing round-2 MF-17 AUROC intervals, MF-10 answerability adjudication on the existing seeded 100-negative sample, and MF-7 gold-paragraph control. It owns only `04_experiments/src/r3_r3_3b_*.py`, new files under `04_experiments/results/c1/r3/R3-3b/**`, and `sessions/R3-3b-deferred-analyses/**`. It must not touch any R3-4d-owned paths, prior results, frozen run, preregistration, or draft/template; no new review or draft edit is requested.

Three read-only parallel feasibility audits found that prior R3-3 outputs already include MF-17 bootstrap intervals, MF-10 LLM adjudication, and MF-7 gold-indicator control. Their limitations motivate a separately keyed post-hoc re-derivation: the prior MF-10 labels omit GPU/device provenance and have low agreement; the MF-7 gold indicator is tautological and D3 has pooled hit/miss rather than per-rung data; the MF-17 paired analysis should assert item-id alignment. res-s1 is instructed not to overwrite or relabel the old evidence. It was launched through `ops/hermes_runner.ps1` with budget 10800. Immediate process check found Hermes `-p res-s1` PID 10412 (runner PowerShell PID 43428). Prompt double-quote check: false (zero quote characters).

res-s4 remains assigned to R3-4d. No lead was polled or waited on. Claude Code is to independently verify the new outputs before integrating any result keys.
