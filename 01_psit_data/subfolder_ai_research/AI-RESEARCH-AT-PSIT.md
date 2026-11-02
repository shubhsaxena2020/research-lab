# PSIT's AI research: what it publishes, who does it, and where a student can fit in

**What this page is for.** An evidence-based picture of AI work at PSIT (Pranveer Singh Institute of Technology, Kanpur, including PSIT College of Higher Education), from 793 PSIT-affiliated publication records plus PSIT's own public pages. Written for Shubh, first-semester BCA at PSIT CHE: what the institute does in AI, and where a gap he could work in might be.

**How the numbers were made.** `01_psit_data/papers.csv` (793 records; Crossref, Europe PMC, PubMed) has a boolean column `ai_related`. One-line count: **n=168 rows where `ai_related=='yes'`** — 21.2% of 793, matching `ai_related_total: 168` in `analysis/numbers.json`. Script: `01_psit_data/scripts/ai_subset_tables.py`; it writes the four CSVs used below.

---

## 1. Summary

PSIT publishes a lot, and a rising share is tagged AI: 168 of 793 records (21.2%), 62 dated 2026. The shape is narrow: mostly applied machine learning bolted onto another field — pharmacy and clinical reviews that *describe* AI, optical-communication papers with a learning component, small medical-imaging classifiers, IoT and agriculture dashboards. One in six AI-tagged titles is a review or survey; about a third are papers at broad Indian IEEE conferences. Measured: a name match of the 168 recorded venue strings against 21 named AI venues returns 0 hits — the denominator, the method and what it cannot see are in §5.1 — the median citation count is 0.5, and 84 of the 168 (50%) have no citations, concentrated in the 2025-26 cohort (§5.2). Authors divide into a CSE/IT/ECE group and a pharmacy group that barely intersect (§3.3). Publicly, PSIT advertises AI through three AI-named B.Tech programmes, an AICTE IDEA Lab, and a 2021 MoU for an "AI/ML Centre of Excellence" with two Noida companies, but publishes nothing checkable about compute, datasets or equipment, and its R&D pages are empty shells.

Measured on abstracts (§5.3): of the 108 records whose abstract is at least 200 characters, 3 mention a baseline, 1 a standard deviation, 0 a random seed; 59 records have no abstract at all, so this describes the abstracts, not the papers. **Interpretation:** the domain problems are real, and these abstracts rarely carry the evidence a replication would need; that gap is where a careful undergraduate can add something.

## 2. What AI work PSIT publishes

### 2.1 The 40 most recent AI-related records

All 40 fall in 2026 because 2026 alone holds 62 AI records (a partial year, including in-press items). PSIT authors appear as published, variants included.

