#!/usr/bin/env python
"""Build claims for verify_citations.py add from the S2b shortlist (title + DOI/arXiv id only).

Bibliographic fields in the CSV come from the resolving API, never from this file: a claim whose
title does not match the resolved record is rejected by the tool, which is the point.
"""
import json
import os
import re

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(LAB, "staging")

WANT = [
    "Predictable Failure in Multi-Hop Retrieval",
    "Sufficiency-Gated Retrieval-Augmented Generation",
    "Before Answering: Evidence Sufficiency under Size-Matched",
    "Learning When to Remember: Risk-Sensitive Contextual Bandits",
    "BalanceRAG: Joint Risk Calibration",
    "Reliable Biomedical RAG with Answerability-Aware Hybrid Retrieval",
    "RCL: A Retrieval-Confidence Layer",
    "The Confidence Gate Theorem",
    "Training Negatives Still Matter After Calibrating",
    "Do LLMs Know When Evidence is Insufficient",
    "Cost-Aware Gated Retrieval",
    "Abstain-R1: Calibrated Abstention",
    "Beyond Confidence: Adaptive Abstention in Dual-Threshold Conformal Prediction",
    "Where Abstention Lives",
    "When Should LLMs Abstain? Chain-of-Self-Questioning",
    "The Fragility of Phishing Detection Models",
    "Default Zero-Shot LLM APIs Over-Flag Indian Financial SMS",
    "Anonymous Supplementary Artifact",
    "Cost-Sensitive Conformal Prediction and Human-in-the-Loop Abstention",
    "Distribution-Free Error Control for Fraud Alert Triage",
    "Objective over Architecture: Fraud Detection Under Extreme Imbalance",
    "Explainable fraud detection under fixed false positive rate",
    "The Threshold, Not the Model",
    "ConformalGuard: False-Positive-Controlled Action Gating",
    "A Hybrid Context-Aware Hinglish Spam And Scam Detection System",
    "Beyond Keywords: Attack Signatures",
    "Cost-Sensitive Threshold Optimization for Network Intrusion Detection",
]


def key(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


rows = {}
for ln in open(os.path.join(STAGE, "S2b-openalex-hits.jsonl"), encoding="utf-8"):
    r = json.loads(ln)
    rows.setdefault(key(r["title"]), r)

out, missing = [], []
for w in WANT:
    k = key(w)
    hit = None
    for tk, r in rows.items():
        if tk.startswith(k[:40].strip()):
            hit = r
            break
    if hit is None:
        missing.append(w)
        continue
    ident = hit.get("doi") or ""
    if not ident:
        missing.append(w + " [no DOI]")
        continue
    out.append({"title": hit["title"], "year": hit.get("year"), "doi_or_arxiv": ident})

path = os.path.join(STAGE, "S2b-claims.jsonl")
with open(path, "w", encoding="utf-8") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
print(f"claims: {len(out)}  ->  {path}")
print("missing:", missing)
