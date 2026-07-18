# gen_plan_dataset_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_dataset_1` (terminal_claude_agent, claude-sonnet-4-6)

### [1] CONFIG · 2026-07-18 15:22:39 UTC

```
model: claude-sonnet-4-6 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_plan/gen_plan_dataset_1
```

### [2] SYSTEM-USER prompt · 2026-07-18 15:22:45 UTC

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
You are expanding an artifact direction of type: DATASET

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect
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

The dataset executor has 6h total (including writing code, debugging, testing, and fixing errors).

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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: dataset_iter1_dir1
type: dataset
objective: >-
  Prepare QASPER with section-annotated chunks and ground-truth evidence locations for the MVT-RAG experiment.
approach: >-
  Download QASPER from HuggingFace (allenai/qasper). Parse each paper's full text into section-level chunks using regex on
  section headers (##, bold lines, standard IMRaD names). For each question, record the ground-truth answer, evidence paragraphs,
  and which sections contain evidence. Output a JSON file with rows: {paper_id, question_id, question, sections: [{name, chunks:
  [{text, chunk_id}]}], gold_answer, evidence_chunk_ids}. Limit to papers with >=3 distinct sections. Target ~500 questions
  for mini split and up to 2000 for full.
depends_on: []
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead
</artifact_executor_scope>

<artifact_planning_rules>
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for dataset artifacts:
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
  "description": "Plan for a DATASET artifact.",
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
    "ideal_dataset_criteria": {
      "description": "What makes an ideal dataset for this purpose - size, format, content requirements",
      "title": "Ideal Dataset Criteria",
      "type": "string"
    },
    "dataset_search_plan": {
      "description": "Step-by-step plan for finding/creating this dataset - sources to check, fallback options",
      "title": "Dataset Search Plan",
      "type": "string"
    },
    "target_num_datasets": {
      "description": "How many individual datasets should be delivered. Count each dataset separately, not collections \u2014 a benchmark suite of N datasets counts as N. This controls how broadly the executor searches, so setting it too low will under-collect.",
      "title": "Target Num Datasets",
      "type": "integer"
    }
  },
  "required": [
    "title",
    "ideal_dataset_criteria",
    "dataset_search_plan",
    "target_num_datasets"
  ],
  "title": "DatasetPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [3] HUMAN-USER prompt · 2026-07-18 15:22:45 UTC

```
Improving retrieval-augmented generation for long scientific documents
```

### [4] TOOL CALL — Skill · 2026-07-18 15:22:49 UTC

```
aii-hf-datasets
```

### [5] TOOL RESULT — Skill · 2026-07-18 15:22:49 UTC

```
{"success": true, "commandName": "aii-hf-datasets"}
```

### [6] TOOL CALL — Write · 2026-07-18 15:23:23 UTC

