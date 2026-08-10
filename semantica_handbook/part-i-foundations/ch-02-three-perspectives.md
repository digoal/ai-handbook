---
title: 阅读指南 — 三个视角分别在说什么
slug: ch-02-three-perspectives
part: part-i-foundations
audience: all
reading_time: 8
prerequisites: [ch-01-welcome]
semantica_version: 0.6.0
---

# ch-02 阅读指南 — 三视角分层模型

> 本手册的每一章都分三层讲。本章解释为什么这么做, 以及如何按角色跳读。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 一眼判断"这一章里, 我**作为某角色**该读哪一节"。
- 知道怎么挑阅读路径: 用户线、开发线、架构线三条独立通道。
- 知道哪些章节可以跳, 哪些必须按顺序。

### 1.2 三视角分层契约

每章固定三节, 顺序不变:

| 节 | 视角 | 不讲什么 | 讲什么 | 文风 |
|---|---|---|---|---|
| **1. 用户视角** | "我要用它做什么" | 内部类 / API 签名 / 模块依赖 | 能做什么 / 怎么用 / 结果长什么样 / 5-9 步可跑通 | 二级标题 + 子项列表 + 可复制命令 + 截图位 |
| **2. 开发者视角** | "我要改/集成它" | 取舍原因 / 商业策略 | API 表 + 关键代码路径 + 扩展点 + 最小复现脚本 | 代码块 + API 表 + step-by-step |
| **3. 架构师视角** | "它为什么这样设计" | 入门级用法 | 设计取舍 + 与同类对比 + 何时重新设计 | 决策矩阵 + ADR 片段 + trade-offs |

### 1.3 何时只看其中一节

- **只要跑通 demo**: 只读 §1 用户视角, 跟着 5-9 步操作即可。
- **要集成到现有系统**: 读完 §1 后跳到 §2 开发者视角的 API 表。
- **要评估是否采纳/扩展**: 先跳到 §3 架构师视角, 再回 §2 看扩展点。

### 1.4 何时不能跳

- **第一次接触 Semantica**: 顺序读完 Part I (ch-01 → ch-07)。
- **要写新数据源/新 LLM 适配**: 必须读完对应核心模块章节的 §2 + §3, 不止 §1。

## 2. 开发者视角(Developer)

### 2.1 三视角在文档工程上的实现

每章顶部 YAML frontmatter 强制四字段 (除基础信息外):

```yaml
audience: all        # primary | developer | architect | all
```

`primary` = 偏向"用户视角", 但仍保留三节结构。
`developer` = 偏向"开发者视角", 但仍保留三节结构。
`architect` = 偏向"架构师视角", 但仍保留三节结构。
`all` = 三视角平均笔墨。

CI 通过 `scripts/lint_perspectives.py` 强制每章必须含三节标题:

```
## 1. 用户视角(User)
## 2. 开发者视角(Developer)
## 3. 架构师视角(Architect)
```

### 2.2 关键词黑名单

`scripts/lint_perspectives.py` 同时检查: 用户视角节中**不**应出现以下词汇 (≥3 次):

- `class Xxx` / `def xxx` / `@dataclass` / `abstractmethod`
- 具体类名: `GraphBuilder [[ch-55-glossary]] / ProvenanceManager / DecisionRecorder / HybridSearch [[ch-55-glossary]] / FalkorDB / ReteEngine / DatalogReasoner / OntologyGenerator / EmbeddingGenerator / LLMExtraction`
- 具体文件: `config_manager.py / orchestrator.py / graphStore.ts`

如果出现 ≥3 次, lint 拒绝通过; 提示应移到 §2。

### 2.3 关键代码路径

- `templates/chapter.md` — 章节模板, 强制三节结构。
- `scripts/lint_perspectives.py` — lint 实现 (≤130 行)。
- `scripts/validate_frontmatter.py` — frontmatter JSON Schema 校验 (≤130 行)。
- `scripts/check_links.py` — `[[ch-XX-slug]]` 与 `[[fig-NN]]` 双向链接审计。

### 2.4 扩展点

- 想新增"产品经理视角": 复制 §1 模板, 加一节 `## 4. PM 视角` 并扩展 lint 关键字白名单。
- 想新增"安全视角": 同上, 重点检查"用户视角"里不出现密钥/Token/PII 字面量。

## 3. 架构师视角(Architect)

### 3.1 设计取舍 — 为什么固定三视角而不是更多

**为什么是 3 而不是 4 或 5?**
- 三视角覆盖了"业务/工程/决策"三轴, 互相正交。
- 加第四视角 (如 PM / SRE / 安全) 会让边界不清, 章节膨胀 30% 但信息密度下降。
- 工程实践上, 三层契约与"用户故事 → 实现 → 架构"对应, 符合敏捷/Clean 架构的语境。

**为什么顺序固定 User → Developer → Architect?**
- 用户最易读, 放前面降低放弃率。
- 开发者最常查, 居中方便读者"读完用户层再来这里"。
- 架构师内容最重, 殿后让深度读者愿意翻到底。

### 3.2 与同类文档风格对比

| 文档风格 | 视角数 | 典型代表 | Semantica 选择 |
|---|---|---|---|
| 单视角叙述 | 1 | 多数 README | ❌ 信息密度低 |
| 双视角 (用户/技术) | 2 | AWS 文档部分章节 | ⚠ 缺失架构决策 |
| **三视角** | **3** | **本手册** / 部分 O'Reilly 书 | ✅ 信息密度与可读性平衡 |
| 多视角 (≥4) | ≥4 | 极少数内部文档 | ❌ 维护成本高 |

### 3.3 何时重新审视分层**: 当

- 单视角节字数 ≤ 200 字持续 ≥ 5 章 → 该视角对该主题不必要, 合并。
- 关键词黑名单持续误报 (≥10 次/章) → 阈值过严或章节主题不匹配视角契约。
- 读者反馈"找不到入口" → 把 §1 移到所有章节末尾作 FAQ。

## 本章图表

> 本章为方法论介绍, 不引入 Mermaid 图。三视角契约的 C4 图见 [[ch-04-architecture-30kft]]。

## 跨章引用

- 上一章: [[ch-01-welcome]]
- 下一章: [[ch-04-architecture-30kft]] (顺序上 ch-04 优先, 它定义术语)
- 安装: [[ch-03-install]]
- 阅读路径速查: [README 三条路径](../README.md#2-三条阅读路径)