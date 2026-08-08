# 第 1 章 `Why Memory: 为什么 Agent 需要 Cognee`

> 本章目标:读完本章,你将能够
> - 说清楚 LLM Agent(智能体)在长期记忆上的三大核心痛点,以及传统 RAG(Retrieval-Augmented Generation,检索增强生成)为什么难以根治。
> - 用一句话解释 cognee 的 ECL 范式:**E**xtract → **C**ognify → **L**oad,并把它和"先切块后检索"的传统 RAG 区分开。
> - 用 BEAM 长上下文基准的两个数字(100K = 0.79,10M = 0.67)证明"图 + 向量 + 关系"这条路线值得做。
> - 画出 cognee 与 Mem0 / Zep / Letta / Graphiti 之间的边界,知道什么场景下应该选谁。

## 前置知识

- 阅读本书前建议先浏览仓库 `<COGNEE_REPO>/README.md` 与 `cognee/skill.md`,建立 cognee 是什么的直觉。
- 需要的基础库:`cognee>=1.4.0`、`pydantic>=2.0`、`asyncio`。
- 环境:Python 3.10–3.14,默认后端栈为 SQLite + LanceDB + Ladybug(零配置即可跑通)。
- 已安装 LLM Provider(OpenAI / Anthropic / Gemini 任选其一),并设置好对应的环境变量。

## 本章导览

- 1.1 Agent 的三大记忆痛点:上下文腐烂、跨会话语义漂移、工具调用冗余。
- 1.2 传统 RAG 的天花板:切片扁平、丢失关系、无法多跳。
- 1.3 cognee 的设计哲学:ECL(Extract → Cognify → Load)。
- 1.4 BEAM 长上下文基准:100K = 0.79,10M = 0.67。
- 1.5 与同类项目的边界:Mem0 / Zep / Letta / Graphiti 的差异化定位。
- 1.6 一个真实的"Agent 失忆"场景演示。

---

## 1.1 Agent 的三大记忆痛点

**为什么:** 一个能跑通单次对话的 LLM 应用,放到真实生产里,几乎都会在第二周开始"失忆"。这不是 bug,而是 LLM 推理栈与人类记忆之间的结构性错配。具体来说,有三个痛点几乎一定会出现。

第一,上下文腐烂(Context Rot)。当一次会话的对话轮次超过 30 轮,或者一次性塞进 50KB 以上的历史,模型对早期信息的召回率就会肉眼可见地下降。这不是 prompt 工程能修的——它来自注意力机制的物理限制。一个直接后果是:Agent 越聊越"糊涂",开始重复提同样的问题、引用早已被否定的方案。

第二,跨会话语义漂移(Cross-Session Semantic Drift)。会话一旦结束,所有上下文就被丢弃。第二天 Agent 重新上线,面对同一个用户,既不知道昨天答应了什么,也不知道用户上次偏好"简洁"。如果把历史塞进 system prompt,会迅速撞到 token 上限;如果不塞,就完全失忆。

第三,工具调用冗余(Tool Call Redundancy)。Agent 为了在多轮里维持"看起来在做事",会反复调用 search_web、read_file、query_db 这些工具,只是为了让上下文里"有东西"。统计上,这类冗余调用常常占总调用的 40% 以上,既烧 token 也烧钱。

**怎么做:** 解决这三个痛点的共同前提,是把"对话里的临时上下文"和"Agent 应该长期记住的事实"分离开。前者留在 prompt 里就好,后者必须落库,变成可被结构化检索的"记忆"。cognee 的整个设计就是围绕这个分离展开的——它提供的是一个面向 Agent 的记忆层,而不是又一个向量数据库。

## 1.2 传统 RAG 的天花板

**为什么:** 既然上下文腐烂,那把所有历史"切片 → 向量化 → 检索"再塞回去,是不是就够了?遗憾的是,这条路有三个绕不开的天花板。

| 维度 | 传统 RAG 的做法 | 实际后果 |
|---|---|---|
| 切片粒度 | 按 token 切固定大小 chunk(Chunk,片段) | "Alice 喜欢 Slack"和"Bob 不喜欢 Slack"会被切成两段孤立向量 |
| 关系建模 | 无显式关系,只有向量距离 | "Alice 是 Bob 的经理"这种关系完全丢失 |
| 多跳推理 | Top-K 段落 → 单次 LLM 调用 | 跨段落的事实串联无法在检索阶段完成 |

这三个天花板直接决定了 RAG 的能力上限:**它能做"找相似",但做不了"找关联"**。在 BEAM 这类需要多会话、多跳推理的基准里,纯 RAG 的得分天花板大致在 0.4–0.5 区间(参见 `<COGNEE_REPO>/cognee/eval_framework/beam/REPORT.md` 附录 D 列出的 `cognee_completion` 策略说明)。

