---
title: 溯源 (Provenance) — W3C PROV-O
slug: ch-20-provenance
part: part-ii-core-modules
audience: all
reading_time: 11
prerequisites: [ch-05-data-models]
semantica_version: 0.6.0
---

# ch-20 溯源 (Provenance) — W3C PROV-O

> 让每个实体/边/决策都可问"哪里来"。本章讲解 `ProvenanceManager` + L1/L2/L3 桥接公理 + W3C PROV-O 导出。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 记录每个 Entity / Relationship / Chunk / Decision 的来源 (chunk_id → extractor_id → model_version → timestamp)。
- 反向追溯: 问"这个实体是从哪些文档的哪一行抽出来的"。
- 正向追溯: 问"这个 chunk 产出了哪些实体"。
- 导出 W3C PROV-O (Turtle / JSON) 给监管方。
- 完整性校验 (checksum) — 检测数据被篡改。

### 1.2 一段最小可跑示例

```python
from semantica.provenance import ProvenanceManager

pm = ProvenanceManager(storage_path="./provenance.db")

# 记录
chunk_ref = pm.track_chunk(text="Einstein discovered relativity.",
                            source_doc="paper.pdf", offset=42, length=128)
entity_ref = pm.track_entity(entity_id="e1", name="Einstein", type="PERSON",
                              chunk_refs=[chunk_ref])
rel_ref = pm.track_relationship(rel_id="r1", source_id="e1",
                                  target_id="e2", type="discovered")

# 反向追溯
lineage = pm.trace_lineage(entity_id="e1")
print(lineage)  # 列出 e1 来自哪些 chunk, 哪些文档

# 导出 PROV-O
pm.export_prov(format="turtle", output_path="./prov.ttl")
```

### 1.3 何时不用

- 你的数据量极小 (<1k 节点), 无审计需求 → 跳过 Provenance。
- 你已有 audit log 系统 (Splunk / Datadog) → 在那里记 provenance 即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.provenance.ProvenanceManager(storage_path=None)
semantica.provenance.provenance_methods.track_entity(...)
semantica.provenance.provenance_methods.track_relationship(...)
semantica.provenance.provenance_methods.track_chunk(...)
semantica.provenance.provenance_methods.track_property_source(...)
semantica.provenance.provenance_methods.get_lineage(...)
semantica.provenance.provenance_methods.trace_lineage(...)
semantica.provenance.provenance_methods.trace_descendants(...)
semantica.provenance.provenance_methods.query_recorded_between(...)
semantica.provenance.provenance_methods.get_all_sources(...)
semantica.provenance.provenance_methods.invalidate(...)
semantica.provenance.provenance_methods.audit_log(...)
semantica.provenance.provenance_methods.export_prov(...)
```

### 2.2 关键代码路径

- `semantica/provenance/manager.py:59` — `ProvenanceManager` 主类。
- `semantica/provenance/manager.py:263` — `track_entity`。
- `semantica/provenance/manager.py:417` — `track_relationship`。
- `semantica/provenance/manager.py:475` — `track_chunk`。
- `semantica/provenance/manager.py:546` — `track_property_source`。
- `semantica/provenance/manager.py:748` — `get_lineage`。
- `semantica/provenance/manager.py:814` — `trace_lineage`。
- `semantica/provenance/manager.py:838` — `trace_descendants`。
- `semantica/provenance/manager.py:947` — `query_recorded_between`。
- `semantica/provenance/manager.py:969` — `get_all_sources`。
- `semantica/provenance/manager.py:1011` — `invalidate`。
- `semantica/provenance/manager.py:1151` — `audit_log`。
- `semantica/provenance/manager.py:1203` — `export_prov` (Turtle / JSON)。
- `semantica/provenance/bridge_axiom.py` — L1/L2/L3 桥接公理。
- `semantica/provenance/integrity.py` — checksum 校验。
- `semantica/provenance/schemas.py` — PROV-O schema。
- `semantica/provenance/storage.py` — SQLite-backed 默认存储。

### 2.3 最小复现脚本

```python
# examples/ch-20-provenance-minimal.py mirror
import tempfile
from semantica.provenance import ProvenanceManager

with tempfile.TemporaryDirectory() as tmp:
    pm = ProvenanceManager(storage_path=f"{tmp}/prov.db")
    chunk_ref = pm.track_chunk(text="hi", source_doc="x.txt", offset=0, length=2)
    ent_ref = pm.track_entity(entity_id="e1", name="x", type="X", chunk_refs=[chunk_ref])
    print("lineage:", pm.trace_lineage("e1"))
    pm.export_prov(format="turtle", output_path=f"{tmp}/prov.ttl")
```

### 2.4 扩展点

- **加新存储后端**: 继承 `BaseProvenanceStorage`, 实现 `put / get / query`。
- **加新导出格式**: 扩 `export_prov(format=...)` 支持 PROV-XML / JSON-LD。
- **加新公理层**: 在 `bridge_axiom.py` 加 `_compute_axiom_l4` (Level 4: 因果链)。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么用 W3C PROV-O 而不是自研格式?**
- PROV-O 是国际标准, 监管方/合作方可直接消费。
- 标准库 (rdflib) 工具链丰富, 转换/可视化/校验都有现成方案。
- 代价: 概念多 (Entity/Activity/Agent/Bundle), 学习曲线陡。

**为什么 SQLite 默认存储?**
- 零部署、单机可用, 适合 demo / 测试。
- 生产可切 Postgres / Neo4j 节点存储 (`storage_postgres.py`)。
- 路径由 `provenance.storage_path` 配置项控制, 见 `core/config_manager.py:DEFAULT_CONFIG.provenance`。

### 3.2 与同类对比

| 维度 | Semantica provenance | OpenLineage | Marquez |
|---|---|---|---|
| 标准 | W3C PROV-O | OpenLineage 自有 | OpenLineage 自有 |
| 实体粒度 | Entity / Rel / Chunk / Decision | Dataset / Job / Run | 同 OpenLineage |
| 反向追溯 | ✅ trace_lineage | ⚠ 弱 | ⚠ 弱 |
| 校验 | ✅ checksum | ❌ | ❌ |

### 3.3 何时重新设计

- 数据量 > 100M → 必上 Postgres / 专用 lineage 系统 (DataHub / Atlas)。
- 出现"跨组织 federation" → 引入 PROV-O bundle + 签名。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-19-triplet-store]]
- 下一章: [[ch-21-context-decision]]
- W3C PROV-O: [w3.org/TR/prov-o](https://www.w3.org/TR/prov-o/)