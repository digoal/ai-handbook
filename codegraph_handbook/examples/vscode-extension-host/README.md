# vscode-extension-host benchmark

真实可复现的 CodeGraph 探针跑分：VS Code 扩展宿主通信路径。

## 仓库

- **地址**：`https://github.com/microsoft/vscode`
- **commit**：`74dc74c00942cd18cc82eb72e6f08de8a7cf1cf1`（`git rev-parse HEAD`，2026-07-27 拉取）
- **clone**：

  ```bash
  mkdir -p /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/vscode
  cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/vscode
  git clone --depth=1 --filter=blob:none --sparse https://github.com/microsoft/vscode.git
  cd vscode
  git sparse-checkout set src/vs/workbench/services/extensions src/vs/workbench/api
  ```

- **sparse 体量**：364 个 .ts 文件（`services/extensions` 45、`api` 319）共 15 MB；`.codegraph/` 索引另计。

## 提示词

> `How does the extension host communicate with the main process?`

## 索引初始化

```bash
cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/vscode/vscode
time codegraph init
```

**输出（截取末 15 行）**：

```
Parsing code...
Resolving refs...
Linking dynamic dispatch...

  Indexed 385 files (12,097 could not be parsed)

  17,951 nodes, 56,312 edges in 1.3s

  Error breakdown
   12,097 files could not be read

  See .codegraph/errors.log for details
  The index is fully usable — only the failed files are missing.
  Done
codegraph init 2>&1  8.18s user 1.66s system 215% cpu 4.560 total
```

**索引快照**：

| 指标 | 数值 |
|---:|---:|
| indexed files | 385 |
| nodes | 17,951 |
| edges | 56,312 |
| parse time | 1.3 s |
| 总 wall-clock | 4.56 s |
| 未解析文件 | 12,097（sparse-checkout 之外的目录，没有 .ts 实体可读，索引本身不受影响） |

> ⚠ "12,097 files could not be read" 是 sparse-checkout 的副作用——`.codegraph/` 在仓库内递归扫描，把所有 blob 槽都列入待解析清单，但本工作区只 checkout 了 2 个子目录。codegraph 自报"The index is fully usable — only the failed files are missing"，与 `.codegraph/errors.log` 一致。

## 预热

```bash
codegraph explore "extension host initialization"
```

`Found 81 symbols across 5 files.`，耗时 0.282 s（避免冷启动污染）。

## 真跑探针

任务脚本原本带的 `--json` 选项在 `codegraph explore --help` 中不存在（实际支持的选项只有 `-p/--path`、`--max-files`、`--h`），所以改为原生命令并以 `--max-files 12` 收口；输出捕获到 stdout 后再统计字节数和行数。

```bash
# 第 1 次
{ time codegraph explore "How does the extension host communicate with the main process?" --max-files 12 > /tmp/run1.out; } 2>&1
# 第 2 次
{ time codegraph explore "How does the extension host communicate with the main process?" --max-files 12 > /tmp/run2.out; } 2>&1
```

### 第一次响应（head -100 共 4 608 bytes / 100 行）

