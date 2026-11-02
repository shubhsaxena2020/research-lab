# H2 — adversarial tests for `tools/verify_citations.py`

Session: S3 (subagent). Date: 2026-11-03. Rule of engagement: **add-only** — no change to
`tools/*.py`, `tools/lib/*`, `tools/CONTRACTS.md`, `RULES.md` or any existing test.

## 1. Files

| File | Status |
|---|---|
| `tools/tests/test_verify_citations_adversarial.py` | **new** (39 tests, all offline) |
| `sessions/S3-experiments/reports/H2-cite-adversarial.md` | **new** (this report) |
| anything under `tools/lib/`, `tools/*.py`, existing tests | untouched |

No fixtures directory was needed: every API body is built inline and injected through the
tool's own `fetch(url) -> str` seam. `main()` is driven by monkeypatching
`netcache.make_fetcher`, so `--no-write`/`--json`/exit codes are exercised end to end without
a socket. All writes go to `tmp_path`.

## 2. Commands and real output

```
$ python -m pytest tools/tests/test_verify_citations_adversarial.py -q -rxX
....xx......................x..........
=========================== short test summary info ===========================
XFAIL tools/tests/test_verify_citations_adversarial.py::test_crossref_string_title_parser_returns_none_not_a_single_character - BUG: parse_crossref treats a string title as a sequence and keeps only its first character
XFAIL tools/tests/test_verify_citations_adversarial.py::test_crossref_author_as_dict_does_not_crash - BUG: parse_crossref raises AttributeError when message.author is a dict
XFAIL tools/tests/test_verify_citations_adversarial.py::test_survey_that_prefixes_the_target_title_is_not_verified - BUG: containment lift scores a longer survey title 0.95, so a title-only record verifies against a different paper
36 passed, 3 xfailed in 0.49s
```

```
$ python -m pytest tools/tests -q
4 failed, 257 passed, 3 xfailed in 22.39s
```

The 4 failures are **pre-existing and unrelated** — all in `tools/tests/test_docs_and_cli.py`
(`tools/check_all.py` missing from `CLI_SPEC`, a stale `ALLOWED_ABSENT` entry
`02_literature/verification_report.md`, and the `02_literature/verified_citations.csv`
header disagreeing with CONTRACTS §1). None of them mention this file; they reflect
in-flight work from other sessions on `tools/check_all.py` and the repo's current
`verified_citations.csv`.

```
$ git status --porcelain
?? tools/tests/test_verify_citations_adversarial.py      # the only file this task added
```

## 3. What is covered (39 tests)

**Hostile API bodies (14)** — HTML `429` page, truncated JSON, `{"message": {}}`,
Crossref `title` as a string, `author` as a dict, Atom feed with no `entry`, two-entry feed
(only the first may vouch), `&amp;` + CDATA title, 8 MB of whitespace (asserted `< 5 s`),
`PoliteFetcher.max_bytes` guard with a stubbed `urlopen` (oversized raises, under-cap passes),
UTF-8 BOM body, JSON-escaped `\u0000`, raw NUL byte.

**Record edges (12)** — accented (`Résumé of Naïve Bäyes`) and CJK titles round-trip from CSV
and verify; punctuation-only title; empty title + no id ⇒ ERROR; `doi:10.1000/XYZ` normalised
before the Crossref URL; `arXiv:1706.03762v5` queried as `id_list=1706.03762` (no `v5`);
old-style `cs/0112017`; duplicate CSV key (warning on stderr, `n_total == 1`); `and`
separators; trailing `;`; 40 authors; `van der Waals` particles (and the same-surname /
different-given-name rejection).

**Comparison traps (6)** — same title+year but different first author; anagram reordering;
6-word survey prefix; retracted arXiv variant one word apart; year off by 5; DOI that
resolves to a different paper.

**Status plumbing (4)** — Crossref `FetchError` + working title search ⇒ VERIFIED via title
(failure still recorded in `resolver.errors`); total fetch failure ⇒ ERROR; `''` everywhere ⇒
not VERIFIED; `main(['--csv', …, '--offline', '--no-write', '--json'])` ⇒ parsed JSON has
`n_verified == 0`, `n_error == n_total`, exit code 1.

