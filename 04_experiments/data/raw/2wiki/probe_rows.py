import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from probe import get, RAW

ds = sys.argv[1]
r = get(f"https://datasets-server.huggingface.co/rows?dataset={ds}&config=default&split=validation&offset=0&length=2",
        f"3a-rows-{ds.replace('/', '__')}-page0")
if r is not None:
    print("status", r.status_code)
    j = r.json()
    if "rows" in j:
        print("num_rows_total", j.get("num_rows_total"))
        print("features:", json.dumps(j.get("features"))[:1200])
        print("row0:", json.dumps(j["rows"][0], ensure_ascii=False)[:2500])
        (RAW / "rows_page0_sample.json").write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        print(r.text[:600])
