# Writer report — VIVA-QA.md (R3-6b student pack)

Lane: R3-6b-student-pack, writer of deliverable 2. Date: 2026-11-19.
Supersedes the earlier draft report in this path, which keyed its numbers to `MAP-*` IDs; the canonical
table is `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` (`C01`–`C23`, `N1`–`N8`), and this version uses it.

## Output

- Wrote `07_student/VIVA-QA.md` — full overwrite; 13 Q&A entries, 1,328 words.
- Wrote this report only. No other file created or modified. No git command. Nothing under `05_paper/`,
  `06_review/`, `04_experiments/` or another lane folder was written.

## Sources read, in order

1. `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md` (the only source of numbers).
2. `sessions/R3-6b-student-pack/TASK.md` (deliverable 2 spec).
3. `04_experiments/results/c1/r3/R3-3b/ANSWERS.md`.
4. `orchestration/HEAD-REVIEW.md` checkpoints 9–11.
5. `sessions/R3/COMMON.md`, header of `sessions/R3/TRIAGE.md`.
6. Re-parsed with `json.load`: `mf10_adjudication.json`, `mf17_auroc_intervals.json`,
   `mf7_gold_control.json`, `04_experiments/results/c1/results_full.json`,
   `04_experiments/results/c1_corrected/results_full.json`.

