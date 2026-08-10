---
title: Flow A — 文本 → 实体 → 图谱 → 查询 → 可视化
slug: ch-40-flow-a-text-to-graph
part: part-v-workflows
audience: all
reading_time: 14
prerequisites: [ch-04-architecture-30kft, ch-06-quickstart-three-flows]
semantica_version: 0.6.0
---

# ch-40 Flow A — 文本 → 实体 → 图谱 → 查询 → 可视化

> 主轴 A 的端到端剧本: 一份白皮书 → 拆 chunk → 抽实体/关系 → 入图 → 检索 → 可视化。本章复刻 `cookbook/introduction/01-08` 的完整路径。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 一段连贯 Python (≈30 行) 跑完 ingest → parse → normalize → split → semantic_extract → kg → analytics → visualize。
- 对应 notebook: `cookbook/introduction/01_Welcome_to_Semantica` → `08_Your_First_Knowledge_Graph`。

### 1.2 完整端到端剧本

```python
from semantica import Semantica

fw = Semantica()
result = fw.build_knowledge_base(
    sources=["./docs/whitepaper.pdf", "./docs/spec.md"],
    embeddings=True,
    graph=True,
    temporal=True,
)
kg = result["knowledge_graph"]
print(f"Nodes: {kg.number_of_nodes()}  Edges: {kg.number_of_edges()}")

# 查询
hits = fw.graph_builder.search("Einstein")
for h in hits:
    print(f"- {h['name']} ({h['type']}) conf={h['confidence']:.2f}")

# 可视化
from semantica.visualization import KGVisualizer
KGVisualizer(kg).visualize_network(output_path="./kg.html", layout="force_atlas_2")

fw.shutdown()
```

### 1.3 何时不用

- 你的源数据已是结构化 → 跳 ingest / parse。
- 你只要实体不要关系 → 用 `extract_entities` 单步。
- 你要 LLM 决策 → 走 [ch-42-flow-c-decision-intel]。

## 2. 开发者视角(Developer)

### 2.1 调用的 API 与背后类

| 步骤 | API | 文件 / 行 |
|---|---|---|
| 1. ingest | `fw.file_ingestor` | `semantica/ingest/file_ingestor.py` |
| 2. parse | `fw.document_parser` | `semantica/parse/document_parser.py` |
| 3. normalize | `semantica.normalize.*` | `semantica/normalize/` |
| 4. split | `semantica.split.*` | `semantica/split/` |
| 5. extract | `semantica.semantic_extract.methods.extract_entities_llm` | `semantica/semantic_extract/methods.py:883` |
| 6. embed | `fw.embedding_generator.generate_embeddings` | `semantica/embeddings/embedding_generator.py:135` |
| 7. kg build | `fw.graph_builder.build` | `semantica/kg/graph_builder.py` |
| 8. query | `fw.graph_builder.search` | `semantica/kg/` |
| 9. visualize | `KGVisualizer.visualize_network` | `semantica/visualization/kg_visualizer.py:187` |

### 2.2 关键代码路径

- `semantica/core/orchestrator.py:281` — `build_knowledge_base` 编排器入口。
- `semantica/core/orchestrator.py:454` — `run_pipeline` 单步执行。
- `semantica/core/orchestrator.py:801` — `_build_knowledge_graph` 子步骤。
- `semantica/core/orchestrator.py:853` — `_generate_embeddings` 子步骤。

### 2.3 最小复现脚本

```python
# examples/ch-40-flow-A.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica import Semantica

fw = Semantica()
try:
    r = fw.build_knowledge_base(
        sources=["./README.md"],
        embeddings=False, graph=True,
    )
    print(f"nodes={r['knowledge_graph'].number_of_nodes()}")
finally:
    fw.shutdown()
```

### 2.4 扩展点

- 想自定义 step: 写 `PipelineBuilder` ([ch-24-pipeline]) 而不是用 `build_knowledge_base`。
- 想换 LLM: `fw.config.set("semantic_extract.default_provider", "anthropic")`。

## 3. 架构师视角(Architect)

### 3.1 这条主轴揭示的"6 层必要性"

主轴 A 必须穿过 6 层才能完成: ingest → parse → normalize → split → extract → kg。

- 跳过 ingest: 数据进不来。
- 跳过 parse: PDF 字节无法解释。
- 跳过 normalize: 多语言混合失败。
- 跳过 split: 单 chunk > LLM 窗口。
- 跳过 extract: 无实体 / 关系。
- 跳过 kg: 无图谱。

> 因此 Semantica 的 6 层架构 ([ch-04-architecture-30kft]]) 不是过度设计, 而是"端到端 AI 应用"的最小集合。

### 3.2 三主轴的差异

| 主轴 | 输入节奏 | 写入节奏 | 适合场景 |
|---|---|---|---|
| A | 单次 | 一次性 ETL | 文档归档 / 知识库初始化 |
| B | 多源并行 | 周期性同步 | 多源融合 / 数据中台 |
| C | 流式 | 实时决策 | Agent 决策点 / 合规 |

### 3.3 何时拆解主轴

- 当用户总把 A 当 B 用 (想做融合但只给单源) → 在 `build_knowledge_base` 加 `multi_source=True` 自动走 B。
- 当用户做增量更新 → 引入 `framework.run_pipeline(custom_pipeline, delta)` 而非 `build_knowledge_base`。

## 本章图表

> 本章无 Mermaid 图。整链路见 [[ch-04-architecture-30kft]] FIG-02。

## 跨章引用

- 上一章: [[ch-39-ide-plugins]]
- 下一章: [[ch-41-flow-b-multi-source]]
- Cookbook 入口: [cookbook/introduction/](https://github.com/semantica-agi/semantica/tree/main/cookbook/introduction)
- 架构: [[ch-04-architecture-30kft]]