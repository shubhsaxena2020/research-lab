import json, time, urllib.request, urllib.parse, os
UA = "mailto:shubh.saxena2020@gmail.com"
queries = [
 "abstention gate retrieval features two thresholds",
 "retrieval feature abstention both directions per rung",
 "hard negative ladder abstention precision false refusal",
 "negative hardness ladder retrieval gate",
 "two threshold abstention band retrieval",
 "abstain precision abstain recall false refusal rung",
 "overlap matched negatives abstention gate",
 "surface features abstention audit AUROC",
 "retrieval score gate answerability ladder",
 "dead zone abstention retrieval",
 "per rung abstention precision coverage",
 "retrieval-only features abstention calibration",
 "hardness ladder negatives abstention",
 "answerability gate retrieval features false refusal",
 "negative construction abstention gate both directions",
 "separability audit retrieval features",
 "overlap matched negatives retrieval abstention",
 "two thresholds retrieval features abstention gate",
]
outdir="02_literature/related-work-r3/raw/openalex_r3"
os.makedirs(outdir, exist_ok=True)
log=[]
for i,q in enumerate(queries,1):
    url="https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=5&mailto=shubh.saxena2020@gmail.com"
    try:
        with urllib.request.urlopen(url) as r:
            d=json.load(r)
        cnt=d["meta"]["count"]
        tops=[(w.get("title"), w.get("publication_year"), w.get("id")) for w in d.get("results",[])]
        rec={"idx":i,"query":q,"index":"OpenAlex","date":"2026-11-08","count":cnt,"top":tops}
        log.append(rec)
        with open(f"{outdir}/q{i:02d}.json","w",encoding="utf-8") as f:
            json.dump(d,f,indent=2)
        print(f"{i:2d} | {cnt:8d} | {q}")
        for t,y,oid in tops[:3]:
            print(f"     - {y} {t} ({oid})")
    except Exception as e:
        rec={"idx":i,"query":q,"index":"OpenAlex","date":"2026-11-08","error":str(e)}
        log.append(rec)
        print(f"{i:2d} | ERROR | {q} | {e}")
    time.sleep(1.2)
with open("02_literature/related-work-r3/openalex_r3_log.json","w",encoding="utf-8") as f:
    json.dump(log,f,indent=2)
print("done", len(log))
