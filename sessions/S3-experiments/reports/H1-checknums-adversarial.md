# H1 — adversarial edge-case tests for `tools/check_numbers.py`

Session: S3 (subagent). Date: 2026-11-03. Rule of engagement: **add-only** — no change to
`tools/check_numbers.py`, `tools/lib/*`, `tools/CONTRACTS.md`, `RULES.md` or any existing
test. The five defects below are reported, not fixed.

## 1. Files

| File | Status |
|---|---|
| `tools/tests/test_check_numbers_adversarial.py` | **new** (42 tests: 37 pass, 5 `xfail`) |
| `sessions/S3-experiments/reports/H1-checknums-adversarial.md` | **new** (this report) |
| `tools/check_numbers.py`, `tools/lib/*`, `tools/CONTRACTS.md`, `RULES.md`, `tools/tests/test_check_numbers.py` | untouched |

No `tools/tests/fixtures/checknums_adv/` directory was needed: every case builds a tiny repo
(draft + `index.json` + results JSON + empty `exempt.json`) under pytest's `tmp_path` and
drives `cn.main([... --json --quiet --no-write])` in-process. Two consequences worth knowing:

- `--exempt` always points at an **empty** config written per case, so the shipped
  `04_experiments/config/exempt_numbers.json` cannot mask a tokeniser bug;
- `--no-write` means no report is ever written to `06_review/audits/`, and nothing is written
  under `05_paper/draft/` or `04_experiments/`. `write_text(..., newline="")` is used so the
  CRLF case really writes CRLF on Windows instead of being normalised by Python.

## 2. Commands and real output

```
$ python -m pytest tools/tests/test_check_numbers_adversarial.py -q
....x..x........x.....x...x...............
37 passed, 5 xfailed in 1.32s
```

```
$ python -m pytest tools/tests/test_check_numbers_adversarial.py -q -rxX
XFAIL ...::TestNumberFormats::test_european_thousands_separator_is_not_silently_truncated - BUG: European '1.234,56' splits into 1.234 + 56; the integer part is compared (and can MATCH) as if it were the whole number
XFAIL ...::TestNumberFormats::test_percent_with_a_space_before_the_sign_matches - BUG: '12.3 %' (space before %) is parsed as plain 12.3, so a correct percentage is reported MISMATCH
XFAIL ...::TestRoundingTolerance::test_zero_point_five_zero_percent_is_not_one_half - BUG: '0.50%' (=0.005) MATCHes stored 0.5 via the percent-units fallback, a 100x error reported as traced
XFAIL ...::TestMarkerPlacement::test_stacked_markers_do_not_silently_discard_one - BUG: a second stacked % num: marker is silently discarded; the number is checked only against the last one
XFAIL ...::TestStructuralNumbers::test_bare_equation_number_is_not_a_result - BUG: a bare equation number '(1)' is UNTRACEABLE unless the word 'Equation' precedes it
37 passed, 5 xfailed in 1.32s
```

`--runxfail` (the same suite with the five bugs promoted to failures) reports exactly those
five and nothing else: `5 failed, 37 passed in 0.91s`.

```
$ python -m pytest tools/tests/test_check_numbers.py -q
..............................................                           [100%]
46 passed in 0.90s
```

The pre-existing suite is unchanged at 46/46. The whole directory:

```
$ python -m pytest tools/tests -q
1 failed, 297 passed, 8 xfailed in 22.05s
```

The single failure is **pre-existing and unrelated**:
`test_docs_and_cli.py::test_contracts_s1_verified_citations_columns` — the repo's
`02_literature/verified_citations.csv` header (`id,url,doi_or_arxiv,retrieved_on,verified_by_command`)
disagrees with CONTRACTS §1. It mentions neither this file nor `check_numbers.py`; H2 saw four
such failures, so another session is actively changing that area.

```
$ git status --porcelain -- tools/tests/test_check_numbers_adversarial.py sessions/S3-experiments/reports/
?? sessions/S3-experiments/reports/
?? tools/tests/test_check_numbers_adversarial.py
```

(The repo is largely uncommitted, so `git status` also lists many files this task did not
touch. `06_review/audits/numbers-audit.md` still carries its 02:46 timestamp — `--no-write`
means the suite never rewrote it.)

## 3. What the 42 tests cover

**Number formats (10).** `1.2e-3` and `3E+05` match their stored values (exponent parsed, not
truncated to the mantissa); U+2212 `−0.5` keeps its sign while `0.5` next to it does not;
`1,234,567` is **one** token equal to 1234567; `+0.5` and `0.5x` are the same number as 0.5;
`12.3%` matches 0.123 and its evidence names the percentage reading; `12.3 %` must match too
(**bug 2**); `p<0.001` is a finding when unmarked and matches when marked (p-values get no
blanket exemption), `n=150` matches; `0.80`-`0.85` are two separately marked numbers and
marking only the lower bound still flags `0.85`; `~0.9` matches but `~` is not an exemption
(a one-character bypass would otherwise exist); `1/3` yields two untraceable digits rather
than being exempted as a path or list marker.

