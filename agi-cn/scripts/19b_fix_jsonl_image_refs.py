#!/usr/bin/env python3
"""
scripts/19b_fix_jsonl_image_refs.py
===================================
直接修复 chapters/*/translated.jsonl 中的图引用,把旧路径替换为新 SVG 路径。

输入:output/agi-zh-by-chapter/svg/manifest.json(图清单)
处理:对每条记录(无论 type),对其 content/translated 字段做正则替换

替换规则(基于 figure_id):
  normalized/figures/figure-N.jpg → svg/fig-X-Y.svg (按上下文 ID)
  images/fig14_2.png → svg/fig-14-2.svg
  fig15-1.png → svg/fig-15-1.svg
  ...

策略:
  对每个 chunk,找出所有 ![alt](path) 引用,提取 figure ID,替换为 SVG 路径。
  与 scripts/19_fix_image_refs.py 逻辑相同,但作用于 translated.jsonl。
"""

import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"
SVG_MANIFEST = ROOT / "output" / "agi-zh-by-chapter" / "svg" / "manifest.json"


def figure_id_from_alt(alt: str, path: str) -> str | None:
    m = re.search(r"图\s*(\d+)\s*[.\-]\s*(\d+)", alt)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.search(r"图\s*(\d+)\s*[_\-]?\.?\s*(\d+)", path)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.search(r"(?:fig|figure)[_-]?(\d+)[_-](\d+)", path.lower())
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None


def fix_text(text: str, manifest: dict, chapter_id: int) -> str:
    """修复文本中的图引用"""
    if "![" not in text:
        return text

    # 找出所有匹配
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def replace_one(m):
        alt = m.group(1)
        path = m.group(2)
        # 跳过 URL
        if path.startswith(("http://", "https://")):
            return m.group(0)
        # 跳过已正确的 SVG 路径
        if path.endswith(".svg") and "fig-" in path:
            return m.group(0)
        # 跳过断锚
        if path.startswith("#"):
            return ""
        # 提取 figure ID
        fig_id = figure_id_from_alt(alt, path)
        if not fig_id:
            return m.group(0)
        # 检查 manifest
        if fig_id in manifest:
            svg_path = manifest[fig_id]["file"]
            title_zh = manifest[fig_id]["title"]
            new_alt = f"图 {fig_id.replace('-', '.')} {title_zh}"
            return f"![{new_alt}]({svg_path})"
        return m.group(0)

    return pattern.sub(replace_one, text)


def main():
    if not SVG_MANIFEST.exists():
        print("SVG manifest 不存在")
        return
    manifest = json.loads(SVG_MANIFEST.read_text(encoding="utf-8"))
    manifest = {k: v for k, v in manifest.items() if v.get("valid")}
    print(f"SVG manifest: {len(manifest)} 个有效图")

    chapters = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]
    total = 0
    for ch in chapters:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"
        jsonl = ch_dir / "translated.jsonl"
        if not jsonl.exists():
            continue

        records = []
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            # 修复 translated 字段(对所有 type)
            if rec.get("translated"):
                old = rec["translated"]
                new = fix_text(old, manifest, cid)
                if new != old:
                    rec["translated"] = new
                    total += 1
            # 修复 content 字段(英文原文中可能也有引用,虽然少见)
            if rec.get("content"):
                old = rec["content"]
                new = fix_text(old, manifest, cid)
                if new != old:
                    rec["content"] = new
            records.append(rec)

        # 写回
        jsonl.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
            encoding="utf-8",
        )

    print(f"已修复 {total} 条 translated.jsonl 记录")


if __name__ == "__main__":
    main()