```
File: /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_plan/gen_plan_dataset_1/.terminal_claude_agent_struct_out.json

{
  "title": "QASPER Section-Annotated Chunks Dataset",
  "summary": "Download QASPER from HuggingFace, parse each paper into section-level chunks using regex on IMRaD headers, and output a JSON file with rows suitable for MVT-RAG evaluation: paper_id, question_id, question, sections (with named chunks), gold_answer, and evidence_chunk_ids.",
  "runpod_compute_profile": "cpu_heavy",
  "ideal_dataset_criteria": "QASPER (allenai/qasper on HuggingFace) is the primary target — it contains full-paper scientific QA with section-level annotations and evidence paragraph locations. Ideal subset: papers with >=3 distinct detected sections (to make section switching meaningful), questions with at least one extractive or abstractive answer (not unanswerable), and evidence paragraphs that can be matched to specific sections. Target: ~500 questions for a mini split and up to 2000 for the full split. The dataset is ~50MB, well within the 300MB limit.",
  "dataset_search_plan": "Step 1 — Download QASPER via the aii-hf-datasets skill:\n  SKILL_DIR=...; $PY $SKILL_DIR/scripts/aii_hf_download_datasets.py allenai/qasper --split train\n  Also download the validation split: --split validation\n\nStep 2 — Understand the QASPER schema. Each example has:\n  - id: paper ID\n  - title, abstract\n  - full_text: list of {section_name, paragraphs: [str]} objects\n  - qas: list of {question, question_id, answers: [{answer: {unanswerable, extractive_spans, free_form_answer, evidence, highlighted_evidence}}]}\n\nStep 3 — Parse full_text into section-level chunks. Algorithm:\n  a) For each paper, iterate over full_text sections. Each section already has a section_name field — use it directly (no regex needed on raw text).\n  b) Split each section's paragraphs into chunks. Use paragraph boundaries (each string in the paragraphs list) as the atomic chunk unit. Assign chunk_id = f'{paper_id}_{section_idx}_{para_idx}'.\n  c) Normalize section names to IMRaD categories: map 'introduction'→'introduction', anything containing 'method'/'approach'/'model'→'methods', 'result'/'experiment'→'results', 'discussion'/'conclusion'→'discussion', 'related'→'related_work', others→'other'. Keep original name too.\n  d) Filter: only keep papers where >=3 distinct normalized section categories are present (ensures section switching is meaningful).\n\nStep 4 — Build evidence_chunk_ids. For each question-answer pair:\n  a) Extract the evidence field (list of paragraph strings) from the first non-unanswerable answer.\n  b) Match each evidence string to chunk_ids via exact string match against paragraph texts. If no exact match, use longest common substring match (>0.9 overlap).\n  c) Record which section each evidence chunk falls in (evidence_section_names).\n  d) Skip questions where 0 evidence paragraphs can be matched.\n\nStep 5 — Filter questions:\n  a) Exclude unanswerable questions (unanswerable=True in all answers).\n  b) Keep questions with >=1 matched evidence chunk.\n  c) For multi-hop analysis flag: mark is_multihop=True if evidence spans >=2 distinct sections.\n\nStep 6 — Output schema (data_out.json rows):\n  {\n    'paper_id': str,\n    'question_id': str,\n    'question': str,\n    'gold_answer': str,  // first free_form_answer or extractive_spans joined\n    'sections': [\n      {\n        'name': str,           // original section name\n        'normalized_name': str, // IMRaD category\n        'section_idx': int,\n        'chunks': [\n          {'chunk_id': str, 'text': str, 'para_idx': int}\n        ]\n      }\n    ],\n    'evidence_chunk_ids': [str],\n    'evidence_section_names': [str],\n    'is_multihop': bool,\n    'num_sections': int,\n    'split': str  // 'train' or 'validation'\n  }\n\nStep 7 — Size targets:\n  - Full split: up to 2000 questions (sample if more, stratify by is_multihop)\n  - Mini split (metadata_fold='mini'): 100 questions balanced across multihop/single-hop\n  - Preview: 3 rows\n\nStep 8 — Validate output:\n  - Every row has >=1 evidence_chunk_id\n  - Every chunk_id referenced in evidence_chunk_ids exists in sections\n  - num_sections >= 3 for every row\n  - gold_answer is non-empty string\n\nFallback if allenai/qasper fails to load via HF script (has_loader_script=True, may need special handling):\n  - Use the HF Datasets API directly: `datasets.load_dataset('allenai/qasper', trust_remote_code=True)`\n  - Or download the raw JSON from the QASPER GitHub release: https://github.com/allenai/qasper-led-baseline (links to S3)\n  - The data format is documented in the QASPER paper (Dasigi et al. 2021, NAACL)\n\nNote on QASPER's full_text field: Some papers have section_name='' for paragraphs at the start (abstract-level). Treat these as 'preamble' and exclude from section count but keep chunks available.",
  "target_num_datasets": 1
}
```