**怎么做:** 唯一被验证能突破这个上限的办法,是让检索层同时持有三种结构化视图:向量(语义相似)、图(实体关系)、关系表(原文出处与时间戳)。cognee 把这三种视图统一在一棵知识图(Knowledge Graph)中,而不是让用户自己拼三个数据库。

![Ch01 — 传统 RAG vs Cognee ECL](../../assets/diagrams/ch01-01-rag-vs-cognee-ecl.svg)

> 关键实现见 `<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py` 第 86–92 行的 docstring,默认 cognify 管线就是把"分类 → 切片 → 实体抽取 → 关系识别 → 图构建 → 摘要"这六步串成一条 DAG(有向无环图)。

---

## 1.3 Cognee 的设计哲学:ECL

**为什么:** cognee 把所有的工作收敛成一个三段式范式——**E**xtract → **C**ognify → **L**oad,简称 **ECL**。这并不是一个花哨的缩写,它对应的是真实工程里的三个不同阶段:把原始数据抽取成结构化对象、把这些对象组织成知识图、把图与向量与关系一起落到存储后端。这三个阶段的产物在 cognee 内部有明确的对齐语义,所以任何后续的检索、记忆强化(memify)、遗忘(forget)操作都可以在同一棵图上做。

这一思想被写进了 cognee 的官方设计哲学文档 `<COGNEE_REPO>/cognee/skill.md`(共 610 行)。摘录其中最核心的一段:

> "Cognee lets agents improve by remembering more useful things, organizing them into searchable graph memory, and reusing successful past work in future runs."

也就是说,cognee 的目标不是"更好的检索",而是"让 Agent 在下一次行动时,能拿到上一次行动留下的全部有效信号"。

**怎么做:** 用 cognee 的 Python API,这个三段式可以浓缩成下面这十行代码:

```python
import asyncio
import cognee
from cognee import SearchType

async def main():
    # E — Extract:摄取原始数据(文本/文件/URL/列表均可)
    await cognee.add(
        "LangChain 是一个 LLM 编排框架,核心抽象是 Chain 与 Agent。",
        dataset_name="agent_kb",
    )

    # C — Cognify:把数据组织成知识图(Knowledge Graph)
    await cognee.cognify(datasets="agent_kb")

    # L — Load:检索(这一步把图、向量、关系三种视图一起拉出来)
    results = await cognee.search(
        query_text="LangChain 的核心抽象是什么?",
        query_type=SearchType.GRAPH_COMPLETION,
        datasets="agent_kb",
    )
    print(results)

asyncio.run(main())
```

> 上述三步走的等效标准示例见 `<COGNEE_REPO>/examples/demos/simple_cognee_example.py>`(该文件使用更高层的 v2 API `remember`/`recall` 包装了同等语义)。SearchType 的全部 18 种枚举定义在 `<COGNEE_REPO>/cognee/modules/search/types/SearchType.py`。

如果你已经在跑一个 Agent 框架,完全可以把 ECL 当作"记忆层"接进去,Agent 本身不需要知道 cognee 的存在:

```python
import asyncio
import cognee
from cognee import SearchType

async def recall_for_agent(user_id: str, question: str):
    # 在调用 LLM 之前,先把"记忆"拿回来
    context = await cognee.search(
        query_text=question,
        query_type=SearchType.GRAPH_COMPLETION,
        datasets=f"user_{user_id}",
        top_k=15,
    )
    return context
```

ECL 的好处在于它是**单向且可回放**的:任何时刻你都可以重跑 `cognify`,在不动原始数据的前提下重建知识图;反过来你也可以用 `memify` 在不重建的前提下增量加固记忆。这是和"切完就塞向量库"的最大区别——后者是不可回放、不可强化、不可遗忘的。

---

## 1.4 BEAM 基准:为什么这个方向值得做

**为什么:** 自卖自夸没意义,需要外部基准。BEAM(Long-context Benchmark for Evaluating Agent Memory)是 2025 年提出的多会话长上下文基准,覆盖信息抽取、多跳推理、知识更新、时序推理、摘要、偏好跟随、弃答、矛盾消解、事件排序、指令跟随十类能力,总分区间 0–1。

cognee 团队在 100K 上下文规模下拿到了 **0.79** 的总分(基于 held-out 会话的固定 hybrid 检索配置),在 10M 规模下拿到了 **0.67** 的探索性分数(基于问题类型路由)。这两个数字写在官方评测报告 `<COGNEE_REPO>/cognee/eval_framework/beam/REPORT.md` 第 9 行的总结句中(同时给出两个数字),以及第 91–92 行的表格汇总(100K=0.79 在第 91 行,10M=0.67 在第 92 行)。

