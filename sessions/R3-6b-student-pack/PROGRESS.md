# R3-6b student pack — PROGRESS

Lane: R3-6b-student-pack. Profile res-s1. Started 2026-11-19T00:01 IST.

## Read first (done, lead)

- `RULES.md`, `sessions/R3-COMMON.md` (`sessions/R3/COMMON.md`), `sessions/R3/TRIAGE.md`,
  `orchestration/HEAD-REVIEW.md` checkpoints 9–10, `sessions/R3-6b-student-pack/TASK.md`,
  `ops/lead_protocol_r3.txt`.
- Evidence: `04_experiments/results/c1/r3/R3-3b/ANSWERS.md`, `mf17_auroc_intervals.json`,
  `mf10_adjudication.json`, `mf7_gold_control.json`, `04_experiments/PREREGISTRATION.md`
  (§1 H1 lines 22–25, §10 D1 lines 165–181, §10 D4 lines 240–268, D5 line 272),
  `sessions/R3-4d-verify-fold/reports/mf14-fix.md`, `04_experiments/results/c1/results_full.json`,
  `04_experiments/results/c1_corrected/results_full.json`.
- No `STOP` file. No commit, no branch change, no write outside `07_student/` and this lane folder.

## Lead's own source verification (before handing a claim inventory to writers)

Parsed directly with `python`/`json.load`; values below are what the files hold.

| Claim | Source | Value |
|---|---|---|
| kappa overall | `mf10_adjudication.json` `results['c1.r3_3b.mf10.cohen_kappa_overall']` (full: `mf10.agreement.kappa`) | 0.2802 (0.2801966292134831) |
| raw agreement / n | `...mf10.raw_agreement_po`, `n_agreed`, `n_items`, `n_disagreed` | 0.59, 59, 100, 41 |
| labeller answerable | `...labeller_A_answerable_n`, `labeller_B_answerable_n` | 62, 21 |
| resolver / resolved | `...resolver_resolved_1_n`, `_0_n`, `resolved_answerable_n`, `_share` | 35, 6, 56, 0.56 |
| per-rung kappa | `...rung1..4.kappa` | 0.0, 0.2991, 0.026, 0.1379 |
| frozen held-out AUROC | `mf17_auroc_intervals.json` `...frozen_heldout_auroc.point/.ci95_lo/.ci95_hi` | 0.9823630831643002 [0.9776211411662427, 0.9866543835742593] |
| corrected held-out AUROC | `...corrected_heldout_auroc.*` | 0.8738488843813388 [0.8586833140203312, 0.8893003500532195] |
| paired diff | `...paired_auroc_diff.diff/.ci95_lo/.ci95_hi`, nested `.contains_zero` | 0.10851419878296142 [0.09458017350090517, 0.12252082237972457], false |
| held-out n / resampling | `mf17...denominators.held_out_common`, `n_boot`, `seed` | 1,879 items (400 rung 0 + 1,479 negatives, 18 article clusters), 10,000, 20261118 |
| gold-indicator control | `...mf17.gold_indicator_control_auroc.point`; `mf7...dev.r1.auroc_plus_is_gold`, `auroc_is_gold_alone_answerable_oriented`, `is_gold_deterministic_from_label` | 1.0; 1.0; 1.0; true |
| gold control baseline | `mf7...dev.r1.auroc_surface_lex` | 0.9762 |
| D3 pooled | `mf7...d3_pooled.all.n_hit/.n_miss/auroc_surface_lex_hit_vs_miss` | 655, 145, 0.7327 (dev 342/58, test 313/87) |
| D3 per-rung | `mf7...d3_pooled.per_rung_R1_R3_estimand_available`, `rungs_present_value` | false, −1 |
| MF-14 registered band R4 | `c1/results_full.json` `test.band_primary.per_rung.4.abstain_precision` | 1.0 → 100.00% |
| MF-14 frozen exploratory R4 | `c1/results_full.json` `test.exploratory_band.per_rung.4.abstain_precision` | 0.8471 → 84.71% |
| MF-14 spec-corrected exploratory R4 | `c1_corrected/results_full.json` `test.exploratory_band.per_rung.4.abstain_precision` | 0.1253 → 12.53% |
| AUROC pair (MF-14) | `c1`/`c1_corrected` `discrimination.test_auroc` | 0.9824 → 0.8738 |

