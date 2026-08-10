#!/usr/bin/env python3
"""
Verify each chapter contains required sections:
- ## 1. 用户视角(User)
- ## 2. 开发者视角(Developer)
- ## 3. 架构师视角(Architect)
- ## 跨章引用

Optional:
- ## 本章图表 (if chapter contains a mermaid block)

Usage:
    python scripts/check_chapter_sections.py
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

REQUIRED_SECTIONS = [
    ("User", re.compile(r"^##\s+1\.\s*用户视角", re.MULTILINE)),
    ("Developer", re.compile(r"^##\s+2\.\s*开发者视角", re.MULTILINE)),
    ("Architect", re.compile(r"^##\s+3\.\s*架构师视角", re.MULTILINE)),
    ("CrossReferences", re.compile(r"^##\s+跨章引用", re.MULTILINE)),
]
HAS_MERMAID = re.compile(r"^```mermaid", re.MULTILINE)
HAS_FIG = re.compile(r"^###\s+FIG-", re.MULTILINE)


def iter_chapters() -> list[Path]:
    chapters: list[Path] = []
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            chapters.extend(sorted(part_dir.glob("ch-*.md")))
    return chapters


def main() -> int:
    chapters = iter_chapters()
    errors: list[str] = []
    warnings: list[str] = []
    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        for label, pat in REQUIRED_SECTIONS:
            if not pat.search(text):
                errors.append(f"{ch.name}: missing required section '{label}'")
        # Optional: 本章图表 when chapter has mermaid or FIG heading
        if HAS_MERMAID.search(text) or HAS_FIG.search(text):
            if not re.search(r"^##\s+本章图表", text, re.MULTILINE):
                warnings.append(f"{ch.name}: has mermaid/FIG but missing '## 本章图表' section")
    if errors:
        print(f"✗ {len(errors)} required-section issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    if warnings:
        print(f"⚠ {len(warnings)} optional-section warning(s):")
        for w in warnings[:20]:
            print(f"  - {w}")
    print(f"✓ {len(chapters)} chapter(s) have all required sections.")
    return 0


if __name__ == "__main__":
    sys.exit(main())