#!/usr/bin/env python3
"""Evaluation checker for RAG retrieval results.

Parses a playground result text file, calculates 1D IoU against ground truth spans,
and displays an organized summary table with Recall@1, Recall@3, and Recall@5 metrics.

Usage:
    uv run python checker.py <result_file.txt>
    uv run python checker.py results_for_10_samples_code_dataset.txt
    uv run python checker.py sample_result_10.txt --iou 0.05
"""

import argparse
import os
import re
import sys
from typing import List, NamedTuple, Tuple


class GroundTruth(NamedTuple):
    file_path: str
    start: int
    end: int


class RetrievedSource(NamedTuple):
    file_path: str
    start: int
    end: int
    score: float = 0.0


class QuestionBlock(NamedTuple):
    q_num: int
    question: str
    gt_sources: List[GroundTruth]
    retrieved: List[RetrievedSource]


def calculate_iou(start1: int, end1: int, start2: int, end2: int) -> float:
    """Calculate 1D Intersection over Union (IoU) between two character spans."""
    intersection = max(0, min(end1, end2) - max(start1, start2))
    union = (end1 - start1) + (end2 - start2) - intersection
    if union <= 0:
        return 0.0
    return intersection / union


def parse_result_file(file_path: str) -> List[QuestionBlock]:
    """Parse question blocks, ground truth sources, and retrieved MinimalSources."""
    if not os.path.exists(file_path):
        print(f"\033[91mError: File not found: {file_path}\033[0m")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by dotted lines or Question headings
    raw_blocks = re.split(r"\.{10,}|(?=Question\s+\d+:)", content)
    question_blocks: List[QuestionBlock] = []

    for block in raw_blocks:
        block = block.strip()
        if not block or "Question" not in block or "Ground Truth" not in block:
            continue

        # Extract question number and text
        q_match = re.search(r"Question\s+(\d+):\s*(.+?)(?=\nGround Truth|$)", block, re.DOTALL)
        if not q_match:
            continue
        q_num = int(q_match.group(1))
        question_text = q_match.group(2).strip().replace("\n", " ")

        # Extract Ground Truth sources
        gt_matches = re.findall(
            r"File:\s*(\S+)\s*\[(\d+)\s*:\s*(\d+)\]",
            block
        )
        gt_sources = [
            GroundTruth(file_path=m[0], start=int(m[1]), end=int(m[2]))
            for m in gt_matches
        ]

        # Extract Retrieved MinimalSources
        # Handles lines like: ('score: 15.62', MinimalSource(file_path='...', first_character_index=..., last_character_index=...))
        ret_matches = re.findall(
            r"(?:score:\s*([\d\.\-]+))?.*?MinimalSource\(\s*file_path=['\"]([^'\"]+)['\"]\s*,\s*first_character_index=(\d+)\s*,\s*last_character_index=(\d+)\s*\)",
            block
        )

        retrieved: List[RetrievedSource] = []
        for m in ret_matches:
            score = float(m[0]) if m[0] else 0.0
            retrieved.append(
                RetrievedSource(
                    file_path=m[1],
                    start=int(m[2]),
                    end=int(m[3]),
                    score=score
                )
            )

        question_blocks.append(
            QuestionBlock(
                q_num=q_num,
                question=question_text,
                gt_sources=gt_sources,
                retrieved=retrieved
            )
        )

    return question_blocks


def strip_ansi(s: str) -> str:
    """Remove ANSI escape sequences to compute true printable width."""
    return re.sub(r"\033\[[0-9;]*m", "", s)


def pad_ansi(s: str, width: int, align: str = "left") -> str:
    """Pad string considering visible characters only (ignoring ANSI codes)."""
    vis_len = len(strip_ansi(s))
    pad = max(0, width - vis_len)
    if align == "right":
        return (" " * pad) + s
    return s + (" " * pad)


