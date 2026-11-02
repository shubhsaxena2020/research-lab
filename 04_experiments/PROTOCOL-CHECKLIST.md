# PRE-REGISTRATION CHECKLIST (topic-agnostic)

Phase 2 is LOCKED: this file is the *checklist*, not a protocol. It exists so that the moment
the head writes `TOPIC APPROVED` in `orchestration/HEAD-REVIEW.md`, S3-9 is a fill-in job of a
few hours rather than a design job. Nothing here is a hypothesis — every line is a question
that must be answered and then frozen.

`04_experiments/PROTOCOL.md` is the output: the answers, written down, hashed, and committed
**before** the first real run. If the protocol changes after seeing results, that is a
deviation, and deviations are logged in the protocol with the reason and the date.

---

## 0. Freeze mechanics

- [ ] `04_experiments/PROTOCOL.md` written and reviewed before any run on the real data.
- [ ] Hash recorded: `python -c "import hashlib;print(hashlib.sha256(open('04_experiments/PROTOCOL.md','rb').read()).hexdigest())"`
      and the hash written into `PROTOCOL.md` itself and into `sessions/S3-experiments/STATUS.md`.
- [ ] The first run's `meta.json` records the protocol hash (a run whose protocol hash is not
      the frozen one is not a protocol run).
- [ ] A "deviations" table exists and is empty at freeze time.

## 1. Hypotheses

- [ ] One primary hypothesis, stated as a directional prediction with a metric and a
      population, and a falsification condition ("we would abandon this if ...").
- [ ] Secondary hypotheses listed separately and marked exploratory — they get no
      confirmatory p-values, only effect sizes and intervals.
- [ ] The null result is stated as an acceptable outcome and what would be reported if it
      happens. (RULES #2: negative results are reported as negative.)

## 2. Data

- [ ] Exact dataset, version or commit, licence, and the URL used to obtain it.
- [ ] Public only (RULES #6). No private chats, no personal files, no login-walled scraping.
- [ ] Inclusion/exclusion rules, deduplication rules, and the final N after filtering.
- [ ] Splits defined by a rule, not by hand: the split file or the seeding rule is committed.
- [ ] Preprocessing frozen: tokenisation, normalisation, missing-value handling.
- [ ] What data would make the study impossible (leakage, insufficient N) and the check for it.

## 3. Baselines

- [ ] At least one trivial baseline (majority class / random / last value) — it calibrates
      whether the task is even non-trivial.
- [ ] At least one strong published baseline for the chosen task, with its citation VERIFIED
      in `02_literature/verified_citations.csv` and its reported number recorded, including
      the caveat that our re-implementation may differ from the paper's number.
- [ ] Baseline hyperparameters come from the source paper or a documented default, never tuned
      on the test set.

## 4. Metrics

- [ ] Primary metric named, with its direction and its chance level.
- [ ] Secondary metrics named. Anything reported later that is not on this list is exploratory.
- [ ] The exact computation is a function in `04_experiments/` with a unit test on a
      hand-computed example (a metric that is computed differently from the citation is a
      silent lie).
- [ ] Whether the metric is computed per example or per seed, stated — p-values over examples
      are not p-values over runs.

## 5. Sample size, seeds, and the analysis plan

- [ ] Number of seeds, fixed in advance, and why that number (not "as many as time allowed").
- [ ] Every configuration runs the same seed set; the seed list is written down.
- [ ] Primary analysis: paired test across seeds (Wilcoxon if n >= 6, sign test below), effect
      size named, bootstrap CI with `n_boot` and `ci_seed` recorded.
- [ ] Multiplicity: the family of comparisons is declared, and Holm or BH is applied and
      reported with the family size (CONTRACTS §4).
- [ ] Stopping rule: what ends the experiment (run count, wall-clock cap, or a checkpoint), and
      what is done if it ends early. No peeking at results and then extending.
- [ ] Compute plan: expected wall-clock and RAM, and whether it needs `ops/HEAVY.lock`.

## 6. What counts as failure

- [ ] The pre-registered failure conditions, in numbers: "if the treatment does not beat the
      trivial baseline on the primary metric, the claim is dropped".
- [ ] What is reported if the effect is in the wrong direction.
- [ ] What is reported if the effect is too small to matter (a significance test with a
      trivial effect size is a failure of the claim, not a success of the test).

## 7. After the freeze

- [ ] `python 04_experiments/harness/runner.py ... --check-repro 2` passes on the first config.
- [ ] `python tools/check_numbers.py --draft 05_paper/draft/` passes before any draft is called
      done.
- [ ] `02_literature/NOVELTY-CHECK.md` exists with the search queries and their results before
      the word "novel" appears anywhere (RULES #5).

---

## Why this checklist exists

A pre-registration is not bureaucracy for a student paper. It is the only defence against the
most common way a small study becomes dishonest: running several configurations, seeing which
one wins, and then writing the method section as if that one had been planned. The frozen hash
makes that visible, and the deviations table makes it honest when it happens.
