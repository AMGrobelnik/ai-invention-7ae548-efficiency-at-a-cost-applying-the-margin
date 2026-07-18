#!/usr/bin/env python3
"""MVT-RAG vs Baselines evaluation on QASPER: F1, EM, retrieval efficiency, bootstrap tests."""

import gc
import json
import math
import os
import re
import resource
import string
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# ── Resource limits (29GB container, 4 CPUs, no GPU) ──────────────────────────
RAM_LIMIT = int(24 * 1024**3)
resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT, RAM_LIMIT))

WORKSPACE = Path(__file__).parent
DATASET_PATH = Path(
    "/ai-inventor/aii_data/runs/run_4kY-r_e962fK/3_invention_loop/iter_1/"
    "gen_art/gen_art_dataset_1/temp/datasets/full_allenai_qasper_qasper_validation.json"
)

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "meta-llama/llama-3.1-8b-instruct"
COST_PER_CALL = 0.0006  # conservative estimate for llama 3.1 8b via OpenRouter
COST_LIMIT = 8.0

# ── QASPER answer normalization (Dasigi et al. 2021 style) ────────────────────

def normalize_answer(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = s.translate(str.maketrans("", "", string.punctuation))
    return " ".join(s.split())


def token_f1(pred: str, gold: str) -> float:
    p_toks = normalize_answer(pred).split()
    g_toks = normalize_answer(gold).split()
    if not p_toks or not g_toks:
        return 0.0
    common = set(p_toks) & set(g_toks)
    if not common:
        return 0.0
    prec = len(common) / len(p_toks)
    rec = len(common) / len(g_toks)
    return 2 * prec * rec / (prec + rec)


def best_f1(pred: str, golds: list) -> float:
    return max((token_f1(pred, g) for g in golds), default=0.0)


def best_em(pred: str, golds: list) -> float:
    np_pred = normalize_answer(pred)
    return float(any(np_pred == normalize_answer(g) for g in golds))


# ── Document parsing ──────────────────────────────────────────────────────────

def parse_paper(paper: dict) -> list:
    """Return list of {name, chunks} sections."""
    ft = paper.get("full_text", {})
    names = ft.get("section_name", [])
    paragraphs = ft.get("paragraphs", [])
    sections = []
    for name, paras in zip(names, paragraphs):
        chunks = [p.strip() for p in paras if isinstance(p, str) and p.strip()]
        if chunks:
            sections.append({"name": name or "unknown", "chunks": chunks})
    return sections


def flatten_chunks(sections: list) -> tuple:
    """Return (chunk_meta, chunk_texts) where chunk_meta = [(section_name, chunk_text)]."""
    meta, texts = [], []
    for sec in sections:
        for c in sec["chunks"]:
            meta.append((sec["name"], c))
            texts.append(c)
    return meta, texts


# ── Retrieval methods ─────────────────────────────────────────────────────────

def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """a: (D,), b: (N, D) → (N,) similarities."""
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return b_norm @ a_norm


def mvt_rag(query_emb: np.ndarray, sections: list, chunk_embs: np.ndarray, chunk_meta: list) -> tuple:
    """MVT-RAG: stop retrieving when marginal gain < environment average G_env."""
    sec_map = defaultdict(list)
    for i, (sname, _) in enumerate(chunk_meta):
        sec_map[sname].append(i)

    # G_env = mean of per-section best similarity
    g_env_values = []
    for sname, idxs in sec_map.items():
        sims = cosine_sim(query_emb, chunk_embs[idxs])
        g_env_values.append(float(np.max(sims)))
    G_env = float(np.mean(g_env_values)) if g_env_values else 0.3

    sec_potential = {
        sname: float(np.max(cosine_sim(query_emb, chunk_embs[idxs])))
        for sname, idxs in sec_map.items()
    }

    retrieved_texts = []
    retrieved_embs = []
    visited = set()

    while True:
        remaining = {s: p for s, p in sec_potential.items() if s not in visited}
        if not remaining:
            break
        cur_sec = max(remaining, key=remaining.get)
        visited.add(cur_sec)

        for idx in sec_map[cur_sec]:
            chunk_emb = chunk_embs[idx]
            q_sim = float(cosine_sim(query_emb, chunk_emb.reshape(1, -1))[0])
            if retrieved_embs:
                ret_arr = np.stack(retrieved_embs)
                max_ret_sim = float(np.max(cosine_sim(chunk_emb, ret_arr)))
                novelty = 1.0 - max_ret_sim
            else:
                novelty = 1.0
            G_t = q_sim * novelty
            if G_t < G_env and retrieved_texts:
                break
            retrieved_texts.append(chunk_meta[idx][1])
            retrieved_embs.append(chunk_emb)

    return retrieved_texts, G_env


def mvt_noenv_rag(query_emb: np.ndarray, sections: list, chunk_embs: np.ndarray,
                  chunk_meta: list, threshold: float = 0.3) -> list:
    """MVT ablation: replace G_env with fixed threshold."""
    sec_map = defaultdict(list)
    for i, (sname, _) in enumerate(chunk_meta):
        sec_map[sname].append(i)
    sec_potential = {
        sname: float(np.max(cosine_sim(query_emb, chunk_embs[idxs])))
        for sname, idxs in sec_map.items()
    }
    retrieved_texts = []
    retrieved_embs = []
    visited = set()
    while True:
        remaining = {s: p for s, p in sec_potential.items() if s not in visited}
        if not remaining:
            break
        cur_sec = max(remaining, key=remaining.get)
        visited.add(cur_sec)
        for idx in sec_map[cur_sec]:
            chunk_emb = chunk_embs[idx]
            q_sim = float(cosine_sim(query_emb, chunk_emb.reshape(1, -1))[0])
            if retrieved_embs:
                ret_arr = np.stack(retrieved_embs)
                novelty = 1.0 - float(np.max(cosine_sim(chunk_emb, ret_arr)))
            else:
                novelty = 1.0
            G_t = q_sim * novelty
            if G_t < threshold and retrieved_texts:
                break
            retrieved_texts.append(chunk_meta[idx][1])
            retrieved_embs.append(chunk_emb)
    return retrieved_texts


def topk_dense(query_emb: np.ndarray, chunk_embs: np.ndarray, chunk_meta: list, k: int) -> list:
    sims = cosine_sim(query_emb, chunk_embs)
    idxs = np.argsort(sims)[::-1][:k]
    return [chunk_meta[i][1] for i in idxs]


def bm25_retrieval(query: str, chunk_meta: list, k: int = 5) -> list:
    from rank_bm25 import BM25Okapi
    corpus = [text.split() for _, text in chunk_meta]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(query.split())
    idxs = np.argsort(scores)[::-1][:k]
    return [chunk_meta[i][1] for i in idxs]


def flare_style_retrieval(query_emb: np.ndarray, chunk_embs: np.ndarray,
                          chunk_meta: list, threshold: float = 0.3) -> list:
    """FLARE-style: retrieve while cosine sim > threshold (at least 1 chunk)."""
    sims = cosine_sim(query_emb, chunk_embs)
    order = np.argsort(sims)[::-1]
    chunks = [chunk_meta[i][1] for i in order if sims[i] >= threshold]
    if not chunks:
        chunks = [chunk_meta[order[0]][1]]
    return chunks[:15]  # cap


# ── LLM answer generation ─────────────────────────────────────────────────────

_openai_client = None


def get_client():
    global _openai_client
    if _openai_client is None:
        import openai
        _openai_client = openai.OpenAI(
            api_key=OPENROUTER_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
    return _openai_client


def generate_answer(query: str, chunks: list) -> str:
    if not chunks:
        context = "No context available."
    else:
        context = "\n\n".join(chunks[:10])
    prompt = (
        f"You are answering questions about a scientific paper. "
        f"Use only the provided context.\n\n"
        f"Context:\n{context[:3000]}\n\n"
        f"Question: {query}\n"
        f"Answer concisely in 1-3 sentences:"
    )
    try:
        client = get_client()
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return ""


# ── Bootstrap test ────────────────────────────────────────────────────────────

def bootstrap_ci_and_p(a: np.ndarray, b: np.ndarray, n: int = 10000, seed: int = 42) -> dict:
    """Paired bootstrap: CI and p-value for mean(a) - mean(b)."""
    rng = np.random.default_rng(seed)
    obs_delta = float(np.mean(a) - np.mean(b))
    n_samples = len(a)
    boot_deltas = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, n_samples, n_samples)
        boot_deltas[i] = np.mean(a[idx]) - np.mean(b[idx])
    ci_lo = float(np.percentile(boot_deltas, 2.5))
    ci_hi = float(np.percentile(boot_deltas, 97.5))
    p_val = float(np.mean(boot_deltas <= 0))
    return {"obs_delta": obs_delta, "ci_lo": ci_lo, "ci_hi": ci_hi, "p_value": p_val}


# ── Multi-hop classification ──────────────────────────────────────────────────

def is_multihop(retrieved_sections: list) -> bool:
    """Multi-hop if evidence spans ≥2 distinct sections."""
    return len(set(retrieved_sections)) >= 2


# ── Main ──────────────────────────────────────────────────────────────────────

METHODS = ["mvt_rag", "mvt_noenv", "topk_3", "topk_5", "topk_10", "bm25_5", "flare", "no_rag"]


@logger.catch(reraise=True)
def main():
    logger.info("Loading sentence-transformers model")
    from sentence_transformers import SentenceTransformer
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Model loaded")

    logger.info(f"Loading QASPER from {DATASET_PATH}")
    papers = json.loads(DATASET_PATH.read_text())
    logger.info(f"Loaded {len(papers)} papers")

    # Limit based on cost
    N_PAPERS = int(os.environ.get("N_PAPERS", "281"))
    papers = papers[:N_PAPERS]

    total_cost = 0.0
    per_question_results = []  # list of dicts
    skipped = 0

    for paper_idx, paper in enumerate(tqdm(papers, desc="Papers")):
        sections = parse_paper(paper)
        if not sections:
            skipped += 1
            continue

        chunk_meta, chunk_texts = flatten_chunks(sections)
        if not chunk_texts:
            skipped += 1
            continue

        # Embed all chunks
        chunk_embs = embed_model.encode(chunk_texts, batch_size=64, show_progress_bar=False)
        chunk_embs = np.array(chunk_embs, dtype=np.float32)

        qas = paper.get("qas", {})
        questions = qas.get("question", [])
        all_answers_list = qas.get("answers", [])

        for q_idx, (question, answers_obj) in enumerate(zip(questions, all_answers_list)):
            # Parse gold answers
            gold_answers = []
            for ans in answers_obj.get("answer", []):
                if not ans.get("unanswerable", True):
                    ffa = ans.get("free_form_answer", "")
                    if ffa:
                        gold_answers.append(ffa)
                    spans = ans.get("extractive_spans", [])
                    for sp in spans:
                        if isinstance(sp, str) and sp.strip():
                            gold_answers.append(sp.strip())
            if not gold_answers:
                continue

            if total_cost >= COST_LIMIT:
                logger.warning("Cost limit reached, stopping")
                break

            query_emb = embed_model.encode([question], show_progress_bar=False)[0]
            query_emb = np.array(query_emb, dtype=np.float32)

            # Run all retrieval methods
            mvt_chunks, G_env = mvt_rag(query_emb, sections, chunk_embs, chunk_meta)
            noenv_chunks = mvt_noenv_rag(query_emb, sections, chunk_embs, chunk_meta)
            topk3_chunks = topk_dense(query_emb, chunk_embs, chunk_meta, 3)
            topk5_chunks = topk_dense(query_emb, chunk_embs, chunk_meta, 5)
            topk10_chunks = topk_dense(query_emb, chunk_embs, chunk_meta, 10)
            bm25_chunks = bm25_retrieval(question, chunk_meta, 5)
            flare_chunks = flare_style_retrieval(query_emb, chunk_embs, chunk_meta)
            norag_chunks = []

            method_chunk_map = {
                "mvt_rag": mvt_chunks,
                "mvt_noenv": noenv_chunks,
                "topk_3": topk3_chunks,
                "topk_5": topk5_chunks,
                "topk_10": topk10_chunks,
                "bm25_5": bm25_chunks,
                "flare": flare_chunks,
                "no_rag": norag_chunks,
            }

            # Generate answers for all methods (parallel LLM calls)
            answers_by_method = {}
            if total_cost < COST_LIMIT:
                with ThreadPoolExecutor(max_workers=8) as pool:
                    futures = {pool.submit(generate_answer, question, chunks): method
                               for method, chunks in method_chunk_map.items()}
                    for fut in as_completed(futures):
                        m = futures[fut]
                        try:
                            answers_by_method[m] = fut.result()
                        except Exception as e:
                            logger.error(f"LLM failed for {m}: {e}")
                            answers_by_method[m] = ""
                total_cost += COST_PER_CALL * len(method_chunk_map)

            # Determine multi-hop status from MVT retrieved sections
            mvt_sections_retrieved = list({chunk_meta[chunk_texts.index(c)][0]
                                           for c in mvt_chunks if c in chunk_texts})
            multihop = is_multihop(mvt_sections_retrieved)

            for method, answer in answers_by_method.items():
                chunks = method_chunk_map[method]
                f1 = best_f1(answer, gold_answers)
                em = best_em(answer, gold_answers)
                per_question_results.append({
                    "paper_id": paper.get("id", ""),
                    "question": question,
                    "method": method,
                    "chunks_retrieved": len(chunks),
                    "answer": answer,
                    "gold_answers": gold_answers,
                    "f1": f1,
                    "exact_match": em,
                    "multihop": multihop,
                    "g_env": G_env if method == "mvt_rag" else None,
                })

            logger.debug(f"Paper {paper_idx} q{q_idx}: cost=${total_cost:.2f} mvt={len(mvt_chunks)} topk5=5")

        if total_cost >= COST_LIMIT:
            break

        # Free memory
        del chunk_embs
        gc.collect()

    logger.info(f"Collected {len(per_question_results)} records, total_cost=${total_cost:.3f}, skipped={skipped}")

    # ── Aggregate stats per method ──────────────────────────────────────────
    def get_by_method(method, key):
        return [r[key] for r in per_question_results if r["method"] == method]

    summary = {}
    for method in METHODS:
        f1s = get_by_method(method, "f1")
        ems = get_by_method(method, "exact_match")
        chunks = get_by_method(method, "chunks_retrieved")
        if not f1s:
            continue
        summary[method] = {
            "mean_f1": float(np.mean(f1s)),
            "mean_em": float(np.mean(ems)),
            "mean_chunks": float(np.mean(chunks)),
            "n": len(f1s),
        }

    logger.info("Method summary:")
    for m, s in summary.items():
        logger.info(f"  {m}: F1={s['mean_f1']:.4f} EM={s['mean_em']:.4f} chunks={s['mean_chunks']:.1f} n={s['n']}")

    # ── Bootstrap significance tests (MVT-RAG vs each baseline) ───────────────
    mvt_f1s = np.array(get_by_method("mvt_rag", "f1"))
    bootstrap_results = {}
    baselines = ["mvt_noenv", "topk_3", "topk_5", "topk_10", "bm25_5", "flare", "no_rag"]
    for bl in baselines:
        bl_f1s = np.array(get_by_method(bl, "f1"))
        if len(bl_f1s) == 0 or len(mvt_f1s) == 0:
            continue
        min_n = min(len(mvt_f1s), len(bl_f1s))
        bs = bootstrap_ci_and_p(mvt_f1s[:min_n], bl_f1s[:min_n], n=10000)
        bootstrap_results[f"mvt_rag_vs_{bl}"] = bs
        logger.info(f"  mvt_rag vs {bl}: delta={bs['obs_delta']:.4f} CI=[{bs['ci_lo']:.4f},{bs['ci_hi']:.4f}] p={bs['p_value']:.4f}")

    # Ablation: MVT-RAG vs MVT-NoEnv
    noenv_f1s = np.array(get_by_method("mvt_noenv", "f1"))
    if len(noenv_f1s) > 0 and len(mvt_f1s) > 0:
        min_n = min(len(mvt_f1s), len(noenv_f1s))
        ablation = bootstrap_ci_and_p(mvt_f1s[:min_n], noenv_f1s[:min_n])
        logger.info(f"  Ablation G_env: delta={ablation['obs_delta']:.4f} CI=[{ablation['ci_lo']:.4f},{ablation['ci_hi']:.4f}] p={ablation['p_value']:.4f}")
    else:
        ablation = {}

    # ── Stratified analysis: single-hop vs multi-hop ───────────────────────
    strat = {}
    for method in METHODS:
        mh_f1 = [r["f1"] for r in per_question_results if r["method"] == method and r["multihop"]]
        sh_f1 = [r["f1"] for r in per_question_results if r["method"] == method and not r["multihop"]]
        mh_em = [r["exact_match"] for r in per_question_results if r["method"] == method and r["multihop"]]
        sh_em = [r["exact_match"] for r in per_question_results if r["method"] == method and not r["multihop"]]
        strat[method] = {
            "multihop": {"n": len(mh_f1), "mean_f1": float(np.mean(mh_f1)) if mh_f1 else 0.0,
                         "mean_em": float(np.mean(mh_em)) if mh_em else 0.0},
            "singlehop": {"n": len(sh_f1), "mean_f1": float(np.mean(sh_f1)) if sh_f1 else 0.0,
                          "mean_em": float(np.mean(sh_em)) if sh_em else 0.0},
        }

    # ── Verdict ────────────────────────────────────────────────────────────
    mvt_mean_f1 = summary.get("mvt_rag", {}).get("mean_f1", 0.0)
    topk5_mean_f1 = summary.get("topk_5", {}).get("mean_f1", 0.0)
    mvt_mean_chunks = summary.get("mvt_rag", {}).get("mean_chunks", 99.0)
    topk5_mean_chunks = summary.get("topk_5", {}).get("mean_chunks", 5.0)
    ablation_delta = ablation.get("obs_delta", 0.0) if ablation else 0.0
    ablation_ci_lo = ablation.get("ci_lo", 0.0) if ablation else 0.0

    bs_mvt_vs_topk5 = bootstrap_results.get("mvt_rag_vs_topk_5", {})
    f1_gain_ci_excl_0 = bs_mvt_vs_topk5.get("ci_lo", 0.0) > 0

    if mvt_mean_f1 > topk5_mean_f1 and mvt_mean_chunks < topk5_mean_chunks and ablation_ci_lo > 0:
        verdict = "CONFIRM"
        verdict_reason = (
            f"MVT-RAG (F1={mvt_mean_f1:.3f}) outperforms top-k-5 (F1={topk5_mean_f1:.3f}) "
            f"while retrieving fewer chunks ({mvt_mean_chunks:.1f} vs {topk5_mean_chunks:.1f}), "
            f"and the G_env ablation CI excludes 0 (delta={ablation_delta:.4f} CI_lo={ablation_ci_lo:.4f})."
        )
    elif mvt_mean_f1 > topk5_mean_f1 or mvt_mean_chunks < topk5_mean_chunks:
        verdict = "PARTIAL"
        # check if multihop advantage present
        mvt_mh = strat.get("mvt_rag", {}).get("multihop", {}).get("mean_f1", 0.0)
        topk5_mh = strat.get("topk_5", {}).get("multihop", {}).get("mean_f1", 0.0)
        verdict_reason = (
            f"MVT-RAG shows partial success: F1={mvt_mean_f1:.3f} vs top-k-5 F1={topk5_mean_f1:.3f}, "
            f"chunks={mvt_mean_chunks:.1f} vs {topk5_mean_chunks:.1f}. "
            f"Multi-hop: MVT={mvt_mh:.3f} vs topk5={topk5_mh:.3f}. "
            f"G_env ablation delta={ablation_delta:.4f}."
        )
    else:
        verdict = "DISCONFIRM"
        verdict_reason = (
            f"MVT-RAG (F1={mvt_mean_f1:.3f}, chunks={mvt_mean_chunks:.1f}) does not outperform "
            f"top-k-5 (F1={topk5_mean_f1:.3f}, chunks={topk5_mean_chunks:.1f}). "
            f"The ecological stopping criterion does not confer measurable advantage."
        )

    logger.info(f"Verdict: {verdict} — {verdict_reason}")

    # ── Build eval_out.json in required schema format ──────────────────────
    # metrics_agg: primary numbers
    metrics_agg = {"mvt_rag_f1": round(mvt_mean_f1, 4)}
    for method, s in summary.items():
        metrics_agg[f"{method}_f1"] = round(s["mean_f1"], 4)
        metrics_agg[f"{method}_em"] = round(s["mean_em"], 4)
        metrics_agg[f"{method}_chunks"] = round(s["mean_chunks"], 2)
    for k, v in bootstrap_results.items():
        metrics_agg[f"bootstrap_{k}_delta"] = round(v["obs_delta"], 4)
        metrics_agg[f"bootstrap_{k}_p"] = round(v["p_value"], 4)
    metrics_agg["ablation_genv_delta"] = round(ablation_delta, 4)

    # Build examples list
    examples = []
    for r in per_question_results:
        if r["method"] == "mvt_rag":
            # Find other method results for same paper/question
            same_q = {rec["method"]: rec for rec in per_question_results
                      if rec["paper_id"] == r["paper_id"] and rec["question"] == r["question"]}
            ex = {
                "input": r["question"],
                "output": " | ".join(r["gold_answers"]),
                "predict_mvt_rag": r["answer"],
                "eval_f1_mvt_rag": round(r["f1"], 4),
                "eval_em_mvt_rag": round(r["exact_match"], 4),
                "eval_chunks_mvt_rag": float(r["chunks_retrieved"]),
            }
            for bl in baselines:
                if bl in same_q:
                    rec = same_q[bl]
                    ex[f"predict_{bl}"] = rec["answer"]
                    ex[f"eval_f1_{bl}"] = round(rec["f1"], 4)
                    ex[f"eval_chunks_{bl}"] = float(rec["chunks_retrieved"])
            ex["metadata_multihop"] = r["multihop"]
            ex["metadata_paper_id"] = r["paper_id"]
            examples.append(ex)

    eval_out = {
        "metadata": {
            "evaluation_name": "MVT-RAG vs Baselines F1 & Efficiency Eval",
            "dataset": "allenai/qasper validation",
            "n_papers": len(papers),
            "n_questions": len(examples),
            "total_cost_usd": round(total_cost, 4),
            "verdict": verdict,
            "verdict_reason": verdict_reason,
            "bootstrap_results": bootstrap_results,
            "ablation_genv": ablation,
            "stratified_analysis": strat,
            "summary_per_method": summary,
        },
        "metrics_agg": {k: v for k, v in metrics_agg.items() if isinstance(v, (int, float))},
        "datasets": [
            {
                "dataset": "allenai/qasper_validation",
                "examples": examples,
            }
        ],
    }

    out_path = WORKSPACE / "eval_out.json"
    out_path.write_text(json.dumps(eval_out, indent=2))
    logger.info(f"Saved eval_out.json ({out_path.stat().st_size / 1e6:.1f} MB)")

    # ── Validate schema ────────────────────────────────────────────────────
    logger.info("Validating schema...")
    SKILL_DIR = Path("/ai-inventor/.claude/skills/aii-json")
    PY = SKILL_DIR / "../.ability_client_venv/bin/python"
    VAL_SCRIPT = SKILL_DIR / "scripts/aii_json_validate_schema.py"
    import subprocess
    result = subprocess.run(
        [str(PY), str(VAL_SCRIPT), "--format", "exp_eval_sol_out", "--file", str(out_path.absolute())],
        capture_output=True, text=True
    )
    logger.info(f"Validation stdout: {result.stdout.strip()}")
    if result.returncode != 0:
        logger.error(f"Validation failed: {result.stderr.strip()}")
    else:
        logger.info("Schema validation PASSED")

    logger.info("Done.")
    return verdict


if __name__ == "__main__":
    main()
