---
title: 知识图构建 (KG)
slug: ch-14-knowledge-graph
part: part-ii-core-modules
audience: all
reading_time: 13
prerequisites: [ch-12-semantic-extract, ch-13-embeddings]
semantica_version: 0.6.0
---

# ch-14 知识图构建 (KG)

> 把 (实体 / 关系 / 嵌入) 整合为一张可分析、可检索、可推理的知识图。本章讲解 `GraphBuilder [[ch-55-glossary]]` + 解析 + 时序 + 链接预测。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 节点/边的批量 upsert, 与 graph_store 协作。
- 实体解析 (entity resolution) — 把"Acme" / "Acme Inc." / "Acme Corporation" 合并。
- 中心度 / 社区检测 / 链接预测 / 时序回放。
- 与 `semantica.vector_store` 协同做混合检索。

### 1.2 一段最小可跑示例

```python
from semantica import Semantica

fw = Semantica()
result = fw.build_knowledge_base(
    sources=["./docs/intro.md"],
    embeddings=True, graph=True,
)
kg = result["knowledge_graph"]
print(f"Nodes: {kg.number_of_nodes()}  Edges: {kg.number_of_edges()}")
fw.shutdown()
```

> 想要更细的图算法(pagerank / 社区 / 链接预测), 见 [[#2.2 关键代码路径]] 与 [[#2.4 扩展点]]。

### 1.3 何时不用

- 你不需要图分析, 只需要 CRUD → 直接用图库适配层。
- 你的图极小 (<100 节点) → NetworkX 单进程即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.kg.GraphBuilder()
semantica.kg.GraphAnalyzer(knowledge_graph)
semantica.kg.EntityResolver()                  # 实体对齐
semantica.kg.TemporalGraphQuery(knowledge_graph)  # 时序回放
semantica.kg.BiTemporalFact(...)
semantica.kg.CommunityDetector()
semantica.kg.LinkPredictor()
semantica.kg.kg_methods.build_graph(...)
semantica.kg.kg_methods.analyze_graph(...)
semantica.kg.kg_methods.resolve_entities(...)
```

### 2.2 关键代码路径

- `semantica/kg/graph_builder.py` — `GraphBuilder.add_entities / add_relationships / build`。
- `semantica/kg/methods.py:162` — `build_kg` facade。
- `semantica/kg/methods.py:212` — `analyze_graph` facade。
- `semantica/kg/methods.py:260` — `resolve_entities` facade。
- `semantica/kg/entity_resolver.py` — 相似度 + 阻塞 + 投票。
- `semantica/kg/temporal.py` — `BiTemporalFact / TemporalGraphQuery`。

### 2.3 最小复现脚本

```python
# examples/ch-14-kg-minimal.py mirror
from semantica.kg import GraphBuilder, GraphAnalyzer

b = GraphBuilder()
b.add_entities([
    {"id": "A", "name": "Albert Einstein", "type": "PERSON"},
    {"id": "B", "name": "Niels Bohr", "type": "PERSON"},
])
b.add_relationships([{"source_id": "A", "target_id": "B", "type": "debated_with"}])

kg = b.build()
analyzer = GraphAnalyzer(kg)
print("centrality:", analyzer.pagerank())
print("predictions:", analyzer.link_prediction("A", top_k=3))
```

### 2.4 扩展点

- **加新算法**: 继承 `BaseAnalyzer.algorithm`, 注册到 `GraphAnalyzer._algorithms`。
- **加新图数据源**: 在 `GraphBuilder.add_*` 加方法, 适配 NetworkX/igraph/iGraph 等。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 KG 与 graph_store 拆开?**
- KG 是"图分析层" (中心度、社区、预测), graph_store 是"持久化层" (Cypher / GQL)。
- 拆开允许用 NetworkX 内存图做原型, 同一份代码切到 Neo4j 生产。
- 代价: 双重抽象, 新人需理解"图分析 ≠ 图存储"。

### 3.2 与同类对比

| 维度 | Semantica kg | NetworkX + 手写 | Neo4j GDS |
|---|---|---|---|
| 内置算法 | 10+ (pagerank / louvain / link prediction / centrality) | 全部手写 | 50+ (GDS 库) |
| 实体解析 | ✅ | ❌ | ⚠ 需 APOC |
| 时序图 | ✅ BiTemporal | ❌ | ❌ (需扩展) |

### 3.3 何时重新设计

- 图节点 > 1M → 必上 Neo4j / FalkorDB, KG 仍可用 NetworkX 副本做小样本分析。
- 需要图神经网络 (GNN) → 扩 `kg/gnn/` 子包。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-13-embeddings]]
- 下一章: [[ch-15-ontology]]
- 图存储后端: [[ch-18-graph-store]]
- 时序图细节: [[ch-25-change-management]]