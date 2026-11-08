# R3-1 metrics & statistics — PROGRESS

## Batch 1 (4 parallel subagents) — verified

Evidence:
- r3_metrics_core.py — DEFINITIONS.md, metrics.json, metrics.md: frozen band pooled precision 0.83, coverage 0.05/0.25; top1 0.63/0.87. Re-run exit 0; independent recompute matches. Report verify_core.md.
- r3_metrics_intervals.py — intervals.json/md: CP uppers 0/400=0.0092, 0/1479=0.0025; n_articles=18; min ratio 0.4521; no_dense CI [0.0038,0.0196] excludes 0; dense_only CI [-0.0078,0.0161] includes 0; frozen-vs-corrected [0.0951,0.1228]. Re-run exit 0; scipy check matches. Report verify_intervals_h3.md.
- r3_metrics_h3.py — h3.json: no constrained threshold exists (max feasible recall 0.9756 < 0.9898); re-matched diff -0.0169 CI [-0.0264,-0.0074]; cap binds on dev (0.095) not held-out (0.11 breached). Re-run exit 0. Report verify_intervals_h3.md.
- r3_metrics_rung2.py + test_r3_metrics_rung2.py — rung2.json: held-out 280/120, dev 273/127, min p 0.0524. Re-run exit 0, 2 tests pass. Report verify_rung2.md.

## Batch 2 (tests + ANSWERS, 4 tasks) — verified

Evidence:
- test_r3_metrics_core.py — 3 tests incl. 10-row hand fixture (pooled 6/7, coverage 0.3/0.5) pass. Report test_core.md.
- test_r3_metrics_intervals.py (6) + test_r3_metrics_h3.py (5) — 11 passed. Report test_intervals_h3.md.
- ANSWERS.md (160 lines) covers all 14 MFs. Report answers.md.
- Full suite: 16 tests passed (core 3 + rung2 2 + intervals 6 + h3 5) in 281s.
- Files: 8 metrics (DEFINITIONS, ANSWERS, metrics.json/md, intervals.json/md, h3.json, rung2.json), 4 scripts, 4 test files. 11 reports.

CARD COMPLETE
