#!/usr/bin/env python
"""Write reader batches from the curated high-risk lists, pulling abstracts from the local JSON.

No network. If an abstract is missing the batch says so and the reader must fetch the record.
"""
import json
import os
import re
import textwrap

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(LAB, "staging")
BATCH = os.path.join(STAGE, "S2b-batches")
os.makedirs(BATCH, exist_ok=True)

C1_TITLES = [
    "The Confidence Gate Theorem: When Should Ranked Decision Systems Abstain",
    "Training Negatives Still Matter After Calibrating Answerability Readouts",
    "Predictable Failure in Multi-Hop Retrieval: Score-Distributional Confidence Scoring and Abstention",
    "Evidence-Calibrated RAG for Unanswerable Question Answering: Retrieval Coverage, Abstention Calibration",
    "Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention",
    "Sufficiency-Gated Retrieval-Augmented Generation: Reducing Hallucination via Context Adequacy Estimation",
    "RCL: A Retrieval-Confidence Layer for Detecting Insufficient Context in Enterprise Retrieval-Augmented",
    "Before Answering: Evidence Sufficiency under Size-Matched Memory Construction",
    "BalanceRAG: Joint Risk Calibration for Cascaded Retrieval-Augmented Generation",
    "Cost-Aware Gated Retrieval: Decoupling Retrieval Initiation from Evidence-Conditioned Escalation",
    "Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL",
    "An LLM-Based Multi-Path Question Answering System with XGBoost Routing and Threshold-Based Refusal",
    "Refer, Infer, or Abstain: Investigating Latent Skill Selection of Large Language Models",
    "To Answer or to Abstain: Mitigating Search-Agent Hallucinations via Abstention-Aware Reinforcement",
    "Towards Reliable Long-Context Reasoning: Detecting Unanswerable Questions via FactGuard",
    "Answerability: LLMs Know What They Can Answer, Not Whether They Are Right",
    "Know Before You Fetch: Calibrated Retrieval-Budget Allocation for Retrieval-Augmented Generation",
    "Trusted Uncertainty in Large Language Models: A Unified Framework for Confidence Calibration",
    "Bounded-Abstention Pairwise Learning to Rank",
    "Difficulty-Gated Fusion of Reasoning Views for Temporal Retrieval",
    "When Silence Is Golden: Can LLMs Learn to Abstain in Temporal QA and Beyond",
    "Do I have the Knowledge to Answer? Investigating Answerability of Knowledge Base Questions",
    "Challenges in Information-Seeking QA: Unanswerable Questions and Paragraph Retrieval",
    "Learning When to Remember: Risk-Sensitive Contextual Bandits for Abstention-Aware Memory Retrieval",
    "Evidence-Gated Agent Architecture (EGAA): Evidence Sufficiency, Policy Hard-Gating, Plan Validation",
    "FinAbstain: Uncertainty-Calibrated Multimodal RAG for Selective Financial Forecasting",
    "Evaluating and Mitigating Over-Refusals in LLMs via Task-aware Representation Steering",
    "Understanding and Mitigating Over-refusal for Large Language Models via Representation Intervention",
    "AERIS-Chart: Evidence-Sufficient And Uncertainty-Calibrated Retrieval For Chart Claim Verification",
    "Reliable Biomedical RAG with Answerability-Aware Hybrid Retrieval",
    "When Visual Evidence Is Insufficient: How Instructions, Post-Training, and Internal Activations Shape",
    "Beyond Output-Space Calibration: Spectral Evidence Bundling for Selective Reliability Estimation",
]

