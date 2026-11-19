# Writer report — 07_student/ROUND3-DIGEST.md (R3-6b student pack, batch 1)

Lane: R3-6b-student-pack. Writer: digest writer (res-s1). Date: 2026-11-19.

Write path: `07_student/ROUND3-DIGEST.md` (overwritten completely).
Report path: `sessions/R3-6b-student-pack/reports/writer-digest.md` (this file).
No other file was created or modified. No git state change, no network, no write outside these two paths.

This report supersedes the earlier `writer-digest.md` in this lane, which used a `MAP-*` numbering that
is not the canonical inventory and cited no verifiable source for the MF-14 triple. That scheme is gone:
the digest now cites only `C01..C23` and `N1..N8` from `CLAIM-INVENTORY.md`.

## Sources read, in the mandated order

1. `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` — canonical claim table; the only source of numbers.
2. `sessions/R3-6b-student-pack/TASK.md` — deliverable 1 spec.
3. `04_experiments/results/c1/r3/R3-3b/ANSWERS.md` — plain statements of the three post-hoc analyses.
4. `orchestration/HEAD-REVIEW.md` checkpoints 9, 10, 11 only.
5. `sessions/R3/COMMON.md`; `sessions/R3/TRIAGE.md` header.
6. My own re-read of the JSON files, to confirm five values rather than trust the table.

## Independent value check (my command, my output)

```
$ python -c "import json; d=json.load(open('04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json',encoding='utf-8')); \
    print(d['results']['c1.r3_3b.mf10.cohen_kappa_overall'], d['results']['c1.r3_3b.mf10.raw_agreement_po'], \
          d['results']['c1.r3_3b.mf10.n_items'])"
0.2802 0.59 100

$ python -c "... mf17_auroc_intervals.json ..."
frozen point    0.9823630831643002
corrected point 0.8738488843813388
paired diff     0.10851419878296142

$ python -c "... mf7_gold_control.json ..."
c1.r3_3b.mf7.gold_control.dev.r1.auroc_surface_lex = 0.9762
c1.r3_3b.mf7.gold_control.dev.r1.auroc_plus_is_gold = 1.0
c1.r3_3b.mf7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented = 1.0
c1.r3_3b.mf7.gold_control.dev.r1.is_gold_deterministic_from_label = True
c1.r3_3b.mf7.d3_pooled.all.n_hit = 655
c1.r3_3b.mf7.d3_pooled.all.n_miss = 145
c1.r3_3b.mf7.d3_pooled.all.auroc_surface_lex_hit_vs_miss = 0.7327
c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available = False
c1.r3_3b.mf7.d3_pooled.rungs_present_value = -1

$ python -c "... results_full.json (C1) and results_full.json (C1C) ..."
C20 1.0      C21 0.8471      C22 0.1253
```

One key-shape note for whoever re-runs these: MF-7's `results` keys are **flat dotted strings**, e.g.
`results['c1.r3_3b.mf7.d3_pooled.all.n_hit']`; `results['c1.r3_3b.mf7.d3_pooled']` raises `KeyError`.
MF-17's keys are **nested objects** (`['...frozen_heldout_auroc']['point']`). The inventory's `key`
column is correct in both cases — this note is only about re-typing them.

## PROOF CHECK (a) — word count

```
$ python -c "t=open('07_student/ROUND3-DIGEST.md',encoding='utf-8').read(); print(len(t.split()))"
1146
$ wc -w 07_student/ROUND3-DIGEST.md
1146 07_student/ROUND3-DIGEST.md
```

1146 words — inside the 900–1150 band the structure spec asks for, well under the 1300 hard ceiling.

## PROOF CHECK (b) — every numeral in the file, its ID, and the inventory value copied

Every numeral that appears in `07_student/ROUND3-DIGEST.md` is a row below. "As written" quotes the file.

