# Independent review — COMPLETENESS, STRUCTURE, TRACEABILITY, SCOPE (R3-6b, batch 2)

Reviewer: completeness reviewer (res-s1 subagent). Date: 2026-11-19. Read-only.
Scope reviewed: `07_student/ROUND3-DIGEST.md`, `07_student/VIVA-QA.md`, `07_student/SOURCE-MAP.md`,
against `sessions/R3-6b-student-pack/TASK.md`, `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md`,
`orchestration/HEAD-REVIEW.md` checkpoints 9–11, the three writer reports, and `PROGRESS.md`.
Nothing was edited. This report is the only file written.

## Check table

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Digest exists, explains Round 3 + the three R3-3b findings, ~2 pages, all required limit explanations | **PASS** | `ROUND3-DIGEST.md` 1,146 words (83 lines) → inside the 1,100–1,350 band, defensible as "about two pages" (no code, 3 small tables). Round 3 explained at L9 (44 must-fix items, one lane each, N8); three sections at L15/L27/L37. Required limits present: post-hoc/exploratory (L3, L49), not human gold (L25, L51), no frozen verdict revised (L4, L50), not in the draft (L4 L50, N6), κ 0.2802 meaning (L19–L23), MF-7 tautology (L41), D3 pooled/rung −1 (L45, L53), H1 not exercisable (L57–L61), MF-14 registered vs exploratory (L63–L71). |
| 2 | Viva Q&A covers MF-14, H1, κ, gold indicator, forbidden claims; first-semester readable | **PASS** | 13 Q&A, 1,328 words. Per-answer words: Q1 82, Q2 115, Q3 114, Q4 101, Q5 54, Q6 109, Q7 93, Q8 71, Q9 67, Q10 54, Q11 58, Q12 142, Q13 75 → **max 142, median 82**. Topics: Q2 MF-14, Q3 H1, Q4 κ, Q6 gold indicator, Q12 refusal list. Jargon is defined in-line ("abstention gate", "rung", "bootstrap"). |
| 3 | SOURCE-MAP maps every numeric claim to exact path/key, exact value, rounding; no unsupported numbers | **PASS** | 32 rows. All 23 numeric IDs + 8 fact IDs of the inventory are present. Every JSON key in the map was re-read here and resolves: C01 0.2802, C02 0.59/59/100, C04 41, C05 62/21, C06 35/6/0, C07 56/0.56, C08 0.0/0.2991/0.026/0.1379/25×4, C09 0.1975/5/0.05, C10 0.9823630831643002 [0.9776211411662427, 0.9866543835742593], C11 0.8738488843813388 [0.8586833140203312, 0.8893003500532195], C12 0.10851419878296142 [0.09458017350090517, 0.12252082237972457] nested `contains_zero`=false, C13 1879/400/1479/18, C13b 10000/20261118, C14 0.9762, C15 1.0, C16 1.0/true, C17 655/145/800/0.7327, C18 342/58/313/87, C19 false/−1; C20 1.0, C21 0.8471, C22 0.1253 in the two `results_full.json`. All quoted line numbers spot-checked and correct (mf10:236/243/246/251/259/277, mf17:1254–1256/1178–1180/1395–1397/1046/1050/1053/1660, mf7:1800/1801/1767/1848/1849/1896/1906, c1:536/597/364, c1c:500). sha256 prefixes match the inventory. C03 derivation reproduces: (0.59−0.2802)/(1−0.2802)=0.4304. No unsupported numeral found in either student document. |
| 4 | Every numeral carries a claim ID | **FAIL (minor)** | 42 digit-bearing sentences in the digest, 35 carry an ID; 53 in the viva, 39 carry an ID. After discarding headings, list numbering and ID fragments, **3 substantive sentences carry numerals with no ID**: `ROUND3-DIGEST.md:71`, `ROUND3-DIGEST.md:23`, `VIVA-QA.md:19`. ID mentions: digest 54, viva 59 (all inside parentheses). Detail in gaps 2–4. |
| 5 | Required framing (a)–(h) present | **PASS** | (a) exploratory/post-hoc ×3 — digest L3/L49, viva Q11; (b) not yet in draft — digest L4/L50 (N6), viva Q11/Q12; (c) no frozen verdict revised — digest L4/L50, viva Q2; (d) κ ≠ accuracy, ≠ human gold — digest L23/L25, viva Q4; (e) gold indicator tautological — digest L41, viva Q6; (f) D3 pooled rung −1, no per-rung — digest L45/L53, viva Q9; (g) H1 not exercisable, neither confirmed nor refuted — digest L61, viva Q3; (h) MF-14 three run labels — digest L67–L69, viva Q2. |
| 6 | Git scope: protected paths untouched; expected writes identified | **PASS (with warning)** | No path under `05_paper/template`, `05_paper/draft`, `05_paper/tables`, `05_paper/figures` is modified (clean). Expected writes under `07_student/` (3 files) and `sessions/R3-6b-student-pack/` (untracked). **Warning:** `04_experiments/RESULTS-INDEX.json` (staged, `M `) and `06_review/audits/numbers-audit.md` (staged, `M `) are modified in the working tree. I cannot attribute these to any person; by diff content they belong to the R3-4f probe run (see git evidence), not to R3-6b. |
| 7 | Cross-document consistency (10 numbers) | **PASS** | 37 numeric tokens appear in both documents; every shared token is byte-identical. Sampled 10: 0.2802, 0.59, 41, 56%, 0.43, 0.9824, 0.8738, 0.1085, 12.53%, 84.71% — same rendering, same rounding in both. Near-miss scan (same value, different digits) found none. Only divergence: digest prints "95% interval" (L33), viva prints "interval" (Q7) — the confidence level is dropped in the viva, no value differs. |
| 8 | Three writer reports exist and state their own proof checks; lead's checks documented | **PASS (with caveat)** | `reports/writer-digest.md` (1,761 w), `reports/writer-viva.md` (1,471 w), `reports/writer-source-map.md` (1,963 w) all exist with command/output proof blocks (e.g. digest: `python -c "import json; …"` → `0.2802 0.59 100`; map: `grep -c '^| C\|^| N'` → 32). Lead's own batch-1 verification is documented at `PROGRESS.md:102–113` (sha256 re-computed, line numbers spot-checked, C03 derived two ways). **Caveat:** of the other two batch-2 reviewer reports, `review-limits.md` exists (written 02:58, concurrently with this review) but `review-numbers.md` did not exist at 03:06, so the number-by-number independent check the TASK requires is not yet documented. `PROGRESS.md:126–132` still reads as batch 2 not having run. |

