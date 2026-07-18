#!/usr/bin/env python3
"""MVT-RAG vs baselines on QASPER scientific QA dataset.

Implements Marginal Value Theorem-based section switching for RAG retrieval,
comparing against fixed-k dense retrieval, BM25, confidence-threshold baselines.
"""

import asyncio
import gc
import json
import math
import os
import resource
import sys
from pathlib import Path
from typing import Any

import aiohttp
import numpy as np
import psutil
from loguru import logger
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# ── Hardware detection ──────────────────────────────────────────────────────
def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float:
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError):
            pass
    return psutil.virtual_memory().total / 1e9

NUM_CPUS = _detect_cpus()
TOTAL_RAM_GB = _container_ram_gb()
RAM_BUDGET = int(TOTAL_RAM_GB * 0.75 * 1e9)  # 75% of container RAM
logger.info(f"Hardware: {NUM_CPUS} CPUs, {TOTAL_RAM_GB:.1f} GB RAM")
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

# ── Config ──────────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "meta-llama/llama-3.1-8b-instruct"
COST_PER_CALL_USD = 0.0002  # ~100 in + 200 out tokens at llama-3.1-8b pricing
COST_LIMIT = 8.0
N_PAPERS = int(os.environ.get("N_PAPERS", "100"))
MAX_CHUNKS_CAP = 20  # prevent degenerate MVT with very low G_env
API_CONCURRENCY = 8
EMBED_BATCH = 128

WORKSPACE = Path(__file__).parent
OUTPUT_PATH = WORKSPACE / "method_out.json"
MINI_N = int(os.environ.get("MINI_N", "0"))  # if >0, only process that many papers

METHODS = [
    "mvt_rag", "mvt_noenv",
    "topk_3", "topk_5", "topk_10",
    "bm25_5", "thresh_0.3", "thresh_0.5",
    "no_rag",
]

# ── Data loading ─────────────────────────────────────────────────────────────
def load_qasper(n_papers: int) -> list[dict]:
    from datasets import load_dataset
    logger.info("Loading QASPER validation split...")
    ds = load_dataset("allenai/qasper", split="validation", trust_remote_code=True)
    papers = list(ds)[:n_papers]
    logger.info(f"Loaded {len(papers)} papers")
    return papers

def parse_paper(paper: dict) -> list[dict]:
    """Parse paper into sections with chunks.

    QASPER full_text is a columnar dict:
      {"section_name": [str, ...], "paragraphs": [[str, ...], ...]}
    """
    sections = []
    ft = paper.get("full_text") or {}
    if isinstance(ft, dict):
        names = ft.get("section_name") or []
        paragraphs_list = ft.get("paragraphs") or []
        for name, paras in zip(names, paragraphs_list):
            name = (name or "unknown").strip() or "unknown"
            paras = paras or []
            chunks = [p.strip() for p in paras if isinstance(p, str) and p.strip()]
            if chunks:
                sections.append({"name": name, "chunks": chunks})
    elif isinstance(ft, list):
        for section in ft:
            name = (section.get("section_name") or "unknown").strip() or "unknown"
            paras = section.get("paragraphs") or []
            chunks = [p.strip() for p in paras if isinstance(p, str) and p.strip()]
            if chunks:
                sections.append({"name": name, "chunks": chunks})
    if not sections:
        abstract = paper.get("abstract", "")
        if abstract:
            sections.append({"name": "abstract", "chunks": [abstract]})
    return sections

# ── Embedding ────────────────────────────────────────────────────────────────
_embed_model = None

def get_embed_model():
    global _embed_model
    if _embed_model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading SentenceTransformer all-MiniLM-L6-v2...")
        _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Embedding model loaded")
    return _embed_model

def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_embed_model()
    return model.encode(texts, batch_size=EMBED_BATCH, show_progress_bar=False, normalize_embeddings=True)

