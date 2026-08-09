#!/usr/bin/env python3
"""
scripts/01_extract_pdf.py
=========================
把 pdftotext -layout 输出的整本 raw-layout.txt 按页切分为 normalized/pages/page-NNNN.md

输入: source/raw-layout.txt (pdftotext 用 \x0c form feed 分页)
输出: normalized/pages/page-0001.md ... page-0453.md

页面分隔约定:
- \x0c (form feed, ASCII 12) 是 pdftotext 的页边界
- 每页保存为独立 Markdown 文件
- 文件命名: page-0001.md 4 位补零
- 文件顶部写入: <!-- page: NNNN | source: pdftotext -layout -->

依赖: 仅 Python 标准库
"""

import os
import sys
import hashlib
import json
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
SOURCE_FILE = ROOT / "source" / "raw-layout.txt"
OUTPUT_DIR = ROOT / "normalized" / "pages"
OUTPUT_FILE = ROOT / "normalized" / "pages-index.json"


def extract_pages(text: bytes) -> list[bytes]:
    """按 \\x0c 切分页"""
    pages = text.split(b"\x0c")
    # 最后一页通常是空(末尾的 form feed),去掉
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return pages


def normalize_page_text(page_bytes: bytes) -> str:
    """规范化单页文本"""
    # 解码为 UTF-8,忽略错误
    text = page_bytes.decode("utf-8", errors="replace")
    # 去除行尾空白,保留段落结构
    lines = text.split("\n")
    normalized = []
    for line in lines:
        # 保留原始缩进,只去除尾部空白
        normalized.append(line.rstrip())
    return "\n".join(normalized).strip("\n")


def page_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main():
    if not SOURCE_FILE.exists():
        print(f"ERROR: {SOURCE_FILE} 不存在", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = SOURCE_FILE.read_bytes()
    pages = extract_pages(raw)

    print(f"提取到 {len(pages)} 页")

    index = {
        "source_file": str(SOURCE_FILE),
        "extracted_at": __import__("datetime").datetime.now().isoformat(),
        "page_count": len(pages),
        "pages": [],
    }

    for i, page_bytes in enumerate(pages, start=1):
        text = normalize_page_text(page_bytes)
        sha = page_sha256(text)
        page_file = OUTPUT_DIR / f"page-{i:04d}.md"

        # 文件内容: HTML 注释 + 页面文本
        content = f"<!-- page: {i:04d} | sha256: {sha} | source: pdftotext -layout -->\n\n{text}\n"
        page_file.write_text(content, encoding="utf-8")

        index["pages"].append({
            "page": i,
            "file": str(page_file.relative_to(ROOT)),
            "sha256": sha,
            "char_count": len(text),
            "line_count": text.count("\n") + 1,
        })

    OUTPUT_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"已写入 {len(pages)} 个页面文件到 {OUTPUT_DIR}")
    print(f"索引: {OUTPUT_FILE}")

    # 简单统计
    total_chars = sum(p["char_count"] for p in index["pages"])
    total_lines = sum(p["line_count"] for p in index["pages"])
    empty = sum(1 for p in index["pages"] if p["char_count"] < 50)
    print(f"总字符数: {total_chars:,} | 总行数: {total_lines:,} | 短/空页(<50字符): {empty}")


if __name__ == "__main__":
    main()