# Fix report — ROUND3-DIGEST.md (R3-6b student pack)

Editor lane: digest only. Written 2026-11-19. Files written: `07_student/ROUND3-DIGEST.md` (edited)
and this report. No other file touched.

Inputs read: `reports/review-numbers.md`, `reports/review-limits.md`, `reports/review-complete.md`,
`07_student/ROUND3-DIGEST.md`, `07_student/SOURCE-MAP.md` (rows C10, C11, C20–C23),
`sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` (N1–N8).

## Fixes applied

1. **IDs attached to the bare numerals.**
   - L73 (MF-14 "Never print…" paragraph): `12.53% (C22)`, `100.00% (C20)`, `84.71% (C21)`, and the
     AUROC pair now reads `0.9824 (C10) and 0.8738 (C11)`, with the comparability rule `(C23)` on the
     sentence that carries it and again at the end of the clause.
   - L25 ("How to read it"): `0.2802 (C01)`; the following `0.59` is now `0.59 (C02)`.
   - MF-14 table: ID moved onto the number (`100.00% (C20)`) so the table row is self-tagging.
   - "Don't say" table: the two quoted values now carry the ID of the number they quote
     (`(C15)` on the AUROC 1.0 line, `(C22)` on the 12.53% line).
   - Rest of the file re-tagged where a sentence carried its ID only at the end of a run of numerals
     (AUROC result paragraph, "What was counted", D3 sentence at `rung = −1 (C19)`), and the
     unresolved `i.e.` was removed so `56 of the 100 … 0.56 … 56% (C07)` sits in one clause.
   - No value, rounding or rendering changed.
2. **SOURCE-MAP pointer** added as a second blockquote immediately after the "Read this first" box
   (L7), two sentences: every number carries an ID like (C01); `07_student/SOURCE-MAP.md` gives the
   file, JSON key and stored value; a number not in that table does not belong in the digest.
3. **Jargon defined** — "Four words first" renamed **"A few words first"** (L13) and extended with
   `threshold`, `operating point`, `band`, `dev` vs `held-out`, and `discordant pair`, in the compact
   register of the existing gloss. Trimmed elsewhere to hold the word budget: the `44 must-fix items`
   sentence lost a redundant clause, and the `0.755` fragment described below was dropped.
4. **Inherited mislabel removed (review-limits finding 2).** L61 no longer says "dev over-refusal
   0.755": `0.755` is `test.band_primary.over_refusal` (held-out), and PREREG §10 D1 describes it with
   self-contradictory wording. Since this pack may not assert anything about over-refusal or caps, the
   clause was deleted rather than relabelled. H1's evidence is unchanged: 92.9% of dev items below the
   lower cut-off (N2), 1.00 in every rung (N2), no discordant pairs (N4).
5. **Review-limits finding 7 applied**: "The frozen run's AUROC is 0.9824" → "The frozen run's held-out
   AUROC, recomputed post-hoc with no model retrained, is 0.9824 (C10)".
6. **Review-complete gap 6 partly addressed**: L54 now reads `(C23, C10)` so the threshold-free half is
   anchored to the comparability rule plus the measurement it applies to.

## Limits preserved (all still present)

exploratory/post-hoc (L3, L51) · not yet in the draft (N6, L4, L52) · no frozen verdict revised
(N5, L4, L52) · kappa is agreement, not accuracy, not human gold (L25, L53) · gold indicator
tautological / deterministic function of the label (L43) · D3 pooled only at rung = −1, no per-rung
estimate (L47, L82) · H1 not exercisable and neither confirmed nor refuted (L59–63, L83) · MF-14 with
all three run labels — frozen D1 / as-run D1 / post-hoc D4 (L69–71) · 90.73% still not named.

## Proof check output (verbatim)

### (a) word count

```
$ wc -w 07_student/ROUND3-DIGEST.md
1289 07_student/ROUND3-DIGEST.md
```

### (b) numeral → nearest ID tag, per clause

Script: `C:\Users\shubh\AppData\Local\hermes\profiles\res-s1\cache\scratch\digest_check3.py`
(decimal points protected from the clause splitter; labels such as `C01`, `N5`, `MF-14`, `D1`, `R1`,
`rung 0`, `rungs 1 to 4` blanked before numeral matching; nearest tag by character distance, ties to
the preceding tag).

