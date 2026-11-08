# TASK R3-2 — pre-registration integrity & reproducibility (main laptop, profile res-s2)

Goal: make the provenance of every result auditable, answering MF-4, 24, 30, 31, 32, 33, 37 (full text + evidence in
`06_review/reviews/round2-c1/AGGREGATE.md`).

OWNED: `04_experiments/PREREGISTRATION.md` (APPEND-ONLY: new dated amendment section at the end, never edit earlier text),
`04_experiments/PREREGISTRATION.sha256` (append a line), `04_experiments/requirements-lock.txt`,
`04_experiments/ENVIRONMENT.md`, `04_experiments/REPRODUCE.md`, `04_experiments/harness/**` (provenance fixes only, keep
tests green), `04_experiments/results/c1/r3/repro/**`, `sessions/R3-2-prereg-repro/**`.

Deliverables
1. Audit first: what does PREREGISTRATION.md + .sha256 actually contain today (the .sha256 lists a D4 hash — does the .md
   have a D4 section? when was it added relative to the corrected run's timestamps?). Write the facts with timestamps to
   `results/c1/r3/repro/PREREG-AUDIT.md`. Do not alter history.
2. MF-4/MF-32: if D4 is missing or incomplete in the log, append it as a POST-HOC deviation dated today, stating plainly it was
   recorded after the corrected run existed, and append the new hash line. MF-24: same treatment for the overlap-augmented
   audit (0.977/0.889/0.923) — find whether it is in the frozen text; if not, log it as a post-hoc exploratory analysis.
3. MF-31: explain why the frozen run's `preregistration_sha256` is '#' (find the bug in the harness), fix the harness for
   future runs with a test, and record the reconstructed link (which hash was current at the run's start time, with evidence)
   — never edit the frozen run's files.
4. MF-37: the frozen run came from a dirty tree. Reconstruct as far as possible which code produced it (git log/diff vs the
   run's commit, file mtimes) into `results/c1/r3/repro/DIRTY-TREE.md`; fix the harness to store `git diff` with every future
   run (test it).
5. MF-30: `requirements-lock.txt` from the real Hermes venv (`python -m pip freeze`), model checkpoints with exact HF revisions
   (MiniLM, cross-encoder, Qwen2.5-0.5B-Instruct — read their local cache refs), `ENVIRONMENT.md` with OS/CPU/python.
6. MF-33: `REPRODUCE.md` — the complete command list, in order, that regenerates every reported result incl. the transfer item
   builder and the reader baseline; run each command that is cheap (< 5 min) and confirm the output hash matches; mark the
   rest "not re-run" honestly.
7. `results/c1/r3/repro/ANSWERS.md` — per MF item: verdict, evidence, proposed draft sentences for §8 / deviation section.
