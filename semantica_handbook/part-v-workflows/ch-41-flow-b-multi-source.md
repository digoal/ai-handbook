---
title: Flow B — 多源 → 去重 → 冲突 → 推理 → 决策
slug: ch-41-flow-b-multi-source
part: part-v-workflows
audience: all
reading_time: 14
prerequisites: [ch-22-deduplication, ch-23-conflicts, ch-16-reasoning]
semantica_version: 0.6.0
---

# ch-41 Flow B — 多源 → 去重 → 冲突 → 推理 → 决策

> 主轴 B 的端到端剧本: 多源并行接入 → 冲突检测 → 实体对齐 → 推理 → 决策图。本章复刻 `cookbook/advanced/06_Multi_Source_Data_Integration` (66 KB, 多个 Python 数据源生态整合)。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 同时从 PDF / Web / Snowflake / Databricks / Kafka 接入数据。
- 自动检测 5 类冲突 (value / type / temporal / relationship / logical)。
- 投票 / 时间戳 / 优先级 三种消解策略。
- 实体解析 (entity resolution) 把 "Acme" / "Acme Inc." / "Acme Corp" 合并。
- 跑 Datalog 推理找新关系, 把决策挂入决策图。

### 1.2 完整端到端剧本

```python
from semantica.ingest import FileIngestor, WebIngestor, SnowflakeIngestor
from semantica.semantic_extract.methods import extract_entities_llm
from semantica.conflicts.methods import detect_conflicts, resolve_conflicts
from semantica.deduplication.methods import merge_entities
from semantica.reasoning.methods import run_datalog
from semantica.context.decision_methods import record_decision, add_causal_relationship

# 1) 多源接入
sources = [
    FileIngestor().ingest(["./docs/source1.pdf"])[0],
    WebIngestor().ingest(["https://example.com/source2.html"])[0],
    SnowflakeIngestor().ingest(query="SELECT content FROM papers WHERE id < 100", warehouse="COMPUTE_WH")[0],
]

# 2) 抽取 (并行)
ents = [extract_entities_llm(s.content, provider="openai", model="gpt-4o-mini") for s in sources]

# 3) 冲突检测 + 解决
conflicts = detect_conflicts(ents)
resolved = resolve_conflicts(conflicts, strategy="voting")

# 4) 实体合并
merged = merge_entities(resolved, duplicates=None, strategy="merge")

# 5) 推理
facts = run_datalog(["person(X) :- name(X, 'Einstein')."])

# 6) 决策
d = record_decision(category="multi_source_merge",
                     scenario="Acme 实体合并",
                     reasoning="投票 3 个源, 多数为 'Acme Corp'",
                     outcome={"canonical": "Acme Corp"},
                     confidence=0.95,
                     decided_by="etl@bank.com")
add_causal_relationship(d["id"], "preceded", "dec-next-step")
```

### 1.3 何时不用

- 单源 → 用 [ch-40-flow-a-text-to-graph]。
- 不需要冲突解决 → 跳过 `conflicts`。
- 不需要推理 → 跳过 `run_datalog`。

## 2. 开发者视角(Developer)

### 2.1 调用的 API 与背后类

| 步骤 | API | 文件 |
|---|---|---|
| 1. ingest 多源 | `FileIngestor / WebIngestor / SnowflakeIngestor` | `semantica/ingest/` |
| 2. 抽取 (并行) | `extract_entities_llm` | `semantica/semantic_extract/methods.py:883` |
| 3. 冲突检测 | `detect_conflicts` | `semantica/conflicts/methods.py:130` |
| 4. 冲突解决 | `resolve_conflicts(strategy="voting")` | `semantica/conflicts/methods.py:201` |
| 5. 实体合并 | `merge_entities(strategy="merge")` | `semantica/deduplication/methods.py:296` |
| 6. 推理 | `run_datalog` | `semantica/reasoning/methods.py` |
| 7. 决策 | `record_decision / add_causal_relationship` | `semantica/context/decision_methods.py:23` |

### 2.2 关键代码路径

- `semantica/conflicts/methods.py:399` — `generate_investigation_guide` (冲突待人工裁定)。
- `semantica/deduplication/methods.py:345` — `build_clusters` (相似度聚类)。
- `semantica/context/decision_methods.py:650` — `create_policy_with_versioning` (决策闸门)。

### 2.3 最小复现脚本

```python
# examples/ch-41-flow-B-mini.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica.conflicts.methods import detect_conflicts, resolve_conflicts
from semantica.deduplication.methods import merge_entities

src = [{"source": "A", "claims": [{"s": "Acme", "p": "name", "o": "Acme Inc."}]},
       {"source": "B", "claims": [{"s": "Acme", "p": "name", "o": "Acme Corp"}]}]

c = detect_conflicts(src)
resolved = resolve_conflicts(c, strategy="voting")
print(merge_entities(resolved, strategy="merge"))
```

### 2.4 扩展点

- **自定义冲突策略**: 在 `conflicts/ConflictResolver._strategies` 注册新策略。
- **自定义合并动作**: 在 `deduplication/MergeStrategy._actions` 加分支。

## 3. 架构师视角(Architect)

### 3.1 这条主轴是 Semantica 与传统 KG 的差异化所在

传统 KG 工具 (Neo4j / Stardog) 假设数据已被 ETL 清洗干净, 不负责冲突解决。

Semantica 主轴 B 把"多源 → 去重 → 冲突 → 推理" 完整闭环, 让用户在数据中台层就把矛盾暴露出来, 而不是"建图后才发现 GDS 算法结果不一致"。

### 3.2 与同类对比

| 维度 | Semantica Flow B | Apache Airflow + dbt | Palantir Foundry |
|---|---|---|---|
| 冲突解决 | ✅ 内置 | ⚠ 仅 schema | ✅ 商业 |
| 实体解析 | ✅ | ❌ | ✅ |
| 推理 / 决策 | ✅ | ❌ | ⚠ |

### 3.3 何时重新设计

- 源 > 20 → 引入 `source_registry` 集中管理源定义 + 凭证。
- 决策数 > 100k → 引入专用决策图 (Neo4j cluster)。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-40-flow-a-text-to-graph]]
- 下一章: [[ch-42-flow-c-decision-intel]]
- 数据源: [[ch-37-data-sources]]
- 决策细节: [[ch-21-context-decision]]