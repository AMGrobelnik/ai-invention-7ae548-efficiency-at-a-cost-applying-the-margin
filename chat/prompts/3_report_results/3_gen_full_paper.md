# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 17:19:20 UTC

````
<system-prompt>
<research_methodology>
Write like an experienced academic. Reviewers judge both the science and the writing.

- Claims must be proportional to evidence. Choose verbs carefully — "demonstrate," "observe," and "hypothesize" mean different things.
- Every result needs: what was measured, on what data, the numbers, and what they mean.
- Methodology must be specific enough to reproduce. Related work must be organized by theme, not a literature dump.
- State limitations honestly. Avoid both overclaiming and excessive hedging.
</research_methodology>

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
</system-prompt>

<prompt>
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_4kY-r_e962fK/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
abstract: >-
  Retrieval-augmented generation (RAG) over long scientific documents faces a fundamental coverage-versus-precision tradeoff:
  fixed-$k$ retrieval either misses critical evidence or floods the context window with irrelevant text. We propose MVT-RAG,
  which operationalizes the Marginal Value Theorem (MVT) from ecological foraging theory as an adaptive section-switching
  criterion for scientific RAG. The algorithm models each document section as a foraging patch and switches to the next most
  promising section when the current marginal information gain—query relevance weighted by novelty relative to already-retrieved
  content—falls below the document-wide environmental average $G_{\mathrm{env}}$. On the QASPER scientific QA benchmark ($n=223$
  questions, 100 papers), MVT-RAG achieves a 3.8$\times$ retrieval efficiency gain over top-$k$-5 (1.3 vs.\ 5.0 chunks per
  question) and is Pareto-non-dominated among all evaluated methods. However, MVT-RAG achieves F1=0.138 compared to 0.217
  for top-$k$-5, a statistically significant deficit ($\Delta=-0.079$, 95\% CI $[-0.102, -0.057]$). Oracle retrieval analysis
  confirms that the quality gap is driven entirely by under-retrieval (oracle F1=0.140 for MVT-RAG vs.\ 0.441 for top-$k$-5),
  and an ablation study—corrected from a prior version to use a threshold of 0.5, matching the dataset median $G_{\mathrm{env}}$—finds
  no statistically significant advantage for the ecology-derived adaptive threshold over a fixed comparator ($p=0.68$, CI
  $[-0.007, +0.010]$). We diagnose the root cause as systematic over-estimation of $G_{\mathrm{env}}$ from single-chunk section
  sampling and identify multi-chunk averaging as a direct, testable remedy. Strict exact match is zero for all methods—a genuine
  property of QASPER's citation-key gold answers, not a metric error—while lenient exact match reaches 0.121 for MVT-RAG vs.\
  0.265 for top-$k$-5.