def embed_paper(sections: list[dict]) -> tuple[list[tuple[str, str]], np.ndarray]:
    """Returns (chunk_meta, embeddings). chunk_meta = list of (section_name, chunk_text)."""
    chunk_meta = [(s["name"], c) for s in sections for c in s["chunks"]]
    texts = [c for _, c in chunk_meta]
    embs = embed_texts(texts)
    return chunk_meta, embs

# ── Retrieval methods ─────────────────────────────────────────────────────────
def _build_sec_map(chunk_meta: list[tuple[str, str]]) -> dict[str, list[int]]:
    sec_map: dict[str, list[int]] = {}
    for i, (sname, _) in enumerate(chunk_meta):
        sec_map.setdefault(sname, []).append(i)
    return sec_map

def mvt_rag(
    query_emb: np.ndarray,
    chunk_embs: np.ndarray,
    chunk_meta: list[tuple[str, str]],
) -> tuple[list[str], float]:
    """MVT-RAG: switch sections based on ecology-derived G_env threshold."""
    sec_map = _build_sec_map(chunk_meta)
    if not sec_map:
        return [], 0.0

    # G_env: mean of per-section best similarity → average patch quality
    sec_best_sims = []
    sec_potential: dict[str, float] = {}
    for sname, idxs in sec_map.items():
        sims = cosine_similarity(query_emb.reshape(1, -1), chunk_embs[idxs])[0]
        best = float(np.max(sims))
        sec_best_sims.append(best)
        sec_potential[sname] = best
    G_env = float(np.mean(sec_best_sims))

    retrieved: list[tuple[str, np.ndarray]] = []
    visited: set[str] = set()

    while len(retrieved) < MAX_CHUNKS_CAP:
        remaining = {s: p for s, p in sec_potential.items() if s not in visited}
        if not remaining:
            break
        cur_sec = max(remaining, key=remaining.get)  # type: ignore
        visited.add(cur_sec)

        ret_embs = [r[1] for r in retrieved]

        for idx in sec_map[cur_sec]:
            chunk_emb = chunk_embs[idx]
            chunk_text = chunk_meta[idx][1]

            q_sim = float(cosine_similarity(query_emb.reshape(1, -1), chunk_emb.reshape(1, -1))[0][0])

            if ret_embs:
                ret_arr = np.stack(ret_embs)
                max_ret_sim = float(np.max(cosine_similarity(chunk_emb.reshape(1, -1), ret_arr)[0]))
                novelty = 1.0 - max_ret_sim
            else:
                novelty = 1.0

            G_t = q_sim * novelty

            if G_t < G_env and retrieved:
                break  # switch to next section

            retrieved.append((chunk_text, chunk_emb))
            ret_embs.append(chunk_emb)

    return [r[0] for r in retrieved], G_env

def mvt_noenv_rag(
    query_emb: np.ndarray,
    chunk_embs: np.ndarray,
    chunk_meta: list[tuple[str, str]],
    threshold: float = 0.5,
) -> list[str]:
    """MVT ablation: fixed threshold instead of ecology-derived G_env."""
    sec_map = _build_sec_map(chunk_meta)
    if not sec_map:
        return []

    sec_potential: dict[str, float] = {}
    for sname, idxs in sec_map.items():
        sims = cosine_similarity(query_emb.reshape(1, -1), chunk_embs[idxs])[0]
        sec_potential[sname] = float(np.max(sims))

    retrieved: list[tuple[str, np.ndarray]] = []
    visited: set[str] = set()

    while len(retrieved) < MAX_CHUNKS_CAP:
        remaining = {s: p for s, p in sec_potential.items() if s not in visited}
        if not remaining:
            break
        cur_sec = max(remaining, key=remaining.get)  # type: ignore
        visited.add(cur_sec)

        ret_embs = [r[1] for r in retrieved]

        for idx in sec_map[cur_sec]:
            chunk_emb = chunk_embs[idx]
            chunk_text = chunk_meta[idx][1]

            q_sim = float(cosine_similarity(query_emb.reshape(1, -1), chunk_emb.reshape(1, -1))[0][0])

            if ret_embs:
                ret_arr = np.stack(ret_embs)
                max_ret_sim = float(np.max(cosine_similarity(chunk_emb.reshape(1, -1), ret_arr)[0]))
                novelty = 1.0 - max_ret_sim
            else:
                novelty = 1.0

            G_t = q_sim * novelty

            if G_t < threshold and retrieved:
                break

            retrieved.append((chunk_text, chunk_emb))
            ret_embs.append(chunk_emb)

    return [r[0] for r in retrieved]

