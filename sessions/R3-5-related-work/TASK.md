# TASK R3-5 — related work & novelty refresh (LAPTOP 2, profile res-s5)

You run on laptop 2 in a COPY of the repo at `C:\Users\admin\research-lab` (wherever RULES.md/COMMON.md say
`C:\Users\shubh\research-lab`, read `C:\Users\admin\research-lab`). The head copies your OWNED folder back to the main laptop.
Python here: `C:\Users\admin\AppData\Local\hermes\tools\python-3.14.9+20261021-win32-x64\python.exe` (or `python` inside
Hermes; no torch — none needed).

Goal: answer MF-23 and MF-28 and satisfy HEAD-REVIEW condition 1 (novelty re-check beyond arXiv).

OWNED: `02_literature/related-work-r3/**` and `sessions/R3-5-related-work/**` only. Everything else read-only.

Deliverables
1. From `02_literature/NOVELTY-CHECK.md`, `NOVELTY-PRESCAN.md`, `GAP-MINING.md`, `deep_dives/`: list the five nearest
   neighbours the project's own search marked closest (incl. RINSE, GRAB-RAG, DeclineCraft and the work that occupies the
   separability finding). For each: verified id (resolve DOI/arXiv/OpenAlex by a real API call; title must match), data,
   metric, negative construction, operating point reported, both-direction reporting yes/no — quoted evidence with page or
   section from the source text (sources are in `02_literature/sources/txt/` where available; fetch the abstract/PDF text
   politely otherwise and cache it in `02_literature/related-work-r3/raw/`).
2. MF-28: re-read DeclineCraft and write the correct one-line characterisation with a quote.
3. `related-work-r3/table7.json` — machine-readable Table 7 rows (this paper + the >= 7 works), every cell with a source
   pointer (file + quote or section). Schema: {"rows":[{"work","id","data","metric","negatives","operating_point",
   "both_directions","source_quotes":{...}}]}. The integrator generates the table from it (MF-36).
4. Novelty refresh: OpenAlex + Crossref + Semantic Scholar (if it answers; it refused before — record refusals) with >= 15
   slice-wording queries per the HEAD-REVIEW condition 1 (gate on retrieval features + two thresholds + both directions per
   rung). Log every query, index, date, hit count, and every candidate collision checked, to `related-work-r3/NOVELTY-R3.md`,
   with a verdict: still "incremental", or "C1 is dead" (if a paper fits two thresholds on retrieval features AND reports both
   directions per rung). Verified new citations go to `related-work-r3/new_citations.csv` in the verified_citations.csv schema.
5. `related-work-r3/ANSWERS.md` — per MF item: verdict, evidence, proposed related-work paragraph text (own words, no pasted
   paper text, quotes marked and cited).
Batches of >= 3 subagents: e.g. one per neighbour paper, one per index for the novelty queries, one reviewer re-checking
previous batch's ids and quotes.
