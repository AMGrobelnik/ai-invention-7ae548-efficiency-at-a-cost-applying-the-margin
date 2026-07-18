# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_paper_text`
> Run: `run_4kY-r_e962fK` — Efficiency at a Cost: Applying the Marginal Value Theorem to Scientific Document Retrieval
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 16:46:14 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A research paper writer (Step 3.4: GEN_PAPER_TEXT in the invention loop)

You received the hypothesis, all artifacts, the previous paper draft (if any), and reviewer feedback.
Write a complete paper draft with figure placeholders.

Publication-quality paper → strong contribution. Weak paper → wasted iteration.
</your_role>
</ai_inventor_context>

<research_methodology>
Write like a researcher drafting a paper, not a chatbot summarizing bullet points.

- Structure as a paper would: research question → methodology → results → analysis → limitations. Not a list of "we did X, then Y."
- Ground every claim in specific artifacts and specific numbers. "Results show improvement" is empty — state effect sizes, baselines, and conditions.
- Be honest about what worked, what didn't, and why. Don't spin failures as "future work."
- The paper's headline contribution should be a positive or surprising finding. Negative results are valuable context but should not be the primary narrative — lead with what works.
- Address reviewer feedback from previous iterations explicitly — show you've thought about each critique.
</research_methodology>

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

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

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
</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

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

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

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

<all_artifacts>
FULL EVIDENCE BASE: All 4 research artifacts across all iterations.

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

--- Item 4 ---
id: art_KbNBwRPCMWDx
type: evaluation
title: 'MVT-RAG Evaluation: F1, Pareto & Bootstrap Analysis'
summary: >-
  Full evaluation of MVT-RAG and 8 baselines on QASPER (n=223 questions, 100 papers). Key results: VERDICT=PARTIAL — MVT-RAG
  is Pareto-non-dominated (1.3 chunks/question vs 5.0 for topk_5), but achieves lower F1 (0.138 vs 0.217 for topk_5). Metrics
  computed: (1) Token-level F1 recomputed with QASPER-style normalization — our values closely match stored values (high per-example
  correlation); (2) EM=0.0 confirmed genuine — strict EM=0.0 across all methods because QASPER gold answers contain citation
  keys (BIBREF*) never reproduced verbatim by LLMs; lenient EM also near-zero due to paraphrasing; (3) Oracle retrieval F1:
  MVT-RAG=0.140 vs topk_5=0.441 — oracle gap of 0.301 explains the retrieval under-performance (MVT stops too early); (4)
  Pareto frontier includes mvt_rag, mvt_noenv, topk_3, topk_5, topk_10, thresh_0_5, no_rag — MVT-RAG is non-dominated; (5)
  G_env ablation: p=0.68, CI=[-0.007, 0.010] includes zero — ecology-derived adaptive G_env provides NO significant benefit
  over fixed threshold=0.5; (6) 36-pair bootstrap significance matrix (10k resamples): MVT-RAG significantly worse than topk_3/5/10/bm25
  (p≈1.0), not significantly different from thresh_0.5 (similar chunk count); (7) Multi-hop subgroup (questions from papers
  with ≥3 questions, n=223): no advantage for MVT-RAG; (8) G_env distribution: mean=0.272, std=0.075 — correlation with chunks
  r≈-0.1 and F1 gap r≈0.05 (weak). Root cause: G_env threshold too aggressive causing under-retrieval, not a generation failure.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 1 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

type: evaluation
title: 'MVT-RAG Evaluation: F1, Pareto & Bootstrap Analysis'
id: art_KbNBwRPCMWDx
summary: >-
  Full evaluation of MVT-RAG and 8 baselines on QASPER (n=223 questions, 100 papers). Key results: VERDICT=PARTIAL — MVT-RAG
  is Pareto-non-dominated (1.3 chunks/question vs 5.0 for topk_5), but achieves lower F1 (0.138 vs 0.217 for topk_5). Metrics
  computed: (1) Token-level F1 recomputed with QASPER-style normalization — our values closely match stored values (high per-example
  correlation); (2) EM=0.0 confirmed genuine — strict EM=0.0 across all methods because QASPER gold answers contain citation
  keys (BIBREF*) never reproduced verbatim by LLMs; lenient EM also near-zero due to paraphrasing; (3) Oracle retrieval F1:
  MVT-RAG=0.140 vs topk_5=0.441 — oracle gap of 0.301 explains the retrieval under-performance (MVT stops too early); (4)
  Pareto frontier includes mvt_rag, mvt_noenv, topk_3, topk_5, topk_10, thresh_0_5, no_rag — MVT-RAG is non-dominated; (5)
  G_env ablation: p=0.68, CI=[-0.007, 0.010] includes zero — ecology-derived adaptive G_env provides NO significant benefit
  over fixed threshold=0.5; (6) 36-pair bootstrap significance matrix (10k resamples): MVT-RAG significantly worse than topk_3/5/10/bm25
  (p≈1.0), not significantly different from thresh_0.5 (similar chunk count); (7) Multi-hop subgroup (questions from papers
  with ≥3 questions, n=223): no advantage for MVT-RAG; (8) G_env distribution: mean=0.272, std=0.075 — correlation with chunks
  r≈-0.1 and F1 gap r≈0.05 (weak). Root cause: G_env threshold too aggressive causing under-retrieval, not a generation failure.
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
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
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 16:46:14 UTC

```
Improving retrieval-augmented generation for long scientific documents
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-07-18 16:46:20 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: Academic paper writing guidance for AI research. Covers paper structure, figure placeholders, bibliography building with Semantic Scholar, and citation rules. Does NOT cover LaTeX compilation or figure file generation — see aii-paper-to-latex for that.
---

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-07-18 16:46:26 UTC

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
