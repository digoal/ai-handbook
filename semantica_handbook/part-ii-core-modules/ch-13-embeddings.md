---
title: Embedding 抽象层
slug: ch-13-embeddings
part: part-ii-core-modules
audience: all
reading_time: 11
prerequisites: [ch-12-semantic-extract]
semantica_version: 0.6.0
---

# ch-13 Embedding 抽象层

> 把"任意文本 / 图节点 / 向量"嵌入到统一空间。本章讲解 `EmbeddingGenerator` + 5 种 provider + 5 种 pooling 策略。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 8 家 LLM/Embedding provider 统一接口 (OpenAI / BGE / FastEmbed / Llama / HF / Cohere / Voyage / Mistral)。
- 5 种 pooling: Mean / Max / CLS / Attention / Hierarchical。
- 批量嵌入 + 增量更新 + 跨实体相似度计算。

### 1.2 一段最小可跑示例

```python
from semantica.embeddings import EmbeddingGenerator

gen = EmbeddingGenerator(provider="openai", model="text-embedding-3-large")

vecs = gen.generate_embeddings(["Einstein discovered relativity.",
                                "He later won the Nobel Prize."])

sim = gen.compare_embeddings(vecs[0], vecs[1])
print(f"cosine sim = {sim:.4f}")
```

### 1.3 何时不用

- 你已经有自己的 embedding pipeline → 跳过本模块, 直接入 vector_store。
- 你的语料极少 (<100 文档) → 用 sklearn TF-IDF 即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.embeddings.EmbeddingGenerator(provider, model, ...)
semantica.embeddings.embed_text(text, provider, model)             # 函数式
semantica.embeddings.calculate_similarity(vec_a, vec_b, metric="cosine")
semantica.embeddings.pool_embeddings(vecs, strategy="mean")
semantica.embeddings.check_available_providers()
semantica.embeddings.GraphEmbeddingManager()
semantica.embeddings.VectorEmbeddingManager()
```

### 2.2 关键代码路径

- `semantica/embeddings/embedding_generator.py:56` — `EmbeddingGenerator` 主类。
- `semantica/embeddings/embedding_generator.py:135` — `generate_embeddings`。
- `semantica/embeddings/embedding_generator.py:217` — `compare_embeddings`。
- `semantica/embeddings/embedding_generator.py:260` — `process_batch`。
- `semantica/embeddings/methods.py:92` — `generate_embeddings` facade。
- `semantica/embeddings/methods.py:143` — `embed_text`。
- `semantica/embeddings/methods.py:203` — `calculate_similarity`。
- `semantica/embeddings/methods.py:248` — `pool_embeddings`。
- `semantica/embeddings/methods.py:331` — `check_available_providers`。
- `semantica/embeddings/provider_stores.py` — `OpenAIStore / BGEStore / FastEmbedStore / LlamaStore`。

### 2.3 最小复现脚本

```python
# examples/ch-13-embed-minimal.py mirror
from semantica.embeddings import EmbeddingGenerator

# 仅在装了 hf extras 时可用
gen = EmbeddingGenerator(provider="huggingface", model="sentence-transformers/all-MiniLM-L6-v2")
vecs = gen.generate_embeddings(["hello world", "good morning"])
print(f"dim={len(vecs[0])} sim={gen.compare_embeddings(vecs[0], vecs[1]):.4f}")
```

### 2.4 扩展点

- **加新 provider**: 继承 `BaseEmbedder.generate / compare / pool`, 在 `provider_stores.py` 注册。
- **加新 pooling 策略**: 在 `pool_embeddings(strategy="my_strategy")` 加分支。
- **加新相似度指标**: 扩 `compare_embeddings(metric=...)`, 支持 euclidean / manhattan / dot / cosine。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 pooling 在 embedding 层, 而不是在 vector_store 层?**
- 不同 pooling 产生的向量"语义"不同 (mean vs cls), 在 vector 层做 pooling 会让存储语义模糊。
- 在 embedding 层固化 pooling, 让 vector_store 只关心"存 + 检索"。
- 代价: 同一文本换 pooling 必须重新嵌入, 不能在 vector_store 端切换。

### 3.2 与同类对比

| 维度 | Semantica embeddings | LangChain Embeddings | LlamaIndex Embeddings |
|---|---|---|---|
| Provider 数 | 8 (内置) + extras 扩展 | 30+ | 30+ |
| Pooling | ✅ 5 策略 | ❌ | ❌ |
| 图节点嵌入 | ✅ GraphEmbeddingManager | ❌ | ❌ |

### 3.3 何时重新设计

- 引入 "异步预嵌入" pipeline → 加 `EmbeddingScheduler`, 配合 `pipeline.PipelineBuilder`。
- 多语种混合 → 加 `multilingual_pooling` (加权 mean per language)。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-12-semantic-extract]]
- 下一章: [[ch-14-knowledge-graph]]
- LLM provider 适配: [[ch-33-llm-providers]]