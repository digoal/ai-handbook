---
title: FAQ — 常见问答
slug: ch-54-faq
part: part-vii-reference
audience: all
reading_time: 6
prerequisites: []
semantica_version: 0.6.0
---

# ch-54 FAQ — 常见问答

> 本章列最常见的 12 个问题。

## 1. 用户视角(User)

### Q1: Semantica 与 LangChain / LlamaIndex 的核心区别?

| 维度 | Semantica | LangChain | LlamaIndex |
|---|---|---|---|
| 核心 | 决策图 + 上下文图 | Chain / Agent | Index / Query |
| 溯源 | ✅ W3C PROV-O 一等 | ❌ | ❌ |
| 冲突解决 | ✅ 5 类 | ❌ | ⚠ 弱 |
| 时序知识图 | ✅ BiTemporal | ❌ | ❌ |
| 本体治理 | ✅ OWL+SHACL+SKOS | ❌ | ❌ |

### Q2: Semantica 是开源的吗? 用什么协议?

MIT 协议, 完全开源。商业支持: [support@getsemantica.ai](mailto:support@getsemantica.ai)。

### Q3: 安装后需要什么凭证?

最小安装零凭证。要用 LLM 抽取 / 嵌入, 需要 OpenAI / Anthropic 等的 API key, 通过环境变量 `SEMANTICA_API_KEYS__OPENAI=sk-...` 注入。

### Q4: 数据存在哪里? 安全吗?

由用户选: 内存图 / Neo4j / pgvector / Pinecone / 轻量 Redis 一体图库 / ...。Semantica 不收集任何遥测数据。详见 [[ch-49-security]]。

### Q5: 单机能跑多大数据?

- NetworkX: ≤100k 节点, 单进程。
- 主流图库 (Neo4j / 轻量 Redis 一体图库): 1M+ 节点, 需 8 GB+ 内存。
- pgvector: 视 Postgres 配置。
- 极限数据 → K8s cluster + sharding, 见 [[ch-44-k8s-helm]]。

### Q6: 怎么从 LangChain 迁移?

- 数据导出: `from semantica.export import ParquetExporter` 出 Parquet, LangChain `Document.load_parquet()` 读入。
- 不建议"迁移", 两者可并存 (LangChain 做 RAG, Semantica 做 KG)。

### Q7: 怎么加新 LLM provider?

在 `semantica/llms/` 加类, 继承 `BaseLLM`, 注册到 `pyproject.toml:[llm-xxx]` extras。

### Q8: KG 更新是"全量"还是"增量"?

默认全量 (`build_knowledge_base` 重建)。增量用 `framework.run_pipeline(custom_pipeline, new_data)`, 配合 `ProvenanceManager.invalidate` 处理 stale 节点。

### Q9: 决策图和 KG 是一张图还是两张图?

同一张图 (ContextGraph [[ch-55-glossary]])。Decision 是图节点, label=`decision`, 与 Entity 节点同构。

### Q10: 怎么让决策可被监管?

`ProvenanceManager.export_prov(format="turtle")` 出 W3C PROV-O; `trace_decision_chain(format="mermaid")` 出因果图。两者均见 [[ch-21-context-decision]]。

### Q11: Semantica 适合 RAG 吗?

适合"知识图谱增强的 RAG" (GraphRAG)。若只是纯文本 RAG, LangChain / LlamaIndex 更轻。

### Q12: 怎么联系社区?

- Discord: [discord.gg/semantica](https://discord.gg/semantica)
- GitHub Issues
- Email: [support@getsemantica.ai](mailto:support@getsemantica.ai)

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/__init__.py:13` — `__version__ = "0.6.0"`。
- `semantica/cli.py:721` — `changelog` 子命令, 支持 `--json`。
- `CHANGELOG.md` (156 KB) — 全量变更日志。

### 2.2 最小复现脚本

```python
from semantica import __version__
print(f"Semantica version: {__version__}")
```

## 3. 架构师视角(Architect)

### 3.1 设计取舍

FAQ 是 reference 章, 通常跳过三视角分层; 但 lint 强制要求, 所以这里放极简两节。

### 3.2 何时补充新问题

- 同一问题出现 ≥3 次 → 加入 FAQ。
- 问题涉及设计取舍 → 升级为独立章节。

## 跨章引用

- 上一章: [[ch-53-troubleshooting]]
- 下一章: [[ch-55-glossary]]
- 入门: [[ch-01-welcome]]