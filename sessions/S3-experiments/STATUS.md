# STATUS S3-experiments

last_update: 2026-11-03T07:22+05:30 (S3b)
state: **S3b in progress.** Numbers audit **PASSES** on the rewritten draft. Rung 5, the transfer arm,
the top-1 variant, the statistics addendum and a spec-corrected re-implementation of the dense features
are all run and written. Draft rewritten as a NEGATIVE RESULT / audit paper and rebuilt from a template.
Review round 2, claims audit, originality re-run and the student digest are in flight.

## What S3b has done so far (verified from disk, not from reports)

1. **Numbers audit: PASS.** `python tools/check_numbers.py --draft 05_paper/draft/paper.md` →
   `417 number(s) in 1 file(s): 263 matched, 154 exempt, 0 finding(s)` / `PASS`. It was 79 findings at
   session start. The draft is now *generated* (`05_paper/build_draft.py` from
   `05_paper/template/draft_template.md`) and every table is emitted by
   `04_experiments/src/make_paper_assets.py` with per-cell `num:` markers, so a stale number cannot
   survive a rebuild.
2. **Exploratory rung 5 (overlap-matched negatives), deviation D2 declared before its numbers existed.**
   Matching worked as far as the pool allows: mean |overlap(chosen) − overlap(gold)| 10.29% on test
   against 42.08% for a random negative. The gate is *not* defeated: R5 abstain precision 89.25%
   [85.75, 91.75] at the exploratory point, between R2 and R3. Surface audit 0.721 on dev, the closest
   any rung has come to the 0.75 stop rule; it passes.
3. **H2 transfer on the 400 built 2WikiMultihopQA items, frozen operating point.** Confirmatory 98.50%
   precision at 89.50% over-refusal (degenerate, uninformative); exploratory 85.50% [79.50, 89.50], a
   drop of 7.25 points. Discrimination collapses from 0.982 to **0.640** AUROC. Direction test only.
4. **2WikiMultihopQA citation resolved and title-checked**: DOI 10.18653/v1/2020.coling-main.580; the
   abstract sentence that establishes the dataset was quoted; four authors (no Nagata). arXiv 2011.01079
   is a pentaquark paper and is not cited as this work.
5. **Top-1-presented variant (deviation D3), the review's top objection.** BM25 rank-1 is the gold
   paragraph for 78.25% of test questions. The same stack detects hit vs miss at 0.945 AUROC, refusing
   63.22% of misses and 2.56% of hits. It confirms the mechanism and cannot exculpate the gate.
6. **Statistics addendum** (review items MF-3..MF-6): rung-2 subsample exchangeable (smallest p = 0.052);
   cluster-by-article intervals agree with item-level ones (four of five narrower); exploratory R1−R3 =
   7.00% [4.50, 9.75]; band and recall-matched single refuse identical negatives (0 discordant pairs).
7. **A real defect found and disclosed (deviation D4).** `features.py` used the presented passage as its
   own dense query, so `dense_presented ≡ dense_top1 ≡ 1.0` on every R0–R3 row and the dense-cosine
   baseline was a constant. A spec-conformant re-implementation (question as query) drops held-out AUROC
   from 0.982 to 0.874 and collapses exploratory R4 precision to 12.53%: the gate cannot see a swapped
   answer span inside the gold paragraph. Both runs are reported; the frozen run is not refitted.
8. **Originality corpus built** (nine source PDFs converted to text, 96k words) and the mechanical check
   run on the previous draft: zero unquoted eight-gram hits, eight uncited scare quotes (removed in the
   rewrite).

## Environment facts

- `python` 3.11.15 with torch, bm25s, sentence-transformers, sklearn, scipy. matplotlib and pandas are
  absent, so figures are emitted as SVG by code.
- Feature passes are minutes, not hours (seven minutes for the full 3,752-item set), so no heavy-lock
  contention arose.
- `pdftotext` is available at /mingw64/bin/pdftotext and was used for the originality corpus.

## Next in this session

1. Review round 2 (six personas) and answers to all twelve must-fix items.
2. `06_review/CLAIMS-AUDIT.md` plus `tools/claims_audit.py` on the accepted draft.
3. Originality re-run on the rebuilt draft; remove uncited quotes.
4. `06_review/STUDENT-DIGEST-S3.md`.
5. Final: `tools/check_all.py`, reader tests, and this file.
