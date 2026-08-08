# 第 4 章 · 配置全解(env / 忽略规则 / 遥测)

> **面向读者**:用户 · **预计阅读**:20 分钟
> **前置依赖**:{{chapter:3}}
> **本章目标**:列出所有可调旋钮,理解 `.codegraph/` 目录含义、env vs config file 取舍、遥测与守护进程开关

## 4.1 引言

你可能已经跑了 `codegraph init`、在 IDE 里装了 MCP 服务器,现在想"动点手脚":某个仓库忘了初始化就让 daemon 起来了;WSL2 上 `/mnt/c` 路径下文件监听卡死;团队里想把 `.tsx` 文件也用 TS 解析器吃下;或者单纯想关掉遥测。本章把所有可调旋钮摊开讲。

CodeGraph 把配置分成三类,适用边界清晰:

| 类别 | 谁来管 | 谁生效 | 何时用 |
|------|--------|--------|--------|
| **环境变量 `CODEGRAPH_*`** | 当前进程 shell / `.envrc` / CI 配置 | 单次进程(`process.env` 即时读取) | 一次性、机器级、CI 注入 |
| **`codegraph.json`(项目根)** | 团队 / 仓库 | 该目录下所有进程 | 想随 git 一起版本化 |
| **`.codegraph/` 目录** | 单台机器 | 这台机器的这个项目 | 索引、缓存、daemon 锁 |

理解边界后,你会知道"WSL2 共享索引"该改 env,而不是改 JSON;"团队统一把 `.jsx` 当 TSX"该改 JSON,而不是改 env。

## 4.2 概念铺垫

### 4.2.1 `.codegraph/` 目录布局

`codegraph init` 在项目根建一个 `.codegraph/`(`src/directory.ts:644-660`),里面只有四样东西会显式落地:

| 路径 | 作用 | 能不能入 git |
|------|------|--------------|
| `.codegraph/codegraph.db` | SQLite 主库,所有节点/边/FTS5/索引都住在这里 | 否 |
| `.codegraph/.gitignore` | 自带 `*\n!.gitignore`,把整目录挡在 git 外(见 `directory.ts:593-598`) | 是(本身) |
| `.codegraph/daemon.pid` / `daemon.sock` | 后台守护进程的 PID + Unix 命名管道 | 否 |
| `.codegraph/cache/`、`*.log`、未来文件 | 缓存与诊断日志 | 否 |

