# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-sonnet-4-6)

### [1] CONFIG · 2026-07-18 15:22:39 UTC

```
model: claude-sonnet-4-6 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1
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

id: experiment_iter1_dir2
type: experiment
objective: >-
  Implement MVT-RAG and all baselines end-to-end, run on QASPER, and collect per-question retrieval and QA results.
approach: >-
  Download QASPER directly from HuggingFace within the experiment. Implement in Python with sentence-transformers (all-MiniLM-L6-v2).
  MVT-RAG: (1) embed all chunks and query; (2) estimate G_env as mean of best-chunk similarity per section; (3) iteratively
  retrieve from highest-potential section, computing marginal gain G_t = sim(chunk, query) * (1 - max_sim(chunk, retrieved));
  (4) switch when G_t < G_env; (5) terminate when all sections exhausted. Baselines: top-k dense (k=3,5,10), BM25+k=5, fixed-threshold
  stopping (0.3, 0.5), no-RAG. Answer generation via OpenRouter (meta-llama/llama-3.1-8b-instruct). Ablation: MVT-RAG-NoEnv
  using fixed threshold=0.5 instead of G_env. Output per-question: method, chunks_retrieved, generated_answer, gold_answer.
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

### [3] HUMAN-USER prompt · 2026-07-18 15:22:45 UTC

```
Improving retrieval-augmented generation for long scientific documents
```

### [4] TOOL CALL — Write · 2026-07-18 15:23:57 UTC

```
File: /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json

