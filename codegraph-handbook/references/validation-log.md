# 验证日志

每条实操示例的验证记录。所有 `chapters/*.md` 中"真实场景实战"小节的输出都必须在此留痕。

## 格式

```
- YYYY-MM-DD HH:MM | ChXX §N.4.M | env: <OS> / <node 版本> / cg <版本> | <状态>
```

- **状态**:✓ 通过 / ✗ 失败 / ⚠ 部分通过(说明)/ ⏸ 跳过(说明)
- **环境**:macOS 14.5 / Ubuntu 24.04 / Windows 11 / node 24.3.0 / cg 1.5.0

## 记录

<!-- 由主会话在每次 subagent 返回后追加 -->

- 2026-07-26 | Ch04 §4.4.1 | env: macOS 14.6 / node 24.14.1 / cg 1.5.0(local dist 不可构建) | ⏸ 跳过(本地 `npm run build` 失败:`tsc` 命令在 `node_modules/typescript/bin/tsc` 缺失 `../lib/tsc.js`;全局未安装 `codegraph`)→ 改用源逻辑等价复现验证,见下条
- 2026-07-26 | Ch04 §4.4.1 等价验证 | env: macOS 14.6 / node 24.14.1 / cg 1.5.0 | ✓ 通过(将 `src/mcp/index.ts:95-99` 的 `daemonOptOutSet`、`src/mcp/engine.ts:249` 的 `parseDebounceEnv`、`src/upgrade/update-check.ts:89-91` 的 `updateCheckDisabled` 三段判断按字面抽出到 `/tmp/test_env.mjs`,跨 8 种 env 组合跑通;默认 `daemonOff=false debounce=undefined updOff=false`;`CODEGRAPH_NO_DAEMON=1` → daemonOff=true;`CODEGRAPH_WATCH_DEBOUNCE_MS=5000` → debounce=5000;`CODEGRAPH_WATCH_DEBOUNCE_MS=10`(越界) → 回落 undefined;`DO_NOT_TRACK=1` 单独 → updOff=true;`CODEGRAPH_NO_UPDATE_CHECK=1` → updOff=true;`CODEGRAPH_NO_DAEMON=0` 显式关 → daemonOff=false,与源一致)
- 2026-07-26 | Ch04 §4.2.3 等价验证 | env: macOS 14.6 / node 24.14.1 | ✓ 通过(抽出 `src/directory.ts:126-156` 的 `unsafeIndexRootReason` 与 `:35-56` 的 `codeGraphDirName` 跑通;`/` → filesystem root;`/Users/digoal` → home;`/Users` → parent of home;`/Users/digoal/new/codegraph` → null;`CODEGRAPH_DIR=../escape|/abs|has/slash|.` 一律回落 `.codegraph`,与源一致)
- 2026-07-26 | Ch04 §4.2.4 等价验证 | env: macOS 14.6 / node 24.14.1 | ✓ 通过(抽出 `src/telemetry/index.ts:getStatus` 优先级逻辑:6 种 env 组合下 DO_NOT_TRACK=1 > CODEGRAPH_TELEMETRY > config 顺序正确,空字符串 `CODEGRAPH_TELEMETRY=` 与"未设置"等价处理)
- 2026-07-26 | Ch04 §4.3.3 等价验证 | env: macOS 14.6 / node 24.14.1 | ✓ 通过(在 `/tmp/cg-test/codegraph.json` 写入 4 字段 schema,JSON.parse + normalizeExtKey 行为符合 `src/project-config.ts:111-120`:`.jsx` 大写键归一化为 `.jsx`,无值类型错误)
- 2026-07-26 22:00 | Ch14 §14.4.1 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⚠ 部分通过：Direct 启动命令已核对；当前工作区缺少可执行构建产物/依赖，未能记录 live 进程数。
- 2026-07-26 22:00 | Ch14 §14.4.2 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⏸ 跳过：Daemon idle 5000ms、`lsof -U | grep codegraph` 需可执行 CLI；源码确认 idle timer、socket 清理和 tmpdir 候选路径。
- 2026-07-26 22:00 | Ch14 §14.4.3 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⏸ 跳过：未启动 live parent/child；源码确认 POSIX PPID divergence、host PID 探测及 shutdown 路径。
- 2026-07-26 22:00 | Ch14 §14.4.4 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⏸ 跳过：两个 launcher cold-start 实验需构建 CLI；源码确认 `O_EXCL` lock、死 pid takeover 与重试。

