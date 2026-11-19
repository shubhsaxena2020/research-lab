# Fix report — VIVA-QA.md, three re-review defects (R3-6b)

Lane: `R3-6b-student-pack`. Written 2026-11-19.
Defects routed from `reports/re-review-limits.md` §3 (verdict: DEFECTS FOUND — 3).

**Files written: two.** `07_student/VIVA-QA.md` (the three fixes) and this report. Nothing else touched;
no git state changed.

| # | Defect | Location | Fix |
|---|---|---|---|
| 1 | `0.755` printed as "the refused share" in a dev sentence — it is the band arm's held-out over-refusal, so the sentence mixed halves and made an over-refusal claim the pack may not make | old lines 38–39, in Q3 | clause `the refused share was **0.755**, ` **deleted**; 0.907 / 0.948 / 92.9% / 1.00 kept with their (N2) tags |
| 2 | per-rung κ quoted as a min–max range with no n — invites a trend reading and drops the n = 25 that SOURCE-MAP C08 requires | old line 50, end of Q4 | replaced with all four values, the per-rung n, and the "not an ordering" limit |
| 3 | `AUROC` used at line 29 (Q2) and Q6 but defined only in Q7; `abstain precision` never defined in the viva | preamble glossary, lines 6–12 | two one-line glosses added to the existing "Words used in these answers" block; Q7 untouched |

No other sentence was rewritten. No number was added that is not already in the file or in
`sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` (new numerals: 0.026 and 0.1379 for C08, 25 for C08 —
both already in SOURCE-MAP C08 and CLAIM-INVENTORY).

---

## 1. Proof checks

### (a) `0.755` is gone

```
$ grep -n '0.755' 07_student/VIVA-QA.md
$ echo $?
1
```
No output, exit 1. `0.755` appears nowhere in the file.

### (b) no `cap` / `over-refus` / `feasible` text

```
$ grep -niE 'over-refus|declared cap|\bcap\b|feasible' 07_student/VIVA-QA.md
$ echo $?
1
```
No output, exit 1. Also checked: `grep -n '90\.73' 07_student/VIVA-QA.md` → no output, exit 1 (90.73%
still absent).

### (c) new Q3 and Q4, verbatim

Q3 (lines 36–44):

```
**3. Why is H1 not exercisable, and may you say it was confirmed or refuted?**

Answer: No to both. H1's criterion was that abstain precision must not rise across rungs 1 to 4, and fall by
at least **15** points from rung 1 to rung 3 (N1). At the degenerate registered operating point — t_lo
**0.907**, t_hi **0.948** (N2) — **92.9%** of dev items fell below the low threshold, and every gate reported
**1.00** in every rung (N2). The rung-1 minus rung-3 comparison had no discordant pair (N4). Neither confirmed
nor refuted; an exploratory arm cannot rescue it (N3).

*If pushed, say:* "Not exercisable, so neither confirmed nor refuted (N2, N4)."
```

Q4 (lines 46–56):

```
**4. What does kappa 0.2802 (C01) mean?**

Answer: In this post-hoc re-check, **Cohen's kappa** compares how often two labellers agree with how often
luck alone would make them agree. Here it is **0.2802** (C01). Observed agreement was **0.59** (C02): **59**
of **100** items agreed. Luck alone would give about **0.43** (C03, derived from C01 and C02). So: **modest
agreement beyond chance between these two LLM labellers, in this particular setup**. Not accuracy, not
agreement with a human, not evidence the labels are true. Per rung it was **0.0**, **0.2991**, **0.026** and
**0.1379**, on **25** items each (C08) — with n = 25 those figures are unstable, and their order is not a
hardness ordering.

*If pushed, say:* "0.2802 (C01) is agreement between two LLMs — not accuracy, not human gold."
```

Q4 answer body = **107 words** (under the ~120 limit). Q3 answer body = 84 words.

Preamble glosses as added (lines 10–12):

```
with none, a paired test has nothing to compare. **AUROC** is the chance the gate scores a random answerable
item above a random negative — threshold-free, not an accuracy. **Abstain precision** is, of the items the gate
refused, the share that really were negatives.
```

### (d) word counts

Whole file: `wc -w 07_student/VIVA-QA.md` = **1398** (inside 1,150–1,400). `wc -l` = 132.
Q&A count: `grep -cE '^\*\*[0-9]+\. '` = **13** (inside 12–16).

Per-answer word counts (block = heading + answer + *if pushed*; body = the `Answer:` text only):

