# 目录

> mdbook / GitBook 兼容

## 序
- [前言](./README.md)
- [术语表](./GLOSSARY.md)
- [写作规范](./style-guide.md)

---

## Part I · 基础认知 (Foundation)

- [第 1 章 为什么 Agent 需要 Cognee](./chapters/part-01-foundation/chapter-01-why-memory.md)
- [第 2 章 安装与五分钟上手](./chapters/part-01-foundation/chapter-02-install-quickstart.md)
- [第 3 章 Hello World:`add` / `cognify` / `search` 三步走](./chapters/part-01-foundation/chapter-03-add-cognify-search.md)
- [第 4 章 核心概念速览:ECL、SearchType、Retriever 三段式](./chapters/part-01-foundation/chapter-04-core-concepts.md)
- [第 5 章 与同类项目对比:Mem0 / Zep / Graphiti / Letta / LangChain Memory](./chapters/part-01-foundation/chapter-05-vs-alternatives.md)

---

## Part II · 架构深潜 (Architecture)

- [第 6 章 模块总览与代码地图](./chapters/part-02-architecture/chapter-06-module-map.md)
- [第 7 章 数据模型与实体:DataPoint / Entity / NodeSet / KnowledgeGraph](./chapters/part-02-architecture/chapter-07-data-model.md)
- [第 8 章 管道引擎 Pipelines:Task / Pipeline / DAG](./chapters/part-02-architecture/chapter-08-pipelines.md)
- [第 9 章 检索器三段式:get_retrieved_objects / get_context / get_completion](./chapters/part-02-architecture/chapter-09-retrievers.md)
- [第 10 章 存储后端:SQLite / LanceDB / Ladybug 与 Postgres 全栈](./chapters/part-02-architecture/chapter-10-storage-backends.md)
- [第 11 章 可观测性与追踪:OpenTelemetry / Langfuse / Trace](./chapters/part-02-architecture/chapter-11-observability.md)
- [第 12 章 大图治理:Sync / Migrations / Truth Subspace / Prune](./chapters/part-02-architecture/chapter-12-graph-governance.md)

---

## Part III · API 与检索 (API & Retrieval)

- [第 13 章 v1 底层 API 详解:`add` / `cognify` / `search`](./chapters/part-03-api/chapter-13-v1-api.md)
- [第 14 章 v2 内存 API:`remember` / `recall` / `improve` / `forget`](./chapters/part-03-api/chapter-14-v2-memory-api.md)
- [第 15 章 SearchType 全景与选型:18 种检索类型逐项详解](./chapters/part-03-api/chapter-15-search-type-tour.md)
- [第 16 章 Memify:`cognee.memify()` 与自适应记忆](./chapters/part-03-api/chapter-16-memify.md)
- [第 17 章 自定义管道与 DAG:@register_task 与 run_custom_pipeline](./chapters/part-03-api/chapter-17-custom-pipelines.md)
- [第 18 章 Agent Memory:`cognee.agent_memory` 与子代理](./chapters/part-03-api/chapter-18-agent-memory.md)

---

## Part IV · 集成与生态 (Integrations)

- [第 19 章 `cognee-cli` 完整子命令手册](./chapters/part-04-integrations/chapter-19-cli-manual.md)
- [第 20 章 Claude Code / Claude Agent SDK 集成(主流)](./chapters/part-04-integrations/chapter-20-claude-code.md)
- [第 21 章 Strands / LangGraph / CrewAI / Google ADK 集成(主流 4 框架)](./chapters/part-04-integrations/chapter-21-frameworks.md)
- [第 22 章 聊天工具集成:Telegram / Slack / Web Widget(主流 3)](./chapters/part-04-integrations/chapter-22-chat-tools.md)
- [第 23 章 无代码与 IDE/终端集成(长尾 11 集成)](./chapters/part-04-integrations/chapter-23-nocode-ide.md)

---

## Part V · 实战与运维 (Production & Ops)

- [第 24 章 配置与数据集治理:`cognee.config` / datasets / agents / 权限](./chapters/part-05-production/chapter-24-config-datasets.md)
- [第 25 章 数据迁移:Mem0 / Zep(Graphiti) / Letta / COGXArchive](./chapters/part-05-production/chapter-25-migration.md)
- [第 26 章 评测:BEAM 与 `cognee eval`](./chapters/part-05-production/chapter-26-evals-beam.md)
- [第 27 章 性能调优与缓存:Postgres Session Cache / LanceDB 索引](./chapters/part-05-production/chapter-27-performance-cache.md)
- [第 28 章 API Server:FastAPI / 认证 / 多租户 / Docker / K8s](./chapters/part-05-production/chapter-28-api-server-deploy.md)
- [第 29 章 前端 UI:cognee-frontend Next.js 控制台](./chapters/part-05-production/chapter-29-frontend-ui.md)
- [第 30 章 贡献指南:从 AGENTS.md 到模块扩展](./chapters/part-05-production/chapter-30-contributing.md)

---

## 附录
- [FAQ](./appendix/faq.md)
- [参考文献与论文](./appendix/references.md)
- [章节计划 CHAPTER_OUTLINE](./CHAPTER_OUTLINE.md)
- [代码片段集](./assets/code-samples/)