# 术语表

> 本术语表为本书统一用语。出现冲突时,以本表为准。所有术语首次出现在章节中时,均采用"中文(English)"的标注方式。

## A

| 术语 | 中文 | 说明 |
|---|---|---|
| Add | 摄取 | 数据写入,通常对应 `cognee.add()` |
| Agent | 智能体 | LLM 驱动的自主决策单元 |
| Agent Memory | 智能体记忆 | `cognee.modules.agent_memory` 提供的子代理级记忆 API |
| AGENTS.md | 项目治理文档 | cognee 主仓库的开发者指南(130 行) |
| API Key | 接口密钥 | 访问 cognee 服务端的认证凭证 |
| Assistant | 助手 | 与 Agent 同义,本书统一用"Agent" |
| Aider | 终端编码 Agent | 一款命令行的 AI 编码工具 |
| Alembic | SQLAlchemy 迁移工具 | cognee 用它管理关系库 schema 演化 |

## B

| 术语 | 中文 | 说明 |
|---|---|---|
| BEAM | 长上下文基准 | `cognee/eval_framework/beam/`,100K=0.79,10M=0.67 |
| BoundTask | 已绑定的任务 | 新式 pipeline API 的核心抽象 |
| Bucket | 桶 | 默认 backend 配置中的存储分区概念 |

## C

| 术语 | 中文 | 说明 |
|---|---|---|
| Chunk | 片段 | 文档切分后的语义单元 |
| Chunking | 分块 | 将文档切成 chunk 的过程 |
| Classify | 分类 | cognify pipeline 的第一步,识别文档类型 |
| Claude Agent SDK | Claude Agent SDK | Anthropic 官方的 Agent 开发 SDK |
| Claude Code | Claude Code CLI | Anthropic 官方的 CLI 编码工具 |
| CLI | 命令行 | `cognee-cli` |
| Cognify | 认知化 | v1 API 核心动作,从原始数据构建知识图 |
| Codex CLI | Codex CLI | OpenAI 的终端编码 Agent |
| Code Rule | 代码规则 | `CODING_RULES` 检索类型返回的程序性约束 |
| ContextVar | 上下文变量 | Python `contextvars` 库,cognee 用它支持 dataset 嵌套调用 |
| Cosmos DB | Cosmos DB | 微软的分布式数据库,可选图后端 |
| CrewAI | CrewAI | 多 Agent 编排框架 |
| Cypher | Cypher 查询 | Neo4j 的图查询语言 |

## D

| 术语 | 中文 | 说明 |
|---|---|---|
| Dataset | 数据集 | cognee 权限/隔离的基本单位 |
| DataPoint | 数据点 | cognee 图领域对象基类(继承自 Pydantic) |
| DCO | 开发者原创证书 | cognee 贡献要求签署 |
| Dify | Dify | 开源 LLM 应用平台 |
| DLT | data load tool | 关系库/SaaS 数据摄取工具 |
| Docker Compose | Docker Compose | 多容器编排配置 |
| DuckDB | DuckDB | 进程内 OLAP 数据库 |

## E

| 术语 | 中文 | 说明 |
|---|---|---|
| ECL | 提取-认知化-加载 | Extract → Cognify → Load,cognee 的核心流水线范式 |
| Embedding | 向量化 | 把文本转为稠密向量 |
| Entity | 实体 | 图节点的一种,代表概念 |
| EntityType | 实体类型 | 实体的类别 |
| Eval | 评测 | 衡量检索/生成质量的体系 |
| Export | 导出 | `cognee.export()` 反向把图导出到文件 |
| Extract | 提取 | ECL 的第一步 |

## F

| 术语 | 中文 | 说明 |
|---|---|---|
| FAISS | FAISS | Facebook 的向量检索库(可选后端) |
| Feedback | 反馈 | `FeedbackEntry`,影响后续检索权重 |
| Forget | 遗忘 | v2 API:`cognee.forget()`,对应 GDPR 被遗忘权 |
| Forgetting | 遗忘机制 | 删除指定 dataset / data 的操作 |

## G

| 术语 | 中文 | 说明 |
|---|---|---|
| Gemini | Gemini | Google 的 LLM,通过 LiteLLM 接入 |
| Global Context Index | 全局上下文索引 | 跨 dataset 的统一上下文视图,由 memify pipeline 构建 |
| Graph | 图 | 知识图谱,本书记"知识图"或直接用"graph" |
| Graphiti | Graphiti | Zep 的图记忆后端,与 cognee 通过 migration 互通 |
| Graph DB | 图数据库 | 存储知识图的数据库 |

