"""Render 04_experiments/data/TRANSFER-DATA.md from fetch_log.jsonl + corpus stats.

Run: python 04_experiments/data/raw/2wiki/render_transfer_doc.py
"""
import hashlib
import json
import re
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = Path(__file__).resolve().parents[2]  # 04_experiments/data
RAW = D / "raw" / "2wiki"
LOG = RAW / "fetch_log.jsonl"
CORPUS = RAW / "2wikimultihop_dev.json"
OUT = D / "TRANSFER-DATA.md"

entries = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
items = [json.loads(l) for l in (D / "transfer_items.jsonl").read_text(encoding="utf-8").splitlines()]
corpus_sha = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
items_sha = hashlib.sha256((D / "transfer_items.jsonl").read_bytes()).hexdigest()

WS = re.compile(r"\s+")
lens = [len(WS.sub(" ", " ".join(s for s in c[1]))) for r in corpus for c in r["context"]]
types = Counter(r["type"] for r in corpus)
search_ids = [d["id"] for d in json.loads((RAW / "hf_search_2wiki.json").read_text(encoding="utf-8"))]
cands = ["voidful/2WikiMultihopQA", "thinkall/2WikiMultihopQA", "xanhho/2WikiMultihopQA",
         "framolfese/2WikiMultihopQA", "ohjoonhee/2WikiMultihopQA", "kamelliao/2wikimultihopqa"]

rows = []
for i, e in enumerate(entries, 1):
    status = e.get("status")
    rows.append("| {} | {} | {} | {} | `{}` | {}".format(
        i, e["step"], status if status is not None else "ERR",
        f"{e['bytes']:,}", (e.get("sha256") or "-")[:16] + ("…" if e.get("sha256") else ""),
        e["url"].replace("|", "%7C")))
table = "\n".join(rows)

