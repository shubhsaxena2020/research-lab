# CLAIMS AUDIT — fixture: evidence file missing on row M2 (should FAIL)

Draft: `tools/tests/fixtures/claims/draft_min/paper.md`

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| M1 | "The baseline reaches 0.812 accuracy" | Abstract | tools/tests/fixtures/claims/results/main_baseline.json | accuracy | python 04_experiments/harness/run.py --config configs/baseline.json --seed 0 | 0.812 | YES | single seed | SS |
| M2 | "our reranker raises this to 0.865" | Abstract | tools/tests/fixtures/claims/results/main_ours_missing.json | accuracy | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 0.865 | YES | same split as M1 | SS |
