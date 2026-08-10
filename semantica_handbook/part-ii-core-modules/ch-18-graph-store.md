---
title: 图库适配 (Graph Store)
slug: ch-18-graph-store
part: part-ii-core-modules
audience: all
reading_time: 12
prerequisites: [ch-14-knowledge-graph]
semantica_version: 0.6.0
---

# ch-18 图库适配 (Graph Store)

> 4 家 LPG 图库 (Neo4j / FalkorDB / Apache AGE / Amazon Neptune) 统一接口。本章讲解 `GraphStore [[ch-55-glossary]]` + 查询引擎 + 分析。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 一行切后端: `backend="neo4j" / "falkordb" / "age" / "neptune"`。
- 节点/边的 CRUD + Cypher 查询 + 最短路径 + 邻居检索。
- 高级分析: 中心度 / 社区检测 (内置 GDS 算法)。
- 时序图 (Neo4j 5+ 时态功能 / FalkorDB 社区扩展)。

### 1.2 一段最小可跑示例

```python
from semantica.graph_store import GraphStore

# 默认 NetworkX 内存图
gs = GraphStore(backend="neo4j", uri="bolt://localhost:7687",
                user="neo4j", password="password")

# 创建
gs.create_node("Person", {"id": "p1", "name": "Einstein"})
gs.create_relationship("p1", "discovered", "c1", target_type="Concept", target_props={"name": "relativity"})

# 查询
hits = gs.shortest_path("p1", "p2", algorithm="dijkstra")
neighbors = gs.get_neighbors("p1", depth=2)
```

### 1.3 何时不用

- 数据 < 100 节点 → NetworkX 内存图即可。
- 你需要 RDF + SPARQL → 用 [[ch-19-triplet-store]]。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.graph_store.GraphStore(backend, **conn_kwargs)
semantica.graph_store.NodeManager()
semantica.graph_store.RelationshipManager()
semantica.graph_store.QueryEngine(gs)
semantica.graph_store.GraphAnalytics(gs)
semantica.graph_store.graph_store_methods.create_node(...)
semantica.graph_store.graph_store_methods.create_relationship(...)
semantica.graph_store.graph_store_methods.execute_query(...)
semantica.graph_store.graph_store_methods.shortest_path(...)
semantica.graph_store.graph_store_methods.get_neighbors(...)
semantica.graph_store.graph_store_methods.run_analytics(...)
```

### 2.2 关键代码路径

- `semantica/graph_store/graph_store.py:43-524` — `NodeManager / RelationshipManager / QueryEngine / GraphAnalytics`。
- `semantica/graph_store/graph_store.py:524` — 顶层 `GraphStore`。
- `semantica/graph_store/methods.py:91` — `create_node`。
- `semantica/graph_store/methods.py:235` — `create_relationship`。
- `semantica/graph_store/methods.py:403` — `execute_query`。
- `semantica/graph_store/methods.py:433` — `shortest_path`。
- `semantica/graph_store/methods.py:465` — `get_neighbors`。
- 后端: `neo4j_store.py / falkordb_store.py / age_store.py / amazon_neptune.py`。

### 2.3 最小复现脚本

```python
# examples/ch-18-graphstore-minimal.py mirror
from semantica.graph_store import GraphStore

# 内存 NetworkX (无需启动 Neo4j)
gs = GraphStore(backend="networkx")
gs.create_node("Person", {"id": "p1", "name": "Einstein"})
gs.create_node("Concept", {"id": "c1", "name": "relativity"})
gs.create_relationship("p1", "discovered", "c1")
print("Nodes:", gs.stats())
```

### 2.4 扩展点

- **加新后端**: 继承 `BaseGraphStoreBackend`, 实现 `create_node / create_relationship / execute_query`, 在 `GraphStore._backend_registry` 注册。
- **加新查询语言**: 扩 `QueryEngine` 支持 GQL / Gremlin / Cypher 子集。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 GraphStore 与 KG 拆开?**
- KG 是"图分析 + 构建", GraphStore 是"持久化"。
- 同一份 KG 代码可在 NetworkX (原型) / Neo4j (生产) / FalkorDB (Redis 一体) 间切。

**为什么支持 4 个后端而不是"只 Neo4j"?**
- FalkorDB 适合与 Redis 已有栈共存 (低延迟)。
- AGE 适合 PostgreSQL 已有栈 (单一数据库)。
- Neptune 适合 AWS 一体化部署。

### 3.2 与同类对比

| 维度 | Semantica graph_store | Neo4j 原生 | LangChain GraphStores |
|---|---|---|---|
| 后端数 | 4 + NetworkX | 1 | 5 |
| 查询缓存 | ✅ | ❌ | ❌ |
| 时序 | ✅ (BiTemporal) | ⚠ 5+ 时间树 | ❌ |

### 3.3 何时重新设计

- 节点 > 100M → 拆 cluster / sharding。
- 出现多图联邦 → 引入 federation layer。

## 本章图表

> 本章无 Mermaid 图。集成矩阵见 [[ch-35-graph-stores-compat]]。

## 跨章引用

- 上一章: [[ch-14-knowledge-graph]]
- 下一章: [[ch-19-triplet-store]]