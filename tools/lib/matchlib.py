"""Fuzzy comparison helpers for citation verification.

The hard part of citation checking is not fetching metadata, it is deciding whether two
strings name the same work. Rules used here, and why:

  * Titles are compared after Unicode NFKD folding (drops accents), lowercasing, removing
    LaTeX/markup, removing punctuation and collapsing whitespace. `_{}` `$` braced caps are
    stripped because BibTeX titles carry them.
  * Two title scores are computed and the *minimum* is used: `difflib` ratio (sensitive to
    word order and to long shared phrases) and a token-set F1 (insensitive to word order and
    to repeated boilerplate). Taking the minimum means a title must pass both, which is what
    catches "A Study of X" vs "X: A Study" being different papers with the same bag of words.
  * Authors are compared by *surname set* overlap (Jaccard), plus an explicit first-author
    check, because surname sets alone accept a different first author on a 9-author paper.
  * Years are compared with a tolerance of 1 year by default: preprint-vs-proceedings years
    legitimately differ by one. Anything more is a MISMATCH reason.
"""

from __future__ import annotations

import difflib
import re
import unicodedata
from typing import Iterable, List, Optional, Sequence, Set

# --------------------------------------------------------------------------- text


def fold(text: str) -> str:
    """NFKD-fold, strip accents, lowercase, collapse whitespace."""
    if not text:
        return ""
    t = unicodedata.normalize("NFKD", text)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.lower()
    t = t.replace("\u00ad", "")
    return re.sub(r"\s+", " ", t).strip()


_LATEX_NOISE = [
    (re.compile(r"\\[a-zA-Z]+\s*"), " "),      # \emph \textit ...
    (re.compile(r"[{}]"), ""),                  # braces protect case, they are not separators
    (re.compile(r"\$"), " "),                    # math mode
    (re.compile(r"``|''|--|~"), " "),
]

_STOP = {
    "a", "an", "the", "of", "for", "on", "in", "to", "and", "with", "via", "by",
    "from", "at", "as", "is", "are", "be", "it", "its", "towards", "toward",
}


