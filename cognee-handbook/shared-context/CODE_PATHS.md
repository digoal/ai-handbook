# 共享代码路径索引(给所有写作子 Agent)

> 所有路径均为绝对路径,在 Phase 1 探索中已全部验证存在。
> 引用时直接复制,不要自己推导或猜测。

## 顶层入口

```
<COGNEE_REPO>/
├── README.md                     主 README,1.0 API 介绍
├── CLAUDE.md                     605 行开发者指南(章节级描述最完整)
├── AGENTS.md                     130 行精简版
├── CONTRIBUTING.md
├── pyproject.toml                version = "1.4.0"
├── docker-compose.yml
├── SESSION_POSTGRES_CACHE_PLAN.md
└── cognee/                       核心 Python 包
```

## cognee/ 顶层

```
<COGNEE_REPO>/cognee/
├── __init__.py                   导出所有公共 API(V1 + V2)
├── __main__.py
├── version.py                    get_cognee_version()
├── base_config.py
├── skill.md                      610 行设计哲学(必读)
├── CLAUDE.md                     605 行开发者指南
├── low_level.py                  细粒度函数
├── pipelines/                    新式 pipeline API
├── memify_pipelines/             memify 预定义管道
├── memory/                       MemoryEntry 定义
│   └── entries.py                QAEntry / TraceEntry / FeedbackEntry / SkillRunEntry
├── modules/                      领域模块(agent_memory / cognify / search / ...)
├── infrastructure/               基础设施(databases / llm / engine / ...)
├── tasks/                        任务实现(ingestion / documents / chunks / graph / ...)
├── api/v1/                       v1 + v2 API 实现
├── cli/                          CLI 入口与子命令
├── alembic/                      关系库迁移
├── shared/                       通用工具(data_models 等)
├── migration/                    跨框架迁移源
├── eval_framework/               BEAM 等评测框架
└── modules/visualization/        图谱可视化
```

## API 实现路径

| API | 路径 |
|---|---|
| `cognee.add` | `<COGNEE_REPO>/cognee/api/v1/add/add.py` |
| `cognee.cognify` | `<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py` |
| `cognee.search` | `<COGNEE_REPO>/cognee/api/v1/search/search.py` |
| `cognee.remember` | `<COGNEE_REPO>/cognee/api/v1/remember/remember.py` |
| `cognee.recall` | `<COGNEE_REPO>/cognee/api/v1/recall/recall.py` |
| `cognee.improve` | `<COGNEE_REPO>/cognee/api/v1/improve/improve.py` |
| `cognee.forget` | `<COGNEE_REPO>/cognee/api/v1/forget/forget.py` |
| `cognee.memify` | `<COGNEE_REPO>/cognee/modules/memify/memify.py` |
| `cognee.delete` | `<COGNEE_REPO>/cognee/api/v1/delete/delete.py` |
| `cognee.update` | `<COGNEE_REPO>/cognee/api/v1/update/update.py` |
| `cognee.prune` | `<COGNEE_REPO>/cognee/api/v1/prune.py` |
| `cognee.config` | `<COGNEE_REPO>/cognee/api/v1/config/config.py` |
| `cognee.datasets` | `<COGNEE_REPO>/cognee/api/v1/datasets/datasets.py` |
| `cognee.agents` | `<COGNEE_REPO>/cognee/api/v1/agents/agents.py` |
| `cognee.visualize_graph` | `<COGNEE_REPO>/cognee/api/v1/visualize.py` |
| `cognee.start_ui` | `<COGNEE_REPO>/cognee/api/v1/ui.py` |
| `cognee.run_custom_pipeline` | `<COGNEE_REPO>/cognee/modules/run_custom_pipeline.py` |
| `cognee.agent_memory` | `<COGNEE_REPO>/cognee/modules/agent_memory/` |

## 核心模型路径

