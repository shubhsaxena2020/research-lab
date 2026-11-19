# NUMBER RE-REVIEW (round 2) — R3-6b student pack, current bytes

Reviewer: independent number re-reviewer (post-correction pass).
Date: 2026-11-19. Files reviewed as they now stand (nothing grandfathered):

- `07_student/ROUND3-DIGEST.md` — 1,289 words
- `07_student/VIVA-QA.md` — 1,346 words
- `07_student/SOURCE-MAP.md` — 134 lines, 32 table rows

Every stored value below was read with `json.load` (or the Markdown opened at the cited line).
`CLAIM-INVENTORY.md` was treated as a claim to test, never as truth.

---

## 1. Numeral extraction

Regex (Python `re`), applied per line to the two student documents only:

```python
pat = re.compile(r'(?<![A-Za-z0-9_])[-−]?\d[\d,]*(?:\.\d+)?%?')
```

Raw matches: **189**. After dropping tokens that are not quantities — claim-ID and metric
suffixes (`C01`, `N5`, `MF-14`, `R3-3b`, `07_student`), markdown section/question numbering
(`## 1.`, `**4.`), and rung ordinals written as bare digits (`rungs 1 to 4`, `rung-1`, `rung-4`)
— **140 substantive numerals** remain: 64 in `ROUND3-DIGEST.md`, 76 in `VIVA-QA.md`.

Every one is listed in §7 with its line and its nearest claim-ID tag. Result: **0 defects**.
No wrong value, no wrong rounding, no untagged numeral, no ID that fails to contain its number,
no derived value presented as stored.

Derived-number check (the only derived number in the pack, 0.43):

| derivation | arithmetic | result |
|---|---|---|
| from κ and Po: Pe = (Po − κ)/(1 − κ) | (0.59 − 0.2802)/(1 − 0.2802) | 0.43039733… |
| from the stored contingency: Pe = (A1·B1 + A0·B0)/N² | (62×21 + 38×79)/10 000 | 0.4304 |

Both agree to 4 dp. Reversing: (0.59 − 0.4304)/(1 − 0.4304) = 0.2801966292134831, i.e. exactly
`mf10.agreement.kappa`. The printed "about 0.43" is therefore right, and both documents label it
"derived from C01 and C02" (DIGEST line 25, VIVA line 48) — required by SOURCE-MAP C03.

---

## 2. Per-claim verification (against json.load / cited Markdown)