`.gitignore` 是新版自动生成的——一段通配 `*` 加 `!.gitignore` 自身,覆盖了所有未来会冒出来的瞬态文件,旧版允许列表(没把 `daemon.pid` 列进去,#788)被自动识别并原地升级,你什么都不用动(`directory.ts:601-616`)。所以**不要**自己往 `.codegraph/.gitignore` 加 `*.db` 之类——版本管理器会用通配回退覆盖你的自定义规则。规则一旦丢失,索引就会跟着入库,仓库体积会爆炸。

### 4.2.2 `.codegraph-*` 同胞目录

`isCodeGraphDataDir()`(`directory.ts:74-80`)承认三类目录都是 CodeGraph 的索引:

- `.codegraph`(默认)
- `.codegraph-*`(任何 `.codegraph-` 前缀)
- 当前 `CODEGRAPH_DIR` 覆盖值

这第三条是给"同一棵树被两个环境共享"准备的(经典是 Windows 原生 + WSL 共享同一工作树,#636):daemon 锁文件记的是平台相关的 PID 与 socket(SQLite 在 WSL2 ↔ Windows 文件系统边界上的文件锁不可靠),所以两个 daemon 共用一份索引会损坏。两边各设 `CODEGRAPH_DIR=.codegraph-win` / `CODEGRAPH_DIR=.codegraph-wsl`,各自的索引、socket、锁互不干扰。

### 4.2.3 哪些目录不能当索引根

`unsafeIndexRootReason()`(`directory.ts:126-156`)会在 `init` 与 `index` 命令里硬拒三种"看似目录,其实是黑洞"的根:

- 文件系统根:`/`、`C:\`
- 用户 home:`$HOME`
- home 的祖先:`/Users`、`/home`

理由索引 home 会拽进 `Library`、`.cache`、其它项目——多 GB 索引 + 监听风暴 + macOS 上 fd 撑爆整台机器(#845)。如果确实需要(测试容器 / CI 跑 fixture),加 `--force` 绕过。

### 4.2.4 env vs config file 取舍

一个粗略决策树:

- **机器级**、**CI 级**、**临时性** → env。例:`CODEGRAPH_NO_DAEMON=1`、`CODEGRAPH_TELEMETRY=0`。
- **项目级**、**团队共享**、**随仓库走** → `codegraph.json`。例:`extensions`、`.jsx` 当 TSX。
- **单次会话且需要审计**(例如"今天我先关掉遥测再跑 init")→ `codegraph telemetry off`,会写到 `~/.codegraph/telemetry.json`,永久生效。

## 4.3 正文

### 4.3.1 `.codegraph/` 目录解剖

参见 4.2.1。补充两点:

1. `isInitialized()`(`directory.ts:93-101`)要求 `.codegraph/` 与 `codegraph.db` 都存在——光建空目录不算"已初始化",也不会触发 MCP 服务器接管。
2. `validateDirectory()`(`directory.ts:781-813`)每次启动都会自检 `.gitignore` 的存在与时效,缺则重建、过时则就地升级——所以**无需**手工维护这个文件。

### 4.3.2 `CODEGRAPH_*` 环境变量大全

下表覆盖源代码中已识别到的全部 `CODEGRAPH_*` 环境变量。按"用户可调 vs 内部"分组。**默认值**列为"未设置"或"1/0 触发"会在表中注明。

#### 4.3.2.1 用户级旋钮(可直接调到)

| 变量 | 默认 | 用途 | 出处 |
|------|------|------|------|
| `CODEGRAPH_DIR` | `.codegraph` | 改索引目录名,必须是不含分隔符的段名(WSL/Windows 共享树场景) | `src/directory.ts:36-56` |
| `CODEGRAPH_TELEMETRY` | (由 `~/.codegraph/telemetry.json` 与 `DO_NOT_TRACK` 决定) | `=0` 关、`=1` 开,直接覆盖配置文件 | `src/telemetry/index.ts` + `TELEMETRY.md` |
| `CODEGRAPH_NO_UPDATE_CHECK` | 未设 | 关掉后台 GitHub release 探针 | `src/upgrade/update-check.ts:89-91` |
| `DO_NOT_TRACK` | 未设 | 跨工具的"别打给我的家"约定,同时关遥测和更新检查 | `TELEMETRY.md`、`update-check.ts:89-91` |
| `CODEGRAPH_NO_DAEMON` | 未设 | `=1` 直接跑,不拉后台 daemon(WSL2、断网环境常用) | `src/mcp/index.ts:95-99` |
| `CODEGRAPH_NO_WATCH` | 未设 | 关闭文件监听,关掉自动 sync(慢盘、CI) | `src/bin/codegraph.ts:1738` |
| `CODEGRAPH_WATCH_DEBOUNCE_MS` | 引擎默认 | 文件监听合并去抖,clamp 在 [100ms, 60s](`src/mcp/engine.ts:249`) | `src/mcp/engine.ts:249` |
| `CODEGRAPH_VERSION` | 包内 `package.json` | 启动时强制锁版本(企业灰度用) | `src/bin/codegraph.ts:2428` |
| `CODEGRAPH_PROMPT_HOOK` | `1` | `=0` 关掉 Claude Code prompt hook 前置 | `src/bin/codegraph.ts:1226` |
| `CODEGRAPH_NO_PROMPT_HOOK` | 未设 | 同上,`=1` 触发,优先级等同 `=0` | 同上 |
| `CODEGRAPH_DEBUG` | 未设 | 打开内部调试日志(stderr) | `src/errors.ts:181` |
| `CODEGRAPH_ASCII` / `CODEGRAPH_UNICODE` | 自动 | 强制 TUI 用 ASCII 或 Unicode 字符 | `src/ui/glyphs.ts:34-37` |
| `CODEGRAPH_MCP_DEBUG` | 未设 | MCP 协议帧写到 stderr | `src/mcp/transport.ts:196` |
| `CODEGRAPH_MCP_TOOLS` | (全开) | 逗号分隔,只暴露指定 MCP 工具给客户端 | `src/mcp/tools.ts:785` |
| `CODEGRAPH_NO_FAST_INIT` | 未设 | `=1` 走完整初始化(诊断 / 测时用) | `src/index.ts:459` |
| `CODEGRAPH_NO_WAL_DEFER` | 未设 | `=1` 禁用 WAL checkpoint 延迟 | `src/index.ts:466` |
| `CODEGRAPH_WAL_VALVE_MB` | (自适应) | WAL 容量阈值,按当前库大小算 | `src/index.ts:477` |
| `CODEGRAPH_SYNTH_TIMINGS` | 未设 | 把每个解析/解决阶段耗时打到 stderr | `src/index.ts:519` 等 |
| `CODEGRAPH_ADAPTIVE_EXPLORE` | `1` | `=0` / `=false` 关掉自适应 explore 行为 | `src/mcp/tools.ts:320` |
| `CODEGRAPH_EXPLORE_LINENUMS` | `1` | `=0` 不返回行号 | `src/mcp/tools.ts:304` |
| `CODEGRAPH_CATCHUP_GATE_TIMEOUT_MS` | 引擎默认 | explore 与 sync 的同步闸门超时 | `src/mcp/tools.ts:337` |
| `CODEGRAPH_NO_INSTALL_REFRESH` | 未设 | `=1` 跳过自升级时刷新安装 | `src/upgrade/index.ts:510` |
| `CODEGRAPH_ALLOW_UNSAFE_NODE` | 未设 | 跳过 PATH 校验,直接用当前 node | `src/bin/codegraph.ts:93/103` |
| `CODEGRAPH_NO_RELAUNCH` | 未设 | `=1` 禁用二进制自我替换 | `src/upgrade/index.ts` |

#### 4.3.2.2 内部旋钮(给维护者与测试用)

| 变量 | 含义 |
|------|------|
| `CODEGRAPH_DAEMON_INTERNAL` | 守护进程自识别,"我是 daemon 本体" 标志(`src/mcp/index.ts:102`) |
| `CODEGRAPH_WASM_RELAUNCHED` | 标记进程是否已经被 wasm 重启过,防止递归 |
| `CODEGRAPH_HOST_PPID` / `CODEGRAPH_PPID_POLL_MS` | 父进程监视(`src/mcp/proxy.ts:183`、`bin/command-supervision.ts:65-66`) |
| `CODEGRAPH_STARTUP_HANDSHAKE_TIMEOUT_MS` | MCP 启动握手超时 |
| `CODEGRAPH_DAEMON_IDLE_TIMEOUT_MS` / `_MAX_IDLE_MS` / `_CLIENT_SWEEP_MS` | daemon 空闲/客户端清扫节奏(`src/mcp/daemon.ts:730-746`) |
| `CODEGRAPH_QUERY_POOL_SIZE` / `_BUSY_TIMEOUT_MS` | resolver worker 池大小与忙等超时 |
| `CODEGRAPH_QUERY_WORKER_ALLOW_TEST_CRASH` | 测试钩子,允许 `__test_crash__` 假死 |
| `CODEGRAPH_WATCHDOG_TIMEOUT_MS` / `CODEGRAPH_NO_WATCHDOG` | PPID watchdog 调优 |
| `CODEGRAPH_RESOLVER_CACHE_SIZE` / `_RESOLVE_WORKERS` / `_RESOLVE_PROFILE` / `_PARALLEL_RESOLVE_MIN` / `_NO_PARALLEL_RESOLVE` | 解析器调优与剖析 |
| `CODEGRAPH_AMBIGUOUS_NAME_CEILING` | 名称匹配阈值 |
| `CODEGRAPH_RANK_NO_MULTITERM` | 搜索多词排序开关 |
| `CODEGRAPH_KERNEL` / `_KERNEL_CFNPTR` / `_KERNEL_DEBUG` / `_KERNEL_PATH` / `_KERNEL_LANGS` | 内核(NAPI)层开关 |
| `CODEGRAPH_PARSE_TIMEOUT_MS` / `_PARSE_WORKERS` | 解析超时与并行度 |
| `CODEGRAPH_BIN_DIR` / `_INSTALL_DIR` | 安装路径覆盖 |
| `CODEGRAPH_FORCE_WATCH` / `_MAX_DIR_WATCHES` | watcher 强制开启 / 最大目录监听数 |
| `CODEGRAPH_NO_STORE_WORKER` | 关 store worker 复用 |
| `CODEGRAPH_WAL_VALVE_DEBUG` | WAL 阀门调试日志 |
| `CODEGRAPH_MCP_LOG_ATTACH` | `=1` 把代理日志挂到 daemon(`src/mcp/proxy.ts:53`) |
| `CODEGRAPH_INSTRUCTIONS_BLOCK` / `_SECTION_START` / `_SECTION_END` / `_START` / `_END` | 输出切片(测试用) |
| `CODEGRAPH_VALUE_REFS` | 调试值引用 |

注:以上均不保证稳定 API,会在小版本里改语义或改名——你的 `.envrc` 应该只 pin 4.3.2.1 表里的旋钮。

### 4.3.3 `codegraph.json` 团队共享配置

放在**项目根**——和 `.codegraph/` 一起被 Git 管理。`loadParsedConfig()`(`src/project-config.ts:272-290`)读 + 解析 + mtime 缓存,所以一次索引只读一次盘。

完整 schema(`project-config.ts:34-70`):

```json
{
  "extensions":     { ".dota_lua": "lua", ".jsx": "tsx" },
  "includeIgnored": ["legacy-modules/"],
  "exclude":        ["static/vendor/**"],
  "include":        ["Tools/**"]
}
```

四个字段,逐个解释:

- **`extensions`**:文件扩展名 → 语言 id 的覆盖。值必须是已支持的语言(`isLanguageSupported()`),否则 warn-and-skip。键会自动 lowercase 加 `.`,所以 `jsx` 和 `.JSX` 等价。**用户映射在 built-in 之上、冲突时胜出**——所以也可以"重新指向"已支持扩展(`.h` → `cpp`)。
- **`includeIgnored`**:从 gitignored 的目录里**复活**被嵌入的 git 仓库(#622、#699)。例:父仓 `.gitignore` 排除了 `legacy-modules/`,但 `legacy-modules/foo/.git` 里其实是个独立项目,你想让它入索引。
- **`exclude`**:**把已入 git 的路径**踢出索引(#999)。`.gitignore` 只能挡未跟踪文件,所以"已 commit 的 vendor 主题包"只能在这里挡。
- **`include`**:把被 `.gitignore` 挡掉的**自有源码**强行拉回(SVN/Perforce 单 VCS 仓库常用)。内置默认忽略的 `node_modules`、`.git`、`.codegraph*` 永远不会被这个白名单复活,但 `exclude` 永远胜出。

任一字段缺失、JSON 损坏、值非法——降级为零配置默认值,**不会**让索引失败。错误以 `logWarn` 形式写到 stderr。

### 4.3.4 忽略规则

三层叠加,先后顺序是"内置默认 → `.gitignore` → `codegraph.json`":

1. **内置默认**:`SUBPROJECT_SCAN_SKIP`(`directory.ts:180-184`)——`node_modules`、`.git`、`.svn`、`.hg`、`dist`、`build`、`out`、`target`、`vendor`、`bin`、`obj`、`.next`、`.nuxt`、`.svelte-kit`、`.cache`、`coverage`、`.venv`、`venv`、`__pycache__`、`.turbo`、`.idea`、`.vscode`、`tmp`、`temp`。这层**永远**生效,`include` 也救不回来。
2. **`.gitignore`**:Git 标准语义。gitignored 的**目录**里的内嵌 git 仓库默认不索引(#970、#976)。
3. **`codegraph.json` 覆盖**:`includeIgnored`、`exclude`、`include`。

如果想"全局放过 .gitignore":目前的设计是`includeIgnored` 只覆盖**内嵌 git 仓库**——它不是"通配白名单"。要彻底复活某条 `.gitignore` 路径,要么改 `.gitignore` 本身,要么用 `include`(注意上面三层顺序)。

### 4.3.5 遥测

完整定义见 `TELEMETRY.md`,实现见 `src/telemetry/index.ts`。四个开关优先级(**从高到低**):

1. `DO_NOT_TRACK=1` → 永远关
2. `CODEGRAPH_TELEMETRY=0|1` → 临时覆盖
3. `~/.codegraph/telemetry.json` 里的 `enabled` 字段(`codegraph telemetry on/off` 写的就是它)
4. 默认 `enabled=true`(installer 第一次启动时弹出 toggle,没人见过 installer 就 `default-notice` 默认开)

`codegraph telemetry status` 显示当前状态、是什么决定的、你的 machine_id(`src/telemetry/index.ts:getStatus()`)。**关就是关**——关掉后不发任何包、不开 socket、不发"已退订" 心跳,缓冲里没发的数据会被删除。

数据形态(摘要,详见 `TELEMETRY.md`):

- 事件:`install` / `index` / `usage_rollup` / `uninstall`
- 不收:源码、文件路径、IP、机器指纹之外的任何东西
- endpoint:`https://telemetry.getcodegraph.com/v1/events`(公开可审计的 Cloudflare Worker,服务端有 allowlist,IP 丢弃)
- 缓冲:256KB 本地 JSONL,失败静默、绝不重试、绝不延迟 MCP 工具调用

### 4.3.6 更新检查

与遥测**独立**但共用同一组开关。

- `DO_NOT_TRACK=1` → 关
- `CODEGRAPH_NO_UPDATE_CHECK=1` → 关(只关这个,不关遥测)
- 默认开,at most once / day(`UPDATE_CHECK_TTL_MS = 24h`,`UPDATE_CHECK_FAILURE_BACKOFF_MS = 1h`)
- 实现:`src/upgrade/update-check.ts`,fire-and-forget 网络请求,缓存到 `~/.codegraph/update-check.json`,失败静默
- 触发面:MCP initialize、stderr 一行、`codegraph_status` 输出

### 4.3.7 Daemon / Watcher 调优

Daemon 的三种运行模式(`src/mcp/index.ts:90-110`):

| 模式 | 怎么进 | 适用 |
|------|--------|------|
| **Daemon**(默认) | launcher spawn 一个 detached daemon,后续启动复用 socket | 桌面、长会话 |
| **Direct** | `CODEGRAPH_NO_DAEMON=1`,单进程内嵌跑 | WSL2 / 断网 / CI |
| **Internal** | `CODEGRAPH_DAEMON_INTERNAL=1`,被 launcher 设上 | "我是 daemon 本体" 自识别 |

WSL2 + Windows 文件系统的 `/mnt/c` 项目,常需要 `CODEGRAPH_NO_DAEMON=1 CODEGRAPH_NO_WATCH=1` 组合——监听层既慢又会反复触发同步。

Watcher 去抖:

```bash
CODEGRAPH_WATCH_DEBOUNCE_MS=2000   # 1~2s 适合格式化保存链多的工程
CODEGRAPH_WATCH_DEBOUNCE_MS=10000  # 大仓 + 大量生成文件
```

范围外(<100ms 或 >60s)或非数字都会回落到引擎默认值(`src/mcp/engine.ts:249`)。

## 4.4 真实场景实战

### 场景 4.1:关闭遥测 + 关 daemon(WSL2 模式)

```bash
# 永久 + 跨 shell 关遥测
codegraph telemetry off

# 单次会话:不进 daemon、不监听
export CODEGRAPH_NO_DAEMON=1
export CODEGRAPH_NO_WATCH=1
codegraph init && codegraph mcp
```

注意关遥测后**不会**关更新检查。要彻底静默:

```bash
export DO_NOT_TRACK=1          # 一次关两个
# 或
export CODEGRAPH_NO_UPDATE_CHECK=1
```

### 场景 4.2:在 monorepo 里加 `codegraph.json` 让子仓被索引

仓库根 `codegraph.json`:

```json
{
  "includeIgnored": ["legacy-modules/"]
}
```

父仓 `.gitignore` 把 `legacy-modules/` 排除掉了——但里面每个子目录都是独立 git 仓库、你想让它们入索引。运行 `codegraph init`,CodeGraph 会沿 `legacy-modules/foo/.git` 自动发现并索引子仓。

### 场景 4.3:调 watcher debounce 适配大仓库

```bash
export CODEGRAPH_WATCH_DEBOUNCE_MS=8000   # 8s
codegraph mcp
```

启动日志会写一行:`[CodeGraph MCP] File watcher debounce: 8000ms (CODEGRAPH_WATCH_DEBOUNCE_MS)`,便于确认生效。

## 4.5 本章小结

- `.codegraph/` 是**单台机器**的索引,永远别 commit;`.gitignore` 由 CodeGraph 自维护,别手改。
- `codegraph.json` 在**项目根**,随 git 走,只承担团队级别的扩展名与 ignore 覆盖。
- `CODEGRAPH_*` env 是**单次进程**生效,适合机器级、CI 级旋钮。
- 遥测、更新检查、daemon、watcher——每条都有"用户级"开关,默认开,关掉后行为有明确定义。

## 4.6 常见踩坑

- **误以为 `codegraph telemetry off` 也关更新检查**——不会,要用 `CODEGRAPH_NO_UPDATE_CHECK=1` 或 `DO_NOT_TRACK=1`。
- **手动往 `.codegraph/.gitignore` 加规则**——会被自动重写。新版只接受"通配 `*` + `!.gitignore`" 一种模式。
- **`CODEGRAPH_DIR=../something`**——路径分隔符、`..`、绝对路径一律被忽略并 warn(`src/directory.ts:36-56`),不要用它来"把索引挪到外面"。
- **在 WSL2 跑 `init`** 时给的是 `/mnt/c/...`——监听可能完全卡死,加 `CODEGRAPH_NO_WATCH=1`。
- **`includeIgnored` 当作"全部 gitignore 白名单"用**——它只复活内嵌 git 仓库。普通被忽略的源码用 `include`。
- **改 `codegraph.json` 不重启**——mtime 缓存让下次索引自动重读(`project-config.ts:284-286`),无需手动重启。
- **试图把 home 当索引根**——被 `unsafeIndexRootReason()` 硬拒,加 `--force` 之前先确认你愿意听 `#845` 故事。

## 4.7 下一章预告

{{chapter:5}}

## 4.8 参考

- `src/directory.ts` —— 目录布局、`codeGraphDirName`(`:35-56`)、`isCodeGraphDataDir`(`:74-80`)、`unsafeIndexRootReason`(`:126-156`)、`createDirectory`(`:644-660`)、`.gitignore` 自维护(`:593-638`)
- `src/project-config.ts` —— `codegraph.json` schema 与解析、四个字段语义(`:34-70`、`:300-339`)
- `src/telemetry/index.ts` —— 遥测客户端、precedence 顺序、`getStatus`
- `src/upgrade/update-check.ts` —— 更新检查、`updateCheckDisabled`(`:89-91`)
- `src/mcp/{index,engine,daemon}.ts` —— `CODEGRAPH_NO_DAEMON`、`CODEGRAPH_WATCH_DEBOUNCE_MS`、daemon 空闲超时
- `src/bin/codegraph.ts` —— `CODEGRAPH_NO_WATCH` 路由(`:1738`)、prompt hook 开关(`:1226`)、`CODEGRAPH_VERSION`(`:2428`)
- `src/ui/glyphs.ts`、`src/ui/color.ts` —— 渲染相关的 `CODEGRAPH_ASCII` / `CODEGRAPH_UNICODE` / `NO_COLOR` / `FORCE_COLOR`
- `TELEMETRY.md`(项目根)—— 遥测完整定义、采集字段白名单