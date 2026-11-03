# Scam, fraud and misinformation detection — deep dive (S2-7)

## 0. Scope and method

I searched through the lab's citation tool (OpenAlex + arXiv + Crossref behind
`verify_citations.py`) and, where the tool's upstream APIs were rate-limited, through a public web
search engine to locate candidate records, which were then put back through the tool for
verification. Roughly twelve query batches covered: SMS spam detection and its datasets; smishing
and phishing-URL corpora; LLM-based phishing generation and defence; fraud detection in digital
payments with an India angle; misinformation benchmarks (fact-verification, fake-news, truthfulness
evaluation); code-mixed and multilingual fraud text; paraphrase and adversarial evasion; and
calibration / human-in-the-loop triage. About 140 candidate records were screened by title and
abstract; forty-odd claims went to the verifier and 39 resolved into the verified CSV (two were
rejected on the first pass for title mismatch and re-claimed against the API's own title, because
OpenAlex indexes a shortened form of the 2011 DocEng title). One paper I had planned to cite turned
out to have been withdrawn by arXiv moderators and was dropped — a small demonstration of why the
gate exists).

Three things separate this from a normal survey. First, I measured the canonical dataset myself
rather than quoting remembered numbers, because "how much headroom is left on UCI?" decides whether
an SMS-based project is worth doing at all (script and log in
`02_literature/staging/S2-7-probe_uci.py` and `S2-7-probe_uci.log`). Second, every
licence in the table below was read off the dataset's own page or repository metadata on
2026-11-03, not recalled. Third, I treat the "misinformation detection" literature as a warning
rather than a template: it is five years ahead of scam detection in discovering that its own
benchmarks were measuring the wrong thing, and scam detection is repeating the mistake.

## 1. Taxonomy

