---
title: RDF 三元组库 (Triplet Store)
slug: ch-19-triplet-store
part: part-ii-core-modules
audience: all
reading_time: 11
prerequisites: [ch-15-ontology]
semantica_version: 0.6.0
---

# ch-19 RDF 三元组库 (Triplet Store)

> 5 个 RDF 三元组库统一接口 (Oxigraph 内置 + Blazegraph/Jena/RDF4J/Anzo 远程 SPARQL)。本章讲解 `TripletStore` + SPARQL 引擎 + BulkLoader。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 把 KG 序列化为 RDF (Turtle / N-Triples / RDF/XML)。
- 跑 SPARQL 1.1 查询 (SELECT / CONSTRUCT / ASK / UPDATE)。
- 远程接入 Blazegraph / Jena / RDF4J / Anzo (走 SPARQL HTTP 协议)。
- 内置 Oxigraph (进程嵌入式, 0 部署)。

### 1.2 一段最小可跑示例

```python
from semantica.triplet_store import TripletStore

# 内置 Oxigraph
ts = TripletStore(backend="oxigraph", path="./data.oxigraph")

ts.add([
    ("<http://ex/Einstein>", "<http://ex/discovered>", "<http://ex/relativity>"),
    ("<http://ex/Einstein>", "<http://ex/type>", "<http://ex/Person>"),
])

# SPARQL
results = ts.query("""
PREFIX ex: <http://ex/>
SELECT ?o WHERE { <http://ex/Einstein> ex:discovered ?o }
""")
for row in results:
    print(row)
```

### 1.3 何时不用

- 你的数据已是 Neo4j 节点/边 → 用 [[ch-18-graph-store]], 不必额外存 RDF。
- 你不需要 SPARQL → 用 LPG 图库即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.triplet_store.TripletStore(backend, **conn_kwargs)
semantica.triplet_store.BulkLoader(ts)
semantica.triplet_store.QueryEngine(ts)
semantica.triplet_store.triplet_store_methods.add_triplets(...)
semantica.triplet_store.triplet_store_methods.query_sparql(...)
semantica.triplet_store.triplet_store_methods.import_rdf(...)
semantica.triplet_store.triplet_store_methods.export_rdf(...)
```

### 2.2 关键代码路径

- `semantica/triplet_store/triplet_store.py` — `TripletStore.add / query / bulk_load`。
- `semantica/triplet_store/oxigraph_store.py` — 进程嵌入式。
- `semantica/triplet_store/sparql_endpoint.py` — Blazegraph / Jena / RDF4J / Anzo HTTP 适配。
- `semantica/triplet_store/bulk_loader.py` — 百万级批量入库。
- `semantica/triplet_store/query_engine.py` — SPARQL 解析 + 模板。

### 2.3 最小复现脚本

```python
# examples/ch-19-triplet-minimal.py mirror
import tempfile, os
from semantica.triplet_store import TripletStore

with tempfile.TemporaryDirectory() as tmp:
    ts = TripletStore(backend="oxigraph", path=os.path.join(tmp, "store"))
    ts.add([("<S>", "<P>", "<O>")])
    print(ts.query("SELECT ?o WHERE { <S> <P> ?o }"))
```

### 2.4 扩展点

- **加新后端**: 继承 `BaseTripletStoreBackend`, 实现 SPARQL Protocol 1.1 兼容接口。
- **加新 RDF 序列化**: 扩 `import_rdf / export_rdf` 支持 JSON-LD / N-Quads / TriG。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 TripletStore 独立于 GraphStore [[ch-55-glossary]]?**
- LPG (节点/边) vs RDF (三元组) 是两种范式, 查询语言、推理能力、标准化程度都不同。
- Semantica 同时支持两者, 允许"图分析用 LPG, 语义 Web 用 RDF"。
- 代价: 数据双写一致性 (KG → LPG + RDF), 由 `ProvenanceManager` 兜底。

### 3.2 与同类对比

| 维度 | Semantica triplet_store | Apache Jena | rdflib |
|---|---|---|---|
| 内置引擎 | ✅ Oxigraph | ❌ | ❌ |
| 远程 SPARQL | ✅ 4 后端 | ✅ | ⚠ |
| Bulk load | ✅ | ✅ | ⚠ |

### 3.3 何时重新设计

- 三元组 > 1B → 拆 cluster (Blazegraph / Stardog)。
- 出现 federation → 引入 SPARQL FEDERATION。

## 本章图表

> 本章无 Mermaid 图。集成矩阵见 [[ch-36-triple-stores-compat]]。

## 跨章引用

- 上一章: [[ch-15-ontology]] / [[ch-18-graph-store]]
- 下一章: [[ch-20-provenance]]