# TOY CLAIMS AUDIT — NOT A RESULT

Toy version of `06_review/CLAIMS-AUDIT-TEMPLATE.md`, used to prove `tools/claims_audit.py`
works end to end on the toy draft. Nothing here is a paper claim.

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| C-01 | "The baseline reaches an accuracy of 0.8704, while the logistic classifier reaches 0.8852." | Abstract | 04_experiments/results/summary_toy.json | stats.toy_baseline.mean | python 04_experiments/toy/run_toy.py | 0.8704 | YES | TOY: synthetic task, 3 seeds, mean over seeds; the second number is a separate row | SS |
| C-02 | "the logistic classifier reaches 0.8852" | Abstract | 04_experiments/results/summary_toy.json | stats.toy_ours.mean | python 04_experiments/toy/run_toy.py | 0.8852 | YES | TOY: not significant at n=3, p=0.50 | SS |
| C-03 | "trained on 150 points per class" | Method | 04_experiments/harness/configs/toy_ours.json | n_per_class | python 04_experiments/toy/run_toy.py --config 04_experiments/harness/configs/toy_ours.json | 150 | YES | TOY: synthetic gaussian blobs | SS |
