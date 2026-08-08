# 19. `computer` 客户端 API 参考

> **读者**:开发者 / 用户
> **预计阅读**:8 分钟
> **前置依赖**:[第 4 章 基础操作](04_user_basics.md)

## 目标

把 `@cloudflare/computer` 主包 + sub-path exports 的所有公开 API 列一遍,每条标注 `path:line` 引用,便于查阅。

> 本章是"摘要式参考",不是逐字 API dump。每个签名以源码当前状态(`8758b51`)为准;若 `git log` 后续修改了某个方法,请提 PR 同步本章。

---

## 19.1 主入口:`@cloudflare/computer`

`packages/computer/src/index.ts:0-105`

### Workspace 构造与取出

| 符号 | 来源 | 用途 |
|---|---|---|
| `Workspace` | `src/workspace.ts:259` | 主 facade,见 [第 4 章](04_user_basics.md#41-workspace--一切的入口) |
| `WorkspaceOptions` | `src/workspace.ts:179ish` | 构造参数 |
| `withWorkspace` | `src/with-workspace.ts:34-79` | DO mixin |
| `getWorkspace` | `src/client.ts:366-406` | 从 stub host 取 stub |

### Workspace Stub

| 符号 | 来源 | 用途 |
|---|---|---|
| `WorkspaceStub` | `src/stub.ts:90+` | 顶层 stub 组合 |
| `WorkspaceFilesystemStub` | `src/stub.ts` | `fs.*` 远端视图 |
| `WorkspaceRuntimeStub` | `src/stub.ts` | `runtime.*` 远端视图 |
| `WorkspaceRuntimeExecHandleStub` | `src/stub.ts` | exec handle 远端视图 |
| `WorkspaceGitStub` | `src/stub.ts` | `git.*` 远端视图 |
| `WorkspaceAssetsStub` | `src/stub.ts` | `assets.*` 远端视图 |

### Runtime

| 符号 | 来源 | 用途 |
|---|---|---|
| `WorkspaceRuntimeClient` | `src/client.ts` | 客户端 runtime 类型 |
| `WorkspaceRuntimeExecOptions` | `src/runtime/runtime.ts` | exec options |
| `WorkspaceRuntimeGetOptions` | `src/runtime/runtime.ts` | getExec options |
| `WorkspaceRuntimeKillOptions` | `src/runtime/runtime.ts` | killExec options |
| `WorkspaceRuntimeResult` | `src/runtime/types.ts` | exec 完成后 result 形状 |
| `WorkspaceRuntimeEvent` | `src/runtime/types.ts` | exec 期间 event 形状 |
| `WorkspaceRuntimeStatus` | `src/runtime/types.ts` | status 枚举 |
| `WorkspaceRuntimeValue` | `src/runtime/types.ts` | exec return value |
| `WorkspaceTrustedModule` | `src/runtime/types.ts` | 模块后端 trusted module 形状 |
| `WorkspaceRegisteredBackend` | `src/runtime/types.ts` | 注册到 workspace 的 backend 描述 |
| `WorkspaceRuntimeLoader` | `src/runtime/types.ts` | dynamic worker loader 形状 |

### Backend 接口

| 符号 | 来源 | 用途 |
|---|---|---|
| `BackendHandle` | `src/backend.ts:72` | `connect()` 返回值 |
| `WorkspaceBackend` | `src/backend.ts:38` | 策略接口 |

### Test Backend

| 符号 | 来源 | 用途 |
|---|---|---|
| `TestBackend` | `src/backends/test.ts:1` | 内存假后端 |
| `TestBackendOptions` | `src/backends/test.ts` | options 形状 |

### SQL / VFS(`@cloudflare/dofs` re-export)

| 符号 | 来源 | 用途 |
|---|---|---|
| `SQLiteWorkspaceProvider` | `@cloudflare/dofs` | node:fs 形状的 facade |
| `Database` | `@cloudflare/dofs` | SQL 入口 |
| `initializeSchema` | `@cloudflare/dofs` | 初始化 SQLite schema |
| `ApplyResult` | `@cloudflare/dofs` | applyChangesSync 返回值 |
| `DurableObjectStorageLike` | `@cloudflare/dofs` | DO storage 类型 |
| `SkippedEntry` | `@cloudflare/dofs` | sync skip reason |
| `SQLiteWorkspaceProviderOptions` | `@cloudflare/dofs` | provider options |

> 注:`@cloudflare/dofs` 的 fs primitives **当前未从 `@cloudflare/computer` 主入口 re-export**,只在 `@cloudflare/dofs` 自身入口可见。

### Mount

| 符号 | 来源 | 用途 |
|---|---|---|
| `R2Bucket` | `src/mounts/` | R2 mount |
| `R2BucketBinding` | `src/mounts/` | wrangler binding |
| `R2BucketOptions` | `src/mounts/` | options |
| `EagerMount` | `src/mounts/types.ts` | mount 父类 |
| `Mount` | `src/mounts/types.ts` | mount 类型 |
| `MountBase` | `src/mounts/types.ts` | mount 基类 |
| `MountContext` | `src/mounts/types.ts` | mount 上下文 |
| `MountFactory` | `src/mounts/types.ts` | mount 工厂 |
| `MountWriteAPI` | `src/mounts/types.ts` | mount 写 API |

### Shell helpers

| 符号 | 来源 | 用途 |
|---|---|---|
| `sh` | `src/sh.ts` | shell 命令拼接便利 |
| `shellQuote` | `src/sh.ts` | shell quote helper |
| `RawShellValue` | `src/sh.ts` | 原始 shell value |
| `ShellValue` | `src/sh.ts` | shell value |
| `ExecEncoding` | `src/runtime/types.ts` | encoding 枚举("utf8" / "base64") |
| `ExecSyncResult` | `src/runtime/types.ts` | sync exec result 形状 |
| `KillSignal` | `src/runtime/types.ts` | kill 信号 |

### 观测

| 符号 | 来源 | 用途 |
|---|---|---|
| `noopObserver` | `src/observe.ts:101` | 默认 noop observer |
| `WorkspaceObserver` | `src/observe.ts:101` | observer 接口 |
| `WorkspaceSpan` | `src/observe.ts` | span 类型 |
| `WorkspaceAttributes` | `src/observe.ts` | span attrs |
| `WorkspaceAttributeValue` | `src/observe.ts` | span attr value |

### 重试

| 符号 | 来源 | 用途 |
|---|---|---|
| `SyncRetryScheduler` | `src/workspace.ts:59` | sync 重试调度器 |
| `SyncRetryIntent` | `src/workspace.ts:47` | 重试意图 |
| `SyncRetryOptions` | `src/workspace.ts` | options |
| `WorkspaceRetryPendingSyncResult` | `src/workspace.ts` | 重试结果 |

### Proxy

| 符号 | 来源 | 用途 |
|---|---|---|
| `WorkspaceProxy` | `src/proxy.ts` | workerd-only |
| `WorkspaceProxyProps` | `src/proxy.ts` | props |
| `WorkspaceServiceProxy` | `src/proxy.ts` | service proxy |
| `WorkspaceServiceProxyProps` | `src/proxy.ts` | props |
| `ArtifactsCLITarget` | `src/proxy.ts` | artifacts CLI target |
| `ThinkWorkspaceCompatibility` | `src/proxy.ts` | think 兼容类型 |

> `src/proxy-stub.ts` 是 Node 端 fallback,实例化 throw。

### Wire codec

| 符号 | 来源 | 用途 |
|---|---|---|
| `decodeExecEvents` | `src/exec-wire.ts` | exec event 解码 |
| `encodeExecEvents` | `src/exec-wire.ts` | exec event 编码 |
| `decodeRuntimeEvents` | `src/exec-wire.ts` | runtime event 解码 |
| `encodeRuntimeEvent` | `src/exec-wire.ts` | runtime event 编码 |

---

## 19.2 Sub-path:`@cloudflare/computer/backends/container`

| 符号 | 来源 | 用途 |
|---|---|---|
| `CloudflareContainerBackend` | `src/backends/container/cloudflare-container.ts:141` | Container 后端 |
| `withWorkspaceContainer` | `src/backends/container/container-host.ts` | Container DO mixin |

---

## 19.3 Sub-path:`@cloudflare/computer/backends/worker-shell`

| 符号 | 来源 | 用途 |
|---|---|---|
| `WorkerShellBackend` | `src/backends/worker-shell/worker-shell.ts:156` | just-bash 后端 |

---

## 19.4 Sub-path:`@cloudflare/computer/backends/worker-javascript`

| 符号 | 来源 | 用途 |
|---|---|---|
| `WorkerJavaScriptBackend` | `src/backends/worker-javascript/worker-javascript.ts:134` | ES module 后端 |

---

## 19.5 Sub-path:`@cloudflare/computer/shell/*`

Tree-shake 友好的 shell 命令 bundle 组:

| Sub-path | 主要内容 |
|---|---|
| `./shell/core` | 核心 shell bundle(必装) |
| `./shell/curl` | curl 命令 |
| `./shell/html-to-markdown` | HTML → MD 转换 |
| `./shell/python` | python runner |
| `./shell/sqlite` | sqlite 命令 |
| `./shell/js-exec` | JS 执行 |
| `./shell/yq` | YAML processor |
| `./shell/file` | file utility |
| `./shell/xan` | xan CSV processor |
| `./shell/jq` | JSON processor |

`packages/computer/src/backends/worker-shell/shell-modules.ts:32` 的 `assembleShellModules(groups: ShellModuleGroup[])` 决定哪些组进 bundle。

---

## 19.6 Sub-path:`@cloudflare/computer/git`

| 符号 | 来源 | 用途 |
|---|---|---|
| `createGitClient` | `src/git/index.ts:339` | isomorphic-git factory |
| `GitClient` | `src/git/index.ts:232` | git client 类型 |
| (CLI 子命令) | `src/git/cli.ts` | argv CLI |

---

## 19.7 Sub-path:`@cloudflare/computer/assets`

| 符号 | 来源 | 用途 |
|---|---|---|
| `createAssets` | `src/assets/index.ts` | R2 presigned URL factory |
| `AssetsClient` | `src/assets/index.ts` | assets client 类型 |

---

## 19.8 Sub-path:`@cloudflare/computer/artifacts`

| 符号 | 来源 | 用途 |
|---|---|---|
| `createArtifact` | `src/artifacts/index.ts` | Artifacts factory |
| `ArtifactClient` | `src/artifacts/index.ts` | artifacts client 类型 |
| `runArtifactsCLI` | `src/artifacts/cli.ts` | CLI 入口 |

---

## 19.9 Sub-path:`@cloudflare/computer/tools`

| 符号 | 来源 | 用途 |
|---|---|---|
| `createAITools` | `src/tools/ai.ts` | AI SDK 工具集(`read`/`write`/`edit`/`ls`/`exec`/`publish`) |
| `createExecTool` | `src/tools/exec.ts:1` | 单 exec tool |
| `createPublishTool` | `src/tools/publish.ts:1` | 单 publish tool |
| (FS tools) | `src/tools/fs/*` | `read` / `write` / `edit` / `ls` / `grep` |

---

## 19.10 Sub-path:`@cloudflare/computer/observe/cloudflare`

`packages/computer/src/observe/cloudflare.ts` —— 把观测 hook 接到 `ctx.tracing`。

---

## 19.11 `@cloudflare/computer-rpc`(private 包,但可独立 import)

| Sub-path | 用途 |
|---|---|
| `.` | wire types(`WorkspaceRPC` / `SyncRPC` / `ShellRPC` / `ExecEvent` / `WireError`) |
| `./server` | `createSyncServer` / `createShellServer` / `createWorkspaceServer` / `acceptWebSocketSession` / `serveHTTPBatch` |
| `./client` | `createSyncClient` / `createWorkspaceClient` |
| `./driver` | `pullOnce` / `pushOnce` / `tick` / `reconcileWatermarks` |
| `./debug` | `enableStubTracking` / `stubSnapshot` / `isStubTrackingEnabled` |

---

## 19.12 `@cloudflare/dofs`(private 包,可在仓库内 import)

入口 `packages/dofs/src/index.ts:0-67`:

- `Database` / `initializeSchema` / `SQLiteWorkspaceProvider`
- fs primitives:`mkdir` / `writeFile` / `readFile` / `rm` / `readdir` / `stat` / `chmod` / `find` / `ls` / `grep` / `symlink` / `readlink` / `gc` / `watch`
- sync blocks:`applyChanges` / `pushObjects` / `fetchChanges` / `fetchObjects` / `hasObjects` / `buildManifest` / `currentRev`
- 子入口 `./testing`:`SQLiteTestStorage`(基于 `node:sqlite`)

---

## 19.13 `@cloudflare/computerd`(private 包)

入口 `packages/computerd/src/index.ts`:

- CLI:`main()`(`packages/computerd/src/cli/computerd.ts:448-628`)
- FUSE:`mountFuse` / `mountShim` / `unmount`
- Exec:`Runner` / `EventLog`

子入口 `./cli/computerd` 提供 bin。

---

## 延伸阅读

- [第 4 章:基础操作](04_user_basics.md) — 用户视角
- [第 9 章:自定义后端](09_dev_backend.md) — Backend 契约
- [第 10 章:客户端与 SDK](10_dev_client.md) — `withWorkspace` 与 stub
- [第 20 章:`computerd` CLI 参考](20_ref_cli.md)
- [第 21 章:配置参考](21_ref_config.md)
- [第 22 章:错误码与异常](22_ref_errors.md)
- [`packages/computer/README.md`](../../packages/computer/README.md)
- [`packages/computer/src/index.ts`](../../packages/computer/src/index.ts)