Verdict: **NOT COMPLETE** — one check failed (numerals-with-ID) and one student sentence asserts a fact the inventory explicitly forbids (gap 1).

## Gaps

1. **`07_student/VIVA-QA.md:24` — unsupported and false claim, no map row, must be removed.**
   Text: "The 84.71% arm over-refused past its declared cap — not a clean operating point."
   `CLAIM-INVENTORY.md:85–86` states: "no writer may assert a cap breach or cap compliance for C21/C22,
   because those keys are deliberately not in this inventory." `PROGRESS.md:114–119` already records the
   real held-out over-refusal (9.50% as-run, 11.00% spec-corrected) and calls the sentence false; it is
   still in the file. `SOURCE-MAP.md` has no row for any over-refusal or cap claim, so the sentence has
   no source at all.
2. **`07_student/ROUND3-DIGEST.md:71` — three claim numbers, no ID.**
   "Never print 12.53% as replacing 100.00%, nor 84.71% as a clean point — that arm came from deviation D1."
   The three values carry C20/C21/C22 in the table two lines above but no ID in the sentence itself.
3. **`07_student/ROUND3-DIGEST.md:23` — bare numeral.** "0.2802 is **modest agreement beyond chance between
   these two LLM labellers**." The paragraph's IDs (C03, C01, C02) come later in the sentence sequence; the
   restated κ has no ID of its own at that point.
4. **`07_student/VIVA-QA.md:19` — bare numeral.** "The 84.71% arm over-refused…" — same sentence as gap 1,
   and 84.71% (C21) is not tagged in it.
5. **`07_student/SOURCE-MAP.md:13,43` — row ID `C13b` does not exist in the inventory.**
   The map adds a 32nd ID to carry `n_boot`/`seed` and declares it a split of C13 (L13–17, L43). The
   reverse-join therefore fails literally: map row IDs ⊄ inventory IDs. No student document cites `C13b`,
   so nothing is unresolvable — but the map now contains an ID the inventory does not define.
6. **`07_student/ROUND3-DIGEST.md:52` — over-broad citation.** "**AUROC is threshold-free, not an accuracy**
   (C23)". C23 is the PREREG comparability rule (PREREG L262–264: thresholds not comparable, AUROC is
   because it is threshold-free); "not an accuracy" is not in C23 — it lives in MF-17's limitation notes.
   No ID covers the "not an accuracy" half of that bullet.
7. **No student document points at `07_student/SOURCE-MAP.md`.** Digest: 0 mentions; viva: 0 mentions (it
   points at `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` at L4, an internal file). Deliverable 3's
   traceability chain is not reachable from the pack a student is given. `PROGRESS.md:121` records this as
   open.
8. **`sessions/R3-6b-student-pack/PROGRESS.md:58` — stale figures.** "Digest 1,204 words; viva 14 answers /
   1,198 words; source map 32 `| MAP-` rows" contradicts the final numbers at `PROGRESS.md:98`
   (1,146 / 13 Q&A / 1,328 / map C01–C23+N1–N8). The batch-1 section was not marked superseded.
9. **Batch-2 review evidence incomplete.** Under `reports/` only the three `writer-*.md` files plus
   `review-limits.md` (02:58) and this file exist; **`review-numbers.md` is absent**, so the TASK's
   independent number-by-number check and the lead's "every numeric mapping checked" gate are not yet
   documented for the final files (`PROGRESS.md:126–132`).

Nothing else found: all 31 inventory IDs resolve to a map row, all map values match the JSON, both student
documents print shared numbers identically, and no protected path carries this lane's work.

## Set comparisons (mechanical)

