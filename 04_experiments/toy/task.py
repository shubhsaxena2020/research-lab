#!/usr/bin/env python
"""TOY - NOT A RESULT

Synthetic two-class classification task used only to exercise the experiment
harness end to end.  Nothing here is a scientific claim and no number produced
by this file may be cited anywhere.

Two baselines, stdlib only (no numpy needed):

* ``centroid`` -- nearest class mean (the "baseline" config);
* ``logistic`` -- binary logistic regression trained from scratch with
  full-batch gradient descent on the log loss (the "ours" config).

Data: two anisotropic gaussian blobs (class 0 is wider along one axis, class 1
along the other) rotated by a fixed angle, drawn from ``random.Random(seed)``,
so a given seed always produces exactly the same dataset.

``run_task(config) -> dict`` returns the flat metric dict the runner persists:
``accuracy``, ``f1_macro``, ``loss``, ``accuracy_train``, ``n_train``,
``n_test``.
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Sequence, Tuple

TOY = True
BANNER = "TOY - NOT A RESULT"

Point = Tuple[float, float]


# --------------------------------------------------------------------------- #
# data
# --------------------------------------------------------------------------- #
def make_blobs(n_per_class: int = 150, sep: float = 2.2, std_a: float = 1.3,
               std_b: float = 0.8, angle_deg: float = 20.0,
               seed: int = 0) -> Tuple[List[Point], List[int]]:
    """Deterministic two-class dataset (points already rotated)."""
    rng = random.Random(int(seed))
    theta = math.radians(angle_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    points: List[Point] = []
    labels: List[int] = []
    for label, (cx, sa, sb) in enumerate(((-sep / 2.0, std_a, std_b),
                                         (+sep / 2.0, std_b, std_a))):
        for _ in range(int(n_per_class)):
            u = rng.gauss(0.0, sa)
            v = rng.gauss(0.0, sb)
            x = cx + u
            y = v
            points.append((x * cos_t - y * sin_t, x * sin_t + y * cos_t))
            labels.append(label)
    return points, labels


def train_test_split(points: Sequence[Point], labels: Sequence[int], test_frac: float = 0.3,
                     seed: int = 0) -> Tuple[List[Point], List[int], List[Point], List[int]]:
    order = list(range(len(points)))
    random.Random(int(seed) + 7919).shuffle(order)
    n_test = max(1, int(round(len(order) * test_frac)))
    test_idx = set(order[:n_test])
    x_tr, y_tr, x_te, y_te = [], [], [], []
    for i in order:
        if i in test_idx:
            x_te.append(points[i])
            y_te.append(labels[i])
        else:
            x_tr.append(points[i])
            y_tr.append(labels[i])
    return x_tr, y_tr, x_te, y_te


# --------------------------------------------------------------------------- #
# models
# --------------------------------------------------------------------------- #
def fit_centroid(x: Sequence[Point], y: Sequence[int]) -> List[Point]:
    sums = [[0.0, 0.0], [0.0, 0.0]]
    counts = [0, 0]
    for point, label in zip(x, y):
        sums[label][0] += point[0]
        sums[label][1] += point[1]
        counts[label] += 1
    return [(sums[c][0] / max(counts[c], 1), sums[c][1] / max(counts[c], 1)) for c in (0, 1)]


def predict_centroid(centroids: Sequence[Point], x: Sequence[Point]) -> List[int]:
    out = []
    for point in x:
        d0 = (point[0] - centroids[0][0]) ** 2 + (point[1] - centroids[0][1]) ** 2
        d1 = (point[0] - centroids[1][0]) ** 2 + (point[1] - centroids[1][1]) ** 2
        out.append(0 if d0 <= d1 else 1)
    return out


def standardize(x_train: Sequence[Point], x_test: Sequence[Point]) -> Tuple[List[Point], List[Point]]:
    n = len(x_train)
    mean = [sum(p[j] for p in x_train) / n for j in (0, 1)]
    std = []
    for j in (0, 1):
        var = sum((p[j] - mean[j]) ** 2 for p in x_train) / max(n - 1, 1)
        std.append(math.sqrt(var) or 1.0)
    norm = lambda pts: [((p[0] - mean[0]) / std[0], (p[1] - mean[1]) / std[1]) for p in pts]
    return norm(x_train), norm(x_test)


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def fit_logistic(x: Sequence[Point], y: Sequence[int], epochs: int = 400, lr: float = 0.5,
                 l2: float = 0.0) -> Tuple[List[float], float]:
    """Full-batch GD on mean log loss; deterministic zero init."""
    w = [0.0, 0.0]
    b = 0.0
    n = len(x)
    for _ in range(int(epochs)):
        gw = [0.0, 0.0]
        gb = 0.0
        for (x0, x1), label in zip(x, y):
            p = _sigmoid(b + w[0] * x0 + w[1] * x1)
            err = p - label
            gw[0] += err * x0
            gw[1] += err * x1
            gb += err
        for j in (0, 1):
            w[j] -= lr * (gw[j] / n + l2 * w[j])
        b -= lr * gb / n
    return w, b


def predict_logistic(model: Tuple[Sequence[float], float], x: Sequence[Point]) -> List[int]:
    w, b = model
    return [1 if _sigmoid(b + w[0] * p[0] + w[1] * p[1]) >= 0.5 else 0 for p in x]


def log_loss(model: Tuple[Sequence[float], float], x: Sequence[Point],
             y: Sequence[int]) -> float:
    w, b = model
    total = 0.0
    for point, label in zip(x, y):
        p = min(max(_sigmoid(b + w[0] * point[0] + w[1] * point[1]), 1e-12), 1 - 1e-12)
        total += -(label * math.log(p) + (1 - label) * math.log(1 - p))
    return total / max(len(x), 1)


# --------------------------------------------------------------------------- #
# metrics
# --------------------------------------------------------------------------- #
def accuracy(y_true: Sequence[int], y_pred: Sequence[int]) -> float:
    if not y_true:
        return 0.0
    return sum(int(a == b) for a, b in zip(y_true, y_pred)) / len(y_true)


def f1_macro(y_true: Sequence[int], y_pred: Sequence[int]) -> float:
    scores = []
    for cls in (0, 1):
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        denom = 2 * tp + fp + fn
        scores.append((2 * tp / denom) if denom else 0.0)
    return sum(scores) / len(scores)


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #
def run_task(config: Dict[str, Any]) -> Dict[str, Any]:
    """Run one toy configuration; returns a flat metrics dict."""
    seed = int(config.get("seed", 0))
    model_name = str(config.get("model", "logistic"))
    if model_name not in ("centroid", "logistic"):
        raise ValueError(f"unknown toy model {model_name!r}; use 'centroid' or 'logistic'")

    points, labels = make_blobs(
        n_per_class=int(config.get("n_per_class", 150)),
        sep=float(config.get("sep", 2.2)),
        std_a=float(config.get("std_a", 1.3)),
        std_b=float(config.get("std_b", 0.8)),
        angle_deg=float(config.get("angle_deg", 20.0)),
        seed=seed,
    )
    x_tr, y_tr, x_te, y_te = train_test_split(points, labels, seed=seed)

    if model_name == "centroid":
        centroids = fit_centroid(x_tr, y_tr)
        pred_te = predict_centroid(centroids, x_te)
        pred_tr = predict_centroid(centroids, x_tr)
        loss = None
    else:
        xtr_s, xte_s = standardize(x_tr, x_te)
        model = fit_logistic(xtr_s, y_tr,
                             epochs=int(config.get("epochs", 400)),
                             lr=float(config.get("lr", 0.5)),
                             l2=float(config.get("l2", 0.0)))
        pred_te = predict_logistic(model, xte_s)
        pred_tr = predict_logistic(model, xtr_s)
        loss = round(log_loss(model, xte_s, y_te), 6)

    metrics: Dict[str, Any] = {
        "accuracy": round(accuracy(y_te, pred_te), 6),
        "accuracy_train": round(accuracy(y_tr, pred_tr), 6),
        "f1_macro": round(f1_macro(y_te, pred_te), 6),
        "n_train": len(x_tr),
        "n_test": len(x_te),
        "model": model_name,
    }
    if loss is not None:
        metrics["loss"] = loss
    print(f"[toy] model={model_name} seed={seed} "
          f"acc={metrics['accuracy']:.4f} f1={metrics['f1_macro']:.4f} "
          f"n_train={metrics['n_train']} n_test={metrics['n_test']}")
    return metrics


if __name__ == "__main__":
    import json

    print(BANNER)
    print(json.dumps(run_task({"seed": 0, "model": "logistic"}), indent=2, sort_keys=True))
