#!/usr/bin/env python3
"""
scripts/03_normalize_text.py
============================
页面级清洗:去除每页的页眉/页脚/页码/作者名

输入: normalized/pages/page-NNNN.md
输出: normalized/cleaned/page-NNNN.md(同结构,清洗后)

清洗规则:
- 删除每页顶部的 "A. Gullí" / 章节名 + 页码 格式的页眉
- 删除每页底部的页码 + 章节名(如 "  Pattern   NNN")
- 保留正文内容
"""

import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
PAGES_DIR = ROOT / "normalized" / "pages"
CLEANED_DIR = ROOT / "normalized" / "cleaned"


# 页眉模式(出现在每页顶部/底部)
HEADER_PATTERNS = [
    # 奇数页(右侧): "  N Chapter Name           NNN"
    r"^\s*\d{1,2}\s+[A-Z][A-Za-z][A-Za-z\s(),/:&\-'.]{2,60}?\s{2,}\d{1,3}\s*$",
    # 偶数页(左侧): "NNN       A. Gullí"
    r"^\s*\d{1,3}\s{2,}A\.\s*Gullí\s*$",
    # "  NNN" 单独页码(页脚)
    r"^\s*\d{1,3}\s*$",
    # 罗马数字页眉/页脚
    r"^\s*[ivxlcdm]+\s+[A-Z][A-Za-z\s()]+(?:\s+\d+)?\s*$",
    r"^\s*[A-Z][A-Za-z\s()]+\s+[ivxlcdm]+\s*$",
]


def is_header_or_footer(line: str) -> bool:
    for pat in HEADER_PATTERNS:
        if re.match(pat, line):
            return True
    return False


def clean_page(content: str) -> str:
    lines = content.split("\n")
    if not lines:
        return content

    # 跳过开头的 HTML 注释行(页面标识)和空行
    start = 0
    while start < len(lines):
        line = lines[start].strip()
        if line.startswith("<!--") or line == "":
            start += 1
        else:
            break

    # 跳过页眉:从 start 开始删除连续匹配的页眉行
    while start < len(lines) and is_header_or_footer(lines[start]):
        start += 1

    # 跳过页脚:从底部开始删除连续匹配的页脚行
    end = len(lines)
    while end > start and is_header_or_footer(lines[end - 1]):
        end -= 1

    cleaned = lines[start:end]

    # 删除连续的多个空行(保留最多 2 个)
    result = []
    blank_count = 0
    for line in cleaned:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)

    return "\n".join(result).strip("\n")


def main():
    if not PAGES_DIR.exists():
        print(f"ERROR: {PAGES_DIR} 不存在", file=sys.stderr)
        sys.exit(1)

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    page_files = sorted(PAGES_DIR.glob("page-*.md"))
    print(f"开始清洗 {len(page_files)} 页...")

    cleaned_count = 0
    total_removed_chars = 0
    for f in page_files:
        content = f.read_text(encoding="utf-8")
        original_len = len(content)
        cleaned = clean_page(content)

        # 保留 HTML 注释行(页面标识)
        page_id_line = ""
        for line in content.split("\n"):
            if line.startswith("<!-- page:"):
                page_id_line = line
                break

        output = f"{page_id_line}\n\n{cleaned}\n"
        cleaned_file = CLEANED_DIR / f.name
        cleaned_file.write_text(output, encoding="utf-8")

        removed = original_len - len(cleaned)
        total_removed_chars += removed
        if removed > 50:
            cleaned_count += 1

    print(f"清洗完成: {cleaned_count} 页有显著变化(>50 字符)")
    print(f"总计删除: {total_removed_chars:,} 字符")


if __name__ == "__main__":
    main()