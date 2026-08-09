#!/usr/bin/env python3
"""
scripts/19_fix_image_refs.py
============================
统一所有图引用为 ![图 X.Y 中文说明](svg/fig-X-Y.svg) 格式。

功能:
  1. 修复已有图引用:
     - ![图 X.Y 描述](normalized/figures/figure-N.jpg) → ![图 X.Y 中文说明](svg/fig-X-Y.svg)
     - ![alt](images/fig14_2.png) → ![图 X.Y 中文说明](svg/fig-X-Y.svg)
     - ![alt](#) → 删除(断锚)
     - 图 X.Y (纯文字) → ![图 X.Y 说明](svg/fig-X-Y.svg)
  2. 插入缺失的图引用(原书有但翻译稿没有):
     - 找到提及 "图 X.Y" 的位置
     - 插入 ![图 X.Y 中文说明](svg/fig-X-Y.svg)

输入:
  - output/agi-zh-by-chapter/svg/manifest.json(图清单)
  - output/agi-zh-by-chapter/*.md(待修复)

输出:
  - 原地修改章节文件
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"
SVG_MANIFEST = BY_CHAPTER_DIR / "svg" / "manifest.json"
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"


def load_manifest() -> dict:
    """加载 SVG manifest,key 为 "X-Y" 格式"""
    if not SVG_MANIFEST.exists():
        return {}
    data = json.loads(SVG_MANIFEST.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if v.get("valid")}


def figure_id_from_alt(alt: str, path: str) -> str | None:
    """从 alt 文本或路径提取 figure ID,格式 "X-Y" """
    # alt 形如 "图 3.1 描述" → "3-1"
    m = re.search(r"图\s*(\d+)\s*[.\-]\s*(\d+)", alt)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.search(r"图\s*(\d+)\.(\d+)", alt)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    # path 形如 "fig3-1.svg" / "fig14_2.png" / "图7-3.png" / "图19-4"(无后缀)
    # 1. 中文 "图X-Y" 形式
    m = re.search(r"图\s*(\d+)\s*[_\-]?\.?\s*(\d+)", path)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    # 2. fig 英文形式
    m = re.search(r"fig[_-]?(\d+)[_-](\d+)", path.lower())
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None


def fix_chapter(ch_file: Path, manifest: dict, chapters_data: list[dict]) -> dict:
    """修复一个章节的图引用"""
    cid = int(ch_file.name.split("-")[0])
    text = ch_file.read_text(encoding="utf-8")
    original_text = text

    changes = {"replaced": 0, "deleted": 0, "inserted": 0}

    # 1. 修复已有引用
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        # 检测 ![alt](path) 引用
        matches = list(re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", line))
        if not matches:
            new_lines.append(line)
            continue

        new_line = line
        # 从后往前替换,避免索引错位
        for m in reversed(matches):
            alt = m.group(1)
            path = m.group(2)

            # 断锚:删除整行
            if path.startswith("#") or not path.strip():
                # 删除整行(因为它只剩这个无效引用)
                new_line = ""
                changes["deleted"] += 1
                continue

            # 提取 figure ID
            fig_id = figure_id_from_alt(alt, path)
            if not fig_id:
                # 不能识别,保留原样
                continue

            # 检查 SVG manifest
            if fig_id in manifest:
                svg_path = manifest[fig_id]["file"]  # 形如 "svg/fig-3-1.svg"
                title_zh = manifest[fig_id]["title"]
                new_alt = f"图 {fig_id.replace('-', '.')} {title_zh}"
                new_ref = f"![{new_alt}]({svg_path})"
                new_line = new_line[:m.start()] + new_ref + new_line[m.end():]
                changes["replaced"] += 1

        new_lines.append(new_line)

    text = "\n".join(new_lines)

    # 2. 插入缺失的图引用
    # 找出本章对应的 manifest 中的图 IDs
    chapter_figs = [k for k, v in manifest.items() if v.get("chapter") == cid]
    inserted_figs = set()

    for fig_id in chapter_figs:
        # 检查是否已有引用
        if f"svg/fig-{fig_id}.svg" in text:
            continue
        # 检查是否提到"图 X.Y"作为文字
        fig_dot = fig_id.replace("-", ".")
        # 查找引用位置
        pattern = re.compile(rf"图\s*{re.escape(fig_id.split('-')[0])}\s*[.\-]\s*{fig_id.split('-')[1]}|图\s*{re.escape(fig_dot)}")
        m = pattern.search(text)
        if not m:
            # 找不到引用位置,跳过
            continue

        title_zh = manifest[fig_id]["title"]
        svg_path = manifest[fig_id]["file"]
        alt_text = f"图 {fig_dot} {title_zh}"
        fig_ref = f"![{alt_text}]({svg_path})"

        # 在提及行后插入(同行末尾或新行)
        insert_pos = m.end()
        # 找到行末
        line_end = text.find("\n", insert_pos)
        if line_end == -1:
            line_end = len(text)
        # 在行末插入
        new_text = text[:line_end] + "\n\n" + fig_ref + "\n\n" + text[line_end:]
        text = new_text
        inserted_figs.add(fig_id)
        changes["inserted"] += 1

    if text != original_text:
        ch_file.write_text(text, encoding="utf-8")

    return changes


def main():
    print("=== 统一图引用 ===")
    manifest = load_manifest()
    print(f"SVG manifest: {len(manifest)} 个有效图")

    chapters_data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]

    total = {"replaced": 0, "deleted": 0, "inserted": 0}
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        ch = fix_chapter(ch_file, manifest, chapters_data)
        if any(ch.values()):
            print(f"  {ch_file.name}: 替换 {ch['replaced']} / 删除 {ch['deleted']} / 插入 {ch['inserted']}")
        for k, v in ch.items():
            total[k] += v

    print(f"\n=== 汇总 ===")
    for k, v in total.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()