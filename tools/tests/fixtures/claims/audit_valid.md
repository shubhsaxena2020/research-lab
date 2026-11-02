# CLAIMS AUDIT — fixture draft (should PASS)

Test fixture for `tools/tests/test_claims_audit.py`. The draft it audits is
`tools/tests/fixtures/claims/draft/paper.md`; all numbers are synthetic fixture data.

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| A1 | "We evaluate a compact cross-encoder reranker on 1,000 held-out public queries." | Abstract | tools/tests/fixtures/claims/results/main_ours.json | _meta.n | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 1,000 | YES | one public benchmark only | SS |
| A2 | "The baseline reaches 0.812 accuracy" | Abstract | tools/tests/fixtures/claims/results/main_baseline.json | accuracy | python 04_experiments/harness/run.py --config configs/baseline.json --seed 0 | 0.812 | YES | single seed for this number; seed spread in A4 | SS |
| A3 | "our reranker raises this to 0.865" | Abstract | tools/tests/fixtures/claims/results/main_ours.json | accuracy | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 0.865 | YES | same split as A2 | SS |
| A4 | "Across 5 seeds the improvement is stable" | Abstract | tools/tests/fixtures/claims/results/summary_main.json | n_seeds | python 04_experiments/harness/aggregate.py --experiment main | 5 | YES | 5 seeds is small; CI in summary_main.json | SS |
| A5 | "with a Holm-corrected p-value of 0.031" | Abstract | tools/tests/fixtures/claims/results/summary_main.json | paired.p_value | python 04_experiments/harness/aggregate.py --experiment main | 0.031 | YES | family of 3 comparisons, Holm \| not Bonferroni | SS |
| A6 | "To our knowledge this is the first audit that binds every abstract claim to a stored result." | Abstract | tools/tests/fixtures/claims/NOVELTY-CHECK.md | audit claim binding | `grep -n "audit\|novel" tools/tests/fixtures/claims/NOVELTY-CHECK.md` | no prior audit binds every abstract claim to a stored result | YES | searched 2 queries only; no full-text screening | SS |
| A7 | "Prior work reports strong ranking results on standard benchmarks [@vaswani2017]." | Introduction | tools/tests/fixtures/claims/verified_citations.csv | key=vaswani2017 | python tools/verify_citations.py --csv 02_literature/citations.csv --online | VERIFIED | YES | survey claim, not a head-to-head rerun | SS |
| A8 | "On the same held-out queries the reranker improves accuracy to 0.865,
at 14.2 ms mean latency per query." | Introduction | tools/tests/fixtures/claims/results/main_ours.json | accuracy | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 0.865 | YES | latency measured on CPU only, not GPU | SS |
| A9 | "at 14.2 ms mean latency per query" | Introduction | tools/tests/fixtures/claims/results/main_ours.json | latency_ms | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 14.2 | YES | single machine, batch size 1 | SS |
| EX-001 | "Example row — our method halves the error rate." | Abstract | tools/tests/fixtures/claims/results/does_not_exist.json | accuracy | echo "not a real command" | 0.5 | NO | example only, never judged | — |
