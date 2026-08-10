#!/usr/bin/env python3
"""
Validate FIG-NN consistency across handbook.

Catches three failure modes:
1. README declares a FIG-NN that no chapter actually draws (ghost figure).
2. A chapter declares ### FIG-NN that README doesn't list.
3. Same FIG-NN declared in multiple chapters (number collision).

Usage:
    python scripts/check_figures.py [chapter.md ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HANDBOOK_ROOT = Path(__file__).resolve().parent.parent
README = HANDBOOK_ROOT / "README.md"

# Match `### FIG-NN ...` (NN = 1-3 digits) inside chapter ### headings
CHAPTER_FIG_RE = re.compile(r"^###\s+(FIG-(\d{1,3}))\b", re.MULTILINE)
# Match FIG-NN tokens in README (not just in headings)
README_FIG_RE = re.compile(r"\bFIG-(\d{1,3})\b")
PARTS = [
    "part-i-foundations",
    "part-ii-core-modules",
    "part-iii-cross-cutting",
    "part-iv-integrations",
    "part-v-workflows",
    "part-vi-operations",
    "part-vii-reference",
]


def iter_chapters(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    chapters: list[Path] = []
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            chapters.extend(sorted(part_dir.glob("ch-*.md")))
    return chapters


def chapter_figures(chapter_text: str) -> list[str]:
    """Return sorted list of `fig-NN` ids declared via `### FIG-NN ...`."""
    return sorted({f"fig-{int(m.group(2)):02d}" for m in CHAPTER_FIG_RE.finditer(chapter_text)})


def readme_figures() -> list[str]:
    if not README.exists():
        return []
    text = README.read_text(encoding="utf-8")
    return sorted({f"fig-{int(m.group(1)):02d}" for m in README_FIG_RE.finditer(text)})


def main() -> int:
    chapters = iter_chapters(sys.argv[1:])
    readme = set(readme_figures())

    declared: dict[str, list[Path]] = {}  # fig-NN -> [chapter_paths]
    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        for fid in chapter_figures(text):
            declared.setdefault(fid, []).append(ch)

    errors: list[str] = []

    # Ghost: README mentions but no chapter declares
    for fid in readme:
        if fid not in declared:
            errors.append(f"GHOST: README mentions {fid.upper()} but no chapter declares it")

    # Orphan: chapter declares but README doesn't list
    for fid in sorted(declared):
        if fid not in readme:
            chs = ", ".join(p.name for p in declared[fid])
            errors.append(f"ORPHAN: chapter(s) [{chs}] declare {fid.upper()} but README doesn't list it")

    # Collision: same FIG-NN in multiple chapters
    for fid, chs in sorted(declared.items()):
        if len(chs) > 1:
            names = ", ".join(p.name for p in chs)
            errors.append(f"COLLISION: {fid.upper()} declared in multiple chapters: {names}")

    if errors:
        print(f"✗ {len(errors)} FIG issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    total_figs = len(declared)
    print(f"✓ {total_figs} unique figure(s) consistent between README and chapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())