**Rounding (5).** Stored `0.8703706667` accepts `0.8704` (4dp) and `0.87` (2dp) and rejects
`0.871` — see §5 for the rule asserted and why. `50%` matches stored 0.5; `0.50%` must not
(**bug 3**).

**Marker placement (8).** Markdown marker on the line above binds the next number; a trailing
Markdown marker binds the number to its left; `% num:id` + blank line binds the next non-blank
line (documented) but a marker five lines above a number must **not** bind it (asserted as
`UNBOUND_MARKER` *and* `UNTRACEABLE`, so neither half is silent); the LaTeX table-row pattern
(marker above the row + trailing marker for the second cell) binds two ids to two numbers;
trailing whitespace inside both marker syntaxes is tolerated; stacked markers must not
silently drop one (**bug 4**); a `num:` marker inside a two-line HTML comment is reported as
`UNBOUND_MARKER` and matches nothing rather than silently vouching for a distant number.

**Structural numbers (4).** One paragraph containing `## 3. Results`, `Figure 2`, `Table 3`,
`Section 4.1`, `[12]`, `[12, 15]`, `2020-2024`, `10.1000/xyz`, `arXiv:1706.03762`, `v2.1.3`
and a URL with a query string produces **zero** findings, and each form is excused by its own
named rule (no catch-all); a bare equation number `(1)` is asserted exempt (**bug 5**); an
HTML comment and a LaTeX `%` comment that mention numbers contribute **zero tokens**; a
`% num:a` lookalike inside a Markdown fenced block creates no marker and does not launder the
example number.

**Marker/index integrity (7).** Missing results file, JSON-object value and `null` value are
all `INDEX_ERROR` with a reason that names the file/key; a numeric **string** `"0.812"` and a
float `0.812` both match; the same id used twice for the same value passes (both occurrences
matched), used twice for different values flags the disagreeing one and still matches the
other; a `"toy": true` entry whose value is wrong reports `MISMATCH` both with and without
`--allow-toy` (the toy flag must relax provenance only, never the value comparison).

**Files (6).** `\SI{0.812}{}` is a printed number and must be marked (and a `% num:` above it
binds the number inside the braces); CRLF keeps both the value and the reported line number;
a UTF-8 BOM does not hide the first marker in `.md` or `.tex`; tabs change nothing; empty
`.md` and `.tex` files exit 0 with `n_tokens == 0`; a directory scan audits every `.md`
recursively — including `sub/README.md` — while skipping `__pycache__`.

## 4. Bugs found (lead to fix; tests are `xfail(strict=False)`)

Reproductions below are real runs of the tool (in-process `main()`, exit codes and report
fields as printed).

### 4.1 A space before `%` turns a percentage into a plain number — false `MISMATCH`

```
Rate <!-- num:a -->12.3 %<!-- /num --> of runs.        (stored 0.123)
-> exit 1: MISMATCH :: printed '12.3' = 12.3 but stored is 0.123; diff 12.177 > allowed 0.05
Rate <!-- num:a -->12.3%<!-- /num --> of runs.         (stored 0.123)
-> exit 0, MATCH
```

`NUMBER_RE`'s `(?P<suffix>%|…)` only fires when `%` is glued to the digits, and the
`PERCENT_WORD_RE` fallback accepts `percent|per cent|pct` but not a spaced `%`. A thin space
before `%` is standard typography (siunitx `\SI{12.3}{\percent}` prints one; house styles
require one), so a correct draft is flagged and the author's only remedy is to change the
typography. Fix direction: allow `\s*%` in the suffix check (and consume the space so the
column arithmetic stays honest).

### 4.2 A stacked second `% num:` marker is silently discarded — a wrong marker disappears

```
% num:a        <- entry a = 0.9
% num:b        <- entry b = 0.812
0.812 \\
-> exit 0; findings []; matched ids ['b']
```

Both markers bind the same token (each looks at the next lines and finds it), but
`audit_file` builds `covered[id(tok)] = mk` in a loop, so the later marker overwrites the
earlier. Marker `a` still has `bound == [tok]`, so it is **not** reported as
`UNBOUND_MARKER`; its claim of 0.9 is never compared. A stale marker left above a live one is
exactly the artefact the tool exists to catch, and here it is invisible. Fix direction: either
refuse a token claimed by more than one marker (report the surplus as `UNBOUND_MARKER`), or
check the token against every marker that bound it.

### 4.3 `0.50%` (0.005) is accepted as a stored `0.5` — 100× error reported as traced

```
Only <!-- num:a -->0.50%<!-- /num --> diverged.        (stored 0.5)
-> exit 0; evidence: printed '0.50%' vs stored 0.5; stored value is already in percent
   units; diff 0.00 <= allowed 0.00500
```

