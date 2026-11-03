# Transfer corpus: 2WikiMultihopQA dev — acquisition record

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
| sha256 | `48b9bdc69654dc580fda5f935a48b88cb89f11887587310af60d406c8d0111a6` |
| rows | 12,576 (dev/validation) |
| fields per row | `_id, type, question, context, supporting_facts, evidences, answer` |
| question types | compositional 5,236, comparison 3,040, bridge_comparison 2,751, inference 1,549 |
| paragraphs per question | median 10 |
| paragraph length (chars) | median 203, mean 355 |

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
| 1 | 1a-hf-search-2wiki | 200 | 36,784 | `af468dc47492423e…` | https://huggingface.co/api/datasets?search=2wiki&limit=100
| 2 | 1b-hf-search-2wikimultihop | 200 | 18,580 | `87a116b9c28949e0…` | https://huggingface.co/api/datasets?search=2wikimultihop&limit=100
| 3 | 2-splits-0 | 200 | 260 | `6025124ee757cb9b…` | https://datasets-server.huggingface.co/splits?dataset=voidful/2WikiMultihopQA
| 4 | 2-splits-1 | 200 | 111 | `b0907f139df067bb…` | https://datasets-server.huggingface.co/splits?dataset=thinkall/2WikiMultihopQA
| 5 | 2-splits-2 | 501 | 205 | `cb7ef9f1e6ebfb41…` | https://datasets-server.huggingface.co/splits?dataset=xanhho/2WikiMultihopQA
| 6 | 2-splits-3 | 200 | 269 | `611b2a3cf768fd58…` | https://datasets-server.huggingface.co/splits?dataset=framolfese/2WikiMultihopQA
| 7 | 2-splits-4 | 200 | 266 | `c123cda1d90af5e6…` | https://datasets-server.huggingface.co/splits?dataset=ohjoonhee/2WikiMultihopQA
| 8 | 2-splits-5 | 501 | 284 | `54ea6de885b7fdb7…` | https://datasets-server.huggingface.co/splits?dataset=kamelliao/2wikimultihopqa
| 9 | 3a-rows-voidful__2WikiMultihopQA-page0 | 503 | 162 | `258c66556e2e065b…` | https://datasets-server.huggingface.co/rows?dataset=voidful/2WikiMultihopQA&config=default&split=validation&offset=0&length=2
| 10 | 3a-debug-voidful-text | 503 | 162 | `258c66556e2e065b…` | https://datasets-server.huggingface.co/rows?dataset=voidful/2WikiMultihopQA&config=default&split=validation&offset=0&length=2
| 11 | 3b-rows-framolfese | 503 | 162 | `258c66556e2e065b…` | https://datasets-server.huggingface.co/rows?dataset=framolfese/2WikiMultihopQA&config=default&split=validation&offset=0&length=1
| 12 | 3b-rows-ohjoonhee | 503 | 162 | `258c66556e2e065b…` | https://datasets-server.huggingface.co/rows?dataset=ohjoonhee/2WikiMultihopQA&config=default&split=validation&offset=0&length=1
| 13 | 2b-tree-voidful | 200 | 403 | `c525d75aa9aeb113…` | https://huggingface.co/api/datasets/voidful/2WikiMultihopQA/tree/main?recursive=true
| 14 | 2b-tree-framolfese | 200 | 1,563 | `5cdcce5862c2a5d5…` | https://huggingface.co/api/datasets/framolfese/2WikiMultihopQA/tree/main?recursive=true
| 15 | 2b-tree-ohjoonhee | 200 | 1,562 | `0ba18865a3bb42ea…` | https://huggingface.co/api/datasets/ohjoonhee/2WikiMultihopQA/tree/main?recursive=true
| 16 | 2b-tree-thinkall | 200 | 993 | `a13926928e993026…` | https://huggingface.co/api/datasets/thinkall/2WikiMultihopQA/tree/main?recursive=true
| 17 | 2a-resolve-voidful-dev.json | 200 | 55,934,464 | `48b9bdc69654dc58…` | https://huggingface.co/datasets/voidful/2WikiMultihopQA/resolve/main/dev.json
| 18 | 2a-resolve-voidful-README | 404 | 15 | `f36668ddf22403a3…` | https://huggingface.co/datasets/voidful/2WikiMultihopQA/resolve/main/README.md
| 19 | 3-3-github-README-master | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihopqa/master/README.md
| 20 | 3-3-github-dev-master | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihopqa/master/dev.json
| 21 | 3-3-github-dev-main | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihopqa/main/dev.json
| 22 | 3-3-github-data-dev-master | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihopqa/master/data/dev.json
| 23 | 3-3-github-LICENSE-master | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihopqa/master/LICENSE
| 24 | 3-lic-framolfese-README | 200 | 5,462 | `1f5b8791e8fede71…` | https://huggingface.co/datasets/framolfese/2WikiMultihopQA/resolve/main/README.md
| 25 | 3-ghorg-repos | 200 | 172,739 | `7bb7b00837bbcfeb…` | https://api.github.com/orgs/Alab-NII/repos?per_page=100
| 26 | 3-ghsearch | 200 | 23,057 | `b3fa762ba8478cef…` | https://api.github.com/search/repositories?q=2wikimultihopqa+in:name
| 27 | 3-gh-readme-master | 200 | 7,114 | `bb0cf42315c4e65c…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/README.md
| 28 | 3-gh-dev-master | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/dev.json
| 29 | 3-gh-dev-main | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihop/main/dev.json
| 30 | 3-gh-data-dev-master | 404 | 14 | `d5558cd419c8d46b…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/data/dev.json
| 31 | 3-gh-license | 200 | 11,337 | `b8c1d7752e71597a…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/LICENSE
| 32 | 3-gh-readme-cached | 200 | 7,114 | `bb0cf42315c4e65c…` | https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/README.md
| 33 | lic-api-voidful | 200 | 447 | `070feb008107f405…` | https://huggingface.co/api/datasets/voidful/2WikiMultihopQA
| 34 | lic-api-framolfese | 200 | 2,290 | `e01620bfd3cefb73…` | https://huggingface.co/api/datasets/framolfese/2WikiMultihopQA
| 35 | 4-dropbox-data.zip-ranged-1KB | 206 | 1,024 | `6e5afcf1e393c01f…` | https://www.dropbox.com/s/npidmtadreo6df2/data.zip?dl=1

### What each step showed

1. **HuggingFace search API** — `?search=2wiki` returned 68 dataset ids (full list in
   `raw/2wiki/hf_search_2wiki.json`), including `voidful/2WikiMultihopQA`, `thinkall/2WikiMultihopQA`,
   `xanhho/2WikiMultihopQA`, `framolfese/2WikiMultihopQA`, `ohjoonhee/2WikiMultihopQA`,
   `kamelliao/2wikimultihopqa`. Candidate ids probed for splits: `voidful/2WikiMultihopQA`, `thinkall/2WikiMultihopQA`, `xanhho/2WikiMultihopQA`, `framolfese/2WikiMultihopQA`, `ohjoonhee/2WikiMultihopQA`, `kamelliao/2wikimultihopqa`.
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
| rows | 400 (200 rung-0 / 200 rung-3) |
| distinct qids | 200 |
| sha256 | `2ae0ce0c40aa8a70828ae8aa775621dc5fe4cdcdcfdad0795d362ee01d6a1e09` |
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
  comparable passage lengths (medians 352 vs 287 chars).
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
203 vs 716 chars), and 2Wiki questions are multi-hop/comparison by
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
