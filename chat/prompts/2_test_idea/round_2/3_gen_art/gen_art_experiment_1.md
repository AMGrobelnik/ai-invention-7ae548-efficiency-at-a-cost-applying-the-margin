# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 16:30:08 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

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

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx1
type: experiment
title: 'MVT-RAG G_env Fix: Quality vs Efficiency'
summary: >-
  Re-run MVT-RAG on QASPER with corrected G_env estimators (top-3/top-5 mean, alpha=0.7 discount), fixed MVT-NoEnv ablation
  threshold, top-k-1/2 baselines, oracle condition, EM bug fix, and section-recall metric. Primary goal: test whether multi-chunk
  G_env closes the F1 gap (0.122→target 0.165+) while retaining efficiency advantage.
runpod_compute_profile: cpu_heavy
implementation_pseudocode: |-
  ## Setup

  ```
  DEP_DATA = '/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'
  OUTPUT = './method_out.json'
  OPENROUTER_MODEL = 'meta-llama/llama-3.1-8b-instruct'
  BUDGET_USD = 1.50  # hard cap, track cumulative

  # Use aii-openrouter-llms skill for LLM calls
  # Use aii-python skill for coding standards
  ```

  ## Step 1: Load and Validate Data

  ```
  Load full_data_out.json (2000 examples)
  Filter to metadata_fold==1 (validation set, ~223 questions)
    - Each example: input JSON has {question, paper_id, sections_summary}
    - output JSON has {gold_answer, evidence_chunk_ids, evidence_section_names}
    - metadata fields: metadata_is_multihop, metadata_num_sections, etc.

  Parse sections_summary to reconstruct per-paper chunk list:
    Each section has section_name, normalized_section, chunks (list of {chunk_id, text})
  Group chunks by paper_id -> section -> list of chunks
  ```

  ## Step 2: Embeddings (one-time, cache to disk)

  ```
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer('all-MiniLM-L6-v2')  # CPU-only, fast

  For each unique paper in validation set:
    For each chunk across all sections:
      embed chunk text -> vector (384-dim)
    Cache paper_id -> {chunk_id: embedding} as embeddings.pkl

  For each question:
    embed question text -> query_vector
    Cache question_id -> query_vector

  Note: ~223 questions x avg 50 chunks/paper = ~11k embeddings total, fast on CPU
  ```

  ## Step 3: EM Normalization Fix

  ```
  # QASPER official normalization from their evaluation script:
  def normalize_answer(s):
      s = s.lower()
      s = re.sub(r'\b(a|an|the)\b', ' ', s)  # remove articles
      s = re.sub(r'[^\w\s]', '', s)           # remove punctuation
      s = ' '.join(s.split())                  # normalize whitespace
      return s

  def exact_match(pred, gold_list):
      pred_norm = normalize_answer(pred)
      return any(normalize_answer(g) == pred_norm for g in gold_list)

  def token_f1(pred, gold_list):
      pred_tokens = normalize_answer(pred).split()
      best_f1 = 0
      for gold in gold_list:
          gold_tokens = normalize_answer(gold).split()
          common = Counter(pred_tokens) & Counter(gold_tokens)
          n_common = sum(common.values())
          if n_common == 0: continue
          prec = n_common / len(pred_tokens)
          rec = n_common / len(gold_tokens)
          f1 = 2*prec*rec/(prec+rec)
          best_f1 = max(best_f1, f1)
      return best_f1

  # gold_answer in output JSON may be a list (multiple valid answers) or
  # a string - handle both cases. QASPER answers can be 'yes'/'no'/free text/list.
  ```

  ## Step 4: MVT-RAG Core Implementation

  ```python
  def cosine_sim(a, b):
      return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

  def marginal_gain(chunk_emb, query_emb, retrieved_embs):
      query_sim = cosine_sim(chunk_emb, query_emb)
      if not retrieved_embs:
          novelty = 1.0
      else:
          max_sim_to_retrieved = max(cosine_sim(chunk_emb, r) for r in retrieved_embs)
          novelty = 1.0 - max_sim_to_retrieved
      return query_sim * novelty

  def estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1):
      # top_n: number of top chunks per section to average
      section_scores = []
      for sec in sections:
          sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)
                  for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]
          if not sims: continue
          top_sims = sorted(sims, reverse=True)[:top_n]
          section_scores.append(np.mean(top_sims))
      return np.mean(section_scores) if section_scores else 0.0

  def mvt_retrieve(query_emb, sections, chunk_embeddings,
                   g_env_top_n=1, alpha=1.0, max_chunks=15):
      """
      g_env_top_n: 1 (original), 3 (top-3), 5 (top-5)
      alpha: discount factor applied to G_env (0.7 = more permissive)
      Returns: list of retrieved chunk_ids in order
      """
      g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=g_env_top_n)
      effective_threshold = alpha * g_env

      # Score sections by best chunk similarity (for ordering)
      section_priority = []
      for sec in sections:
          sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)
                  for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]
          best = max(sims) if sims else 0.0
          section_priority.append((best, sec))
      section_priority.sort(reverse=True)

      retrieved_chunk_ids = []
      retrieved_embs = []

      for _, sec in section_priority:
          # Within section, retrieve chunks in descending query similarity order
          chunks_sorted = sorted(
              sec['chunks'],
              key=lambda c: cosine_sim(chunk_embeddings.get(c['chunk_id'], np.zeros(384)), query_emb),
              reverse=True
          )
          for chunk in chunks_sorted:
              if len(retrieved_chunk_ids) >= max_chunks:
                  return retrieved_chunk_ids
              cid = chunk['chunk_id']
              if cid not in chunk_embeddings:
                  continue
              g_t = marginal_gain(chunk_embeddings[cid], query_emb, retrieved_embs)
              if g_t < effective_threshold:
                  break  # switch to next section
              retrieved_chunk_ids.append(cid)
              retrieved_embs.append(chunk_embeddings[cid])

      return retrieved_chunk_ids
  ```

  ## Step 5: MVT-NoEnv Fixed-Threshold Ablation (CORRECTED)

  ```python
  # Pilot pass: compute actual G_env distribution across all validation questions
  # using top-1 estimator, then use median as fixed threshold
  def compute_pilot_g_env(validation_questions, chunk_embeddings, query_embeddings):
      g_envs = []
      for q in validation_questions:
          sections = get_sections(q)
          query_emb = query_embeddings[q['question_id']]
          g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1)
          g_envs.append(g_env)
      return np.median(g_envs)  # use as fixed threshold for NoEnv ablation

  # MVT-NoEnv: same algorithm but threshold=fixed_threshold instead of per-question G_env
  def mvt_noenv_retrieve(query_emb, sections, chunk_embeddings, fixed_threshold, max_chunks=15):
      # Same as mvt_retrieve but g_env is replaced by fixed_threshold
      # (this is the correct ablation: no ecology-derived environment average)
      ...
  ```

  ## Step 6: All Baselines

  ```python
  # Top-k dense retrieval: flatten all chunks for paper, sort by query cosine sim, take top k
  def topk_retrieve(query_emb, all_chunks, chunk_embeddings, k):
      sims = [(cosine_sim(chunk_embeddings[c['chunk_id']], query_emb), c['chunk_id'])
              for c in all_chunks if c['chunk_id'] in chunk_embeddings]
      sims.sort(reverse=True)
      return [cid for _, cid in sims[:k]]

  # Oracle: use gold evidence_chunk_ids directly (no retrieval error)
  def oracle_retrieve(gold_evidence_chunk_ids):
      return gold_evidence_chunk_ids
  ```

  ## Step 7: LLM Answer Generation

  ```python
  # Via OpenRouter - use aii-openrouter-llms skill for setup
  # Model: meta-llama/llama-3.1-8b-instruct
  # Prompt template:
  SYSTEM = "You are a scientific QA assistant. Answer questions using ONLY the provided context. Be concise."

  def build_prompt(question, chunks_text_list):
      context = '\n\n'.join([f'[Chunk {i+1}]: {t}' for i, t in enumerate(chunks_text_list)])
      return f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

  # Cost tracking:
  # llama-3.1-8b-instruct: ~$0.06/1M input tokens, $0.06/1M output tokens
  # ~223 questions x 10 variants x avg 1500 input tokens = ~3.3M tokens = ~$0.20 total
  # Very safe within $1.50 budget

  # IMPORTANT: If no chunks retrieved, use empty context fallback
  # Track cost after each batch of 10 calls; stop if approaching $1.50
  ```

  ## Step 8: Section Recall Metric

  ```python
  def section_recall(retrieved_chunk_ids, gold_evidence_section_names, chunk_id_to_section):
      """
      For multi-hop questions: what fraction of gold evidence sections
      have at least one retrieved chunk?
      """
      retrieved_sections = set(chunk_id_to_section.get(cid) for cid in retrieved_chunk_ids)
      gold_sections = set(gold_evidence_section_names)
      if not gold_sections:
          return 1.0
      return len(retrieved_sections & gold_sections) / len(gold_sections)
  ```

  ## Step 9: Full Experiment Loop

  ```python
  VARIANTS = [
      {'name': 'top-k-1',      'type': 'topk',   'k': 1},
      {'name': 'top-k-2',      'type': 'topk',   'k': 2},
      {'name': 'top-k-3',      'type': 'topk',   'k': 3},
      {'name': 'top-k-5',      'type': 'topk',   'k': 5},
      {'name': 'top-k-10',     'type': 'topk',   'k': 10},
      {'name': 'mvt-top1',     'type': 'mvt',    'g_env_top_n': 1, 'alpha': 1.0},  # original
      {'name': 'mvt-top3',     'type': 'mvt',    'g_env_top_n': 3, 'alpha': 1.0},  # FIX: multi-chunk
      {'name': 'mvt-top5',     'type': 'mvt',    'g_env_top_n': 5, 'alpha': 1.0},  # FIX: multi-chunk
      {'name': 'mvt-alpha0.7', 'type': 'mvt',    'g_env_top_n': 1, 'alpha': 0.7}, # FIX: discount
      {'name': 'mvt-noenv',    'type': 'mvt_noenv'},  # fixed threshold ablation
      {'name': 'oracle',       'type': 'oracle'},
  ]

  results = []  # per-question results
  cumulative_cost = 0.0

  for q in validation_questions:  # ~223 questions
      question = q['input_parsed']['question']
      paper_sections = get_sections_for_paper(q)
      gold_answer = q['output_parsed']['gold_answer']  # may be list or string
      gold_chunk_ids = q['output_parsed']['evidence_chunk_ids']
      gold_section_names = q['output_parsed']['evidence_section_names']
      is_multihop = q['metadata_is_multihop']
      query_emb = embed(question)

      q_result = {'question_id': q['metadata_question_id'],
                  'is_multihop': is_multihop, 'variants': {}}

      for variant in VARIANTS:
          # 1. Retrieve chunks
          if variant['type'] == 'topk':
              retrieved = topk_retrieve(query_emb, all_chunks, chunk_embs, variant['k'])
          elif variant['type'] == 'mvt':
              retrieved = mvt_retrieve(query_emb, paper_sections, chunk_embs,
                                       g_env_top_n=variant['g_env_top_n'],
                                       alpha=variant['alpha'])
          elif variant['type'] == 'mvt_noenv':
              retrieved = mvt_noenv_retrieve(query_emb, paper_sections, chunk_embs, fixed_threshold)
          else:  # oracle
              retrieved = gold_chunk_ids

          # 2. Build context from retrieved chunks
          context_texts = [chunk_id_to_text[cid] for cid in retrieved if cid in chunk_id_to_text]

          # 3. LLM answer generation
          if cumulative_cost >= 1.40:  # safety stop
              predicted_answer = '[BUDGET_EXCEEDED]'
          else:
              prompt = build_prompt(question, context_texts)
              predicted_answer, cost = call_openrouter(OPENROUTER_MODEL, prompt)
              cumulative_cost += cost

          # 4. Compute metrics
          gold_list = gold_answer if isinstance(gold_answer, list) else [gold_answer]
          em = exact_match(predicted_answer, gold_list)
          f1 = token_f1(predicted_answer, gold_list)
          sec_rec = section_recall(retrieved, gold_section_names, chunk_id_to_section)
          n_chunks = len(retrieved)

          q_result['variants'][variant['name']] = {
              'retrieved_chunk_ids': retrieved,
              'predicted_answer': predicted_answer,
              'em': em, 'f1': f1,
              'n_chunks_retrieved': n_chunks,
              'section_recall': sec_rec,
          }

      results.append(q_result)

  # Aggregate metrics across all questions
  for variant_name in [v['name'] for v in VARIANTS]:
      avg_em = mean(r['variants'][variant_name]['em'] for r in results)
      avg_f1 = mean(r['variants'][variant_name]['f1'] for r in results)
      avg_chunks = mean(r['variants'][variant_name]['n_chunks_retrieved'] for r in results)
      avg_sec_rec = mean(r['variants'][variant_name]['section_recall'] for r in results)
      # Also compute for multihop subset
      multihop_results = [r for r in results if r['is_multihop']]
      ...

  # Bootstrap 95% CI for F1 differences (MVT vs top-k-5 as primary comparison)
  # 10000 bootstrap samples with paired resampling
  ```

  ## Step 10: Output

  ```python
  method_out = {
      'summary': {
          'n_questions': len(results),
          'n_multihop': sum(r['is_multihop'] for r in results),
          'total_cost_usd': cumulative_cost,
          'per_variant_aggregate': {
              variant_name: {
                  'mean_em': ..., 'mean_f1': ...,
                  'mean_chunks': ..., 'mean_section_recall': ...,
                  'multihop_mean_f1': ..., 'multihop_mean_section_recall': ...
              }
          },
          'bootstrap_ci_mvt_top3_vs_topk5_f1': [lower, upper],
          'bootstrap_ci_mvt_alpha07_vs_topk5_f1': [lower, upper],
          'pilot_g_env_median': fixed_threshold,
      },
      'per_question': results  # full detail for analysis
  }

  with open('method_out.json', 'w') as f:
      json.dump(method_out, f, indent=2)
  ```

  ## Key Implementation Notes

  1. **Data parsing**: The dependency dataset stores input/output as JSON strings—parse with `json.loads()`.
     `sections_summary` in the input JSON contains the full chunk list per section.

  2. **Embedding caching**: Save to `embeddings_cache.pkl` after first run. Check for cache file at start.

  3. **Gold answer format**: QASPER answers can be 'yes'/'no', extractive spans, or lists. The dataset
     artifact normalizes these; treat as list always.

  4. **EM=0 debug**: Before full run, spot-check 5 examples: print raw predicted answer, gold answers,
     and normalized versions. If all EM=0 even on oracle condition, the LLM prompt/parsing is broken.

  5. **Oracle F1 ceiling**: Oracle should achieve ~0.4-0.6 F1 on QASPER (known upper bound from literature).
     If oracle F1 < 0.3, the LLM call or answer parsing is likely broken—fix before full run.

  6. **Sections parsing**: The sections_summary is a list of section objects. Each section has `chunks`
     list. Re-group by `normalized_section` name to get IMRaD categories.

  7. **Papers with few sections**: If a paper has only 1-2 sections, MVT switching is trivial.
     These are excluded by the dataset (>=3 distinct sections filter) but verify at runtime.

  8. **OpenRouter setup**: Use the aii-openrouter-llms skill to get the API key and call pattern.
     All calls must go through OpenRouter—no direct Anthropic/OpenAI endpoints.
