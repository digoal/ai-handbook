#!/usr/bin/env python3
"""
scripts/10_merge_chapters.py
============================
合并所有 29 章为最终 Markdown,并生成章节独立文件 + manifest

输入: chapters/<id>-<slug>/translated.jsonl
输出:
  output/agi-zh.md                           # 单文件交付
  output/agi-zh-by-chapter/<id>-<slug>.md    # 章节独立
  output/agi-zh-manifest.json                # 完整追溯
"""

import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"
OUTPUT_DIR = ROOT / "output"
BY_CHAPTER_DIR = OUTPUT_DIR / "agi-zh-by-chapter"


def load_chapters() -> list[dict]:
    return yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]


def format_code_block(content: str) -> str:
    """把代码块格式化为 Markdown 围栏"""
    # 保留原始内容,但加上围栏
    # 推断语言(简单启发式)
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


def load_translated(ch_dir: Path) -> list[dict]:
    f = ch_dir / "translated.jsonl"
    if not f.exists():
        return []
    return [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]


def merge_chapter(chapter: dict, blocks: list[dict]) -> str:
    """合并一章的所有块为 Markdown"""
    lines = []
    cid = chapter["id"]

    # 章节标题
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
    chapters = load_chapters()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BY_CHAPTER_DIR.mkdir(parents=True, exist_ok=True)

    full_lines = []
    manifest_chapters = []
    total_chars = 0
    total_code_chars = 0

    # 顶部标题与版权声明
    full_lines.extend([
        "# Agentic Design Patterns(智能体设计模式)",
        "",
        "**A Hands-On Guide to Building Intelligent Systems**",
        "",
        "*Antonio Gullí · Springer 2025 · ISBN 978-3-032-01401-6*",
        "",
        "**中文翻译版 · 仅供个人学习与内部研究使用**",
        "",
        "<!-- 翻译说明:由 Claude AI 全自动翻译,经人工抽检校对。原书 Springer 2025 版权所有,翻译稿为受版权保护的演绎作品,仅供学习使用 -->",
        "",
        "---",
        "",
        "## 目录",
        "",
    ])

    # 目录(用各章标题)
    for ch in chapters:
        if ch["part"] == "I" and ch["id"] == 1:
            full_lines.append("")
            full_lines.append("### Part I: The Patterns(模式篇,共 21 章)")
            full_lines.append("")
        elif ch["part"] == "II" and ch["id"] == 22:
            full_lines.append("")
            full_lines.append("### Part II: The Supplement(补充篇,共 8 章)")
            full_lines.append("")

        full_lines.append(f"- [第 {ch['id']} 章 {ch['zh_title']}](#第-{ch['id']}-章-{re.sub(r'[()]', '', ch['zh_title'])[:20]})")

    full_lines.append("")
    full_lines.append("---")
    full_lines.append("")

    # Part I 起始
    full_lines.append("# Part I: The Patterns(模式篇)")
    full_lines.append("")
    full_lines.append("<!-- part: I -->")
    full_lines.append("")

    current_part = "I"

    for ch in chapters:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"

        # Part 切换
        if ch["part"] != current_part:
            current_part = ch["part"]
            full_lines.append("")
            full_lines.append("---")
            full_lines.append("")
            full_lines.append(f"# Part {'II' if current_part == 'II' else 'I'}: The Supplement(补充篇)" if current_part == "II" else "# Part I: The Patterns(模式篇)")
            full_lines.append("")
            full_lines.append(f"<!-- part: {current_part} -->")
            full_lines.append("")

        blocks = load_translated(ch_dir)
        if not blocks:
            print(f"警告: Ch {cid} 没有翻译结果")
            continue

        # 生成章节内容
        chapter_md = merge_chapter(ch, blocks)

        # 写入独立文件
        ch_file = BY_CHAPTER_DIR / f"{cid:02d}-{slug}.md"
        ch_file.write_text(chapter_md + "\n", encoding="utf-8")

        # 累加到全文
        full_lines.append(chapter_md)
        full_lines.append("")
        full_lines.append("---")
        full_lines.append("")

        # 统计
        ch_chars = sum(len(b.get("translated", "")) for b in blocks)
        ch_code_chars = sum(len(b.get("translated", "")) for b in blocks if b.get("type") == "code")
        total_chars += ch_chars
        total_code_chars += ch_code_chars

        manifest_chapters.append({
            "id": cid,
            "part": ch["part"],
            "slug": slug,
            "zh_title": ch["zh_title"],
            "en_title": ch["en_title"],
            "pdf_pages": [ch["pdf_start_page"], ch["pdf_end_page"]],
            "block_count": len(blocks),
            "char_count": ch_chars,
            "code_char_count": ch_code_chars,
            "file": str(ch_file.relative_to(ROOT)),
        })

    # 写入完整 Markdown
    final_md = "\n".join(full_lines)
    full_file = OUTPUT_DIR / "agi-zh.md"
    full_file.write_text(final_md + "\n", encoding="utf-8")

    # 写入 manifest
    manifest = {
        "metadata": {
            "title_en": "Agentic Design Patterns",
            "title_zh": "智能体设计模式",
            "subtitle": "A Hands-On Guide to Building Intelligent Systems",
            "author": "Antonio Gullí",
            "publisher": "Springer Nature",
            "year": 2025,
            "isbn": "978-3-032-01401-6",
            "translator_note": "由 Claude AI 全自动翻译,经人工抽检校对。仅供个人学习使用。",
        },
        "structure": {
            "total_chapters": len(manifest_chapters),
            "part_i_count": sum(1 for c in manifest_chapters if c["part"] == "I"),
            "part_ii_count": sum(1 for c in manifest_chapters if c["part"] == "II"),
            "total_chars": total_chars,
            "total_code_chars": total_code_chars,
            "total_text_chars": total_chars - total_code_chars,
        },
        "files": {
            "full_markdown": str(full_file.relative_to(ROOT)),
            "by_chapter_dir": str(BY_CHAPTER_DIR.relative_to(ROOT)),
        },
        "chapters": manifest_chapters,
    }
    manifest_file = OUTPUT_DIR / "agi-zh-manifest.json"
    manifest_file.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"=== 合并完成 ===")
    print(f"完整文件: {full_file}")
    print(f"  大小: {full_file.stat().st_size:,} 字节")
    print(f"  字符: {len(final_md):,}")
    print(f"章节独立: {BY_CHAPTER_DIR}")
    print(f"  共 {len(manifest_chapters)} 个文件")
    print(f"manifest: {manifest_file}")
    print(f"")
    print(f"=== 统计 ===")
    print(f"  章节总数: {len(manifest_chapters)}")
    print(f"  Part I: {manifest['structure']['part_i_count']} 章")
    print(f"  Part II: {manifest['structure']['part_ii_count']} 章")
    print(f"  总字符: {total_chars:,}")
    print(f"  其中代码块: {total_code_chars:,}")
    print(f"  纯文本: {total_chars - total_code_chars:,}")


if __name__ == "__main__":
    main()