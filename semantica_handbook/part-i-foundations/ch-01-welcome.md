---
title: Semantica 是什么、谁该用、不该用
slug: ch-01-welcome
part: part-i-foundations
audience: all
reading_time: 12
prerequisites: []
semantica_version: 0.6.0
---

# ch-01 Semantica 是什么、谁该用、不该用

> 一句话定义: Semantica = "AI 代理的问责 + 上下文"层。它把非结构化文本变成可追溯的语义图, 让每一笔 AI 决策都能被审计、被复用、被回滚。

## 1. 用户视角(User)

### 1.1 我能用它做什么

Semantica 解决三类高频痛点:

- **把分散的语料变成一张可查询的语义图** — 从 PDF / 网页 / 数据库 / Snowflake / HuggingFace Hub 拉数据, 自动抽实体/关系, 落到你选定的图库 (Neo4j / FalkorDB / AGE / Neptune / NetworkX)。
- **在 AI 决策图上做合规闸** — 每次 `record_decision()` 都被记为图节点, 通过 `add_causal_relationship()` 串成因果链, `check_decision_rules()` 在做决策前先跑策略门, `trace_decision_chain()` 出 W3C PROV-O 审计包。
- **多源融合 + 冲突解决 + 去重** — 同时从 Slack / Snowflake / Databricks / Kafka / Web 拉数据, 框架自动检测 5 类冲突 (value/type/temporal/relationship/logical) 并支持 `voting` 等策略消解, 然后做实体对齐 (entity resolution)。

