# COMPUTE.md — R3 exploratory P(True) baseline

- **What:** Ollama logprob support verification and run notes for
  `04_experiments/src/r3_exp_ptruth.py`.
- **Endpoint:** `http://127.0.0.1:11434/api/generate` (Ollama 0.40.15).
- **Model:** `qwen2.5:1.5b-instruct` (NOT the paper's pinned reader
  `Qwen/Qwen2.5-0.5B-Instruct`; see disclosure below).
- **Logprob support:** verified. Request body uses `"logprobs": true` and
  `"top_logprobs": 20`; the streamed response includes per-token `logprob` and
  `top_logprobs` entries. `top_logprobs` maximum observed/accepted is 20
  (values above 20 return HTTP 400).
- **Generation settings:** `num_predict=1`, `temperature=0.0`. The first
  generated token's `top_logprobs` contains both `True` and `False`, so
  `P(True) = exp(lp_True)/(exp(lp_True)+exp(lp_False))`.
- **Concurrency:** one request at a time (no batching). Per-request timeout 60s.
- **Heavy lock:** `ops/HEAVY.lock` acquired for the GPU run (released on
  completion).
- **Resume:** by `item_id` in `ptruth_scores.csv` (553 dev items scored).
- **Status:** exploratory / post-hoc, dev-only. Not part of the pre-registered
  gate. Model differs from the paper's Qwen2.5-0.5B-Instruct reader; results
  are not directly comparable to B4.
- **Verified on:** 2026-11-08.