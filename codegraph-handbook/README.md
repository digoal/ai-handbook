# CodeGraph Handbook

> 给 AI Coding Agent 当 MCP 服务的本地代码知识图谱 — 系统性电子书

[![chapters](https://img.shields.io/badge/chapters-19-blue)](#目录)
[![diagrams](https://img.shields.io/badge/mermaid-11-green)](#目录)
[![validations](https://img.shields.io/badge/validations-80%2B-orange)](references/validation-log.md)
[![codegraph](https://img.shields.io/badge/codegraph-v1.5.0-purple)](https://github.com/colbymchenry/codegraph)

`codegraph` 把代码库预建成知识图谱(节点 + 边 + 文件 + FTS5),让 Claude Code / Cursor / Codex 等 AI Coding Agent 通过一次 MCP 调用拿到所需源码 + 调用路径 + 爆炸半径,**省掉 grep/Read 链**。100% 本地,Rust + tree-sitter + napi-rs + SQLite 实现的零原生插件工具。

这本 Handbook 系统化讲清楚它怎么用、怎么搭、怎么扩、怎么调。

> 📊 **7 仓真实 benchmark 跑分**:见 [examples/README.md](examples/README.md) 汇总表与各子目录(当前 commit + cg 1.5.0 实测)

---

## 给三类读者的入口

### 用户(开发者,70%)

想让 Claude Code 更快、更准、更省 token?

1. **[Ch02 · 5 分钟快速上手](chapters/02-quickstart.md)** — 装 CLI → init → 第一次对话
2. **[Ch06 · MCP 工具完全手册](chapters/06-mcp-tools-manual.md)** — 8 个 tool 何时用哪个
3. **[Ch09 · 真实场景案例库](chapters/09-case-studies.md)** — 7 仓 7 问实测
4. **[Ch18 · FAQ](chapters/18-faq.md)** — 17 个最常被问的问题

### 开发者(贡献者,20%)

想给 codegraph 加语言、写 MCP tool、改 schema?

1. **[Ch12 · Rust 内核与 tree-sitter NAPI 桥接](chapters/12-rust-kernel.md)** — buffer contract + ABI 校验
2. **[Ch11 · 知识图谱 Schema](chapters/11-schema-deep-dive.md)** — 22 node / 12 edge / 19 索引
3. **[Ch15 · 评估体系与搜索质量环](chapters/15-evaluation.md)** — quality loop 怎么驱动改进
4. **[Ch16 · 贡献者指南](chapters/16-contributing.md)** — `/add-lang` + Cargo.toml 14 crate + A/B

### 架构师(设计者,10%)

想理解怎么给 AI Agent 提供知识层?

1. **[Ch01 · 背景:context 困境](chapters/01-background.md)** — 问题域
2. **[Ch10 · 进程拓扑与端到端数据流](chapters/10-process-topology.md)** — 全链路图(F-5)
3. **[Ch14 · MCP 协议工程化](chapters/14-mcp-three-modes.md)** — 三模式决策表
4. **[Ch13 · Context 组装管线](chapters/13-context-pipeline.md)** — 5 阶段管线

---

## 目录

完整目录见 **[SUMMARY.md](SUMMARY.md)**,所有 19 章、5 部分、11 张 mermaid 图、全书统计。

---

## 阅读方式

### 选项 A · GitHub 直读

直接在 GitHub / VS Code / Cursor 里读 `chapters/*.md`。所有 mermaid 图已经以 ```` ```mermaid ```` 代码块内联在各章里,GitHub / VS Code / Cursor 会自动渲染。

### 选项 B · mkdocs 站点

```bash
cd ~/new/codegraph-handbook
pip install mkdocs mkdocs-material
# 创建 mkdocs.yml 后:makdocs serve
```

### 选项 C · mdbook

```bash
# 创建 book.toml + SUMMARY.md 对齐后
mdbook serve
```

### 选项 D · 静态站点

任何支持 markdown 的站点生成器(astro、docusaurus、hugo)都可直接 ingest。

---

## 验证态度

这本书每个"真实场景实战"小节里的命令输出都来自**真机跑**:

- `references/validation-log.md` — 180 行,~80 条验证条目
- 每条记录包含日期、章节、命令、环境(macOS 14 / node 24 / cg 1.5.0)、状态
- 部分因环境限制的验证(Windows-only、WSL2、需要私有网络)在日志中明确标记为 ⚠ 或 ⏸

---

## 引用约定

- `file_path:line_number` — 指向 codegraph 源码位置
- `{{chapter:NN}}` — 内部引用第 N 章(SUMMARY.md 有完整索引)
- mermaid 图 — 以 ```mermaid 代码块内联在各章,不再有独立文件

---

## 关键事实索引

| 主题 | 章节 |
|------|------|
| 7 benchmark 实测数据 | Ch09 |
| 22 node / 12 edge | Ch11 |
| ABI=2 / 20 langs / kernel.node 34 MB | Ch12 |
| Direct / Proxy / Daemon 决策表 | Ch14 |
| PASS_THRESHOLD=0.5 / 7 类评测 | Ch15 |
| 8 个 MCP tool | Ch06 |
| 20+ CLI 命令 | Ch07 |
| 60+ CODEGRAPH_* env | Ch04 |
| 8 target agent 配置 JSON | Ch03 |
| 11 mermaid 图 | 内联在各章 ```mermaid 代码块 |

---

## 锚定版本

- codegraph v1.5.0(2026-07-22)
- Claude Code ≥ 1.0
- Node 20-24(v25 因 V8 Turboshaft Zone OOM 被硬拦)
- macOS 14.x / Ubuntu 24.04 / Windows 11

---

## 贡献

发现错误或想补充内容?参见 [Ch16 贡献者指南](chapters/16-contributing.md) 的代码提交流程;内容性补充直接改 `chapters/*.md` 后跑 `references/validation-log.md` 的检查清单。

## 许可

本文档基于 MIT 协议发布,引用 codegraph 仓库部分受其协议约束。