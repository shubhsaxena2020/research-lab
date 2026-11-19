# Fix report — 07_student/VIVA-QA.md (R3-6b student pack)

Editor lane: viva corrections. Written 2026-11-19. Inputs read in full: `reports/review-numbers.md`,
`reports/review-limits.md`, `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md`, `07_student/SOURCE-MAP.md`,
`07_student/ROUND3-DIGEST.md` (read-only, for vocabulary consistency).
Only `07_student/VIVA-QA.md` was written (plus this report).

## What was wrong and what it now says

### 1. The blocking defect — cap breach attributed to the arm that does not breach it (fixed)

Before, `07_student/VIVA-QA.md` lines 23–25:

> … but the two AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold. The
> 84.71% arm over-refused past its declared cap — not a clean operating point.

After, lines 27–29:

> … but the two AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold. That
> middle arm is exploratory: deviation D1 added it (C21), so it is not the registered number.

The cap clause is deleted outright, not moved. No 0.095 / 0.100 / 0.11 was introduced; `grep` for
`declared cap`, `0.095`, `0.100`, `0.11`, `11.00%`, `9.50%` and `90.73` all return 0. The replacement limit
("exploratory — deviation D1 added it — not the registered number") is the C21 label note in
`CLAIM-INVENTORY.md` §D and `SOURCE-MAP.md` line 51, and needs no numeral.

### 2. Numeral → claim ID tagging (fixed)

- The bare `84.71%` in the deleted clause is gone with the clause.
- Question headings that quote a number now carry its ID too: Q4 `0.2802 (C01)`, Q5 `(C04, C07)`,
  Q6 `1.0 (C15)`, Q8 `0.1085 (C12)`.
- Tag placement tightened where an ID sat one clause away from its number: `0.59 (C02)` now tags the rate
  itself; the C13 block reads `1,879 held-out items (C13): 400 …, 1,479 …, 18 …, 10,000 …, seed 20261118
  (C13)`; the N2 threshold pair is `t_lo 0.907, t_hi 0.948 (N2)` inside the same dash-bounded clause.
- Audit: 81 numerals, 81 tagged, 0 untagged (snippet below).

### 3. Exploratory / post-hoc status restated inside the findings (fixed)

- Q4: "In this post-hoc re-check, **Cohen's kappa** compares …"
- Q5: "In the same post-hoc re-check, the labellers were lopsided …"
- Q6: "In this post-hoc control, the feature restates the label …"
- Q9: "… records hit or miss — post-hoc, not confirmatory (N5)."
No number was added by any of these four clauses.

### 4. Jargon glossed once, at the top (fixed)

New paragraph under the header, "**Words used in these answers.**", defines **threshold**, **operating
point**, **band**, **dev** / **held-out**, and **discordant pair** in one line each. Q1 now states that the
four **rungs** are R1 to R4, easy to hard.

### 5. Q3 trimmed (fixed)

138 words / ~65 s → **115 words** (~50 s). Kept: H1's criterion with the 15-point limb (N1), the degenerate
registered operating point with t_lo 0.907 / t_hi 0.948 / 92.9% / 0.755 / precision 1.00 in every rung (N2),
no discordant pairs (N4), and "neither confirmed nor refuted; an exploratory arm cannot rescue it" (N3).
Removed only the "registered test was a shape" metaphor and one redundant clause.

### 6. Header pointer (fixed)

Line 3–4 no longer points at `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md`; it points at
`07_student/SOURCE-MAP.md` as the ID-to-source lookup, and notes the IDs are stable.

### 7. Shape preserved

13 Q&A (inside 12–16), every answer short, the `*If pushed, say:*` pattern kept on Q2, Q3, Q4, Q6, all
required topics present (MF-14 with three run labels, H1 not exercisable, kappa, gold-indicator 1.0, the
refuse-list). MF-14 run labels are unchanged and word for word: "registered band, frozen run, D1",
"frozen exploratory band, as run, still D1", "spec-corrected exploratory band, post-hoc, deviation D4".
Not softened: "not human gold", "tautological", "pooled rung = −1 / −1, pooled", "not exercisable",
"not yet in the draft". No value, rounding or label was altered; no new number was introduced.

One inherited wording fix inside scope: Q3's "dev over-refusal 0.755" became "the refused share was
0.755 (N2)". The value and its N2 citation are untouched; the mislabelled half (review-limits finding 2 —
0.755 is `test.band_primary.over_refusal`, held-out) is no longer asserted either way, because a
dev/held-out claim for that number is outside this pack's claim set.

## Proof checks (verbatim output)

### (a) word count

```
$ wc -w 07_student/VIVA-QA.md
1346 07_student/VIVA-QA.md
```

### (b) numeral audit — every numeral, ID tag in the same clause

Script: `$TMPDIR/verify_final.py` (flattens the file, splits on sentence/semicolon/em-dash boundaries,
strips claim IDs, artifact IDs, run labels and rung designators, then requires a `(Cnn)`/`(Nn)`
parenthetical in the same clause).

```
=== (b) NUMERAL AUDIT ===
numerals total: 81
tagged: 81 UNTAGGED: 0
```

Distinct value tokens found, all traceable to a claim-inventory row (C01–C23, C13b, N1–N8):
`0.2802, 0.59, 59, 100, 0.43, 41, 62, 21, 35, 6, 0, 56, 56%, 0.0, 0.2991, 0.1975, 5, 0.9824, 0.9776,
0.9867, 0.8738, 0.8587, 0.8893, 0.1085, 0.0946, 0.1225, 1,879, 400, 1,479, 18, 10,000, 20261118, 0.9762,
1.0, 0.7327, 655, 145, 800, 342, 58, 313, 87, −1, 100.00%, 84.71%, 12.53%, 15, 0.907, 0.948, 92.9%,
0.755, 1.00`.

### (c) `grep -n 'over-refus'`

```
$ grep -n 'over-refus' 07_student/VIVA-QA.md
$ echo $?
1
```

No output, exit 1 (no match).

### (d) `grep -c 'exploratory\|post-hoc'`

```
$ grep -c 'exploratory\|post-hoc' 07_student/VIVA-QA.md
16
```

16 matching lines, up from the pre-fix file: the added occurrences are the label restatements in Q4, Q5,
Q6, the "post-hoc, not confirmatory" clause in Q9, and the Q2 replacement clause.

### (e) deleted line, before and after

Before (lines 23–25):

```
… but the two AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold. The
84.71% arm over-refused past its declared cap — not a clean operating point.
```

After (lines 27–29):

```
… but the two AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold. That
middle arm is exploratory: deviation D1 added it (C21), so it is not the registered number.
```

### (f) `git status --short 07_student/`

```
$ git status --short 07_student/
?? 07_student/
```

The directory is untracked in this repo (it holds only the student pack), so git reports the whole
directory rather than the file. Nothing else under `07_student/` was touched by this lane:
`ROUND3-DIGEST.md`, `SOURCE-MAP.md` were opened read-only, and no path under `05_paper/`, `06_review/` or
`04_experiments/` was written.

## Residual notes for the lead

- `SOURCE-MAP.md` line 51 still carries the review-numbers finding 2 defect (`per_rung` cited at 561,
  actual 556). That file belongs to another editor; not touched here.
- `CLAIM-INVENTORY.md` §D still forbids any cap statement for C21/C22, and the viva now makes none.