## H

| 术语 | 中文 | 说明 |
|---|---|---|
| Hermes | Hermes Agent | cognee 集成的智能体框架之一 |
| Hook | 钩子 | Claude Code / Vellum 的生命周期回调 |
| Host Session | 主会话 | Claude Code 的顶级会话 ID |

## I

| 术语 | 中文 | 说明 |
|---|---|---|
| Identity Field | 身份字段 | DataPoint 的稳定 ID 派生字段 |
| Improve | 强化 | v2 API:`cognee.improve()`,把反馈写回图 |
| Index Fields | 索引字段 | 需要向量化的字段 |
| Ingestion | 摄取 | 数据写入过程 |
| Integration | 集成 | cognee 与其他系统的桥接包 |
| Inventory | 清单 | `inventory.yml`,cognee-integrations 的注册中心 |

## J

| 术语 | 中文 | 说明 |
|---|---|---|
| JSON Schema | JSON 模式 | Pydantic 模型导出的结构化约束 |

## K

| 术语 | 中文 | 说明 |
|---|---|---|
| Kuzu | Kuzu | 一种嵌入式图数据库 |
| Knowledge Graph | 知识图 | 由实体和关系组成的语义网络 |

## L

| 术语 | 中文 | 说明 |
|---|---|---|
| Ladybug | Ladybug | cognee 默认本地图数据库(Kuzu 的官方 fork) |
| LangChain | LangChain | LLM 应用编排框架(对比项) |
| LangGraph | LangGraph | LangChain 的图编排子库 |
| LanceDB | LanceDB | cognee 默认向量数据库 |
| Langfuse | Langfuse | 开源 LLM 可观测平台 |
| Letta | Letta | Agent 记忆框架(对比项) |
| LLM | 大语言模型 | |
| LM Studio | LM Studio | 本地模型推理工具(类似 Ollama) |
| Load | 加载 | ECL 的第三步,数据落到存储后端 |
| Low-Level API | 底层 API | `cognee.low_level` 模块的细粒度函数 |

## M

| 术语 | 中文 | 说明 |
|---|---|---|
| Marketplace | 市场 | Claude Code / Codex / Vellum 的插件市场 |
| MCP | 模型上下文协议 | Model Context Protocol,Anthropic 提出的 Agent ↔ 工具协议 |
| Memify | 记忆化 | cognee 自适应巩固记忆的过程 |
| Memify Pipeline | 记忆化管道 | `cognee/memify_pipelines/` 中的预定义流程 |
| Memory Entry | 记忆条目 | `cognee/memory/entries.py` 的基类 |
| MemoryEntry | MemoryEntry | cognee 内存 API 的条目类型 |
| Migration | 迁移 | 把数据从其他框架迁入/迁出 cognee |
| Mistral | Mistral | 一种开源 LLM |
| Multi-Tenancy | 多租户 | 多用户/多租户的数据隔离 |

## N

| 术语 | 中文 | 说明 |
|---|---|---|
| n8n | n8n | 开源工作流自动化平台 |
| Namespace | 命名空间 | Identity Field 的 UUID5 命名空间 |
| NetworkX | NetworkX | Python 图算法库 |
| Node | 节点 | 图节点,分 LLM 输出节点与持久化节点 |
| NodeSet | 节点集 | 轻量标签,用于 dataset 内分组 |
| Notebook | 笔记本 | Jupyter Notebook |

## O

| 术语 | 中文 | 说明 |
|---|---|---|
| Ollama | Ollama | 本地 LLM 推理工具 |
| Ontology | 本体 | 领域词汇与关系的形式化定义(OWL) |
| Ontology Resolver | 本体解析器 | cognee 中加载本体并约束抽取的模块 |
| OpenAI | OpenAI | LLM 提供商 |
| OpenClaw | OpenClaw | cognee 集成的多作用域 Agent 框架 |
| OpenTelemetry | OpenTelemetry | 分布式追踪标准 |
| OpenAPI | OpenAPI | REST API 规范 |
| OWLS | 本体语言 | Web Ontology Language |

## P