def normalize_title(title: str) -> str:
    t = title or ""
    for pat, rep in _LATEX_NOISE:
        t = pat.sub(rep, t)
    t = fold(t)
    t = re.sub(r"[\u2010-\u2015\-_/\\|]+", " ", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_tokens(title: str, drop_stopwords: bool = True) -> List[str]:
    toks = normalize_title(title).split()
    if drop_stopwords:
        kept = [w for w in toks if w not in _STOP]
        # never return nothing: a title made only of stopwords is still a title
        return kept or toks
    return toks


def title_ratio(a: str, b: str) -> float:
    """difflib similarity on normalized titles (0..1). Order-sensitive."""
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return difflib.SequenceMatcher(None, na, nb, autojunk=False).ratio()


def token_f1(a: str, b: str) -> float:
    """Token-set F1 on content words (0..1). Order-insensitive."""
    ta, tb = set(title_tokens(a)), set(title_tokens(b))
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    if inter == 0:
        return 0.0
    prec, rec = inter / len(ta), inter / len(tb)
    return 2 * prec * rec / (prec + rec)


def title_similarity(a: str, b: str) -> float:
    """Conservative combined title score: min(difflib, token-F1), plus a bounded lift for
    subtitle truncation.

    The lift exists because databases routinely store a subtitle-less title ("BERT:
    Pre-training of Deep Bidirectional Transformers") while the record quotes the full one.
    It is deliberately narrow: the shorter title must be fully contained in the longer, and
    the *extra* words on the longer side must be few and must not be the words that turn one
    work into a different work (survey, review, benchmark, correction ...). Without that
    guard, a survey whose title merely begins with the target title scores 0.95 and a wrong
    DOI gets recorded as VERIFIED — the exact failure RULES.md #1 exists to prevent.
    """
    r = title_ratio(a, b)
    f = token_f1(a, b)
    score = min(r, f)
    na, nb = normalize_title(a), normalize_title(b)
    short, long_ = (na, nb) if len(na) <= len(nb) else (nb, na)
    if short and short in long_ and len(short.split()) >= 4:
        extra = [t for t in long_.replace(short, " ", 1).split()]
        different_work = _DIFFERENT_WORK_MARKERS & set(extra)
        if len(extra) <= _MAX_SUBTITLE_EXTRA and not different_work:
            score = max(score, 0.95)
    return round(score, 4)


#: Extra words above this count mean the "longer title" is a different, larger work.
_MAX_SUBTITLE_EXTRA = 4

#: Words that turn a title into a different work even when only a few are added.
_DIFFERENT_WORK_MARKERS = {
    "survey", "review", "tutorial", "benchmark", "benchmarks", "dataset", "datasets",
    "challenge", "revisited", "correction", "corrigendum", "erratum", "retraction",
    "commentary", "comment", "critique", "response", "reply", "reprint", "preprint",
    "extended", "appendix", "addendum",
}


# --------------------------------------------------------------------------- authors

_PARTICLES = {"van", "von", "de", "der", "den", "da", "di", "la", "le", "del", "du", "bin", "al"}


def split_authors(raw: str) -> List[str]:
    """Split an author string into individual names.

    Accepts 'A; B', 'A and B', 'A, B, C' only when it looks like 'Surname, Given' pairs.
    """
    if not raw:
        return []
    if ";" in raw:
        parts = raw.split(";")
    elif " and " in raw:
        parts = re.split(r"\s+and\s+", raw)
    else:
        parts = [raw]
    return [p.strip() for p in parts if p.strip()]


def surname(name: str) -> str:
    """Best-effort surname extraction from 'Given Surname' or 'Surname, Given'."""
    n = name.strip()
    if not n:
        return ""
    if "," in n:
        n = n.split(",")[0]
    else:
        toks = n.split()
        if len(toks) == 1:
            n = toks[0]
        else:
            # 'Ashish Vaswani' -> 'Vaswani'; 'Ludwig van Beethoven' -> 'van Beethoven'
            tail = [toks[-1]]
            i = len(toks) - 2
            while i >= 0 and toks[i].lower() in _PARTICLES:
                tail.insert(0, toks[i])
                i -= 1
            n = " ".join(tail)
    n = fold(n)
    n = re.sub(r"[^\w\s\-]", "", n)
    return re.sub(r"\s+", " ", n).strip()


def surname_set(names: Iterable[str]) -> Set[str]:
    return {s for s in (surname(n) for n in names) if s}


def author_recall(mine: Sequence[str], theirs: Sequence[str]) -> Optional[float]:
    """Fraction of the authors I listed that really are authors of the resolved work.

    This, not Jaccard, is the right primary check: drafts routinely cite only the first
    author ("Vaswani et al.") while the database lists eight. Jaccard would call that a
    mismatch, which is a false alarm on a correct citation.
    """
    a, b = surname_set(mine), surname_set(theirs)
    if not a or not b:
        return None
    return round(len(a & b) / len(a), 4)


def author_jaccard(mine: Sequence[str], theirs: Sequence[str]) -> Optional[float]:
    a, b = surname_set(mine), surname_set(theirs)
    if not a or not b:
        return None
    return round(len(a & b) / len(a | b), 4)


def author_similarity(mine: Sequence[str], theirs: Sequence[str]) -> Optional[float]:
    """max(recall, jaccard) — passes either "all my names are theirs" (short citation) or
    "our author lists overlap heavily" (full citation). Neither alone is sufficient."""
    r = author_recall(mine, theirs)
    j = author_jaccard(mine, theirs)
    if r is None or j is None:
        return None
    return round(max(r, j), 4)


def _given_initial(name: str) -> str:
    n = name.strip()
    if "," in n:
        given = n.split(",", 1)[1].strip()
    else:
        toks = n.split()
        given = " ".join(toks[:-1]) if len(toks) > 1 else ""
    given = fold(given)
    for ch in given:
        if ch.isalpha():
            return ch
    return ""


def first_author_agrees(mine: Sequence[str], theirs: Sequence[str]) -> Optional[bool]:
    """Surname must match; when both sides give a given name, the initial must match too.

    Initial-level comparison catches 'John Smith' vs 'Alice Smith' without demanding that
    'J. Smith' and 'John Smith' be written the same way.
    """
    if not mine or not theirs:
        return None
    if surname(mine[0]) != surname(theirs[0]):
        return False
    i1, i2 = _given_initial(mine[0]), _given_initial(theirs[0])
    if i1 and i2 and i1 != i2:
        return False
    return True



# --------------------------------------------------------------------------- verdicts


def is_authoritative_id(text: str) -> bool:
    return bool(re.search(r"\b10\.\d{4,9}/\S+", text or ""))


def numbers_in(text: str) -> List[float]:
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text or "")]
