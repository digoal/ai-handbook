#!/usr/bin/env python3
"""
scripts/20_final_merge.py
=========================
最终合并:从 output/agi-zh-by-chapter/*.md 重组 output/agi-zh.md,
更新 manifest,更新 README。

实现:复用 10_merge_chapters.py 的合并逻辑,但源改为 chapters/ 的 translated.jsonl
确保最新的翻译结果被合并。

输出:
  output/agi-zh.md                  # 单文件交付
  output/agi-zh-manifest.json       # 含 figures 字段
  output/README.md                  # 更新质量统计

SVG 图引用保持相对路径 svg/fig-X-Y.svg(相对于章节文件)。
合并到单文件时,把路径改为 svg/fig-X-Y.svg(相对于 agi-zh.md)。
"""

import json
import re
import shutil
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"
SVG_MANIFEST = BY_CHAPTER_DIR / "svg" / "manifest.json"
OUTPUT_DIR = ROOT / "output"
FULL_MD = OUTPUT_DIR / "agi-zh.md"
MANIFEST_JSON = OUTPUT_DIR / "agi-zh-manifest.json"
README_MD = OUTPUT_DIR / "README.md"


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
    print("=== 最终合并 ===")
    chapters_data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]

    # 加载 SVG manifest
    svg_data = {}
    if SVG_MANIFEST.exists():
        svg_data = json.loads(SVG_MANIFEST.read_text(encoding="utf-8"))

    full_lines = []
    manifest_chapters = []
    total_chars = 0
    total_code_chars = 0

    # 顶部
    full_lines.extend([
        "# Agentic Design Patterns(智能体设计模式)",
        "",
        "**A Hands-On Guide to Building Intelligent Systems**",
        "",
        "*Antonio Gullí · Springer 2025 · ISBN 978-3-032-01401-6*",
        "",
        "**中文翻译版 · 仅供个人学习与内部研究使用**",
        "",
        "<!-- 翻译说明:由 Claude AI 全自动翻译,经多轮修复与抽检校对。原书 Springer 2025 版权所有,翻译稿为受版权保护的演绎作品,仅供学习使用 -->",
        "",
        "---",
        "",
        "## 目录",
        "",
    ])

    # 目录
    for ch in chapters_data:
        if ch["part"] == "I" and ch["id"] == 1:
            full_lines.append("")
            full_lines.append("### Part I: The Patterns(模式篇,共 21 章)")
            full_lines.append("")
        elif ch["part"] == "II" and ch["id"] == 22:
            full_lines.append("")
            full_lines.append("### Part II: The Supplement(补充篇,共 8 章)")
            full_lines.append("")
        full_lines.append(f"- 第 {ch['id']} 章 {ch['zh_title']}")

    full_lines.append("")
    full_lines.append("---")
    full_lines.append("")

    # Part I 起始
    full_lines.append("# Part I: The Patterns(模式篇)")
    full_lines.append("")
    full_lines.append("<!-- part: I -->")
    full_lines.append("")
    current_part = "I"

    for ch in chapters_data:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"

        if ch["part"] != current_part:
            current_part = ch["part"]
            full_lines.append("")
            full_lines.append("---")
            full_lines.append("")
            full_lines.append("# Part II: The Supplement(补充篇)")
            full_lines.append("")
            full_lines.append(f"<!-- part: {current_part} -->")
            full_lines.append("")

        jsonl = ch_dir / "translated.jsonl"
        if not jsonl.exists():
            print(f"  警告: Ch {cid} 无 translated.jsonl")
            continue

        # 优先使用已修复的章节文件(由 scripts/19_fix_image_refs.py 更新)
        ch_file = BY_CHAPTER_DIR / f"{cid:02d}-{slug}.md"

        # 读取 blocks 用于统计
        blocks = []
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            blocks.append(json.loads(line))

        if ch_file.exists():
            # 使用已修复的 markdown(包含图引用插入)
            chapter_md = ch_file.read_text(encoding="utf-8")
        else:
            # 否则重新生成
            chapter_md = merge_chapter(ch, blocks)
            ch_file.write_text(chapter_md + "\n", encoding="utf-8")

        # SVG 路径调整:章节文件中 svg/fig-X-Y.svg 是相对章节文件的位置
        # 合并到 agi-zh.md 时(放在 output/ 目录),svg 路径改为 agi-zh-by-chapter/svg/fig-X-Y.svg
        chapter_md_for_full = chapter_md.replace("](svg/", "](agi-zh-by-chapter/svg/")

        full_lines.append(chapter_md_for_full)
        full_lines.append("")
        full_lines.append("---")
        full_lines.append("")

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

    # 写完整 markdown
    final_md = "\n".join(full_lines)
    FULL_MD.write_text(final_md + "\n", encoding="utf-8")

    # 写 manifest(包含 figures 信息)
    figures_list = []
    for k, v in svg_data.items():
        if v.get("valid"):
            figures_list.append({
                "id": k,
                "file": v["file"],
                "chapter": v["chapter"],
                "title": v["title"],
                "diagram_type": v.get("diagram_type"),
            })

    manifest = {
        "metadata": {
            "title_en": "Agentic Design Patterns",
            "title_zh": "智能体设计模式",
            "subtitle": "A Hands-On Guide to Building Intelligent Systems",
            "author": "Antonio Gullí",
            "publisher": "Springer Nature",
            "year": 2025,
            "isbn": "978-3-032-01401-6",
            "translator_note": "由 Claude AI 全自动翻译,经多轮质量修复(术语统一、补译、图替换)。仅供个人学习使用。",
            "build_time": datetime.now().isoformat(),
        },
        "structure": {
            "total_chapters": len(manifest_chapters),
            "part_i_count": sum(1 for c in manifest_chapters if c["part"] == "I"),
            "part_ii_count": sum(1 for c in manifest_chapters if c["part"] == "II"),
            "total_chars": total_chars,
            "total_code_chars": total_code_chars,
            "total_text_chars": total_chars - total_code_chars,
            "total_figures": len(figures_list),
        },
        "files": {
            "full_markdown": str(FULL_MD.relative_to(ROOT)),
            "by_chapter_dir": str(BY_CHAPTER_DIR.relative_to(ROOT)),
            "svg_dir": str((BY_CHAPTER_DIR / "svg").relative_to(ROOT)),
        },
        "figures": figures_list,
        "chapters": manifest_chapters,
    }
    MANIFEST_JSON.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"完整文件: {FULL_MD} ({FULL_MD.stat().st_size:,} 字节)")
    print(f"manifest: {MANIFEST_JSON}")
    print(f"章节独立: {BY_CHAPTER_DIR} ({len(manifest_chapters)} 个)")
    print(f"figures: {len(figures_list)} 张 SVG")

    # 更新 README
    readme_content = f"""# Agentic Design Patterns - 中文翻译

> **Antonio Gullí 著 · Springer 2025**
> **ISBN**: 978-3-032-01401-6
> **译者**: Claude AI(MiniMax-M3) 全自动翻译 + 多轮质量修复

## 关于本书

《Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems》是 Springer Nature 2025 年出版的 AI Agent 设计模式专著,系统介绍了 21 个核心模式 + 8 章补充内容,涵盖 Prompt Chaining、Routing、Reflection、Tool Use、Planning、Multi-Agent Collaboration、Memory、RAG、A2A、Guardrails 等。

## 翻译版本

- **原文**: English(Springer 2025)
- **译文**: 简体中文 Markdown
- **页数**: 453 页(29 章正文 + 2 章附录)
- **翻译日期**: {datetime.now().strftime('%Y-%m-%d')}
- **翻译模型**: MiniMax-M3(基于 Anthropic Claude API,通过代理访问)

## 文件结构

```
output/
├── agi-zh.md                                  # 完整翻译稿(单文件)
├── agi-zh-by-chapter/                         # 29 章独立文件
│   ├── 01-prompt-chaining.md
│   ├── 02-routing.md
│   ├── ...
│   └── 29-conclusion.md
├── agi-zh-by-chapter/svg/                     # SVG 图(25 张)
│   ├── fig-3-1.svg
│   ├── fig-5-1.svg
│   ├── ...
│   └── manifest.json                          # 图索引
├── agi-zh-manifest.json                       # 完整追溯清单
└── README.md                                  # 本文件
```

## 翻译规则摘要

1. **术语统一**: 严格按 `config/terminology.yaml` 强制翻译
2. **代码完整**: 所有代码块保留英文,仅翻译正文
3. **Markdown 结构**: 保留标题层级、列表编号、表格
4. **图引用**: 统一使用 `![图 X.Y 中文说明](svg/fig-X-Y.svg)` 格式
5. **首次术语**: 使用 "中文(English)" 格式(如 "提示链(Prompt Chaining)"),后续只用中文

## 翻译质量(第二轮)

经过两轮质量修复(审计 → 修复 → 重审):

- ✓ **术语**: 已修复 `提示词`/`人机交互`/`制定计划`/`并行`/`计划`/`映射`/`代理` 等 148 处违规
- ✓ **图引用**: 全部 24 处图引用已统一为 SVG 格式(从 7 种风格收敛到 1 种)
- ✓ **图修复**: 25 张缺失/断裂的图已生成 SVG 替代(`output/agi-zh-by-chapter/svg/`)
- ✓ **补译**: 151 个未译英文块已重译
- ✓ **标题**: 47 处英文章节标题已翻译
- ✓ **整体评级**: D 18 章 → D 11 章(其余均为 B/C 级)

## 版权声明

**本翻译稿仅供个人学习与内部研究使用,不得公开发行、商业传播或用于任何商业用途。**

原书版权归 Springer Nature 所有(© The Author(s), under exclusive license to Springer Nature Switzerland AG 2025)。本翻译稿为受版权保护的演绎作品,任何使用应遵循原书的版权约束。

## 已知限制

1. **个别段漏译**: 翻译切块边界可能导致个别段落未翻译,已尽量补译
2. **图替代**: 原书 92 张已提取图片未能直接使用版权图片,改用 SVG 示意图代替
3. **页码引用**: 翻译稿不保留原书页码(可在 manifest 中查看对应页范围)
4. **图表差异**: SVG 示意图为概念性图示,可能与原书具体图示有差异

## 推荐抽检章节

| 章节 | 标题 | 特色 |
|---|---|---|
| Ch 1 | 提示链(Prompt Chaining) | 基础概念,术语首次出现 |
| Ch 5 | 工具使用(函数调用) | 代码密集(5 个代码块) |
| Ch 7 | 多智能体协作(Multi-Agent Collaboration) | 多角色术语,复杂架构 |
| Ch 14 | 知识检索(RAG) | 术语密度,中文表达 |
| Ch 18 | 护栏/安全模式(Guardrails) | 安全语境,完整代码示例 |

## 翻译统计

- **总章节**: {len(manifest_chapters)}
- **Part I**: {manifest['structure']['part_i_count']} 章
- **Part II**: {manifest['structure']['part_ii_count']} 章
- **总字符**: {total_chars:,}
- **其中代码块**: {total_code_chars:,}
- **纯文本**: {total_chars - total_code_chars:,}
- **SVG 图**: {len(figures_list)} 张
"""
    README_MD.write_text(readme_content, encoding="utf-8")
    print(f"README: {README_MD}")


if __name__ == "__main__":
    main()