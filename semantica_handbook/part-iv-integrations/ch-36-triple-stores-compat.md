---
title: Triple Stores 适配矩阵 — 5 家
slug: ch-36-triple-stores-compat
part: part-iv-integrations
audience: all
reading_time: 9
prerequisites: [ch-19-triplet-store]
semantica_version: 0.6.0
---

# ch-36 Triple Stores 适配矩阵 — 5 家

> 5 家 RDF 三元组库统一接口 (Oxigraph / Blazegraph / Apache Jena / Eclipse RDF4J / Cambridge Semantics Anzo)。本章给出 SPARQL 1.1 兼容矩阵与部署选择。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 5 家 RDF 三元组库统一 facade。
- 进程嵌入式 Oxigraph (默认, 0 部署)。
- 远程 SPARQL HTTP 协议接入其它 4 家。

### 1.2 适配矩阵

| 后端 | extras | 部署 | 适用场景 |
|---|---|---|---|
| **Oxigraph** | `tripletstore-oxigraph` | 进程嵌入式 | 单机 / 原型 / 测试 |
| **Blazegraph** | (SPARQL HTTP) | 自托管 / AWS | 大规模 (10B+ 三元组) |
| **Apache Jena Fuseki** | (SPARQL HTTP) | 自托管 | 学术 / 工业标准 |
| **Eclipse RDF4J** | (SPARQL HTTP) | 自托管 / 商业 | 企业级 + SHACL 强 |
| **Cambridge Semantics Anzo** | (SPARQL HTTP) | 商业 | 企业级 + BI 整合 |

### 1.3 一段最小可跑示例

```python
from semantica.triplet_store import TripletStore

# 默认 Oxigraph (本地文件)
ts = TripletStore(backend="oxigraph", path="./kg.oxigraph")

# 远程 SPARQL
ts = TripletStore(backend="blazegraph", url="http://localhost:9999/blazegraph")
ts = TripletStore(backend="jena", url="http://localhost:3030/kg/sparql")
ts = TripletStore(backend="rdf4j", url="http://localhost:8080/rdf4j-server/repositories/kg")
```

### 1.4 何时不用

- 你不需要 RDF/SPARQL → 用 [[ch-35-graph-stores-compat]]。
- 数据 < 100k 三元组 → 跳过 RDF, 直接用 LPG。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/triplet_store/oxigraph_store.py` — `OxigraphStore` (进程嵌入)。
- `semantica/triplet_store/sparql_endpoint.py` — 通用 SPARQL HTTP 适配。
- `semantica/triplet_store/bulk_loader.py` — 批量入库。
- `semantica/triplet_store/query_engine.py` — SPARQL 解析与执行。

### 2.2 最小复现脚本

```python
# examples/ch-36-ts-factory.py mirror
import os, tempfile
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica.triplet_store import TripletStore

with tempfile.TemporaryDirectory() as tmp:
    ts = TripletStore(backend="oxigraph", path=f"{tmp}/store")
    ts.add([("<S>", "<P>", "<O>")])
    rows = ts.query("SELECT ?o WHERE { <S> <P> ?o }")
    print("hits:", len(list(rows)))
```

### 2.3 已知陷阱

- **SPARQL 方言差异**: 各家 SPARQL 1.1 实现差异 (e.g., property paths 在 Fuseki / Blazegraph 表现不一)。
- **Oxigraph 嵌入式**: 多线程不安全, 需 GIL 保护或独立进程。
- **Blazegraph 退役**: 2024 年起社区活跃度下降, 长期建议 Stardog / GraphDB。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 SPARQL 是事实标准, 而非自研查询语言?**
- SPARQL 1.1 是 W3C 标准, 几乎所有 RDF 库都支持。
- 用户可以"用 Semantica 写入, 用 Apache Jena Studio 查询"。

### 3.2 与同类对比

| 维度 | Semantica triplet_store | rdflib | Owlready2 |
|---|---|---|---|
| 内置引擎 | ✅ Oxigraph | ❌ | ❌ |
| 远程 SPARQL | ✅ 4 后端 | ⚠ 弱 | ❌ |
| Bulk load | ✅ | ⚠ | ❌ |

### 3.3 何时重新设计

- 三元组 > 1B → 切 Stardog / GraphDB / Anzo (商业级)。
- 多知识库联邦 → SPARQL FEDERATION。

## 跨章引用

- 上一章: [[ch-35-graph-stores-compat]]
- 下一章: [[ch-37-data-sources]]