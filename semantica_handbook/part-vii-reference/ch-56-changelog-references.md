---
title: Changelog 与版本引用
slug: ch-56-changelog-references
part: part-vii-reference
audience: all
reading_time: 5
prerequisites: []
semantica_version: 0.6.0
---

# ch-56 Changelog 与版本引用

> 本章汇总 Semantica 各版本重大变更, 帮助读者快速对齐 API 演进。

## 1. 用户视角(User)

### 1.1 版本速查

| 版本 | 状态 | 重大变更 |
|---|---|---|
| **v0.6.0** | 当前 | Distance Intelligence / Ontology Hub / 安全加固 / 11 个 MCP tools 扩展到 12 |
| **v0.5.0** | 已发布 | BiTemporal 决策图 / 实时 Explorer 搜索 / 12 类导出 |
| **v0.4.0** | 已发布 | 决策图作为一等图节点 / `add_causal_relationship` |
| **v0.3.0** | 已发布 | 5 类冲突解决 / multi-source integration |
| **v0.2.0** | 已发布 | 7 个 LLM provider / FAISS / Neo4j 后端 |
| **v0.1.0** | 已发布 | MVP / 单 PDF / 单图 |

### 1.2 升级路径

- **v0.5 → v0.6**: `pip install -U semantica`, 无破坏性 API 变更。
- **v0.4 → v0.5**: `ProvenanceManager.export_prov` 输出格式略改 (Turtle 头部), 不破坏 RDF 解析。
- **v0.3 → v0.4**: `record_decision` 增加 `decided_by` 必填字段 (旧版本可空)。
- **v0.2 → v0.3**: `ConflictResolver.resolve` 改名 `resolve_conflicts`, 旧名仍兼容但 deprecation warning。

### 1.3 一段最小可跑示例

```bash
# 查 changelog
semantica changelog --json | jq '.[0]'

# 看当前版本
semantica --version
```

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.__version__   # "0.6.0"
semantica.cli.changelog  # 子命令, 输出 JSON / Markdown
```

### 2.2 关键代码路径

- `semantica/__init__.py:13` — `__version__ = "0.6.0"`。
- `semantica/cli.py:721` — `changelog` 子命令。
- `CHANGELOG.md` (156 KB) — 全量 changelog。
- `RELEASE_NOTES.md` — 高层摘要。
- `pyproject.toml:7` — `version = "0.6.0"`。

### 2.3 最小复现脚本

```python
# examples/ch-56-version.py mirror
from semantica import __version__
print(f"Semantica version: {__version__}")
```

### 2.4 已知陷阱

- **CHANGELOG.md 156 KB**: 不用读全, 用 `semantica changelog --since 0.5.0` 过滤。
- **SemVer 偏移**: v0.6 仍可能有 breaking change (minor 版本可含 breaking), 升级前查 changelog。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 v0.x 而不是 v1.0?**
- v1.0 是"承诺稳定 API", Semantica 仍在快速演进, 用 v0.x 表示"基本可用但 API 可能改"。
- 预计 v1.0 在 v0.9 或 v1.0 时释放。

**为什么 CHANGELOG.md 156 KB?**
- v0.2 起每个 PR 自动生成条目, 历史条目累积。

### 3.2 与同类对比

| 维度 | Semantica 版本 | LangChain 版本 | LlamaIndex 版本 |
|---|---|---|---|
| 当前 | v0.6.0 | v0.3.x | v0.12.x |
| SemVer | 0.x (演化中) | 0.x | 0.x |
| 自动 CHANGELOG | ✅ | ✅ | ✅ |

### 3.3 何时重新设计

- v1.0 发布 → 引入 NEP (Next-Extension-Proposal) 流程。
- API 稳定后 → 引入 `lts` / `stable` 双轨。

## 跨章引用

- 上一章: [[ch-55-glossary]]
- 上一章 (Part VI 末): [[ch-49-security]]
- 完整 changelog: [CHANGELOG.md](https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md)