# TOY DRAFT — NOT A RESULT

> This file exists only to exercise the toolchain end to end (PROMPT.md S3 Phase One
> fallback). Every number here is synthetic and must never be cited.

## Abstract

We compare a nearest-centroid baseline against a logistic-regression classifier on a
synthetic two-blob task. The baseline reaches an accuracy of
<!-- num:toy.accuracy.toy_baseline -->0.8704<!-- /num -->, while the logistic classifier
reaches <!-- num:toy.accuracy.toy_ours -->0.8852<!-- /num -->.

## Introduction

Retrieval and classification systems are usually measured against a simple centroid
baseline before a learned model is claimed to add anything. This toy note records that
comparison on a synthetic task, purely so the surrounding toolchain can be exercised
end to end.

## Method

Both models are trained on <!-- num:toy.protocol.n_per_class -->150<!-- /num --> points
per class drawn from two anisotropic gaussian blobs. The baseline assigns each point to
the nearest class centroid; the treatment fits a logistic classifier by full-batch
gradient descent for <!-- num:toy.protocol.epochs -->400<!-- /num --> epochs at a learning
rate of <!-- num:toy.protocol.lr -->0.5<!-- /num -->. We report the mean over
<!-- num:toy.protocol.n_seeds -->3<!-- /num --> seeds on the held-out split.

## Results

The treatment is higher on every one of the <!-- num:toy.protocol.n_pairs -->3<!-- /num -->
paired seeds, but with that few pairs the smallest attainable two-sided sign-test
p-value is <!-- num:toy.protocol.p -->0.50<!-- /num -->, so we make no claim of
significance. The confidence interval is reported only as indicative.

## Limitations

Three seeds is far too few for a confidence interval to be trusted, and the task is
synthetic, so nothing here transfers to a real dataset.
