#!/usr/bin/env python3
"""Extract all mermaid blocks from chapter markdown files.

Writes assets/diagrams/<NN>-<slug>.mmd for each ```mermaid ... ``` block
in chapters/. Names are derived from the chapter number and a running index,
so render order is deterministic.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIAG_DIR = ROOT / "assets" / "diagrams"

CHAPTER_PAT = re.compile(r"chapter-(\d{2})-([a-z0-9-]+)\.md$")
MERMAID_PAT = re.compile(r"^```mermaid\n(.*?)\n```$", re.DOTALL | re.MULTILINE)


def slugify(text: str) -> str:
    """Extract a clean lowercase english/digit slug from a `%% title:` line.

    Strips `ChXX — ` prefix, removes punctuation, replaces spaces with dashes.
    Falls back to 'diagram' if nothing usable remains.
    """
    # Drop `ChNN — ` or `ChNN - ` prefix if present
    text = re.sub(r"^Ch\d{1,2}\s*[—\-:]\s*", "", text.strip())
    # Drop the chapter title (everything before the first em-dash or colon)
    parts = re.split(r"[—:]", text, maxsplit=1)
    rest = parts[1] if len(parts) == 2 else parts[0]
    rest = re.sub(r"[^A-Za-z0-9]+", "-", rest)
    return rest.strip("-").lower()[:50] or "diagram"


def extract() -> int:
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    # Clear stale .mmd files from prior runs so renames stay clean
    for stale in DIAG_DIR.glob("*.mmd"):
        stale.unlink()
    count = 0
    for md in sorted((ROOT / "chapters").rglob("chapter-*.md")):
        m = CHAPTER_PAT.search(md.name)
        if not m:
            continue
        ch_num = m.group(1)
        for idx, match in enumerate(MERMAID_PAT.finditer(md.read_text(encoding="utf-8")), 1):
            body = match.group(1).strip()
            title_match = re.match(r"^%%\s*title:\s*(.+)$", body.splitlines()[0])
            slug = slugify(title_match.group(1) if title_match else f"diagram-{idx}")
            out = DIAG_DIR / f"ch{ch_num}-{idx:02d}-{slug}.mmd"
            out.write_text(body + "\n", encoding="utf-8")
            count += 1
            print(f"  {out.name}")
    return count


if __name__ == "__main__":
    n = extract()
    print(f"\nExtracted {n} mermaid blocks")
    sys.exit(0)