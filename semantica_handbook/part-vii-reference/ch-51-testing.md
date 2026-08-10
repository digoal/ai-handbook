---
title: 测试 — 77 测试文件矩阵与覆盖率策略
slug: ch-51-testing
part: part-vii-reference
audience: all
reading_time: 8
prerequisites: []
semantica_version: 0.6.0
---

# ch-51 测试 — 77 测试文件矩阵与覆盖率策略

> `tests/` 目录 77 文件 + 每模块子目录覆盖, 用 `pytest` + `pytest.mark.integration` 区分单元 / 集成测试。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 跑全部单测: `pytest tests/ -m "not integration"`。
- 跑集成测试: `pytest tests/ -m integration` (需外部 API / 服务)。
- 看覆盖率: `pytest --cov=semantica --cov-report=html`。

### 1.2 一段最小可跑示例

```bash
# 全部单测
pytest tests/ -m "not integration" -x

# 集成测试 (需 OpenAI key / Neo4j 等)
pytest tests/ -m integration

# 单个模块
pytest tests/kg/ -v

# 覆盖率
pytest --cov=semantica --cov-report=term-missing
```

### 1.3 何时不用

- 你只想跑某个 CLI → `semantica doctor` 已包含核心模块检查。
- 你要做端到端 → 用 `tests/integration/` 下的脚本。

## 2. 开发者视角(Developer)

### 2.1 测试目录结构

| 子目录 | 文件数 | 重点 |
|---|---|---|
| `tests/core/` | 2 | test_core, test_core_integration |
| `tests/kg/` | 17 | 算法 / link prediction / path finding / similarity / node embeddings / temporal |
| `tests/semantic_extract/` | 14 | extractors / retry / robustness / fallback / structured output |
| `tests/embeddings/` | 14 | provider stores / pooling |
| `tests/ingest/` | 14 | 8 类 ingestor |
| `tests/graph_store/` | 7 | 4 后端 + methods wrapper |
| `tests/vector_store/` | 5 | 7 后端 |
| `tests/triplet_store/` | 4 | Oxigraph + 远程 SPARQL |
| `tests/reasoning/` | 5 | Rete / Datalog / SPARQL |
| `tests/ontology/` | 5 | OWL / SHACL |
| `tests/pipeline/` | 5 | DAG / resource scheduler |
| `tests/provenance/` | 5 | lineage / PROV-O export |
| `tests/context/` | 3 | ContextGraph [[ch-55-glossary]] / decision / policy |
| `tests/explorer/` | 4 | REST 端点 |
| `tests/integrations/agno/` | 3 | Agno 集成 |
| `tests/cookbook/` | 5 | 跑 notebook 作集成测试 |

### 2.2 关键文件

- `tests/test_import.py` — 公共 API 导入验证。
- `tests/test_all_features.py` — 端到端 smoke。
- `tests/test_cli_commands.py` — CLI 全命令验证。
- `tests/test_notebook_*.py` — 跑 notebook 作集成测试。
- `pyproject.toml:[tool.pytest.ini_options]` — `integration` marker 定义。

### 2.3 最小复现脚本

```bash
# 1) 单测
pytest tests/test_import.py tests/test_all_features.py -v

# 2) 集成 (需配 key)
OPENAI_API_KEY=sk-xxx pytest tests/integration/ -v

# 3) 覆盖率
pytest --cov=semantica --cov-report=html tests/
```

### 2.4 扩展点

- **加新测试**: 在 `tests/<模块>/` 加 `test_xxx.py`, 用 `@pytest.mark.integration` 标记需外部依赖。
- **覆盖率门槛**: 在 `pyproject.toml` 加 `--cov-fail-under=80`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么用 `pytest.mark.integration` 区分?**
- 单元测试要快 (<2 min), CI 默认跑。
- 集成测试慢 (~30 min), 只在手动 + nightly 跑。
- 用户本地 `pytest` 默认跳过 integration, 体验好。

**为什么跑 notebook 作测试?**
- notebook 是"代码", 与源码同步维护, 是"活的文档"。
- 集成测试 = "notebook 跑通"。

### 3.2 与同类对比

| 维度 | Semantica tests | LangChain tests | LlamaIndex tests |
|---|---|---|---|
| 文件数 | 77 | 100+ | 200+ |
| notebook 集成测试 | ✅ | ⚠ | ✅ |
| Integration marker | ✅ | ⚠ | ⚠ |

### 3.3 何时重新设计

- 单测 > 2 min → 拆 CI 多阶段 (fast / slow)。
- 覆盖率 < 60% → 加 `pytest --cov-fail-under`。

## 跨章引用

- 上一章: [[ch-50-cookbook-index]]
- 下一章: [[ch-52-contributing]]
- CI: [[ch-46-cicd]]