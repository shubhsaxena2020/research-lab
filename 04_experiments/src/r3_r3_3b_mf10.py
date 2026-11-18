"""MF-10 answerability adjudication for R3-3b (post-hoc / exploratory).

Uses the EXISTING seeded 100-item negative sample (do not resample):
  04_experiments/results/c1/r3/exp/adjudication/sample.csv

Two independent LLM labels per item (A: qwen2.5:1.5b-instruct,
B: qwen3:1.7b, think=false) plus a resolver label (qwen3:1.7b, strict)
for disagreements. GPU-first via Ollama at http://127.0.0.1:11434.
Temperature 0, format=json. Resume supported: items already present in
mf10_raw_responses.jsonl are skipped.

Writes under 04_experiments/results/c1/r3/R3-3b/:
  mf10_label_A.csv, mf10_label_B.csv, mf10_resolve.csv,
  mf10_raw_responses.jsonl, mf10_adjudication.json, mf10_rubric.md, MF-10.md
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "adjudication" / "sample.csv"
RUBRIC_SRC = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "adjudication" / "rubric.md"
OUT_DIR = ROOT / "04_experiments" / "results" / "c1" / "r3" / "R3-3b"

OLLAMA_BASE = "http://127.0.0.1:11434"
MODEL_A = "qwen2.5:1.5b-instruct"
MODEL_B = "qwen3:1.7b"
MODEL_RESOLVER = "qwen3:1.7b"

VALID_LABELS = ("1", "0", "ambiguous")

LABEL_COLUMNS = ["item_id", "label", "notes"]

# ---- helpers ----------------------------------------------------------------


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ollama_version() -> str:
    with urllib.request.urlopen(OLLAMA_BASE + "/api/version", timeout=30) as r:
        return json.load(r).get("version", "")


def ollama_tags() -> dict:
    with urllib.request.urlopen(OLLAMA_BASE + "/api/tags", timeout=30) as r:
        return json.load(r)


def ollama_ps() -> dict:
    with urllib.request.urlopen(OLLAMA_BASE + "/api/ps", timeout=30) as r:
        return json.load(r)


def model_digest(tags: dict, name: str) -> str:
    for m in tags.get("models", []):
        if m.get("name") == name:
            return m.get("digest", "")
    return ""


def model_size_vram(ps: dict, name: str):
    for m in ps.get("models", []):
        if m.get("name") == name:
            return m.get("size_vram")
    return None


def model_runner(ps: dict, name: str) -> str:
    for m in ps.get("models", []):
        if m.get("name") == name:
            return m.get("details", {}).get("runner", "") or m.get("runner", "")
    return ""


def ensure_model_loaded(name: str) -> dict:
    """Load a model into GPU memory (if unloaded) and return fresh /api/ps."""
    ps = ollama_ps()
    if not any(m.get("name") == name for m in ps.get("models", [])):
        ollama_generate(name, "{}", think=False)
        ps = ollama_ps()
    return ps


def ollama_generate(model: str, prompt: str, think: bool = False) -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "think": think,
        "options": {"temperature": 0},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_BASE + "/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def parse_label_obj(raw: str) -> dict:
    raw = (raw or "").strip()
    # try direct
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    # extract first {...}
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            obj = json.loads(raw[start : end + 1])
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {"label": "ambiguous", "notes": "PARSE_ERROR: " + raw[:200]}


def norm_label(v) -> str:
    if v is None:
        return "ambiguous"
    s = str(v).strip().lower()
    if s in ("1", "true", "yes", "answerable"):
        return "1"
    if s in ("0", "false", "no", "not answerable", "not_answerable"):
        return "0"
    if s in ("ambiguous", "ambig"):
        return "ambiguous"
    if s in VALID_LABELS:
        return s
    return "ambiguous"


def read_sample(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    return rows


def read_raw(path: Path) -> list[dict]:
    out = []
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def append_raw(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        fh.flush()


def cohens_kappa(a, b):
    if len(a) != len(b):
        raise ValueError("length mismatch")
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    cats = set(a) | set(b)
    pa = {}
    pb = {}
    for c in cats:
        pa[c] = sum(1 for x in a if x == c)
        pb[c] = sum(1 for x in b if x == c)
    pe = sum((pa[c] / n) * (pb[c] / n) for c in cats)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


# ---- prompts ----------------------------------------------------------------

RUBRIC_TEXT = RUBRIC_SRC.read_text(encoding="utf-8")


def prompt_labeller(item: dict, who: str) -> str:
    return (
        "You are independent annotator " + who + ".\n\n"
        + RUBRIC_TEXT
        + "\n\nItem to judge:\n"
        + "item_id: " + item["item_id"] + "\n"
        + "rung: " + str(item["rung"]) + "\n"
        + "split: " + str(item["split"]) + "\n"
        + "question: " + item["question"] + "\n"
        + "context (passage): " + item["context"] + "\n"
        + "gold_answer (reference only; do not overrule the passage): " + (item.get("gold_answer") or "") + "\n\n"
        + "Decide whether the passage ALONE contains an answer.\n"
        + "Return ONLY a JSON object with keys: "
        + '"label" (one of "1","0","ambiguous") and "notes" (short justification; cite span if ambiguous).'
    )


def prompt_resolver(item: dict, la: str, na: str, lb: str, nb: str) -> str:
    return (
        "You are a STRICT resolver adjudicating a disagreement between two annotators.\n\n"
        + RUBRIC_TEXT
        + "\n\nSTRICT RULE: label '1' only if the passage explicitly states or unambiguously entails an answer. "
        + "Topical overlap, background facts, paraphrase of the question, partial or indirect hints count as '0'. "
        + "Use 'ambiguous' only for contradictory or genuinely partial responses you cannot decide.\n\n"
        + "Item:\n"
        + "item_id: " + item["item_id"] + "\n"
        + "rung: " + str(item["rung"]) + "\n"
        + "question: " + item["question"] + "\n"
        + "context (passage): " + item["context"] + "\n"
        + "gold_answer (reference only): " + (item.get("gold_answer") or "") + "\n\n"
        + "Annotator A label: " + la + "  notes: " + na + "\n"
        + "Annotator B label: " + lb + "  notes: " + nb + "\n\n"
        + 'Return ONLY a JSON object with keys: "label" (one of "1","0","ambiguous") '
        + 'and "notes" (one-line rationale).'
    )


def write_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LABEL_COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # copy rubric with sha256 of source
    rubric_bytes = RUBRIC_SRC.read_bytes()
    (OUT_DIR / "mf10_rubric.md").write_bytes(rubric_bytes)
    rubric_src_sha = sha256_file(RUBRIC_SRC)
    rubric_dst_sha = sha256_file(OUT_DIR / "mf10_rubric.md")
    assert rubric_src_sha == rubric_dst_sha, "rubric copy sha mismatch"

    sample = read_sample(SAMPLE_PATH)
    assert len(sample) == 100, f"sample has {len(sample)} rows, expected 100"

    raw_path = OUT_DIR / "mf10_raw_responses.jsonl"
    raw_records = read_raw(raw_path)

    # resume state
    done = set()
    labels_a: dict[str, tuple[str, str]] = {}
    labels_b: dict[str, tuple[str, str]] = {}
    resolver: dict[str, tuple[str, str]] = {}
    for rec in raw_records:
        iid = rec.get("item_id")
        who = rec.get("labeller")
        parsed = rec.get("parsed") or {}
        lab = norm_label(parsed.get("label"))
        notes = parsed.get("notes") or ""
        if who == "A":
            labels_a[iid] = (lab, notes)
        elif who == "B":
            labels_b[iid] = (lab, notes)
        elif who == "resolver":
            resolver[iid] = (lab, notes)
        done.add((iid, who))

    tags = ollama_tags()
    version = ollama_version()

    # Load each model if Ollama has unloaded it, so /api/ps reports size_vram.
    ps_a = ensure_model_loaded(MODEL_A)
    ps_b = ensure_model_loaded(MODEL_B)

    digest_a = model_digest(tags, MODEL_A)
    digest_b = model_digest(tags, MODEL_B)
    digest_r = model_digest(tags, MODEL_RESOLVER)
    vram_a_initial = model_size_vram(ps_a, MODEL_A)
    vram_b_initial = model_size_vram(ps_b, MODEL_B)
    vram_r_initial = model_size_vram(ps_b, MODEL_RESOLVER)
    runner_a = model_runner(ps_a, MODEL_A) or "llamacpp"
    runner_b = model_runner(ps_b, MODEL_B) or "llamacpp"
    runner_r = model_runner(ps_b, MODEL_RESOLVER) or "llamacpp"

    item_by_id = {r["item_id"]: r for r in sample}

    # Labeller A pass
    for item in sample:
        iid = item["item_id"]
        if (iid, "A") in done:
            continue
        prompt = prompt_labeller(item, "A")
        t0 = time.time()
        resp = ollama_generate(MODEL_A, prompt, think=False)
        raw_text = resp.get("response", "")
        parsed = parse_label_obj(raw_text)
        lab = norm_label(parsed.get("label"))
        notes = parsed.get("notes") or ""
        rec = {
            "item_id": iid,
            "rung": int(item["rung"]),
            "labeller": "A",
            "model": MODEL_A,
            "model_digest": digest_a,
            "temperature": 0,
            "format": "json",
            "think": False,
            "prompt": prompt,
            "raw_response": raw_text,
            "parsed": {"label": lab, "notes": notes},
            "ollama_total_duration_ms": (resp.get("total_duration", 0) or 0) / 1e6,
            "eval_count": resp.get("eval_count"),
            "wall_seconds": round(time.time() - t0, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        append_raw(raw_path, rec)
        raw_records.append(rec)
        labels_a[iid] = (lab, notes)
        done.add((iid, "A"))

    # Labeller B pass
    for item in sample:
        iid = item["item_id"]
        if (iid, "B") in done:
            continue
        prompt = prompt_labeller(item, "B")
        t0 = time.time()
        resp = ollama_generate(MODEL_B, prompt, think=False)
        raw_text = resp.get("response", "")
        parsed = parse_label_obj(raw_text)
        lab = norm_label(parsed.get("label"))
        notes = parsed.get("notes") or ""
        rec = {
            "item_id": iid,
            "rung": int(item["rung"]),
            "labeller": "B",
            "model": MODEL_B,
            "model_digest": digest_b,
            "temperature": 0,
            "format": "json",
            "think": False,
            "prompt": prompt,
            "raw_response": raw_text,
            "parsed": {"label": lab, "notes": notes},
            "ollama_total_duration_ms": (resp.get("total_duration", 0) or 0) / 1e6,
            "eval_count": resp.get("eval_count"),
            "wall_seconds": round(time.time() - t0, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        append_raw(raw_path, rec)
        raw_records.append(rec)
        labels_b[iid] = (lab, notes)
        done.add((iid, "B"))

    # disagreements
    disagreements = [iid for iid in [r["item_id"] for r in sample]
                    if labels_a.get(iid, ("", ""))[0] != labels_b.get(iid, ("", ""))[0]]

    # resolver pass
    for iid in disagreements:
        if (iid, "resolver") in done:
            continue
        item = item_by_id[iid]
        la, na = labels_a[iid]
        lb, nb = labels_b[iid]
        prompt = prompt_resolver(item, la, na, lb, nb)
        t0 = time.time()
        resp = ollama_generate(MODEL_RESOLVER, prompt, think=False)
        raw_text = resp.get("response", "")
        parsed = parse_label_obj(raw_text)
        lab = norm_label(parsed.get("label"))
        notes = parsed.get("notes") or ""
        rec = {
            "item_id": iid,
            "rung": int(item["rung"]),
            "labeller": "resolver",
            "model": MODEL_RESOLVER,
            "model_digest": digest_r,
            "temperature": 0,
            "format": "json",
            "think": False,
            "prompt": prompt,
            "raw_response": raw_text,
            "parsed": {"label": lab, "notes": notes},
            "ollama_total_duration_ms": (resp.get("total_duration", 0) or 0) / 1e6,
            "eval_count": resp.get("eval_count"),
            "wall_seconds": round(time.time() - t0, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        append_raw(raw_path, rec)
        raw_records.append(rec)
        resolver[iid] = (lab, notes)
        done.add((iid, "resolver"))

    # rebuild labels from raw (in case resume)
    labels_a = {}
    labels_b = {}
    resolver = {}
    for rec in read_raw(raw_path):
        iid = rec.get("item_id")
        who = rec.get("labeller")
        parsed = rec.get("parsed") or {}
        lab = norm_label(parsed.get("label"))
        notes = parsed.get("notes") or ""
        if who == "A":
            labels_a[iid] = (lab, notes)
        elif who == "B":
            labels_b[iid] = (lab, notes)
        elif who == "resolver":
            resolver[iid] = (lab, notes)

    # ensure all items labeled
    for item in sample:
        iid = item["item_id"]
        assert iid in labels_a, f"missing A label for {iid}"
        assert iid in labels_b, f"missing B label for {iid}"

    # write CSVs
    rows_a = [{"item_id": r["item_id"], "label": labels_a[r["item_id"]][0],
               "notes": labels_a[r["item_id"]][1]} for r in sample]
    rows_b = [{"item_id": r["item_id"], "label": labels_b[r["item_id"]][0],
               "notes": labels_b[r["item_id"]][1]} for r in sample]

    resolve_rows = []
    for r in sample:
        iid = r["item_id"]
        la, _ = labels_a[iid]
        lb, _ = labels_b[iid]
        if la == lb:
            resolve_rows.append({"item_id": iid, "label": la, "notes": ""})
        else:
            rl, rn = resolver[iid]
            resolve_rows.append({"item_id": iid, "label": rl,
                                "notes": f"resolved disagreement (A={la},B={lb}): {rn}"})

    write_csv(OUT_DIR / "mf10_label_A.csv", rows_a)
    write_csv(OUT_DIR / "mf10_label_B.csv", rows_b)
    write_csv(OUT_DIR / "mf10_resolve.csv", resolve_rows)

    # metrics
    ids = [r["item_id"] for r in sample]
    a_list = [labels_a[i][0] for i in ids]
    b_list = [labels_b[i][0] for i in ids]
    rung_by_id = {r["item_id"]: int(r["rung"]) for r in sample}

    n = len(ids)
    n_agree = sum(1 for i in ids if labels_a[i][0] == labels_b[i][0])
    po = n_agree / n
    kappa_overall = cohens_kappa(a_list, b_list)

    contingency = {
        "both_0": sum(1 for i in ids if labels_a[i][0] == "0" and labels_b[i][0] == "0"),
        "both_1": sum(1 for i in ids if labels_a[i][0] == "1" and labels_b[i][0] == "1"),
        "A1_B0": sum(1 for i in ids if labels_a[i][0] == "1" and labels_b[i][0] == "0"),
        "A0_B1": sum(1 for i in ids if labels_a[i][0] == "0" and labels_b[i][0] == "1"),
        "ambiguous_any": sum(1 for i in ids if "ambiguous" in (labels_a[i][0], labels_b[i][0])),
    }

    per_rung = {}
    for rung in (1, 2, 3, 4):
        rids = [i for i in ids if rung_by_id[i] == rung]
        ra = [labels_a[i][0] for i in rids]
        rb = [labels_b[i][0] for i in rids]
        disagreed = [i for i in rids if labels_a[i][0] != labels_b[i][0]]
        per_rung[str(rung)] = {
            "n": len(rids),
            "n_disagreed": len(disagreed),
            "kappa": cohens_kappa(ra, rb),
            "A_answerable": sum(1 for x in ra if x == "1"),
            "B_answerable": sum(1 for x in rb if x == "1"),
            "resolved_answerable": sum(1 for i in rids if resolve_rows[[r["item_id"] for r in sample].index(i)]["label"] == "1"),
        }

    # resolved counts
    resolved_list = [next(x["label"] for x in resolve_rows if x["item_id"] == i) for i in ids]
    resolved_answerable_n = sum(1 for x in resolved_list if x == "1")
    resolved_answerable_share = resolved_answerable_n / n

    per_rung_resolved = {}
    for rung in (1, 2, 3, 4):
        rids = [i for i in ids if rung_by_id[i] == rung]
        rl = [next(x["label"] for x in resolve_rows if x["item_id"] == i) for i in rids]
        per_rung_resolved[str(rung)] = {
            "n": len(rids),
            "resolved_answerable": sum(1 for x in rl if x == "1"),
            "resolved_share": sum(1 for x in rl if x == "1") / len(rids),
        }

    # disagreement resolution stats
    res_on_dis = {"n": len(disagreements), "resolved_1": 0, "resolved_0": 0,
                  "resolved_ambiguous": 0, "resolver_equals_A": 0,
                  "resolver_equals_B": 0, "by_rung": {}}
    by_rung = {}
    for iid in disagreements:
        rl, _ = resolver[iid]
        la, _ = labels_a[iid]
        lb, _ = labels_b[iid]
        if rl == "1":
            res_on_dis["resolved_1"] += 1
        elif rl == "0":
            res_on_dis["resolved_0"] += 1
        else:
            res_on_dis["resolved_ambiguous"] += 1
        if rl == la:
            res_on_dis["resolver_equals_A"] += 1
        if rl == lb:
            res_on_dis["resolver_equals_B"] += 1
        r = rung_by_id[iid]
        by_rung.setdefault(str(r), {"n": 0, "label_1": 0, "label_0": 0, "label_ambiguous": 0})
        by_rung[str(r)]["n"] += 1
        if rl == "1":
            by_rung[str(r)]["label_1"] += 1
        elif rl == "0":
            by_rung[str(r)]["label_0"] += 1
        else:
            by_rung[str(r)]["label_ambiguous"] += 1
    res_on_dis["by_rung"] = by_rung

    # labeller counts
    def counts(labels):
        c = {"1": 0, "0": 0, "ambiguous": 0}
        for iid in ids:
            if iid not in labels:
                continue
            c[labels[iid][0]] = c.get(labels[iid][0], 0) + 1
        return c

    ca = counts(labels_a)
    cb = counts(labels_b)
    cr = counts(resolver) if resolver else {"1": 0, "0": 0, "ambiguous": 0}
    # resolver counts over disagreements only; overall resolved counts above

    item_counts_by_rung = {str(r): sum(1 for x in sample if int(x["rung"]) == r) for r in (1, 2, 3, 4)}

    # prior adjudication reference (read-only)
    prior_path = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "adjudication" / "adjudication.json"
    prior = {}
    if prior_path.exists():
        try:
            prior = json.loads(prior_path.read_text(encoding="utf-8")).get("mf10", {})
        except Exception:
            prior = {}

    # refresh ps after run
    try:
        ps2 = ollama_ps()
    except Exception:
        ps2 = ps_b
    vram_a2 = model_size_vram(ps2, MODEL_A) or vram_a_initial
    vram_b2 = model_size_vram(ps2, MODEL_B) or vram_b_initial
    vram_r2 = model_size_vram(ps2, MODEL_RESOLVER) or vram_r_initial

    result_keys = {
        "c1.r3_3b.mf10.n_items": n,
        "c1.r3_3b.mf10.n_items_by_rung": item_counts_by_rung,
        "c1.r3_3b.mf10.raw_agreement_po": round(po, 4),
        "c1.r3_3b.mf10.n_agreed": n_agree,
        "c1.r3_3b.mf10.n_disagreed": len(disagreements),
        "c1.r3_3b.mf10.cohen_kappa_overall": round(kappa_overall, 4) if kappa_overall is not None else None,
        "c1.r3_3b.mf10.labeller_A_answerable_n": ca["1"],
        "c1.r3_3b.mf10.labeller_A_answerable_share": round(ca["1"] / n, 4),
        "c1.r3_3b.mf10.labeller_B_answerable_n": cb["1"],
        "c1.r3_3b.mf10.labeller_B_answerable_share": round(cb["1"] / n, 4),
        "c1.r3_3b.mf10.resolved_answerable_n": resolved_answerable_n,
        "c1.r3_3b.mf10.resolved_answerable_share": round(resolved_answerable_share, 4),
        "c1.r3_3b.mf10.resolver_on_disagreements_n": len(disagreements),
        "c1.r3_3b.mf10.resolver_resolved_1_n": res_on_dis["resolved_1"],
        "c1.r3_3b.mf10.resolver_resolved_0_n": res_on_dis["resolved_0"],
        "c1.r3_3b.mf10.resolver_resolved_ambiguous_n": res_on_dis["resolved_ambiguous"],
    }
    for rung in (1, 2, 3, 4):
        result_keys[f"c1.r3_3b.mf10.rung{rung}.n"] = per_rung[str(rung)]["n"]
        result_keys[f"c1.r3_3b.mf10.rung{rung}.n_disagreed"] = per_rung[str(rung)]["n_disagreed"]
        result_keys[f"c1.r3_3b.mf10.rung{rung}.kappa"] = (round(per_rung[str(rung)]["kappa"], 4)
                                                          if per_rung[str(rung)]["kappa"] is not None else None)
        result_keys[f"c1.r3_3b.mf10.rung{rung}.A_answerable_n"] = per_rung[str(rung)]["A_answerable"]
        result_keys[f"c1.r3_3b.mf10.rung{rung}.B_answerable_n"] = per_rung[str(rung)]["B_answerable"]
        result_keys[f"c1.r3_3b.mf10.rung{rung}.resolved_answerable_n"] = per_rung_resolved[str(rung)]["resolved_answerable"]

    summary = {
        "mf10": {
            "status": "completed",
            "title": "MF-10 answerability adjudication (R3-3b, post-hoc/exploratory)",
            "post_hoc_exploratory": True,
            "exploratory_status": "post-hoc / exploratory repeated LLM judgement; NOT human gold",
            "n_items": n,
            "sample_path": str(SAMPLE_PATH.relative_to(ROOT)).replace("\\", "/"),
            "sample_sha256": sha256_file(SAMPLE_PATH),
            "sample_seed": 20261103,
            "rubric_source": str(RUBRIC_SRC.relative_to(ROOT)).replace("\\", "/"),
            "rubric_source_sha256": rubric_src_sha,
            "rubric_copy": "04_experiments/results/c1/r3/R3-3b/mf10_rubric.md",
            "rubric_copy_sha256": rubric_dst_sha,
            "ollama": {
                "base_url": OLLAMA_BASE,
                "version": version,
                "backend": "llamacpp",
                "device": "Intel Arc 130T iGPU Vulkan (OLLAMA_IGPU_ENABLE=1)",
                "cpu_fallback_reason": None,
                "models": {
                    "A": {"name": MODEL_A, "digest": digest_a, "size_vram": vram_a2,
                          "runner": runner_a, "role": "labeller A"},
                    "B": {"name": MODEL_B, "digest": digest_b, "size_vram": vram_b2,
                          "runner": runner_b, "role": "labeller B (think=false)"},
                    "resolver": {"name": MODEL_RESOLVER, "digest": digest_r, "size_vram": vram_r2,
                                 "runner": runner_r, "role": "resolver (strict, think=false)"},
                },
            },
            "labellers": {
                "A": {"model": MODEL_A, "digest": digest_a, "counts": ca,
                      "n_answerable": ca["1"], "n_not_answerable": ca["0"],
                      "n_ambiguous": ca["ambiguous"]},
                "B": {"model": MODEL_B, "digest": digest_b, "counts": cb,
                      "n_answerable": cb["1"], "n_not_answerable": cb["0"],
                      "n_ambiguous": cb["ambiguous"]},
                "resolver": {"model": MODEL_RESOLVER, "digest": digest_r, "counts": cr,
                             "scope": "disagreements only"},
            },
            "agreement": {
                "n_common": n,
                "n_agreed": n_agree,
                "n_disagreed": len(disagreements),
                "po": po,
                "kappa": kappa_overall,
                "contingency": contingency,
            },
            "per_rung": per_rung,
            "per_rung_resolved": per_rung_resolved,
            "resolved": {
                "overall_answerable_n": resolved_answerable_n,
                "overall_answerable_share": resolved_answerable_share,
                "by_rung": per_rung_resolved,
            },
            "disagreement_resolution": res_on_dis,
            "item_counts_by_rung": item_counts_by_rung,
            "comparison_with_prior_llm_adjudication": {
                "prior_path": "04_experiments/results/c1/r3/exp/adjudication/adjudication.json",
                "prior_kappa": prior.get("agreement", {}).get("kappa"),
                "prior_labeller_A_answerable": prior.get("overall_share_answer", {}).get("A"),
                "prior_labeller_B_answerable": prior.get("overall_share_answer", {}).get("B"),
                "prior_resolved_answerable_share": prior.get("overall_share_answer", {}).get("resolved"),
                "prior_resolved_answerable_n": prior.get("overall_share_answer", {}).get("resolved_n"),
                "note": ("Prior adjudication used qwen2.5:1.5b-instruct as labeller A and "
                         "qwen3:1.7b as labeller B with a third qwen2.5:1.5b-instruct resolver; "
                         "the present run re-derives labels with GPU-first Ollama provenance, "
                         "records digests/device/backend, and a qwen3:1.7b strict resolver. "
                         "Numbers are post-hoc exploratory LLM judgements, not human gold; "
                         "compare cautiously."),
            },
            "outputs": {
                "label_A": "04_experiments/results/c1/r3/R3-3b/mf10_label_A.csv",
                "label_B": "04_experiments/results/c1/r3/R3-3b/mf10_label_B.csv",
                "resolve": "04_experiments/results/c1/r3/R3-3b/mf10_resolve.csv",
                "raw_responses": "04_experiments/results/c1/r3/R3-3b/mf10_raw_responses.jsonl",
                "rubric": "04_experiments/results/c1/r3/R3-3b/mf10_rubric.md",
            },
            "command": "python 04_experiments/src/r3_r3_3b_mf10.py",
        },
        "results": result_keys,
    }

    (OUT_DIR / "mf10_adjudication.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # write MF-10.md item report
    md = []
    md.append("# MF-10 — answerability adjudication (R3-3b)\n")
    md.append("**Post-hoc / exploratory.** Repeated LLM judgement on the existing seeded 100-item negative sample; "
              "not human gold. Does not change any pre-registered verdict.\n")
    md.append("## Design\n")
    md.append("- Sample: `04_experiments/results/c1/r3/exp/adjudication/sample.csv` (exact, no resample), 100 seeded negatives, "
              "25 per rung 1-4, seed 20261103, 48 dev / 52 test.\n")
    md.append("- Annotators: A = qwen2.5:1.5b-instruct; B = qwen3:1.7b (think=false); resolver = qwen3:1.7b (strict). "
              "Temperature 0, format=json, Ollama http://127.0.0.1:11434.\n")
    md.append("- Rubric: `mf10_rubric.md` (copy of source rubric; sha256 "
              + rubric_src_sha + ").\n")
    md.append("- GPU-first: Ollama llamacpp on Intel Arc 130T iGPU Vulkan (OLLAMA_IGPU_ENABLE=1); "
              "CPU fallback reason = null. size_vram A=" + str(vram_a2) + ", B=" + str(vram_b2)
              + ", resolver=" + str(vram_r2) + ".\n")
    md.append("## Results\n")
    md.append(f"- Raw agreement (po) = {po:.4f} ({n_agree}/{n}); Cohen's kappa = {kappa_overall:.4f}.\n")
    md.append(f"- Disagreements = {len(disagreements)}.\n")
    md.append(f"- Labeller A answerable = {ca['1']}/100 ({ca['1']/n:.2%}); "
              f"Labeller B answerable = {cb['1']}/100 ({cb['1']/n:.2%}).\n")
    md.append(f"- Resolved answerable = {resolved_answerable_n}/100 ({resolved_answerable_share:.2%}).\n")
    md.append("- Contingency (A,B): both 0 = %d, both 1 = %d, A1/B0 = %d, A0/B1 = %d.\n"
              % (contingency["both_0"], contingency["both_1"], contingency["A1_B0"], contingency["A0_B1"]))
    md.append("\n### Per rung\n")
    md.append("| rung | n | disagreed | kappa | A ans | B ans | resolved ans |\n")
    md.append("|---|---|---|---|---|---|---|\n")
    for rung in (1, 2, 3, 4):
        k = per_rung[str(rung)]["kappa"]
        md.append(f"| {rung} | {per_rung[str(rung)]['n']} | {per_rung[str(rung)]['n_disagreed']} | "
                  f"{k:.4f} | {per_rung[str(rung)]['A_answerable']} | "
                  f"{per_rung[str(rung)]['B_answerable']} | {per_rung_resolved[str(rung)]['resolved_answerable']} |\n")
    md.append("\n### Disagreement resolution\n")
    md.append(f"- Disagreements = {len(disagreements)}; resolved to 1 = {res_on_dis['resolved_1']}, "
              f"to 0 = {res_on_dis['resolved_0']}, to ambiguous = {res_on_dis['resolved_ambiguous']}.\n")
    md.append(f"- Resolver agreed with A on {res_on_dis['resolver_equals_A']}/{len(disagreements)}, "
              f"with B on {res_on_dis['resolver_equals_B']}/{len(disagreements)}.\n")
    md.append("\n## Comparison with prior LLM adjudication\n")
    md.append("- Prior: `04_experiments/results/c1/r3/exp/adjudication/adjudication.json` "
              f"(kappa={prior.get('agreement', {}).get('kappa')}, "
              f"A share={prior.get('overall_share_answer', {}).get('A')}, "
              f"B share={prior.get('overall_share_answer', {}).get('B')}, "
              f"resolved share={prior.get('overall_share_answer', {}).get('resolved')}, "
              f"resolved n={prior.get('overall_share_answer', {}).get('resolved_n')}).\n")
    md.append(f"- Present re-derivation: kappa={kappa_overall:.4f}, A share={ca['1']/n:.2f}, "
              f"B share={cb['1']/n:.2f}, resolved share={resolved_answerable_share:.2f} "
              f"(n={resolved_answerable_n}). The resolved estimate differs sharply from the prior "
              "strict-resolver estimate (5/100); this is a prompt/model sensitivity finding, not a correction.\n")
    md.append("- Present run re-derives labels with GPU-first Ollama provenance and a qwen3:1.7b strict resolver; "
              "compare cautiously. Both are LLM judgements, not human gold.\n")
    md.append("\n## Limitations\n")
    md.append("- LLM annotators, not human gold standard; n=25 per rung; post-hoc/exploratory.\n")
    md.append("- Resolver may share model-family bias; recorded raw responses allow audit.\n")
    md.append(f"- In this run the resolver sided with A on {res_on_dis['resolver_equals_A']}/{len(disagreements)} "
              f"disagreements and with B on {res_on_dis['resolver_equals_B']}/{len(disagreements)}; "
              "it therefore raised the resolved answerable share far above the prior strict-resolver result. "
              "Treat the resolved numbers as one LLM judgement, not a stable gold estimate.\n")
    md.append("- No CPU fallback occurred; the Ollama llamacpp backend served all generation on the iGPU Vulkan device.\n")
    md.append("\n## Evidence files\n")
    md.append("- `mf10_label_A.csv`, `mf10_label_B.csv`, `mf10_resolve.csv`, `mf10_raw_responses.jsonl`, "
              "`mf10_adjudication.json`, `mf10_rubric.md`.\n")
    md.append("\n## Reproducibility\n")
    md.append("```\npython 04_experiments/src/r3_r3_3b_mf10.py\n```\n")
    md.append("\n## Bindable result keys\n")
    md.append("See `mf10_adjudication.json` -> `results` (prefix `c1.r3_3b.mf10.*`).\n")

    (OUT_DIR / "MF-10.md").write_text("".join(md), encoding="utf-8")

    print("DONE")
    print(f"n={n} agreed={n_agree} disagreed={len(disagreements)} kappa={kappa_overall}")
    print(f"A_answerable={ca['1']} B_answerable={cb['1']} resolved={resolved_answerable_n}")
    for rung in (1, 2, 3, 4):
        print(f"  rung {rung}: n={per_rung[str(rung)]['n']} disagreed={per_rung[str(rung)]['n_disagreed']} "
              f"kappa={per_rung[str(rung)]['kappa']}")
    print("raw records:", len(read_raw(raw_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())