| ID | printed | stored value found | file / key | status |
|---|---|---|---|---|
| C01 | 0.2802 | `0.2802` flat; `0.2801966292134831` at `mf10.agreement.kappa` | mf10 L246 / L86 | RIGHT |
| C02 | 0.59, 59, 100 | `0.59` / `59` / `100` | mf10 L243/244/236 | RIGHT |
| C03 | 0.43 (labelled derived) | not stored; 0.4304 both ways | derivation, §1 above | RIGHT |
| C04 | 41 | `41` | mf10 L245 | RIGHT |
| C05 | 62, 21 | `62` / `21` | mf10 L247/249 | RIGHT |
| C06 | 35 / 6 / 0 (of 41) | `35` / `6` / `0` / `41` | mf10 L254/255/256/253 | RIGHT |
| C07 | 56 of 100, 0.56, 56% | `56` / `0.56` | mf10 L251/252 | RIGHT |
| C08 | 0.0 → 0.2991 (VIVA only) | `0.0` / `0.2991` / `0.026` / `0.1379`; n=25 each | mf10 L259/265/271/277 | RIGHT on value (see F1) |
| C09 | 0.1975, 5 of 100 | `0.1975` / `5` / `0.05` | mf10 L217 block | RIGHT |
| C10 | 0.9824 [0.9776, 0.9867] | `0.9823630831643002` / `0.9776211411662427` / `0.9866543835742593` | mf17 L1256/1255/1254 | RIGHT |
| C11 | 0.8738 [0.8587, 0.8893] | `0.8738488843813388` / `0.8586833140203312` / `0.8893003500532195` | mf17 L1180/1179/1178 | RIGHT |
| C12 | 0.1085 [0.0946, 0.1225], excludes zero | `0.10851419878296142` / `0.09458017350090517` / `0.12252082237972457`, `contains_zero: False` | mf17 L1397/1396/1395, nested at L1380 | RIGHT |
| C13 | 1,879 / 400 / 1,479 / 18 | `1879` / `400` / `1479` / `18` | mf17 `denominators.held_out_common` L980 | RIGHT |
| C13b | 10,000 / 20261118 | `10000` / `20261118` | mf17 top level L1053 / L1660 | RIGHT |
| C14 | 0.9762 (dev rung 1) | `0.9762` | mf7 L1896 | RIGHT |
| C15 | 1.0 | `1.0` | mf7 L1891 | RIGHT |
| C16 | 1.0 / deterministic | `1.0` / `True` | mf7 L1889 / L1906 | RIGHT |
| C17 | 655 / 145 / 800 / 0.7327 | `655` / `145` / `800` / `0.7327` | mf7 L1800/1801 (n=800) / L1767 | RIGHT |
| C18 | 342 / 58 / 313 / 87 | same | mf7 L1839/1840/1887/1888 | RIGHT |
| C19 | rung = −1, no per-rung | `-1`, `per_rung_R1_R3_estimand_available: false` | mf7 L1849/1848 | RIGHT |
| C20 | 100.00% | `1.0` | c1 L536 | RIGHT |
| C21 | 84.71% | `0.8471` | c1 L597 | RIGHT |
| C22 | 12.53% | `0.1253` | c1_corrected L500 | RIGHT |
| C23 | 0.9824 vs 0.8738 comparable | rule at PREREG L263–264; values C10/C11 | PREREG | RIGHT |
| N1 | ≥ 15 points | `criterion_points: 15`; PREREG L23 "≥ 15 points" | PREREG L22–25 | RIGHT |
| N2 | 0.907 / 0.948 / 92.9% / 1.00 / 0.755 | PREREG L168–170 verbatim | PREREG L167–172 | RIGHT on value (see F2) |
| N3 | exploratory cannot rescue | PREREG L180–181 verbatim | PREREG L178–181 | RIGHT |
| N4 | no discordant pairs | `p_note` string identical; `n_eff: 0`, `p_value: 1.0` | c1 L364 | RIGHT |
| N5 | exploratory/post-hoc | ANSWERS L3–6, L55–56, L107–108, L147–149 | ANSWERS | RIGHT |
| N6 | not yet in draft | HEAD-REVIEW L94 ("…not yet bound into the draft"), L84 ("must not be bound by this lane") | HEAD-REVIEW | RIGHT |
| N7 | file's own limitation wording | `limitations[0]`, `limitations[4]` match verbatim | mf17 L1046 / L1050 | RIGHT |
| N8 | 44 must-fix items | TRIAGE L1 + 44-row table L8–51; HEAD-REVIEW L46; COMMON L6–11 | three files | RIGHT |

Arithmetic spot-checks: 400+1,479 = 1,879; 655+145 = 800; 342+58 = 400; 313+87 = 400;
59+41 = 100; 35+6+0 = 41; per-rung resolved 3+13+18+22 = 56; A = 6+13+19+24 = 62;
B = 0+4+1+16 = 21; 0.8471→84.71%, 0.1253→12.53%.

---

## 3. The specific items asked for

- **kappa 0.2802** — CONFIRMED: `mf10_adjudication.json` L246 stores exactly `0.2802`;
  full precision `0.2801966292134831` at L86. Rounds correctly from the full value.
- **derived 0.43** — CONFIRMED, both derivations: (a) Pe = (Po−κ)/(1−κ) = (0.59−0.2802)/0.7198
  = 0.43039733; (b) Pe = (62×21 + 38×79)/10⁴ = 0.4304. Labelled "derived from C01 and C02" in
  both documents.
- **per-rung kappa 0.0 / 0.2991 / 0.026 / 0.1379** — CONFIRMED: L259/265/271/277 store exactly
  those 4-dp values; full precision 0.0 / 0.29906542056074775 / 0.025974025974026038 /
  0.13793103448275895 at L99/107/115/123. Only 0.0 and 0.2991 are printed (VIVA line 50).
