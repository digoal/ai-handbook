# 翻译质量审计报告

生成时间: 2026-08-09
审计章节: 29

## 评级分布

| 评级 | 章节数 | 含义 |
|---|---|---|
| A | 0 | 无问题或极轻微 |
| B | 6 | 个别问题,可控 |
| C | 10 | 多处问题,需修复 |
| D | 13 | 严重问题,优先修复 |

## 总问题统计

| 问题类型 | 数量 |
|---|---|
| untranslated_paragraphs | 60 |
| untranslated_headings | 226 |
| forbidden_terms | 41 |
| image_issues | 0 |
| at_a_glance_untranslated | 1 |

## 章节详细评级

| # | 章节 | 字符数 | 中文占比 | 未译段 | 未译标题 | 术语 | 图问题 | 评级 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 提示链 | 8,943 | 54% | 0 | 4 | 2 | 0 | C |
| 2 | 路由 | 18,817 | 13% | 2 | 34 | 0 | 0 | D |
| 3 | 并行化 | 15,904 | 24% | 6 | 14 | 4 | 0 | D |
| 4 | 反思 | 12,868 | 21% | 4 | 11 | 1 | 0 | D |
| 5 | 工具使用(函数调用) | 25,001 | 14% | 0 | 13 | 1 | 0 | C |
| 6 | 规划 | 11,648 | 33% | 1 | 1 | 3 | 0 | C |
| 7 | 多智能体协作 | 18,269 | 24% | 2 | 29 | 3 | 0 | D |
| 8 | 记忆管理 | 24,680 | 22% | 1 | 30 | 0 | 0 | D |
| 9 | 学习与适应 | 8,870 | 48% | 4 | 1 | 2 | 0 | C |
| 10 | 模型上下文协议 | 14,923 | 42% | 0 | 15 | 1 | 0 | D |
| 11 | 目标设定与监控 | 12,362 | 26% | 0 | 4 | 1 | 0 | C |
| 12 | 异常处理与恢复 | 5,918 | 44% | 2 | 1 | 1 | 0 | C |
| 13 | 人在回路 | 7,964 | 48% | 1 | 3 | 0 | 0 | C |
| 14 | 知识检索(RAG) | 15,914 | 36% | 4 | 2 | 0 | 0 | C |
| 15 | 智能体间通信(A2A) | 13,372 | 31% | 5 | 2 | 2 | 0 | D |
| 16 | 资源感知优化 | 15,680 | 27% | 3 | 6 | 2 | 0 | D |
| 17 | 推理技术 | 21,418 | 42% | 9 | 9 | 0 | 0 | D |
| 18 | 护栏/安全模式 | 22,559 | 28% | 1 | 19 | 1 | 0 | D |
| 19 | 评估与监控 | 17,996 | 40% | 0 | 7 | 1 | 0 | C |
| 20 | 优先级排序 | 11,347 | 21% | 0 | 1 | 0 | 0 | B |
| 21 | 探索与发现 | 14,664 | 30% | 5 | 2 | 3 | 0 | D |
| 22 | 高级提示技术 | 25,101 | 56% | 1 | 0 | 1 | 0 | B |
| 23 | AI 智能体交互:从 GUI 到真实世界环境 | 5,334 | 63% | 1 | 0 | 1 | 0 | B |
| 24 | 智能体框架速览 | 7,291 | 40% | 2 | 10 | 1 | 0 | D |
| 25 | 使用 AgentSpace 构建智能体 | 1,368 | 38% | 1 | 0 | 1 | 0 | B |
| 26 | CLI 上的 AI 智能体 | 4,056 | 51% | 1 | 5 | 2 | 0 | C |
| 27 | 深入引擎:智能体推理引擎内部探秘 | 10,280 | 49% | 4 | 1 | 4 | 0 | D |
| 28 | 编程智能体 | 2,543 | 61% | 0 | 2 | 0 | 0 | B |
| 29 | 结语 | 6,025 | 69% | 0 | 0 | 3 | 0 | B |

## P0 严重问题清单(详细)

### 第 1 章 提示链 (Prompt Chaining)

**术语违规 (2)**:
- 第 42 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 44 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

**At a Glance 未翻译 (1)**: 中文占比 < 50%

### 第 2 章 路由 (Routing)

**未译英文段落 (2)**:
- 第 149 行: `You will also need to set up your environment with your API key for the language model you choose (e.g., OpenAI, Google Gemini, Anthropic). As mention...`
- 第 169 行: `The Agent Development Kit (ADK) is a framework for engineering agentic systems, providing a structured environment for defining an agent's capabilitie...`

### 第 3 章 并行化 (Parallelization)