fallback_plan: |-
  ## Primary Fallback: Reduce LLM calls

  If cost is tracking high (>$0.80 after 100 questions), reduce variants by dropping top-k-10 and oracle, which are less critical for the core hypothesis. Run 5 core variants: top-k-1, top-k-3, top-k-5, mvt-top3, mvt-alpha0.7.

  ## Secondary Fallback: Skip LLM, use retrieval-only metrics

  If OpenRouter is unavailable or budget is too tight, skip LLM generation entirely and report only:
  - Retrieval precision/recall (gold evidence chunks retrieved)
  - Section recall
  - N chunks retrieved per question

  These metrics directly test the core hypothesis (does multi-chunk G_env improve retrieval quality?) without needing generation. Report retrieval F1 (did we retrieve the right chunks?) instead of answer F1.

  ## Embedding Fallback

  If sentence-transformers is slow on CPU, use `paraphrase-MiniLM-L3-v2` (smaller/faster) or TF-IDF cosine similarity as a zero-dependency alternative. TF-IDF is much faster and still captures keyword overlap.

  ## Data Fallback

  If sections_summary doesn't contain full chunk text (parse error), fall back to re-loading QASPER directly from HuggingFace (`allenai/qasper`, validation split) and re-parsing sections inline using the same logic as the dataset artifact's data.py.

  ## Truncation Fallback

  If 223 questions take too long (>5h with embeddings+LLM), run on 100 questions (first 50 single-hop + first 50 multihop) and report results on that subset with a note.
