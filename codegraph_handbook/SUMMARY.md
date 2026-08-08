# CodeGraph Handbook · 目录

> 给 AI Coding Agent 当 MCP 服务的本地代码知识图谱(codegraph v1.5.0)系统性电子书
> 18 章 + 序章,3300 行,11 张 mermaid 图(已内联),~80 条真机验证记录

---

## 阅读路径

| 你是谁 | 必读 | 可选 |
|--------|------|------|
| **用户**(70%) | Ch02 / Ch06 / Ch09 / Ch18 | Ch01 / Ch03-05 / Ch07-08 |
| **开发者**(20%) | Ch11-12 / Ch15-16 | Ch09 / Ch13-14 / Ch18 |
| **架构师**(10%) | Ch01 / Ch10-15 | Ch02 / Ch16 / Ch18 |

---

## 目录

### 序章

| Ch | 标题 | 面向读者 | 阅读 | 一句话摘要 |
|----|------|----------|------|------------|
| 00 | 序章 | 全员 | 5 min | 三类读者开场 + 阅读路径图 |

### Part 1 · Foundations

| Ch | 标题 | 面向读者 | 阅读 | 一句话摘要 |
|----|------|----------|------|------------|
| 01 | 背景:AI Coding 的 context 困境 | 用户/架构师 | 15 min | 为什么需要 codegraph,89/69/60 数据来源 |
| 02 | 5 分钟快速上手 | 用户 | 10 min | 装 CLI → init → Claude Code 对话 |
| 03 | 安装、升级与多 Agent 集成 | 用户 | 20 min | 8 个 Agent × 3 OS × 3 安装路径 |
| 04 | 配置全解(env / 忽略规则 / 遥测) | 用户 | 20 min | 60+ env / `codegraph.json` / `codegraph telemetry` |

### Part 2 · User Guide

| Ch | 标题 | 面向读者 | 阅读 | 一句话摘要 |
|----|------|----------|------|------------|
| 05 | 与 Claude Code 协作的标准范式 | 用户 | 25 min | 5 类 prompt × 8 个 tool + 三档 prompt hook |
| 06 | MCP 工具完全手册(8 个) | 用户 | 30 min | 8 tool 输入输出、典型边界 |
| 07 | CLI 命令完全手册(20 个) | 用户/开发者 | 30 min | 20+ 命令的 flags + CLI↔MCP 对照 |
| 08 | 增量同步、Watcher 与降级策略 | 用户/开发者 | 20 min | 三平台差异 + adaptive debounce + banner 解读 |
| 09 | 真实场景案例库(7 仓 7 问) | 用户 | 30 min | shallow clone 7 仓实测 + 原 README 问题 |

### Part 3 · Architecture Deep Dive

| Ch | 标题 | 面向读者 | 阅读 | 一句话摘要 |
|----|------|----------|------|------------|
| 10 | 进程拓扑与端到端数据流 | 架构师/开发者 | 25 min | Launcher → Daemon → Engine → SQLite 全链路 |
| 11 | 知识图谱 Schema(node / edge / FTS5) | 架构师/开发者 | 25 min | 22 node kind + 12 edge kind + 19 索引 |
| 12 | Rust 内核与 tree-sitter NAPI 桥接 | 架构师/开发者 | 30 min | buffer contract + ABI 校验 + wasm fallback |
| 13 | Context 组装管线 | 架构师 | 25 min | parse → search → expand → format 五阶段 |
| 14 | MCP 协议工程化(三模式) | 架构师 | 25 min | Direct / Proxy / Daemon + hello + 三 watchdog |
| 15 | 评估体系与搜索质量环 | 架构师/开发者 | 25 min | recall / MRR / latency + 7 类测试电池 |

### Part 4 · Developer Guide

| Ch | 标题 | 面向读者 | 阅读 | 一句话摘要 |
|----|------|----------|------|------------|
| 16 | 贡献者指南:加语言 / 加 tool / 改 schema | 开发者 | 30 min | /add-lang + Cargo.toml 14 crate + 评测 |

### Part 5 · Reference

| Ch | 标题 | 面向读者 | 阅读 | 一句话摘要 |
|----|------|----------|------|------------|
| 17 | 术语表(32 词) | 全员 | 查词 | 中英对照 + 出处分级 |
| 18 | FAQ(17 题) | 全员 | 查词 | 安装/hook/monorepo/同步/性能/工具/贡献/升级 |

---

## 附件

- 11 张 mermaid 图 — 已内联在各章 ` ```mermaid ` 代码块中
- `references/cross-refs.md` — 跨章引用追踪表
- `references/validation-log.md` — 所有实操验证记录(180 行)
- `references/terminology-source.md` — 32 术语出处分级
- `references/main-session-state.md` — compact checkpoint
- `examples/README.md` — 7 仓真实 benchmark 汇总表
- `examples/{vscode-extension-host,excalidraw-canvas,django-orm,tokio-runtime,okhttp-interceptors,gin-middleware,alamofire-request}/README.md` — 各仓详细跑分报告

---

## 全书字数统计

| 范围 | 行数 |
|------|------|
| 序章 + 18 章 markdown | 3300+ |
| validation-log | 180 |
| mermaid 图(内联) | 11 张,代码块在各章里 |
| examples × 7 + 汇总 | ~1000 字 |

---

## 锚定版本

- codegraph v1.5.0(2026-07-22 commit)
- Claude Code ≥ 1.0
- Node 20-24(v25 硬拦)
- macOS 14.x / Ubuntu 24.04 / Windows 11