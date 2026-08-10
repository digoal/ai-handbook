#!/usr/bin/env python3
"""
Verify that each chapter file's stem matches its frontmatter `slug` field
exactly (case-sensitive, lowercase-required).

Usage:
    python scripts/check_slug_filename.py
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

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
SLUG_RE = re.compile(r"^slug:\s*(\S+)\s*$", re.MULTILINE)


def parse_slug(text: str) -> str | None:
    m = FRONTMATTER_RE.search(text)
    if not m:
        return None
    sm = SLUG_RE.search(m.group(1))
    return sm.group(1) if sm else None


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
    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        slug = parse_slug(text)
        stem = ch.stem
        if slug is None:
            errors.append(f"{ch}: missing `slug:` in frontmatter")
            continue
        if slug != stem:
            errors.append(f"{ch.name}: frontmatter slug=`{slug}` ≠ filename stem=`{stem}`")
        if any(c.isupper() for c in stem):
            errors.append(f"{ch.name}: filename stem contains uppercase (slug must be lowercase)")
    if errors:
        print(f"✗ {len(errors)} slug/filename mismatch(es):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✓ {len(chapters)} chapter(s): slug == filename stem, all lowercase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())