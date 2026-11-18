# Batch-1 independent re-verification (review-batch1)

Scope: independent re-check of audit-A.md, audit-B.md, audit-C.md against the actual
`05_paper/draft/paper.md` (696 lines) and `06_review/RESPONSE-LETTER-R3.md` (435 lines).
No file was edited except this report. All line numbers below refer to the generated draft
unless the template/code is named explicitly. Verdict-line counting was done programmatically
(regex over every `Verdict:` line paired with its nearest preceding `##/### MF` header), not by eye.

## Top-line result

Every substantive audit verdict in the assigned claim set is **confirmed**. All ten "downgrades"
(letter says `resolved`, audit says partial/not-implemented) are independently reproduced. The
inventory count in audit-B is **exactly confirmed**: 85 verdict lines, 23 resolved / 51 partial /
11 deferred. Three secondary discrepancies were found (letter-vs-draft table numbering, an
incomplete occurrence list in audit-C, and template-derived line numbers in audit-B MF-35/MF-40);
none changes a verdict.

---

## 1. MF-14 — R4 placement and unscoped §5.2 — audit-A "partial": CONFIRMED

- Draft L450 (Table 6): `Band abstain precision, R4 | ...100.00%... | ...90.73%...`
- Draft L456 (Table 6): `Exploratory precision, R4 | ...84.71%... | ...12.53%...`

The corrected exploratory cell `12.53%` sits in the *same row* as frozen exploratory `84.71%`,
not in the row carrying registered band `100.00%`. The abstract repeats the same framing at
L46–49: `breaks the gate once the dense features are implemented as specified — refusal on R4
falls to ...12.53%... and discrimination from ...0.982... to ...0.874... AUROC.` — with no
"exploratory" qualifier. §5.2 (L581–590) contains no occurrence of "exploratory"; it reads
`When they come apart — R4, where the passage matches perfectly and one span is wrong — the gate
has nothing to work with, and the corrected run shows it.` D4 is presented as a deviation
(L434–437: `we implemented the feature as §3.2 specifies ... as a declared, post-hoc sensitivity
analysis (deviation D4)`), not promoted to primary. Both halves of the MF-14 demand therefore
remain unmet. **Mismatch with letter**: L61 verdict `resolved` and change text
`report registered R4 100.00% beside exploratory 12.53% and restrict §5.2`.

## 2. R3-MF-39 — 'abstain recall' still present — audit-C "Not implemented": CONFIRMED (audit under-enumerates)

Draft contains **5** occurrences, not the 3 listed in audit-C:

- L17 (Abstract): `maximise abstain recall (the refusal rate, P(refused | negative))`
- **L76 (§1, H2): `precision at equal abstain recall when applied to a disjoint held-out half and to a second corpus.`** — missed by audit-C
- **L78 (§1, H3): `score, by at least five points, at matched abstain recall.`** — missed by audit-C
- L179 (§3.3): `Both maximise dev abstain recall (the refusal rate, P(refused | negative))`
- L218 (§3.5): `called abstain precision (its 'abstain recall' is the same refusal rate)`

Audit-C quoted L17, L179, L218 and reached the right verdict; the omission of L76/L78 makes the
finding stronger, not weaker. **Mismatch with letter**: L423 verdict `resolved`, change text
`the undefined term 'abstain recall' is removed from the Abstract/§3.3`.

## 3. MF-35 / MF-40 — generator prefixes; seven vs eight tables — audit-B "partial": CONFIRMED

- Draft contains exactly **7** `**Table N.**` captions (L127, L241, L262, L273, L379, L439, L463), not 8. Captions are sequential and in appearance order.
- Template `05_paper/template/draft_template.md` placeholder order: L132 `{{TABLE:T7_prior_work}}`, L242 `{{TABLE:T3_audit}}`, L257 `{{TABLE:T1_per_rung}}`, L261 `{{TABLE:T2_hypotheses}}`, L363 `{{TABLE:T5_arms}}`, L415 `{{TABLE:T4_frozen_vs_corrected}}`, L419 `{{TABLE:T6_ablations_corrected}}`. So T7→Table 1, T3→Table 2, T1→Table 3, T2→Table 4, T5→Table 5, T4→Table 6, T6→Table 7. `make_paper_assets.py` L588–594 writes the files in T1…T7 order — exactly the misalignment audit-B reports.
- Table 2 caption (L241) is not self-contained: `n per rung as listed in Table 3.`