| # | Numeral as written | Cited ID | Inventory value copied | Location |
|---|---|---|---|---|
| 1 | 0.2802 | C01 | 0.2802 | §1 result, §1 how-to-read, don't-say table |
| 2 | 0.59 | C02 | 0.59 | §1 result, §1 how-to-read |
| 3 | 59 | C02 | 59 | §1 result ("59 of the 100 items") |
| 4 | 100 | C02 | 100 | §1 question, §1 result (×2) |
| 5 | 41 | C04 | 41 | §1 result (×2), don't-say table |
| 6 | 62 | C05 | 62 | §1 result |
| 7 | 21 | C05 | 21 | §1 result |
| 8 | 35 | C06 | 35 | §1 result |
| 9 | 6 | C06 | 6 | §1 result |
| 10 | 0 ("0 ambiguous") | C06 | 0 | §1 result |
| 11 | 56 | C07 | 56 | §1 result |
| 12 | 0.56 | C07 | 0.56 | §1 result |
| 13 | 56% | C07 | 0.56 (= 56%) | §1 result |
| 14 | 0.43 | C03 — **derived from C01 and C02** | 0.4304 | §1 how-to-read, explicitly labelled derived |
| 15 | 95% (×3) | C10, C11, C12 | "95% CI" in each claim | §2 result |
| 16 | 0.9824 | C10 | 0.9823630831643002 | §2 result, MF-14 close, don't-say table |
| 17 | 0.9776 | C10 | 0.9776211411662427 | §2 result |
| 18 | 0.9867 | C10 | 0.9866543835742593 | §2 result |
| 19 | 0.8738 | C11 | 0.8738488843813388 | §2 result, MF-14 close |
| 20 | 0.8587 | C11 | 0.8586833140203312 | §2 result |
| 21 | 0.8893 | C11 | 0.8893003500532195 | §2 result |
| 22 | 0.1085 | C12 | 0.10851419878296142 | §2 result |
| 23 | 0.0946 | C12 | 0.09458017350090517 | §2 result |
| 24 | 0.1225 | C12 | 0.12252082237972457 | §2 result |
| 25 | "excludes zero" | C12 | `contains_zero` = false | §2 result |
| 26 | 1,879 | C13 | 1879 | §2 what-was-counted |
| 27 | 400 | C13 | 400 | §2 what-was-counted |
| 28 | "rung 0" | C13 | 0 | §2 what-was-counted |
| 29 | 1,479 | C13 | 1479 | §2 what-was-counted |
| 30 | "rungs 1 to 4" | C13 | 1–4 | §2 what-was-counted |
| 31 | 18 | C13 | 18 | §2 what-was-counted |
| 32 | 10,000 | C13 | 10000 | §2 what-was-counted |
| 33 | 20261118 | C13 | 20261118 | §2 what-was-counted |
| 34 | 1.0 | C15 | 1.0 | §3 gold-indicator paragraph |
| 35 | 1.0 | C16 | 1.0 | §3 gold-indicator paragraph, limits bullet |
| 36 | 0.9762 | C14 | 0.9762 | §3 honest comparison |
| 37 | "dev rung 1" | C14 | dev, r1 | §3 honest comparison |
| 38 | 655 | C17 | 655 | §3 D3 |
| 39 | 145 | C17 | 145 | §3 D3 |
| 40 | 800 | C17 | 800 ("of 800") | §3 D3 |
| 41 | 0.7327 | C17 | 0.7327 | §3 D3 |
| 42 | −1 | C19 | -1 (`rungs_present_value`) | §3 D3, don't-say table |
| 43 | "R1–R3" (no per-rung estimate) | C19 | false (`per_rung_R1_R3_estimand_available`) | §3 D3 |
| 44 | 100.00% (×2) | C20 | 1.0 (= 100.00%) | MF-14 table, closing paragraph |
| 45 | 84.71% (×2) | C21 | 0.8471 (= 84.71%) | MF-14 table, closing paragraph |
| 46 | 12.53% (×4) | C22 | 0.1253 (= 12.53%) | MF-14 table, closing paragraph, don't-say table |
| 47 | "15-point drop" | N1 | "≥ 15 points" | H1 paragraph |
| 48 | 92.9% | N2 | 92.9% | H1 paragraph |
| 49 | 0.755 | N2 | 0.755 (dev over-refusal) | H1 paragraph |
| 50 | 1.00 | N2 | 1.00 ("abstain precision 1.00 in every rung") | H1 paragraph |
| 51 | 44 | N8 | 44 round-2 must-fix items | "What Round 3 is" |
| 52 | "rungs 1 to 4", "rung 1", "rung 3" | N1 | "rungs 1→4", "rung-1 minus rung-3" | H1 paragraph |
| 53 | 0.9824 / 0.8738 (C23 sentence) | C23 (values from C10, C11) | 0.9824; 0.8738 | MF-14 closing paragraph |

