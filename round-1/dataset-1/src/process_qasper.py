#!/usr/bin/env python3
"""Process QASPER into section-level chunks for MVT-RAG evaluation."""

import json
import random
import sys
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WS = Path(__file__).parent
TRAIN_PATH = WS / "temp/datasets/full_allenai_qasper_qasper_train.json"
VAL_PATH   = WS / "temp/datasets/full_allenai_qasper_qasper_validation.json"
OUT_PATH   = WS / "data_out.json"

IMRAD_MAP = {
    "introduction": "introduction",
    "related": "related_work",
    "background": "related_work",
    "method": "methods",
    "approach": "methods",
    "model": "methods",
    "experiment": "results",
    "result": "results",
    "evaluation": "results",
    "ablation": "results",
    "discussion": "discussion",
    "conclusion": "discussion",
    "limitation": "discussion",
    "future": "discussion",
    "analysis": "results",
}

def normalize_section(name: str) -> str:
    if not name:
        return "preamble"
    low = name.lower()
    if not low.strip():
        return "preamble"
    for k, v in IMRAD_MAP.items():
        if k in low:
            return v
    return "other"


def overlap_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    # Check substring containment
    if a in b or b in a:
        return 1.0
    # Check prefix overlap (first 80 chars)
    a80, b80 = a[:80], b[:80]
    if a80 == b80:
        return 1.0
    # Count common words
    wa = set(a.split())
    wb = set(b.split())
    if not wa or not wb:
        return 0.0
    inter = len(wa & wb)
    return inter / max(len(wa), len(wb))


def process_paper(paper: dict, split: str) -> list[dict]:
    paper_id = paper["id"]
    ft = paper.get("full_text", {})
    if not ft:
        return []

    # full_text is columnar: {section_name: [...], paragraphs: [[...], ...]}
    section_names = ft.get("section_name", [])
    paragraphs_by_section = ft.get("paragraphs", [])

    if len(section_names) != len(paragraphs_by_section):
        logger.warning(f"{paper_id}: section count mismatch")
        return []

    # Build section/chunk structure
    sections = []
    chunk_lookup: dict[str, str] = {}  # chunk_id -> text

    for sec_idx, (sec_name, paras) in enumerate(zip(section_names, paragraphs_by_section)):
        norm = normalize_section(sec_name)
        chunks = []
        for para_idx, para_text in enumerate(paras):
            if not para_text or not para_text.strip():
                continue
            chunk_id = f"{paper_id}_{sec_idx}_{para_idx}"
            chunks.append({"chunk_id": chunk_id, "text": para_text, "para_idx": para_idx})
            chunk_lookup[chunk_id] = para_text
        if chunks:
            sections.append({
                "name": sec_name,
                "normalized_name": norm,
                "section_idx": sec_idx,
                "chunks": chunks,
            })

    # Filter: need >=3 distinct normalized categories (excluding preamble)
    norm_cats = {s["normalized_name"] for s in sections if s["normalized_name"] != "preamble"}
    if len(norm_cats) < 3:
        return []

    # Process QAs (columnar format)
    qas = paper.get("qas", {})
    if not qas:
        return []

    questions = qas.get("question", [])
    question_ids = qas.get("question_id", [])
    answers_list = qas.get("answers", [])

    rows = []
    for q_idx, (question, question_id, answer_group) in enumerate(
        zip(questions, question_ids, answers_list)
    ):
        # answer_group is a dict with key "answer" -> list of annotator answers
        if isinstance(answer_group, dict):
            ann_answers = answer_group.get("answer", [])
        else:
            ann_answers = answer_group

        # Find first non-unanswerable answer
        gold_answer = ""
        evidence_texts = []
        for ann in ann_answers:
            if isinstance(ann, dict) and not ann.get("unanswerable", True):
                ff = ann.get("free_form_answer", "")
                spans = ann.get("extractive_spans", [])
                if ff:
                    gold_answer = ff
                elif spans:
                    gold_answer = " ".join(spans)
                evidence_texts = ann.get("evidence", [])
                break

        if not gold_answer:
            continue

        # Match evidence texts to chunk IDs
        evidence_chunk_ids = []
        for ev_text in evidence_texts:
            if not ev_text or not ev_text.strip():
                continue
            best_cid = None
            best_ratio = 0.0
            for cid, ctext in chunk_lookup.items():
                r = overlap_ratio(ev_text[:200], ctext[:200])
                if r > best_ratio:
                    best_ratio = r
                    best_cid = cid
            if best_cid and best_ratio >= 0.5:
                evidence_chunk_ids.append(best_cid)

        if not evidence_chunk_ids:
            continue

        # Determine evidence sections
        ev_section_names = []
        ev_section_norm = set()
        for cid in evidence_chunk_ids:
            parts = cid.split("_")
            sec_idx = int(parts[-2])
            for s in sections:
                if s["section_idx"] == sec_idx:
                    ev_section_names.append(s["name"])
                    ev_section_norm.add(s["normalized_name"])
                    break

        is_multihop = len(ev_section_norm) >= 2

        rows.append({
            "paper_id": paper_id,
            "question_id": question_id,
            "question": question,
            "gold_answer": gold_answer,
            "sections": sections,
            "evidence_chunk_ids": evidence_chunk_ids,
            "evidence_section_names": ev_section_names,
            "is_multihop": is_multihop,
            "num_sections": len(sections),
            "split": split,
        })

    return rows


