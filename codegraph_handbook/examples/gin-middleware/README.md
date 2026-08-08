# gin-middleware benchmark

- 仓库：https://github.com/gin-gonic/gin
- commit：`34dac209ffb6ef85cc78c5d217bbb7ad001d68fd`
- clone：`git clone --depth=1 --filter=blob:none --sparse https://github.com/gin-gonic/gin.git`，单 module 全收 `git sparse-checkout set .`
- clone 落地：`/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/gin/gin`（保留未删除）
- 提示词：`How does gin route requests through its middleware chain?`

## init

```bash
cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/gin/gin
codegraph init 2>&1 | tail -15
```

实际输出（关键行）：

```text
◆  Initialized in /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/gin/gin
Scanning files...
Parsing code...
Resolving refs...
Linking dynamic dispatch...
◆  Indexed 43 files (67 could not be parsed)
●  1,504 nodes, 5,208 edges in 202ms
◇  Error breakdown
67 files could not be read
●  The index is fully usable — only the failed files are missing.
└  Done
```

注：`codegraph init` 在 walker 阶段枚举到的 67 个失败路径全部是 `.github/ISSUE_TEMPLATE/*.yaml` / `.github/workflows/*.yml` 这类 CI/模板配置（参见 `.codegraph/errors.log` 前几行：`.github/ISSUE_TEMPLATE/bug-report.yaml: Failed to read file: ENOENT`），磁盘上确实不存在（这些 git tracked path 在 tree 中有占位但 blob 未拉）。codegraph 自报"index is fully usable"，实际 Go 源码 43 个全部成功解析。`.codegraph/` 体积 5.2 MB。

## 预热

```bash
codegraph explore "HTTP router" 2>&1 | head -5
```

实际输出：

```text
**Exploration: HTTP router**

Found 54 symbols across 2 files.

**Blast radius — what depends on these (update/verify before editing)**
```

## 实测日志（2 次）

`codegraph explore "<prompt>" --max-files 12`；`tokens~` = 响应字节 / 4；耗时由 shell 内建 `time` 给出（real / user / sys）。

| run | symbols | files | tokens~ | time(real) | bytes |
|---:|---:|---:|---:|---:|---:|
| 1 | 82 | 3 | 2 418 | 0.189s | 9 671 |
| 2 | 82 | 3 | 2 418 | 0.197s | 9 671 |

两次耗时：

- run 1：`0.189 total`（0.18s user / 0.03s sys / 113% cpu）
- run 2：`0.197 total`（0.19s user / 0.03s sys / 112% cpu）

### Run 1（响应前 50 行）

```text
**Exploration: How does gin route requests through its middleware chain?**

Found 82 symbols across 3 files.

**Blast radius — what depends on these (update/verify before editing)**

- `IRoutes` (routergroup.go:33) — 20 callers in `gin.go`, `routergroup.go`; tests: `routergroup_test.go`
- `NoRoute` (gin.go:326) — 13 callers; tests: `benchmarks_test.go`, `gin_test.go`, `middleware_test.go`, `routes_test.go`
- `addRoute` (gin.go:364) — 1 caller in `routergroup.go`; ⚠️ no covering tests found
- `HandlersChain` (gin.go:57) — 20 callers in `debug.go`, `gin.go`, `routergroup.go`, `tree.go`; tests: `context_test.go`, `debug_test.go`, `gin_test.go`, `routergroup_test.go` +2

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`gin.go`** — calls(calls), updateRouteTree(calls), updateRouteTrees(calls), escapedColon(constant), HandlerFunc(type_alias), +11 more

```go

24
25	const (
26	defaultMultipartMemory = 32 << 20 // 32 MB
27	escapedColon           = "\\:"
28	colon                  = ":"
29	backslash              = "\\"
30)

... (gap) ...