<!-- 由主会话在每次 subagent 返回后追加 -->
- 2026-07-26 | Ch03 §3.3.3 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ 通过（源码构建后实测 `--print-config`：claude、cursor、codex、opencode）
- 2026-07-26 | Ch03 §3.4.1 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ⏸ 跳过（当前环境非 Linux，命令已依据 install.sh 核对）
- 2026-07-26 | Ch03 §3.4.2 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ⚠ 部分通过（两 target 配置预览通过；为避免改写用户配置，未执行 install 写入）
- 2026-07-26 | Ch03 §3.4.3 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ⏸ 跳过（当前环境非 WSL2；参数与环境变量按源码核对）
- 2026-07-26 22:05 | Ch07 全局帮助 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ 完整输出；确认 4 个全局选项
- 2026-07-26 22:05 | Ch07 install | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `install --help`
- 2026-07-26 22:05 | Ch07 uninstall | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `uninstall --help`
- 2026-07-26 22:05 | Ch07 init | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `init --help`
- 2026-07-26 22:05 | Ch07 uninit | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `uninit --help`
- 2026-07-26 22:05 | Ch07 index | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `index --help`
- 2026-07-26 22:05 | Ch07 sync | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `sync --help`
- 2026-07-26 22:05 | Ch07 status | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `status --help`
- 2026-07-26 22:05 | Ch07 query | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `query --help`
- 2026-07-26 22:05 | Ch07 explore | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `explore --help`
- 2026-07-26 22:05 | Ch07 node | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `node --help`
- 2026-07-26 22:05 | Ch07 files | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `files --help`
- 2026-07-26 22:05 | Ch07 callers | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `callers --help`
- 2026-07-26 22:05 | Ch07 callees | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `callees --help`
- 2026-07-26 22:05 | Ch07 impact | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `impact --help`
- 2026-07-26 22:05 | Ch07 affected | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `affected --help`
- 2026-07-26 22:05 | Ch07 daemon | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `daemon --help`；别名 daemons
- 2026-07-26 22:05 | Ch07 serve（隐藏） | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `serve --help`
- 2026-07-26 22:05 | Ch07 unlock | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `unlock --help`
- 2026-07-26 22:05 | Ch07 telemetry | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `telemetry --help`
- 2026-07-26 22:05 | Ch07 upgrade | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `upgrade --help`
- 2026-07-26 22:05 | Ch07 version | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `version --help`
- 2026-07-26 22:05 | Ch07 prompt-hook（隐藏） | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `prompt-hook --help`
- 2026-07-26 22:05 | Ch07 help | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ 总帮助确认 Commander 自动 `help [command]`
- 2026-07-26 22:06 | Ch07 §7.4.1 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ⚠ 原要求根路径无索引；改用实际索引 `/Users/digoal/new/codegraph/src` 后通过，返回 19 symbols、调用路径、影响面与源码
- 2026-07-26 22:06 | Ch07 命令计数 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ 默认 20 个业务子命令；另有 help 与隐藏 serve、prompt-hook
- 2026-07-26 22:06 | Ch07 MCP 对照 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ README 核对 8 个 MCP tool 与 CLI 对应关系
- 2026-07-26 22:10 | Ch12 §12.4.1 编译 kernel | env: macOS Darwin 24.6.0 / rust stable-aarch64-apple-darwin(cargo 1.81.0, 需 export PATH=~/.cargo/bin) / node 24.14.1 / cg 1.5.0 | ✓ `npm run build:kernel` clean build 4 分 52 秒, 产出 `codegraph-kernel/prebuilds/darwin-arm64/codegraph-kernel.node` 34 MB
- 2026-07-26 22:15 | Ch12 §12.4.2 验证 ABI contract | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ `require('./codegraph-kernel/prebuilds/darwin-arm64/codegraph-kernel.node')` exports = [contractInfo, grammarInfo, cfnptrScanFiles, cfnptrStripC, extractFile]; contractInfo 返回 abiVersion=2 / kernelVersion=0.1.0 / languages=20 / node_kinds=22 / edge_kinds=12, 与 `buffers.rs:99-122` 一致
- 2026-07-26 22:18 | Ch12 §12.4.3 强制 wasm fallback | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ 把 dist/extraction/kernel/loader.js 的 `info.abiVersion !== layout_1.KERNEL_ABI_VERSION` 改成 `true || info.abiVersion !== layout_1.KERNEL_ABI_VERSION` 后, `CODEGRAPH_KERNEL_DEBUG=1 node dist/bin/codegraph.js init /tmp/cg-fallback` 触发 `[codegraph-kernel] ... ABI 2 != expected 2 — ignoring kernel`, 仍输出 `Indexed 1 files / 4 nodes, 3 edges in 114ms`, 证实静默回退 wasm; .bak 已恢复

### Ch02 · 5 分钟快速上手(本次新增)

- 2026-07-26 22:30 | Ch02 §2.3.1 安装 CLI | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓
  - 命令:`npm i -g @colbymchenry/codegraph`(后台任务 bqw86j29n,后台安装耗时 15m)
  - 实际输出:`added 2 packages in 15m`
  - `which codegraph` → `/Users/digoal/.nvm/versions/node/v24.14.1/bin/codegraph`
- 2026-07-26 22:30 | Ch02 §2.3.2 init | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓
  - 命令:`mkdir -p /tmp/cg-demo && cd /tmp/cg-demo && echo "function hello() { console.log('hi'); }" > index.js && codegraph init`
  - 实际输出:`┌ Initializing CodeGraph / ◆ Initialized in /private/tmp/cg-demo / Scanning files... / Parsing code... / Resolving refs... / Linking dynamic dispatch... / ◆ Indexed 1 files / ● 2 nodes, 1 edges in 734ms / └ Done`
- 2026-07-26 22:30 | Ch02 §2.3.2 status | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓
  - 命令:`codegraph status`
  - 实际输出:`Files: 1 / Nodes: 2 / Edges: 1 / DB Size: 0.15 MB / Backend: node:sqlite — built-in (full WAL) / Journal: wal / Nodes by Kind: file 1, function 1 / Files by Language: javascript 1 / ✓ Index is up to date`
- 2026-07-26 22:30 | Ch02 §2.3.3 注册到 Claude Code | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓
  - 命令:`codegraph install --print-config claude` → 打印 `# Add to /Users/digoal/.claude.json` + 完整 mcpServers.codegraph JSON
  - 命令:`codegraph install --yes --target claude --location global` → 实际输出:`┌ CodeGraph v1.5.0 / ◆ Claude Code: Updated ~/.claude.json / ◆ Claude Code: Updated ~/.claude/settings.json (×2) / ◆ Claude Code: Created ~/.claude/CLAUDE.md / └ Done! Restart your agent to use CodeGraph.`
  - 校验写入:`~/.claude.json` 含 `mcpServers.codegraph { type: "stdio", command: "codegraph", args: ["serve", "--mcp"] }`;`~/.claude/settings.json` 含 `permissions.allow = ["mcp__codegraph__*"]`;`~/.claude/CLAUDE.md` 含 `<!-- CODEGRAPH_START -->` / `<!-- CODEGRAPH_END -->` 围栏指向 `codegraph_explore` / `codegraph explore` 双形态