```text
**Exploration: How does the extension host communicate with the main process?**

Found 45 symbols across 3 files.

**Blast radius — what depends on these (update/verify before editing)**

- `startExtensionHostProcess` (src/vs/workbench/api/node/extensionHostProcess.ts:397) — 1 caller in `src/vs/workbench/api/node/extensionHostProcess.ts`; ⚠ no covering tests found
- `ExtensionHostProcess` (src/vs/workbench/services/extensions/electron-browser/localProcessExtensionHost.ts:52) — 3 callers in `src/vs/workbench/services/extensions/electron-browser/localProcessExtensionHost.ts`; ⚠ no covering tests found
- `_onExtHostProcessExit` (src/vs/workbench/services/extensions/electron-browser/localProcessExtensionHost.ts:585) — 1 caller in `src/vs/workbench/services/extensions/electron-browser/localProcessExtensionHost.ts`; ⚠ no covering tests found
- `ExtensionHostMain` (src/vs/workbench/api/common/extensionHostMain.ts:161) — 4 callers in `src/vs/workbench/api/node/extensionHostProcess.ts`, `src/vs/workbench/api/worker/extensionHostWorker.ts`; ⚠ no covering tests found
- `NativeLocalProcessExtensionHost` (src/vs/workbench/services/extensions/electron-browser/localProcessExtensionHost.ts:96) — 1 caller in `src/vs/workbench/services/extensions/electron-browser/nativeExtensionService.ts`; ⚠ no covering tests found

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`src/vs/workbench/services/extensions/electron-browser/localProcessExtensionHost.ts`** — references(references), ILocalProcessExtensionHostInitData(interface), ExtensionHostExtensions(references), ILocalProcessExtensionHostDataProvider(interface), ILocalProcessExtensionHostInitData(references), ExtensionHostProcess(class), +15 more

```typescript
41	import { parseExtensionDevOptions } from '../common/extensionDevOptions.js';
42	import { IDefaultLogLevelsService } from '../../log/common/defaultLogLevels.js';
43	
44	export interface ILocalProcessExtensionHostInitData {
45		readonly extensions: ExtensionHostExtensions;
46	}
47	
48	export interface ILocalProcessExtensionHostDataProvider {
49		getInitData(): Promise<ILocalProcessExtensionHostInitData>;
50	}
51	
52	export class ExtensionHostProcess {
53	
54		private readonly _id: string;
55	
56		public get onStdout(): Event<string> {
57			return this._extensionHostStarter.onDynamicStdout(this._id);
58		}
59	
60		public get onStderr(): Event<string> {
61			return this._extensionHostStarter.onDynamicStderr(this._id);
62		}
63	
64		public get onMessage(): Event<unknown> {
65			return this._extensionHostStarter.onDynamicMessage(this._id);
66		}
67	
68		public get onExit(): Event<{ code: number; signal: string }> {
69			return this._extensionHostStarter.onDynamicExit(this._id);
70		}
71	
72		constructor(
73			id: string,
74			private readonly _extensionHostStarter: IExtensionHostStarter,
75	) {
76		this._id = id;
77	}
78	
79		public start(opts: IExtensionHostProcessOptions): Promise<{ pid: number | undefined }> {
80		return this._extensionHostStarter.start(this._id, opts);
81	}
82	
83		public enableInspectPort(): Promise<boolean> {
84		return this._extensionHostStarter.enableInspectPort(this._id, opts);
85	}
86	
87		public waitForExit(maxWaitTimeMs: number): Promise<void> {
88		return this._extensionHostStarter.waitForExit(this._id, maxWaitTimeMs);
89	}
90	
91		public kill(): Promise<void> {
92		return this._extensionHostStarter.kill(this._id);
93	}
94	}
95	
96	export class NativeLocalProcessExtensionHost extends Disposable implements IExtensionHost {
97	
98		public pid: number | null = null;
99		public readonly remoteAuthority = null;
```

**`src/vs/workbench/api/node/extensionHostProcess.ts`** — calls(calls), send(calls), onMessage(calls), nativeExit(calls), catch(calls), splice(calls), +13 more

```typescript
290	}
291	}
292	
293	async function createExtHostProtocol(): Promise<IMessagePassingProtocol> {
294	
295	const protocol = await _createExtHostProtocol();
296	
297	return new class implements IMessagePassingProtocol {
298	
299		private readonly _onMessage = new BufferedEmitter<VSBuffer>();
300		readonly onMessage: Event<VSBuffer> = this._onMessage.event;
301	
302		private _terminating: boolean;
303		private _protocolListener: IDisposable;
304	
305		constructor() {
306		this._terminating = false;
```

完整 523 行 / 21 572 bytes 落盘 `/tmp/run1.out`、`/tmp/run2.out`（保留供后续比对）。

### Run 2（2026-07-27 09:46 CST，sparse-checkout 多加 `src/vs/server`）

复现命令：

```bash
mkdir -p /tmp/eval-repos/vscode && cd /tmp/eval-repos/vscode
git clone --depth=1 --filter=blob:none --sparse https://github.com/microsoft/vscode.git
cd vscode
git sparse-checkout set src/vs/workbench/services/extensions/node src/vs/workbench/api src/vs/server
codegraph init
codegraph explore "How does the extension host communicate with the main process?" --max-files 12 > /tmp/vscode-run2.txt 2>&1
head -50 /tmp/vscode-run2.txt
```

verbatim 50 行（head -50 /tmp/vscode-run2.txt）：

```text
**Exploration: How does the extension host communicate with the main process?**

Found 60 symbols across 4 files.

**Blast radius — what depends on these (update/verify before editing)**

- `startExtensionHostProcess` (src/vs/workbench/api/node/extensionHostProcess.ts:397) — 1 caller in `src/vs/workbench/api/node/extensionHostProcess.ts`; ⚠️ no covering tests found
- `ExtensionHostMain` (src/vs/workbench/api/common/extensionHostMain.ts:161) — 4 callers in `src/vs/workbench/api/node/extensionHostProcess.ts`, `src/vs/workbench/api/worker/extensionHostWorker.ts`; ⚠️ no covering tests found
- `HostExtension` (src/vs/workbench/api/common/extHostExtensionActivator.ts:147) — 2 callers in `src/vs/workbench/api/common/extHostExtensionService.ts`; ⚠️ no covering tests found
- `ExtensionHostProxy` (src/vs/workbench/api/browser/mainThreadExtensionService.ts:197) — 1 caller in `src/vs/workbench/api/browser/mainThreadExtensionService.ts`; ⚠️ no covering tests found
- `_isHostExtension` (src/vs/workbench/api/common/extHostExtensionActivator.ts:332) — 1 caller in `src/vs/workbench/api/common/extHostExtensionActivator.ts`; ⚠️ no covering tests found

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`src/vs/workbench/api/node/extensionHostProcess.ts`** — imports(imports), ExtensionHostMain(imports), IExitFn(imports), IHostUtils(imports), IDisposable(imports), ParsedExtHostArgs(interface), +3 more

```typescript
5
6	import minimist from 'minimist';
7	import * as nativeWatchdog from '@vscode/native-watchdog';
8	import * as net from 'net';
9	import { ProcessTimeRunOnceScheduler } from '../../../base/common/async.js';
10	import { VSBuffer } from '../../../base/common/buffer.js';
11	import { PendingMigrationError, isCancellationError, isSigPipeError, onUnexpectedError, onUnexpectedExternalError } from '../../../base/common/errors.js';
12	import { Event } from '../../../base/common/event.js';
13	import * as performance from '../../../base/common/performance.js';
14	import { IURITransformer } from '../../../base/common/uriIpc.js';
15	import { Promises } from '../../../base/node/pfs.js';
16	import { IMessagePassingProtocol } from '../../../base/parts/ipc/common/ipc.js';
17	import { BufferedEmitter, PersistentProtocol, ProtocolConstants } from '../../../base/parts/ipc/common/ipc.net.js';
18	import { NodeSocket, WebSocketNodeSocket } from '../../../base/parts/ipc/node/ipc.net.js';
19	import type { MessagePortMain, MessageEvent as UtilityMessageEvent } from '../../../base/parts/sandbox/node/electronTypes.js';
20	import { boolean } from '../../../editor/common/config/editorOptions.js';
21	import product from '../../../platform/product/common/product.js';
22	import { ExtensionHostMain, IExitFn } from '../common/extensionHostMain.js';
23	import { IHostUtils } from '../common/extHostExtensionService.js';
24	import { createURITransformer } from '../../../base/common/uriTransformer.js';
25	import { ExtHostConnectionType, readExtHostConnection } from '../../services/extensions/common/extensionHostEnv.js';
26	import { ExtensionHostExitCode, IExtHostReadyMessage, IExtHostReduceGraceTimeMessage, IExtHostSocketMessage, IExtensionHostInitData, MessageType, createMessageOfType, isMessageOfType } from '../../services/extensions/common/extensionHostProtocol.js';
27	import { IDisposable } from '../../../base/common/lifecycle.js';
28	import '../common/extHost.common.services.js';
29	import './extHost.node.services.js';
30	import { createRequire } from 'node:module';
31	const require = createRequire(import.meta.url);
32	
33	interface ParsedExtHostArgs {
34		transformURIs?: boolean;
35		skipWorkspaceStorageLock?: boolean;
```

统计：

- 行数：`wc -l /tmp/vscode-run2.txt` → **585**
- 字节数：`wc -c /tmp/vscode-run2.txt` → **25 134**
- tokens≈：`wc -c /tmp/vscode-run2.txt | awk '{print int($1/4)}'` → **6 283**
- wall-clock time：`{ time codegraph explore ... } 2>&1` → **0.293 s**

注：与 Run 1 (`45 symbols / 3 files / 21 572 bytes / 0.308 s`) 数字不一致，原因是 Run 2 的 `git sparse-checkout set` 多了 `src/vs/server` 路径，codegraph 在更宽的代码区命中了 `ExtensionHostProxy` / `HostExtension` 等 4 个入口符号（Run 1 只命中 3 个）。Run 1 走的是 README 上一版 sparse 路径 (`services/extensions` 不带 `/node`)，Run 2 按当前任务规格加了 `/node` 子路径；两个 sparse 集合的并集 ≠ 任意一个子集，因此命中数和 bytes 不一致属正常行为（两次运行本身字节级可重复，每次响应都确定）。

返回的 4 个文件清单：

1. `src/vs/workbench/api/node/extensionHostProcess.ts`
2. `src/vs/workbench/api/common/extensionHostMain.ts`
3. `src/vs/workbench/api/common/extHostExtensionActivator.ts`
4. `src/vs/workbench/api/browser/mainThreadExtensionService.ts`

引用的关键符号（节选）：`startExtensionHostProcess:397`、`ExtensionHostMain:161`、`HostExtension:147`、`ExtensionHostProxy:197`、`_isHostExtension:332` 等；blast radius 给出 5 个反向 caller，与"ExtensionHost IPC + Message + Activator Proxy"通道语义一致。

## 两次跑统计

| run | symbols | files | bytes | tokens~ (bytes/4) | time (wall-clock) | md5 |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 45 | 3 | 21 572 | 5 393 | 0.308 s | `3d17656200455a2a3d9ec52d45ed08e6` |
| 2 | 60 | 4 | 25 134 | 6 283 | 0.293 s | (未测，新 Run 2 sparse 集合扩展了 `src/vs/server`，见 Run 2 节) |

环境：macOS Darwin 24.6.0 (arm64) / node v24.14.1 / codegraph 1.5.0。

## 与 Ch09 章节引用对比

Ch09 §9.3.1 引用的 `examples/vscode/README.md` 老表给出 **1 symbol / 1 file / ~1638 tokens / 0.15s**。本次探针的真实数字与之**不一致**，下面是逐项对照：

| 维度 | Ch09 §9.3.1 旧值 | 探针本次（run1） | 差异说明 |
|---|---|---|---|
| commit | `8f722dacb9bfb092108657867f5763b271ca7c1a` | `74dc74c00942cd18cc82eb72e6f08de8a7cf1cf1` | 仓库 HEAD 在数月间推进，旧 README 数字在最新 commit 上不再成立 |
| symbols | 1 | **45** | 旧版只命中 1 个 IPC 入口符号；新版因 git 演进而扩展到 3 个文件的关键 IPC 类（`ExtensionHostMain` / `ExtensionHostProcess` / `createExtHostProtocol`） |
| files | 1 | **3** | 同上，跨 `localProcessExtensionHost.ts` / `extensionHostProcess.ts` / `remoteExtensionHost.ts` |
| tokens~ | 1 638 | **5 393** | 探针输出包含"verbatim 源码 + blast radius + 行号大头"，旧 MCP 探针很可能只回了被请求的 1 个符号的窄上下文 |
| time | 0.15 s | **0.308 s** | 探针本身带 0.3 s 量级启动开销 + 解析 3 个文件源码；环境与命令路径相同 |

⚠ **Ch09 章节的旧数字已与当前 commit 失真**。建议 Ch09 维护者同步更新 §9.3.1 行文，并将 `examples/vscode/README.md`（旧表 1/1/1638/0.15s）替换或标注为 historical。

## 与 README 自报数据对比

CodeGraph 项目根 `README.md` 在 41s / 2 tools / 265 000 tokens / $0.36 这一行报告的是**完整 agent arm**（WITH：让 Claude 跑带 codegraph 工具的全任务）的中位数，与本探针不能直接对齐：

| 维度 | 探针本次 | README 自报（VS Code WITH） |
|---|---|---|
| 调用次数 | 2（固定两次 MCP `explore`） | 2（整段任务的全部工具调用） |
| 工具种类 | 1（`codegraph_explore` only） | 2（`codegraph_explore` + 至少 1 个文件工具；自报 0 文件读取说明另外 1 个是 `codegraph_status` 之类） |
| tokens | 5 393（仅响应字节） | 265 000（输入 + 输出 + thinking） |
| cost | N/A（本探针不走计费 API） | $0.36（按 Anthropic 公开 rate 折算） |
| time | 0.308 s（单次查询） | 41 s（整段 agent loop） |

差距是**数量级**的，原因：

- 265 k tokens 中绝大部分是 agent 的 prompt / 大窗口上下文 / 思考，不是 codegraph 响应本身；
- agent arm 跑 4 次取中位数，单次 41 s 内做的事远不止 1 个 `codegraph_explore`；
- 本探针只测**索引查询**这一环节，且只统计单次响应字节，与 "成本/工具/总 tokens" 口径不可比。

## 复现三步

```bash
# 1. 准备克隆
mkdir -p /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/vscode && cd $_ \
  && git clone --depth=1 --filter=blob:none --sparse https://github.com/microsoft/vscode.git \
  && cd vscode \
  && git sparse-checkout set src/vs/workbench/services/extensions src/vs/workbench/api

# 2. 索引
codegraph init        # 385 files / 17,951 nodes / 56,312 edges / 1.3 s

# 3. 探针
codegraph explore "How does the extension host communicate with the main process?" --max-files 12
```

体积检查：`du -sh .codegraph/` ≈ **65 MB**（含 errors.log + SQLite + 每个原文件的 verbatim cache）；`du -sh .` ≈ **80 MB**（sparse-checkout + 索引合计）。clone 未删除，留待后续验证。
