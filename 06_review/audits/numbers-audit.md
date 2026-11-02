# Numbers audit

> **Scope: NOT a paper draft (fixture / toy / template path): a PASS here says the tool works, NOT that any draft passed its audit.**
> Audited path: `04_experiments/toy/draft_toy.md`

Draft: `04_experiments/toy/draft_toy.md`  
Index: `04_experiments/RESULTS-INDEX.json`  
Generated: 2026-11-02T21:16:00Z  
Toy numbers allowed: True

**PASS** — 0 finding(s) over 1 file(s).

| scanned | matched | exempt | untraceable | mismatch | dangling | index error | unbound |
|---|---|---|---|---|---|---|---|
| 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |

## Findings

None. Every numeric token is marked-and-matching or exempt.

## Matched numbers

| where | printed | marker | stored | evidence |
|-------|---------|--------|--------|----------|
| `04_experiments/toy/draft_toy.md:10` | `0.8704` | `toy.accuracy.toy_baseline` | `0.8703706667` | printed '0.8704' vs stored 0.8703706667; diff 0.0000293333 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `04_experiments/toy/draft_toy.md:11` | `0.8852` | `toy.accuracy.toy_ours` | `0.8851853333` | printed '0.8852' vs stored 0.8851853333; diff 0.0000146667 <= allowed 0.0005 (half last decimal 0.00005, entry tolerance 0.0005) |
| `04_experiments/toy/draft_toy.md:22` | `150` | `toy.protocol.n_per_class` | `150` | printed '150' vs stored 150; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `04_experiments/toy/draft_toy.md:25` | `400` | `toy.protocol.epochs` | `400` | printed '400' vs stored 400; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `04_experiments/toy/draft_toy.md:26` | `0.5` | `toy.protocol.lr` | `0.5` | printed '0.5' vs stored 0.5; diff 0.0 <= allowed 0.05 (half last decimal 0.05, entry tolerance 0.0) |
| `04_experiments/toy/draft_toy.md:27` | `3` | `toy.protocol.n_seeds` | `3` | printed '3' vs stored 3; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `04_experiments/toy/draft_toy.md:31` | `3` | `toy.protocol.n_pairs` | `3` | printed '3' vs stored 3; diff 0 <= allowed 0.5 (half last decimal 0.5, entry tolerance 0.0) |
| `04_experiments/toy/draft_toy.md:33` | `0.50` | `toy.protocol.p` | `0.5` | printed '0.50' vs stored 0.5; diff 0.00 <= allowed 0.005 (half last decimal 0.005, entry tolerance 0.0) |

## Rules this run applied

Exemptions are narrow by construction: each rule below is a named, fixed pattern in `tools/check_numbers.py` (or a pattern you supplied via `--exempt`). No catch-all.

- `year` — a bare 4-digit integer 1900-2100 (a calendar year, not a measurement)
- `section_number` — numbering of a Markdown heading ('## 3.1 Method') or after §
- `float_prefix` — number right after Figure/Table/Eq./Section/Algorithm/... (a label)
- `page_line` — number after p./pp./page/line, including ranges (12-14)
- `list_marker` — ordered-list numbering ('1.', '2)') at the start of a line
- `citation_number` — bracketed citation numbers: [12], [3, 5], [12-14]
- `doi` — digits inside a DOI (10.xxxx/...)
- `arxiv_id` — arXiv identifier (arXiv:1706.03762)
- `url` — digits inside an http(s):// or www. URL
- `file_path` — digits inside a file path (fig/plot3.pdf)
- `iso_date` — ISO date 2026-11-03
- `footnote_marker` — markdown footnote reference [^1]
- `latex_command_arg` — argument of \ref \label \cite \includegraphics \begin ...
- `latex_dimension` — LaTeX length: 11pt, 0.9\textwidth, width=0.5\linewidth
- `identifier_attached` — digit glued to a name (GPT-4, ResNet-50, v2, L2)
- `config_exempt` — number covered by a pattern in the --exempt config file

Extra patterns from `04_experiments/config/exempt_numbers.json`:

- `learning[-_ ]?rate\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9.]+(?:[eE][-+]?[0-9]+)?`
- `\blr\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9.]+(?:[eE][-+]?[0-9]+)?`
- `dropout(?:\s*(?:rate|probability|p))?\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9.]+`
- `batch[-_ ]?size\s*(?:=\s*|:\s*|of\s+|is\s+)?[0-9,]+`
- `\bepochs?\s*(?:=\s*|:\s*)[0-9,]+`
- `\b[0-9]+\s*epochs?\b`
- `\bseed\s*(?:=\s*|:\s*)?[0-9]+`
- `\b[0-9]+-fold\b`
- `\b[0-9]{2}/[0-9]{2}\s*(?:train|test|validation|split)\b`
- `\b(?:max|min)[-_ ]?(?:len|length|tokens|new[-_ ]?tokens)\s*(?:=\s*|:\s*|of\s+)[0-9,]+`
- `\bwarm[-_ ]?up\s*(?:=\s*|:\s*|of\s+)[0-9,]+`
- `\b[0-9]+\s*(?:hidden\s+)?(?:units|layers|heads)\b`
- `\b[0-9]+\s*-\s*(?:layer|unit|head)\b`
- `\b[0-9]+\s+(?:[a-z]+\s+)?(?:attention\s+heads|units|layers|heads|dimensions)\b`
- `\b95\s*%\s*(?:CI\b|confidence)`

A number passes only if it is inside a `num:` marker whose id is in the results index and whose stored value matches (percentages allowed, rounding allowed up to half of the last printed decimal place), or if one of the rules above applies. Everything else must be fixed before the draft is called done (RULES.md #2).