Non-result facts: H1 criterion = `PREREGISTRATION.md` §1 lines 22–25 (non-increasing rungs 1→4 and
rung1−rung3 drop ≥ 15 points). "Not exercisable" = §10 D1 lines 165–172: at the registered rule
(maximise dev abstain recall subject to dev abstain precision ≥ 0.80) fitted t_lo = 0.907,
t_hi = 0.948, single t = 0.939, 92.9% of dev items refused below t_lo alone, dev over-refusal 0.755,
"Every gate then reports abstain precision 1.00 in every rung, so H1 and H3 cannot be tested at that
operating point." D1 point 2: the exploratory arm "cannot rescue a hypothesis". D4: thresholds refitted,
"not comparable between the two runs; AUROC is". Not-in-draft: HEAD-REVIEW checkpoint 10 — R3-3b
"must not be bound by this lane", "Nothing is bound into the draft yet" (BRIEF-pass6 §State).

## Batch 1 — three parallel writers (one blocking delegate_task, exactly 3 tasks)

| Task | Owned write path | Report |
|---|---|---|
| digest writer | `07_student/ROUND3-DIGEST.md` | `sessions/R3-6b-student-pack/reports/writer-digest.md` |
| viva writer | `07_student/VIVA-QA.md` | `.../reports/writer-viva.md` |
| source-map writer | `07_student/SOURCE-MAP.md` | `.../reports/writer-source-map.md` |

All three files exist (`ls -l` 01:14 / 00:34 / 00:46). Digest 1,204 words; viva 14 answers / 1,198 words;
source map 32 `| MAP-` rows. No path outside the two owned roots was written by the writers.

## What is verified vs NOT verified — defects found by the lead

Verified: every numeric value the three documents could cite exists in the JSON at the key stated above,
and the seven MF-14 numbers the writers could not read are the ones the lead parsed directly from
`c1/results_full.json` and `c1_corrected/results_full.json` (they were correct as handed down).

NOT verified / defective:

1. **The claim-ID join between the three files is broken.** The digest and viva key their numbers to IDs
   assigned from the brief's topic ranges (digest MAP-1 = kappa 0.2802), while `SOURCE-MAP.md` assigned
   the same IDs to different topics (kappa sits at its MAP-8, MF-7 starts at its MAP-15). The documents
   and the map do not resolve to each other, so the deliverable requirement "map every numeric claim to
   the exact source path and JSON result key" is not met in substance.
2. **`SOURCE-MAP.md` rows MAP-24..MAP-27 are the wrong claims.** They map pooled registered/exploratory
   0.9993 / 0.755 / 0.0527 / 0.9216 / 0.095 / 0.2544 instead of the MF-14 comparison the digest and viva
   cite under those IDs (registered band R4 100.00%, frozen exploratory R4 84.71%, spec-corrected
   exploratory R4 12.53%, AUROC 0.9824 → 0.8738). The MF-14 block therefore has no correct map row.
3. **Neither student document cites the MF-14 numbers to a file it can point at.** Both writers disclosed
   that 100.00 / 84.71 / 12.53 were taken from the brief, not from a file they opened. The values are
   right (lead-verified), but the traceability requirement is not yet satisfied on the page.
4. **Digest dropped MAP-9** (per-rung kappa) in its length pass while viva cites it; unverified that every
   numeral in the final digest text still carries a resolvable ID after that edit.
5. Digest is 1,204 words (target 900–1,150, ceiling 1,300) — inside the ceiling, above target.

