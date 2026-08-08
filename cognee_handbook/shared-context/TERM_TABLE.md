# 共享术语表(给所有写作子 Agent)

> 完整版见 `../GLOSSARY.md`。这里只保留最常被引用、易出错的 30 条。

## API 名(保留英文不译)

- `add`, `cognify`, `search`, `delete`, `memify`, `update`, `prune`, `config`, `datasets`, `agents`
- `remember`, `recall`, `improve`, `forget`, `serve`, `disconnect`, `push`, `export`
- `enable_tracing`, `get_last_trace`, `clear_traces`
- `start_ui`, `visualize_graph`, `start_visualization_server`
- `run_custom_pipeline`

## 动作用词统一

| 英文 | 中文动词 | 中文名词 |
|---|---|---|
| cognify | 认知化 | 认知化动作 |
| memify | 记忆化 | 记忆化管道 |
| remember | 记忆 | 记忆条目 |
| recall | 回忆 | 召回结果 |
| improve | 强化 | 强化操作 |
| forget | 遗忘 | 遗忘操作 |
| add | 摄取 | 摄取动作 |
| prune | 剪枝 | 剪枝操作 |
| ingest | 摄取 | 摄取管道 |

## 核心实体(保留英文 + 中文)

- **Entity**:实体(继承自 DataPoint)
- **Edge**:关系(注意区分 LLM 输出的 Edge 与持久化的 Edge)
- **Chunk**:片段
- **Document**:文档
- **DataPoint**:数据点(基类)
- **NodeSet**:节点集(轻量标签)
- **Node**:节点(图节点)
- **KnowledgeGraph**:知识图
- **MemoryEntry**:记忆条目
- **MemoryEntry 子类**:`QAEntry` / `TraceEntry` / `FeedbackEntry` / `SkillRunEntry`
- **Skill**:技能(程序性记忆单元)
- **Dataset**:数据集
- **Pipeline**:管道
- **Task**:任务
- **PipelineRun / TaskRun / DataItemStatus**:执行日志模型

## 检索类型(英文保留 + 中文)

| SearchType 枚举 | 中文 | 一句话用途 |
|---|---|---|
| `CHUNKS` | 片段检索 | 返回原始 chunk 列表 |
| `CHUNKS_LEXICAL` | 词法片段检索 | 基于词法的 chunk 检索 |
| `SUMMARIES` | 摘要检索 | 返回 summary 节点 |
| `RAG_COMPLETION` | RAG 补全 | 经典 RAG,向量检索 + LLM |
| `HYBRID_COMPLETION` | 混合补全 | 向量 + 图混合 |
| `TRIPLET_COMPLETION` | 三元组补全 | 实体-关系-实体三元组 |
| `GRAPH_COMPLETION` | 图补全 | 图遍历 + LLM |
| `GRAPH_COMPLETION_COT` | 图补全思维链 | 带 CoT 的图补全 |
| `GRAPH_COMPLETION_DECOMPOSITION` | 图补全分解 | 子查询分解 |
| `GRAPH_COMPLETION_CONTEXT_EXTENSION` | 图补全上下文扩展 | 上下文窗口扩展 |
| `GRAPH_SUMMARY_COMPLETION` | 图摘要补全 | 基于 summary 的图补全 |
| `CYPHER` | Cypher 检索 | 直接返回 Cypher 查询结果 |
| `NATURAL_LANGUAGE` | 自然语言 Cypher | NL → Cypher |
| `TEMPORAL` | 时序检索 | 时间感知 |
| `FEELING_LUCKY` | 自动选型 | 让 cognee 决定 SearchType |
| `CODING_RULES` | 代码规则检索 | 程序性约束 |
| `CODE` | 代码检索 | 源代码上下文 |
| `AGENTIC_COMPLETION` | Agent 补全 | 多轮推理,可挂 skill/tool |

## 默认栈(常被引用,务必一致)

- **关系库**:SQLite(`cognee/infrastructure/databases/relational/`)
- **向量库**:LanceDB(`cognee/infrastructure/databases/vector/lancedb/`)
- **图数据库**:Ladybug(`cognee/infrastructure/databases/graph/ladybug/`)
- **可全部换为**:Postgres(`cognee/infrastructure/databases/hybrid/postgres/`)+ PGVector + pgvector

## 集成(常被引用)

- **Claude Code 插件**:`<COGNEE_INTEGRATIONS_REPO>/integrations/claude-code/`
- **Claude Agent SDK**:`<COGNEE_INTEGRATIONS_REPO>/integrations/claude-agent-sdk/`
- **独立 MCP Server**:`<COGNEE_REPO>/cognee-mcp/`

## 版本号

- cognee: **1.4.0**(基线 2026-07-26)
- Python: **>=3.10, <3.15**

## 禁止词(不要使用)

- "传统的 episodic/semantic/procedural 三层"——cognee 实际是短期/长期/程序性/巩固四层
- "Emergence Cognition Loop"——ECL = Extract → Cognify → Load
- 把 `cognee.search(query, query_type=...)` 写成 `cognee.search(query, search_type=...)` ——实际参数名是 `query_type`(v1)