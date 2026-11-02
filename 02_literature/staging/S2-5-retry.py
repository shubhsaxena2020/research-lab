#!/usr/bin/env python
"""Retry verification for claims that failed on 429, one claim at a time."""
import csv, json, os, subprocess, sys, time

ROOT = r"C:\Users\shubh\research-lab"
CSV = os.path.join(ROOT, "02_literature", "staging", "S2-5-verified.csv")
TOOL = os.path.join(ROOT, "02_literature", "tools", "verify_citations.py")

CLAIMS = {
    "2406.10229": "Quantifying Variance in Evaluation Benchmarks",
    "2405.01535": "Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models",
    "2407.18370": "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement",
    "2503.13657": "Why Do Multi-Agent LLM Systems Fail?",
    "2406.01297": "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs",
    "2403.07974": "LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code",
}

def titles():
    with open(CSV, newline="", encoding="utf-8") as f:
        return {r["title"] for r in csv.DictReader(f)}

for rnd in range(1, 6):
    have = titles()
    todo = {k: v for k, v in CLAIMS.items() if v not in have}
    print(f"round {rnd}: {len(have)} rows, {len(todo)} missing", flush=True)
    if not todo:
        break
    for axid, title in todo.items():
        tmp = os.path.join(ROOT, "02_literature", "staging", f"_one_{axid}.jsonl")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(json.dumps({"title": title, "doi_or_arxiv": f"arXiv:{axid}"}) + "\n")
        r = subprocess.run([sys.executable, TOOL, "add", "--in", tmp, "--out", CSV],
                           capture_output=True, text=True, timeout=900)
        tail = (r.stderr or "").strip().splitlines()[-1:] or [""]
        print(f"  {axid}: {tail[0][:120]}", flush=True)
        time.sleep(20)
    time.sleep(30)

have = titles()
print("final rows:", len(have))
for t in sorted(have):
    print("  ", t[:80])