| 模型 | 路径 |
|---|---|
| DataPoint 基类 | `<COGNEE_REPO>/cognee/infrastructure/engine/models/DataPoint.py` |
| Edge | `<COGNEE_REPO>/cognee/infrastructure/engine/models/Edge.py` |
| Entity | `<COGNEE_REPO>/cognee/modules/engine/models/Entity.py` |
| EntityType | `<COGNEE_REPO>/cognee/modules/engine/models/EntityType.py` |
| NodeSet | `<COGNEE_REPO>/cognee/modules/engine/models/node_set.py` |
| Skill | `<COGNEE_REPO>/cognee/modules/engine/models/Skill.py` |
| 持久化 Node | `<COGNEE_REPO>/cognee/modules/graph/models/Node.py` |
| 持久化 Edge | `<COGNEE_REPO>/cognee/modules/graph/models/Edge.py` |
| Dataset | `<COGNEE_REPO>/cognee/modules/data/models/Dataset.py` |
| PipelineRun | `<COGNEE_REPO>/cognee/modules/pipelines/models/PipelineRun.py` |
| LLM 输出 Node/Edge | `<COGNEE_REPO>/cognee/shared/data_models.py` |
| SearchType | `<COGNEE_REPO>/cognee/modules/search/types/SearchType.py` |

## Pipeline 与 Task 路径

| 概念 | 路径 |
|---|---|
| Task 抽象 | `<COGNEE_REPO>/cognee/modules/pipelines/tasks/task.py` |
| 经典 run_pipeline | `<COGNEE_REPO>/cognee/modules/pipelines/operations/pipeline.py` |
| 新式 BoundTask API | `<COGNEE_REPO>/cognee/modules/pipelines/operations/run_pipeline.py` |
| run_tasks 底层 | `<COGNEE_REPO>/cognee/modules/pipelines/operations/run_tasks_base.py` |
| validate_pipeline_tasks | `<COGNEE_REPO>/cognee/modules/pipelines/operations/validate_pipeline_tasks.py` |

## Cognify 默认 pipeline 任务路径

| 任务 | 路径 |
|---|---|
| classify_documents | `<COGNEE_REPO>/cognee/tasks/documents/classify_documents.py` |
| extract_chunks_from_documents | `<COGNEE_REPO>/cognee/tasks/documents/extract_chunks_from_documents.py` |
| extract_graph_and_summarize | `<COGNEE_REPO>/cognee/tasks/graph/extract_graph_and_summarize.py` |
| extract_graph_from_data | `<COGNEE_REPO>/cognee/tasks/graph/extract_graph_from_data.py` |
| add_data_points | `<COGNEE_REPO>/cognee/tasks/storage/add_data_points.py` |
| index_data_points | `<COGNEE_REPO>/cognee/tasks/storage/index_data_points.py` |
| index_graph_edges | `<COGNEE_REPO>/cognee/tasks/storage/index_graph_edges.py` |
| extract_dlt_fk_edges | `<COGNEE_REPO>/cognee/tasks/ingestion/extract_dlt_fk_edges.py` |
| resolve_data_directories | `<COGNEE_REPO>/cognee/tasks/ingestion/resolve_data_directories.py` |
| ingest_data | `<COGNEE_REPO>/cognee/tasks/ingestion/ingest_data.py` |
| extract_events_and_timestamps | `<COGNEE_REPO>/cognee/tasks/temporal_graph/extract_events_and_entities.py` |

## 检索器路径

