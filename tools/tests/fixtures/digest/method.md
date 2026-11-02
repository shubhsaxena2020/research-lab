# Method

We study whether a small retrieval module improves short-answer grading. This section describes the pipeline we built and the choices a reader would need to repeat it.

The pipeline has three stages: clean the answer text, retrieve the closest reference answer, and score the pair with a small classifier. Each stage is deterministic except the classifier's initialisation, which we fix with a seed.

We train the classifier on 1200 labelled pairs and hold out 300 for testing. We report accuracy <!-- num:main.accuracy.baseline -->0.812<!-- /num --> for the baseline and macro F1 for every configuration.

Our retrieval step follows the dual-encoder design of \cite{reimers2019}, adapted to short answers. We use a fixed learning rate and early stopping on the validation split.

We also run an ablation study that removes the retrieval stage. We do not optimise BLEU because the task is graded short answers, not translation.

Every run uses the same split and seed, and the exact command is recorded in the run metadata. We report negative results in the results section rather than hiding them.
