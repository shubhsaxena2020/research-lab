# Independent number review — R3-6b student pack

Reviewer: numbers only (arithmetic + source fidelity). Read-only; no student file was edited.
Date: 2026-11-19. Files under review: `07_student/ROUND3-DIGEST.md`, `07_student/VIVA-QA.md`,
`07_student/SOURCE-MAP.md`.

## VERDICT: MISMATCHES FOUND

Two defects. One is a real numeric/attribution error in a spoken answer (finding 1). One is a wrong
line number in the source map (finding 2). Everything else — all 139 numerals in the two student
documents and all 32 rows / ~90 cited line numbers in the map — checks out against the JSON and
Markdown as read by `json.load` and by line.

---

## Findings

### 1. WRONG — cap breach attributed to the arm that does not breach it (high severity)

- **File:** `07_student/VIVA-QA.md`, **line 24**
- **Quoted fragment:** "The 84.71% arm over-refused past its declared cap — not a clean operating point."
- **Cited ID:** none attached to the numeral (nearest preceding is `(C23)`, which is the
  AUROC-comparability rule and does **not** contain 84.71). The value belongs to C21.
- **Printed value:** "over-refused past its declared cap"
- **Stored values:**

  | quantity | key | value |
  |---|---|---|
  | frozen exploratory band, held-out over-refusal (the 84.71% / C21 arm) | `c1/results_full.json` → `test.exploratory_band.over_refusal` | **0.095** (9.50%) |
  | same arm, dev over-refusal at fit | `c1/results_full.json` → `exploratory.operating_point.band.dev_over_refusal` | **0.1** (exactly at the cap, `feasible: true`) |
  | spec-corrected exploratory band, held-out over-refusal (the 12.53% / C22 arm) | `c1_corrected/results_full.json` → `test.exploratory_band.over_refusal` | **0.11** (11.00%) |
  | declared cap | `04_experiments/PREREGISTRATION.md` §10 D1 consequence 2, line 179 | `dev over-refusal <= 0.10` |

  9.50% < 10.00%, and the dev fit sits exactly at 0.10 and is `feasible: true`. On no reading is
  the 84.71% arm past its cap. The arm that exceeds 0.10 is the **12.53% (C22)** arm at 11.00%.
  The repo already says so: `04_experiments/results/c1/r3/metrics/ANSWERS.md` lines 92–100
  ("corrected arm 11.00% over-refusal versus declared 0.10 cap … `dev_over_refusal` = 0.095,
  `held_out_over_refusal` = 0.11, `breached_on_dev` = false, `breached_on_held_out` = true"), and
  `04_experiments/results/c1_corrected/SUMMARY.md` line 19 ("Exploratory band — over-refusal
  (rung 0) | 0.0950 | 0.1100").
- **Second problem with the same clause:** `CLAIM-INVENTORY.md` line 85 states "no writer may assert
  a cap breach or cap compliance for C21/C22, because those keys are deliberately not in this
  inventory." So the clause is a forbidden claim *and* factually wrong.
- **Fix:** delete the clause (preferred — restores inventory compliance). If any cap statement is
  kept it must be moved to the C22 sentence and read "the 12.53% arm's held-out over-refusal is
  11.00%, above the declared 0.10 cap." Do not say it of the 84.71% arm.

### 2. WRONG — SOURCE-MAP line number for the C21 `per_rung` path (low severity)

- **File:** `07_student/SOURCE-MAP.md`, **line 51** (C21 row)
- **Quoted fragment:** "`"test"` (489) → `"exploratory_band"` (551) → `"per_rung"` (561) →
  `"4"` (596) → `abstain_precision` (line 597)"
- **Stated:** `"per_rung"` at line 561. **Actual:** line **556** (`      "per_rung": {`).
  Line 561 is `            "hi": 1.0,` — the upper bound of rung 1's `ci95`, not `per_rung`.
  Verified `"exploratory_band"` at 551 and `"abstain_precision": 0.8471` at 597 are correct;
  the terminal value and the fix path are right, only the intermediate hop is wrong.
- **Fix:** change "(561)" to "(556)". This is the only line number in the map that does not resolve.

---

## High-risk items — explicit right/wrong

| item | claim | stored | status |
|---|---|---|---|
| κ 0.2802 | C01 | `c1.r3_3b.mf10.cohen_kappa_overall` = 0.2802; full precision `mf10.agreement.kappa` = 0.2801966292134831 → 4 dp 0.2802 | **RIGHT** |
| derived 0.43 | C03, labelled "derived from C01 and C02" in both docs | no stored key; recomputed two ways, both **0.4304**: (0.59−0.2801966292134831)/(1−0.2801966292134831) = 0.4304000231…, and marginals (62·21 + 38·79)/10000 = 4304/10000 = 0.4304. Back-substituting Pe=0.4304 into (Po−Pe)/(1−Pe) returns **0.2801966292134831**, identical to the stored κ | **RIGHT** (derivation arithmetically correct, correctly labelled and correctly rounded per the map's "4 dp (0.4304); 2 dp (0.43) acceptable") |
| per-rung κ set 0.0 / 0.2991 / 0.026 / 0.1379 | C08 | flat keys 0.0 / 0.2991 / 0.026 / 0.1379; full precision 0.0 / 0.29906542056074775 / 0.025974025974026038 / 0.13793103448275895; `n_items_by_rung` = 25 each | **RIGHT** (all four round correctly from full precision; VIVA's "ran from 0.0 to 0.2991" is min→max of the set, correct) |
| 0.9824 / 0.9776 / 0.9867 | C10 | 0.9823630831643002 / 0.9776211411662427 / 0.9866543835742593 | **RIGHT** (4 dp faithful) |
| 0.8738 / 0.8587 / 0.8893 | C11 | 0.8738488843813388 / 0.8586833140203312 / 0.8893003500532195 | **RIGHT** |
| 0.1085 / 0.0946 / 0.1225, "excludes zero" | C12 | 0.10851419878296142 / 0.09458017350090517 / 0.12252082237972457; nested `contains_zero` = **False** | **RIGHT**; also arithmetically consistent: 0.9823630831643002 − 0.8738488843813388 = 0.1085141987829614 = stored diff. "Excludes zero" matches `contains_zero: false` (there is no flat `*.contains_zero` key — the map's warning is correct) |
| 1,879 / 400 / 1,479 / 18 / 10,000 / 20261118 | C13, C13b | `denominators.held_out_common` = {n_items 1879, n_positive_rung0 400, n_negative_rungs1to4 1479, n_article_clusters 18}; top-level `n_boot` 10000, `seed` 20261118 | **RIGHT**; 400 + 1,479 = 1,879 checks out |
| 0.9762 | C14 | `mf7.gold_control.dev.r1.auroc_surface_lex` = 0.9762 (file stores only 4 dp) | **RIGHT** |
| gold-indicator 1.0s | C15, C16 | `auroc_plus_is_gold` = 1.0; `auroc_is_gold_alone_answerable_oriented` = 1.0; `auroc_is_gold_alone_raw` = 0.0; `is_gold_deterministic_from_label` = true | **RIGHT** |
| 655 / 145 / 800 | C17 | `d3_pooled.all` n_hit 655, n_miss 145, n 800 | **RIGHT**; 655+145 = 800 |
| 342 / 58 / 313 / 87 | C18 | dev 342/58 (n 400), test 313/87 (n 400) | **RIGHT**; 342+313 = 655 and 58+87 = 145, consistent with C17 |
| 0.7327 | C17 | `d3_pooled.all.auroc_surface_lex_hit_vs_miss` = 0.7327 | **RIGHT** |
| 100.00 / 84.71 / 12.53 and their three run labels | C20 / C21 / C22 | c1 `test.band_primary.per_rung.4.abstain_precision` = 1.0; c1 `test.exploratory_band.per_rung.4` = 0.8471; c1_corrected `test.exploratory_band.per_rung.4` = 0.1253 | **RIGHT** on all three values and on all three labels (registered/frozen/D1, frozen exploratory/as-run/D1, spec-corrected exploratory/post-hoc/D4). Only the extra cap sentence on VIVA line 24 is wrong (finding 1) |
| N2: 0.907 / 0.948 / 0.939 / 92.9% / 0.755 / 1.00 | N2 | PREREG §10 D1, lines 167–172 contain every one verbatim; project's own `thresholds.band` gives t_lo 0.90722098925 → 0.907, t_hi 0.947838803928 → 0.948, single `t` 0.939398578046 → 0.939 | **RIGHT** as a quote of frozen prose. Two caveats, neither the student's fault: (i) `placement_diagnostic.dev_refused_below_lo` = 0.9295, whose 1-dp percent is 93.0, not 92.9 — PREREG truncated; (ii) "1.00 in every rung" is exact only at 2 dp: the stored registered-band sequence is [1.0, **0.9964**, 1.0, 1.0] (`hypotheses.H1.sequence`) |
| N1: 15 points | N1 | PREREG §1 H1, line 23: "the drop from rung 1 to rung 3 is ≥ 15 points" | **RIGHT** |
| over-refusal sentences | — | see finding 1; digest line 59 ("dev over-refusal 0.755", N2) is a faithful quote of PREREG line 169 | digest **RIGHT**, VIVA line 24 **WRONG** |

---

## Extraction counts (reproducible)

Method: read each student file line by line; strip markdown heading markers and leading list/question
numbering (`1. `, `**4. `); strip claim and fact IDs (`C\d\d`, `N\d`), artifact IDs (`MF-\d+`, `D\d`,
`H1..H3`, `B\d`, `S\d`), lane labels (`R3-3b`, `R3-6b`, `R3-6b-student-pack`, `R3-4x`), the project name
pattern `Round \d+`, and rung designators (`rung 0`, `rung 1 to 4`, `rung = −1`); then match
`\d[\d,]*(\.\d+)?%?`.

- **139 numerals** are values: **63** in `ROUND3-DIGEST.md`, **76** in `VIVA-QA.md`.
- Excluded by rule, not by hand: 25 further digit runs that are names or labels, not values — section
  and question numbers, "Round 3" (5 occurrences), artifact/lane strings, and rung designators
  ("rung 0", "rungs 1 to 4", "rung 1 to rung 3"). Raw digit-run count before exclusion: 164
  (that is the number to compare if the lead re-runs the same regex without the strip list).
- Every one of the 139 has a claim ID in its own sentence or in the sentence it continues; **none is
  bare**, except the repeated "84.71%" on VIVA line 24, which carries no ID of its own and sits next to
  an ID (C23) that does not contain it — folded into finding 1.
- Only **one** numeral in either file is derived rather than stored: 0.43 (C03), and it is both
  labelled "derived from C01 and C02" and computed correctly (above).
- `SOURCE-MAP.md`: **32 table rows** (C01–C23 = 23, plus the C13b split = 24, plus N1–N8 = 8), matching
  the map's own coverage claim of "23 numeric claim IDs + 8 fact IDs = 31 claim IDs, written as 32 table
  rows". All 32 rows were checked: every JSON key resolves under `json.load`, every stored value matches,
  every rounding is inside the map's own permitted rendering, and every cited line number resolves except
  the single `per_rung` hop in finding 2.

---

## Non-mismatch notes (do not need fixing in the student files, but the lead should know)

- **N-a — inventory alias keys do not exist.** `CLAIM-INVENTORY.md` rows C20–C22 assert parenthetical
  aliases `c1.band.precision.r4.run`, `c1.expl.precision.r4.run`, `c1.expl.precision.r4.corr`. Neither
  `results_full.json` contains any key matching `c1.band.precision` or `c1.expl.precision`
  (`grep -c` returns 0 for both files). The student documents do not print these aliases and
  `SOURCE-MAP.md` does not repeat them, so the pack is clean; the inventory is not.
- **N-b — "MF-1…MF-44".** `SOURCE-MAP.md` line 61 says "the 44-row table MF-1…MF-44".
  `sessions/R3/TRIAGE.md` prints bare `1`…`44` under an `MF` header column. Count is right
  (44 rows, exactly lines 8–51, ids 1–44 with none missing); only the literal "MF-" prefix is the map's
  own rendering.
- **N-c — dev vs held-out wording for 0.755.** PREREG line 169 reads "dev over-refusal is 0.755 on the
  held-out half", which is self-contradictory, and the number sits at `test.band_primary.over_refusal`
  (held-out) while also appearing in the deviation text as a dev figure. Both student documents copy
  PREREG's wording. Not a number error, but it is the same dev/held-out confusion that produced
  finding 1 — worth a one-line clarification if the pack is revised.
- **N-d — hashes.** All five sha256 values in `SOURCE-MAP.md` §3 match the bytes on disk
  (`2324d8605534…`, `07c3a0f8a54f…`, `0728d92714d0…`, `e4cf65cb0b2b…`, `936ce0b89e22…`), so the line
  numbers in the map are quoted against the same files this review read.

---

## Commands and snippets run

1. `python -c "import json; d=json.load(open('.../mf10_adjudication.json'))"` — dumped every
   `c1.r3_3b.mf10.*` flat key, plus the top-level `mf10` block (`agreement.kappa`,
   `agreement.contingency`, `per_rung`, `resolved`, `disagreement_resolution`,
   `comparison_with_prior_llm_adjudication`, `exploratory_status`).
2. Same for `mf17_auroc_intervals.json` — dumped `denominators`, `seed`, `n_boot`, all `*auroc*` and
   `*diff*` keys, and the full `limitations` list.
3. Same for `mf7_gold_control.json` — dumped all 294 `c1.r3_3b.mf7.*` keys including the whole
   `gold_control.{dev,test}.r{1..4}` grid and `d3_pooled.{all,dev,test}`.
4. Both `results_full.json` files — printed `test.{band_primary,exploratory_band}` =
   `{coverage, n_items, over_refusal, per_rung.{1..4}.abstain_precision, pooled_abstain_precision}`,
   plus `exploratory.operating_point`, `exploratory.H1_sequence`, `hresholds.*`, `hypotheses.H1`
   (incl. `sign_test`).
5. `python -c "... == 'over_refusal'"` walk over both results files to confirm whether the key is
   dev or held-out: read `04_experiments/src/run_c1.py` lines 95–203, which builds
   `blocks = {"band_primary": G.metrics_block(ref_band, test_items, s_test, ...)}` — i.e.
   `test.*.over_refusal` is computed on the **held-out** items, while the 0.10 cap is enforced during
   dev fitting (`over_cap = cfg.get("exploratory_max_over_refusal", 0.10)`, line 122).
6. Arithmetic: `(0.59-0.2801966292134831)/(1-0.2801966292134831)`, `(62*21+38*79)/10000`,
   `(0.59-0.4304)/(1-0.4304)` → 0.4304, 0.4304, 0.2801966292134831.
7. Line-number resolver script (`chk1.py`): read the exact 1-based line of all ~90 cited lines in
   `mf10_adjudication.json`, `mf17_auroc_intervals.json`, `mf7_gold_control.json`,
   both `results_full.json`, `PREREGISTRATION.md`, `HEAD-REVIEW.md`, `ANSWERS.md`, `TRIAGE.md`,
   `COMMON.md` and printed each with its content.
8. `hashlib.sha256` over the five cited files, compared against `SOURCE-MAP.md` §3.
9. Numeral extractor (`numerals2.py`) — the strip list and regex described in "Extraction counts",
   printing every retained numeral with its file and line.
10. `grep -rn "over-refusal" 04_experiments/` to find the repo's own statement of the cap breach
    (`results/c1/r3/metrics/ANSWERS.md` MF-20, `results/c1_corrected/SUMMARY.md` line 19),
    used as the corroborating source for finding 1.
11. `awk`/`python` row counts on `sessions/R3/TRIAGE.md` (44 rows, lines 8–51, ids 1–44).

Scratch scripts live outside the repo at
`C:\Users\shubh\AppData\Local\hermes\profiles\res-s1\cache\scratch\{chk1,chk2,chk3,numerals,numerals2}.py`.
Nothing under `07_student/` or any other tracked path was modified.
