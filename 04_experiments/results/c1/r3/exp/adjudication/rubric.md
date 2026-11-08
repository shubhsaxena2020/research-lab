# Adjudication rubric — does the passage answer the question?

## Task

For each item in `sample.csv` you are shown a `question` and a `context`
(passage). Decide whether the passage, **on its own**, contains an answer
to the question.

## Labels

| label       | meaning                                                                 |
|-------------|-------------------------------------------------------------------------|
| `1`         | **answerable** — the passage states (or unambiguously entails) an answer to the question |
| `0`         | **not answerable** — the passage does not contain an answer to the question |
| `ambiguous` | the passage arguably contains a partial, indirect, or contradictory answer; you cannot decide confidently |

Record your decision in `label_A.csv` / `label_B.csv` as `label` and add a
short `notes` entry for every `ambiguous` item (cite the relevant span or
explain why it is partial / indirect / contradictory).

## Rules

1. Judge **only** from the passage. External knowledge does not count:
   if the correct answer is *true* but *not stated* in the passage, the
   label is `0`.
2. Paraphrase counts. The passage need not use the exact words of the
   answer — if a reader can extract the answer from the passage alone,
   the label is `1`. (For reference, `sample.csv` also carries the
   `gold_answer` from the source dataset; do not let it overrule the
   passage: a gold answer that is absent from the passage is `0`.)
3. A passage that answers a *different* question, or is on an unrelated
   topic, is `0`.
4. A passage that *mentions* the topic but omits the specific fact the
   question asks for is `0`.
5. Use `ambiguous` sparingly: only when the passage is partially,
   indirectly, or contradictorily responsive — not for items you merely
   find difficult. If you can point to a sentence that gives the answer,
   it is `1`.
6. Rung numbers in `sample.csv` are metadata about how the negative was
   constructed; they are not evidence for or against answerability.

## Quality checks

- Annotators label independently; do not discuss items before labelling.
- `resolve.csv` is completed afterwards: for every disagreement between
  the two annotators, record the final label and a one-line rationale in
  `notes`.
- Agreement is reported as Cohen's kappa (`--kappa` in
  `04_experiments/src/r3_exp_adjudicate.py`) and is exploratory / post-hoc.

## Annotator disclosure

If LLM annotators are used, record the model name, version and prompt
alongside the labels. An LLM is not a human gold standard; any
contradiction between an LLM label and the source dataset is resolved by
human adjudication.
