# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-sonnet-4-6)

### [1] CONFIG · 2026-07-18 16:27:11 UTC

```
model: claude-sonnet-4-6 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1
```

### [2] SYSTEM-USER prompt · 2026-07-18 16:27:17 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

<available_resources>
<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<hypothesis>
kind: hypothesis
title: 'MVT Section Switching: Efficiency-Quality Tradeoff in Scientific RAG'
hypothesis: >-
  The Marginal Value Theorem (MVT) from ecological foraging theory provides an interpretable, parameter-free criterion for
  adaptive section switching in retrieval-augmented generation over long scientific documents, but its naive implementation
  with single-chunk G_env estimation causes systematic under-retrieval that yields lower answer quality than fixed-k baselines.
  Specifically: modeling document sections (introduction, methods, results, discussion) as forageable 'patches' and estimating
  the environment-wide average marginal gain G_env from the single best-matching chunk per section, the MVT criterion triggers
  section switching too aggressively—achieving 4x retrieval efficiency (1.3 vs 5.0 chunks/question) at the cost of significantly
  lower F1 (0.122 vs 0.190 for top-k-5 on QASPER). We hypothesize that replacing the single-chunk G_env estimator with a multi-chunk
  average (mean of top-3 similarity scores per section) or applying a discount factor α < 1 to the raw G_env will substantially
  close the oracle retrieval F1 gap without sacrificing the efficiency advantage, because the corrected estimator will better
  approximate the true expected marginal return rate within each section and avoid premature patch abandonment. The ecology-derived
  adaptive baseline provides no statistically distinguishable benefit over a fixed threshold at current estimation quality,
  but this null result is attributable to G_env estimation noise rather than a flaw in the MVT framework itself.
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
_relation_rationale: >-
  Same MVT framework; reframed as efficiency-quality tradeoff with G_env miscalibration as the diagnosed root cause.
_confidence_delta: decreased
_key_changes:
- >-
  Primary positive claim (MVT-RAG outperforms fixed-k baselines in F1) is replaced by a negative finding: MVT-RAG significantly
  underperforms top-k-5 (F1=0.122 vs 0.190, p=1.00 in wrong direction).
- >-
  Efficiency advantage is retained as a real but partial contribution: 4x fewer chunks confirmed, but not Pareto-superior
  to top-k-1/2 without quality recovery.
- >-
  G_env estimation (single-chunk per section) is now identified as the primary bottleneck driving under-retrieval, not the
  MVT switching framework itself.
- >-
  G_env ablation null result (CI includes zero vs fixed threshold) is incorporated: the ecology-derived adaptive baseline
  provides no measurable benefit at current estimation quality.
- >-
  Proposed fix is now part of the testable hypothesis: multi-chunk G_env (mean of top-3 per section) or discount factor α
  < 1 as the next experimental target.
- >-
  Framing shifts from 'MVT outperforms baselines' to 'MVT framework is sound but G_env estimator requires correction to realize
  quality gains alongside efficiency gains'.
- >-
  EM=0 anomaly noted as a metric implementation concern requiring verification before final conclusions on absolute performance.
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter2_dir1
type: experiment
objective: >-
  Re-run MVT-RAG with multi-chunk G_env variants (top-3/top-5 mean), discount-factor variant (alpha=0.7), corrected MVT-NoEnv
  ablation threshold, top-k-1/k-2 baselines, oracle condition, EM bug fix, and section-recall metric.
approach: >-
  Load QASPER data from the existing dataset artifact (full_data_out.json). Re-implement MVT-RAG with three G_env estimator
  variants: (a) top-1 per section (original), (b) mean of top-3 per section, (c) mean of top-5 per section. Add discount-factor
  variant: G_eff = 0.7 * G_env. Fix MVT-NoEnv ablation: compute actual median G_env across questions from a pilot pass, then
  use that as the fixed threshold. Add top-k-1 and top-k-2 baselines. Add oracle condition: give gold evidence paragraphs
  directly to LLM. Add section-recall metric for multi-hop questions. Debug EM=0 bug by spot-checking predicted vs gold strings
  and comparing against QASPER reference normalization (lowercase, remove articles/punctuation, tokenize). Run on 223-question
  validation subset for comparability. LLM: meta-llama/llama-3.1-8b-instruct via OpenRouter (~$1.50 budget). Output method_out.json
  with per-question results for all variants.
depends_on:
- id: art_jHUX0qukOYMI
  label: dataset
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [3] HUMAN-USER prompt · 2026-07-18 16:27:17 UTC

```
Improving retrieval-augmented generation for long scientific documents
```

### [4] TOOL CALL — Write · 2026-07-18 16:29:01 UTC

````
File: /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json