| # | Year | Title | Venue | PSIT authors | DOI |
|---|------|-------|-------|--------------|-----|
| 1 | 2026 | A Detailed Insight into AI-driven Specific Damage Site Nano-detection (SDSND) for Precision Diagnosis of Breast Cancer | Current Cancer Therapy Reviews | Amrit; Brijesh Kumar Chaurasia; Chetan Gupta; Pragati Kumar; Pranay Wal | 10.2174/0115733947443575260824075827 |
| 2 | 2026 | A Graph-Based NLP for Threat Detection in Healthcare | ICISESSC 2026 | Brijesh Kumar Churasia | 10.1109/icisessc68634.2026.11542786 |
| 3 | 2026 | A Hybrid Machine Learning Approach with Explainable AI for Colorectal Cancer Risk Prediction from Dietary and Lifestyle Data | IC-AIDA 2026 | P. Shyam Prasad | 10.1109/ic-aida68291.2026.11564481 |
| 4 | 2026 | A Machine Learning-based Approach for Smart Agriculture Monitoring and Decision Support | Advanced Image Processing and Video Intelligence Applications | Anita Shukla; Ankit Jain | 10.2174/9798898815912126010014 |
| 5 | 2026 | A Novel Method for Identification and Classification of Spoken Language Using Machine Learning Approaches | Int. J. of Innovations & Research Analysis | Sanjeev Shukla | 10.62823/ijira/06.02(i).9040 |
| 6 | 2026 | A Survey Review of Computational Models and Their Applications in Predicting Drug-Drug Interactions | Current Bioinformatics | Ankita Wal; Devika Tripathi; Nand Kishore Sharma; Parul Srivastava | 10.2174/0115748936443228260708060955 |
| 7 | 2026 | Adaptive Memory Compression for Large Language Models: A Structured Multi-Stage Architecture with FAISS-Based Archival Retrieval | IC-SIT 2026 | Deepak Gupta; Suryansh Shukla; Uditanshu; Unnati Gupta | 10.1109/ic-sit69723.2026.11735767 |
| 8 | 2026 | Advances in artificial intelligence for predictive toxicology: From QSAR and omics integration to clinical safety translation | Computational Biology and Chemistry | Dwivedi J; Pandey K; Wal P | 10.1016/j.compbiolchem.2026.109120 |
| 9 | 2026 | Advancing Pharmacovigilance: AI and Deep Learning Approaches to Detect Adverse Drug Reactions from Big Data | Current Drug Safety | Pranay Wal | 10.2174/0115748863451595260605050739 |
| 10 | 2026 | AI-Assisted Energy Management System for an Ultra-Long-Endurance Solar-Powered High-Altitude UAV | (preprint, TechRxiv) | Vipin Kumar Jaiswal | 10.36227/techrxiv.177040552.20971330/v1 |
| 11 | 2026 | AI-driven Diagnostics, Phytocompound-based Therapeutics and Novel Approaches for Intracerebral Haemorrhage: A Systematic Review | Current Neurovascular Research | Ankita Wal; Madhup Ojha; Man Mohan Shukla; Zulfa Nooreen | 10.2174/0115672026450332260716093238 |
| 12 | 2026 | AI-driven digital twin for performance monitoring and fault prediction in optical communication networks | Journal of Optical Communications | Keshav Kumar; Mohit Kumar Srivastava; Vivek Kumar | 10.1515/joc-2026-0411 |
| 13 | 2026 | AI-driven visible light communication for smart hospitals and healthcare IoT | Journal of Optical Communications | Ankush Verma | 10.1515/joc-2025-0526 |
| 14 | 2026 | AI-Enabled Personalized Medicine in Lung Cancer: Diagnostics, Prognostics, and Targeted Drug Delivery — A Systematic Review | Current Pharmacogenomics and Personalized Medicine | Harsh Vardhan Johri; Zulfa Nooreen | 10.2174/0118756921432491260401063552 |
| 15 | 2026 | AI-integrated Approaches in Alzheimer's Disease: Linking Molecular Pathways, Biomarkers, and Emerging Therapies | Current Drug Targets | Kritika Sachan; Namra Aziz; Pranay Wal; Sakshi Srivastava | 10.2174/0113894501504715261014100550 |
| 16 | 2026 | AI-Powered Personalized Learning Systems for Enhancing Self-Confidence and Communication Skills | J. of Asia Entrepreneurship and Sustainability | Nandita Maurya; Purnima Sharma; Shalika Grace Das | 10.66635/s3jqc362 |
| 17 | 2026 | Air quality assessment using geospatial technique and artificial neural network (ANN) analysis for an urban city, Uttar Pradesh | J. of Environmental Engineering and Science | Abhishek Dixit | 10.1680/jenes.25.00019 |
| 18 | 2026 | An ensemble of deep learning models with falcon optimization assisted diabetic retinopathy diagnosis on retinal fundus images | Scientific Reports | Gupta IK | 10.1038/s41598-025-11075-x |
| 19 | 2026 | An Interpretable Hybrid Deep Learning Framework for Student Placement Prediction Using PSO-GA-Bayesian Optimized ANN with SHAP-LIME Explainability | (preprint, Research Square) | Upasana Dugal | 10.21203/rs.3.rs-10747729/v1 |
| 20 | 2026 | Artificial Intelligence in Phenylketonuria: Bridging Conventional Gaps in Diagnosis and Treatment — A Systematic Review | Reviews on Recent Clinical Trials | Ankita Wal; Himangi Vig; Nishant Kumar; Raghuraj Singh Suryavanshi | 10.2174/0115748871444112260226045508 |
| 21 | 2026 | Artificial Intelligence-Driven Diagnosis, Prediction, and Management of Polycystic Ovarian Disease (PCOD): A Comprehensive Systematic Review | Current Pharmaceutical Design | Ankita Wal | 10.2174/0113816128453237260817113317 |
| 22 | 2026 | Artificial Intelligence-Driven Gene Delivery Systems in Dementia: A Comprehensive Review | Current Gene Therapy | Ankita Wal; Brijesh Chaurasia; Manmohan Shukla; Pranay Wal | 10.2174/0115665232436545260906074748 |
| 23 | 2026 | Artificial Intelligence-powered Advances in Phytomedicine: A Systematic Review on Plant-based Drug Discovery Software | Current Drug Discovery Technologies | Aditi Nigam; Ankita Wal; Himangi Vig; Virat Kumar Pandey | 10.2174/0115701638388155251020065128 |
| 24 | 2026 | Brain Tumor Detection in MRI images Using Hybrid Machine Learning Model | ICSPED 2026 | Pradeep Kumar Gupta; Utkarsh Pandey | 10.1109/icsped65817.2026.11448483 |
| 25 | 2026 | Design and Evaluation of a Secure Air-Gapped LLM-Based Intelligence Analysis Framework | (preprint, Research Square) | Anand Rawat | 10.21203/rs.3.rs-9016380/v1 |
| 26 | 2026 | Efficient Phishing URL Detection Using Minimal-Feature Machine Learning Models | GTSS 2026 | Amit Yadav; Kanak Pandey; Kartik Bajpai; Krati Tiwari; Mahi Sonkar | 10.1109/gtss68743.2026.11679599 |
| 27 | 2026 | Enhancing Semantic Segmentation-based Change Detection in Bi-temporal Satellite Images | Recent Patents on Engineering | Satyasundara Mahapatra | 10.2174/0118722121499906261007055340 |
| 28 | 2026 | Federated graph equalization for orientation-robust cell-free visible light communication with angle-diversity receivers | Journal of Optical Communications | Keshav Kumar; Man Mohan Shukla; Mohit Kumar Srivastava | 10.1515/joc-2026-0230 |
| 29 | 2026 | Forensic Applications of Generative AI in Image Reconstruction | Advancements in Forensic Analysis of Digital Images (book) | Esha Tripathi; Mohit Pandey; Shubhangi Sankhyadhar | 10.4018/979-8-3373-3795-1.ch003 |
| 30 | 2026 | From 16S rRNA to deep learning: Evolution of computational approaches in human microbiome studies | Computational Biology and Chemistry | Dwivedi J; Shukla MM; Upadhyay A; Wal A | 10.1016/j.compbiolchem.2025.108852 |
| 31 | 2026 | From Automation to Augmentation: The Changing Role of AI in Management | Int. J. of Advanced Research in Science, Communication and Technology | Prachi Malhotra; Smruti Ranjan Rath | 10.48175/ijarsct-38080 |
| 32 | 2026 | Genomic Analysis and Bioinformatic Tools: Mapping Paths to Precision Medicine | Current Chemical Biology | Anil Kumar Yadav; Ashish Srivastava; Parul Srivastava | 10.2174/0122127968433199260303195205 |
| 33 | 2026 | Harnessing CRISPR-Cas Technology for Precision Antimicrobial Targeting | Current Topics in Medicinal Chemistry | Ankita Wal; Neha Verma; Zulfa Nooreen | 10.2174/0115680266395401251105000157 |
| 34 | 2026 | Harnessing multimodal deep representation with dimensionality reducing approach for enhanced intrusion detection system in IoT networks | Scientific Reports | Singh R | 10.1038/s41598-026-36135-8 |
| 35 | 2026 | Harnessing the Power of Large Language Models for Drug Discovery: A Systematic Review | Current Computer-Aided Drug Design | Ankita Wal; Manmohan Shukla; Pranay Wal; Kritika Sachan | 10.2174/0115734099432517260829135754 |
| 36 | 2026 | Human-Centered AI and Decision Support in Security Operations Centers | Advances in Computational Intelligence and Robotics | Anita Shukla | 10.4018/979-8-2600-1970-2.ch006 |
| 37 | 2026 | Hybrid Deep Learning Approach for Brain Tumor Detection Using Swin Transformer | EVST 2026 | Ankush Verma | 10.1109/evst69093.2026.11660600 |
| 38 | 2026 | Hybrid Deep Learning Architecture for Glaucoma Detection: Integrating a Multi-Network CNN Ensemble with ANFIS | Int. J. of Research and Scientific Innovation | Ishan Dwivedi; Mritunjay Yadav; Pradeep Yadav | 10.51244/ijrsi.2026.1303000149 |
| 39 | 2026 | Industry 5.0 and Digital Transformation: The Convergence of Humanity and Technology | Metaverse Dynamics | Divyanshi Yadav; Sebya Yadav | 10.1108/978-1-83662-666-420261001 |
| 40 | 2026 | Intelligent Modeling of Mechanical Behavior in FDM-Fabricated Graphene/PLA Composites Using ANN, GEP, and RSM Approaches | Engineering Reports | Ritesh Dixit | 10.1002/eng2.71120 |

