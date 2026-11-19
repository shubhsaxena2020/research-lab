# Writer report — SOURCE-MAP.md (R3-6b student pack)

Task: map every numeric claim in the student pack to its exact source file and JSON result key, using the
canonical IDs in `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md`.

Wrote: `07_student/SOURCE-MAP.md` (completely overwritten — the previous `MAP-1..MAP-32` draft is gone) and
this report. No other path was created or modified. No git commands, no writes under `05_paper/**`,
`06_review/**`, `04_experiments/**`, or any other lane folder.

## 1. What the file is

A 32-row mapping card, one row per canonical claim ID, with the seven columns in the required order:

`| ID | value as printed | rounding | source path (relative to repo root) | exact JSON key or file section+lines | stored value (exact, unrounded) | label/limit note |`

followed by the four required sections: **How to read a JSON key**, **Paths and hashes** (the three R3-3b files
with sha256), **Known exclusions** (90.73% and the no-re-derivation rule).

Every value in the `stored value` column was produced by `json.load` in this task — not copied from the
inventory, `ANSWERS.md`, or the previous draft. Line numbers in the key column are 1-based and were computed
against the exact bytes whose sha256 is printed in the map.

## 2. Proof check (a) — row count = 32

```
$ grep -o '^| [CN][0-9]*[a-z]* |' 07_student/SOURCE-MAP.md | tr -d '| ' | sort -u | tr '\n' ' '
C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C13b C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 N1 N2 N3 N4 N5 N6 N7 N8

$ grep -c '^| C\|^| N' 07_student/SOURCE-MAP.md
32
```

**Composition, stated plainly because the brief's arithmetic does not close.** The inventory defines
**C01–C23 = 23 numeric IDs**, not 24 (A: C01–C09 = 9, B: C10–C13 = 4, C: C14–C19 = 6, D: C20–C23 = 4). So
23 numeric + 8 fact = 31 IDs. To reach the required 32 rows **without inventing, renumbering, or merging an
ID**, C13 is written as two rows:

- `C13` — the item denominators, `denominators.held_out_common` (block opens line 980);
- `C13b` — the resampling config, top-level `n_boot` (line 1053) and `seed` (line 1660).

That split is not cosmetic: the "exact JSON key" column can name only one path per row, and these two groups
of numbers live in different parts of the file. Both rows say what they are, and the map header states
"C13b is a split of C13, not a new claim ID". **23 + 8 + 1 split = 32.** If the lead prefers strictly one row
per ID, deleting the `C13b` row and appending its two values to C13 is the only edit needed; coverage of the
inventory is unchanged either way.

## 3. Proof check (b) — the script that loaded every cited key, and its output

Exactly what I ran, from the repo root, with the system `python` (3.11.15). For every ID it resolves the keys
named in the table, prints the JSON value, and then checks that value against the text of that row's
`stored value` cell. Final line = mismatch count.

