# 22. 错误码与异常

> **读者**:用户
> **预计阅读**:6 分钟
> **前置依赖**:[第 6 章 常见错误与排查](06_user_troubleshooting.md)

## 目标

把所有错误码(POSIX errno / wire / exec)集中在一页,标注 throw 路径与客户端处理建议。

---

## 22.1 POSIX errno(`packages/dofs/src/errors.ts`)

由 `createWorkspaceError(code, message, path)` 工厂构造,形状像 `NodeJS.ErrnoException`(`err.code` + `err.path`)。

| Code | 含义 | 触发场景 | 处理建议 |
|---|---|---|---|
| `ENOENT` | 文件 / 目录不存在 | `readFile` 不存在的路径、`stat` 失败 | 先 `mkdir -p` 父目录;`statOrNull` / `exists` swallow |
| `EISDIR` | 对目录调用文件操作 | `readFile` 一个目录 | 改用 `readdir` / `ls` |
| `EEXIST` | 目录已存在 | `mkdir` 不带 `recursive: true` | 加 `recursive: true`,或先检查 |
| `ENOTDIR` | 父路径不是目录 | `mkdir` 时父路径是文件 | 先创建父目录 |
| `ENOTEMPTY` | 目录非空 | `rm` 不带 `recursive: true` | 加 `recursive: true`,或先清空 |
| `ELOOP` | symlink 环(超过 40 跳) | symlink 自环 | 检查 symlink |
| `EPERM` | 权限不足 | 操作被 capability 层拒绝 | 改 backend / mount 配置 |
| `EACCES` | 同上 | — | 同上 |
| `EROFS` | 只读文件系统 | 试图写 mount 进来的 R2 只读分支 | 不写,或换 mount |
| `ENOSYS` | 操作未实现 | 调了一个 backend 没实现的 fs 动词 | 改 backend |
| `EINVAL` | 参数非法 | `mkdir` 模式非法等 | 检查参数 |
| `EIO` | SQLite 写失败 | 磁盘满 / 事务冲突 | 看 `/__computerd/stats` 的 RSS / heap |

---

## 22.2 WireError(`packages/rpc/src/interface.ts:158`)

由 RPC server 主动 throw,client adapter rethrow 为 `WorkspaceError` 保留 `code`。

| Code | 触发 | 处理 |
|---|---|---|
| `ENOENT` | wire 上 path 不存在 | (与 POSIX 重名,但来源不同) |
| `EUNKNOWN_HASH` | `fetchObjects` 收到 manifest 引用的 hash 但本地不存在 | 触发 `applyChangesSync` 重试 → 升级到 `8758b51` 之后 |
| `ESHUTDOWN` | 对端进程已关闭,本次调用晚到 | 重连:重新构造 workspace stub |
| `EAUTH` | 协议层鉴权失败 | **未在代码中确认触发路径**;走重连 + 检查 access token |
| `EPROTOCOL` | wire 帧不符合 `WorkspaceRPC` | 确认 client / server 版本一致 |

---

## 22.3 ExecError(`packages/computerd/src/exec/types.ts:71`)

由 `Runner.exec / get` 抛出,`class ExecError extends Error` 持有 `readonly code`。

| Code | 触发 | 处理 |
|---|---|---|
| `EEXEC_BUSY` | 同一个 exec id 已存在,旧 handle 未释放 | 检查是否漏 `using` / `[Symbol.dispose]()` |
| `ENOENT` | exec id 不存在(`getExec` / `killExec`) | 不抛这个,返回 null |
| `ELOG_TRUNCATED` | exec log buffer 满了(`EXEC_LOG_MAX_BYTES`) | 调大 `EXEC_LOG_MAX_BYTES`,或用流式消费 |

---

## 22.4 Process 退出码(`runtime.exec` 返回值)

`await run.result()` 的 `exitCode` 字段:

| Exit Code | 含义 | 处理 |
|---|---|---|
| `0` | 成功 | — |
| `1` | 一般错误 | 看 stderr |
| `2` | 命令误用(shell builtin) | 看 stderr |
| `126` | 找到但不可执行 | chmod +x |
| `127` | 命令未找到 | 检查 PATH 或用绝对路径 |
| `130` | SIGINT(用户 Ctrl-C) | 正常 |
| `137` | SIGKILL(超时) | 调大 `timeoutMs` 或拆短任务 |
| `139` | SIGSEGV(段错误) | 子进程 bug |
| `143` | SIGTERM | 优雅关闭 |

---

## 22.5 `isWorkspaceTransportFailure`(transport 错误辨识)

`packages/computer/src/transport-failure.ts` 的 `isWorkspaceTransportFailure` 区分:

- **transport failure**:WS 断 / capnweb stale stub / 重连错误 → 应该**重连**,不要当业务错误;
- **application error**:`WorkspaceError` / `ExecError` → 按 `code` branch。

