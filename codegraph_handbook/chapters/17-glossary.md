# 第 17 章 · 术语表

> **面向读者**:全员 · **预计阅读**:10 分钟(查词)
> **前置依赖**:无
> **本章目标**:统一全书名词,出处分级可追溯

## 17.1 使用说明

- 每个术语给出**中文名 / 英文原文 / 出处 / 出处分级**
- 出处分级:**L1**(代码 `src/` 内直接定义)、**L2**(README/docs 内出现)、**L3**(基于事实的合理推断)
- 完整出处追踪见 `references/terminology-source.md`
- 链接引用:`[L1]` = L1 强出处,`[L2]` = L2 文档出处,`[L3]` = L3 推断

---

## 17.2 基础(Basic)

| # | 中文 | 英文 | 出处 | 解释 |
|---|------|------|------|------|
| 1 | 索引 | index | [L1] `src/db/schema.sql` | 把代码库扫一遍,提取所有符号/边/文件并写入 `.codegraph/codegraph.db` |
| 2 | 知识图谱 | knowledge graph | [L1] `src/graph/` | 由 nodes(符号)+ edges(关系)组成的图结构 |
| 3 | 节点 | node | [L1] `src/types.ts:22-45` | 图谱中的一项实体,22 种 kind(file/class/function/...) |
| 4 | 边 | edge | [L1] `src/types.ts:56-69` | 节点间的关系,12 种 kind(calls/imports/extends/...) |
| 5 | FTS5 | FTS5 | [L1] `src/db/schema.sql: nodes_fts` | SQLite 5 全文检索虚拟表,无外部依赖 |
| 6 | SQLite WAL | SQLite WAL | [L1] `src/db/index.ts:24-50` | SQLite Write-Ahead Logging 模式,读写并发不互锁 |
| 7 | PRAGMA | PRAGMA | [L1] `src/db/index.ts:24-50` | SQLite 配置语句,codegraph 设置 busy_timeout/WAL/cache 等 |

---

## 17.3 MCP 与传输(MCP & Transport)

| # | 中文 | 英文 | 出处 | 解释 |
|---|------|------|------|------|
| 8 | MCP | MCP(Model Context Protocol) | [L1] `src/mcp/` | 让 agent 调用外部工具的标准化协议(JSON-RPC 2.0) |
| 9 | JSON-RPC | JSON-RPC 2.0 | [L1] `src/mcp/transport.ts` | 一种基于 JSON 的远程过程调用协议,codegraph 用它做 MCP 消息格式 |
| 10 | stdio | stdio | [L1] `src/mcp/transport.ts: StdioTransport` | 标准输入/输出,最直接的进程间通信方式 |
| 11 | Unix socket | Unix domain socket | [L1] `src/mcp/transport.ts: SocketTransport` | POSIX 同主机进程通信,macOS/Linux 用;Windows 用 named pipe |
| 12 | PPID watchdog | PPID watchdog | [L1] `src/mcp/ppid-watchdog.ts` | 监控 parent PID,host SIGKILL 时自动清理子进程 |
| 13 | 握手 | handshake | [L1] `src/mcp/startup-handshake.ts` | daemon 启动时与 launcher 的协议握手,hello 行先于 JSON-RPC 防 wedge |
| 14 | 工具 | tool | [L1] `src/mcp/tools.ts` | MCP 协议中 agent 可调用的函数;codegraph 默认只暴露 1 个 |
| 15 | 资源 | resource | [L2] MCP 规范 | MCP 协议的另一类暴露对象(文件/数据);codegraph 当前未用 |
| 16 | initialize | initialize | [L1] `src/mcp/server-instructions.ts:20-70` | MCP 会话初始化方法,server 返回 instructions 与 tool 列表 |

---

## 17.4 架构(Architecture)

| # | 中文 | 英文 | 出处 | 解释 |
|---|------|------|------|------|
| 17 | 直接模式 | direct mode | [L1] `src/mcp/index.ts:1-90` | 单进程 stdin/stdout 跑 MCP,无 daemon 共享 |
| 18 | 代理模式 | proxy mode | [L1] `src/mcp/proxy.ts` | launcher 是薄 stdin↔socket pipe,带 PPID watchdog |
| 19 | 守护模式 | daemon mode | [L1] `src/mcp/daemon.ts` | detached 背景进程,Unix socket 多路复用 N 个 client,空闲 300s 退出 |
| 20 | 会话 | session | [L1] `src/mcp/session.ts` | 单 MCP 连接的协议状态机(initialize / tools/list / tools/call) |
| 21 | 引擎 | engine | [L1] `src/mcp/engine.ts` | MCPEngine,daemon 内单例,持 CodeGraph + watcher + ToolHandler |
| 22 | 启动器 | launcher | [L1] `src/bin/codegraph.ts: serve` | `codegraph serve --mcp` 启动的进程,可能是 direct/proxy/daemon-spawner |

