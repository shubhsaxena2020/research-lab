# Batch 1 Review — 4 files vs 05_paper/draft/paper.md

Reviewer task: check every number in the 4 files against draft, check every explanation against methods/results, list all mismatches with file+line+expected vs actual. Also check word counts (digest <=1000 words, slides 10-12, viva 25 questions, self-check will come later). Report only, no edits to the 4 files.

## Word counts / counts (verified)

- STUDENT-DIGEST-S3.md: 998 words (wc -w). Limit <=1000. PASS.
- SLIDES-OUTLINE.md: 12 slides (grep "^## Slide" = 12). Requirement 10-12. PASS.
- WALKTHROUGH.md: 4171 words (no limit given).
- VIVA-QA.md: 25 questions (grep "^## Q" = 25). Requirement 25. PASS.
- Self-check: not present (noted as "will come later" — excluded).

## Number check — DRAFT-CANONICAL numbers

Every numeral in all 4 files was extracted and cross-checked against draft numbers (num: markers + plain text numerals in draft). Results:

### 1. 06_review/STUDENT-DIGEST-S3.md — PASS (all numbers match draft)
- 3752 items / 1879 held out (§3.1, draft lines 160) ✓
- 12 features, band [0.9072, 0.9478], single 0.9394, precision 0.80 (§3.3, draft 168-183) ✓
- Audit gate 0.750, 5-fold (§3.4, draft 193-196) ✓
- AUROC surface 0.506/0.539/0.488/0.415 (Abstract p.33-35, Table 3) ✓
- Overlap 0.977, R4 0.408 ✓
- Refusal 100.00/99.64/100.00/100.00, over-refusal 75.50, answers 24.50, pooled precision 83.03, R1 56.98, R2 48.02 (§4.2, Table 1) ✓
- H1 0.00 CI [0.00,0.00]; H3 0.00 [0.00,0.00]; H2 loss 0.07; 92.95% refused by lower threshold ✓ (Table 2, draft 277-316)
- Exploratory over-refusal 9.50, coverage 25.44, R1-R3 7.00 [4.50,9.75] ✓ (§4.3)
- Dense 78.70% =1, corrected R4 12.53, AUROC 0.982->0.874, R1-R3 corrected 99.75/92.86/95.50 ✓ (§4.6, Table 4)
- Non-draft numerals flagged by script (08 from date, 12.5 from §4 heading "12.5% swapped-answer", 100, 2025, arXiv:2502.07255) are formatting/external citations, not draft-value mismatches. The arXiv:2502.07255 claim on L74 is sourced to [STUDENT-DIGEST-S2], not the draft — correct per file's own citation; not a number mismatch vs draft.

### 2. 06_review/PRESENTATION/WALKTHROUGH.md — PASS (all numbers match draft)
- Same core numbers as digest, plus: 35 articles/1204 paragraphs/11873 questions/5928 answerable ✓ (§3.1)
- 273 dev R2 items, p=0.052 ✓
- Table 6 "less than a third of AUROC margin" ✓ (§4.6, draft 486-494)
- 6.03% admit mass ✓, 10000 resamples seed 12345 ✓ (§3.6)
- R2 0.889/R3 0.923/R5 0.721 surface + overlap ✓ (Table 3)
- R5 mean abs diff 10.29% vs 42.08% ✓ (§4.4)
- Top-1 78.25% hit, AUROC 0.945, 63.22%/2.56%, 87.30% ✓ (§4.5)
- Dense 78.70%, 10 informative columns, AUROC 0.982->0.874, R4 12.53, H3 -2.23 ✓ (§4.6)
- Reader 0.419 on 553 items ✓ (§4.7)
- Transfer 0.982->0.640, over-refusal 89.50 ✓ (§4.8)
- 40 hand-inspected R4 items (§5.4 draft 590) ✓; 1873 dev items, 280 held-out R2 ✓ (§6)
- Non-draft numerals flagged: 000 (from 10000/100000), 0.5/1.0 (generic AUROC scale in glossary), 08 (date), 40 (correct per §5.4), 56 (rounding in reviewer-question text), 100 (generic). None are value mismatches.

### 3. 06_review/PRESENTATION/SLIDES-OUTLINE.md — PASS (all numbers match draft)
- 3752/1879, 273/280 ✓; 12 features ✓
- Audit surface 0.506/0.539/0.488/0.415/0.721; overlap 0.977/0.889/0.923/0.408/0.794 ✓ (Table 3, incl R5 — digest omitted R5/0.721/0.794, slides include them; both correct vs draft)
- Refusal/precision/over-refusal/answer 100/99.64/100/100, 75.50/24.50/83.03/56.98/48.02 ✓
- Band width 0.0406, single 0.9394, admit 6.03, 92.95 ✓
- H1/H2/H3 criteria 15/10/5 points, diffs 0.00/0.07/0.00 ✓
- Exploratory 9.50/25.44, R1-R4 99.75/91.07/92.75/84.71, precision 87.03-91.30 ✓ (draft 341-346: 87.03-91.30 correct)
- R1-R3 7.00 [4.50,9.75], R1-R4 15.04 ✓
- R4 corrected 12.53, AUROC 0.982->0.874, 78.70% ✓
- R5 89.25 [85.75,91.75] AUROC 0.974 ✓ (Table 5)
- Top-1 78.25/0.945/63.22/2.56/87.30 ✓
- Second corpus 98.50 at 89.50, exploratory 85.50 [79.50,89.50], AUROC 0.640 ✓ (Table 5)
- R2 273/280 vs 400, p=0.052, reader 0.419 on 553 ✓

