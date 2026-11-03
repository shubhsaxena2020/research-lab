# UNAVAILABLE sources — baseline run 2026-11-03

None. All 9 sources cited in `05_paper/draft/paper.md` were obtained (HTTP 200, valid PDF,
sha256 in `fetch_log.jsonl`) and converted; every `.txt` is above 2,000 words, so no source was
a scanned PDF and no OCR was needed.

No text in this corpus was hand-typed or reconstructed from memory.

Two citation-register gaps found while resolving ids (register fix is the lead's call, RULES.md #1;
`verified_citations.csv` was read only, not edited):

- `arXiv:2309.07597` (C-Pack / BGE) is cited inline in the draft but has **no row** in
  `02_literature/verified_citations.csv`.
- `10.18653/v1/2020.coling-main.580` (2WikiMultiHopQA) is cited in the draft (§6 Limitations,
  §7 Ethics) but has **no row** in the register. Its DOI resolves via Crossref to
  "Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps"
  (COLING 2020), and the PDF calls the dataset 2WikiMultiHopQA.