testing_plan: |-
  ## Step 0: Verify Data Loading (5 min)

  ```python
  import json
  data = json.load(open(DEP_DATA))
  validation = [x for x in data if x['metadata_fold'] == 1]
  print(f'Validation size: {len(validation)}')
  print('First example input keys:', json.loads(validation[0]['input']).keys())
  print('First example output keys:', json.loads(validation[0]['output']).keys())
  print('Is multihop distribution:', sum(x['metadata_is_multihop'] for x in validation))
  ```
  Expect: ~223 validation examples, input has question+sections_summary, output has gold_answer+evidence_chunk_ids.

  ## Step 1: Mini smoke test on 5 examples (15 min)

  Run ALL variants on 5 questions (mix of single-hop and multihop).
  - Check embeddings work: cosine sims in [0.0, 1.0] range
  - Check G_env estimation produces non-zero values
  - Check MVT retrieves between 1-15 chunks (not always 0 or 15)
  - Check oracle retrieves the correct chunk IDs
  - Check LLM returns non-empty string (1 LLM call to verify API)
  - Check EM normalization: manually verify normalized predicted vs gold for 2 examples
  - Print per-example summary table: variant | n_chunks | f1 | em

  ## Step 2: EM debug check (5 min)

  For oracle condition on 5 examples:
  - Print raw LLM output
  - Print gold_answer
  - Print normalize(pred) vs normalize(gold)
  - If EM=0 for oracle on obvious 'yes'/'no' answers, fix normalization
  - Target: oracle F1 >= 0.30 on 5-example sample

  ## Step 3: Embedding cache check (2 min)

  After first mini run, verify `embeddings_cache.pkl` exists and reload correctly. Second mini run should be faster.

  ## Step 4: 50-question validation run (30 min)

  Run all variants on 50 questions before full 223.
  - Verify cost tracking: cumulative_cost after 50q x 10 variants should be ~$0.40
  - Verify multihop questions are present (should be ~17 of 50)
  - Check aggregate F1 table looks reasonable: oracle > top-k-5 > top-k-1
  - If top-k-5 F1 is still ~0.190 (matching iter1), data pipeline is consistent
  - Check mvt-top3 F1 vs mvt-top1 F1: expect improvement (this is the core hypothesis)

  ## Full run completion signals

  - Oracle F1 >= 0.35 (literature upper bound for 8B model on QASPER is ~0.40-0.50)
  - Top-k-5 F1 ~0.17-0.22 (within range of published results)
  - MVT-top3 retrieves more chunks than MVT-top1 (G_env reduced → less aggressive switching)
  - Bootstrap CI for MVT-top3 vs top-k-5 F1: check whether CI excludes zero (confirms hypothesis)
  - Cost <= $1.00 total
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

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

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

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
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [2] HUMAN-USER prompt · 2026-07-18 16:30:08 UTC

