---
title: Graph Stores 适配矩阵 — 4 家
slug: ch-35-graph-stores-compat
part: part-iv-integrations
audience: all
reading_time: 9
prerequisites: [ch-18-graph-store]
semantica_version: 0.6.0
---

# ch-35 Graph Stores 适配矩阵 — 4 家

> 4 家 LPG 图库 + NetworkX 内存图。本章给出 Neo4j / FalkorDB / Apache AGE / Amazon Neptune 的接入步骤与权衡。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 4 家图库统一 facade: Neo4j / 轻量 Redis 一体图库 / Postgres 扩展 / AWS 一体图库。
- NetworkX 单进程内存图 (默认, 测试用)。
- Cypher 查询语言 (AWS 一体图库支持 openCypher / Gremlin / SPARQL)。

### 1.2 适配矩阵

| 后端 | extras | 部署 | 适用场景 |
|---|---|---|---|
| **Neo4j** | `graph-neo4j` | 自托管 / Aura | 业界标准, GDS 算法齐全 |
| **FalkorDB** | `graph-falkordb` | Redis 一体 | 低延迟 / Redis 已有栈 |
| **Apache AGE** | `graph-apache-age` | Postgres 扩展 | 已有 Postgres 栈 |
| **Amazon Neptune** | `graph-amazon-neptune` | AWS 一体 | AWS 多区域部署 |
| **NetworkX** | (内置) | 内存 | 测试 / 原型 (<100k 节点) |

### 1.3 一段最小可跑示例

```python
from semantica.graph_store import GraphStore [[ch-55-glossary]]

# Neo4j
gs = GraphStore(backend="neo4j",
                uri="bolt://localhost:7687",
                user="neo4j", password="password")

# FalkorDB
gs = GraphStore(backend="falkordb", host="localhost", port=6379)

# Apache AGE
gs = GraphStore(backend="age",
                dsn="postgresql://u:p@h/db",
                graph_name="kg")

# Neptune
gs = GraphStore(backend="neptune",
                endpoint="my-neptune.cluster.amazonaws.com",
                port=8182)
```

### 1.4 何时不用

- 节点 < 10k → NetworkX 即可。
- 你已有 Redis → 轻量 Redis 一体图库零额外组件。
- 你要"向量 + 图" 同库 → Qdrant / Neo4j 5+。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/graph_store/neo4j_store.py` — `Neo4jStore`。
- `semantica/graph_store/falkordb_store.py` — `FalkorDBStore`。
- `semantica/graph_store/age_store.py` — `AGEStore` (Apache AGE, 基于 psycopg2)。
- `semantica/graph_store/amazon_neptune.py` — `NeptuneStore` (HTTPS + Bolt)。
- `semantica/graph_store/graph_store.py:524` — 顶层 `GraphStore` 路由。

### 2.2 最小复现脚本

```python
# examples/ch-35-gs-factory.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica.graph_store import GraphStore

# 默认 NetworkX (无需任何服务)
gs = GraphStore(backend="networkx")
print("backend:", gs.backend_name)  # "networkx"
```

### 2.3 已知陷阱

- **Neo4j Aura 免费层**: 限制 50k 节点 + 175k 关系, 超出需付费。
- **FalkorDB**: 强依赖 Redis 版本 ≥ 7.0。
- **Apache AGE**: 需先 `CREATE EXTENSION age;` 且 graph 是 namespace。
- **Neptune**: 私有 VPC, 需 IAM 角色 + 安全组。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 4 家, 不学 Neo4j 一家独大?**
- FalkorDB 适合"Redis 已有栈, 想加图查询"。
- AGE 适合"Postgres 已有栈, 想加图查询"。
- Neptune 适合"AWS 一体化 + 跨区域"。
- 不同客户场景不同, Semantica 兼容并蓄。

### 3.2 与同类对比

| 维度 | Semantica graph_store | LangChain GraphStores | LlamaIndex PropertyGraph |
|---|---|---|---|
| 后端数 | 4 + NetworkX | 5 | 1 (NetworkX) |
| Cypher | ✅ | ⚠ | ⚠ |

### 3.3 何时重新设计

- 节点 > 100M → 必上 Neo4j cluster + sharding。
- 多图联邦 → 引入 federation layer。

## 跨章引用

- 上一章: [[ch-34-vector-stores-compat]]
- 下一章: [[ch-36-triple-stores-compat]]