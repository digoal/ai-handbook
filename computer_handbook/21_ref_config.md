# 21. 配置参考

> **读者**:用户 / 开发者
> **预计阅读**:5 分钟
> **前置依赖**:[第 3 章 安装配置](03_user_install.md)

## 目标

把所有可配置项(wrangler 字段、`computerd` env vars、workspace 构造参数)集中在一页。

---

## 21.1 `wrangler.jsonc` 关键字段

### 顶层

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | string | Worker 名 |
| `main` | string | Worker 入口,默认 `src/index.ts` |
| `compatibility_date` | string | Cloudflare 平台 compatibility date |
| `compatibility_flags` | string[] | `["nodejs_compat", "experimental"]` |
| `observability.traces.enabled` | boolean | 接 Cloudflare Traces(`@cloudflare/computer/observe/cloudflare`) |

### Containers

```jsonc
"containers": [{
  "class_name": "ContainerExample",
  "image": "./Dockerfile",
  "instance_type": "standard-2",
  "max_instances": 5
}]
```

| 字段 | 说明 |
|---|---|
| `class_name` | 对应 DO class 名(`durable_objects.bindings[].class_name`) |
| `image` | `"<ghcr.io/...:tag>"` 或 `"./Dockerfile"`(本地构建) |
| `instance_type` | `"standard-1"` / `"standard-2"` / `"standard-3"` 等 |
| `max_instances` | 单 DO 的 Container 最大并发数 |

### Durable Objects

```jsonc
"durable_objects": {
  "bindings": [{ "name": "CONTAINER_EXAMPLE", "class_name": "ContainerExample" }]
}
```

### Migrations

```jsonc
"migrations": [{ "tag": "v1", "new_sqlite_classes": ["ContainerExample"] }]
```

`new_sqlite_classes` 启用 DO SQLite。

### R2 buckets

```jsonc
"r2_buckets": [{ "binding": "Bucket", "bucket_name": "computer-container-hello" }]
```

R2 可挂载为只读 mount(`/workspace/r2`,通过 `Workspace.mounts` 选项)。

### Worker loaders

```jsonc
"worker_loaders": [...]
```

`env.LOADER` 用于 `WorkerShellBackend` / `WorkerJavaScriptBackend` 在 Dynamic Worker 里跑 shell / JS。

---

## 21.2 `computerd` 环境变量

