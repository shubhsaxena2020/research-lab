"""Acquire the PDFs the draft cites. Writes fetch_log.jsonl (url, status, bytes, sha256, ts)."""
import hashlib, json, os, time, urllib.request, urllib.error

SRC = os.path.dirname(os.path.abspath(__file__))
UA = "research-lab-acquisition/1.0 (mailto:shubh.saxena2020@gmail.com)"
LOG = os.path.join(SRC, "fetch_log.jsonl")
CAP_FILES = 10
CAP_BYTES = 80 * 1024 * 1024

TARGETS = [
    ("arxiv-2403.01461", "https://arxiv.org/pdf/2403.01461"),
    ("arxiv-1806.03822", "https://arxiv.org/pdf/1806.03822"),
    ("arxiv-2407.18418", "https://arxiv.org/pdf/2407.18418"),
    ("arxiv-2610.28340", "https://arxiv.org/pdf/2610.28340"),
    ("arxiv-2309.07597", "https://arxiv.org/pdf/2309.07597"),
    ("arxiv-1901.04085", "https://arxiv.org/pdf/1901.04085"),
    ("arxiv-2004.04906", "https://arxiv.org/pdf/2004.04906"),
    ("arxiv-2207.05221", "https://arxiv.org/pdf/2207.05221"),
    ("acl-2020.coling-main.580", "https://aclanthology.org/2020.coling-main.580.pdf"),
]


def log(rec):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read()


total = 0
nfiles = 0
for name, url in TARGETS:
    if nfiles >= CAP_FILES:
        break
    dest = os.path.join(SRC, name + ".pdf")
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"skip (exists): {name}")
        nfiles += 1
        continue
    for attempt in (1, 2):
        ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        try:
            status, body = get(url)
            size = len(body)
            if size < 10000 or not body[:5].startswith(b"%PDF"):
                raise ValueError(f"not a PDF ({size} bytes)")
            if total + size > CAP_BYTES:
                print(f"STOP: byte cap would be exceeded by {name}")
                raise SystemExit(0)
            with open(dest, "wb") as f:
                f.write(body)
            sha = hashlib.sha256(body).hexdigest()
            total += size
            nfiles += 1
            log({"ts": ts, "url": url, "status": status, "bytes": size, "sha256": sha,
                 "file": os.path.basename(dest), "attempt": attempt})
            print(f"OK  {name}: {size/1024:.0f} KB sha256 {sha[:16]}")
            break
        except Exception as e:
            code = getattr(e, "code", None)
            log({"ts": ts, "url": url, "status": code, "bytes": 0, "sha256": None,
                 "file": os.path.basename(dest), "attempt": attempt, "error": str(e)[:200]})
            print(f"ERR {name} attempt {attempt}: {code or ''} {e}")
            if attempt == 1:
                time.sleep(20)
    time.sleep(2)  # polite gap between requests

print(f"TOTAL {nfiles} files, {total/1024/1024:.1f} MB")
