# 4 Results

We evaluate on the test split of the public benchmark released in 2024 [12]. The setup
follows prior work [3, 5] and the protocol described in Section 2.2; Figure 2 shows the
data pipeline and Table 1 lists every hyperparameter. Code and predictions are archived at
https://example.org/archive/v1.2, and the baseline is the implementation from
arXiv:1706.03762 (doi:10.48550/arXiv.1706.03762), described on pp. 12-14 of its appendix.

## 4.1 Training details

We train for 30 epochs with a batch size of 32 and a learning rate of 3e-4, using 10-fold
cross-validation on the development split. Every configuration is run from a fixed seed so
that the same command reproduces the same table.

## 4.2 Main results

The baseline reaches <!-- num:main.accuracy.baseline -->0.812<!-- /num --> test accuracy and
<!-- num:main.f1.baseline -->0.79<!-- /num --> macro F1, while our model reaches
<!-- num:main.accuracy.ours -->0.910<!-- /num --> accuracy, i.e.
<!-- num:main.accuracy.ours -->91.0%<!-- /num -->, at
<!-- num:main.speedup.ours -->3.5x<!-- /num --> the training speed. Over
<!-- num:main.seeds -->5<!-- /num --> seeds the baseline has a standard deviation of
<!-- num:main.std.baseline -->0.0075<!-- /num -->, and a paired Wilcoxon test gives
p = <!-- num:main.p.paired -->0.031<!-- /num -->. All numbers are computed from
<!-- num:main.n -->1,000<!-- /num --> held-out examples, as recorded in Eq. (3).

| Model | Accuracy | Macro F1 | Runs |
|-------|----------|----------|------|
| Baseline | <!-- num:main.accuracy.baseline -->0.812<!-- /num --> | <!-- num:main.f1.baseline -->0.79<!-- /num --> | <!-- num:main.seeds -->5<!-- /num --> |
| Ours | <!-- num:main.accuracy.ours -->0.910<!-- /num --> | <!-- num:main.f1.ours -->0.903<!-- /num --> | <!-- num:main.seeds -->5<!-- /num --> |

Two steps remain before submission:

1. Re-run the baseline with the archived config (Section 3.1).
2. Check the confidence intervals reported in Figure 3.
