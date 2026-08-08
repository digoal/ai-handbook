# 23. 术语表

> **读者**:全员
> **预计阅读**:4 分钟
> **前置依赖**:无

## 目标

把整个 handbook 用到的专有名词按"领域"分组,每条一句话定义 + 在哪里出现。

---

## 23.1 平台与基础设施

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **Cloudflare Durable Object(DO)** | Cloudflare Edge 上有持久化 SQLite 的 actor | [第 1 章](01_overview.md)、[第 12 章](12_arch_overview.md) |
| **Cloudflare Container** | Cloudflare 提供的 Linux 容器运行时 | [第 3 章](03_user_install.md)、[第 12 章](12_arch_overview.md) |
| **Cloudflare Workers** | Cloudflare Edge 上的 serverless V8 isolate | [第 3 章](03_user_install.md)、[第 10 章](10_dev_client.md) |
| **Cloudflare R2** | Cloudflare 的对象存储(S3 兼容) | [第 21 章](21_ref_config.md) |
| **Wrangler** | Cloudflare 的 Worker / DO / Container 部署 CLI | [第 3 章](03_user_install.md) |
| **Egress interceptor** | Cloudflare 用于路由 DO 出站 WS 的机制 | [第 12 章](12_arch_overview.md) |

---

## 23.2 仓库自身

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **Workspace** | `@cloudflare/computer` 的核心 facade | [第 4 章](04_user_basics.md) |
| **`computerd`** | Container 内运行的 Node SEA 二进制守护进程 | [第 2 章](02_quickstart.md)、[第 20 章](20_ref_cli.md) |
| **Backend** | `WorkspaceBackend` 策略接口,4 个内置实现 | [第 3 章](03_user_install.md)、[第 9 章](09_dev_backend.md) |
| **TestBackend** | in-memory 假 backend,用于 Vitest | [第 11 章](11_dev_testing.md) |
| **CloudflareContainerBackend** | 走 `computerd` + FUSE 的 backend | [第 3 章](03_user_install.md) |
| **WorkerShellBackend** | 走 Dynamic Worker + just-bash 的 backend | [第 3 章](03_user_install.md) |
| **WorkerJavaScriptBackend** | 走 Dynamic Worker + ES module 的 backend | [第 3 章](03_user_install.md) |
| **`@cloudflare/dofs`** | SQLite-backed VFS 内核(私有包) | [第 7 章](07_dev_packages.md)、[第 8 章](08_dev_vfs.md) |
| **`@cloudflare/computer-rpc`** | capnweb wire types + driver(私有包) | [第 7 章](07_dev_packages.md)、[第 14 章](14_arch_protocol.md) |
| **`@cloudflare/computerd`** | computerd 的 npm 源(私有包) | [第 7 章](07_dev_packages.md) |
| **`@cloudflare/computer-computerd-linux-x64`** | Docker 镜像 context(私有包) | [第 7 章](07_dev_packages.md) |
| **`@cloudflare/think`** | Cloudflare 的 AI agent SDK,`examples/think` 演示了集成 | [第 10 章](10_dev_client.md) |

---

## 23.3 VFS / 存储

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **VFS**(Virtual File System) | 虚拟文件系统,这里是 SQLite-backed | [第 1 章](01_overview.md) |
| **chunk** | 写盘的最小单位(默认 512 KiB) | [第 5 章](05_user_advanced.md)、[第 8 章](08_dev_vfs.md) |
| **content-addressing** | 以内容哈希(sha256)为 key 的存储 | [第 8 章](08_dev_vfs.md)、[第 13 章](13_arch_abstractions.md) |
| **manifest** | 文件级别的 chunk 列表(content-addressed) | [第 8 章](08_dev_vfs.md) |
| **staged chunk** | 已落 `vfs_blobs` 但未进 `vfs_manifests` 的 chunk | [第 8 章](08_dev_vfs.md)、`8758b51` |
| **linked chunk** | 已被 manifest 引用的 chunk | [第 8 章](08_dev_vfs.md) |
| **inode** | VFS 中的"文件元数据行"(`vfs_nodes`) | [第 8 章](08_dev_vfs.md) |
| **tombstone** | `vfs_changes` 中标记删除的 entry | [第 8 章](08_dev_vfs.md)、[第 15 章](15_arch_consistency.md) |
| **resolve cache** | `path → node_id` 的 SQL 缓存(事务感知) | [第 8 章](08_dev_vfs.md)、[第 15 章](15_arch_consistency.md) |
| **GC** | orphan blob 回收(commit 时执行) | [第 17 章](17_arch_performance.md) |
| **blob cache** | `vfs_blobs` 字节缓存 | [第 8 章](08_dev_vfs.md) |
| **`SAVEPOINT`** | SQLite 的嵌套事务原语 | [第 15 章](15_arch_consistency.md) |
| **`Database.transactionSync`** | DO SQLite 原生事务 + SAVEPOINT 包装 | [第 8 章](08_dev_vfs.md) |

