# 6. 常见错误与排查

> **读者**:用户
> **预计阅读**:8 分钟
> **前置依赖**:[第 4 章 基础操作](04_user_basics.md)

## 目标

按"启动 → 同步 → 写入 → 执行 → 销毁"的链路分组列出最常见的错误,每条错误给出:**症状 / 触发条件 / 修法**。同时给出"该看哪些指标 / 日志"的入门指引。

---

## 6.1 F6. 错误处理流程

**F6. 错误处理流程图** — 出错后第一步该看哪?

```mermaid
flowchart TD
  ERR[出错了]:::err
  Q1{哪一层报错?}:::q
  P1["`computerd` 启动<br/>或 FUSE 挂载"]:::layer
  P2["npm install / build<br/>或 wrangler 部署"]:::layer
  P3["运行时<br/>ws.fs / runtime.exec"]:::layer
  P4["capnweb WS<br/>断 / 重连 / stub 泄漏"]:::layer

  A1["看 env vars<br/>FUSE_MOUNT / PORT / MOUNT_POINT<br/>/__computerd/info"]:::ans
  A2["看 dist / build 日志<br/>看 .codegraph/ 索引<br/>重跑 npm run build"]:::ans
  A3["看 error.code<br/>对照 22_ref_errors<br/>看 /__computerd/stats"]:::ans
  A4["CAPNWEB_TRACK_STUBS=1<br/>/__computerd/stubs<br/>查是否漏 using"]:::ans

  ERR --> Q1
  Q1 -->|启动期| P1 --> A1
  Q1 -->|构建期| P2 --> A2
  Q1 -->|运行期| P3 --> A3
  Q1 -->|连接期| P4 --> A4

  classDef err fill:#ffd6d6,stroke:#b83b3b,color:#3d1414
  classDef q fill:#fff5d6,stroke:#b89c3b,color:#3d3416
  classDef layer fill:#dbe9ff,stroke:#3b6db8,color:#1a2c4e
  classDef ans fill:#dff5d8,stroke:#3b8a3a,color:#1a3d18
```

---

## 6.2 启动期错误(`computerd` 起不来)

| 现象 / 关键句 | 触发条件 | 处理方法 |
|---|---|---|
| `DISABLE_FUSE is no longer supported; use FUSE_MOUNT=none instead` | 用了已废弃 env | 改用 `FUSE_MOUNT=none` |
| `FUSE_SHIM is no longer supported; use FUSE_MOUNT=shim instead` | 同上 | 改用 `FUSE_MOUNT=shim` |
| `WSD_FUSE_BACKEND is no longer supported` | 同上 | 改用 `FUSE_MOUNT=fuse` 或 `macfuse` |
| `PORT must be an integer between 0 and 65535` | `PORT` 不是合法整数 | 改成 `0-65535` 整数 |
| `MOUNT_POINT must be an absolute path` | 给的是相对路径 | 用绝对路径,默认 `/workspace` |
| `EXEC_LOG_MAX_BYTES must be a positive integer` | 给了非整数 / 0 / NaN | 改成正整数 |
| `fuse-native` 编译失败 | 缺 build toolchain | `apt-get install build-essential libfuse-dev`,或 `npm install --ignore-scripts` |
| `file in wrong format` link 错 | Linux arm64 host 用了 x86 预编译 libfuse | 替换 aarch64 libfuse 并 `npx node-gyp rebuild` |
| `npm test` 报 `Cannot find module '@cloudflare/dofs/dist/...'` | 没先 build 兄弟包 | `npm run build` 然后再 `npm test` |
| FUSE 测试不通过 `EPERM` | 容器里手工 `mknod /dev/fuse`,但没有 `--privileged` | 把 `/dev/fuse` 留空,或真给 `--privileged` / `CAP_SYS_ADMIN` |

启动期最有效的自检三连:

```bash
curl http://127.0.0.1:$PORT/health           # → ok
curl http://127.0.0.1:$PORT/__computerd/info # → {backend, mountPoint, port}
curl http://127.0.0.1:$PORT/__computerd/stats # → 行数 / RSS / heap
```

