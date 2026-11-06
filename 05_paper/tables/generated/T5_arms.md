| Arm (all exploratory) | Abstain precision | 95% CI | Over-refusal | Discrimination |
|---|---:|---|---:|---:|
| Rung R5, confirmatory band | <!-- num:c1.r5.precision.conf -->100.00%<!-- /num --> | [<!-- num:c1.r5.ci.lo -->100.00%<!-- /num -->, <!-- num:c1.r5.ci.hi -->100.00%<!-- /num -->] | degenerate, see §4.4 | <!-- num:c1.r5.auroc -->0.974<!-- /num --> |
| Rung R5, exploratory band | <!-- num:c1.r5.precision.expl -->89.25%<!-- /num --> | [<!-- num:c1.r5.expl.ci.lo -->85.75%<!-- /num -->, <!-- num:c1.r5.expl.ci.hi -->91.75%<!-- /num -->] | matching residue <!-- num:c1.r5.match.mean_absdiff -->10.29%<!-- /num --> | <!-- num:c1.r5.auroc -->0.974<!-- /num --> |
| Second-corpus arm, confirmatory band | <!-- num:c1.tr.precision.conf -->98.50%<!-- /num --> | not informative | <!-- num:c1.tr.over_refusal.conf -->89.50%<!-- /num --> | <!-- num:c1.tr.auroc -->0.640<!-- /num --> |
| Second-corpus arm, exploratory band | <!-- num:c1.tr.precision.expl -->85.50%<!-- /num --> | [<!-- num:c1.tr.ci.lo -->79.50%<!-- /num -->, <!-- num:c1.tr.ci.hi -->89.50%<!-- /num -->] | <!-- num:c1.tr.over_refusal.expl -->57.50%<!-- /num --> | <!-- num:c1.tr.auroc -->0.640<!-- /num --> |
| Top-1 presented (hit rate <!-- num:c1.t1.hit.test -->78.25%<!-- /num -->) | <!-- num:c1.t1.precision.miss -->87.30%<!-- /num --> P(miss | refused) | not informative | <!-- num:c1.t1.refuse.hit -->2.56%<!-- /num --> of hits refused | <!-- num:c1.t1.auroc -->0.945<!-- /num --> |

Every arm here is exploratory. R5 and the top-1 variant are declared deviations (D2, D3). The second-corpus arm is H2's pre-declared second corpus, but its construct differs (no article grouping, shorter passages, multi-hop questions), so it supports a direction claim only.
