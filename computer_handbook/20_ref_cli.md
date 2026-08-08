# 20. `computerd` CLI 参考

> **读者**:用户 / 开发者
> **预计阅读**:5 分钟
> **前置依赖**:[第 2 章 五分钟跑通](02_quickstart.md)

## 目标

把 `computerd` 守护进程的所有 env vars / HTTP 端点 / SEA 构建流程汇总成一页参考。

> ⚠ `computerd` **没有传统 argparse 子命令**——它的所有"命令选项"都是环境变量。

---

## 20.1 启动方式

```bash
# 1. 通过 npx
npx -p @cloudflare/computerd computerd

# 2. 自己构建
npm run build:bin --workspace=@cloudflare/computerd
./artifacts/computerd/computerd-linux-x64

# 3. 通过 Docker 镜像
docker run --rm -p 45678:45678 \
  -e PORT=45678 \
  ghcr.io/cloudflare/computer-computerd-linux-x64:main
```

入口:`packages/computerd/src/cli/computerd.ts:448-628` 的 `main()`。

---

## 20.2 环境变量全集

| 变量 | 默认 | 必填? | 解析 | 说明 |
|---|---|---|---|---|
| `PORT` | `45678` | 否 | `parsePort` | HTTP 监听端口,必须 `0-65535` 整数 |
| `MOUNT_POINT` | `/workspace` | 否 | `parseMountPoint` | FUSE 挂载点,必须**绝对路径** |
| `FUSE_MOUNT` | `auto` | 否 | `parseFuseMountMode` | `auto` / `fuse` / `macfuse` / `shim` / `none` |
| `UPSTREAM_URL` | (空) | 否 | — | ws(s)/http(s) URL;启动时打开 `SyncClient` 跑 sync loop |
| `EXEC_LOG_MAX_BYTES` | runner 默认 | 否 | — | in-memory exec log buffer 上限,**正整数** |
| `LOG_FILE` | (空) | 否 | `installLogging` | 设了就装日志写入 + 崩溃处理 |
| `CAPNWEB_TRACK_STUBS` | `0` | 否 | — | 打开后 `/__computerd/stubs` 才返回 stub 快照 |

### 已废弃(出现即拒绝启动)

| 已废弃 env | 替代 |
|---|---|
| `DISABLE_FUSE` | `FUSE_MOUNT=none` |
| `FUSE_SHIM` | `FUSE_MOUNT=shim` |
| `WSD_FUSE_BACKEND` | `FUSE_MOUNT=fuse` / `macfuse` |

兜底:`rejectLegacyFuseEnv`(`packages/computerd/src/cli/computerd.ts`)。

---

## 20.3 HTTP 端点全集

| 方法 + 路径 | 行为 | 备注 |
|---|---|---|
| `POST /api` | capnweb HTTP-batch RPC | — |
| `POST /connect` | body `{ url, healthTimeoutMs? }`;`computerd` 反向拨回 `url` 并打开 WS session | **同一时间只挂一个 outbound session** |
| `GET /ws`(Upgrade) | 长连 WS,capnweb 会话,容器主同步通道 | `noServer: true, perMessageDeflate: true` |
| `GET /health` | `200 OK` + `ok\n` | FUSE 是否 ready 不影响 |
| `GET /__computerd/info` | JSON `{ backend, mountPoint, port }` | — |
| `GET /__computerd/stats` | JSON:DOFS 表行计数 + blob 总字节 + orphan blob 计数 + RSS/heap/external/arrayBuffers | — |
| `GET /__computerd/stubs` | JSON,**需 `CAPNWEB_TRACK_STUBS=1`** | stub 跟踪 |
| `GET /` | `200 OK` + `{}` | — |
| 其它 | `404 not found\n` / `405 method not allowed\n` | — |

---

## 20.4 自检命令

```bash
curl http://127.0.0.1:$PORT/health
curl http://127.0.0.1:$PORT/__computerd/info
curl http://127.0.0.1:$PORT/__computerd/stats | jq

# 启用 stub 跟踪
export CAPNWEB_TRACK_STUBS=1
# 重启后:
curl http://127.0.0.1:$PORT/__computerd/stubs | jq
```

---

## 20.5 SEA 单文件二进制构建

`packages/computerd/scripts/build-bin.mjs:64-135`(`main()` + `buildTarget()`):

```bash
# 单平台
npm run build:bin --workspace=@cloudflare/computerd

# 多平台 / 全部
node packages/computerd/scripts/build-bin.mjs \
  --targets linux-x64,linux-arm64,macos-x64 \
  --output artifacts/computerd
```

构建产物路径(示例):`artifacts/computerd/computerd-linux-x64`。

**构建管线**(`packages/computerd/scripts/`):

1. `build.mjs` —— `tsc` → `dist/cli/computerd.cjs`;
2. `build-bin.mjs` —— esbuild bundle + postject 注入 NODE_SEA_BLOB;
3. `sea/bundle.mjs` —— esbuild metafile + bundleComputerd;
4. `sea/bootstrap.cjs` —— Node SEA bootstrap。

**发布**:changesets release 路径推 `ghcr.io/cloudflare/computer-computerd-linux-x64:<version>` 与 `registry.cloudflare.com`。

---

## 20.6 故障排查速查

| 现象 | 修法 |
|---|---|
| `fuse-native` 编译失败 | `apt-get install build-essential libfuse-dev`,或 `npm install --ignore-scripts` |
| `file in wrong format` link 错(arm64) | 替换 aarch64 libfuse + `npx node-gyp rebuild` |
| `PORT must be an integer between 0 and 65535` | 改成合法整数 |
| `MOUNT_POINT must be an absolute path` | 用绝对路径 |
| `EXEC_LOG_MAX_BYTES must be a positive integer` | 改成正整数 |
| `DISABLE_FUSE is no longer supported; use FUSE_MOUNT=none instead` | 改用 `FUSE_MOUNT=none` |
| `/__computerd/stubs` 返回 404 | `export CAPNWEB_TRACK_STUBS=1` 后重启 |
| `upstream /health unreachable` | 显式设 `healthTimeoutMs`;确认 `computer.internal` 路由活着 |
| Docker 镜像 push 失败 | 装 `libfuse2t64 fuse3` 后重跑 |

详见 [第 6 章](06_user_troubleshooting.md) 和 [第 22 章](22_ref_errors.md)。

---

## 20.7 监控指标(`/__computerd/stats` JSON 形状)

```ts
{
  dofs: {
    vfs_nodes: number,
    vfs_changes: number,
    vfs_blobs: number,
    vfs_chunks: number,
    vfs_manifests: number,
    blob_bytes: number,
    orphan_blobs: number,  // GC 落后信号
  },
  memory: {
    rss: number,
    heapUsed: number,
    external: number,
    arrayBuffers: number,
  }
}
```

---

## 延伸阅读

- [第 2 章:五分钟跑通](02_quickstart.md) — 启动步骤
- [第 3 章:安装、配置](03_user_install.md) — env 变量概览
- [第 6 章:常见错误与排查](06_user_troubleshooting.md)
- [第 21 章:配置参考](21_ref_config.md) — wrangler / env 全集
- [`packages/computerd/README.md`](../../packages/computerd/README.md)
- [`packages/computerd/src/cli/computerd.ts`](../../packages/computerd/src/cli/computerd.ts)