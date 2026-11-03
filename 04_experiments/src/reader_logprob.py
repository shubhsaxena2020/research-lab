"""C1 — baseline B4: reader-confidence (mean answer-token log-probability).

PREREGISTRATION.md §4 (reader-side features) and §5 (B4) fix this baseline:

    reader_mean_logprob = mean token log-probability of the reader's **greedy** answer
    (<= 16 tokens) to the question *given the presented passage*.

So for every item we build a chat prompt (system = answer from the passage only, or say
NOT_ANSWERABLE; user = passage + question), greedy-decode at most 16 new tokens, and average the
per-token log-probabilities of exactly those generated tokens (prompt tokens excluded). Nothing here
is fitted; B4 is used later as a single-threshold gate on this score.

Two implementation facts worth stating in the paper's methods:

* **Batching.** Items are decoded in left-padded batches (``--batch-size``) purely for CPU throughput.
  Log-probabilities are read from ``generate(output_scores=True)`` per row and per step, so padding
  never enters the average. ``tools/verify_batching.py`` style checks (see --batch-size 1 comparison in
  the run report) confirm batch size changes numbers only at float32 noise level.
* **Failures are not scored.** An item that raises, or that generates zero tokens, is written to
  ``reader_errors.csv`` with the error text and skipped; it never receives a fabricated log-probability
  and is never silently dropped from the count.

The file is append-and-fsync with resume-by-item_id, so a killed run restarts where it stopped.

CLI
---
    python 04_experiments/src/reader_logprob.py --limit 5
    python 04_experiments/src/reader_logprob.py --time-budget 1500
    python 04_experiments/src/reader_logprob.py --model Qwen/Qwen2.5-0.5B-Instruct --batch-size 8
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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_experiments" / "data"
ITEMS = DATA / "items.jsonl"
OUT_CSV = DATA / "reader_features.csv"
ERR_CSV = DATA / "reader_errors.csv"
META_JSON = DATA / "reader_meta.json"
LOCK = ROOT / "ops" / "HEAVY.lock"

DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
CSV_HEADER = ["item_id", "reader_answer", "reader_mean_logprob", "reader_n_tokens"]
ERROR_HEADER = ["item_id", "error", "ts_utc"]
MAX_NEW_TOKENS = 16
# Prompt guard: longest SQuAD paragraph in this item set is ~4.1k chars (~1.0k tokens); the renderer
# below clips far above that so a pathological item cannot blow the 32k context, and the clip is
# counted in meta so a silent truncation could never hide.
MAX_CONTEXT_CHARS = 8000
NOT_ANSWERABLE = "NOT_ANSWERABLE"

SYSTEM_PROMPT = (
    "You answer questions using only the passage the user provides. "
    "Reply with the shortest span from the passage that answers the question, with no explanation. "
    f"If the passage does not contain the answer, reply exactly {NOT_ANSWERABLE}."
)


# --------------------------------------------------------------------------------------------------
# pure functions (unit-tested without a model)
# --------------------------------------------------------------------------------------------------
def clip_context(context: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Keep head and tail of an over-long passage; returns text unchanged when it already fits."""
    if len(context) <= max_chars:
        return context
    head = max_chars * 2 // 3
    tail = max_chars - head
    return context[:head] + " ... " + context[-tail:]


