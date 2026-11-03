# Originality check report

- Generated: 2026-11-03T01:04:03Z
- Draft: `05_paper\draft\paper.md` (2668 words)
- Corpus: `02_literature\sources\txt` -- 9 file(s), 102992 words
- Parameters: n=8, min-words=8, context=12 words each side, quote budget=2.00%

## Verdict: **PASS**

- No UNQUOTED shared run of 8+ words found in this corpus.
- Hits: 0 total, 0 unquoted (longest 0), 0 quoted (longest 0).

## Quotation audit

- Quoted words: 30 / 2668 = **1.12%** (budget 2.00%)
- Quoted spans: 8; without a citation in the same sentence: 8
- QUOTE FINDING: 8 quoted span(s) without a citation in the same sentence

| # | line | words | cited | text |
|---|------|-------|-------|------|
| Q01 | 63 | 4 | **NO** | "this rung is hard" |
| Q02 | 63 | 6 | **NO** | "this rung is identifiable from formatting" |
| Q03 | 185 | 2 | **NO** | "it transfers" |
| Q04 | 229 | 4 | **NO** | "abstain precision 0.98" |
| Q05 | 247 | 5 | **NO** | "is this the retrieved passage" |
| Q06 | 250 | 2 | **NO** | "premise violation" |
| Q07 | 251 | 2 | **NO** | "answer absent" |
| Q08 | 258 | 5 | **NO** | "retrieval found the gold paragraph" |

## Corpus sources

| source | words | hits | longest shared run |
|--------|-------|------|--------------------|
| acl-2020.coling-main.580.txt | 9316 | 0 | 0 (CLEAR) |
| arxiv-1806.03822.txt | 4417 | 0 | 0 (CLEAR) |
| arxiv-1901.04085.txt | 2279 | 0 | 0 (CLEAR) |
| arxiv-2004.04906.txt | 9369 | 0 | 0 (CLEAR) |
| arxiv-2207.05221.txt | 20374 | 0 | 0 (CLEAR) |
| arxiv-2309.07597.txt | 9257 | 0 | 0 (CLEAR) |
| arxiv-2403.01461.txt | 3662 | 0 | 0 (CLEAR) |
| arxiv-2407.18418.txt | 16566 | 0 | 0 (CLEAR) |
| arxiv-2610.28340.txt | 27752 | 0 | 0 (CLEAR) |

## Hits

None. Nothing in this corpus shares a run of 8+ consecutive words with the draft.

## Caveat

Not a plagiarism detector. A PASS means no shared run of >= 8 words outside quotation marks was found in THIS corpus, which contains only the sources we consulted. It does not prove originality and does not check the web.

---

# Run record and provenance (baseline 2026-11-03)

Not a classification. This run is the *baseline reading* taken before the draft is rewritten;
no hit was classified and no prose was edited (RULES.md #3 gate is the lead's call).

## Command and result

```
python tools/originality_check.py --draft 05_paper/draft/paper.md \
  --corpus 02_literature/sources/txt --n 8 --min-words 8 \
  --out 06_review/originality-20261103-baseline.md     # exit 0
python tools/originality_check.py ... --json           # 06_review/originality-20261103-baseline.json
```

- verdict line: `verdict: PASS  hits=0 unquoted=0 quoted=0 longest_unquoted=0`
- quoted words: 30/2668 = **1.12%** of budget 2.00%; uncited quoted spans: **8**
- `--strict-quotes` exits **1** on those 8 spans (see Quotation audit above). The four pass
  criteria in ORIGINALITY.md therefore do **not** all hold, even though the n-gram criterion does.

## Corpus

9 sources, 7.88 MB, 102,992 checker tokens — the nine works the draft cites in prose. Manifest,
per-file word counts, sha256 and rebuild instructions: `02_literature/sources/CORPUS.md`
(machine-readable: `corpus_manifest.json`; every request: `fetch_log.jsonl`). Nothing was
UNAVAILABLE (`02_literature/sources/UNAVAILABLE.md`).

## The zero is a real zero, not a broken run

A control draft was built in scratch (`ctrl.md` = this draft plus one 18-word run copied verbatim
from `arxiv-2403.01461.txt` inserted after `## Abstract`) and checked with the same parameters:

```
H001 UNQUOTED  18w draft:9 <- arxiv-2403.01461.txt:15      verdict: FAIL hits=1 unquoted=1
```

The tool detects an injected run of that length at the corpus size used here, so `hits=0` on
`05_paper/draft/paper.md` means no 8-word run is shared with these nine texts. (A second control
that appended the same phrase *after* `## References` produced no hit — the References section is
stripped to end-of-file, as documented. Anything appended at the end of the draft is invisible.)

## Title-vs-claim check (each id resolved, then its PDF read)

| cited | resolves to | draft claims | verdict |
|---|---|---|---|
| 2403.01461 | Answerability in Retrieval-Augmented Open-Domain Question Answering | "98%-to-1% collapse across negative samplers", random vs high-overlap negatives | **matches** — abstract: "from 98% to 1%" on excerpts "with high semantic overlap" |
| 1806.03822 | Know What You Don't Know: Unanswerable Questions for SQuAD | SQuAD 2.0 dev pool | **matches** (SQuAD 2.0 dataset paper) |
| 2407.18418 | Know Your Limits: A Survey of Abstention in LLMs | "separate refusal-because-unsupported from refusal-because-uncertain" | **matches loosely** — the framework is query answerability / model confidence / human values (§1 contributions), not the words "unsupported/uncertain"; defensible gloss, wording could be tightened |
| 2610.28340 | DeclineCraft: ... Jointly Measuring Combined Retrieval and Parametric Knowledge | "measures retrieval and parametric abstention jointly" | **matches** |
| 2309.07597 | C-Pack: Packed Resources For General **Chinese** Embeddings | "`bge-small-en-v1.5` [2309.07597]" | **partial mismatch** — paper documents the BGE family (small 24M / base / large) and C-MTEB, all Chinese; the English `-en-v1.5` variant is not described there |
| 1901.04085 | Passage Re-ranking with BERT | "cross-encoder reranking with a **MiniLM** passage reranker [1901.04085]" | **mismatch** — the paper is a BERT-base/large cross-encoder on MS MARCO + TREC-CAR; the string "MiniLM" does not occur in it (0 hits). Right architecture, wrong model family |
| 2004.04906 | Dense Passage Retrieval for ODQA | dense retrieval baseline | **matches** |
| 2207.05221 | Language Models (Mostly) Know What They Know | "asking the reader for its own **answer-token probability**" | **mismatch (method)** — the paper's instrument is P(True), a probability elicited *after* an answer is proposed, not the answer-token probability; §5.2 of the draft in fact ran `mean generated-token log-probability`, which is neither |
| 10.18653/v1/2020.coling-main.580 | Constructing A Multi-hop QA Dataset ... (2WikiMultiHopQA), COLING 2020 | 2WikiMultihopQA dev, no article grouping | **matches** — DOI resolves via Crossref; the PDF names the dataset 2WikiMultiHopQA |

Register gaps (for the lead, `verified_citations.csv` was not edited): 2309.07597 and
2020.coling-main.580 are cited in the draft but have no row in the register.

## What this run cannot say

Corpus = these nine PDFs only. The SQuAD 2.0 data files, `bm25s` docs, and anything read but not
archived are outside it. No paraphrase, structure, idea or figure reuse is measured. A PASS here
is one narrow checkable claim, not a finding of originality.
