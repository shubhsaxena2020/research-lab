# ANSWERS — R3-5 (related work & novelty refresh)

## MF-23 — Table 7 omits the five nearest neighbours from our own search

Verdict: FIXED (evidence supplied; integrator updates the draft).

Evidence:
- `02_literature/related-work-r3/table7.json` now contains 12 rows: this paper plus 11 neighbours, including
  the five named in the review (N1 arXiv:2502.07255, N2 arXiv:2609.22056, N3 doi:10.32604/cmc.2026.088937,
  N4 arXiv:2609.32269, N10 doi:10.5281/zenodo.20547014) and RINSE/GRAB-RAG/DeclineCraft/Abdumalikov/Two Axes/
  RefusalBench. Every cell carries a source pointer in `source_quotes`.
- Search record: `02_literature/NOVELTY-CHECK.md` (84 OpenAlex + 91 arXiv queries, 2026-11-03) and the round-3
  refresh `02_literature/related-work-r3/NOVELTY-R3.md` (18 further OpenAlex slice queries, 2026-11-08).
- What §4.1's audit adds beyond N4's surface-only adversary (AUROC 0.979 from paragraph count): our audit
  reports the surface-only AUROC per rung (R1-R4) and its sensitivity variant with question-passage overlap,
  plus the overlap-matched (R5) and top-1-presented controls, so a rung that only measures formatting is caught
  and rebuilt rather than reported as a result.

Proposed related-work paragraph (own words, quotes marked):

> The closest prior work is RINSE (Chen, Hua, Xiao, 2026, arXiv:2609.37469), which asks whether sufficiency
> can be judged from the question and evidence alone and reports a sufficiency score of 0.837 against 0.746 for
> the best of ten prior methods, using substitution, deletion and question-swap constructions that control
> surface features; it does not fit thresholds on retrieval features and does not report a false-refusal rate
> per rung. GRAB-RAG (Setiawan, 2026, arXiv:2608.22228) tests the same questions under supportive, degraded,
> missing and misleading contexts and finds that small frozen models "still answer 41.6% of misleading questions"
> under explicit abstention prompting; it is prompt-based, with no threshold pair and no per-rung precision.
> DeclineCraft (Thakur, Saparov, Ribeiro, 2026, arXiv:2610.28340) measures retrieval-side and parametric
> abstention jointly and reports Correct Abstention Rate alongside Answerable Attempt Rate; it does not use a
> retrieval-feature gate. Beyond Confidence (Kumar et al., 2025, arXiv:2502.07255) supplies the two-threshold
> construct in perception (conformal plus abstention thresholds, AUC 0.993-0.995), but on camera/LiDAR, not
> retrieval features, and with no hardness ladder. Predictable Failure (Bacellar, 2026, arXiv:2609.22056) fits
> a logistic abstention policy on up to nine retrieval features and reports a Confident-Wrong-Answer Rate, but
> one policy across five failure regimes, with no dead zone and no per-rung false-refusal rate. Sufficiency-Gated
> RAG (Shishir et al., 2026, doi:10.32604/cmc.2026.088937) reports both an unsupported rate (17.1% at 57.2%
> coverage) and a wrongful-refusal rate (7.0% of sufficient contexts), but at a single calibrated operating point.
> Before Answering (Mondal et al., 2026, arXiv:2609.32269) occupies the separability finding: a classifier that
> only counts paragraphs reaches AUROC 0.979 on deleted-evidence negatives, which is why our rungs are
> size-matched and audited. Reliable Biomedical RAG (Saha et al., 2026, doi:10.5281/zenodo.20547014) is the
> nearest "retrieval-score gate plus hard negatives" work and reports both answerable recall (97.5%) and
> unsupported recall (64.3%). Two Axes (Wagner, 2026, arXiv:2607.08456) argues the two-sided point with
> thresholds on correctness and answerability scores, but from hidden-state probes rather than retrieval features.
> RefusalBench (Muhamed et al., 2025, arXiv:2510.10390) supplies a stronger perturbation ladder (176 strategies,
> six categories, three intensities) but as a benchmark, with no gate. Abdumalikov et al. (2024,
> arXiv:2403.01461) is the observation the ladder is built on: accuracy falls "from 98% to 1%" when random-negative
> training meets high-overlap excerpts. The delta this paper keeps is narrow: a four-rung negative ladder, held
> out per rung, with two dev-fitted thresholds on six retrieval features, reporting abstain precision, over-refusal
> and coverage per rung, plus where the band sits relative to the observed dev feature range.

## MF-28 — Table 7's DeclineCraft row mischaracterised

Verdict: FIXED (evidence supplied; integrator updates the draft).

Evidence:
- Source: arXiv:2610.28340 (Thakur, Saparov, Ribeiro, 2026), abstract (OpenAlex reconstruction, cached at
  `02_literature/related-work-r3/raw/openalex-n3`? no, DeclineCraft abstract from OpenAlex W7223089569):
  "Reliable retrieval-augmented generation (RAG) requires recognizing when neither retrieved documents nor
  parametric knowledge supports an answer. We introduce DeclineCraft, a dynamic abstention benchmark whose
  unanswerable questions target Minecraft feature additions after a corpus cut-off, with audits of possible
  parametric exposure. ... Across 27 LLMs, we measure Correct Abstention Rate (CAR; how often models acknowledge
  insufficient knowledge on unanswerable questions), Answerable Attempt Rate and Answer Accuracy."
- The paper's own §2 already says DeclineCraft "measures retrieval-side and parametric abstention jointly",
  which contradicts the old Table 7 row ("per category, retrieval and memory reported separately").
- MF-28 asks to remove "several unanswerable classes" and "retrieval and memory reported separately" unless a
  named section supports them; the abstract supports "jointly", not "separately".

Correct one-line characterisation (with quote):

> DeclineCraft (arXiv:2610.28340) is "a dynamic abstention benchmark whose unanswerable questions target
> Minecraft feature additions after a corpus cut-off, with audits of possible parametric exposure", measuring
> "Correct Abstention Rate (CAR; how often models acknowledge insufficient knowledge on unanswerable questions),
> Answerable Attempt Rate and Answer Accuracy" across 27 LLMs; retrieval and parametric abstention are measured
> jointly, not separately, and the unanswerable class is post-cut-off Minecraft features, not "several
> unanswerable classes".

Proposed corrected Table 7 row:

| DeclineCraft, arXiv:2610.28340 | Minecraft feature-addition unanswerable questions plus corpus cut-off | post-cut-off additions with parametric-exposure audits | Correct Abstention Rate and Answerable Attempt Rate | per model and retrieval condition; no retrieval-feature gate or threshold pair |
