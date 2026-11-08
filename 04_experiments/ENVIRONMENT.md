# ENVIRONMENT — C1 reproducibility (MF-30)

Frozen environment for every number in `04_experiments/results/`. Regenerate with
`python -m pip freeze > 04_experiments/requirements-lock.txt` inside the Hermes
venv below; the lockfile's sha256 is recorded in `REPRODUCE.md` and must match
before any result is re-derived.

## Host

- OS: Windows 10, version 10.0.26300 (Windows 11 host kernel reported as Windows 10)
- CPU: Intel64 Family 6 Model 197 Stepping 2, GenuineIntel, 14 logical cores
- Host name (machine): recorded per-run in `meta.json:host` by the harness

## Python

- Interpreter: `C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
- Version: 3.11.15
- `PYTHONHASHSEED`: 0 (set by `harness.runner.set_seeds`; launch with
  `PYTHONHASHSEED=0 python ...` for string-hash-dependent runs)

## Key libraries (from the venv)

- torch 2.15.0+cpu
- bm25s 0.3.16
- transformers 5.22.1
- sentence-transformers (provides `SentenceTransformer`, `CrossEncoder`)
- scikit-learn, numpy, scipy
- Full pin set: `04_experiments/requirements-lock.txt` (156 lines,
  sha256 `a49823349ededc0869dcc881b0ccc99c73d0723d96062087988eb02066a481a1`)

## Model checkpoints (Hugging Face cache, exact revisions)

| Model | HF id | Revision (refs/main) | Local cache dir |
|---|---|---|---|
| Dense encoder | `BAAI/bge-small-en-v1.5` | `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a` | `%USERPROFILE%\.cache\huggingface\hub\models--BAAI--bge-small-en-v1.5\snapshots\5c38ec7c...` |
| Cross-encoder | `cross-encoder/ms-marco-MiniLM-L-6-v2` | `233902d25c440f23af6f7d6e94d2946bac0bee0a` | `%USERPROFILE%\.cache\huggingface\hub\models--cross-encoder--ms-marco-MiniLM-L-6-v2\snapshots\233902d...` |
| Reader LLM | `Qwen/Qwen2.5-0.5B-Instruct` | `7ae557604adf67be50417f59c2c2f167def9a775` | `%USERPROFILE%\.cache\huggingface\hub\models--Qwen--Qwen2.5-0.5B-Instruct\snapshots\7ae5576...` |

Revisions verified from the cache's `refs/main` files on 2026-11-08. The dense and
cross-encoder revisions are the ones pinned in `PREREGISTRATION.md` §4; the reader
revision is the default of `reader_logprob.py` (`DEFAULT_MODEL`).

## Git state

- HEAD commit (round-3 setup): `76c67968227e3ae7a771b068aa6a6a364a57eb00`
  (`76c6796`)
- Working tree is dirty (round-3 in progress; no commit made by this lane).

## Heavy compute

- One heavy job at a time via `ops/HEAVY.lock` (`04_experiments/harness/lock.py`).
- Reader baseline (`reader_logprob.py`) is the heavy CPU job (~minutes); run it
  alone, with free RAM >= 8 GB.
}