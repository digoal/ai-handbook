# 第 6 章 · MCP 工具完全手册

> **面向读者**:用户 · **预计阅读**:30 分钟
> **前置依赖**:第 5 章
> **本章目标**:精通 8 个 tool、何时用哪个

## 6.1 引言

CodeGraph 通过 MCP 暴露 8 个具名 tool,Claude Code / Cursor / Codex 等客户端用 JSON-RPC 2.0 调用。本章逐个给 schema、产出、何时用——读后 30 秒能选对该发哪个。

## 6.2 概念铺垫

**MCP** 是 Anthropic 的工具协议:server 宣告 tool,client 用 `tools/call` 触发,server 返回 `result.content[].text`(Markdown)。`codegraph serve --mcp` 用 stdio。调用形如:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call",
 "params":{"name":"codegraph_xxx","arguments":{...}}}
```

**Default-1-tool**:`server-instructions.ts:32-48` 把 `codegraph_explore` 立为主入口,默认只开它。其它靠 `CODEGRAPH_MCP_TOOLS` 启用(`DEFAULT_MCP_TOOLS = {'explore'}` in `tools.ts`)——避免 8 个描述占满 prompt。

## 6.3 正文

### 6.3.1 白名单与默认

schema 真源 `src/mcp/tools.ts:536-746`。**何时用哪个**:explore 一站式解决 80%;余下场景:纯符号列表 → `search`;上下游 → `callers`/`callees`;重构爆炸半径 → `impact`;等价 `Read` → `node`;文件树/健康度 → `files`/`status`。

启用:`CODEGRAPH_MCP_TOOLS=explore,search,node,callers,callees,impact,files,status`(逗号,**不带** `codegraph_` 前缀)。

实测默认 1 个:`{"name":"codegraph_explore","description":"PRIMARY TOOL..."}`。加 env 后 8 个全开:`search,callers,callees,impact,node,explore,status,files`。

### 6.3.2 codegraph_explore(主入口)

**schema**:`query`(必填)、`maxFiles`(默认 12)、`projectPath`(可选)。**何时用**:几乎任何问题——"X 怎么工作"、"X 在哪"、"架构"、"bug 在哪"——都先发。一次返回行号源码 + 调用路径 + 爆炸半径。

实测(`/tmp/tokio-demo` 的 `greet`):
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"codegraph_explore","arguments":{"query":"greet function","maxFiles":3,"projectPath":"/tmp/tokio-demo"}}}' | codegraph serve --mcp
```
返回:`Found 2 symbols across 1 file / greet (src/main.rs:9) — 1 caller in src/main.rs; ⚠️ no covering tests found`,随后 `1\tuse tokio::time::{sleep, Duration}` 格式的逐字行号源码。

### 6.3.3 codegraph_node(双模)

**模式一 · 读文件**:只传 `file`(path 或 basename),等价 `Read`,返回行号源码 + 依赖;可选 `offset`/`limit`/`symbolsOnly`。**模式二 · 单符号**:传 `symbol`(+ `includeCode=true` 拿函数体),返回位置 + 签名 + trail;重名时 `file` + `line` 钉一个。

实测 `{"file":"src/main.rs"}` → `**src/main.rs** — 26 lines, 4 symbols · no other indexed file depends on it` 加 1-26 行逐字源码。`{"symbol":"greet","includeCode":true}` → `**greet** — src/main.rs:9 / 9\tasync fn greet(name: &str) {...} / Called by ← main (src/main.rs:4)`。

**何时用**:explore 取多符号,node 取单个;改文件前 node 一下既有源码又有爆炸半径。

### 6.3.4 codegraph_search(快速定位)

**schema**:`query`(必填)、`kind`(function/method/class/interface/type/variable/route/component)、`limit`(默认 10)。实测 `{"query":"greet"}` → `**Search Results (1 found)** / **greet** (function) / src/main.rs:9 / (name: &str)`。

**何时用**:只要"有没有、叫什么、在哪行",不要源码——比 explore 省 token。前缀匹配,`auth` 会同时命中 `AuthService`、`authenticate`。

### 6.3.5 codegraph_callers / codegraph_callees

schema 对称:`symbol`(必填)、`file`(同名消歧)、`limit`(默认 20)。`callers` 找谁调它,`callees` 找它调谁。

实测 `callers greet` → `**Callers of greet (1 found)** / - main (function) - src/main.rs:4`。`callees main` → `2 distinct definitions (narrow with file) / main (function) — src/main.rs:4 / - greet / src/main.rs (file) — src/main.rs:1 / - (no callees)`——同名 `main` 出现两处,提示用 `file` 消歧。

**何时用**:explore 已给 trail,要单独 grep 上下游做 diff/自动化时。

### 6.3.6 codegraph_impact(爆炸半径)

**schema**:`symbol`(必填)、`file`、`depth`(默认 2)。沿调用图走 N 层。