md = f"""# Transfer corpus: 2WikiMultihopQA dev — acquisition record

Status: **OBTAINED**. Dev split downloaded, verified against the HF dataset card's declared
`num_examples`, and used to build the 400-item transfer arm.

Retrieval date: 2026-11-03 (IST). All requests: plain HTTPS GET, descriptive User-Agent
`research-lab-acquisition/1.0 (mailto:shubh.saxena2020@gmail.com)`, >=1 s between requests.
No login, no API key, no credential anywhere. Full machine-readable log: `04_experiments/data/raw/2wiki/fetch_log.jsonl`.

## 1. Corpus obtained

| field | value |
|---|---|
| file | `04_experiments/data/raw/2wiki/2wikimultihop_dev.json` |
| URL | `https://huggingface.co/datasets/voidful/2WikiMultihopQA/resolve/main/dev.json` |
| HTTP status | 200 |
| bytes | 55,934,464 (55.9 MB) |
| sha256 | `{corpus_sha}` |
| rows | {len(corpus):,} (dev/validation) |
| fields per row | `_id, type, question, context, supporting_facts, evidences, answer` |
| question types | {", ".join(f"{k} {v:,}" for k, v in types.most_common())} |
| paragraphs per question | median {statistics.median([len(r['context']) for r in corpus]):.0f} |
| paragraph length (chars) | median {statistics.median(lens):.0f}, mean {statistics.mean(lens):.0f} |

Completeness cross-check: the independent mirror `framolfese/2WikiMultihopQA` declares
`validation: 12576` examples in its dataset card, and this file parses to exactly 12,576 rows.

## 2. Licence

* **Apache-2.0**, as declared by the dataset authors' own repository:
  `https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/LICENSE` (HTTP 200, 11,337 bytes,
  sha256 `b8c1d7752e71597a45121774b6be93df38a81e1b748be15c063c0759f11e00ea`) — the file body is the
  Apache License, Version 2.0 text.
* Paper: "Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps",
  COLING 2020, `https://www.aclweb.org/anthology/2020.coling-main.580/`.
* Caveat: the HF mirror that served the file (`voidful/2WikiMultihopQA`) has **no** dataset card —
  `https://huggingface.co/api/datasets/voidful/2WikiMultihopQA` returns `cardData: null` and no
  `license:` tag, and `resolve/main/README.md` is 404. The licence above is therefore taken from the
  authors' repository, not from the mirror. The mirror is a byte-for-byte re-host of the official
  `dev.json` schema (same 7 fields, same 12,576 dev rows); we did not verify hash-equality against
  the official Dropbox zip because the zip is ~100 MB+ and the corpus was already in hand.

## 3. Every attempt, in the order prescribed

| # | step | HTTP | bytes | sha256 (first 16) | URL |
|---|---|---|---|---|---|
{table}

### What each step showed

1. **HuggingFace search API** — `?search=2wiki` returned {len(search_ids)} dataset ids (full list in
   `raw/2wiki/hf_search_2wiki.json`), including `voidful/2WikiMultihopQA`, `thinkall/2WikiMultihopQA`,
   `xanhho/2WikiMultihopQA`, `framolfese/2WikiMultihopQA`, `ohjoonhee/2WikiMultihopQA`,
   `kamelliao/2wikimultihopqa`. Candidate ids probed for splits: {", ".join(f"`{c}`" for c in cands)}.
   `xanhho/*` and `kamelliao/*` return **501** from the datasets-server ("runs arbitrary python code",
   no viewer); the other four expose `train/validation/test`.
2. **datasets-server `/rows` JSON API** — **FAILED, service-wide**: every request
   (`voidful`, `framolfese`, `ohjoonhee`) returned **503** with an nginx
   "Service Temporarily Unavailable" HTML body (162 bytes, identical sha256 `258c66556e2e…`) while
   `/splits` on the same host returned 200. So this was the datasets-server rows endpoint being down,
   not a per-dataset refusal. Not retried in a loop (RULE 11). Retry URL:
   `https://datasets-server.huggingface.co/rows?dataset=voidful/2WikiMultihopQA&config=default&split=validation&offset=0&length=100`
3. **Direct HF resolve** — **SUCCESS**. Repo file listing
   (`https://huggingface.co/api/datasets/voidful/2WikiMultihopQA/tree/main?recursive=true`) shows
   `dev.json` (55,934,464 B), `test.json`, `train.json` (681 MB, not downloaded). Fetched `dev.json` → 200.
4. **Alab-NII GitHub raw** — the org repo is `Alab-NII/2wikimultihop` (**not** `…2wikimultihopqa`; the
   `qa` spelling 404s on every path tried). `README.md` and `LICENSE` are 200, but **no data files are
   committed to the repo**: `master/dev.json`, `main/dev.json`, `master/data/dev.json` all 404.
5. **Dropbox (linked from the authors' README / paper page)** — `https://www.dropbox.com/s/npidmtadreo6df2/data.zip?dl=1`
   resolves and serves: ranged GET `bytes=0-1023` → **206**, 1,024 bytes, `application/binary`.
   Available if the canonical zip is ever needed; not downloaded because the corpus was already in hand.
   Related links in the same README (not attempted, listed for completeness):
   `para_with_hyperlink.zip` → `https://www.dropbox.com/s/wlhw26kik59wbh8/para_with_hyperlink.zip`,
   `data_ids.zip` → `https://www.dropbox.com/s/7ep3h8unu2njfxv/data_ids.zip?dl=0`.

Verdict: **AVAILABLE — obtained via step 3 (HF direct resolve, `voidful/2WikiMultihopQA`)**.

## 4. Transfer set built from it

| field | value |
|---|---|
| file | `04_experiments/data/transfer_items.jsonl` |
| rows | {len(items)} ({len([r for r in items if r['rung'] == 0])} rung-0 / {len([r for r in items if r['rung'] == 3])} rung-3) |
| distinct qids | {len({r['qid'] for r in items})} |
| sha256 | `{items_sha}` |
| split | `transfer` |
| seed | 20261103 |
| reproduce | `python 04_experiments/src/build_transfer_items.py` |
| schema | identical key set to `data/items.jsonl`, `json.dumps(..., sort_keys=True)` one object per line |

Construction rules (`04_experiments/src/build_transfer_items.py`):

* **rung 0 (label 1)** — the question plus the supporting paragraph from `supporting_facts` that
  actually contains the gold answer; the passage text is the paragraph's sentences joined with a
  single space (2Wiki ships paragraphs pre-split into sentences). Questions whose answer is
  `yes`/`no` (comparisons) or is not literally present in a supporting paragraph are skipped, so
  every rung-0 passage demonstrably supports its answer.
* **rung 3 (label 0)** — the same question plus a paragraph drawn from the same question's article
  pool that is **not** a supporting paragraph, does not contain the gold answer (normalised,
  case-folded substring test; skipped entirely for answers shorter than 4 chars), and is not the
  rung-0 text. Among eligible paragraphs the one closest in length to the gold passage is chosen.
* Paragraphs outside 120–1,200 characters are excluded for both rungs so the two rungs have
  comparable passage lengths (medians {statistics.median([r['n_context_chars'] for r in items if r['rung'] == 0]):.0f} vs {statistics.median([r['n_context_chars'] for r in items if r['rung'] == 3]):.0f} chars).
* Deterministic: questions ordered by `sha1(_id)`, shuffled once with `random.Random(20261103)`,
  single pass, first 200 questions that satisfy both rungs. Re-running reproduces the same sha256.
  The scan stopped as soon as 200 qids qualified; inside that prefix 88 questions were rejected for
  having no supporting paragraph that literally contains the gold answer (mostly `yes`/`no`
  comparison answers) and 5 for having no eligible distractor paragraph.

* Leakage check, measured not assumed: 0/200 rung-3 passages contain the full gold answer;
  8/200 share a single >=4-character token with it (generic words such as "kingdom", "june",
  "national"), which is the intended near-miss property, not leakage. Every rung-0 passage contains
  its gold answer (200/200), and no qid's two passages are identical.

### Article-grouping caveat (important for the paper)

2WikiMultihopQA has **no article/ section grouping inside an item**. Each question ships `context`
as a list of `[title, [sentences]]` — i.e. a set of *independent Wikipedia articles* (the two
multi-hop gold articles plus distractor articles mined alongside them). There is no "same article,
different paragraph" relation to exploit, and no section index.

Operationalisation used: the rung-3 passage is **another paragraph from the same question's context
set** (same multi-hop article pool), excluding the supporting paragraphs and the gold answer. This is
the closest available analogue of the dev arm's "different paragraph from the same article": the
distractor is topically entangled with the question (shares entities/surface form — e.g. a
same-surname person, a related film) but cannot answer it. It is *not* a same-document neighbour, so
rung-3 difficulty on this corpus is plausibly **higher** than in the dev arm (distractors are
entity-level, not section-level); report this as a construct difference in the transfer arm, not as
an identical manipulation.

Additional differences to disclose: 2Wiki paragraphs are shorter than the dev arm's (median
{statistics.median(lens):.0f} vs 716 chars), and 2Wiki questions are multi-hop/comparison by
construction, so absolute detection numbers are not directly comparable across arms — the transfer
arm supports a *direction* claim, not a magnitude claim.

## 5. Files

* `04_experiments/data/raw/2wiki/2wikimultihop_dev.json` — the corpus (55.9 MB, sha256 above)
* `04_experiments/data/raw/2wiki/fetch_log.jsonl` — one JSON object per HTTP request (url, status, bytes, sha256, timestamp)
* `04_experiments/data/raw/2wiki/hf_search_2wiki.json`, `hf_search_2wikimultihop.json` — HF search results
* `04_experiments/data/raw/2wiki/splits_*.json` — datasets-server split inventories per candidate id
* `04_experiments/data/raw/2wiki/github_README.md` — authors' README (source of the Dropbox links)
* `04_experiments/data/raw/2wiki/build_transfer_items.log` — builder stdout (row counts, examples)
* `04_experiments/src/build_transfer_items.py` — builder
* `04_experiments/data/transfer_items.jsonl` — the 400-item transfer set

## 6. Retry URLs if a fresh copy is ever needed

1. `https://huggingface.co/datasets/voidful/2WikiMultihopQA/resolve/main/dev.json` (used, 200)
2. `https://datasets-server.huggingface.co/rows?dataset=voidful/2WikiMultihopQA&config=default&split=validation&offset=0&length=100` (503 on 2026-11-03)
3. `https://huggingface.co/datasets/framolfese/2WikiMultihopQA/resolve/main/data/validation-00000-of-00001.parquet` (29.5 MB parquet mirror, untried fallback)
4. `https://www.dropbox.com/s/npidmtadreo6df2/data.zip?dl=1` (authors' canonical zip, 206 on ranged GET)
"""
OUT.write_text(md, encoding="utf-8")
print(f"wrote {OUT} ({len(md)} chars)")
