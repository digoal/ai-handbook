#!/usr/bin/env python3
"""
scripts/02_build_page_map.py
============================
建立 PDF 物理页码 → 章节 / 块 ID 的映射,并输出 page-map.json

输入: config/chapters.yaml + normalized/pages/*.md
输出: normalized/page-map.json

映射逻辑:
- 物理页 40 = Part I 扉页
- 物理页 41 = Ch 1 起始
- 物理页 356 = Part II 扉页
- 物理页 357 = Ch 22 起始
- 物理页 449 = Glossary
- 物理页 451 = Index
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML,请运行: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
PAGES_DIR = ROOT / "normalized" / "pages"
OUTPUT_FILE = ROOT / "normalized" / "page-map.json"


def load_chapters() -> dict:
    return yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))


def main():
    chapters = load_chapters()

    page_map = {
        "meta": {
            "total_pdf_pages": 453,
            "part_i_start": 40,
            "part_ii_start": 356,
            "back_matter_start": 449,
        },
        "chapters": {},
        "pages": [],  # 每页的章节归属
    }

    # 为每章构建页范围
    all_chapters = chapters["chapters"]
    for ch in all_chapters:
        cid = ch["id"]
        page_map["chapters"][cid] = {
            "id": cid,
            "part": ch["part"],
            "slug": ch["slug"],
            "en_title": ch["en_title"],
            "zh_title": ch["zh_title"],
            "pdf_start_page": ch["pdf_start_page"],
            "pdf_end_page": ch["pdf_end_page"],
            "toc_start_page": ch["toc_start_page"],
        }

    # 为每页标章节
    for page_num in range(1, 454):
        chapter_id = None
        part = None

        # Part I 扉页
        if page_num == 40:
            part = "I"
            chapter_id = None  # 扉页不属于具体章
        # Part II 扉页
        elif page_num == 356:
            part = "II"
            chapter_id = None
        # 章节正文
        else:
            for ch in all_chapters:
                if ch["pdf_start_page"] <= page_num <= ch["pdf_end_page"]:
                    chapter_id = ch["id"]
                    part = ch["part"]
                    break

        # 附录
        if chapter_id is None and page_num >= 449:
            if page_num < 451:
                section = "glossary"
            else:
                section = "index"
            page_map["pages"].append({
                "page": page_num,
                "chapter_id": None,
                "part": None,
                "section": section,
            })
        elif chapter_id is None and page_num < 40:
            # 前言/目录/版权
            page_map["pages"].append({
                "page": page_num,
                "chapter_id": None,
                "part": None,
                "section": "frontmatter",
            })
        elif chapter_id is None and page_num == 40:
            page_map["pages"].append({
                "page": page_num,
                "chapter_id": None,
                "part": "I",
                "section": "part_divider",
            })
        elif chapter_id is None and page_num == 356:
            page_map["pages"].append({
                "page": page_num,
                "chapter_id": None,
                "part": "II",
                "section": "part_divider",
            })
        else:
            page_map["pages"].append({
                "page": page_num,
                "chapter_id": chapter_id,
                "part": part,
                "section": "chapter",
            })

    OUTPUT_FILE.write_text(
        json.dumps(page_map, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"已生成 {OUTPUT_FILE}")
    print(f"总页数: {len(page_map['pages'])}")
    print(f"识别章节数: {len(page_map['chapters'])}")

    # 统计各章节页数
    print("\n=== 各章节 PDF 页数 ===")
    for cid in sorted(page_map["chapters"].keys(), key=int):
        ch = page_map["chapters"][cid]
        page_count = ch["pdf_end_page"] - ch["pdf_start_page"] + 1
        print(f"  Ch {cid:>2} {ch['zh_title']:<28} [{ch['pdf_start_page']:>3}-{ch['pdf_end_page']:>3}] = {page_count:>2} 页")

    # 验证没有空隙和重叠
    print("\n=== 验证章节页码连续性 ===")
    prev_end = 0
    issues = []
    for cid in sorted(page_map["chapters"].keys(), key=int):
        ch = page_map["chapters"][cid]
        if ch["pdf_start_page"] != prev_end + 1 and not (cid == 1 and prev_end == 0):
            if prev_end > 0 and ch["pdf_start_page"] - prev_end > 1:
                issues.append(f"  Ch {cid}: 起始 {ch['pdf_start_page']} 与上一章结束 {prev_end} 有空隙 {ch['pdf_start_page'] - prev_end - 1} 页")
        prev_end = ch["pdf_end_page"]
    if not issues:
        print("  ✓ 所有章节页码连续(允许 < 40 与 356 的扉页间隔)")
    else:
        for issue in issues:
            print(issue)


if __name__ == "__main__":
    main()