**53 rows. Unmapped numerals: none.** Digits that are identifier text rather than measurements are
listed separately below, deliberately excluded from the table because they are not claims:

`C01`–`C07`, `C10`–`C17`, `C19`–`C23`; `N1`–`N8`; `MF-7`, `MF-10`, `MF-14`, `MF-17`; `R1`–`R4`;
`D1`, `D4`; `Round 3`; `D3` (analysis name); section numbers `1.`, `2.`, `3.`.

Inventory rows deliberately **not** used: C08 (per-rung kappa 0.0 / 0.2991 / 0.026 / 0.1379, 25 items),
C09 (prior kappa 0.1975, 5 of 100, 0.05), C18 (D3 dev/test splits 342 / 58 / 313 / 87). None was needed
for the fixed structure, and each would have added a number the student does not need. **90.73% is
absent** — `grep -c '90.73'` returns 0.

## PROOF CHECK (c) — IDs used and exploratory labelling

```
$ grep -o 'C[0-9][0-9]' 07_student/ROUND3-DIGEST.md | sort -u
C01 C02 C03 C04 C05 C06 C07 C10 C11 C12 C13 C14 C15 C16 C17 C19 C20 C21 C22 C23

$ grep -o 'N[0-9]' 07_student/ROUND3-DIGEST.md | sort -u
N1 N2 N3 N4 N5 N6 N7 N8

$ grep -c 'exploratory' 07_student/ROUND3-DIGEST.md
5

$ grep -c 'post-hoc' 07_student/ROUND3-DIGEST.md
8

$ grep -c 'not exercisable' 07_student/ROUND3-DIGEST.md
3

$ grep -c 'MAP-' 07_student/ROUND3-DIGEST.md
0
```

## Requirement-by-requirement self-check

| Requirement | Status | Where |
|---|---|---|
| Plain English, short sentences, BCA-semester-1 audience | done | definitions block; no notation beyond `−1` |
| Define abstention gate, AUROC, rung, negative, kappa, bootstrap interval, post-hoc | done | "What Round 3 is" + first line of §1/§2/§3 + box |
| Every numeral carries an inventory ID inline | done | 53/53 above |
| Only derived number is C03, labelled derived | done | "0.43 (C03, derived from C01 and C02)" |
| Exploratory / post-hoc + not in draft, stated early | done | 3-line box |
| No frozen verdict revised | done | box, limits bullet, §1, §3 |
| Kappa = modest agreement beyond chance; not accuracy / human / truth | done | §1 how-to-read |
| Gold-indicator 1.0 tautological, cannot show gate works | done | §3 |
| Contrast with 0.9762 (C14) and pooled D3 0.7327 (C17) | done | §3 |
| D3 pooled rung = −1 only; no per-rung R1–R3 estimate | done | §3 + don't-say table |
| MF-17: AUROC defined as ranking score, threshold-free, not accuracy; n = 1,879, 10,000 resamples | done | §2 |
| H1 not exercisable; not confirmed; not refuted from exploratory ordering | done | H1 section (N1, N2, N4, N3) |
| MF-14: three numbers each with run label; thresholds not comparable, AUROC is | done | MF-14 table + closing paragraph (C23) |
| Round 3 = 44 must-fix items, one short paragraph (N8) | done | "What Round 3 is" |
| Structure order | done | title, 3-line box, Round 3, three subsections, limits, H1/MF-14, do-don't table |
| 900–1150 words | done | 1146 |

## Notes and gaps for the lead

1. **No unresolved source gaps.** All 53 numerals map to an inventory row the lead already verified;
   five were re-checked against the JSON by me.
2. **`95%` has no standalone inventory row.** It appears only inside the C10/C11/C12 claim text
   ("95% CI"). The digest cites it under those three IDs. A dedicated row would be an inventory change,
   not a digest change — flagging it rather than inventing an ID.
3. **MF-7 flat keys.** As noted above; a trap only for anyone re-typing key paths.
4. **Deliberate omission.** The digest does not name the labeller models or the resolver, because
   `ANSWERS.md` does not name them; C05 describes them only as labellers A and B, which is what the
   digest uses.

Nothing in the digest asserts human gold, a per-rung D3 estimate, an H1 confirmation or refutation, or
a third operating point.
