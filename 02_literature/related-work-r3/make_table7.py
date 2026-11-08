import json

rows = []

def add(work, idv, data, metric, negatives, op, both, quotes):
    rows.append({"work":work,"id":idv,"data":data,"metric":metric,"negatives":negatives,
                 "operating_point":op,"both_directions":both,"source_quotes":quotes})

add("This paper (C1 audit)","n/a (unpublished workshop draft)",
 "SQuAD v2.0 dev, article-disjoint split (35 articles, 1204 paragraphs)",
 "abstain precision, over-refusal, coverage",
 "four constructed rungs R1-R4, plus overlap-matched (R5) and top-1-presented variants",
 "two dev-fitted thresholds on six retrieval features with a dead zone between them; every precision reported beside over-refusal and coverage",
 "yes",
 {"work":"05_paper/draft/paper.md section 2 Table 7 lines 127-133",
  "data":"05_paper/draft/paper.md section 3.1 lines 138-146",
  "metric":"05_paper/draft/paper.md Abstract and section 4.2",
  "negatives":"05_paper/draft/paper.md section 3.1 rung table lines 148-155",
  "operating_point":"04_experiments/config/c1_gate.json; 05_paper/draft/paper.md section 3.3",
  "both_directions":"05_paper/draft/paper.md section 4.2 Table 1"})

add("Abdumalikov et al.","arXiv:2403.01461",
 "ODQA corpora; SQuAD v2.0 unanswerable pairs used for repair",
 "answerability accuracy",
 "random text excerpts vs excerpts with high semantic overlap",
 "one accuracy figure per sampler; coverage not reported",
 "no",
 {"work":"02_literature/NOVELTY-PRESCAN.md section 1 and section 6 item 6",
  "id":"02_literature/sources/txt/arxiv-2403.01461.txt header (arXiv:2403.01461v1)",
  "data":"02_literature/NOVELTY-PRESCAN.md section 1 (SQuAD 2.0-style unanswerable pairs restore it to near 100%)",
  "metric":"02_literature/sources/txt/arxiv-2403.01461.txt lines 26-28 (decrease in predictive accuracy, from 98% to 1%)",
  "negatives":"02_literature/sources/txt/arxiv-2403.01461.txt lines 20-28 (random text excerpts vs high semantic overlap)",
  "operating_point":"02_literature/NOVELTY-PRESCAN.md section 1 (one accuracy figure per sampler)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (no per-rung false-refusal rate reported)"})

add("RINSE (Chen, Hua, Xiao)","arXiv:2609.37469",
 "six ODQA datasets with paired sufficient/insufficient evidence",
 "sufficiency score (0.837 vs 0.746 best of 10)",
 "substitution, deletion and question-swap constructions controlling surface features",
 "single score; 36.5 ms per question; no coverage or false-refusal column",
 "no",
 {"work":"02_literature/NOVELTY-PRESCAN.md section 1 (A1)",
  "id":"02_literature/related-work-r3/raw/arxiv-2609.37469.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2609.37469.html abstract (Across six datasets)",
  "metric":"02_literature/related-work-r3/raw/arxiv-2609.37469.html abstract (score of 0.837 (chance 0.5), exceeding best of 10 prior methods (0.746))",
  "negatives":"02_literature/related-work-r3/raw/arxiv-2609.37469.html abstract (substitution, deletion, and question-swap constructions)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2609.37469.html abstract (36.5 ms per question on a single GPU)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (no false-refusal rate per rung)"})

add("GRAB-RAG (Setiawan)","arXiv:2608.22228",
 "Natural Questions and HotpotQA",
 "abstention/answer rate on misleading questions (41.6% answered)",
 "four context conditions: supportive, degraded, missing, misleading",
 "prompt-based; no threshold or coverage table reported",
 "partial",
 {"work":"02_literature/NOVELTY-PRESCAN.md section 1 (A2)",
  "id":"02_literature/related-work-r3/raw/arxiv-2608.22228.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2608.22228.html abstract (Natural Questions and HotpotQA)",
  "metric":"02_literature/related-work-r3/raw/arxiv-2608.22228.html abstract (still answer 41.6% of misleading questions)",
  "negatives":"02_literature/related-work-r3/raw/arxiv-2608.22228.html abstract (supportive, degraded, missing, and misleading)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2608.22228.html abstract (five abstention policies on three small frozen models)",
  "both_directions":"02_literature/NOVELTY-PRESCAN.md section 1 (abstains on missing; answers 41.6% of misleading; no false-refusal rate on answerable)"})

