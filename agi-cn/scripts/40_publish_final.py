#!/usr/bin/env python3
"""阶段 7: 发布级单文件 — 合并 + 扉页 + 锚链目录"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"


def slug_to_anchor(zh_title: str, num: int) -> str:
    """生成章节标题锚链"""
    return f"第-{num}-章-{zh_title.replace(':', '').replace(' ', '')}"


def main():
    print("=== 阶段 7: 发布级单文件 ===\n")

    # 加载章节元数据
    data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding='utf-8'))
    chapters = data['chapters']

    # 构建封面 + 版权 + 前言 + 目录
    cover = """# Agentic Design Patterns(智能体设计模式)

**A Hands-On Guide to Building Intelligent Systems**

*Antonio Gullí 著 · Springer 2025 · ISBN 978-3-032-01401-6*

**中文翻译版 · 仅供个人学习与内部研究使用**

---

## 版权声明

翻译稿仅供个人学习与内部研究使用,**不得公开发行、商业传播或用于任何商业用途**。

原书版权归 Springer Nature 所有(© The Author(s), under exclusive license to Springer Nature Switzerland AG 2025)。本翻译稿为受版权保护的演绎作品,任何使用应遵循原书的版权约束。

---

## 译者前言

本翻译稿由 Claude AI(MiniMax-M3 模型)全自动翻译,经三轮质量修复与发布标准审查:

- **第 1 轮**(2026-08-09):术语统一、补译、图替换
- **第 2 轮**(2026-08-09):未译段落清零、Ch 18 D → A、围栏修复
- **第 3 轮**(2026-08-09):发布标准收官,29/29 章节 A 级

本稿面向中文读者学习研究使用,保留所有正文结构、代码示例与图替代,术语严格遵循统一表。翻译采用意译为主,技术名词以"中文(English)"格式首次出现,代码块完全保留原文。

---

## 目录

"""

    # 章节分组(Part I / Part II)
    toc_parts = {"I": [], "II": []}
    for ch in chapters:
        toc_parts[ch['part']].append(ch)

    toc_lines = []
    for part in ["I", "II"]:
        part_zh = "模式篇" if part == "I" else "补充篇"
        toc_lines.append(f"### Part {part}: The Patterns({part_zh})")
        toc_lines.append("")
        for ch in toc_parts[part]:
            anchor = slug_to_anchor(ch['zh_title'], ch['id'])
            toc_lines.append(f"- [{ch['zh_title']}](#{anchor})  ")
            toc_lines.append(f"  *({ch['en_title']})* — 原书 pp. {ch['pdf_start_page']}-{ch['pdf_end_page']}")
        toc_lines.append("")

    toc = "\n".join(toc_lines)

    # 合并所有章节内容
    chapter_blocks = []
    for ch in chapters:
        ch_file = BY_CHAPTER_DIR / f"{ch['id']:02d}-{ch['slug']}.md"
        if not ch_file.exists():
            print(f"  ⚠ {ch_file.name} 不存在,跳过")
            continue
        text = ch_file.read_text(encoding='utf-8')
        chapter_blocks.append(text)

    # 写入 agi-zh.md
    out_path = ROOT / "output" / "agi-zh.md"
    full_content = cover + toc + "\n---\n\n" + "\n\n---\n\n".join(chapter_blocks)
    full_content += "\n\n---\n\n## 译者后记\n\n本翻译稿由 Claude AI 全自动翻译,经三轮质量审查达成发布标准。如有翻译疑问或建议,请对照原书 Springer 2025 出版版本。\n"
    out_path.write_text(full_content, encoding='utf-8')

    size_kb = out_path.stat().st_size / 1024
    print(f"  ✓ output/agi-zh.md: {size_kb:.1f} KB")
    print(f"  ✓ 包含 {len(chapter_blocks)} 章")
    print(f"  ✓ 封面 + 版权 + 前言 + 锚链目录 + 章节 + 后记")
    return 0


if __name__ == "__main__":
    sys.exit(main())
