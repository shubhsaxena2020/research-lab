# Metric definitions (R3-1)

- Abstain precision P(negative | refused): (number of refused items that are negatives) / (number of refused items); per-rung abstain precision restricts negatives to rung k: n_refused_rung_k / (n_refused_rung_k + n_refused_answerable).
- Per-rung refusal rate P(refused | negative of rung k): n_refused_rung_k / n_rung_k (abstain recall on that rung).
- Over-refusal P(refused | answerable): n_refused_answerable / n_answerable.
- Coverage (item population): 1 - mean(refused) over all items = admitted items / all items.
- Coverage (question population): (# qids whose rung-0 item is not refused) / (# qids).
- Abstain recall (pooled): n_refused_negatives / n_negatives.
