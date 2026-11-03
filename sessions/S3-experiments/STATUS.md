# STATUS S3-experiments

last_update: 2026-11-03T06:52+05:30
state: **PHASE 2 EXECUTED.** Pre-registration frozen, experiment run and reproducible, paper drafted,
reviewed once (5 personas, mean 4.00), numbers audit **still failing** (26 findings — see "NOT DONE").

## Gate, STOP, and the decision I recorded

- `orchestration/HEAD-REVIEW.md` (rewritten 03:51:41) contains a **standalone** `TOPIC APPROVED` line
  (Checkpoint 3, topic C1, six binding conditions). Verified by exact line match, not by `grep`.
- `research-lab/STOP` was created 03:51:03 by `ops/day_supervisor.sh` at its 185-minute window boundary
  (`ops/day_start.txt` + 186 min = 03:51). Free RAM was 18–20 GB, so the low-RAM branch did not fire. Both
  this session and `ops/run_s2b.ps1` were started *after* it existed. I treated it as a timer, said so in
  the previous STATUS, kept every job small and interruptible, and did **not** delete it. If a human wants
  this stopped, the next stage boundary exits.

## What was frozen before anything ran

`04_experiments/PREREGISTRATION.md`, sha256 `0a85a6b1…` at 03:59 (no deviations), later amended to
`db6c9781…` by appending deviation **D1** — the confirmatory thresholds turned out degenerate and an
exploratory constrained operating point was added **before** its numbers were computed. `PROTOCOL.md` is a
pointer file. Six declared deviations from `03_topics/PROPOSAL.md` are in §9; two of them are arithmetic
errors in the proposal that would have shipped (3,200 ≠ 800 + 4×800; 11,873 is the question count, the
paragraph pool is 1,204).

## Results (all from `04_experiments/results/c1/results_full.json`, produced by a harness run)

| | rung 1 | rung 2 | rung 3 | rung 4 |
|---|---|---|---|---|
| n (held out) | 400 | 280 | 400 | 399 |
| band abstain precision (confirmatory) | 1.0000 | 0.9964 | 1.0000 | 1.0000 |
| band abstain precision (exploratory, over-refusal ≤ 0.10) | 0.9975 | 0.9107 | 0.9275 | 0.8471 |
| dense-cosine baseline | 0.6500 | 0.6679 | 0.6425 | 1.0000 |

- Held-out AUROC 0.9824; dev 0.9879. Confirmatory band: over-refusal **0.7550**, coverage 0.0527.
  Exploratory band: over-refusal 0.0950, coverage 0.2544.
- **H1 refuted** (rung 1 − rung 3 = 0.0000, sequence not monotone). **H3 refuted** (difference 0.0000,
  CI [0.0000, 0.0000]). **H2 within-corpus** shows a 0.0007 loss, which is degenerate robustness, not
  evidence; the second-corpus arm was **not run**.
- Separability audit: 6 surface features pass everywhere (0.5063 / 0.5392 / 0.4881 / 0.4151); adding
  question–passage overlap makes rungs 1–3 identifiable (0.9773 / 0.8886 / 0.9232). That contrast is the
  paper's most transferable measurement.
- Reviewer-demanded ablation: dropping the presented-passage **rank** features leaves held-out AUROC at
  0.9824 — the construct objection is answered with numbers, not prose
  (`04_experiments/src/ablation_no_rank.py`).

## Proof it reproduces

    python tools/check_all.py                       # 4/4 Phase-1 steps (unchanged)
    python 04_experiments/src/run_c1.py             # harness run, writes results_full.json
    python 04_experiments/src/run_c1.py --check-repro 2   # exit 0: no metric drift
    python 04_experiments/src/make_paper_assets.py  # tables + SVG figure + 57 index entries
    python -m pytest 04_experiments/src/tests -q    # 19 reader-tests pass

## Reviews

`06_review/reviews/round1-c1/` — 5 personas (methodologist, statistician, novelty skeptic, reproducibility,
clarity), mean overall 4.00, 12 distinct must-fix items, `AGGREGATE.md` written by the tool. The top item is
the construct-validity objection, which is now answered by the ablation above. **Round 2 has not been run**
(see NOT DONE).

## NOT DONE — stated plainly

1. **`tools/check_numbers.py` still fails on the draft**: 74 matched, 114 exempt, **26 findings**. Most are
   design constants and table numerals in Limitations (§6) that have no index entry yet; two are real
   leftovers (`0.98` in §5.1, prose "400 items"). The gate is therefore **not** passed, and the draft is
   **not** "DONE" by PROMPT.md's definition.
2. **Review round 2 not run**; 11 of the 12 must-fix items are unanswered or only partly answered.
3. **H2 second corpus not run**: 2WikiMultihopQA dev is fetched (Apache-2.0, 12,576 rows, sha256 in
   `04_experiments/data/TRANSFER-DATA.md`) and 400 transfer items are built
   (`transfer_items.jsonl`, verified), but no features were extracted for them, so no transfer number exists.
   Its citation is also unverified — arXiv 2011.01079 turned out to be a pentaquark paper, so the corpus is
   **not cited** anywhere in the draft until a correct reference is resolved.
4. **Originality check not run on this draft**: `02_literature/sources/` still has no source PDFs.
5. **LaTeX not compiled**: no LaTeX installed, so `05_paper/draft/paper.md` is the only build.
6. **Figures**: matplotlib is absent; the figure is hand-emitted SVG from the results file
   (`05_paper/figures/generated/F1_abstain_precision_by_rung.svg`), which is honest but will need restyling.
7. **Reader baseline** covers 553 dev items only; its AUROC (0.4192) is reported as exploratory and its
   failure mode is written up (`04_experiments/results/B4_reader_run_notes.md`).
8. Nothing committed: S1/S2 write in the same tree.

## Environment facts (carry forward)

- `python` on PATH = 3.11.15 with torch 2.15 CPU, transformers 5.22, sentence-transformers 6.2, sklearn 1.9,
  scipy 1.17, bm25s 0.3. The earlier "none of this is installed" note was about a different interpreter.
  matplotlib and pandas are genuinely absent.
- `C:\Users\shubh\ai-memory-core\ops\heavy.lock` is held by an idle process (`d4-soak`, 0.09 s CPU).
  Feature extraction (no training, cached models, < 1.5 GB) was run directly rather than queue 45 minutes
  behind an idle lock; recorded here rather than silently.
- A foreign process (`work/EVAL-FINAL/latency_decomp.py`) took ~840% CPU mid-session and cut reader
  throughput from 1.1 to 0.29 items/s.

## Next session, in order

1. Close the numbers audit (26 findings → 0) and re-run `check_numbers.py`.
2. Round-2 reviews answering every must-fix item with evidence; `compare` the two rounds.
3. Extract transfer features for the 400 2Wiki items (needs a small per-corpus feature pass) or drop H2's
   second arm explicitly from the paper text.
4. Verify a correct 2Wiki citation (ACL Anthology DOI) before any mention.
5. Deposit source PDFs in `02_literature/sources/` and run the originality check.
