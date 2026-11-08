# R3-6 task-slides — `06_review/PRESENTATION/SLIDES-OUTLINE.md`

Status: **DONE**.

## What was created

- `06_review/PRESENTATION/SLIDES-OUTLINE.md` — 12-slide talk outline (title, problem, setup, ladder, audit, result, why-negative, coverage-constrained, swapped-answer finding, controls, limitations, what-I-learned + AI-use disclosure), with speaker notes per slide.
- `sessions/R3-6-digest/reports/task-slides.md` — this report.

## Counts

- Slides: 12 (within the requested 10–12 range).
- Words: 2007 (incl. speaker notes).

## Grounding

Every numeric claim copied from `05_paper/draft/paper.md` and tagged "(draft as of 2026-11-08; may change in round 3)". Key figures used: SQuAD dev 35 articles / 1204 paragraphs / 11873 questions / 5928 answerable; 400 sampled per half; 3752 items (1879 held out); R2 273 dev / 280 held out; 12 features; target precision 0.80; band refuses 100.00/99.64/100.00/100.00%; over-refusal 75.50%; answer rate 24.50%; pooled precision 83.03%; R1 precision 56.98%, R2 48.02%; band [0.9072,0.9478]; dev admit mass 6.03%; 92.95% refused below lower; H1 0.00% CI [0.00,0.00]; H2 loss 0.07%; H3 0.00% CI [0.00,0.00]; audit surface AUROCs 0.506/0.539/0.488/0.415/0.721 and +overlap 0.977/0.889/0.923/0.408/0.794; exploratory over-refusal 9.50%, coverage 25.44%, R1–R3 drop 7.00% CI [4.50,9.75]; corrected AUROC 0.982→0.874, R4 84.71%→12.53%, dense-eq-1 78.70%; R5 89.25% CI [85.75,91.75], AUROC 0.974; top-1 hit rate 78.25%, AUROC 0.945, miss-refusal 63.22%, hit-refusal 2.56%, P(miss|refused) 87.30%; second corpus 98.50% / 89.50% over-refusal, 85.50% CI [79.50,89.50], AUROC 0.640; reader baseline AUROC 0.419 on 553 dev items; R2 exchangeability p 0.052.

## Notes

- Only this file and the report were written; no other files modified.
- Numbers are draft values subject to round-3 changes.