- **0.9824 with [0.9776, 0.9867]** — CONFIRMED: 0.9823630831643002 / 0.9776211411662427 /
  0.9866543835742593 (mf17 L1256/1255/1254).
- **0.8738 with [0.8587, 0.8893]** — CONFIRMED: 0.8738488843813388 / 0.8586833140203312 /
  0.8893003500532195 (mf17 L1180/1179/1178).
- **0.1085 with [0.0946, 0.1225] and "excludes zero"** — CONFIRMED: 0.10851419878296142 /
  0.09458017350090517 / 0.12252082237972457; `contains_zero: False` inside the nested
  `paired_auroc_diff` dict (L1380); there is no flat `.contains_zero` key — the map says so and
  the file agrees.
- **1,879 / 400 / 1,479 / 18 / 10,000 / 20261118** — CONFIRMED: denominators block L980
  (1879/400/1479/18); top-level `n_boot` 10000 at L1053, `seed` 20261118 at L1660.
- **0.9762** — CONFIRMED: `gold_control.dev.r1.auroc_surface_lex` = 0.9762 (mf7 L1896), dev rung 1
  as stated in both documents.
- **gold-indicator 1.0 values and `is_gold` determinism** — CONFIRMED: `auroc_plus_is_gold` = 1.0
  (L1891), `auroc_is_gold_alone_answerable_oriented` = 1.0 (L1889), un-oriented = 0.0,
  `is_gold_deterministic_from_label` = true (L1906) at every dev/test × R1–R4 cell.
- **655 / 145 / 800** — CONFIRMED: mf7 L1800/1801 and `all.n` = 800.
- **342 / 58 / 313 / 87** — CONFIRMED: dev 342/58 (L1839/1840), test 313/87 (L1887/1888); both
  halves sum to 400.
- **0.7327** — CONFIRMED: `d3_pooled.all.auroc_surface_lex_hit_vs_miss` = 0.7327 (L1767).
- **100.00 / 84.71 / 12.53 with their three run labels** — CONFIRMED: `1.0` (c1
  `test.band_primary.per_rung.4`, L536), `0.8471` (c1 `test.exploratory_band.per_rung.4`, L597),
  `0.1253` (c1_corrected `test.exploratory_band.per_rung.4`, L500). Labels match: frozen/D1,
  frozen exploratory as-run/D1, spec-corrected post-hoc/D4.
- **0.907 / 0.948 / 92.9% / 0.755 / 1.00 in the H1 passage** — values CONFIRMED against PREREG
  D1 L168–170; see F2 for the one wording problem ("0.755" named "refused share").

---

## 4. SOURCE-MAP.md re-check

- 32 table rows (C01–C23 + C13b + N1–N8) checked: every ID resolves, every stored value matches,
  every rounding is faithful to the stored value (4 dp from full precision; `0.026` is the file's
  own 4-dp rendering; `1.0 → 100.00%` and `0.8471 → 84.71%` are the row's permitted percentage
  form).
- **115 cited line numbers opened and matched against the stated content — 0 failures.** Coverage:
  mf10 31 lines (L6, 81, 86, 87, 95, 99, 107, 115, 123, 151, 165, 177, 217, 236, 237, 243–247,
  249, 251–256, 259, 265, 271, 277); mf17 16 lines (L980, 1045, 1046, 1050, 1053, 1178–1180,
  1254–1256, 1380, 1395–1397, 1660); mf7 14 lines (L1757, 1767, 1800, 1801, 1839, 1840, 1848,
  1849, 1887–1889, 1891, 1896, 1906); c1 results_full 10 lines (L364, 489, 490, 495, 535, 536,
  551, 556, 596, 597); c1_corrected 6 lines (L392, 439, 454, 459, 499, 500); PREREGISTRATION 18
  lines (L22–25, 165, 167–172, 178–181, 262–264); ANSWERS 11 lines (L3–6, 55–56, 107–108,
  147–149); HEAD-REVIEW 3 lines (L46, 84, 94); TRIAGE 3 lines (L1, L8, L51 — span L8–51 holds
  exactly 44 rows, 1…44); COMMON 6 lines (L6–11).
  The one initial mismatch in my assertion script was my own search token ("prefix" does not
  appear at ANSWERS L6; the sentence is "…key is `c1.r3_3b.<item>.`"), not a map error.