def topk_dense(
    query_emb: np.ndarray,
    chunk_embs: np.ndarray,
    chunk_meta: list[tuple[str, str]],
    k: int,
) -> list[str]:
    sims = cosine_similarity(query_emb.reshape(1, -1), chunk_embs)[0]
    idxs = np.argsort(sims)[::-1][:k]
    return [chunk_meta[i][1] for i in idxs]

def bm25_retrieval(
    query: str,
    chunk_meta: list[tuple[str, str]],
    k: int = 5,
) -> list[str]:
    corpus = [c.split() for _, c in chunk_meta]
    if not corpus:
        return []
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(query.split())
    idxs = np.argsort(scores)[::-1][:k]
    return [chunk_meta[i][1] for i in idxs]

def threshold_retrieval(
    query_emb: np.ndarray,
    chunk_embs: np.ndarray,
    chunk_meta: list[tuple[str, str]],
    threshold: float,
) -> list[str]:
    sims = cosine_similarity(query_emb.reshape(1, -1), chunk_embs)[0]
    order = np.argsort(sims)[::-1]
    chunks = [chunk_meta[i][1] for i in order if sims[i] >= threshold]
    if not chunks:
        chunks = [chunk_meta[order[0]][1]]  # at least one
    return chunks[:MAX_CHUNKS_CAP]

# ── Oracle retrieval F1 ───────────────────────────────────────────────────────
def oracle_retrieval_f1(retrieved_chunks: list[str], gold_spans: list[str]) -> float:
    """Check if gold extractive spans appear in retrieved chunks."""
    if not gold_spans or not retrieved_chunks:
        return 0.0
    retrieved_text = " ".join(retrieved_chunks).lower()
    hits = sum(1 for span in gold_spans if span.lower().strip() in retrieved_text)
    return hits / len(gold_spans)

# ── Evaluation metrics ────────────────────────────────────────────────────────
def token_f1(pred: str, gold: str) -> float:
    pred_toks = set(pred.lower().split())
    gold_toks = set(gold.lower().split())
    if not pred_toks or not gold_toks:
        return 0.0
    common = pred_toks & gold_toks
    if not common:
        return 0.0
    p = len(common) / len(pred_toks)
    r = len(common) / len(gold_toks)
    return 2 * p * r / (p + r)

def best_f1(pred: str, gold_answers: list[str]) -> float:
    return max((token_f1(pred, g) for g in gold_answers), default=0.0)

def best_em(pred: str, gold_answers: list[str]) -> float:
    return max(
        (float(pred.strip().lower() == g.strip().lower()) for g in gold_answers),
        default=0.0,
    )

