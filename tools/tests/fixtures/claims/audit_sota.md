# CLAIMS AUDIT — fixture: "state of the art" with no novelty row (should FAIL)

Draft: `tools/tests/fixtures/claims/draft_sota/paper.md`

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| S1 | "Our reranker is state of the art on the public benchmark, reaching 0.865 accuracy." | Abstract | tools/tests/fixtures/claims/results/main_ours.json | accuracy | python 04_experiments/harness/run.py --config configs/main.json --seed 0 | 0.865 | YES | one benchmark only | SS |
