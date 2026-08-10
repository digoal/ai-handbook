---
title: 变更管理 (Change Management) — 版本 / 回滚 / 时序
slug: ch-25-change-management
part: part-ii-core-modules
audience: all
reading_time: 9
prerequisites: [ch-14-knowledge-graph]
semantica_version: 0.6.0
---

# ch-25 变更管理 (Change Management) — 版本 / 回滚 / 时序

> 让 KG 像 Git 一样可版本化、可 diff、可回滚。本章讲解 `EnhancedVersionManager` + `SQLiteVersionStorage` + checksum 校验。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- KG snapshot (commit): 任意时刻冻结一张图, 给个 commit_id。
- diff: 比对两个 commit_id 的实体/边差异。
- rollback: 把图恢复到某 commit_id 状态。
- 时序版本: `BiTemporalFact` 区分 valid_time (业务时间) 与 recorded_at (记录时间)。
- checksum 校验: 检测 commit 是否被篡改。

### 1.2 一段最小可跑示例

```python
from semantica.change_management import EnhancedVersionManager, SQLiteVersionStorage

storage = SQLiteVersionStorage("./kg_versions.db")
mgr = EnhancedVersionManager(storage)

# commit
v1 = mgr.commit(graph=v1_kg, message="initial ingest")
v2 = mgr.commit(graph=v2_kg, message="add 10 entities")

# diff
diff = mgr.diff(v1, v2)
print(f"Added nodes: {diff.added_nodes}")

# rollback
mgr.rollback(v1)
```

### 1.3 何时不用

- 你的 KG 是只读的 → 跳过 change_management。
- 你用 Neo4j 5+ 时态功能 → 用 Neo4j 内置, 不必额外版本层。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.change_management.SQLiteVersionStorage(path)
semantica.change_management.InMemoryVersionStorage()
semantica.change_management.EnhancedVersionManager(storage)
semantica.change_management.EnhancedTemporalVersionManager(storage)
semantica.change_management.OntologyVersionManager(...)
semantica.change_management.compute_checksum(graph)
semantica.change_management.verify_checksum(graph, expected)
```

### 2.2 关键代码路径

- `semantica/change_management/sqlite_version_storage.py` — 默认 SQLite 存储。
- `semantica/change_management/in_memory_version_storage.py` — 内存 (测试用)。
- `semantica/change_management/enhanced_version_manager.py` — `EnhancedVersionManager.commit / diff / rollback`。
- `semantica/change_management/temporal_version_manager.py` — `BiTemporalFact` 双时态。
- `semantica/change_management/ontology_version_manager.py` — 本体版本管理。

### 2.3 最小复现脚本

```python
# examples/ch-25-versioning-minimal.py mirror
import tempfile, networkx as nx
from semantica.change_management import (
    EnhancedVersionManager, SQLiteVersionStorage, compute_checksum, verify_checksum,
)

with tempfile.TemporaryDirectory() as tmp:
    storage = SQLiteVersionStorage(f"{tmp}/v.db")
    mgr = EnhancedVersionManager(storage)
    g = nx.DiGraph(); g.add_node("a")
    v = mgr.commit(graph=g, message="first")
    print("checksum:", compute_checksum(g))
    print("verify:", verify_checksum(g, compute_checksum(g)))
```

### 2.4 扩展点

- **加新存储后端**: 继承 `BaseVersionStorage`, 实现 `put / get / list`。
- **加 diff 策略**: 扩 `EnhancedVersionManager.diff(method=...)` 支持 RDF diff / JSON Patch。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么双时态 (BiTemporal)?**
- valid_time: 业务事件真实发生时间 (e.g., "贷款在 2024-01-01 获批")。
- recorded_at: 系统记录时间 (e.g., "我们在 2024-01-15 入库")。
- 双时态让"晚到的真相"也能正确归档 (2024-01-01 发生的事, 2024-02-01 才被记录)。

### 3.2 与同类对比

| 维度 | Semantica change_management | Git (LFS) | DVC | Neo4j 5 时态 |
|---|---|---|---|---|
| 双时态 | ✅ | ❌ | ❌ | ✅ |
| Diff 算法 | node/edge set diff | blob diff | blob diff | time-tree |
| Checksum | ✅ | ✅ (sha) | ✅ | ⚠ |

### 3.3 何时重新设计

- 提交频率 > 1k/天 → 引入增量提交 (delta commit)。
- 多团队协作 → 引入 branch + merge。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-24-pipeline]]
- 下一章: [[ch-26-visualization-export]]
- 时序图: [[ch-14-knowledge-graph]] § 时序小节