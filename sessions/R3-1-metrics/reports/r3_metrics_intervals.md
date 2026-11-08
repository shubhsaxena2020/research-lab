# R3-1 metrics — r3_metrics_intervals

- Command: `python 04_experiments/src/r3_metrics_intervals.py`
- Seed: 12345, N_BOOT: 10000
- Outputs: `04_experiments/results/c1/r3/metrics/intervals.json`, `intervals.md`

## Key results
- H1 discordant pairs: 0/400; CP upper 0.0092; Wilson upper 0.0095
- H3 discordant pairs: 0/1479; CP upper 0.0025; Wilson upper 0.0026
- Interval method mismatch: True -> ['1', '3', '4']
- Cluster n_articles: 18 (verified)
- Rung-1 cluster CI: {'hi': 1.0, 'lo': 1.0}
- Rung-3 cluster CI: {'hi': 1.0, 'lo': 1.0}
- Min width ratio corrected: 0.4521
- all_12 vs no_dense CI: 0.0038 to 0.0196 (diff 0.0116)
- all_12 vs dense_only CI: -0.0078 to 0.0161 (diff 0.0043)
- frozen vs corrected CI: 0.0951 to 0.1228 (diff 0.1085)
- top1_0.945: 0.9453 [0.9211, 0.9663] feasible=True
- transfer_0.640: 0.6402 [0.5852, 0.6944] feasible=True
- audit_sensitivity_0.977: 0.9773 [0.9679, 0.9855] feasible=True

## Inputs sha256
- items_jsonl: c6f46ad80e7d15f495cd2a4b1e7b5a5556bfa929264c7afabd81826dd8d049d0
- features_csv: f9de87f699da1e73968dde27c5a55600c23c077ff9e5a446823e05abe0733cbb
- features_corrected_csv: 1d7f1b3aa16234168d1801565bf5c0f074d7260f2006574505fcee725fdd2fa6
- features_top1_csv: 3d22e100c1991ed63b3155ef6f0f66a873377d410ce0b9d629346ed4185e4a5c
- features_transfer_csv: f7c70b07edae77a3126a39d04addb1753e85717ab83c43b9c2d706141dbe8582
- predictions_csv: 154ed6df4756ae28a13823ffdf6811db0e7c6809d5d23498cb799e24ccd03133
- results_full_json: e4cf65cb0b2bae52e4ee4b379e0c4e66450ed21474d71b57e49e8d4218c36b35
- stats_addendum_json: 9c3d20d161191bfaa62e4c93d8071532e5541bb93474c28e2cc27a9558dde4a6
- ablations_json: 2b6c29c0e21133375f2ee027980a8ca90d467482f5b1c8e43189d9d4cf32c193
- top1_variant_json: 299c3e0569b4cef98342ac57930ce2b12398f00a7810a5b4bb80df7af7b65117
- transfer_json: 690278824756a208309e10a65f7cf231fb26b67cf5ab0a104d1069c985d3d614
- audit_json: c1ad496e07cc9ac0ec2c85f1f83c65f6c0cb7a09b840dd4da1f194673cb07489