@logger.catch(reraise=True)
def main():
    all_rows: list[dict] = []

    for path, split in [(TRAIN_PATH, "train"), (VAL_PATH, "validation")]:
        logger.info(f"Loading {split} from {path}")
        papers = json.loads(path.read_text())
        logger.info(f"Loaded {len(papers)} papers for {split}")

        split_rows = []
        skipped_sections = 0
        for paper in papers:
            rows = process_paper(paper, split)
            if not rows:
                skipped_sections += 1
            split_rows.extend(rows)

        logger.info(f"{split}: {len(split_rows)} questions kept, {skipped_sections} papers skipped (insufficient sections)")
        all_rows.extend(split_rows)

    logger.info(f"Total rows before sampling: {len(all_rows)}")

    # Sample up to 2000 stratified by is_multihop
    random.seed(42)
    multihop = [r for r in all_rows if r["is_multihop"]]
    singlehop = [r for r in all_rows if not r["is_multihop"]]
    logger.info(f"Multihop: {len(multihop)}, Single-hop: {len(singlehop)}")

    if len(all_rows) > 2000:
        # Proportional sampling
        mh_target = min(len(multihop), int(2000 * len(multihop) / len(all_rows)))
        sh_target = 2000 - mh_target
        sampled = random.sample(multihop, min(mh_target, len(multihop))) + \
                  random.sample(singlehop, min(sh_target, len(singlehop)))
        random.shuffle(sampled)
        all_rows = sampled

    # Validate
    errors = 0
    for row in all_rows:
        if not row["evidence_chunk_ids"]:
            errors += 1
            continue
        if row["num_sections"] < 3:
            errors += 1
            continue
        if not row["gold_answer"]:
            errors += 1
            continue
        # Verify chunk IDs exist in sections
        all_cids = {c["chunk_id"] for s in row["sections"] for c in s["chunks"]}
        for cid in row["evidence_chunk_ids"]:
            if cid not in all_cids:
                errors += 1
                break

    logger.info(f"Validation errors: {errors} / {len(all_rows)}")

    # Build mini (100 balanced) and preview (3 rows)
    mh_rows = [r for r in all_rows if r["is_multihop"]]
    sh_rows = [r for r in all_rows if not r["is_multihop"]]
    mini = random.sample(mh_rows, min(50, len(mh_rows))) + \
           random.sample(sh_rows, min(50, len(sh_rows)))
    random.shuffle(mini)
    preview = all_rows[:3]

    # Save
    OUT_PATH.write_text(json.dumps(all_rows, indent=2))
    (WS / "mini_data_out.json").write_text(json.dumps(mini, indent=2))
    (WS / "preview_data_out.json").write_text(json.dumps(preview, indent=2))

    logger.info(f"Saved {len(all_rows)} rows to data_out.json")
    logger.info(f"Saved {len(mini)} rows to mini_data_out.json")
    logger.info(f"Saved 3 rows to preview_data_out.json")

    # Stats summary
    stats = {
        "total_rows": len(all_rows),
        "multihop_rows": len([r for r in all_rows if r["is_multihop"]]),
        "singlehop_rows": len([r for r in all_rows if not r["is_multihop"]]),
        "train_rows": len([r for r in all_rows if r["split"] == "train"]),
        "validation_rows": len([r for r in all_rows if r["split"] == "validation"]),
        "validation_errors": errors,
        "mini_rows": len(mini),
    }
    logger.info(f"Stats: {stats}")
    (WS / "dataset_stats.json").write_text(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