```
Improving retrieval-augmented generation for long scientific documents
```

### [3] SKILL-INPUT — aii-python · 2026-07-18 16:30:40 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-07-18 16:30:40 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-json · 2026-07-18 16:30:40 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SKILL-INPUT — aii-file-size-limit · 2026-07-18 16:30:48 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [7] SKILL-INPUT — aii-use-hardware · 2026-07-18 16:30:48 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [8] SKILL-INPUT — aii-parallel-computing · 2026-07-18 16:30:48 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SKILL-INPUT — aii-openrouter-llms · 2026-07-18 16:30:48 UTC

The agent loaded the **aii-openrouter-llms** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-openrouter-llms
description: Searches and calls LLMs from OpenRouter's extensive catalog (Claude, GPT, Gemini, Llama, Mistral, DeepSeek, etc.) with reasoning and temperature control. Use when user needs to access various LLMs, compare language models, call different model providers, find the best model for a task, or look up model pricing and costs per million tokens.
---

## Contents

- Workflow (2-phase model discovery and calling)
- Scripts (Search, Get Params, Call)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: Model Discovery and Calling

### Phase 1: Search for Models
Find models with pricing, context length, and descriptions
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

### Phase 2 (optional): Get Model Parameters
Check what parameters a specific model supports
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

### Phase 3: Call Model
Call a model using the API name from search results
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

---

## Scripts

### Search OpenRouter models (aii_or_search_llms.py)

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: When running multiple searches, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_search_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {} --limit 5' ::: 'claude' 'gpt' 'gemini'
```

**Example output:**
```
Found 5 models for query: claude

[1] Anthropic: Claude Opus 4.5
    API: anthropic/claude-opus-4.5
    Context: 200,000 tokens
    Price: $5.00/M in, $25.00/M out
    Claude Opus 4.5 is Anthropic's frontier reasoning model...

[2] Anthropic: Claude Haiku 4.5
    API: anthropic/claude-haiku-4.5
    Context: 200,000 tokens
    Price: $1.00/M in, $5.00/M out
    ...
```

**Parameters:**

`query` (optional, positional)
- Search query to filter models (e.g., 'claude', 'gpt', 'reasoning')

`--limit, -n` (optional)
- Maximum number of results (default: 10)

`--series, -s` (optional)
- Filter by model family
- Valid: GPT, Claude, Gemini, Grok, Cohere, Nova, Qwen, Yi, DeepSeek, Mistral, Llama2, Llama3, Llama4, RWKV, Qwen3, Router, Media, Other, PaLM

`--timeout` (optional)
- Request timeout in seconds (default: 60)

**Tips:**
- Use the `API` field from results for the `--model` parameter in calls
- Search is fast (queries OpenRouter's model list)

---

### Get model parameters (aii_or_get_llm_params.py)

Get detailed information and supported parameters for a specific model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

**Parallel execution (multiple models):**

IMPORTANT: When checking multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_get_llm_params.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {}' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: Anthropic: Claude Haiku 4.5
API: anthropic/claude-haiku-4.5

=== Capabilities ===
Context Length: 200,000 tokens
Max Output: 64,000 tokens
Modality: text+image->text
Input: image, text
Output: text
Moderated: Yes

=== Pricing ===
Input: $1.0000/M tokens
Output: $5.0000/M tokens

=== Supported Parameters ===
  - include_reasoning
  - max_tokens
  - reasoning
  - stop
  - temperature
  - tool_choice
  - tools
  - top_k
  - top_p
```

**Parameters:**

`model` (required, positional)
- Model API name (e.g., 'anthropic/claude-haiku-4.5', 'openai/o1')

`--timeout` (optional)
- Request timeout in seconds (default: 30)

**Tips:**
- Use after search to see which parameters a model supports
- Check supported_parameters before using --reasoning or other options

---

### Call OpenRouter model (aii_or_call_llms.py)

Make an API call to an OpenRouter LLM model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

**Parallel execution (multiple calls):**

IMPORTANT: When calling multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_call_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --model {} --input "What is 2+2?"' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: anthropic/claude-haiku-4.5

Response:
Four.

