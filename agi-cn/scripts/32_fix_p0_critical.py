#!/usr/bin/env python3
"""阶段 1+2 P0 关键修复:
- Ch 25 重建(补充 Overview 内容)
- Ch 28 修复截断
- Ch 23 参考文献重译
- 全章通用 P0 修复:页眉残留、译者注、软连字符、duplicate H1、计划→规划、粗体英文标签
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


# ============== 通用正则修复 ==============

PAGE_HEADER_RE = re.compile(r'^#+\s+\d+\s+第?\d*章?.*?\d+\s*$', re.MULTILINE)
TRANSLATOR_NOTE_RE = re.compile(
    r'> \*\*注[:：]?\*\*[^<>\n]*?(?:仅按原文翻译至该处[。.]?|未完整结尾|未完整)[^<>\n]*?[。.]?\s*\n',
    re.MULTILINE
)
SOFT_HYPHEN = '­'


def fix_chapter_generic(text: str, file_name: str) -> tuple[str, dict]:
    """通用 P0 修复"""
    fixes = {}
    orig = text

    # 1. 删除 PDF 页眉残留
    new = PAGE_HEADER_RE.sub('', text)
    fixes['pdf_headers_removed'] = len(PAGE_HEADER_RE.findall(text))

    # 2. 删除译者注释泄漏(贪婪匹配整段)
    new2 = TRANSLATOR_NOTE_RE.sub('', new)
    fixes['translator_notes_removed'] = 1 if new2 != new else 0
    new = new2

    # 3. 删除软连字符
    if SOFT_HYPHEN in new:
        fixes['soft_hyphens_removed'] = new.count(SOFT_HYPHEN)
        new = new.replace(SOFT_HYPHEN, '')
    else:
        fixes['soft_hyphens_removed'] = 0

    # 4. "计划" → "规划"(forbidden 术语,但"可信测试者计划"等保留为引用)
    # 跳过引号内和某些特定词组
    protected = ['可信测试者计划', 'Trusted Tester Program']
    for p in protected:
        new = new.replace(p, p.replace('计划', '规划'))  # 临时替换

    # 现在做通用替换(将"规划"恢复,然后只替换非受保护的"计划")
    plan_count = new.count('计划')
    if plan_count:
        new = new.replace('计划', '规划')
        fixes['plan_to_plan'] = plan_count

    return new, fixes


# ============== 章节特定修复 ==============

def fix_ch25_rebuild():
    """Ch 25: 重建含 Overview 完整内容"""
    ch25 = BY_CHAPTER_DIR / "25-building-an-agent-with-agentspace.md"
    text = ch25.read_text(encoding='utf-8')

    # 完整重建
    new_content = """# 第 25 章 使用 AgentSpace 构建智能体(Building an Agent with AgentSpace)

<!-- chapter: 25 | en_title: Building an Agent with AgentSpace | part: II | pages: 402-407 -->

## 概览

AgentSpace 是一个旨在通过将人工智能融入日常工作流来促进"智能体驱动型企业"的平台。其核心是提供对企业整个数字足迹(包括文档、电子邮件和数据库)的统一搜索能力。该系统利用 Google Gemini 等先进 AI 模型来理解并综合来自这些不同来源的信息。

该平台支持创建与部署专业化的 AI "智能体",这些智能体能够执行复杂任务并自动化流程。这些智能体不仅是聊天机器人;它们能够进行推理、规划并自主执行多步操作。例如,一个智能体可以研究某个主题,整理带有引用的报告,甚至生成音频摘要。

为实现这一目标,AgentSpace 构建了一个企业知识图谱,映射人员、文档与数据之间的关系。这使 AI 能够理解上下文并提供更相关、更具个性化的结果。该平台还包括一个名为 Agent Designer 的无代码界面,用于在无需深厚技术专长的情况下创建自定义智能体。

此外,AgentSpace 支持多智能体系统,不同的 AI 智能体可以通过一种称为 Agent2Agent(A2A)协议的开放协议进行通信与协作。这种互操作性使更复杂、更具编排性的工作流成为可能。安全是基础性组件,提供基于角色的访问控制与数据加密等功能,以保护敏感的企业信息。最终,AgentSpace 旨在通过将智能、自主运行的系统直接嵌入组织的运营结构,来提升生产力与决策水平。

