"""Probe public sources for 2WikiMultihopQA dev. Logs URL/status/bytes/sha256 to a JSONL log."""
import json, time, hashlib, pathlib, sys
import requests

ROOT = pathlib.Path(r"C:\Users\shubh\research-lab")
RAW = ROOT / "04_experiments" / "data" / "raw" / "2wiki"
RAW.mkdir(parents=True, exist_ok=True)
LOG = ROOT / "04_experiments" / "data" / "raw" / "2wiki" / "fetch_log.jsonl"

UA = "research-lab-acquisition/1.0 (mailto:shubh.saxena2020@gmail.com)"


def log(entry):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(json.dumps({k: entry[k] for k in ("step", "url", "status", "bytes", "sha256") if k in entry}))


def get(url, step, timeout=60, max_bytes=None):
    t0 = time.time()
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout, allow_redirects=True)
        body = r.content
        entry = {
            "step": step, "url": url, "final_url": r.url, "status": r.status_code,
            "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
            "content_type": r.headers.get("content-type"), "elapsed_s": round(time.time() - t0, 2),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        log(entry)
        time.sleep(1.0)
        return r
    except Exception as e:
        log({"step": step, "url": url, "status": None, "bytes": 0, "sha256": None,
             "error": f"{type(e).__name__}: {e}", "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        time.sleep(1.0)
        return None


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "discover"
    if mode == "discover":
        r = get("https://huggingface.co/api/datasets?search=2wiki&limit=100", "1a-hf-search-2wiki")
        if r is not None and r.status_code == 200:
            ids = [d["id"] for d in r.json()]
            print(json.dumps(ids, indent=1))
            (RAW / "hf_search_2wiki.json").write_text(json.dumps(r.json(), indent=1), encoding="utf-8")
        r2 = get("https://huggingface.co/api/datasets?search=2wikimultihop&limit=100", "1b-hf-search-2wikimultihop")
        if r2 is not None and r2.status_code == 200:
            ids2 = [d["id"] for d in r2.json()]
            print("2wikimultihop:", json.dumps(ids2, indent=1))
            (RAW / "hf_search_2wikimultihop.json").write_text(json.dumps(r2.json(), indent=1), encoding="utf-8")