C3_TITLES = [
    "The Fragility of Phishing Detection Models: Evidence from Cross-Corpus Transfer",
    "Anonymous Supplementary Artifact",
    "Default Zero-Shot LLM APIs Over-Flag Indian Financial SMS",
    "Cross-lingual SMS spam detection using GAN-based augmentation",
    "Handling Class Imbalance in SMS Spam Datasets Using Advanced Sampling Techniques",
    "Key insights into recommended SMS spam detection datasets",
    "Cost-Sensitive and Leakage-Aware Evaluation of Credit Card Fraud Detection Under Extreme Class Imbalance",
    "Explainable fraud detection under fixed false positive rate",
    "Objective over Architecture: Fraud Detection Under Extreme Imbalance in Bank Account Opening",
    "Cost-Sensitive Conformal Prediction and Human-in-the-Loop Abstention for Imbalanced High-Stakes",
    "Distribution-Free Error Control for Fraud Alert Triage",
    "Revisiting Resampling Strategies under Extreme Class Imbalance",
    "SMISHGUARD",
    "THRESHOLD OPTIMIZATION STRATEGIES FOR IMBALANCED FRAUD DETECTION MODELS",
    "A Comparative Study of Transformer-Based Models for Multi-Class SMS Phishing Detection",
    "What Standard Evaluations Hide About Detectors of Hijacked LLM Agents",
    "Resilient Semantic Threat Detection at the Edge: A Knowledge Distillation Framework for SMS Spam",
    "A TRANSFORMER-BASED DISTILBERT FRAMEWORK FOR REAL-TIME DETECTION OF PHISHING ATTACKS IN SMS AND WHATSAPP",
]


def load_all():
    out = []
    for name in ("C1", "C3"):
        with open(os.path.join(STAGE, f"S2b-screen-{name}.json"), encoding="utf-8") as f:
            out += json.load(f)
    return out


def find(rows, frag):
    f = re.sub(r"[^a-z0-9]+", " ", frag.lower()).strip()
    best = None
    for r in rows:
        t = re.sub(r"[^a-z0-9]+", " ", (r.get("title") or "").lower()).strip()
        if f in t:
            return r
    # looser: first 6 words
    key = " ".join(f.split()[:6])
    for r in rows:
        t = re.sub(r"[^a-z0-9]+", " ", (r.get("title") or "").lower()).strip()
        if key in t:
            return r
    return best


def write(path, header, items):
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n\n")
        for i, r in enumerate(items, 1):
            if r is None:
                f.write(f"## {i}. [NOT FOUND IN CACHE]\n\n")
                continue
            tt = re.sub(r"\s+", " ", r["title"]).strip()
            vv = re.sub(r"\s+", " ", r.get("venue") or "").strip()[:120]
            f.write(f"## {i}. {tt}\n")
            f.write(f"year={r.get('year')} | venue={vv} | "
                    f"cites={r.get('cites')} | openalex={r.get('openalex_id')} | "
                    f"doi={r.get('doi') or '(none)'}\n")
            if r.get("url"):
                f.write(f"openalex_url={r['url']}\n")
            f.write(f"authors={(r.get('authors') or '')[:200]}\n")
            ab = re.sub(r"\s+", " ", r.get("abstract") or "").strip()
            if ab:
                f.write("abstract: " + textwrap.fill(ab[:1800], 112) + "\n\n")
            else:
                f.write("abstract: (MISSING in OpenAlex — the reader must fetch the record)\n\n")


def main():
    rows = load_all()
    c1 = [find(rows, t) for t in C1_TITLES]
    c3 = [find(rows, t) for t in C3_TITLES]
    missing = [t for t, r in zip(C1_TITLES + C3_TITLES, c1 + c3) if r is None]
    print("missing from cache:", missing)
    for i in range(0, len(c1), 8):
        write(os.path.join(BATCH, f"R{i // 8 + 1}-C1.md"),
              f"Reader batch R{i // 8 + 1}: C1 slice candidates ({len(c1[i:i+8])} papers). "
              "Slice under test: two separate thresholds / a dead zone on RETRIEVAL-side features, "
              "evaluated per negative-hardness level, reporting false-refusal (over-refusal) too.",
              c1[i:i + 8])
    for j in range(0, len(c3), 8):
        write(os.path.join(BATCH, f"R{4 + j // 8}-C3.md"),
              f"Reader batch R{4 + j // 8}: C3 slice candidates ({len(c3[j:j+8])} papers). "
              "Slice under test: operating-point table (precision/recall/alerts per N) at sub-1% "
              "prevalence, threshold set from a cost ratio, ideally code-mixed Indian English SMS.",
              c3[j:j + 8])
    print("batches:", sorted(os.listdir(BATCH)))
    for p in sorted(os.listdir(BATCH)):
        print(p, os.path.getsize(os.path.join(BATCH, p)))


if __name__ == "__main__":
    main()
