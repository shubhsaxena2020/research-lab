# CONTRACTS — shared data formats (binding for all S3 tooling)

Every tool in this lab reads/writes the formats below. Do not invent a variant.
All paths are relative to the repo root `C:\Users\shubh\research-lab`.
All JSON is UTF-8, `ensure_ascii=False`, sorted keys where keys are a set.

---

## 1. Citations: `02_literature/citations.csv` (input) and `verified_citations.csv` (register)

### 1a. The register — ONE schema, owned by S2's tool

`02_literature/verified_citations.csv` is a single file with a single schema. It was briefly
two (S2's 9-column register vs S3's 12-column output, written to the same path), which made
`citations_to_bib.py` and `claims_audit.py` unable to read it. The canonical schema is S2's,
because S2 owns the file; S3's verifier writes exactly these columns too. The mapping lives in
`tools/lib/citation_schema.py` — import it, never re-implement it.

```
id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command
```

- `id`      : required, unique key used to reference the citation in the draft (`\\cite{id}`).
- `title`   : required.
- `authors` : `;`-separated, `Surname, Given` or `Given Surname`. Used for the author check.
- `year`    : 4-digit year. Used for the year check (±1 year tolerance).
- `venue`   : informational only, never used for verification.
- `url`     : the page the record was resolved from (OpenAlex/DOI/arXiv).
- `doi_or_arxiv` : one column holding either a bare DOI (`10.x/y`) or `arXiv:xxxx.xxxxx`.
- `retrieved_on` : ISO date the row was checked.
- `verified_by_command` : the exact command + evidence that proved the row.

Output `02_literature/verified_citations.csv` — exactly these columns, in this order:

```
id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command
```