### 2.2 What else these AI papers are tagged as

`topics` is multi-label, so one paper can be both AI and pharmacy. Within the 168:

| Topic tag | AI papers | Share |
|---|---|---|
| machine-learning | 133 | 79% |
| medicine-clinical | 58 | 35% |
| networks-iot | 31 | 18% |
| security-crypto | 17 | 10% |
| pharmacy-drug-delivery | 14 | 8% |
| nlp | 11 | 7% |
| energy-environment | 11 | 7% |
| pharmacology-toxicology | 10 | 6% |
| data-engineering | 9 | 5% |
| management-economics | 8 | 5% |
| chemistry-materials | 6 | 4% |
| computer-vision | 3 | 2% |
| education-pedagogy | 2 | 1% |

**Measured:** 53 of 168 carry only the `machine-learning` tag. Medicine and pharmacy tags together cover **62 records (36.9%)** when each record is counted once; adding the three column entries (58 + 14 + 10) gives 82, but that sum double-counts multi-labelled records and is not a record count. Computer vision touches 3 records, NLP 11. **Interpretation:** a third of the output carries no domain anchor, which is the shape of a generic "ML for X" paper, and the centre of gravity is biomedical rather than core AI.

### 2.3 Where it is published, and whether those are AI venues

119 distinct venues for 168 papers; 95 appear once.

| Venue | AI papers |
|---|---|
| *(no venue recorded)* | 9 |
| Journal of Optical Communications | 7 |
| Scientific Reports | 5 |
| Advances in Computational Intelligence and Robotics (IGI book series) | 5 |
| Diagnostics (MDPI) | 5 |
| Journal of Biomaterials Science, Polymer Edition | 3 |
| INDIACom 2025 (IEEE) | 3 |
| ICSIT 2025 | 3 |
| Expert Systems (Wiley) | 3 |
| IC-SIT 2026 | 2 |
| Computational Biology and Chemistry | 2 |
| Current Drug Targets | 2 |
| Current Pharmaceutical Design | 2 |
| Current Drug Discovery Technologies | 2 |
| Multimedia Tools and Applications | 2 |

I opened five on 2026-11-03:

- **Journal of Optical Communications** (De Gruyter) — 7 records, the biggest single venue here. Its front page leads with optical-burst-switching and congestion-control articles [10]. An optics journal: "AI-driven digital twin" puts ML inside a communications problem, not at its centre.
- **Diagnostics** (MDPI) — 5 records. Its scope lists about twenty clinical areas, one being "machine learning and artificial intelligence in diagnostics" [11] — an accepted sub-topic, not the subject.
- **Expert Systems** (Wiley) — 3 records, and a genuine AI journal: "the integration of artificial intelligence and knowledge engineering in real-world complex systems" [12]. The most AI-native venue in the top 15, and a journal, not a conference.
- **Scientific Reports** — 5 records. Broad multidisciplinary Nature Portfolio journal, no AI-specific scope [13]: a general bar, not an AI one.
- **Advances in Computational Intelligence and Robotics** — 5 records, but an IGI Global *book series* (ISSN 2327-0411) [14], not a journal or conference; chapters there are edited-volume contributions.

**IC-AIDA 2026** (IEEE, Bangalore, 10-11 April 2026) is real [15] — a broad "AI-driven innovations" conference. IC-SIT, ICISESSC, ICSPED, EVST and GTSS follow the same pattern: recent, wide-scope, IEEE-branded, India-hosted.

### 2.4 What kind of AI work this actually is

Reading ten titles and abstracts, five genres repeat:

1. **Review-of-AI-in-my-field.** 27 of 168 titles (16.1%) contain review/survey/systematic/overview/insight/advances — AI in phenylketonuria, AI in PCOD, LLMs for drug discovery.
2. **Optimiser-of-the-month classifiers.** 18 of 168 titles (10.7%) name an optimiser: "Falcon Optimizer with Ensemble of Deep Learning", "Fennec Fox Optimization", "PSO-GA-Bayesian Optimized ANN", "golden jackal optimization of XGBoost". A standard classifier, a new metaheuristic around its hyperparameters, accuracy on a public medical image set.
3. **ANN as a regression tool in a non-CS field.** Air quality in Kanpur from station data; 3D-printed graphene/PLA composites via "ANN, GEP, and RSM"; crop yield forecasting.
4. **Systems papers with a learning component.** Digital twins for optical networks, federated learning for visible-light communication, LLM memory compression with FAISS.
5. **Descriptive essays.** "From Automation to Augmentation: The Changing Role of AI in Management"; "Industry 5.0 and Digital Transformation" — no experiment at all.

Fragments as evidence, each under 15 words:

- "The proposed model captures the non-linear interactions" — air-quality ANN paper (row 17).
- "Falcon Optimizer with Ensemble of Deep Learning Algorithm" — retinopathy paper (row 18).
- "This review describes an advanced breast cancer detection system" — breast-cancer AI review (row 1).

A keyword scan of the 108 abstracts over 200 characters (same denominator as §5.3; counts printed by `scripts/ai_abstract_audit.py`, saved to `raw/ai_abstract_audit.json`) finds "dataset" in 29, "accuracy" in 38, "baseline" in 3, "ablation" in 2, "standard deviation" or "±" in 1, "seed" in 0, a significance test ("statistically significant" or "p-value") in 2, "cross-validation" in 5, "reproduc…" in 2. **Measured:** the vocabulary of ML evaluation is rare in these abstracts. **Interpretation:** that says little about the papers — an abstract is a lossy summary, and a paper can fix seeds in its methods section without saying so. I read no full text.

One integrity note: the 168 include a retraction note and the article it retracts — "Retraction Note: COVID-19 Detection using adopted convolutional neural networks and high-performance computing" (2026) and "RETRACTED ARTICLE: COVID-19 Detection using adopted convolutional neural networks and high-performance computing" (2024), both in Multimedia Tools and Applications, both flagged `ai_related`, so both are counted in every statistic on this page. A second retraction pair ("Real-Time Fraud Detection and Securing Customer Transactions in E-Commerce", 2025) sits outside the 168 because neither of its records is flagged `ai_related`. Separately, the abstract attached to one 2026 intrusion-detection paper (row 34) concerns rural cycling-network planning — a possible Crossref metadata mix-up. `UNCERTAIN`: I did not open the publisher page.

## 3. Who does it

### 3.1 From the data: the 185 author strings, top ten

Counted from `psit_authors` over the 168 AI records; variants are as published, so these are lower bounds.

| Author (as published) | AI papers | Department evidence (`affiliations`) |
|---|---|---|
| Brijesh Kumar Chaurasia | 10 | CSE (+ "Chaurasia BK" 3, "Brijesh Chaurasia" 1 → ~14) |
| Ankita Wal | 10 | Pharmacy |
| Pranay Wal | 9 | Pharmacy |
| Rajat Verma | 7 | CSE |
| Sushant Agarwal | 6 | CSE (+ "Agarwal S" 5 → ~11) |
| Mohit Kumar Srivastava | 5 | ECE |
| Ruchika Rastogi | 5 | Business Administration |
| Arunendra Singh | 5 | Information Technology |
| Zulfa Nooreen | 4 | Pharmacy |
| Keshav Kumar | 4 | optical/communication group |

**Measured:** the AI output splits between a CSE/IT/ECE group and a pharmacy group of at least the same size. **Interpretation:** a conversation about "AI at PSIT" that only involves computer science misses about half the output.

### 3.2 From public pages: what the institute says about itself