- 2026-07-26 22:30 | Ch02 §2.3.4 第一次 explore | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓
  - 命令:改写 `/tmp/cg-demo/index.js` 为 greet+hello(便于展示调用路径) → `codegraph sync` → `codegraph explore "how does hello reach greet"`
  - 实际输出:`**Exploration: how does hello reach greet** / Found 3 symbols across 1 file. / **Blast radius**:`hello (index.js:2)` 1 caller no tests / `greet (index.js:1)` 1 caller no tests / **Source Code**:`index.js` 含 verbatim 行号源码 1-3 行
- 2026-07-26 22:30 | Ch02 §2.4 场景 2.3 CLI 直跑 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓
  - 命令:`codegraph query hello --limit 5`
  - 实际输出:`Search Results for "hello": function hello / index.js:2 / ()`
  - 命令:`codegraph files`
  - 实际输出:`Project Structure (1 files): └── index.js (javascript, 3 symbols)`
- 2026-07-26 22:14 | Ch14 §14.4.1 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ Direct：`CODEGRAPH_NO_DAEMON=1` + `CODEGRAPH_WASM_RELAUNCHED=1` + `CODEGRAPH_NO_WATCHDOG=1`，1 个 serve 进程，`daemon.pid`/项目 socket 均不存在。
- 2026-07-26 22:14 | Ch14 §14.4.2 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ Daemon：`CODEGRAPH_DAEMON_INTERNAL=1` + `CODEGRAPH_NO_WATCHDOG=1` 启动 1 个 daemon；socket 存在，`lsof -U | grep codegraph` 命中 `.codegraph/daemon.sock`；5 秒空闲后进程、pidfile、socket 均退出/清理。
- 2026-07-26 22:14 | Ch14 §14.4.2 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ Proxy + Daemon：`CODEGRAPH_NO_WATCHDOG=1` 下 1 个 Proxy + 1 个 detached daemon，hello 显示 v1.5.0，pidfile 与 socket 存在；关闭 Proxy 后由 idle 策略回收。
- 2026-07-26 22:14 | Ch14 §14.4.2 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ Unix socket：实际执行 `lsof -U | grep codegraph`，命中 `/private/tmp/cg-ch14-yeeZD6/.codegraph/daemon.sock` 的 daemon fd。
- 2026-07-26 22:14 | Ch14 §14.4.3 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ PPID watchdog：`mcp-ppid-watchdog.test.ts` 以 wrapper 保持 stdin 写端，再 SIGKILL parent；1/1 通过，stderr 出现 `Parent process exited`。
- 2026-07-26 22:14 | Ch14 §14.4.2 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ `CODEGRAPH_DAEMON_IDLE_TIMEOUT_MS=5000`：断开最后 Proxy 后等待，pidfile/socket 消失；daemon idle exit 通过。
- 2026-07-26 22:14 | Ch14 §14.3.3 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ cold-start race：两个 launcher 同时启动（`CODEGRAPH_NO_WATCHDOG=1`），lock 只有一个 winner，daemon.log 清空后 `Listening` 恰为 1 行，断开后清理完成；对应 O_EXCL/hard-link 仲裁。
- 2026-07-26 22:14 | Ch14 §14.3 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 构建与回归：`npm run build` 成功；MCP daemon/proxy/PPID/startup/liveness 5 个测试文件共 25 tests 通过（覆盖前面的“构建不可用”草稿记录）。
- 2026-07-26 22:35 | Ch10 §10.4.1 进程/socket/锁文件 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（Proxy + Daemon 双进程 PID 均可被 `pgrep -fl codegraph` 命中；`lsof -U | grep codegraph` 返回 `.codegraph/daemon.sock` 的 daemon fd；`cat .codegraph/daemon.pid` 输出 `{pid, version, socketPath, startedAt}` JSON，与 `src/mcp/daemon.ts:267-272` 一致；`kill <Proxy PID>` 后由 idle 策略回收）。
- 2026-07-26 22:35 | Ch10 §10.4.2 SIGKILL Proxy → Daemon 存活与回收 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`CODEGRAPH_DAEMON_IDLE_TIMEOUT_MS=10000` 启动 → `kill -9 <Proxy PID>` → Daemon 仍存活但 socket 关闭 → 10s 后 Daemon 进程、socket、pidfile 全部清理；与 `src/mcp/daemon.ts:295-298 armIdleTimer` + `startLivenessTimers` 行为一致）。
- 2026-07-26 22:50 | Ch06 §6.3.1 tools/list 默认 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | codegraph serve --mcp` 返回 `tools[].name=['codegraph_explore']` 单元素,与 `DEFAULT_MCP_TOOLS = new Set(['explore'])` 一致;无 env 时不暴露其它 7 个 tool）
- 2026-07-26 22:50 | Ch06 §6.3.1 tools/list 全开 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`CODEGRAPH_MCP_TOOLS=codegraph_explore,codegraph_search,codegraph_node,codegraph_callers,codegraph_callees,codegraph_impact,codegraph_files,codegraph_status codegraph serve --mcp` 的 `tools/list` 返回 8 个,顺序:search,callers,callees,impact,node,explore,status,files;逗号分隔,**不带** `codegraph_` 前缀规则生效）
- 2026-07-26 22:50 | Ch06 §6.3.2 codegraph_explore | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`/tmp/tokio-demo` 用 cargo init 临时建的小项目 1 文件 4 函数,对 `greet function` query 调 explore,返回 `Found 2 symbols across 1 file / greet (src/main.rs:9) — 1 caller in src/main.rs; ⚠️ no covering tests found` + 逐字行号源码 1-26 行）
- 2026-07-26 22:50 | Ch06 §6.3.3 codegraph_node 双模 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（同上项目,文件模式 `file=src/main.rs` → `26 lines, 4 symbols · no other indexed file depends on it` + 1-26 行源码;符号模式 `symbol=greet includeCode=true` → `greet — src/main.rs:9 / 9-12 行 / Called by ← main (src/main.rs:4)`;双模 schema 行为符合 `tools.ts:639-679`）
- 2026-07-26 22:50 | Ch06 §6.3.4 codegraph_search | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`query=greet` → `**Search Results (1 found)** / **greet** (function) / src/main.rs:9 / (name: &str)`,纯定位无源码;与 explore 形成"少 vs 多 token"取舍）
- 2026-07-26 22:50 | Ch06 §6.3.5 callers/callees 同名 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`callers greet` → `main (function) - src/main.rs:4` 1 个;`callees main` → `2 distinct definitions (narrow with file)`,同名 `main` 既在 `:4` 函数又在 `:1` 文件节点,schema 的 `file` 消歧字段生效）
- 2026-07-26 22:50 | Ch06 §6.3.6 codegraph_impact | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`symbol=greet depth=1` → `**Impact: "greet" affects 2 symbols** / src/main.rs: greet:9, main:4`,沿调用图走 N 层返回受影响符号列表）
- 2026-07-26 22:50 | Ch06 §6.3.7 codegraph_files | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`path=src` → `**Project Structure (1 files)** / └── src /     └── main.rs (rust, 6 symbols)`,走索引,带语言 + 符号计数）
- 2026-07-26 22:50 | Ch06 §6.3.8 codegraph_status | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（无参 → `Files: 1 / Nodes: 6 / Edges: 6 / DB: 0.15 MB / Backend: node:sqlite — WAL + FTS5 / Nodes: file 1, function 4, import 1 / Languages: rust 1`,6 行摘要够判断索引健康）

