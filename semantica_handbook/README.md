---
title: Semantica Handbook 索引与导读
slug: handbook-readme
part: part-i-foundations
audience: all
reading_time: 10
prerequisites: []
semantica_version: 0.6.0
last_reviewed: 2026-08-10
handbook_version: 1.0.0
status: production
---

# Semantica Handbook — 系统化手册

> **Semantica** 是面向 AI 代理的"问责 + 上下文"层(Accountability & Context Layer for AI Agents)。本手册从『开发者 / 用户 / 架构师』三个视角系统化讲述其设计与用法。

[![Handbook Lint](https://github.com/semantica-agi/semantica/actions/workflows/handbook-lint.yml/badge.svg)](https://github.com/semantica-agi/semantica/actions/workflows/handbook-lint.yml) [![Chapters](https://img.shields.io/badge/chapters-56-blue)]() [![Last Reviewed](https://img.shields.io/badge/last_reviewed-2026--08--10-green)]() [![Semantica Version](https://img.shields.io/badge/semantica-v0.6.0-orange)]()

---

## 1. 这是什么

Semantica 是一套把『非结构化文本 → 语义层 + 知识图谱 + 嵌入 + 决策图谱 → 可审计 AI 决策』端到端串起来的 Python + TypeScript 全栈框架。本 handbook 是其系统化手册, 涵盖:

- 27 个 Python 子包、~150 个公开 API
- CLI(~80 个子命令)、REST API(~100 个端点)、MCP Server(12 个工具)、Knowledge Explorer 工作台(7 个 workspace)
- 与 8 家 LLM、7 个向量库、4 个图库、5 个 RDF 库的集成矩阵
- 三条主用户工作流(文本建图 / 多源融合 / 决策智能)
- Docker / Compose / 5 个云平台的部署与运维

---

## 2. 三条阅读路径

按角色挑路径:

| 路径 | 目标读者 | 时长 | 路径 |
|---|---|---|---|
| **A. 快速上手** | 想 1 小时内跑通一个 demo 的产品/数据科学家 | 60 分钟 | ch-01 → ch-03 → ch-06 → ch-40 → ch-43 |
| **B. 完整通读** | 想体系化理解 Semantica 全貌的工程师 | 8-10 小时 | 顺序读完 Part I → Part VII |
| **C. 架构向深读** | 想评估/扩展/改造 Semantica 的架构师 | 6 小时 | ch-04 → ch-05 → ch-17 → ch-18 → ch-21 → ch-30 → ch-32 → ch-42 |

任何路径都可跳到 [GLOSSARY](GLOSSARY.md) 查术语。

---

## 3. 章节索引

### Part I 入门 Foundations
- [ch-01-welcome](part-i-foundations/ch-01-welcome.md) — Semantica 是什么、谁该用、不该用
- [ch-02-three-perspectives](part-i-foundations/ch-02-three-perspectives.md) — 阅读指南
- [ch-03-install](part-i-foundations/ch-03-install.md) — 安装与可选依赖
- [ch-04-architecture-30kft](part-i-foundations/ch-04-architecture-30kft.md) — 高层架构 (FIG-1/2)
- [ch-05-data-models](part-i-foundations/ch-05-data-models.md) — 核心数据模型 (FIG-3/4)
- [ch-06-quickstart-three-flows](part-i-foundations/ch-06-quickstart-three-flows.md) — 三主轴最小示例 (FIG-9)
- [ch-07-configuration-primer](part-i-foundations/ch-07-configuration-primer.md) — 配置极简

### Part II 核心模块 Core Modules
- [ch-08-ingest](part-ii-core-modules/ch-08-ingest.md)
- [ch-09-parse](part-ii-core-modules/ch-09-parse.md)
- [ch-10-normalize](part-ii-core-modules/ch-10-normalize.md)
- [ch-11-split](part-ii-core-modules/ch-11-split.md)
- [ch-12-semantic-extract](part-ii-core-modules/ch-12-semantic-extract.md)
- [ch-13-embeddings](part-ii-core-modules/ch-13-embeddings.md)
- [ch-14-knowledge-graph](part-ii-core-modules/ch-14-knowledge-graph.md)
- [ch-15-ontology](part-ii-core-modules/ch-15-ontology.md)
- [ch-16-reasoning](part-ii-core-modules/ch-16-reasoning.md)
- [ch-17-vector-store](part-ii-core-modules/ch-17-vector-store.md)
- [ch-18-graph-store](part-ii-core-modules/ch-18-graph-store.md)
- [ch-19-triplet-store](part-ii-core-modules/ch-19-triplet-store.md)
- [ch-20-provenance](part-ii-core-modules/ch-20-provenance.md)
- [ch-21-context-decision](part-ii-core-modules/ch-21-context-decision.md)
- [ch-22-deduplication](part-ii-core-modules/ch-22-deduplication.md)
- [ch-23-conflicts](part-ii-core-modules/ch-23-conflicts.md)
- [ch-24-pipeline](part-ii-core-modules/ch-24-pipeline.md)
- [ch-25-change-management](part-ii-core-modules/ch-25-change-management.md)
- [ch-26-visualization-export](part-ii-core-modules/ch-26-visualization-export.md)

### Part III 横切面 Cross-cutting
- [ch-27-cli](part-iii-cross-cutting/ch-27-cli.md) (FIG-14)
- [ch-28-server-api](part-iii-cross-cutting/ch-28-server-api.md) (FIG-5)
- [ch-29-worker](part-iii-cross-cutting/ch-29-worker.md)
- [ch-30-mcp-server](part-iii-cross-cutting/ch-30-mcp-server.md) (FIG-15)
- [ch-31-explorer-frontend](part-iii-cross-cutting/ch-31-explorer-frontend.md) (FIG-6)
- [ch-32-lifecycle-errors-config](part-iii-cross-cutting/ch-32-lifecycle-errors-config.md) (FIG-11/12/13)

### Part IV 集成 Integrations
- [ch-33-llm-providers](part-iv-integrations/ch-33-llm-providers.md) (FIG-7)
- [ch-34-vector-stores-compat](part-iv-integrations/ch-34-vector-stores-compat.md)
- [ch-35-graph-stores-compat](part-iv-integrations/ch-35-graph-stores-compat.md)
- [ch-36-triple-stores-compat](part-iv-integrations/ch-36-triple-stores-compat.md)
- [ch-37-data-sources](part-iv-integrations/ch-37-data-sources.md)
- [ch-38-agent-frameworks](part-iv-integrations/ch-38-agent-frameworks.md)
- [ch-39-ide-plugins](part-iv-integrations/ch-39-ide-plugins.md)

### Part V 用户工作流 Workflows
- [ch-40-flow-a-text-to-graph](part-v-workflows/ch-40-flow-a-text-to-graph.md)
- [ch-41-flow-b-multi-source](part-v-workflows/ch-41-flow-b-multi-source.md)
- [ch-42-flow-c-decision-intel](part-v-workflows/ch-42-flow-c-decision-intel.md) (FIG-8)

### Part VI 部署运维 Operations
- [ch-43-docker-compose](part-vi-operations/ch-43-docker-compose.md)
- [ch-44-k8s-helm](part-vi-operations/ch-44-k8s-helm.md)
- [ch-45-cloud-platforms](part-vi-operations/ch-45-cloud-platforms.md)
- [ch-46-cicd](part-vi-operations/ch-46-cicd.md)
- [ch-47-performance-benchmark](part-vi-operations/ch-47-performance-benchmark.md)
- [ch-48-observability](part-vi-operations/ch-48-observability.md)
- [ch-49-security](part-vi-operations/ch-49-security.md)

### Part VII 参考 Reference
- [ch-50-cookbook-index](part-vii-reference/ch-50-cookbook-index.md)
- [ch-51-testing](part-vii-reference/ch-51-testing.md)
- [ch-52-contributing](part-vii-reference/ch-52-contributing.md)
- [ch-53-troubleshooting](part-vii-reference/ch-53-troubleshooting.md)
- [ch-54-faq](part-vii-reference/ch-54-faq.md)
- [ch-55-glossary](part-vii-reference/ch-55-glossary.md)
- [ch-56-changelog-references](part-vii-reference/ch-56-changelog-references.md)

---

## 4. 图表索引

| ID | 名称 | 所在章 |
|---|---|---|
| FIG-01 | 高层系统架构图 | ch-04 |
| FIG-02 | 端到端数据流 | ch-04 |
| FIG-03 | 核心实体类图 | ch-05 |
| FIG-04 | 实体↔存储映射 | ch-05 |
| FIG-05 | REST+WS 序列 | ch-28 |
| FIG-06 | Explorer 组件树 | ch-31 |
| FIG-07 | LLM/向量/图库适配矩阵 | ch-33~35 |
| FIG-08 | 决策图时序 | ch-42 |
| FIG-09 | 三主轴对照 | ch-06 |
| FIG-10 | 部署拓扑 | ch-44 |
| FIG-11 | 配置 deep-merge 规则 | ch-32 |
| FIG-12 | 异常类层级 | ch-32 |
| FIG-13 | 生命周期状态 | ch-32 |
| FIG-14 | CLI 命令树 | ch-27 |
| FIG-15 | MCP tools/resources | ch-30 |

---

## 5. 三视角分层契约

每章固定三节:

| 节 | 视角 | 文风 |
|---|---|---|
| 1. 用户视角(User) | 5-9 步可跑通 + 截图占位 | 二级标题、子项列表、可复制命令 |
| 2. 开发者视角(Developer) | API 表 + 代码路径 + 最小复现脚本 | 代码块、API 表、step-by-step |
| 3. 架构师视角(Architect) | 设计取舍 + 与同类对比 + 何时重新设计 | 决策矩阵、ADR、trade-offs |

> CI lint 强制每章必须含三视角节, 否则拒绝合并。

---

## 6. 维护脚本

```bash
# 1) 校验所有章节 frontmatter (含 array element pattern)
python scripts/validate_frontmatter.py

# 2) 校验 [[ch-XX-slug]] 与 [[fig-NN]] 双向链接 (含 Markdown 普通链接)
python scripts/check_links.py

# 3) 校验三视角分层纯度 (阈值=1, 含高风险 token 加权)
python scripts/lint_perspectives.py

# 4) 校验 README 中 FIG-NN 在章节里有声明 (无幽灵图、无编号冲突)
python scripts/check_figures.py

# 5) 校验 slug 与文件名 stem 严格相等 (lowercase)
python scripts/check_slug_filename.py

# 6) 校验每章必需节齐全 (三视角 + 跨章引用)
python scripts/check_chapter_sections.py

# 7) 校验术语首次出现处反链 [[ch-55-glossary]] (soft fail, 仅 top 30)
python scripts/check_glossary_backlinks.py

# 8) 渲染所有 Mermaid 块到 SVG
bash scripts/render_mmd.sh

# 仅校验(不渲染)
bash scripts/render_mmd.sh --check
```

---

## 7. 反馈与贡献

- 章节编辑模板: [templates/chapter.md](templates/chapter.md)
- Frontmatter schema: [templates/frontmatter.schema.json](templates/frontmatter.schema.json)
- 投稿指南: [CONTRIBUTING.md](CONTRIBUTING.md)
- 术语表: [GLOSSARY.md](GLOSSARY.md)

---

## 8. 发行说明 (Release Notes)

### v1.0.0 (2026-08-10) — 商业发布级

**亮点**:
- 56 章系统化覆盖 7 卷 (入门 → 核心 → 横切 → 集成 → 工作流 → 部署 → 参考)。
- 8 个 CI 校验脚本 (frontmatter / perspectives / links / figures / slug / sections / glossary / render)。
- 15 张 Mermaid 图全部渲染到 `assets/diagrams/*.svg`。
- 56 个 examples stub 在 `examples/`, 与 56 章一一对应。
- 5 个 ch-55 新词条 (method_registry / _ModuleProxy / build_knowledge_base / ConfigurationError / TypeError)。
- 32 处术语反链自动补齐 (ch-01/02/04/06/07/08/11/14/15/17/18/19/21/28/31/32/35/37/38/42/44/50/51/53)。

**修复**: ch-14 build_graph → build_kg / ch-21 module-level 拆分 / ch-08 register_reader → method_registry / ch-04 行号 / ch-30 _handler / ch-03 LLM extras / FIG-07 幽灵图 / FIG-10/11 冲突 / ch-40-42 slug 大小写。

**已知不在范围内**: mcp_server `SERVER_INFO["version"]` 0.4.0 不一致 (源码问题) / 真实产品截图 (需产品提供) / handbook 与 docs.getsemantica.ai 同步 (Mintlify 站外)。

完整 changelog: [CHANGELOG.md](CHANGELOG.md)

### 下版本路线图 (v1.1.0)

- `.github/workflows/handbook-lint.yml` 接入 (8 校验 CI 守门)
- Semantica v0.7 同步 (`SEM005` 限流错误码)
- Mintlify docs 自动同步
- 国际化 (zh-CN / en-US 双语)

### 校验摘要 (8 项)

```text
✓ validate_frontmatter.py  →  56/56 chapter(s) frontmatter valid
✓ lint_perspectives.py      →  56/56 three-perspective sections
✓ check_links.py            →  0 broken references
✓ check_figures.py          →  15 unique figures consistent
✓ check_slug_filename.py   →  56/56 slug-stem aligned
✓ check_chapter_sections.py →  56/56 required sections
✓ check_glossary_backlinks.py →  every term has backlink
✓ render_mmd.sh             →  14 mermaid blocks rendered
```