| 术语 | 中文 | 说明 |
|---|---|---|
| Permission | 权限 | cognee 多租户访问控制 |
| PGVector | PGVector | Postgres 的向量扩展 |
| Pipeline | 管道 | cognee 任务编排的基本单位 |
| Pipeline Run | 管道运行 | 一次管道执行的实例 |
| Plan Mode | 计划模式 | Claude Code 的只读交互模式 |
| Postgres | Postgres | PostgreSQL 关系数据库 |
| Provenance | 溯源 | 记忆来自哪个 source 的元数据 |
| Provider | 提供商 | LLM / 存储后端的供应商适配器 |
| Prune | 剪枝 | `cognee.prune()`,反向清理记忆 |

## Q

| 术语 | 中文 | 说明 |
|---|---|---|
| QA | 问答 | Question-Answer |
| QAEntry | QAEntry | `cognee/memory/entries.py` 中的问答条目类型 |
| Qdrant | Qdrant | 一种向量数据库 |

## R

| 术语 | 中文 | 说明 |
|---|---|---|
| RAG | 检索增强生成 | Retrieval-Augmented Generation |
| Recall | 回忆 | v2 API:`cognee.recall()` |
| Recall Response | 回忆响应 | `RecallResponse`,判别联合类型 |
| Remember | 记忆 | v2 API:`cognee.remember()` |
| Repository | 仓库 | 代码仓库 |
| Retriever | 检索器 | cognee 19 个检索实现 |
| Rerank | 重排 | 对检索结果二次排序 |
| RUFF | Ruff | Python linter 与 formatter |

## S

| 术语 | 中文 | 说明 |
|---|---|---|
| Sandbox | 沙箱 | 隔离运行环境 |
| Search | 搜索 | v1 API:`cognee.search()` |
| Search Type | 检索类型 | `SearchType`,18 种 |
| Serve | 服务 | 启动 cognee API server |
| Session | 会话 | 一次连续交互的上下文 |
| Session Distillation | 会话蒸馏 | 把短期 session 提炼为长期记忆 |
| Skill | 技能 | 程序性记忆单元 |
| Skill Run | 技能运行 | `SkillRunEntry` |
| Skill Set | 技能集 | 一组相关 skill |
| Skill Sync | 技能同步 | session → graph 的固化 |
| Slack | Slack | 团队聊天工具 |
| SQLite | SQLite | 嵌入式关系数据库,cognee 默认 |
| Starter Kit | 入门工具包 | `cognee-starter-kit` |
| Strands | Strands | AWS 的 Agent SDK |
| Structured Output | 结构化输出 | LLM 返回符合 Pydantic 模型的 JSON |
| Subprocess Mode | 子进程模式 | 图/向量库运行在独立子进程(cognee 默认) |
| Sync | 同步 | dataset 间同步 / push 到云 |

## T

| 术语 | 中文 | 说明 |
|---|---|---|
| Task | 任务 | pipeline 的基本执行单元 |
| Task Concurrency | 任务并发数 | pipeline 的并行度上限 |
| Telegram | Telegram | 即时通讯工具 |
| Temporal | 时序 | 时间感知的检索类型 |
| Text Chunker | 文本分块器 | 默认 chunker,基于 token 数 |
| Tokenizer | 分词器 | tiktoken / Gemini tokenizer 等 |
| Tool | 工具 | Agent 可调用的函数 |
| Top-K | Top-K | 检索返回的最大结果数 |
| Trace | 追踪 | `TraceEntry`,Agent 执行轨迹 |
| Truth Subspace | 真值子空间 | 可解释子图查询 |

## U

| 术语 | 中文 | 说明 |
|---|---|---|
| Update | 更新 | v1 API:`cognee.update()`,覆盖已有 data |
| Upload | 上传 | 摄取数据的一种方式 |
| Use Case | 场景 | 用户故事 |
| UUID5 | UUID v5 | 基于命名空间的稳定 UUID |

## V

| 术语 | 中文 | 说明 |
|---|---|---|
| Vellum | Vellum | 文档处理平台(集成方) |
| Vector DB | 向量数据库 | 存储 embedding 的数据库 |
| Visualize | 可视化 | `cognee.visualize_graph()` 等 |
| VS Code | VS Code | Microsoft 的代码编辑器 |

## W

| 术语 | 中文 | 说明 |
|---|---|---|
| WAL | 预写日志 | Write-Ahead Log,Ladybug 用于持久化 |
| Weaviate | Weaviate | 一种向量数据库 |
| Web Widget | Web 组件 | 嵌入式聊天窗口 |

## Z

| 术语 | 中文 | 说明 |
|---|---|---|
| Zep | Zep | Agent 记忆平台(对比项) |
| zep/Graphiti | Zep/Graphiti | Zep 的图记忆后端 |