---

## 17.5 提取(Extraction)

| # | 中文 | 英文 | 出处 | 解释 |
|---|------|------|------|------|
| 23 | tree-sitter | tree-sitter | [L1] `codegraph-kernel/Cargo.toml` | 增量解析器,生成具类型 AST;codegraph 用 Rust + wasm 两种 runtime |
| 24 | AST | AST(abstract syntax tree) | [L2] 通用概念 | 抽象语法树,tree-sitter 的输出 |
| 25 | wasm | WebAssembly | [L1] `package.json: tree-sitter-wasms` | Rust kernel 不可用时的 fallback 路径 |
| 26 | NAPI | NAPI | [L1] `codegraph-kernel/Cargo.toml` | Node ↔ Rust 跨语言桥接,codegraph 用 napi-rs 3 |
| 27 | buffer contract | buffer contract | [L1] `codegraph-kernel/src/lib.rs:46-89` | kernel 输出 5 块连续 Buffer 的字节布局约定,TS 端解码 |
| 28 | napi-rs | napi-rs | [L1] `codegraph-kernel/Cargo.toml` | Rust 端 NAPI 实现框架 |

---

## 17.6 集成(Integration)

| # | 中文 | 英文 | 出处 | 解释 |
|---|------|------|------|------|
| 29 | 提示词钩子 | prompt hook | [L1] `src/bin/codegraph.ts:1219-1246` | Claude Code 的 UserPromptSubmit 钩子,三档 gate 自动预填上下文 |
| 30 | UserPromptSubmit | UserPromptSubmit | [L1] `src/installer/targets/claude.ts:409-412` | Claude Code 钩子事件名,在用户提交 prompt 时触发 |
| 31 | mcpServers | mcpServers | [L1] `src/installer/targets/shared.ts:24-30` | `~/.claude.json` 里的 MCP server 注册块 |
| 32 | slash command | slash command | [L1] `.claude/skills/` | Claude Code 的 `/`-菜单命令;codegraph 项目内注册了 `/add-lang`、`/agent-eval` |

---

## 17.7 流程与图谱(Processes & Graph)

补充几个在正文中反复出现、但未在前 32 词里的关键概念:

| 中文 | 英文 | 出处 | 解释 |
|------|------|------|------|
| 完全限定名 | qualified_name | [L1] `src/types.ts:131-200` | 符号的全路径名,如 `MyClass.myMethod` |
| 未解析引用 | unresolved ref | [L1] `src/db/schema.sql: unresolved_refs` | 解析时找不到目标的引用,pending/failed 状态机重试 |
| 接收者类型 | receiver type | [L1] `src/types.ts: return_type` | 方法所属类型,影响 dispatch 解析 |
| 合成边 | synthesis edge | [L1] `src/resolution/` | 跨语言桥接(如 Swift↔ObjC、TurboModules)的启发式边,标 `provenance: heuristic` |
| 去抖 | debounce | [L1] `src/sync/watcher.ts:67-75` | 文件事件触发延迟合并,避免频繁 sync |
| 自适应去抖 | adaptive debounce | [L1] `src/sync/watcher.ts:67-75` | debounce 阈值随文件数动态调整(≤2 文件 300ms,>500 pending 全扫) |
| 派生扫描差异 | full scan-diff | [L1] `src/sync/watcher.ts` | sync 时基于 (size, mtime) + content-hash 的对账 |
| 幂等 | idempotent | [L3] | edges UNIQUE 约束保证重复 sync 不产生重复边 |

---

## 17.8 本章小结

- 32 词覆盖基础、MCP、架构、提取、集成 5 大类
- 出处分级让读者知道哪些是源代码定义的硬事实,哪些是文档叙述,哪些是推断
- 后续章节遇术语模糊可回查本章

## 17.9 下一章预告

最后一章 FAQ 把读者最常问的 17 个问题集中作答。

## 17.10 参考

- `references/terminology-source.md` — 完整出处追踪表
- `src/types.ts` — 节点/边 schema 的真相
- `src/db/schema.sql` — 表与索引的真相