## Resume (2026-11-19, second run) — root-cause fix of the ID join, then batch 1 again

The three batch-1 defects were all symptoms of one cause: three writers each invented their own claim
numbering. Fix applied at the source, not in the prose:

- Lead wrote `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` — 23 numeric IDs (C01–C23) and 8 fact IDs
  (N1–N8), each with the exact source path, the exact JSON key or PREREG section+lines, the exact stored
  value and the permitted rounding. Every row was produced by `json.load` on the file itself.
- Batch 1 was re-run as one blocking `delegate_task` with exactly three parallel writers, each owning one
  file and reading the same inventory: digest -> `07_student/ROUND3-DIGEST.md`
  (`reports/writer-digest.md`), viva -> `07_student/VIVA-QA.md` (`reports/writer-viva.md`), map ->
  `07_student/SOURCE-MAP.md` (`reports/writer-source-map.md`). Because SOURCE-MAP covers **all** inventory
  IDs, the join is by construction rather than by negotiation.
- Result: digest 1,146 words / 83 lines; viva 1,328 words / 128 lines, 13 Q&A; source map 32 rows /
  3,157 words. All three use the same ID namespace (digest C01–C07,C10–C17,C19–C23; viva C01–C23;
  map C01–C23 + N1–N8).

### Lead verification performed on batch 1 (opened every file, re-ran the checks)

- sha256 re-computed for all five evidence files; they match the map's `Paths and hashes` table exactly
  (`2324d8605534`, `07c3a0f8a54f`, `0728d92714d0`, `e4cf65cb0b2b`, `936ce0b89e22`).
- JSON line numbers spot-checked against the map (mf10:236/246 = `n_items`/`cohen_kappa_overall`;
  mf17:1256 = `frozen_heldout_auroc.point`; c1:536 = `abstain_precision: 1.0`;
  c1c:500 = `0.1253`; mf7:1800 = `d3_pooled.all.n_hit: 655`). All correct.
- C03 derivation independently re-derived two ways: `Pe = (Po − κ)/(1 − κ) = 0.4304` and
  `Pe = (62×21 + 38×79)/10000 = 0.4304`.
- Inventory corrected in three places after that check: C17 gained `.n = 800` (both student files print
  "of 800"); N5 gained the `mf10.exploratory_status` "NOT human gold" string; N7 widened to limitation
  items 1–2–5 (item 2 is the "no model is retrained" sentence the digest cites).
- **Defect found and confirmed by the lead's own check:** `VIVA-QA.md` Q2 says "The 84.71% arm over-refused
  past its declared cap". That is false. Held-out over-refusal is 0.095 (9.50%) for the as-run exploratory
  arm (`c1` `test.exploratory_band.over_refusal`) and 0.110 (11.00%) for the spec-corrected arm
  (`c1_corrected`). The earlier PROGRESS note repeated the same error; the inventory now forbids any cap
  claim for C21/C22 because over-refusal keys are outside this pack's claim set. Batch 2 must catch this
  independently.
- Still open at the time of writing: nothing else found by the lead's read of the two student files except
  that neither document points the student at `07_student/SOURCE-MAP.md` (the viva points at the internal
  inventory instead).

## Batch 2 — three independent reviewers (run, blocking, exactly 3 tasks)

- `reports/review-numbers.md` — 139 numerals in the two student documents + 32 map rows + ~90 cited line
  numbers checked against `json.load` output. Verdict MISMATCHES FOUND, 2 defects: (1) VIVA-QA.md:24
  attributes a cap breach to the 84.71% arm (stored over-refusal 0.095 held-out, 0.100 dev exactly at the
  cap, `feasible: true`; the 11.00% breach belongs to the 12.53% arm in `c1_corrected`); (2) SOURCE-MAP.md
  line 51 cites `per_rung` at line 561, actual 556. Everything else it marked RIGHT, including the κ set,
  all three AUROC intervals, the paired difference (it re-derived 0.9823630831643002 − 0.8738488843813388 =
  the stored 0.1085), C13's 400+1,479=1,879, C17 655+145=800 and C18's 342+313/58+87 cross-sum.