**Write path (3)** — `--no-write` leaves `--out-dir` empty; `write_verified_csv` emits only
VERIFIED rows, every row with non-empty `source_url` + `retrieved_at`, and a MISMATCH result
whose evidence carries a Crossref URL never leaks; end-to-end `main()` over
VERIFIED/MISMATCH/NOT_FOUND/ERROR writes exactly one row and a report whose status counts
sum to `n_total`.

Policy assertion for the retracted arXiv item: **MISMATCH**, never VERIFIED — one word of
difference is a different claim, so the record must be re-checked by a human.

## 4. Bugs found (lead to fix; tests are `xfail(strict=False)`)

1. **`parse_crossref` truncates a string `title` to its first character.**
   `titles = msg.get("title")` is treated as a sequence, so
   `{"title": "Attention Is All You Need"}` yields `"A"`. Not a verification bypass (the
   result is MISMATCH), but the evidence recorded in `verification_report.json` is garbage and
   a genuinely short one-word title would collide with it. Fix: `if isinstance(titles, str):
   titles = [titles]`.
   Test: `test_crossref_string_title_parser_returns_none_not_a_single_character`.

2. **`parse_crossref` raises `AttributeError` when `message.author` is a dict.**
   `for a in msg.get("author") or []` iterates the dict's keys (strings), then `a.get(...)`
   explodes; the exception escapes `verify_record` and kills the whole batch. This violates
   the module's own contract ("Parsers … never raise on bad input (return None instead)") and
   is the only input in this suite that takes the tool down instead of degrading.
   Traceback: `verify_citations.py:191 in parse_crossref → AttributeError: 'str' object has
   no attribute 'get'`.
   Test: `test_crossref_author_as_dict_does_not_crash`.

3. **Containment lift lets a longer survey title verify a shorter record (false positive).**
   `matchlib.title_similarity` lifts any strict substring containment with ≥ 4 tokens to
   `0.95`, which clears the `0.90` gate. A title-only record `"Attention Is All You Need"`
   (year 2017) therefore comes out **VERIFIED (confidence 0.975)** against
   `"Attention Is All You Need: A Comprehensive Survey of Transformer Architectures in Vision,
   Speech, Language, and Beyond"` (2017, different author) returned by Crossref search.
   Reachable exactly when the CSV row has no author column — the common case for
   title-only registers. Risk: a different paper (survey, extended version, "revisited"
   follow-up) gets a `verified_citations.csv` row with a wrong DOI/URL.
   Suggested direction (lead's call): lift only when the *candidate* is the longer string
   (database truncated the record's title), and cap the extra-word count (e.g. ≤ 3 tokens) or
   require the extra text to look like a subtitle. Alternatively require `a_score is not None`
   before granting the lift.
   Test: `test_survey_that_prefixes_the_target_title_is_not_verified`.

Everything else held: exact-title repos, unicode, 40 authors, particles, duplicate keys,
BOM/NUL/8 MB bodies, FetchError-vs-'' plumbing and the write path all behaved correctly.

## 5. Limitations / judgement calls recorded (not bugs)

- A 200 response carrying an HTML error page (`429 Too Many Requests`) ends as **NOT_FOUND**,
  not ERROR: the parsers see no metadata and `resolver.errors` stays empty because no
  `FetchError` was raised. The task allowed either, but it means an error page is reported as
  "this paper does not exist". A body sniff (`body.lstrip()[:1] == "<"`) would upgrade it to
  ERROR.
- `{"message": {}}` yields a candidate with an empty title, so the verdict is MISMATCH (title
  ratio 0) rather than NOT_FOUND, and the DataCite fallback is skipped (`cand is not None`).
  Safe, but it hides a missing-title condition behind a "mismatched paper" label.
- `''` for every URL is treated as absence (NOT_FOUND) rather than ERROR. Intentional per the
  404-as-answer design in `netcache`; the test asserts only "never VERIFIED".
- Escaped `\u0000` in a title is accepted and normalises to a space, so an otherwise identical
  title still verifies. Harmless; asserted only as "no crash, no ERROR".
- `parse_arxiv` uses `root.find("entry")`, i.e. document order — safe for the real
  `max_results=1` query, and the two-entry test proves entry #2 cannot vouch.
- The 8 MB test measures wall time on the *parse* path; the byte cap itself lives in
  `PoliteFetcher` and is tested separately with a stubbed `urlopen`.