{
  "title": "MVT-RAG G_env Fix: Quality vs Efficiency",
  "summary": "Re-run MVT-RAG on QASPER with corrected G_env estimators (top-3/top-5 mean, alpha=0.7 discount), fixed MVT-NoEnv ablation threshold, top-k-1/2 baselines, oracle condition, EM bug fix, and section-recall metric. Primary goal: test whether multi-chunk G_env closes the F1 gap (0.122→target 0.165+) while retaining efficiency advantage.",
  "runpod_compute_profile": "cpu_heavy",
  "implementation_pseudocode": "## Setup\n\n```\nDEP_DATA = '/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'\nOUTPUT = './method_out.json'\nOPENROUTER_MODEL = 'meta-llama/llama-3.1-8b-instruct'\nBUDGET_USD = 1.50  # hard cap, track cumulative\n\n# Use aii-openrouter-llms skill for LLM calls\n# Use aii-python skill for coding standards\n```\n\n## Step 1: Load and Validate Data\n\n```\nLoad full_data_out.json (2000 examples)\nFilter to metadata_fold==1 (validation set, ~223 questions)\n  - Each example: input JSON has {question, paper_id, sections_summary}\n  - output JSON has {gold_answer, evidence_chunk_ids, evidence_section_names}\n  - metadata fields: metadata_is_multihop, metadata_num_sections, etc.\n\nParse sections_summary to reconstruct per-paper chunk list:\n  Each section has section_name, normalized_section, chunks (list of {chunk_id, text})\nGroup chunks by paper_id -> section -> list of chunks\n```\n\n## Step 2: Embeddings (one-time, cache to disk)\n\n```\nfrom sentence_transformers import SentenceTransformer\nmodel = SentenceTransformer('all-MiniLM-L6-v2')  # CPU-only, fast\n\nFor each unique paper in validation set:\n  For each chunk across all sections:\n    embed chunk text -> vector (384-dim)\n  Cache paper_id -> {chunk_id: embedding} as embeddings.pkl\n\nFor each question:\n  embed question text -> query_vector\n  Cache question_id -> query_vector\n\nNote: ~223 questions x avg 50 chunks/paper = ~11k embeddings total, fast on CPU\n```\n\n## Step 3: EM Normalization Fix\n\n```\n# QASPER official normalization from their evaluation script:\ndef normalize_answer(s):\n    s = s.lower()\n    s = re.sub(r'\\b(a|an|the)\\b', ' ', s)  # remove articles\n    s = re.sub(r'[^\\w\\s]', '', s)           # remove punctuation\n    s = ' '.join(s.split())                  # normalize whitespace\n    return s\n\ndef exact_match(pred, gold_list):\n    pred_norm = normalize_answer(pred)\n    return any(normalize_answer(g) == pred_norm for g in gold_list)\n\ndef token_f1(pred, gold_list):\n    pred_tokens = normalize_answer(pred).split()\n    best_f1 = 0\n    for gold in gold_list:\n        gold_tokens = normalize_answer(gold).split()\n        common = Counter(pred_tokens) & Counter(gold_tokens)\n        n_common = sum(common.values())\n        if n_common == 0: continue\n        prec = n_common / len(pred_tokens)\n        rec = n_common / len(gold_tokens)\n        f1 = 2*prec*rec/(prec+rec)\n        best_f1 = max(best_f1, f1)\n    return best_f1\n\n# gold_answer in output JSON may be a list (multiple valid answers) or\n# a string - handle both cases. QASPER answers can be 'yes'/'no'/free text/list.\n```\n\n## Step 4: MVT-RAG Core Implementation\n\n```python\ndef cosine_sim(a, b):\n    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)\n\ndef marginal_gain(chunk_emb, query_emb, retrieved_embs):\n    query_sim = cosine_sim(chunk_emb, query_emb)\n    if not retrieved_embs:\n        novelty = 1.0\n    else:\n        max_sim_to_retrieved = max(cosine_sim(chunk_emb, r) for r in retrieved_embs)\n        novelty = 1.0 - max_sim_to_retrieved\n    return query_sim * novelty\n\ndef estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1):\n    # top_n: number of top chunks per section to average\n    section_scores = []\n    for sec in sections:\n        sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)\n                for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]\n        if not sims: continue\n        top_sims = sorted(sims, reverse=True)[:top_n]\n        section_scores.append(np.mean(top_sims))\n    return np.mean(section_scores) if section_scores else 0.0\n\ndef mvt_retrieve(query_emb, sections, chunk_embeddings,\n                 g_env_top_n=1, alpha=1.0, max_chunks=15):\n    \"\"\"\n    g_env_top_n: 1 (original), 3 (top-3), 5 (top-5)\n    alpha: discount factor applied to G_env (0.7 = more permissive)\n    Returns: list of retrieved chunk_ids in order\n    \"\"\"\n    g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=g_env_top_n)\n    effective_threshold = alpha * g_env\n\n    # Score sections by best chunk similarity (for ordering)\n    section_priority = []\n    for sec in sections:\n        sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)\n                for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]\n        best = max(sims) if sims else 0.0\n        section_priority.append((best, sec))\n    section_priority.sort(reverse=True)\n\n    retrieved_chunk_ids = []\n    retrieved_embs = []\n\n    for _, sec in section_priority:\n        # Within section, retrieve chunks in descending query similarity order\n        chunks_sorted = sorted(\n            sec['chunks'],\n            key=lambda c: cosine_sim(chunk_embeddings.get(c['chunk_id'], np.zeros(384)), query_emb),\n            reverse=True\n        )\n        for chunk in chunks_sorted:\n            if len(retrieved_chunk_ids) >= max_chunks:\n                return retrieved_chunk_ids\n            cid = chunk['chunk_id']\n            if cid not in chunk_embeddings:\n                continue\n            g_t = marginal_gain(chunk_embeddings[cid], query_emb, retrieved_embs)\n            if g_t < effective_threshold:\n                break  # switch to next section\n            retrieved_chunk_ids.append(cid)\n            retrieved_embs.append(chunk_embeddings[cid])\n\n    return retrieved_chunk_ids\n```\n\n## Step 5: MVT-NoEnv Fixed-Threshold Ablation (CORRECTED)\n\n```python\n# Pilot pass: compute actual G_env distribution across all validation questions\n# using top-1 estimator, then use median as fixed threshold\ndef compute_pilot_g_env(validation_questions, chunk_embeddings, query_embeddings):\n    g_envs = []\n    for q in validation_questions:\n        sections = get_sections(q)\n        query_emb = query_embeddings[q['question_id']]\n        g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1)\n        g_envs.append(g_env)\n    return np.median(g_envs)  # use as fixed threshold for NoEnv ablation\n\n# MVT-NoEnv: same algorithm but threshold=fixed_threshold instead of per-question G_env\ndef mvt_noenv_retrieve(query_emb, sections, chunk_embeddings, fixed_threshold, max_chunks=15):\n    # Same as mvt_retrieve but g_env is replaced by fixed_threshold\n    # (this is the correct ablation: no ecology-derived environment average)\n    ...\n```\n\n## Step 6: All Baselines\n\n```python\n# Top-k dense retrieval: flatten all chunks for paper, sort by query cosine sim, take top k\ndef topk_retrieve(query_emb, all_chunks, chunk_embeddings, k):\n    sims = [(cosine_sim(chunk_embeddings[c['chunk_id']], query_emb), c['chunk_id'])\n            for c in all_chunks if c['chunk_id'] in chunk_embeddings]\n    sims.sort(reverse=True)\n    return [cid for _, cid in sims[:k]]\n\n# Oracle: use gold evidence_chunk_ids directly (no retrieval error)\ndef oracle_retrieve(gold_evidence_chunk_ids):\n    return gold_evidence_chunk_ids\n```\n\n## Step 7: LLM Answer Generation\n\n```python\n# Via OpenRouter - use aii-openrouter-llms skill for setup\n# Model: meta-llama/llama-3.1-8b-instruct\n# Prompt template:\nSYSTEM = \"You are a scientific QA assistant. Answer questions using ONLY the provided context. Be concise.\"\n\ndef build_prompt(question, chunks_text_list):\n    context = '\\n\\n'.join([f'[Chunk {i+1}]: {t}' for i, t in enumerate(chunks_text_list)])\n    return f\"Context:\\n{context}\\n\\nQuestion: {question}\\n\\nAnswer:\"\n\n# Cost tracking:\n# llama-3.1-8b-instruct: ~$0.06/1M input tokens, $0.06/1M output tokens\n# ~223 questions x 10 variants x avg 1500 input tokens = ~3.3M tokens = ~$0.20 total\n# Very safe within $1.50 budget\n\n# IMPORTANT: If no chunks retrieved, use empty context fallback\n# Track cost after each batch of 10 calls; stop if approaching $1.50\n```\n\n## Step 8: Section Recall Metric\n\n```python\ndef section_recall(retrieved_chunk_ids, gold_evidence_section_names, chunk_id_to_section):\n    \"\"\"\n    For multi-hop questions: what fraction of gold evidence sections\n    have at least one retrieved chunk?\n    \"\"\"\n    retrieved_sections = set(chunk_id_to_section.get(cid) for cid in retrieved_chunk_ids)\n    gold_sections = set(gold_evidence_section_names)\n    if not gold_sections:\n        return 1.0\n    return len(retrieved_sections & gold_sections) / len(gold_sections)\n```\n\n## Step 9: Full Experiment Loop\n\n```python\nVARIANTS = [\n    {'name': 'top-k-1',      'type': 'topk',   'k': 1},\n    {'name': 'top-k-2',      'type': 'topk',   'k': 2},\n    {'name': 'top-k-3',      'type': 'topk',   'k': 3},\n    {'name': 'top-k-5',      'type': 'topk',   'k': 5},\n    {'name': 'top-k-10',     'type': 'topk',   'k': 10},\n    {'name': 'mvt-top1',     'type': 'mvt',    'g_env_top_n': 1, 'alpha': 1.0},  # original\n    {'name': 'mvt-top3',     'type': 'mvt',    'g_env_top_n': 3, 'alpha': 1.0},  # FIX: multi-chunk\n    {'name': 'mvt-top5',     'type': 'mvt',    'g_env_top_n': 5, 'alpha': 1.0},  # FIX: multi-chunk\n    {'name': 'mvt-alpha0.7', 'type': 'mvt',    'g_env_top_n': 1, 'alpha': 0.7}, # FIX: discount\n    {'name': 'mvt-noenv',    'type': 'mvt_noenv'},  # fixed threshold ablation\n    {'name': 'oracle',       'type': 'oracle'},\n]\n\nresults = []  # per-question results\ncumulative_cost = 0.0\n\nfor q in validation_questions:  # ~223 questions\n    question = q['input_parsed']['question']\n    paper_sections = get_sections_for_paper(q)\n    gold_answer = q['output_parsed']['gold_answer']  # may be list or string\n    gold_chunk_ids = q['output_parsed']['evidence_chunk_ids']\n    gold_section_names = q['output_parsed']['evidence_section_names']\n    is_multihop = q['metadata_is_multihop']\n    query_emb = embed(question)\n\n    q_result = {'question_id': q['metadata_question_id'],\n                'is_multihop': is_multihop, 'variants': {}}\n\n    for variant in VARIANTS:\n        # 1. Retrieve chunks\n        if variant['type'] == 'topk':\n            retrieved = topk_retrieve(query_emb, all_chunks, chunk_embs, variant['k'])\n        elif variant['type'] == 'mvt':\n            retrieved = mvt_retrieve(query_emb, paper_sections, chunk_embs,\n                                     g_env_top_n=variant['g_env_top_n'],\n                                     alpha=variant['alpha'])\n        elif variant['type'] == 'mvt_noenv':\n            retrieved = mvt_noenv_retrieve(query_emb, paper_sections, chunk_embs, fixed_threshold)\n        else:  # oracle\n            retrieved = gold_chunk_ids\n\n        # 2. Build context from retrieved chunks\n        context_texts = [chunk_id_to_text[cid] for cid in retrieved if cid in chunk_id_to_text]\n\n        # 3. LLM answer generation\n        if cumulative_cost >= 1.40:  # safety stop\n            predicted_answer = '[BUDGET_EXCEEDED]'\n        else:\n            prompt = build_prompt(question, context_texts)\n            predicted_answer, cost = call_openrouter(OPENROUTER_MODEL, prompt)\n            cumulative_cost += cost\n\n        # 4. Compute metrics\n        gold_list = gold_answer if isinstance(gold_answer, list) else [gold_answer]\n        em = exact_match(predicted_answer, gold_list)\n        f1 = token_f1(predicted_answer, gold_list)\n        sec_rec = section_recall(retrieved, gold_section_names, chunk_id_to_section)\n        n_chunks = len(retrieved)\n\n        q_result['variants'][variant['name']] = {\n            'retrieved_chunk_ids': retrieved,\n            'predicted_answer': predicted_answer,\n            'em': em, 'f1': f1,\n            'n_chunks_retrieved': n_chunks,\n            'section_recall': sec_rec,\n        }\n\n    results.append(q_result)\n\n# Aggregate metrics across all questions\nfor variant_name in [v['name'] for v in VARIANTS]:\n    avg_em = mean(r['variants'][variant_name]['em'] for r in results)\n    avg_f1 = mean(r['variants'][variant_name]['f1'] for r in results)\n    avg_chunks = mean(r['variants'][variant_name]['n_chunks_retrieved'] for r in results)\n    avg_sec_rec = mean(r['variants'][variant_name]['section_recall'] for r in results)\n    # Also compute for multihop subset\n    multihop_results = [r for r in results if r['is_multihop']]\n    ...\n\n# Bootstrap 95% CI for F1 differences (MVT vs top-k-5 as primary comparison)\n# 10000 bootstrap samples with paired resampling\n```\n\n## Step 10: Output\n\n```python\nmethod_out = {\n    'summary': {\n        'n_questions': len(results),\n        'n_multihop': sum(r['is_multihop'] for r in results),\n        'total_cost_usd': cumulative_cost,\n        'per_variant_aggregate': {\n            variant_name: {\n                'mean_em': ..., 'mean_f1': ...,\n                'mean_chunks': ..., 'mean_section_recall': ...,\n                'multihop_mean_f1': ..., 'multihop_mean_section_recall': ...\n            }\n        },\n        'bootstrap_ci_mvt_top3_vs_topk5_f1': [lower, upper],\n        'bootstrap_ci_mvt_alpha07_vs_topk5_f1': [lower, upper],\n        'pilot_g_env_median': fixed_threshold,\n    },\n    'per_question': results  # full detail for analysis\n}\n\nwith open('method_out.json', 'w') as f:\n    json.dump(method_out, f, indent=2)\n```\n\n## Key Implementation Notes\n\n1. **Data parsing**: The dependency dataset stores input/output as JSON strings—parse with `json.loads()`.\n   `sections_summary` in the input JSON contains the full chunk list per section.\n\n2. **Embedding caching**: Save to `embeddings_cache.pkl` after first run. Check for cache file at start.\n\n3. **Gold answer format**: QASPER answers can be 'yes'/'no', extractive spans, or lists. The dataset\n   artifact normalizes these; treat as list always.\n\n4. **EM=0 debug**: Before full run, spot-check 5 examples: print raw predicted answer, gold answers,\n   and normalized versions. If all EM=0 even on oracle condition, the LLM prompt/parsing is broken.\n\n5. **Oracle F1 ceiling**: Oracle should achieve ~0.4-0.6 F1 on QASPER (known upper bound from literature).\n   If oracle F1 < 0.3, the LLM call or answer parsing is likely broken—fix before full run.\n\n6. **Sections parsing**: The sections_summary is a list of section objects. Each section has `chunks`\n   list. Re-group by `normalized_section` name to get IMRaD categories.\n\n7. **Papers with few sections**: If a paper has only 1-2 sections, MVT switching is trivial.\n   These are excluded by the dataset (>=3 distinct sections filter) but verify at runtime.\n\n8. **OpenRouter setup**: Use the aii-openrouter-llms skill to get the API key and call pattern.\n   All calls must go through OpenRouter—no direct Anthropic/OpenAI endpoints.",
  "fallback_plan": "## Primary Fallback: Reduce LLM calls\n\nIf cost is tracking high (>$0.80 after 100 questions), reduce variants by dropping top-k-10 and oracle, which are less critical for the core hypothesis. Run 5 core variants: top-k-1, top-k-3, top-k-5, mvt-top3, mvt-alpha0.7.\n\n## Secondary Fallback: Skip LLM, use retrieval-only metrics\n\nIf OpenRouter is unavailable or budget is too tight, skip LLM generation entirely and report only:\n- Retrieval precision/recall (gold evidence chunks retrieved)\n- Section recall\n- N chunks retrieved per question\n\nThese metrics directly test the core hypothesis (does multi-chunk G_env improve retrieval quality?) without needing generation. Report retrieval F1 (did we retrieve the right chunks?) instead of answer F1.\n\n## Embedding Fallback\n\nIf sentence-transformers is slow on CPU, use `paraphrase-MiniLM-L3-v2` (smaller/faster) or TF-IDF cosine similarity as a zero-dependency alternative. TF-IDF is much faster and still captures keyword overlap.\n\n## Data Fallback\n\nIf sections_summary doesn't contain full chunk text (parse error), fall back to re-loading QASPER directly from HuggingFace (`allenai/qasper`, validation split) and re-parsing sections inline using the same logic as the dataset artifact's data.py.\n\n## Truncation Fallback\n\nIf 223 questions take too long (>5h with embeddings+LLM), run on 100 questions (first 50 single-hop + first 50 multihop) and report results on that subset with a note.",
  "testing_plan": "## Step 0: Verify Data Loading (5 min)\n\n```python\nimport json\ndata = json.load(open(DEP_DATA))\nvalidation = [x for x in data if x['metadata_fold'] == 1]\nprint(f'Validation size: {len(validation)}')\nprint('First example input keys:', json.loads(validation[0]['input']).keys())\nprint('First example output keys:', json.loads(validation[0]['output']).keys())\nprint('Is multihop distribution:', sum(x['metadata_is_multihop'] for x in validation))\n```\nExpect: ~223 validation examples, input has question+sections_summary, output has gold_answer+evidence_chunk_ids.\n\n## Step 1: Mini smoke test on 5 examples (15 min)\n\nRun ALL variants on 5 questions (mix of single-hop and multihop).\n- Check embeddings work: cosine sims in [0.0, 1.0] range\n- Check G_env estimation produces non-zero values\n- Check MVT retrieves between 1-15 chunks (not always 0 or 15)\n- Check oracle retrieves the correct chunk IDs\n- Check LLM returns non-empty string (1 LLM call to verify API)\n- Check EM normalization: manually verify normalized predicted vs gold for 2 examples\n- Print per-example summary table: variant | n_chunks | f1 | em\n\n## Step 2: EM debug check (5 min)\n\nFor oracle condition on 5 examples:\n- Print raw LLM output\n- Print gold_answer\n- Print normalize(pred) vs normalize(gold)\n- If EM=0 for oracle on obvious 'yes'/'no' answers, fix normalization\n- Target: oracle F1 >= 0.30 on 5-example sample\n\n## Step 3: Embedding cache check (2 min)\n\nAfter first mini run, verify `embeddings_cache.pkl` exists and reload correctly. Second mini run should be faster.\n\n## Step 4: 50-question validation run (30 min)\n\nRun all variants on 50 questions before full 223.\n- Verify cost tracking: cumulative_cost after 50q x 10 variants should be ~$0.40\n- Verify multihop questions are present (should be ~17 of 50)\n- Check aggregate F1 table looks reasonable: oracle > top-k-5 > top-k-1\n- If top-k-5 F1 is still ~0.190 (matching iter1), data pipeline is consistent\n- Check mvt-top3 F1 vs mvt-top1 F1: expect improvement (this is the core hypothesis)\n\n## Full run completion signals\n\n- Oracle F1 >= 0.35 (literature upper bound for 8B model on QASPER is ~0.40-0.50)\n- Top-k-5 F1 ~0.17-0.22 (within range of published results)\n- MVT-top3 retrieves more chunks than MVT-top1 (G_env reduced → less aggressive switching)\n- Bootstrap CI for MVT-top3 vs top-k-5 F1: check whether CI excludes zero (confirms hypothesis)\n- Cost <= $1.00 total"
}
````

