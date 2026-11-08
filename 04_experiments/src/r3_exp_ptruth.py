"""R3 exploratory: P(True)-style reader baseline (Kadavath et al. 2207.05221).

Given question + passage + a proposed answer, ask the local Ollama model
(qwen2.5:1.5b-instruct) whether the proposed answer is true and take
P(True) = softmax(logprob("True"), logprob("False")) over the first generated
token. Run on the 553 dev items that have reader scores (reader_features.csv).

Exploratory / post-hoc: not part of the pre-registered gate. The reader model
here (Qwen2.5-1.5B-Instruct via Ollama) differs from the paper's pinned reader
(Qwen/Qwen2.5-0.5B-Instruct); this is disclosed in the summary and COMPUTE.md.

CLI
---
    python 04_experiments/src/r3_exp_ptruth.py
    python 04_experiments/src/r3_exp_ptruth.py --limit 5
    python 04_experiments/src/r3_exp_ptruth.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shlex
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_experiments" / "data"
ITEMS = DATA / "items.jsonl"
READER_FEATURES = DATA / "reader_features.csv"
OUT_DIR = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp"
OUT_CSV = OUT_DIR / "ptruth_scores.csv"
OUT_JSON = OUT_DIR / "ptruth_summary.json"
ERR_CSV = OUT_DIR / "ptruth_errors.csv"
LOCK = ROOT / "ops" / "HEAVY.lock"

DEFAULT_MODEL = "qwen2.5:1.5b-instruct"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
CSV_HEADER = ["item_id", "label", "rung", "proposed_answer", "ptruth", "logprob_true", "logprob_false"]
ERROR_HEADER = ["item_id", "error", "ts_utc"]
MAX_CONTEXT_CHARS = 8000
TIMEOUT_S = 60


# --------------------------------------------------------------------------------------------------
# pure functions (unit-tested without Ollama)
# --------------------------------------------------------------------------------------------------
def clip_context(context: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    if len(context) <= max_chars:
        return context
    head = max_chars * 2 // 3
    tail = max_chars - head
    return context[:head] + " ... " + context[-tail:]


def build_prompt(item: dict, proposed_answer: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    passage = clip_context(str(item.get("context") or "").strip(), max_chars)
    question = str(item.get("question") or "").strip()
    pa = str(proposed_answer or "").strip()
    return (
        f"Passage:\n{passage}\n\n"
        f"Question: {question}\n\n"
        f"Proposed answer: {pa}\n\n"
        "Is the proposed answer true? Reply with only True or False.\n"
    )


def find_true_false_logprobs(top_logprobs: list) -> tuple[float | None, float | None]:
    """Extract logprob('True') and logprob('False') from an Ollama top_logprobs list."""
    lp_true = None
    lp_false = None
    for entry in (top_logprobs or []):
        if not isinstance(entry, dict):
            continue
        tok = str(entry.get("token", "")).strip().lower()
        try:
            lp = float(entry.get("logprob"))
        except (TypeError, ValueError):
            continue
        if tok == "true":
            lp_true = lp
        elif tok == "false":
            lp_false = lp
    return lp_true, lp_false


def ptruth_from_logprobs(lp_true, lp_false) -> float | None:
    if lp_true is None or lp_false is None:
        return None
    m = max(float(lp_true), float(lp_false))
    et = math.exp(float(lp_true) - m)
    ef = math.exp(float(lp_false) - m)
    denom = et + ef
    if denom == 0:
        return None
    return float(et / denom)


def parse_ollama_response_lines(lines) -> tuple[float | None, float | None, str | None, str | None]:
    """Parse streamed Ollama /api/generate lines. Returns (lp_true, lp_false, first_token, error)."""
    first_entry = None
    for raw in lines:
        raw = raw.strip() if hasattr(raw, "strip") else raw
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        lps = obj.get("logprobs")
        if lps and first_entry is None:
            # lps is a list with one entry for the first generated token
            first_entry = lps[0] if isinstance(lps, list) and lps else None
        if isinstance(obj, dict) and obj.get("done"):
            break
    if first_entry is None:
        return None, None, None, "no logprobs in response"
    first_token = first_entry.get("token") if isinstance(first_entry, dict) else None
    candidates = []
    if isinstance(first_entry, dict):
        candidates.append(first_entry)
        candidates.extend(first_entry.get("top_logprobs") or [])
    lp_true, lp_false = find_true_false_logprobs(candidates)
    return lp_true, lp_false, first_token, None


def ollama_ptruth(prompt: str, model: str = DEFAULT_MODEL, url: str = OLLAMA_URL,
                  timeout: int = TIMEOUT_S) -> tuple[float, float, float, str | None]:
    """Call Ollama; return (ptruth, lp_true, lp_false, first_token). Raises on failure."""
    data = {
        "model": model,
        "prompt": prompt,
        "logprobs": True,
        "top_logprobs": 20,
        "options": {"num_predict": 1, "temperature": 0.0},
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        # read all lines
        raw = resp.read().decode("utf-8", errors="replace")
    lines = raw.splitlines()
    lp_true, lp_false, first_token, err = parse_ollama_response_lines(lines)
    if err:
        raise RuntimeError(err)
    p = ptruth_from_logprobs(lp_true, lp_false)
    if p is None:
        raise RuntimeError("True/False not found in top_logprobs")
    return float(p), float(lp_true), float(lp_false), first_token


def load_items(path: Path = ITEMS) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_reader_features(path: Path = READER_FEATURES) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["item_id"]] = row
    return out


def build_worklist(items: list[dict], features: dict[str, dict]) -> list[tuple[dict, str]]:
    """Dev items that have reader scores; proposed answer = reader's greedy answer."""
    work = []
    for it in items:
        if it.get("split") != "dev":
            continue
        iid = it["item_id"]
        rf = features.get(iid)
        if rf is None:
            continue
        proposed = (rf.get("reader_answer") or "").strip()
        if not proposed:
            # fallback: gold answer for answerable, else NOT_ANSWERABLE
            if it.get("label") == 1 and it.get("gold_answer"):
                proposed = str(it["gold_answer"]).strip()
            else:
                proposed = "NOT_ANSWERABLE"
        work.append((it, proposed))
    return work


