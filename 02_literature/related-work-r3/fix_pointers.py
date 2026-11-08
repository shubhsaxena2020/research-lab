import json

p="02_literature/related-work-r3/table7.json"
obj=json.load(open(p,encoding="utf-8"))
rows=obj["rows"]

# descriptor-only source pointers (file + section), no fabricated quotes
ptr = {
 "This paper (C1 audit)": {
   "work":"05_paper/draft/paper.md section 2 (Related work) lines 108-125",
   "id":"05_paper/draft/paper.md (this paper, unpublished workshop draft)",
   "data":"05_paper/draft/paper.md section 3.1 lines 138-146",
   "metric":"05_paper/draft/paper.md Abstract and section 4.2",
   "negatives":"05_paper/draft/paper.md section 3.1 rung table lines 148-155",
   "operating_point":"04_experiments/config/c1_gate.json; 05_paper/draft/paper.md section 3.3",
   "both_directions":"05_paper/draft/paper.md section 4.2 Table 1"
 },
 "Abdumalikov et al.": {
   "work":"02_literature/NOVELTY-PRESCAN.md section 1 (Family A) and section 6 item 6",
   "id":"02_literature/sources/txt/arxiv-2403.01461.txt header (arXiv:2403.01461v1)",
   "data":"02_literature/NOVELTY-PRESCAN.md section 1 (SQuAD 2.0-style unanswerable pairs)",
   "metric":"02_literature/sources/txt/arxiv-2403.01461.txt lines 26-28",
   "negatives":"02_literature/sources/txt/arxiv-2403.01461.txt lines 20-28",
   "operating_point":"02_literature/NOVELTY-PRESCAN.md section 1 (one accuracy figure per sampler)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (no false-refusal rate per rung)"
 },
 "RINSE (Chen, Hua, Xiao)": {
   "work":"02_literature/NOVELTY-PRESCAN.md section 1 (A1)",
   "id":"02_literature/related-work-r3/raw/arxiv-2609.37469.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2609.37469.html (abstract, six datasets)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2609.37469.html (abstract, score 0.837 vs 0.746)",
   "negatives":"02_literature/related-work-r3/raw/arxiv-2609.37469.html (abstract, substitution/deletion/question-swap)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2609.37469.html (abstract, 36.5 ms per question)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N1 row: no false-refusal column)"
 },
 "GRAB-RAG (Setiawan)": {
   "work":"02_literature/NOVELTY-PRESCAN.md section 1 (A2)",
   "id":"02_literature/related-work-r3/raw/arxiv-2608.22228.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2608.22228.html (abstract, NQ and HotpotQA)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2608.22228.html (abstract, 41.6% misleading answered)",
   "negatives":"02_literature/related-work-r3/raw/arxiv-2608.22228.html (abstract, four context conditions)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2608.22228.html (abstract, five policies, three models)",
   "both_directions":"02_literature/NOVELTY-PRESCAN.md section 1 (A2 row)"
 },
 "DeclineCraft (Thakur, Saparov, Ribeiro)": {
   "work":"02_literature/NOVELTY-PRESCAN.md section 1 (A4)",
   "id":"02_literature/sources/txt/arxiv-2610.28340.txt header (arXiv:2610.28340v1)",
   "data":"02_literature/related-work-r3/raw/openalex-2610.28340.json (abstract reconstruction)",
   "metric":"02_literature/related-work-r3/raw/openalex-2610.28340.json (abstract, CAR and Answerable Attempt Rate)",
   "negatives":"02_literature/related-work-r3/raw/openalex-2610.28340.json (abstract, Minecraft feature additions)",
   "operating_point":"02_literature/related-work-r3/raw/openalex-2610.28340.json (abstract, 38 of 40 configurations)",
   "both_directions":"02_literature/NOVELTY-PRESCAN.md section 6 item 5"
 },
 "Beyond Confidence (Kumar et al.)": {
   "work":"02_literature/NOVELTY-CHECK.md section 3 (N1 row)",
   "id":"02_literature/related-work-r3/raw/arxiv-2502.07255.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2502.07255.html (abstract, CIFAR-100/ImageNet1K/ModelNet40)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2502.07255.html (abstract, AUC 0.993 to 0.995)",
   "negatives":"02_literature/NOVELTY-CHECK.md section 3 (N1 row: no ladder, no false-refusal column)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2502.07255.html (abstract, dual thresholds)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N1 row: no false-refusal column)"
 },
 "Predictable Failure in Multi-Hop Retrieval (Bacellar)": {
   "work":"02_literature/NOVELTY-CHECK.md section 3 (N2 row)",
   "id":"02_literature/related-work-r3/raw/arxiv-2609.22056.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2609.22056.html (abstract, three benchmarks)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2609.22056.html (abstract, CWAR 39.5% to 20.6% at 50% coverage)",
   "negatives":"02_literature/related-work-r3/raw/arxiv-2609.22056.html (abstract, five failure regimes)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2609.22056.html (abstract, RCS abstention policy)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N2 row: one policy, no dead zone, no over-refusal rate)"
 },
 "Sufficiency-Gated RAG (Shishir et al.)": {
   "work":"02_literature/NOVELTY-CHECK.md section 3 (N3 row)",
   "id":"02_literature/related-work-r3/raw/openalex-n3.json (OpenAlex record)",
   "data":"02_literature/related-work-r3/raw/n3.txt (HotpotQA and MuSiQue)",
   "metric":"02_literature/related-work-r3/raw/n3.txt lines 33-35 (17.1% unsupported, 7.0% wrongly refused)",
   "negatives":"02_literature/related-work-r3/raw/openalex-n3.json (abstract, relevance vs sufficiency)",
   "operating_point":"02_literature/related-work-r3/raw/n3.txt lines 406-417 (40th percentile threshold)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N3 row: wrongful refusal of sufficient contexts)"
 },
 "Before Answering (Mondal et al.)": {
   "work":"02_literature/NOVELTY-CHECK.md section 3 (N4 row)",
   "id":"02_literature/related-work-r3/raw/arxiv-2609.32269.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2609.32269.html (abstract, three datasets)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2609.32269.html (abstract, AUROC 0.979 and 0.968/0.983)",
   "negatives":"02_literature/related-work-r3/raw/arxiv-2609.32269.html (abstract, deletion vs size-matched)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2609.32269.html (abstract, error 0.850 to 0.631 at 5% coverage)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N4 row: occupies the separability finding)"
 },
 "Reliable Biomedical RAG (Saha et al.)": {
   "work":"02_literature/NOVELTY-CHECK.md section 3 (N10 row)",
   "id":"02_literature/related-work-r3/raw/openalex-n10.json (OpenAlex record)",
   "data":"02_literature/related-work-r3/raw/openalex-n10.json (abstract, SciFact counts)",
   "metric":"02_literature/related-work-r3/raw/openalex-n10.json (abstract, Recall@5 0.773 and 80.5% accuracy)",
   "negatives":"02_literature/related-work-r3/raw/openalex-n10.json (abstract, hard negatives)",
   "operating_point":"02_literature/NOVELTY-CHECK.md section 3 (N10 row: single operating point)",
   "both_directions":"02_literature/NOVELTY-CHECK.md section 3 (N10 row: answerable and unsupported recall)"
 },
 "Two Axes of LLM Abstention (Wagner)": {
   "work":"02_literature/NOVELTY-PRESCAN.md section 1 (A3)",
   "id":"02_literature/related-work-r3/raw/arxiv-2607.08456.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2607.08456.html (abstract, five models 2B-14B)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2607.08456.html (abstract, probe 0.69 to 0.77 AUROC)",
   "negatives":"02_literature/related-work-r3/raw/arxiv-2607.08456.html (abstract, unanswerable/false-premise)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2607.08456.html (abstract, 0.75 coverage)",
   "both_directions":"02_literature/NOVELTY-PRESCAN.md section 1 (A3 row)"
 },
 "RefusalBench (Muhamed et al.)": {
   "work":"02_literature/NOVELTY-PRESCAN.md section 1 (A5)",
   "id":"02_literature/related-work-r3/raw/arxiv-2510.10390.html (title/abstract)",
   "data":"02_literature/related-work-r3/raw/arxiv-2510.10390.html (abstract, NQ and GaRAGe)",
   "metric":"02_literature/related-work-r3/raw/arxiv-2510.10390.html (abstract, refusal accuracy <50%)",
   "negatives":"02_literature/related-work-r3/raw/arxiv-2510.10390.html (abstract, 176 perturbations)",
   "operating_point":"02_literature/related-work-r3/raw/arxiv-2510.10390.html (abstract, benchmark only)",
   "both_directions":"02_literature/NOVELTY-PRESCAN.md section 1 (A5 row)"
 }
}

# also fix Predictable Failure metric cell value (was wrong)
for r in rows:
    if r["work"].startswith("Predictable Failure"):
        r["metric"] = "CWAR, AUC-AC, ECE (CWAR 39.5% to 20.6% at 50% coverage)"

for r in rows:
    r["source_quotes"] = ptr[r["work"]]

with open(p,"w",encoding="utf-8") as f:
    json.dump(obj,f,indent=2,ensure_ascii=False)
print("updated", len(rows))