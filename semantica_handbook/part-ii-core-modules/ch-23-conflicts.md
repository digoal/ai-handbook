---
title: 冲突检测与解决 (Conflicts)
slug: ch-23-conflicts
part: part-ii-core-modules
audience: all
reading_time: 9
prerequisites: [ch-22-deduplication]
semantica_version: 0.6.0
---

# ch-23 冲突检测与解决 (Conflicts)

> 多源数据冲突是常态。本章讲解 5 类冲突检测 + 投票/优先级/手动 三种解决策略 + 调查向导。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 检测 5 类冲突: value / type / temporal / relationship / logical。
- 解决策略: `voting` / `latest_wins` / `priority_source` / `manual`。
- 生成"调查向导" — 列出每个冲突的最可能真相, 等待人工裁定。
- 追踪冲突来源 (`track_sources`) — 谁说 A、谁说 B。

### 1.2 一段最小可跑示例

```python
from semantica.conflicts.methods import detect_conflicts, resolve_conflicts, generate_investigation_guide

sources = [
    {"source": "doc1.pdf", "claims": [{"subject": "Acme", "predicate": "revenue", "object": "10M"}]},
    {"source": "doc2.pdf", "claims": [{"subject": "Acme", "predicate": "revenue", "object": "12M"}]},
]

conflicts = detect_conflicts(sources)
# -> [{'type': 'value', 'predicate': 'revenue', 'values': ['10M', '12M'], 'sources': ['doc1.pdf', 'doc2.pdf']}]

resolved = resolve_conflicts(conflicts, strategy="voting")
guide = generate_investigation_guide(conflicts)
print(guide)
```

### 1.3 何时不用

- 单源数据 → 无冲突可言。
- 你的源数据已统一 (同一份 Snowflake 表) → 在 SQL 层去重即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.conflicts.methods.detect_conflicts(sources)
semantica.conflicts.methods.resolve_conflicts(conflicts, strategy)
semantica.conflicts.methods.analyze_conflicts(conflicts)
semantica.conflicts.methods.track_sources(claim)
semantica.conflicts.methods.generate_investigation_guide(conflicts)
semantica.conflicts.ConflictDetector()
semantica.conflicts.ConflictResolver()
semantica.conflicts.SourceTracker()
```

### 2.2 关键代码路径

- `semantica/conflicts/methods.py:130` — `detect_conflicts`。
- `semantica/conflicts/methods.py:201` — `resolve_conflicts`。
- `semantica/conflicts/methods.py:259` — `analyze_conflicts`。
- `semantica/conflicts/methods.py:313` — `track_sources`。
- `semantica/conflicts/methods.py:399` — `generate_investigation_guide`。

### 2.3 最小复现脚本

```python
# examples/ch-23-conflict-minimal.py mirror
from semantica.conflicts.methods import detect_conflicts, resolve_conflicts

src = [
    {"source": "A", "claims": [{"subject": "x", "predicate": "y", "object": "1"}]},
    {"source": "B", "claims": [{"subject": "x", "predicate": "y", "object": "2"}]},
]

c = detect_conflicts(src)
print("Conflicts:", c)
print("Resolved (voting):", resolve_conflicts(c, strategy="voting"))
```

### 2.4 扩展点

- **加新冲突类型**: 扩 `ConflictDetector._detectors`。
- **加新解决策略**: 在 `ConflictResolver._strategies` 注册。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 5 类而不是 1 类 "value conflict"?**
- value (数值冲突) / type (类型冲突) / temporal (时间冲突) / relationship (关系冲突) / logical (逻辑矛盾, 如 P→¬P)。
- 单一 value 会让"X 是 Person vs X 是 Organization"无法表达。

### 3.2 与同类对比

| 维度 | Semantica conflicts | Great Expectations | Deequ |
|---|---|---|---|
| 冲突类型 | 5 (含逻辑) | 主要 schema | 主要统计 |
| 解决策略 | 4 | 1 (fail) | 1 (report) |
| 调查向导 | ✅ | ❌ | ❌ |

### 3.3 何时重新设计

- 冲突数 > 100k → 引入冲突聚类 (相同 predicate 聚合)。
- 出现"跨 schema 冲突" → 加 schema 映射层。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-22-deduplication]]
- 下一章: [[ch-24-pipeline]]