- `reports/review-limits.md` — 7 PASS, 1 PARTIAL, 2 FAIL. FAILs: the same cap sentence (independently
  reproduced, so the defect is confirmed by two reviewers and by the lead), and readability (undefined
  "operating point", "band", "dev", "discordant pairs", "threshold"; Q3 ~138 words, ~65 s aloud). PARTIAL:
  viva answers 4, 5, 6 and 9 do not restate the post-hoc label before Q11.
- `reports/review-complete.md` — 7 of 8 checks pass; all 31 inventory IDs resolve (digest cites 28, viva
  29, union = inventory, none missing from the map); scope clean — no writes by this lane outside
  `07_student/` and this lane folder. Gaps: 9, including (a) SOURCE-MAP.md uses the ID `C13b`, which is a
  labelled split of C13 but not an inventory ID, and (b) numerals with no ID tag at ROUND3-DIGEST.md:71,
  ROUND3-DIGEST.md:23 and VIVA-QA.md:19.

Lead cross-check of the reviewers: the cap sentence is confirmed false by direct read of
`test.exploratory_band.over_refusal` in both `results_full.json` files (0.095 vs 0.110) plus
`exploratory.operating_point.band.dev_over_refusal` = 0.1; the SOURCE-MAP line-561 error is confirmed by
reading line 556 of `c1/results_full.json`. All three reports exist and were opened.

## State at budget exhaustion — corrections NOT applied

The two reviewers' defects and the lead's own are all still open in the student files, because the run-time
budget ended before a correction batch (three writers/editors) and the required independent re-review could
run. Nothing was committed; no frozen result, preregistration, draft, or res-s4 path was touched.

Working-tree note (scope honesty): `git status` shows ` M 04_experiments/RESULTS-INDEX.json` and
` M 06_review/audits/numbers-audit.md`. Both were already modified when this lane started (they appear in
the session-start status and in the first `git status` this run took, before any write), and no command in
this lane wrote them — they belong to the res-s4 / R3-4f work. This lane's only writes are the three files
under `07_student/` and the seven files under `sessions/R3-6b-student-pack/` (3 writer reports, 3 reviewer
reports, PROGRESS.md + this inventory).

## Batch 3 — three parallel correction editors (run, blocking, exactly 3 tasks)

Each editor owned one file; no editor touched another's file.

| Task | File | Report | Result |
|---|---|---|---|
| viva editor | `07_student/VIVA-QA.md` | `reports/fix-viva.md` | false cap clause deleted, 84.71% arm replaced by a D1-exploratory limit; 81/81 numerals tagged; post-hoc status restated in Q4/Q5/Q6/Q9; jargon gloss added; Q3 138→115 words; pointer moved to SOURCE-MAP.md |
| digest editor | `07_student/ROUND3-DIGEST.md` | `reports/fix-digest.md` | MF-14 paragraph and κ sentence retagged (C20/C21/C22/C10/C11/C23, C01); SOURCE-MAP pointer added; threshold/operating-point/band/dev/discordant-pair glosses added; the inherited "dev over-refusal 0.755" mislabel removed; 1,146→1,289 words |
| source-map editor | `07_student/SOURCE-MAP.md` | `reports/fix-source-map.md` | `per_rung` hop 561→556; C03 cross-check parenthetical sharpened (block at 81, `contingency` key at 87); C13b split note added; 112 line numbers re-verified, all values re-loaded with `json.load`, 0 value mismatches |

