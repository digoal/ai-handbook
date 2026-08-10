---
title: 分块 (Split) — Graph-aware chunking
slug: ch-11-split
part: part-ii-core-modules
audience: all
reading_time: 9
prerequisites: [ch-10-normalize]
semantica_version: 0.6.0
---

# ch-11 分块 (Split)

> 把"干净文本"切成下游 NER / 嵌入 直接消费的 chunk。本章讲解 7 种分块策略, 含 GraphRAG 友好的 graph-aware 切片。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 7 种 chunker 选其一: `FixedChunker / SentenceChunker / SemanticChunker / GraphAwareChunker [[ch-55-glossary]] / EntityAwareChunker / RelationAwareChunker / HierarchicalChunker`。
- 在 GraphRAG 场景, 用 `GraphAwareChunker` 让 chunk 边界贴合"实体提及范围"。
- 设置 chunk_size / overlap / boundary_respect。

### 1.2 一段最小可跑示例

```python
from semantica.split import (
    FixedChunker, GraphAwareChunker, HierarchicalChunker,
)

text = "Einstein discovered relativity in 1905. He later won the Nobel Prize..."

# 固定大小
chunks = FixedChunker(chunk_size=256, overlap=32).split(text)

# Graph-aware (实体边界)
chunks = GraphAwareChunker(strategy="entity_boundary").split(text)

# 层级 chunk (parent → child)
chunks = HierarchicalChunker(parent_size=2048, child_size=256).split(text)
```

### 1.3 何时不用

- **纯 RAG, 不要 GraphRAG**: `FixedChunker` 就够。
- **你的语料全是表格 / SQL 行**: 不必 split, 整行作为 chunk。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.split.FixedChunker(chunk_size, overlap)               # 字符固定窗口
semantica.split.SentenceChunker(max_sentences=5)                # 句子边界
semantica.split.SemanticChunker(similarity_threshold=0.7)       # 嵌入相似度
semantica.split.GraphAwareChunker(strategy="entity_boundary")   # 实体边界
semantica.split.EntityAwareChunker()                            # 实体共现
semantica.split.RelationAwareChunker()                          # 主谓宾边界
semantica.split.HierarchicalChunker(parent_size, child_size)    # 双层
```

### 2.2 关键代码路径

- `semantica/split/__init__.py` — 7 个 chunker export。
- `semantica/split/fixed_chunker.py` — 基于字符 offset。
- `semantica/split/sentence_chunker.py` — 基于 NLTK / spaCy。
- `semantica/split/semantic_chunker.py` — 基于嵌入相似度。
- `semantica/split/graph_aware_chunker.py` — `entity_boundary / relation_boundary / community_boundary` 三策略。
- `semantica/split/hierarchical_chunker.py` — 父→子递归。

### 2.3 最小复现脚本

```python
# examples/ch-11-split-minimal.py mirror
from semantica.split import FixedChunker, GraphAwareChunker

text = open("./README.md").read()

fixed = FixedChunker(chunk_size=512, overlap=64).split(text)
graph = GraphAwareChunker(strategy="entity_boundary").split(text)

print(f"Fixed: {len(fixed)} chunks; Graph: {len(graph)} chunks")
```

### 2.4 扩展点

- **自定义 chunker**: 继承 `BaseChunker.split(text) -> list[Chunk]`, 注册到 `split.registry`。
- **加新 boundary 策略**: 在 `GraphAwareChunker.strategy` 加值, 在 `graph_aware_chunker.py:_strategy_router` 分支。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 GraphRAG 需要 graph-aware chunking?**
- 固定窗口会把"实体 A → 实体 B"切到两个 chunk, 导致下游 NER 把它们当孤立实体, 丢失关系。
- GraphAwareChunker 用 NER 预标注 + 句子级共现检测, 让 chunk 边界贴在"实体提及的完整窗口"上。
- 代价: 第一遍 NER 预标注耗时, 但下游准确率显著提升 (Cookbook 12 vs 13 对照)。

### 3.2 与同类对比

| 维度 | Semantica split | LangChain TextSplitters | LlamaIndex SentenceSplitter |
|---|---|---|---|
| Chunker 数 | 7 | 8 | 4 |
| Graph-aware | ✅ 3 策略 | ❌ | ❌ |
| Hierarchical | ✅ | ⚠ 仅 ParentDocument | ⚠ |

### 3.3 何时重新设计

- chunker 数 > 12 → 拆 `split-fixed` / `split-graph-aware` 子包。
- 用户 GraphRAG 命中率 < 60% → 引入社区检测 (louvain) 自动 chunk。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-10-normalize]]
- 下一章: [[ch-12-semantic-extract]]
- 数据流位置: [[ch-04-architecture-30kft]] FIG-02 第 5 步