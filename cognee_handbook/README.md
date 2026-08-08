# 《Cognee 记忆工程:面向 LLM Agent 的开源记忆框架实战》

> 一本面向 Claude Code CLI 用户、Agent 开发者与架构师的中文电子书
> 代码基线:`cognee` v1.4.0 + `cognee-integrations`
> 基线日期:2026-07-26

## 这是什么

Cognee 是一个开源 AI Agent 记忆框架,提供:

- **v1 底层 API**:`add → cognify → search`(图/向量/关系三层存储)
- **v2 内存 API**:`remember → recall → improve → forget`(Agent 友好的四步生命周期)
- **18+ SearchType**:从 RAG 到 Graph Completion,从 Cypher 到 Temporal
- **24 个集成**:Claude Code / Claude Agent SDK / Strands / LangGraph / CrewAI / Google ADK / Telegram / Slack / VS Code / n8n / Dify …
- **可选存储后端**:SQLite / Postgres、Ladybug / Neo4j / Kuzu、LanceDB / PGVector / Qdrant / Weaviate

本书把这套生态用 30 章、5 大篇系统讲清楚,从"为什么需要"到"生产部署"完整闭环。

## 读者画像

- **Claude Code CLI 用户**:想把"上次会话做了啥"变成长期记忆(本书第 20 章)
- **Agent 应用开发者**:需要把记忆挂到自己搭的 ReAct / Plan-and-Execute Agent(本书第 18、20、21 章)
- **架构师 / SRE**:评估存储后端、规划权限、跑 BEAM 评测、上 Kubernetes(本书第 10、24、26、28 章)
- **二次开发者**:想自定义 Pipeline / Task / Retriever / Graph Model(本书第 7、8、9、17 章)

## 阅读路径

| 你是谁 | 推荐路径 |
|---|---|
| 第一次听说 Cognee | Ch01 → Ch02 → Ch03 → Ch04 |
| Claude Code 重度用户 | Ch01 → Ch02 → Ch03 → Ch04 → Ch13 → Ch14 → Ch20 |
| Agent 框架开发者 | Ch01 → Ch04 → Ch07 → Ch13 → Ch14 → Ch15 → Ch18 → Ch21 |
| 架构师 | Ch01 → Ch06 → Ch07 → Ch08 → Ch09 → Ch10 → Ch11 → Ch24 → Ch26 → Ch27 → Ch28 |
| 准备落地生产 | Ch01 → Ch10 → Ch11 → Ch24 → Ch25 → Ch26 → Ch27 → Ch28 |

## 全书目录

### Part I · 基础认知 (Foundation)

- [Ch01 为什么 Agent 需要 Cognee](./chapters/part-01-foundation/chapter-01-why-memory.md)
- [Ch02 安装与五分钟上手](./chapters/part-01-foundation/chapter-02-install-quickstart.md)
- [Ch03 Hello World:`add` / `cognify` / `search` 三步走](./chapters/part-01-foundation/chapter-03-add-cognify-search.md)
- [Ch04 核心概念速览:ECL、SearchType、Retriever 三段式](./chapters/part-01-foundation/chapter-04-core-concepts.md)
- [Ch05 与同类项目对比:Mem0 / Zep / Graphiti / Letta / LangChain Memory](./chapters/part-01-foundation/chapter-05-vs-alternatives.md)

### Part II · 架构深潜 (Architecture)

- [Ch06 模块总览与代码地图](./chapters/part-02-architecture/chapter-06-module-map.md)
- [Ch07 数据模型与实体:DataPoint / Entity / NodeSet / KnowledgeGraph](./chapters/part-02-architecture/chapter-07-data-model.md)
- [Ch08 管道引擎 Pipelines:Task / Pipeline / DAG](./chapters/part-02-architecture/chapter-08-pipelines.md)
- [Ch09 检索器三段式:get_retrieved_objects / get_context / get_completion](./chapters/part-02-architecture/chapter-09-retrievers.md)
- [Ch10 存储后端:SQLite / LanceDB / Ladybug 与 Postgres 全栈](./chapters/part-02-architecture/chapter-10-storage-backends.md)
- [Ch11 可观测性与追踪:OpenTelemetry / Langfuse / Trace](./chapters/part-02-architecture/chapter-11-observability.md)
- [Ch12 大图治理:Sync / Migrations / Truth Subspace / Prune](./chapters/part-02-architecture/chapter-12-graph-governance.md)

### Part III · API 与检索 (API & Retrieval)

