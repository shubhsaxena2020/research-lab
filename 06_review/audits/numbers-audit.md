# Numbers audit

> **Scope: a PAPER draft: this PASS can be quoted as evidence that the draft's numbers are traceable.**
> Audited path: `05_paper/draft/paper.md`

Draft: `05_paper/draft/paper.md`  
Index: `04_experiments/RESULTS-INDEX.json`  
Generated: 2026-11-03T02:19:20Z  
Toy numbers allowed: False

**PASS** — 0 finding(s) over 1 file(s).

| scanned | matched | exempt | untraceable | mismatch | dangling | index error | unbound |
|---|---|---|---|---|---|---|---|
| 474 | 296 | 178 | 0 | 0 | 0 | 0 | 0 |

## Findings

None. Every numeric token is marked-and-matching or exempt.

## Matched numbers

| where | printed | marker | stored | evidence |
|-------|---------|--------|--------|----------|
| `05_paper/draft/paper.md:18` | `0.80` | `c1.const.target_precision` | `0.8` | printed '0.80' vs stored 0.8; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:19` | `75.50%` | `c1.band.over_refusal.run` | `0.755` | printed '75.50%' vs stored 0.755; percentage form: 75.50/100 = 0.755, so '75.50%' is the same number as 0.755; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:20` | `24.50%` | `c1.pm.band.answer_rate` | `0.245` | printed '24.50%' vs stored 0.245; percentage form: 24.50/100 = 0.245, so '24.50%' is the same number as 0.245; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:21` | `83.03%` | `c1.pm.band.pooled_precision` | `0.8303` | printed '83.03%' vs stored 0.8303; percentage form: 83.03/100 = 0.8303, so '83.03%' is the same number as 0.8303; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:23` | `100.00%` | `c1.pm.band.refusal.r1` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:24` | `99.64%` | `c1.pm.band.refusal.r2` | `0.9964` | printed '99.64%' vs stored 0.9964; percentage form: 99.64/100 = 0.9964, so '99.64%' is the same number as 0.9964; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:25` | `100.00%` | `c1.pm.band.refusal.r3` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:26` | `100.00%` | `c1.pm.band.refusal.r4` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:27` | `0.00%` | `c1.h1.diff` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:27` | `0.00%` | `c1.h1.lo` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:28` | `0.00%` | `c1.h1.hi` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:29` | `0.00%` | `c1.h3.diff` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:30` | `0.00%` | `c1.h3.lo` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:30` | `0.00%` | `c1.h3.hi` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:32` | `0.07%` | `c1.h2.loss` | `0.0007` | printed '0.07%' vs stored 0.0007; percentage form: 0.07/100 = 0.0007, so '0.07%' is the same number as 0.0007; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:34` | `0.506` | `c1.audit.surface.r1` | `0.5063` | printed '0.506' vs stored 0.5063; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:34` | `0.539` | `c1.audit.surface.r2` | `0.5392` | printed '0.539' vs stored 0.5392; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:35` | `0.488` | `c1.audit.surface.r3` | `0.4881` | printed '0.488' vs stored 0.4881; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:35` | `0.415` | `c1.audit.surface.r4` | `0.4151` | printed '0.415' vs stored 0.4151; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:37` | `0.977` | `c1.audit.surface_lex.r1` | `0.9773` | printed '0.977' vs stored 0.9773; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:37` | `0.889` | `c1.audit.surface_lex.r2` | `0.8886` | printed '0.889' vs stored 0.8886; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:38` | `0.923` | `c1.audit.surface_lex.r3` | `0.9232` | printed '0.923' vs stored 0.9232; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:39` | `75.50%` | `c1.band.over_refusal.run` | `0.755` | printed '75.50%' vs stored 0.755; percentage form: 75.50/100 = 0.755, so '75.50%' is the same number as 0.755; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:41` | `56.98%` | `c1.pm.band.precision.r1` | `0.5698` | printed '56.98%' vs stored 0.5698; percentage form: 56.98/100 = 0.5698, so '56.98%' is the same number as 0.5698; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:42` | `48.02%` | `c1.pm.band.precision.r2` | `0.4802` | printed '48.02%' vs stored 0.4802; percentage form: 48.02/100 = 0.4802, so '48.02%' is the same number as 0.4802; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:45` | `89.25%` | `c1.r5.precision.expl` | `0.8925` | printed '89.25%' vs stored 0.8925; percentage form: 89.25/100 = 0.8925, so '89.25%' is the same number as 0.8925; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:48` | `12.53%` | `c1.expl.precision.r4.corr` | `0.1253` | printed '12.53%' vs stored 0.1253; percentage form: 12.53/100 = 0.1253, so '12.53%' is the same number as 0.1253; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:49` | `0.982` | `c1.auroc.test.run` | `0.9824` | printed '0.982' vs stored 0.9824; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:49` | `0.874` | `c1.auroc.test.corr` | `0.8738` | printed '0.874' vs stored 0.8738; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:64` | `98%` | `c1.lit.acc.random` | `0.98` | printed '98%' vs stored 0.98; percentage form: 98/100 = 0.98, so '98%' is the same number as 0.98; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:64` | `1%` | `c1.lit.acc.overlap` | `0.01` | printed '1%' vs stored 0.01; percentage form: 1/100 = 0.01, so '1%' is the same number as 0.01; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:140` | `35` | `c1.data.articles` | `35` | printed '35' vs stored 35; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:141` | `1204` | `c1.data.paragraphs` | `1204` | printed '1204' vs stored 1204; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:142` | `11873` | `c1.data.questions` | `11873` | printed '11873' vs stored 11873; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:143` | `5928` | `c1.data.answerable` | `5928` | printed '5928' vs stored 5928; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:159` | `3752` | `c1.items.total` | `3752` | printed '3752' vs stored 3752; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:160` | `1879` | `c1.items.test` | `1879` | printed '1879' vs stored 1879; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:161` | `273` | `c1.items.rung2.dev` | `273` | printed '273' vs stored 273; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:168` | `12` | `c1.const.n_gate_features` | `12` | printed '12' vs stored 12; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:180` | `0.80` | `c1.const.target_precision` | `0.8` | printed '0.80' vs stored 0.8; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:181` | `0.9072` | `c1.thr.lo` | `0.90722098925` | printed '0.9072' vs stored 0.90722098925; diff 0.00002098925 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:181` | `0.9478` | `c1.thr.hi` | `0.947838803928` | printed '0.9478' vs stored 0.947838803928; diff 0.000038803928 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:182` | `0.0406` | `c1.band.width` | `0.040618` | printed '0.0406' vs stored 0.040618; diff 0.000018 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:183` | `0.9394` | `c1.thr.single` | `0.939398578046` | printed '0.9394' vs stored 0.939398578046; diff 0.000001421954 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:185` | `6.03%` | `c1.dev.admit_mass` | `0.0603` | printed '6.03%' vs stored 0.0603; percentage form: 6.03/100 = 0.0603, so '6.03%' is the same number as 0.0603; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:186` | `92.95%` | `c1.dev.refused_below_lo` | `0.9295` | printed '92.95%' vs stored 0.9295; percentage form: 92.95/100 = 0.9295, so '92.95%' is the same number as 0.9295; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:192` | `6` | `c1.const.n_surface_features` | `6` | printed '6' vs stored 6; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:194` | `5` | `c1.const.cv_folds` | `5` | printed '5' vs stored 5; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:196` | `0.750` | `c1.const.audit_gate` | `0.75` | printed '0.750' vs stored 0.75; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:204` | `0.415` | `c1.audit.surface.r4` | `0.4151` | printed '0.415' vs stored 0.4151; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:213` | `100.00%` | `c1.pm.band.refusal.r1` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:214` | `48.02%` | `c1.pm.band.precision.r2` | `0.4802` | printed '48.02%' vs stored 0.4802; percentage form: 48.02/100 = 0.4802, so '48.02%' is the same number as 0.4802; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:215` | `56.98%` | `c1.pm.band.precision.r1` | `0.5698` | printed '56.98%' vs stored 0.5698; percentage form: 56.98/100 = 0.5698, so '56.98%' is the same number as 0.5698; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:220` | `83.03%` | `c1.pm.band.pooled_precision` | `0.8303` | printed '83.03%' vs stored 0.8303; percentage form: 83.03/100 = 0.8303, so '83.03%' is the same number as 0.8303; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:221` | `97.29%` | `c1.pm.expl.pooled_precision` | `0.9729` | printed '97.29%' vs stored 0.9729; percentage form: 97.29/100 = 0.9729, so '97.29%' is the same number as 0.9729; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:227` | `10000` | `c1.stats.n_boot` | `10000` | printed '10000' vs stored 10000; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:228` | `12345` | `c1.stats.seed` | `12345` | printed '12345' vs stored 12345; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:245` | `0.506` | `c1.audit.surface.r1` | `0.5063` | printed '0.506' vs stored 0.5063; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:245` | `0.977` | `c1.audit.surface_lex.r1` | `0.9773` | printed '0.977' vs stored 0.9773; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:245` | `0.750` | `c1.const.audit_gate` | `0.75` | printed '0.750' vs stored 0.75; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:246` | `0.539` | `c1.audit.surface.r2` | `0.5392` | printed '0.539' vs stored 0.5392; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:246` | `0.889` | `c1.audit.surface_lex.r2` | `0.8886` | printed '0.889' vs stored 0.8886; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:246` | `0.750` | `c1.const.audit_gate` | `0.75` | printed '0.750' vs stored 0.75; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:247` | `0.488` | `c1.audit.surface.r3` | `0.4881` | printed '0.488' vs stored 0.4881; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:247` | `0.923` | `c1.audit.surface_lex.r3` | `0.9232` | printed '0.923' vs stored 0.9232; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:247` | `0.750` | `c1.const.audit_gate` | `0.75` | printed '0.750' vs stored 0.75; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:248` | `0.415` | `c1.audit.surface.r4` | `0.4151` | printed '0.415' vs stored 0.4151; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:248` | `0.408` | `c1.audit.surface_lex.r4` | `0.4082` | printed '0.408' vs stored 0.4082; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:248` | `0.750` | `c1.const.audit_gate` | `0.75` | printed '0.750' vs stored 0.75; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:249` | `0.721` | `c1.r5.audit.surface` | `0.7208` | printed '0.721' vs stored 0.7208; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:249` | `0.794` | `c1.r5.audit.lex` | `0.7936` | printed '0.794' vs stored 0.7936; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:249` | `0.750` | `c1.const.audit_gate` | `0.75` | printed '0.750' vs stored 0.75; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:254` | `0.977` | `c1.audit.surface_lex.r1` | `0.9773` | printed '0.977' vs stored 0.9773; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:258` | `0.408` | `c1.audit.surface_lex.r4` | `0.4082` | printed '0.408' vs stored 0.4082; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:266` | `400` | `c1.pm.n.r1` | `400` | printed '400' vs stored 400; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:266` | `100.00%` | `c1.pm.band.refusal.r1` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:266` | `56.98%` | `c1.pm.band.precision.r1` | `0.5698` | printed '56.98%' vs stored 0.5698; percentage form: 56.98/100 = 0.5698, so '56.98%' is the same number as 0.5698; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:266` | `99.75%` | `c1.pm.expl.refusal.r1` | `0.9975` | printed '99.75%' vs stored 0.9975; percentage form: 99.75/100 = 0.9975, so '99.75%' is the same number as 0.9975; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:266` | `91.30%` | `c1.pm.expl.precision.r1` | `0.913` | printed '91.30%' vs stored 0.913; percentage form: 91.30/100 = 0.913, so '91.30%' is the same number as 0.913; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:267` | `280` | `c1.pm.n.r2` | `280` | printed '280' vs stored 280; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:267` | `99.64%` | `c1.pm.band.refusal.r2` | `0.9964` | printed '99.64%' vs stored 0.9964; percentage form: 99.64/100 = 0.9964, so '99.64%' is the same number as 0.9964; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:267` | `48.02%` | `c1.pm.band.precision.r2` | `0.4802` | printed '48.02%' vs stored 0.4802; percentage form: 48.02/100 = 0.4802, so '48.02%' is the same number as 0.4802; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:267` | `91.07%` | `c1.pm.expl.refusal.r2` | `0.9107` | printed '91.07%' vs stored 0.9107; percentage form: 91.07/100 = 0.9107, so '91.07%' is the same number as 0.9107; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:267` | `87.03%` | `c1.pm.expl.precision.r2` | `0.8703` | printed '87.03%' vs stored 0.8703; percentage form: 87.03/100 = 0.8703, so '87.03%' is the same number as 0.8703; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:268` | `400` | `c1.pm.n.r3` | `400` | printed '400' vs stored 400; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:268` | `100.00%` | `c1.pm.band.refusal.r3` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:268` | `56.98%` | `c1.pm.band.precision.r3` | `0.5698` | printed '56.98%' vs stored 0.5698; percentage form: 56.98/100 = 0.5698, so '56.98%' is the same number as 0.5698; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:268` | `92.75%` | `c1.pm.expl.refusal.r3` | `0.9275` | printed '92.75%' vs stored 0.9275; percentage form: 92.75/100 = 0.9275, so '92.75%' is the same number as 0.9275; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:268` | `90.71%` | `c1.pm.expl.precision.r3` | `0.9071` | printed '90.71%' vs stored 0.9071; percentage form: 90.71/100 = 0.9071, so '90.71%' is the same number as 0.9071; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:269` | `399` | `c1.pm.n.r4` | `399` | printed '399' vs stored 399; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:269` | `100.00%` | `c1.pm.band.refusal.r4` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:269` | `56.92%` | `c1.pm.band.precision.r4` | `0.5692` | printed '56.92%' vs stored 0.5692; percentage form: 56.92/100 = 0.5692, so '56.92%' is the same number as 0.5692; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:269` | `84.71%` | `c1.pm.expl.refusal.r4` | `0.8471` | printed '84.71%' vs stored 0.8471; percentage form: 84.71/100 = 0.8471, so '84.71%' is the same number as 0.8471; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:269` | `89.89%` | `c1.pm.expl.precision.r4` | `0.8989` | printed '89.89%' vs stored 0.8989; percentage form: 89.89/100 = 0.8989, so '89.89%' is the same number as 0.8989; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:271` | `83.03%` | `c1.pm.band.pooled_precision` | `0.8303` | printed '83.03%' vs stored 0.8303; percentage form: 83.03/100 = 0.8303, so '83.03%' is the same number as 0.8303; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:271` | `97.29%` | `c1.pm.expl.pooled_precision` | `0.9729` | printed '97.29%' vs stored 0.9729; percentage form: 97.29/100 = 0.9729, so '97.29%' is the same number as 0.9729; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:271` | `24.50%` | `c1.pm.band.answer_rate` | `0.245` | printed '24.50%' vs stored 0.245; percentage form: 24.50/100 = 0.245, so '24.50%' is the same number as 0.245; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:277` | `15` | `c1.crit.h1` | `15` | printed '15' vs stored 15; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:277` | `0.00%` | `c1.h1.diff` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:277` | `0.00%` | `c1.h1.lo` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:277` | `0.00%` | `c1.h1.hi` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:278` | `10` | `c1.crit.h2` | `10` | printed '10' vs stored 10; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:278` | `5` | `c1.crit.h2.slack` | `5` | printed '5' vs stored 5; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:278` | `0.07%` | `c1.h2.loss` | `0.0007` | printed '0.07%' vs stored 0.0007; percentage form: 0.07/100 = 0.0007, so '0.07%' is the same number as 0.0007; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:279` | `5` | `c1.crit.h3` | `5` | printed '5' vs stored 5; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:279` | `0.00%` | `c1.h3.diff` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:279` | `0.00%` | `c1.h3.lo` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:279` | `0.00%` | `c1.h3.hi` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:282` | `100.00%` | `c1.band.precision.r1.run` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:283` | `99.64%` | `c1.band.precision.r2.run` | `0.9964` | printed '99.64%' vs stored 0.9964; percentage form: 99.64/100 = 0.9964, so '99.64%' is the same number as 0.9964; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:284` | `100.00%` | `c1.band.precision.r3.run` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:285` | `100.00%` | `c1.band.precision.r4.run` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:286` | `75.50%` | `c1.band.over_refusal.run` | `0.755` | printed '75.50%' vs stored 0.755; percentage form: 75.50/100 = 0.755, so '75.50%' is the same number as 0.755; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:287` | `24.50%` | `c1.pm.band.answer_rate` | `0.245` | printed '24.50%' vs stored 0.245; percentage form: 24.50/100 = 0.245, so '24.50%' is the same number as 0.245; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:294` | `0.00%` | `c1.h1.diff` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:295` | `0.00%` | `c1.h1.lo` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:295` | `0.00%` | `c1.h1.hi` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:303` | `0.00%` | `c1.h3.diff` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:304` | `0.00%` | `c1.h3.lo` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:304` | `0.00%` | `c1.h3.hi` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:306` | `0.00` | `c1.st.match.maxdiff` | `0.0` | printed '0.00' vs stored 0.0; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:307` | `75.50%` | `c1.st.match.over.band` | `0.755` | printed '75.50%' vs stored 0.755; percentage form: 75.50/100 = 0.755, so '75.50%' is the same number as 0.755; diff 0.000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:308` | `72.50%` | `c1.st.match.over.matched` | `0.725` | printed '72.50%' vs stored 0.725; percentage form: 72.50/100 = 0.725, so '72.50%' is the same number as 0.725; diff 0.000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:314` | `0.07%` | `c1.h2.loss` | `0.0007` | printed '0.07%' vs stored 0.0007; percentage form: 0.07/100 = 0.0007, so '0.07%' is the same number as 0.0007; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:316` | `92.95%` | `c1.dev.refused_below_lo` | `0.9295` | printed '92.95%' vs stored 0.9295; percentage form: 92.95/100 = 0.9295, so '92.95%' is the same number as 0.9295; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:320` | `56.98%` | `c1.pm.band.precision.r1` | `0.5698` | printed '56.98%' vs stored 0.5698; percentage form: 56.98/100 = 0.5698, so '56.98%' is the same number as 0.5698; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:321` | `48.02%` | `c1.pm.band.precision.r2` | `0.4802` | printed '48.02%' vs stored 0.4802; percentage form: 48.02/100 = 0.4802, so '48.02%' is the same number as 0.4802; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:323` | `83.69%` | `c1.band.dev_precision` | `0.8369` | printed '83.69%' vs stored 0.8369; percentage form: 83.69/100 = 0.8369, so '83.69%' is the same number as 0.8369; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:327` | `1.69%` | `c1.b1.pooled` | `0.0169` | printed '1.69%' vs stored 0.0169; percentage form: 1.69/100 = 0.0169, so '1.69%' is the same number as 0.0169; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:328` | `74.58%` | `c1.b2.pooled.run` | `0.7458` | printed '74.58%' vs stored 0.7458; percentage form: 74.58/100 = 0.7458, so '74.58%' is the same number as 0.7458; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:336` | `0.80` | `c1.const.target_precision` | `0.8` | printed '0.80' vs stored 0.8; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:337` | `0.10` | `c1.const.over_cap` | `0.1` | printed '0.10' vs stored 0.1; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:338` | `9.50%` | `c1.expl.over_refusal.run` | `0.095` | printed '9.50%' vs stored 0.095; percentage form: 9.50/100 = 0.095, so '9.50%' is the same number as 0.095; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:339` | `25.44%` | `c1.expl.coverage.run` | `0.2544` | printed '25.44%' vs stored 0.2544; percentage form: 25.44/100 = 0.2544, so '25.44%' is the same number as 0.2544; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:341` | `99.75%` | `c1.expl.precision.r1.run` | `0.9975` | printed '99.75%' vs stored 0.9975; percentage form: 99.75/100 = 0.9975, so '99.75%' is the same number as 0.9975; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:342` | `91.07%` | `c1.expl.precision.r2.run` | `0.9107` | printed '91.07%' vs stored 0.9107; percentage form: 91.07/100 = 0.9107, so '91.07%' is the same number as 0.9107; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:343` | `92.75%` | `c1.expl.precision.r3.run` | `0.9275` | printed '92.75%' vs stored 0.9275; percentage form: 92.75/100 = 0.9275, so '92.75%' is the same number as 0.9275; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:344` | `84.71%` | `c1.expl.precision.r4.run` | `0.8471` | printed '84.71%' vs stored 0.8471; percentage form: 84.71/100 = 0.8471, so '84.71%' is the same number as 0.8471; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:345` | `87.03%` | `c1.pm.expl.precision.r2` | `0.8703` | printed '87.03%' vs stored 0.8703; percentage form: 87.03/100 = 0.8703, so '87.03%' is the same number as 0.8703; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:346` | `91.30%` | `c1.pm.expl.precision.r1` | `0.913` | printed '91.30%' vs stored 0.913; percentage form: 91.30/100 = 0.913, so '91.30%' is the same number as 0.913; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:347` | `7.00%` | `c1.st.expl.diff` | `0.07` | printed '7.00%' vs stored 0.07; percentage form: 7.00/100 = 0.07, so '7.00%' is the same number as 0.07; diff 0.00 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:348` | `4.50%` | `c1.st.expl.lo` | `0.045` | printed '4.50%' vs stored 0.045; percentage form: 4.50/100 = 0.045, so '4.50%' is the same number as 0.045; diff 0.000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:348` | `9.75%` | `c1.st.expl.hi` | `0.0975` | printed '9.75%' vs stored 0.0975; percentage form: 9.75/100 = 0.0975, so '9.75%' is the same number as 0.0975; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:350` | `15.04%` | `c1.st.expl.r14` | `0.1504` | printed '15.04%' vs stored 0.1504; percentage form: 15.04/100 = 0.1504, so '15.04%' is the same number as 0.1504; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:350` | `11.53%` | `c1.st.expl.r14.lo` | `0.1153` | printed '11.53%' vs stored 0.1153; percentage form: 11.53/100 = 0.1153, so '11.53%' is the same number as 0.1153; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:351` | `18.80%` | `c1.st.expl.r14.hi` | `0.188` | printed '18.80%' vs stored 0.188; percentage form: 18.80/100 = 0.188, so '18.80%' is the same number as 0.188; diff 0.000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:362` | `10.29%` | `c1.r5.match.mean_absdiff` | `0.1029` | printed '10.29%' vs stored 0.1029; percentage form: 10.29/100 = 0.1029, so '10.29%' is the same number as 0.1029; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:363` | `42.08%` | `c1.r5.match.contrast` | `0.4208` | printed '42.08%' vs stored 0.4208; percentage form: 42.08/100 = 0.4208, so '42.08%' is the same number as 0.4208; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:370` | `100.00%` | `c1.r5.precision.conf` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:370` | `100.00%` | `c1.r5.ci.lo` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:370` | `100.00%` | `c1.r5.ci.hi` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:370` | `0.974` | `c1.r5.auroc` | `0.9736` | printed '0.974' vs stored 0.9736; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:371` | `89.25%` | `c1.r5.precision.expl` | `0.8925` | printed '89.25%' vs stored 0.8925; percentage form: 89.25/100 = 0.8925, so '89.25%' is the same number as 0.8925; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:371` | `85.75%` | `c1.r5.expl.ci.lo` | `0.8575` | printed '85.75%' vs stored 0.8575; percentage form: 85.75/100 = 0.8575, so '85.75%' is the same number as 0.8575; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:371` | `91.75%` | `c1.r5.expl.ci.hi` | `0.9175` | printed '91.75%' vs stored 0.9175; percentage form: 91.75/100 = 0.9175, so '91.75%' is the same number as 0.9175; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:371` | `10.29%` | `c1.r5.match.mean_absdiff` | `0.1029` | printed '10.29%' vs stored 0.1029; percentage form: 10.29/100 = 0.1029, so '10.29%' is the same number as 0.1029; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:371` | `0.974` | `c1.r5.auroc` | `0.9736` | printed '0.974' vs stored 0.9736; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:372` | `98.50%` | `c1.tr.precision.conf` | `0.985` | printed '98.50%' vs stored 0.985; percentage form: 98.50/100 = 0.985, so '98.50%' is the same number as 0.985; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:372` | `89.50%` | `c1.tr.over_refusal.conf` | `0.895` | printed '89.50%' vs stored 0.895; percentage form: 89.50/100 = 0.895, so '89.50%' is the same number as 0.895; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:372` | `0.640` | `c1.tr.auroc` | `0.6402` | printed '0.640' vs stored 0.6402; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:373` | `85.50%` | `c1.tr.precision.expl` | `0.855` | printed '85.50%' vs stored 0.855; percentage form: 85.50/100 = 0.855, so '85.50%' is the same number as 0.855; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:373` | `79.50%` | `c1.tr.ci.lo` | `0.795` | printed '79.50%' vs stored 0.795; percentage form: 79.50/100 = 0.795, so '79.50%' is the same number as 0.795; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:373` | `89.50%` | `c1.tr.ci.hi` | `0.895` | printed '89.50%' vs stored 0.895; percentage form: 89.50/100 = 0.895, so '89.50%' is the same number as 0.895; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:373` | `57.50%` | `c1.tr.over_refusal.expl` | `0.575` | printed '57.50%' vs stored 0.575; percentage form: 57.50/100 = 0.575, so '57.50%' is the same number as 0.575; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:373` | `0.640` | `c1.tr.auroc` | `0.6402` | printed '0.640' vs stored 0.6402; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:374` | `78.25%` | `c1.t1.hit.test` | `0.7825` | printed '78.25%' vs stored 0.7825; percentage form: 78.25/100 = 0.7825, so '78.25%' is the same number as 0.7825; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:374` | `87.30%` | `c1.t1.precision.miss` | `0.873` | printed '87.30%' vs stored 0.873; percentage form: 87.30/100 = 0.873, so '87.30%' is the same number as 0.873; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:374` | `2.56%` | `c1.t1.refuse.hit` | `0.0256` | printed '2.56%' vs stored 0.0256; percentage form: 2.56/100 = 0.0256, so '2.56%' is the same number as 0.0256; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:374` | `0.945` | `c1.t1.auroc` | `0.9453` | printed '0.945' vs stored 0.9453; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:379` | `89.25%` | `c1.r5.precision.expl` | `0.8925` | printed '89.25%' vs stored 0.8925; percentage form: 89.25/100 = 0.8925, so '89.25%' is the same number as 0.8925; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:380` | `85.75%` | `c1.r5.expl.ci.lo` | `0.8575` | printed '85.75%' vs stored 0.8575; percentage form: 85.75/100 = 0.8575, so '85.75%' is the same number as 0.8575; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:380` | `91.75%` | `c1.r5.expl.ci.hi` | `0.9175` | printed '91.75%' vs stored 0.9175; percentage form: 91.75/100 = 0.9175, so '91.75%' is the same number as 0.9175; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:381` | `91.07%` | `c1.expl.precision.r2.run` | `0.9107` | printed '91.07%' vs stored 0.9107; percentage form: 91.07/100 = 0.9107, so '91.07%' is the same number as 0.9107; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:382` | `84.71%` | `c1.expl.precision.r4.run` | `0.8471` | printed '84.71%' vs stored 0.8471; percentage form: 84.71/100 = 0.8471, so '84.71%' is the same number as 0.8471; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:384` | `0.721` | `c1.r5.audit.surface` | `0.7208` | printed '0.721' vs stored 0.7208; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:398` | `78.25%` | `c1.t1.hit.test` | `0.7825` | printed '78.25%' vs stored 0.7825; percentage form: 78.25/100 = 0.7825, so '78.25%' is the same number as 0.7825; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:402` | `0.945` | `c1.t1.auroc` | `0.9453` | printed '0.945' vs stored 0.9453; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:403` | `63.22%` | `c1.t1.refuse.miss` | `0.6322` | printed '63.22%' vs stored 0.6322; percentage form: 63.22/100 = 0.6322, so '63.22%' is the same number as 0.6322; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:404` | `2.56%` | `c1.t1.refuse.hit` | `0.0256` | printed '2.56%' vs stored 0.0256; percentage form: 2.56/100 = 0.0256, so '2.56%' is the same number as 0.0256; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:405` | `87.30%` | `c1.t1.precision.miss` | `0.873` | printed '87.30%' vs stored 0.873; percentage form: 87.30/100 = 0.873, so '87.30%' is the same number as 0.873; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:416` | `78.70%` | `c1.obs.dense.eq1` | `0.787` | printed '78.70%' vs stored 0.787; percentage form: 78.70/100 = 0.787, so '78.70%' is the same number as 0.787; diff 0.000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:430` | `0.988` | `c1.auroc.dev.run` | `0.9879` | printed '0.988' vs stored 0.9879; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:430` | `0.887` | `c1.auroc.dev.corr` | `0.887` | printed '0.887' vs stored 0.887; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:431` | `0.982` | `c1.auroc.test.run` | `0.9824` | printed '0.982' vs stored 0.9824; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:431` | `0.874` | `c1.auroc.test.corr` | `0.8738` | printed '0.874' vs stored 0.8738; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:432` | `100.00%` | `c1.band.precision.r1.run` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:432` | `100.00%` | `c1.band.precision.r1.corr` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:433` | `99.64%` | `c1.band.precision.r2.run` | `0.9964` | printed '99.64%' vs stored 0.9964; percentage form: 99.64/100 = 0.9964, so '99.64%' is the same number as 0.9964; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:433` | `99.64%` | `c1.band.precision.r2.corr` | `0.9964` | printed '99.64%' vs stored 0.9964; percentage form: 99.64/100 = 0.9964, so '99.64%' is the same number as 0.9964; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:434` | `100.00%` | `c1.band.precision.r3.run` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:434` | `100.00%` | `c1.band.precision.r3.corr` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:435` | `100.00%` | `c1.band.precision.r4.run` | `1.0` | printed '100.00%' vs stored 1.0; percentage form: 100.00/100 = 1.00, so '100.00%' is the same number as 1.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:435` | `90.73%` | `c1.band.precision.r4.corr` | `0.9073` | printed '90.73%' vs stored 0.9073; percentage form: 90.73/100 = 0.9073, so '90.73%' is the same number as 0.9073; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:436` | `75.50%` | `c1.band.over_refusal.run` | `0.755` | printed '75.50%' vs stored 0.755; percentage form: 75.50/100 = 0.755, so '75.50%' is the same number as 0.755; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:436` | `91.50%` | `c1.band.over_refusal.corr` | `0.915` | printed '91.50%' vs stored 0.915; percentage form: 91.50/100 = 0.915, so '91.50%' is the same number as 0.915; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:437` | `5.27%` | `c1.band.coverage.run` | `0.0527` | printed '5.27%' vs stored 0.0527; percentage form: 5.27/100 = 0.0527, so '5.27%' is the same number as 0.0527; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:437` | `3.83%` | `c1.band.coverage.corr` | `0.0383` | printed '3.83%' vs stored 0.0383; percentage form: 3.83/100 = 0.0383, so '3.83%' is the same number as 0.0383; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:438` | `99.75%` | `c1.expl.precision.r1.run` | `0.9975` | printed '99.75%' vs stored 0.9975; percentage form: 99.75/100 = 0.9975, so '99.75%' is the same number as 0.9975; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:438` | `99.75%` | `c1.expl.precision.r1.corr` | `0.9975` | printed '99.75%' vs stored 0.9975; percentage form: 99.75/100 = 0.9975, so '99.75%' is the same number as 0.9975; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:439` | `91.07%` | `c1.expl.precision.r2.run` | `0.9107` | printed '91.07%' vs stored 0.9107; percentage form: 91.07/100 = 0.9107, so '91.07%' is the same number as 0.9107; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:439` | `92.86%` | `c1.expl.precision.r2.corr` | `0.9286` | printed '92.86%' vs stored 0.9286; percentage form: 92.86/100 = 0.9286, so '92.86%' is the same number as 0.9286; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:440` | `92.75%` | `c1.expl.precision.r3.run` | `0.9275` | printed '92.75%' vs stored 0.9275; percentage form: 92.75/100 = 0.9275, so '92.75%' is the same number as 0.9275; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:440` | `95.50%` | `c1.expl.precision.r3.corr` | `0.955` | printed '95.50%' vs stored 0.955; percentage form: 95.50/100 = 0.955, so '95.50%' is the same number as 0.955; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:441` | `84.71%` | `c1.expl.precision.r4.run` | `0.8471` | printed '84.71%' vs stored 0.8471; percentage form: 84.71/100 = 0.8471, so '84.71%' is the same number as 0.8471; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:441` | `12.53%` | `c1.expl.precision.r4.corr` | `0.1253` | printed '12.53%' vs stored 0.1253; percentage form: 12.53/100 = 0.1253, so '12.53%' is the same number as 0.1253; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:442` | `9.50%` | `c1.expl.over_refusal.run` | `0.095` | printed '9.50%' vs stored 0.095; percentage form: 9.50/100 = 0.095, so '9.50%' is the same number as 0.095; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:442` | `11.00%` | `c1.expl.over_refusal.corr` | `0.11` | printed '11.00%' vs stored 0.11; percentage form: 11.00/100 = 0.11, so '11.00%' is the same number as 0.11; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:443` | `0.00%` | `c1.h3.diff.run` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:443` | `-2.23%` | `c1.h3.diff.corr` | `-0.0223` | printed '-2.23%' vs stored -0.0223; percentage form: -2.23/100 = -0.0223, so '-2.23%' is the same number as -0.0223; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:444` | `74.58%` | `c1.b2.pooled.run` | `0.7458` | printed '74.58%' vs stored 0.7458; percentage form: 74.58/100 = 0.7458, so '74.58%' is the same number as 0.7458; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:444` | `99.73%` | `c1.b2.pooled.corr` | `0.9973` | printed '99.73%' vs stored 0.9973; percentage form: 99.73/100 = 0.9973, so '99.73%' is the same number as 0.9973; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:445` | `27.73%` | `c1.b2.coverage.run` | `0.2773` | printed '27.73%' vs stored 0.2773; percentage form: 27.73/100 = 0.2773, so '27.73%' is the same number as 0.2773; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:445` | `0.27%` | `c1.b2.coverage.corr` | `0.0027` | printed '0.27%' vs stored 0.0027; percentage form: 0.27/100 = 0.0027, so '0.27%' is the same number as 0.0027; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:451` | `12` | `c1.abl.all_12.n` | `12` | printed '12' vs stored 12; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:451` | `0.887` | `c1.abl.all_12.dev` | `0.887` | printed '0.887' vs stored 0.887; diff 0.000 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:451` | `0.874` | `c1.abl.all_12.test` | `0.8738` | printed '0.874' vs stored 0.8738; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:451` | `91.50%` | `c1.abl.all_12.over` | `0.915` | printed '91.50%' vs stored 0.915; percentage form: 91.50/100 = 0.915, so '91.50%' is the same number as 0.915; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:451` | `12.53%` | `c1.abl.all_12.r4` | `0.1253` | printed '12.53%' vs stored 0.1253; percentage form: 12.53/100 = 0.1253, so '12.53%' is the same number as 0.1253; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:452` | `4` | `c1.abl.dense_only.n` | `4` | printed '4' vs stored 4; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:452` | `0.888` | `c1.abl.dense_only.dev` | `0.8876` | printed '0.888' vs stored 0.8876; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:452` | `0.870` | `c1.abl.dense_only.test` | `0.8695` | printed '0.870' vs stored 0.8695; diff 0.0005 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:452` | `94.75%` | `c1.abl.dense_only.over` | `0.9475` | printed '94.75%' vs stored 0.9475; percentage form: 94.75/100 = 0.9475, so '94.75%' is the same number as 0.9475; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:452` | `23.06%` | `c1.abl.dense_only.r4` | `0.2306` | printed '23.06%' vs stored 0.2306; percentage form: 23.06/100 = 0.2306, so '23.06%' is the same number as 0.2306; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:453` | `1` | `c1.abl.lex_overlap_only.n` | `1` | printed '1' vs stored 1; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:453` | `0.812` | `c1.abl.lex_overlap_only.dev` | `0.8118` | printed '0.812' vs stored 0.8118; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:453` | `0.811` | `c1.abl.lex_overlap_only.test` | `0.8111` | printed '0.811' vs stored 0.8111; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:453` | `92.25%` | `c1.abl.lex_overlap_only.over` | `0.9225` | printed '92.25%' vs stored 0.9225; percentage form: 92.25/100 = 0.9225, so '92.25%' is the same number as 0.9225; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:453` | `10.03%` | `c1.abl.lex_overlap_only.r4` | `0.1003` | printed '10.03%' vs stored 0.1003; percentage form: 10.03/100 = 0.1003, so '10.03%' is the same number as 0.1003; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:454` | `7` | `c1.abl.no_bm25.n` | `7` | printed '7' vs stored 7; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:454` | `0.881` | `c1.abl.no_bm25.dev` | `0.8814` | printed '0.881' vs stored 0.8814; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:454` | `0.868` | `c1.abl.no_bm25.test` | `0.8683` | printed '0.868' vs stored 0.8683; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:454` | `91.25%` | `c1.abl.no_bm25.over` | `0.9125` | printed '91.25%' vs stored 0.9125; percentage form: 91.25/100 = 0.9125, so '91.25%' is the same number as 0.9125; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:454` | `12.53%` | `c1.abl.no_bm25.r4` | `0.1253` | printed '12.53%' vs stored 0.1253; percentage form: 12.53/100 = 0.1253, so '12.53%' is the same number as 0.1253; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:455` | `11` | `c1.abl.no_cross_encoder.n` | `11` | printed '11' vs stored 11; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:455` | `0.886` | `c1.abl.no_cross_encoder.dev` | `0.8857` | printed '0.886' vs stored 0.8857; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:455` | `0.872` | `c1.abl.no_cross_encoder.test` | `0.8715` | printed '0.872' vs stored 0.8715; diff 0.0005 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:455` | `93.75%` | `c1.abl.no_cross_encoder.over` | `0.9375` | printed '93.75%' vs stored 0.9375; percentage form: 93.75/100 = 0.9375, so '93.75%' is the same number as 0.9375; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:455` | `13.78%` | `c1.abl.no_cross_encoder.r4` | `0.1378` | printed '13.78%' vs stored 0.1378; percentage form: 13.78/100 = 0.1378, so '13.78%' is the same number as 0.1378; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:456` | `8` | `c1.abl.no_dense.n` | `8` | printed '8' vs stored 8; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:456` | `0.867` | `c1.abl.no_dense.dev` | `0.8669` | printed '0.867' vs stored 0.8669; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:456` | `0.862` | `c1.abl.no_dense.test` | `0.8623` | printed '0.862' vs stored 0.8623; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:456` | `87.75%` | `c1.abl.no_dense.over` | `0.8775` | printed '87.75%' vs stored 0.8775; percentage form: 87.75/100 = 0.8775, so '87.75%' is the same number as 0.8775; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:456` | `9.77%` | `c1.abl.no_dense.r4` | `0.0977` | printed '9.77%' vs stored 0.0977; percentage form: 9.77/100 = 0.0977, so '9.77%' is the same number as 0.0977; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:457` | `11` | `c1.abl.no_lex_overlap.n` | `11` | printed '11' vs stored 11; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:457` | `0.888` | `c1.abl.no_lex_overlap.dev` | `0.8877` | printed '0.888' vs stored 0.8877; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:457` | `0.874` | `c1.abl.no_lex_overlap.test` | `0.8742` | printed '0.874' vs stored 0.8742; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:457` | `90.50%` | `c1.abl.no_lex_overlap.over` | `0.905` | printed '90.50%' vs stored 0.905; percentage form: 90.50/100 = 0.905, so '90.50%' is the same number as 0.905; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:457` | `13.03%` | `c1.abl.no_lex_overlap.r4` | `0.1303` | printed '13.03%' vs stored 0.1303; percentage form: 13.03/100 = 0.1303, so '13.03%' is the same number as 0.1303; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:458` | `10` | `c1.abl.no_rank.n` | `10` | printed '10' vs stored 10; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:458` | `0.884` | `c1.abl.no_rank.dev` | `0.8845` | printed '0.884' vs stored 0.8845; diff 0.0005 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:458` | `0.872` | `c1.abl.no_rank.test` | `0.8718` | printed '0.872' vs stored 0.8718; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:458` | `92.25%` | `c1.abl.no_rank.over` | `0.9225` | printed '92.25%' vs stored 0.9225; percentage form: 92.25/100 = 0.9225, so '92.25%' is the same number as 0.9225; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:458` | `13.28%` | `c1.abl.no_rank.r4` | `0.1328` | printed '13.28%' vs stored 0.1328; percentage form: 13.28/100 = 0.1328, so '13.28%' is the same number as 0.1328; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:461` | `0.982` | `c1.auroc.test.run` | `0.9824` | printed '0.982' vs stored 0.9824; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:461` | `0.874` | `c1.auroc.test.corr` | `0.8738` | printed '0.874' vs stored 0.8738; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:464` | `99.75%` | `c1.expl.precision.r1.corr` | `0.9975` | printed '99.75%' vs stored 0.9975; percentage form: 99.75/100 = 0.9975, so '99.75%' is the same number as 0.9975; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:465` | `92.86%` | `c1.expl.precision.r2.corr` | `0.9286` | printed '92.86%' vs stored 0.9286; percentage form: 92.86/100 = 0.9286, so '92.86%' is the same number as 0.9286; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:466` | `95.50%` | `c1.expl.precision.r3.corr` | `0.955` | printed '95.50%' vs stored 0.955; percentage form: 95.50/100 = 0.955, so '95.50%' is the same number as 0.955; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:467` | `12.53%` | `c1.expl.precision.r4.corr` | `0.1253` | printed '12.53%' vs stored 0.1253; percentage form: 12.53/100 = 0.1253, so '12.53%' is the same number as 0.1253; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:472` | `0.00%` | `c1.h1.diff.corr` | `0.0` | printed '0.00%' vs stored 0.0; percentage form: 0.00/100 = 0.00, so '0.00%' is the same number as 0.0; diff 0.00 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:474` | `-2.23%` | `c1.h3.diff.corr` | `-0.0223` | printed '-2.23%' vs stored -0.0223; percentage form: -2.23/100 = -0.0223, so '-2.23%' is the same number as -0.0223; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:475` | `-3.11%` | `c1.h3.diff.lo.corr` | `-0.0311` | printed '-3.11%' vs stored -0.0311; percentage form: -3.11/100 = -0.0311, so '-3.11%' is the same number as -0.0311; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:475` | `-1.35%` | `c1.h3.diff.hi.corr` | `-0.0135` | printed '-1.35%' vs stored -0.0135; percentage form: -1.35/100 = -0.0135, so '-1.35%' is the same number as -0.0135; diff 0.0000 <= allowed 0.00005 (half last decimal 0.00005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:477` | `0.80` | `c1.const.target_precision` | `0.8` | printed '0.80' vs stored 0.8; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:479` | `11.00%` | `c1.expl.over_refusal.corr` | `0.11` | printed '11.00%' vs stored 0.11; percentage form: 11.00/100 = 0.11, so '11.00%' is the same number as 0.11; diff 0.00 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:480` | `0.10` | `c1.const.over_cap` | `0.1` | printed '0.10' vs stored 0.1; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:483` | `99.73%` | `c1.b2.pooled.corr` | `0.9973` | printed '99.73%' vs stored 0.9973; percentage form: 99.73/100 = 0.9973, so '99.73%' is the same number as 0.9973; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:484` | `0.27%` | `c1.b2.coverage.corr` | `0.0027` | printed '0.27%' vs stored 0.0027; percentage form: 0.27/100 = 0.0027, so '0.27%' is the same number as 0.0027; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:490` | `0.862` | `c1.abl.no_dense.test` | `0.8623` | printed '0.862' vs stored 0.8623; diff 0.0003 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:491` | `0.874` | `c1.abl.all_12.test` | `0.8738` | printed '0.874' vs stored 0.8738; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:492` | `0.811` | `c1.abl.lex_overlap_only.test` | `0.8111` | printed '0.811' vs stored 0.8111; diff 0.0001 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:501` | `273` | `c1.st.exch.kept.dev` | `273` | printed '273' vs stored 273; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:502` | `127` | `c1.st.exch.dropped.dev` | `127` | printed '127' vs stored 127; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:504` | `0.052` | `c1.st.exch.p` | `0.052366` | printed '0.052' vs stored 0.052366; diff 0.000366 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:510` | `0.45` | `c1.st.cluster.ratio.conf.r2` | `0.4521` | printed '0.45' vs stored 0.4521; diff 0.0021 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:511` | `1.17` | `c1.st.cluster.ratio.expl.r4` | `1.1658` | printed '1.17' vs stored 1.1658; diff 0.0042 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:518` | `0.00` | `c1.st.match.maxdiff` | `0.0` | printed '0.00' vs stored 0.0; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:522` | `553` | `c1.reader.n` | `553` | printed '553' vs stored 553; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:524` | `0.419` | `c1.reader.auroc` | `0.4192` | printed '0.419' vs stored 0.4192; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:537` | `400` | `c1.data.transfer.items` | `400` | printed '400' vs stored 400; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:539` | `98.50%` | `c1.tr.precision.conf` | `0.985` | printed '98.50%' vs stored 0.985; percentage form: 98.50/100 = 0.985, so '98.50%' is the same number as 0.985; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:540` | `89.50%` | `c1.tr.over_refusal.conf` | `0.895` | printed '89.50%' vs stored 0.895; percentage form: 89.50/100 = 0.895, so '89.50%' is the same number as 0.895; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:542` | `85.50%` | `c1.tr.precision.expl` | `0.855` | printed '85.50%' vs stored 0.855; percentage form: 85.50/100 = 0.855, so '85.50%' is the same number as 0.855; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:542` | `79.50%` | `c1.tr.ci.lo` | `0.795` | printed '79.50%' vs stored 0.795; percentage form: 79.50/100 = 0.795, so '79.50%' is the same number as 0.795; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:543` | `89.50%` | `c1.tr.ci.hi` | `0.895` | printed '89.50%' vs stored 0.895; percentage form: 89.50/100 = 0.895, so '89.50%' is the same number as 0.895; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:544` | `7.25` | `c1.tr.drop.expl` | `7.25` | printed '7.25' vs stored 7.25; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:545` | `0.982` | `c1.auroc.test.run` | `0.9824` | printed '0.982' vs stored 0.9824; diff 0.0004 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:546` | `0.640` | `c1.tr.auroc` | `0.6402` | printed '0.640' vs stored 0.6402; diff 0.0002 <= allowed 0.0005 (half last decimal 0.0005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:556` | `0.80` | `c1.const.target_precision` | `0.8` | printed '0.80' vs stored 0.8; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |
| `05_paper/draft/paper.md:558` | `24.50%` | `c1.pm.band.answer_rate` | `0.245` | printed '24.50%' vs stored 0.245; percentage form: 24.50/100 = 0.245, so '24.50%' is the same number as 0.245; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:559` | `83.03%` | `c1.pm.band.pooled_precision` | `0.8303` | printed '83.03%' vs stored 0.8303; percentage form: 83.03/100 = 0.8303, so '83.03%' is the same number as 0.8303; diff 0.0000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:562` | `75.50%` | `c1.band.over_refusal.run` | `0.755` | printed '75.50%' vs stored 0.755; percentage form: 75.50/100 = 0.755, so '75.50%' is the same number as 0.755; diff 0.000 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `05_paper/draft/paper.md:602` | `273` | `c1.items.rung2.dev` | `273` | printed '273' vs stored 273; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:603` | `280` | `c1.pm.n.r2` | `280` | printed '280' vs stored 280; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0) |
| `05_paper/draft/paper.md:608` | `553` | `c1.reader.n` | `553` | printed '553' vs stored 553; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `05_paper/draft/paper.md:609` | `1873` | `c1.items.dev` | `1873` | printed '1873' vs stored 1873; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |

## Exemptions used

| rule | count | example | why it is not a result |
|------|-------|---------|------------------------|
| `arxiv_id` | 21 | `2403.01461` | arXiv identifier (arXiv:1706.03762) |
| `config_exempt` | 11 | `95%` | number covered by a pattern in the --exempt config file |
| `doi` | 2 | `10.18653` | digits inside a DOI (10.xxxx/...) |
| `file_path` | 32 | `05` | digits inside a file path (fig/plot3.pdf) |
| `float_prefix` | 21 | `3` | number right after Figure/Table/Eq./Section/Algorithm/... (a label) |
| `identifier_attached` | 16 | `1` | digit glued to a name (GPT-4, ResNet-50, v2, L2) |
| `list_marker` | 13 | `1` | ordered-list numbering ('1.', '2)') at the start of a line |
| `section_number` | 53 | `7` | numbering of a Markdown heading ('## 3.1 Method') or after § |
| `year` | 9 | `2024` | a bare 4-digit integer 1900-2100 (a calendar year, not a measurement) |

## Rules this run applied

Exemptions are narrow by construction: each rule below is a named, fixed pattern in `tools/check_numbers.py` (or a pattern you supplied via `--exempt`). No catch-all.

- `year` — a bare 4-digit integer 1900-2100 (a calendar year, not a measurement)
- `section_number` — numbering of a Markdown heading ('## 3.1 Method') or after §
- `float_prefix` — number right after Figure/Table/Eq./Section/Algorithm/... (a label)
- `page_line` — number after p./pp./page/line, including ranges (12-14)
- `list_marker` — ordered-list numbering ('1.', '2)') at the start of a line
- `citation_number` — bracketed citation numbers: [12], [3, 5], [12-14]
- `doi` — digits inside a DOI (10.xxxx/...)
- `arxiv_id` — arXiv identifier (arXiv:1706.03762)
- `url` — digits inside an http(s):// or www. URL
- `file_path` — digits inside a file path (fig/plot3.pdf)
- `iso_date` — ISO date 2026-11-03
- `footnote_marker` — markdown footnote reference [^1]
- `latex_command_arg` — argument of \ref \label \cite \includegraphics \begin ...
- `latex_dimension` — LaTeX length: 11pt, 0.9\textwidth, width=0.5\linewidth
- `identifier_attached` — digit glued to a name (GPT-4, ResNet-50, v2, L2)
- `equation_number` — a bracketed integer or one-decimal section number: equation (1), section (2.1)
- `config_exempt` — number covered by a pattern in the --exempt config file

Extra patterns from `04_experiments/config/exempt_numbers.json`:

- `learning[-_ ]?rate\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9.]+(?:[eE][-+]?[0-9]+)?`
- `\blr\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9.]+(?:[eE][-+]?[0-9]+)?`
- `dropout(?:\s*(?:rate|probability|p))?\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9.]+`
- `batch[-_ ]?size\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9,]+`
- `\bepochs?\s*(?:=\s*|:\s*)[0-9,]+`
- `\b[0-9]+\s*epochs?\b`
- `\bseed\s*(?:=\s*|:\s*)?[0-9]+`
- `\b[0-9]+-fold\b`
- `\b[0-9]{2}/[0-9]{2}\s*(?:train|test|validation|split)\b`
- `\b(?:max|min)[-_ ]?(?:len|length|tokens|new[-_ ]?tokens)\s*(?:=\s*|:\s*|of\s+)[0-9,]+`
- `\bwarm[-_ ]?up\s*(?:=\s*|:\s*|of\s+)[0-9,]+`
- `\b[0-9]+\s*(?:hidden\s+)?(?:units|layers|heads)\b`
- `\b[0-9]+\s*-\s*(?:layer|unit|head)\b`
- `\b[0-9]+\s+(?:[a-z]+\s+)?(?:attention\s+heads|units|layers|heads|dimensions)\b`
- `\b95\s*%\s*(?:CI\b|confidence)`

A number passes only if it is inside a `num:` marker whose id is in the results index and whose stored value matches (percentages allowed, rounding allowed up to half of the last printed decimal place), or if one of the rules above applies. Everything else must be fixed before the draft is called done (RULES.md #2).