# ── LLM answer generation (async) ────────────────────────────────────────────
async def generate_answer_async(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    query: str,
    chunks: list[str],
) -> str:
    context = "\n\n".join(chunks[:10]) if chunks else "No context available."
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer concisely in 1-2 sentences:"
    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.0,
    }
    async with sem:
        for attempt in range(3):
            try:
                async with session.post(
                    OPENROUTER_BASE,
                    json=payload,
                    headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["choices"][0]["message"]["content"].strip()
                    elif resp.status == 429:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        text = await resp.text()
                        logger.warning(f"API error {resp.status}: {text[:200]}")
                        return ""
            except Exception as e:
                logger.warning(f"LLM call attempt {attempt+1} failed: {e}")
                await asyncio.sleep(2 ** attempt)
    return ""

# ── Bootstrap stat test ───────────────────────────────────────────────────────
def bootstrap_p(a: list[float], b: list[float], n: int = 5000) -> float:
    """Bootstrap p-value: P(mean(a) <= mean(b)) under resampling."""
    if not a or not b or len(a) != len(b):
        return float("nan")
    arr_a = np.array(a)
    arr_b = np.array(b)
    rng = np.random.default_rng(42)
    n_s = len(arr_a)
    obs_diff = np.mean(arr_a) - np.mean(arr_b)
    boot_diffs = []
    for _ in range(n):
        idx = rng.integers(0, n_s, n_s)
        boot_diffs.append(np.mean(arr_a[idx]) - np.mean(arr_b[idx]))
    return float(np.mean(np.array(boot_diffs) <= 0))

# ── Main experiment ───────────────────────────────────────────────────────────
@logger.catch(reraise=True)
def main() -> None:
    n_papers = MINI_N if MINI_N > 0 else N_PAPERS
    logger.info(f"Starting MVT-RAG experiment: {n_papers} papers, methods={METHODS}")

    papers = load_qasper(n_papers)

    # Preload embedding model once
    get_embed_model()

    # Collect all (paper, question, gold_answers, gold_spans, chunk_meta, chunk_embs)
    all_qas: list[dict[str, Any]] = []

    logger.info("Parsing papers and building QA pairs...")
    for paper in tqdm(papers, desc="Parsing papers"):
        sections = parse_paper(paper)
        if not sections:
            continue

        chunk_meta, chunk_embs = embed_paper(sections)
        if not chunk_meta:
            continue

        # qas is a columnar dict: {question: [...], answers: [...], ...}
        qas_col = paper.get("qas") or {}
        questions_list = qas_col.get("question") or [] if isinstance(qas_col, dict) else [q.get("question", "") for q in qas_col]
        answers_col = qas_col.get("answers") or [] if isinstance(qas_col, dict) else [q.get("answers", []) for q in qas_col]

        for question, answers_for_q in zip(questions_list, answers_col):
            question = (question or "").strip()
            if not question:
                continue

            gold_answers = []
            gold_spans = []
            # answers_for_q is {answer: [list of answer dicts]}
            ans_list = []
            if isinstance(answers_for_q, dict):
                ans_list = answers_for_q.get("answer") or []
            elif isinstance(answers_for_q, list):
                for item in answers_for_q:
                    if isinstance(item, dict):
                        inner = item.get("answer")
                        if isinstance(inner, list):
                            ans_list.extend(inner)
                        elif isinstance(inner, dict):
                            ans_list.append(inner)
                        else:
                            ans_list.append(item)

            for ans in ans_list:
                if not isinstance(ans, dict):
                    continue
                if ans.get("unanswerable"):
                    continue
                ffa = (ans.get("free_form_answer") or "").strip()
                if ffa:
                    gold_answers.append(ffa)
                for span in ans.get("extractive_spans") or []:
                    if span and span.strip():
                        gold_spans.append(span.strip())

            # Also accept extractive spans as gold answers when no free_form
            if not gold_answers and gold_spans:
                gold_answers = gold_spans[:3]  # use top 3 spans as gold
            if not gold_answers:
                continue

            all_qas.append({
                "paper_id": paper.get("id", ""),
                "question": question,
                "gold_answers": gold_answers,
                "gold_spans": gold_spans,
                "chunk_meta": chunk_meta,
                "chunk_embs": chunk_embs,
                "sections": sections,
            })

    logger.info(f"Total QA pairs: {len(all_qas)}")

    # ── Retrieval phase ────────────────────────────────────────────────────
    logger.info("Running retrieval methods...")
    per_question: list[dict[str, Any]] = []
    total_cost = 0.0

    for qa in tqdm(all_qas, desc="Retrieving"):
        question = qa["question"]
        chunk_meta = qa["chunk_meta"]
        chunk_embs = qa["chunk_embs"]
        sections = qa["sections"]
        gold_answers = qa["gold_answers"]
        gold_spans = qa["gold_spans"]

        query_emb = embed_texts([question])[0]

        mvt_chunks, g_env = mvt_rag(query_emb, chunk_embs, chunk_meta)

        method_chunks: dict[str, list[str]] = {
            "mvt_rag": mvt_chunks,
            "mvt_noenv": mvt_noenv_rag(query_emb, chunk_embs, chunk_meta),
            "topk_3": topk_dense(query_emb, chunk_embs, chunk_meta, 3),
            "topk_5": topk_dense(query_emb, chunk_embs, chunk_meta, 5),
            "topk_10": topk_dense(query_emb, chunk_embs, chunk_meta, 10),
            "bm25_5": bm25_retrieval(question, chunk_meta, 5),
            "thresh_0.3": threshold_retrieval(query_emb, chunk_embs, chunk_meta, 0.3),
            "thresh_0.5": threshold_retrieval(query_emb, chunk_embs, chunk_meta, 0.5),
            "no_rag": [],
        }

        # Oracle retrieval F1 (no LLM needed)
        oracle_f1s = {m: oracle_retrieval_f1(chunks, gold_spans) for m, chunks in method_chunks.items()}

        per_question.append({
            "paper_id": qa["paper_id"],
            "question": question,
            "gold_answers": gold_answers,
            "gold_spans": gold_spans,
            "method_chunks": {m: len(c) for m, c in method_chunks.items()},
            "method_chunks_text": method_chunks,
            "oracle_f1": oracle_f1s,
            "g_env": g_env,
        })

        # Budget check: 9 methods per question
        total_cost += COST_PER_CALL_USD * len(METHODS)
        if total_cost >= COST_LIMIT:
            logger.warning(f"Cost limit reached at {total_cost:.2f} USD, stopping")
            break

    logger.info(f"Retrieval done. Running LLM answer generation...")

    # ── LLM generation phase (async) ────────────────────────────────────────
    async def run_llm_phase() -> None:
        nonlocal total_cost
        sem = asyncio.Semaphore(API_CONCURRENCY)
        connector = aiohttp.TCPConnector(limit=API_CONCURRENCY * 2)
        async with aiohttp.ClientSession(connector=connector) as session:
            for pq in tqdm(per_question, desc="LLM answers"):
                if total_cost >= COST_LIMIT:
                    break
                tasks = {}
                for method in METHODS:
                    chunks = pq["method_chunks_text"][method]
                    tasks[method] = asyncio.create_task(
                        generate_answer_async(session, sem, pq["question"], chunks)
                    )
                answers = {}
                for method, task in tasks.items():
                    answers[method] = await task
                    total_cost += COST_PER_CALL_USD

                pq["answers"] = answers
                pq["f1"] = {m: best_f1(answers[m], pq["gold_answers"]) for m in METHODS}
                pq["em"] = {m: best_em(answers[m], pq["gold_answers"]) for m in METHODS}

    asyncio.run(run_llm_phase())
    logger.info(f"LLM phase done. Total cost: ${total_cost:.4f}")

    # ── Summary statistics ─────────────────────────────────────────────────
    def get_vals(key: str, method: str) -> list[float]:
        return [pq[key][method] for pq in per_question if key in pq and method in pq[key]]

    summary_stats: dict[str, Any] = {}
    for method in METHODS:
        f1s = get_vals("f1", method)
        ems = get_vals("em", method)
        oracle = get_vals("oracle_f1", method)
        n_chunks = [pq["method_chunks"][method] for pq in per_question]
        summary_stats[method] = {
            "mean_f1": float(np.mean(f1s)) if f1s else 0.0,
            "std_f1": float(np.std(f1s)) if f1s else 0.0,
            "mean_em": float(np.mean(ems)) if ems else 0.0,
            "mean_oracle_retrieval_f1": float(np.mean(oracle)) if oracle else 0.0,
            "mean_chunks": float(np.mean(n_chunks)) if n_chunks else 0.0,
            "n": len(f1s),
        }

    # Bootstrap p-values vs topk_5
    topk5_f1s = get_vals("f1", "topk_5")
    topk5_oracle = get_vals("oracle_f1", "topk_5")
    for method in METHODS:
        if method == "topk_5":
            continue
        mf1 = get_vals("f1", method)
        moracle = get_vals("oracle_f1", method)
        n = min(len(mf1), len(topk5_f1s))
        if n > 10:
            summary_stats[method]["p_vs_topk5_f1"] = bootstrap_p(mf1[:n], topk5_f1s[:n])
            summary_stats[method]["p_vs_topk5_oracle"] = bootstrap_p(moracle[:n], topk5_oracle[:n])

    logger.info("Summary stats:")
    for m, s in summary_stats.items():
        logger.info(
            f"  {m}: F1={s['mean_f1']:.3f} EM={s['mean_em']:.3f} "
            f"oracle={s['mean_oracle_retrieval_f1']:.3f} chunks={s['mean_chunks']:.1f} n={s['n']}"
        )

    # ── Format output for exp_gen_sol_out schema ───────────────────────────
    # Schema: {datasets: [{dataset, examples: [{input, output, predict_*, metadata_*}]}]}
    examples = []
    for pq in per_question:
        if "answers" not in pq:
            continue
        ex: dict[str, Any] = {
            "input": pq["question"],
            "output": pq["gold_answers"][0] if pq["gold_answers"] else "",
            "metadata_paper_id": str(pq["paper_id"]),
            "metadata_gold_answers": json.dumps(pq["gold_answers"]),
            "metadata_gold_spans": json.dumps(pq["gold_spans"][:5]),  # cap for size
            "metadata_g_env": str(round(pq["g_env"], 4)),
        }
        for method in METHODS:
            safe = method.replace(".", "_").replace("-", "_")
            ex[f"predict_{safe}"] = pq["answers"].get(method, "")
            ex[f"metadata_f1_{safe}"] = str(round(pq["f1"].get(method, 0.0), 4))
            ex[f"metadata_em_{safe}"] = str(round(pq["em"].get(method, 0.0), 4))
            ex[f"metadata_oracle_f1_{safe}"] = str(round(pq["oracle_f1"].get(method, 0.0), 4))
            ex[f"metadata_chunks_{safe}"] = str(pq["method_chunks"].get(method, 0))
        examples.append(ex)

    output = {
        "metadata": {
            "method_name": "MVT-RAG",
            "description": "Marginal Value Theorem-based section switching for RAG on QASPER",
            "llm_model": LLM_MODEL,
            "n_papers": len(papers),
            "n_questions": len(examples),
            "total_cost_usd": round(total_cost, 4),
            "retrieval_methods": METHODS,
            "summary_stats": summary_stats,
        },
        "datasets": [
            {
                "dataset": "allenai/qasper",
                "examples": examples,
            }
        ],
    }

    OUTPUT_PATH.write_text(json.dumps(output, indent=2))
    logger.info(f"Output written to {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size / 1e6:.1f} MB)")

    # Summary print
    logger.info("=== FINAL RESULTS ===")
    for m, s in summary_stats.items():
        p = s.get("p_vs_topk5_f1", float("nan"))
        logger.info(
            f"{m:15s}: F1={s['mean_f1']:.3f}±{s['std_f1']:.3f} "
            f"oracle={s['mean_oracle_retrieval_f1']:.3f} chunks={s['mean_chunks']:.1f} "
            f"p_vs_topk5={p:.3f}"
        )

if __name__ == "__main__":
    main()