- **A faculty directory exists** at psit.ac.in/academics/faculty — name, designation, qualification, "Areas of Specialization", a Scholar/ResearchGate link field [1]. On 2026-11-03 only the Mechanical Engineering block rendered; the list is served per department from an endpoint that answered "Access Denied", so **I could not read the CSE roster**. `UNCERTAIN`: whether the CSE roster is as incomplete as the one profile below.
- **Profiles list publications, unusably.** Prof. Subhash Singh Parihar (Professor, CSE) lists 13 journal papers as plain text — journal and title, **no years, no DOIs** for most [2], including "Object detection using augmented attention assisted diffusion based vision transformer", Signal, Image and Video Processing (2026). A profile that cannot be checked is not evidence of output.
- **Three AI-named degrees**: B.Tech CSE (Artificial Intelligence) [3], CSE (Data Science) [4], CSE (AI and Machine Learning). The CSE page claims 960 B.Tech and 18 M.Tech seats and NBA accreditation in 2019 and 2022, but its "Faculty Excellence" paragraph names **no faculty at all** [3].
- **AICTE IDEA Lab** is the one lab with names: Chief Mentor Dr Man Mohan Shukla (Vice President), Faculty Coordinator Dr Raghuraj Singh Suryavanshi (Additional Director), Co-Coordinator Dr Nand Kishore Sharma (HOD, CSE), five "Tech Gurus", four student ambassadors [5]. A makerspace, not an AI research lab.
- **A "Center of Excellence for AI/ML" exists on paper**: MoU dated 6 July 2021 between PSIT, The Ikigai Lab (Noida) and Pingala AI Pvt Ltd, "to establish a Center of Excellence (CoE) at PSIT in focused area of AI/ML learnings" [6]. Its clauses concern training programmes, certificates and fee-sharing — not equipment or publications. The Self Study Report repeats the claim and adds a "VIRTUAL Lab dedicated to PYTHON Programming" with IIT Kanpur [7].
- **The R&D pages are empty.** `psit.ac.in/research_and_innovation/research_center` renders as navigation plus footer — 1,015 characters, no labs, no equipment, no projects [8]; "Research Publications" and "Patent Published" are `javascript:void(0)`.
- **PSIT CHE's BCA page** describes the department (formed 2015, intake 240) and syllabus, and lists **no faculty, no labs, no research** [9].

### 3.3 Where the two lists do and do not overlap

**Measured:** five people named on the public lab, centre or IDEA Lab pages also appear in the 168 records, and each overlap is administrative rather than methodological. Dr Nand Kishore Sharma (HOD CSE, IDEA Lab co-coordinator) appears once in the data, on a drug-drug-interaction review. Dr Raghuraj Singh Suryavanshi (Additional Director) appears on two pharmacy-side reviews; Dr Man Mohan Shukla on three under that spelling and three more as "Manmohan Shukla". Mr Ankit Jain and Mr Ritesh Dixit, both IDEA Lab "Tech Gurus", each appear as AI authors (smart agriculture; ANN for 3D-printed composites).

**Measured:** the four most prolific AI authors — Chaurasia (~14), Ankita Wal (10), Pranay Wal (9), Rajat Verma (7) — appear on none of the public lab, centre or IDEA Lab pages I loaded. Chaurasia is named on PSIT conference committees as CSE faculty [16]; a search snippet called him "Dean-R&I", which I could not confirm on any page I loaded (`UNCERTAIN`). The Wals have 19 AI papers between them and are never mentioned on PSIT's AI or labs pages. **Interpretation:** the non-overlap is the finding — a student reading only psit.ac.in would come away thinking PSIT's AI people are the IDEA Lab staff, while the publication record points elsewhere. That reading rests on the few pages I loaded, not on a complete site search.

## 4. Strengths

1. **AI output is growing and is a fifth of everything PSIT publishes.** 168 of 793 (21.2%); AI share by year rises from 4.2% (2019) to 24.0% (2022), 28.4% (2023), 26.5% (2026). Counts: 1, 6, 12, 21, 33, 33, 62 for 2019, 2021-2026.
2. **A domain adjacency: pharmacy plus computation.** 58 AI records touch clinical medicine, 14 drug delivery, with pharmacy authors who publish repeatedly (A. Wal 10, P. Wal 9). **Interpretation:** few Indian engineering colleges sit beside a pharmacy school producing AI-adjacent work at this rate — I did not compare against other institutes, so this is an impression from the dataset, not a benchmark.
3. **Some work reaches respectable general venues.** 5 in Scientific Reports, 3 in Expert Systems (a real AI journal [12]), 1 each in Medical & Biological Engineering & Computing and Journal of Critical Care — indexed, international, peer-reviewed. The 2 Multimedia Tools and Applications records are one paper and its retraction notice (2024, 2026 — §2.4), so they are not evidence of output.
4. **A visible teaching pipeline into AI.** Three AI-named B.Tech programmes [3][4], a 960-strong CSE intake, an IDEA Lab with student ambassadors [5], a documented AI/ML centre partnership [6][7].
5. **PSIT runs its own conferences.** ICNGTSE 2025 and 2026 [16], EACE, with named technical and publication committees — a low-friction route to a first paper, subject to gap 1.

## 5. Gaps