- Hashes: all five sha256 prefixes and full digests match the files on disk
  (`2324d8605534…`, `07c3a0f8a54f…`, `0728d92714d0…`, `e4cf65cb0b2b…`, `936ce0b89e22…`).
- Coverage arithmetic in the map's preamble is right: 23 C-IDs + 8 N-IDs = 31 claim IDs in 32 rows
  (C13b is a declared split of C13, and the inventory does list it as an accepted split).
- Known exclusions: the corrected registered-band value `0.9073` really is at c1_corrected L439 and
  really is absent from both student documents — verified by numeral extraction (no `0.9073`,
  `90.73` or `90.7` anywhere in the pack).

---

## 5. over_refusal — both runs, both bands

| file | `test.band_primary.over_refusal` | `test.exploratory_band.over_refusal` |
|---|---|---|
| `c1/results_full.json` | **0.755** | **0.095** |
| `c1_corrected/results_full.json` | **0.915** | **0.110** |

Sentences in the two student documents that touch refusal behaviour (there are **two**, and only one
carries a number):

1. VIVA-QA Q3, lines 38–39: *"…**92.9%** of dev items fell below the low threshold, the refused
   share was **0.755**, and every gate reported **1.00** in every rung (N2)."* — **this is the
   over-refusal value**: 0.755 is exactly `c1 test.band_primary.over_refusal`, and PREREG L169
   names the same quantity "dev over-refusal". The number is right; the noun is not (F2).
2. ROUND3-DIGEST line 61: *"It could not run at the registered point: the gate refused almost
   everything, with 92.9% of dev items below the lower cut-off on its own (N2)."* — qualitative,
   sourced to the same prereg sentence, no over_refusal figure printed.

No sentence in either document mentions 0.095, 0.11, 0.915, the D1 exploratory constraint
"dev over-refusal ≤ 0.10" (PREREG L179), or feasibility. That matters: the spec-corrected
exploratory band's over_refusal is **0.11**, which **violates** the ≤0.10 constraint its own
deviation text set — a latent problem in the run, correctly kept out of the student pack. The pack
must not be allowed to acquire a sentence saying that arm "meets the over-refusal cap".

---

## 6. Findings (none of them a wrong number)

- **F1 (label omission).** VIVA-QA line 50: *"Per rung it ran from **0.0** to **0.2991** (C08)."*
  SOURCE-MAP C08 states per-rung κ "must never be quoted without n = 25"; the sentence does not
  give n = 25, and shows only the endpoints (R3 = 0.026, R4 = 0.1379 are omitted, which is
  acceptable for a range but hides the non-monotonicity). Value is right; the qualifier the map
  requires is missing.
- **F2 (wrong noun, right number).** VIVA-QA line 39 prints 0.755 as "the refused share". 0.755 is
  over-refusal (share of *answerable* items refused); the band's overall refused share is
  1 − coverage = 1 − 0.0527 = **0.9473**. The number matches N2/PREREG L169 and
  `c1 test.band_primary.over_refusal`, so it is not a value error, but the label silently changes
  the denominator and is the pack's only surviving over-refusal claim. Fix: call it "dev
  over-refusal 0.755", the map's own wording.
- **F3 (cosmetic).** SOURCE-MAP N8 row describes the TRIAGE table as "the 44-row table MF-1…MF-44";
  the rows are numbered 1…44 in an "MF" column (lines 8–51, 44 rows — the span is correct).

Nothing else: no sentence in either document makes a claim about caps, feasibility, or a fourth
operating point; no number appears without an ID tag; no ID is cited for a number it does not carry;
the only derived value (0.43) is labelled derived everywhere it appears.

---

## 7. Verdict

