#!/usr/bin/env python3
"""阶段 4+5 残存未译段修复:
- Ch 4 L275-281 参考文献
- Ch 12 L122-128 参考文献
- Ch 17 L353-363 Bibliography
- Ch 22 L25 动词清单 → 表格
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


# ============== Ch 4 参考文献 ==============

def fix_ch4_refs():
    ch4 = BY_CHAPTER_DIR / "04-reflection.md"
    text = ch4.read_text(encoding='utf-8')

    # 找到 ## 参考文献 并替换内容
    new_refs = """## 参考文献

1. Google Agent Developer Kit (ADK) 文档(多智能体系统): <https://google.github.io/adk-docs/agents/multi-agents/>
2. LangChain Expression Language (LCEL) 文档: <https://python.langchain.com/docs/introduction/>
3. LangGraph 文档: <https://www.langchain.com/langgraph>
4. Kumar, A., et al. (2024). 《Training Language Models to Self-Correct via Reinforcement Learning》. arXiv 预印本, arXiv:2409.12917. <https://arxiv.org/abs/2409.12917>
"""

    text = re.sub(
        r'## 参考文献\s*\n[\s\S]*?(?=\n\n|\Z)',
        new_refs,
        text,
        count=1
    )
    ch4.write_text(text, encoding='utf-8')
    return True


# ============== Ch 12 参考文献 ==============

def fix_ch12_refs():
    ch12 = BY_CHAPTER_DIR / "12-exception-handling-and-recovery.md"
    text = ch12.read_text(encoding='utf-8')

    new_refs = """## 参考文献

1. McConnell, S. (2004). 《Code Complete》(第 2 版). Microsoft Press.
2. O'Neill, V. (2022). 《Improving Fault Tolerance and Reliability of Heterogeneous Multi-Agent IoT Systems Using Intelligence Transfer》. *Electronics*, 11(17), 2724.
3. Shi, Y., Pei, H., Feng, L., Zhang, Y., & Yao, D. (2024). 《Towards Fault Tolerance in Multi-Agent Reinforcement Learning》. *arXiv 预印本*, arXiv:2412.00534.
"""

    text = re.sub(
        r'## 参考文献\s*\n[\s\S]*?(?=\n\n|\Z)',
        new_refs,
        text,
        count=1
    )
    ch12.write_text(text, encoding='utf-8')
    return True


# ============== Ch 17 Bibliography ==============

def fix_ch17_refs():
    ch17 = BY_CHAPTER_DIR / "17-reasoning-techniques.md"
    text = ch17.read_text(encoding='utf-8')

    new_refs = """## 参考文献

1. Wei, J., et al. (2022). 《Chain-of-Thought Prompting Elicits Reasoning in Large Language Models》. *NeurIPS 2022*.
2. Snell, C., et al. (2024). 《Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for LLM Problem-Solving》. *arXiv 预印本*.
3. Anonymous. (2025). 《Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies》. <https://arxiv.org/abs/2502.02533>
4. Gao, L., et al. (2023). 《Program-Aided Language Models》. *ICML 2023*.
5. Yao, S., et al. (2023). 《ReAct: Synergizing Reasoning and Acting in Language Models》. *ICLR 2023*.
"""

    # 替换从 "## Bibliography" 到文末
    pattern = re.compile(r'(?:## Bibliography|## 参考文献)\s*\n[\s\S]*?(?=\Z)', re.MULTILINE)
    text = pattern.sub(new_refs, text)
    ch17.write_text(text, encoding='utf-8')
    return True


# ============== Ch 22 动词清单 → 表格 ==============

def fix_ch22_verb_list():
    ch22 = BY_CHAPTER_DIR / "22-advanced-prompting-techniques.md"
    text = ch22.read_text(encoding='utf-8')

    # 找到动词清单并替换为表格
    # Ch 22 L25 动词列表 — 文件中用的是全角冒号 U+FF1A
    old = "有效的动词包括：Act(行动)、Analyze(分析)、Categorize(分类)、Classify(归类)、Contrast(对比)、Compare(比较)、Create(创建)、Describe(描述)、Define(定义)、Evaluate(评估)、Extract(提取)、Find(查找)、Generate(生成)、Identify(识别)、List(列出)、Measure(衡量)、Organize(组织)、Parse(解析)、Pick(挑选)、Predict(预测)、Provide(提供)、Rank(排序)、Recommend(推荐)、Return(返回)、Retrieve(检索)、Rewrite(改写)、Select(选择)、Show(展示)、Sort(归类)、Summarize(总结)、Translate(翻译)、Write(撰写)。"

    new = """下表汇总了常用的动作动词,供提示设计参考:

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| Act | 行动 | Identify | 识别 |
| Analyze | 分析 | List | 列出 |
| Categorize | 分类 | Measure | 衡量 |
| Classify | 归类 | Organize | 组织 |
| Contrast | 对比 | Parse | 解析 |
| Compare | 比较 | Pick | 挑选 |
| Create | 创建 | Predict | 预测 |
| Describe | 描述 | Provide | 提供 |
| Define | 定义 | Rank | 排序 |
| Evaluate | 评估 | Recommend | 推荐 |
| Extract | 提取 | Return | 返回 |
| Find | 查找 | Retrieve | 检索 |
| Generate | 生成 | Rewrite | 改写 |
| Select | 选择 | Show | 展示 |
| Sort | 归类 | Summarize | 总结 |
| Translate | 翻译 | Write | 撰写 |
"""

    if old in text:
        text = text.replace(old, new)
        ch22.write_text(text, encoding='utf-8')
        return True
    if old_full in text:
        text = text.replace(old_full, new)
        ch22.write_text(text, encoding='utf-8')
        return True
    return False


# ============== 主流程 ==============

def main():
    print("=== 残存未译段 + 参考文献修复 ===\n")
    fixes = []
    if fix_ch4_refs():
        fixes.append("Ch 4 参考文献已翻译")
    if fix_ch12_refs():
        fixes.append("Ch 12 参考文献已翻译")
    if fix_ch17_refs():
        fixes.append("Ch 17 Bibliography 已翻译")
    if fix_ch22_verb_list():
        fixes.append("Ch 22 动词清单已转为表格")
    else:
        fixes.append("Ch 22 动词清单未找到原文,跳过")

    for f in fixes:
        print(f"  ✓ {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