**Cluster 1 — SMS/email spam filtering as a benchmark artefact.** The founding paper is Almeida,
Hidalgo and Yamakami's 2011 collection, which is the origin of the UCI SMS Spam Collection
(5,574 messages, 747 spam, 13.4%). Everything downstream inherits its structure: a two-class,
English, UK-and-Singapore-flavoured corpus where spam is promotional ("Sunshine Quiz! Win a super
Sony DVD recorder"), not fraudulent. Later work tried to break out of it. Tang et al. built
SpamHunter, a pipeline that mines Twitter for users *reporting* spam they received, runs object
detection on the screenshots, OCRs the message text, and produced 21,918 messages in 75 languages
over 2018–2021, with 95% precision and 87% recall at the pipeline level. Salman et al. then
aggregated the field into a ~68,000-message "Super SMS" corpus (61% ham / 39% spam) with an explicit
longitudinal analysis of how spam vocabulary drifted, and in a 2026 follow-up used it to test
*deployed* systems rather than academic classifiers — where SpamHunter's own hosted service scored
51.71% accuracy at 14.56% true-positive rate, i.e. it missed 85% of the spam in its own successor
dataset.

**Cluster 2 — smishing and URL-centric detection.** This cluster assumes the payload is a link.
Timko and Rahman released Smishing Dataset I: 1,062 community-submitted SMS phishing messages from
smishtank.com, enriched with VirusTotal and WHOIS features per URL. Earlier smishing-specific detectors such as
DSmishSMS (Mishra and Soni, 2021) were trained on small private collections, which is why their
accuracy figures do not transfer to other corpora. The systematic review by Pritom et al. (2026) surveys the whole attack/defence/dataset space and puts US 2024 SMS-phishing losses at
$470M. The uncomfortable empirical fact for this cluster is in my own probe: only 14.3% of the spam
in UCI contains a URL at all. A URL-centric detector is blind to the majority of the canonical
benchmark, and the modern Indian scam repertoire (digital arrest, KYC, "your parcel is held") is
mostly link-free by design because the attack happens in a voice call or a WhatsApp thread.

**Cluster 3 — LLM-generated social engineering, measured on humans.** Hazell's 2023 study generated
unique spear-phishing messages for over 600 British MPs with GPT-3.5 and GPT-4 at a fraction of a
cent each, and showed that basic prompt engineering defeats the vendor safeguards of the time.
Heiding et al. (IEEE Access 2024) ran the stronger experiment: 112 participants, four arms, and a
click-through rate of 19–28% for generic control emails, 30–44% for GPT-4-generated emails, 69–79%
for human-crafted V-Triad emails, and 43–81% when GPT-4 was guided by the V-Triad. The honest
reading is that in 2024 an LLM alone was *worse* than a skilled human social engineer but better than
a generic template, and the combination was worst of all. The 2025 SoK on LLM-generated phishing
systematises nine stages by which attackers breach model guardrails and names the structural
asymmetry: offence adapts per campaign, defence is static and reactive.

**Cluster 4 — defending at LLM scale.** Two strategies dominate. Fine-tuning wins on accuracy:
SpaLLM-Guard reports 98.6% accuracy with under 2% balanced FP/FN for a fine-tuned Mixtral, and is
explicit that zero-shot prompting is unreliable. Prompting is cheaper but capped: the MAKE 2024
study got a maximum F1 of 92.74% from prompt engineering on 1,000 phishing URLs, against fine-tuned
base models. A third strategy is stylometry — the ESWA 2025 study generated 63 GPT-4o phishing emails,
found Gmail and Outlook let more through than Yahoo, and then used 60 stylometric features to catch
what the filters missed. That last result is the seed of the most interesting open question in the
area, and §3 returns to it.

**Cluster 5 — Indian and Global-South payment fraud.** This is where the literature is thinnest
relative to the size of the problem. What exists: an industry paper from Google on UPI/Google Pay
that fine-tunes an LLM classifier on up to four million transactions and reports 93.33% accuracy on
curated transaction data, plus 89% accuracy on generated reasoning; CASE, an agentic system that
interviews potential victims to elicit scam intelligence for downstream enforcement; and BEACON, a
fine-tuned LLM that labels cybercrime narratives along six psychological manipulation categories and
a fourteen-stage tactical lifecycle, with ten categories aligned to Indian law-enforcement
nomenclature including "Digital Arrest", reporting a 20% accuracy gain over its base model. BEACON
is the closest thing to Indian-context scam NLP that exists, and its data is described as
"real-world and synthetically augmented" narratives with no independent audit. Outside India, the
AfricanNLP 2025 MOZ-Smishing benchmark for mobile-money fraud is the model of what a usable
Global-South corpus looks like: small, open-licensed, task-defined.

**Cluster 6 — misinformation: fact verification versus style classification.** Two research
communities share a name and almost nothing else. Fact verification (FEVER, SciFact) is a
retrieval-plus-entailment task with evidence: the label is derived from documents, so the model must
ground. Style classification (LIAR, the Twitter rumour sets, most "fake news" work) labels a claim
by its source, topic or prose style, with no evidence chain. TruthfulQA is a third thing again — an
evaluation of whether a *model's own answers* to adversarial questions are true, which is a
truthfulness benchmark for generators, not a misinformation detector.

The misinformation/disinformation distinction is almost never operationalised. Disinformation
requires intent to deceive; no benchmark in the table below carries an intent label, so a paper that
claims to detect "disinformation" is in practice scoring veracity or genre. Altay et al. (2023)
catalogue that slippage and the measurement problems it creates. Conflating these three tasks is the
field's original sin, and I keep them separate in the table.

**Cluster 7 — the measurement critique.** A small, recent, unusually honest literature exists that
mostly says the previous six clusters overstate themselves. Xiao and Mayer's SoK surveys 248
well-cited misinformation-detection papers and concludes that "current state-of-the-art in
fully-automated misinformation detection has limited efficacy in detecting human-generated
misinformation"; their replication found stylometry-based detection above 80% accuracy on routine
tasks dropping to about 50% in adversarial cases. Wu and Hooi show that event-based rumour benchmarks
leak: after event-separated re-splitting, state-of-the-art accuracy on Twitter16 falls from 90.2% to
44.3%. Pelrine et al. show that classifying on the first three digits of a tweet ID — i.e. the date —
reaches state-of-the-art on Twitter16. The 2024 dataset guide audits 75 misinformation datasets and
finds keyword-label predictivity far above baseline in four of them, and that most contain examples
that are ambiguous or impossible to verify. The 2025 "Truth over Tricks" paper shows that injecting
sentiment, style, topic or perplexity shortcuts drops detector accuracy by roughly 80% on average and
to 0% in the worst case, and that on datasets requiring actual world knowledge, detectors perform at
roughly chance. misinfo-general operationalises the fix: six generalisation axes (time, event, topic,
publisher, political bias, misinformation type) with distant labelling to force distribution shift.

## 2. What is saturated

Four things are done to death and adding another instance adds nothing.

*Another classifier on UCI SMS Spam.* There are dozens; the numbers are all 97–99% and the ranking
between architectures is noise. My own 46-second baseline (below) reaches F1 0.924, and the
literature's 0.98–0.99 may be inflated: the corpus carries 8.0% exact and 9.3% near-duplicate
messages, and no published split I found groups duplicates before splitting. Any paper whose
headline is "transformer beats SVM on UCI" is reporting a split artefact.

*Another smishing classifier on a self-collected set of a few hundred messages.* Typically no
baseline, no deduplication, no temporal split, and a train/test split of the same campaign.

*Zero-shot LLM prompting for phishing or spam detection, presented as a result.* SpaLLM-Guard already
established that zero-shot is unreliable and fine-tuning works; a paper that rediscovers this on a
new prompt template contributes a prompt, not a finding.

*Style-based "fake news" detection on LIAR or an ISOT-style corpus.* The measurement-critique cluster
has already shown these detect topic and publisher, not falsity.

## 3. What is genuinely open

**Open 1 — there is no public, licensed, modern Indian scam corpus, and the substitutes are not
substitutes.** After searching I can state this precisely. There is no peer-reviewed paper with a
released, licensed corpus of 2023–2026 Indian English, Hindi or Hinglish scam messages. The nearest
artefacts are: (a) BEACON's narrative set, released via an anonymous repository, described as
real-world plus synthetically augmented, with no licence and no annotation-agreement statistics;
(b) a Hugging Face dataset titled "Indian Scam Communication Dataset", Apache-2.0, 10k–100k rows,
Hindi+English, last modified July 2026, 31 downloads, whose card lists the scam categories it covers
and the models you might fine-tune but states no collection method, no annotator process and no
provenance — it may be templated or model-generated and a reader cannot tell; (c) MOZ-Smishing, which
is licensed and clean but is Mozambican Portuguese mobile-money fraud. The legitimate public
substitute is therefore not "find the dataset" but "construct one with a documented template space":
enumerate the manipulation tactics (urgency, authority impersonation, payment-rail instruction,
threat of arrest, KYC expiry), instantiate each with a small number of real public examples cited to
news reporting, and generate the rest from a *published* template grammar so that the synthetic/
real boundary is auditable. The relevant caution is that a synthetic corpus measures your template
space, not the world.

**Open 2 — nobody models the cost asymmetry, and almost nobody reports calibration.** The 2026
survey of operational evidence for LLMs in fraud and trust-and-safety codes 49 sources and finds
that among the 18 fraud and investigation sources, *none* report per-decision latency, per-decision
dollar cost, or calibration evidence. That is an extraordinary gap for a task where a false negative
is a stolen life-savings and a false positive is a blocked payment. My own probe makes the
consequence concrete: the same TF-IDF+logistic-regression scores give F1 0.924 at the default 0.5
threshold, 0.946 at a threshold of 0.64, 0.828 with recall collapsed to 0.707 at 0.9, and 0.128 at
0.99 — a factor of seven in F1 from threshold choice alone, with the score distribution's median at
0.12. A class-balanced model whose probabilities are not recalibrated to the deployment prior puts
the default threshold in the wrong place, silently. This is also the failure mode of the lab's other
asset (an abstention gate whose threshold sat outside the observed feature range): the same disease,
a threshold chosen without looking at the score distribution.

The repair kit exists, but mostly outside this area. Temperature scaling is the standard
one-parameter fix for over-confident classifiers (Guo et al., 2017). X-MAP is one of very few
spam/phishing papers that quotes an asymmetric operating point at all: a false-rejection rate of
0.089 at a 95% true-reject rate. Saka et al. (2026) show the full recipe on high-stakes legal
triage — recalibrate, then apply class-conditional conformal risk control to decide what to
auto-clear versus escalate — reaching 96.8% auto-clear accuracy with 0.5% of errors escaping
review, against 3.8% untuned. Real-time phone-scam work shows the same trade-off in another
costume: recall has to be bought with timeliness, so the operating point is a function of how long
the system may wait before warning the user (Shen et al., 2025).

**Open 3 — paraphrase evasion is measured for spam and for machine-text detection, but not for scam
intent, and never with an attacker-cost column.** The 2022 empirical SMS study tests paraphrasing,
EDA, homograph substitution, character spacing and character swaps against shallow, deep, syntactic
and semantic models, and finds word-embedding features comparatively robust. The 2026 robustness
study goes further and only admits perturbations verified to survive real SMS/RCS delivery, finding
that adversarial training transfers within a perturbation family but degrades sharply across
families, and recommending operating points for false-positive-sensitive vs recall-critical
deployments — the closest thing in this area to a cost-aware evaluation. Outside spam, the AI-text
detection literature has measured the collapse precisely: recursive paraphrasing drops watermark
TPR at 1% FPR from 99.3% to 9.7% and zero-shot detector AUROC from 96.5% to 25.2%, while DIPPER
paraphrasing drops DetectGPT from 70.3% to 4.6%. What nobody reports is the *cost* of the attack in
tokens or rupees per evaded message, which is the only number that tells a defender whether evasion
is economically rationed.

**Open 4 — the style-versus-factuality control has not been run for scam detection.** "Truth over
Tricks" shows that misinformation detectors keyed on sentiment, style, topic and perplexity collapse
when those cues are decorrelated from the label, and that accuracy on knowledge-requiring sets falls
to roughly chance. The scam analogue — train a detector on *surface form only* (punctuation,
capitalisation, message length, emoji, URL shape, currency symbols, digit patterns) with content
words removed, and see how much of the headline F1 survives — has, as far as I can resolve, not been
published. It matters because it decides whether "scam detection" is currently a legitimacy
classifier or a fraud classifier, and because regulatory claims ("our system detects fraud") would be
false in the former case.

**Open 5 — duplicate and near-duplicate leakage is unquantified in every SMS benchmark.** My probe
finds 444/5,574 (8.0%) exact-normalised duplicates and 518/5,574 (9.3%) messages with a ≥0.8
shingle-Jaccard near-duplicate in UCI. No paper I found reports a deduplicated split for UCI or for
Super SMS, and none reports group-aware cross-validation. The rumour-detection literature already
demonstrates what this does: 90.2% → 44.3% once the leak is closed.

**Open 6 — cross-lingual and code-mixed scam detection has no benchmark at all.** The Hinglish
literature I could resolve is almost entirely sentiment, emotion, sarcasm and cyberbullying. Fraud-R1
(8,564 cases, five fraud types, 15 LLMs, multi-round evaluation) is the only multilingual
fraud-robustness benchmark, and its own finding is a substantial Chinese/English performance gap.
There is no Hinglish equivalent, and no study of whether transliteration (Roman script Hindi) versus
Devanagari changes detector behaviour.

## 4. Benchmarks and datasets that a CPU laptop can actually use

Every licence below was read from the dataset's own page or repository API on 2026-11-03. Where the
answer is "no licence", that is the finding, not an omission.

| Dataset | What it contains | Size | Language | Age | Licence (verified) | Class balance | CPU cost | Specific validity threat |
|---|---|---|---|---|---|---|---|---|
| UCI SMS Spam Collection (Almeida et al.) | Promotional/UK SMS spam vs ham | 5,574 msgs | English | created 2011, donated Jun 2012 | CC BY 4.0 (stated on UCI page, DOI 10.24432/C5CC84) | 747 spam / 4,827 ham (13.4%) | <1 s to load; 46 s for 5-fold TF-IDF+LR (measured) | 8.0% exact dup, 9.3% near-dup (measured); spam is 2000s-era promotional, not fraudulent; labels from forum posts |
| SpamHunter / Clues in Tweets (Tang et al.) | Victim-reported SMS spam, OCR'd from tweet screenshots | 21,918 msgs (75 langs) | 75 languages | 2018–2021 | No LICENSE file in `opmusic/SpamHunter_dataset` (GitHub API reports none) | spam-only; you supply negatives | trivial (plain text) | Selection bias (people who tweet screenshots); OCR errors; no ham class; spam-only corpus cannot yield a precision figure |
| Smishing Dataset I (Timko & Rahman) | Community-submitted smishing SMS + URL/VirusTotal/WHOIS features | 1,062 msgs, 24 columns | English | 2024 (messages from 2022 on) | No licence stated on smishtank.com; direct CSV download, no account | phishing-only, no ham | trivial (732 KB CSV) | Positive-only; submission bias to one site; VirusTotal features are non-reproducible after the fact |
| Super SMS / "Investigating Evasive Techniques" corpus (Salman et al.) | Longitudinally analysed SMS spam+ham | ~68,000 msgs | English | 2024 | Paper says released for research; I could not locate a stable public download | 61% ham / 39% spam | minutes | If unavailable, treat as unavailable; the 2026 robustness paper reuses it, so an access request may work |
| Indian Scam Communication Dataset (Hugging Face) | "SMS, WhatsApp, call transcripts, chat" labelled scam/non-scam | ~10,000 claimed | Hindi + English (Hinglish) | last modified Jul 2026 | Apache-2.0 (dataset card) | unknown; card says "possible labels" | trivial | Provenance undocumented — no collection method, no annotators, no agreement; 31 downloads; assume synthetic until proven otherwise |
| MOZ-Smishing (AfricanNLP 2025) | Mobile-money fraud messages | small (benchmark set) | Portuguese (Mozambique) | 2025 | `creativeml-openrail-m` per HF card | task-defined | trivial | Licence is an odd fit for text; small; not Indian |
| FEVER | Claim + Wikipedia evidence → Supported/Refuted/NotEnoughInfo | 185k claims | English | 2018 | CC BY-SA 3.0 (fever.ai) | roughly balanced over 3 labels | Wiki dump is the cost; claim classification is minutes | Evidence retrieval dominates cost; domain is encyclopedic, not fraud |
| SciFact | Scientific claim verification against abstracts | 1.4k claims, 5k abstracts | English | 2020 | claims CC BY 4.0; corpus ODC-By 1.0 (LICENSE.md) | ~half supported | seconds-to-minutes | Tiny; biomedical only; near-duplicate abstracts across claims |
| TruthfulQA | Whether a *model's* answers to adversarial questions are true | 817 questions | English | 2022 | Apache-2.0 (repo) | not a binary classification set | minutes with a small judge | Not a misinformation detector at all; scoring needs a judge model or human |
| PhishTank | Live verified phishing URLs | ~thousands live at any time | URL only | continuous | No open licence; developer terms; app key registration required for automated downloads (verified on developer_info.php) | positive-only | trivial | Only *online-valid* phishes are served — dead URLs vanish, so any historical dataset built from it is survivorship-biased; no redistribution rights |
| OpenPhish | Live phishing URLs | live feed | URL only | continuous | Free feed for personal/academic research; no redistribution, no commercial use (terms.html) | positive-only | trivial | Reports each URL at most once per 14 days, never dead URLs — you cannot reconstruct history; ToS forbids republishing, so a paper cannot ship the data |
| misinfo-general | OOD generalisation across six axes | multi-corpus | English | 2024 | No LICENSE file in `ioverho/misinfo-general` (GitHub API reports none) | inherited | hours (many sub-benchmarks) | Licence ambiguity; distant labelling is noisy |
| Fraud-R1 | Multi-round LLM resistance to fraud/phishing inducements | 8,564 cases, 5 fraud types | Chinese + English | 2025 | see ACL anthology / repo | fraud-only scenarios | hours if you evaluate many models | Evaluates LLMs as *victims*, not as detectors; no ham class |

Two structural notes that the table cannot carry. First, the two URL feeds (PhishTank, OpenPhish) are
operational blocklists, not research corpora: they are positive-only, they delete history, and their
terms forbid redistribution, so a paper can use them for a live evaluation but cannot publish a
reproducible split derived from them. Second, the "modern, licensed, non-Western payment-fraud
corpus" does not exist for India; MOZ-Smishing exists for Mozambique, which tells you the gap is
about who funds dataset construction, not about technical difficulty.

## 5. Baselines runnable on this hardware

All of these are CPU-only, single laptop, no CUDA.

**TF-IDF + logistic regression (measured).** Word unigrams and bigrams, hashed to 2^17 buckets,
sublinear tf, L2-normalised, class-balanced logistic loss, five stratified folds, idf fitted inside
each training fold. F1 0.924 at threshold 0.5 (P 0.902 / R 0.946, 77 false positives out of 4,827
ham), F1 0.946 at the best threshold found by sweeping (P 0.984 / R 0.912). Total wall clock: 46
seconds including an O(n²) near-duplicate scan. This is the baseline any UCI-based paper must beat,
and it is also the cheapest possible calibration demonstration.

**fastText.** Hashed n-gram bag-of-words with a linear classifier; training on 5.5k short messages is
seconds and the model is a few MB. Expect it to land within noise of the TF-IDF baseline on a corpus
this size — the honest use of fastText here is as a *second* cheap baseline, not as an improvement.
Practical caveat: prebuilt wheels for very new CPython versions are unreliable, so budget ten minutes
for a source build or skip it.

**Small transformer fine-tunes.** Three candidates that fit comfortably in 2 GB and train in minutes
on 5.5k short texts: `distilbert-base-multilingual-cased` (~135M params, ~540 MB fp32), `MiniLM-L6`
(~23M, ~90 MB), and for Indic text `MuRIL-base` (~236M, ~950 MB) or `IndicBERT`. At 5,574 messages
and 64–128 tokens, one epoch is a few thousand steps of batch 16 — on the order of 5–15 minutes per
epoch on this CPU, so 3 epochs is a coffee break, not a cluster job. Freeze the lower layers if you
need it faster. The published numbers to beat on UCI-family corpora are 0.98–0.99 F1 / accuracy
(fine-tuned Mixtral reports 98.6% accuracy with <2% balanced FP/FN on Super SMS), but see §2: part of
that gap to my 0.924 is duplicates and test-set tuning, and the burden of proof is on whoever claims
the transformer, not on the baseline.

**Zero-shot small LLM prompting.** A 0.5B–2B instruct model in GGUF, run through llama.cpp, at
roughly 1–3 s per message on this CPU: usable for a 500-message qualitative probe, not for a
benchmark. The literature is unambiguous that zero-shot is the weakest option (SpaLLM-Guard), so use
it as a *ceiling check on your labels* — if a 1B model agrees with your hand labels less than 80% of
the time, your labelling guide is underspecified — rather than as a detector.

**What is not runnable here, and should be said out loud.** Anything scored by a 70B judge is not a
primary metric on this hardware; anything requiring a full Wikipedia dump per epoch is an hour per
run, not a minute; and any "we evaluate 15 LLMs" design (Fraud-R1) is out of scope unless the
public dev-time API is used, in which case the cost is dollars per run and the results are not
reproducible by a reader without the same API access.

## 6. Five candidate gaps

**G1 — the cost curve for scam triage, reported as a break-even ratio.** Every paper reports F1;
none reports what a false negative costs relative to a false positive, and the 2026 operational
survey confirms that zero of 18 fraud sources report calibration. The cheapest experiment: take UCI
and Super SMS, sweep the decision threshold, and instead of assuming a cost ratio, *invert* the
problem — report the FN:FP cost ratio at which each operating point becomes optimal. That converts an
arbitrary free parameter into a reported quantity a deployment team can compare against its own
numbers. Confound: the score distribution depends on the classifier, so the break-even ratio is
model-specific and a reviewer will ask whether you have just re-plotted the ROC. Mitigation: report
the break-even ratio for at least one non-parametric ranker alongside the parametric one, and show it
is stable. The cheapest variant of the whole study gives the classifier an abstain action and plots
coverage against precision on the deferred set: that is the measurement that diagnosed the lab's own
abstention gate (which over-refused on answerable items; a contaminated private evaluation, no figure
quoted), and human-in-the-loop
triage work suggests the upside is real — an LLM pre-filter automated 41.5% of a live review queue
while lifting human precision and recall by 9–11 points absolute (Thomas et al., 2024).

**G2 — the style-only control.** Strip content words, keep surface form (length, punctuation,
capitalisation, digits, currency symbols, emoji, URL shape, sender-ID pattern) and measure how much
of the headline F1 survives on UCI, Super SMS and Smishing Dataset I. If a style-only model reaches,
say, 0.85 F1, then the field's "detectors" are largely detecting *genre*, exactly as the
misinformation SoK found. Confound: the ablation also removes legitimate signal (urgency lexicon is
content), so a low style-only score does not prove the model is content-driven — you need the
complementary arm (content-only, style stripped) to interpret it, and near-duplicates inflate both
arms. Mitigation: deduplicate first, report both arms, and use a permutation test on the style
features.

**G3 — the code-mixing degradation curve.** Take a verified English scam set, produce three
Hinglish variants (full transliteration, 50% code-mixed, Devanagari), and measure the F1 delta for a
monolingual English encoder, a multilingual encoder and MuRIL. The claim under test is that
multilingual pretraining buys robustness to code-mixing, which is widely assumed and, for fraud text,
untested. Confound: machine-translated Hinglish is not natural Hinglish — the measured "degradation"
may be translationese, and a native reader will spot it immediately. Mitigation: human-verify 100
samples per variant and report inter-annotator naturalness ratings alongside the F1 delta.

**G4 — paraphrase evasion priced in attacker tokens.** Paraphrase scam messages with a small local
model at three strengths, measure detector F1 drop *and* record the tokens (hence cost) the attacker
spent per successfully evaded message. The AI-text literature gives the shape of the collapse
(TPR@1%FPR 99.3% → 9.7%); nobody gives the price. Confound: your paraphraser is weaker than a
motivated attacker's, so you underestimate evasion — state it as a lower bound. Mitigation: include
one human-paraphrased arm on 100 messages as an upper bound, and report both.

**G5 — dedup-aware splits, and what they do to the reported state of the art.** Re-split UCI and
Super SMS with near-duplicate groups held out together, re-run the standard baselines, and report the
delta with confidence intervals. The rumour literature predicts a large drop (90.2% → 44.3%); if SMS
shows a small drop, that is itself a useful negative result and it makes every future UCI paper
cheaper to evaluate. Confound: grouping shrinks the effective test set and widens intervals, so a
"drop" may be variance; use repeated grouped CV (5×5) and report intervals, not point estimates.

## 7. References

Listed alphabetically by first author; in-text citations give author and year. Every entry was
resolved through `verify_citations.py` and appears in `02_literature/staging/S2-7-verified.csv`
with its retrieval date. Where the record has a published DOI that DOI is given; where only an
arXiv DOI exists the entry says arXiv.

1. Arush Sachdeva, Rajendraprasad Saravanan, Gargi Sarkar, et al. BEACON: A Unified Behavioral-Tactical Framework for Explainable Cybercrime Analysis with Large Language Models (2025). arXiv preprint. arXiv:2512.06555
2. Camille Thibault, Jacob-Junqi Tian, Gabrielle Peloquin-Skulski, et al. A Guide to Misinformation Detection Data and Evaluation (2024). arXiv preprint. arXiv:2411.05060
3. Chidimma Opara, Paolo Modesti, Lewis Golightly. Evaluating spam filters and Stylometric Detection of AI-generated phishing emails (2025). Expert Systems with Applications. 10.1016/j.eswa.2025.127044
4. Chuan Guo, Geoff Pleiss, Yu Sun, et al. On Calibration of Modern Neural Networks (2017). arXiv preprint. arXiv:1706.04599
5. Daniel Timko, Muhammad Lutfor Rahman. Smishing Dataset I: Phishing SMS Dataset from Smishtank.com (2024). 10.1145/3626232.3653282
6. David Wadden, Shanchuan Lin, Kyle Lo, et al. Fact or Fiction: Verifying Scientific Claims (2020). Conference on Empirical Methods in Natural Language Processing (EMNLP). 10.18653/v1/2020.emnlp-main.609
7. Devendra Dahiphale, Naveen Madiraju, Justin Lin, et al. Enhancing Trust and Safety in Digital Payments: An LLM-Powered Approach (2024). 10.1109/BigData62323.2024.10825105
8. Felermino D. M. A. Ali, Henrique Lopes Cardoso, Rui Sousa‐Silva, et al. MOZ-Smishing: A Benchmark Dataset for Detecting Mobile Money Frauds (2025). Workshop on African Natural Language Processing (AfricaNLP). 10.18653/v1/2025.africanlp-1.23
9. Fengchao Chen, Tingmin Wu, Van Nguyen, et al. SoK: Systematizing Generation, Characteristics, and Defenses in LLM-Generated Phishing (2025). arXiv preprint. arXiv:2508.21457
10. Fouad S. Trad, Ali Chehab. Prompt Engineering or Fine-Tuning? A Case Study on Phishing Detection with Large Language Models (2024). Machine Learning and Knowledge Extraction. 10.3390/make6010018
11. Fredrik Heiding, Bruce Schneier, Arun Vishwanath, et al. Devising and Detecting Phishing Emails Using Large Language Models (2024). IEEE Access. 10.1109/access.2024.3375882
12. Herun Wan, Jiaying Wu, Minnan Luo, et al. Truth over Tricks: Measuring and Mitigating Shortcut Learning in Misinformation Detection (2025). arXiv preprint. arXiv:2506.02350
13. Ivo Verhoeven, Pushkar Mishra, Ekaterina Shutova. Yesterday's News: Benchmarking Multi-Dimensional Out-of-Distribution Generalization of Misinformation Detection Models (2024). 10.1162/COLI.a.585
14. James Peter Thorne, Andreas Vlachos, Christos Christodoulopoulos, et al. FEVER: a Large-scale Dataset for Fact Extraction and VERification (2018). Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT). 10.18653/v1/n18-1074
15. Jiaying Wu, Bryan Hooi. Probing Spurious Correlations in Popular Event-Based Rumor Detection Benchmarks (2022). arXiv preprint. arXiv:2209.08799
16. Julian Hazell. Spear Phishing With Large Language Models (2023). arXiv preprint. arXiv:06972
17. Kalpesh Krishna, Yixiao Song, Marzena Karpinska, et al. Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense (2023). arXiv preprint. arXiv:2303.13408
18. Kellin Pelrine, Jacob Danovitch, Reihaneh Rabbany. The Surprising Performance of Simple Baselines for Misinformation Detection (2021). arXiv preprint. arXiv:2104.06952
19. Keyur Gabani. Operational Evidence Gaps for LLMs in Fraud Detection and Trust-and-Safety Workflows (2026). arXiv preprint. arXiv:2607.13078
20. Kurt Thomas, Patrick Gage Kelley, David Tao, et al. Supporting Human Raters with the Detection of Harmful Content using Large Language Models (2024). arXiv preprint. arXiv:2406.12800
21. Madelyne Xiao, Jonathan Mayer. SoK: Machine Learning for Misinformation Detection (2023). arXiv preprint. arXiv:2308.12215
22. Mir Mehedi A. Pritom, Seyed Mohammad Sanjari, Maraz Mia, et al. Short Message Service (SMS) Phishing Attacks and Defenses: A Systematic Review (2026). arXiv preprint. arXiv:2604.11429
23. Muhammad Salman, Muhammad Ikram, Mohamed Ali Kaafar. An Empirical Analysis of SMS Scam Detection Systems (2022). arXiv preprint. arXiv:2210.10451
24. Muhammad Salman, Muhammad Ikram, Mohamed Ali Kâafar. Investigating Evasive Techniques in SMS Spam Filtering: A Comparative Analysis of Machine Learning Models (2024). IEEE Access. 10.1109/access.2024.3364671
25. Muhammad Salman, Muhammad Ikram, Nardine Basta, et al. SpaLLM-Guard: Pairing SMS Spam Detection Using Open-source and Commercial LLMs (2025). arXiv preprint. arXiv:2501.04985
26. Muhammad Salman, Muhammad Islam, Muhammad Ikram, et al. Johnny Still Receives Spam SMS: Assessing the Robustness of SMS Spam Detection (2026). arXiv preprint. arXiv:2609.01171
27. Nitish Jaipuria, Lorenzo Gatto, Zijun Kan, et al. CASE: An Agentic AI Framework for Enhancing Scam Intelligence in Digital Payments (2025). 2025 IEEE International Conference on Big Data (BigData), Macau, China, 2025, pp. 2177-2183. 10.1109/BigData66926.2025.11402424
28. Qi Zhang, Dian Chen, Lance M. Kaplan, et al. X-MAP: eXplainable Misclassification Analysis and Profiling for Spam and Phishing Detection (2026). arXiv preprint. arXiv:2602.15298
29. Sacha Altay, Manon Berriche, Alberto Acerbi. Misinformation on Misinformation: Conceptual and Methodological Challenges (2023). Social Media + Society. 10.1177/20563051221150412
30. Sandhya Mishra, Devpriya Soni. DSmishSMS-A System to Detect Smishing SMS (2021). Neural Computing and Applications. 10.1007/s00521-021-06305-y
31. Shu Yang, Shenzhe Zhu, Zeyu Wu, et al. Fraud-R1 : A Multi-Round Benchmark for Assessing the Robustness of LLM Against Augmented Fraud and Phishing Inducements (2025). arXiv preprint. arXiv:2502.12904
32. Siyuan Tang, Xianghang Mi, Ying Li, et al. Clues in Tweets: Twitter-Guided Discovery and Analysis of SMS Spam (2022). ACM CCS 2022. 10.1145/3548606.3559351
33. Stephanie Lin, Jacob K. Hilton, Owain Evans. TruthfulQA: Measuring How Models Mimic Human Falsehoods (2022). Proceedings of the conference - Association for Computational Linguistics. Meeting. 10.18653/v1/2022.acl-long.229
34. Surya Saka. Calibrated Trust, Not Sharper Prediction: An Empirical Test of Uncertainty Fusion (2026). arXiv preprint. arXiv:2608.14617
35. Tiago A. Almeida, José María Gómez Hidalgo, Akebo Yamakami. Contributions to the study of SMS spam filtering (2011). ACM Symposium on Document Engineering (DocEng). 10.1145/2034691.2034742
36. Vinu Sankar Sadasivan, Aounon Kumar, Sriram Balasubramanian, et al. Can AI-Generated Text be Reliably Detected? (2023). arXiv preprint. arXiv:2303.11156
37. William Yang Wang. "Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection (2017). Proceedings of the conference - Association for Computational Linguistics. Meeting. 10.18653/v1/p17-2067
38. Yekai Li, Rufan Zhang, Wenxin Rong, et al. SpamDam: Towards Privacy-Preserving and Adversary-Resistant SMS Spam Detection (2024). arXiv preprint. arXiv:2404.09481
39. Zitong Shen, Sineng Yan, Youqian Zhang, et al. "It Warned Me Just at the Right Moment": Exploring LLM-based Real-time Detection of Phone Scams (2025). arXiv preprint. arXiv:2502.03964