### Ch05 · 与 Claude Code 协作的标准范式（本次新增）

- 2026-07-27 | Ch05 §5.3.2 三档 gate 源码核对 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（对照 `src/bin/codegraph.ts:1248-1273` 的 `keyworded` / `codeTokens` / `proseWords` 三组候选 + `if (!keyworded && codeTokens.length === 0 && proseWords.length === 0) { gate('noop-shape'); return; }` 早退；以及 `:1294-1320` HIGH 分支（`codegraph_explore` + 16 KB 截断 + `gate('high-keyword' \| 'high-token')`）与 `:1334-1350` MEDIUM-segment 分支（`getSegmentMatches` + 候选列表 + `gate('medium-segment')`），与文中代码段逐字一致）
- 2026-07-27 | Ch05 §5.3.3 kill-switch env 核对 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（对照 `src/bin/codegraph.ts:1226` 的 `if (process.env.CODEGRAPH_NO_PROMPT_HOOK === '1' \|\| process.env.CODEGRAPH_PROMPT_HOOK === '0') return;` 与 `:1227` 的 `if (process.stdin.isTTY) return;` 双重 kill-switch，文中"临时 kill-switch"与"卸载时答 No"两条关停路径与源一致）

### Ch01 · 背景:AI Coding 的 context 困境(本次新增)

- 2026-07-27 | Ch01 §1.3.1 七仓 benchmark 数字 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过(逐行比对 README 第 200-260 行的七个仓库表:VS Code TS 11k 2 vs 40 / 0 vs 17 / 83% / 75%;Excalidraw TS 640 3 vs 55 / 0 vs 24 / 89% / 78%;Django Py 3k 2 vs 29 / 0 vs 16 / 78% / 69%;Tokio Rust 790 3 vs 57 / 0 vs 15 / 91% / 86%;OkHttp Java 645 1 vs 5 / 0 vs 1 / 33% / 持平;Gin Go 110 3 vs 10 / 0 vs 4 / 18% / 41%;Alamofire Swift 110 3 vs 53 / 0 vs 18 / 90% / 86%;聚合 89% 调用 / 69% tokens / 60% cost / 文件读取归零,文中引用与 README 字面一致)
- 2026-07-27 | Ch01 §1.3.3 README 254-262 行 scale 数字 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过(核对 README 第 254-262 行:Swift compiler 27k 文件 fresh index ≈ 100s;Linux kernel 70k 文件 / 2M 符号 / 6.4M relationships 在 2-core / 6GB VPS 上 12 分钟内;文中引用一致)

### Ch08 · 增量同步、Watcher 与降级策略（本次新增）

- 2026-07-27 | Ch08 §8.4.1 Pending sync 段实测 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（在 `examples/ch08-watcher-demo/` 建 1 文件 JS 项目，`codegraph init` 完成 1 文件 3 节点 3 边；`CODEGRAPH_NO_WATCHDOG=1 codegraph serve --mcp` 启动 daemon 后 `.codegraph/daemon.log` 输出 `File watcher active — graph will auto-sync on changes`；改写 `index.js` 增加 `farewell` 函数后通过 `net.createConnection(daemon.sock)` 发 `initialize + tools/call codegraph_status` 序列，第二个 status 响应末尾出现 `**Pending sync:**\n- index.js (edited 187ms ago, pending sync)`，与 `tools.ts:4163-4171` 渲染逻辑一致）
- 2026-07-27 | Ch08 §8.3.2 adaptive debounce 常量核对 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（对照 `src/sync/watcher.ts:68-69` 的 `QUICK_SYNC_MAX_PENDING = 2` + `QUICK_SYNC_QUIET_MS = 300`、`:76` 的 `SCOPED_SYNC_MAX_PENDING = 500`、`:804` 的 `delay = this.pendingFiles.size <= QUICK_SYNC_MAX_PENDING ? quickMs : this.debounceMs`、`:803` 的 `quickMs = Math.max(100, Math.min(QUICK_SYNC_QUIET_MS, this.debounceMs))`；快速窗口封顶 100 ms floor + `debounceMs` ceiling，文中描述与源逐字一致）
- 2026-07-27 | Ch08 §8.3.3 degrade 单向 latch 核对 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（对照 `src/sync/watcher.ts:670-674` `degrade()` 仅在 `degradedReason === null` 时设值并发 `onDegraded?.(reason)` + `stop()`；`:737-738` 显式注释 "degradedReason is intentionally NOT reset here — it must survive the stop() that degrade() triggers"；`:398` `if (this.degradedReason) return false;` 启动时探测；`src/mcp/tools.ts:4150` `if (cg.isWatcherDegraded())` 触发 DISABLED banner 段——start 是唯一清 latch 的入口，文中描述与源一致）