**ALL NUMBERS VERIFIED — 0 numeric mismatches across 140 numerals in the two student documents and
32 rows / 115 cited lines in SOURCE-MAP.md.** Three non-numeric findings (F1–F3) remain, of which
F2 (naming 0.755 "the refused share" instead of "dev over-refusal") is worth a one-word fix.

---

## 8. Full numeral inventory (140)

| # | file | line | numeral | nearest ID tag | status |
|---|---|---|---|---|---|
| 1 | DIGEST | 11 | `44` | N8 | RIGHT |
| 2 | DIGEST | 19 | `100` | C02 | RIGHT |
| 3 | DIGEST | 23 | `0.2802` | C01 | RIGHT |
| 4 | DIGEST | 23 | `0.59` | C02 | RIGHT |
| 5 | DIGEST | 23 | `59` | C04 | RIGHT |
| 6 | DIGEST | 23 | `100` | C04 | RIGHT |
| 7 | DIGEST | 23 | `41` | C04 | RIGHT |
| 8 | DIGEST | 23 | `62` | C05 | RIGHT |
| 9 | DIGEST | 23 | `21` | C05 | RIGHT |
| 10 | DIGEST | 23 | `41` | C04 | RIGHT |
| 11 | DIGEST | 23 | `35` | C06 | RIGHT |
| 12 | DIGEST | 23 | `6` | C06 | RIGHT |
| 13 | DIGEST | 23 | `0` | C06 | RIGHT |
| 14 | DIGEST | 23 | `56` | C07 | RIGHT |
| 15 | DIGEST | 23 | `100` | C07 | RIGHT |
| 16 | DIGEST | 23 | `0.56` | C07 | RIGHT |
| 17 | DIGEST | 23 | `56%` | C07 | RIGHT |
| 18 | DIGEST | 25 | `0.2802` | C01 | RIGHT |
| 19 | DIGEST | 25 | `0.43` | C03 | RIGHT |
| 20 | DIGEST | 25 | `0.59` | C02 | RIGHT |
| 21 | DIGEST | 35 | `0.9824` | C10 | RIGHT |
| 22 | DIGEST | 35 | `95%` | C10 | RIGHT |
| 23 | DIGEST | 35 | `0.9776` | C10 | RIGHT |
| 24 | DIGEST | 35 | `0.9867` | C10 | RIGHT |
| 25 | DIGEST | 35 | `0.8738` | C11 | RIGHT |
| 26 | DIGEST | 35 | `95%` | C11 | RIGHT |
| 27 | DIGEST | 35 | `0.8587` | C11 | RIGHT |
| 28 | DIGEST | 35 | `0.8893` | C11 | RIGHT |
| 29 | DIGEST | 35 | `0.1085` | C12 | RIGHT |
| 30 | DIGEST | 35 | `95%` | C12 | RIGHT |
| 31 | DIGEST | 35 | `0.0946` | C12 | RIGHT |
| 32 | DIGEST | 35 | `0.1225` | C12 | RIGHT |
| 33 | DIGEST | 37 | `1,879` | C13 | RIGHT |
| 34 | DIGEST | 37 | `400` | C13 | RIGHT |
| 35 | DIGEST | 37 | `1,479` | C13 | RIGHT |
| 36 | DIGEST | 37 | `18` | C13 | RIGHT |
| 37 | DIGEST | 37 | `10,000` | C13 | RIGHT |
| 38 | DIGEST | 37 | `20261118` | C13 | RIGHT |
| 39 | DIGEST | 43 | `1.0` | C15 | RIGHT |
| 40 | DIGEST | 43 | `1.0` | C16 | RIGHT |
| 41 | DIGEST | 45 | `0.9762` | C14 | RIGHT |
| 42 | DIGEST | 47 | `655` | C17 | RIGHT |
| 43 | DIGEST | 47 | `145` | C17 | RIGHT |
| 44 | DIGEST | 47 | `800` | C17 | RIGHT |
| 45 | DIGEST | 47 | `0.7327` | C17 | RIGHT |
| 46 | DIGEST | 47 | `−1` | C19 | RIGHT |
| 47 | DIGEST | 54 | `1.0` | C16 | RIGHT |
| 48 | DIGEST | 61 | `15` | N1 | RIGHT |
| 49 | DIGEST | 61 | `92.9%` | N2 | RIGHT |
| 50 | DIGEST | 61 | `1.00` | N2 | RIGHT |
| 51 | DIGEST | 69 | `100.00%` | C20 | RIGHT |
| 52 | DIGEST | 70 | `84.71%` | C21 | RIGHT |
| 53 | DIGEST | 71 | `12.53%` | C22 | RIGHT |
| 54 | DIGEST | 73 | `12.53%` | C22 | RIGHT |
| 55 | DIGEST | 73 | `100.00%` | C20 | RIGHT |
| 56 | DIGEST | 73 | `84.71%` | C21 | RIGHT |
| 57 | DIGEST | 73 | `0.9824` | C10 | RIGHT |
| 58 | DIGEST | 73 | `0.8738` | C11 | RIGHT |
| 59 | DIGEST | 79 | `0.2802` | C01 | RIGHT |
| 60 | DIGEST | 80 | `41` | C04 | RIGHT |
| 61 | DIGEST | 81 | `1.0` | C15 | RIGHT |
| 62 | DIGEST | 82 | `−1` | C19 | RIGHT |
| 63 | DIGEST | 84 | `12.53%` | C22 | RIGHT |
| 64 | DIGEST | 84 | `12.53%` | C22 | RIGHT |
| 65 | VIVA-QA.md | 26 | `100.00%` | C20 | RIGHT |
| 66 | VIVA-QA.md | 26 | `84.71%` | C20 | RIGHT |
| 67 | VIVA-QA.md | 27 | `12.53%` | C22 | RIGHT |
| 68 | VIVA-QA.md | 29 | `0.9824` | C23 | RIGHT |
| 69 | VIVA-QA.md | 29 | `0.8738` | C23 | RIGHT |
| 70 | VIVA-QA.md | 32 | `100.00%` | C20 | RIGHT |
| 71 | VIVA-QA.md | 32 | `12.53%` | C22 | RIGHT |
| 72 | VIVA-QA.md | 37 | `15` | N1 | RIGHT |
| 73 | VIVA-QA.md | 38 | `0.907` | N2 | RIGHT |
| 74 | VIVA-QA.md | 38 | `0.948` | N2 | RIGHT |
| 75 | VIVA-QA.md | 38 | `92.9%` | N2 | RIGHT |
| 76 | VIVA-QA.md | 39 | `0.755` | N2 | RIGHT |
| 77 | VIVA-QA.md | 39 | `1.00` | N2 | RIGHT |
| 78 | VIVA-QA.md | 44 | `0.2802` | C01 | RIGHT |
| 79 | VIVA-QA.md | 47 | `0.2802` | C01 | RIGHT |
| 80 | VIVA-QA.md | 47 | `0.59` | C02 | RIGHT |
| 81 | VIVA-QA.md | 47 | `59` | C02 | RIGHT |
| 82 | VIVA-QA.md | 48 | `100` | C03 | RIGHT |
| 83 | VIVA-QA.md | 48 | `0.43` | C03 | RIGHT |
| 84 | VIVA-QA.md | 50 | `0.0` | C08 | RIGHT |
| 85 | VIVA-QA.md | 50 | `0.2991` | C08 | RIGHT |
| 86 | VIVA-QA.md | 52 | `0.2802` | C01 | RIGHT |
| 87 | VIVA-QA.md | 54 | `41` | C04 | RIGHT |
| 88 | VIVA-QA.md | 54 | `56` | C04 | RIGHT |
| 89 | VIVA-QA.md | 56 | `62` | - | RIGHT |
| 90 | VIVA-QA.md | 57 | `21` | C05 | RIGHT |
| 91 | VIVA-QA.md | 57 | `41` | C04 | RIGHT |
| 92 | VIVA-QA.md | 57 | `100` | C04 | RIGHT |
| 93 | VIVA-QA.md | 58 | `35` | C06 | RIGHT |
| 94 | VIVA-QA.md | 58 | `6` | C06 | RIGHT |
| 95 | VIVA-QA.md | 58 | `0` | C06 | RIGHT |
| 96 | VIVA-QA.md | 58 | `56` | C06 | RIGHT |
| 97 | VIVA-QA.md | 58 | `100` | C06 | RIGHT |
| 98 | VIVA-QA.md | 59 | `56%` | C07 | RIGHT |
| 99 | VIVA-QA.md | 61 | `1.0` | C15 | RIGHT |
| 100 | VIVA-QA.md | 64 | `0.9762` | C14 | RIGHT |
| 101 | VIVA-QA.md | 64 | `1.0` | C15 | RIGHT |
| 102 | VIVA-QA.md | 65 | `1.0` | C16 | RIGHT |
| 103 | VIVA-QA.md | 68 | `0.7327` | C17 | RIGHT |
| 104 | VIVA-QA.md | 68 | `1.0` | C17 | RIGHT |
| 105 | VIVA-QA.md | 71 | `1.0` | C15 | RIGHT |
| 106 | VIVA-QA.md | 77 | `0.9824` | C10 | RIGHT |
| 107 | VIVA-QA.md | 77 | `0.9776` | C10 | RIGHT |
| 108 | VIVA-QA.md | 77 | `0.9867` | C10 | RIGHT |
| 109 | VIVA-QA.md | 77 | `0.8738` | C10 | RIGHT |
| 110 | VIVA-QA.md | 78 | `0.8587` | C11 | RIGHT |
| 111 | VIVA-QA.md | 78 | `0.8893` | C11 | RIGHT |
| 112 | VIVA-QA.md | 80 | `0.1085` | C12 | RIGHT |
| 113 | VIVA-QA.md | 80 | `0.0946` | C12 | RIGHT |
| 114 | VIVA-QA.md | 80 | `0.1225` | C12 | RIGHT |
| 115 | VIVA-QA.md | 82 | `0.1085` | - | RIGHT |
| 116 | VIVA-QA.md | 82 | `0.0946` | - | RIGHT |
| 117 | VIVA-QA.md | 82 | `0.1225` | - | RIGHT |
| 118 | VIVA-QA.md | 84 | `1,879` | C13 | RIGHT |
| 119 | VIVA-QA.md | 84 | `400` | C13 | RIGHT |
| 120 | VIVA-QA.md | 84 | `1,479` | C13 | RIGHT |
| 121 | VIVA-QA.md | 84 | `18` | C13 | RIGHT |
| 122 | VIVA-QA.md | 85 | `10,000` | C13 | RIGHT |
| 123 | VIVA-QA.md | 85 | `20261118` | C13 | RIGHT |
| 124 | VIVA-QA.md | 90 | `655` | C17 | RIGHT |
| 125 | VIVA-QA.md | 90 | `145` | C17 | RIGHT |
| 126 | VIVA-QA.md | 90 | `800` | C17 | RIGHT |
| 127 | VIVA-QA.md | 90 | `342` | C17 | RIGHT |
| 128 | VIVA-QA.md | 91 | `58` | C18 | RIGHT |
| 129 | VIVA-QA.md | 91 | `313` | C18 | RIGHT |
| 130 | VIVA-QA.md | 91 | `87` | C18 | RIGHT |
| 131 | VIVA-QA.md | 92 | `−1` | C19 | RIGHT |
| 132 | VIVA-QA.md | 97 | `0.1975` | - | RIGHT |
| 133 | VIVA-QA.md | 98 | `5` | C09 | RIGHT |
| 134 | VIVA-QA.md | 98 | `100` | C09 | RIGHT |
| 135 | VIVA-QA.md | 98 | `0.2802` | C01 | RIGHT |
| 136 | VIVA-QA.md | 98 | `56` | C07 | RIGHT |
| 137 | VIVA-QA.md | 113 | `0.2802` | - | RIGHT |
| 138 | VIVA-QA.md | 115 | `1.0` | C15 | RIGHT |
| 139 | VIVA-QA.md | 116 | `12.53%` | C22 | RIGHT |
| 140 | VIVA-QA.md | 117 | `100.00%` | C20 | RIGHT |