```ts
import { isWorkspaceTransportFailure } from "@cloudflare/computer";

try {
  await ws.fs.readFile("/x");
} catch (err) {
  if (isWorkspaceTransportFailure(err)) {
    // 重连
  } else if (err instanceof WorkspaceError) {
    switch (err.code) {
      case "ENOENT": ...; break;
      case "EIO": ...; break;
      default: throw err;
    }
  } else {
    throw err;
  }
}
```

---

## 22.6 `SyncRetryIntent`(应用层重试意图)

`packages/computer/src/workspace.ts:47` 定义。**不**抛,而是标记:

```ts
{
  id: string,
  attemptedAt: number,
  reason: string,
}
```

由 `Workspace.runPostPull` 在 sync pull 失败时调用 `SyncRetryScheduler.schedule(intent)`。

---

## 22.7 错误抛出位置速查

| 文件 | 函数 | 错误 |
|---|---|---|
| `packages/dofs/src/storage.ts` | `databaseOnError` 等 | DB failures → `EIO` |
| `packages/dofs/src/fs/stat.ts:1-86` | `statShared` | `ENOENT` |
| `packages/dofs/src/fs/mkdir.ts` | `mkdirImpl` | `EEXIST` / `ENOTDIR` / `ENOTEMPTY` |
| `packages/dofs/src/fs/rm.ts` | `rmImpl` | `ENOENT` / `ENOTEMPTY` |
| `packages/dofs/src/fs/resolve.ts` | `resolveInode` | `ELOOP`(40 跳) |
| `packages/dofs/src/fs/readFile.ts` / `writeFile.ts` | — | `EIO` / `EINVAL` |
| `packages/rpc/src/server.ts` | `SyncRPCServer` methods | `EUNKNOWN_HASH` / `EPROTOCOL` |
| `packages/computerd/src/exec/runner.ts:72-` | `Runner.exec` / `get` | `EEXEC_BUSY` / `ELOG_TRUNCATED` |
| `packages/computerd/src/cli/computerd.ts` | `parsePort` / `parseMountPoint` / `rejectLegacyFuseEnv` | 配置错误(进程退出) |
| `packages/computer/src/runtime/capability.ts:79-86` | `exists` | swallow `ENOENT` 返回 false |
| `packages/computer/src/stub.ts:132-145` | `statOrNull` / `lstatOrNull` | swallow `ENOENT` 返回 null |
| `packages/computer/src/shell.ts:115` | `CommandExecutor.exec` | `push` 失败 catch + log,`pushed=0`;命令仍跑 |
| `packages/computer/src/shell.ts:239` | `runPostPull` | catch `pull` 失败,surface `sync: { status: "pending" }` |
| `packages/computer/src/proxy-stub.ts` | `WorkspaceProxy` 实例化 | throw(仅在非 workerd 环境) |

---

## 22.8 catch 模式推荐

### 不要

```ts
// ❌ 把 transport 错误当业务错误吞
try { await ws.fs.readFile("/x"); }
catch (e) { console.log("file not found"); }
// → 实际是 WS 断了,下次调用都会失败
```

### 推荐

```ts
// ✅ 按 code branch
try { await ws.fs.readFile("/x"); }
catch (err) {
  if (isWorkspaceTransportFailure(err)) {
    // 重连或重试
  } else if (err instanceof WorkspaceError && err.code === "ENOENT") {
    return new Response("not found", { status: 404 });
  } else {
    throw err;
  }
}
```

### 也推荐

```ts
// ✅ 关键操作双重检查
const content = await ws.fs.exists("/x")
  ? await ws.fs.readFile("/x", "utf8")
  : null;
```

---

## 22.9 设计原则

来自 `packages/dofs/src/errors.ts` 注释:

1. **不引入 emoji** —— 错误信息是程序化消费的;
2. **新错误类优先于新错误码** —— 当行为是异常流破坏时;
3. **抛之前先检查** —— `EEXIST` for `mkdir` 仅在 `resolveInode` 返回 null 后触发;
4. **`createWorkspaceError` 工厂保证形状一致** —— `err.code` + `err.path` 都是字符串;
5. **transport failure 与业务错误分离** —— 见 §22.5。

---

## 延伸阅读

- [第 6 章:常见错误与排查](06_user_troubleshooting.md) — 故障排查速查
- [第 14 章:capnweb 协议](14_arch_protocol.md#149-协议错误-vs-业务错误) — 错误码在 wire 中的位置
- [`packages/dofs/src/errors.ts`](../../packages/dofs/src/errors.ts) — POSIX 错误工厂
- [`packages/computerd/src/exec/types.ts`](../../packages/computerd/src/exec/types.ts) — `ExecErrorCode`
- [`packages/computer/src/transport-failure.ts`](../../packages/computer/src/transport-failure.ts) — transport failure 辨识