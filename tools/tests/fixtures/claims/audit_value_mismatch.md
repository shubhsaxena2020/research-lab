# CLAIMS AUDIT — fixture: printed value disagrees with the stored value (should FAIL)

Draft: `tools/tests/fixtures/claims/draft_min/paper.md`

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| V1 | "The baseline reaches 0.812 accuracy" | Abstract | tools/tests/fixtures/claims/results/main_baseline.json | accuracy | python 04_experiments/harness/run.py --config configs/baseline.json --seed 0 | 0.812 | YES | single seed | SS |
| V2 | "our reranker raises this to 0.865" | Abstract | tools/tests/fixtures/claims/results/main_ours.json | accuracy | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 0.900 | YES | copied from a different run by mistake | SS |