```python
import json, re, os
base = r"C:\Users\shubh\research-lab"
P = {
 "f10": "04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json",
 "f17": "04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json",
 "f7":  "04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json",
 "fr":  "04_experiments/results/c1/results_full.json",
 "fc":  "04_experiments/results/c1_corrected/results_full.json",
}
J = {k: json.load(open(os.path.join(base, v), encoding="utf-8")) for k, v in P.items()}

def flat(f, k):            # literal dotted key inside the file's "results" object
    return J[f]["results"][k]

def path(f, *p):           # genuine nested path
    x = J[f]
    for q in p:
        x = x[q]
    return x

CHECKS = {
 "C01": [("flat", "f10", "c1.r3_3b.mf10.cohen_kappa_overall"), ("path", "f10", "mf10", "agreement", "kappa")],
 "C02": [("flat", "f10", "c1.r3_3b.mf10.raw_agreement_po"), ("flat", "f10", "c1.r3_3b.mf10.n_agreed"),
         ("flat", "f10", "c1.r3_3b.mf10.n_items")],
 "C04": [("flat", "f10", "c1.r3_3b.mf10.n_disagreed")],
 "C05": [("flat", "f10", "c1.r3_3b.mf10.labeller_A_answerable_n"), ("flat", "f10", "c1.r3_3b.mf10.labeller_B_answerable_n")],
 "C06": [("flat", "f10", "c1.r3_3b.mf10.resolver_resolved_1_n"), ("flat", "f10", "c1.r3_3b.mf10.resolver_resolved_0_n"),
         ("flat", "f10", "c1.r3_3b.mf10.resolver_resolved_ambiguous_n"), ("flat", "f10", "c1.r3_3b.mf10.resolver_on_disagreements_n")],
 "C07": [("flat", "f10", "c1.r3_3b.mf10.resolved_answerable_n"), ("flat", "f10", "c1.r3_3b.mf10.resolved_answerable_share")],
 "C08": [("flat", "f10", "c1.r3_3b.mf10.rung1.kappa"), ("flat", "f10", "c1.r3_3b.mf10.rung2.kappa"),
         ("flat", "f10", "c1.r3_3b.mf10.rung3.kappa"), ("flat", "f10", "c1.r3_3b.mf10.rung4.kappa"),
         ("flat", "f10", "c1.r3_3b.mf10.n_items_by_rung"),
         ("path", "f10", "mf10", "per_rung", "1", "kappa"), ("path", "f10", "mf10", "per_rung", "2", "kappa"),
         ("path", "f10", "mf10", "per_rung", "3", "kappa"), ("path", "f10", "mf10", "per_rung", "4", "kappa")],
 "C09": [("path", "f10", "mf10", "comparison_with_prior_llm_adjudication", "prior_kappa"),
         ("path", "f10", "mf10", "comparison_with_prior_llm_adjudication", "prior_resolved_answerable_n"),
         ("path", "f10", "mf10", "comparison_with_prior_llm_adjudication", "prior_resolved_answerable_share")],
 "C10": [("flat", "f17", "c1.r3_3b.mf17.frozen_heldout_auroc.point"), ("flat", "f17", "c1.r3_3b.mf17.frozen_heldout_auroc.ci95_lo"),
         ("flat", "f17", "c1.r3_3b.mf17.frozen_heldout_auroc.ci95_hi")],
 "C11": [("flat", "f17", "c1.r3_3b.mf17.corrected_heldout_auroc.point"), ("flat", "f17", "c1.r3_3b.mf17.corrected_heldout_auroc.ci95_lo"),
         ("flat", "f17", "c1.r3_3b.mf17.corrected_heldout_auroc.ci95_hi")],
 "C12": [("flat", "f17", "c1.r3_3b.mf17.paired_auroc_diff.diff"), ("flat", "f17", "c1.r3_3b.mf17.paired_auroc_diff.ci95_lo"),
         ("flat", "f17", "c1.r3_3b.mf17.paired_auroc_diff.ci95_hi"),
         ("flatn", "f17", "c1.r3_3b.mf17.paired_auroc_diff", "contains_zero")],
 "C13": [("path", "f17", "denominators", "held_out_common", "n_items"), ("path", "f17", "denominators", "held_out_common", "n_positive_rung0"),
         ("path", "f17", "denominators", "held_out_common", "n_negative_rungs1to4"),
         ("path", "f17", "denominators", "held_out_common", "n_article_clusters")],
 "C13b": [("path", "f17", "n_boot"), ("path", "f17", "seed")],
 "C14": [("flat", "f7", "c1.r3_3b.mf7.gold_control.dev.r1.auroc_surface_lex")],
 "C15": [("flat", "f7", "c1.r3_3b.mf7.gold_control.dev.r1.auroc_plus_is_gold")],
 "C16": [("flat", "f7", "c1.r3_3b.mf7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented"),
         ("flat", "f7", "c1.r3_3b.mf7.gold_control.dev.r1.is_gold_deterministic_from_label")],
 "C17": [("flat", "f7", "c1.r3_3b.mf7.d3_pooled.all.n_hit"), ("flat", "f7", "c1.r3_3b.mf7.d3_pooled.all.n_miss"),
         ("flat", "f7", "c1.r3_3b.mf7.d3_pooled.all.auroc_surface_lex_hit_vs_miss")],
 "C18": [("flat", "f7", "c1.r3_3b.mf7.d3_pooled.dev.n_hit"), ("flat", "f7", "c1.r3_3b.mf7.d3_pooled.dev.n_miss"),
         ("flat", "f7", "c1.r3_3b.mf7.d3_pooled.test.n_hit"), ("flat", "f7", "c1.r3_3b.mf7.d3_pooled.test.n_miss")],
 "C19": [("flat", "f7", "c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available"),
         ("flat", "f7", "c1.r3_3b.mf7.d3_pooled.rungs_present_value")],
 "C20": [("path", "fr", "test", "band_primary", "per_rung", "4", "abstain_precision")],
 "C21": [("path", "fr", "test", "exploratory_band", "per_rung", "4", "abstain_precision")],
 "C22": [("path", "fc", "test", "exploratory_band", "per_rung", "4", "abstain_precision")],
 "N4":  [("path", "fr", "hypotheses", "H1", "sign_test", "p_note")],
 "N7":  [("path", "f17", "limitations", 0), ("path", "f17", "limitations", 4)],
}

def resolve(spec):
    kind = spec[0]
    if kind == "flat":
        return flat(spec[1], spec[2])
    if kind == "flatn":
        return J[spec[1]]["results"][spec[2]][spec[3]]
    return path(spec[1], *spec[2:])

md = open(os.path.join(base, "07_student", "SOURCE-MAP.md"), encoding="utf-8").read().splitlines()
rows = {}
for line in md:
    m = re.match(r"^\| ([CN]\d+[a-z]?) \|", line)
    if m:
        rows[m.group(1)] = line
print("rows parsed from table:", len(rows))

mismatch = []
for cid, specs in CHECKS.items():
    stored = [c.strip() for c in rows[cid].split("|")][6]
    out = []
    for spec in specs:
        v = resolve(spec)
        out.append(repr(v))
        token = repr(v).strip("'")
        if token not in stored and str(v) not in stored:
            mismatch.append((cid, repr(v), stored[:90]))
    print("%-5s %s" % (cid, "  ".join(out)))

print()
print("rows total:", len(rows))
print("rows with checks:", len(CHECKS))
print("mismatches (stored column vs JSON):", len(mismatch))
for m in mismatch:
    print("  MISMATCH", m)

# C03 derivation, printed for the record
po = flat("f10", "c1.r3_3b.mf10.raw_agreement_po")
k = path("f10", "mf10", "agreement", "kappa")
pe = (po - k) / (1 - k)
print()
print("C03 Pe from (Po,kappa) = %r  -> rounded %r" % (pe, round(pe, 4)))
print("C03 Pe from marginals    = %r" % ((62 * 21 + 38 * 79) / 10000))
print("C03 back-check kappa     = %r" % ((po - 0.4304) / (1 - 0.4304)))
```