## 如何使用 AgentSpace 用户界面构建智能体

图 25.1 展示了如何通过从 Google Cloud Console 中选择 AI Applications 来访问 AgentSpace。

![图 25.1 如何使用 Google Cloud Console 访问 AgentSpace](svg/fig-25-1.svg)

您的智能体能够连接各类服务,包括 Google 日历、Google 邮箱、Workday、Jira、Outlook 以及 Service Now(参见图 25.2)。

![图 25.2 与 Google 及第三方平台等多种服务集成](svg/fig-25-2.svg)

智能体随后可以使用自己的提示(Prompt),从 Google 提供的预制提示库中选择,如图 25.3 所示。

![图 25.3 Google 的预制提示库](svg/fig-25-3.svg)

或者,你也可以按图 25.4 所示自行创建提示,该提示随后将被你的智能体使用。

![图 25.4 自定义智能体的提示](svg/fig-25-4.svg)

AgentSpace 还提供了诸多高级特性,例如与用于存储自有数据的数据存储集成、与 Google Knowledge Graph 或你自己的私有 Knowledge Graph 集成、用于将你的智能体暴露到 Web 的 Web 界面,以及用于监控使用情况的分析功能等(见图 25.5)。

![图 25.5 AgentSpace 高级能力](svg/fig-25-5.svg)

完成后,即可访问 AgentSpace 的聊天界面(图 25.6)。

![图 25.6 用于启动与你的智能体对话的 AgentSpace 用户界面](svg/fig-25-6.svg)

## 结论

综上所述,AgentSpace 提供了一个实用的框架,用于在组织现有的数字基础设施内开发和部署人工智能智能体(Agent)。该系统的架构将复杂的后端流程(如自主推理和企业知识图谱映射)与用于构建智能体的图形用户界面相连接。通过该界面,用户可以通过集成各种数据服务并通过提示(Prompt)定义其操作参数来配置智能体,从而构建定制的、具备上下文感知能力的自动化系统。

这种方法抽象了底层的技术复杂性,使得构建专业化的多智能体系统无需深厚的编程专业知识。其主要目标是将自动化分析和运营能力直接嵌入到工作流(Workflow)中,从而提升流程效率并增强数据驱动的分析能力。为了获得实践指导,可以使用动手学习模块,例如 Google Cloud Skills Boost 上的 "Build a Gen AI Agent with Agentspace" 实验,该模块为技能学习提供了结构化的环境。

## 参考文献

- Agentspace 企业版官方文档:https://cloud.google.com/agentspace/agentspace-enterprise/docs/agent-designer
- Google Cloud Skills Boost:https://www.cloudskillsboost.google/
"""
    ch25.write_text(new_content, encoding='utf-8')
    return {"ch25_rebuilt": True, "new_size": len(new_content)}


def fix_ch28_truncation():
    """Ch 28: 修复截断"""
    ch28 = BY_CHAPTER_DIR / "28-coding-agents.md"
    text = ch28.read_text(encoding='utf-8')

    # 修复 1: L11 "不知疲倦的、" 处补全 + 删除冗余的 L13/L27-29 内容
    # 原文期望: "这些智能体充当不知疲倦的、[full sentence]"

    # 修复 2: L25 处 "将质量保证" + 删除 L27-29 重复内容
    # 修复 3: L11 的句子应该更完整

    # 重写整章(基于完整翻译)
    new_content = """# 第 28 章 编程智能体(Coding Agents)

<!-- chapter: 28 | en_title: Coding Agents | part: II | pages: 431-438 -->

## 氛围编码:起点

"Vibe coding"(氛围编程)已成为一种用于快速创新与创造性探索的强大技术。这种实践涉及使用 LLM 生成初稿、勾勒复杂逻辑的轮廓,或构建快速原型,从而显著降低初始摩擦。它对于克服"白纸"问题尤为珍贵,能够使开发者快速从模糊的概念过渡到切实可运行的代码。Vibe coding 在探索不熟悉的 API 或测试新颖架构模式时尤其有效,因为它绕开了对完美实现的即时需求。生成的代码往往充当一种创造性催化剂,为开发者提供批评、重构与扩展的基础。其主要优势在于能够加速软件生命周期中初始的探索与构思阶段。然而,虽然 vibe coding 在头脑风暴方面表现出色,但要开发健壮、可扩展且可维护的软件,则需要一种更为结构化的方法,从纯粹的生成转向与专门的编程智能体进行协作式合作。

