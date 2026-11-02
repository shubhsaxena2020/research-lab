"""Check the 10-line READ THIS FIRST block at the top of the seven S1 foundation docs.

For each file: count numbered lines in the block (must be 10), report the word
delta against the pre-edit word count (must be < 250), and print the reading
time stated in item 10. Run from the repo root or from this folder:

    python 00_foundations/verify_read_first.py
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

# Word counts measured with len(text.split()) before the block was added.
BASELINE = {
    "WHAT-IS-A-PAPER.md": 4000,
    "HOW-TO-WRITE-ONE.md": 4600,
    "VENUES-AND-PUBLISHING.md": 6833,
    "ETHICS-AND-AI-USE.md": 5524,
    "WHAT-A-PAPER-DOES-FOR-YOU.md": 5720,
    "GLOSSARY.md": 5757,
    "READING-LIST.md": 2191,
}

HEADER = "> **READ THIS FIRST — 10 lines**"
ITEM = re.compile(r"^> (\d{1,2})\. (.+)$")


def check(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    if lines[0].startswith("# ") is False:
        return {"error": "file does not start with an H1"}
    try:
        start = lines.index(HEADER)
    except ValueError:
        return {"error": "block header missing"}

    items = []
    i = start + 1
    while i < len(lines):
        m = ITEM.match(lines[i])
        if not m:
            break
        items.append(int(m.group(1)))
        i += 1

    numbers_ok = items == list(range(1, 11))
    last = lines[i - 1] if items else ""
    time_stated = ""
    m = re.search(r"(about [\d,]+ minutes[^.]*|a few seconds per word)", last)
    if m:
        time_stated = m.group(1)

    delta = len(text.split()) - BASELINE[os.path.basename(path)]
    return {
        "lines": len(items),
        "numbers_ok": numbers_ok,
        "delta": delta,
        "time": time_stated,
        "after_title": start == 2,
    }


def main():
    rows, bad = [], 0
    for name in BASELINE:
        r = check(os.path.join(BASE, name))
        if r.get("error"):
            rows.append((name, "ERR", "-", "-", r["error"]))
            bad += 1
            continue
        ok = r["lines"] == 10 and bool(r["numbers_ok"]) and int(r["delta"]) < 250 and bool(r["after_title"])
        bad += 0 if ok else 1
        rows.append((name, r["lines"], r["delta"], r["time"], "OK" if ok else "FAIL"))

    w = [max(len(str(x[i])) for x in rows + [("file", "block lines", "word delta", "reading time stated", "status")]) for i in range(5)]
    print("| " + " | ".join(h.ljust(w[i]) for i, h in enumerate(["file", "block lines", "word delta", "reading time stated", "status"])) + " |")
    print("|" + "|".join("-" * (w[i] + 2) for i in range(5)) + "|")
    for x in rows:
        print("| " + " | ".join(str(v).ljust(w[i]) for i, v in enumerate(x)) + " |")
    print()
    print("checks: 10 numbered lines, numbering 1-10, block starts directly after the H1, word delta < 250")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