**未译英文段落 (6)**:
- 第 103 行: `Furthermore, a valid API key for the chosen language model must be configured in the local environment for authentication. import os import asyncio fr...`
- 第 116 行: `OPENAI_API_KEY) try: llm: Optional[ChatOpenAI] = ChatOpenAI(model="gpt-4o-mini", temperature=0.7) except Exception as e: print(f"Error initializing la...`
- 第 125 行: `cuted in parallel. summarize_chain: Runnable = ( ChatPromptTemplate.from_messages([ ("system", "Summarize the following topic concisely:"), ("user", "...`
- 第 395 行: `[Google 智能体开发工具包(ADK)文档(多智能体系统)](https://google.github.io/adk-docs/agents/multi-agents/): https://google.github.io/adk-docs/agents/multi-agents/...`
- 第 397 行: `[LangChain 表达式语言(LCEL)文档(并行)](https://python.langchain.com/docs/concepts/lcel/): https://python.langchain.com/docs/concepts/lcel/...`

**术语违规 (4)**:
- 第 1 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 5 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 7 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 63 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 4 章 反思 (Reflection)

**未译英文段落 (4)**:
- 第 33 行: `Repeat until the post meets quality standards. – Benefit: Produces more polished and effective content....`
- 第 77 行: `Reviewing previous turns in a conversation to maintain context, correct mis- understandings, or improve response quality....`
- 第 213 行: `Specifically, the code showcases this by employing a Generator-Critic structure, where one component (the Generator) produces an initial result or pla...`
- 第 252 行: `This code demonstrates the use of a sequential agent pipeline in Google ADK for generating and reviewing text....`

**术语违规 (1)**:
- 第 7 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 5 章 工具使用(函数调用) (Tool Use (Function Calling))

**术语违规 (1)**:
- 第 7 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 6 章 规划 (Planning)

**未译英文段落 (1)**:
- 第 260 行: `Perplexity，Introducing Perplexity Deep Research，https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research...`

**术语违规 (3)**:
- 第 35 行: `计划` → 应改为 `规划` (源术语:Planning)
- 第 39 行: `计划` → 应改为 `规划` (源术语:Planning)
- 第 39 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 7 章 多智能体协作 (Multi-Agent Collaboration)

**未译英文段落 (2)**:
- 第 31 行: `<!-- TRANSLATION_NOTE: 下一块标题"Multi-Agent Collaboration: Exploring Interrelationships and Communication Structures"按术语表规则译为"多智能体协作:探索相互关系与通信结构" -->...`
- 第 411 行: `多智能体系统——协作的力量:https://aravindakumar.medium.com/introducing-multi-agent-frameworks-the-power-of-collaboration-e9db31bba1b6...`

**术语违规 (3)**:
- 第 60 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 86 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 86 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 8 章 记忆管理 (Memory Management)

**未译英文段落 (1)**:
- 第 570 行: `[Vertex AI Agent Engine Memory Bank](https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-memory-bank-in-public-preview)...`

### 第 9 章 学习与适应 (Learning and Adaptation)

**未译英文段落 (4)**:
- 第 82 行: `an initial program, an evaluation file, and a configuration file. The evolve. run(iterations = 1000) line starts the evolutionary process, running for...`
- 第 137 行: `AlphaEvolve blog: https://deepmind.google/discover/blog/alphaevolve-­a-­gemini-­ powered-­coding-­agent-­for-­designing-­advanced-­algorithms/...`
- 第 146 行: `Proximal Policy Optimization Algorithms by John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. You can find it on arXiv: ht...`
- 第 150 行: `Robeyns, M., Aitchison, L., & Szummer, M. (2025). A Self-Improving Coding Agent. arXiv:2504.15228v2: https://arxiv.org/pdf/2504.15228 https://github.c...`

**术语违规 (2)**:
- 第 12 行: `映射` → 应改为 `反思` (源术语:Reflection)
- 第 51 行: `映射` → 应改为 `反思` (源术语:Reflection)

### 第 10 章 模型上下文协议 (Model Context Protocol)

**术语违规 (1)**:
- 第 142 行: `代理` → 应改为 `智能体` (源术语:Agent)

### 第 11 章 目标设定与监控 (Goal Setting and Monitoring)

**术语违规 (1)**:
- 第 109 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 12 章 异常处理与恢复 (Exception Handling and Recovery)

**未译英文段落 (2)**:
- 第 126 行: `O'Neill, V. (2022). Improving Fault Tolerance and Reliability of Heterogeneous Multi-Agent IoT Systems Using Intelligence Transfer. *Electronics*, 11(...`
- 第 128 行: `Shi, Y., Pei, H., Feng, L., Zhang, Y., & Yao, D. (2024). Towards Fault Tolerance in Multi-Agent Reinforcement Learning. *arXiv* preprint arXiv:2412.00...`

**术语违规 (1)**:
- 第 25 行: `代理` → 应改为 `智能体` (源术语:Agent)