---

## 6.3 同步期错误(WS 断、stub 泄漏、watermark 不一致)

| 现象 | 触发条件 | 处理方法 |
|---|---|---|
| `/__computerd/stubs` 返回 `stub tracking disabled (set CAPNWEB_TRACK_STUBS=1)` | 没开启 stub 跟踪 | `export CAPNWEB_TRACK_STUBS=1` 后重启 |
| 远端 stub 数持续上涨 | 没用 `using` 释放 `getWorkspace(...)` 或 `exec(...)` 返回的句柄 | 所有句柄用 `using` 包裹,`finally` 里 `[Symbol.dispose]()` |
| `upstream /health unreachable: ...` | `POST /connect` 默认 30s 健康探测超时 | 显式设 `healthTimeoutMs`;确认 `computer.internal` 路由活着 |
| container 重启后 push/pull 偶发失败 | `_vfs_watermark.pushRev` 与对端不一致 | 触发 `reconcileWatermarks`(`packages/rpc/src/sync-driver.ts:396`)|
| PR/Worker 报 `RPC stub not found` | 远端进程已被销毁,但本地 stub 还活着 | 检查是否调用了 `ws[Symbol.dispose]()` |
| 长任务卡住不输出 | `transformStream` 没 flush,或浏览器禁用 `x-accel-buffering` | 显式 `controller.enqueue(...)`;SSE header 加 `x-accel-buffering: no` |

---

## 6.4 写入期错误(VFS / chunk / sha256)

| 现象 / 关键句 | 触发条件 | 处理方法 |
|---|---|---|
| `ENOENT` | 文件或目录不存在 | 先 `mkdir -p` 父目录 |
| `EISDIR` | 对目录调用 `readFile` | 改用 `readdir` / `ls` |
| `EEXIST` | `mkdir` 时目录已存在 | 用 `recursive: true`,或先检查 |
| `ENOTEMPTY` | `rm` 时目录非空 | 用 `recursive: true`,或先清空 |
| `ELOOP` | 符号链接环(超过 40 跳) | 检查 symlink |
| `EIO` | SQLite 写失败(磁盘满 / 事务冲突) | 看 `/__computerd/stats` 的 RSS / heap |
| chunk 引用计数错(staged vs linked) | 见最近提交 `8758b51 dofs: Guard the staged-chunk link path` | 升级到包含 `8758b51` 之后;触发 `_vfs_changes` 重建 manifest |

写入错误码的完整定义在 `packages/dofs/src/errors.ts`(`createWorkspaceError(code, message, path)`),见 [第 22 章](22_ref_errors.md)。

---

## 6.5 执行期错误(`runtime.exec` 失败)

| 现象 | 触发条件 | 处理方法 |
|---|---|---|
| `EEXEC_BUSY` | 同一个 exec id 已存在,旧 handle 未释放 | 检查是否漏 `using` / `[Symbol.dispose]()` |
| `ELOG_TRUNCATED` | exec log buffer 满了(`EXEC_LOG_MAX_BYTES`) | 调大 `EXEC_LOG_MAX_BYTES`;或用流式消费 |
| `ESHUTDOWN` | 对端进程已关闭,本次调用晚到 | 重连:重新构造 Workspace stub |
| `EAUTH` | 协议层鉴权失败(*未在代码中确认,需读 X 后填入*) | 检查 access token / 路由 ACL |
| `EPROTOCOL` | wire 帧不符合 `WorkspaceRPC` | 确认客户端 / 服务端版本一致 |
| 进程退出码非 0 | 真实命令失败 | `await result()` 看 `exitCode` / `stderr` |
| `exitCode = 137` | `SIGKILL`(超时) | 调大 `timeoutMs` 或拆短任务 |

`packages/computerd/src/exec/types.ts:71` 定义了 `ExecErrorCode = "EEXEC_BUSY" | "ENOENT" | "ELOG_TRUNCATED"`。