`compare()` offers two readings for any percent token: "printed/100 vs stored" and
"printed vs stored". The second exists for results files that store `81.2` rather than
`0.812`, but it also accepts `0.50%` as `0.5`. The two readings cannot both be right for one
token: the fraction reading says 0.005, the percent reading says 0.5. Fix direction: only use
the percent-units reading when the fraction reading is *impossible* (e.g. `|printed/100 -
stored|` exceeds the window **and** `|printed - stored|` is within it **and** stored > 1, or
prefer the fraction reading whenever `stored <= 1`). Test asserts `MISMATCH`.

### 4.4 European `1.234,56` is split into `1.234` + `56`, and the integer part can MATCH

```
tokens for "Value 1.234,56 here.": [('1.234', '1.234'), ('56', '56')]
Value <!-- num:a -->1.234<!-- /num -->,56 g.           (stored 1.234)
-> exit 1, but a MATCH row is emitted: printed '1.234' vs stored 1.234
```

`NUMBER_RE` knows the Anglo grouping `\d{1,3}(,\d{3})+` but not the European `1.234,56`, so
the integer part becomes a complete-looking token that matches a value 1000× smaller and is
printed as traced evidence, while the fractional remainder is flagged separately. A marker
around the whole number produces two `MISMATCH`es, so a correctly written European draft can
never pass. Fix direction: either recognise `\d{1,3}(\.\d{3})+,\d+` as one token, or reject
it loudly (an `UNTRACEABLE`/`INDEX_ERROR`-style finding saying "locale-formatted number").

### 4.5 A bare equation number `(1)` is `UNTRACEABLE`

```
The loss in (1) is minimised.              -> exit 1: UNTRACEABLE token '1'
The loss in Equation (1) is minimised.     -> exit 0 (float_prefix)
```

The module docstring lists "equation numbers" among the exemptions and `RULE_DOC` says the
same, but only the `Equation (1)` spelling matches `FLOAT_PREFIX_RE`; a parenthesised number
standing alone is treated as a result. Real papers cross-reference equations as `(1)` or
`Eq. (1)` all the time. Fix direction: exempt a token that is exactly `(\d+)` and is not
inside a marker (a parenthesised integer is never a measured value), or add a named
`equation_number` rule so the exemption stays visible in the report.

## 5. Rule choices asserted deliberately (not bugs)

- **Rounding.** The asserted rule is the tool's documented one: the window is *half of the
  last printed decimal place* (0.0005 for `0.871`), never a fixed dp count. `0.8703706667`
  therefore accepts `0.8704` and `0.87` and rejects `0.871` — 0.871 is not the correctly
  rounded form at 3dp (0.870) or 2dp (0.87), so accepting it would require an arbitrary
  tolerance the index never declared. The supported escape hatch is asserted in the same
  test: an entry with `"tolerance": 0.001` **does** accept `0.871`.
- **LaTeX marker + blank line.** The brief suggested a blank line should sever `% num:id`.
  I asserted the opposite (it binds the next non-blank line) because that is what the tool
  documents in `find_markers`/`bind_markers`, and because a comment followed by a blank line
  is normal LaTeX layout. The dangerous half of the same rule is pinned separately: a marker
  must not reach a number more than four lines away, and that case must produce *both*
  `UNBOUND_MARKER` and `UNTRACEABLE`.
- **Directory scan.** Documented behaviour is asserted: every `.md`/`.tex` under `--draft` is
  a draft (only `SKIP_DIRS` are skipped), so `sub/README.md` **is** audited and its number is
  a finding. That is the contract, and the consequence is worth stating in the docs: a draft
  directory must contain drafts only — a README placed beside the sections will fail the
  audit. If a README exclusion is wanted, it is a tool change plus a `RULE_DOC` line, not a
  test change.

## 6. Limitations of this suite

- **No LaTeX environment awareness.** `%` inside `verbatim`/`lstlisting` is literal text, but
  the tool treats every `%` as a comment, so a `% num:id` line inside a code listing is a
  marker (and can bind a number outside the listing). Not asserted as a bug — it would need
  environment tracking the tool never claims — but worth knowing before a draft embeds LaTeX
  examples. The Markdown fenced-block case *is* covered and behaves safely.
- **No inline code-span awareness** in Markdown: `` `--context 60` `` in prose is an
  untraceable `60`. Fail-safe, out of the brief's scope, not asserted.
- **Rounding at exponent boundaries** is asserted only through the documented half-ulp rule
  (`1.2e-3` → half-ulp 0.00005, matching the existing `3e-4` test); whether that is the
  *physically* right precision for scientific notation is a design question, not a bug.
- **`--exempt` config interaction** is deliberately excluded (empty config per case), so these
  tests say nothing about the shipped pattern list; the existing suite covers it.
- **Locale coverage is one case.** `1.234,56` is the only European form tested; `1 234,56`
  (space grouping) is not.
- **No performance/scale test** (huge drafts, pathological regex backtracking).
- The five `xfail`s are `strict=False`, so if the lead fixes a bug the test will report
  XPASS rather than failing the suite — flip them to `strict=True` (or drop the marker) once
  the fix lands, so a regression cannot silently return.