Output, verbatim — this is the table's `stored value` column resolved from the JSON:

```
rows parsed from table: 32
C01   0.2802  0.2801966292134831
C02   0.59  59  100
C04   41
C05   62  21
C06   35  6  0  41
C07   56  0.56
C08   0.0  0.2991  0.026  0.1379  {'1': 25, '2': 25, '3': 25, '4': 25}  0.0  0.29906542056074775  0.025974025974026038  0.13793103448275895
C09   0.1975  5  0.05
C10   0.9823630831643002  0.9776211411662427  0.9866543835742593
C11   0.8738488843813388  0.8586833140203312  0.8893003500532195
C12   0.10851419878296142  0.09458017350090517  0.12252082237972457  False
C13   1879  400  1479  18
C13b  10000  20261118
C14   0.9762
C15   1.0
C16   1.0  True
C17   655  145  0.7327
C18   342  58  313  87
C19   False  -1
C20   1.0
C21   0.8471
C22   0.1253
N4    'no discordant pairs (all differences zero)'
N7    'All intervals are post-hoc/exploratory; no frozen verdict is revised.'  'The gold-indicator column is a label-construction artefact; its AUROC is not evidence about rung hardness.'

rows total: 32
rows with checks: 24
mismatches (stored column vs JSON): 0

C03 Pe from (Po,kappa) = 0.4304  -> rounded 0.4304
C03 Pe from marginals    = 0.4304
C03 back-check kappa     = 0.2801966292134831
```

`rows with checks: 24` = the 22 C-IDs that resolve to a stored key (C01–C23 minus C03) + `C13b` + the two
JSON-backed fact rows N4 and N7. The other rows (C03, N1, N2, N3, N5, N6, N8, and C23 whose numbers are
delegated to C10/C11) are prose or derived and carry that in their own cells.

C03 was checked two independent ways, both giving 0.4304: from (Po, κ) and from the stored contingency table
`(62×21 + 38×79)/10000`. Back-substituting 0.4304 with Po = 0.59 reproduces 0.2801966292134831 exactly, so
C01/C02/C03 are mutually consistent and C03 introduces no third independent measurement.

## 4. Proof check (c) — the C20 / C21 / C22 path

These three are genuine nested paths in `results_full.json`, not flat dotted keys, and the rung key is the
string `"4"`:

```python
json.load(open("04_experiments/results/c1/results_full.json"))['test']['band_primary']['per_rung']['4']['abstain_precision']
  -> 1.0        # C20  registered band (frozen, D1)              -> 100.00%

json.load(open("04_experiments/results/c1/results_full.json"))['test']['exploratory_band']['per_rung']['4']['abstain_precision']
  -> 0.8471     # C21  frozen exploratory (as-run, D1)            -> 84.71%

json.load(open("04_experiments/results/c1_corrected/results_full.json"))['test']['exploratory_band']['per_rung']['4']['abstain_precision']
  -> 0.1253     # C22  spec-corrected exploratory (post-hoc, D4)  -> 12.53%
```

Line locations, verified against the bytes: C1 → `"test"` 489, `band_primary` 490, `per_rung` 495, `"4"` 535,
`abstain_precision` 536; C1 → `exploratory_band` 551, `per_rung` 561, `"4"` 596, `abstain_precision` 597;
C1C → `"test"` 392, `exploratory_band` 454, `per_rung` 459, `"4"` 499, `abstain_precision` 500.

**Trap now documented in the map.** Both `results_full.json` files contain an earlier `"test"` block nested
inside `ablation_no_rank` (C1 line 19). A naive grep for `"test"` or `[0]`-indexing lands on the ablation block
and reads different gates. The map's section 2 warns about it and every line number points at the top-level
block.

**Excluded on purpose:** `results/c1_corrected/results_full.json` →
`test.band_primary.per_rung.4.abstain_precision` = **0.9073** at line 439. It appears in the map only inside
"Known exclusions", never as a claim row.

## 5. JSON vs inventory mismatches

**None.** Every value the inventory states was re-read from the JSON and agrees exactly, including the places
where the inventory quotes two precisions:

- **C01** — the flat key `cohen_kappa_overall` really does store the **rounded** `0.2802` (line 246), and
  `mf10.agreement.kappa` really does hold `0.2801966292134831` (line 86). The row records both and labels which
  is which, so a writer cannot claim 4-dp precision from the flat key.
- **C08** — the flat `rung{n}.kappa` keys store the rounded `0.0 / 0.2991 / 0.026 / 0.1379`; full precision
  exists only at `mf10.per_rung.{1..4}.kappa`. Both are recorded, with the n = 25 warning.
- **C12** — confirmed there is **no** flat key ending `.contains_zero`; it lives inside the nested dict stored
  at `results['c1.r3_3b.mf17.paired_auroc_diff']` (line 1380). The C12 cell and section 2 both say so.

## 6. Unresolvable keys

**None.** Every key path cited in the map resolved against the current bytes. One row is deliberately not a
key: **C03**, which is derived from C01 + C02 and is labelled as such in the row, in the rounding column, and
in "Known exclusions".

## 7. Coverage of the inventory

- **C01–C23:** all present, in order, none merged, none renumbered.
- **N1–N8:** all present with file + section heading + line numbers — `TRIAGE.md` line 1 and rows 8–51;
  `HEAD-REVIEW.md` Checkpoint 5 line 46, Checkpoint 10 line 84, Checkpoint 11 line 94; `COMMON.md` §"What the
  project is" lines 6–11; `PREREGISTRATION.md` §1 lines 22–25, §10 D1 lines 165–172 and 178–181, §10 D4 lines
  262–264; `ANSWERS.md` header 3–6 plus the Label line of each item; `c1/results_full.json`
  `hypotheses.H1.sign_test.p_note` line 364; `mf17` `limitations` items 1 and 5 (lines 1046, 1050).
- The seven required framing sentences in inventory §F carry no numbers, so they are not rows; the
  label/limit column enforces each one on the rows it governs (exploratory/not-in-draft for C01–C19 with N5/N6;
  κ is not accuracy at C01; tautological at C15/C16; pooled rung = −1 with no per-rung estimate at C17–C19;
  H1 not exercisable and neither confirmed nor refuted at C20 with N1–N4; MF-14 run labels on C20/C21/C22; no
  frozen verdict revised everywhere).

## 8. Residual risks for the reviewer

1. **The 32-row count depends on the C13 split** (§2). Coverage of the inventory is unaffected; only the count
   moves between 31 and 32.
2. **There is no `Document` column** — the seven-column contract is fixed, so the map does not say which
   student file uses which row. The digest and viva should therefore carry the `C..`/`N..` ID in parentheses
   next to each number (the join the previous `MAP-n` scheme used). I did not add an eighth column because the
   column order was specified.
3. **Line numbers are byte-exact for today's files.** The sha256 values are recorded in the map so the check is
   reproducible; if any of the five JSON files is regenerated, both the line numbers and this map must be
   re-run.
