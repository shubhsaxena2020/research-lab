"""MF-10 third-labeller resolver: stricter rubric, explicit answer span required.
Reads disagreements + sample.csv, runs Ollama, writes raw decisions JSON.

Model: qwen2.5:1.5b-instruct (resolver R, third labeller, disclosed).
Prompt: requires an explicit answer span in the passage (quote it) before label 1.
"""
import csv, json, os, urllib.request

BASE = "C:/Users/shubh/research-lab/04_experiments/results/c1/r3/exp/adjudication/"
MODEL = "qwen2.5:1.5b-instruct"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

A = {r["item_id"]: r for r in csv.DictReader(open(BASE + "label_A.csv", encoding="utf-8", newline=""))}
B = {r["item_id"]: r for r in csv.DictReader(open(BASE + "label_B.csv", encoding="utf-8", newline=""))}
S = {r["item_id"]: r for r in csv.DictReader(open(BASE + "sample.csv", encoding="utf-8", newline=""))}

dis = sorted([k for k in A if A[k]["label"] != B[k]["label"]], key=lambda x: (int(S[x]["rung"]), x))
print(f"disagreements: {len(dis)}")

SYSTEM = ("You are a strict annotator judging whether a passage ANSWERS a question. "
          "Default to label 0 unless you can quote an explicit answer-bearing span from the passage. "
          "Topical mentions, background facts, or partial/indirect hints do NOT count as 1.")

TEMPLATE = """STRICT RUBRIC — 'answerable' (1) requires an EXPLICIT answer span in the passage.
Reply with ONLY a JSON object (no other text):
{{"label": "1" or "0", "evidence": "<verbatim quote from passage supporting label 1, or empty string if label 0>", "rationale": "<one short sentence>"}}

Rules:
- label "1" ONLY if you can quote a verbatim span of the passage that directly gives the answer to the question.
- Paraphrase of the question, topical overlap, or a passage answering a DIFFERENT question is NOT 1.
- If no such verbatim quote exists, label must be "0".
- External knowledge is forbidden: only the passage counts.

Question: {q}
Passage: {c}
"""

def call(prompt: str) -> str:
    payload = json.dumps({"model": MODEL, "prompt": prompt, "system": SYSTEM, "stream": False,
                          "options": {"temperature": 0, "num_predict": 500}}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    return data.get("response", "")

results = []
for i, k in enumerate(dis):
    s = S[k]
    prompt = TEMPLATE.format(q=s["question"], c=s["context"][:4000])
    raw = call(prompt)
    results.append({"item_id": k, "rung": s["rung"], "A": A[k]["label"], "B": B[k]["label"],
                    "question": s["question"], "raw": raw})
    print(f"{i+1}/26 {k} rung={s['rung']} :: {raw[:220].replace(chr(10),' | ')}")

out = BASE + "_resolver_tmp/resolver_raw.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump({"model": MODEL, "system": SYSTEM, "template": TEMPLATE, "results": results}, f, indent=2, ensure_ascii=False)
print("WROTE", out)