Tokens: 12 in, 5 out
```

**Parameters:**

`--model, -m` (required)
- API model name from search results (format: `provider/model-name`)
- Examples: `anthropic/claude-sonnet-4`, `openai/gpt-5`, `google/gemini-2.5-pro`

`--input, -i` (required, unless using --input-json)
- Simple string prompt

`--input-json` (optional)
- Full conversation JSON for multi-turn (mutually exclusive with --input)

`--max-tokens` (optional)
- Maximum output tokens (default: 9000)

`--reasoning` (optional)
- Reasoning effort for reasoning models: `minimal`, `low`, `medium`, `high`

`--temperature, -t` (optional)
- Randomness (0.0-2.0): 0.0=deterministic, 0.7=balanced, 1.5+=creative

`--top-p` (optional)
- Nucleus sampling (0.0-1.0)

`--instructions` (optional)
- System instructions/prompt

`--web-search` (optional)
- Enable web search with max results (e.g., 10)

`--params, -p` (optional)
- Extra model-specific parameters as JSON string
- Use `aii_or_get_llm_params.py` to see which params a model supports
- Example: `--params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'`

`--timeout` (optional)
- Request timeout in seconds (default: 120)

**Examples:**

Simple call:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "Write a haiku about coding" \
  --temperature 0.8
```

With system instructions:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-haiku-4.5" \
  --input "Explain recursion" \
  --instructions "You are a helpful programming tutor. Keep explanations concise."
```

With reasoning (for o1-style models):
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "openai/o1" \
  --input "Solve this complex math problem" \
  --reasoning high
```

With web search:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "What are the latest AI news?" \
  --web-search 10 \
  --max-tokens 15000
```

With extra model-specific params:
```bash
# Step 1: Check what params the model supports
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "meta-llama/llama-3.3-70b-instruct"
# Shows: frequency_penalty, top_k, seed, min_p, etc.

# Step 2: Call with those params
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "meta-llama/llama-3.3-70b-instruct" \
  --input "Write a short poem" \
  --params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'
```

---

## Tips

- Use `aii_or_search_llms.py` first to find models, then copy `API` field for `--model`
- Use `aii_or_get_llm_params.py` to check what params a model supports before using `--params`
- For web search, increase `--max-tokens` to handle larger responses (15000+)

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [10] SYSTEM-USER prompt · 2026-07-18 16:40:52 UTC

```
[Your previous response had no visible output. Please continue and produce a user-visible response.]
```

### [11] SYSTEM-USER prompt · 2026-07-18 16:41:06 UTC

```
[Your previous response had no visible output. Please continue and produce a user-visible response.]
```

### [12] SYSTEM-USER prompt · 2026-07-18 16:41:14 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx1
type: experiment
title: 'MVT-RAG G_env Fix: Quality vs Efficiency'
summary: >-
  Re-run MVT-RAG on QASPER with corrected G_env estimators (top-3/top-5 mean, alpha=0.7 discount), fixed MVT-NoEnv ablation
  threshold, top-k-1/2 baselines, oracle condition, EM bug fix, and section-recall metric. Primary goal: test whether multi-chunk
  G_env closes the F1 gap (0.122→target 0.165+) while retaining efficiency advantage.