实测 `{"symbol":"greet","depth":1}` → `**Impact: "greet" affects 2 symbols** / src/main.rs: greet:9, main:4`。

**何时用**:改函数签名/重构前必发。默认 `depth=2`,大项目调到 5+ 但小心 token 爆。

### 6.3.7 codegraph_files(索引文件树)

**schema**:`path`(子目录过滤)、`pattern`(glob 如 `*.tsx`)、`format`(`tree`/`flat`/`grouped`)、`includeMetadata`(默认 true)、`maxDepth`。

实测 `{"path":"src"}` → `**Project Structure (1 files)** / └── src /     └── main.rs (rust, 6 symbols)`。**何时用**:进陌生仓库第一件事——走索引,比 `Glob` 快。

### 6.3.8 codegraph_status(健康度)

**schema**:`projectPath`(可选)。实测 → `**CodeGraph Status** / Files: 1 / Nodes: 6 / Edges: 6 / DB: 0.15 MB / Backend: node:sqlite — WAL + FTS5 / Nodes: file 1, function 4, import 1 / Languages: rust 1`。

**何时用**:`explore` 返回 "No relevant code found" 或 "⚠️ auto-sync DISABLED" 时——快速判断是索引空、watcher 挂了,还是没 init。

### 6.3.9 projectPath 跨项目

每个 tool 都有可选 `projectPath`。**何时用**:同 session 查多项目(microservice / monorepo 子项目);从该路径向上找最近的 `.codegraph/`。**无 default project 的 gateway server 上**是必填——schema 自动把 `required` 加上(`tools.ts:748-765` 的 `requireProjectPath`)。跨项目时**不要省略**,否则服务器拒收。

## 6.4 真实场景实战

**场景 1 · 改函数前看爆炸半径**。`{"name":"codegraph_impact","arguments":{"symbol":"greet","depth":2,"projectPath":"/tmp/tokio-demo"}}` → `affects 2 symbols: greet:9, main:4`,只有 `main` 一处调用,安全。

**场景 2 · 同名消歧**。`{"name":"codegraph_callees","arguments":{"symbol":"main","projectPath":"/tmp/tokio-demo"}}` → `2 distinct definitions`,同名 `main` 既在 `src/main.rs:4`(函数)也作为文件节点 `src/main.rs:1`。补传 `file=src/main.rs` 钉一个。

**场景 3 · 陌生仓库第一扫**。`files` → `src/main.rs (rust, 6 symbols)`;`status` → `Files 1 / Nodes 6 / Edges 6`;然后 `explore "what does main do"` 拿源码 + trail。

## 6.5 本章小结

- 8 个 tool:`explore`(主)、`node`(双模)、`search`(定位)、`callers`/`callees`(上下游)、`impact`(爆炸半径)、`files`(树)、`status`(健康度)
- 默认只开 explore,其它通过 `CODEGRAPH_MCP_TOOLS` 启用
- 响应是 Markdown 文本
- 必传:explore/search 要 `query`;callers/callees/impact 要 `symbol`;node 要 `file` 或 `symbol`
- `projectPath`:跨项目、gateway server 上必填

## 6.6 常见踩坑

1. **忘传 `projectPath`**:gateway 模式 server 拒收,返错而非猜默认。
2. **`CODEGRAPH_MCP_TOOLS` 多写 `codegraph_` 前缀**:变成"找不到该 tool"。正确:`explore,search,...`。
3. **explore 没结果立刻 Read**:80% 是查询词不对。先 `files`/`status` 看索引,**别 grep 重做**。
4. **同名不传 `file` 消歧**:`callers foo` 大仓可能 20+ 定义。`callers foo file=src/foo.ts` 钉一个。
5. **`impact depth=10`** token 爆。默认 2 就够。
6. **改文件后立刻查**:索引滞后 ~1s。看到 "⚠️ Some files edited since last index sync" banner 时,Read 列出的文件确认。

## 6.7 下一章预告

第 7 章《CLI 命令行完全手册》把这些 tool 的命令行对偶——`codegraph explore`、`node`、`callers`、`callees`、`impact`、`query`、`files`、`status`——逐个拆,讲 20 个业务子命令的 flag、JSON 输出、脚本化用法。不用 MCP 客户端、想 shell loop 时翻它。

## 6.8 参考

- `src/mcp/tools.ts:536-746` — 8 个 tool 的 schema 真源
- `src/mcp/tools.ts` 内 `DEFAULT_MCP_TOOLS = new Set(['explore'])` — 默认只开 explore
- `src/mcp/tools.ts:748-765` `requireProjectPath` — 无 default project 时把 `projectPath` 标 required
- `src/mcp/server-instructions.ts:20-70` — server 启动时灌给 client 的指令文本(含 anti-patterns)
- 第 2 章 — 5 分钟安装 + 注册 MCP server
- 第 5 章 — 前置依赖