import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from probe import get, RAW

CANDIDATES = [
    "voidful/2WikiMultihopQA",
    "thinkall/2WikiMultihopQA",
    "xanhho/2WikiMultihopQA",
    "framolfese/2WikiMultihopQA",
    "ohjoonhee/2WikiMultihopQA",
    "kamelliao/2wikimultihopqa",
]

mode = sys.argv[1]
if mode == "splits":
    for i, ds in enumerate(CANDIDATES):
        r = get(f"https://datasets-server.huggingface.co/splits?dataset={ds}", f"2-splits-{i}")
        if r is not None and r.status_code == 200:
            j = r.json()
            print(ds, "->", json.dumps(j.get("splits"))[:400])
            (RAW / f"splits_{ds.replace('/', '__')}.json").write_text(json.dumps(j, indent=1), encoding="utf-8")
        elif r is not None:
            print(ds, "->", r.status_code, r.text[:200])