runpod_compute_profile: cpu_heavy
implementation_pseudocode: |-
  ## Setup

  ```
  DEP_DATA = '/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'
  OUTPUT = './method_out.json'
  OPENROUTER_MODEL = 'meta-llama/llama-3.1-8b-instruct'
  BUDGET_USD = 1.50  # hard cap, track cumulative

  # Use aii-openrouter-llms skill for LLM calls
  # Use aii-python skill for coding standards
  ```

  ## Step 1: Load and Validate Data

  ```
  Load full_data_out.json (2000 examples)
  Filter to metadata_fold==1 (validation set, ~223 questions)
    - Each example: input JSON has {question, paper_id, sections_summary}
    - output JSON has {gold_answer, evidence_chunk_ids, evidence_section_names}
    - metadata fields: metadata_is_multihop, metadata_num_sections, etc.

  Parse sections_summary to reconstruct per-paper chunk list:
    Each section has section_name, normalized_section, chunks (list of {chunk_id, text})
  Group chunks by paper_id -> section -> list of chunks
  ```

  ## Step 2: Embeddings (one-time, cache to disk)

  ```
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer('all-MiniLM-L6-v2')  # CPU-only, fast

  For each unique paper in validation set:
    For each chunk across all sections:
      embed chunk text -> vector (384-dim)
    Cache paper_id -> {chunk_id: embedding} as embeddings.pkl

  For each question:
    embed question text -> query_vector
    Cache question_id -> query_vector

  Note: ~223 questions x avg 50 chunks/paper = ~11k embeddings total, fast on CPU
  ```

  ## Step 3: EM Normalization Fix

  ```
  # QASPER official normalization from their evaluation script:
  def normalize_answer(s):
      s = s.lower()
      s = re.sub(r'\b(a|an|the)\b', ' ', s)  # remove articles
      s = re.sub(r'[^\w\s]', '', s)           # remove punctuation
      s = ' '.join(s.split())                  # normalize whitespace
      return s

  def exact_match(pred, gold_list):
      pred_norm = normalize_answer(pred)
      return any(normalize_answer(g) == pred_norm for g in gold_list)

  def token_f1(pred, gold_list):
      pred_tokens = normalize_answer(pred).split()
      best_f1 = 0
      for gold in gold_list:
          gold_tokens = normalize_answer(gold).split()
          common = Counter(pred_tokens) & Counter(gold_tokens)
          n_common = sum(common.values())
          if n_common == 0: continue
          prec = n_common / len(pred_tokens)
          rec = n_common / len(gold_tokens)
          f1 = 2*prec*rec/(prec+rec)
          best_f1 = max(best_f1, f1)
      return best_f1

  # gold_answer in output JSON may be a list (multiple valid answers) or
  # a string - handle both cases. QASPER answers can be 'yes'/'no'/free text/list.
  ```

  ## Step 4: MVT-RAG Core Implementation

  ```python
  def cosine_sim(a, b):
      return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

  def marginal_gain(chunk_emb, query_emb, retrieved_embs):
      query_sim = cosine_sim(chunk_emb, query_emb)
      if not retrieved_embs:
          novelty = 1.0
      else:
          max_sim_to_retrieved = max(cosine_sim(chunk_emb, r) for r in retrieved_embs)
          novelty = 1.0 - max_sim_to_retrieved
      return query_sim * novelty

  def estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1):
      # top_n: number of top chunks per section to average
      section_scores = []
      for sec in sections:
          sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)
                  for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]
          if not sims: continue
          top_sims = sorted(sims, reverse=True)[:top_n]
          section_scores.append(np.mean(top_sims))
      return np.mean(section_scores) if section_scores else 0.0

  def mvt_retrieve(query_emb, sections, chunk_embeddings,
                   g_env_top_n=1, alpha=1.0, max_chunks=15):
      """
      g_env_top_n: 1 (original), 3 (top-3), 5 (top-5)
      alpha: discount factor applied to G_env (0.7 = more permissive)
      Returns: list of retrieved chunk_ids in order
      """
      g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=g_env_top_n)
      effective_threshold = alpha * g_env

      # Score sections by best chunk similarity (for ordering)
      section_priority = []
      for sec in sections:
          sims = [cosine_sim(chunk_embeddings[c['chunk_id']], query_emb)
                  for c in sec['chunks'] if c['chunk_id'] in chunk_embeddings]
          best = max(sims) if sims else 0.0
          section_priority.append((best, sec))
      section_priority.sort(reverse=True)

      retrieved_chunk_ids = []
      retrieved_embs = []

      for _, sec in section_priority:
          # Within section, retrieve chunks in descending query similarity order
          chunks_sorted = sorted(
              sec['chunks'],
              key=lambda c: cosine_sim(chunk_embeddings.get(c['chunk_id'], np.zeros(384)), query_emb),
              reverse=True
          )
          for chunk in chunks_sorted:
              if len(retrieved_chunk_ids) >= max_chunks:
                  return retrieved_chunk_ids
              cid = chunk['chunk_id']
              if cid not in chunk_embeddings:
                  continue
              g_t = marginal_gain(chunk_embeddings[cid], query_emb, retrieved_embs)
              if g_t < effective_threshold:
                  break  # switch to next section
              retrieved_chunk_ids.append(cid)
              retrieved_embs.append(chunk_embeddings[cid])

      return retrieved_chunk_ids
  ```

  ## Step 5: MVT-NoEnv Fixed-Threshold Ablation (CORRECTED)

  ```python
  # Pilot pass: compute actual G_env distribution across all validation questions
  # using top-1 estimator, then use median as fixed threshold
  def compute_pilot_g_env(validation_questions, chunk_embeddings, query_embeddings):
      g_envs = []
      for q in validation_questions:
          sections = get_sections(q)
          query_emb = query_embeddings[q['question_id']]
          g_env = estimate_g_env(query_emb, sections, chunk_embeddings, top_n=1)
          g_envs.append(g_env)
      return np.median(g_envs)  # use as fixed threshold for NoEnv ablation

  # MVT-NoEnv: same algorithm but threshold=fixed_threshold instead of per-question G_env
  def mvt_noenv_retrieve(query_emb, sections, chunk_embeddings, fixed_threshold, max_chunks=15):
      # Same as mvt_retrieve but g_env is replaced by fixed_threshold
      # (this is the correct ablation: no ecology-derived environment average)
      ...
  ```

  ## Step 6: All Baselines

  ```python
  # Top-k dense retrieval: flatten all chunks for paper, sort by query cosine sim, take top k
  def topk_retrieve(query_emb, all_chunks, chunk_embeddings, k):
      sims = [(cosine_sim(chunk_embeddings[c['chunk_id']], query_emb), c['chunk_id'])
              for c in all_chunks if c['chunk_id'] in chunk_embeddings]
      sims.sort(reverse=True)
      return [cid for _, cid in sims[:k]]

  # Oracle: use gold evidence_chunk_ids directly (no retrieval error)
  def oracle_retrieve(gold_evidence_chunk_ids):
      return gold_evidence_chunk_ids
  ```

  ## Step 7: LLM Answer Generation

  ```python
  # Via OpenRouter - use aii-openrouter-llms skill for setup
  # Model: meta-llama/llama-3.1-8b-instruct
  # Prompt template:
  SYSTEM = "You are a scientific QA assistant. Answer questions using ONLY the provided context. Be concise."

  def build_prompt(question, chunks_text_list):
      context = '\n\n'.join([f'[Chunk {i+1}]: {t}' for i, t in enumerate(chunks_text_list)])
      return f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

  # Cost tracking:
  # llama-3.1-8b-instruct: ~$0.06/1M input tokens, $0.06/1M output tokens
  # ~223 questions x 10 variants x avg 1500 input tokens = ~3.3M tokens = ~$0.20 total
  # Very safe within $1.50 budget

  # IMPORTANT: If no chunks retrieved, use empty context fallback
  # Track cost after each batch of 10 calls; stop if approaching $1.50
  ```

  ## Step 8: Section Recall Metric

  ```python
  def section_recall(retrieved_chunk_ids, gold_evidence_section_names, chunk_id_to_section):
      """
      For multi-hop questions: what fraction of gold evidence sections
      have at least one retrieved chunk?
      """
      retrieved_sections = set(chunk_id_to_section.get(cid) for cid in retrieved_chunk_ids)
      gold_sections = set(gold_evidence_section_names)
      if not gold_sections:
          return 1.0
      return len(retrieved_sections & gold_sections) / len(gold_sections)
  ```

  ## Step 9: Full Experiment Loop

  ```python
  VARIANTS = [
      {'name': 'top-k-1',      'type': 'topk',   'k': 1},
      {'name': 'top-k-2',      'type': 'topk',   'k': 2},
      {'name': 'top-k-3',      'type': 'topk',   'k': 3},
      {'name': 'top-k-5',      'type': 'topk',   'k': 5},
      {'name': 'top-k-10',     'type': 'topk',   'k': 10},
      {'name': 'mvt-top1',     'type': 'mvt',    'g_env_top_n': 1, 'alpha': 1.0},  # original
      {'name': 'mvt-top3',     'type': 'mvt',    'g_env_top_n': 3, 'alpha': 1.0},  # FIX: multi-chunk
      {'name': 'mvt-top5',     'type': 'mvt',    'g_env_top_n': 5, 'alpha': 1.0},  # FIX: multi-chunk
      {'name': 'mvt-alpha0.7', 'type': 'mvt',    'g_env_top_n': 1, 'alpha': 0.7}, # FIX: discount
      {'name': 'mvt-noenv',    'type': 'mvt_noenv'},  # fixed threshold ablation
      {'name': 'oracle',       'type': 'oracle'},
  ]

  results = []  # per-question results
  cumulative_cost = 0.0

  for q in validation_questions:  # ~223 questions
      question = q['input_parsed']['question']
      paper_sections = get_sections_for_paper(q)
      gold_answer = q['output_parsed']['gold_answer']  # may be list or string
      gold_chunk_ids = q['output_parsed']['evidence_chunk_ids']
      gold_section_names = q['output_parsed']['evidence_section_names']
      is_multihop = q['metadata_is_multihop']
      query_emb = embed(question)

      q_result = {'question_id': q['metadata_question_id'],
                  'is_multihop': is_multihop, 'variants': {}}

      for variant in VARIANTS:
          # 1. Retrieve chunks
          if variant['type'] == 'topk':
              retrieved = topk_retrieve(query_emb, all_chunks, chunk_embs, variant['k'])
          elif variant['type'] == 'mvt':
              retrieved = mvt_retrieve(query_emb, paper_sections, chunk_embs,
                                       g_env_top_n=variant['g_env_top_n'],
                                       alpha=variant['alpha'])
          elif variant['type'] == 'mvt_noenv':
              retrieved = mvt_noenv_retrieve(query_emb, paper_sections, chunk_embs, fixed_threshold)
          else:  # oracle
              retrieved = gold_chunk_ids

          # 2. Build context from retrieved chunks
          context_texts = [chunk_id_to_text[cid] for cid in retrieved if cid in chunk_id_to_text]

          # 3. LLM answer generation
          if cumulative_cost >= 1.40:  # safety stop
              predicted_answer = '[BUDGET_EXCEEDED]'
          else:
              prompt = build_prompt(question, context_texts)
              predicted_answer, cost = call_openrouter(OPENROUTER_MODEL, prompt)
              cumulative_cost += cost

          # 4. Compute metrics
          gold_list = gold_answer if isinstance(gold_answer, list) else [gold_answer]
          em = exact_match(predicted_answer, gold_list)
          f1 = token_f1(predicted_answer, gold_list)
          sec_rec = section_recall(retrieved, gold_section_names, chunk_id_to_section)
          n_chunks = len(retrieved)

          q_result['variants'][variant['name']] = {
              'retrieved_chunk_ids': retrieved,
              'predicted_answer': predicted_answer,
              'em': em, 'f1': f1,
              'n_chunks_retrieved': n_chunks,
              'section_recall': sec_rec,
          }

      results.append(q_result)

  # Aggregate metrics across all questions
  for variant_name in [v['name'] for v in VARIANTS]:
      avg_em = mean(r['variants'][variant_name]['em'] for r in results)
      avg_f1 = mean(r['variants'][variant_name]['f1'] for r in results)
      avg_chunks = mean(r['variants'][variant_name]['n_chunks_retrieved'] for r in results)
      avg_sec_rec = mean(r['variants'][variant_name]['section_recall'] for r in results)
      # Also compute for multihop subset
      multihop_results = [r for r in results if r['is_multihop']]
      ...

  # Bootstrap 95% CI for F1 differences (MVT vs top-k-5 as primary comparison)
  # 10000 bootstrap samples with paired resampling
  ```

  ## Step 10: Output

  ```python
  method_out = {
      'summary': {
          'n_questions': len(results),
          'n_multihop': sum(r['is_multihop'] for r in results),
          'total_cost_usd': cumulative_cost,
          'per_variant_aggregate': {
              variant_name: {
                  'mean_em': ..., 'mean_f1': ...,
                  'mean_chunks': ..., 'mean_section_recall': ...,
                  'multihop_mean_f1': ..., 'multihop_mean_section_recall': ...
              }
          },
          'bootstrap_ci_mvt_top3_vs_topk5_f1': [lower, upper],
          'bootstrap_ci_mvt_alpha07_vs_topk5_f1': [lower, upper],
          'pilot_g_env_median': fixed_threshold,
      },
      'per_question': results  # full detail for analysis
  }

  with open('method_out.json', 'w') as f:
      json.dump(method_out, f, indent=2)
  ```

  ## Key Implementation Notes

  1. **Data parsing**: The dependency dataset stores input/output as JSON strings—parse with `json.loads()`.
     `sections_summary` in the input JSON contains the full chunk list per section.

  2. **Embedding caching**: Save to `embeddings_cache.pkl` after first run. Check for cache file at start.

  3. **Gold answer format**: QASPER answers can be 'yes'/'no', extractive spans, or lists. The dataset
     artifact normalizes these; treat as list always.

  4. **EM=0 debug**: Before full run, spot-check 5 examples: print raw predicted answer, gold answers,
     and normalized versions. If all EM=0 even on oracle condition, the LLM prompt/parsing is broken.

  5. **Oracle F1 ceiling**: Oracle should achieve ~0.4-0.6 F1 on QASPER (known upper bound from literature).
     If oracle F1 < 0.3, the LLM call or answer parsing is likely broken—fix before full run.

  6. **Sections parsing**: The sections_summary is a list of section objects. Each section has `chunks`
     list. Re-group by `normalized_section` name to get IMRaD categories.

  7. **Papers with few sections**: If a paper has only 1-2 sections, MVT switching is trivial.
     These are excluded by the dataset (>=3 distinct sections filter) but verify at runtime.

  8. **OpenRouter setup**: Use the aii-openrouter-llms skill to get the API key and call pattern.
     All calls must go through OpenRouter—no direct Anthropic/OpenAI endpoints.