add("DeclineCraft (Thakur, Saparov, Ribeiro)","arXiv:2610.28340",
 "Minecraft feature-addition unanswerable questions plus corpus cut-off",
 "Correct Abstention Rate (CAR) and Answerable Attempt Rate",
 "unanswerable questions targeting post-cut-off additions, with parametric-exposure audits",
 "per model and retrieval condition; no feature gate or threshold pair",
 "yes",
 {"work":"02_literature/NOVELTY-PRESCAN.md section 1 (A4)",
  "id":"02_literature/sources/txt/arxiv-2610.28340.txt header (arXiv:2610.28340v1)",
  "data":"02_literature/related-work-r3/raw/openalex (abstract reconstruction, W7223089569)",
  "metric":"02_literature/related-work-r3/raw/openalex (abstract): Correct Abstention Rate (CAR; how often models acknowledge insufficient knowledge on unanswerable questions), Answerable Attempt Rate and Answer Accuracy",
  "negatives":"02_literature/related-work-r3/raw/openalex (abstract): dynamic abstention benchmark whose unanswerable questions target Minecraft feature additions after a corpus cut-off, with audits of possible parametric exposure",
  "operating_point":"02_literature/related-work-r3/raw/openalex (abstract): single-shot retrieval significantly raises CAR in 38 of 40 configurations",
  "both_directions":"02_literature/NOVELTY-PRESCAN.md section 6 item 5 (Reports abstention on unanswerable items and answerable attempt rate together)"})

add("Beyond Confidence (Kumar et al.)","arXiv:2502.07255",
 "CIFAR-100, ImageNet1K, ModelNet40 (camera and LiDAR perception)",
 "detection AUC 0.993-0.995, coverage >90%, abstention 13.5-63.4%",
 "environmental perturbations in perception (not text negatives)",
 "dual conformal threshold plus abstention threshold; adaptive abstention as severity increases",
 "no",
 {"work":"02_literature/NOVELTY-CHECK.md section 3 (N1)",
  "id":"02_literature/related-work-r3/raw/arxiv-2502.07255.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2502.07255.html abstract (CIFAR-100, ImageNet1K, and ModelNet40)",
  "metric":"02_literature/related-work-r3/raw/arxiv-2502.07255.html abstract (AUC: 0.993 to 0.995; coverage (>90.0%); adaptive abstention (13.5% to 63.4%))",
  "negatives":"02_literature/NOVELTY-CHECK.md section 3 (N1: no ladder, no false-refusal column)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2502.07255.html abstract (conformal threshold ... abstention threshold optimized through ROC analysis)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N1: no false-refusal column)"})

add("Predictable Failure in Multi-Hop Retrieval (Bacellar)","arXiv:2609.22056",
 "MuSiQue, 2WikiMultiHopQA, HoVer",
 "CWAR, AUC-AC, ECE",
 "five failure regimes (query length, hop-1 concentration, etc.)",
 "RCS logistic on up to nine retrieval features; abstention at fixed coverage (50%)",
 "no",
 {"work":"02_literature/NOVELTY-CHECK.md section 3 (N2)",
  "id":"02_literature/related-work-r3/raw/arxiv-2609.22056.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2609.22056.html abstract (MuSiQue, 2WikiMultiHopQA, HoVer)",
  "metric":"02_literature/related-work-r3/raw/arxiv-2609.22056.html abstract (CWAR from 14.5% to 62.1%; ECE=0.035)",
  "negatives":"02_literature/related-work-r3/raw/arxiv-2609.22056.html abstract (five failure regimes)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2609.22056.html abstract (abstention policy; 50% coverage)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N2: one policy, no dead zone, no over-refusal rate)"})

add("Sufficiency-Gated RAG (Shishir et al.)","doi:10.32604/cmc.2026.088937",
 "HotpotQA and MuSiQue",
 "unsupported rate (17.1% at 57.2% coverage) and wrongful refusal of sufficient contexts (7.0%)",
 "retrieved passages (sufficiency vs relevance)",
 "single calibrated operating point (cross-encoder, 40th percentile threshold)",
 "yes",
 {"work":"02_literature/NOVELTY-CHECK.md section 3 (N3)",
  "id":"02_literature/related-work-r3/raw/openalex-n3.json (OpenAlex record)",
  "data":"02_literature/related-work-r3/raw/n3.txt (HotpotQA/MuSiQue evaluation)",
  "metric":"02_literature/related-work-r3/raw/n3.txt lines 33-35 (17.1% unsupported at 57.2% coverage, with 7.0% of sufficient contexts wrongly refused)",
  "negatives":"02_literature/related-work-r3/raw/openalex-n3.json abstract (Relevance, however, does not imply sufficiency)",
  "operating_point":"02_literature/related-work-r3/raw/n3.txt lines 406-417 (threshold is the 40th percentile of that distribution)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N3: reporting wrongful refusal of sufficient contexts (7.0%) -- one half of the false-refusal column)"})