### 第 13 章 人在回路 (Human-in-the-Loop)

**未译英文段落 (1)**:
- 第 156 行: `A Survey of Human-in-the-loop for Machine Learning, Xingjiao Wu, Luwei Xiao, Yixuan Sun, Junhang Zhang, Tianlong Ma, Liang He: https://arxiv.org/abs/2...`

### 第 14 章 知识检索(RAG) (Knowledge Retrieval (RAG))

**未译英文段落 (4)**:
- 第 307 行: `Google AI for Developers Documentation. Retrieval Augmented Generation - https:// cloud.google.com/vertex-­ai/generative-­ai/docs/rag-­engine/rag-­ove...`
- 第 310 行: `Google Cloud Vertex AI RAG Corpus https://cloud.google.com/vertex-­ai/genera- tive-­ai/docs/rag-­engine/manage-­your-­rag-­corpus#corpus-­management...`
- 第 313 行: `LangChain and LangGraph: Leonie Monigatti, "Retrieval-Augmented Generation (RAG): From Theory to LangChain Implementation," https://medium.com/data-­ ...`
- 第 318 行: `Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. https://arxiv.org/abs/2005.11401...`

### 第 15 章 智能体间通信(A2A) (Inter-Agent Communication (A2A))

**未译英文段落 (5)**:
- 第 182 行: `让我们考察智能体到智能体(A2A)协议的实际应用。仓库 https://github.com/google-a2a/a2a-samples/tree/main/samples 提供了 Java、Go 和 Python 示例,展示了 LangGraph、CrewAI、Azure AI Foundry ...`
- 第 326 行: `Chen, B. (2025, April 22). How to Build Your First Google A2A Project: A Step-by-­Step Tutorial. Trickle.so Blog. https://www.trickle.so/blog/how-­to-...`
- 第 328 行: `Communication between different AI frameworks such as LangGraph, CrewAI, and Google ADK https://www.trickle.so/blog/how-­to-­build-­google-­a2a-­proje...`
- 第 330 行: `Designing Collaborative Multi-Agent Systems with the A2A Protocol https://www.oreilly.com/radar/designing-­collaborative-­multi-­agent-­systems-­with-...`
- 第 334 行: `Getting Started with Agent-to-Agent (A2A) Protocol: https://codelabs.developers.google.com/intro-­a2a-­purchasing-­concierge#0...`

**术语违规 (2)**:
- 第 31 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 13 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 16 章 资源感知优化 (Resource-Aware Optimization)

**未译英文段落 (3)**:
- 第 13 行: `Built-in evaluation fea- tures allow systematic assessment of agent performance, which can be used for system refinement (see Chap. 19). Next, two age...`
- 第 121 行: `代码采用 MIT 许可证,可在 GitHub 上获取:(https://github.com/mahtabsyed/21-Agentic-Patterns/blob/main/16_Resource_Aware_Opt_LLM_Reflection_v2.ipynb)。...`
- 第 309 行: `OpenRouter offers a detailed leaderboard (https://openrouter.ai/rankings) which ranks available AI models based on their cumulative token production. ...`

**术语违规 (2)**:
- 第 89 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 108 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 17 章 推理技术 (Reasoning Techniques)

**未译英文段落 (9)**:
- 第 61 行: `Classical computers use bits (0 or 1), processing information sequentially. Quantum computers use qubits, which can be 0, 1, or both simultaneously (s...`
- 第 71 行: `Classical computers process information using bits, which can be either a 0 or a 1 at any given time, performing operations sequentially. In contrast,...`
- 第 75 行: `<!-- TRANSLATION_NOTE: 上下文连贯处理。"Tree-of-Thought" 按术语表译为"思维树",原文使用 Tree-of-Thought 而非标准 Tree of Thoughts,翻译时按上下文保留。-->...`
- 第 212 行: `This allows the model to evolve its problem-solving abilities without direct human supervision. Ultimately, these reasoning models don't just produce ...`
- 第 323 行: `application 利用了 React 与 Vite、Tailwind CSS、Shadcn UI、LangGraph 以及 Google Gemini。该项目遵循 Apache 2.0 许可证(图 17.7)。...`

### 第 18 章 护栏/安全模式 (Guardrails/Safety Patterns)

**未译英文段落 (1)**:
- 第 446 行: `fields like finance, healthcare, or legal research. Use them to enforce ethical guidelines, prevent the spread of misinformation, protect brand safety...`

**术语违规 (1)**:
- 第 164 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 19 章 评估与监控 (Evaluation and Monitoring)

**术语违规 (1)**:
- 第 13 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 21 章 探索与发现 (Exploration and Discovery)

