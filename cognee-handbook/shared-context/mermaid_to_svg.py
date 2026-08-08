#!/usr/bin/env python3
"""Rewrite inline ```mermaid blocks in chapter markdown to image refs.

Output goes to chapters/<part>/<chapter>.md (SVG refs in place of mermaid
blocks) so the chapters stay readable in any markdown viewer.

For each ```mermaid block we:
  1. Look up the matching .mmd in assets/diagrams/.
  2. Replace the whole fenced block with a single markdown image link
     ![Title](assets/diagrams/<NN>-<slug>.svg).

Block matching order follows the order in the chapter file, so the
chapter-NN-idx slug from extract_mermaid.py lines up.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Output directory: by default we write SVG-replaced chapters back into
# `chapters/`, replacing the inline ```mermaid blocks. The original
# inline-mermaid versions live in `chapters-inline-mermaid.bak/`.
DIST = ROOT / "chapters"
DIAG_DIR = ROOT / "assets" / "diagrams"

CHAPTER_PAT = re.compile(r"chapter-(\d{2})-([a-z0-9-]+)\.md$")
MERMAID_PAT = re.compile(r"^```mermaid\n(.*?)\n```\s*$", re.DOTALL | re.MULTILINE)
TITLE_PAT = re.compile(r"^%%\s*title:\s*(.+)$")


def collect_per_chapter() -> dict[str, list[Path]]:
    """Map chapter file name -> ordered list of corresponding .mmd files."""
    by_chapter: dict[str, list[Path]] = {}
    for mmd in sorted(DIAG_DIR.glob("ch*-*.mmd")):
        m = re.match(r"ch(\d{2})-\d{2}-", mmd.name)
        if not m:
            continue
        num = m.group(1)
        # find chapter file by its prefix number
        for chap in (ROOT / "chapters").rglob(f"chapter-{num}-*.md"):
            by_chapter.setdefault(chap.name, []).append(mmd)
    return by_chapter


def rewrite_one(chap_md: Path, mmd_files: list[Path]) -> Path:
    text = chap_md.read_text(encoding="utf-8")
    out_parts: list[str] = []
    last_end = 0
    mmd_iter = iter(mmd_files)
    for match in MERMAID_PAT.finditer(text):
        out_parts.append(text[last_end:match.start()])
        body = match.group(1).strip()
        title_m = TITLE_PAT.match(body.splitlines()[0])
        title = title_m.group(1).strip() if title_m else "diagram"
        try:
            mmd = next(mmd_iter)
        except StopIteration:
            # Mismatched count — fall back to fenced-code comment
            out_parts.append(f"<!-- mermaid block (no svg) -->\n\n```mermaid\n{body}\n```\n")
            last_end = match.end()
            continue
        # Image path is relative to the chapter file's directory (chapters/<part>/
        # chapter-XX-...md), so pandoc (which resolves <img> against the input
        # file's directory) finds the SVG in the repo-root assets/diagrams/ via
        # the leading `../../`.  Verified against cognee-handbook Makefile
        # `epub`/`pdf`/`html` targets which also pass `--resource-path=.`
        # to give pandoc an explicit fallback search path.
        svg_rel = Path("..", "..", "assets", "diagrams", mmd.stem + ".svg")
        out_parts.append(f"![{title}]({svg_rel.as_posix()})\n")
        last_end = match.end()
    out_parts.append(text[last_end:])
    rewritten = "".join(out_parts)

    rel = chap_md.relative_to(ROOT / "chapters")
    dest = DIST / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(rewritten, encoding="utf-8")
    return dest


def main() -> int:
    by_chapter = collect_per_chapter()
    # We write back into DIST (== chapters/) — back up the source first.
    # The caller is responsible for `cp -r chapters chapters-inline-mermaid.bak`
    # before invoking this; we don't back up again to avoid clobbering prior runs.
    DIST.mkdir(parents=True, exist_ok=True)
    written = 0
    for chap_name, mmds in sorted(by_chapter.items()):
        chap_md = next((ROOT / "chapters").rglob(chap_name), None)
        if chap_md is None:
            continue
        dest = rewrite_one(chap_md, mmds)
        written += 1
        print(f"  {dest.relative_to(ROOT)}")
    print(f"\nRewrote {written} chapters into {DIST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())