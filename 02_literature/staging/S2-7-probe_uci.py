"""S2-7 sanity probe on the UCI SMS Spam Collection (CC BY 4.0, DOI 10.24432/C5CC84).

Answers three decision-critical questions with OUR OWN measurement instead of a
remembered number:
  1. how much of the task a hand-written keyword rule already solves (ceiling probe)
  2. how much headroom a TF-IDF + logistic-regression model has over that rule
  3. how many exact / near-duplicate messages exist (split-leakage risk)

Dependencies: numpy only (sklearn is not installed on this machine). Deterministic.
Run:  python 02_literature/staging/S2-7-probe_uci.py
"""
import io
import re
import zlib
import zipfile
import urllib.request

import numpy as np

URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

# A deliberately naive rule a student would actually write: classic spam vocabulary.
KEYWORDS = [
    "free", "win", "winner", "prize", "claim", "urgent", "txt", "text ",
    "cash", "award", "guaranteed", "congrat", "http", "www.", "pound", "$",
    "reply", "stop", "unsubscribe", "bonus", "ringtone", "voucher", "selected",
    "call ",
]


def load():
    raw = urllib.request.urlopen(URL, timeout=90).read()
    zf = zipfile.ZipFile(io.BytesIO(raw))
    text = zf.read("SMSSpamCollection").decode("utf-8", "replace")
    labels, msgs = [], []
    for line in text.splitlines():
        if not line.strip():
            continue
        lab, msg = line.split("\t", 1)
        labels.append(1 if lab.strip() == "spam" else 0)
        msgs.append(msg.strip())
    return np.array(labels, dtype=np.int64), msgs


def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(m):
    w = norm(m).split()
    return w + [a + "_" + b for a, b in zip(w, w[1:])]   # unigrams + bigrams


def hashed_csr(msgs, n_buckets=1 << 17):
    data, indices, indptr = [], [], [0]
    for m in msgs:
        cnt = {}
        for t in tokens(m):
            k = zlib.crc32(t.encode()) % n_buckets
            cnt[k] = cnt.get(k, 0) + 1
        for k in sorted(cnt):
            indices.append(k)
            data.append(1.0 + np.log(cnt[k]))
        indptr.append(len(data))
    return (np.asarray(data, np.float64), np.asarray(indices, np.int64),
            np.asarray(indptr, np.int64), len(msgs), n_buckets)


def tfidf_transform(data, indices, indptr, n, n_buckets):
    df = np.zeros(n_buckets)
    for i in range(n):
        df[indices[indptr[i]:indptr[i + 1]]] += 1.0
    idf = np.log((1.0 + n) / (1.0 + df)) + 1.0
    out_v = []
    for i in range(n):
        s, e = indptr[i], indptr[i + 1]
        v = data[s:e] * idf[indices[s:e]]
        nrm = np.sqrt((v * v).sum()) or 1.0
        out_v.append(v / nrm)
    return np.concatenate(out_v)


def spmv(idx, val, indptr, w):
    if len(val) == 0:
        return np.zeros(len(indptr) - 1)
    full = val * w[idx]
    return np.add.reduceat(full, indptr[:-1])


def train_logreg(idx, val, indptr, y, n_feat, epochs=300, lr=3.0, l2=1e-5):
    n = len(y)
    w = np.zeros(n_feat)
    sw = np.where(y == 1, 0.5 * n / max(y.sum(), 1), 0.5 * n / max((1 - y).sum(), 1))
    lens = np.diff(indptr)
    for _ in range(epochs):
        z = spmv(idx, val, indptr, w)
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        g = (p - y) * sw / n
        gw = np.zeros_like(w)
        np.add.at(gw, idx, val * np.repeat(g, lens))
        w -= lr * (gw + l2 * w)
    return w


def score(idx, val, indptr, w):
    z = spmv(idx, val, indptr, w)
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def prf(y, p):
    tp = int(((p == 1) & (y == 1)).sum())
    fp = int(((p == 1) & (y == 0)).sum())
    fn = int(((p == 0) & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1, fp, fn


def main():
    y, msgs = load()
    n = len(y)
    print(f"n={n} spam={int(y.sum())} ({y.mean()*100:.1f}%) ham={int((1-y).sum())}")
    L = np.array([len(m) for m in msgs])
    print(f"chars: mean={L.mean():.1f} median={np.median(L):.0f} p95={np.percentile(L,95):.0f}")

    kp = np.array([1 if any(k in (" " + m.lower() + " ") for k in KEYWORDS) else 0 for m in msgs])
    pr, rc, f1, fp, fn = prf(y, kp)
    print(f"KEYWORD RULE    P={pr:.3f} R={rc:.3f} F1={f1:.3f}  fires on {kp.mean()*100:.1f}%  FP={fp} FN={fn}")

    data, idx, indptr, nrows, nb = hashed_csr(msgs)
    val = tfidf_transform(data, idx, indptr, nrows, nb)

    rng = np.random.RandomState(7)
    order = rng.permutation(n)
    folds = np.zeros(n, dtype=int)
    for f in range(5):
        folds[order[f::5]] = f

    proba = np.zeros(n)
    for f in range(5):
        tr = np.where(folds != f)[0]
        te = np.where(folds == f)[0]
        # rebuild idf inside the training fold only (no test-fold leakage)
        tr_i = np.concatenate([idx[indptr[i]:indptr[i+1]] for i in tr])
        tr_v = np.concatenate([val[indptr[i]:indptr[i+1]] for i in tr])
        tr_ptr = np.concatenate([[0], np.cumsum([indptr[i+1] - indptr[i] for i in tr])])
        w = train_logreg(tr_i, tr_v, tr_ptr, y[tr], nb)
        te_i = np.concatenate([idx[indptr[i]:indptr[i+1]] for i in te])
        te_v = np.concatenate([val[indptr[i]:indptr[i+1]] for i in te])
        te_ptr = np.concatenate([[0], np.cumsum([indptr[i+1] - indptr[i] for i in te])])
        proba[te] = score(te_i, te_v, te_ptr, w)

    for thr in (0.5, 0.9, 0.99):
        p = (proba >= thr).astype(int)
        pr, rc, f1, fp, fn = prf(y, p)
        print(f"TFIDF+LR thr={thr:<5} P={pr:.3f} R={rc:.3f} F1={f1:.3f} FP={fp} FN={fn}")

    seen, dup = set(), 0
    for m in msgs:
        k = norm(m)
        if k in seen:
            dup += 1
        seen.add(k)
    print(f"exact-normalised duplicates: {dup}/{n} ({dup/n*100:.1f}%)")

    tok = [tokens(m) for m in msgs]
    sh = [set(zip(t, t[1:], t[2:])) for t in tok]
    near = 0
    for i in range(n):
        si = sh[i]
        if not si:
            continue
        for j in range(i + 1, n):
            sj = sh[j]
            inter = len(si & sj)
            if inter >= 0.8 * max(1, min(len(si), len(sj))):
                near += 1
                break
    print(f"messages with a >=0.8-shingle near-duplicate: {near}/{n} ({near/n*100:.1f}%)")

    url = sum(1 for m, l in zip(msgs, y) if l == 1 and re.search(r"http|www\.", m, re.I))
    print(f"spam containing a URL: {url}/{int(y.sum())} ({url/y.sum()*100:.1f}%)")


if __name__ == "__main__":
    main()
