#!/usr/bin/env python3
"""
Check that all [[ch-XX-slug]] and [[fig-NN]] cross-references in handbook
chapters resolve to existing chapter files or known figures.

Usage:
    python scripts/check_links.py [chapter.md ...]
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

# Two reference styles: chapter slug + figure id
CHAPTER_REF_RE = re.compile(r"\[\[ch-([0-9]{2})-([a-z0-9-]+)\]\]")
FIGURE_REF_RE = re.compile(r"\[\[fig-([0-9]{1,3})\]\]")
# Markdown plain link: [text](path) — check that path resolves to an existing chapter file
MD_LINK_RE = re.compile(r"\]\((part-[a-z]+/[a-z0-9-]+\.md)(?:#[^)]*)?\)")

# Known figure inventory is now derived from actual chapter `### FIG-NN` headings
# (no static KNOWN_FIGURES fallback — that allowed ghost figures).


def iter_chapters(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    chapters: list[Path] = []
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            chapters.extend(sorted(part_dir.glob("ch-*.md")))
    return chapters


def known_slugs() -> set[str]:
    """Build set of all ch-NN-slug currently present on disk."""
    slugs: set[str] = set()
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            for md in part_dir.glob("ch-*.md"):
                # ch-NN-slug.md -> ch-NN-slug
                slugs.add(md.stem)
    return slugs


def known_figures() -> set[str]:
    """Build set of declared fig IDs in chapter Mermaid blocks. No fallback — ghost figures fail."""
    declared: set[str] = set()
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            for md in part_dir.glob("ch-*.md"):
                text = md.read_text(encoding="utf-8")
                for m in re.finditer(r"###\s+(FIG-(\d{1,3}))", text):
                    declared.add(f"fig-{int(m.group(2)):02d}")
    return declared  # NO fallback to KNOWN_FIGURES — ghost figures must be fixed at source


def main() -> int:
    chapters = iter_chapters(sys.argv[1:])
    slugs = known_slugs()
    figures = known_figures()
    errors: list[str] = []

    for md in chapters:
        text = md.read_text(encoding="utf-8")
        for ref in CHAPTER_REF_RE.finditer(text):
            slug = f"ch-{ref.group(1)}-{ref.group(2)}"
            if slug not in slugs:
                errors.append(f"{md}: broken chapter ref [[{slug}]]")
        for ref in FIGURE_REF_RE.finditer(text):
            fid = f"fig-{int(ref.group(1)):02d}"
            if fid not in figures:
                errors.append(f"{md}: broken figure ref [[{fid}]]")
        for ref in MD_LINK_RE.finditer(text):
            relpath = ref.group(1)
            full = (md.parent / relpath).resolve()
            # only check if it's a chapter file
            if "part-" in relpath and not full.exists():
                errors.append(f"{md}: broken markdown link to {relpath}")

    if errors:
        print(f"✗ {len(errors)} broken reference(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✓ {len(chapters)} chapter(s) checked, 0 broken references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())