| Q | block | body |
|---|---|---|
| 1 | 94 | 88 |
| 2 | 124 | 95 |
| 3 | 111 | 84 |
| 4 | 130 | 107 |
| 5 | 73 | 60 |
| 6 | 123 | 99 |
| 7 | 74 | 62 |
| 8 | 73 | 62 |
| 9 | 84 | 72 |
| 10 | 58 | 48 |
| 11 | 67 | 53 |
| 12 | 146 | 138 (seven bullets; unchanged) |
| 13 | 81 | 67 |
| **sum** | **1238** | — |

The 160 words outside the Q blocks are the title, the two-line usage note and the glossary.

### (e) numeral audit — every numeral with its adjacent ID

Method: split the answers into sentences, take every token matching `\d[\d,\.]*%?`, and record the claim IDs
(`C\d\d`, `N\d`) present in the same sentence.

```python
import re
lines = open("07_student/VIVA-QA.md", encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lines) if re.match(r'^\*\*\d+\. ', l)]
for k, i in enumerate(idx):
    end = idx[k+1] if k+1 < len(idx) else len(lines)
    txt = " ".join(lines[i:end])
    for s in re.split(r'(?<=[.!?])\s+', txt):
        nums = re.findall(r'\d[\d,\.]*%?', s)
        if not nums:
            continue
        ids = sorted(set(re.findall(r'\bC\d\d\b|\bN\d\b', s)))
        print(k+1, nums, ids or "UNTAGGED", "|", s.strip()[:80])
```

Result: **67 sentences carry a numeral; 45 carry their ID in the same sentence; 22 do not.** Every one of the
22 is a non-measurement:

- **13** are the question numbers themselves (`**1.` … `**13.`).
- **5** are name tokens, not measurements: `R1 to R4` (rung names, Q1), `H1` (hypothesis name, Q1 and Q3),
  `MF-14` (cell name, Q2), `Never quote D3 as per-rung` (D3 = dataset name, Q9).
- **4** are numerals inside a *quoted refused claim* in Q12, where the ID follows in the very next clause of
  the same bullet: `"Kappa 0.2802 …"` → `(C01)`; `"12.53% is the real R4 number now"` → `(C22)`;
  `"D3 gives a per-rung result"` → `(C19)`; `"H1 was refuted"` → `(N2, N4)`.

**Untagged measurement numerals: none.** Every value a student would actually say out loud carries its ID in
the same sentence — including the four C08 values and the 25 added by this fix:

```
Q4 ['0.0', '0.2991', '0.026', '0.1379', '25', '08', '25'] ['C08']
   Per rung it was **0.0**, **0.2991**, **0.026** and **0.1379**, on **25** items each (C08) …
```

### (f) `AUROC` gloss now precedes first use

```
$ grep -n 'AUROC' 07_student/VIVA-QA.md | head -3
10:with none, a paired test has nothing to compare. **AUROC** is the chance the gate scores a random answerable
31:AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold. That middle arm is
65:**6. What does the gold-indicator AUROC of 1.0 (C15) mean?**
```

The gloss is at line 10; the first *use* is at line 31. Q7 (line 77 ff.) is unchanged and remains the full
explanation.

`abstain precision` likewise: defined at line 11, first used at line 27 (Q2).

---

## 2. Constraints re-checked after the edit

| Constraint | State |
|---|---|
| 12–16 Q&A | 13 |
| total 1,150–1,400 words | 1398 |
| every numeral keeps its ID tag | verified above; no untagged measurement |
| run labels verbatim | line 28–29: "Registered band, frozen run, D1" / "Frozen exploratory band, as run, still D1" / "Spec-corrected exploratory band, post-hoc, deviation D4" — unchanged |
| "not human gold" | present, Q4 *if pushed* (unchanged) |
| "tautological" | present, Q6 *if pushed* (unchanged) |
| "pooled rung = −1" statement | present, Q9 lines 95–97: "the only rung value present is **−1**, pooled (C19). Never quote D3 as per-rung." (unchanged) |
| "not exercisable" | present, Q3 heading + *if pushed*, Q12 bullet 1 (unchanged) |
| "not yet in the draft" | present, Q11 and Q12 (unchanged) |
| 90.73% absent | confirmed absent |
| no `cap` / `over-refus` / `feasible` | confirmed absent |
| `0.755` absent | confirmed absent |

## 3. Not done (out of scope, for the lead)

The re-review's advisory items were left alone: the `hypotheses.H1.supported = false` field in the frozen
`results_full.json` is still not pre-empted in Q3, and viva 34 still names two of the three MF-14 numbers.
Neither is one of the three defects, and fixing either would have meant writing new text into Q2/Q3 beyond
the requested clause deletion.