---

## 23.4 同步 / wire

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **capnweb** | Cloudflare 的"capnproto over WS" RPC 子集 | [第 14 章](14_arch_protocol.md) |
| **WorkspaceRPC** | `SyncRPC + ShellRPC` 的组合 wire 契约 | [第 13 章](13_arch_abstractions.md)、[第 14 章](14_arch_protocol.md) |
| **SyncRPC** | 同步状态用的 RPC 通道(`push` / `fetchChanges` / ...) | [第 14 章](14_arch_protocol.md) |
| **ShellRPC** | 执行命令用的 RPC 通道(`exec` / `getExec` / ...) | [第 14 章](14_arch_protocol.md) |
| **push / pull** | 同步的两个方向;`push` 把变更推到对端,`pull` 把变更拉回 DO | [第 5 章](05_user_advanced.md)、[第 14 章](14_arch_protocol.md) |
| **`pushRev` / `fetchRev`** | watermark,持久化对端协商进度 | [第 15 章](15_arch_consistency.md) |
| **`fetchCursor`** | 拉取游标(`_vfs_fetch_cursor` 表) | [第 8 章](08_dev_vfs.md) |
| **`PULL_BATCH_SIZE = 256`** | pull 每次批大小 | [第 17 章](17_arch_performance.md) |
| **ChangeEntry** | `vfs_changes` 的 entry 类型 | [第 8 章](08_dev_vfs.md) |
| **ManifestChunk** | `vfs_manifests` 的 entry 类型 | [第 8 章](08_dev_vfs.md) |
| **heartbeat** | 周期性 `SyncRPC.watermarks()` 调用 | [第 14 章](14_arch_protocol.md)、[第 15 章](15_arch_consistency.md) |
| **end-to-end backpressure** | capnweb ReadableStream 让 consumer 慢 → kernel pipe → 子进程阻塞 | [第 4 章](04_user_basics.md)、[第 14 章](14_arch_protocol.md) |
| **stub disposal** | capnweb export table 项释放(`using` / `[Symbol.dispose]()`) | [第 4 章](04_user_basics.md)、[第 14 章](14_arch_protocol.md) |
| **`Symbol.dispose`** | JavaScript 的资源释放 hook(同 `using` 语法) | [第 4 章](04_user_basics.md) |
| **LWW**(Last-Write-Wins) | 冲突策略;晚的覆盖早的 | [第 15 章](15_arch_consistency.md) |
| **`SyncRetryIntent`** | sync 失败的应用层重试意图 | [第 22 章](22_ref_errors.md) |

---

## 23.5 执行 / runtime

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **exec handle** | `runtime.exec(...)` 返回的句柄,既是 stream 又有 result | [第 4 章](04_user_basics.md) |
| **ExecEvent** | exec 期间的 stream 事件 | [第 4 章](04_user_basics.md)、[第 14 章](14_arch_protocol.md) |
| **`callable`** | `WorkspaceBackend.callable?: true` 的 flag,决定走 `CommandExecutor` 还是 `ModuleExecutor` | [第 9 章](09_dev_backend.md)、[第 13 章](13_arch_abstractions.md) |
| **`ModuleExecutor`** | callable backend 的执行路径(host capability calls) | [第 12 章](12_arch_overview.md) |
| **`CommandExecutor`** | 非 callable backend 的执行路径(push → exec → pull) | [第 12 章](12_arch_overview.md) |
| **`WorkspaceScopedFS`** | 模块后端 FS 调用的唯一入口(做路径限制 / 权限 / 限额) | [第 9 章](09_dev_backend.md)、[第 16 章](16_arch_security.md) |
| **Runner** | `computerd` 内 spawn + 监管子进程的类 | [第 4 章](04_user_basics.md) |
| **just-bash** | Vercel 的 TypeScript bash 子集实现,`WorkerShellBackend` 用它 | [第 1 章](01_overview.md)、[第 3 章](03_user_install.md) |
| **exec log buffer** | `computerd` 内存中保留的 exec 事件 buffer(`EXEC_LOG_MAX_BYTES`) | [第 20 章](20_ref_cli.md) |
| **`EEXEC_BUSY`** | 同一 exec id 已存在,旧 handle 未释放 | [第 6 章](06_user_troubleshooting.md)、[第 22 章](22_ref_errors.md) |
| **`ELOG_TRUNCATED`** | exec log buffer 满 | [第 22 章](22_ref_errors.md) |

---