Re-verification result: every value I quote matched the JSON on disk. Two inventory key paths are loose —
C09's values live in the top-level `mf10` block (`mf10.comparison_with_prior_llm_adjudication.prior_kappa
= 0.1975`, `.prior_resolved_answerable_n = 5`, `.prior_resolved_answerable_share = 0.05`), not in
`results[...]`; and C17–C19 are flat keys (`c1.r3_3b.mf7.d3_pooled.all.n_hit` etc.), not nested objects.
No value differed.

## (a) Word count

```
$ wc -w < 07_student/VIVA-QA.md
1328
```

Target was "about 900–1300". 1328 is 28 over after five trimming passes (1822 → 1545 → 1518 → 1398 →
1349 → 1328). Every further cut would have removed a required qualifier or a required numeral, so I
stopped there rather than drop content the spec makes mandatory.

## (b) Every numeral in the file, its ID, and the inventory value

| # | Numeral as written | ID cited | Inventory value copied |
|---|---|---|---|
| 1 | 100.00% | C20 | 1.0 → 100.00% (registered band, frozen D1) |
| 2 | 84.71% | C21 | 0.8471 (frozen exploratory, as-run D1) |
| 3 | 12.53% | C22 | 0.1253 (spec-corrected exploratory, post-hoc D4) |
| 4 | 0.9824 | C23 | 0.9824 (cross-ref; C23 asserts AUROC comparability) |
| 5 | 0.8738 | C23 | 0.8738 (cross-ref) |
| 6 | 15 | N1 | "rung-1 minus rung-3 drop ≥ 15 points" |
| 7 | 0.907 | N2 | t_lo = 0.907 |
| 8 | 0.948 | N2 | t_hi = 0.948 |
| 9 | 92.9% | N2 | 92.9% of dev items below t_lo alone |
| 10 | 0.755 | N2 | dev over-refusal 0.755 |
| 11 | 1.00 | N2 | "abstain precision 1.00 in every rung" |
| 12 | 0.2802 | C01 | 0.2802 (0.2801966292134831) |
| 13 | 0.59 | C02 | 0.59 |
| 14 | 59 | C02 | 59 (n_agreed) |
| 15 | 100 | C02 | 100 (n_items) |
| 16 | 0.43 | C03 | 0.4304 — text says "derived from C01 and C02" |
| 17 | 0.0 | C08 | 0.0 (rung 1 kappa) |
| 18 | 0.2991 | C08 | 0.2991 (rung 2 kappa) |
| 19 | 62 | C05 | 62 (labeller A answerable) |
| 20 | 21 | C05 | 21 (labeller B answerable) |
| 21 | 41 | C04 | 41 (n_disagreed) |
| 22 | 35 | C06 | 35 (resolver → answerable) |
| 23 | 6 | C06 | 6 (resolver → not answerable) |
| 24 | 0 | C06 | 0 (ambiguous) |
| 25 | 56 | C07 | 56 (resolved answerable) |
| 26 | 56% | C07 | 0.56 (resolved_answerable_share) |
| 27 | 0.9762 | C14 | 0.9762 (dev r1 auroc_surface_lex) |
| 28 | 1.0 | C15 | 1.0 (auroc_plus_is_gold) |
| 29 | 1.0 | C16 | 1.0 (auroc_is_gold_alone_answerable_oriented) |
| 30 | 0.7327 | C17 | 0.7327 (lexical AUROC hit-vs-miss) |
| 31 | 0.9824 | C10 | 0.9823630831643002 |
| 32 | 0.9776 | C10 | 0.9776211411662427 |
| 33 | 0.9867 | C10 | 0.9866543835742593 |
| 34 | 0.8738 | C11 | 0.8738488843813388 |
| 35 | 0.8587 | C11 | 0.8586833140203312 |
| 36 | 0.8893 | C11 | 0.8893003500532195 |
| 37 | 0.1085 | C12 | 0.10851419878296142 |
| 38 | 0.0946 | C12 | 0.09458017350090517 |
| 39 | 0.1225 | C12 | 0.12252082237972457 |
| 40 | 1,879 | C13 | 1879 (held_out_common.n_items) |
| 41 | 400 | C13 | 400 (n_positive_rung0) |
| 42 | 1,479 | C13 | 1479 (n_negative_rungs1to4) |
| 43 | 18 | C13 | 18 (n_article_clusters) |
| 44 | 10,000 | C13 | 10000 (n_boot) |
| 45 | 20261118 | C13 | 20261118 (seed) |
| 46 | 655 | C17 | 655 (d3 pooled n_hit) |
| 47 | 145 | C17 | 145 (d3 pooled n_miss) |
| 48 | 800 | C17 | 800 (C17 wording "of 800") |
| 49 | 342 | C18 | 342 (dev n_hit) |
| 50 | 58 | C18 | 58 (dev n_miss) |
| 51 | 313 | C18 | 313 (test n_hit) |
| 52 | 87 | C18 | 87 (test n_miss) |
| 53 | −1 | C19 | −1 (rungs_present_value = pooled) |
| 54 | 0.1975 | C09 | 0.1975 (prior_kappa) |
| 55 | 5 | C09 | 5 (prior_resolved_answerable_n) |

Rows: **55** distinct numeral/ID pairings. Numerals that recur in several answers (0.2802, 0.9824, 0.8738,
12.53%, 100.00%, 84.71%, 56, 100, 41, 1.0) carry the same ID inline at each occurrence.

Digit-bearing tokens that are labels, not claims: `R3-3b` (lane), `R1`–`R4` (rungs), `D1`/`D4`
(deviations), `MF-14` (review item), `H1` (hypothesis), `C*`/`N*` IDs.

Removed during drafting because they had no inventory row: `0.5` (AUROC coin-flip baseline — rewritten
"a coin flip would score half"), `20`/`60` (spelling out the 20–60 second rule — rewritten "well under a
minute"), `top-1` (rewritten "first-ranked passage"), and the old draft's labeller model names, GPU
description and `MAP-*` IDs (model names and GPU are not in the inventory at all).

## (c) IDs used and entry count

```
$ grep -o 'C[0-9][0-9]' 07_student/VIVA-QA.md | sort -u
C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23
$ grep -o 'C[0-9][0-9]' 07_student/VIVA-QA.md | sort -u | wc -l
23
$ grep -o 'N[0-9]' 07_student/VIVA-QA.md | sort -u
N1 N2 N3 N4 N5 N6
$ grep -cE '^\*\*[0-9]{1,2}\. [A-Z]' 07_student/VIVA-QA.md
13
```

All 23 claim IDs are used. N7 and N8 are unused: the spec's required questions do not need them, and N7's
content is already carried by C16 plus the "construction artefact" framing the inventory authorises.

## Automated numeral sweep

`numcheck.py` (scratch file) strips IDs and labels, extracts every numeric token, and matches it to the
table above:

```
total numeric tokens after scrubbing: 83
unmapped tokens: ['-6', '3', '3,']
unmapped count: 3
words: 1328
qa_entries: 13
```

The three residuals are scrubbing artefacts, each confirmed by printing its context: `-6` is the tail of
the lane label `R3-6b` in the title, `3` is a slice of `12.53%`, and `3,` is a slice of the `D3,` label.
No un-mapped numeral remains.

## Required-question coverage

| Required topic | Entry | IDs |
|---|---|---|
| MF-14 registered vs exploratory | Q2 | C20, C21, C22, C23 |
| H1 not exercisable; not confirmed, not refuted | Q3 | N1, N2, N4, N3 |
| kappa 0.2802 | Q4 | C01, C02, C03, C08 |
| gold-indicator AUROC 1.0 | Q6 | C14, C15, C16, C17 |
| claims you must not make | Q12 | N2–N6, C01, C15, C16, C19, C20, C22 |
| raw agreement / 41 disagreements / 56 resolved | Q5 | C02, C04, C05, C06, C07 |
| exploratory-post-hoc, not yet in the draft | Q11 | N5, N6 |
| what an AUROC is, not accuracy | Q7 | C10, C11 |
| paired difference excludes zero | Q8 | C12, C13 |
| D3 pooled, no per-rung estimate | Q9 | C17, C18, C19 |
| the two adjudication runs, cautious comparison | Q10 | C09, C01, C07 |
| scoping answer if the gate "fails" | Q13 | C22 |

Language checks: no sentence calls H1 confirmed or refuted; kappa is described only as modest agreement
beyond chance between two LLM labellers with no human gold; the 1.0 is called a tautology / construction
artefact; D3 is called pooled with no per-rung estimate; MF-14 carries all three run labels; every R3-3b
item is labelled exploratory/post-hoc and not in the draft.

## Issues

- 1,328 words against a 900–1300 target (28 over). Cutting further would have removed a mandatory
  qualifier, a mandatory numeral, or the refusal list.
- Inventory key-path imprecision for C09 and C17–C19, noted above; values are unaffected.
- The old draft in this path used `MAP-*` IDs and stated labeller model names and a GPU detail the
  inventory does not support; both are gone.
