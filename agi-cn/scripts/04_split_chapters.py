#!/usr/bin/env python3
"""
scripts/04_split_chapters.py
============================
按章节合并清洗后的页面,生成每章的 source.md 和初步结构

输入: normalized/cleaned/*.md + config/chapters.yaml
输出:
  chapters/<id>-<slug>/source.md       # 该章完整 Markdown
  chapters/<id>-<slug>/meta.json       # 章节元数据
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
CLEANED_DIR = ROOT / "normalized" / "cleaned"
CHAPTERS_DIR = ROOT / "chapters"


def load_chapters() -> list[dict]:
    data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))
    return data["chapters"]


def read_page(page_num: int) -> str:
    f = CLEANED_DIR / f"page-{page_num:04d}.md"
    if not f.exists():
        return ""
    return f.read_text(encoding="utf-8")


def merge_pages_to_markdown(start: int, end: int) -> str:
    """合并多页为单 Markdown"""
    parts = []
    for p in range(start, end + 1):
        content = read_page(p)
        # 移除 HTML 注释(已记录在 page-map 中)
        content = re.sub(r"<!--.*?-->\n*", "", content)
        parts.append(content.strip("\n"))
    return "\n\n".join(parts)


def main():
    chapters = load_chapters()
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

    summary = []
    for ch in chapters:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"
        ch_dir.mkdir(parents=True, exist_ok=True)

        start = ch["pdf_start_page"]
        end = ch["pdf_end_page"]

        # 合并章节页面
        content = merge_pages_to_markdown(start, end)

        # 写入 source.md
        source_file = ch_dir / "source.md"
        header = (
            f"# 第 {cid} 章 {ch['zh_title']}\n\n"
            f"<!-- chapter: {cid} | en_title: {ch['en_title']} | part: {ch['part']} | "
            f"pages: {start}-{end} | toc_page: {ch['toc_start_page']} -->\n\n"
        )
        source_file.write_text(header + content + "\n", encoding="utf-8")

        # 元数据
        meta = {
            "id": cid,
            "part": ch["part"],
            "slug": slug,
            "en_title": ch["en_title"],
            "zh_title": ch["zh_title"],
            "pdf_pages": [start, end],
            "page_count": end - start + 1,
            "char_count": len(content),
            "word_count": len(content.split()),
            "source_file": str(source_file.relative_to(ROOT)),
        }
        meta_file = ch_dir / "meta.json"
        meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        summary.append({
            "id": cid,
            "zh_title": ch["zh_title"],
            "pages": f"{start}-{end}",
            "page_count": end - start + 1,
            "chars": len(content),
        })

    # 输出摘要
    print("=== 29 章切分完成 ===")
    total_chars = 0
    total_pages = 0
    for s in summary:
        print(f"  Ch {s['id']:>2} {s['zh_title']:<28} [{s['pages']:<8}] "
              f"{s['page_count']:>2} 页 | {s['chars']:>6,} 字符")
        total_chars += s["chars"]
        total_pages += s["page_count"]
    print(f"\n总计: {total_pages} 页 | {total_chars:,} 字符(约 {total_chars // 5:,} 英文词)")


if __name__ == "__main__":
    main()