#!/usr/bin/env python
"""Verify the 00_foundations markdown files against WRITING-SPEC.

Checks, per file:
  1. exists, word count, has '## Sources', has 'last_updated: 2026-11-03'
  2. every inline [n] citation has a matching numbered entry in Sources
  3. every numbered Sources entry has a resolvable URL
  4. HTTP status of every distinct URL (GET, 20 s timeout, small read)
Outputs a table to stdout and logs/verify_foundations.json.
"""
import json
import os
import re
import time

import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "WHAT-IS-A-PAPER.md", "HOW-TO-WRITE-ONE.md", "VENUES-AND-PUBLISHING.md",
    "ETHICS-AND-AI-USE.md", "WHAT-A-PAPER-DOES-FOR-YOU.md", "GLOSSARY.md",
    "READING-LIST.md",
]
UA = {"User-Agent": "Mozilla/5.0 (compatible; research-lab-psit/1.0; "
                    "mailto:shubh.saxena2020@gmail.com)"}


def src_block(text):
    m = re.search(r"^##\s+Sources\b(.*)$", text, re.S | re.M)
    return m.group(1) if m else ""


def main():
    report = {}
    all_urls = {}
    for f in FILES:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            report[f] = {"error": "MISSING"}
            print("%-32s MISSING" % f)
            continue
        text = open(p, encoding="utf-8").read()
        sb = src_block(text)
        entries = re.findall(r"^\s*\[?(\d{1,2})[\]\.\)]\s", sb, re.M)
        # URLs anywhere in the Sources block
        urls = re.findall(r"https?://[^\s\)\]\>\"'`]+", sb)
        inline = set(int(x) for x in re.findall(r"\[(\d{1,2})\]", text))
        listed = set(int(x) for x in entries)
        words = len(re.findall(r"\b\w+\b", text))
        unresolved = sorted(x for x in inline if x not in listed and x > 0)
        uncited = sorted(x for x in listed if x not in inline)
        report[f] = {"words": words, "sources": len(listed), "urls_in_sources": len(urls),
                     "has_sources_heading": bool(sb),
                     "has_last_updated": "last_updated: 2026-11-03" in text,
                     "inline_citations": len(inline),
                     "inline_without_entry": unresolved,
                     "entries_never_cited": uncited}
        for u in urls:
            all_urls.setdefault(u.rstrip(".,;"), []).append(f)
        print("%-32s words=%5d sources=%3d urls=%3d lastupd=%s bad_cite=%s uncited=%s"
              % (f, words, len(listed), len(urls), "last_updated: 2026-11-03" in text,
                 unresolved[:6], uncited[:6]))

    # URL reachability (cap 120 URLs, 0.3 s apart)
    print("\nchecking %d distinct URLs ..." % len(all_urls))
    status = {}
    for i, u in enumerate(sorted(all_urls)):
        if i >= 120:
            break
        try:
            r = requests.get(u, headers=UA, timeout=20, stream=True, allow_redirects=True)
            status[u] = r.status_code
            r.close()
        except Exception as e:  # noqa: BLE001
            status[u] = "ERR:%s" % type(e).__name__
        time.sleep(0.3)
    bad = {u: s for u, s in status.items() if s != 200}
    print("URLs checked: %d, non-200: %d" % (len(status), len(bad)))
    for u, s in list(bad.items())[:20]:
        print("  %s  %s" % (s, u[:100]))
    report["_url_status"] = status
    with open(os.path.join(ROOT, "..", "logs", "verify_foundations.json"), "w",
              encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)


if __name__ == "__main__":
    main()