1. **No named AI venue in the recorded venue field — 0 of 168, by a scoped name match.** The earlier draft said "none of 168" without saying what was matched or what the method would miss, so here are the four parts a reader needs to check it.
   - **Denominator.** The 168 records with `ai_related=='yes'` in `01_psit_data/papers.csv`, retrieved 2026-11-03. They carry 119 distinct venue strings; 9 records have no venue recorded.
   - **Method.** A case-insensitive, whole-token regex name match on the `venue` field against 21 names: ACL, NeurIPS, NIPS, ICML, CVPR, AAAI, EMNLP, ICLR, KDD, SIGIR, IJCAI, ICCV, ECCV, NAACL, WSDM, CIKM, TKDE, TNNLS, Pattern Recognition, Neural Networks, Expert Systems with Applications. It is one line of Python, run from the repo root, printing `168 0` (appendix). Whole-token matching means a substring such as the "nips" inside "snips" cannot count as a hit.
   - **Result.** 0 of 168 match. A match over titles as well as venues returns 4 hits, all of them the generic phrase "neural networks" inside a title (including the retraction note in §2.4), which is why the check is restricted to the venue field.
   - **What the method cannot see.** It matches a deposited string, not a publisher page. A paper in an unnamed workshop of a NeurIPS/ACL-class conference, a venue abbreviated in a non-standard way ("Proc. 41st Int. Conf. on Machine Learning"), or a series renamed after deposit would be missed. The dataset is itself a Crossref/Europe PMC/PubMed union (509 Crossref-only, 181 Crossref+Europe PMC+PubMed, 98 Europe PMC+PubMed, 4 Europe PMC, 1 PubMed), not a census of PSIT output. The claim this supports is "0 in this dataset", not "0 at PSIT".
   - The venue in the list with the clearest AI remit is Expert Systems (Wiley), 3 records [12]; the rest of the top 15 are domain journals, book series or broad conferences (§2.3).
2. **Citation counts are low, and the zeros are mostly recent.** AI subset: mean 5.56, median 0.5, 75th percentile 4, 90th 17, maximum 76; **84 of 168 (50%) have zero citations** — against mean 6.91 and median 1 for all 793. Split by year: 57 of the 62 records dated 2026 have none (91.9%), 17 of 33 in 2025 (51.5%), but only 8 of the 54 dated 2023-24 (14.8%) — where the median is 3 citations and the mean 7.94. **Interpretation:** the headline 50% is largely an age effect rather than a quality signal; the earlier draft's claim that "the 2023-24 AI papers show the same pattern" was wrong, and is withdrawn.
3. **Evaluation markers are rare in abstracts; the papers themselves were not read.** Counts over the 108 records whose abstract is at least 200 characters: 3 mention a baseline, 2 an ablation, 2 a significance test ("statistically significant" or "p-value"), 1 a standard deviation or "±", 5 cross-validation, 0 a random seed, 0 a confidence interval. 7 of the 108 (6.5%) contain any of the five markers (baseline, seed, spread, significance test, ablation). 59 of 168 records (35%) have no abstract at all, so every count is a floor over the 64% that do. Script `scripts/ai_abstract_audit.py`, output `raw/ai_abstract_audit.json`.
   **Interpretation:** these counts are consistent with abstracts that leave evaluation detail out, and they do not establish that the papers omit it. An abstract is a lossy summary — a paper can fix its seeds and report spreads in the methods section without either word reaching the abstract. What the count settles is what the abstracts say; settling the papers needs the PDFs, and this page opened none. For context, 18 of 168 titles (10.7%) name an optimiser ("Falcon", "Fennec Fox", "PSO-GA-Bayesian", "golden jackal") around an otherwise standard classifier — whether those papers report seeds or baselines is not something this record can show.
4. **Domain applications, not methods — from titles and abstracts only.** Medicine/clinical (58 records) and pharmacy (14) outnumber computer vision (3) and NLP (11) several times over; 53 records carry only the `machine-learning` tag. **Interpretation:** I saw no title among the 168 that announces a new architecture, loss function, released dataset or benchmark, and the ten titles read in §2.4 fit the five genres listed there. That is a reading of titles and abstracts; a full-text pass could overturn it.
5. **No public information on compute, datasets or equipment.** The R&D page has no content [8]; department pages promise "advanced laboratories with the latest software and hardware tools" and specify nothing [3]; the AI/ML MoU is about training fees, not infrastructure [6]. A text search of the cached Self Study Report (95 pages, extracted with `pdftotext -layout`) returns 0 hits for "GPU", "NVIDIA", "HPC", "supercomputer" and "graphics processing"; "cluster" occurs twice, both times for adopted villages under Unnat Bharat Abhiyaan, not for machines [7]. A student cannot tell whether one GPU exists. `UNAVAILABLE`: internal inventory — per RULES.md an email question, not an inference.
6. **Public research information is close to unusable.** Profiles without years or DOIs [2], a department page naming no faculty [3], a directory whose data endpoint refuses requests [1], a BCA page with no research [9]. A collaborator cannot answer "who works on what" from the institute's own site.

## 6. Where could a student contribute

*Three shapes. Each assumes a supervisor's name on the paper and a novelty check before you start.*

### Shape (i) — Replicate one PSIT applied-ML paper, with seeds and baselines

**What.** Take one medical-imaging classifier, re-run it on the same public data, and report what the original did not: five seeds, mean ± standard deviation, two baselines (logistic regression on flattened features; an off-the-shelf pretrained CNN with no optimiser), a patient-level split.

**Target.** The diabetic-retinopathy line is cleanest: "Transfer learning-driven ensemble model for detection of diabetic retinopathy" (Medical & Biological Engineering & Computing, 2023, 8 citations — the most-cited AI paper here) and the 2026 Scientific Reports follow-up with a "Falcon Optimizer" ensemble. Both use retinal fundus images, with public data available (APTOS 2019, EyePACS on Kaggle).