> Knowledge Explorer 主界面见 [[ch-31-explorer-frontend]] (运行 `semantica-explorer` 后访问 http://localhost:8000/ 可看实际界面)。

### 1.2 一段最小可跑示例 (5-9 步)

```bash
# 1) 安装核心包
pip install semantica

# 2) 自检环境
semantica doctor

# 3) 初始化配置
semantica init

# 4) 从一个 PDF 抽取并构建 KG (一次性端到端)
semantica kg build --sources ./docs/whitepaper.pdf --temporal
```

```python
# 5) 或者用 Python API (推荐交互场景)
from semantica import Semantica
framework = Semantica()
result = framework.build_knowledge_base(
    sources=["./docs/whitepaper.pdf", "./docs/spec.md"],
    embeddings=True,
    graph=True,
)
print(result["statistics"])
framework.shutdown()
```

跑通这段, 你得到:
- 一个 NetworkX/Neo4j 图, 含 N 个实体、M 条边
- 一组 OpenAI/HuggingFace 嵌入向量(取决于 `~/.semantica/config.yaml` 配的 provider)
- 一份 provenance 报告(每个节点都能问"从哪行文本抽出来的")

### 1.3 三类典型用户画像

| 画像 | 痛点 | Semantica 帮到哪 |
|---|---|---|
| **AI 应用工程师** | "我的 LLM 老是编, 找不到证据" | 把 prompt + 检索 + 证据绑进决策图, `trace_decision_chain` 一键看证据链 |
| **数据科学家** | "我有 10 个 Snowflake 表 + 1000 篇 PDF, 想找谁和谁相关" | 一行 `semantica kg build --sources ...` 串起 ingest → extract → KG → analytics |
| **合规 / 风控 / 审计** | "我想给监管方一份可解释报告" | `export_prov` 出 W3C PROV-O, `trace_decision_chain` 出 mermaid 因果链 |

### 1.4 何时不用

- **你要的是 RAG 检索, 不需要治理** — 用 LangChain / LlamaIndex 的 RAG 模板更快。
- **你要的是单纯的图数据库** — 直接用 Neo4j / FalkorDB / Memgraph。
- **你要的是微调 LLM** — Semantica 是"治理 LLM 输出", 不替代训练。
- **你要的是纯实时流式 OLAP** — Semantica 有 `semantica.ingest.stream_ingestor` 但其重心在事件落地为图节点, 不是 ClickHouse / Pinot 那种时序聚合。

## 2. 开发者视角(Developer)

### 2.1 公开 API 速查

```python
from semantica import Semantica              # 主类, semantica/core/orchestrator.py:38
from semantica.core import build_knowledge_base, run_pipeline  # 框架级 facade, core/methods.py

# 主入口
framework = Semantica(config_dict={...})     # 显式 Config dict
framework = Semantica()                       # 默认配置
framework = Semantica(config=cfg_obj)         # 已构建 Config 对象

# 端到端管线
result = framework.build_knowledge_base(sources=[...], embeddings=True, graph=True)

# 单步管线 (适合自定义场景)
result = framework.run_pipeline(pipeline_or_dict, data)

# 生命周期
framework.initialize()        # 显式初始化, 通常 build_* 内部已调用
framework.get_status()        # {state, health, modules, plugins, config}
framework.shutdown()          # 优雅关闭
```

公共 dot-notation 通过 `semantica/__init__.py:47-67` 的 `_ModuleProxy` 暴露, 共 14 个子模块:
`semantica.kg / ingest / embeddings / semantic_extract / visualization / kg_qa / pipeline / parse / normalize / export / vector_store / triplet_store / graph_store / ontology / evals`。

### 2.2 关键代码路径

- `semantica/core/orchestrator.py:38` — `Semantica` 主类 (1026 行), 持有 `ConfigManager / LifecycleManager / PluginRegistry`。
- `semantica/core/methods.py:94` — `build_knowledge_base()` 框架级 facade, 内部包了 `Semantica(config).initialize().build_knowledge_base().shutdown()` 全流程。
- `semantica/core/lifecycle.py:59` — `LifecycleManager`, 状态机 UNINITIALIZED → INITIALIZING → READY → RUNNING → STOPPING → STOPPED。
- `semantica/__init__.py:47` — `_ModuleProxy` lazy loader, 让你写 `semantica.kg.GraphBuilder [[ch-55-glossary]]` 而不必先 `import semantica.kg`。
- `semantica/utils/exceptions.py:49` — `SemanticaError` 根异常, 5 个子类 (Validation / Processing / Configuration / Quality / TemporalValidation)。

### 2.3 最小复现脚本

```python
# examples/ch-01-smoke.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "WARNING")

from semantica import Semantica

fw = Semantica()
try:
    print("State:", fw.lifecycle_manager.get_state())
    print("Modules ready:", fw.lifecycle_manager.get_health_summary())
finally:
    fw.shutdown()
```

跑通看到 `READY` 即表示骨架正常。

### 2.4 扩展点

- **加新数据源**: 写一个继承 `semantica.ingest.BaseIngestor` 的类, 注册到 `ingest.register_reader`。
- **加新抽取策略**: 在 `semantica.semantic_extract.providers.BaseProvider` 子类化 `generate / generate_structured`。
- **加新图库后端**: 实现 `semantica.graph_store.graph_store.GraphStore [[ch-55-glossary]]` 接口, 在 `GraphStore.__init__` 路由。
- **加新 MCP tool**: 在 `semantica/mcp_server/__init__.py:288` 的 `TOOLS` 列表追加 `(name, schema, handler)` 三元组。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

- **选 "图 + 向量" 双存储, 而非单一图库**: 决策链路需要 graph traversal (因果链), 但语义检索需要 ANN (相似度), Semantica 不强迫用户在某一端让步。代价是双写一致性 (每条 decision 既入 vector_store 又入 graph_store), 由 `ProvenanceManager` 兜底。
- **选 "config dict + env override", 而非 Pydantic/Settings**: `core/config_manager.py:658` 的纯 stdlib + pyyaml 实现, 让 `pip install` 不强制拉 pydantic。代价是 schema 校验必须自己写。
- **选 "_ModuleProxy lazy import", 而非 eager `from .kg import *`**: 27 个子包不可能全部 eager 加载, 否则冷启动爆炸。代价是 IDE 自动补全略弱, 但运行时 `getattr` 性能可忽略。

### 3.2 与同类对比

| 维度 | Semantica | LangChain | LlamaIndex | Neo4j (原生) |
|---|---|---|---|---|
| **核心抽象** | 决策图 + 上下文图 | Chain / Agent | Index / Query | Cypher / 图 |
| **溯源 (PROV-O)** | ✅ 一等公民 | ❌ | ❌ | ⚠ 仅数据库层 |
| **冲突解决** | ✅ 5 类策略 | ❌ | ⚠ dedup 弱 | ❌ |
| **时序知识图** | ✅ valid_time + recorded_at 双时态 | ❌ | ❌ | ❌ (需扩展) |
| **本体治理** | ✅ OWL + SHACL + SKOS | ❌ | ❌ | ⚠ 仅标签 |
| **生态** | MCP / Agno 原生, 8 家 LLM | 6+ Agent 框架 | 中等 | 大 |
| **门槛** | 中 (Python + 图) | 低 | 低 | 低-中 |

### 3.3 何时重新设计 / 不引入 Semantica

- 当你的用例是纯 RAG (≤5 文档, ≤1k token) — 杀鸡用牛刀。
- 当你的合规需求仅仅是 "日志留存" 而非 "可解释因果链" — 简单 ELK 栈够用。
- 当你的数据规模 < 10k 节点 — NetworkX 内存图就够, 不必引入 Neo4j。

## 本章图表

> 本章为开篇导览, 不引入 Mermaid 图。架构图见 [[ch-04-architecture-30kft]]。

## 跨章引用

- 下一步: [[ch-02-three-perspectives]] — 弄清三视角的读法
- 高层架构: [[ch-04-architecture-30kft]]
- 入门安装: [[ch-03-install]]
- 最小示例: [[ch-06-quickstart-three-flows]]