# Originality check report

- Generated: 2026-11-08T09:11:31Z
- Draft: `05_paper\draft\paper.md` (7410 words)
- Corpus: `02_literature\sources\txt` -- 9 file(s), 102992 words
- Parameters: n=8, min-words=8, context=12 words each side, quote budget=2.00%

## Verdict: **FAIL**

- FAIL: 6 UNQUOTED shared run(s) of >= 8 words
- Hits: 6 total, 6 unquoted (longest 12), 0 quoted (longest 0).

## Quotation audit

- Quoted words: 5 / 7410 = **0.07%** (budget 2.00%)
- Quoted spans: 1; without a citation in the same sentence: 1
- QUOTE FINDING: 1 quoted span(s) without a citation in the same sentence

| # | line | words | cited | text |
|---|------|-------|-------|------|
| Q01 | 479 | 5 | **NO** | "this passage answers the question" |

## Corpus sources

| source | words | hits | longest shared run |
|--------|-------|------|--------------------|
| acl-2020.coling-main.580.txt | 9316 | 1 | 12 (OK) |
| arxiv-1806.03822.txt | 4417 | 0 | 0 (CLEAR) |
| arxiv-1901.04085.txt | 2279 | 0 | 0 (CLEAR) |
| arxiv-2004.04906.txt | 9369 | 1 | 8 (OK) |
| arxiv-2207.05221.txt | 20374 | 0 | 0 (CLEAR) |
| arxiv-2309.07597.txt | 9257 | 2 | 9 (OK) |
| arxiv-2403.01461.txt | 3662 | 2 | 8 (OK) |
| arxiv-2407.18418.txt | 16566 | 0 | 0 (CLEAR) |
| arxiv-2610.28340.txt | 27752 | 0 | 0 (CLEAR) |

## Hits

### H001 -- UNQUOTED, 12 words

- Draft: line 687, sentence 278
- Source: `acl-2020.coling-main.580.txt` line 1, sentence 1
- Shared text: "Constructing a Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps"
- Draft context: ...Unanswerable Questions for SQuAD. arXiv:1806.03822, 2018. - Ho, Nguyen, Sugawara, Aizawa. Constructing a Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps. COLING 2020, DOI 10.18653/v1/2020.coling-main.580; arXiv:2011...
- Source context: ...Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps Xanh Ho♥♣, Anh-Khoa Duong Nguyen♦, Saku Sugawara♣, Akiko Aizawa♥♣ ♥ The Graduate...
- Decide: coincidental technical phrase (fine) / unmarked quotation (MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).

### H002 -- UNQUOTED, 9 words

- Draft: line 694, sentence 291
- Source: `arxiv-2309.07597.txt` line 646, sentence 610
- Shared text: "Dense Passage Retrieval for Open-Domain Question Answering. arXiv"
- Draft context: ...Passage Re-ranking with BERT. arXiv:1901.04085, 2019. - Karpukhin et al. Dense Passage Retrieval for Open-Domain Question Answering. arXiv:2004.04906, 2020. - Kadavath et al. Language Models (Mostly) Know What They...
- Source context: ...Wu, and Haifeng Wang. 2020. RocketQA: An optimized training (2023). approach to dense passage retrieval for open-domain question answering. arXiv preprint arXiv:2010.08191 (2020). [61] Lee Xiong, Chenyan Xiong, Ye Li...
- Decide: coincidental technical phrase (fine) / unmarked quotation (MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).

### H003 -- UNQUOTED, 8 words

- Draft: line 684, sentence 272
- Source: `arxiv-2403.01461.txt` line 1, sentence 1
- Shared text: "Answerability in Retrieval-Augmented Open-Domain Question Answering"
- Draft context: ...in this draft, with the identifier used for verification: - Abdumalikov, Minervini, Kementchedjhieva. Answerability in Retrieval-Augmented Open-Domain Question Answering. arXiv:2403.01461, 2024. - Rajpurkar, Jia, Liang. Know What You Don't Know...
- Source context: ...Answerability in Retrieval-Augmented Open-Domain Question Answering Rustam Abdumalikov Pasquale Minervini Yova Kementchedjhieva University of Copenhagen University of Tartu...
- Decide: coincidental technical phrase (fine) / unmarked quotation (MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).

### H004 -- UNQUOTED, 8 words

- Draft: line 692, sentence 285
- Source: `arxiv-2309.07597.txt` line 1, sentence 1
- Shared text: "C-Pack: Packed Resources for General Chinese Embeddings"
- Draft context: ...retrieval and parametric abstention benchmark. arXiv:2610.28340, 2026. - Xiao et al. C-Pack: Packed Resources for General Chinese Embeddings. arXiv:2309.07597, 2023. - Nogueira, Cho. Passage Re-ranking with BERT. arXiv...
- Source context: ...C-Pack: Packed Resources For General Chinese Embeddings Shitao Xiao† Zheng Liu†∗ Peitian Zhang stxiao@baai.ac.cn zhengliu1026@gmail...
- Decide: coincidental technical phrase (fine) / unmarked quotation (MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).

### H005 -- UNQUOTED, 8 words

- Draft: line 694, sentence 291
- Source: `arxiv-2004.04906.txt` line 1, sentence 1
- Shared text: "Dense Passage Retrieval for Open-Domain Question Answering"
- Draft context: ...Passage Re-ranking with BERT. arXiv:1901.04085, 2019. - Karpukhin et al. Dense Passage Retrieval for Open-Domain Question Answering. arXiv:2004.04906, 2020. - Kadavath et al. Language Models (Mostly) Know What...
- Source context: ...Dense Passage Retrieval for Open-Domain Question Answering Vladimir Karpukhin∗, Barlas Og˘uz,∗ Sewon Min†, Patrick Lewis, Ledell Wu, Sergey...
- Decide: coincidental technical phrase (fine) / unmarked quotation (MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).

### H006 -- UNQUOTED, 8 words

- Draft: line 694, sentence 291
- Source: `arxiv-2403.01461.txt` line 258, sentence 160
- Shared text: "Dense Passage Retrieval for Open-Domain Question Answering"
- Draft context: ...Passage Re-ranking with BERT. arXiv:1901.04085, 2019. - Karpukhin et al. Dense Passage Retrieval for Open-Domain Question Answering. arXiv:2004.04906, 2020. - Kadavath et al. Language Models (Mostly) Know What...
- Source context: ...Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. Dense passage retrieval for open- domain question answering. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language...
- Decide: coincidental technical phrase (fine) / unmarked quotation (MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).

## Caveat

Not a plagiarism detector. A PASS means no shared run of >= 8 words outside quotation marks was found in THIS corpus, which contains only the sources we consulted. It does not prove originality and does not check the web.