**Why PSIT's output makes it feasible.** Standard transfer learning plus ensembling; nothing exotic to rebuild. The opening is visible in the abstracts: 0 of 108 audited abstracts mention a seed and 3 a baseline (§5.3) — a fact about abstracts, so check both PDFs before promising a correction. **Interpretation:** reporting variance and baselines is the kind of corrective result a workshop can accept even when the numbers come out worse.

**What it takes.** 6-10 weeks: licence, a script with fixed seeds, one GPU-week at most (free Colab or Kaggle is enough at 224×224), and honesty about what "replication" means without the original code.

**What makes it not worth doing.** If the original publishes code and a full results table, nothing needs correcting. If the licence forbids redistribution, your replication cannot be checked. If you cannot confirm preprocessing, it is a comparison study — frame it that way or drop it.

### Shape (ii) — A small benchmark on an Indian-context task

**What.** Take a task where PSIT published single-point results and turn it into an evaluation: several methods, one fixed split, error analysis by subgroup.

**(a) Kanpur air quality.** "Air quality assessment using geospatial technique and ANN analysis for an urban city, Uttar Pradesh" (2026) uses "eight years of monthly air quality data (2011-2018) from five monitoring stations". That data is public (CPCB, UPPCB). Compare the ANN against gradient boosting and a seasonal-naive baseline, forecast rather than interpolate (train 2011-2016, test 2017-2018), report per-station errors.

**(b) Phishing-URL detection with minimal features.** "Efficient Phishing URL Detection Using Minimal-Feature Machine Learning Models" (GTSS 2026); public datasets exist (PhishTank, UCI). The question is not "can a model do it" but "how few features before it breaks, and does that hold across datasets".

**Why PSIT's output makes it feasible.** Both papers show faculty care about the problem and will supervise; both use data obtainable without an institutional agreement. They supply domain judgement; you supply evaluation discipline.

**What it takes.** 8-12 weeks, no GPU; cleaning Indian government portal data (missing months, renamed stations) is most of the work.

**What makes it not worth doing.** If the Indian-context benchmark already exists, you are duplicating. If the data cannot be redistributed, nobody can reproduce your split. If the task is saturated at 99%, a better number means nothing.

### Shape (iii) — A dataset paper from public Indian sources

**What.** Build, document and release a resource nobody has: a datasheet, a licence, a baseline, a documented collection process.

**Best fit given PSIT's strengths.** The pharmacy group publishes drug-drug-interaction and pharmacovigilance work (rows 6, 9, 30, 35; 10 records tagged pharmacology-toxicology). Build an **Indian-brand drug-interaction corpus**: map Indian market brand names (public CDSCO and NPPA listings) to generic ingredients, and pair them with interaction labels from openFDA labels. The question: do existing DDI models fail on Indian brand names, where brand-to-generic mapping is ambiguous?

**Why PSIT's output makes it feasible.** PSIT has pharmacists who can validate the mapping — the scarce part — and CSE faculty who can run the baseline. Few undergraduate projects have both sides on one campus.

**What it takes.** 3-4 months, most of it not modelling: licensing, deduplication, a labelling protocol with two annotators and an agreement score.

**What makes it not worth doing.** If you cannot redistribute the labels, it is not a dataset paper. If two annotators cannot agree above roughly 80% on a 200-item pilot, the labels are too subjective — stop rather than ship noise. If a comparable resource exists, contribute to it instead.

### Who to talk to

Start with your own department (BCA at PSIT CHE) and ask for a referral into CSE/IT: Dr Nand Kishore Sharma (HOD CSE), Dr Raghuraj Singh Suryavanshi (Additional Director, IDEA Lab coordinator), or Prof. Brijesh Kumar Chaurasia, the most prolific AI author in the dataset. For shape (iii), Prof. Ankita Wal and Prof. Pranay Wal on the pharmacy side. Bring one printed page: the specific paper, the number you want to reproduce, the dataset you already downloaded. That is a much easier yes than "I want to do research".

## Appendix: reproduce the two numbers

Both commands run from the repo root against `papers.csv` as retrieved 2026-11-03.

**Venue name match** — prints `168 0` (records checked, records matched):

```bash
python -c "import csv,re;r=[x for x in csv.DictReader(open('01_psit_data/papers.csv',encoding='utf-8')) if x['ai_related']=='yes'];p=re.compile(r'(?<![A-Za-z0-9])(ACL|NeurIPS|NIPS|ICML|CVPR|AAAI|EMNLP|ICLR|KDD|SIGIR|IJCAI|ICCV|ECCV|NAACL|WSDM|CIKM|TKDE|TNNLS|Pattern Recognition|Neural Networks|Expert Systems with Applications)(?![A-Za-z0-9])',re.I);print(len(r),sum(1 for x in r if p.search(x['venue'])))"
```

**Abstract audit** — prints the counts quoted in §2.4 and §5.3 and writes `01_psit_data/raw/ai_abstract_audit.json`:

```bash
python 01_psit_data/scripts/ai_abstract_audit.py
```

Its output should include `subset: 168 of 793 records`, `venue name matches: 0 of 168 records` and `abstracts audited (>= 200 chars): 108 of 168`.

