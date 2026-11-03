# B4 reader-confidence — run notes (2026-11-03)

**Status: PARTIAL COVERAGE. 553 of 3,752 items scored (all dev). Not a result for the paper — this is
the feature-extraction run for baseline B4, which `PREREGISTRATION.md` §5 defines as a single
threshold on `reader_mean_logprob`.**

Artifacts (all under `C:\Users\shubh\research-lab\04_experiments\`):

| file | contents |
|---|---|
| `src/reader_logprob.py` | extractor (CLI, resume, time budget, errors file, meta) |
| `src/tests/test_reader_logprob.py` | 19 tests, no model loaded, 2.6 s |
| `data/reader_features.csv` | `item_id,reader_answer,reader_mean_logprob,reader_n_tokens` — 553 rows |
| `data/reader_meta.json` | model, dtype, device, items/sec, wall time, RAM, command (1800 s run) |
| `data/reader_meta_resume_check.json` | meta of the 1-item resume check |
| `data/reader_errors.csv` | not created: 0 item failures |

## What was run

    python 04_experiments/src/reader_logprob.py --batch-size 8 --threads 13 --time-budget 1800 --ignore-stop

Model `Qwen/Qwen2.5-0.5B-Instruct`, fp32, CPU, 494.0M params, greedy, ≤16 new tokens, batch 8.
Load 9.0 s. Generation wall **1924.9 s (32.1 min, last batch overran the 1800 s check)**, 552 items,
**0.287 items/s**, 0 errors, 0 items with an undefined log-probability.

The resume check (`--limit 1`) read the existing file, reported `already_scored=552 todo=3200`, scored
the one remaining item and appended it → 553 rows. Resume is exercised end-to-end, not just unit-tested.

### Throughput caveat (why coverage is 15 %)

Rate fell from 1.10 items/s to 0.36 items/s inside the run while an unrelated process
(`work/EVAL-FINAL/latency_decomp.py`, pid 21500) held ≈8.4 of 14 logical cores at 841 % CPU. Per
RULES #9 nothing outside the repo was touched. At the uncontended rate (~1.0 items/s, measured on 64-item
probes: batch 8/13 threads 1.00, batch 16/8 threads 1.09, bf16 no gain) the full 3,752 items need
≈60 min — twice the 30-minute cap, so full coverage needs a second window:

    python 04_experiments/src/reader_logprob.py --batch-size 8 --threads 13 --time-budget 1800 --ignore-stop

It resumes automatically (skip by `item_id`) and appends+fsyncs per batch.

## Measurements actually observed (dev only, 118 questions × 5 rungs)

| rung | n | mean logprob | median | refuses (`NOT_ANSWERABLE`) |
|---|---|---|---|---|
| 0 answerable | 118 | −0.204 | −0.154 | 15 % |
| 1 random | 118 | −0.094 | −0.036 | 91 % |
| 2 same-entity | 81 | −0.131 | −0.060 | 79 % |
| 3 near-miss | 118 | −0.153 | −0.092 | 79 % |
| 4 premise violation | 118 | −0.273 | −0.199 | 19 % |

Descriptive AUROC of `reader_mean_logprob` as an **abstain** score (rung-0 vs that rung; >0.5 = the
reader is less confident on that rung's passages than on gold ones):

| rung | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| abstain AUROC | 0.725 | 0.632 | 0.589 | 0.394 |

## Two findings the gate stage must handle (both reproducible from the CSV above)

1. **The refusal string contaminates the score.** `NOT_ANSWERABLE` is 5 tokens the model emits at
   p≈0.98, so a *confident refusal* scores ≈ −0.02 while a *correct short answer* scores ≈ −0.2.
   Mean logprob therefore measures how sure the model is of whichever string it produced, not whether
   the passage supports it: rung 1 (easiest to detect) gets the *highest* confidence of any rung,
   rung 0 sits below rungs 1–2, and rung 4 (hardest: 19 % refused, i.e. 81 % confidently wrong) has the
   lowest. A one-sided `admit iff s ≥ t` rule on this score refuses answerable items more than random
   negatives at the low end. This is a property of the pre-registered B4 definition, so it is reported,
   not patched: B4 is expected to underperform, and H1's "abstain precision" for B4 may be non-monotone.
2. **The refusal indicator is a much stronger signal than the confidence value** (rung 1: 91 % refusal
   vs rung 0: 15 %), but it is a *different* baseline — it is answer-string matching, not
   `reader_mean_logprob`. If the head wants it, it needs its own line in the pre-registration; it must
   not be folded into B4 after the freeze.

## Verification performed

* `python -m pytest 04_experiments/src/tests/test_reader_logprob.py -q` → **19 passed in 2.60 s**.
* 5-item real run printed 5 rows, answers plausible, logprobs finite and ≤ 0
  (e.g. `dev:56e16839cd28a01900c6788a:r0,number of gates,-0.166025,4`).
* Batch invariance: same 5 items at `--batch-size 1` vs `--batch-size 5` → identical answer strings,
  |Δ mean logprob| ≤ 1.1e-5 (fp32 noise). Batching is throughput only.
* 553 rows: 553 unique ids, 0 unknown ids, 0 nan/empty logprob, all ≤ 0, `reader_n_tokens` ∈ [2, 16],
  0 empty answers, all dev split.