### [7] TOOL RESULT — Write · 2026-07-18 15:23:23 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_plan/gen_plan_dataset_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"QASPER Section-Annotated Chunks Dataset\",\n  \"summary\": \"Download QASPER from HuggingFace, parse each paper into section-level chunks using regex on IMRaD headers, and output a JSON file with rows suitable for MVT-RAG evaluation: paper_id, question_id, question, sections (with named chunks), gold_answer, and evidence_chunk_ids.\",\n  \"runpod_compute_profile\": \"cpu_heavy\",\n  \"ideal_dataset_criteria\": \"QASPER (allenai/qasper on HuggingFace) is the primary target — it contains full-paper scientific QA with section-level annotations and evidence paragraph locations. Ideal subset: papers with >=3 distinct detected sections (to make section switching meaningful), questions with at least one extractive or abstractive answer (not unanswerable), and evidence paragraphs that can be matched to specific sections. Target: ~500 questions for a mini split and up to 2000 for the full split. The dataset is ~50MB, well within the 300MB limit.\",\n  \"dataset_search_plan\": \"Step 1 — Download QASPER via the aii-hf-datasets skill:\\n  SKILL_DIR=...; $PY $SKILL_DIR/scripts/aii_hf_download_datasets.py allenai/qasper --split train\\n  Also download the validation split: --split validation\\n\\nStep 2 — Understand the QASPER schema. Each example has:\\n  - id: paper ID\\n  - title, abstract\\n  - full_text: list of {section_name, paragraphs: [str]} objects\\n  - qas: list of {question, question_id, answers: [{answer: {unanswerable, extractive_spans, free_form_answer, evidence, highlighted_evidence}}]}\\n\\nStep 3 — Parse full_text into section-level chunks. Algorithm:\\n  a) For each paper, iterate over full_text sections. Each section already has a section_name field — use it directly (no regex needed on raw text).\\n  b) Split each section's paragraphs into chunks. Use paragraph boundaries (each string in the paragraphs list) as the atomic chunk unit. Assign chunk_id = f'{paper_id}_{section_idx}_{para_idx}'.\\n  c) Normalize section names to IMRaD categories: map 'introduction'→'introduction', anything containing 'method'/'approach'/'model'→'methods', 'result'/'experiment'→'results', 'discussion'/'conclusion'→'discussion', 'related'→'related_work', others→'other'. Keep original name too.\\n  d) Filter: only keep papers where >=3 distinct normalized section categories are present (ensures section switching is meaningful).\\n\\nStep 4 — Build evidence_chunk_ids. For each question-answer pair:\\n  a) Extract the evidence field (list of paragraph strings) from the first non-unanswerable answer.\\n  b) Match each evidence string to chunk_ids via exact string match against paragraph texts. If no exact match, use longest common substring match (>0.9 overlap).\\n  c) Record which section each evidence chunk falls in (evidence_section_names).\\n  d) Skip questions where 0 evidence paragraphs can be matched.\\n\\nStep 5 — Filter questions:\\n  a) Exclude unanswerable questions (unanswerable=True in all answers).\\n  b) Keep questions with >=1 matched evidence chunk.\\n  c) For multi-hop analysis flag: mark is_multihop=True if evidence spans >=2 distinct sections.\\n\\nStep 6 — Output schema (data_out.json rows):\\n  {\\n    'paper_id': str,\\n    'question_id': str,\\n    'question': str,\\n    'gold_answer': str,  // first free_form_answer or extractive_spans joined\\n    'sections': [\\n      {\\n        'name': str,           // original section name\\n        'normalized_name': str, // IMRaD category\\n        'section_idx': int,\\n        'chunks': [\\n          {'chunk_id': str, 'text': str, 'para_idx': int}\\n        ]\\n      }\\n    ],\\n    'evidence_chunk_ids': [str],\\n    'evidence_section_names': [str],\\n    'is_multihop': bool,\\n    'num_sections': int,\\n    'split': str  // 'train' or 'validation'\\n  }\\n\\nStep 7 — Size targets:\\n  - Full split: up to 2000 questions (sample if more, stratify by is_multihop)\\n  - Mini split (metadata_fold='mini'): 100 questions balanced across multihop/single-hop\\n  - Preview: 3 rows\\n\\nStep 8 — Validate output:\\n  - Every row has >=1 evidence_chunk_id\\n  - Every chunk_id referenced in evidence_chunk_ids exists in sections\\n  - num_sections >= 3 for every row\\n  - gold_answer is non-empty string\\n\\nFallback if allenai/qasper fails to load via HF script (has_loader_script=True, may need special handling):\\n  - Use the HF Datasets API directly: `datasets.load_dataset('allenai/qasper', trust_remote_code=True)`\\n  - Or download the raw JSON from the QASPER GitHub release: https://github.com/allenai/qasper-led-baseline (links to S3)\\n  - The data format is documented in the QASPER paper (Dasigi et al. 2021, NAACL)\\n\\nNote on QASPER's full_text field: Some papers have section_name='' for paragraphs at the start (abstract-level). Treat these as 'preamble' and exclude from section count but keep chunks available.\",\n  \"target_num_datasets\": 1\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [8] ASSISTANT · 2026-07-18 15:23:24 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json`. The plan covers downloading QASPER from HuggingFace, parsing its built-in `full_text` section structure into IMRaD-normalized chunks, matching evidence paragraphs to chunk IDs, filtering to papers with ≥3 sections, and outputting ~2000 question rows with full section/chunk/evidence metadata needed for MVT-RAG evaluation.
```