- [Ch13 v1 底层 API 详解:`add` / `cognify` / `search`](./chapters/part-03-api/chapter-13-v1-api.md)
- [Ch14 v2 内存 API:`remember` / `recall` / `improve` / `forget`](./chapters/part-03-api/chapter-14-v2-memory-api.md)
- [Ch15 SearchType 全景与选型:18 种检索类型逐项详解](./chapters/part-03-api/chapter-15-search-type-tour.md)
- [Ch16 Memify:`cognee.memify()` 与自适应记忆](./chapters/part-03-api/chapter-16-memify.md)
- [Ch17 自定义管道与 DAG:@register_task 与 run_custom_pipeline](./chapters/part-03-api/chapter-17-custom-pipelines.md)
- [Ch18 Agent Memory:`cognee.agent_memory` 与子代理](./chapters/part-03-api/chapter-18-agent-memory.md)

### Part IV · 集成与生态 (Integrations)

- [Ch19 `cognee-cli` 完整子命令手册](./chapters/part-04-integrations/chapter-19-cli-manual.md)
- [Ch20 Claude Code / Claude Agent SDK 集成(主流)](./chapters/part-04-integrations/chapter-20-claude-code.md)
- [Ch21 Strands / LangGraph / CrewAI / Google ADK 集成(主流 4 框架)](./chapters/part-04-integrations/chapter-21-frameworks.md)
- [Ch22 聊天工具集成:Telegram / Slack / Web Widget(主流 3)](./chapters/part-04-integrations/chapter-22-chat-tools.md)
- [Ch23 无代码与 IDE/终端集成(长尾 11 集成)](./chapters/part-04-integrations/chapter-23-nocode-ide.md)

### Part V · 实战与运维 (Production & Ops)

- [Ch24 配置与数据集治理:`cognee.config` / datasets / agents / 权限](./chapters/part-05-production/chapter-24-config-datasets.md)
- [Ch25 数据迁移:Mem0 / Zep(Graphiti) / Letta / COGXArchive](./chapters/part-05-production/chapter-25-migration.md)
- [Ch26 评测:BEAM 与 `cognee eval`](./chapters/part-05-production/chapter-26-evals-beam.md)
- [Ch27 性能调优与缓存:Postgres Session Cache / LanceDB 索引](./chapters/part-05-production/chapter-27-performance-cache.md)
- [Ch28 API Server:FastAPI / 认证 / 多租户 / Docker / K8s](./chapters/part-05-production/chapter-28-api-server-deploy.md)
- [Ch29 前端 UI:cognee-frontend Next.js 控制台](./chapters/part-05-production/chapter-29-frontend-ui.md)
- [Ch30 贡献指南:从 AGENTS.md 到模块扩展](./chapters/part-05-production/chapter-30-contributing.md)

### 附录

- [FAQ](./appendix/faq.md)
- [参考文献与论文](./appendix/references.md)
- [章节计划 CHAPTER_OUTLINE](./CHAPTER_OUTLINE.md)
- [完整目录 mdbook/GitBook 版](./SUMMARY.md)

## 仓库结构

```
cognee-handbook/
├── README.md                       本文件
├── SUMMARY.md                      全书目录
├── GLOSSARY.md                     术语表
├── style-guide.md                  写作与 mermaid 规范
├── CHAPTER_OUTLINE.md              章节计划
├── shared-context/                 注入子 Agent 的共享素材
├── chapters/                       30 章 markdown 源文件
├── assets/                         图、截图、代码样例
├── templates/                      章节模板与 mermaid 模板
└── code-review/                    校验报告
```

## 贡献与反馈

本书采用与 cognee 主项目一致的开放治理。完整规约见 **`style-guide.md`**,要点速览:
- 内容须与代码真实路径一致(`<COGNEE_REPO>/...`、`<COGNEE_INTEGRATIONS_REPO>/...`、`<HANDBOOK_REPO>`)
- 代码片段须经 `python -c` 验证可运行,**协议层必须清晰**(Python SDK / v2 memory / HTTP JSON / CLI 字段名不同)
- Unicode 直引号 / 弯引号必须 ASCII,数字事实由脚本验证(18 SearchType / 18 CLI / 24 inventory)
- 版本基线 v1.4.0,每次升级需同步
- mermaid 模板见 `templates/mermaid-template.md`

最近两轮 fact-check 已写入 `code-review/fact-check-report.md`(M11,30 章)与 `code-review/fact-check-m12.md`(M12,附录 + SVG + 代码块),下次写作前请先回看。

## 许可

本书基于 cognee 仓库(Apache 2.0 / 自有许可)内容创作,引用请保留出处。