paper_text: |-
  # Introduction

  Retrieval-augmented generation (RAG) [1] has become the dominant paradigm for grounding large language model (LLM) responses in document evidence. For short, topically uniform documents, global top-$k$ dense retrieval [2] performs well: a query is embedded, the $k$ nearest chunks are retrieved, and an LLM generates from the concatenated context. For long scientific papers—which can span 8,000–20,000 tokens distributed across structurally heterogeneous sections—the fixed-$k$ strategy faces a fundamental tradeoff. With $k$ too small, critical evidence in minority sections is missed; with $k$ too large, the context window fills with irrelevant text that degrades LLM output quality and increases inference cost.

  Scientific documents have a structural property that fixed-$k$ retrieval ignores: the IMRaD layout (Introduction, Methods, Results, Discussion) concentrates different types of information in predictable locations. A question about a specific experimental result points to Results; a question about motivation points to Introduction. Treating all chunks as exchangeable discards this structural signal.

  Adaptive retrieval methods such as FLARE [3] and IRCoT [4] address the question of *when* to retrieve by conditioning retrieval on generation uncertainty or chain-of-thought state. Stop-RAG [5] frames the continuation decision as a learned Markov decision process. These methods improve over fixed-$k$ in multi-hop settings but share a common limitation: they decide whether to retrieve more content globally, without modeling *which section* to draw from next.

  We propose MVT-RAG, which draws on the *Marginal Value Theorem* (MVT) from behavioral ecology [6] to provide a principled section-switching criterion. The MVT—originally derived to explain when a forager should leave a depleting resource patch—states that departure is optimal when the current marginal return rate equals the environment-wide average. Applied to RAG, document sections are patches, retrieved chunks deplete available information within a section, and the document-wide average similarity provides a natural estimate of the environmental return rate. The resulting algorithm is parameter-free (given $G_{\mathrm{env}}$), training-free, and requires no LLM calls during retrieval.

  [FIGURE:fig1]

  We evaluate MVT-RAG on QASPER [8], a benchmark of 888 full NLP papers with information-seeking questions and evidence annotations, using 223 questions from 100 validation papers. The results are mixed in a diagnostically informative way.

  **Summary of Contributions:**
  - MVT-RAG achieves F1=0.138, significantly below top-$k$-5 (F1=0.217, $\Delta=-0.079$, 95\% CI $[-0.102, -0.057]$, $p{<}0.001$), while retrieving 3.8$\times$ fewer chunks. The method is Pareto-non-dominated: no evaluated baseline achieves equal or higher F1 with equal or fewer chunks (Section 5).
  - Oracle retrieval analysis confirms that the quality deficit is entirely a retrieval failure, not a generation failure: MVT-RAG oracle F1=0.140 vs.\ top-$k$-5 oracle F1=0.441, a gap of 0.301 (Section 5).
  - We correct a threshold specification error from a prior version: MVT-NoEnv uses threshold=0.5 (matching the observed dataset median $G_{\mathrm{env}}=0.265$), not 0.3. With this correction, the $G_{\mathrm{env}}$ ablation finds no significant benefit for ecology-derived adaptive averaging over a matched fixed threshold ($\Delta=+0.002$, CI $[-0.007, +0.010]$, $p=0.68$, Section 6).
  - We explain the EM=0 anomaly: QASPER gold answers routinely contain literal BIBREF citation keys that no LLM reproduces verbatim, making strict EM uninformative. Lenient EM (gold-as-substring) reaches 0.121 for MVT-RAG vs.\ 0.265 for top-$k$-5 (Section 5).
  - We diagnose the root cause as $G_{\mathrm{env}}$ over-estimation from single-chunk sampling, identify multi-chunk averaging as the minimal fix, and provide a theoretical argument for its expected effect (Section 6).

  # Background

  ## Marginal Value Theorem

  The Marginal Value Theorem [6] addresses the optimal foraging problem: given an environment of heterogeneous resource patches that deplete as a forager extracts resources, when should the forager leave the current patch? Charnov showed that under mild regularity conditions (unimodal gain curves, constant travel cost), the optimal departure rule is: *leave the current patch when its instantaneous return rate equals the long-run average return rate across the entire environment*.

  Formally, if $g_t$ denotes the marginal gain at step $t$ within the current patch and $G_{\mathrm{env}}$ is the environment-wide average gain, the MVT switching condition is:
  $$g_t < G_{\mathrm{env}}$$
  This rule is parameter-free once $G_{\mathrm{env}}$ is estimated, and adapts automatically to the current environment without a hand-tuned threshold.

  ## Information Foraging Theory

  Pirolli [7] extended optimal foraging models to human information search, showing that users navigate information spaces—web pages, document corpora—using strategies analogous to biological foragers. Users follow navigational cues that predict information gain in adjacent regions, leaving a current source when its *information scent* drops relative to alternatives. This framing motivates using section headers and similarity scores as proxies for ecological patch membership and resource density.

  InForage [9] applies Information Foraging Theory with reinforcement learning to train a search controller for multi-source web retrieval across independent documents. Unlike InForage—which learns a policy and operates across independent documents—MVT-RAG applies the specific MVT optimality criterion to *intra-document* section switching within a single scientific paper, requiring no training. Moore [10] applies MVT to model human semantic memory retrieval as a descriptive cognitive model; our work is prescriptive, using MVT as an engineering design criterion with evaluable downstream consequences.

  # Method

  ## Section Parsing and IMRaD Normalization

  MVT-RAG treats each document section as a foraging patch. We parse sections from QASPER's columnar `section_name`/`paragraphs` schema and normalize section names to six IMRaD-inspired categories: *introduction*, *methods*, *results*, *discussion*, *related\_work*, and *other*. The normalization applies keyword matching on section headers (e.g., "experiment" and "evaluation" map to *results*; "approach" and "model" map to *methods*). Papers with fewer than three distinct normalized categories are excluded; 776 of 888 training papers and 265 of 281 validation papers pass this filter \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-7ae548-efficiency-at-a-cost-applying-the-margin/tree/main/round-1/dataset-1}}.

  Each paragraph within a section constitutes one chunk. All chunks and queries are encoded with `all-MiniLM-L6-v2` [11], a lightweight sentence embedding model.

  ## MVT-RAG Algorithm

  Let $\mathcal{S} = \{s_1, \ldots, s_m\}$ denote the set of document sections and $q$ the query vector. The algorithm proceeds in three phases:

  **Phase 1: Environment estimation.** For each section $s_i$, compute the best-matching chunk similarity:
  $$\hat{g}_i = \max_{c \in s_i} \cos(c, q)$$
  The environmental average is then $G_{\mathrm{env}} = \frac{1}{m} \sum_{i=1}^{m} \hat{g}_i$.

  **Phase 2: Adaptive retrieval.** Initialize an empty retrieved set $R = \emptyset$. At each step: (1) select the unvisited section $s^*$ with the highest $\hat{g}_{s^*}$; (2) retrieve chunks from $s^*$ in descending similarity order; (3) for each candidate chunk $c_t$, compute the marginal gain
  $$g_t = \cos(c_t, q) \cdot \left(1 - \max_{r \in R} \cos(c_t, r)\right)$$
  where the first factor captures query relevance and the second captures novelty relative to already-retrieved content; (4) if $g_t < G_{\mathrm{env}}$, mark $s^*$ as exhausted and switch to the next highest-potential section; otherwise, add $c_t$ to $R$.

  **Phase 3: Termination.** Stop when all sections are exhausted or abandoned. Return $R$.

  **MVT-NoEnv ablation.** To test whether the ecology-derived dynamic $G_{\mathrm{env}}$ is load-bearing, we define MVT-NoEnv as the same algorithm with $G_{\mathrm{env}}$ replaced by a fixed threshold of 0.5. This threshold was chosen to match the empirically observed dataset median $G_{\mathrm{env}}$ (median=0.265 over 223 questions \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-7ae548-efficiency-at-a-cost-applying-the-margin/tree/main/round-2/evaluation-1}}), providing a fair comparison: both variants operate at the same calibration point in the aggregate, differing only in whether the threshold adapts per-question.

  ## Answer Generation

  Retrieved chunks are concatenated in ranked order and passed to `meta-llama/llama-3.1-8b-instruct` via OpenRouter with the prompt: *"Answer the following question based only on the provided context. Be concise."* If no chunks are retrieved, the model is prompted without context (equivalent to the no-RAG baseline).

  # Experimental Setup

  ## Dataset

  We evaluate on QASPER [8], a benchmark of 888 full-text NLP research papers with question–answer pairs annotated with evidence paragraph spans. Our main experiment uses 100 papers from the validation split, covering 223 answerable questions. Questions are stratified by a multi-hop flag (122 multi-hop, 101 single-hop, defined as questions from papers with $\geq$3 questions in the validation set).

  Answer quality is measured with the canonical QASPER token-level F1 metric: for each question, F1 is computed between the predicted answer and each gold answer string after stopword and punctuation normalization, taking the maximum across gold answers. We also report *oracle retrieval F1*—the best F1 achievable by passing gold evidence chunks to the LLM—to separate retrieval quality from generation quality.

  **Note on exact match.** Strict EM is zero for all methods across all nine systems. This is a genuine property of QASPER, not a metric implementation error: QASPER gold answers frequently contain literal citation keys (``BIBREF19'', ``BIBREF31''), multi-token technical phrases, or partial sentences that LLMs never reproduce verbatim. We verified this by manually inspecting 20 randomly sampled questions where predicted answers were semantically correct but scored EM=0. As an additional signal, we report *lenient EM* (the gold answer is a substring of the prediction), which reaches 0.121 for MVT-RAG vs.\ 0.265 for top-$k$-5 .

  ## Baselines

  We compare MVT-RAG against eight systems:

  - **Top-$k$ dense** ($k \in \{3, 5, 10\}$): global nearest-neighbor retrieval using `all-MiniLM-L6-v2` embeddings.
  - **BM25-5**: BM25 [12] retrieval with $k=5$, providing a lexical baseline.
  - **Threshold-0.3 / Threshold-0.5**: FLARE-style [3] confidence-threshold retrieval that continues retrieving until all retrieved chunks have similarity below the threshold.
  - **MVT-NoEnv**: MVT framework with $G_{\mathrm{env}}$ replaced by a fixed threshold of 0.5 (see Section 3.2).
  - **No-RAG**: LLM prompted without any retrieved context.

  ## Statistical Testing

  All pairwise comparisons use paired bootstrap resampling with 10,000 replications. We report observed delta, 95\% confidence intervals, and two-tailed $p$-values. An effect is considered significant at $\alpha=0.05$.

  # Results

  [FIGURE:fig2]

  Table 1 presents the main results over 223 QASPER validation questions .

  | Method | F1 | Lenient EM | Chunks/Q | Oracle F1 |
  |---|---|---|---|---|
  | MVT-RAG | 0.138 | 0.121 | **1.30** | 0.140 |
  | MVT-NoEnv | 0.136 | 0.099 | 1.00 | 0.119 |
  | Top-$k$-3 | 0.189 | 0.211 | 3.00 | 0.341 |
  | Top-$k$-5 | 0.217 | 0.265 | 5.00 | 0.441 |
  | Top-$k$-10 | **0.220** | **0.309** | 10.00 | **0.596** |
  | BM25-5 | 0.198 | 0.206 | 5.00 | 0.338 |
  | Thresh-0.3 | 0.202 | 0.256 | 8.83 | 0.495 |
  | Thresh-0.5 | 0.165 | 0.152 | 2.44 | 0.249 |
  | No-RAG | 0.065 | 0.036 | 0.00 | 0.000 |

  **Retrieval efficiency.** MVT-RAG retrieves a mean of 1.30 chunks per question—3.8$\times$ fewer than top-$k$-5 and 6.8$\times$ fewer than Threshold-0.3. MVT-RAG significantly outperforms the no-RAG baseline (delta=+0.073, 95\% CI [+0.057, +0.091], $p{<}0.001$), confirming that even 1.3 chunks per question contributes meaningfully.

  **Answer quality deficit.** MVT-RAG achieves F1=0.138, significantly below top-$k$-5 (delta=$-$0.079, 95\% CI [$-$0.102, $-$0.057], $p{<}0.001$) and below top-$k$-3 (delta=$-$0.051, 95\% CI [$-$0.073, $-$0.031], $p{<}0.001$). MVT-RAG is not significantly different from Threshold-0.5 ($p=0.002$ in the unfavorable direction), which retrieves 2.44 chunks at F1=0.165.

  **Pareto analysis.** Despite the quality deficit, MVT-RAG is *Pareto-non-dominated*: no other evaluated method achieves equal or higher F1 with equal or fewer chunks . The nearest efficiency-matched comparators are no-RAG (0 chunks, F1=0.065) and Threshold-0.5 (2.44 chunks, F1=0.165). MVT-RAG occupies the efficiency frontier at 1.3 chunks, delivering F1=0.138—substantially better than no retrieval and better-than-noise compared to Threshold-0.5 ($\Delta=+0.027$, CI [$-$0.045, $-$0.010], $p=0.002$). While we do not have top-$k$-1 or top-$k$-2 as baselines, the Pareto frontier result establishes that the MVT criterion extracts more from 1.3 chunks than any fixed-threshold strategy at similar efficiency in this evaluation.

  **Oracle retrieval analysis.** The oracle retrieval F1 gap is the primary diagnostic: MVT-RAG achieves oracle F1=0.140, compared to 0.441 for top-$k$-5 (gap=0.301). Since oracle F1 measures whether gold evidence spans are present in the retrieved set irrespective of generation quality, this gap confirms that MVT-RAG's quality deficit is driven entirely by *under-retrieval*—the switching criterion abandons sections before the relevant evidence is collected. The LLM reader performs similarly given the same evidence; retrieval, not generation, is the bottleneck.

  # Analysis

  ## Corrected G_env Ablation

  [FIGURE:fig3]

  A prior version of this paper contained a specification error: it described MVT-NoEnv as using a fixed threshold of 0.3, while the code implemented threshold=0.5. This discrepancy potentially undermined the ablation's validity, since a stricter threshold (0.5 vs.\ dynamic G_env with mean 0.281) would spuriously resemble the MVT variant. We have corrected this: MVT-NoEnv now consistently uses threshold=0.5 throughout the code, artifacts, and paper, matching the observed dataset median $G_{\mathrm{env}}=0.265$ .

  With this correction, the ablation shows: F1 delta (MVT-RAG minus MVT-NoEnv) = +0.002, 95\% CI [$-$0.007, +0.010], $p=0.68$. The confidence interval is entirely within a negligibly small range and includes zero throughout. We conclude that the ecology-derived adaptive $G_{\mathrm{env}}$ mechanism provides no statistically significant benefit over a fixed threshold calibrated to the same aggregate level. Both variants retrieve approximately the same number of chunks per question (1.30 for MVT-RAG, 1.00 for MVT-NoEnv), confirming that at current estimation quality, the adaptive baseline does not yield a different operational point on the efficiency-quality curve.

  This null result has a clear mechanistic explanation. The MVT's theoretical advantage—automatic calibration to document content—requires that $G_{\mathrm{env}}$ estimated from a single best-matching chunk per section accurately reflects the true expected marginal return across the section. In QASPER, $G_{\mathrm{env}}$ has mean 0.281 and standard deviation 0.115 across 223 questions, with moderate negative correlation with chunks retrieved (Spearman $\rho=-0.408$, $p{<}0.001$). A higher $G_{\mathrm{env}}$ sets a more aggressive threshold and retrieves fewer chunks—but the correlation with per-question F1 gap is near zero ($\rho=-0.048$, $p=0.47$). This weak correlation indicates that the adaptive calibration is responsive to document similarity structure but not to the underlying information density that determines whether more chunks would actually help. The single-chunk estimate is too noisy to recover this signal.

  ## Diagnosis: G_env Over-Estimation and the Path to Correction

  The core failure mode is that the single-chunk $G_{\mathrm{env}}$ estimator systematically overestimates the expected marginal gain at the point where retrieval becomes productive. In QASPER, many questions have gold evidence in specific technical paragraphs surrounded by low-relevance content. The top-ranked chunk per section (used to compute $\hat{g}_i$) is often the one useful paragraph. Once it is retrieved, the stopping criterion triggers immediately—before adjacent paragraphs that provide complementary evidence are examined.

  The minimal correction is to replace the single-chunk estimator with a multi-chunk average:
  $$G_{\mathrm{env}}^{(K)} = \frac{1}{m} \sum_{i=1}^{m} \frac{1}{K} \sum_{j=1}^{K}epaspectratio` (figure*). Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

PLACEMENT BY ASPECT RATIO (use the `aspect_ratio` field on each figure):
- `21:9` (architecture diagrams / hero figures): \begin{figure*}[!t] (full two-column width, top of page). The hero architecture diagram should appear EARLY in the paper — typically at the top of page 2. Marker placement in paper_text already determines this; preserve it.
- `16:9` (comparisons, multi-panel results): \begin{figure*}[!t] for full-width or \begin{figure}[!htbp] for single-column.
- `4:3` / `1:1` / `3:2` / `3:4` / `9:16`: \begin{figure}[!htbp] (single-column).
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.

Improving retrieval-augmented generation for long scientific documents
</prompt> \cos(c_{i,j}, q)$$
  where $c_{i,j}$ is the $j$-th most similar chunk in section $s_i$. For $K=3$, this averages over the top three chunks per section, providing a more conservative baseline that accounts for the fact that relevant information is often distributed across multiple adjacent paragraphs rather than concentrated in one. Because the top-$K$ average is strictly less than or equal to the top-1 maximum, $G_{\mathrm{env}}^{(K)} \leq G_{\mathrm{env}}^{(1)}$ always, meaning the corrected estimator will systematically allow more retrieval per section before switching—exactly the direction needed. An alternative fix is a multiplicative discount $G_{\mathrm{eff}} = \alpha \cdot G_{\mathrm{env}}$ with $\alpha < 1$; both modifications are parameter-light and consistent with MVT variants that incorporate patch-depletion curves. We identify implementing and evaluating this variant as the most important next step.

  ## Multi-Hop Analysis

  For questions from papers with $\geq$3 questions in the validation set, which we use as a proxy for the multi-hop flag ($n=122$), MVT-RAG achieves F1=0.139 vs.\ top-$k$-5 F1=0.215. MVT-RAG underperforms on this subgroup at the same magnitude as the overall deficit, ruling out the hypothesis that the section-switching mechanism provides a special advantage for questions that require evidence from multiple sections.

  The multi-hop deficit is informative for a subtle reason: the MVT algorithm *does* switch sections—section traversal is operationally functional. The diagnosis is the same as the overall finding: the algorithm abandons each section too early, collecting too few chunks before switching, so that even when the correct set of sections is visited, the relevant paragraphs within each are often missed. A complete evaluation would track section recall—what fraction of gold-evidence sections are visited by MVT-RAG—but the current experiment does not expose this metric. We note this as a limitation and as a target for future diagnostic instrumentation.

  # Related Work

  ## Adaptive RAG

  FLARE [3] triggers retrieval when token-level generation probability falls below a confidence threshold, addressing the question of *when* to retrieve during generation. IRCoT [4] interleaves retrieval with chain-of-thought reasoning, using reasoning state to form retrieval queries. Both methods operate at the global document level without modeling section structure. Stop-RAG [5] formulates the retrieval continuation decision as a finite-horizon MDP with a learned stopping value function; it is the closest prior method in spirit to MVT-RAG but requires training data and does not model section selection. MVT-RAG's key distinction is that it combines section-level structure (selecting *where* to retrieve from next) with an analytically derived, training-free switching criterion.

  ## Hierarchical and Structure-Aware RAG

  Hierarchical RAG methods organize documents into tree structures and traverse them using similarity-based node selection. GraphReader [13] builds a graph over long documents and uses an LLM-driven agent to navigate it. These methods exploit structure more deeply than flat chunk retrieval but rely on LLM calls during the retrieval phase, making them substantially more expensive. MVT-RAG's section-switching requires no LLM calls during retrieval, relying only on dense similarity computation.

  ## Foraging Theory in Information Systems

  InForage [9] is the most closely related recent work: it applies Information Foraging Theory with reinforcement learning to train a search controller for multi-source web retrieval. The key distinctions from MVT-RAG are: (i) InForage is a trained RL policy; MVT-RAG applies the MVT criterion analytically without training; (ii) InForage operates over independent web documents; MVT-RAG targets sections within a single scientific paper. Moore [10] applies MVT to cognitive models of semantic memory retrieval as a descriptive exercise; our work uses MVT as an engineering design criterion with evaluable downstream consequences.

  ## QASPER and Scientific QA

  Dasigi et al. [8] introduced QASPER for information-seeking QA over full scientific papers, providing section-level evidence annotations that make it ideal for evaluating section-aware retrieval. No prior work has applied foraging-theoretic switching criteria to this benchmark. Prior QASPER baselines use passage-level retrieval followed by extractive or abstractive QA, without modeling section-level information distribution.

  # Discussion

  The main finding of this paper is simultaneously confirmatory and cautionary. MVT-RAG's ecological framing yields a concrete, interpretable algorithm that achieves real efficiency gains: 3.8$\times$ fewer retrieved chunks than top-$k$-5, with the method confirmed to lie on the Pareto efficiency frontier. These gains are not accompanied by competitive answer quality, and the diagnosis is specific: the $G_{\mathrm{env}}$ estimator is systematically too aggressive because single-chunk per-section sampling overestimates the true environmental return rate.

  The corrected G_env ablation (threshold=0.5, matching the dataset median) confirms that the ecology-derived adaptive calibration provides no measurable benefit over a fixed comparator at current estimation quality, isolating $G_{\mathrm{env}}$ estimation as the mechanistic bottleneck rather than the MVT switching framework itself.

  **Limitations.** First, our evaluation uses Llama-3.1-8B as the reader. Larger models with stronger instruction-following may tolerate sparse retrieved contexts better, potentially narrowing the F1 gap at 1.3 chunks per question. Second, QASPER's short, citation-heavy gold answers amplify the penalty for under-retrieval: when the one correct sentence is absent from the retrieved set, F1=0 regardless of answer quality. Third, the multi-hop analysis uses number of questions per paper as a proxy for cross-section evidence requirements; a more principled stratification would require annotating whether gold evidence spans cross section boundaries. Fourth, section parsing relies on header-based heuristics; papers with non-standard structures reduce the accuracy of section detection. Fifth, we do not evaluate top-$k$-1 or top-$k$-2 directly, which would provide the tightest efficiency-matched baselines; the Pareto frontier result is conditional on the nine methods tested.

  # Conclusion

  We have proposed and evaluated MVT-RAG, the first application of the Marginal Value Theorem from ecological foraging to adaptive section switching in scientific RAG. Treating document sections as foraging patches and switching sections when marginal semantic information gain falls below the document-wide average yields a training-free, LLM-call-free retrieval algorithm that achieves 3.8$\times$ fewer chunks per question than top-$k$-5 and is Pareto-non-dominated among evaluated methods. On QASPER, MVT-RAG significantly outperforms the no-RAG baseline (+0.073 F1, $p{<}0.001$) but significantly underperforms top-$k$-5 ($-$0.079 F1, $p{<}0.001$). Oracle retrieval analysis localizes the failure to under-retrieval, not generation quality. A corrected ablation study—reconciling a prior threshold specification error to use 0.5 matching the dataset median $G_{\mathrm{env}}$—finds no significant benefit for the ecology-derived adaptive threshold over a fixed comparator. We identify multi-chunk $G_{\mathrm{env}}$ averaging (mean of top-$K$ similarities per section) as the minimal, theoretically grounded fix and provide a mechanistic argument for why it will allow more retrieval per section without sacrificing the efficiency advantage.

  Future directions: (1) implement and evaluate the multi-chunk $G_{\mathrm{env}}^{(K)}$ estimator; (2) add section-visit recall as a diagnostic metric to assess whether the section-switching logic correctly identifies gold-evidence sections in multi-hop questions; (3) combine MVT switching with within-section cross-encoder re-ranking to improve oracle recall while preserving the framework's computational efficiency.

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
summary: >-
  MVT-RAG applies the Marginal Value Theorem from ecology to adaptive section switching in scientific RAG, treating document
  sections as foraging patches. On QASPER (223 questions), it achieves 3.8x retrieval efficiency over top-k-5 (1.3 vs 5.0
  chunks/question) and is Pareto-non-dominated, but achieves significantly lower F1 (0.138 vs 0.217). Oracle analysis confirms
  the deficit is entirely due to under-retrieval. A corrected ablation (threshold=0.5, matching dataset median G_env=0.265)
  finds no benefit for adaptive over fixed threshold (p=0.68). The root cause is G_env over-estimation from single-chunk section
  sampling; multi-chunk averaging is proposed as the minimal fix.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
title: MVT-RAG Algorithm Overview
caption: >-
  MVT-RAG pipeline for adaptive section switching in scientific RAG. Document sections are modeled as foraging patches; the
  algorithm estimates the environmental average return $G_{\mathrm{env}}$ from a lightweight initial pass, then iteratively
  retrieves from the highest-potential section and switches when marginal gain falls below $G_{\mathrm{env}}$.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right, on a white background. Five main components connected by arrows: (1) 'Scientific
  Paper' (gray box, icon of stacked pages) with label 'IMRaD Sections: Intro | Methods | Results | Discussion'. Arrow pointing
  right to (2) 'Environment Estimation' (blue box): 'G_env = mean of best-chunk similarity per section' with a small formula:
  G_env = (1/m) * sum(max_cos(c,q)). Arrow pointing right to (3) 'Adaptive Retrieval Loop' (green box, slightly taller): top
  sub-box reads 'Visit highest-potential section'; middle sub-box reads 'g_t = cos(c_t, q) * (1 - max cos(c_t, R))'; bottom
  sub-box reads 'if g_t < G_env → switch section'. Arrow pointing right to (4) 'Retrieved Chunks R' (light orange box): '~1.3
  chunks/question avg'. Arrow pointing right to (5) 'LLM Answer' (purple box): 'Llama-3.1-8B'. Below component (3), a small
  circular arrow labeled 'Iterative patch depletion'. Sans-serif font (Arial/Helvetica), clean white background, no 3D effects.
  Aspect ratio 21:9.
aspect_ratio: '21:9'
summary: >-
  Hero architecture diagram showing the MVT-RAG pipeline from document sections through environment estimation to adaptive
  retrieval and LLM answer generation.
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
title: Efficiency-Quality Tradeoff Across Methods
caption: >-
  Efficiency-quality Pareto frontier on QASPER ($n=223$ questions). Each point represents one retrieval method; x-axis is
  mean chunks retrieved per question (lower = more efficient); y-axis is token-level F1. The Pareto frontier (dashed line)
  connects non-dominated methods. MVT-RAG (star marker) lies on the frontier at 1.30 chunks/F1=0.138, between no-RAG and Threshold-0.5.
  No method achieves equal or higher F1 with equal or fewer chunks.
image_gen_detailed_description: >-
  Scatter plot on white background. X-axis: 'Mean Chunks Retrieved per Question' ranging from 0 to 11. Y-axis: 'Token-Level
  F1' ranging from 0.00 to 0.24. Nine data points: (1) 'No-RAG' at (0.0, 0.065), gray circle; (2) 'MVT-NoEnv' at (1.0, 0.136),
  orange circle; (3) 'MVT-RAG' at (1.30, 0.138), red star, slightly larger marker, labeled; (4) 'Thresh-0.5' at (2.44, 0.165),
  purple circle; (5) 'Top-k-3' at (3.0, 0.189), blue circle; (6) 'BM25-5' at (5.0, 0.198), green circle; (7) 'Top-k-5' at
  (5.0, 0.217), blue circle; (8) 'Thresh-0.3' at (8.83, 0.202), purple circle; (9) 'Top-k-10' at (10.0, 0.220), blue circle.
  Dashed gray step-line connecting Pareto-non-dominated points: No-RAG (0.0, 0.065) -> MVT-RAG (1.30, 0.138) -> Thresh-0.5
  (2.44, 0.165) -> Top-k-3 (3.0, 0.189) -> Top-k-5 (5.0, 0.217) -> Top-k-10 (10.0, 0.220), labeled 'Pareto frontier'. Legend
  in top-left. Sans-serif font. Grid lines light gray. Aspect ratio 16:9.
aspect_ratio: '21:9'
summary: >-
  Pareto frontier plot showing MVT-RAG lies on the efficiency-quality frontier at 1.3 chunks/question despite lower absolute
  F1 than top-k baselines.
figure_path: figures/fig2_v0.jpg

--- Item 3 ---
id: fig3
title: G_env Distribution and Ablation Results
caption: >-
  Left: Distribution of per-question $G_{\mathrm{env}}$ values (mean of best-chunk similarities per section) across 223 QASPER
  questions ($\mu=0.281$, $\sigma=0.115$, median=0.265). The MVT-NoEnv fixed threshold (0.5) is marked; note it lies above
  the median, making it more conservative than the average adaptive threshold. Right: Bootstrap confidence intervals for the
  G_env ablation (MVT-RAG minus MVT-NoEnv, $\Delta=+0.002$, 95\% CI $[-0.007, +0.010]$, $p=0.68$), confirming no significant
  benefit for the adaptive mechanism.
image_gen_detailed_description: >-
  Two-panel figure side by side on white background. Left panel: Histogram of G_env values. X-axis: 'G_env (per-question environmental
  average)' from 0.0 to 0.7. Y-axis: 'Count' from 0 to 35. Histogram bins of width 0.05, steel blue bars, approximately bell-shaped
  with peak around 0.25-0.30. Mean line at x=0.281 (solid red vertical line, labeled 'mean=0.281'). Median line at x=0.265
  (dashed orange vertical line, labeled 'median=0.265'). MVT-NoEnv threshold line at x=0.5 (solid dark gray vertical line,
  labeled 'fixed threshold=0.5'). Title 'G_env Distribution (n=223)'. Right panel: Forest plot / CI bar chart. Single row:
  'MVT-RAG vs MVT-NoEnv' with point estimate at x=+0.002 (small black dot), horizontal error bar from x=-0.007 to x=+0.010
  (95% CI), thick line from -0.007 to +0.010. Vertical dashed line at x=0 (null). X-axis: 'F1 Delta (MVT-RAG minus MVT-NoEnv)'
  from -0.02 to +0.02. Y-axis label 'Method Comparison'. Title 'G_env Ablation (p=0.68)'. Text annotation: 'CI includes zero:
  no significant benefit'. Sans-serif font. Aspect ratio 16:9.
aspect_ratio: '21:9'
summary: >-
  Shows G_env distribution (mean 0.281, median 0.265) and ablation CI confirming no significant benefit from adaptive G_env
  over fixed threshold.
figure_path: figures/fig3_v0.jpg
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/filename.jpg}
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure*|figure}[placement], \includegraphics, \caption, \label, \end{...} — pick env + placement by the figure's `aspect_ratio` field (see PLACEMENT below). Constrain every \includegraphics with `width=\linewidth,height=0.4\textheight,keepaspectratio` (single-column) or `width=\textwidth,height=0.45\textheight,ke
````

### [2] SKILL-INPUT — aii-paper-to-latex · 2026-07-18 17:19:25 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: LaTeX paper assembly and compilation. Covers document setup, figure inclusion from pre-generated JPEGs, compilation process, and output files. Use when assembling a paper from pre-written text and pre-generated figures into a compiled PDF.
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figure JPEGs, and bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.jpg}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS use `[!htbp]` float placement (NOT `[t]` or `[h]` alone)
- ALWAYS constrain with `width` and `keepaspectratio` to prevent page takeover
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/*.jpg` — all figure images (pre-generated, copied into workspace)
````

### [3] SKILL-INPUT — aii-semscholar-bib · 2026-07-18 17:19:29 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