def evaluate_and_display(blocks: List[QuestionBlock], iou_thresh: float = 0.05, top_k: int = 5) -> None:
    """Evaluate retrieval results against ground truth and render formatted summary table."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    print()
    print(f"{BOLD}╔═══════════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║                              RAG RETRIEVAL EVALUATION REPORT                                  ║{RESET}")
    print(f"{BOLD}╚═══════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f" {DIM}Evaluation criteria: exact file_path match + IoU >= {iou_thresh:.2f} within Top-{top_k}{RESET}\n")

    # Table Header
    header = f"{BOLD}{'#':<4} {'Target File':<32} {'Best Rank':<11} {'Best IoU':<10} {'Status':<10} {'Question Summary':<26}{RESET}"
    divider = "─" * 96
    print(header)
    print(divider)

    hits_k1 = 0
    hits_k3 = 0
    hits_k5 = 0
    total = len(blocks)

    for b in blocks:
        best_rank = None
        best_iou = 0.0

        for rank, r in enumerate(b.retrieved[:top_k], 1):
            for gt in b.gt_sources:
                if r.file_path == gt.file_path:
                    iou = calculate_iou(gt.start, gt.end, r.start, r.end)
                    if iou > best_iou:
                        best_iou = iou
                    if iou >= iou_thresh and best_rank is None:
                        best_rank = rank

        gt_file = b.gt_sources[0].file_path if b.gt_sources else "unknown"
        short_file = gt_file.split("/")[-1]
        if len(short_file) > 30:
            short_file = short_file[:27] + "..."

        q_summary = b.question
        if len(q_summary) > 24:
            q_summary = q_summary[:21] + "..."

        is_hit = best_rank is not None

        if is_hit:
            hits_k5 += 1
            if best_rank <= 3:
                hits_k3 += 1
            if best_rank == 1:
                hits_k1 += 1
            rank_str = f"{CYAN}Rank {best_rank}{RESET}"
            iou_str = f"{best_iou * 100:>5.1f}%"
            status_str = f"{GREEN}HIT  ✅{RESET}"
        else:
            rank_str = f"{DIM}—{RESET}"
            iou_str = f"{best_iou * 100:>5.1f}%" if best_iou > 0 else f"{DIM}0.0%{RESET}"
            status_str = f"{RED}MISS ❌{RESET}"

        col_q = pad_ansi(f"Q{b.q_num}", 4)
        col_file = pad_ansi(short_file, 32)
        col_rank = pad_ansi(rank_str, 11)
        col_iou = pad_ansi(iou_str, 10)
        col_status = pad_ansi(status_str, 10)
        col_summary = pad_ansi(q_summary, 26)

        print(f"{col_q} {col_file} {col_rank} {col_iou} {col_status} {col_summary}")

    print(divider)

    # Calculate percentages
    r1_pct = (hits_k1 / total * 100) if total else 0.0
    r3_pct = (hits_k3 / total * 100) if total else 0.0
    r5_pct = (hits_k5 / total * 100) if total else 0.0

    print(f"\n{BOLD}📊 SUMMARY METRICS (Total Questions: {total}){RESET}")
    print(f"  • {BOLD}Recall@1:{RESET} {hits_k1:>2} / {total}  ({CYAN}{r1_pct:5.1f}%{RESET})")
    print(f"  • {BOLD}Recall@3:{RESET} {hits_k3:>2} / {total}  ({CYAN}{r3_pct:5.1f}%{RESET})")
    print(f"  • {BOLD}Recall@5:{RESET} {hits_k5:>2} / {total}  ({BOLD}{YELLOW if r5_pct < 80 else GREEN}{r5_pct:5.1f}%{RESET})")

    # Subject Target Check
    print(f"\n{BOLD}🎯 SUBJECT REQUIREMENTS CHECK:{RESET}")
    docs_status = f"{GREEN}PASS (>= 80%){RESET}" if r5_pct >= 80 else f"{RED}FAIL (< 80%){RESET}"
    code_status = f"{GREEN}PASS (>= 50%){RESET}" if r5_pct >= 50 else f"{RED}FAIL (< 50%){RESET}"

    print(f"  • If evaluated as Documentation Dataset: {docs_status}")
    print(f"  • If evaluated as Code Dataset:          {code_status}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG retrieval results from test output file.")
    parser.add_argument("result_file", type=str, help="Path to the results text file (e.g. results_for_10_samples_code_dataset.txt)")
    parser.add_argument("--iou", type=float, default=0.05, help="IoU threshold for a hit (default: 0.05)")
    parser.add_argument("--k", type=int, default=5, help="Top-K cutoff for recall (default: 5)")
    args = parser.parse_args()

    blocks = parse_result_file(args.result_file)
    if not blocks:
        print(f"\033[93mNo question blocks found in {args.result_file}\033[0m")
        return

    evaluate_and_display(blocks, iou_thresh=args.iou, top_k=args.k)


if __name__ == "__main__":
    main()
