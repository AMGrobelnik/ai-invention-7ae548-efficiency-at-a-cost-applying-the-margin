#!/usr/bin/env python3
"""Convert QASPER data_out.json into exp_sel_data_out.json schema for MVT-RAG evaluation."""

import json
import sys
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/data.log", rotation="30 MB", level="DEBUG")

WS = Path(__file__).parent
DATA_IN = WS / "data_out.json"
OUT_PATH = WS / "full_data_out.json"


def build_input(row: dict) -> str:
    """Build the RAG retrieval input: question + section context summary."""
    sections_summary = "; ".join(
        f"[{s['normalized_name'].upper()}] {s['name']} ({len(s['chunks'])} chunks)"
        for s in row["sections"]
    )
    return json.dumps({
        "question": row["question"],
        "paper_id": row["paper_id"],
        "sections": sections_summary,
        "num_sections": row["num_sections"],
    })


def build_output(row: dict) -> str:
    """Build the output: gold answer + evidence location."""
    return json.dumps({
        "gold_answer": row["gold_answer"],
        "evidence_chunk_ids": row["evidence_chunk_ids"],
        "evidence_section_names": row["evidence_section_names"],
    })


@logger.catch(reraise=True)
def main():
    logger.info(f"Loading {DATA_IN}")
    rows = json.loads(DATA_IN.read_text())
    logger.info(f"Loaded {len(rows)} rows")

    examples = []
    for row in rows:
        inp = build_input(row)
        out = build_output(row)
        examples.append({
            "input": inp,
            "output": out,
            "metadata_fold": 0 if row["split"] == "train" else 1,
            "metadata_paper_id": row["paper_id"],
            "metadata_question_id": row["question_id"],
            "metadata_is_multihop": row["is_multihop"],
            "metadata_num_sections": row["num_sections"],
            "metadata_split": row["split"],
            "metadata_evidence_count": len(row["evidence_chunk_ids"]),
            "metadata_task_type": "rag_qa",
        })

    result = {
        "metadata": {
            "source": "allenai/qasper",
            "description": "QASPER section-annotated chunks for MVT-RAG evaluation",
            "total_examples": len(examples),
            "multihop_count": sum(1 for e in examples if e["metadata_is_multihop"]),
        },
        "datasets": [
            {
                "dataset": "qasper",
                "examples": examples,
            }
        ],
    }

    OUT_PATH.write_text(json.dumps(result, indent=2))
    logger.info(f"Saved {len(examples)} examples to {OUT_PATH}")


if __name__ == "__main__":
    main()