## 23.6 构建 / 工具链

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **SEA**(Single Executable Application) | Node.js 18+ 的单文件可执行特性 | [第 7 章](07_dev_packages.md)、[第 20 章](20_ref_cli.md) |
| **`postject`** | 把 SEA blob 注入 Node 二进制的工具 | [第 20 章](20_ref_cli.md) |
| **`esbuild`** | 高速 TS/JS bundler,SEA 用它打包 | [第 7 章](07_dev_packages.md) |
| **Rolldown** | 高速 Rust 写的 bundler,`@cloudflare/computer` 用它 | [第 7 章](07_dev_packages.md) |
| **Biome** | 统一 lint + format(替代 ESLint + Prettier) | [第 21 章](21_ref_config.md) |
| **sherif** | 保证跨 workspace 版本对齐的工具 | [第 11 章](11_dev_testing.md) |
| **Vitest** | 测试运行器 | [第 11 章](11_dev_testing.md) |
| **`@cloudflare/vitest-pool-workers`** | workerd runner for vitest | [第 11 章](11_dev_testing.md) |
| **changesets** | 版本管理 + 发布工具 | [第 18 章](18_arch_roadmap.md) |
| **pkg-pr-new** | PR 期间发布预览版 npm 包的工具 | [第 11 章](11_dev_testing.md) |
| **`fuse-native`** | libfuse 的 Node.js 绑定 | [第 7 章](07_dev_packages.md) |
| **macFUSE** | macOS 上的 FUSE 实现 | [第 2 章](02_quickstart.md) |
| **`@platformatic/vfs`** | node:fs-shaped VFS 抽象,`SQLiteWorkspaceProvider` 基于它 | [第 8 章](08_dev_vfs.md) |
| **isomorphic-git** | 纯 JS git 实现,workspace git 基于它 | [第 7 章](07_dev_packages.md) |

---

## 23.7 测试 / 调试

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **`SQLiteTestStorage`** | 基于 `node:sqlite` 的 DO storage 替代,用于 Vitest | [第 11 章](11_dev_testing.md) |
| **`CountingStorage`** | 装饰 SQL 调用的工具,记录读 / 写次数 + 行数 | [第 11 章](11_dev_testing.md) |
| **`stubSnapshot`** | `@cloudflare/computer-rpc/debug` 提供,查 stub 数量 | [第 11 章](11_dev_testing.md) |
| **`/__computerd/stubs`** | `computerd` 暴露的 stub 快照 HTTP 端点(需 `CAPNWEB_TRACK_STUBS=1`) | [第 11 章](11_dev_testing.md) |
| **`/__computerd/stats`** | `computerd` 暴露的运行统计 HTTP 端点 | [第 11 章](11_dev_testing.md) |
| **`/__computerd/info`** | `computerd` 暴露的 backend / mount / port 信息 | [第 2 章](02_quickstart.md) |
| **TDD** | Test-Driven Development,新功能先写测试 | [第 11 章](11_dev_testing.md) |
| **fs-bench.sh** | `computerd` vs ext4 vs tmpfs 三方性能对比脚本 | [第 11 章](11_dev_testing.md)、[第 17 章](17_arch_performance.md) |

---

## 23.8 协议层 / 安全

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **POSIX errno** | `ENOENT` / `EEXIST` 等传统 Unix 错误码 | [第 22 章](22_ref_errors.md) |
| **`WorkspaceError`** | wire 上的应用错误,保留 `code` | [第 22 章](22_ref_errors.md) |
| **`ExecError`** | exec 期间的错误,持有 `code` | [第 22 章](22_ref_errors.md) |
| **`WireErrorCode`** | `ENOENT` / `EUNKNOWN_HASH` / `ESHUTDOWN` / `EAUTH` / `EPROTOCOL` | [第 22 章](22_ref_errors.md) |
| **`isWorkspaceTransportFailure`** | 辨识 transport 失败 vs 业务错误 | [第 22 章](22_ref_errors.md) |
| **EAUTH** | wire 层鉴权码(**未在代码中确认触发路径**) | [第 16 章](16_arch_security.md) |
| **trust boundary** | 信任域边界(public / edge / container) | [第 16 章](16_arch_security.md) |
| **capability policy** | `WorkspaceScopedFS` 中的路径 / 权限 / 限额策略 | [第 16 章](16_arch_security.md) |

---

## 23.9 其他

| 术语 | 一句话 | 出现位置 |
|---|---|---|
| **PREVIEW** | 当前包状态:API 不稳定,未升 `latest` | [第 1 章](01_overview.md)、[第 18 章](18_arch_roadmap.md) |
| **rollup/dts** | Rolldown 的 dts 插件,产出 `.d.ts` | [第 7 章](07_dev_packages.md) |
| **git worktree** | git 在 workspace 上的工作树语义(子模块) | [第 18 章](18_arch_roadmap.md) |
| **AI SDK tools** | Vercel AI SDK 的 `Tool` 类型,`createAITools` 产出 | [第 10 章](10_dev_client.md)、[第 19 章](19_ref_api.md) |
| **sub-path export** | npm package `exports` 字段下的 sub-path(如 `@cloudflare/computer/git`) | [第 7 章](07_dev_packages.md)、[第 19 章](19_ref_api.md) |

---

## 延伸阅读

- 本 handbook 全部 23 章 + README 索引
- [`docs/README.md`](../../docs/README.md) — 既有专题索引
- [`README.md`](../../README.md) — 项目根 README