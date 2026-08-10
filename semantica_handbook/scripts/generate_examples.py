#!/usr/bin/env python3
"""Generate handbook/examples/ch-NN-*.py stub scripts for all 56 chapters.

Each stub is ≤30 lines, suppresses logs, imports semantica defensively
(try/except ImportError) so it works without installing the full package.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HANDBOOK_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = HANDBOOK_ROOT / "part-i-foundations"
EXAMPLES_DIR = HANDBOOK_ROOT / "examples"

PARTS = [
    "part-i-foundations", "part-ii-core-modules", "part-iii-cross-cutting",
    "part-iv-integrations", "part-v-workflows", "part-vi-operations",
    "part-vii-reference",
]

TITLE_RE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
SLUG_RE = re.compile(r"^slug:\s*(ch-\d{2}-[a-z0-9-]+)\s*$", re.MULTILINE)


def chapter_title_slug(md_path: Path) -> tuple[str, str]:
    text = md_path.read_text(encoding="utf-8")
    m = TITLE_RE.search(text)
    s = SLUG_RE.search(text)
    if not (m and s):
        raise ValueError(f"Missing title/slug in {md_path}")
    return m.group(1), s.group(1)


def generate_stub(slug: str, title: str) -> str:
    return f'''# examples/{slug}.py
# Handbook chapter: {title}
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "{slug}"
CHAPTER_TITLE = "{title}"

print(f"handbook example for: {{CHAPTER_SLUG}}")
print(f"  title: {{CHAPTER_TITLE}}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
'''


def main() -> int:
    EXAMPLES_DIR.mkdir(exist_ok=True)
    written = 0
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if not part_dir.exists():
            continue
        for md in sorted(part_dir.glob("ch-*.md")):
            try:
                title, slug = chapter_title_slug(md)
            except ValueError as e:
                print(f"skip {md}: {e}", file=sys.stderr)
                continue
            target = EXAMPLES_DIR / f"{slug}.py"
            if not target.exists():
                target.write_text(generate_stub(slug, title), encoding="utf-8")
                written += 1
    print(f"✓ Wrote {written} new example stub(s) in {EXAMPLES_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())