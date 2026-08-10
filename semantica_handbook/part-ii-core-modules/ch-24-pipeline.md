---
title: 流水线编排 (Pipeline) — PipelineBuilder + ExecutionEngine
slug: ch-24-pipeline
part: part-ii-core-modules
audience: all
reading_time: 12
prerequisites: [ch-08-ingest, ch-09-parse, ch-10-normalize, ch-11-split, ch-12-semantic-extract]
semantica_version: 0.6.0
---

# ch-24 流水线编排 (Pipeline)

> 把任意步骤串成可暂停 / 可恢复 / 可并行 / 可失败的 DAG。本章讲解 `PipelineBuilder` DSL + `ExecutionEngine` 调度器。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 自定义 step (函数 / 类 / dict) 串成 DAG。
- `connect_steps()` 控制依赖, `set_parallelism()` 控制并行度。
- `pause / resume / stop` 实时控制。
- 内置 `FailureHandler` (retry / skip / abort) 与 `ResourceScheduler`。

### 1.2 一段最小可跑示例

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine

builder = PipelineBuilder()
builder.add_step("ingest", fn=lambda ctx: print("ingest") or {"docs": []})
builder.add_step("parse", fn=lambda ctx: print("parse") or {"text": ""})
builder.add_step("extract", fn=lambda ctx: print("extract") or {"ents": []})
builder.connect_steps("ingest", "parse").connect_steps("parse", "extract")

pipeline = builder.build()
result = ExecutionEngine(pipeline).execute(initial_data={"src": "./data.pdf"})
print(result.output)
```

### 1.3 何时不用

- 你只需要线性 ETL → 直接写 `for src in sources: ingest -> parse -> extract`, 引入 pipeline 是过度工程。
- 你的 step 数 > 1000 → 考虑 Airflow / Prefect / Dagster (工业级 DAG 引擎)。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.pipeline.PipelineBuilder()
semantica.pipeline.ExecutionEngine(pipeline)
semantica.pipeline.ParallelismManager()
semantica.pipeline.ResourceScheduler()
semantica.pipeline.FailureHandler()
semantica.pipeline.PipelineValidator()
semantica.pipeline.PipelineTemplateManager()
```

### 2.2 关键代码路径

- `semantica/pipeline/pipeline_builder.py:94` — `PipelineBuilder`。
- `semantica/pipeline/pipeline_builder.py:119` — `add_step`。
- `semantica/pipeline/pipeline_builder.py:151` — `connect_steps`。
- `semantica/pipeline/pipeline_builder.py:188` — `build`。
- `semantica/pipeline/pipeline_builder.py:313` — `serialize`。
- `semantica/pipeline/execution_engine.py:113` — `execute_pipeline`。
- `semantica/pipeline/execution_engine.py:445-461` — `pause / resume / stop`。
- `semantica/pipeline/execution_engine.py:472` — `get_progress`。
- `semantica/pipeline/pipeline_provenance.py` — pipeline 与 ProvenanceManager 集成。

### 2.3 最小复现脚本

```python
# examples/ch-24-pipeline-minimal.py mirror
from semantica.pipeline import PipelineBuilder, ExecutionEngine

b = PipelineBuilder()
b.add_step("s1", fn=lambda c: {"v": 1})
b.add_step("s2", fn=lambda c: {"v": c["v"] * 2})
b.add_step("s3", fn=lambda c: {"v": c["v"] + 1})
b.connect_steps("s1", "s2").connect_steps("s2", "s3")

p = b.build()
print(ExecutionEngine(p).execute(initial_data={}).output)
```

### 2.4 扩展点

- **加新 step 类型**: 继承 `BaseStep.run(context) -> dict`, 在 `add_step` 注册。
- **加新调度策略**: 扩 `ResourceScheduler._policy`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么不直接用 Airflow?**
- PipelineBuilder 是 in-process 同步 DSL, 适合 notebook / 单机 ETL。
- Airflow 是分布式 DAG 引擎, 适合云端 cron job。
- Semantica 把 PipelineBuilder 作为"快速原型", 把 Airflow 作为"生产调度", 用户自己挑。

### 3.2 与同类对比

| 维度 | Semantica pipeline | Airflow | Prefect | Dagster |
|---|---|---|---|---|
| 部署 | in-process | 分布式 | 分布式 | 分布式 |
| 暂停/恢复 | ✅ | ✅ | ✅ | ✅ |
| 失败策略 | 3 (retry/skip/abort) | 5 | 4 | 4 |
| Provenance 集成 | ✅ 内置 | ❌ | ⚠ | ⚠ |

### 3.3 何时重新设计

- step 数 > 100 → 引入 PipelineTemplateManager (模板)。
- DAG 跨进程 → 引入 Redis / Kafka 队列。

## 本章图表

> 本章无 Mermaid 图。整链路流水线见 [[ch-04-architecture-30kft]] FIG-02。

## 跨章引用

- 上一章: [[ch-23-conflicts]]
- 下一章: [[ch-25-change-management]]
- 端到端用法: [[ch-40-flow-a-text-to-graph]]