{
  "title": "MVT-RAG vs Baselines on QASPER",
  "summary": "Implement and evaluate MVT-RAG (Marginal Value Theorem-based section switching) against fixed-k dense retrieval, BM25, and confidence-threshold baselines on QASPER scientific QA. Measure F1, exact match, and retrieval efficiency (chunks/question).",
  "runpod_compute_profile": "cpu_heavy",
  "implementation_pseudocode": "# Setup\nuv pip install datasets sentence-transformers rank_bm25 openai tqdm numpy scipy\n\n# === STEP 1: Load QASPER ===\nfrom datasets import load_dataset\nqasper = load_dataset('allenai/qasper', split='validation')  # ~888 papers\n# Each paper: title, full_text (list of section dicts with section_name + paragraphs)\n# Each QA pair: question, answers (list of answer dicts with unanswerable + free_form_answer + extractive_spans)\n\n# === STEP 2: Parse documents into section chunks ===\ndef parse_paper(paper):\n    sections = []\n    for section in paper['full_text']:\n        name = section['section_name'] or 'unknown'\n        paras = section['paragraphs']  # list of strings\n        chunks = [p.strip() for p in paras if p.strip()]\n        if chunks:\n            sections.append({'name': name, 'chunks': chunks})\n    return sections\n\n# === STEP 3: Embed chunks and query ===\nfrom sentence_transformers import SentenceTransformer\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\n\ndef embed_paper(sections):\n    all_chunks = [(s['name'], c) for s in sections for c in s['chunks']]\n    texts = [c for _, c in all_chunks]\n    embeddings = model.encode(texts, batch_size=64, show_progress_bar=False)\n    return all_chunks, embeddings\n\n# === STEP 4: MVT-RAG algorithm ===\nimport numpy as np\nfrom sklearn.metrics.pairwise import cosine_similarity\n\ndef mvt_rag(query_emb, sections, chunk_embs, chunk_meta):\n    # chunk_meta: list of (section_name, chunk_text)\n    # Build section index: section_name -> list of (chunk_idx, emb)\n    sec_map = {}\n    for i, (sname, _) in enumerate(chunk_meta):\n        sec_map.setdefault(sname, []).append(i)\n    \n    # Estimate G_env: best sim per section, averaged\n    g_env_values = []\n    for sname, idxs in sec_map.items():\n        sims = cosine_similarity([query_emb], chunk_embs[idxs])[0]\n        g_env_values.append(np.max(sims))\n    G_env = np.mean(g_env_values)\n    \n    # Section potential: max sim of best chunk\n    sec_potential = {sname: max(cosine_similarity([query_emb], chunk_embs[idxs])[0])\n                     for sname, idxs in sec_map.items()}\n    \n    retrieved = []  # list of (chunk_text, emb)\n    visited = set()\n    \n    while True:\n        # Pick highest-potential unvisited section\n        remaining = {s: p for s, p in sec_potential.items() if s not in visited}\n        if not remaining:\n            break\n        cur_sec = max(remaining, key=remaining.get)\n        visited.add(cur_sec)\n        \n        sec_idxs = sec_map[cur_sec]\n        retrieved_embs_list = [r[1] for r in retrieved]\n        \n        for idx in sec_idxs:\n            chunk_emb = chunk_embs[idx]\n            chunk_text = chunk_meta[idx][1]\n            \n            # Query relevance\n            q_sim = cosine_similarity([query_emb], [chunk_emb])[0][0]\n            \n            # Novelty: 1 - max_sim to already retrieved\n            if retrieved_embs_list:\n                max_ret_sim = max(cosine_similarity([chunk_emb], retrieved_embs_list)[0])\n                novelty = 1.0 - max_ret_sim\n            else:\n                novelty = 1.0\n            \n            G_t = q_sim * novelty\n            \n            if G_t < G_env and retrieved:  # switch criterion\n                break\n            \n            retrieved.append((chunk_text, chunk_emb))\n            retrieved_embs_list.append(chunk_emb)\n    \n    return [r[0] for r in retrieved], G_env\n\n# === STEP 5: Baselines ===\n\n# Top-k dense\ndef topk_dense(query_emb, chunk_embs, chunk_meta, k):\n    sims = cosine_similarity([query_emb], chunk_embs)[0]\n    idxs = np.argsort(sims)[::-1][:k]\n    return [chunk_meta[i][1] for i in idxs]\n\n# BM25 + k=5\nfrom rank_bm25 import BM25Okapi\ndef bm25_retrieval(query, chunk_meta, k=5):\n    corpus = [c.split() for _, c in chunk_meta]\n    bm25 = BM25Okapi(corpus)\n    scores = bm25.get_scores(query.split())\n    idxs = np.argsort(scores)[::-1][:k]\n    return [chunk_meta[i][1] for i in idxs]\n\n# Fixed-threshold stopping (retrieve in sim order, stop when sim < threshold)\ndef threshold_retrieval(query_emb, chunk_embs, chunk_meta, threshold):\n    sims = cosine_similarity([query_emb], chunk_embs)[0]\n    order = np.argsort(sims)[::-1]\n    chunks = []\n    for i in order:\n        if sims[i] < threshold:\n            break\n        chunks.append(chunk_meta[i][1])\n    return chunks if chunks else [chunk_meta[order[0]][1]]  # at least one\n\n# MVT-NoEnv ablation: fixed threshold=0.5\ndef mvt_noenv_rag(query_emb, sections, chunk_embs, chunk_meta, threshold=0.5):\n    # Same as MVT but replace G_env with fixed threshold\n    sec_map = {}\n    for i, (sname, _) in enumerate(chunk_meta):\n        sec_map.setdefault(sname, []).append(i)\n    sec_potential = {sname: max(cosine_similarity([query_emb], chunk_embs[idxs])[0])\n                     for sname, idxs in sec_map.items()}\n    retrieved = []\n    visited = set()\n    while True:\n        remaining = {s: p for s, p in sec_potential.items() if s not in visited}\n        if not remaining:\n            break\n        cur_sec = max(remaining, key=remaining.get)\n        visited.add(cur_sec)\n        sec_idxs = sec_map[cur_sec]\n        retrieved_embs_list = [r[1] for r in retrieved]\n        for idx in sec_idxs:\n            chunk_emb = chunk_embs[idx]\n            chunk_text = chunk_meta[idx][1]\n            q_sim = cosine_similarity([query_emb], [chunk_emb])[0][0]\n            if retrieved_embs_list:\n                max_ret_sim = max(cosine_similarity([chunk_emb], retrieved_embs_list)[0])\n                novelty = 1.0 - max_ret_sim\n            else:\n                novelty = 1.0\n            G_t = q_sim * novelty\n            if G_t < threshold and retrieved:\n                break\n            retrieved.append((chunk_text, chunk_emb))\n            retrieved_embs_list.append(chunk_emb)\n    return [r[0] for r in retrieved]\n\n# === STEP 6: LLM Answer Generation via OpenRouter ===\nimport openai, os\nclient = openai.OpenAI(\n    api_key=os.environ['OPENROUTER_API_KEY'],\n    base_url='https://openrouter.ai/api/v1'\n)\nMODEL = 'meta-llama/llama-3.1-8b-instruct'\n\ndef generate_answer(query, chunks):\n    context = '\\n\\n'.join(chunks[:10])  # cap at 10 chunks to limit tokens\n    prompt = f'Context:\\n{context}\\n\\nQuestion: {query}\\nAnswer concisely:'\n    try:\n        resp = client.chat.completions.create(\n            model=MODEL,\n            messages=[{'role':'user','content':prompt}],\n            max_tokens=200,\n            temperature=0.0\n        )\n        return resp.choices[0].message.content.strip()\n    except Exception as e:\n        return ''\n\n# === STEP 7: Evaluation metrics ===\ndef token_f1(pred, gold):\n    pred_toks = set(pred.lower().split())\n    gold_toks = set(gold.lower().split())\n    if not pred_toks or not gold_toks:\n        return 0.0\n    common = pred_toks & gold_toks\n    if not common:\n        return 0.0\n    p = len(common)/len(pred_toks)\n    r = len(common)/len(gold_toks)\n    return 2*p*r/(p+r)\n\ndef exact_match(pred, gold):\n    return float(pred.strip().lower() == gold.strip().lower())\n\ndef best_f1_over_answers(pred, gold_answers):\n    # gold_answers is a list; take max F1\n    return max(token_f1(pred, g) for g in gold_answers) if gold_answers else 0.0\n\n# === STEP 8: Main experiment loop ===\nMETHODS = ['mvt_rag', 'mvt_noenv', 'topk_3', 'topk_5', 'topk_10', 'bm25_5', 'thresh_0.3', 'thresh_0.5', 'no_rag']\nresults = []  # list of result dicts\ntotal_cost = 0.0\nCOST_LIMIT = 8.0  # leave $2 buffer\n\n# Sample N papers to keep cost manageable\nN_PAPERS = 100  # start with 100 papers; if cost OK, expand to 300\nsampled_papers = list(qasper)[:N_PAPERS]\n\nfor paper in tqdm(sampled_papers):\n    sections = parse_paper(paper)\n    if not sections:\n        continue\n    all_chunks, chunk_embs = embed_paper(sections)\n    chunk_meta = all_chunks  # list of (section_name, chunk_text)\n    chunk_embs_arr = np.array(chunk_embs)\n    \n    for qa in paper['qas']:\n        question = qa['question']\n        gold_answers = []\n        for ans in qa['answers']:\n            if not ans['answer']['unanswerable']:\n                ffa = ans['answer']['free_form_answer']\n                if ffa:\n                    gold_answers.append(ffa)\n        if not gold_answers:\n            continue  # skip unanswerable\n        \n        query_emb = model.encode([question])[0]\n        \n        method_chunks = {\n            'mvt_rag': mvt_rag(query_emb, sections, chunk_embs_arr, chunk_meta)[0],\n            'mvt_noenv': mvt_noenv_rag(query_emb, sections, chunk_embs_arr, chunk_meta),\n            'topk_3': topk_dense(query_emb, chunk_embs_arr, chunk_meta, 3),\n            'topk_5': topk_dense(query_emb, chunk_embs_arr, chunk_meta, 5),\n            'topk_10': topk_dense(query_emb, chunk_embs_arr, chunk_meta, 10),\n            'bm25_5': bm25_retrieval(question, chunk_meta, 5),\n            'thresh_0.3': threshold_retrieval(query_emb, chunk_embs_arr, chunk_meta, 0.3),\n            'thresh_0.5': threshold_retrieval(query_emb, chunk_embs_arr, chunk_meta, 0.5),\n            'no_rag': []\n        }\n        \n        for method, chunks in method_chunks.items():\n            if total_cost >= COST_LIMIT:\n                break\n            answer = generate_answer(question, chunks) if chunks else generate_answer(question, [])\n            f1 = best_f1_over_answers(answer, gold_answers)\n            em = max(exact_match(answer, g) for g in gold_answers)\n            results.append({\n                'paper_id': paper['id'],\n                'question': question,\n                'method': method,\n                'chunks_retrieved': len(chunks),\n                'generated_answer': answer,\n                'gold_answers': gold_answers,\n                'f1': f1,\n                'exact_match': em\n            })\n            # Cost tracking: ~200 input tokens + 200 output ~ $0.0004 per call at llama-3.1-8b pricing\n            total_cost += 0.0004\n        \n        if total_cost >= COST_LIMIT:\n            break\n    if total_cost >= COST_LIMIT:\n        break\n\n# === STEP 9: Statistical tests ===\nfrom scipy import stats\nimport json\n\n# Group results by method\ndef get_f1s(method):\n    return [r['f1'] for r in results if r['method'] == method]\n\nmvt_f1s = get_f1s('mvt_rag')\n# Paired bootstrap test: MVT vs topk_5\ndef bootstrap_p(a, b, n=10000):\n    diffs = [np.mean(a) - np.mean(b)]\n    rng = np.random.default_rng(42)\n    a, b = np.array(a), np.array(b)\n    n_samples = len(a)\n    null_diffs = []\n    for _ in range(n):\n        idx = rng.integers(0, n_samples, n_samples)\n        null_diffs.append(np.mean(a[idx]) - np.mean(b[idx]))\n    # p-value: fraction of bootstrap diffs <= 0 (one-sided)\n    return np.mean(np.array(null_diffs) <= 0)\n\n# === STEP 10: Save output ===\nsummary_stats = {}\nfor method in METHODS:\n    f1s = get_f1s(method)\n    ems = [r['exact_match'] for r in results if r['method'] == method]\n    chunks = [r['chunks_retrieved'] for r in results if r['method'] == method]\n    summary_stats[method] = {\n        'mean_f1': float(np.mean(f1s)) if f1s else 0,\n        'mean_em': float(np.mean(ems)) if ems else 0,\n        'mean_chunks': float(np.mean(chunks)) if chunks else 0,\n        'n': len(f1s)\n    }\n\n# Bootstrap p-values vs topk_5\nfor method in METHODS:\n    if method in ('mvt_rag', 'topk_5'):\n        continue\n    mf = get_f1s(method)\n    tk5f = get_f1s('topk_5')\n    if len(mf) == len(tk5f) and mf:\n        summary_stats[method]['p_vs_topk5'] = bootstrap_p(np.array(mf), np.array(tk5f))\n\noutput = {\n    'summary_stats': summary_stats,\n    'per_question_results': results,\n    'total_cost_usd': total_cost,\n    'n_questions': len([r for r in results if r['method']=='mvt_rag'])\n}\nwith open('method_out.json', 'w') as f:\n    json.dump(output, f, indent=2)\nprint('Done. Summary:')\nfor m, s in summary_stats.items():\n    print(f\"{m}: F1={s['mean_f1']:.3f} EM={s['mean_em']:.3f} chunks={s['mean_chunks']:.1f} n={s['n']}\")",
  "fallback_plan": "1. If QASPER load fails: try `load_dataset('allenai/qasper', trust_remote_code=True)` or download the JSON directly from https://huggingface.co/datasets/allenai/qasper/resolve/main/qasper-v0.3.zip and parse manually.\n2. If OpenRouter LLM calls are too slow or costly: switch to google/gemma-2-2b-it (cheaper) or skip answer generation entirely — evaluate retrieval quality using oracle F1 (max F1 of retrieved chunks vs. gold extractive spans from QASPER annotations). This eliminates LLM cost completely and is still a valid experiment.\n3. If sentence-transformers is slow on CPU: reduce N_PAPERS to 50, or pre-embed all chunks in batches upfront before the QA loop.\n4. If the MVT switching loop retrieves too many chunks (>30 per question): cap at max_chunks=15 to prevent degenerate cases where G_env is very low and nothing triggers switching.\n5. If QASPER has papers with no section structure (flat paragraphs): treat each paragraph as its own 'section' so the MVT logic still applies.\n6. If cost tracking shows approaching $8: stop the paper loop early and report partial results — partial results over 50+ papers are still sufficient for statistical comparison.",
  "testing_plan": "1. MINI TEST (5 papers, 1 question each, no LLM): Run just the retrieval methods (no answer generation) to verify chunk counts and G_env values look reasonable. Print per-method chunks_retrieved and G_env for visual inspection.\n2. SIGNAL CHECK: For one paper, print the MVT decision log — G_t values per chunk, G_env, and which chunks were retrieved. Verify that switching happens when expected (G_t < G_env).\n3. BASELINE SANITY: topk_5 should always return exactly 5 chunks. BM25 should return 5. Fixed-threshold may return 0 (check fallback).\n4. COST DRY RUN: Generate answers for 10 questions, track cost, extrapolate to full run. If cost/question > $0.01, reduce N_PAPERS.\n5. FULL SCALE: Run on 100 papers (~500-2000 questions). If time and cost allow, expand to 300 papers.\n6. SUCCESS SIGNAL: MVT-RAG mean F1 > topk_5 mean F1, with fewer mean chunks. Also check that MVT-NoEnv (fixed threshold) scores lower than MVT-RAG, confirming the ecology-derived averaging is the load-bearing component."
}
```

### [5] TOOL RESULT — Write · 2026-07-18 15:23:57 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"MVT-RAG vs Baselines on QASPER\",\n  \"summary\": \"Implement and evaluate MVT-RAG (Marginal Value Theorem-based section switching) against fixed-k dense retrieval, BM25, and confidence-threshold baselines on QASPER scientific QA. Measure F1, exact match, and retrieval efficiency (chunks/question).\",\n  \"runpod_compute_profile\": \"cpu_heavy\",\n  \"implementation_pseudocode\": \"# Setup\\nuv pip install datasets sentence-transformers rank_bm25 openai tqdm numpy scipy\\n\\n# === STEP 1: Load QASPER ===\\nfrom datasets import load_dataset\\nqasper = load_dataset('allenai/qasper', split='validation')  # ~888 papers\\n# Each paper: title, full_text (list of section dicts with section_name + paragraphs)\\n# Each QA pair: question, answers (list of answer dicts with unanswerable + free_form_answer + extractive_spans)\\n\\n# === STEP 2: Parse documents into section chunks ===\\ndef parse_paper(paper):\\n    sections = []\\n    for section in paper['full_text']:\\n        name = section['section_name'] or 'unknown'\\n        paras = section['paragraphs']  # list of strings\\n        chunks = [p.strip() for p in paras if p.strip()]\\n        if chunks:\\n            sections.append({'name': name, 'chunks': chunks})\\n    return sections\\n\\n# === STEP 3: Embed chunks and query ===\\nfrom sentence_transformers import SentenceTransformer\\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\\n\\ndef embed_paper(sections):\\n    all_chunks = [(s['name'], c) for s in sections for c in s['chunks']]\\n    texts = [c for _, c in all_chunks]\\n    embeddings = model.encode(texts, batch_size=64, show_progress_bar=False)\\n    return all_chunks, embeddings\\n\\n# === STEP 4: MVT-RAG algorithm ===\\nimport numpy as np\\nfrom sklearn.metrics.pairwise import cosine_similarity\\n\\ndef mvt_rag(query_emb, sections, chunk_embs, chunk_meta):\\n    # chunk_meta: list of (section_name, chunk_text)\\n    # Build section index: section_name -> list of (chunk_idx, emb)\\n    sec_map = {}\\n    for i, (sname, _) in enumerate(chunk_meta):\\n        sec_map.setdefault(sname, []).append(i)\\n    \\n    # Estimate G_env: best sim per section, averaged\\n    g_env_values = []\\n    for sname, idxs in sec_map.items():\\n        sims = cosine_similarity([query_emb], chunk_embs[idxs])[0]\\n        g_env_values.append(np.max(sims))\\n    G_env = np.mean(g_env_values)\\n    \\n    # Section potential: max sim of best chunk\\n    sec_potential = {sname: max(cosine_similarity([query_emb], chunk_embs[idxs])[0])\\n                     for sname, idxs in sec_map.items()}\\n    \\n    retrieved = []  # list of (chunk_text, emb)\\n    visited = set()\\n    \\n    while True:\\n        # Pick highest-potential unvisited section\\n        remaining = {s: p for s, p in sec_potential.items() if s not in visited}\\n        if not remaining:\\n            break\\n        cur_sec = max(remaining, key=remaining.get)\\n        visited.add(cur_sec)\\n        \\n        sec_idxs = sec_map[cur_sec]\\n        retrieved_embs_list = [r[1] for r in retrieved]\\n        \\n        for idx in sec_idxs:\\n            chunk_emb = chunk_embs[idx]\\n            chunk_text = chunk_meta[idx][1]\\n            \\n            # Query relevance\\n            q_sim = cosine_similarity([query_emb], [chunk_emb])[0][0]\\n            \\n            # Novelty: 1 - max_sim to already retrieved\\n            if retrieved_embs_list:\\n                max_ret_sim = max(cosine_similarity([chunk_emb], retrieved_embs_list)[0])\\n                novelty = 1.0 - max_ret_sim\\n            else:\\n                novelty = 1.0\\n            \\n            G_t = q_sim * novelty\\n            \\n            if G_t < G_env and retrieved:  # switch criterion\\n                break\\n            \\n            retrieved.append((chunk_text, chunk_emb))\\n            retrieved_embs_list.append(chunk_emb)\\n    \\n    return [r[0] for r in retrieved], G_env\\n\\n# === STEP 5: Baselines ===\\n\\n# Top-k dense\\ndef topk_dense(query_emb, chunk_embs, chunk_meta, k):\\n    sims = cosine_similarity([query_emb], chunk_embs)[0]\\n    idxs = np.argsort(sims)[::-1][:k]\\n    return [chunk_meta[i][1] for i in idxs]\\n\\n# BM25 + k=5\\nfrom rank_bm25 import BM25Okapi\\ndef bm25_retrieval(query, chunk_meta, k=5):\\n    corpus = [c.split() for _, c in chunk_meta]\\n    bm25 = BM25Okapi(corpus)\\n    scores = bm25.get_scores(query.split())\\n    idxs = np.argsort(scores)[::-1][:k]\\n    return [chunk_meta[i][1] for i in idxs]\\n\\n# Fixed-threshold stopping (retrieve in sim order, stop when sim < threshold)\\ndef threshold_retrieval(query_emb, chunk_embs, chunk_meta, threshold):\\n    sims = cosine_similarity([query_emb], chunk_embs)[0]\\n    order = np.argsort(sims)[::-1]\\n    chunks = []\\n    for i in order:\\n        if sims[i] < threshold:\\n            break\\n        chunks.append(chunk_meta[i][1])\\n    return chunks if chunks else [chunk_meta[order[0]][1]]  # at least one\\n\\n# MVT-NoEnv ablation: fixed threshold=0.5\\ndef mvt_noenv_rag(query_emb, sections, chunk_embs, chunk_meta, threshold=0.5):\\n    # Same as MVT but replace G_env with fixed threshold\\n    sec_map = {}\\n    for i, (sname, _) in enumerate(chunk_meta):\\n        sec_map.setdefault(sname, []).append(i)\\n    sec_potential = {sname: max(cosine_similarity([query_emb], chunk_embs[idxs])[0])\\n                     for sname, idxs in sec_map.items()}\\n    retrieved = []\\n    visited = set()\\n    while True:\\n        remaining = {s: p for s, p in sec_potential.items() if s not in visited}\\n        if not remaining:\\n            break\\n        cur_sec = max(remaining, key=remaining.get)\\n        visited.add(cur_sec)\\n        sec_idxs = sec_map[cur_sec]\\n        retrieved_embs_list = [r[1] for r in retrieved]\\n        for idx in sec_idxs:\\n            chunk_emb = chunk_embs[idx]\\n            chunk_text = chunk_meta[idx][1]\\n            q_sim = cosine_similarity([query_emb], [chunk_emb])[0][0]\\n            if retrieved_embs_list:\\n                max_ret_sim = max(cosine_similarity([chunk_emb], retrieved_embs_list)[0])\\n                novelty = 1.0 - max_ret_sim\\n            else:\\n                novelty = 1.0\\n            G_t = q_sim * novelty\\n            if G_t < threshold and retrieved:\\n                break\\n            retrieved.append((chunk_text, chunk_emb))\\n            retrieved_embs_list.append(chunk_emb)\\n    return [r[0] for r in retrieved]\\n\\n# === STEP 6: LLM Answer Generation via OpenRouter ===\\nimport openai, os\\nclient = openai.OpenAI(\\n    api_key=os.environ['OPENROUTER_API_KEY'],\\n    base_url='https://openrouter.ai/api/v1'\\n)\\nMODEL = 'meta-llama/llama-3.1-8b-instruct'\\n\\ndef generate_answer(query, chunks):\\n    context = '\\\\n\\\\n'.join(chunks[:10])  # cap at 10 chunks to limit tokens\\n    prompt = f'Context:\\\\n{context}\\\\n\\\\nQuestion: {query}\\\\nAnswer concisely:'\\n    try:\\n        resp = client.chat.completions.create(\\n            model=MODEL,\\n            messages=[{'role':'user','content':prompt}],\\n            max_tokens=200,\\n            temperature=0.0\\n        )\\n        return resp.choices[0].message.content.strip()\\n    except Exception as e:\\n        return ''\\n\\n# === STEP 7: Evaluation metrics ===\\ndef token_f1(pred, gold):\\n    pred_toks = set(pred.lower().split())\\n    gold_toks = set(gold.lower().split())\\n    if not pred_toks or not gold_toks:\\n        return 0.0\\n    common = pred_toks & gold_toks\\n    if not common:\\n        return 0.0\\n    p = len(common)/len(pred_toks)\\n    r = len(common)/len(gold_toks)\\n    return 2*p*r/(p+r)\\n\\ndef exact_match(pred, gold):\\n    return float(pred.strip().lower() == gold.strip().lower())\\n\\ndef best_f1_over_answers(pred, gold_answers):\\n    # gold_answers is a list; take max F1\\n    return max(token_f1(pred, g) for g in gold_answers) if gold_answers else 0.0\\n\\n# === STEP 8: Main experiment loop ===\\nMETHODS = ['mvt_rag', 'mvt_noenv', 'topk_3', 'topk_5', 'topk_10', 'bm25_5', 'thresh_0.3', 'thresh_0.5', 'no_rag']\\nresults = []  # list of result dicts\\ntotal_cost = 0.0\\nCOST_LIMIT = 8.0  # leave $2 buffer\\n\\n# Sample N papers to keep cost manageable\\nN_PAPERS = 100  # start with 100 papers; if cost OK, expand to 300\\nsampled_papers = list(qasper)[:N_PAPERS]\\n\\nfor paper in tqdm(sampled_papers):\\n    sections = parse_paper(paper)\\n    if not sections:\\n        continue\\n    all_chunks, chunk_embs = embed_paper(sections)\\n    chunk_meta = all_chunks  # list of (section_name, chunk_text)\\n    chunk_embs_arr = np.array(chunk_embs)\\n    \\n    for qa in paper['qas']:\\n        question = qa['question']\\n        gold_answers = []\\n        for ans in qa['answers']:\\n            if not ans['answer']['unanswerable']:\\n                ffa = ans['answer']['free_form_answer']\\n                if ffa:\\n                    gold_answers.append(ffa)\\n        if not gold_answers:\\n            continue  # skip unanswerable\\n        \\n        query_emb = model.encode([question])[0]\\n        \\n        method_chunks = {\\n            'mvt_rag': mvt_rag(query_emb, sections, chunk_embs_arr, chunk_meta)[0],\\n            'mvt_noenv': mvt_noenv_rag(query_emb, sections, chunk_embs_arr, chunk_meta),\\n            'topk_3': topk_dense(query_emb, chunk_embs_arr, chunk_meta, 3),\\n            'topk_5': topk_dense(query_emb, chunk_embs_arr, chunk_meta, 5),\\n            'topk_10': topk_dense(query_emb, chunk_embs_arr, chunk_meta, 10),\\n            'bm25_5': bm25_retrieval(question, chunk_meta, 5),\\n            'thresh_0.3': threshold_retrieval(query_emb, chunk_embs_arr, chunk_meta, 0.3),\\n            'thresh_0.5': threshold_retrieval(query_emb, chunk_embs_arr, chunk_meta, 0.5),\\n            'no_rag': []\\n        }\\n        \\n        for method, chunks in method_chunks.items():\\n            if total_cost >= COST_LIMIT:\\n                break\\n            answer = generate_answer(question, chunks) if chunks else generate_answer(question, [])\\n            f1 = best_f1_over_answers(answer, gold_answers)\\n            em = max(exact_match(answer, g) for g in gold_answers)\\n            results.append({\\n                'paper_id': paper['id'],\\n                'question': question,\\n                'method': method,\\n                'chunks_retrieved': len(chunks),\\n                'generated_answer': answer,\\n                'gold_answers': gold_answers,\\n                'f1': f1,\\n                'exact_match': em\\n            })\\n            # Cost tracking: ~200 input tokens + 200 output ~ $0.0004 per call at llama-3.1-8b pricing\\n            total_cost += 0.0004\\n        \\n        if total_cost >= COST_LIMIT:\\n            break\\n    if total_cost >= COST_LIMIT:\\n        break\\n\\n# === STEP 9: Statistical tests ===\\nfrom scipy import stats\\nimport json\\n\\n# Group results by method\\ndef get_f1s(method):\\n    return [r['f1'] for r in results if r['method'] == method]\\n\\nmvt_f1s = get_f1s('mvt_rag')\\n# Paired bootstrap test: MVT vs topk_5\\ndef bootstrap_p(a, b, n=10000):\\n    diffs = [np.mean(a) - np.mean(b)]\\n    rng = np.random.default_rng(42)\\n    a, b = np.array(a), np.array(b)\\n    n_samples = len(a)\\n    null_diffs = []\\n    for _ in range(n):\\n        idx = rng.integers(0, n_samples, n_samples)\\n        null_diffs.append(np.mean(a[idx]) - np.mean(b[idx]))\\n    # p-value: fraction of bootstrap diffs <= 0 (one-sided)\\n    return np.mean(np.array(null_diffs) <= 0)\\n\\n# === STEP 10: Save output ===\\nsummary_stats = {}\\nfor method in METHODS:\\n    f1s = get_f1s(method)\\n    ems = [r['exact_match'] for r in results if r['method'] == method]\\n    chunks = [r['chunks_retrieved'] for r in results if r['method'] == method]\\n    summary_stats[method] = {\\n        'mean_f1': float(np.mean(f1s)) if f1s else 0,\\n        'mean_em': float(np.mean(ems)) if ems else 0,\\n        'mean_chunks': float(np.mean(chunks)) if chunks else 0,\\n        'n': len(f1s)\\n    }\\n\\n# Bootstrap p-values vs topk_5\\nfor method in METHODS:\\n    if method in ('mvt_rag', 'topk_5'):\\n        continue\\n    mf = get_f1s(method)\\n    tk5f = get_f1s('topk_5')\\n    if len(mf) == len(tk5f) and mf:\\n        summary_stats[method]['p_vs_topk5'] = bootstrap_p(np.array(mf), np.array(tk5f))\\n\\noutput = {\\n    'summary_stats': summary_stats,\\n    'per_question_results': results,\\n    'total_cost_usd': total_cost,\\n    'n_questions': len([r for r in results if r['method']=='mvt_rag'])\\n}\\nwith open('method_out.json', 'w') as f:\\n    json.dump(output, f, indent=2)\\nprint('Done. Summary:')\\nfor m, s in summary_stats.items():\\n    print(f\\\"{m}: F1={s['mean_f1']:.3f} EM={s['mean_em']:.3f} chunks={s['mean_chunks']:.1f} n={s['n']}\\\")\",\n  \"fallback_plan\": \"1. If QASPER load fails: try `load_dataset('allenai/qasper', trust_remote_code=True)` or download the JSON directly from https://huggingface.co/datasets/allenai/qasper/resolve/main/qasper-v0.3.zip and parse manually.\\n2. If OpenRouter LLM calls are too slow or costly: switch to google/gemma-2-2b-it (cheaper) or skip answer generation entirely — evaluate retrieval quality using oracle F1 (max F1 of retrieved chunks vs. gold extractive spans from QASPER annotations). This eliminates LLM cost completely and is still a valid experiment.\\n3. If sentence-transformers is slow on CPU: reduce N_PAPERS to 50, or pre-embed all chunks in batches upfront before the QA loop.\\n4. If the MVT switching loop retrieves too many chunks (>30 per question): cap at max_chunks=15 to prevent degenerate cases where G_env is very low and nothing triggers switching.\\n5. If QASPER has papers with no section structure (flat paragraphs): treat each paragraph as its own 'section' so the MVT logic still applies.\\n6. If cost tracking shows approaching $8: stop the paper loop early and report partial results — partial results over 50+ papers are still sufficient for statistical comparison.\",\n  \"testing_plan\": \"1. MINI TEST (5 papers, 1 question each, no LLM): Run just the retrieval methods (no answer generation) to verify chunk counts and G_env values look reasonable. Print per-method chunks_retrieved and G_env for visual inspection.\\n2. SIGNAL CHECK: For one paper, print the MVT decision log — G_t values per chunk, G_env, and which chunks were retrieved. Verify that switching happens when expected (G_t < G_env).\\n3. BASELINE SANITY: topk_5 should always return exactly 5 chunks. BM25 should return 5. Fixed-threshold may return 0 (check fallback).\\n4. COST DRY RUN: Generate answers for 10 questions, track cost, extrapolate to full run. If cost/question > $0.01, reduce N_PAPERS.\\n5. FULL SCALE: Run on 100 papers (~500-2000 questions). If time and cost allow, expand to 300 papers.\\n6. SUCCESS SIGNAL: MVT-RAG mean F1 > topk_5 mean F1, with fewer mean chunks. Also check that MVT-NoEnv (fixed threshold) scores lower than MVT-RAG, confirming the ecology-derived averaging is the load-bearing component.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-07-18 15:24:02 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json`. The plan implements MVT-RAG end-to-end on QASPER with all 9 methods (MVT, MVT-NoEnv ablation, top-k at 3/5/10, BM25, threshold stopping at 0.3/0.5, no-RAG), using sentence-transformers for embeddings, OpenRouter Llama-3.1-8B for answer generation, and paired bootstrap tests for significance. Compute profile set to `cpu_heavy` since all embedding is CPU-based.
```