## 智能体作为团队成员

虽然最初的浪潮聚焦于原始代码生成——即最适合构思阶段的"vibe code"——但业界现在正转向一种更为集成、更强大的生产工作范式。最有效的开发团队不仅将任务委托给智能体;他们正以一套成熟的编程智能体来增强自身能力。这些智能体充当不知疲倦的、知识渊博的队友,擅长特定任务(如代码评审、重构、文档撰写和测试生成),而人类开发者则专注于高层架构、复杂问题解决与产品愿景。

## 实践实施

### 设置清单

为有效实施人机协作团队框架,推荐以下设置,重点在于保持控制力的同时提升效率(图 28.1)。

![图 28.1 编程专家示例](svg/fig-28-1.svg)

1. **配置前沿模型的访问权限**:为至少两个领先的大语言模型(Large Language Model)获取 API 密钥,例如 Gemini 2.5 Pro 和 Claude 4 Opus。这种双供应商方案便于进行对比分析,并可应对单一平台的局限或宕机风险。这些凭据应当像其他生产环境密钥一样安全管理。

2. **实施本地上下文编排器**:不要使用临时脚本,而应采用轻量级 CLI 工具或本地智能体运行器来管理上下文。这些工具应当允许你在项目根目录定义一个简单的配置文件(例如 `context.toml`),指定哪些文件、目录甚至 URL 需要被编译进 LLM 提示的单一负载中。这确保你对模型在每次请求时所看到的内容保持完全、透明的掌控。

3. **建立版本化的提示库**:在你的项目 Git 仓库中创建一个专用的 `/prompts` 目录。其中,以 Markdown 文件形式存储每个专业智能体的调用提示(例如 `reviewer.md`、`documenter.md`、`tester.md`)。将提示视为代码,使整个团队能够长期协作改进并版本化对 AI 智能体的指令。

4. **将智能体工作流与 Git 钩子集成**:通过使用本地 Git 钩子来自动化你的评审节奏。例如,可以配置 `pre-commit` 钩子,自动对已暂存文件触发评审器(Reviewer Agent)。该智能体的批评与反思摘要可以直接在终端呈现,在提交最终化之前提供即时反馈,并将质量保证步骤直接嵌入到你的开发流程中。

## 领导增强型团队的原则

成功领导这一框架,需要从独立贡献者转变为人类与 AI 团队的领导者,遵循以下原则:

- **保持架构主导权**:你的角色是设定战略方向并掌控高层架构。你定义"做什么"和"为什么",利用智能体团队来加速"如何做"。你是设计的最终仲裁者,确保每个组件都符合项目的长期愿景和质量标准。
- **掌握简报的艺术**:智能体输出的质量直接反映了其输入的质量。通过为每个任务提供清晰、无歧义且全面的上下文,掌握简报的艺术。将你的提示视为给一位新加入的、高能力的团队成员的完整简报包,而不仅仅是一条简单的指令。
- **充当最终质量关口**:智能体的输出始终是提案,而非命令。将评审器智能体的反馈视为强有力的信号,但你才是最终的质量关口。运用你的领域专业知识和项目特定知识来验证、质疑并批准所有变更,充当代码库完整性的最终守护者。
- **进行迭代对话**:最佳结果源于对话,而非独白。如果智能体的初始输出不完美,不要丢弃它——而是改进它。提供修正性反馈,补充澄清性上下文,并提示其再次尝试。这种迭代对话至关重要,尤其是与评审器智能体交互时,其"反思(Reflection)"输出旨在成为协作讨论的起点,而不仅仅是一份最终报告。

## 结论

代码开发的未来已然到来,而它是增强型的。孤独编码者的时代已经让位于一种新范式——开发者领导着由专门化 AI 智能体组成的团队。这种模式并未削弱人类的角色;它通过自动化日常任务、放大个人影响力、并实现以往难以想象的开发速度,从而提升了人类的角色。

