# 术语出处分级

记录 32 个术语的出处分级,确保 Ch17 术语表有可追溯的引用源。

## 出处分级

- **L1 · 强出处**:代码 `src/` 内文件直接定义,引用 `file_path:line_number`
- **L2 · 文档出处**:`README.md`/`docs/*.md`/`site/**/*.md` 内出现
- **L3 · 推断**:基于代码事实的合理推断(无直接出处)

## 32 术语预分级

| 术语 | 分类 | 出处级别 | 候选引用 |
|------|------|----------|----------|
| index | 基础 | L1 | `src/db/schema.sql` |
| knowledge graph | 基础 | L1 | `src/graph/` |
| node | 基础 | L1 | `src/types.ts:22-45` |
| edge | 基础 | L1 | `src/types.ts:56-69` |
| FTS5 | 基础 | L1 | `src/db/schema.sql: nodes_fts` |
| SQLite WAL | 基础 | L1 | `src/db/index.ts:24-50` |
| PRAGMA | 基础 | L1 | `src/db/index.ts:24-50` |
| MCP | MCP | L1 | `src/mcp/` |
| JSON-RPC | MCP | L1 | `src/mcp/transport.ts` |
| stdio | MCP | L1 | `src/mcp/transport.ts: StdioTransport` |
| Unix socket | MCP | L1 | `src/mcp/transport.ts: SocketTransport` |
| PPID watchdog | MCP | L1 | `src/mcp/ppid-watchdog.ts` |
| handshake | MCP | L1 | `src/mcp/startup-handshake.ts` |
| tool | MCP | L1 | `src/mcp/tools.ts` |
| resource | MCP | L1 | MCP 协议规范 |
| initialize | MCP | L1 | `src/mcp/server-instructions.ts:20-70` |
| direct mode | 架构 | L1 | `src/mcp/index.ts:1-90` |
| proxy mode | 架构 | L1 | `src/mcp/proxy.ts` |
| daemon mode | 架构 | L1 | `src/mcp/daemon.ts` |
| session | 架构 | L1 | `src/mcp/session.ts` |
| engine | 架构 | L1 | `src/mcp/engine.ts` |
| launcher | 架构 | L1 | `src/bin/codegraph.ts: serve` |
| tree-sitter | 提取 | L1 | `codegraph-kernel/` |
| AST | 提取 | L2 | 通用概念 |
| wasm | 提取 | L1 | `package.json: tree-sitter-wasms` |
| NAPI | 提取 | L1 | `codegraph-kernel/Cargo.toml` |
| buffer contract | 提取 | L1 | `codegraph-kernel/src/lib.rs:46-89` |
| napi-rs | 提取 | L1 | `codegraph-kernel/Cargo.toml` |
| FSEvents | 提取 | L1 | `src/sync/watcher.ts:1-30` |
| inotify | 提取 | L1 | `src/sync/watcher.ts:1-30` |
| qualified_name | 图 | L1 | `src/types.ts:131-200` |
| debounce | 流程 | L1 | `src/sync/watcher.ts:67-75` |
| prompt hook | 集成 | L1 | `src/bin/codegraph.ts:1219-1246` |
| UserPromptSubmit | 集成 | L1 | `src/installer/targets/claude.ts:417-437` |
| mcpServers | 集成 | L1 | `src/installer/targets/shared.ts:24-30` |
| slash command | 集成 | L1 | `.claude/skills/` |

## Ch17 补充出处

| 术语 | Ch17 行号 | 一句话出处 |
|------|-----------|------------|
| SQLite WAL | Ch17:24 | `src/db/index.ts:24-50` 说明 SQLite 使用 Write-Ahead Logging 以支持读写并发。 |
| PRAGMA | Ch17:25 | `src/db/index.ts:24-50` 记录 codegraph 通过 PRAGMA 配置 busy_timeout、WAL 和 cache。 |
| JSON-RPC | Ch17:34 | `src/mcp/transport.ts` 定义 MCP 使用的 JSON-RPC 2.0 消息格式。 |
| stdio | Ch17:35 | `src/mcp/transport.ts` 中的 StdioTransport 通过标准输入/输出传输消息。 |
| Unix socket | Ch17:36 | `src/mcp/transport.ts` 中的 SocketTransport 使用 Unix domain socket 做同主机进程通信。 |
| PPID watchdog | Ch17:37 | `src/mcp/ppid-watchdog.ts` 监控父进程 PID 并在父进程终止时清理子进程。 |
| 握手 | Ch17:38 | `src/mcp/startup-handshake.ts` 定义 daemon 启动时与 launcher 的协议握手。 |
| initialize | Ch17:41 | `src/mcp/server-instructions.ts:20-70` 定义 MCP 会话的 initialize 初始化方法。 |

| skill | 集成 | L1 | `.claude/skills/add-lang/SKILL.md` |