## Sources

1. PSIT Kanpur, *Faculty* directory — https://www.psit.ac.in/academics/faculty — retrieved 2026-11-03.
2. PSIT Kanpur, *Faculty Profile: Subhash Singh Parihar* — https://www.psit.ac.in/academics/profile/4037/Subhash-Singh-Parihar — retrieved 2026-11-03.
3. PSIT Kanpur, *B.Tech CSE (Artificial Intelligence), About Department* — https://www.psit.ac.in/academics/eb2/computer-science-and-engineering/1 — retrieved 2026-11-03.
4. PSIT Kanpur, *B.Tech CSE (Data Science)* — https://www.psit.ac.in/academics/eb2/computer-science-and-engineering/3 — retrieved 2026-11-03.
5. PSIT AICTE IDEA Lab, *Operational and Management Personnel* — https://www.psit.ac.in/aicteidealab/operational_and_management_personnel.php — retrieved 2026-11-03.
6. PSIT, *Memorandum of Understanding to Establish a Center of Excellence for AI/ML* (PSIT, The Ikigai Lab, Pingala AI Pvt Ltd), 6 July 2021 — https://www.psit.ac.in/QIF/cr3/3.5.1/Data/Memorandum-of-understanding/6_Ikgai%20lab%20MoU.pdf — retrieved 2026-11-03.
7. PSIT, *Self Study Report* — https://www.psit.ac.in/QIF/ssr/ssr.pdf — retrieved 2026-11-03.
8. PSIT Kanpur, *Research and Innovation: Research Center* — https://www.psit.ac.in/research_and_innovation/research_center — retrieved 2026-11-03 (renders as navigation only).
9. PSIT College of Higher Education, *Department of Computer Applications (BCA)* — https://psitche.ac.in/bca.php?title=about-department — retrieved 2026-11-03.
10. De Gruyter Brill, *Journal of Optical Communications* — https://www.degruyterbrill.com/journal/key/joc/html — retrieved 2026-11-03.
11. MDPI, *Diagnostics — Aims & Scope* — https://www.mdpi.com/journal/diagnostics/about — retrieved 2026-11-03.
12. Wiley, *Expert Systems: The Journal of Knowledge Engineering — Overview* — https://onlinelibrary.wiley.com/page/journal/14680394/homepage/productinformation.html — retrieved 2026-11-03.
13. Nature Portfolio, *About Scientific Reports* — https://www.nature.com/srep/about — retrieved 2026-11-03.
14. ISSN Portal, *Advances in Computational Intelligence and Robotics book series* (ISSN 2327-0411) — https://portal.issn.org/resource/ISSN/2327-0411 — retrieved 2026-11-03.
15. proceedings.com, *IC-AIDA 2026, Bangalore, 10-11 April 2026 — table of contents* — https://www.proceedings.com/content/086/086317webtoc.pdf — retrieved 2026-11-03.
16. PSIT Kanpur, *ICNGTSE-II 2026 — committee* — https://www.psit.ac.in/icngtse_2026/ — retrieved 2026-11-03.

Dataset: `01_psit_data/papers.csv` (793 records; Crossref 509, Crossref+Europe PMC+PubMed 181, Europe PMC+PubMed 98, Europe PMC 4, PubMed 1). All counts from `01_psit_data/scripts/ai_subset_tables.py`, which writes `table_ai_recent40.csv`, `table_ai_topics.csv`, `table_ai_authors.csv`, `table_ai_venues.csv`; the venue match and abstract counts come from `01_psit_data/scripts/ai_abstract_audit.py`, which writes `01_psit_data/raw/ai_abstract_audit.json`.

## How confident is this?

- **Solid.** The 168/793 count, year and venue distributions, author counts, topic tags and citation statistics are arithmetic over `papers.csv` and reproduce exactly with the scripts. The 0-of-168 venue result is a whole-token name match over the `venue` field and reproduces with the one-line command in the appendix.
- **Solid.** The public-page facts (IDEA Lab personnel, the 2021 AI/ML MoU, the empty R&D page, the AI degree programmes, the profile with no DOIs) were each loaded and read on 2026-11-03 and are quoted from those pages.
- **Weak, flagged in place.** The abstract counts describe 108 abstracts, not 168 papers: 59 records have no abstract, an abstract is a lossy summary, and no full text was read. The numbers and the year split of zero citations are in `raw/ai_abstract_audit.json`.
- **UNCERTAIN.** Whether the CSE faculty directory is as incomplete as the one profile I opened — the per-department endpoint answered "Access Denied", so I read one department (Mechanical) and one profile.
- **UNCERTAIN.** Prof. Chaurasia's title. Search snippets say "Dean-R&I"; the pages I loaded name him only as CSE faculty on conference committees [16].
- **UNCERTAIN.** The title/abstract mismatch on row 34. Either the metadata or the abstract is wrong; I did not open the publisher page.
- **Scope limit.** The 0-of-168 venue result describes this dataset, not PSIT. The dataset is a Crossref/Europe PMC/PubMed union and matches venue strings only, so an unnamed workshop paper or an unusually abbreviated venue would be missed (§5.1).
- **Not covered.** Internal lab inventory, GPU availability, funded AI projects, papers under review — none is public, and per RULES.md must come from the R&D cell by email, not inference.

last_updated: 2026-11-03
