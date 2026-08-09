#!/usr/bin/env python3
"""重新引用 13 个 orphan SVG:在合适位置插入 ![图 X.Y 中文](svg/fig-X-Y.svg)"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


def link_svg_to_chapter(ch_file: Path, fig_id: str, alt_text: str, insert_after_pattern: str | None = None) -> bool:
    """在章节中插入 SVG 引用"""
    text = ch_file.read_text(encoding='utf-8')

    # 检查是否已引用
    if f"svg/fig-{fig_id}.svg" in text:
        return False

    # 构造引用行
    ref = f"\n\n![图 {fig_id.replace('-', '.')} {alt_text}](svg/fig-{fig_id}.svg)\n"

    # 找到插入位置
    lines = text.split('\n')
    insert_idx = None

    if insert_after_pattern:
        for i, line in enumerate(lines):
            if re.search(insert_after_pattern, line):
                insert_idx = i + 1
                # 找下一个空行或段落边界
                while insert_idx < len(lines) and lines[insert_idx].strip():
                    insert_idx += 1
                break

    if insert_idx is None:
        # 默认:插入到文件末尾的参考文献之前
        for i, line in enumerate(lines):
            if re.match(r'^## 参考文献\s*$', line.strip()):
                insert_idx = i
                break
        if insert_idx is None:
            insert_idx = len(lines)

    lines.insert(insert_idx, ref.strip())
    text = '\n'.join(lines)
    ch_file.write_text(text, encoding='utf-8')
    return True


def main():
    print("=== 重新引用 orphan SVG ===\n")

    # 13 orphan SVG + 上下文
    orphans = [
        # (chapter_file, fig_id, alt_text, after_pattern)
        ("03-parallelization.md", "3-1", "并行化模式:多组件并发执行", r"^##.*并行化模式"),
        ("03-parallelization.md", "3-2", "并行化模式视觉总览", r"^##.*并行化模式"),
        ("05-tool-use.md", "5-1", "智能体使用工具的若干示例", r"^##.*工具使用"),
        ("06-planning.md", "6-4", "规划模式视觉总览", r"^##.*规划模式"),
        ("07-multi-agent-collaboration.md", "7-1", "多智能体系统架构", r"^##.*多智能体"),
        ("08-memory-management.md", "8-1", "记忆管理模式视觉总览", r"^##.*记忆管理"),
        ("10-model-context-protocol.md", "10-1", "模型上下文协议(MCP)架构", r"^##.*MCP"),
        ("11-goal-setting-and-monitoring.md", "11-2", "目标设定与监控模式视觉总览", r"^##.*目标设定"),
        ("13-human-in-the-loop.md", "13-1", "人在回路(HITL)模式", r"^##.*人在回路"),
        ("14-knowledge-retrieval-rag.md", "14-2", "智能体式 RAG:推理智能体优化检索", r"^##.*RAG"),
        ("16-resource-aware-optimization.md", "16-1", "OpenRouter:多模型路由平台", r"^##.*资源感知"),
        ("17-reasoning-techniques.md", "17-3", "ReAct 范式:推理-行动循环", r"^##.*推理-行动"),
        ("17-reasoning-techniques.md", "17-8", "推理设计模式总览", r"^##.*推理设计模式总览"),
    ]

    linked = 0
    for fname, fig_id, alt, pattern in orphans:
        ch_file = BY_CHAPTER_DIR / fname
        if not ch_file.exists():
            continue
        if link_svg_to_chapter(ch_file, fig_id, alt, pattern):
            print(f"  ✓ {fname}: 引用 fig-{fig_id}.svg")
            linked += 1
        else:
            print(f"  - {fname}: fig-{fig_id}.svg 已存在")

    print(f"\n=== 共重新引用 {linked} 张 SVG ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
