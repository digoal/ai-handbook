#!/usr/bin/env python3
"""
scripts/17b_regenerate_md.py
=============================
根据 chapters/<id>-<slug>/translated.jsonl 重新生成
output/agi-zh-by-chapter/<id>-<slug>.md 文件。

在 17_fix_translation.py 修改了 translated.jsonl 后调用。

实现:复用 10_merge_chapters.py 的 merge_chapter 逻辑。
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


def format_code_block(content: str) -> str:
    lang = "python"
    if "import os" in content or "from langchain" in content:
        lang = "python"
    elif "const " in content or "function " in content:
        lang = "javascript"
    elif "$ " in content and ("pip" in content or "npm" in content):
        lang = "bash"
    elif "{" in content and "}" in content and ":" in content and not "def " in content:
        lang = "yaml"
    return f"```{lang}\n{content}\n```"


def merge_chapter(chapter: dict, blocks: list[dict]) -> str:
    lines = []
    cid = chapter["id"]
    lines.append(f"# 第 {cid} 章 {chapter['zh_title']}({chapter['en_title']})")
    lines.append("")
    lines.append(
        f"<!-- chapter: {cid} | part: {chapter['part']} | "
        f"pages: {chapter['pdf_start_page']}-{chapter['pdf_end_page']} | "
        f"translated_from: pdf/{chapter['pdf_start_page']:03d}-{chapter['pdf_end_page']:03d} -->"
    )
    lines.append("")

    for blk in blocks:
        btype = blk.get("type", "text")
        content = blk.get("translated", "")
        if btype == "code":
            lines.append(format_code_block(content))
            lines.append("")
        else:
            if content:
                lines.append(content)
                lines.append("")
    return "\n".join(lines)


def main():
    chapters_data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]

    total = 0
    for ch in chapters_data:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"
        jsonl = ch_dir / "translated.jsonl"
        if not jsonl.exists():
            print(f"  跳过 Ch {cid}: 无 translated.jsonl")
            continue

        blocks = []
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            blocks.append(json.loads(line))

        chapter_md = merge_chapter(ch, blocks)
        ch_file = BY_CHAPTER_DIR / f"{cid:02d}-{slug}.md"
        ch_file.write_text(chapter_md + "\n", encoding="utf-8")
        total += 1

    print(f"已重新生成 {total} 个章节 markdown 文件")


if __name__ == "__main__":
    main()