def build_messages(item: dict, max_chars: int = MAX_CONTEXT_CHARS) -> list[dict]:
    """Chat messages for one item: system + user(passage, question). No tokenizer involved."""
    passage = clip_context(str(item.get("context") or "").strip(), max_chars)
    question = str(item.get("question") or "").strip()
    user = f"Passage:\n{passage}\n\nQuestion: {question}\nAnswer:"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def render_prompt(tokenizer, item: dict, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """apply_chat_template with the generation prompt, as text (tokenisation happens at batch time)."""
    return tokenizer.apply_chat_template(
        build_messages(item, max_chars), tokenize=False, add_generation_prompt=True
    )


def generation_length(ids: list[int], pad_id: int | None, eos_id: int | None) -> int:
    """Number of generated tokens, counting a terminal EOS (it is a generated token, and its
    log-probability is part of the answer's confidence). Trailing padding is not counted."""
    n = 0
    for tid in ids:
        if pad_id is not None and tid == pad_id and pad_id != eos_id:
            break
        n += 1
        if eos_id is not None and tid == eos_id:
            break
    return n


def token_logprobs_from_logits(logits, token_ids) -> list[float]:
    """log-softmax of `logits` [T, V] gathered at `token_ids` [T]; returns T floats.

    Accepts torch tensors or nested lists (the tests use plain lists so no model is loaded).
    """
    try:
        import torch
    except ImportError:  # pragma: no cover - torch is present in this environment
        torch = None

    if torch is not None and hasattr(logits, "float"):
        lp = torch.log_softmax(logits.float(), dim=-1)
        ids = torch.as_tensor(token_ids, dtype=torch.long, device=lp.device)
        return [float(v) for v in lp.gather(-1, ids.view(-1, 1)).view(-1).tolist()]

    out: list[float] = []
    for row, tid in zip(logits, token_ids):
        row = [float(v) for v in row]
        m = max(row)
        lse = m + math.log(sum(math.exp(v - m) for v in row))
        out.append(row[int(tid)] - lse)
    return out


def summarize_logprobs(logprobs: list[float]) -> tuple[float, int]:
    """(mean, n). Raises on an empty list: a mean over zero tokens is not a number we may invent."""
    if not logprobs:
        raise ValueError("no generated tokens: mean log-probability undefined")
    return float(sum(logprobs) / len(logprobs)), len(logprobs)


def score_rows_from_batch(step_logits, gen_ids, pad_id, eos_id, decode):
    """Turn one batched generation into per-item (answer, mean_logprob, n_tokens).

    `step_logits`  : list over decoding steps of a [B, V] tensor (generate's `scores`).
    `gen_ids`      : [B, T] tensor of generated token ids (prompt stripped).
    `decode`       : callable(list[int]) -> str.
    Rows whose generation is empty are returned as None so the caller can log an error row.
    """
    rows: list[dict | None] = []
    n_batch = len(gen_ids)
    for i in range(n_batch):
        ids = [int(t) for t in gen_ids[i].tolist()]
        n = generation_length(ids, pad_id, eos_id)
        if n == 0:
            rows.append(None)
            continue
        lps: list[float] = []
        for t in range(n):
            lps.extend(token_logprobs_from_logits(step_logits[t][i : i + 1], ids[t : t + 1]))
        mean, n_tok = summarize_logprobs(lps)
        rows.append({"answer": decode(ids[:n]), "mean_logprob": mean, "n_tokens": n_tok})
    return rows


def format_row(item_id: str, answer: str, mean_logprob: float, n_tokens: int) -> list[str]:
    return [
        item_id,
        " ".join(str(answer).split()),  # collapse newlines so the CSV stays one row per item
        f"{float(mean_logprob):.6f}",
        str(int(n_tokens)),
    ]


def read_existing_ids(path: Path) -> set[str]:
    """item_ids already scored. Tolerates a half-written final line from a killed run."""
    ids: set[str] = set()
    if not path.exists():
        return ids
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        if header != CSV_HEADER:
            if header is None:
                return ids
            raise SystemExit(
                f"{path} has an unexpected header {header!r}; expected {CSV_HEADER!r}. "
                "Refusing to append to a file with a different schema."
            )
        for rec in reader:
            if len(rec) == len(CSV_HEADER) and rec[0]:
                ids.add(rec[0])
    return ids


def append_rows(path: Path, header: list[str], rows: list[list[str]]) -> None:
    """Append `rows`, creating the file with `header` if absent, then flush + fsync."""
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


def load_items(path: Path = ITEMS) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def free_ram_gb() -> float | None:
    try:
        import psutil  # noqa: PLC0415

        return round(psutil.virtual_memory().available / 1e9, 2)
    except Exception:
        pass
    try:  # Windows fallback, no third-party dependency
        import ctypes

        class _MS(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        m = _MS()
        m.dwLength = ctypes.sizeof(_MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return round(m.ullAvailPhys / 1e9, 2)
    except Exception:
        return None


# --------------------------------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------------------------------
def load_reader(model_id: str, dtype_name: str = "float32", local_files_only: bool = False):
    """Load tokenizer + causal LM on CPU. Returns (model, tokenizer, resolved_dtype_name)."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch_dtypes = {"float32": torch.float32, "bfloat16": torch.bfloat16, "float16": torch.float16}
    if dtype_name not in torch_dtypes:
        raise SystemExit(f"--dtype must be one of {sorted(torch_dtypes)}")
    torch_dtype = torch_dtypes[dtype_name]

    tok = AutoTokenizer.from_pretrained(model_id, local_files_only=local_files_only)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "left"  # required for batched generation with per-row bookkeeping
    if tok.pad_token_id == tok.eos_token_id:
        # Qwen2.5 ships <|endoftext|> as pad in some revisions; keep pad != eos so the first EOS is
        # unambiguously a stop token rather than padding.
        tok.pad_token = "<|endoftext|>" if "<|endoftext|>" in tok.get_vocab() else tok.eos_token

    kwargs = dict(local_files_only=local_files_only)
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch_dtype, **kwargs)
    except TypeError:  # transformers < 5 spells it torch_dtype
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch_dtype, **kwargs)
    model.to("cpu")
    model.eval()
    model.config.use_cache = True
    return model, tok, dtype_name


def decode_batch(model, tok, items: list[dict], max_new_tokens: int = MAX_NEW_TOKENS):
    """Greedy-decode one batch; returns (rows, prompts) with rows aligned to `items`."""
    import torch

    prompts = [render_prompt(tok, it) for it in items]
    enc = tok(prompts, return_tensors="pt", padding=True, padding_side="left")
    prompt_len = enc["input_ids"].shape[1]
    pad_id, eos_id = tok.pad_token_id, tok.eos_token_id
    with torch.inference_mode():
        out = model.generate(
            **enc,
            max_new_tokens=max_new_tokens,
            do_sample=False,  # greedy, per PREREGISTRATION §4
            num_beams=1,
            output_scores=True,
            return_dict_in_generate=True,
            pad_token_id=pad_id,
            eos_token_id=eos_id,
        )
    gen_ids = out.sequences[:, prompt_len:]
    rows = score_rows_from_batch(
        out.scores, gen_ids, pad_id, eos_id, lambda ids: tok.decode(ids, skip_special_tokens=True)
    )
    return rows, prompts


# --------------------------------------------------------------------------------------------------
# lock
# --------------------------------------------------------------------------------------------------
def acquire_lock(path: Path = LOCK, stale_after_s: float = 3 * 3600) -> bool:
    """RULES #10: one heavy job at a time on this shared laptop."""
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
    payload = f"pid={os.getpid()} job=reader_logprob started={time.strftime('%Y-%m-%dT%H:%M:%S')}"
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
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="B4 reader-confidence baseline (mean answer-token logprob).")
    ap.add_argument("--limit", type=int, default=None, help="score at most N new items")
    ap.add_argument("--time-budget", type=float, default=1800.0,
                    help="seconds of generation work before stopping (default 1800 = 30 min cap)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dtype", default="float32", choices=["float32", "bfloat16", "float16"])
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--max-new-tokens", type=int, default=MAX_NEW_TOKENS)
    ap.add_argument("--threads", type=int, default=8, help="torch CPU threads (shared laptop: keep low)")
    ap.add_argument("--items", type=Path, default=ITEMS)
    ap.add_argument("--out", type=Path, default=OUT_CSV)
    ap.add_argument("--errors", type=Path, default=ERR_CSV)
    ap.add_argument("--meta", type=Path, default=META_JSON)
    ap.add_argument("--local-files-only", action="store_true")
    ap.add_argument("--no-resume", action="store_true", help="ignore existing rows and start over")
    ap.add_argument(
        "--ignore-stop",
        action="store_true",
        help="keep going when research-lab/STOP exists (RULES #11 safety brake; caller must say why)",
    )
    ap.add_argument("--dry-run", action="store_true", help="build prompts for --limit items, no model")
    args = ap.parse_args(argv)
    _argv = list(sys.argv) if argv is None else [sys.argv[0], *argv]
    cmdline = " ".join(shlex.quote(a) for a in _argv)
    if not cmdline.startswith("python"):
        cmdline = "python " + cmdline

    items = load_items(args.items)
    done = set() if args.no_resume else read_existing_ids(args.out)
    todo = [it for it in items if it["item_id"] not in done]
    print(f"items total={len(items)} already_scored={len(done)} todo={len(todo)}", flush=True)
    if args.limit is not None:
        todo = todo[: args.limit]

    if args.dry_run:
        for it in todo:
            msgs = build_messages(it)
            print(it["item_id"], "|", msgs[1]["content"][:160].replace("\n", " "), flush=True)
        print(f"dry-run: {len(todo)} prompts built, model not loaded")
        return 0
    if not todo:
        print("nothing to do (all items already scored)")
        return 0
    if not acquire_lock():
        print("another heavy job holds ops/HEAVY.lock; exiting without starting (RULES #10)", file=sys.stderr)
        return 3

    t_start_wall = time.time()
    try:
        import torch

        torch.set_num_threads(max(1, args.threads))
        ram_before = free_ram_gb()
        model, tok, dtype_resolved = load_reader(args.model, args.dtype, args.local_files_only)
        ram_after_load = free_ram_gb()
        t_loaded = time.time()
        print(
            f"loaded {args.model} dtype={dtype_resolved} device=cpu "
            f"params={sum(p.numel() for p in model.parameters()) / 1e6:.1f}M "
            f"free_ram={ram_after_load}GB load={t_loaded - t_start_wall:.1f}s",
            flush=True,
        )

        n_done, n_err, seen = 0, 0, 0
        t_gen_start = time.time()
        stopped_reason = "completed"
        batch_rows: list[list[str]] = []
        err_rows: list[list[str]] = []
        while seen < len(todo):
            elapsed = time.time() - t_gen_start
            if elapsed >= args.time_budget:
                stopped_reason = f"time_budget ({args.time_budget:.0f}s) reached"
                break
            chunk = todo[seen : seen + max(1, args.batch_size)]
            seen += len(chunk)
            try:
                rows, _prompts = decode_batch(model, tok, chunk, args.max_new_tokens)
            except Exception as exc:  # log the whole batch, keep going
                ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                for it in chunk:
                    err_rows.append([it["item_id"], f"{type(exc).__name__}: {exc}", ts])
                    n_err += 1
                append_rows(args.errors, ERROR_HEADER, err_rows)
                err_rows = []
                print(f"batch failed at item {chunk[0]['item_id']}: {exc}", flush=True)
                continue

            ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            for it, row in zip(chunk, rows):
                if row is None:
                    err_rows.append([it["item_id"], "no tokens generated (immediate EOS)", ts])
                    n_err += 1
                    continue
                batch_rows.append(
                    format_row(it["item_id"], row["answer"], row["mean_logprob"], row["n_tokens"])
                )
                n_done += 1
            append_rows(args.out, CSV_HEADER, batch_rows)  # flush + fsync every batch
            batch_rows = []
            if err_rows:
                append_rows(args.errors, ERROR_HEADER, err_rows)
                err_rows = []
            if n_done and n_done % (args.batch_size * 10) < args.batch_size:
                rate = n_done / max(1e-9, time.time() - t_gen_start)
                print(
                    f"{n_done}/{len(todo)} items  {rate:.2f} items/s  "
                    f"eta {(len(todo) - n_done) / max(rate, 1e-9) / 60:.1f} min  "
                    f"free_ram={free_ram_gb()}GB",
                    flush=True,
                )
            if (ROOT / "STOP").exists() and not args.ignore_stop:
                stopped_reason = "STOP file present"
                break
    finally:
        release_lock()

    wall_gen = time.time() - t_gen_start
    total_wall = time.time() - t_start_wall
    rows_on_disk = read_existing_ids(args.out)
    ips = n_done / wall_gen if wall_gen > 0 else 0.0
    meta = {
        "baseline": "B4 reader_mean_logprob",
        "model": args.model,
        "dtype": dtype_resolved,
        "device": "cpu",
        "quantised": False,
        "max_new_tokens": args.max_new_tokens,
        "batch_size": args.batch_size,
        "torch_threads": args.threads,
        "torch_version": __import__("torch").__version__,
        "transformers_version": __import__("transformers").__version__,
        "n_scored_this_run": n_done,
        "n_errors_this_run": n_err,
        "n_rows_in_csv": len(rows_on_disk),
        "n_items_requested": args.limit,
        "items_per_sec": round(ips, 4),
        "wall_seconds_generation": round(wall_gen, 2),
        "wall_seconds_total": round(total_wall, 2),
        "load_seconds": round(t_loaded - t_start_wall, 2),
        "free_ram_gb_before": ram_before,
        "free_ram_gb_after_load": ram_after_load,
        "free_ram_gb_end": free_ram_gb(),
        "stopped_reason": stopped_reason,
        "stop_file_present_at_start": (ROOT / "STOP").exists(),
        "stop_overridden_by_caller": bool(args.ignore_stop),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(t_start_wall)),
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "command": cmdline,
        "items_file": str(args.items),
        "items_file_sha256_note": "see data/item_stats.json sha256_items_jsonl",
        "output_csv": str(args.out),
        "errors_csv": str(args.errors),
    }
    args.meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(
        f"\ndone: scored={n_done} errors={n_err} rows_in_csv={len(rows_on_disk)} "
        f"gen_wall={wall_gen / 60:.2f} min items/s={ips:.3f} stopped={stopped_reason}"
    )
    print(f"meta -> {args.meta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
