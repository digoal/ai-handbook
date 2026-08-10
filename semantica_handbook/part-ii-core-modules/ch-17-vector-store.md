---
title: 向量库适配 (Vector Store)
slug: ch-17-vector-store
part: part-ii-core-modules
audience: all
reading_time: 12
prerequisites: [ch-13-embeddings]
semantica_version: 0.6.0
---

# ch-17 向量库适配 (Vector Store)

> 7 家向量库统一接口 (FAISS / Qdrant / Weaviate / Pinecone / Milvus / pgvector / sqlite-vec)。本章讲解 `VectorStore` + HybridSearch [[ch-55-glossary]] (RRF 融合)。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 一行切换 7 家向量库后端。
- 混合检索 (dense + sparse + metadata) + RRF 融合。
- 决策嵌入 (decision embedding) 一等公民。
- 索引自动选择 (IVF / HNSW / Flat) + 量化。

### 1.2 一段最小可跑示例

```python
from semantica.vector_store import VectorStore

# 默认 FAISS (本地文件)
vs = VectorStore(backend="faiss", dim=768, index_path="./vectors.faiss")

# 上传
vs.add_documents([
    {"id": "d1", "text": "Einstein discovered relativity", "vector": [...], "metadata": {...}},
    {"id": "d2", "text": "Bohr debated quantum mechanics", "vector": [...], "metadata": {...}},
])

# 检索
hits = vs.search(query_vector=[...], top_k=5)
print(hits)
```

切换后端: `backend="qdrant"` / `"weaviate"` / `"pinecone"` / `"milvus"` / `"pgvector"` / `"sqlite-vec"` 即可, API 不变。

### 1.3 何时不用

- 你不需要 ANN 检索 → 直接用 NetworkX / Postgres tsvector。
- 数据 < 1k 向量 → sklearn NearestNeighbors 即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.vector_store.VectorStore(backend, dim, index_path)
semantica.vector_store.VectorIndexer()
semantica.vector_store.HybridSearch()
semantica.vector_store.vector_store_methods.store_vectors(...)
semantica.vector_store.vector_store_methods.search_vectors(...)
semantica.vector_store.vector_store_methods.update_vectors(...)
semantica.vector_store.vector_store_methods.delete_vectors(...)
semantica.vector_store.vector_store_methods.create_index(...)
semantica.vector_store.vector_store_methods.hybrid_search(...)
```

### 2.2 关键代码路径

- `semantica/vector_store/vector_store.py:100` — `VectorStore` 主类。
- `semantica/vector_store/vector_store.py:334` — `add_documents`。
- `semantica/vector_store/vector_store.py:645` — `search`。
- `semantica/vector_store/vector_store.py:663` — `search_vectors`。
- `semantica/vector_store/vector_store.py:738` — `update_vectors`。
- `semantica/vector_store/vector_store.py:767` — `delete_vectors`。
- `semantica/vector_store/vector_store.py:1249` — `VectorIndexer`。
- `semantica/vector_store/methods.py:149` — `store_vectors`。
- `semantica/vector_store/methods.py:177` — `search_vectors`。
- `semantica/vector_store/methods.py:304` — `hybrid_search`。
- `semantica/vector_store/hybrid_search.py` — `RRF` (Reciprocal Rank Fusion)。
- 后端实现: `faiss_store.py / qdrant_store.py / weaviate_store.py / pinecone_store.py / milvus_store.py / pgvector_store.py / sqlite_vec_store.py`。

### 2.3 最小复现脚本

```python
# examples/ch-17-vector-minimal.py mirror
import numpy as np
from semantica.vector_store import VectorStore

vs = VectorStore(backend="faiss", dim=4)
vs.add_documents([
    {"id": "a", "vector": np.random.rand(4).tolist(), "metadata": {"k": 1}},
    {"id": "b", "vector": np.random.rand(4).tolist(), "metadata": {"k": 2}},
])
hits = vs.search(query_vector=np.random.rand(4).tolist(), top_k=2)
print(hits)
```

### 2.4 扩展点

- **加新后端**: 继承 `BaseVectorStoreBackend`, 注册到 `VectorStore._backend_registry`。
- **加新融合策略**: 扩 `HybridSearch` 支持 weighted_concat / borda_count / distribution_based。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 dense + sparse + metadata 三源混合?**
- dense (语义) 召回"看起来像", sparse (BM25) 召回"字面像", metadata 召回"标签像"。三者互补。
- RRF 融合不调权重, 对新用户友好。
- 代价: 索引成本 3 倍, 检索延迟 +50%。

### 3.2 与同类对比

| 维度 | Semantica vector_store | LangChain VectorStores | LlamaIndex VectorStores |
|---|---|---|---|
| 后端数 | 7 | 20+ | 20+ |
| 混合检索 | ✅ RRF | ⚠ EnsembleRetriever | ⚠ |
| 决策嵌入 | ✅ | ❌ | ❌ |

### 3.3 何时重新设计

- 文档数 > 10M → 必上 Pinecone / Milvus 集群版。
- 多模态 → 扩 multimodal vector。

## 本章图表

> 本章无 Mermaid 图。集成矩阵见 [[ch-34-vector-stores-compat]]。

## 跨章引用

- 上一章: [[ch-13-embeddings]]
- 下一章: [[ch-18-graph-store]]
- 数据流位置: [[ch-04-architecture-30kft]] FIG-02 第 11 步