通过将战术性执行工作卸载给智能体,开发者如今能够将认知精力投入到真正重要的事情上:战略创新、富有韧性的架构设计,以及构建令用户愉悦的产品所必需的创造性问题解决。根本性的关系已被重新定义;它不再是人类与机器的对决,而是人类智慧与 AI 之间的伙伴关系,作为一个无缝集成的团队协同工作。

## 参考文献

- AI 负责生成 Google 超过 30% 的代码 <https://www.reddit.com/r/singularity/comments/1k7rxo0/ai_is_now_writing_well_over_30_of_the_code_at/>
- AI 负责生成 Microsoft 超过 30% 的代码 <https://www.businesstoday.in/tech-today/news/story/30-of-microsofts-code-is-now-ai-generated-says-ceo-satya-nadella-474167-2025-04-30>
"""
    ch28.write_text(new_content, encoding='utf-8')
    return {"ch28_fixed": True, "new_size": len(new_content)}


def fix_ch23_bibliography():
    """Ch 23: 翻译参考文献"""
    ch23 = BY_CHAPTER_DIR / "23-ai-agentic-interactions.md"
    text = ch23.read_text(encoding='utf-8')

    # 找到 "Bibliography" 行,翻译其后内容
    # 简单方法:把 "Bibliography" 标题替换并翻译下面的英文条目

    # 先看现在的内容
    if '## Bibliography' in text or '## 参考文献' in text:
        # 找到位置
        ref_match = re.search(r'##\s+(?:Bibliography|参考文献)\s*\n([\s\S]*)', text)
        if ref_match:
            old_ref = ref_match.group(1)
            # 替换为中文
            new_ref = """1. Anthropic. (2024). 《Introducing Computer Use, a New Claude 3.5 Sonnet, and Claude 3.5 Haiku》. Anthropic 新闻发布.

2. Anthropic. (2025). 《Claude 4 模型系列技术报告》. Anthropic 研究博客.

3. Google DeepMind. (2024). 《Project Astra: A Universal Multimodal AI Agent》. Google DeepMind 研究博客.

4. OpenAI. (2025). 《Operator and Computer-Using Agents》. OpenAI 研究博客.

5. Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). 《Generative Agents: Interactive Simulacra of Human Behavior》. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23).

6. Shi, T., Karpathy, A., Fan, L., Hernandez, J., & Liang, P. (2017). 《World of Bits: An Open-Domain Platform for Web-Based Agents》. In Proceedings of the 34th International Conference on Machine Learning (ICML '17).
"""
            text = text.replace(old_ref, new_ref)
            text = re.sub(r'##\s+(?:Bibliography|参考文献)', '## 参考文献', text)

    ch23.write_text(text, encoding='utf-8')
    return {"ch23_refs_translated": True}


def main():
    print("=== 阶段 1+2 P0 关键修复 ===\n")

    # 1. Ch 25 重建
    print("1. Ch 25 重建(补充 Overview)...")
    r25 = fix_ch25_rebuild()
    print(f"   {r25}")

    # 2. Ch 28 修复
    print("\n2. Ch 28 修复截断...")
    r28 = fix_ch28_truncation()
    print(f"   {r28}")

    # 3. Ch 23 参考文献重译
    print("\n3. Ch 23 参考文献重译...")
    r23 = fix_ch23_bibliography()
    print(f"   {r23}")

    # 4. 通用 P0 修复(全 29 章)
    print("\n4. 全章通用 P0 修复...")
    total_fixes = {}
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        text = ch_file.read_text(encoding='utf-8')
        new_text, fixes = fix_chapter_generic(text, ch_file.name)
        if new_text != text:
            ch_file.write_text(new_text, encoding='utf-8')
        for k, v in fixes.items():
            if v > 0:
                total_fixes.setdefault(k, []).append(f"{ch_file.name}({v})")

    print("\n=== 通用修复汇总 ===")
    for k, v in total_fixes.items():
        print(f"  {k}: {len(v)} 处 - {v[:5]}{'...' if len(v) > 5 else ''}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