```
(a) WORDS: 1289
(b) NUMERALS: 65 | UNTAGGED: 0 []
  line   7  07        -> C01
  line  11  44        -> N8
  line  19  100       -> C02
  line  23  0.2802    -> C01
  line  23  0.59      -> C02
  line  23  59        -> C04
  line  23  100       -> C04
  line  23  41        -> C04
  line  23  62        -> C05
  line  23  21        -> C05
  line  23  41        -> C04
  line  23  35        -> C04
  line  23  6,        -> C06
  line  23  0         -> C06
  line  23  56        -> C07
  line  23  100       -> C07
  line  23  0.56      -> C07
  line  23  56%       -> C07
  line  25  0.2802    -> C01
  line  25  0.43      -> C03
  line  25  0.59      -> C02
  line  35  0.9824    -> C10
  line  35  95%       -> C10
  line  35  0.9776    -> C10
  line  35  0.9867    -> C10
  line  35  0.8738    -> C11
  line  35  95%       -> C11
  line  35  0.8587    -> C11
  line  35  0.8893    -> C11
  line  35  0.1085    -> C12
  line  35  95%       -> C12
  line  35  0.0946    -> C12
  line  35  0.1225    -> C12
  line  37  1,879     -> C13
  line  37  400       -> C13
  line  37  1,479     -> C13
  line  37  18        -> C13
  line  37  10,000    -> C13
  line  37  20261118  -> C13
  line  43  1.0       -> C15
  line  43  1.0       -> C16
  line  45  0.9762    -> C14
  line  47  655       -> C17
  line  47  145       -> C17
  line  47  800       -> C17
  line  47  0.7327    -> C17
  line  54  1.0       -> C16
  line  61  15        -> N1
  line  61  92.9%     -> N2
  line  61  1.00      -> N2
  line  61  -1        -> N2
  line  61  -3        -> N2
  line  69  100.00%   -> C20
  line  70  84.71%    -> C21
  line  71  12.53%    -> C22
  line  73  12.53%    -> C22
  line  73  100.00%   -> C20
  line  73  84.71%    -> C21
  line  73  0.9824    -> C10
  line  73  0.8738    -> C11
  line  79  0.2802    -> C01
  line  80  41        -> C04
  line  81  1.0       -> C15
  line  84  12.53%    -> C22
  line  84  12.53%    -> C22
```

Untagged numerals: **none** (empty list). Reading notes: `line 7 "07"` is the path `07_student/` in the
new SOURCE-MAP pointer, whose clause carries (C01); `line 61 "-1"/"-3"` are the rung designators in
"rung-1 minus rung-3", matched only because the hyphen is not a space.

### (c) SOURCE-MAP references

```
$ grep -c 'SOURCE-MAP' 07_student/ROUND3-DIGEST.md
1
```

### (d) over-refusal / cap statements

```
$ grep -n 'over-refus\|cap' 07_student/ROUND3-DIGEST.md
$ echo $?
1
```

No match. (The old L59 "dev over-refusal 0.755" clause is gone; see fix 4.)

### (e) git scope

```
$ git status --short 07_student/
?? 07_student/
```

The whole directory is still untracked, as in the completeness review's evidence, so no tracked file
under `07_student/` shows as modified; the edit is inside the untracked directory and no other path was
written by this lane.

## Residual notes for the lead

- The digest does not print `0.755` at all now. It is a real stored value (`test.band_primary.
  over_refusal`) whose only permitted rendering in the pack (N2) is PREREG's own "dev over-refusal"
  wording, which is the mislabel the language review flagged; the inventory also bars cap/over-refusal
  assertions. Deleting it costs no argument: H1's saturation is carried by 92.9% (N2), 1.00 (N2) and
  "no discordant pairs" (N4). If the lead prefers to keep the number, it must be tagged (N2) and
  described as a held-out rate, which contradicts the PREREG quote — a decision above this lane.
- `VIVA-QA.md` still carries the false cap sentence at L24 and the three unlabelled answers
  (review-limits findings 1 and 4). Not this lane's file.
- `SOURCE-MAP.md` L51 still has the wrong `per_rung` line number (561 → 556, review-numbers finding 2).
  Not this lane's file.