详见 [第 20 章](20_ref_cli.md#202-环境变量全集)。

---

## 21.3 `Workspace` 构造参数

```ts
new Workspace({
  storage,               // 必需:DO 的 ctx.storage,或 Testing 的 SQLiteTestStorage
  mounts?,               // R2 等挂载
  backends,              // 1 个或多个 WorkspaceBackend
  git?,                  // createGitClient()(默认 isomorphic-git)
  assets?,               // createAssets()(R2 presigned URL)
  artifacts?,            // createArtifact()(Cloudflare Artifacts binding)
  defaultGitIdentity?,   // { name, email }
  observer?,             // noopObserver | createCloudflareObserver({ tracing })
  useThink?,             // (未在代码中确认)
});
```

`packages/computer/src/workspace.ts:179ish` 是 `WorkspaceOptions` 的定义位置。

### Mount 形态

```ts
mounts: {
  "/workspace/r2": R2Bucket(env.Bucket),
}
```

`R2Bucket` / `R2BucketBinding` / `R2BucketOptions` 见 [第 19 章](19_ref_api.md#19-mount)。

### Backend 形态

```ts
backends: [
  new CloudflareContainerBackend({
    id: "container",
    container: () => this,
    workspace: { binding: "ContainerExample", id: this.ctx.id.toString() },
  }),
  new WorkerShellBackend({
    id: "shell",
    loader: env.LOADER,
    commands: [
      import("@cloudflare/computer/shell/core"),
      import("@cloudflare/computer/shell/curl"),
    ],
  }),
  new WorkerJavaScriptBackend({
    id: "worker-javascript",
    loader: env.LOADER,
  }),
  new TestBackend({ id: "test" }),
],
```

---

## 21.4 `wrangler.jsonc` 完整示例(`examples/container`)

```jsonc
{
  "name": "computer-container-example",
  "main": "src/index.ts",
  "compatibility_date": "2025-04-01",
  "compatibility_flags": ["nodejs_compat", "experimental"],
  "containers": [{
    "class_name": "ContainerExample",
    "image": "./Dockerfile",
    "instance_type": "standard-2",
    "max_instances": 5
  }],
  "durable_objects": {
    "bindings": [{ "name": "CONTAINER_EXAMPLE", "class_name": "ContainerExample" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["ContainerExample"] }],
  "r2_buckets": [{ "binding": "Bucket", "bucket_name": "computer-container-hello" }],
  "observability": { "traces": { "enabled": true } }
}
```

---

## 21.5 `.dev.vars` (本地 secrets)

`wrangler dev` 会从 `.dev.vars` 读 secrets(env vars),本地不 commit(`packages/computerd/.gitignore` 排除,根目录也排除)。

```bash
# .dev.vars(示例)
CUSTOM_TOKEN=xxxx
LOG_FILE=/tmp/dev.log
```

---

## 21.6 Biome 配置(`biome.jsonc`)

| 字段 | 值 |
|---|---|
| `indentStyle` | `space` |
| `indentWidth` | `2` |
| `lineWidth` | `100` |
| 适用文件 | `**/*.ts` `tsx` `js` `mjs` `cjs` `json` `jsonc` |
| 排除 | `node_modules` / `dist` / `artifacts` / `.venv` / `.devbox` / `package-lock.json` / `worker-configuration.d.ts` |
| 引号 | `"double"` |
| trailing commas | `"all"` |
| 分号 | `"always"` |

`packages/computer-computerd-linux-x64/Dockerfile` 在 changesets release 时通过 `.github/changeset-version.mjs` 改写 `:0.1.1` 版本标签(例)。

---

## 21.7 changesets 配置(`.changeset/config.json`)

```json
{
  "changelog": "@changesets/changelog-github",
  "privatePackages": {
    "version": true,
    "tag": false
  }
}
```

含义:

- `privatePackages.version = true`:私有包也产生版本号 + CHANGELOG;
- `privatePackages.tag = false`:私有包**不**发布到 npm。

---

## 21.8 CI 配置(`.github/workflows/`)

| Workflow | 触发 | 内容 |
|---|---|---|
| `ci.yml` | PR push to main / next | 包矩阵 + example 矩阵 + preview;`libfuse2t64 fuse3` install;`biome check` + `tsc --noEmit` + `vitest run` |
| `release.yml` | CI(main, completed) | changesets-driven 版本 / 发布;publish `computerd` 镜像到 `ghcr.io` 与 `registry.cloudflare.com` |
| `main-computerd-image.yml` | CI(main, completed) | 推 `ghcr.io/cloudflare/computer-computerd-linux-x64:main` |
| `close-unrequested-prs.yml` | `pull_request_target [opened, reopened]` | 关闭非授权 PR |

---

## 21.9 `.gitignore`(顶层,摘)

| 排除项 | 说明 |
|---|---|
| `dist/` | 构建产物 |
| `artifacts/` | SEA 二进制输出 |
| `generated/` | 自动生成 |
| `.dev.vars` | wrangler dev 本地 secrets |
| `worker-configuration.d.ts` | wrangler 生成 |
| `node_modules/` | — |
| `.codegraph/` | 本地 CodeGraph 索引(可选) |

---

## 延伸阅读

- [第 3 章:安装、配置](03_user_install.md)
- [第 20 章:`computerd` CLI 参考](20_ref_cli.md)
- [`examples/container/wrangler.jsonc`](../../examples/container/wrangler.jsonc)
- [`packages/computer/src/workspace.ts`](../../packages/computer/src/workspace.ts)
- [`biome.jsonc`](../../biome.jsonc)
- [`.changeset/config.json`](../../.changeset/config.json)
- [`.github/workflows/`](../../.github/workflows/)