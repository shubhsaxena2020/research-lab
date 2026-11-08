# verify-ids — R3-5 related-work id verification

Generated: 2026-11-08 (local check)
Inputs: `02_literature/related-work-r3/table7.json`, `02_literature/verified_citations.csv`

Endpoints used: arXiv ids via `https://export.arxiv.org/api/query?id_list=...`; DOIs via `https://api.crossref.org/works/<doi>` (Zenodo/DataCite DOIs that 404 on Crossref were additionally checked on Zenodo).

## Resolution results

| # | work | id | resolved title | match | in verified_citations.csv |
|---|------|----|----------------|-------|---------------------------|
| 1 | This paper (C1 audit) | n/a (unpublished workshop draft) | n/a (not resolved; unpublished) | n/a | no (allowed as n/a) |
| 2 | Abdumalikov et al. | arXiv:2403.01461 | Answerability in Retrieval-Augmented Open-Domain Question Answering | yes | yes (exact) |
| 3 | RINSE (Chen, Hua, Xiao) | arXiv:2609.37469 | Relevance Is Not Sufficient Evidence: Detecting Evidence Gaps Before Generation in RAG | yes | yes (exact) |
| 4 | GRAB-RAG (Setiawan) | arXiv:2608.22228 | Prompt-Based Abstention Fails Under Misleading Context: A Controlled Study of Small Frozen RAG Models | yes | yes (exact) |
| 5 | DeclineCraft (Thakur, Saparov, Ribeiro) | arXiv:2610.28340 | DeclineCraft: A RAG Abstention Benchmark for Jointly Measuring Combined Retrieval and Parametric Knowledge | yes | yes (exact) |
| 6 | Beyond Confidence (Kumar et al.) | arXiv:2502.07255 | Beyond Confidence: Adaptive Abstention in Dual-Threshold Conformal Prediction for Autonomous System Perception | yes | no (id not verbatim; same title present under DOI 10.1109/COINS65080.2025.11125785) |
| 7 | Predictable Failure in Multi-Hop Retrieval (Bacellar) | arXiv:2609.22056 | Predictable Failure in Multi-Hop Retrieval: Score-Distributional Confidence Scoring and Abstention | yes | yes (exact) |
| 8 | Sufficiency-Gated RAG (Shishir et al.) | doi:10.32604/cmc.2026.088937 | Sufficiency-Gated Retrieval-Augmented Generation: Reducing Hallucination via Context Adequacy Estimation | yes | no (id has `doi:` prefix; bare DOI 10.32604/cmc.2026.088937 present) |
| 9 | Before Answering (Mondal et al.) | arXiv:2609.32269 | Before Answering: Evidence Sufficiency under Size-Matched Memory Construction | yes | yes (exact) |
| 10 | Reliable Biomedical RAG (Saha et al.) | doi:10.5281/zenodo.20547014 | Crossref: no resolution (HTTP 404). Zenodo record 20547014: Reliable Biomedical RAG with Answerability-Aware Hybrid Retrieval | no (Crossref 404); yes via Zenodo fallback | no (id has `doi:` prefix; bare DOI 10.5281/zenodo.20547014 present) |
| 11 | Two Axes of LLM Abstention (Wagner) | arXiv:2607.08456 | Two Axes of LLM Abstention: Answer Correctness and Question Answerability | yes | yes (exact) |
| 12 | RefusalBench (Muhamed et al.) | arXiv:2510.10390 | RefusalBench: Generative Evaluation of Selective Refusal in Grounded Language Models | yes | yes (exact) |

## Mismatches / notes

- `arXiv:2502.07255` (Beyond Confidence) resolves on arXiv with a matching title, but `verified_citations.csv` stores it under DOI `10.1109/COINS65080.2025.11125785`, not the arXiv id; the id string is absent from the CSV.
- `doi:10.32604/cmc.2026.088937` and `doi:10.5281/zenodo.20547014` use a `doi:` prefix that never appears in `verified_citations.csv` (CSV uses bare DOIs); the bare DOIs are present. Recommend normalizing table7 ids to bare DOI form (or CSV to prefixed form) for consistency.
- `doi:10.5281/zenodo.20547014` does not resolve via the Crossref works endpoint (HTTP 404) because it is a DataCite/Zenodo DOI; it does resolve on Zenodo (record 20547014) with a matching title. The canonical DOI recorded by Zenodo is `10.5281/zenodo.20547015`.
- `n/a (unpublished workshop draft)` is not present in `verified_citations.csv`, which is acceptable per the "or are 'n/a'" rule.

## Summary

- 11 of 12 ids resolve to a real paper with a matching title (10 via the specified endpoints; 1 via Zenodo fallback after Crossref 404).
- 8 of 12 ids appear verbatim in `verified_citations.csv`; 2 DOI ids appear only as bare DOIs (prefix mismatch); 1 arXiv id appears only under a different DOI; `n/a` is allowed.