| Retriever | 路径 |
|---|---|
| BaseRetriever(三段式) | `<COGNEE_REPO>/cognee/modules/retrieval/base_retriever.py` |
| Chunks | `<COGNEE_REPO>/cognee/modules/retrieval/chunks_retriever.py` |
| Summaries | `<COGNEE_REPO>/cognee/modules/retrieval/summaries_retriever.py` |
| Graph Completion | `<COGNEE_REPO>/cognee/modules/retrieval/graph_completion_retriever.py` |
| Graph Summary Completion | `<COGNEE_REPO>/cognee/modules/retrieval/graph_summary_completion_retriever.py` |
| Graph Completion CoT | `<COGNEE_REPO>/cognee/modules/retrieval/graph_completion_cot_retriever.py` |
| Graph Completion Decomposition | `<COGNEE_REPO>/cognee/modules/retrieval/graph_completion_decomposition_retriever.py` |
| Graph Completion Context Extension | `<COGNEE_REPO>/cognee/modules/retrieval/graph_completion_context_extension_retriever.py` |
| Triplet | `<COGNEE_REPO>/cognee/modules/retrieval/triplet_retriever.py` |
| Hybrid | `<COGNEE_REPO>/cognee/modules/retrieval/hybrid_retriever.py` |
| Cypher | `<COGNEE_REPO>/cognee/modules/retrieval/cypher_search_retriever.py` |
| Natural Language | `<COGNEE_REPO>/cognee/modules/retrieval/natural_language_retriever.py` |
| Temporal | `<COGNEE_REPO>/cognee/modules/retrieval/temporal_retriever.py` |
| Code | `<COGNEE_REPO>/cognee/modules/retrieval/code_retriever.py` |
| Coding Rules | `<COGNEE_REPO>/cognee/modules/retrieval/coding_rules_retriever.py` |
| Agentic | `<COGNEE_REPO>/cognee/modules/retrieval/agentic_retriever.py` |
| Completion | `<COGNEE_REPO>/cognee/modules/retrieval/completion_retriever.py` |
| BM25 | `<COGNEE_REPO>/cognee/modules/retrieval/bm25_retriever.py` |
| Lexical | `<COGNEE_REPO>/cognee/modules/retrieval/lexical_retriever.py` |
| Jaccard | `<COGNEE_REPO>/cognee/modules/retrieval/jaccard_retrival.py` |

## 存储后端路径

| 适配器 | 路径 |
|---|---|
| 图引擎工厂 | `<COGNEE_REPO>/cognee/infrastructure/databases/graph/get_graph_engine.py` |
| 向量引擎工厂 | `<COGNEE_REPO>/cognee/infrastructure/databases/vector/get_vector_engine.py` |
| 关系引擎工厂 | `<COGNEE_REPO>/cognee/infrastructure/databases/relational/get_relational_engine.py` |
| Ladybug 适配 | `<COGNEE_REPO>/cognee/infrastructure/databases/graph/ladybug/adapter.py` |
| Kuzu 适配 | `<COGNEE_REPO>/cognee/infrastructure/databases/graph/kuzu/adapter.py` |
| Neo4j 适配 | `<COGNEE_REPO>/cognee/infrastructure/databases/graph/neo4j_driver/adapter.py` |
| LanceDB 适配 | `<COGNEE_REPO>/cognee/infrastructure/databases/vector/lancedb/LanceDBAdapter.py` |
| PGVector 适配 | `<COGNEE_REPO>/cognee/infrastructure/databases/vector/pgvector/PGVectorAdapter.py` |
| Postgres Hybrid | `<COGNEE_REPO>/cognee/infrastructure/databases/hybrid/postgres/adapter.py` |
| SQLAlchemy 适配 | `<COGNEE_REPO>/cognee/infrastructure/databases/relational/sqlalchemy/SqlAlchemyAdapter.py` |
| Embedding 引擎 | `<COGNEE_REPO>/cognee/infrastructure/databases/vector/embeddings/get_embedding_engine.py` |

## LLM 路径

| 概念 | 路径 |
|---|---|
| LLM Gateway | `<COGNEE_REPO>/cognee/infrastructure/llm/LLMGateway.py` |
| LLM 配置 | `<COGNEE_REPO>/cognee/infrastructure/llm/config.py` |
| LiteLLM + Instructor | `<COGNEE_REPO>/cognee/infrastructure/llm/structured_output_framework/litellm_instructor/` |
| Tokenizer resolver | `<COGNEE_REPO>/cognee/infrastructure/llm/tokenizer/resolver.py` |

## Memify 路径