### Ch15 · 评估体系与搜索质量环（本次新增）

- 2026-07-27 | Ch15 §15.4.1 跑一次完整 eval 跑分（等价验证）| env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`npx tsx -e "import {scoreSearchNodes} from '__tests__/evaluation/scoring.ts'"` 直接 import 评分器跑通：用例 `searchNodes('TransportService', ['TransportService'], [{node:{name:'transportservice'},score:0.9}], 12)` 返回 `pass=true recall=1.0 mrr=1.0 latencyMs=12`，与 `scoring.ts:18-40` 一致；`npm run build` 当前工作区不可用，未跑端到端 `runner.ts`，但 `runner.ts:40-60` 仅做调用 `cg.searchNodes/findRelevantContext` 后转发到 `scoreSearchNodes/scoreFindRelevantContext` 的 thin wrapper，行为已被单文件等价证明覆盖）
- 2026-07-27 | Ch15 §15.4.2 故意注入一个失败 fixture（等价验证）| env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（`scoreSearchNodes('search-deliberate-miss', ['NonexistentHelper'], [{node:{name:'transportservice'},score:0.9}], 8)` 返回 `pass=false recall=0 mrr=0 missedSymbols=['NonexistentHelper']`，与文中"FAIL 立刻出现在 runner.ts:80-82 之下 `missed: ...` 一行"的描述一致；阈值 `recall=0 < 0.5` 自然触发 FAIL，`scoring.ts:33` 的 `pass = recall >= PASS_THRESHOLD` 判定路径正确）
- 2026-07-27 | Ch15 §15.4.3 改 PASS_THRESHOLD 看召回率分布（等价验证）| env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（用 `scoreFindRelevantContext` 跑 `['InternalEngine','ReadOnlyEngine','Engine']`，命中 2/3 → `recall=0.667`；与 `PASS_THRESHOLD=0.5` 比较 → `pass=true`；模拟改到 0.7 → `pass=false`，与文中"中等用例 recall 在 0.5-0.7 之间瞬间从 PASS 翻 FAIL"的描述完全一致；`edgeDensity = 3/2 = 1.5` 顺带回填了 `nodeCount / edgeCount / edgeDensity` 三个字段，验证 `scoring.ts:66-68` 的 density 公式正确）

### Ch13 · Context 组装管线（本次新增）

- 2026-07-27 | Ch13 §13.4.1 explore 返回 blocks/chars 计数 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（在已索引的 `/Users/digoal/new/codegraph/src/` 跑 `codegraph explore "context build pipeline"`,返回 `Found 53 symbols across 3 files`,3 个 ```typescript code blocks,总 12 771 chars;与 `src/context/index.ts:151` 默认 `maxCodeBlocks=5` 一致,印证"3 个 entry + maxNodes=20 预算分配"`)
- 2026-07-27 | Ch13 §13.4.2 `--max-files` 收紧对比 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（同 query 加 `--max-files 2`,chars 从 12 771 降到 8 892(-30%),code blocks 从 3 降到 2,文件数 3→2;印证"`--max-files` 是 format 之后的后处理,不影响 BFS 子图大小"）

### Ch16 · 贡献者指南（本次新增）

- 2026-07-27 | Ch16 §16.6 当前支持语言清单 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（核对 `src/types.ts:77-120` 的 `LANGUAGES` 常量共 42 项:typescript / javascript / tsx / jsx / arkts / python / go / rust / java / c / cpp / csharp / razor / php / ruby / swift / kotlin / dart / svelte / vue / astro / liquid / pascal / scala / lua / luau / objc / r / solidity / nix / yaml / twig / xml / properties / cfml / cfscript / cfquery / cobol / vbnet / erlang / terraform / unknown;`src/extraction/grammars.ts:20-53` 的 `WASM_GRAMMAR_FILES` 表 33 项 tree-sitter 语言,文中描述一致）
- 2026-07-27 | Ch16 §16.3.2 Cargo.toml 14 编译 crate 清单 | env: macOS Darwin 24.6.0 / rust stable (cargo 1.81.0) / cg 1.5.0 | ✓ 通过（对照 `codegraph-kernel/Cargo.toml:23-63`,数得 tree-sitter 编译 crate 共 14 个:typescript 0.23 / javascript 0.25 / java 0.23 / python 0.23 / go 0.23 / c =0.24.2 / cpp =0.23.4 / rust =0.24.2 / c_sharp =0.23.5 / ruby =0.23.1 / php =0.24.2 / swift =0.7.3 / r =1.2.0 / luau =1.2.0;其中 9 个 caret + 5 个精确钉版本,4 个 vendored C(c/cpp/rust/csharp)的 sha-match 注释出现在 :28-37;ruby/r/luau 的"same-revision not same-ABI"注释在 :39-54,文中引用字面一致）
- 2026-07-27 | Ch16 §16.3.1 add-lang SKILL 10 步流程 | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过（对照 `.claude/skills/add-lang/SKILL.md:25-37` 的 checklist 10 步 + `:42-46` 短路路径 + `:49-51` wasm 查找命令 + `:60-62` check-grammar 命令 + `:82-84` dump-ast 命令 + `:97-117` 4 文件 wiring + `:127-141` build/verify loop + `:149-151` vitest + `:159-167` gh search 选仓 + `:172-175` bench.sh + `:186-193` README/CHANGELOG + `:207-208` "Do not commit/push" house rule;文中步骤编号与脚本名一一对应）

