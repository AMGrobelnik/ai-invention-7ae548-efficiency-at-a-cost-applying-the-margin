# upd_hypo — test_idea

> Phase: `invention_loop` · round 1 · `upd_hypo`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 16:24:55 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Foraging-Based Section Switching for Scientific RAG
hypothesis: >-
  The Marginal Value Theorem (MVT) from ecological foraging theory provides a principled, parameter-free criterion for adaptive
  section switching in retrieval-augmented generation over long scientific documents. Specifically: modeling document sections
  (introduction, methods, results, discussion) as forageable 'patches' and measuring marginal semantic information gain per
  retrieved chunk, the MVT predicts that a retriever should abandon a section and move to the most promising unvisited section
  exactly when the marginal gain within the current section falls to the document-wide average marginal gain. We hypothesize
  that this ecologically-grounded switching criterion outperforms fixed-k retrieval, confidence-threshold stopping, and MDP-based
  adaptive stopping on scientific multi-hop QA benchmarks, because it naturally calibrates exploitation depth to each section's
  actual information density while ensuring global coverage proportional to the document's heterogeneous structure.
motivation: >-
  Long scientific documents present a core structural challenge for RAG: relevant evidence is distributed heterogeneously
  across sections with very different information densities (e.g., a dense results section vs. a sparse introduction). Existing
  adaptive RAG methods (FLARE, Stop-RAG, IRCoT) determine *whether* to retrieve more but not *which section* to retrieve from
  next. Hierarchy-aware methods (HIRAG, KohakuRAG) structure retrieval but use similarity scores or heuristics, not principled
  criteria for section transitions. The MVT, developed in 1976 to explain animal foraging behavior, gives an exact, analytically-derived
  switching rule that has been validated across hundreds of biological systems: leave a depleting patch when its current return
  rate equals the environment average. This rule is parameter-free given a baseline estimate, adapts automatically to document
  content, and directly solves the section-switching problem. If it applies, it would give a theoretically grounded alternative
  to black-box RL controllers or hand-tuned thresholds, while being interpretable and computationally lightweight.
assumptions:
- >-
  Scientific documents have section-level structure (intro/methods/results/discussion or similar) that can be reliably detected
  from headers or document metadata, and sections constitute meaningfully distinct 'information patches' with different densities
  of query-relevant content.
- >-
  Marginal semantic information gain within a section is monotonically non-increasing as more chunks are retrieved (diminishing
  returns), a structural property borrowed from foraging theory's assumption of depleting patches.
- >-
  The document-wide average marginal gain—estimated from an initial lightweight pass (e.g., top-1 similarity per section)—serves
  as a stable enough baseline to apply the MVT switching criterion, even though the forager is simultaneously depleting the
  environment.
- >-
  Semantic novelty of a chunk relative to already-retrieved context (approximated as 1 minus maximum cosine similarity to
  any retrieved chunk, weighted by query relevance) is a usable proxy for the 'energy intake rate' in the MVT.
- >-
  The answer to a scientific query is typically distributed across 2-4 sections, making section-switching a meaningful degree
  of freedom (as opposed to queries answerable from a single sentence).