fallback_plan: |-
  ## Primary Fallback: Reduce LLM calls

  If cost is tracking high (>$0.80 after 100 questions), reduce variants by dropping top-k-10 and oracle, which are less critical for the core hypothesis. Run 5 core variants: top-k-1, top-k-3, top-k-5, mvt-top3, mvt-alpha0.7.

  ## Secondary Fallback: Skip LLM, use retrieval-only metrics

  If OpenRouter is unavailable or budget is too tight, skip LLM generation entirely and report only:
  - Retrieval precision/recall (gold evidence chunks retrieved)
  - Section recall
  - N chunks retrieved per question

  These metrics directly test the core hypothesis (does multi-chunk G_env improve retrieval quality?) without needing generation. Report retrieval F1 (did we retrieve the right chunks?) instead of answer F1.

  ## Embedding Fallback

  If sentence-transformers is slow on CPU, use `paraphrase-MiniLM-L3-v2` (smaller/faster) or TF-IDF cosine similarity as a zero-dependency alternative. TF-IDF is much faster and still captures keyword overlap.

  ## Data Fallback

  If sections_summary doesn't contain full chunk text (parse error), fall back to re-loading QASPER directly from HuggingFace (`allenai/qasper`, validation split) and re-parsing sections inline using the same logic as the dataset artifact's data.py.

  ## Truncation Fallback

  If 223 questions take too long (>5h with embeddings+LLM), run on 100 questions (first 50 single-hop + first 50 multihop) and report results on that subset with a note.