**There is no `status` column.** A row that is not verified belongs in a report, never in this
file (RULES.md #1). Any consumer that needs a status treats a row carrying
`verified_by_command` as VERIFIED; `citation_schema.normalize_row()` does this for you and
also accepts the older 12-column form (`key,...,status,source,source_url,retrieved_at`) and
S2's staging files (`02_literature/staging/*.csv`).

### 1b. Input to `tools/verify_citations.py`

A CSV of *candidates* to be resolved — either the schema above, or this simplest form:

```
key,title,authors,year,doi,arxiv_id,venue
vaswani2017,Attention Is All You Need,"Vaswani, Ashish; Shazeer, Noam",2017,10.48550/arXiv.1706.03762,1706.03762,NeurIPS
```

A `.bib` file works too (`--bib`); no external BibTeX library is needed.

Full report (all statuses) is written to `02_literature/verification_report.json` and
`verification_report.md`:

```json
{"generated_at": "...", "n_total": 12, "n_verified": 10, "n_mismatch": 1, "n_not_found": 1,
 "results": [{"key": "...", "status": "MISMATCH", "confidence": 0.62,
              "evidence": {"title_ratio": 0.62, "authors_ratio": 0.5, "year_delta": 2,
                           "resolved_title": "...", "resolved_authors": [...],
                           "resolved_year": 2019, "source": "crossref",
                           "source_url": "https://api.crossref.org/works/10.x/y",
                           "matched_doi": "10.x/y", "matched_arxiv_id": null},
              "reasons": ["title too dissimilar: 0.62 < 0.90", "year delta 2 > 1"],
              "checked_at": "..."}]}
```

`status` is exactly one of `VERIFIED`, `MISMATCH`, `NOT_FOUND`, or `ERROR` (network/parse
failure — NOT a pass; `ERROR` never counts as verified).

---

## 2. Experiment runs: `04_experiments/runs/<run_id>/`

`run_id` = `<UTC date>T<UTC time>Z_<config_name>_<short git hash>`, e.g.
`20261103T014500Z_baseline_a1b2c3d`.

```
runs/<run_id>/
  meta.json        # provenance, see below
  config.json      # exact resolved config used (copy, not a pointer)
  stdout.log
  stderr.log
  results.json     # metric dict, see below
  artifacts/       # optional per-run files (predictions, checkpoints)
```

`meta.json`:

```json
{"run_id": "...", "config_name": "baseline", "config_sha256": "...",
 "git_commit": "a1b2c3d", "git_dirty": false, "python": "3.11.15",
 "platform": "Windows-11...", "command": "python experiments/train.py --config configs/baseline.json",
 "started_at": "...", "finished_at": "...", "duration_s": 12.4,
 "peak_rss_mb": 210.5, "device": "cpu", "cpu_count": 8, "seed": 0,
 "host": "...", "env": {"PYTHONHASHSEED": "0"}, "notes": ""}
```

`results.json` — flat dict of scalar metrics plus a `_meta` block. Nested dicts allowed one
level only; every leaf must be `int`/`float`/`str`/`bool`/`null`.

```json
{"_meta": {"run_id": "...", "config_name": "baseline", "seed": 0, "split": "test", "n": 1000},
 "accuracy": 0.812, "f1_macro": 0.79, "loss": 0.4123}
```

Metric *names* are the stable contract: `accuracy`, `f1_macro`, `loss`, ... A results file
with a renamed metric breaks `check_numbers.py` and the table generator.

---

## 3. Results index: `04_experiments/RESULTS-INDEX.json`

The single map from "a number in the paper" to "the file that produced it".

```json
{"version": 1,
 "updated_at": "...",
 "entries": [
   {"id": "main.accuracy.baseline",
    "file": "04_experiments/results/main_baseline.json",
    "key": "accuracy",
    "description": "Test accuracy, baseline, seed 0",
    "run_id": "20261103T014500Z_baseline_a1b2c3d",
    "tolerance": 0.0005}
 ]}
```

- `id` is what the draft cites in a marker comment: `<!-- num:main.accuracy.baseline -->0.812<!-- /num -->`
  in Markdown, `% num:main.accuracy.baseline` immediately above the number in LaTeX.
- `file` is relative to repo root. `key` is a dotted path into that JSON
  (`accuracy`, or `_meta.n`).
- `tolerance` (optional, default 0.0) — relative tolerance used when matching a printed
  number to the stored value.
- Files under `04_experiments/results/` are the *aggregated* per-experiment results,
  copied from `runs/<run_id>/results.json` by the harness (`aggregate` command).

---

## 4. Aggregated results + statistics

`04_experiments/results/summary_<experiment>.json`:

```json
{"experiment": "main", "configs": ["baseline", "ours"], "metric": "accuracy",
 "n_seeds": 5, "seeds": [0,1,2,3,4],
 "per_run": {"baseline": [0.79, 0.80, 0.81, 0.79, 0.80]},
 "stats": {"baseline": {"mean": 0.798, "std": 0.0075, "ci95": [0.790, 0.806],
                        "n": 5, "ci_method": "bootstrap", "n_boot": 10000,
                        "ci_seed": 12345},
           "ours": {"mean": 0.910, "std": 0.011, "ci95": [0.900, 0.920], "n": 5,
                    "ci_method": "bootstrap", "n_boot": 10000, "ci_seed": 12345}},
 "paired": {"test": "wilcoxon", "p_value": 0.0312, "effect_size": {"name": "cohens_d", "value": 1.84},
            "n_pairs": 5, "correction": {"method": "holm", "family_size": 3, "p_adjusted": 0.0312,
            "note": "3 comparisons in this family"}},
 "tables": [{"caption": "Main results", "path": "04_experiments/results/table_main.md"}]}
```

Rules: bootstrap CIs always report `n_boot` and `ci_seed`. Any p-value reported in the paper
must carry the correction method and family size. Effect sizes always named.

---

## 5. Toy pipeline (clearly labelled, never a result)

`04_experiments/toy/` — end-to-end dry run. Every file carries `"toy": true` in JSON and a
`TOY — NOT A RESULT` banner in text/markdown. `check_numbers.py --allow-toy` is required to
accept numbers from it; without that flag toy numbers are flagged as untraceable.

---

## 6. Tool CLI conventions

Every tool: `python tools/<tool>.py --help` works; exit code 0 = pass, 1 = findings/failure,
2 = usage error. `--json` prints machine-readable output to stdout. No tool writes outside the
repo root. No tool makes a network call unless the flag `--online` is passed (default offline,
so tests and CI never hit the network). Polite by default: 1 request/second/host, descriptive
User-Agent, exponential backoff on 429/5xx (30/60/120 s, max 3 attempts).

---

## 7. Addendum — things learned by running the toolchain (2026-11-03)

**7.1 An index entry may point at a config file.** The schema in §3 says `file` is a results
file; in practice protocol constants (learning rate, epochs, points per class, number of
seeds) are not *results*, they are *settings*, and their evidence is the config that was
actually used. Pointing the entry at `04_experiments/harness/configs/<name>.json` keeps them
traceable to committed evidence instead of exempting them. `run_id` is optional for such
entries. `aggregate.py` preserves hand-added entries whose ids it does not own — verified by
re-running it and confirming `toy.protocol.*` survives.

**7.2 Free bibliographic APIs are not always available.** From this network on 2026-11-03,
OpenAlex answered `429` with `Retry-After: 15859` (per-IP credit exhausted) and Semantic
Scholar answered `429` as well; Crossref, arXiv and DataCite were healthy. Consequences baked
into the tools:

- title search order is Crossref bibliographic → OpenAlex → Semantic Scholar;
- `404` from Crossref for a DOI falls through to DataCite (arXiv's `10.48550/*` DOIs are
  registered there, not with Crossref);
- a `429` whose `Retry-After` exceeds 120 s marks that host exhausted **for the rest of the
  run** rather than sleeping through the 30/60/120 ladder, which is both pointless and
  impolite;
- the report records `sources_unavailable`, so a run that only looked at two of four indexes
  says so instead of implying a thorough search.

**7.3 `ERROR` is a first-class status.** A network failure must never render as `NOT_FOUND`
("this paper does not exist") or as `VERIFIED`. `verify_citations.py` converts a
`NOT_FOUND`-with-transport-errors into `ERROR`, and `ERROR` never counts toward the verified
total.

**7.4 Toy artefacts are refused by default.** `check_numbers.py --allow-toy`,
`make_figures.py --allow-toy` and `make_digest.py` all refuse numbers whose index entry is
marked `"toy": true` unless told otherwise; `make_tables.py` refuses a toy summary
unconditionally, because a paper table is exactly where a toy number would slip through.

