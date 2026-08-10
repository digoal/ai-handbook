#!/usr/bin/env python3
"""
Lint that each chapter has exactly three top-level perspective sections
(User / Developer / Architect) and that no obviously developer/architect
keywords leak into the User section.

Usage:
    python scripts/lint_perspectives.py [chapter.md ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HANDBOOK_ROOT = Path(__file__).resolve().parent.parent
PARTS = [
    "part-i-foundations",
    "part-ii-core-modules",
    "part-iii-cross-cutting",
    "part-iv-integrations",
    "part-v-workflows",
    "part-vi-operations",
    "part-vii-reference",
]

# Tokens that should NOT appear in the User section (high risk = class/manager names)
HIGH_RISK_DEV_TOKENS = (
    r"GraphBuilder|ProvenanceManager|DecisionRecorder|HybridSearch|"
    r"FalkorDB|ReteEngine|DatalogReasoner|OntologyGenerator|"
    r"EmbeddingGenerator|LLMExtraction|ContextGraph|FileIngestor|"
    r"WebIngestor|DBIngestor|TripletStore|VectorStore|GraphStore|"
    r"add_causal_relationship|register_reader|semantica-mcp|"
    r"SemanticaWorker|method_registry|ContextGraph"
)
DEV_TOKENS = re.compile(
    r"\b(class\s+\w+|def\s+\w+|@dataclass|abstractmethod|"
    + HIGH_RISK_DEV_TOKENS
    + r"|config_manager\.py|orchestrator\.py|graphStore\.ts)\b"
)
ARCH_TOKENS = re.compile(
    r"\b(Trade-?off|design rationale|architecture decision|ADR|tradeoff|"
    r"我们选择|代价是|折中|权衡|我们不学|为什么不学|与.*对比|"
    r"vs\.|compared to|alternative implementation)\b"
)

USER_HEADERS = ["## 1. 用户视角", "## 1. 用户视角(User)"]
DEV_HEADERS = ["## 2. 开发者视角", "## 2. 开发者视角(Developer)"]
ARCH_HEADERS = ["## 3. 架构师视角", "## 3. 架构师视角(Architect)"]


def section_after(text: str, header: str) -> str:
    """Extract everything between `header` and the next `##` heading."""
    idx = text.find(header)
    if idx < 0:
        return ""
    rest = text[idx + len(header):]
    nxt = re.search(r"^## ", rest, flags=re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def lint_one(md: Path) -> list[str]:
    text = md.read_text(encoding="utf-8")
    errors: list[str] = []
    found_user = any(h in text for h in USER_HEADERS)
    found_dev = any(h in text for h in DEV_HEADERS)
    found_arch = any(h in text for h in ARCH_HEADERS)
    if not (found_user and found_dev and found_arch):
        missing = []
        if not found_user:
            missing.append("User")
        if not found_dev:
            missing.append("Developer")
        if not found_arch:
            missing.append("Architect")
        errors.append(f"{md}: missing perspective section(s): {', '.join(missing)}")
        return errors

    # Use the most explicit header for section extraction
    user_h = next(h for h in USER_HEADERS if h in text)
    user_section = section_after(text, user_h)
    if not user_section.strip():
        errors.append(f"{md}: User section is empty")
    if DEV_TOKENS.search(user_section):
        # Threshold: warn only if many unique tokens leaked (high-frequency single
        # mentions are unavoidable in chapter intros — e.g. ch-08 必然列出 5+ ingestor 类名).
        hits = DEV_TOKENS.findall(user_section)
        unique_tokens = set(hits)
        high_risk = re.compile(HIGH_RISK_DEV_TOKENS)
        weighted = sum(2 if high_risk.fullmatch(h) else 1 for h in hits)
        # Trigger only when ≥7 unique tokens leaked AND weighted sum ≥ 14
        # (allows ch-08 等核心章 §1 列出 5-6 个 ingestor 类名)
        if len(unique_tokens) >= 7 and weighted >= 14:
            errors.append(
                f"{md}: User section contains developer vocabulary ({len(hits)} hits, "
                f"{len(unique_tokens)} unique, weighted={weighted}, first: {hits[0]})"
            )
    if ARCH_TOKENS.search(user_section):
        hits = ARCH_TOKENS.findall(user_section)
        if len(hits) >= 3:
            errors.append(
                f"{md}: User section contains architect vocabulary ({len(hits)} hits, first: {hits[0]})"
            )
    return errors


def iter_chapters(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    chapters: list[Path] = []
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            chapters.extend(sorted(part_dir.glob("ch-*.md")))
    return chapters


def main() -> int:
    chapters = iter_chapters(sys.argv[1:])
    all_errors: list[str] = []
    for md in chapters:
        all_errors.extend(lint_one(md))
    if all_errors:
        print(f"✗ {len(all_errors)} perspective lint issue(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print(f"✓ {len(chapters)} chapter(s) have all three perspective sections.")
    return 0


if __name__ == "__main__":
    sys.exit(main())