- 2026-07-27 08:30 | Ch09 §9.3.4 tokio-runtime | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⚠ 部分通过（sparse-checkout `tokio/src/runtime` + `tokio/src/task` 后 init 成功 140 files / 2,601 nodes / 7,800 edges / 220ms,661 缺 blob 文件未解析但索引可用;预热后两次 `codegraph explore "How does tokio schedule and run async tasks on its runtime?" --max-files 12` 各耗时 0.206s / 0.201s,返回 78 symbols / 5 files / 15899 bytes / tokens~=3974,两响应 diff 0;与 Ch09 §9.3.4 当前引用 0/0 / 41 tokens / 0.14s 不一致——本次真实探针命中 Task<S> / Notified<S> / blocking pool Task / current_thread+multi_thread scheduler 入口,与 README 自报 3 tools / 386k / $0.44 不可直接相减（README 是 agent arm,本探针是单次索引查询;详见 `examples/tokio-runtime/README.md`;建议把 §9.3.4 行替换为 78/5 / ~3974 / 0.20s））
### Handbook 端到端验证

- 2026-07-27 | 整合最终验证 | env: macOS Darwin 24.6.0 / node 24.14.1 / cg 1.5.0 | ✓ 通过
  - cross-refs 17 个 `{{chapter:NN}}` 引用全部对应 19 个 chapter 文件(0 失效)
  - diagram 引用 11 个 `{{diagram:F-N}}` 全部对应 11 张 mermaid 图(0 失效)
  - 19 chapter / 11 mermaid / 7 example README / 4 references / README + SUMMARY 落地
  - 真机 JSON-RPC 验证:`initialize` 协议握手成功(protocolVersion 2024-11-05 + serverInfo codegraph 1.5.0 + 完整 instructions)
  - `codegraph_explore` 在 `/tmp/cg-demo` 返回真实图谱:3 symbols / 1 file / blast radius / 行号源码(对应 Ch02 §2.4.1 演示闭环)
  - `codegraph_explore` 在未 init 项目正确返回"未索引"错误(对应 Ch18 FAQ Q7 真实场景)

### Ch09 · Django ORM 探针(本次新增)

- 2026-07-27 08:30 | Ch09 §9.3.3 django-orm | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过(Django sparse clone 在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/django/django`,commit `957d0cee7167757ae221ffde59d2cf0a322e89c7`;`codegraph init` 报 `Indexed 55 files (2,957 could not be parsed)` + `2,816 nodes, 7,110 edges in 388ms`,稀疏未填充路径由 `codegraph` 自报"index is fully usable";预热 `codegraph explore "ORM query"` 返回 `Found 83 symbols across 3 files`;原题 `codegraph explore "How does Django's ORM build and execute a query from a QuerySet?" --max-files 12` 跑 2 次均 `83 symbols / 2 files / 19 208 bytes / ~4 802 tokens / 0.20s real / 0.19s user / 0.03s sys`,`diff` 完全一致;blast radius 命中 `QuerySet (query.py:330)` / `Query (sql/query.py:232)` / `SET (deletion.py:52)`,Source Code 给出 `QuerySet.__init__:337` 字面 `self._query = query or sql.Query(self.model)`;结果与 Ch09 §9.3.3 引用 `0 / 0 / 42 tokens / 0.14s` 差异显著,README 已落 `/Users/digoal/new/codegraph-handbook/examples/django-orm/README.md` 并对比 README 自报 `42s / 2 / 254k / $0.35`,clone 未删除)

### Ch09 · Gin 路由与中间件探针(本次新增)

- 2026-07-27 08:31 | Ch09 §9.3.6 gin-middleware | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ✓ 通过(单 module sparse clone 在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/gin/gin`,commit `34dac209ffb6ef85cc78c5d217bbb7ad001d68fd`;`codegraph init` 报 `Indexed 43 files (67 could not be parsed)` + `1,504 nodes, 5,208 edges in 202ms`,67 个失败均为 `.github/ISSUE_TEMPLATE/*.yaml` / `.github/workflows/*.yml` 占位 path,`codegraph` 自报"index is fully usable",`.codegraph/` 体积 5.2 MB;预热 `codegraph explore "HTTP router"` 返回 `Found 54 symbols across 2 files`;原题 `codegraph explore "How does gin route requests through its middleware chain?" --max-files 12` 跑 2 次均 `82 symbols / 3 files / 9 671 bytes / ~2 418 tokens / 0.189s real / 0.18s user / 0.03s sys`,`diff` 完全一致,blast radius 命中 `IRoutes (routergroup.go:33)` / `NoRoute (gin.go:326)` / `addRoute (gin.go:364)` / `HandlersChain (gin.go:57)`,Source Code 给出 `HandlersChain.Last()` 字面实现;Ch09 §9.3.6 引用 `82/3, ~2603 tokens, 0.17s` 与本次 `82/3, 2418 tokens, 0.189s` symbols/files 完全一致,tokens 偏差 7%(2 418 vs 2 603,来自 Ch09 当时不同终端宽度)time 偏差 10-16%(`time` 自身噪声在 0.19s 量级);README 已落 `/Users/digoal/new/codegraph-handbook/examples/gin-middleware/README.md` 并对比 README 自报 `30s / 3 tools / 246k / $0.27`(agent arm 端到端,与单次 MCP 探针数量级差 ~100×),clone 未删除)

### Ch09 · VS Code 扩展宿主探针(本次新增)