IDs cited, extracted by regex `\b(C\d{2}b?|N[1-8])\b`:

- **Digest (28 IDs):** C01 C02 C03 C04 C05 C06 C07 C10 C11 C12 C13 C14 C15 C16 C17 C19 C20 C21 C22 C23 N1 N2 N3 N4 N5 N6 N7 N8
- **Viva (29 IDs):** C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 N1 N2 N3 N4 N5 N6
- **Map rows (32):** C01–C23 (23) + C13b + N1–N8 (8)
- **only-in-digest:** N7, N8
- **only-in-viva:** C08, C09, C18
- **missing-from-map (cited in a student doc, absent from map):** **none**
- **map IDs not in inventory:** C13b (declared split — gap 5)
- **inventory IDs not in map:** none (23/23 numeric, 8/8 fact)
- **map rows cited by neither student document:** C13b

Counts: inventory 31 IDs (23 C + 8 N); map 32 rows; digest cites 28; viva cites 29; union 31 = full inventory.
ID-tag mentions: digest 54, viva 59; numeral occurrences: digest 162, viva 180 (most are ID fragments,
rung labels R1–R4, dates, heading numbers).

Word counts: digest 1,146; viva 1,328 (13 answers, max 142, median 82); source map 32 rows.

## Git scope evidence (verbatim)

```
$ git status --short
M 04_experiments/RESULTS-INDEX.json
 M 04_experiments/results/summary_toy.json
 M 04_experiments/toy/toy_runs.json
 M 06_review/audits/numbers-audit.md
 M orchestration/HEAD-REVIEW.md
?? 04_experiments/runs/20261118T202642Z_toy_baseline_17239f6-2/
?? 04_experiments/runs/20261118T202642Z_toy_baseline_17239f6/
?? 04_experiments/runs/20261118T202643Z_toy_baseline_17239f6/
?? 04_experiments/runs/20261118T202643Z_toy_ours_17239f6/
?? 04_experiments/runs/20261118T202644Z_toy_ours_17239f6-2/
?? 04_experiments/runs/20261118T202644Z_toy_ours_17239f6/
?? 04_experiments/runs/20261118T202652Z_toy_ours_17239f6-2/
?? 04_experiments/runs/20261118T202652Z_toy_ours_17239f6/
?? 07_student/
?? sessions/R3-4e-consistency/
?? sessions/R3-4f-bind-3b/
?? sessions/R3-6b-student-pack/
?? sessions/R3/orch/BRIEF-pass6.md
?? sessions/R3/orch/LAST-pass6.txt
?? sessions/R3/orch/REPORT-pass6.md

$ git diff --stat
 04_experiments/RESULTS-INDEX.json       |   6 +-
 04_experiments/results/summary_toy.json |   6 +-
 04_experiments/toy/toy_runs.json        |  26 +-
 06_review/audits/numbers-audit.md       | 741 ++++++++++++++++++--------------
 orchestration/HEAD-REVIEW.md            |   6 +
 5 files changed, 435 insertions(+), 350 deletions(-)
```

Readings:

- **Clean (no modified file at all):** `05_paper/template/**`, `05_paper/draft/**`, `05_paper/tables/**`,
  `05_paper/figures/**`; also `04_experiments/results/c1/**` and `c1_corrected/**`.
- **Expected writes for this lane:** `07_student/` (ROUND3-DIGEST.md, VIVA-QA.md, SOURCE-MAP.md) and
  `sessions/R3-6b-student-pack/` — both untracked, both inside the two owned roots.
- **Unexpected, not this lane's content:**
  - `04_experiments/RESULTS-INDEX.json` (staged `M `): diff only repoints three toy `run_id` values to
    `20261118T2026xxZ_toy_*_17239f6` and bumps `updated_at` to 2026-11-18T20:26:51Z.
  - `06_review/audits/numbers-audit.md` (staged `M `): the audit now declares itself "NOT a paper draft"
    and audits `sessions/R3-4f-bind-3b/repro/probe.md`, 25 findings, FAIL. mtime 02:44, after this lane's
    student files.
  - `04_experiments/results/summary_toy.json`, `04_experiments/toy/toy_runs.json`, eight
    `04_experiments/runs/20261118T2026*_toy_*` directories: same toy-run burst.
  - `orchestration/HEAD-REVIEW.md` (+6 lines): Checkpoint 11 text only, mtime 00:02 — written by the head
    review before this lane's writers ran; the lane treats checkpoint 9–11 as read-only input.
  - `sessions/R3-4e-consistency/`, `sessions/R3-4f-bind-3b/`, `sessions/R3/orch/*pass6*`: other lanes.
- **Attribution:** the RESULTS-INDEX/toy/numbers-audit changes are R3-4f probe artefacts by content (the
  audit's own "Audited path" is that lane's `repro/probe.md`), i.e. not R3-6b. I cannot name the process
  that wrote them; I only rule out this lane's writers, whose reports state no writes outside the two owned
  roots. `06_review/audits/numbers-audit.md` currently records a **FAIL** for the R3-4f probe — outside
  this pack's scope, noted only because it sits in a protected path.