```
"Cognee reached 0.79 on the primary 100K evaluation and 0.67
 in an exploratory 10M scale check."
```

**为什么这两个数字重要?** 因为 BEAM 不只是"找相似",它里面大量题目是跨会话多跳的(例如"上周 Alice 提的那个需求,后来 Bob 是怎么回应的?"),纯 RAG 在这种题目上的得分往往在 0.3–0.5。cognee 在 100K 上 0.79、10M 上 0.67,说明"图 + 向量 + 关系"这条路线在跨会话记忆这个维度上,确实是有可复现收益的。

**怎么做:** 如果你想自己复现这两个数字,可以直接用 cognee 仓库里已经准备好的脚本:

```bash
# 预处理 BEAM 100K 数据集
uv run python -m cognee.eval_framework.beam.preprocessing.preprocess \
  --dataset beam --splits 100K \
  --output-dir temp/beam_preprocessed_documents

# 跑 BEAM 评测 sweep
uv run python -m cognee.eval_framework.beam.eval.run_sweep \
  --split 100K --num-runs 4 \
  --config-json-path cognee/eval_framework/beam/report_artifacts/100k_fixed/beam_hybrid_completion_20_20_qa_v1_config.json
```

> 详细复现流程见 `<COGNEE_REPO>/cognee/eval_framework/beam/REPORT.md` 附录 B 与附录 C。

需要强调的是,0.79 不是"绝对分数",它是 BEAM 这个基准上的得分;不同基准、不同 LLM Provider、不同数据集下,数字会浮动。但方向是清晰的:**当 Agent 需要长期记忆时,把记忆建成图,比建成向量集合,在跨会话场景下显著更优**。

---

## 1.5 与同类项目的边界

**为什么:** 2024–2026 年涌现了一大批 Agent 记忆框架,Mem0、Zep/Graphiti、Letta 都各有拥趸。如果不划清边界,选型就是玄学。下表是 cognee 与这四个最常被对比的项目在五个维度上的差异。

| 维度 | cognee | Mem0 | Zep / Graphiti | Letta |
|---|---|---|---|---|
| 核心数据结构 | 知识图 + 向量 + 关系 | 事实三元组 + 向量 | 时序知识图(temporal KG) | 分层记忆 + 文件系统 |
| 数据摄入范式 | ECL 三段式 | add/update/search | add/search + 时序事件 | core memory + archival |
| 图后端可插拔 | 是(Ladybug / Neo4j / Kuzu) | 否 | 是(Neo4j / FalkorDB) | 否 |
| 检索类型数量 | 18 种 SearchType | 主要 1–2 种 | 时序检索 + Cypher | core + archival |
| 与 LLM 解耦 | 是(LLMGateway) | 部分 | 部分 | 否(绑定特定 LLM) |

**怎么做:** 选型可以按一句话判断:

- 如果你的记忆规模在"百条事实"以内、且不强调跨会话推理 → Mem0 够用。
- 如果你已经在用 Zep 服务端、需要时序事件链 → 继续用 Zep/Graphiti。
- 如果你的 Agent 框架强绑定特定 LLM、记忆是次要能力 → Letta 体验更顺滑。
- **如果你需要"既能多跳、又能时序、又能反馈强化、还能换图后端"** → cognee 是当下唯一同时满足这四条的开源方案。

> 这只是一个高层导航。详细的迁移与互操作方案见 Ch25《跨框架迁移与导出》。完整的功能矩阵见 `<COGNEE_REPO>/CLAUDE.md`。

---

## 1.6 一个真实的"Agent 失忆"场景

**为什么:** 理论讲完,讲一个会让你立刻想试 cognee 的真实故事。某 SaaS 公司的支持 Agent 在 2025 年 11 月连续被客户投诉三次,根因都是同一个——Agent 失忆。

场景如下:客户 Alice 在 11 月 1 日的工单里说她"讨厌电话,所有沟通必须走邮件";11 月 15 日的工单里她又反馈"账单问题请抄送 finance@";11 月 22 日她第三次开新工单,Agent 居然又问她"您希望我们用什么方式联系您?",而且完全没读 11 月 15 日的偏好。

**为什么纯 RAG 修不了:** 即使你把三张工单全部切片并向量化塞进向量库,检索"Alice 的沟通偏好"时,Top-K 命中的很可能只是 11 月 22 日这条(因为它最新、关键词最贴),真正有约束力的"抄送 finance@"这条历史偏好反而被淹没在向量距离里。

