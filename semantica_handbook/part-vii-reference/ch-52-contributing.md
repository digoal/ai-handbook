---
title: 贡献指南 — 流程 / 规范 / PR 模板
slug: ch-52-contributing
part: part-vii-reference
audience: all
reading_time: 7
prerequisites: []
semantica_version: 0.6.0
---

# ch-52 贡献指南 — 流程 / 规范 / PR 模板

> Semantica 接受社区贡献。本章讲解贡献流程、commit 规范、PR 模板、Code of Conduct。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 提 issue / PR 到 [github.com/semantica-agi/semantica](https://github.com/semantica-agi/semantica)。
- 写新数据源 / 新 LLM / 新本体对齐器。
- 修文档 / 翻译。
- 加入 [Discord](https://discord.gg/semantica) 社区。

### 1.2 贡献流程

1. Fork 仓库。
2. 创建分支: `git checkout -b feature/xxx` 或 `fix/yyy`。
3. 写代码 + 测试 + 文档。
4. 跑本地校验: `pytest tests/ -m "not integration"` + `semantica doctor`。
5. 提交: `<scope>: <description>` 格式 (见 §1.3)。
6. 推 PR, 填 PR 模板。
7. CI 通过 + 1 reviewer + mainter 合并。

### 1.3 Commit 规范

```
<scope>: <description>

[body]

[footer]
```

scope ∈ {`core`, `ingest`, `kg`, `vector_store`, `graph_store`, `ontology`, `reasoning`, `embeddings`, `semantic_extract`, `provenance`, `context`, `pipeline`, `cli`, `mcp`, `explorer`, `docs`, `tests`, `ci`}

例:

```
kg: add link_prediction transformer
docs: fix FIG-02 mermaid syntax
```

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `CONTRIBUTING.md` — 主贡献指南。
- `CODE_OF_CONDUCT.md` — 社区准则。
- `GOVERNANCE.md` (在 `docs/governance.md`) — 治理结构。
- `.github/PULL_REQUEST_TEMPLATE.md` — PR 模板。
- `.github/ISSUE_TEMPLATE/` — issue 模板 (bug / feature / docs)。

### 2.2 最小复现脚本

```bash
# 1) Fork + clone
git clone https://github.com/<you>/semantica.git

# 2) 建分支
git checkout -b feature/my-data-source

# 3) 装 dev 依赖
pip install ".[dev]"

# 4) 跑单测
pytest tests/ -m "not integration"

# 5) 提 PR
git push origin feature/my-data-source
```

### 2.3 PR 模板

```markdown
## What
- 新增 / 修订 / 删除

## Why
- 解决 issue #XXX / 用户场景

## How
- 关键改动点

## Tests
- [ ] 单元测试覆盖
- [ ] 集成测试 (如需)
- [ ] notebook 验证

## Docs
- [ ] 更新对应手册章
- [ ] CHANGELOG.md 增条目

## Checklist
- [ ] CI 绿
- [ ] 1 reviewer 已看
- [ ] commit 信息合规
```

### 2.4 扩展点

- **新数据源**: 写 `BaseIngestor` 子类 + 测试 + 注册到 `pyproject.toml:[ingest-*]`。
- **新 LLM**: 写 `BaseLLM` 子类 + 测试 + extras 名。
- **新图算法**: 写 `BaseAnalyzer` 子类 + 测试。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么用 conventional commit?**
- 自动生成 CHANGELOG (`release-please` / `semantic-release`)。
- reviewer 一眼看出 scope + 风险。

**为什么 PR 模板强制填?**
- 减少"无说明 PR", 提高 review 效率。

### 3.2 与同类对比

| 维度 | Semantica 贡献 | LangChain 贡献 | LlamaIndex 贡献 |
|---|---|---|---|
| Commit 规范 | conventional | conventional | conventional |
| PR 模板 | ✅ | ✅ | ✅ |
| notebook 必填 | ⚠ | ❌ | ❌ |

### 3.3 何时重新设计

- 贡献者 > 100 → 引入"贡献者联盟" (专门的 reviewer pool)。
- 出现"破坏性变更" → 引入 DEP 流程。

## 跨章引用

- 上一章: [[ch-51-testing]]
- 下一章: [[ch-53-troubleshooting]]