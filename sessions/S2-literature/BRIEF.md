# S2 SUBAGENT BRIEF (read this fully before you start; RULES.md is binding)

Project root: C:\Users\shubh\research-lab  (Windows, bash terminal, python is 3.11 at `python`)

## Who this is for
Shubh, first-semester BCA student in India. The lab must produce ONE small, honest, reproducible
AI research paper in ~1-2 weeks of agent-assisted work, then weeks of student polishing. Audience
for our writing is a workshop / student track / arXiv preprint, NOT NeurIPS main track.

## Hardware reality (this constrains every recommendation you make)
- ONE Windows laptop: 48 GB RAM, Intel Core Ultra 5 225H, Intel Arc iGPU, NO CUDA.
- An old second laptop. No GPU cluster. Budget ~0.
- Available: CPU inference of small models (<=3B, ONNX/GGUF), the public LLM API used for dev-time
  experiments, and embedding models on CPU. Nothing that needs A100s, nothing that trains a
  transformer from scratch, nothing that needs >1 h per benchmark run.

So: any baseline or dataset you recommend must be runnable by **one CPU laptop in minutes-to-hours**.
Flag anything that is not. A dataset that needs a 70B judge to score it is NOT usable as a primary
metric — say so explicitly if you see it.

## The three assets the student actually has (inspiration only; never use private data)
1. A local agent-memory system with retrieval + "say I don't know" abstention, built and measured
   under a strict RAM budget. Its headline measured failure: an abstention gate that refused 47 of
   82 answerable questions (precision 0.30) because the decision lived in the answerer prompt and
   the threshold sat outside the observed feature range.
2. TrustShield — a scam/fraud-message detector that reached a national student finals.
3. Multi-agent orchestration with independent reviewer gates.
Topics where this experience gives a real edge are worth more than topics that merely sound hot.

## The one non-negotiable: citation discipline
Every paper you mention MUST be resolved against a real API through our tool, and only then may its
title appear in your output. If a paper cannot be resolved, drop it. Never cite from memory.

    cd C:\Users\shubh\research-lab

    # 1. find candidates (compact output: id, title, year, venue, doi)
    python 02_literature/tools/verify_citations.py search --query "your query" --limit 15
    python 02_literature/tools/verify_citations.py search --query "exact-ish title" --limit 15 --source both

    # 2. write claims, one JSON object per line, to 02_literature/staging/<YOUR-ID>-claims.jsonl
    #    {"title": "...", "year": "2025", "doi_or_arxiv": "arXiv:2501.01234"}
    #    (doi_or_arxiv is optional if the title is exact enough for OpenAlex)

    # 3. verify -> appends API-truth metadata to your own CSV, rejects mismatches
    python 02_literature/tools/verify_citations.py add \
        --in 02_literature/staging/<YOUR-ID>-claims.jsonl \
        --out 02_literature/staging/<YOUR-ID>-verified.csv

    # 4. pull abstracts in bulk so you can actually read the papers
    python 02_literature/tools/verify_citations.py enrich \
        --in ids.txt --out 02_literature/staging/<YOUR-ID>-abstracts.jsonl

The CSV is the ground truth for authors/year/venue. Copy those values into your markdown.
Read the abstracts before you characterise a paper's contribution — a title is not a result.
`MISMATCH` output means your claimed title does not match the resolved record: fix the title or
drop the paper. Do not "repair" an identifier to make it resolve.

## Reading depth required
"Read at abstract + intro + results level" means: for every paper, the abstract; for the ~8 most
important, also the intro/results. Use `web_extract` on https://arxiv.org/abs/<id> or the HTML
version https://arxiv.org/html/<id>v1 for the deeper reads. Do not read 25 PDFs.

## Output plan
For each deep-dive file, aim 2,500-4,000 words of dense, plain prose. Structure exactly as below.
Write in your own words. No paper text pasted. No bullet-point soup: each section needs a real
argument with numbers where the papers report numbers.

    # <AREA> — deep dive (S2-<n>)
    ## 0. Scope and method   (what you searched, which queries, how many records screened)
    ## 1. Taxonomy           (4-7 clusters; for each: the idea, the representative verified papers,
                              what actually improved and by how much on which benchmark)
    ## 2. What is saturated   (claims already made many times; adding another variant adds nothing)
    ## 3. What is genuinely open  (be specific and adversarial: name the confound, the missing control,
                              the population never tested, the measurement nobody does)
    ## 4. Benchmarks and datasets that a CPU laptop can actually use
        Table: name | what it measures | size | license | download/time cost | known gotchas
        (license and size are MANDATORY columns; verify them from the dataset's own page, not memory)
    ## 5. Baselines runnable on this hardware  (model, params, CPU cost, where to get it)
    ## 6. Five candidate gaps, one paragraph each, each stating the cheapest experiment that would
           test it and the most likely way that experiment would be confounded
    ## 7. References  (numbered; each line = verified title (year) venue + arXiv/DOI)

At the very end of your final reply (not the file), print:

    FILES: <paths you wrote>
    PAPERS_VERIFIED: <N>   (must equal the row count of your CSV)
    STATUS: DONE | PARTIAL <what is missing>

## Operating rules
- Decide and proceed. Do not ask questions; there is nobody to answer.
- Max 3 rework rounds on anything. Report PARTIAL honestly rather than padding.
- Stay inside C:\Users\shubh\research-lab. Do not touch other repos, profiles, or downloads >1 GB.
- Polite API use: the tool already throttles. Do not write your own scraping loop.
- If a command fails twice, change approach; do not retry the same thing five times.