**Mismatches with letter**: L145 MF-35 verdict `resolved`, change text `generator prefixes T1–T7 aligned to appearance order` (false in template); L165 MF-40 verdict `resolved`, change text `self-contained captions ... for all eight tables` (draft has seven, caption L241 defers n to Table 3). Caveat: audit-B's *line numbers* for the table-caption enumeration (L127, L237, L252, L256, L273, L358, L410, L414) are template-derived/approximate — the generated draft's caption lines are the seven listed above. Substance holds; citations do not.

## 4. MF-1 / MF-8 / MF-15 — missing exact fractions — audit-A "partial": CONFIRMED

Programmatic search over the whole draft returns **zero** hits for `400/400`, `279/280`,
`1478/1780`, `1760/1873`, `279/(279+302)`, `279`, `302`, `1478`, `1780`. Draft L266–269 gives only
`n` and percentages (e.g. `R2 | 280 | 99.64% | 48.02% ...`), and L271 gives
`Pooled precision is ...83.03%... at the registered point`. There is no `83.0%` bare figure either.

**Mismatch with letter**: L9 (MF-1) `resolved`, change text `refusal counts per cell (R1 400/400; R2 279/280) and pooled held-out precision 1478/1780 = 83.0%`; L37 (MF-8) `resolved`, `R2 99.64% = 279/280 recall vs precision 279/(279+302) = 48.0%`; L65 (MF-15) `resolved`, `Table 1 R1 400/400, R2 279/280 ... 1760/1873 dev refusals; pooled held-out precision 1478/1780 = 83.0%`.

## 5. MF-20 — no corrected dev over-refusal — audit-A "partial": CONFIRMED

Draft L457: `Exploratory over-refusal | 9.50% | 11.00%.` L494–497: `the corrected exploratory band
ends at an over-refusal of ...11.00%..., above the ...0.10... cap it was constrained to on dev —
the constraint is on dev, not on the held-out half, and we report the breach rather than hide it.`
The dev/held-out distinction and the breach are present; a corrected **dev** over-refusal number is
not. **Mismatch with letter**: L85 verdict `resolved`, change text `give corrected dev over-refusal`.

## 6. MF-2 / MF-34 / R3-MF-3 — thresholds + coverage row — audits A/B/C "resolved/Implemented": CONFIRMED

- L439 (Table 6 caption): `The two runs refit their thresholds on different dev score distributions, so precision and coverage rows compare two operating points; AUROC rows are threshold-free.`
- L441: `| Quantity | Frozen run | Spec-corrected (D4) |` — header is "Frozen run", not "D1".
- L445: `Band lower threshold (t_lo) | 0.9072 | 0.5232`
- L446: `Band upper threshold (t_hi) | 0.9478 | 0.5370`
- L458: `Exploratory coverage | 25.44% | 39.60%.`

All requested quantities and caveats are verbatim. Consistent with letter L13 (MF-2 `resolved`),
L141 (MF-34 `resolved`), L207 (R3-MF-3 `resolved`). Numbering caveat already noted by audit-A:
the letter says "Table 4" for MF-2/MF-34 while the draft renders these as Table 6.

## 7. Other assigned claims spot-checked (all confirm their audits)

- MF-26 (audit-A resolved): L43 verbatim `Overlap separates each rung from answerable items, and the exploratory refusal rates invert between R2 (91.07%) and R3 (92.75%); the overlap-matched R5 (89.25%) sits below R2 (§4.4).`
- MF-27 (audit-B resolved): L394–395 verbatim `which places it between R2 (91.07%) and R4 (84.71%) in the ordering.`
- MF-38 (audit-B resolved): L573 `answers about one question in four (24.50% of answerable questions)`; L19–21 `refuses 75.50% ... answers only 24.50%`.
- MF-11 (audit-A partial): L156–159 contains the "one *respect* ... but not in only one respect" clause, but no per-rung length/overlap distributions; L396 says R5 items `are the longest negatives in the ladder` (matched on overlap, not length).
- MF-41 (audit-B resolved): L294/L298 inline both SVGs with captions; `make_paper_assets.py` L595–596 writes them.
- MF-42 / MF-43 / R3-MF-36 / R3-MF-37 / R3-MF-38 (audit-C Implemented): L343 → §4.6, L124 → §4.7; L416 `63.22% of retrieval misses`, L418 `P(miss refused) = 87.30%`; L394–395, L39–43, L379 respectively confirm.

