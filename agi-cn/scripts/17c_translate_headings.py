#!/usr/bin/env python3
"""
scripts/17c_translate_headings.py
==================================
检测并翻译 output/agi-zh-by-chapter/*.md 中的英文章节标题。

策略:
  - 仅翻译 2 级及以上标题(## , ### 等),因为这是书内章节子标题
  - 1 级标题(#)通常是整章标题,不应翻译
  - 对于每个英文标题:
    1. 优先查找翻译稿对应章节的 source.md,看是否已有中文版
    2. 否则调用 Claude API 翻译(单条标题)
    3. 或使用预定义常见标题映射表(快速修复)

实现:
  - 复用 08_translate_blocks.py 的 translate_block(简化版)
  - 缓存翻译结果,避免重复 API 调用
"""

import json
import os
import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import yaml
    from anthropic import Anthropic
except ImportError as e:
    print(f"缺少依赖: {e}", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"

# 常用术语翻译映射(用于快速修复)
HEADING_TRANSLATIONS = {
    "Parallelization Pattern Overview": "并行化模式概览",
    "Parallelization": "并行化",
    "Reflection Pattern Overview": "反思模式概览",
    "Tool Use (Function Calling) Pattern Overview": "工具使用(函数调用)模式概览",
    "Planning Pattern Overview": "规划模式概览",
    "Multi-Agent Collaboration Pattern Overview": "多智能体协作模式概览",
    "Memory Management Pattern Overview": "记忆管理模式概览",
    "Learning and Adaptation Pattern Overview": "学习与适应模式概览",
    "Model Context Protocol Pattern Overview": "模型上下文协议模式概览",
    "Goal Setting and Monitoring Pattern Overview": "目标设定与监控模式概览",
    "Exception Handling and Recovery Pattern Overview": "异常处理与恢复模式概览",
    "Human-in-the-Loop Pattern Overview": "人在回路模式概览",
    "Knowledge Retrieval (RAG) Pattern Overview": "知识检索(RAG)模式概览",
    "Inter-Agent Communication (A2A) Pattern Overview": "智能体间通信(A2A)模式概览",
    "Resource-Aware Optimization Pattern Overview": "资源感知优化模式概览",
    "Reasoning Techniques Pattern Overview": "推理技术模式概览",
    "Guardrails/Safety Patterns Pattern Overview": "护栏/安全模式概览",
    "Evaluation and Monitoring Pattern Overview": "评估与监控模式概览",
    "Prioritization Pattern Overview": "优先级排序模式概览",
    "Exploration and Discovery Pattern Overview": "探索与发现模式概览",
    "Augmentation, and Limitations": "增强与局限",
    "Safety": "安全性",
    "Conclusion": "结论",
    "Conclusions": "结论",
    "References": "参考文献",
    "Bibliography": "参考文献",
    "At a Glance": "速览",
    "Key Insights": "核心洞察",
    "Practical Applications and Use Cases": "实际应用与用例",
    "Practical Applications & Use Cases": "实际应用与用例",
    "Hands-on Code Examples": "动手代码示例",
    "Hands-on Code": "动手代码",
    "Code Examples": "代码示例",
    "Summary": "小结",
    "Key Takeaways": "关键要点",
    "Best Practices": "最佳实践",
    "Common Pitfalls": "常见陷阱",
    "Implementation Considerations": "实施注意事项",
    "Step-Back Prompting": "回退提示",
    "Vibe Coding: A Starting Point": "氛围编码:起点",
    "Principles for Leading the Augmented Team": "领导增强团队的原则",
    "Claude CLI (Claude Code)": "Claude CLI(Claude Code)",
    "Security Inter-Agent Communication (A2A): Inter-Agent Communication": "安全智能体间通信(A2A):智能体间通信",
    "Implementation Considerations and Best Practices": "实施注意事项与最佳实践",
    # 阶段 2 扩展(review 第三轮)
    "Hands-On Code Example": "动手代码示例",
    "Hands-On Code Example (Google ADK)": "动手代码示例(Google ADK)",
    "Hands-On Code with OpenAI": "使用 OpenAI 的动手代码",
    "Agents as Team Members": "智能体作为团队成员",
    "Code Analysis": "代码分析",
    "Code Generation and Debugging": "代码生成与调试",
    "Complex Problem Solving": "复杂问题求解",
    "Complex Query Answering": "复杂查询应答",
    "Conclusions": "结论",
    "Conversational Agents": "对话式智能体",
    "Google Search": "Google 搜索",
    "Graph RAG": "Graph RAG",
    "Information Processing Workflows": "信息处理工作流",
    "OpenAI Deep Research API": "OpenAI Deep Research API",
    "Overall Conclusion": "总体结论",
    "Planning and Strategy": "规划与策略",
    "Practical Applications and Use Cases": "实际应用与用例",
    "Renewable Energy Findings": "可再生能源发现",
    "Electric Vehicle Findings": "电动汽车发现",
    "Carbon Capture Findings": "碳捕集发现",
    "Summary of Recent Sustainable Technology Advancements": "近期可持续技术进展总结",
    "Summarization and Information Synthesis": "摘要与信息综合",
    "Vertex Memory Bank": "Vertex 记忆库",
    # 保留英文不译(框架/产品名)
    "Aider": "Aider",
    "CrewAI": "CrewAI",
    "Gemini CLI": "Gemini CLI",
    "GitHub Copilot CLI": "GitHub Copilot CLI",
    "Google ADK": "Google ADK",
    "Google Co-scientist": "Google Co-scientist",
    "Grok": "Grok",
    # 兼容无空格形式
    "Claude CLI(Claude Code)": "Claude CLI(Claude Code)",
}


def translate_with_cache(client, model: str, heading: str, cache: dict) -> str:
    """翻译标题(带缓存)"""
    if heading in cache:
        return cache[heading]

    # 静态映射命中
    if heading in HEADING_TRANSLATIONS:
        cache[heading] = HEADING_TRANSLATIONS[heading]
        return HEADING_TRANSLATIONS[heading]

    # 调用 LLM
    prompt = f"""将以下技术书籍的英文小标题翻译为简体中文。
要求:简洁、专业,符合中文书籍的小标题风格。

英文标题: {heading}

只输出翻译后的中文标题,不要任何其他内容。"""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        result = ""
        for blk in response.content:
            if blk.type == "text":
                result += blk.text
        result = result.strip()
        # 去除可能的引号或前缀
        result = re.sub(r'^["\']|["\']$', "", result)
        result = re.sub(r"^翻译[::]\s*|^中文[::]\s*", "", result)
        cache[heading] = result
        return result
    except Exception as e:
        print(f"  Error translating '{heading}': {e}", file=sys.stderr)
        cache[heading] = heading
        return heading


def translate_chapter_headings(ch_file: Path, client, model: str, cache: dict) -> tuple[int, dict]:
    """翻译一个章节的英文标题"""
    text = ch_file.read_text(encoding="utf-8")
    lines = text.split("\n")
    changes = []

    # 收集所有英文标题行(2 级及以上)
    en_heading_indices = []
    for i, line in enumerate(lines):
        m = re.match(r"^(##+)\s+(.+)$", line)
        if not m:
            continue
        title = m.group(2).strip()
        if not title:
            continue
        # 全英文(无中文)
        chinese = sum(1 for c in title if "一" <= c <= "鿿")
        if chinese == 0 and len(title) > 3:
            en_heading_indices.append(i)

    # 并发翻译
    if not en_heading_indices:
        return 0, cache

    headings = [lines[i].split(None, 1)[1] for i in en_heading_indices]

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(translate_with_cache, client, model, h, cache): (i, h)
            for i, h in zip(en_heading_indices, headings)
        }
        for future in as_completed(futures):
            i, original = futures[future]
            try:
                translated = future.result()
            except Exception as e:
                translated = original
            m = re.match(r"^(##+)\s+", lines[i])
            level = m.group(1) if m else "##"
            lines[i] = f"{level} {translated}"
            changes.append((i, original, translated))

    # 写回
    new_text = "\n".join(lines)
    if new_text != text:
        ch_file.write_text(new_text, encoding="utf-8")

    return len(changes), cache


def main():
    chapters_data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]

    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    base_url = os.environ.get("ANTHROPIC_BASE_URL")
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    client = Anthropic(**client_kwargs)
    model = os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", "claude-opus-4-8")

    cache = {}
    total = 0
    for ch in chapters_data:
        cid = ch["id"]
        slug = ch["slug"]
        ch_file = BY_CHAPTER_DIR / f"{cid:02d}-{slug}.md"
        if not ch_file.exists():
            continue
        n, cache = translate_chapter_headings(ch_file, client, model, cache)
        if n > 0:
            print(f"  Ch {cid:>2} {ch['zh_title']:<28}: {n} 标题已翻译")
            total += n

    print(f"\n=== 汇总 ===")
    print(f"总翻译标题: {total}")
    print(f"缓存条目: {len(cache)}")


if __name__ == "__main__":
    main()