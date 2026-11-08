# Task report — VIVA-QA (R3-6)

date: 2026-11-08
status: DONE

## What was produced
- `06_review/PRESENTATION/VIVA-QA.md` — 25 hardest viva/reviewer questions with honest
  short answers, each grounded in `05_paper/draft/paper.md` (draft as of 2026-11-08).
- Source: 44 round-2 must-fix items in `sessions/R3/TRIAGE.md` and
  `06_review/reviews/round2-c1/AGGREGATE.md`, distilled to 25, plus the AI-assistance
  disclosure truth (Q1).

## Coverage of the 25
1. AI authorship disclosure (§7). 2. Precision vs refusal-rate naming (MF-1/8/15/39).
3. 24.50% answer rate / no coverage cap (MF-9/38). 4. H1 not testable at registered point (MF-5/25).
5. H3 degenerate by construction (MF-29). 6. H2 trivial transfer + second corpus (MF-6).
7. Degenerate dense block + D4 (MF-34/4). 8. D4 not in hash chain (MF-4/32).
9. Audit confound with gold paragraph (MF-7). 10. One-sided audit, R4 inverted (MF-13).
11. No adjudicated answerability labels (MF-10). 12. "One axis at a time" contradicted (MF-11).
13. Reader baseline is fluency proxy (MF-12). 14. Coverage denominator (MF-9/38).
15. R4 claim rests on one post-hoc cell (MF-14). 16. Zero-width CIs (MF-16).
17. No AUROC intervals (MF-17). 18. Cluster bootstrap on few articles (MF-18).
19. Corrected H3 not matched (MF-19). 20. Corrected over-refusal 11.00% vs cap (MF-20).
21. Ablation point estimates only (MF-21). 22. Rung-2 shortfall + exchangeability (MF-22).
23. Table 7 omits five near neighbours (MF-23). 24. Reproducibility gaps (MF-30/31/33/37).
25. R5 mis-ordering + "ladder of lexical overlap" overstatement (MF-26/27).

## Verification
- Question count: 25 (grep `^## Q` = 25).
- All quoted numerals taken from `05_paper/draft/paper.md`; review-only figures
  (e.g. corrected dev recalls) are attributed to the review item (MF-n) rather than
  presented as draft facts.
- Only `06_review/PRESENTATION/VIVA-QA.md` and this report were written; no other files touched.

## Issues / notes
- Numbers are draft-as-of-2026-11-08 and may change in round 3; answers say so in the header.
- Corrected-run figures not in the draft (thresholds 0.5232/0.5370, coverage 39.60%,
  R5 93.75%, transfer 97.50%/0.706) were deliberately not quoted; only the draft's
  own corrected numbers (AUROC 0.982→0.874, R4 12.53%, over-refusal 11.00%) are used.