| 概念 | 路径 |
|---|---|
| memify 主入口 | `<COGNEE_REPO>/cognee/modules/memify/memify.py` |
| 默认 task 列表 | `<COGNEE_REPO>/cognee/memify_pipelines/memify_default_tasks.py` |
| apply_feedback_weights | `<COGNEE_REPO>/cognee/memify_pipelines/apply_feedback_weights.py` |
| apply_frequency_weights | `<COGNEE_REPO>/cognee/memify_pipelines/apply_frequency_weights.py` |
| consolidate_entity_descriptions | `<COGNEE_REPO>/cognee/memify_pipelines/consolidate_entity_descriptions.py` |
| create_triplet_embeddings | `<COGNEE_REPO>/cognee/memify_pipelines/create_triplet_embeddings.py` |
| global_context_index | `<COGNEE_REPO>/cognee/memify_pipelines/global_context_index.py` |
| persist_sessions_in_knowledge_graph | `<COGNEE_REPO>/cognee/memify_pipelines/persist_sessions_in_knowledge_graph.py` |
| persist_agent_trace_feedbacks_in_knowledge_graph | `<COGNEE_REPO>/cognee/memify_pipelines/persist_agent_trace_feedbacks_in_knowledge_graph.py` |

## FastAPI 与 CLI 路径

| 概念 | 路径 |
|---|---|
| FastAPI app | `<COGNEE_REPO>/cognee/api/client.py` |
| v1 router 装载 | `<COGNEE_REPO>/cognee/api/v1/` |
| Add router | `<COGNEE_REPO>/cognee/api/v1/add/routers/get_add_router.py` |
| Cognify router | `<COGNEE_REPO>/cognee/api/v1/cognify/routers/get_cognify_router.py` |
| Search router | `<COGNEE_REPO>/cognee/api/v1/search/routers/get_search_router.py` |
| Recall router | `<COGNEE_REPO>/cognee/api/v1/recall/routers/get_recall_router.py` |
| Remember router | `<COGNEE_REPO>/cognee/api/v1/remember/routers/get_remember_router.py` |
| Improve router | `<COGNEE_REPO>/cognee/api/v1/improve/routers/get_improve_router.py` |
| Memify router | `<COGNEE_REPO>/cognee/api/v1/memify/routers/get_memify_router.py` |
| Forget router | `<COGNEE_REPO>/cognee/api/v1/forget/routers/get_forget_router.py` |
| CLI 入口 | `<COGNEE_REPO>/cognee/cli/_cognee.py` |
| CLI 命令实现 | `<COGNEE_REPO>/cognee/cli/commands/` |
| Eval runner | `<COGNEE_REPO>/cognee/eval_framework/runner.py` |
| BEAM 报告 | `<COGNEE_REPO>/cognee/eval_framework/beam/REPORT.md` |

## 集成仓库路径(`<COGNEE_INTEGRATIONS_REPO>/`)