### [5] TOOL RESULT — Write · 2026-07-18 16:29:01 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"MVT-RAG G_env Fix: Quality vs Efficiency\",\n  \"summary\": \"Re-run MVT-RAG on QASPER with corrected G_env estimators (top-3/top-5 mean, alpha=0.7 discount), fixed MVT-NoEnv ablation threshold, top-k-1/2 baselines, oracle condition, EM bug fix, and section-recall metric. Primary goal: test whether multi-chunk G_env closes the F1 gap (0.122→target 0.165+) while retaining efficiency advantage.\",\n  \"runpod_compute_profile\": \"cpu_heavy\",\n  \"implementation_pseudocode\": \"## Setup\\n\\n```\\nDEP_DATA = '/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'\\nOUTPUT = './method_out.json'\\nOPENROUTER_MODEL = 'meta-llama/llama-3.1-8b-instruct'\\nBUDGET_USD = 1.50  # hard cap, track cumulative\\n\\n# Use aii-openrouter-llms skill for LLM calls\\n# Use aii-python skill for coding standards\\n```\\n\\n## Step 1: Load and Validate Data\\n\\n```\\nLoad full_data_out.json (2000 examples)\\nFilter to metadata_fold==1 (validation set, ~223 questions)\\n  - Each example: input JSON has {question, paper_id, sections_summary}\\n  - output JSON has {gold_answer, evidence_chunk_ids, evidence_section_names}\\n  - metadata fields: metadata_is_multihop, metadata_num_sections, etc.\\n\\nParse sections_summary to reconstruct per-paper chunk list:\\n  Each section has section_name, normalized_section, chunks (list of {chunk_id, text})\\nGroup chunks by paper_id -> section -> list of chunks\\n```\\n\\n## Step 2: Embeddings (one-time, cache to disk)\\n\\n```\\nfrom sentence_transformers import SentenceTransformer\\nmodel = SentenceTransformer('all-MiniLM-L6-v2')  # CPU-only, fast\\n\\nFor each unique paper in validation set:\\n  For each chunk across all sections:\\n    embed chunk text -> vector (384-dim)\\n  Cache paper_id -> {chunk_id: embedding} as embeddings.pkl\\n\\nFor each question:\\n  embed question text -> query_vector\\n  Cache question_id -> query_vector\\n\\nNote: ~223 questions x avg 50 chunks/paper = ~11k embeddings total, fast on CPU\\n```\\n\\n## Step 3: EM Normalization Fix\\n\\n```\\n# QASPER official normalization from their evaluation script:\\ndef normalize_answer(s):\\n    s = s.lower()\\n    s = re.sub(r'\\\\b(a|an|the)\\\\b', ' ', s)  # remove articles\\n    s = re.sub(r'[^\\\\w\\\\s]', '', s)           # remove punctuation\\n    s = ' '.join(s.split())                  # normalize whitespace\\n    return s\\n\\ndef exact_match(pred, gold_list):\\n    pred_norm = normalize_answer(pred)\\n    return any(normalize_answer(g) == pred_norm for g in gold_list)\\n\\ndef token_f1(pred, gold_list):\\n    pred_tokens = normalize_answer(pred).split()\\n    best_f1 = 0\\n    for gold in gold_list:\\n        gold_tokens = normalize_answer(gold).split()\\n        common = Counter(pred_tokens) & Counter(gold_tokens)\\n        n_common = sum(common.values())\\n        if n_common == 0: continue\\n        prec = n_common / len(pred_tokens)\\n        rec = n_common / len(gold_tokens)\\n        f1 = 2*prec*rec/(prec+rec)\\n        best_f1 = max(best_f1, f1)\\n    return best_f1\\n\\n# gold_answer in output JSON may be a list (multiple valid answers) or\\n# a string - handle both cases. QASPER answers can be 'yes'/'no'/free text/list.\\n```\\n\\n## Step 4: MVT-RAG Core Implementation\\n\\n```python\\ndef cosine_sim(a, b):\\n    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)\\n\\ndef marginal_gain(chunk_emb, query_emb, retrieved_embs):\\n    query_sim = cosine_sim(chunk_emb, query_emb)\\n    if not retrieved_embs:\\n        novelty = 1.0\\n    else:\\n        max_sim_to_retrieved = max(cosine_sim(chunk_emb, r) for r in retrieved_embs)\\n        novelty = 1.0 - max_sim_to_retrieved\\n    return query_sim * novelty\\n\\ndef estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1):\\n    # top_n: number of top chunks per section to average\\n    section_scores = []\\n    for sec in sections:\\n        sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)\\n                for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]\\n        if not sims: continue\\n        top_sims = sorted(sims, reverse=True)[:top_n]\\n        section_scores.append(np.mean(top_sims))\\n    return np.mean(section_scores) if section_scores else 0.0\\n\\ndef mvt_retrieve(query_emb, sections, chunk_embeddings,\\n                 g_env_top_n=1, alpha=1.0, max_chunks=15):\\n    \\\"\\\"\\\"\\n    g_env_top_n: 1 (original), 3 (top-3), 5 (top-5)\\n    alpha: discount factor applied to G_env (0.7 = more permissive)\\n    Returns: list of retrieved chunk_ids in order\\n    \\\"\\\"\\\"\\n    g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=g_env_top_n)\\n    effective_threshold = alpha * g_env\\n\\n    # Score sections by best chunk similarity (for ordering)\\n    section_priority = []\\n    for sec in sections:\\n        sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)\\n                for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]\\n        best = max(sims) if sims else 0.0\\n        section_priority.append((best, sec))\\n    section_priority.sort(reverse=True)\\n\\n    retrieved_chunk_ids = []\\n    retrieved_embs = []\\n\\n    for _, sec in section_priority:\\n        # Within section, retrieve chunks in descending query similarity order\\n        chunks_sorted = sorted(\\n            sec['chunks'],\\n            key=lambda c: cosine_sim(chunk_embeddings.get(c['chunk_id'], np.zeros(384)), query_emb),\\n            reverse=True\\n        )\\n        for chunk in chunks_sorted:\\n            if len(retrieved_chunk_ids) >= max_chunks:\\n                return retrieved_chunk_ids\\n            cid = chunk['chunk_id']\\n            if cid not in chunk_embeddings:\\n                continue\\n            g_t = marginal_gain(chunk_embeddings[cid], query_emb, retrieved_embs)\\n            if g_t < effective_threshold:\\n                break  # switch to next section\\n            retrieved_chunk_ids.append(cid)\\n            retrieved_embs.append(chunk_embeddings[cid])\\n\\n    return retrieved_chunk_ids\\n```\\n\\n## Step 5: MVT-NoEnv Fixed-Threshold Ablation (CORRECTED)\\n\\n```python\\n# Pilot pass: compute actual G_env distribution across all validation questions\\n# using top-1 estimator, then use median as fixed threshold\\ndef compute_pilot_g_env(validation_questions, chunk_embeddings, query_embeddings):\\n    g_envs = []\\n    for q in validation_questions:\\n        sections = get_sections(q)\\n        query_emb = query_embeddings[q['question_id']]\\n        g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1)\\n        g_envs.append(g_env)\\n    return np.median(g_envs)  # use as fixed threshold for NoEnv ablation\\n\\n# MVT-NoEnv: same algorithm but threshold=fixed_threshold instead of per-question G_env\\ndef mvt_noenv_retrieve(query_emb, sections, chunk_embeddings, fixed_threshold, max_chunks=15):\\n    # Same as mvt_retrieve but g_env is replaced by fixed_threshold\\n    # (this is the correct ablation: no ecology-derived environment average)\\n    ...\\n```\\n\\n## Step 6: All Baselines\\n\\n```python\\n# Top-k dense retrieval: flatten all chunks for paper, sort by query cosine sim, take top k\\ndef topk_retrieve(query_emb, all_chunks, chunk_embeddings, k):\\n    sims = [(cosine_sim(chunk_embeddings[c['chunk_id']], query_emb), c['chunk_id'])\\n            for c in all_chunks if c['chunk_id'] in chunk_embeddings]\\n    sims.sort(reverse=True)\\n    return [cid for _, cid in sims[:k]]\\n\\n# Oracle: use gold evidence_chunk_ids directly (no retrieval error)\\ndef oracle_retrieve(gold_evidence_chunk_ids):\\n    return gold_evidence_chunk_ids\\n```\\n\\n## Step 7: LLM Answer Generation\\n\\n```python\\n# Via OpenRouter - use aii-openrouter-llms skill for setup\\n# Model: meta-llama/llama-3.1-8b-instruct\\n# Prompt template:\\nSYSTEM = \\\"You are a scientific QA assistant. Answer questions using ONLY the provided context. Be concise.\\\"\\n\\ndef build_prompt(question, chunks_text_list):\\n    context = '\\\\n\\\\n'.join([f'[Chunk {i+1}]: {t}' for i, t in enumerate(chunks_text_list)])\\n    return f\\\"Context:\\\\n{context}\\\\n\\\\nQuestion: {question}\\\\n\\\\nAnswer:\\\"\\n\\n# Cost tracking:\\n# llama-3.1-8b-instruct: ~$0.06/1M input tokens, $0.06/1M output tokens\\n# ~223 questions x 10 variants x avg 1500 input tokens = ~3.3M tokens = ~$0.20 total\\n# Very safe within $1.50 budget\\n\\n# IMPORTANT: If no chunks retrieved, use empty context fallback\\n# Track cost after each batch of 10 calls; stop if approaching $1.50\\n```\\n\\n## Step 8: Section Recall Metric\\n\\n```python\\ndef section_recall(retrieved_chunk_ids, gold_evidence_section_names, chunk_id_to_section):\\n    \\\"\\\"\\\"\\n    For multi-hop questions: what fraction of gold evidence sections\\n    have at least one retrieved chunk?\\n    \\\"\\\"\\\"\\n    retrieved_sections = set(chunk_id_to_section.get(cid) for cid in retrieved_chunk_ids)\\n    gold_sections = set(gold_evidence_section_names)\\n    if not gold_sections:\\n        return 1.0\\n    return len(retrieved_sections & gold_sections) / len(gold_sections)\\n```\\n\\n## Step 9: Full Experiment Loop\\n\\n```python\\nVARIANTS = [\\n    {'name': 'top-k-1',      'type': 'topk',   'k': 1},\\n    {'name': 'top-k-2',      'type': 'topk',   'k': 2},\\n    {'name': 'top-k-3',      'type': 'topk',   'k': 3},\\n    {'name': 'top-k-5',      'type': 'topk',   'k': 5},\\n    {'name': 'top-k-10',     'type': 'topk',   'k': 10},\\n    {'name': 'mvt-top1',     'type': 'mvt',    'g_env_top_n': 1, 'alpha': 1.0},  # original\\n    {'name': 'mvt-top3',     'type': 'mvt',    'g_env_top_n': 3, 'alpha': 1.0},  # FIX: multi-chunk\\n    {'name': 'mvt-top5',     'type': 'mvt',    'g_env_top_n': 5, 'alpha': 1.0},  # FIX: multi-chunk\\n    {'name': 'mvt-alpha0.7', 'type': 'mvt',    'g_env_top_n': 1, 'alpha': 0.7}, # FIX: discount\\n    {'name': 'mvt-noenv',    'type': 'mvt_noenv'},  # fixed threshold ablation\\n    {'name': 'oracle',       'type': 'oracle'},\\n]\\n\\nresults = []  # per-question results\\ncumulative_cost = 0.0\\n\\nfor q in validation_questions:  # ~223 questions\\n    question = q['input_parsed']['question']\\n    paper_sections = get_sections_for_paper(q)\\n    gold_answer = q['output_parsed']['gold_answer']  # may be list or string\\n    gold_chunk_ids = q['output_parsed']['evidence_chunk_ids']\\n    gold_section_names = q['output_parsed']['evidence_section_names']\\n    is_multihop = q['metadata_is_multihop']\\n    query_emb = embed(question)\\n\\n    q_result = {'question_id': q['metadata_question_id'],\\n                'is_multihop': is_multihop, 'variants': {}}\\n\\n    for variant in VARIANTS:\\n        # 1. Retrieve chunks\\n        if variant['type'] == 'topk':\\n            retrieved = topk_retrieve(query_emb, all_chunks, chunk_embs, variant['k'])\\n        elif variant['type'] == 'mvt':\\n            retrieved = mvt_retrieve(query_emb, paper_sections, chunk_embs,\\n                                     g_env_top_n=variant['g_env_top_n'],\\n                                     alpha=variant['alpha'])\\n        elif variant['type'] == 'mvt_noenv':\\n            retrieved = mvt_noenv_retrieve(query_emb, paper_sections, chunk_embs, fixed_threshold)\\n        else:  # oracle\\n            retrieved = gold_chunk_ids\\n\\n        # 2. Build context from retrieved chunks\\n        context_texts = [chunk_id_to_text[cid] for cid in retrieved if cid in chunk_id_to_text]\\n\\n        # 3. LLM answer generation\\n        if cumulative_cost >= 1.40:  # safety stop\\n            predicted_answer = '[BUDGET_EXCEEDED]'\\n        else:\\n            prompt = build_prompt(question, context_texts)\\n            predicted_answer, cost = call_openrouter(OPENROUTER_MODEL, prompt)\\n            cumulative_cost += cost\\n\\n        # 4. Compute metrics\\n        gold_list = gold_answer if isinstance(gold_answer, list) else [gold_answer]\\n        em = exact_match(predicted_answer, gold_list)\\n        f1 = token_f1(predicted_answer, gold_list)\\n        sec_rec = section_recall(retrieved, gold_section_names, chunk_id_to_section)\\n        n_chunks = len(retrieved)\\n\\n        q_result['variants'][variant['name']] = {\\n            'retrieved_chunk_ids': retrieved,\\n            'predicted_answer': predicted_answer,\\n            'em': em, 'f1': f1,\\n            'n_chunks_retrieved': n_chunks,\\n            'section_recall': sec_rec,\\n        }\\n\\n    results.append(q_result)\\n\\n# Aggregate metrics across all questions\\nfor variant_name in [v['name'] for v in VARIANTS]:\\n    avg_em = mean(r['variants'][variant_name]['em'] for r in results)\\n    avg_f1 = mean(r['variants'][variant_name]['f1'] for r in results)\\n    avg_chunks = mean(r['variants'][variant_name]['n_chunks_retrieved'] for r in results)\\n    avg_sec_rec = mean(r['variants'][variant_name]['section_recall'] for r in results)\\n    # Also compute for multihop subset\\n    multihop_results = [r for r in results if r['is_multihop']]\\n    ...\\n\\n# Bootstrap 95% CI for F1 differences (MVT vs top-k-5 as primary comparison)\\n# 10000 bootstrap samples with paired resampling\\n```\\n\\n## Step 10: Output\\n\\n```python\\nmethod_out = {\\n    'summary': {\\n        'n_questions': len(results),\\n        'n_multihop': sum(r['is_multihop'] for r in results),\\n        'total_cost_usd': cumulative_cost,\\n        'per_variant_aggregate': {\\n            variant_name: {\\n                'mean_em': ..., 'mean_f1': ...,\\n                'mean_chunks': ..., 'mean_section_recall': ...,\\n                'multihop_mean_f1': ..., 'multihop_mean_section_recall': ...\\n            }\\n        },\\n        'bootstrap_ci_mvt_top3_vs_topk5_f1': [lower, upper],\\n        'bootstrap_ci_mvt_alpha07_vs_topk5_f1': [lower, upper],\\n        'pilot_g_env_median': fixed_threshold,\\n    },\\n    'per_question': results  # full detail for analysis\\n}\\n\\nwith open('method_out.json', 'w') as f:\\n    json.dump(method_out, f, indent=2)\\n```\\n\\n## Key Implementation Notes\\n\\n1. **Data parsing**: The dependency dataset stores input/output as JSON strings—parse with `json.loads()`.\\n   `sections_summary` in the input JSON contains the full chunk list per section.\\n\\n2. **Embedding caching**: Save to `embeddings_cache.pkl` after first run. Check for cache file at start.\\n\\n3. **Gold answer format**: QASPER answers can be 'yes'/'no', extractive spans, or lists. The dataset\\n   artifact normalizes these; treat as list always.\\n\\n4. **EM=0 debug**: Before full run, spot-check 5 examples: print raw predicted answer, gold answers,\\n   and normalized versions. If all EM=0 even on oracle condition, the LLM prompt/parsing is broken.\\n\\n5. **Oracle F1 ceiling**: Oracle should achieve ~0.4-0.6 F1 on QASPER (known upper bound from literature).\\n   If oracle F1 < 0.3, the LLM call or answer parsing is likely broken—fix before full run.\\n\\n6. **Sections parsing**: The sections_summary is a list of section objects. Each section has `chunks`\\n   list. Re-group by `normalized_section` name to get IMRaD categories.\\n\\n7. **Papers with few sections**: If a paper has only 1-2 sections, MVT switching is trivial.\\n   These are excluded by the dataset (>=3 distinct sections filter) but verify at runtime.\\n\\n8. **OpenRouter setup**: Use the aii-openrouter-llms skill to get the API key and call pattern.\\n   All calls must go through OpenRouter—no direct Anthropic/OpenAI endpoints.\",\n  \"fallback_plan\": \"## Primary Fallback: Reduce LLM calls\\n\\nIf cost is tracking high (>$0.80 after 100 questions), reduce variants by dropping top-k-10 and oracle, which are less critical for the core hypothesis. Run 5 core variants: top-k-1, top-k-3, top-k-5, mvt-top3, mvt-alpha0.7.\\n\\n## Secondary Fallback: Skip LLM, use retrieval-only metrics\\n\\nIf OpenRouter is unavailable or budget is too tight, skip LLM generation entirely and report only:\\n- Retrieval precision/recall (gold evidence chunks retrieved)\\n- Section recall\\n- N chunks retrieved per question\\n\\nThese metrics directly test the core hypothesis (does multi-chunk G_env improve retrieval quality?) without needing generation. Report retrieval F1 (did we retrieve the right chunks?) instead of answer F1.\\n\\n## Embedding Fallback\\n\\nIf sentence-transformers is slow on CPU, use `paraphrase-MiniLM-L3-v2` (smaller/faster) or TF-IDF cosine similarity as a zero-dependency alternative. TF-IDF is much faster and still captures keyword overlap.\\n\\n## Data Fallback\\n\\nIf sections_summary doesn't contain full chunk text (parse error), fall back to re-loading QASPER directly from HuggingFace (`allenai/qasper`, validation split) and re-parsing sections inline using the same logic as the dataset artifact's data.py.\\n\\n## Truncation Fallback\\n\\nIf 223 questions take too long (>5h with embeddings+LLM), run on 100 questions (first 50 single-hop + first 50 multihop) and report results on that subset with a note.\",\n  \"testing_plan\": \"## Step 0: Verify Data Loading (5 min)\\n\\n```python\\nimport json\\ndata = json.load(open(DEP_DATA))\\nvalidation = [x for x in data if x['metadata_fold'] == 1]\\nprint(f'Validation size: {len(validation)}')\\nprint('First example input keys:', json.loads(validation[0]['input']).keys())\\nprint('First example output keys:', json.loads(validation[0]['output']).keys())\\nprint('Is multihop distribution:', sum(x['metadata_is_multihop'] for x in validation))\\n```\\nExpect: ~223 validation examples, input has question+sections_summary, output has gold_answer+evidence_chunk_ids.\\n\\n## Step 1: Mini smoke test on 5 examples (15 min)\\n\\nRun ALL variants on 5 questions (mix of single-hop and multihop).\\n- Check embeddings work: cosine sims in [0.0, 1.0] range\\n- Check G_env estimation produces non-zero values\\n- Check MVT retrieves between 1-15 chunks (not always 0 or 15)\\n- Check oracle retrieves the correct chunk IDs\\n- Check LLM returns non-empty string (1 LLM call to verify API)\\n- Check EM normalization: manually verify normalized predicted vs gold for 2 examples\\n- Print per-example summary table: variant | n_chunks | f1 | em\\n\\n## Step 2: EM debug check (5 min)\\n\\nFor oracle condition on 5 examples:\\n- Print raw LLM output\\n- Print gold_answer\\n- Print normalize(pred) vs normalize(gold)\\n- If EM=0 for oracle on obvious 'yes'/'no' answers, fix normalization\\n- Target: oracle F1 >= 0.30 on 5-example sample\\n\\n## Step 3: Embedding cache check (2 min)\\n\\nAfter first mini run, verify `embeddings_cache.pkl` exists and reload correctly. Second mini run should be faster.\\n\\n## Step 4: 50-question validation run (30 min)\\n\\nRun all variants on 50 questions before full 223.\\n- Verify cost tracking: cumulative_cost after 50q x 10 variants should be ~$0.40\\n- Verify multihop questions are present (should be ~17 of 50)\\n- Check aggregate F1 table looks reasonable: oracle > top-k-5 > top-k-1\\n- If top-k-5 F1 is still ~0.190 (matching iter1), data pipeline is consistent\\n- Check mvt-top3 F1 vs mvt-top1 F1: expect improvement (this is the core hypothesis)\\n\\n## Full run completion signals\\n\\n- Oracle F1 >= 0.35 (literature upper bound for 8B model on QASPER is ~0.40-0.50)\\n- Top-k-5 F1 ~0.17-0.22 (within range of published results)\\n- MVT-top3 retrieves more chunks than MVT-top1 (G_env reduced → less aggressive switching)\\n- Bootstrap CI for MVT-top3 vs top-k-5 F1: check whether CI excludes zero (confirms hypothesis)\\n- Cost <= $1.00 total\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [6] ASSISTANT · 2026-07-18 16:29:05 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json`. The plan covers all 11 variants (top-k-1/2/3/5/10, mvt-top1/top3/top5/alpha0.7, mvt-noenv fixed-threshold ablation, oracle), the EM normalization fix using QASPER's official tokenization, G_env multi-chunk estimator implementation, section-recall metric for multihop questions, cost-tracked OpenRouter calls (~$0.20 estimated), and a mini→50q→223q scaling test sequence.
```