---

## 8. Inventory count — audit-B "Inventory and count reconciliation": CONFIRMED EXACTLY

Programmatic parse of all `Verdict:` lines in `RESPONSE-LETTER-R3.md`:

| Cycle | Resolved | Partial | Deferred | Total |
|---|---:|---:|---:|---:|
| Round 2 (MF-1…MF-44) | 18 | 21 | 5 | 44 |
| Round 3 (R3-MF-1…R3-MF-41) | 5 | 30 | 6 | 41 |
| **Total** | **23** | **51** | **11** | **85** |

- 85 verdict lines, **no duplicate IDs, no gaps**: MF-1…MF-44 (44/44) and R3-MF-1…R3-MF-41 (41/41) all present.
- Resolved round-2 IDs match audit-B's list exactly: MF-1, MF-2, MF-8, MF-11, MF-14, MF-15, MF-20, MF-26, MF-27, MF-33, MF-34, MF-35, MF-38, MF-39, MF-40, MF-41, MF-42, MF-43.
- Resolved round-3 IDs match exactly: R3-MF-3, R3-MF-36, R3-MF-37, R3-MF-38, R3-MF-39.
- Deferred round-2: MF-7, MF-10, MF-17, MF-23, MF-28. Deferred round-3: R3-MF-1, R3-MF-9, R3-MF-16, R3-MF-17, R3-MF-21, R3-MF-25.
- Letter header L5 `18 resolved, 21 partial, 5 deferred` matches the parsed round-2 tally.
- Audit-B's tally-discrepancy analysis is correct: any brief claiming "86 entries / 52 partial" is off by one; the letter itself supports 85/51.

## 9. Downgrade ledger (letter verdict → audit verdict → re-verification)

| ID | Letter (R3) | Audit | Independent result |
|---|---|---|---|
| MF-1 | resolved | partial | downgrade confirmed (§4) |
| MF-8 | resolved | partial | downgrade confirmed (§4) |
| MF-11 | resolved | partial | downgrade confirmed (§7) |
| MF-14 | resolved | partial | downgrade confirmed (§1) |
| MF-15 | resolved | partial | downgrade confirmed (§4) |
| MF-20 | resolved | partial | downgrade confirmed (§5) |
| MF-35 | resolved | partial | downgrade confirmed (§3) |
| MF-39 | resolved | partial | downgrade confirmed (§2, plus L209–223 definition is present) |
| MF-40 | resolved | partial | downgrade confirmed (§3) |
| R3-MF-39 | resolved | Not implemented | downgrade confirmed (§2) |

Agreements also re-checked: MF-2, MF-26, MF-27, MF-33, MF-34, MF-38, MF-41, MF-42, MF-43,
R3-MF-3, R3-MF-36, R3-MF-37, R3-MF-38 (§6–§7).

## 10. Issues found

1. **Letter/draft mismatch (material):** ten items carry `Verdict: resolved` in the response letter while the draft lacks the promised evidence (exact fractions, corrected dev over-refusal, restricted §5.2, removed 'abstain recall', aligned generator prefixes, eight tables).
2. **Letter/draft mismatch (numbering):** MF-2/MF-34/R3-MF-3 change text says "Table 4"; the draft renders that content as Table 6. MF-40 promises eight tables; the draft has seven.
3. **Audit-C enumeration incomplete:** 'abstain recall' occurs five times, not the three quoted (L76 and L78 in §1 omitted). Verdict unaffected.
4. **Audit-B citation drift:** MF-35/MF-40 table-caption line numbers are template-derived; generated-draft caption lines are 127/241/262/273/379/439/463. Verdicts unaffected.
