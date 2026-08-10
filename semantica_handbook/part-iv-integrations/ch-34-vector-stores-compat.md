---
title: Vector Stores 适配矩阵 — 7 家
slug: ch-34-vector-stores-compat
part: part-iv-integrations
audience: all
reading_time: 10
prerequisites: [ch-17-vector-store]
semantica_version: 0.6.0
---

# ch-34 Vector Stores 适配矩阵 — 7 家

> 一行切换向量库后端。本章给出 7 家向量库的适配矩阵 + 接入步骤 + 已知陷阱。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 7 家向量库统一 facade: FAISS / Qdrant / Weaviate / Pinecone / Milvus / pgvector / sqlite-vec。
- 单测用 FAISS / sqlite-vec (本地 0 部署)。
- 生产用 Qdrant / Weaviate / Pinecone / Milvus (集群)。
- pgvector 用于"已有 Postgres 栈"。

### 1.2 适配矩阵

| 后端 | extras | 部署 | 适用场景 | 索引 |
|---|---|---|---|---|
| **FAISS** | `vectorstore-faiss` (默认) | 单机文件 | 原型 / 小数据 | IVF / HNSW |
| **Qdrant** | `vectorstore-qdrant` | 自托管 / Qdrant Cloud | 中规模 / 过滤 | HNSW / Scalar |
| **Weaviate** | `vectorstore-weaviate` | 自托管 / WCD | 多模态 / GraphQL | HNSW |
| **Pinecone** | `vectorstore-pinecone` | Serverless (AWS) | 免运维 / 全球分布 | Pod-based |
| **Milvus** | `vectorstore-milvus` | 自托管 / Zilliz | 大规模 / GPU 加速 | IVF / HNSW / ANNOY |
| **pgvector** | `vectorstore-pgvector` | 已有 Postgres | 单 DB 多模 | IVFFlat / HNSW |
| **sqlite-vec** | `vectorstore-sqlite` | 单机文件 | 嵌入式 / 测试 | Flat |

### 1.3 一段最小可跑示例

```python
from semantica.vector_store import VectorStore

# 本地 FAISS (默认, 0 部署)
vs = VectorStore(backend="faiss", dim=768, index_path="./v.faiss")

# Qdrant (需启动 qdrant 服务)
vs = VectorStore(backend="qdrant", url="http://localhost:6333", collection="kg")

# Pinecone
vs = VectorStore(backend="pinecone", api_key="...", index="kg-prod")

# pgvector
vs = VectorStore(backend="pgvector", dsn="postgresql://u:p@h/db")
```

### 1.4 何时不用

- 数据量 < 10k 向量 → 直接用 FAISS。
- 你要"向量 + 图谱"双写一致性 → 用 Qdrant (内置 payload 过滤 + 图遍历)。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/vector_store/faiss_store.py` — `FAISSStore`。
- `semantica/vector_store/qdrant_store.py` — `QdrantStore`。
- `semantica/vector_store/weaviate_store.py` — `WeaviateStore`。
- `semantica/vector_store/pinecone_store.py` — `PineconeStore`。
- `semantica/vector_store/milvus_store.py` — `MilvusStore`。
- `semantica/vector_store/pgvector_store.py` — `PGVectorStore`。
- `semantica/vector_store/sqlite_vec_store.py` — `SQLiteVecStore`。
- `semantica/vector_store/vector_store.py:100` — `VectorStore` 主类 (路由 + 缓存)。
- `semantica/vector_store/hybrid_search.py` — RRF 融合。

### 2.2 最小复现脚本

```python
# examples/ch-34-vs-factory.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica.vector_store import VectorStore

# 不指定 backend → 默认 FAISS
vs = VectorStore(dim=4)
print("backend:", vs.backend_name)  # "faiss"
```

### 2.3 已知陷阱

- **FAISS 序列化**: `index_path` 必填, 否则只 in-memory 不持久化。
- **Qdrant collection**: 首次写入会自动创建 collection, 但 collection params (dim/distance) 不可改。
- **Pinecone quota**: Serverless 免费层 100k 向量, 超出需付费。
- **Milvus 连接**: 需同时指定 host + port, 默认 19530。
- **pgvector extension**: 需先 `CREATE EXTENSION vector;`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 7 个后端, 不做"一个万能后端"?**
- 各家索引算法 (HNSW / IVF / ANNOY) 性能差异大, 强求统一会牺牲性能。
- 部署形态差异 (Serverless vs 自托管) 不允许一个抽象包揽。

### 3.2 与同类对比

| 维度 | Semantica vector_store | LangChain VectorStores | LlamaIndex VectorStores |
|---|---|---|---|
| 后端数 | 7 | 20+ | 20+ |
| 混合检索 | ✅ RRF | ⚠ EnsembleRetriever | ⚠ |
| 决策嵌入 | ✅ | ❌ | ❌ |

### 3.3 何时重新设计

- 文档数 > 100M → 必上 Pinecone / Milvus 集群版 + 分片。
- 多模态向量 → 加 CLIP / BLIP embedding 通道。

## 跨章引用

- 上一章: [[ch-33-llm-providers]]
- 下一章: [[ch-35-graph-stores-compat]]