| 集成 | 路径 |
|---|---|
| 权威 inventory | `<COGNEE_INTEGRATIONS_REPO>/integrations/inventory.yml` |
| 总 README | `<COGNEE_INTEGRATIONS_REPO>/README.md` |
| Claude Code | `<COGNEE_INTEGRATIONS_REPO>/integrations/claude-code/` |
| Claude Agent SDK | `<COGNEE_INTEGRATIONS_REPO>/integrations/claude-agent-sdk/` |
| Strands | `<COGNEE_INTEGRATIONS_REPO>/integrations/strands/` |
| LangGraph | `<COGNEE_INTEGRATIONS_REPO>/integrations/langgraph/` |
| CrewAI | `<COGNEE_INTEGRATIONS_REPO>/integrations/crewai/` |
| Google ADK | `<COGNEE_INTEGRATIONS_REPO>/integrations/google-adk/` |
| Hermes | `<COGNEE_INTEGRATIONS_REPO>/integrations/hermes-agent/` |
| Telegram | `<COGNEE_INTEGRATIONS_REPO>/integrations/telegram/` |
| Slack | `<COGNEE_INTEGRATIONS_REPO>/integrations/slack/` |
| Web Widget | `<COGNEE_INTEGRATIONS_REPO>/integrations/web-widget/` |
| Chat-Memory | `<COGNEE_INTEGRATIONS_REPO>/integrations/chat-memory/` |
| n8n | `<COGNEE_INTEGRATIONS_REPO>/integrations/n8n/` |
| Dify | `<COGNEE_INTEGRATIONS_REPO>/integrations/dify/` |
| VS Code | `<COGNEE_INTEGRATIONS_REPO>/integrations/vscode/` |
| OpenClaw | `<COGNEE_INTEGRATIONS_REPO>/integrations/openclaw/` |
| Codex | `<COGNEE_INTEGRATIONS_REPO>/integrations/codex/` |
| Aider | `<COGNEE_INTEGRATIONS_REPO>/integrations/aider/` |
| Vellum | `<COGNEE_INTEGRATIONS_REPO>/integrations/vellum-assistant/` |
| OpenCode | `<COGNEE_INTEGRATIONS_REPO>/integrations/opencode/` |
| Second Brain | `<COGNEE_INTEGRATIONS_REPO>/integrations/second-brain/` |
| 独立 MCP Server | `<COGNEE_REPO>/cognee-mcp/src/server.py` |
| n8n workflow | `<COGNEE_INTEGRATIONS_REPO>/n8n_workflows/` |

## 关键示例路径

| 示例 | 路径 |
|---|---|
| 最简三步走 | `<COGNEE_REPO>/examples/demos/simple_cognee_example.py` |
| 1.0 内存 API | `<COGNEE_REPO>/examples/demos/remember_recall_improve_example.py` |
| 端到端综合 | `<COGNEE_REPO>/examples/demos/comprehensive_example/cognee_comprehensive_example.py` |
| Agent 快速开始 | `<COGNEE_REPO>/examples/guides/agent_memory_quickstart.py` |
| 自定义数据模型 | `<COGNEE_REPO>/examples/guides/custom_data_models.py` |
| 自定义图模型 | `<COGNEE_REPO>/examples/guides/custom_graph_model.py` |
| 自定义 task | `<COGNEE_REPO>/examples/guides/custom_tasks_and_pipelines.py` |
| 自定义 cognify pipeline | `<COGNEE_REPO>/examples/custom_pipelines/custom_cognify_pipeline_example.py` |
| 组织架构图谱 | `<COGNEE_REPO>/examples/custom_pipelines/organizational_hierarchy/organizational_hierarchy_pipeline_example.py` |
| 多租户演示(SaaS) | `<COGNEE_INTEGRATIONS_REPO>/integrations/langgraph/examples/saas_entitlements_agents.py` |
| Claude Agent SDK MCP | `<COGNEE_INTEGRATIONS_REPO>/integrations/claude-agent-sdk/examples/example.py` |
| Langfuse 遥测 | `<COGNEE_REPO>/examples/guides/langfuse_telemetry.py` |
| 多媒体处理 | `<COGNEE_REPO>/examples/demos/multimedia_processing/multimedia_audio_image_processing_example.py` |

## 子仓库路径

| 子仓库 | 路径 |
|---|---|
| MCP Server | `<COGNEE_REPO>/cognee-mcp/` |
| Frontend | `<COGNEE_REPO>/cognee-frontend/` |
| Starter Kit | `<COGNEE_REPO>/cognee-starter-kit/` |
| DB Workers | `<COGNEE_REPO>/cognee_db_workers/` |
| Distributed | `<COGNEE_REPO>/distributed/` |
| Deployment | `<COGNEE_REPO>/deployment/` |
| Kuzu | `<COGNEE_REPO>/kuzu/` |
| Notebooks | `<COGNEE_REPO>/notebooks/` |
| Examples | `<COGNEE_REPO>/examples/` |
| Docs | `<COGNEE_REPO>/docs/` |
| Evals | `<COGNEE_REPO>/evals/` |