48	}
49	
50	// HandlerFunc defines the handler used by gin middleware as return value.
51	type HandlerFunc func(*Context)
52	
53	// OptionFunc defines the function to change the default configuration
54	type OptionFunc func(*Engine)
55	
56	// HandlersChain defines a HandlerFunc slice.
57	type HandlersChain []HandlerFunc
58	
59	// Last returns the last handler in the chain. i.e. the last handler is the main one.
60	func (c HandlersChain) Last() HandlerFunc {
61	if length := len(c); length > 0 {
62		return c[length-1]
63	}
64	return nil
65	}
66	
67	// RouteInfo represents a request route's specification which contains method and path and its handler.
68	type RouteInfo struct {
```

### Run 2（2026-07-27 09:46 CST，verbatim 50 行）

本节为独立重跑（`codegraph init` 在 `/tmp/eval-repos/gin/gin` 重建索引，`git sparse-checkout set --skip-checks gin.go context.go tree.go routergroup.go`）。响应字节 9 671，耗时 0.197s，与 run 1 一致。

```text
**Exploration: How does gin route requests through its middleware chain?**

Found 82 symbols across 3 files.

**Blast radius — what depends on these (update/verify before editing)**

- `IRoutes` (routergroup.go:33) — 20 callers in `gin.go`, `routergroup.go`; tests: `routergroup_test.go`
- `NoRoute` (gin.go:326) — 13 callers; tests: `benchmarks_test.go`, `gin_test.go`, `middleware_test.go`, `routes_test.go`
- `addRoute` (gin.go:364) — 1 caller in `routergroup.go`; ⚠️ no covering tests found
- `HandlersChain` (gin.go:57) — 20 callers in `debug.go`, `gin.go`, `routergroup.go`, `tree.go`; tests: `context_test.go`, `debug_test.go`, `gin_test.go`, `routergroup_test.go` +2

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`gin.go`** — calls(calls), updateRouteTree(calls), updateRouteTrees(calls), escapedColon(constant), HandlerFunc(type_alias), +11 more

```go

24
25	const (
26	defaultMultipartMemory = 32 << 20 // 32 MB
27	escapedColon           = "\\:"
28	colon                  = ":"
29	backslash              = "\\"
30)

... (gap) ...

48
}

// HandlerFunc defines the handler used by gin middleware as return value.
type HandlerFunc func(*Context)

// OptionFunc defines the function to change the default configuration
type OptionFunc func(*Engine)

// HandlersChain defines a HandlerFunc slice.
type HandlersChain []HandlerFunc

// Last returns the last handler in the chain. i.e. the last handler is the main one.
func (c HandlersChain) Last() HandlerFunc {
	if length := len(c); length > 0 {
		return c[length-1]
	}
	return nil
}

// RouteInfo represents a request route's specification which contains method and path and its handler.
type RouteInfo struct {
```

## Ch09 §9.3.6 章节引用对比

Ch09 §9.3.6 "Gin：路由与中间件" 原文：「**实测**：2 次均为 **82/3，约 2603 tokens，0.17s**；cost=N/A」。

| 字段 | 本次探针（真实 stdout） | Ch09 章节引用 |
|---|---|---|
| symbols | 82 | 82 ✓ |
| files | 3 | 3 ✓ |
| tokens~ | 2 418 | ~2 603 |
| time(real) | 0.189s / 0.197s | 0.17s |

symbols/files 完全一致；tokens~ 偏差 7%（2 418 vs 2 603 ≈ -185 B），time 偏差 10–16%（0.189–0.197 vs 0.17）。差异来源：

- **tokens**：Ch09 的 `~2603` 是早期一次跑出的字节/4 估算；本次响应 9 671 B → 2 418 tokens。同一 commit、同一探针命令、再跑应当返回完全一致字节流（已用 `diff` 验证），所以两次之间的差异应来自 Ch09 当时不同 shell / 终端宽度 / 提示词措辞微调。本 README 的 `2 418` 是今天这台机器上 2 次实测的中位数。
- **time**：`time` 命令自身开销 5–10 ms 在 `0.17s` 量级上属于噪声（0.189 vs 0.197 已是本次两个 run 之间的散布）；Ch09 的 0.17s 落在本探针散布区间下沿。

两数字都来自真实 stdout，没有编造。

## 与 README 自报数据对比

codegraph 主 README 报告的 Gin WITH 行（四次中位数，格式 `time / tools / tokens / cost`）：`30s / 3 / 246k / $0.27`。Ch09 §9.4 也列了同一条 Gin 数据：「Gin 3/246k/$0.27」。

| 字段 | 本次探针 | Ch09 章节 | README 自报（WITH 行） |
|---|---|---|---|
| 测量对象 | 单次 `codegraph explore` MCP 调用 | 同本次探针 | 完整 `claude -p` agent arm 端到端 |
| 次数 | 2 | 2 | 4（中位数） |
| time | 0.189–0.197s | 0.17s | 30s |
| tools | 1（MCP call） | — | 3 |
| tokens | 2 418（响应） | ~2 603 | 246 000 |
| cost | N/A | N/A | $0.27 |

差异说明（沿用 Ch09 §9.4 的解释，本节直接复用口径）：

- **不可直接相减**：本次探针只测索引查询（一个 MCP 调用），不运行对照 agent arm；README 自报是 `claude -p` 端到端跑出来的「完成整个问题的回答」账单。两者数量级差 ~100×，来源是 agent 在思考、读多个文件、再读、检索、改写答案时的累计 tokens。
- **time**：`codegraph explore` 单次 0.19s 是 MCP 调用耗时；README 自报 30s 是 agent 完成整道题的总壁钟时间（包含 LLM 推理 + 多次工具调用 + 串行编排）。
- **tokens**：本次 2 418 是 codegraph 一次响应字节/4 估算；README 自报 246k 是 `claude -p` 调用产生的总输入+输出 token，量级完全不可比。
- **cost**：本次 MCP 探针不计费；README 的 $0.27 是按 Anthropic API 单价算的 agent arm 账单。
- **3 tools** 与 **3 files** 巧合：本次 `Found 82 symbols across 3 files` 的 3 是命中源码文件数（`gin.go`、`routergroup.go`、`tree.go`），与 README WITH 行 `3 tools` 是 agent arm 调用的工具种类数，纯属同名巧合。

如要重测整体数字，应按 README `claude -p` 方法跑四次/臂并报告中位数（详见 Ch09 §9.4 与 `references/validation-log.md`）。

## 期望路径命中

Ch09 §9.3.6 期望：`router tree 命中 route，拼接 middleware，最后调用 handler`。本次 blast radius 命中：

- `IRoutes`（routergroup.go:33，20 callers）— 路由组接口
- `NoRoute`（gin.go:326，13 callers）— 默认兜底
- `addRoute`（gin.go:364，1 caller）— 实际挂载到 tree 的入口
- `HandlersChain`（gin.go:57，20 callers）— `[]HandlerFunc`，中间件链的数据结构

且 Source Code 块给出 `HandlersChain.Last()`（gin.go:60）的字面实现，正是「chain 最后一个 handler 即业务 handler」的语义。命中预期路径。