**怎么做:** 用 cognee 把三张工单摄取进来后,事实会变成一张知识图:

- Alice(实体)
- ─ 偏好 → "邮件沟通"
- ─ 偏好 → "账单抄送 finance@"
- ─ 工单 → Ticket#001
- ─ 工单 → Ticket#015
- ─ 工单 → Ticket#022

之后任意一次 `cognee.search("Alice 的沟通偏好是什么?", query_type="GRAPH_COMPLETION")`,都会沿着 `Alice → 偏好` 这条边把两条偏好一起带回来。

```python
import asyncio
import cognee
from cognee import SearchType

async def support_agent_recall():
    await cognee.add([
        "Alice 在 11 月 1 日表示:她讨厌电话,所有沟通必须走邮件。",
        "Alice 在 11 月 15 日表示:账单问题请抄送 finance@ 团队。",
        "Alice 在 11 月 22 日再次开单:Agent 重新询问沟通方式。",
    ], dataset_name="support_alice")

    await cognee.cognify(datasets="support_alice")

    # 图检索会同时召回"邮件沟通"和"抄送 finance@"两条偏好
    memory = await cognee.search(
        query_text="Alice 的沟通偏好是什么?",
        query_type=SearchType.GRAPH_COMPLETION,
        datasets="support_alice",
    )
    return memory
```

> 上述模式对应的生产示例见 `<COGNEE_REPO>/examples/guides/agent_memory_quickstart.py`。

这个例子看起来简单,但它就是 cognee 与传统 RAG 在"长期记忆"问题上最本质的差别:**传统 RAG 找的是"相似的字",cognee 找的是"相关的边"**。

---

## 小结

- LLM Agent 的长期记忆有三个绕不开的痛点:上下文腐烂、跨会话语义漂移、工具调用冗余。传统 RAG 修不了,因为它只能找相似、不能找关系。
- cognee 的核心范式是 ECL——**E**xtract → **C**ognify → **L**oad,把"原始数据 → 知识图 → 检索"串成一条可回放、可强化、可遗忘的管线。
- 在 BEAM 长上下文基准上,cognee 在 100K 规模拿到了 0.79、10M 规模拿到了 0.67,这是"图 + 向量 + 关系"路线在跨会话记忆场景下的可复现收益。
- cognee 与 Mem0 / Zep / Letta / Graphiti 不是竞争关系,而是不同尺度的记忆引擎;选型应看"图后端可插拔 / 检索类型数量 / LLM 解耦"三条硬指标。
- 真正的"Agent 失忆"修复,靠的不是更大的 prompt,而是把记忆建成结构化的知识图。

## 实践作业

1. **(基础)** 跑通 `examples/demos/simple_cognee_example.py`,在你的本地机器上用默认栈(SQLite + LanceDB + Ladybug)完成一次 `add → cognify → search`。
2. **(进阶)** 把上面的"Alice 失忆"场景写成完整脚本,再用 `SearchType.RAG_COMPLETION` 跑一次同样的 query,对比两次检索结果——直观感受图检索和向量检索的差异。
3. **(挑战)** 在你的脚本里加入 `memify`:再摄取一条新工单"Alice 在 12 月 5 日补充:周末不要联系",然后跑 `await cognee.memify(dataset="support_alice")`,再查一次偏好,验证记忆被强化而非覆盖。

## 推荐阅读

- [[chapter-02-install-quickstart|第 2 章 安装与五分钟上手]](./chapter-02-install-quickstart.md)
- [[chapter-03-add-cognify-search|第 3 章 Hello World:`add` / `cognify` / `search` 三步走]](./chapter-03-add-cognify-search.md)
- [[chapter-04-core-concepts|第 4 章 核心概念速览:ECL、SearchType、Retriever 三段式]](./chapter-04-core-concepts.md)
- [[chapter-26-evals-beam|第 26 章 评测:BEAM 与 `cognee eval`]](../part-05-production/chapter-26-evals-beam.md)
- 设计哲学原文:`<COGNEE_REPO>/cognee/skill.md`
- BEAM 评测报告:`<COGNEE_REPO>/cognee/eval_framework/beam/REPORT.md`
- 论文:Markovic et al. 2025, *Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning*, arXiv:2505.24478
- 综合示例:`<COGNEE_REPO>/examples/demos/comprehensive_example/cognee_comprehensive_example.py`

## 下一章预告

第 2 章《生态地图:在 AI 记忆赛道上定位 cognee》将把视野从 cognee 单点拉到整个 2024–2026 年的 Agent 记忆赛道,横向对比 Mem0 / Zep / Letta / Graphiti 的设计哲学与适用边界,帮助你做出清醒的选型决策。