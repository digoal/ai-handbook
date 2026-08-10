---
title: 去重 (Deduplication) — 精确/模糊/语义
slug: ch-22-deduplication
part: part-ii-core-modules
audience: all
reading_time: 8
prerequisites: [ch-12-semantic-extract]
semantica_version: 0.6.0
---

# ch-22 去重 (Deduplication)

> 把"看起来一样的"实体合并。本章讲解精确 / 模糊 / 语义三种去重策略 + 三种合并动作。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 精确去重: 完全相同 `id` / 完全相同 `(name, type)`。
- 模糊去重: Levenshtein / Jaroard 距离 < 阈值。
- 语义去重: 嵌入余弦相似度 > 阈值。
- 合并策略: `first` / `latest` / `merge` / `voting`。
- 输出 `merged_entity` + 决策记录。

### 1.2 一段最小可跑示例

```python
from semantica.deduplication.methods import detect_duplicates, merge_entities, deduplicate_triplets

entities = [
    {"id": "p1", "name": "Albert Einstein", "type": "PERSON"},
    {"id": "p2", "name": "Einstein, A.", "type": "PERSON"},
    {"id": "p3", "name": "Isaac Newton", "type": "PERSON"},
]

dups = detect_duplicates(entities, strategy="semantic", threshold=0.85)
# -> [(p1, p2)]  (p3 不在 dup 对中)

merged = merge_entities(entities, duplicates=dups, strategy="merge")
print(merged)  # 1 个规范实体 + provenance
```

### 1.3 何时不用

- 你的实体天然唯一 (有外部 ID, 如 ORCID / DOI) → 跳过 dedup。
- 数据量 < 1k → 手工 dedup 即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.deduplication.methods.detect_duplicates(entities, strategy, threshold)
semantica.deduplication.methods.deduplicate_triplets(triplets, ...)
semantica.deduplication.methods.merge_entities(entities, duplicates, strategy)
semantica.deduplication.methods.build_clusters(entities, similarity_matrix)
semantica.deduplication.EntityMerger()
semantica.deduplication.SimilarityCalculator()
semantica.deduplication.ClusterBuilder()
semantica.deduplication.MergeStrategy()
```

### 2.2 关键代码路径

- `semantica/deduplication/methods.py:201` — `detect_duplicates`。
- `semantica/deduplication/methods.py:264` — `deduplicate_triplets`。
- `semantica/deduplication/methods.py:296` — `merge_entities`。
- `semantica/deduplication/methods.py:345` — `build_clusters`。
- `semantica/deduplication/cluster_builder.py` — 相似度图 → 社区检测。
- `semantica/deduplication/entity_merger.py` — 合并 + 冲突字段选择。
- `semantica/deduplication/similarity_calculator.py` — 3 种相似度。
- `semantica/deduplication/merge_strategy.py` — 4 种合并策略。

### 2.3 最小复现脚本

```python
# examples/ch-22-dedup-minimal.py mirror
from semantica.deduplication.methods import detect_duplicates, merge_entities

ents = [{"id": "a", "name": "Albert Einstein", "type": "PERSON"},
        {"id": "b", "name": "Einstein", "type": "PERSON"}]

dups = detect_duplicates(ents, strategy="fuzzy", threshold=0.8)
print("Duplicates:", dups)
print("Merged:", merge_entities(ents, duplicates=dups, strategy="merge"))
```

### 2.4 扩展点

- **加新相似度**: 扩 `SimilarityCalculator._strategies`。
- **加新合并策略**: 在 `MergeStrategy._actions` 加分支。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 dedup 与 conflict 拆开?**
- dedup 是"实体合并" (一对多 → 一), conflict 是"事实冲突" (同一对实体的某字段矛盾)。
- 两者都可能产生新节点, 但前者更常用, 后者只在多源融合场景出现。

### 3.2 与同类对比

| 维度 | Semantica dedup | Dedupe.io | spaCy EntityLinker |
|---|---|---|---|
| 策略数 | 3 (exact/fuzzy/semantic) | 5 | 1 |
| 合并动作 | 4 (first/latest/merge/voting) | 3 | 2 |

### 3.3 何时重新设计

- 实体数 > 10M → 必上 blocking + LSH (局部敏感哈希)。
- 出现多模态实体对齐 → 加 CLIP embedding 通道。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-21-context-decision]]
- 下一章: [[ch-23-conflicts]]
- 主轴 B: [[ch-41-flow-b-multi-source]]