---

## 6.6 构建 / 发布期错误

| 现象 | 触发条件 | 处理方法 |
|---|---|---|
| `npm run build` 失败 | 缺 TS 类型,或某个子包未构建 | 先 `npm run build`,再 `npm test` |
| CI 报 `biome check` 失败 | 格式 / lint 不合规 | `npm run check:fix` |
| CI 报 `sherif` 版本错位 | 跨 workspace 版本不对齐 | `npm run check:fix` 后重提 |
| PR 被自动关闭 | 仓库不接 unsolicited PRs(只放行 OWNER/MEMBER/COLLABORATOR 或打了 `allow-pr` label) | 走 issue / discussions |
| Docker 镜像 push 失败 | 缺 `libfuse2t64 fuse3` | 在构建主机上装包(参考 `release.yml`、`main-computerd-image.yml`) |
| `libfuse.so.2: cannot open shared object file` | release runner 缺系统依赖 | 装 `libfuse2t64 fuse3` 后重跑 |

---

## 6.7 性能瓶颈初判

```bash
# 1) 看看 DOFS 表行数 + RSS + heap 是否爆炸
curl http://127.0.0.1:$PORT/__computerd/stats

# 2) 看是不是 chunk 引用计数异常(staged vs linked)
curl http://127.0.0.1:$PORT/__computerd/stats | jq .orphan_blobs
# 持续上涨 → staged-chunk 没正常 link(参考 8758b51)

# 3) baseline 对比
bash script/run-fs-bench.sh
# 元数据密集型应接近 ext4;大块顺序 I/O 会慢 30x+

# 4) npm install 对比
bash script/run-npm-bench.sh
# 标准 npm install 应在 disk ~2x / tmpfs ~3.6x 范围内
```

---

## 6.8 该看哪些日志?

| 日志 | 含义 |
|---|---|
| `LOG_FILE`(`computerd` env) | `computerd` 主进程日志 + 崩溃处理 |
| `script/computerd-soak.mjs` | 双 peer-to-peer 长跑一致性 |
| `script/computerd-stub-soak.mjs` | 长 WS,查 stub 泄漏 |
| `script/computerd-fuse-flush.mjs` | 验证 FUSE 写缓存是否进 VFS |
| `script/fs-bench.sh` / `run-fs-bench.sh` | 元数据密集型 vs 顺序 I/O |
| `script/run-npm-bench.sh` | 完整 npm install 对比 |
| `examples/*/README.md` 中 `observability.traces.enabled = true` | Cloudflare Traces dashboard 上的 span:`workspace.connect`、`workspace.sync.push/pull`、`workspace.runtime.exec.spawn`、`workspace.fs.*` |

---

## 6.9 升级到包含 `8758b51` 之后

最近一次提交 `dofs: Guard the staged-chunk link path` 修了一个 VFS 守卫问题 —— 当同步期间出现 staged-chunk 引用但未 link 时,VFS 可能会引用不存在的 manifest。升级到 `8758b51` 或之后:

- 重新跑一次 `npm install`(避免 arm64 libfuse 漂移);
- 跑 `npm run build` 后 `npm test`;
- 启动 `computerd` 时观察 `/__computerd/stats` 中 `orphan_blobs` 计数应下降为 0。

---

## 延伸阅读

- [第 22 章:错误码与异常](22_ref_errors.md) — 错误码表 + throw 路径
- [第 8 章:VFS 深入](08_dev_vfs.md) — staged-chunk 与 link 的开发者细节
- [第 11 章:测试与调试](11_dev_testing.md) — TestBackend + Vitest 调试
- [`packages/dofs/src/errors.ts`](../../packages/dofs/src/errors.ts) — POSIX 错误工厂
- [`packages/computerd/src/exec/types.ts`](../../packages/computerd/src/exec/types.ts) — ExecErrorCode
- [`docs/07_injected_service.md`](../07_injected_service.md) — 既有专题:注入服务规范