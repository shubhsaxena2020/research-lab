# Corpus manifest — originality baseline 2026-11-03

Sources the draft `05_paper/draft/paper.md` cites, fetched from the publisher, converted with
`pdftotext -layout -nopgbrk -enc UTF-8`, de-hyphenated once, and kept in `txt/`. This directory
is the corpus for `tools/originality_check.py`. Rebuild notes at the bottom.

| # | file stem | id | title (as printed in the PDF) | bytes | words |
|---|-----------|----|-------------------------------|-------|-------|
| 1 | arxiv-2403.01461 | arXiv:2403.01461 | Answerability in Retrieval-Augmented Open-Domain Question Answering | 155,238 | 3,545 |
| 2 | arxiv-1806.03822 | arXiv:1806.03822 | Know What You Don't Know: Unanswerable Questions for SQuAD | 916,105 | 4,218 |
| 3 | arxiv-2407.18418 | arXiv:2407.18418 | Know Your Limits: A Survey of Abstention in Large Language Models | 740,481 | 16,039 |
| 4 | arxiv-2610.28340 | arXiv:2610.28340 | DeclineCraft: A RAG Abstention Benchmark for Jointly Measuring Combined Retrieval and Parametric Knowledge | 1,301,621 | 25,334 |
| 5 | arxiv-2309.07597 | arXiv:2309.07597 | C-Pack: Packed Resources For General Chinese Embeddings | 1,332,241 | 8,390 |
| 6 | arxiv-1901.04085 | arXiv:1901.04085 | Passage Re-ranking with BERT | 179,659 | 2,093 |
| 7 | arxiv-2004.04906 | arXiv:2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | 383,508 | 8,870 |
| 8 | arxiv-2207.05221 | arXiv:2207.05221 | Language Models (Mostly) Know What They Know | 2,616,253 | 18,802 |
| 9 | acl-2020.coling-main.580 | 10.18653/v1/2020.coling-main.580 | Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps (2WikiMultiHopQA) | 639,331 | 8,933 |

9 files, 8,264,437 bytes (7.88 MB), 96,224 words (whitespace-split; the checker reports 102,992
tokens because it splits on hyphens and NBSP).

Every request is logged in `fetch_log.jsonl` (`ts`, `url`, `status`, `bytes`, `sha256`, `file`,
`attempt`), one line per attempt; sha256 is over the saved PDF. Machine-readable copy of this
table: `corpus_manifest.json`. Fetcher: `fetch.py` (User-Agent
`research-lab-acquisition/1.0 (mailto:shubh.saxena2020@gmail.com)`, >=2 s between requests,
one retry after 20 s, caps 10 files / 80 MB).

No file fell under 500 words, so no scanned-PDF (OCR) problem: `UNAVAILABLE.md` records that
nothing was missing.

## Rebuild

```bash
cd /c/Users/shubh/research-lab
python 02_literature/sources/fetch.py          # idempotent: skips existing PDFs, appends to fetch_log.jsonl
for pdf in 02_literature/sources/*.pdf; do
  base=$(basename "$pdf" .pdf)
  pdftotext -layout -nopgbrk -enc UTF-8 "$pdf" "02_literature/sources/txt/$base.txt"
done
perl -0pi -e 's/(\w)-\n(\w)/$1$2/g' 02_literature/sources/txt/*.txt
```

`arxiv-2309.07597.txt` is not strict UTF-8 out of Xpdf (252 invalid byte sequences from the
Type-1 font warnings); it was rewritten once with `errors='replace'`. Text files are otherwise
byte-for-byte `pdftotext` output.

## Add a source

Drop the PDF in this directory as `arxiv-<id>.pdf` / `acl-<id>.pdf`, extract to `txt/` with the
command above, run the perl de-hyphenation pass, append a row to this table, and re-run the check.
Corpus line numbers in the report are `.txt` line numbers, not PDF pages.

## Corpus scope (honest limits)

Only the nine sources the draft cites in prose are here. Anything read but not archived, the
SQuAD 2.0 dataset itself (JSON, not a paper), and `bm25s` documentation are *not* in the corpus,
so overlap with them is invisible to the checker.