**未译英文段落 (5)**:
- 第 70 行: `This involves synthesizing findings from the experimentation phase with insights from the literature review, structuring the document according to aca...`
- 第 74 行: `The modular architecture of Agent Laboratory ensures computational flexibility. The aim is to enhance research productivity by automating tasks while ...`
- 第 78 行: `While a comprehensive code analysis is beyond the scope of this book, I want to provide you with some key insights and encourage you to delve into the...`
- 第 234 行: `"You are a software engineer directing a machine learning engineer, where the machine learning engineer will be writing the code, and you can interact...`
- 第 239 行: `"You are a machine learning engineer being directed by a PhD student who will help you write the code, and you can interact with them through dialogue...`

**术语违规 (3)**:
- 第 56 行: `计划` → 应改为 `规划` (源术语:Planning)
- 第 166 行: `计划` → 应改为 `规划` (源术语:Planning)
- 第 56 行: `防护` → 应改为 `护栏` (源术语:Guardrails)

### 第 22 章 高级提示技术 (Advanced Prompting Techniques)

**未译英文段落 (1)**:
- 第 25 行: `有效的动词包括：Act(行动)、Analyze(分析)、Categorize(分类)、Classify(归类)、Contrast(对比)、Compare(比较)、Create(创建)、Describe(描述)、Define(定义)、Evaluate(评估)、Extract(提取)、Find(查找)、...`

**术语违规 (1)**:
- 第 156 行: `映射` → 应改为 `反思` (源术语:Reflection)

### 第 23 章 AI 智能体交互:从 GUI 到真实世界环境 (AI Agentic Interactions: From GUI to Real World Environment)

**未译英文段落 (1)**:
- 第 67 行: `参考文献 Anthropic Computer use: https://docs.anthropic.com/en/docs/build-with-claude/computer-use Browser Use: https://docs.browser-use.com/introduction ...`

**术语违规 (1)**:
- 第 28 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 24 章 智能体框架速览 (A Quick Overview of Agentic Frameworks)

**未译英文段落 (2)**:
- 第 92 行: `Its main purpose is to simultaneously generate a joke, a story, and a poem about a given topic and then combine them into a single, formatted text out...`
- 第 160 行: `Crew.AI, https://docs.crewai.com/en/introduction Google's ADK, https://google.github.io/adk-docs/ LangChain, https://www.langchain.com/ LangGraph, htt...`

**术语违规 (1)**:
- 第 27 行: `并行` → 应改为 `并行化` (源术语:Parallelization)

### 第 25 章 使用 AgentSpace 构建智能体 (Building an Agent with AgentSpace)

**未译英文段落 (1)**:
- 第 37 行: `Create a no-code agent with Agent Designer, https://cloud.google.com/agentspace/ agentspace-­enterprise/docs/agent-­designer Google Cloud Skills Boost...`

**术语违规 (1)**:
- 第 31 行: `映射` → 应改为 `反思` (源术语:Reflection)

### 第 26 章 CLI 上的 AI 智能体 (AI Agents on the CLI)

**未译英文段落 (1)**:
- 第 38 行: `"Please go through all Python files, update the import statements and any deprecated function calls to be compatible with the latest version, and then...`

**术语违规 (2)**:
- 第 54 行: `并行` → 应改为 `并行化` (源术语:Parallelization)
- 第 54 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 27 章 深入引擎:智能体推理引擎内部探秘 (Under the Hood: An Inside Look at the Agents' Reasoning Engines)

**未译英文段落 (4)**:
- 第 132 行: `For "reasoning," I retrieve associations with logic, problem-solving, and cognitive processes. Since this is a meta-question about my own process, I f...`
- 第 170 行: `ent sequences words and sentences to maximize clarity and relevance. I draw on patterns from my training to mimic human-like reasoning, such as breaki...`
- 第 249 行: `3² = 9 (memorized) 3³ = 27 (retrieved) 4² = 16 (memorized) 4³ = 64 (retrieved) Compute remaining term 3⁴ = 3³·3 = 27×3 = 81....`
- 第 264 行: `10. Plan response structure – Restate the question. – Show the computed values. – State the conclusion. Surface realization “3⁴ is 81 and 4³ is 64, so...`

**术语违规 (4)**:
- 第 121 行: `映射` → 应改为 `反思` (源术语:Reflection)
- 第 215 行: `映射` → 应改为 `反思` (源术语:Reflection)
- 第 216 行: `映射` → 应改为 `反思` (源术语:Reflection)
- 第 9 行: `计划` → 应改为 `规划` (源术语:Planning)

### 第 29 章 结语 (Conclusion)

**术语违规 (3)**:
- 第 21 行: `计划` → 应改为 `规划` (源术语:Planning)
- 第 21 行: `计划` → 应改为 `规划` (源术语:Planning)
- 第 23 行: `计划` → 应改为 `规划` (源术语:Planning)