add("Before Answering (Mondal et al.)","arXiv:2609.32269",
 "MuSiQue, HotpotQA, 2WikiMultiHopQA",
 "AUROC for unsafe-memory detection (0.979 surface shortcut; 0.968/0.983 MemSafe)",
 "size-matched memory construction vs deletion leak",
 "none (detection AUROC; gate reduces error 0.850 to 0.631 at 5% coverage)",
 "no",
 {"work":"02_literature/NOVELTY-CHECK.md section 3 (N4)",
  "id":"02_literature/related-work-r3/raw/arxiv-2609.32269.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2609.32269.html abstract (MuSiQue, HotpotQA, 2WikiMultiHopQA)",
  "metric":"02_literature/related-work-r3/raw/arxiv-2609.32269.html abstract (AUROC of 0.979; 0.968 and 0.983 AUROC)",
  "negatives":"02_literature/related-work-r3/raw/arxiv-2609.32269.html abstract (deleting supporting passages vs size-matched construction)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2609.32269.html abstract (reduces the error rate from 0.850 to 0.631 at 5% coverage)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N4: occupies the separability finding; no per-rung false-refusal rate)"})

add("Reliable Biomedical RAG (Saha et al.)","doi:10.5281/zenodo.20547014",
 "SciFact (5,183 abstracts, 6,241 passages, 1,109 queries)",
 "Recall@5/10; answerability accuracy 80.5% (97.5% recall answerable, 64.3% unsupported)",
 "out-of-domain and domain-similar hard negatives",
 "single answerability gate; no threshold pair or dead zone",
 "yes",
 {"work":"02_literature/NOVELTY-CHECK.md section 3 (N10)",
  "id":"02_literature/related-work-r3/raw/openalex-n10.json (OpenAlex record)",
  "data":"02_literature/related-work-r3/raw/openalex-n10.json abstract (5,183 scientific abstracts; 1,109 SciFact queries)",
  "metric":"02_literature/related-work-r3/raw/openalex-n10.json abstract (Recall@5 to 0.773; answerability classifier reaches 80.5% validation accuracy, with 97.5% recall on answerable queries and 64.3% recall on unsupported queries)",
  "negatives":"02_literature/related-work-r3/raw/openalex-n10.json abstract (out-of-domain and domain-similar hard negatives)",
  "operating_point":"02_literature/NOVELTY-CHECK.md section 3 (N10: single operating point)",
  "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N10: reports both answerable and unsupported recall)"})

add("Two Axes of LLM Abstention (Wagner)","arXiv:2607.08456",
 "five instruction-tuned models, 2B-14B",
 "AUROC hidden-state probe 0.69-0.77; certified budgets at 0.75 coverage",
 "unanswerable and false-premise questions",
 "two separate thresholds (correctness score and answerability score), not retrieval features",
 "yes",
 {"work":"02_literature/NOVELTY-PRESCAN.md section 1 (A3)",
  "id":"02_literature/related-work-r3/raw/arxiv-2607.08456.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2607.08456.html abstract (five instruction-tuned models from three families (2B to 14B))",
  "metric":"02_literature/related-work-r3/raw/arxiv-2607.08456.html abstract (hidden-state probe reaches 0.69 to 0.77 AUROC)",
  "negatives":"02_literature/related-work-r3/raw/arxiv-2607.08456.html abstract (unanswerable ones or ones resting on a false premise)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2607.08456.html abstract (two axes into a calibrated policy ... 0.75 coverage of correct answers)",
  "both_directions":"02_literature/NOVELTY-PRESCAN.md section 1 (A3: Two-sided argument plus calibrated two-score policy)"})

add("RefusalBench (Muhamed et al.)","arXiv:2510.10390",
 "NQ (single doc) and GaRAGe (multi-doc)",
 "refusal accuracy (<50% on multi-document tasks)",
 "176 perturbation strategies across six uncertainty categories at three intensities",
 "benchmark only; no operating point",
 "no",
 {"work":"02_literature/NOVELTY-PRESCAN.md section 1 (A5)",
  "id":"02_literature/related-work-r3/raw/arxiv-2510.10390.html (title/abstract)",
  "data":"02_literature/related-work-r3/raw/arxiv-2510.10390.html abstract (RefusalBench-NQ (single document) and RefusalBench-GaRAGe (multi-document))",
  "metric":"02_literature/related-work-r3/raw/arxiv-2510.10390.html abstract (refusal accuracy dropping below 50% on multi-document tasks)",
  "negatives":"02_literature/related-work-r3/raw/arxiv-2510.10390.html abstract (176 distinct perturbation strategies across six categories ... three intensity levels)",
  "operating_point":"02_literature/related-work-r3/raw/arxiv-2510.10390.html abstract (benchmark only)",
  "both_directions":"02_literature/NOVELTY-PRESCAN.md section 1 (A5: stronger ladder but no two-sided reporting)"})

obj = {"schema":"related-work-r3/table7 v1","generated":"2026-11-08","rows":rows}
with open("02_literature/related-work-r3/table7.json","w",encoding="utf-8") as f:
    json.dump(obj,f,indent=2,ensure_ascii=False)
print("rows", len(rows))