testing_plan: |-
  ## Step 0: Verify Data Loading (5 min)

  ```python
  import json
  data = json.load(open(DEP_DATA))
  validation = [x for x in data if x['metadata_fold'] == 1]
  print(f'Validation size: {len(validation)}')
  print('First example input keys:', json.loads(validation[0]['input']).keys())
  print('First example output keys:', json.loads(validation[0]['output']).keys())
  print('Is multihop distribution:', sum(x['metadata_is_multihop'] for x in validation))
  ```
  Expect: ~223 validation examples, input has question+sections_summary, output has gold_answer+evidence_chunk_ids.

  ## Step 1: Mini smoke test on 5 examples (15 min)

  Run ALL variants on 5 questions (mix of single-hop and multihop).
  - Check embeddings work: cosine sims in [0.0, 1.0] range
  - Check G_env estimation produces non-zero values
  - Check MVT retrieves between 1-15 chunks (not always 0 or 15)
  - Check oracle retrieves the correct chunk IDs
  - Check LLM returns non-empty string (1 LLM call to verify API)
  - Check EM normalization: manually verify normalized predicted vs gold for 2 examples
  - Print per-example summary table: variant | n_chunks | f1 | em

  ## Step 2: EM debug check (5 min)

  For oracle condition on 5 examples:
  - Print raw LLM output
  - Print gold_answer
  - Print normalize(pred) vs normalize(gold)
  - If EM=0 for oracle on obvious 'yes'/'no' answers, fix normalization
  - Target: oracle F1 >= 0.30 on 5-example sample

  ## Step 3: Embedding cache check (2 min)

  After first mini run, verify `embeddings_cache.pkl` exists and reload correctly. Second mini run should be faster.

  ## Step 4: 50-question validation run (30 min)

  Run all variants on 50 questions before full 223.
  - Verify cost tracking: cumulative_cost after 50q x 10 variants should be ~$0.40
  - Verify multihop questions are present (should be ~17 of 50)
  - Check aggregate F1 table looks reasonable: oracle > top-k-5 > top-k-1
  - If top-k-5 F1 is still ~0.190 (matching iter1), data pipeline is consistent
  - Check mvt-top3 F1 vs mvt-top1 F1: expect improvement (this is the core hypothesis)

  ## Full run completion signals

  - Oracle F1 >= 0.35 (literature upper bound for 8B model on QASPER is ~0.40-0.50)
  - Top-k-5 F1 ~0.17-0.22 (within range of published results)
  - MVT-top3 retrieves more chunks than MVT-top1 (G_env reduced → less aggressive switching)
  - Bootstrap CI for MVT-top3 vs top-k-5 F1: check whether CI excludes zero (confirms hypothesis)
  - Cost <= $1.00 total
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

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

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

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
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [13] SYSTEM-USER prompt · 2026-07-18 16:43:08 UTC

```
[Your previous response had no visible output. Please continue and produce a user-visible response.]
```

### [14] SYSTEM-USER prompt · 2026-07-18 16:43:14 UTC

```
<task-notification>
<task-id>bdgbcregc</task-id>
<tool-use-id>toolu_018AqywFe48HHn6ZxbJGkZrM</tool-use-id>
<output-file>/tmp/claude-0/-ai-inventor-aii-data-runs-run-4kY-r-e962fK-3-invention-loop-iter-2-gen-art-gen-art-experiment-1/c3d5788f-5cb9-49ef-967b-a4e0d5cf7a05/tasks/bdgbcregc.output</output-file>
<status>completed</status>
<summary>Background command "cd /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
timeout 300 .venv/bin/python method.py --smoke-test 2&gt;&amp;1 | tee logs/smoke.log | tail -40" completed (exit code 0)</summary>
</task-notification>
```

### [15] SYSTEM-USER prompt · 2026-07-18 16:43:14 UTC

```
<task-notification>
<task-id>bmd9e3enz</task-id>
<tool-use-id>toolu_01YJb5vSVdPFawk8dNfbtUpx</tool-use-id>
<output-file>/tmp/claude-0/-ai-inventor-aii-data-runs-run-4kY-r-e962fK-3-invention-loop-iter-2-gen-art-gen-art-experiment-1/c3d5788f-5cb9-49ef-967b-a4e0d5cf7a05/tasks/bmd9e3enz.output</output-file>
<status>completed</status>
<summary>Background command "until grep -q "LLM done\|RESULTS SUMMARY\|Error\|Traceback\|BUDGET" /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/logs/smoke.log 2&gt;/dev/null; do sleep 5; done &amp;&amp; tail -30 /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/logs/smoke.log" completed (exit code 0)</summary>
</task-notification>
```

### [16] SYSTEM-USER prompt · 2026-07-18 16:43:54 UTC

```
[Your previous response had no visible output. Please continue and produce a user-visible response.]
```

### [17] SYSTEM-USER prompt · 2026-07-18 16:44:00 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 1/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```

### [18] SYSTEM-USER prompt · 2026-07-18 16:44:36 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 2/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```

### [19] SYSTEM-USER prompt · 2026-07-18 16:45:32 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 3/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```

### [20] SYSTEM-USER prompt · 2026-07-18 16:45:52 UTC

```
[Your previous response had no visible output. Please continue and produce a user-visible response.]
```