def read_existing_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        if header is None:
            return ids
        if header != CSV_HEADER:
            raise SystemExit(
                f"{path} has unexpected header {header!r}; expected {CSV_HEADER!r}."
            )
        for rec in reader:
            if len(rec) == len(CSV_HEADER) and rec[0]:
                ids.add(rec[0])
    return ids


def append_rows(path: Path, header: list[str], rows: list[list[str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(header)
        w.writerows(rows)
        fh.flush()
        os.fsync(fh.fileno())


def compute_auroc(labels: list[int], scores: list[float]) -> float | None:
    try:
        from sklearn.metrics import roc_auc_score
    except Exception:
        # manual fallback (rank-based)
        return _auroc_manual(labels, scores)
    pos = [s for y, s in zip(labels, scores) if y == 1]
    neg = [s for y, s in zip(labels, scores) if y == 0]
    if not pos or not neg:
        return None
    try:
        return float(roc_auc_score(labels, scores))
    except Exception:
        return _auroc_manual(labels, scores)


def _auroc_manual(labels, scores) -> float | None:
    pos = [s for y, s in zip(labels, scores) if y == 1]
    neg = [s for y, s in zip(labels, scores) if y == 0]
    if not pos or not neg:
        return None
    cnt = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                cnt += 1.0
            elif p == n:
                cnt += 0.5
    return cnt / (len(pos) * len(neg))


def fit_threshold(scores: list[float], labels: list[int],
                  target_precision: float = 0.80) -> dict:
    """Single threshold on score (refuse if score < t), dev-fitted under 0.80 rule."""
    import numpy as np
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    neg_mask = (y == 0)
    n_neg = int(neg_mask.sum())
    n_pos = int((y == 1).sum())
    # candidate thresholds: dev quantiles 1..99
    cands = np.unique(np.percentile(s, list(range(1, 100))))
    # ensure bounds included
    cands = np.unique(np.concatenate(([s.min(), s.max()], cands)))
    best = None  # (recall, threshold)
    best_metrics = None
    for t in cands:
        refused = s < float(t)
        n_ref = int(refused.sum())
        n_ref_neg = int((refused & neg_mask).sum())
        precision = (n_ref_neg / n_ref) if n_ref > 0 else 0.0
        recall = (n_ref_neg / n_neg) if n_neg > 0 else 0.0
        if precision >= target_precision:
            key = (recall, float(t))
            if best is None or key > best:
                best = key
                over_ref = float((refused & (y == 1)).sum() / max(1, n_pos))
                cov = 1.0 - (n_ref / max(1, len(s)))
                best_metrics = {
                    "threshold": float(t),
                    "abstain_precision": float(precision),
                    "abstain_recall": float(recall),
                    "over_refusal": over_ref,
                    "coverage": float(cov),
                    "n_refused": n_ref,
                    "n_refused_neg": n_ref_neg,
                }
    if best_metrics is None:
        # fallback: threshold at max score -> refuse none? report no feasible
        best_metrics = {
            "threshold": float(s.max()),
            "abstain_precision": None,
            "abstain_recall": 0.0,
            "over_refusal": 0.0,
            "coverage": 1.0,
            "n_refused": 0,
            "n_refused_neg": 0,
            "feasible": False,
        }
    else:
        best_metrics["feasible"] = True
    best_metrics["target_precision"] = target_precision
    return best_metrics


def acquire_lock(path: Path = LOCK, stale_after_s: float = 3 * 3600) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        age = time.time() - path.stat().st_mtime
        if age < stale_after_s:
            try:
                holder = path.read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                holder = "?"
            print(f"HEAVY.lock held ({age / 60:.0f} min old): {holder}", file=sys.stderr)
            return False
        print(f"taking over stale HEAVY.lock ({age / 3600:.1f} h old)", file=sys.stderr)
    payload = f"pid={os.getpid()} job=r3_exp_ptruth started={time.strftime('%Y-%m-%dT%H:%M:%S')}"
    path.write_text(payload, encoding="utf-8")
    return True


def release_lock(path: Path = LOCK) -> None:
    try:
        if path.exists() and f"pid={os.getpid()}" in path.read_text(encoding="utf-8", errors="replace"):
            path.unlink()
    except OSError:
        pass


# --------------------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="P(True)-style reader baseline via Ollama.")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--time-budget", type=float, default=None, help="seconds cap (default: run all)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--url", default=OLLAMA_URL)
    ap.add_argument("--items", type=Path, default=ITEMS)
    ap.add_argument("--features", type=Path, default=READER_FEATURES)
    ap.add_argument("--out", type=Path, default=OUT_CSV)
    ap.add_argument("--errors", type=Path, default=ERR_CSV)
    ap.add_argument("--summary", type=Path, default=OUT_JSON)
    ap.add_argument("--no-resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    items = load_items(args.items)
    features = load_reader_features(args.features)
    work = build_worklist(items, features)
    print(f"worklist: {len(work)} dev items with reader scores", flush=True)

    done = set() if args.no_resume else read_existing_ids(args.out)
    todo = [(it, pa) for (it, pa) in work if it["item_id"] not in done]
    print(f"already_scored={len(done)} todo={len(todo)}", flush=True)
    if args.limit is not None:
        todo = todo[:args.limit]

    if args.dry_run:
        for it, pa in todo[:10]:
            print(it["item_id"], "|", pa[:60], "|", build_prompt(it, pa)[:80].replace("\n", " "), flush=True)
        print(f"dry-run: {len(todo)} prompts built, no Ollama calls")
        return 0
    if not todo:
        print("nothing to do")
        # still (re)compute summary from disk if possible
        _write_summary(args, items, features, work)
        return 0

    if not acquire_lock():
        print("HEAVY.lock held; exiting", file=sys.stderr)
        return 3

    t_start = time.time()
    t_gen = time.time()
    stopped = "completed"
    n_done = 0
    n_err = 0
    batch_rows: list[list[str]] = []
    err_rows: list[list[str]] = []
    try:
        seen = 0
        while seen < len(todo):
            if args.time_budget is not None and (time.time() - t_gen) >= args.time_budget:
                stopped = f"time_budget ({args.time_budget:.0f}s)"
                break
            it, pa = todo[seen]
            seen += 1
            iid = it["item_id"]
            ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            try:
                prompt = build_prompt(it, pa)
                p, lp_t, lp_f, first_tok = ollama_ptruth(prompt, model=args.model, url=args.url)
            except Exception as exc:
                err_rows.append([iid, f"{type(exc).__name__}: {exc}", ts])
                n_err += 1
                append_rows(args.errors, ERROR_HEADER, err_rows)
                err_rows = []
                print(f"ERR {iid}: {exc}", flush=True)
                continue
            batch_rows.append([
                iid,
                str(it.get("label")),
                str(it.get("rung")),
                " ".join(str(pa).split()),
                f"{p:.6f}",
                f"{lp_t:.6f}",
                f"{lp_f:.6f}",
            ])
            n_done += 1
            append_rows(args.out, CSV_HEADER, batch_rows)
            batch_rows = []
            if n_done % 25 == 0 or n_done == len(todo):
                rate = n_done / max(1e-9, time.time() - t_gen)
                print(f"{n_done}/{len(todo)} done  {rate:.2f} items/s  free? elapsed {(time.time()-t_gen)/60:.1f} min", flush=True)
            if (ROOT / "STOP").exists():
                stopped = "STOP file present"
                break
    finally:
        release_lock()

    # write summary
    _write_summary(args, items, features, work, stopped_reason=stopped,
                   n_done_this_run=n_done, n_err_this_run=n_err, t_gen_start=t_gen)
    wall = time.time() - t_start
    print(f"done: scored_this_run={n_done} errors_this_run={n_err} wall={wall/60:.2f} min stopped={stopped}")
    return 0


def _write_summary(args, items, features, work, stopped_reason="completed",
                   n_done_this_run=0, n_err_this_run=0, t_gen_start=None):
    # load scores from disk
    scores_by_id: dict[str, dict] = {}
    if args.out.exists():
        with open(args.out, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                scores_by_id[row["item_id"]] = row

    # build aligned labels/scores
    labels = []
    sc = []
    rung_labels = {}
    for it, pa in work:
        iid = it["item_id"]
        r = scores_by_id.get(iid)
        if r is None:
            continue
        try:
            p = float(r["ptruth"])
        except (TypeError, ValueError):
            continue
        lab = int(it.get("label"))
        labels.append(lab)
        sc.append(p)
        rung_labels.setdefault(str(it.get("rung")), []).append((lab, p))

    auroc = compute_auroc(labels, sc) if labels else None
    thr = fit_threshold(sc, labels) if labels else None

    per_rung = {}
    for rung, pairs in sorted(rung_labels.items()):
        rl = [x[0] for x in pairs]
        rs = [x[1] for x in pairs]
        per_rung[rung] = {
            "n": len(pairs),
            "n_answerable": sum(1 for y in rl if y == 1),
            "n_negative": sum(1 for y in rl if y == 0),
            "auroc": compute_auroc(rl, rs),
        }

    summary = {
        "baseline": "P(True)-style reader baseline (Kadavath et al. 2207.05221)",
        "exploratory_post_hoc": True,
        "model_ollama": args.model,
        "model_differs_from_paper_reader": True,
        "paper_reader": "Qwen/Qwen2.5-0.5B-Instruct",
        "ollama_endpoint": args.url,
        "n_dev_items_with_reader_scores": len(work),
        "n_scored": len(labels),
        "auroc_answerable_vs_negative": auroc,
        "threshold_080_rule": thr,
        "per_rung_auroc": per_rung,
        "stopped_reason": stopped_reason,
        "n_scored_this_run": n_done_this_run,
        "n_errors_this_run": n_err_this_run,
        "output_csv": str(args.out),
        "errors_csv": str(args.errors),
        "disclosure": (
            "Exploratory/post-hoc, dev-only. Reader model is Qwen2.5-1.5B-Instruct via "
            "Ollama, not the paper's pinned Qwen2.5-0.5B-Instruct. Ollama /api/generate "
            "logprobs verified (see results/c1/r3/exp/COMPUTE.md)."
        ),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"summary -> {args.summary}")


if __name__ == "__main__":
    raise SystemExit(main())