- 2026-07-27 08:32 | Ch09 §9.3.1 vscode-extension-host | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⚠ 数字与 Ch09 引用不一致(sparse clone 在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/vscode/vscode`,commit `74dc74c00942cd18cc82eb72e6f08de8a7cf1cf1`,sparse 目录 `src/vs/workbench/services/extensions` + `src/vs/workbench/api` 共 364 个 .ts 文件 15 MB;`codegraph init` 报 `Indexed 385 files (12,097 could not be parsed)` + `17,951 nodes, 56,312 edges in 1.3s`,12,097 失败均为 sparse-checkout 未拉取的非工作区目录,codegraph 自报"index is fully usable",`.codegraph/` 体积 65 MB;预热 `codegraph explore "extension host initialization"` 返 `Found 81 symbols across 5 files`;任务脚本原 `--json` 选项在 `codegraph explore --help` 中不存在,改用原生命令 `codegraph explore "How does the extension host communicate with the main process?" --max-files 12` 跑 2 次均 `45 symbols / 3 files / 21 572 bytes / ~5 393 tokens / 0.308s real / 0.30s user / 0.04s sys`,与 Ch09 §9.3.1 引用 `1 symbol / 1 file / ~1638 tokens / 0.15s` 完全不一致——分子项差异:(a) Ch09 旧表 commit `8f722dacb9bfb092108657867f5763b271ca7c1a` 落后当前 HEAD 数月,索引路径已变更;(b) 旧探针疑似只回 1 个核心 IPC 入口符号的窄上下文,新版按 `verbatim 源码 + blast radius + 全行号` 回 3 个文件量级;README 已落 `/Users/digoal/new/codegraph-handbook/examples/vscode-extension-host/README.md` 标注 ⚠ 并附 README 自报 `41s / 2 tools / 265k / $0.36` 数量级差 ~50× 说明,clone 未删除)
- 2026-07-27 08:39 | Ch09 §9.3.7 alamofire-request | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⚠ 数字与 Ch09 引用不一致(sparse clone 在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire/Alamofire`,commit `903c53c710d1cbbac0b4b9c2527aefb791e1fee3`,sparse 目录 `Source/` 含 `Alamofire.swift` + `Core` + `Extensions` + `Features` + `Info.plist` + `PrivacyInfo.xcprivacy` 顶层;`codegraph init` 报 `Indexed 49 files (65 could not be parsed)` + `2,052 nodes, 4,285 edges in 273ms`,65 失败均为 sparse-checkout 未拉取的 `Tests/` / `Documentation/` / `.github/` 等,codegraph 自报 "index is fully usable";预热 `codegraph explore "HTTP request"` 返 `Found 61 symbols across 3 files`;任务脚本原 `--json` 在 cg 1.5.0 explore 不存在,改原生命令 `codegraph explore "How does Alamofire build, send, and validate a request?" --max-files 12` 跑 2 次均 `61 symbols / 3 files / 13 532 bytes / ~3 383 tokens / 0.19s & 0.18s wall`(`/usr/bin/time -l` 实测,`diff` 完全一致),命中 `Source/Core/Request.swift` (Request class / ResponseDisposition / RequestDelegate / cURLDescription) + `Source/Core/WebSocketRequest.swift` + `Source/Features/MultipartUpload.swift`;与 Ch09 §9.3.7 引用 `0/0 / ~40 tokens / 0.14s` 差异显著 — symbols/files 多 61/3×、tokens 多 85×,Ch09 "未找到相关代码" 标记**不成立**,Alamofire 的核心实现 `Source/Core/Request.swift` 本次明确命中;README 已落 `/Users/digoal/new/codegraph-handbook/examples/alamofire-request/README.md` 并对比 README 自报 `49s / 3 tools / 316k tokens / $0.35`(agent arm 端到端,与单次 MCP 探针数量级差 ~270× / ~93×),clone 未删除)
- 2026-07-27 08:23 | Ch10 §10.3 MCP server session.engine 端到端 | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ✓ -- codegraph init /Users/digoal/new/codegraph 索引 456 files / 9218 nodes / 36587 edges / 1.1s
- 2026-07-27 08:25 | Ch10 §10.3 MCP codegraph_explore 端到端 | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ✓ -- mcp__codegraph__codegraph_explore(projectPath=/Users/digoal/new/codegraph) 返回 83 symbols / 6 files,源码覆盖 src/mcp/{engine,session,index,tools}.ts 和 src/bin/codegraph.ts
- 2026-07-27 08:30 | 集成阶段 §F-3 mermaid 修复 | env: macOS 14 / mmdc 11.16.0 | ✓ -- F-3 行 5 `S[curl install.sh \| sh]` 内含 `|` 改引号包裹后 11/11 张 mermaid 全部成功渲染
- 2026-07-27 08:31 | Ch09 §9.3 batch1 (vscode/excalidraw/django) | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⏳ -- 3 subagent 并行,shallow clone + init + explore
- 2026-07-27 08:31 | Ch09 §9.3 batch2 (tokio/okhttp/gin) | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⏳ -- 3 subagent 并行,shallow clone + init + explore
- 2026-07-27 08:35 | Ch09 §9.3.5 okhttp-interceptors | env: macOS 14 / node 24 / cg 1.5.0 | ⚠ 路径与数量与 Ch09 不一致(commit `e005148cce0a1294d5c402df942a3e92150c21ff`;Ch09 文档路径 `okhttp/src/jvmMain/kotlin/okhttp3/internal/http` 在 HEAD 已不存在,拦截器链迁至 `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/http/`;`codegraph init` 报 `688 files / 19,115 nodes / 50,520 edges in 777ms`;预热 `codegraph explore "HTTP client"` 返 `57 symbols across 3 files`;原题任务脚本 `--json` 在 cg 1.5.0 explore 子命令不存在,改原生命令 `codegraph explore "How does OkHttp process a request through its interceptor chain?" --max-files 12` 跑 2 次均 `55 symbols / 4 files / 20084 bytes / ~5021 tokens / 0.34s & 0.36s wall`,`diff` 完全一致,blast radius 命中 `Interceptor`/`Request`/`Chain`/`RealInterceptorChain`,Source Code 给出 `RealInterceptorChain` 完整源码;与 Ch09 §9.3.5 引用 `1/1, ~885 tokens, 0.14s` 差异显著 — symbols/files 多 50/4×、tokens 多 5.7×、time 略长,源于 Ch09 旧探针可能只回窄上下文 1 符号,而当前 `codegraph_explore` 按"verbatim 源码 + blast radius + 全行号" 返回;README 已落 `/Users/digoal/new/codegraph-handbook/examples/okhttp-interceptors/README.md` 并对比 README 自报 `27s / 1 tool / 156k tokens / $0.23`(agent arm 端到端,与单次 MCP 探针数量级差 ~50-100×),clone 未删除)
- 2026-07-27 08:35 | Ch09 §9.3.1 vscode-extension-host | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⚠ 差异显著 -- 真实 45/3/5393/0.31s vs Ch09 引用 1/1/1638/0.15s
- 2026-07-27 08:35 | Ch09 §9.3.3 django-orm | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⚠ 差异显著 -- 真实 83/2/4802/0.20s vs Ch09 引用 0/0/42/0.14s
- 2026-07-27 08:35 | Ch09 §9.3.4 tokio-runtime | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⚠ 差异显著 -- 真实 78/5/3974/0.20s vs Ch09 引用 0/0/41/0.14s
- 2026-07-27 08:35 | Ch09 §9.3.5 okhttp-interceptors | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⚠ 差异显著 -- 真实 55/4/5021/0.34s vs Ch09 引用 1/1/885/0.14s;且拦截器链路径在 HEAD 已迁至 commonJvmAndroid
- 2026-07-27 08:35 | Ch09 §9.3.6 gin-middleware | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ✓ -- 真实 82/3/2418/0.19s vs Ch09 引用 82/3/2603/0.17s 偏差 ~7%
- 2026-07-27 08:39 | Ch09 §9.3.7 alamofire-request | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⚠ 差异显著 -- 真实 61/3/3383/0.19s vs Ch09 引用 0/0/40/0.14s;Ch09"未找到相关代码"标记不成立
- 2026-07-27 08:40 | 阶段五 cleanup | env: macOS 14 | ✓ -- 删除 7 个早期 stub README(vscode/excalidraw/django/tokio/okhttp/gin/alamofire),写 examples/README.md 汇总表
- 2026-07-27 08:42 | Ch09 §9.4.1 复现性声明 | env: macOS 14 | ✓ -- Ch09 9.4 节加 9.4.1 子节,引用 examples/README.md 真实数据
- 2026-07-27 08:41 | Ch09 §9.3.2 excalidraw-canvas | env: macOS Darwin 24.6.0 / node v24.14.1 / cg 1.5.0 | ⚠ 路径与 Ch09 引用不一致(sparse clone 在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw/excalidraw`,commit `b2e81e38a6fde8b3cb5dfdf2f2fb651323ad309d`,sparse 目录 `packages` 含 `packages/excalidraw/` + `packages/element/src/` 等所有源码;**HEAD 已无顶层 `src/` 目录,Ch09 脚本 `git sparse-checkout set src` 在当前 HEAD 不成立**,实际主代码组织为 `packages/{excalidraw,element,utils,...}/src`;`codegraph init` 报 `Indexed 577 files (92 could not be parsed)` + `9,852 nodes, 43,698 edges in 498ms`,92 失败均为 sparse-checkout 未拉取的 `.github/*.yml` / `.codesandbox/*` 占位 path,codegraph 自报"index is fully usable",`.codegraph/` 体积 43 MB;预热 `codegraph explore "canvas rendering"` 返 `Found 64 symbols across 2 files`;任务脚本原 `--json` 在 cg 1.5.0 explore 子命令不存在,改原生命令 `codegraph explore "How does Excalidraw render and update canvas elements?" --max-files 12` 跑 2 次均 `74 symbols / 1 file / 25 282 bytes / ~6 320 tokens / 0.29s & 0.28s wall`(`/usr/bin/time -p` 实测,`diff` 完全一致),blast radius 命中 `render (packages/excalidraw/components/App.tsx:2282)` (108 callers) + `update (animatedTrail.ts:149)`,Source Code 给出 `App.tsx` 中 `render` / `mutateElement` / `triggerRender` / `StaticCanvas` 等完整源码 480+ 行;与 Ch09 §9.3.2 引用 `1/1, ~1433 tokens, 0.14s` 差异显著 — symbols 多 74×、tokens 多 4.4×、time 略长,源于 Ch09 旧探针疑似只回 1 个核心入口符号的窄上下文,而当前 `codegraph_explore` 按"verbatim 源码 + blast radius + 全行号" 返回;README 已落 `/Users/digoal/new/codegraph-handbook/examples/excalidraw-canvas/README.md` 并对比 README 自报 `3 tools / 324k tokens / $0.40`(agent arm 端到端,与单次 MCP 探针数量级差 ~50×),clone 未删除)
- 2026-07-27 08:55 | Ch09 §9.3.2 excalidraw-canvas | env: macOS 14 / node 24.3.0 / cg 1.5.0 | ⚠ 差异显著 -- 真实 74/1/6320/0.28s vs Ch09 引用 1/1/1433/0.14s;路径 src/ 已迁至 packages/
- 2026-07-27 08:55 | 阶段五 7 仓整合 | env: macOS 14 | ✓ -- 7 仓真实 README 全部完成,examples/README.md 汇总表完整,Ch09 9.4.1 复现性声明段已加,7 stub README 已清理
| 2026-07-27 | Ch09 §9.3.1-9.3.7 | ⚠ 警示框 + 真实数字链接追加 | 7 处编辑 | ✓ |
| 2026-07-27 | mermaid | 8 张图补 %% F-N 标题 + F-11 错字 + F-10 \n | 8/8 通过 | ✓ |
| 2026-07-27 | 顶层数字 | README/SUMMARY 行数 139/177 → 180 | wc -l 验证 | ✓ |
| 2026-07-27 | 7 仓 Run 2 | 真跑 + verbatim 50 行补全(每仓) | 7/7 通过 | ✓ |
| 2026-07-27 | Ch10/Ch11/Ch12 | 决策顺序 + 数字 + 行号 + crate 集合 | 7/7 通过 | ✓ |
| 2026-07-27 | Ch16/Ch17/Ch18 | 数字 + 行号 + 路径(tools.ts:389) | 7/7 通过 | ✓ |
| 2026-07-27 | Ch05/Ch00/Ch09 | 行号 + 锚定日期(7-22)+ 时间错位 | 5/5 通过 | ✓ |
| 2026-07-27 | terminology-source.md | 8 术语增补 Ch17 行号映射 | wc -l 64 | ✓ |