Lead spot-checks run directly on the corrected files (`grep`, `wc -w`, `grep -c`):
- `over-refus` / `declared cap` → **no match** in either student document (the blocking defect is gone).
- `561` → 0 occurrences in SOURCE-MAP.md; `C13b` → 4 occurrences in SOURCE-MAP.md, 1 row in CLAIM-INVENTORY.md.
- SOURCE-MAP pointer → present once in each of ROUND3-DIGEST.md and VIVA-QA.md.
- Word counts: digest 1,289 (≤ 1,300 ceiling), viva 1,346, map 3,215.

## Batch 4 — independent re-review of the corrected files: NOT RUN

The task card requires an independent re-review after corrections. The edited text is new text: the digest
gained ~143 words and the viva was re-tagged throughout, so the batch-2 reviewer verdicts (139 numerals
checked) no longer cover the current bytes. A lead-side `grep` proves the specific blocking defect is gone
but is not a numeral-by-numeral audit, and the run-time budget ended before batch 4 could run.

## Batch 4 — independent re-review of the corrected files (run, blocking, exactly 3 tasks)

- Numbers re-reviewer: **ALL NUMBERS VERIFIED** — 140 numerals in the current digest + viva, 115 map line
  numbers resolved, 0 mismatches; it re-checked κ 0.2802, the derived 0.43 (both derivations), the per-rung
  κ set, all three AUROC intervals, the paired difference, 1,879/400/1,479/18/10,000/20261118, 0.9762, the
  gold-indicator 1.0s, 655/145/800, 342/58/313/87, 0.7327, and 100.00/84.71/12.53 with their run labels.
  Its report landed at `sessions/R3-6b-student-pack/NUMBER-REREVIEW-2.md` (lane root, not `reports/`) —
  a path deviation, content intact.
- Limits re-reviewer: **DEFECTS FOUND (3)**, 9 other checks PASS. Open: (a) `VIVA-QA.md:38-39` still asserts
  "the refused share was **0.755**", which is the band arm's held-out over-refusal, not the dev statistic it
  sits beside, so the sentence is both an over-refusal claim and self-contradictory; (b) `VIVA-QA.md:50`
  quotes per-rung κ as "ran from **0.0** to **0.2991** (C08)" without the n = 25 that the C08 label note
  requires, and a min-max range invites the ordering reading C08 forbids; (c) "AUROC" is used at
  `VIVA-QA.md:29` and in Q6 before it is defined at :75, and "abstain precision" is never defined in the
  viva. Max answer length 137 words (Q12 bullets), others 47-98, so length is not a defect.
- Completeness re-reviewer: **PACK COMPLETE**, 8/8 checks, 0 gaps — all cited IDs resolve to a map row, the
  reverse check is clean (C13b now valid), every numeral carries an ID tag, the eight required framings are
  present, the batch-3 fixes are all confirmed on disk, and scope is clean.

Lead verification of the three open items (own greps, quoted above): the digest is clean — no `0.755`, no
`over-refus`, no `refused share`; `0.755` and "the refused share was" occur only at `VIVA-QA.md:38-39`;
`0.0 to 0.2991` only at `VIVA-QA.md:50`; the first `AUROC` occurrence is `VIVA-QA.md:29` with the
definition only at :75.

INCOMPLETE: three defects remain open in 07_student/VIVA-QA.md only, all confirmed by the lead on disk — (1) lines 38-39 still say "92.9% of dev items fell below the low threshold, the refused share was 0.755", mixing a dev figure with the band arm's held-out over-refusal and keeping the one over-refusal claim this pack is not allowed to make; (2) line 50 quotes per-rung kappa as "ran from 0.0 to 0.2991 (C08)" without the required n = 25 and implies an ordering the source forbids; (3) AUROC is used at line 29 and in Q6 before its definition at line 75, and "abstain precision" is never defined. A correction edit of VIVA-QA.md plus one independent confirmation of those three lines is the remaining work; every number in both student files is otherwise independently verified (batch 4: 140 numerals, 0 mismatches) and all other limits are correct.