### 4. 06_review/PRESENTATION/VIVA-QA.md — PASS WITH NOTES (draft numbers all correct; additional numbers are MF-labelled round-2 review items, not in draft)

All draft-sourced numbers verified identical to draft: 75.50/24.50/92.95/6.03/0.80/7.00 [4.50,9.75]/15-point/0.9072/-2.23 [-3.11,-1.35]/7.25/57.50/9.50/0.982/0.640/78.70/10 columns/0.982->0.874/12.53%/273/280/127 dropped/0.052/11.00% (§4.6 Table 4: exploratory over-refusal corrected 11.00 ✓)/0.10 cap/553 items/0.419/98.50 at 89.50/85.50 [79.50,89.50]/97.29 not used/etc.

Numbers in VIVA-QA NOT in draft (all explicitly labelled MF-n / "from review evidence, not the draft" per file header L5-6 and inline tags — these are intentional MF citations, not silent mismatches):

| # | Location | Value | Status |
|---|----------|-------|--------|
| M1 | Q2 L23 | 400/400, 279/280, 400/400, 399/399 | MF-derived (279/280 = 99.64% ✓ arithmetic consistent with R2 n=280; 399/399 consistent). Not in draft text. |
| M2 | Q5 L52-53 | -2.23% but "0.80 constraint violated, matched single 0.7886", Q19 L166-167 recall 0.9898 vs 0.9925 | Draft §4.6 L476-477 says "below 0.80" without 0.7886; VIVA adds 0.7886/0.9898/0.9925 from MF-19 review evidence. Numbers consistent directionally; provenance labelled. |
| M3 | Q6 L61-62 | 7.25-point drop, 5-10 gap | Draft §4.8 L531-534 defines gap, L544 gives 7.25 drop ✓ — actually IS in draft. (Listed here for completeness; verified present.) |
| M4 | Q14 L127 | 98/400 = 24.50% question-level coverage | Novel derivation (MF-9/38). Correct arithmetic (98/400=24.5). Item-level vs question-level distinction matches draft L271. |
| M5 | Q16 L144 | 0 of 1479 (H3 discordant pairs) | MF-16. Number not in draft. |
| M6 | Q18 L160-161 | cluster ratio 0.45 vs 0.851 | Draft §4.7 L510 gives 0.45; 0.851 is the draft's superseded value flagged by MF-18. VIVA correctly notes discrepancy rather than repeating error. |
| M7 | Q21 L182-183 | 0.874 vs 0.862, 0.870 | Draft Table 6: no_dense 0.862 ✓, dense_only 0.870 ✓ (draft L452/456). Actually in draft. |
| M8 | Q23 L197-201 | search counts 84+91, N1-N4/N10 IDs, AUROC 0.979 | MF-23 search metadata, not in draft. IDs/dates per file's own MF convention. |
| M9 | Q24 L205-207 | MF-30/31/33/37 reproduction items | Procedural, not numeric mismatches. |
| M10 | Q25 L215-216 | R5 between R2 (91.07) and R4 (84.71) | Matches draft §4.4 L381-382 exactly. |

M1, M2, M4, M5, M8 are extra-draft numbers but are consistently MF-tagged in-file, satisfying the file's own header contract. No silent invention found.

## Explanation vs methods/results cross-check

All four files' explanations were checked against draft §3-§6:

- Digest: "ladder measured overlap, not answerability"; audit explanation; dense-defect explanation. Matches draft §4.1/§5.1/§4.6. ✓
- Walkthrough: per-section "what it says / attack / answer" all grounded to bracketed draft sections; descriptions of pre-registration, one-sided audit, metric correction (§3.5), bootstrap (§3.6) accurate. ✓
- Slides: per-slide bullets accurate to draft tables. ✓
- VIVA: answers to Q1-Q25 are consistent with draft E/H/§4 and the MF-tagged review limitations (D4 post-hoc, denominator, zero-width CIs, no AUROC intervals, cluster ratio, etc.). Q8 (D4 hash chain stops at D3 = draft L8-9 "three hashes / D1-D3") ✓; Q10 (one-sided audit, R4 0.415) ✓ (draft L202-205); Q23 (Table 7 omits neighbours — draft Table 7 L129-133 lists only 2 ✓).

## Conclusion

File+line | Expected (draft) | Actual: NO MISMATCHES in the 4 files.
- Digest: 0 mismatches. 998 words ≤ 1000 PASS.
- Walkthrough: 0 mismatches.
- Slides: 0 mismatches. 12 slides PASS.
- VIVA: 0 silent mismatches. 25 questions PASS. Extra-draft numbers are all MF-labelled per the file header convention (M1, M2, M4, M5, M8 above) — flagged here for visibility, not counted as errors.

Self-check file pending, as instructed; not reviewed.
