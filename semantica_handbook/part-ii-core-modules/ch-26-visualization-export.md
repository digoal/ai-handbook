---
title: 可视化与导出 (Visualization & Export)
slug: ch-26-visualization-export
part: part-ii-core-modules
audience: all
reading_time: 11
prerequisites: [ch-14-knowledge-graph, ch-17-vector-store]
semantica_version: 0.6.0
---

# ch-26 可视化与导出 (Visualization & Export)

> 把 KG 渲成 PNG / SVG / HTML / Plotly, 或导出 RDF / Parquet / Arrow / CSV / JSON-LD。本章讲解 6 类可视化 + 12 类导出。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 6 类可视化: KG / Ontology / Embedding / Analytics / Temporal / SemanticNetwork。
- UMAP / t-SNE / PCA 三种嵌入降维。
- 12 类导出: RDF Turtle / JSON-LD / N-Triples / OWL / SHACL / Parquet / Arrow / Cypher / ArangoDB AQL / GraphML / CSV / HTML。
- 与 [[ch-31-explorer-frontend]] 协作 (浏览器渲染)。

### 1.2 一段最小可跑示例

```python
from semantica.visualization import KGVisualizer, EmbeddingVisualizer
from semantica.export import ParquetExporter, RDFExporter

# 1) 可视化 KG
v = KGVisualizer(knowledge_graph)
v.visualize_network(output_path="./kg.html", layout="force_atlas_2")

# 2) Embedding 2D
EmbeddingVisualizer(vectors, labels=labels).visualize(method="umap",
                                                       output_path="./emb.png")

# 3) 导出 Parquet
ParquetExporter().export(entities=ents, relationships=rels, output_path="./kg.parquet")

# 4) 导出 RDF
RDFExporter().export(kg, output_path="./kg.ttl", format="turtle")
```

### 1.3 何时不用

- 你已经有 BI 工具 (Tableau / Superset) → 导出 Parquet / CSV 给它们即可。
- 你的图 < 50 节点 → matplotlib 手绘即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
# Visualization
semantica.visualization.KGVisualizer(knowledge_graph)
semantica.visualization.OntologyVisualizer(ontology)
semantica.visualization.EmbeddingVisualizer(vectors, labels)
semantica.visualization.AnalyticsVisualizer(analytics_results)
semantica.visualization.TemporalVisualizer(temporal_data)
semantica.visualization.SemanticNetworkVisualizer(network)
semantica.visualization.visualization_methods.visualize_kg(...)
semantica.visualization.visualization_methods.visualize_ontology(...)
semantica.visualization.visualization_methods.visualize_embeddings(...)
semantica.visualization.visualization_methods.visualize_semantic_network(...)
semantica.visualization.visualization_methods.visualize_analytics(...)
semantica.visualization.visualization_methods.visualize_temporal(...)

# Export
semantica.export.RDFExporter()
semantica.export.OWLExporter()
semantica.export.CSVExporter()
semantica.export.ParquetExporter()
semantica.export.ArrowExporter()
semantica.export.GraphMLExporter()
semantica.export.JSONExporter()
semantica.export.YAMLExporter()
semantica.export.Neo4jCSVExporter()
semantica.export.ArangoAQLExporter()
semantica.export.LPGExporter()
semantica.export.DistanceEnrichedExporter()
semantica.export.ReportGenerator()
semantica.export.export_methods.export_graph(...)
semantica.export.export_methods.import_graph(...)
```

### 2.2 关键代码路径

- `semantica/visualization/kg_visualizer.py:79` — `KGVisualizer`。
- `semantica/visualization/kg_visualizer.py:187` — `visualize_network`。
- `semantica/visualization/kg_visualizer.py:292` — `visualize_communities`。
- `semantica/visualization/kg_visualizer.py:350` — `visualize_centrality`。
- `semantica/visualization/kg_visualizer.py:409` — `visualize_entity_types`。
- `semantica/visualization/kg_visualizer.py:455` — `visualize_relationship_matrix`。
- `semantica/visualization/embedding_visualizer.py` — UMAP / t-SNE / PCA。
- `semantica/visualization/methods.py:165` — `visualize_kg` facade。
- `semantica/export/rdf_exporter.py` — Turtle / N-Triples / JSON-LD。
- `semantica/export/owl_exporter.py` — OWL / SHACL 输出。
- `semantica/export/parquet_exporter.py` — Snappy 压缩列式。
- `semantica/export/arrow_exporter.py` — Apache IPC。
- `semantica/export/methods.py` — `export_graph / import_graph` 全套。

### 2.3 最小复现脚本

```python
# examples/ch-26-viz-export-minimal.py mirror
import networkx as nx
from semantica.visualization import KGVisualizer
from semantica.export import ParquetExporter

g = nx.DiGraph()
g.add_node("a", label="A"); g.add_node("b", label="B")
g.add_edge("a", "b", label="knows")

KGVisualizer(g).visualize_network(output_path="/tmp/g.html")
ParquetExporter().export(entities=[{"id": "a"}], relationships=[{"id": "r1"}],
                          output_path="/tmp/g.parquet")
```

### 2.4 扩展点

- **加新可视化**: 继承 `BaseVisualizer`, 实现 `visualize(...) -> Path`。
- **加新导出格式**: 在 `export/__init__.py:_EXPORTERS` 注册新类。
- **加新降维算法**: 扩 `EmbeddingVisualizer(method=...)` 支持 PacMAP / TriMAP。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 visualization 与 export 拆开?**
- Visualization 关注"人类可读", Export 关注"机器可消费", 输出格式与受众不同。
- 拆开后允许: 同一份 KG 同时输出 PNG (报告) + Parquet (数仓) + RDF (语义 Web)。

### 3.2 与同类对比

| 维度 | Semantica visualization | NetworkX draw | pyvis | Graphistry |
|---|---|---|---|---|
| KG / Ontology / Embedding / Analytics / Temporal | ✅ | ⚠ 1 | ⚠ 1 | ⚠ 1 |
| 浏览器渲染 | ✅ HTML | ❌ | ✅ | ✅ |

### 3.3 何时重新设计

- 导出格式 > 20 → 拆 `semantica-export-tabular` / `semantica-export-semantic`。
- 节点 > 100k → 必须先降采样再可视化。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-25-change-management]]
- Explorer 工作台: [[ch-31-explorer-frontend]]
- 端到端剧本: [[ch-40-flow-a-text-to-graph]]