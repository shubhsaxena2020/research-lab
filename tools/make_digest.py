#!/usr/bin/env python
"""make_digest.py - build an auditable one-page student digest for a paper section.

RULES.md #4 is the reason this tool exists: Shubh is the responsible author and must be
able to explain and defend every section. This tool turns a draft section into a study
aid whose honesty is structural, not a matter of trust:

  * "What this section says" bullets are EXTRACTED from each paragraph's topic sentence,
    stripped of citations/markup, put in first person, and cut to 25 words. No new
    content words are allowed in.
  * A number is quoted only if its `<!-- num:id -->` marker resolves through
    04_experiments/RESULTS-INDEX.json to a file and key whose stored value is read back.
  * A citation is quoted only if its key exists in 02_literature/verified_citations.csv,
    and then only its recorded title/venue/year.
  * Everything else becomes an explicit `[TO FILL: ...]` slot. The tool never guesses.

Usage:
    python tools/make_digest.py --section 05_paper/draft/method.md
    python tools/make_digest.py --section 05_paper/draft --all
    python tools/make_digest.py --check 06_review/STUDENT-DIGEST/METHOD.md
    python tools/make_digest.py --check 06_review/STUDENT-DIGEST/METHOD.md --strict

Outputs one `06_review/STUDENT-DIGEST/<SECTION>.md` per input section (see --out-dir).

Exit codes: 0 success / digest complete, 1 findings (check failed, or generated digest
failed its own structural audit), 2 usage error.  No network access, ever.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "06_review" / "STUDENT-DIGEST"
DEFAULT_INDEX = REPO_ROOT / "04_experiments" / "RESULTS-INDEX.json"
DEFAULT_CITATIONS = REPO_ROOT / "02_literature" / "verified_citations.csv"

MAX_BULLET_WORDS = 25
BLOCKS = (
    "What this section says",
    "Why it is there",
    "What could be asked at a talk",
    "Five likely questions with honest answers",
    "Glossary",
)

# --------------------------------------------------------------------------- roles

ROLE_ALIASES = {
    "intro": "intro",
    "introduction": "intro",
    "motivation": "intro",
    "method": "method",
    "methods": "method",
    "methodology": "method",
    "approach": "method",
    "implementation": "method",
    "setup": "method",
    "experiment": "results",
    "experiments": "results",
    "results": "results",
    "result": "results",
    "evaluation": "results",
    "findings": "results",
    "analysis": "results",
    "limitations": "limitations",
    "limitation": "limitations",
    "threats": "limitations",
    "threats_to_validity": "limitations",
    "validity": "limitations",
    "related": "related",
    "related_work": "related",
    "relatedwork": "related",
    "prior_work": "related",
    "background": "related",
    "discussion": "discussion",
    "conclusion": "conclusion",
    "conclusions": "conclusion",
    "summary": "conclusion",
    "abstract": "abstract",
}

ROLES: Dict[str, dict] = {
    "intro": {
        "purpose": (
            "It has to make a reader want the answer: name the problem, show the gap, "
            "and state the contribution so precisely that evidence could contradict it."
        ),
        "checklist": [
            "What problem is being solved, in one sentence?",
            "Whose problem is it, and why does it matter now?",
            "What exactly is missing from existing work, and which citation proves it?",
            "What is the contribution, stated so that evidence could contradict it?",
            "What is explicitly out of scope?",
        ],
        "talk": [
            "What is the problem in one sentence, and who actually has it?",
            "What is the gap in prior work, and which citation shows the gap is real?",
            "What is my contribution, stated so that a result could prove it wrong?",
            "Why is this problem hard, and why is it worth solving now?",
            "What am I explicitly not claiming?",
            "Which sentence here would a sceptical reviewer attack first?",
        ],
        "hard": [
            "Why does this problem matter outside my own dataset?",
            "What is the closest prior work, and why is it not enough?",
            "What is my contribution in one falsifiable sentence?",
            "What assumption about the data or the reader does this section rely on?",
            "What would make me abandon this line of work?",
            "If the contribution is small, why publish it at all?",
        ],
    },
    "method": {
        "purpose": (
            "It has to let a reader reproduce what was done without asking me anything: "
            "inputs, steps, fixed settings, and the choices that could have gone the other way."
        ),
        "checklist": [
            "What goes in and what comes out, in order?",
            "Which choices were forced by the data or task, and which were mine?",
            "What is fixed (seed, split, hyperparameters, code version) so the run repeats?",
            "What would a reader need to re-implement this tomorrow?",
            "Where does it fail, and how would I notice?",
        ],
        "talk": [
            "Walk me through paragraph {p} as if I had to re-implement it tomorrow: what goes in, what comes out?",
            "Why this design choice rather than the obvious alternative?",
            "What is fixed - seed, split, hyperparameters - so someone else gets the same result?",
            "Where does this method fail, and how would I notice before the final score?",
            "Which part of the pipeline is standard, and which part is the contribution?",
            "What would a reader need that this section does not give them?",
        ],
        "hard": [
            "Why this method and not the simplest baseline?",
            "What are the inputs, outputs, and fixed settings, in order?",
            "Which step is most likely to be wrong, and how would I detect that?",
            "How would someone reproduce this from the section alone?",
            "What did I try that did not work, and why is it not reported here?",
            "Which design choice would I change first if I started again?",
        ],
    },
    "results": {
        "purpose": (
            "It has to turn runs into evidence: define each metric, compare against a tuned "
            "baseline, show the spread across seeds, and report what did not work."
        ),
        "checklist": [
            "What does each metric measure, and why this metric for this claim?",
            "What is the baseline, and was it tuned as hard as the method?",
            "How many seeds and runs, and what is the spread?",
            "Which numbers trace to a file in the results index?",
            "What result is negative or missing, and is it reported?",
        ],
        "talk": [
            "Why is {num} the right metric for this claim, and what would a different metric hide?",
            "What result would falsify the claim that the method is better?",
            "How many seeds and runs stand behind {num}, and how wide is the spread?",
            "What is the baseline's strongest setting, and was it tuned as hard as my method?",
            "Which ablation isolates the part of the method that is supposed to cause the gain?",
            "Is the difference behind {num} large enough to matter outside this test set?",
        ],
        "hard": [
            "What exactly does the headline number measure, and on which split?",
            "How many seeds, and what is the variance across them?",
            "Is the baseline tuned as strongly as my method?",
            "What result would falsify the claimed gain?",
            "Which result is negative, and did I report it?",
            "Why should anyone trust these numbers rather than a lucky run?",
        ],
    },
    "limitations": {
        "purpose": (
            "It has to bound the claim: say where the result stops holding, what threatens "
            "it, and what was done about that."
        ),
        "checklist": [
            "Which claim does this limitation weaken, and by how much?",
            "What is the worst-case reading of the limitation?",
            "What was done to reduce it, and what evidence shows it worked?",
            "What would it take to remove the limitation?",
            "Which limitations are about scope, and which are threats to validity?",
        ],
        "talk": [
            "Which result in the paper does this limitation threaten most?",
            "What is the worst-case reading of this limitation?",
            "What did I do to reduce it, and how do I know it worked?",
            "What would it take to remove this limitation?",
            "Which of these is a scope limit, and which is a threat to validity?",
            "Why should a reader still trust the main claim after this admission?",
        ],
        "hard": [
            "Which claim is weakest because of this limitation?",
            "How much would the headline result move under the worst case?",
            "What mitigation did I test, and what did it change?",
            "What data or setting would remove this limitation?",
            "Is this limitation fatal for the intended use, or only for a broader one?",
            "What limitation did I fail to list?",
        ],
    },
    "related": {
        "purpose": (
            "It has to place the work: what exists, what it cannot do, and why this paper "
            "is still needed."
        ),
        "checklist": [
            "Which works are closest, and what can they not do?",
            "Is the comparison fair on data, compute, and tuning?",
            "What gap does this paper fill, stated without dismissing prior work?",
            "Which citation would a reviewer expect and is missing?",
        ],
        "talk": [
            "Which work is closest to mine, and what exactly can it not do?",
            "Is the comparison fair on data, compute, and tuning?",
            "What gap does this paper fill that prior work leaves open?",
            "Which cited work would a reviewer expect me to discuss and I have not?",
            "How has the field changed since the oldest work cited here?",
            "Why is the closest prior work not simply a baseline?",
        ],
        "hard": [
            "What is the strongest prior work, and why is it not sufficient?",
            "What did I borrow, and what is actually new here?",
            "Is the comparison to prior work fair?",
            "Which citation is load-bearing for my gap claim?",
            "What would an expert in this area say I ignored?",
            "Why is this paper needed if the closest work already exists?",
        ],
    },
    "discussion": {
        "purpose": (
            "It has to separate what was measured from what it might mean, and give the "
            "reader the alternative explanations."
        ),
        "checklist": [
            "Which sentence reports a measurement, and which interprets it?",
            "What alternative explanation fits the same numbers?",
            "What would change my mind?",
            "Who could use this, and under what conditions?",
        ],
        "talk": [
            "Which sentence here is a measurement, and which is an interpretation?",
            "What alternative explanation fits the same numbers?",
            "What result would change my mind?",
            "Who could use this, and under what conditions?",
            "What is the practical cost of being wrong here?",
            "Which claim goes beyond what the results section shows?",
        ],
        "hard": [
            "What does the result mean, beyond what was measured?",
            "What is the most plausible alternative explanation?",
            "What evidence would settle between the two explanations?",
            "What are the practical implications, and for whom?",
            "Where does this discussion overreach the results?",
            "What should the reader do differently because of this work?",
        ],
    },
    "conclusion": {
        "purpose": (
            "It has to restate the claim at the strength the evidence supports, point back "
            "to the evidence, and say what comes next."
        ),
        "checklist": [
            "What claim is restated, and is it exactly the claim the results support?",
            "Which number or table backs it?",
            "What is future work, and what is already done?",
            "What am I not claiming?",
        ],
        "talk": [
            "What is the claim in one sentence, and which number backs it?",
            "Does this conclusion claim more than the results show?",
            "What is future work, and what part is already done?",
            "What am I not claiming?",
            "If a reader remembers one sentence, which should it be?",
            "What would I do next with one more month?",
        ],
        "hard": [
            "What is the single claim this paper earns?",
            "Which evidence in the paper supports it?",
            "What does the paper not claim?",
            "What is the next experiment, and why that one?",
            "Would the conclusion survive a failed replication?",
            "What is the honest scope of the contribution?",
        ],
    },
    "abstract": {
        "purpose": (
            "It has to give the whole argument in miniature: problem, method, evidence, limit."
        ),
        "checklist": [
            "Problem, method, result, limit - are all four present?",
            "Is every number in the abstract also in the results?",
            "Does the last sentence promise more than the paper delivers?",
        ],
        "talk": [
            "Which sentence states the problem, and which states the result?",
            "Is every number here traceable to the results?",
            "What is the method in one clause?",
            "What limitation is admitted, and is it enough?",
            "Does the abstract promise more than the paper delivers?",
            "Why would a reader continue past this abstract?",
        ],
        "hard": [
            "What is the problem, method, result, and limit, each in one clause?",
            "Which number in the abstract is load-bearing?",
            "Where is that number in the results?",
            "What does the abstract leave out that changes the reading?",
            "Is the claim calibrated to the evidence?",
            "Would an expert be misled by any sentence here?",
        ],
    },
    "generic": {
        "purpose": (
            "It has to do one job in the argument; if a reader cannot say what that job is "
            "after one pass, the section is not doing it."
        ),
        "checklist": [
            "What job does this section do in the argument?",
            "Which claim depends on it?",
            "What would a reader expect here that is missing?",
            "Which sentence could be cut without loss?",
        ],
        "talk": [
            "What job does this section do in the argument?",
            "Which later claim depends on this section?",
            "What would a reader expect here that is missing?",
            "Which sentence could be cut without losing the argument?",
            "What is the one fact here I must not get wrong?",
            "How does this section connect to the previous one?",
        ],
        "hard": [
            "What is this section for?",
            "Which claim depends on it?",
            "What evidence here is load-bearing?",
            "What is missing that a reader would expect?",
            "What would I cut first, and why?",
            "How would I explain this section in thirty seconds?",
        ],
    },
}

# --------------------------------------------------------------- BCA-level vocabulary
# Deliberately small and boring: words a first-year BCA student already uses in class.
# Anything technical outside this list becomes a glossary entry with a [TO FILL] slot.
BCA_VOCAB = set(
    """
    a about above after again against all also an and any are as at be because been before
    being below between both but by can could did do does doing down during each few for
    from further had has have having he her here hers herself him himself his how i if in
    into is it its itself just me more most my myself no nor not now of off on once only or
    other our ours ourselves out over own same she should so some such than that the their
    theirs them themselves then there these they this those through to too under until up
    very was we were what when where which while who whom why will with would you your
    yours yourself yourselves
    able add added adds after age ago agree air all allow almost alone along already
    although always among amount another answer any anyone anything appear apply area
    around ask asked asks available away back bad base basic basis become becomes becoming
    begin beginning behind believe best better big body book both bring build building
    built business call called calls can cannot care case cases cause certain change
    changed changes check child choose city class classes clear clearly close code college
    come comes coming common company complete computer computers concept consider contain
    contains continue control correct cost course create created creates current data
    database day days decide decided decision describe described describes detail details
    develop developed different difficult direct directly discuss discussed does done
    during easy education effect either else end enough enter entire equal error even
    event ever every everyone everything example examples exist expect expected explain
    explained face fact factor fail failed fall family far fast feel few field figure file
    files find first five follow following follows form found four free friend full general
    get gets getting give given gives go goes going good got great group grow had hand
    happen hard have head hear help high higher him home hope hour how however idea ideas
    important include included includes increase information inside instead interest into
    issue item items job keep kind know known large last late later lead learn least leave
    left less let level life light like line lines list little live local long look looks
    lot low made main make makes making many may maybe mean means measure measured meeting
    member men might mind minute miss month more morning most move much must name named
    need needed needs never new next night number numbers object of often old once one
    ones open order other others page pages paper paragraph part parts past people per
    perhaps
    person place plan point points possible power problem problems process program programs
    provide provided provides public put question questions quick quickly quite rather
    read reading real reason receive record report reported reports require required
    result results return right room run running said same saw say saying says school
    science score second section see seem seen sense sentence set several short show
    showed shown shows side
    simple simply since single sit situation size small social software some someone
    something sometimes soon sort sound speak special stand start started state step steps
    still stop story strong student students study such sure system systems take taken
    takes talk task tasks teach teacher tell test tests than thank thing things think
    third though thought three time times today together told took top topic total toward
    true try trying turn two type types understand until use used useful uses using usual
    value values various view want wanted wants way ways week well went whole why wide will
    within without word words work worked working works world worry write writing written
    year years yes yet young
    """.split()
)

# Technical terms common in CS/ML papers. Phrases are matched case-insensitively.
TECH_TERMS = (
    "ablation study",
    "ablation",
    "accuracy",
    "annotation",
    "anova",
    "auc",
    "baseline",
    "batch size",
    "bayesian",
    "benchmark",
    "bleu",
    "bootstrap",
    "calibration",
    "chi-square",
    "classifier",
    "cohen's d",
    "confidence interval",
    "confusion matrix",
    "corpus",
    "cross-validation",
    "data leakage",
    "decoder",
    "dense retrieval",
    "deterministic",
    "dropout",
    "dual-encoder",
    "effect size",
    "embedding",
    "encoder",
    "epoch",
    "f1",
    "false negative",
    "false positive",
    "feature",
    "fine-tuning",
    "gradient",
    "ground truth",
    "held-out",
    "hyperparameter",
    "inference",
    "initialisation",
    "initialization",
    "inter-annotator agreement",
    "latency",
    "learning rate",
    "logit",
    "macro f1",
    "mean average precision",
    "metric",
    "micro f1",
    "overfitting",
    "p-value",
    "paired test",
    "perplexity",
    "pipeline",
    "precision",
    "pretrained",
    "quantile",
    "recall",
    "regularisation",
    "regularization",
    "retrieval",
    "roc",
    "rouge",
    "seed",
    "softmax",
    "standard deviation",
    "statistical significance",
    "stochastic",
    "supervised",
    "throughput",
    "token",
    "tokenisation",
    "tokenization",
    "transformer",
    "true negative",
    "true positive",
    "underfitting",
    "unsupervised",
    "validation",
    "variance",
    "wilcoxon",
)

# ------------------------------------------------------------------------ markup

NUM_HTML_RE = re.compile(
    r"<!--\s*num:([A-Za-z0-9_.\-/]+)\s*-->(.*?)<!--\s*/num\s*-->", re.S
)
NUM_LATEX_RE = re.compile(
    r"(?:^|\n)[ \t]*%[ \t]*num:([A-Za-z0-9_.\-/]+)[ \t]*\n[ \t]*([^\n]+)"
)
CITE_CMD_RE = re.compile(
    r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear|parencite|textcite)"
    r"\*?(?:\[[^\]]*\])*\{([^}]+)\}"
)
CITE_PANDOC_RE = re.compile(r"\[@([^\]]+)\]")
CITE_BRACE_RE = re.compile(r"\{\{cite:([^}]+)\}\}")
MARKER_LINE_RE = re.compile(r"^%[ \t]*num:[A-Za-z0-9_.\-/]+[ \t]*$")

HEADING_RE = re.compile(r"^#{1,6}\s")
LIST_RE = re.compile(r"^(?:[-*+]|\d+[.)])\s+")


def strip_inline(text: str) -> str:
    """Remove markup/citation noise but keep the number and the words around it."""
    s = text
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)          # images
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)      # links -> link text
    s = NUM_HTML_RE.sub(lambda m: m.group(2), s)        # keep printed number
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)        # other comments
    s = CITE_CMD_RE.sub("", s)
    s = CITE_PANDOC_RE.sub("", s)
    s = CITE_BRACE_RE.sub("", s)
    # A removed citation must not leave "design of , adapted" behind.
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"\b(of|in|on|by|from|with|see)\s*(?=[,.;:])", "", s, flags=re.I)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"%[ \t]*num:[A-Za-z0-9_.\-/]+", "", s)  # LaTeX marker, keep the number
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", s)
    s = s.replace("`", "")
    s = s.replace("$", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_paragraphs(markdown: str) -> List[dict]:
    """Return content paragraphs (1-based index, raw text, display text)."""
    text = markdown.replace("\r\n", "\n").replace("\r", "\n")
    # Drop YAML front matter.
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4:]

    blocks: List[str] = []
    buf: List[str] = []
    in_fence = False

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        # Keep newlines: the LaTeX num marker is only recognisable on its own line.
        joined = "\n".join(part.strip() for part in buf).strip()
        # A buffer that is only a LaTeX marker line is not a paragraph.
        if not joined or MARKER_LINE_RE.match(joined):
            buf = []
            return
        # A lone number under a marker is part of the paragraph above it, not a
        # paragraph of its own (the contract places the marker above the number).
        first_line = joined.split("\n", 1)[0].strip()
        if (
            blocks
            and MARKER_LINE_RE.match(first_line)
            and re.fullmatch(r"[-+]?\d[\d,]*(?:\.\d+)?%?", strip_inline(joined).strip())
        ):
            blocks[-1] = blocks[-1] + "\n" + joined
            buf = []
            return
        blocks.append(joined)
        buf = []

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            # Keep a lone marker line attached to the number that follows it.
            if buf and all(MARKER_LINE_RE.match(p.strip()) for p in buf):
                continue
            flush()
            continue
        if HEADING_RE.match(stripped):
            flush()
            continue
        if stripped.startswith("|") or stripped.startswith("!["):
            flush()
            continue
        if LIST_RE.match(stripped):
            flush()
            buf = [stripped]
            continue
        if MARKER_LINE_RE.match(stripped):
            buf.append(stripped)
            continue
        buf.append(stripped)
    flush()

    paragraphs = []
    for i, raw in enumerate(blocks, start=1):
        display = strip_inline(raw)
        display = LIST_RE.sub("", display).strip()
        if not display:
            continue
        paragraphs.append({"n": len(paragraphs) + 1, "raw": raw, "text": display})
    return paragraphs


def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    # Split only where the punctuation is followed by whitespace, so 0.812 survives.
    parts = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)
    return parts[0].strip()


STOP_TAIL = {
    "and", "or", "but", "which", "that", "with", "for", "to", "of", "in", "on", "by",
    "as", "while", "whereas", "although", "because", "so", "than", "then", "when",
}


def trim_to_words(text: str, limit: int = MAX_BULLET_WORDS) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    head = " ".join(words[:limit])
    # Prefer a clause boundary if one falls late enough to keep the point.
    cut = max(head.rfind(","), head.rfind(";"), head.rfind(":"))
    if cut > len(head) * 0.55:
        head = head[:cut]
    head = head.rstrip(" ,;:")
    words = head.split()
    while words and words[-1].lower().strip(",;:") in STOP_TAIL:
        words.pop()
        head = " ".join(words).rstrip(" ,;:")
    return head + "…"  # attached, so the ellipsis is not a 26th word


def bullet_for(paragraph: dict) -> str:
    """Extract the topic sentence and compress it, without adding content words."""
    s = strip_inline(paragraph["raw"])
    s = first_sentence(s)
    s = re.sub(r"\s*\([^()]*\)", "", s)  # parenthetical asides
    s = re.sub(
        r"^(?:However|Moreover|Furthermore|In addition|Therefore|Thus|Finally|"
        r"First|Second|Next|Also|In this section)[,:]\s*",
        "",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"^This section\s+(describes|presents|explains|reports|shows|introduces|"
        r"outlines|documents)\b",
        r"I \1",
        s,
        flags=re.I,
    )
    s = re.sub(r"\bWe\b", "I", s)
    s = re.sub(r"\bwe\b", "I", s)
    s = re.sub(r"\bOur\b", "My", s)
    s = re.sub(r"\bour\b", "my", s)
    s = re.sub(r"\bourselves\b", "myself", s, flags=re.I)
    s = re.sub(r"\bus\b", "me", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = trim_to_words(s)
    if not s:
        return f"[TO FILL: one-sentence summary of paragraph {paragraph['n']} in my own words]"
    for i, ch in enumerate(s):
        if ch.isalpha():
            if ch.islower():
                s = s[:i] + ch.upper() + s[i + 1:]
            break
    return s


# ------------------------------------------------------------------- evidence

def para_list(paragraphs: Sequence[int]) -> str:
    if len(paragraphs) == 1:
        return f"paragraph {paragraphs[0]}"
    return "paragraphs " + ", ".join(str(p) for p in paragraphs[:-1]) + f" and {paragraphs[-1]}"


def parse_printed_number(text: str) -> Optional[float]:
    cleaned = text.replace("\u2212", "-").replace(",", "")
    m = re.search(r"[-+]?\d+(?:\.\d+)?", cleaned)
    if not m:
        return None
    try:
        value = float(m.group(0))
    except ValueError:
        return None
    if "%" in text:
        value /= 100.0
    return value


def extract_numbers(paragraphs: Sequence[dict]) -> List[dict]:
    found: List[dict] = []
    seen: Dict[str, dict] = {}
    for p in paragraphs:
        for m in NUM_HTML_RE.finditer(p["raw"]):
            item = {
                "id": m.group(1),
                "printed": strip_inline(m.group(2)).strip(),
                "paragraphs": [p["n"]],
            }
            if item["id"] in seen:
                seen[item["id"]]["paragraphs"].append(p["n"])
                continue
            seen[item["id"]] = item
            found.append(item)
        for m in NUM_LATEX_RE.finditer(p["raw"]):
            printed = strip_inline(m.group(2)).strip()
            num = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?%?", printed)
            item = {
                "id": m.group(1),
                "printed": num.group(0) if num else printed,
                "paragraphs": [p["n"]],
            }
            if item["id"] in seen:
                seen[item["id"]]["paragraphs"].append(p["n"])
                continue
            seen[item["id"]] = item
            found.append(item)
    return found


def citation_keys(raw: str) -> List[str]:
    keys: List[str] = []
    for m in CITE_CMD_RE.finditer(raw):
        keys.extend(k.strip() for k in m.group(1).split(",") if k.strip())
    for m in CITE_PANDOC_RE.finditer(raw):
        for item in re.split(r"\s*;\s*", m.group(1)):
            item = re.sub(r"^[-+]?@", "", item.strip())
            key = item.split(",")[0].strip()
            if key:
                keys.append(key)
    for m in CITE_BRACE_RE.finditer(raw):
        keys.extend(k.strip() for k in m.group(1).split(",") if k.strip())
    return keys


def extract_citations(paragraphs: Sequence[dict]) -> List[dict]:
    found: List[dict] = []
    seen: Dict[str, dict] = {}
    for p in paragraphs:
        for key in citation_keys(p["raw"]):
            if key in seen:
                if p["n"] not in seen[key]["paragraphs"]:
                    seen[key]["paragraphs"].append(p["n"])
                continue
            item = {"key": key, "paragraphs": [p["n"]]}
            seen[key] = item
            found.append(item)
    return found


class EvidenceContext:
    """Read-only view of the two evidence files. Never invents a missing record."""

    def __init__(self, index_path: Path, citations_path: Path, root: Path):
        self.root = root
        self.index_path = index_path
        self.citations_path = citations_path
        self.index: Dict[str, dict] = {}
        self.index_error: Optional[str] = None
        self.citations: Dict[str, dict] = {}
        self.citations_error: Optional[str] = None
        self._json_cache: Dict[str, object] = {}
        self._load_index()
        self._load_citations()

    def display(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.root.resolve())).replace("\\", "/")
        except (ValueError, OSError):
            return str(path).replace("\\", "/")

    def _load_index(self) -> None:
        if not self.index_path.is_file():
            self.index_error = f"results index not found at `{self.display(self.index_path)}`"
            return
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            for entry in data.get("entries", []):
                if isinstance(entry, dict) and entry.get("id"):
                    self.index.setdefault(str(entry["id"]), entry)
        except (OSError, ValueError) as exc:
            self.index_error = f"results index could not be read ({exc})"

    def _load_citations(self) -> None:
        if not self.citations_path.is_file():
            self.citations_error = (
                f"verified citations file not found at `{self.display(self.citations_path)}`"
            )
            return
        try:
            with self.citations_path.open("r", encoding="utf-8", newline="") as fh:
                for row in csv.DictReader(fh):
                    key = (row.get("key") or "").strip()
                    if key:
                        self.citations.setdefault(key, row)
        except (OSError, csv.Error) as exc:
            self.citations_error = f"verified citations file could not be read ({exc})"

    def stored_value(self, entry: dict) -> Tuple[Optional[object], Optional[str], Optional[str]]:
        """Return (value, file_as_recorded, reason_if_unresolved)."""
        file_rel = str(entry.get("file") or "").strip()
        key_path = str(entry.get("key") or "").strip()
        if entry.get("toy") is True:
            return None, file_rel, "the index entry is marked `toy` (TOY - NOT A RESULT)"
        if not file_rel:
            return None, None, "the index entry has no `file`"
        if not key_path:
            return None, file_rel, "the index entry has no `key`"
        if file_rel.startswith("04_experiments/toy/"):
            return None, file_rel, "the file is under `04_experiments/toy/` (TOY - NOT A RESULT)"
        path = self.root / file_rel
        if not path.is_file():
            return None, file_rel, f"`{file_rel}` is not on disk"
        if file_rel not in self._json_cache:
            try:
                self._json_cache[file_rel] = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                self._json_cache[file_rel] = exc
        data = self._json_cache[file_rel]
        if isinstance(data, Exception):
            return None, file_rel, f"`{file_rel}` could not be parsed"
        if isinstance(data, dict) and data.get("toy") is True:
            return None, file_rel, f"`{file_rel}` is marked `toy` (TOY - NOT A RESULT)"
        node: object = data
        for part in key_path.split("."):
            if not isinstance(node, dict) or part not in node:
                return None, file_rel, f"`{key_path}` is not in `{file_rel}`"
            node = node[part]
        if isinstance(node, (dict, list)) or node is None:
            return None, file_rel, f"`{key_path}` in `{file_rel}` is not a scalar"
        return node, file_rel, None


def fmt_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return repr(value)
    return str(value)


def values_agree(printed: str, stored: object, tolerance: float) -> bool:
    pv = parse_printed_number(printed)
    if pv is None or isinstance(stored, bool):
        return False
    if isinstance(stored, str):
        sv = parse_printed_number(stored)
    elif isinstance(stored, (int, float)):
        sv = float(stored)
    else:
        return False
    if sv is None:
        return False
    diff = abs(sv - pv)
    if tolerance:
        return diff <= abs(sv) * tolerance + 1e-12
    return diff <= 1e-12


# --------------------------------------------------------------------- glossary

def _term_pattern(term: str) -> re.Pattern:
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", re.I)


TECH_PATTERNS = [(t, _term_pattern(t)) for t in sorted(TECH_TERMS, key=len, reverse=True)]
ACRONYM_RE = re.compile(r"(?<![A-Za-z0-9])[A-Z][A-Z0-9]{1,7}s?(?![A-Za-z0-9])")
# Unseen nominalisations still get a placeholder: -isation / -ization is a reliable
# signal of a technical process noun (tokenisation, initialisation, ...).
MORPH_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]{6,}(?:isation|ization)(?![A-Za-z0-9])", re.I
)
BACKTICK_RE = re.compile(r"`([^`]+)`")


def glossary_terms(paragraphs: Sequence[dict]) -> List[dict]:
    """Find technical terms; definitions are never produced, only slots."""
    entries: Dict[str, dict] = {}
    order = 0

    for p in paragraphs:
        text = p["text"]
        spans: List[Tuple[int, int, str, str]] = []  # start, end, key, surface

        for term, pat in TECH_PATTERNS:
            for m in pat.finditer(text):
                if term.lower() in BCA_VOCAB:
                    continue
                spans.append((m.start(), m.end(), term.lower(), m.group(0)))
        for m in ACRONYM_RE.finditer(text):
            surface = m.group(0)
            base = surface[:-1] if surface.endswith("s") and surface[:-1].isupper() else surface
            if base.lower() in BCA_VOCAB:
                continue
            spans.append((m.start(), m.end(), base.lower(), base))
        for m in MORPH_RE.finditer(text):
            surface = m.group(0)
            if surface.lower() in BCA_VOCAB:
                continue
            spans.append((m.start(), m.end(), surface.lower(), surface))
        for m in BACKTICK_RE.finditer(p["raw"]):
            token = m.group(1).strip()
            if not token or "/" in token or "\\" in token or token.startswith("num:"):
                continue
            if re.search(r"\.(json|csv|py|md|txt|log)$", token, re.I):
                continue
            if not re.match(r"^[A-Za-z][A-Za-z0-9_\-]*$", token):
                continue
            if token.lower() in BCA_VOCAB or len(token) < 3:
                continue
            start = text.lower().find(token.lower())
            if start != -1:
                spans.append((start, start + len(token), token.lower(), token))

        # Keep the longest term at each position; drop spans inside a longer one.
        spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
        kept: List[Tuple[int, int, str, str]] = []
        for span in spans:
            if any(span[0] == k[0] and span[1] == k[1] and span[2] == k[2] for k in kept):
                continue  # same term found by two detectors (acronym + word list)
            if any(span[0] >= k[0] and span[1] <= k[1] and span[2] != k[2] for k in kept):
                continue
            kept.append(span)

        for start, _end, key, surface in kept:
            if key in entries:
                entries[key]["count"] += 1
                continue
            order += 1
            entries[key] = {
                "term": surface,
                "first_p": p["n"],
                "count": 1,
                "order": order,
            }

    return sorted(entries.values(), key=lambda e: (e["first_p"], e["order"]))


def glossary_block(paragraphs: Sequence[dict]) -> str:
    terms = glossary_terms(paragraphs)
    if not terms:
        return "No terms outside the built-in BCA vocabulary were found in this section."
    lines = []
    for t in terms:
        mention = "mention" if t["count"] == 1 else "mentions"
        lines.append(
            f"- **{t['term']}** — [TO FILL: define it in my own words, then say why "
            f"this section needs it] (first appears: paragraph {t['first_p']}; "
            f"{t['count']} {mention})"
        )
    return "\n".join(lines)


# ------------------------------------------------------------------- digest build

def infer_role(stem: str) -> Tuple[str, bool]:
    key = re.sub(r"^\d+[_-]?", "", stem.lower())
    key = re.sub(r"[\s\-]+", "_", key)
    role = ROLE_ALIASES.get(key)
    if role:
        return role, True
    return "generic", False


def visible_numbers(numbers: Sequence[dict], paragraphs: Sequence[dict]) -> List[dict]:
    out = [{"display": n["printed"], "paragraphs": n["paragraphs"]} for n in numbers if n["printed"]]
    if out:
        return out
    # Fall back to decimal numbers the draft actually prints (still not invented).
    for p in paragraphs:
        for m in re.finditer(r"(?<![\w.])[-+]?\d+\.\d+%?(?![\w.])", p["text"]):
            out.append({"display": m.group(0), "paragraphs": [p["n"]]})
    return out


def ref_paragraphs(paragraphs: Sequence[int]) -> str:
    return para_list(paragraphs)


def num_answer(item: dict, ctx: EvidenceContext) -> str:
    ref = ref_paragraphs(item["paragraphs"])
    ident = item["id"]
    printed = item["printed"]
    entry = ctx.index.get(ident)

    if entry is None:
        reason = ctx.index_error or f"that id is not in `{ctx.display(ctx.index_path)}`"
        return (
            f"I point to {ref}, where the draft carries the marker `{ident}`. "
            f"I cannot quote a stored value: {reason}. "
            f"[TO FILL: add the run and file that produced this number to the index, "
            f"or remove the number from the draft.]"
        )

    stored, file_rel, reason = ctx.stored_value(entry)
    key_path = str(entry.get("key") or "")
    if reason is not None:
        return (
            f"I point to {ref}, where the draft carries the marker `{ident}`. "
            f"The index maps that id to `{key_path}` in `{file_rel}`, but {reason}. "
            f"[TO FILL: fix the index or the result file, then regenerate this digest.]"
        )

    value_text = fmt_value(stored)
    tolerance = entry.get("tolerance", 0.0) or 0.0
    try:
        tolerance = float(tolerance)
    except (TypeError, ValueError):
        tolerance = 0.0
    text = (
        f"I point to {ref}, where the draft prints {printed} for `{ident}`. "
        f"The results index maps that id to `{key_path}` in `{file_rel}`, and the stored "
        f"value there is {value_text}."
    )
    if not values_agree(printed, stored, tolerance):
        text += (
            f" [TO FILL: the draft prints {printed} but `{file_rel}` stores {value_text} - "
            f"I must fix one of them before the talk.]"
        )
    text += (
        " [TO FILL: say what this number measures and why this run is the right evidence "
        "for the sentence it sits in.]"
    )
    return text


def cite_answer(item: dict, ctx: EvidenceContext) -> str:
    ref = ref_paragraphs(item["paragraphs"])
    key = item["key"]
    row = ctx.citations.get(key)
    if row is None:
        if ctx.citations_error:
            reason = ctx.citations_error
        else:
            reason = f"`{key}` is not in `{ctx.display(ctx.citations_path)}`"
        return (
            f"I cite `{key}` in {ref}, but I cannot quote the record: {reason}. "
            f"[TO FILL: verify this citation and record it, or remove the sentence that "
            f"depends on it.]"
        )

    status = (row.get("status") or "").strip().upper()
    title = (row.get("title") or "").strip()
    venue = (row.get("venue") or "").strip()
    year = (row.get("year") or "").strip()
    if status and status != "VERIFIED":
        return (
            f"I cite `{key}` in {ref}, but the record has status {status}, not VERIFIED. "
            f"[TO FILL: resolve this citation before the talk, or drop the claim it supports.]"
        )
    if not title:
        return (
            f"I cite `{key}` in {ref}, but the verified record has no title stored. "
            f"[TO FILL: repair the citation record before the talk.]"
        )

    bits = [b for b in (venue, year) if b]
    tail = f" ({', '.join(bits)})" if bits else ""
    return (
        f"I cite `{key}` in {ref}. The verified record is \u201c{title}\u201d{tail} "
        f"[key `{key}`]. [TO FILL: say in one sentence what this source establishes and "
        f"how it supports that paragraph.]"
    )


def build_talk_questions(role: str, paragraphs: Sequence[dict], numbers: Sequence[dict]) -> List[str]:
    bank = ROLES[role]["talk"]
    count = min(6, max(3, len(bank)))
    if role == "results":
        count = 6
    count = min(count, len(bank))
    nums = list(numbers)
    out: List[str] = []
    num_i = 0
    for i in range(count):
        q = bank[i]
        p_used = False
        if "{num}" in q and nums:
            item = nums[num_i % len(nums)]
            num_i += 1
            q = q.replace("{num}", item["display"])
            p = item["paragraphs"][0]
        else:
            q = q.replace("{num}", "this number")
            p = paragraphs[i % len(paragraphs)]["n"] if paragraphs else None
        if "{p}" in q:
            if p is None:
                q = q.replace("paragraph {p}", "this paragraph")
            else:
                q = q.replace("{p}", str(p))
                p_used = True
        if p is not None and not p_used:
            q = f"{q} (paragraph {p})"
        elif p is None:
            q = f"{q} [TO FILL: paragraph reference]"
        out.append(q)
    return out


def build_five(
    role: str,
    paragraphs: Sequence[dict],
    numbers: Sequence[dict],
    citations: Sequence[dict],
    ctx: EvidenceContext,
) -> List[Tuple[str, str]]:
    qa: List[Tuple[str, str]] = []

    def add(question: str, answer: str) -> None:
        if any(question == existing[0] for existing in qa):
            return
        qa.append((question, answer))

    # Interleave numbers and citations so one kind cannot crowd out the other.
    evidence: List[Tuple[str, dict]] = []
    for i in range(max(len(numbers), len(citations))):
        if i < len(numbers):
            evidence.append(("num", numbers[i]))
        if i < len(citations):
            evidence.append(("cite", citations[i]))

    for kind, item in evidence:
        if len(qa) >= 5:
            break
        if kind == "num":
            if item["printed"]:
                q = f"Where does {item['printed']} in {ref_paragraphs(item['paragraphs'])} come from?"
            else:
                q = f"Where does the value marked `{item['id']}` come from?"
            add(q, num_answer(item, ctx))
        else:
            q = (
                f"What does `{item['key']}` actually establish, and why is it cited in "
                f"{ref_paragraphs(item['paragraphs'])}?"
            )
            add(q, cite_answer(item, ctx))

    fallback = list(ROLES[role]["hard"]) + list(ROLES["generic"]["hard"])
    for q in fallback:
        if len(qa) >= 5:
            break
        if any(q == existing[0] for existing in qa):
            continue
        if paragraphs:
            p = paragraphs[len(qa) % len(paragraphs)]["n"]
            answer = (
                f"I would answer from paragraph {p}: [TO FILL: my one-sentence answer, "
                f"naming the evidence (result file, table, or paragraph) that backs it.]"
            )
        else:
            answer = (
                "[TO FILL: my one-sentence answer, naming the evidence (result file, "
                "table, or paragraph) that backs it.]"
            )
        add(q, answer)

    n = 1
    while len(qa) < 5:
        add(
            f"What else could a reader ask about this section ({n})?",
            "[TO FILL: write the question I am afraid of, then answer it with evidence.]",
        )
        n += 1
    return qa[:5]


def build_digest(section_path: Path, role_override: Optional[str], ctx: EvidenceContext) -> dict:
    raw = section_path.read_text(encoding="utf-8")
    paragraphs = parse_paragraphs(raw)
    role, known = infer_role(section_path.stem)
    if role_override:
        role, known = role_override, True

    numbers = extract_numbers(paragraphs)
    citations = extract_citations(paragraphs)
    display_numbers = visible_numbers(numbers, paragraphs)

    bullets = [
        bullet_for(p)
        for p in paragraphs
        if not re.fullmatch(r"[-+]?\d[\d,]*(?:\.\d+)?%?", p["text"].strip())
    ]
    if not bullets:
        bullets = ["[TO FILL: this section has no prose paragraphs to summarize]"]

    role_data = ROLES[role]

    def count_phrase(n: int, word: str) -> str:
        return f"no {word}s" if n == 0 else f"{n} {word}{'' if n == 1 else 's'}"

    stats = (
        f"In this draft it runs to {count_phrase(len(paragraphs), 'paragraph')}, "
        f"{count_phrase(len(numbers), 'numeric marker')} and "
        f"{count_phrase(len(citations), 'cited work')}."
    )
    why = [role_data["purpose"], "", stats, "", "Reader checklist:", ""]
    why += [f"- [ ] {item}" for item in role_data["checklist"]]
    if not known:
        why.insert(
            1,
            "[TO FILL: name this section's role (intro/method/results/limitations) - "
            "the generic checklist below is a placeholder, not an analysis.]",
        )
        why.insert(2, "")

    talk = build_talk_questions(role, paragraphs, display_numbers)
    five = build_five(role, paragraphs, numbers, citations, ctx)

    src_display = ctx.display(section_path)
    lines: List[str] = [
        f"# Student digest - {section_path.stem}",
        "",
        f"Source: `{src_display}` | role: **{role}** | generated by `tools/make_digest.py`",
        "",
        "> Study aid, not a substitute for the draft. Every `[TO FILL]` must be replaced "
        "by me, in my own words, before the talk. This page may not add a fact that is "
        "absent from the draft and its evidence files.",
        "",
        "## What this section says",
        "",
    ]
    lines += [f"- {b}" for b in bullets]
    lines += ["", "## Why it is there", ""] + why
    lines += ["", "## What could be asked at a talk", ""]
    lines += [f"{i}. {q}" for i, q in enumerate(talk, start=1)]
    lines += ["", "## Five likely questions with honest answers", ""]
    for i, (q, a) in enumerate(five, start=1):
        lines += [f"### Q{i}. {q}", "", a, ""]
    lines += ["## Glossary", "", glossary_block(paragraphs)]
    lines.append("")

    text = "\n".join(lines)
    return {
        "text": text,
        "role": role,
        "paragraphs": len(paragraphs),
        "numbers": len(numbers),
        "citations": len(citations),
        "questions": len(five),
        "to_fill": len(re.findall(r"\[TO FILL\b", text)),
    }


# ---------------------------------------------------------------------- checking

def split_h2(text: str) -> List[Tuple[str, str]]:
    parts = re.split(r"^##\s+(.+?)\s*$", text, flags=re.M)
    blocks: List[Tuple[str, str]] = []
    for i in range(1, len(parts) - 1, 2):
        blocks.append((parts[i].strip(), parts[i + 1]))
    return blocks


def check_text(text: str, strict: bool) -> dict:
    findings: List[str] = []
    blocks = split_h2(text)
    by_name: Dict[str, str] = {}
    order: List[str] = []
    for name, body in blocks:
        if name in by_name:
            findings.append(f"duplicate block: ## {name}")
        by_name.setdefault(name, body)
        order.append(name)

    for name in BLOCKS:
        if name not in by_name:
            findings.append(f"missing block: ## {name}")

    positions = [order.index(name) for name in BLOCKS if name in order]
    if positions != sorted(positions):
        findings.append("blocks are out of order")

    body = by_name.get("What this section says", "")
    bullets = [ln for ln in body.splitlines() if re.match(r"^- (?!\[ \])", ln)]
    if not bullets:
        findings.append("'What this section says' has no bullets")
    for i, ln in enumerate(bullets, start=1):
        words = len(ln[2:].replace("\u2026", "").split())
        if words > MAX_BULLET_WORDS:
            findings.append(f"bullet {i} has {words} words (max {MAX_BULLET_WORDS})")

    why = by_name.get("Why it is there", "")
    checks = [ln for ln in why.splitlines() if ln.startswith("- [ ]")]
    if len(checks) < 3:
        findings.append("'Why it is there' has fewer than 3 checklist items")

    talk = by_name.get("What could be asked at a talk", "")
    talk_items = [ln for ln in talk.splitlines() if re.match(r"^\d+[.)]\s+\S", ln)]
    if not (3 <= len(talk_items) <= 6):
        findings.append(f"'What could be asked at a talk' has {len(talk_items)} questions (need 3-6)")

    five_body = by_name.get("Five likely questions with honest answers", "")
    heads = list(re.finditer(r"^### Q(\d+)\.\s*(.+)$", five_body, re.M))
    if len(heads) != 5:
        findings.append(f"'Five likely questions' has {len(heads)} questions (need exactly 5)")
    numbers_found = [int(h.group(1)) for h in heads]
    if numbers_found != list(range(1, len(heads) + 1)):
        findings.append(f"question numbering is not 1..{len(heads)}: {numbers_found}")
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(five_body)
        answer = five_body[head.end():end].strip()
        if not answer.startswith("I "):
            findings.append(f"Q{i + 1} answer is not in the first person ('I ...')")

    glossary = by_name.get("Glossary", "")
    entries = [ln for ln in glossary.splitlines() if ln.startswith("- **")]
    if entries:
        for ln in entries:
            m = re.match(r"^- \*\*(.+?)\*\*\s*([—–:-])\s*(.*)$", ln)
            if not m:
                findings.append(f"glossary entry is malformed: {ln[:60]}")
                continue
            if m.group(2) == ":" or "[TO FILL" not in m.group(3):
                findings.append(f"glossary entry looks like a definition, not a placeholder: {m.group(1)}")
    elif "No terms outside the built-in BCA vocabulary" not in glossary:
        findings.append("'Glossary' is empty (expected entries or the no-terms sentence)")

    unresolved = len(re.findall(r"\[TO FILL\b", text))
    if strict and unresolved:
        findings.append(f"{unresolved} unresolved [TO FILL] slot(s) remain (strict mode)")

    return {
        "ok": not findings,
        "strict": strict,
        "findings": findings,
        "stats": {
            "bullets": len(bullets),
            "checklist_items": len(checks),
            "talk_questions": len(talk_items),
            "five_questions": len(heads),
            "glossary_entries": len(entries),
            "to_fill": unresolved,
        },
    }


# -------------------------------------------------------------------------- CLI

def expand_sections(paths: Sequence[Path], all_mode: bool) -> List[Path]:
    out: List[Path] = []
    for path in paths:
        if all_mode:
            if not path.is_dir():
                raise ValueError(f"--all expects a directory, got: {path}")
            files = sorted(
                p for p in path.glob("*.md")
                if not p.name.startswith(("_", ".")) and p.name.lower() != "readme.md"
            )
            out.extend(files)
        else:
            if not path.is_file():
                raise ValueError(f"section file not found: {path}")
            out.append(path)
    # De-duplicate while preserving order.
    seen = set()
    unique = []
    for p in out:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def output_name(section: Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "-", section.stem).strip("-")
    return f"{stem.upper()}.md"


def write_readme_if_missing(out_dir: Path) -> None:
    # README.md is authored separately; this only prevents a confusing empty dir.
    readme = out_dir / "README.md"
    if readme.is_file():
        return
    readme.write_text(
        "# STUDENT-DIGEST\n\n"
        "Generated study aids. See the README maintained with this directory; every "
        "`[TO FILL]` must be filled in by the student before a talk.\n",
        encoding="utf-8",
    )


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Generate an auditable one-page student digest for a paper section.",
        epilog="Exit codes: 0 pass, 1 findings, 2 usage error.",
    )
    ap.add_argument("--section", type=Path, action="append", default=None,
                    help="draft section file (repeatable); with --all, a directory")
    ap.add_argument("--all", action="store_true",
                    help="treat each --section path as a directory of .md sections")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                    help="digest output directory (default: 06_review/STUDENT-DIGEST)")
    ap.add_argument("--index", type=Path, default=DEFAULT_INDEX,
                    help="results index JSON (default: 04_experiments/RESULTS-INDEX.json)")
    ap.add_argument("--citations", type=Path, default=DEFAULT_CITATIONS,
                    help="verified citations CSV (default: 02_literature/verified_citations.csv)")
    ap.add_argument("--root", type=Path, default=REPO_ROOT,
                    help="repo root used to resolve index `file` paths (default: repo root)")
    ap.add_argument("--role", choices=sorted(ROLES), default=None,
                    help="override the role inferred from the filename")
    ap.add_argument("--check", type=Path, metavar="DIGEST",
                    help="verify an existing digest instead of generating one")
    ap.add_argument("--strict", action="store_true",
                    help="with --check: fail if any [TO FILL] slot remains")
    ap.add_argument("--json", action="store_true", help="machine-readable output on stdout")
    ap.add_argument("--quiet", action="store_true", help="suppress human summary")
    args = ap.parse_args(argv)

    if args.strict and not args.check:
        ap.error("--strict is only valid with --check")

    # ------------------------------------------------------------ check mode
    if args.check:
        if not args.check.is_file():
            ap.error(f"digest not found: {args.check}")
        text = args.check.read_text(encoding="utf-8")
        result = check_text(text, strict=args.strict)
        result["path"] = str(args.check)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif not args.quiet:
            status = "PASS" if result["ok"] else "FAIL"
            print(f"{status}: {args.check}")
            for finding in result["findings"]:
                print(f"  - {finding}")
            s = result["stats"]
            print(
                f"  blocks ok | bullets={s['bullets']} | talk={s['talk_questions']} | "
                f"five={s['five_questions']} | glossary={s['glossary_entries']} | "
                f"to_fill={s['to_fill']}"
            )
        return 0 if result["ok"] else 1

    # --------------------------------------------------------- generate mode
    if not args.section:
        ap.error("--section is required (or pass --check DIGEST)")
    try:
        sections = expand_sections(args.section, args.all)
    except ValueError as exc:
        ap.error(str(exc))
    if not sections:
        ap.error("no section files found")

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    write_readme_if_missing(out_dir)
    ctx = EvidenceContext(args.index, args.citations, args.root)

    results = []
    any_structural = False
    for section in sections:
        try:
            built = build_digest(section, args.role, ctx)
        except OSError as exc:
            ap.error(f"cannot read {section}: {exc}")
        out_path = out_dir / output_name(section)
        if out_path.name.upper() == "README.MD":
            ap.error(f"refusing to overwrite {out_path} with a section digest")
        out_path.write_text(built["text"], encoding="utf-8")
        audit = check_text(built["text"], strict=False)
        if not audit["ok"]:
            any_structural = True
        results.append({
            "section": str(section),
            "out": str(out_path),
            "role": built["role"],
            "paragraphs": built["paragraphs"],
            "numbers": built["numbers"],
            "citations": built["citations"],
            "questions": built["questions"],
            "to_fill": built["to_fill"],
            "check_ok": audit["ok"],
            "check_findings": audit["findings"],
        })

    if args.json:
        print(json.dumps({"mode": "generate", "sections": results}, indent=2, ensure_ascii=False))
    elif not args.quiet:
        for r in results:
            print(
                f"wrote {r['out']} ({r['role']}, {r['paragraphs']} paragraphs, "
                f"{r['numbers']} numbers, {r['citations']} citations, "
                f"{r['questions']} questions, {r['to_fill']} [TO FILL])"
            )
            for finding in r["check_findings"]:
                print(f"  ! {finding}")
    return 1 if any_structural else 0


if __name__ == "__main__":
    sys.exit(main())
