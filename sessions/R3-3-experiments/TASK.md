# TASK R3-3 — new experiments & controls (main laptop, profile res-s3)

Goal: run the missing analyses the reviewers asked for, answering MF-3, 6, 7, 10, 12, 13, 14, 17 (full text + evidence in
`06_review/reviews/round2-c1/AGGREGATE.md`). All of it is EXPLORATORY / post-hoc unless the frozen pre-registration already
names it — say so in every output.

OWNED: `04_experiments/src/r3_exp_*.py`, `04_experiments/src/tests/test_r3_exp_*.py`, `04_experiments/results/c1/r3/exp/**`,
`sessions/R3-3-experiments/**`.

Compute rule (COMMON.md #6, owner instruction): GPU first, then CPU. For the reader, first check whether the local Ollama
(http://127.0.0.1:11434, Vulkan on the Arc iGPU; models present: qwen2.5:1.5b-instruct, qwen3:1.7b) can return token
log-probabilities for a "True"/"False" answer (try the `logprobs` option of /api/chat or /api/generate; record what works in
`results/c1/r3/exp/COMPUTE.md`). If it can, use it (note: it is a different, larger reader than the paper's
Qwen2.5-0.5B-Instruct — report it as such). If not, CPU torch with Qwen2.5-0.5B-Instruct, `torch.set_num_threads(4)`, heavy
lock held, one job at a time. Never run two model jobs at once.

Deliverables
1. MF-12: a P(True)-style reader baseline (Kadavath et al. arXiv:2207.05221 style prompt: question + passage + proposed
   answer -> "Is the proposed answer true?" -> P(True)) on the same 553 dev items, AUROC with interval and a dev-fitted
   threshold under the same 0.80 rule; held-out numbers. If it cannot be run, write why, and propose removing the claim.
2. MF-17: AUROC intervals (bootstrap, fixed seed, >= 2000 resamples or DeLong) for every AUROC the paper reports, and a
   PAIRED difference interval for 0.982 -> 0.874 (frozen vs corrected) on identical items.
3. MF-7: audit variant where answerable items' passage is NOT always the gold paragraph (or a gold-paragraph indicator
   control) to separate "rung hardness" from "is this the gold paragraph".
4. MF-13: two-sided separability audit (|AUROC - 0.5|); report R4's inverted separation explicitly.
5. MF-14: R4 under the registered analysis AND the post-hoc cell, side by side, plus a small robustness check (different
   seed / subsample) so the mechanistic claim does not rest on one cell — or a recommended narrower wording.
6. MF-3: one table with R5 and the transfer arm under BOTH runs (frozen 89.25% vs corrected 93.75%; transfer 85.50% @0.640 vs
   97.50% @0.706 — re-derive, do not copy).
7. MF-6: explicit H2 verdict for the second corpus against the pre-registered rule, with the recall each arm operates at, and
   what the rule says about a 5-10 point loss (quote PREREGISTRATION.md).
8. MF-10: answerability adjudication of a random, seeded sample of >= 100 negatives across rungs: two independent subagent
   labellers using a written rubric (does the passage contain an answer to the question?), agreement (Cohen's kappa),
   disagreements resolved by a third; report the share of "negatives" that actually answer the question. Disclose that the
   labellers are LLM agents.
9. `results/c1/r3/exp/ANSWERS.md` — per MF item: verdict, evidence file + key, command, proposed draft sentences.
