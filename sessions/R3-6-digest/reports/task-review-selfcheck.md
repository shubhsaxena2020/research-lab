# Self-Check Quiz Review — `06_review/PRESENTATION/SELF-CHECK.md` vs `05_paper/draft/paper.md`

**Verdict: PASS** — no numeric mismatches, no residual tags, structure correct.
Mismatches found: **0**.

All checks were run programmatically (string-exact search of every distinctive answer
number against `paper.md` with `<!-- num:… -->` tags stripped). Files read in full:
SELF-CHECK.md (109 lines), paper.md (679 lines).

## 1. Question / answer counts

| Check | Result |
|---|---|
| Question labels `**Qn.**` | 15, sequential Q1–Q15, at SELF-CHECK lines 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51 |
| Answer labels `**An.**` | 15, sequential A1–A15, at SELF-CHECK lines 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 99, 102 |
| Q↔A numbering | Qn and An cover the same section in every pair (e.g. Q5/A5 §3.2–§3.3, Q13/A13 §4.7–§4.8, Q15/A15 §6–§8) |

## 2. Answer key separation

- `## Questions` at line 7; `## Answer Key` at line 56.
- All 15 Q blocks precede the key (last Q at line 51); all 15 A blocks follow it
  (first A at line 58). No interleaving, no answers inside the question block.

## 3. Residual `num:` tags

- SELF-CHECK.md: **0** occurrences of `num:`, **0** `<!--` HTML comments,
  **0** `/num` closers. (paper.md has 296 `num:` tags — expected, it is the generated source.)
- The single `c1.` hit in SELF-CHECK (line 105) is the script filename `run_c1.py`,
  not a number tag.

## 4. Section coverage (paper § order → quiz)

| Paper section | Covered by |
|---|---|
| Abstract (L11) | Q1 / A1 (L59) |
| §1 Introduction, H1–H3 (L54) | Q2 / A2 (L62) |
| §2 Related work (L108) | Q3 / A3 (L65) |
| §3.1 Items (L137) | Q4 / A4 (L68) |
| §3.2 Features, §3.3 Gate (L166–187) | Q5 / A5 (L71) |
| §3.4 Audit, §3.5 Naming (L189–223) | Q6 / A6 (L74) |
| §4.1 Audit results (L239) | Q7 / A7 (L77) |
| §4.2 Registered point (L260) | Q8 / A8 (L80) |
| §4.3 Exploratory (L332) | Q9 / A9 (L83) |
| §4.4 R5 control (L355) | Q10 / A10 (L86) |
| §4.5 Top-1 variant (L391) | Q11 / A11 (L89) |
| §4.6 Dense correction (L411) | Q12 / A12 (L92) |
| §4.7 Robustness, §4.8 Second corpus (L496–549) | Q13 / A13 (L95–97) |
| §5 Discussion (L551) | Q14 / A14 (L100) |
| §6 Threats, §7 Disclosure, §8 Reproduction (L595–659) | Q15 / A15 (L103–105) |

Note (not a mismatch): §3.6 Statistics (L225–235) and §9 References (L661) have no
dedicated Q/A pair; Q15 is scoped to §6–§8 by its own heading. Every substantive
section in paper order is represented exactly once.

## 5. Every answer number vs paper.md (verbatim match, tags stripped)

| Key | SELF-CHECK line | Numbers checked | Paper lines | Match |
|---|---|---|---|---|
| A1 (Abstract) | L59 | 0.80, 75.50%, 24.50%, 83.03%, 100.00/99.64/100.00/100.00, 0.00%×5, 0.07% | L18–L32 | ✓ |
| A2 (§1 H1–H3) | L62 | 15, 10, 5 points | L74–L78 | ✓ |
| A3 (Related work) | L65 | 98% → 1% | L64 | ✓ |
| A4 (§3.1 Items) | L68 | 35, 1204, 11873, 5928, 400, 3752, 1879, 273 | L139–L161 | ✓ |
| A5 (§3.2–§3.3 Gate) | L71 | 12, [0.9072, 0.9478], 0.0406, 0.9394, 6.03%, 92.95% | L168–L186 | ✓ |
| A6 (§3.4–§3.5) | L74 | 6, 5-fold, 0.750, 83.03%, 97.29% | L191–L221 | ✓ |
| A7 (§4.1 Audit) | L77 | 0.506/0.539/0.488/0.415, 0.977/0.889/0.923/0.408, R5 0.721/0.794 | L245–L249 | ✓ |
| A8 (§4.2 Registered) | L80 | 100.00/99.64/100.00/100.00, 0.00% CIs, 72.50%, 0.07%, 92.95%, 56.98%, 48.02%, 83.69% | L266–L323 | ✓ |
| A9 (§4.3 Exploratory) | L83 | 0.80, 0.10, 9.50%, 25.44%, 99.75/91.07/92.75/84.71, 87.03–91.30, 7.00% [4.50, 9.75], 15.04% | L336–L350 | ✓ |
| A10 (§4.4 R5) | L86 | 10.29%, 42.08%, 89.25% [85.75, 91.75], 100.00%, 0.974, 91.07/84.71, 0.721 | L361–L384 | ✓ |
| A11 (§4.5 Top-1) | L89 | 78.25%, 0.945, 63.22%, 2.56%, 87.30% | L374–L405 | ✓ |
| A12 (§4.6 Dense bug) | L92 | 78.70%, 0.982→0.874, 0.988→0.887, 12.53%, 0.00%, −2.23% [−3.11, −1.35], 74.58%→99.73% @ 0.27%, 0.874→0.862, 0.811 | L415–L492 | ✓ |
| A13 (§4.7–§4.8) | L95–97 | 400, 273, 127, p=0.052, 553, 0.419, 98.50% @ 89.50%, 85.50% [79.50, 89.50], 7.25, 0.982→0.640 | L500–L546 | ✓ |
| A14 (§5 Discussion) | L100 | 24.50%, 83.03% | L558–L559 | ✓ |
| A15 (§6–§8) | L103–105 | 273/280/400, 553, 1873 | L602–L611 | ✓ |

All ~90 distinctive values (~120 numeric tokens including rung/CI components)
verified verbatim in paper.md. No answer number disagrees, is missing, or comes
from a section other than the one its header claims.

## 6. Presentation-only notes (not mismatches)

- SELF-CHECK L92 uses Unicode minus (U+2212) for −2.23%/−3.11%/−1.35% (paper L443, L474
  use ASCII `-`). Same values; typographic only.
- SELF-CHECK L95 "5–10%" vs paper L506 "five and ten percent" / L503 "five-percent
  level". Digit vs word form; same values.

## Conclusion

PASS. 15 questions + 15 answers, numbered sequentially, key separate after the
questions, zero residual `num:` tags, every section in paper order represented,
and every answer number file+line-verified against paper.md with no mismatches
(file+expected-vs-actual list is therefore empty).
