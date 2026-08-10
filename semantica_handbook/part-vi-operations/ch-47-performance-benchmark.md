---
title: 性能基准 — Benchmarks Suite
slug: ch-47-performance-benchmark
part: part-vi-operations
audience: all
reading_time: 7
prerequisites: [ch-04-architecture-30kft]
semantica_version: 0.6.0
---

# ch-47 性能基准 — Benchmarks Suite

> Semantica 提供可复现的基准测试, 比较 ingest / extract / kg / query / decision 各环节性能。本章讲解跑法 + 已知数字。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 跑端到端基准: `BENCHMARK_REAL_LIBS=1 python -m semantica.benchmarks.run`。
- 比对不同 LLM provider (OpenAI vs Anthropic vs Ollama)。
- 比对不同图库 (NetworkX vs Neo4j vs FalkorDB)。
- 比对不同向量库 (FAISS vs Qdrant vs Pinecone)。

### 1.2 一段最小可跑示例

```bash
# 1) 触发 GitHub Actions 基准
# 手动 dispatch .github/workflows/benchmark.yml

# 2) 本地跑
BENCHMARK_REAL_LIBS=1 python -m semantica.benchmarks.run \
  --ingest ./docs/ \
  --provider openai \
  --backend networkx
```

### 1.3 已知数字 (基于 README v0.6.0)

| 操作 | 数据规模 | 时间 |
|---|---|---|
| 单 PDF ingest + extract | 10 页 | ~3 s |
| 1000 文档 ingest | 1000 PDF | ~8 min (LLM 抽取) |
| KG build (10k 节点) | 10k 节点 | ~2 s |
| 决策图 1000 决策 | 1000 决策 | ~5 s |
| FalkorDB 查询 (BFS 深度 3) | 10k 节点 | ~50 ms |

### 1.4 何时不用

- 你要"持续监控" → 用 [ch-48-observability] 的 OpenTelemetry。
- 你的用例超出基准范围 → 写自己的 benchmark (参考 `semantica/benchmarks/run.py`)。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/benchmarks/__init__.py` — 基准套件导出。
- `semantica/benchmarks/run.py` — `run()` 主入口。
- `semantica/benchmarks/ingest_bench.py` — Ingest 基准。
- `semantica/benchmarks/extract_bench.py` — Extract 基准。
- `semantica/benchmarks/kg_bench.py` — KG 基准。
- `semantica/benchmarks/query_bench.py` — Query 基准。
- `semantica/benchmarks/decision_bench.py` — Decision 基准。
- `semantica/benchmarks/report.py` — 报告生成。

### 2.2 最小复现脚本

```python
# examples/ch-47-bench.py mirror
import time
from semantica import Semantica

fw = Semantica()
try:
    t0 = time.time()
    r = fw.build_knowledge_base(sources=["./README.md"], embeddings=False, graph=True)
    t1 = time.time()
    print(f"✓ KB build in {t1-t0:.2f}s, nodes={r['knowledge_graph'].number_of_nodes()}")
finally:
    fw.shutdown()
```

### 2.3 扩展点

- **加新基准**: 在 `semantica/benchmarks/` 加 `xxx_bench.py`, 实现 `Benchmark.run()`。
- **接 OpenTelemetry**: 在 `bench.py` 加 span。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么基准要 `BENCHMARK_REAL_LIBS=1` 才跑真实依赖?**
- 默认 `BENCHMARK_REAL_LIBS=0` 用 mock, CI 跑得快 (5 min 跑完)。
- 真实依赖需手工触发, 避免 CI 拉大依赖卡死。
- 用户本地想精确数字时手动跑。

### 3.2 与同类对比

| 维度 | Semantica Bench | LangSmith Bench | LlamaIndex Bench |
|---|---|---|---|
| 真实依赖可关 | ✅ | ❌ | ❌ |
| GitHub Action 集成 | ✅ | ⚠ | ⚠ |

### 3.3 何时重新设计

- 基准脚本 > 20 → 拆 `semantica-bench` 子包。
- 出现"跨版本回归" → 引入 benchmark 历史库。

## 跨章引用

- 上一章: [[ch-46-cicd]]
- 下一章: [[ch-48-observability]]
- 工作流: [[ch-40-flow-a-text-to-graph]]