investigation_approach: >-
  1. DATASETS: Use QASPER (full-paper scientific QA with section annotations) and LongBench subset (scientific tasks). These
  are freely available on HuggingFace and have ground-truth evidence locations. 2. SECTION DETECTION: Parse sections using
  regex on headers (##, bold lines, standard section names). 3. CHUNK EMBEDDING: Encode all chunks using sentence-transformers
  (all-MiniLM-L6-v2 on CPU). 4. MVT-RAG ALGORITHM: (a) Estimate environment average G_env by computing the similarity of the
  best matching chunk per section to the query, averaged across sections. (b) For the most promising unvisited section, retrieve
  chunks iteratively; compute marginal gain G_t = sim(chunk_t, query) × (1 - max_sim(chunk_t, already_retrieved)). (c) When
  G_t < G_env, switch to the next highest-potential unvisited section. (d) Terminate when all sections are either exhausted
  or have been switched from. 5. ANSWER GENERATION: Pass retrieved chunks as context to an LLM via OpenRouter (e.g., Llama-3-8B-instruct)
  to generate answers. 6. BASELINES: (a) Top-k dense retrieval (k=3,5,10), (b) FLARE-style confidence stopping, (c) BM25+fixed-k,
  (d) no-RAG baseline. 7. METRICS: Exact match, token-level F1, and retrieval efficiency (chunks retrieved per question).
  Statistical tests using paired bootstrap.
success_criteria: >-
  CONFIRM: MVT-RAG achieves statistically significantly higher F1 (p < 0.05 via bootstrap) than fixed-k dense retrieval on
  QASPER, while retrieving fewer average chunks per question (efficiency gain). Ideally, MVT-RAG is competitive with or beats
  confidence-based adaptive stopping. Secondary: ablation showing that removing the environment-average baseline (replacing
  MVT with a fixed threshold) degrades performance, confirming the ecology-derived averaging mechanism is load-bearing. DISCONFIRM:
  If MVT-RAG performs at or below fixed-k retrieval across all k values, the diminishing-returns assumption fails (sections
  are not meaningful patches) or the marginal gain proxy is too noisy for the MVT signal to be usable. Partial: If MVT-RAG
  helps only for multi-hop questions (≥2 sections required), that scopes the finding to multi-hop scientific QA specifically.
related_works:
- >-
  InForage (arxiv 2505.09316, 2025): Uses Information Foraging Theory + reinforcement learning to train a search controller
  for multi-source web retrieval. Key difference: InForage models multi-source search across independent documents using RL;
  our approach applies the specific Marginal Value Theorem (an exact optimality criterion, not a learned policy) to intra-document
  section switching within a single long scientific paper—no training required.
- >-
  Stop-RAG (arxiv 2510.14337, 2025): Models iterative retrieval stopping as a finite-horizon MDP, learning a value function
  for 'continue vs. stop.' Key difference: Stop-RAG decides whether to retrieve more globally; MVT-RAG decides which section
  to switch to and when, using an analytically derived (not learned) switching criterion grounded in patch foraging ecology.
- >-
  FLARE (Sun et al. 2023): Uses token-level generation probability to trigger retrieval when the model is uncertain. Key difference:
  FLARE asks 'should I retrieve now?' using LLM confidence; MVT-RAG asks 'which section should I switch to?' using informativeness
  of previously retrieved chunks relative to the document-wide baseline—a structurally different decision.
- >-
  HIRAG / KohakuRAG (2025): Hierarchical RAG methods that organize documents into tree structures and traverse them via LLM-guided
  node selection. Key difference: hierarchy methods use similarity-based greedy selection at each level; MVT-RAG uses a physics-motivated
  rate-comparison criterion for section transitions, requiring no LLM calls during the retrieval phase.
- >-
  Optimal Foraging in Memory Retrieval (arxiv 2511.12759, 2025): Applies MVT to model human semantic memory retrieval (animal-naming
  fluency task) using random walks and Metropolis-Hastings sampling. Key difference: that work models human cognition over
  semantic spaces; our work applies MVT operationally to an engineering system (RAG) with concrete text chunks, document sections
  as patches, and measurable downstream QA performance.
inspiration: >-
  The Marginal Value Theorem (Charnov 1976) is one of the most predictively successful quantitative models in behavioral ecology:
  it predicts that an optimal forager leaves a depleting resource patch exactly when the marginal return rate equals the environment-average
  rate. This rule has been validated in hundreds of animal species and extended to human information search behavior (Pirolli's
  Information Foraging Theory). The key cross-domain insight is structural: scientific documents have the same mathematical
  structure as a patchy foraging environment—heterogeneous section-level information densities, diminishing returns within
  a section, and a switching cost (re-orienting the query context). The MVT's elegance is that it makes a specific, testable,
  parameter-free prediction once you specify what 'energy' (information gain) and 'patch' (document section) mean. No existing
  RAG method uses this ecology-derived optimality criterion for section switching, even though the problem structure it was
  designed to solve maps precisely onto the multi-section retrieval problem.
terms:
- term: Marginal Value Theorem (MVT)
  definition: >-
    A mathematical optimality model from ecology (Charnov 1976) predicting that an optimal forager should leave a resource
    patch when the current marginal return rate within that patch equals the average return rate across the entire foraging
    environment. Requires no tunable threshold parameter—the baseline is derived from the environment itself.
- term: Information patch
  definition: >-
    In this context, a section of a scientific document (e.g., Introduction, Methods, Results, Discussion) treated as an ecological
    foraging patch: a spatially cohesive region containing resources (query-relevant information) that are depleted as the
    retriever extracts chunks.
- term: Marginal information gain
  definition: >-
    The incremental semantic novelty contributed by the next retrieved chunk, defined as the query-relevance score of the
    chunk multiplied by (1 minus its maximum cosine similarity to any already-retrieved chunk). Approximates the 'energy intake
    rate' in the MVT.
- term: Environment-average gain (G_env)
  definition: >-
    The document-wide baseline marginal gain rate, estimated as the average of the best-matching chunk similarity score across
    all sections. This serves as the MVT threshold: switch sections when current marginal gain falls below G_env.
- term: Retrieval efficiency
  definition: >-
    Chunks retrieved per correct answer—a key secondary metric capturing the practical benefit of adaptive stopping. MVT-RAG
    is hypothesized to achieve the same or better answer quality as fixed-k retrieval while using fewer chunks on average.
summary: >-
  We propose applying the Marginal Value Theorem from ecological foraging to long scientific document RAG: model each document
  section as a 'foraging patch' and switch sections when the marginal semantic information gain within the current section
  drops to the document-wide average—an analytically derived, parameter-free criterion. This ecologically-grounded switching
  rule addresses the core limitation of current adaptive RAG methods, which decide whether to retrieve more but not which
  section to retrieve from next, and is hypothesized to improve multi-hop scientific QA accuracy while reducing retrieval
  overhead compared to fixed-k and confidence-based baselines.
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_jHUX0qukOYMI
type: dataset
title: QASPER Scientific QA with Section Chunks
summary: >-
  This artifact prepares the QASPER dataset (allenai/qasper, Dasigi et al. 2021 NAACL) for MVT-RAG evaluation on long scientific
  documents. QASPER contains 888 NLP papers with full text, 8,000+ question-answer pairs, and annotated evidence paragraphs.
  Processing steps: (1) Download train (888 papers) and validation (281 papers) splits from HuggingFace. (2) Parse each paper's
  full_text into section-level chunks using the columnar section_name/paragraphs schema; normalize section names to IMRaD
  categories (introduction, methods, results, discussion, related_work, other, preamble). (3) Filter to papers with >=3 distinct
  normalized section categories (776 of 888 train, 265 of 281 validation pass). (4) Match evidence paragraph strings to chunk
  IDs via substring overlap >=0.5. (5) Filter to answerable questions with >=1 matched evidence chunk. (6) Sample 2000 questions
  stratified by is_multihop flag (153 multihop, 1847 single-hop). Output schema per example: input=JSON string with question,
  paper_id, sections summary; output=JSON string with gold_answer, evidence_chunk_ids, evidence_section_names. Metadata fields:
  metadata_fold (0=train, 1=validation), metadata_paper_id, metadata_question_id, metadata_is_multihop, metadata_num_sections,
  metadata_split, metadata_evidence_count, metadata_task_type=rag_qa. The dataset enables evaluation of section-aware retrieval
  and multi-hop reasoning across paper sections. full_data_out.json: 2000 examples, 3.1MB, schema-validated against exp_sel_data_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_yFawqoDZbtm3
type: experiment
title: MVT-RAG vs Baselines on QASPER Scientific QA
summary: >-
  Implemented and evaluated MVT-RAG (Marginal Value Theorem-based adaptive section switching) against 8 baselines on the QASPER
  scientific QA dataset (100 papers, 223 questions). MVT-RAG uses an ecology-derived stopping criterion: it estimates the
  average information yield across all document sections (G_env) and stops retrieving from the current section when the marginal
  gain (relevance × novelty) drops below this environmental average, then switches to the next most promising section. Baselines:
  top-k dense retrieval (k=3,5,10), BM25 (k=5), confidence-threshold retrieval (0.3, 0.5), MVT-NoEnv ablation (fixed threshold=0.5
  instead of adaptive G_env), and no-RAG. Results on 100 QASPER validation papers (n=223 answerable questions): MVT-RAG F1=0.122
  (1.3 chunks/question), MVT-NoEnv F1=0.119 (1.0 chunks), topk_3 F1=0.165 (3 chunks), topk_5 F1=0.190 (5 chunks), topk_10
  F1=0.203 (10 chunks), BM25-5 F1=0.178 (5 chunks), thresh_0.3 F1=0.175 (8.8 chunks), thresh_0.5 F1=0.148 (2.4 chunks), no_rag
  F1=0.061. Oracle retrieval F1 (span recall): MVT-RAG=0.140, topk_5=0.441, topk_10=0.596. MVT-RAG retrieves far fewer chunks
  (1.3 vs 5) but achieves lower F1, indicating the current G_env threshold is too aggressive in stopping—it under-retrieves
  relative to what the LLM needs. Bootstrap p-values show MVT-RAG is significantly worse than topk_5 (p=1.00). The MVT-NoEnv
  ablation performs similarly to MVT-RAG (F1=0.119 vs 0.122), suggesting the ecology-derived G_env averaging provides minimal
  additional benefit over a fixed threshold at these scales. Key findings: (1) the MVT framework successfully controls retrieval
  budget (1.3 chunks vs 5-10 for baselines), (2) but the efficiency gain comes at a large quality cost, (3) the section-switching
  heuristic does not improve over the ablation, pointing to G_env estimation as the weakest component. LLM: meta-llama/llama-3.1-8b-instruct
  via OpenRouter. Embeddings: all-MiniLM-L6-v2. Total cost: ~$0.40.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 3 ---
id: art_wdAfUesLipEx
type: evaluation
title: 'MVT-RAG vs Baselines: F1 and Retrieval Efficiency'
summary: |-
  Evaluation of MVT-RAG (Marginal Value Theorem-based adaptive retrieval) versus six baselines on the QASPER scientific QA validation set (281 papers). Metrics: token-level F1 (QASPER canonical metric), exact match (EM), retrieval efficiency (chunks/question), 10k paired bootstrap 95% CI and p-values for MVT-RAG vs each baseline, G_env ablation delta (MVT-RAG vs MVT-NoEnv with fixed threshold), and stratified analysis by single-hop vs multi-hop questions.

  Methods evaluated: mvt_rag, mvt_noenv (ablation with fixed threshold=0.3), topk_3, topk_5, topk_10, bm25_5, flare (confidence-threshold style), no_rag. LLM: meta-llama/llama-3.1-8b-instruct via OpenRouter. Embeddings: all-MiniLM-L6-v2.

  Key findings (full run over 281 QASPER validation papers): MVT-RAG achieves strong retrieval efficiency (mean ~1-2 chunks/question vs 5 for top-k-5), confirming the stopping criterion aggressively prunes low-marginal-gain chunks. The G_env ablation shows the ecology-derived environment average is not clearly load-bearing over a fixed threshold (CI includes 0), suggesting the stopping rule's efficiency gain is real but its theoretical ecological framing may not uniquely drive performance. Multi-hop stratification reveals MVT-RAG's per-section traversal approach retrieves fewer chunks in both single-hop and multi-hop settings. Verdict: PARTIAL — efficiency claim confirmed, but F1 advantage over top-k baselines is not statistically significant (bootstrap CI spans zero for most comparisons), and G_env ablation CI does not exclude zero.

  Output files: eval_out.json (per-question results with predict_* and eval_* fields for all 8 methods, bootstrap results, stratified analysis, metadata); full/mini/preview variants generated via aii-json format script. Schema validated against exp_eval_sol_out.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

id: art_jHUX0qukOYMI
type: dataset
title: QASPER Scientific QA with Section Chunks
summary: >-
  This artifact prepares the QASPER dataset (allenai/qasper, Dasigi et al. 2021 NAACL) for MVT-RAG evaluation on long scientific
  documents. QASPER contains 888 NLP papers with full text, 8,000+ question-answer pairs, and annotated evidence paragraphs.
  Processing steps: (1) Download train (888 papers) and validation (281 papers) splits from HuggingFace. (2) Parse each paper's
  full_text into section-level chunks using the columnar section_name/paragraphs schema; normalize section names to IMRaD
  categories (introduction, methods, results, discussion, related_work, other, preamble). (3) Filter to papers with >=3 distinct
  normalized section categories (776 of 888 train, 265 of 281 validation pass). (4) Match evidence paragraph strings to chunk
  IDs via substring overlap >=0.5. (5) Filter to answerable questions with >=1 matched evidence chunk. (6) Sample 2000 questions
  stratified by is_multihop flag (153 multihop, 1847 single-hop). Output schema per example: input=JSON string with question,
  paper_id, sections summary; output=JSON string with gold_answer, evidence_chunk_ids, evidence_section_names. Metadata fields:
  metadata_fold (0=train, 1=validation), metadata_paper_id, metadata_question_id, metadata_is_multihop, metadata_num_sections,
  metadata_split, metadata_evidence_count, metadata_task_type=rag_qa. The dataset enables evaluation of section-aware retrieval
  and multi-hop reasoning across paper sections. full_data_out.json: 2000 examples, 3.1MB, schema-validated against exp_sel_data_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

id: art_yFawqoDZbtm3
type: experiment
title: MVT-RAG vs Baselines on QASPER Scientific QA
summary: >-
  Implemented and evaluated MVT-RAG (Marginal Value Theorem-based adaptive section switching) against 8 baselines on the QASPER
  scientific QA dataset (100 papers, 223 questions). MVT-RAG uses an ecology-derived stopping criterion: it estimates the
  average information yield across all document sections (G_env) and stops retrieving from the current section when the marginal
  gain (relevance × novelty) drops below this environmental average, then switches to the next most promising section. Baselines:
  top-k dense retrieval (k=3,5,10), BM25 (k=5), confidence-threshold retrieval (0.3, 0.5), MVT-NoEnv ablation (fixed threshold=0.5
  instead of adaptive G_env), and no-RAG. Results on 100 QASPER validation papers (n=223 answerable questions): MVT-RAG F1=0.122
  (1.3 chunks/question), MVT-NoEnv F1=0.119 (1.0 chunks), topk_3 F1=0.165 (3 chunks), topk_5 F1=0.190 (5 chunks), topk_10
  F1=0.203 (10 chunks), BM25-5 F1=0.178 (5 chunks), thresh_0.3 F1=0.175 (8.8 chunks), thresh_0.5 F1=0.148 (2.4 chunks), no_rag
  F1=0.061. Oracle retrieval F1 (span recall): MVT-RAG=0.140, topk_5=0.441, topk_10=0.596. MVT-RAG retrieves far fewer chunks
  (1.3 vs 5) but achieves lower F1, indicating the current G_env threshold is too aggressive in stopping—it under-retrieves
  relative to what the LLM needs. Bootstrap p-values show MVT-RAG is significantly worse than topk_5 (p=1.00). The MVT-NoEnv
  ablation performs similarly to MVT-RAG (F1=0.119 vs 0.122), suggesting the ecology-derived G_env averaging provides minimal
  additional benefit over a fixed threshold at these scales. Key findings: (1) the MVT framework successfully controls retrieval
  budget (1.3 chunks vs 5-10 for baselines), (2) but the efficiency gain comes at a large quality cost, (3) the section-switching
  heuristic does not improve over the ablation, pointing to G_env estimation as the weakest component. LLM: meta-llama/llama-3.1-8b-instruct
  via OpenRouter. Embeddings: all-MiniLM-L6-v2. Total cost: ~$0.40.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_wdAfUesLipEx
type: evaluation
title: 'MVT-RAG vs Baselines: F1 and Retrieval Efficiency'
summary: |-
  Evaluation of MVT-RAG (Marginal Value Theorem-based adaptive retrieval) versus six baselines on the QASPER scientific QA validation set (281 papers). Metrics: token-level F1 (QASPER canonical metric), exact match (EM), retrieval efficiency (chunks/question), 10k paired bootstrap 95% CI and p-values for MVT-RAG vs each baseline, G_env ablation delta (MVT-RAG vs MVT-NoEnv with fixed threshold), and stratified analysis by single-hop vs multi-hop questions.

  Methods evaluated: mvt_rag, mvt_noenv (ablation with fixed threshold=0.3), topk_3, topk_5, topk_10, bm25_5, flare (confidence-threshold style), no_rag. LLM: meta-llama/llama-3.1-8b-instruct via OpenRouter. Embeddings: all-MiniLM-L6-v2.

  Key findings (full run over 281 QASPER validation papers): MVT-RAG achieves strong retrieval efficiency (mean ~1-2 chunks/question vs 5 for top-k-5), confirming the stopping criterion aggressively prunes low-marginal-gain chunks. The G_env ablation shows the ecology-derived environment average is not clearly load-bearing over a fixed threshold (CI includes 0), suggesting the stopping rule's efficiency gain is real but its theoretical ecological framing may not uniquely drive performance. Multi-hop stratification reveals MVT-RAG's per-section traversal approach retrieves fewer chunks in both single-hop and multi-hop settings. Verdict: PARTIAL — efficiency claim confirmed, but F1 advantage over top-k baselines is not statistically significant (bootstrap CI spans zero for most comparisons), and G_env ablation CI does not exclude zero.

  Output files: eval_out.json (per-question results with predict_* and eval_* fields for all 8 methods, bootstrap results, stratified analysis, metadata); full/mini/preview variants generated via aii-json format script. Schema validated against exp_eval_sol_out.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Retrieval-augmented generation (RAG) [1] has become the dominant paradigm for grounding large language model (LLM) responses in document evidence. For short documents, global top-$k$ dense retrieval [2] suffices: a query is embedded, the $k$ nearest chunks are retrieved, and an LLM generates from the concatenated context. For long scientific papers—which can span 8,000–20,000 tokens across structurally heterogeneous sections—top-$k$ retrieval faces a fundamental coverage-versus-precision tradeoff. With $k$ too small, critical evidence in minority sections is missed. With $k$ too large, the context window fills with irrelevant text that degrades LLM answer quality and increases cost.

The heterogeneity of scientific documents is not accidental but structural. A typical NLP paper's IMRaD structure (Introduction, Methods, Results, Discussion) places different types of information in different locations: experimental setup in Methods, quantitative outcomes in Results, broader interpretations in Discussion. A question about a specific number naturally points to Results; a question about motivation points to Introduction. Any retrieval strategy that ignores this section structure treats all chunks as exchangeable, discarding information that is immediately available from document layout.

Adaptive retrieval methods such as FLARE [3] and IRCoT [4] address the question of *when* to retrieve by conditioning retrieval on generation uncertainty or chain-of-thought state. Stop-RAG [5] frames the continuation decision as a finite-horizon Markov decision process with a learned value function. These methods improve over fixed-$k$ retrieval in multi-hop settings but share a common limitation: they decide whether to retrieve more content globally, without regard for *which section* to retrieve from next. Hierarchy-aware approaches such as HIRAG structure retrieval around document trees, but select nodes via similarity scores rather than principled criteria for section transitions.

We draw on a complementary tradition: optimal foraging theory from behavioral ecology. The *Marginal Value Theorem* (MVT), introduced by Charnov [6] in 1976, provides an exact, analytically derived criterion for when a forager should leave a depleting resource patch: depart when the current marginal return rate within the patch falls to the environment-wide average. This rule—derived under optimality assumptions—has been validated across hundreds of animal species and extended to human information search behavior by Pirolli's Information Foraging Theory [7]. Crucially, the structural analogy to scientific RAG is precise: sections are patches, retrieved chunks deplete available information within a section, and the document-wide average of per-section best-match similarities provides a natural estimate of the environmental average return.

We propose MVT-RAG, which operationalizes the MVT for section-switching in scientific RAG. The algorithm (1) estimates the environmental average gain $G_{\text{env}}$ from a lightweight initial pass over all sections, (2) iteratively retrieves chunks from the most promising unvisited section, computing marginal gain as relevance weighted by novelty relative to already-retrieved content, and (3) switches to the next highest-potential section when the current marginal gain drops below $G_{\text{env}}$.

[FIGURE:fig1]

We evaluate MVT-RAG on the QASPER benchmark [8], a collection of 888 full NLP papers with 8,000+ information-seeking questions and annotated evidence paragraphs. Our main findings are:

**Summary of Contributions:**
- We propose the first application of the Marginal Value Theorem to intra-document section switching in RAG, providing a parameter-free, training-free, analytically grounded switching criterion (Section 3).
- MVT-RAG achieves a 4$\times$ reduction in retrieval overhead compared to top-$k$-5 retrieval (1.3 vs. 5.0 chunks/question) and significantly outperforms the no-retrieval baseline (F1 delta +0.168, $p$=0.002) on QASPER (Section 5).
- We diagnose the primary failure mode: the G_env threshold derived from single-chunk section sampling is systematically too aggressive, causing under-retrieval and a significant quality gap versus top-$k$ baselines (Section 6).
- An ablation study shows that the ecology-derived dynamic G_env baseline is not statistically distinguishable from a fixed threshold at current scales, isolating G_env estimation as the key component requiring improvement (Section 6).

# Background

## Marginal Value Theorem

The Marginal Value Theorem [6] addresses the optimal foraging problem: given an environment consisting of patches with heterogeneous resource densities that deplete as resources are extracted, when should a forager leave the current patch to travel to a new one? Charnov showed that under mild regularity conditions (unimodal gain curves, constant travel cost), the optimal departure rule is: *leave the current patch when its instantaneous return rate equals the long-run average return rate across the entire environment*.

Formally, if $g_t$ denotes the marginal gain at time step $t$ within the current patch, and $G_{\text{env}}$ is the environment-wide average gain, the MVT switching condition is:
$$g_t < G_{\text{env}}$$
This rule is parameter-free once $G_{\text{env}}$ is specified, and it adapts automatically to the forager's current environment without requiring a hand-tuned threshold.

## Information Foraging Theory

Pirolli [7] extended optimal foraging models to human information search, showing that users navigate information environments—web pages, document corpora—using strategies that resemble those of biological foragers. Under the *information scent* hypothesis, users follow navigational cues (links, headings, keywords) that predict information gain in adjacent regions, leaving a current information source when its scent drops relative to alternatives. This theoretical framing motivates our use of section headers and similarity scores as proxies for ecological patch membership and resource density.

A closely related recent work, InForage [9], applies Information Foraging Theory with reinforcement learning to train a search controller for multi-source web retrieval. Unlike InForage—which learns a policy over independent documents—MVT-RAG applies the specific MVT optimality criterion to intra-document section switching within a single paper, requiring no training. Moore [10] applies MVT to model human semantic memory retrieval (animal-naming fluency tasks); our work differs in applying MVT as an engineering criterion with measurable downstream QA performance.

# Method

## Section Parsing and IMRaD Normalization

MVT-RAG operates on sections as atomic foraging patches. We parse sections from QASPER's columnar `section_name`/`paragraphs` schema, then normalize section names to six IMRaD-inspired categories: *introduction*, *methods*, *results*, *discussion*, *related\_work*, and *other*. The normalization uses keyword matching on section headers (e.g., "experiment" and "evaluation" map to *results*; "approach" and "model" map to *methods*). Papers with fewer than three distinct normalized categories are excluded; 776 of 888 training papers and 265 of 281 validation papers pass this filter [ARTIFACT:art_jHUX0qukOYMI].

Each paragraph within a section becomes one chunk. We encode all chunks and queries with `all-MiniLM-L6-v2` [11], a lightweight sentence embedding model that runs on CPU without additional dependencies.

## MVT-RAG Algorithm

Let $\mathcal{S} = \{s_1, \ldots, s_m\}$ denote the set of document sections and $q$ the query vector. The algorithm proceeds in three phases:

**Phase 1: Environment estimation.** For each section $s_i$, compute the similarity of its best-matching chunk to $q$:
$$\hat{g}_i = \max_{c \in s_i} \cos(c, q)$$
The environmental average is then:
$$G_{\text{env}} = \frac{1}{m} \sum_{i=1}^{m} \hat{g}_i$$

**Phase 2: Adaptive retrieval.** Initialize an empty retrieved set $R = \emptyset$. At each step:
1. Select the unvisited section $s^*$ with the highest $\hat{g}_{s^*}$.
2. Retrieve chunks from $s^*$ in descending similarity order.
3. For each candidate chunk $c_t$, compute the marginal gain:
$$g_t = \cos(c_t, q) \cdot \left(1 - \max_{r \in R} \cos(c_t, r)\right)$$
The first factor captures query relevance; the second captures novelty relative to already-retrieved content.
4. If $g_t < G_{\text{env}}$, mark $s^*$ as exhausted and switch to the next highest-potential section.
5. Otherwise, add $c_t$ to $R$.

**Phase 3: Termination.** Stop when all sections have been either exhausted (no chunk survived the MVT test) or abandoned. Return $R$.

**MVT-NoEnv ablation.** To test whether the ecology-derived dynamic $G_{\text{env}}$ is load-bearing, we define MVT-NoEnv as the same algorithm with $G_{\text{env}}$ replaced by a fixed threshold of 0.3, chosen to match the median environment average observed in the dataset.

## Answer Generation

Retrieved chunks are concatenated in ranked order and passed as context to `meta-llama/llama-3.1-8b-instruct` via OpenRouter with the prompt: *"Answer the following question based only on the provided context. Be concise."* If no chunks are retrieved, the model is prompted without context (equivalent to the no-RAG baseline).

# Experimental Setup

## Dataset

We evaluate on QASPER [8], a benchmark of 888 full-text NLP research papers with question–answer pairs annotated with evidence paragraph spans. The QASPER validation split contains 281 papers. Our main experiment uses a subsample of 100 papers (223 answerable questions) drawn to balance computational cost; the evaluation artifact covers the full 281-paper validation set with a sampled subset [ARTIFACT:art_yFawqoDZbtm3]. Questions are stratified by a multi-hop flag (questions whose gold evidence spans cross two or more sections).

Answer quality is measured with the canonical QASPER token-level F1 metric: for each question, F1 is computed between the predicted answer and each gold answer string (after stopword and punctuation normalization), taking the maximum across gold answers. We additionally report exact match (EM) and *oracle retrieval F1*—the best F1 achievable by passing gold evidence chunks to the LLM—to separate retrieval quality from generation quality.

## Baselines

We compare MVT-RAG against eight systems:

- **Top-$k$ dense** ($k \in \{3, 5, 10\}$): global nearest-neighbor retrieval using `all-MiniLM-L6-v2` embeddings.
- **BM25-5**: BM25 [12] retrieval with $k=5$, providing a sparse lexical baseline.
- **FLARE-style (thresh\_0.3, thresh\_0.5)**: confidence-threshold retrieval that continues retrieving until all retrieved chunks have similarity below the threshold; mimics the FLARE [3] paradigm of uncertainty-driven continuation.
- **MVT-NoEnv**: our MVT framework with $G_{\text{env}}$ replaced by a fixed threshold=0.3.
- **No-RAG**: LLM prompted without any retrieved context.

## Statistical Testing

All pairwise comparisons use paired bootstrap resampling with 10,000 replications. We report observed delta, 95% confidence intervals, and two-tailed $p$-values. An effect is considered significant at $\alpha$=0.05.

# Results

[FIGURE:fig2]

Table 1 presents the main results over 223 QASPER validation questions [ARTIFACT:art_yFawqoDZbtm3].

| Method | F1 | EM | Chunks/Q | Oracle F1 |
|---|---|---|---|---|
| MVT-RAG | 0.122 | 0.000 | **1.30** | 0.140 |
| MVT-NoEnv | 0.119 | 0.000 | 1.00 | 0.119 |
| Top-$k$-3 | 0.165 | 0.000 | 3.00 | 0.341 |
| Top-$k$-5 | 0.190 | 0.000 | 5.00 | 0.441 |
| Top-$k$-10 | **0.203** | 0.000 | 10.00 | **0.596** |
| BM25-5 | 0.178 | 0.000 | 5.00 | 0.338 |
| Thresh-0.3 | 0.175 | 0.000 | 8.83 | 0.495 |
| Thresh-0.5 | 0.148 | 0.000 | 2.44 | 0.249 |
| No-RAG | 0.061 | 0.000 | 0.00 | 0.000 |

**Retrieval efficiency.** MVT-RAG retrieves a mean of 1.30 chunks per question—3.8$\times$ fewer than top-$k$-5 and 6.8$\times$ fewer than the FLARE-style threshold-0.3 baseline. This efficiency advantage is the most robust finding: the MVT stopping criterion reliably prunes low-marginal-gain chunks, confirming that sections constitute meaningful information patches with detectable diminishing returns.

**Answer quality.** MVT-RAG achieves F1=0.122, compared to 0.190 for top-$k$-5. The bootstrap $p$-value is 1.00 (i.e., the observed delta of −0.068 is highly significant in the wrong direction: MVT-RAG is significantly *worse* than top-$k$-5). MVT-RAG does significantly outperform the no-RAG baseline (delta=+0.061, $p$=0.006), confirming that retrieval contributes positively even when highly pruned.

**Oracle retrieval analysis.** The oracle retrieval F1 gap is diagnostic: MVT-RAG achieves an oracle F1 of only 0.140, compared to 0.441 for top-$k$-5. Since oracle F1 measures whether the gold evidence spans are present in the retrieved set regardless of LLM generation quality, this gap confirms that MVT-RAG's low F1 is driven primarily by *under-retrieval*—the switching criterion abandons sections before the relevant evidence chunks are reached.

# Analysis

## G_env Ablation

[FIGURE:fig3]

To test whether the ecology-derived dynamic $G_{\text{env}}$ is the load-bearing component of MVT-RAG, we compare it to MVT-NoEnv, which replaces $G_{\text{env}}$ with a fixed threshold of 0.3. The observed F1 delta is −0.035 (MVT-RAG minus MVT-NoEnv), with 95% CI [−0.074, 0.000] and $p$=0.974 [ARTIFACT:art_wdAfUesLipEx]. The confidence interval barely excludes zero on one side but includes zero throughout most of its range, and the point estimate favors MVT-NoEnv. We conclude that the ecology-derived environmental averaging mechanism provides no statistically distinguishable benefit over a comparable fixed threshold at this evaluation scale.

This null result has a clear mechanistic interpretation: both variants retrieve approximately the same number of chunks (1.30 for MVT-RAG vs. 1.00 for MVT-NoEnv), suggesting that $G_{\text{env}}$ estimated from single-chunk section samples is too noisy to provide a calibration advantage over a hand-tuned constant. The MVT's theoretical benefit—automatic calibration to document content—requires a more accurate estimate of the environmental return rate than the current single-pass approximation provides.

## Stratified Analysis: Single-Hop vs. Multi-Hop Questions

For single-hop questions (questions whose gold evidence lies within one section, $n$=174), MVT-RAG achieves F1=0.128 vs. top-$k$-5 F1=0.196. For multi-hop questions ($n$=49), MVT-RAG achieves F1=0.099 vs. top-$k$-5 F1=0.163. MVT-RAG underperforms on both subsets, ruling out the hypothesis that the section-switching mechanism provides a special advantage for multi-hop questions [ARTIFACT:art_wdAfUesLipEx].

The multi-hop deficit is particularly informative: the MVT's section-switching mechanism is specifically designed for questions that require information from multiple sections, yet it performs worse there relative to top-$k$. The diagnosis is the same as the overall finding: the algorithm *does* switch sections—section traversal is operational—but it abandons each section too early, collecting too few relevant chunks per section before moving on.

## Diagnosis: Threshold Miscalibration

The core failure mode is that $G_{\text{env}}$ systematically overestimates the expected marginal gain at the point where retrieval becomes useful. In QASPER, many questions have gold evidence in specific technical paragraphs surrounded by low-relevance content. The top-ranked chunk per section (used to estimate $\hat{g}_i$) is often the one useful paragraph, but the stopping criterion triggers immediately after it is retrieved—before adjacent paragraphs that provide complementary evidence are examined.

A corrected design would estimate $G_{\text{env}}$ from multiple chunks per section (e.g., the mean of the top-3 per section) or use a multiplicative discount $G_{\text{eff}} = \alpha \cdot G_{\text{env}}$ with $\alpha < 1$ to shift the threshold below the environmental average, allowing more retrieval per section before switching. Both modifications are parameter-light and theoretically consistent with MVT variants that incorporate patch-depletion curves.

# Related Work

## Adaptive RAG

FLARE [3] triggers retrieval when token-level generation probability falls below a confidence threshold, addressing the question of *when* to retrieve during left-to-right generation. IRCoT [4] interleaves retrieval and chain-of-thought reasoning, using reasoning state to form retrieval queries at each step. Both methods operate at the global document level without modeling section structure. Stop-RAG [5] formulates the retrieval continuation decision as a finite-horizon MDP with a learned stopping value function; it is the closest prior method to MVT-RAG in spirit but requires training data and does not model which section to retrieve from next.

## Hierarchical and Structure-Aware RAG

Hierarchical RAG methods organize documents into tree structures and traverse them using similarity-based node selection. GraphReader [13] builds a graph over long documents and uses an agent to navigate it. These methods exploit document structure more deeply than flat chunk retrieval but rely on LLM-driven navigation at each step, making retrieval expensive. MVT-RAG's section-switching criterion requires no LLM calls during retrieval, making it computationally lighter.

## Foraging Theory in Information Systems

InForage [9] is the most closely related recent work: it applies Information Foraging Theory with reinforcement learning to train a search controller for multi-source web retrieval across independent documents. The key distinctions from MVT-RAG are (i) InForage is a trained policy, whereas MVT-RAG applies the MVT analytically without training; (ii) InForage operates over independent web documents, whereas MVT-RAG operates over sections within a single scientific paper. Moore [10] applies MVT to cognitive models of human semantic memory retrieval, a descriptive modeling exercise; our work is prescriptive—we use MVT as an engineering design criterion with evaluable downstream consequences.

## QASPER and Scientific QA

Dasigi et al. [8] introduced QASPER as a benchmark for information-seeking QA over full scientific papers, providing section-level evidence annotations that make it ideal for evaluating section-aware retrieval. Prior QASPER baselines use passage-level retrieval followed by extractive or abstractive QA; no prior work has applied foraging-theoretic switching criteria to this benchmark.

# Discussion

The main finding of this paper is simultaneously positive and cautionary. MVT-RAG's ecological framing yields a concrete, interpretable algorithm with real efficiency gains—4$\times$ fewer retrieved chunks than top-$k$-5—but these efficiency gains are not yet accompanied by competitive answer quality. The diagnosis is specific and actionable: the $G_{\text{env}}$ estimator is too aggressive because it uses the single best-matching chunk per section as a proxy for the full section's expected return, whereas the MVT's optimality assumptions require an estimate of the *average* rate across the entire foraging episode in a section.

**Limitations.** First, our evaluation uses Llama-3.1-8B as the reader model; larger models with better instruction-following may be more tolerant of sparse retrieved contexts, potentially narrowing the F1 gap at lower chunk counts. Second, QASPER's short answers (often 1–5 tokens) amplify the penalty for under-retrieval: if the one correct sentence is not in the retrieved set, F1 is exactly 0 regardless of answer quality. Third, the oracle F1 analysis confirms a retrieval bottleneck, not a generation bottleneck, but we cannot fully disentangle the contribution of chunk boundary effects from the switching threshold per se. Fourth, our section parsing relies on header-based heuristics; papers with non-standard structures (e.g., lack of section headers in some QASPER papers) reduce the accuracy of section detection.

**Future directions.** The most important next step is improving $G_{\text{env}}$ estimation: replacing the single-chunk estimator with a multi-chunk average (e.g., mean of top-3 per section) or a discount factor $\alpha < 1$ that shifts the threshold below the raw environment average. A secondary direction is combining MVT switching with iterative re-ranking: after MVT selects a section, a more powerful cross-encoder could be used to rank chunks within that section, improving the oracle retrieval F1 within the MVT framework's efficient budget.

# Conclusion

We have proposed and evaluated MVT-RAG, the first application of the Marginal Value Theorem from ecological foraging to section switching in scientific RAG. The approach treats document sections as foraging patches and switches sections when the marginal semantic information gain falls below the document-wide environmental average—an analytically derived, parameter-free criterion requiring no training or LLM calls during retrieval. On the QASPER scientific QA benchmark, MVT-RAG retrieves 4$\times$ fewer chunks than top-$k$-5 (1.3 vs. 5.0 per question) and significantly outperforms the no-retrieval baseline. However, the aggressive stopping criterion causes systematic under-retrieval, yielding F1=0.122 versus 0.190 for top-$k$-5, and the ecology-derived dynamic $G_{\text{env}}$ provides no statistically significant advantage over a fixed threshold. We identify $G_{\text{env}}$ miscalibration as the key obstacle and propose multi-chunk estimation as a direct remedy. The MVT framework itself—treating sections as patches with measurable depletion curves—remains a promising, theoretically grounded alternative to black-box learned controllers for structure-aware scientific retrieval.

# References

[1] Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS.

[2] Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain Question Answering. EMNLP.

[3] Jiang et al. (2023). Active Retrieval Augmented Generation (FLARE). EMNLP.

[4] Trivedi et al. (2022). Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions. ACL.

[5] Park et al. (2025). Stop-RAG: Value-Based Retrieval Control for Iterative RAG. arXiv:2510.14337.

[6] Charnov (1976). Optimal foraging, the marginal value theorem. Theoretical Population Biology, 9(2):129–136.

[7] Pirolli (2007). Information Foraging Theory: Adaptive Interaction with Information. Oxford University Press.

[8] Dasigi et al. (2021). A Dataset of Information-Seeking Questions and Answers Anchored in Research Papers. NAACL.

[9] Qian and Liu (2025). Scent of Knowledge: Optimizing Search-Enhanced Reasoning with Information Foraging. NeurIPS.

[10] Moore (2025). Optimal Foraging in Memory Retrieval. arXiv:2511.12759.

[11] Reimers and Gurevych (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. EMNLP.

[12] Robertson and Walker (1994). Some Simple Effective Approximations to the 2-Poisson Model for Probabilistic Weighted Retrieval. SIGIR.

[13] Li et al. (2024). GraphReader: Building Graph-based Agent to Enhance Long-Context Abilities of Large Language Models. EMNLP.

\bibliography{references}
\bibliographystyle{plainnat}
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (rigor) Code-paper discrepancy in the MVT-NoEnv ablation threshold. The paper states 'G_env replaced by a fixed threshold of 0.3, chosen to match the median environment average observed in the dataset.' The code (method.py line 210) implements `threshold: float = 0.5`, and the experiment artifact summary also states 'fixed threshold=0.5'. The ablation conclusion—that G_env provides no benefit over a fixed threshold—is drawn from a comparison where the two variants use different threshold values. This undermines the ablation's validity: MVT-NoEnv with threshold=0.5 is stricter than 0.3, which may explain the similar chunk counts (1.30 vs. 1.00) and similar F1 (0.122 vs. 0.119) as an artifact of the threshold choice rather than the G_env mechanism per se.
  Action: Reconcile the paper and code: pick one threshold value, justify the choice (e.g., the actual median G_env observed in the dataset), rerun MVT-NoEnv with that value, and update all reported numbers. Then re-examine whether the G_env ablation conclusion holds.
- [MAJOR] (evidence) The proposed method underperforms every retrieval baseline by a statistically significant margin, yet the paper frames efficiency (1.3 chunks/question) as a primary contribution. The efficiency gain is real, but there is no evidence that the efficiency-quality tradeoff is Pareto-superior to simply choosing top-k-3, which retrieves 3 chunks at F1=0.165 vs. MVT-RAG's 1.3 chunks at F1=0.122. A method that uses fewer chunks at lower quality is not obviously preferable to cheaper baselines. The paper does not include a cost-quality Pareto analysis comparing MVT-RAG to top-k-1 or top-k-2, which would be the natural efficiency-matched comparisons.
  Action: Add top-k-1 and top-k-2 as baselines to provide a fair efficiency-matched comparison. If MVT-RAG at 1.3 chunks/question is not better than top-k-1 at 1 chunk/question, this must be stated. Alternatively, reframe the contribution explicitly as a diagnostic negative result rather than a working method.
- [MAJOR] (methodology) The fix for G_env miscalibration is described in the Discussion but never validated experimentally. The paper diagnoses the failure mode (single-chunk G_env estimate is too aggressive) and proposes two remedies (multi-chunk mean, discount factor alpha < 1), but neither is implemented. At a top venue, a paper that diagnoses a failure and proposes a fix should either run the fix or provide a theoretical argument for why it works. Without this, the diagnosis is speculative—it could be that even multi-chunk G_env estimation fails, or that the section-switching mechanism itself (not just the threshold) is the bottleneck.
  Action: Implement at least one variant of the proposed fix and add it as an additional experiment. The multi-chunk G_env estimator (mean of top-3 similarity scores per section) is a simple code change. Report whether it closes the oracle F1 gap vs. top-k-5.
- [MAJOR] (evidence) Exact match (EM) is 0.000 for all methods including top-k-10 and oracle conditions. This is anomalous: QASPER has many questions with short, exact answers, and prior work (e.g., Dasigi et al. 2021) reports non-zero EM on the same benchmark. Zero EM across all 9 methods strongly suggests a metric implementation error—likely that the EM normalization (stopword/punctuation removal) is either too aggressive or not applied correctly. If confirmed, this also casts doubt on the F1 numbers.
  Action: Debug the EM metric implementation by spot-checking specific questions where the predicted answer matches the gold answer. Compare against the reference QASPER evaluation script (available in the QASPER GitHub repo). Report the bug fix and re-run evaluation.
- [MINOR] (novelty) The claim 'first application of the Marginal Value Theorem to intra-document section switching' is plausible, but the paper would benefit from a more systematic prior work survey. InForage (ref [9]) applies Information Foraging Theory to multi-document retrieval; HIRAG and similar hierarchy-aware methods also use section-level structure. The distinction from these works is stated qualitatively ('no training', 'intra-document') but not quantitatively compared. Including HIRAG or a similar hierarchy-aware baseline would strengthen the novelty argument.
  Action: Add HIRAG or another section-aware hierarchical RAG baseline if the code is available, or at minimum discuss quantitative comparisons from published HIRAG results on QASPER.
- [MINOR] (scope) The evaluation uses only one LLM reader (Llama-3.1-8B) and one embedding model (all-MiniLM-L6-v2). The paper mentions in Limitations that larger models may be more tolerant of sparse contexts, but does not test this. With 8B parameters, the LLM may be too weak to reliably answer from even the correct single chunk, making it hard to disentangle retrieval quality from generation quality.
  Action: Add an oracle retrieval condition where the LLM is given the exact gold evidence paragraph(s) regardless of retrieval method. If the oracle F1 is substantially higher than the best retrieval F1, the evaluation correctly diagnoses a retrieval bottleneck. This experiment is already partially done (oracle F1 is reported), but the paper should discuss what oracle F1 implies for the maximum achievable score given the reader model.
- [MINOR] (clarity) The introduction's contribution bullet points create a misleading impression. Bullet 2 states '+0.168 F1 delta vs. no-RAG baseline' as a headline result, while bullet 3 notes 'significant quality gap versus top-k baselines'. A reader skimming contributions sees a positive result before seeing the negative one. The positioning should reflect the primary finding: MVT-RAG achieves efficiency gains at a significant quality cost.
  Action: Reorder contributions so that the quality deficit relative to baselines is stated before the efficiency gain. Alternatively, combine them into a single honest statement: 'MVT-RAG achieves 4x retrieval efficiency over top-k-5 at the cost of lower answer quality (F1=0.122 vs. 0.190), and we diagnose G_env miscalibration as the fixable root cause.'
- [MINOR] (methodology) The multi-hop stratification (n=49 multi-hop, n=174 single-hop) is reported as a secondary finding, but the diagnostic value is limited because the section-switching mechanism *does* traverse multiple sections—the deficit on multi-hop questions is attributed to under-retrieval per section rather than failure to switch sections. It would be more informative to report whether MVT-RAG actually visits the correct number of sections for multi-hop questions (i.e., does it switch sections when the gold evidence spans multiple sections?).
  Action: Add a metric tracking section recall: for multi-hop questions, what fraction of gold evidence sections are visited by MVT-RAG? This directly tests whether the section-switching logic is functionally correct separate from the threshold calibration issue.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 16:24:55 UTC

```
Improving retrieval-augmented generation for long scientific documents
```

### [3] SYSTEM-USER prompt · 2026-07-18 16:25:32 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Same MVT framework; refined to diagnose G_env miscalibration as root cause and reframe contribution as efficiency-quality tradeoff with proposed fix.' is too long (at most 120 characters, got 149)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
