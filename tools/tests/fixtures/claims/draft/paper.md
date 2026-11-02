# A Compact Reranker for Public Retrieval Benchmarks

Fixture draft for `tools/tests/test_claims_audit.py`. Synthetic text; not a real paper.

## Abstract

We evaluate a compact cross-encoder reranker on 1,000 held-out public queries. The baseline
reaches 0.812 accuracy; our reranker raises this to 0.865. Across 5 seeds the improvement is
stable, with a Holm-corrected p-value of 0.031. To our knowledge this is the first audit that
binds every abstract claim to a stored result.

## 1 Introduction

Retrieval quality bounds the accuracy of every downstream answer. Prior work reports strong
ranking results on standard benchmarks [@vaswani2017]. We ask whether a smaller reranker can
match a larger one at lower inference cost.

On the same held-out queries the reranker improves accuracy to 0.865, at 14.2 ms mean latency
per query.

## 2 Method

We fine-tune a 6-layer cross-encoder for 3 epochs with a batch size of 64.
