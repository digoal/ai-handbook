# 16. 安全与隔离

> **读者**:架构师
> **预计阅读**:6 分钟
> **前置依赖**:[第 12 章 系统架构总览](12_arch_overview.md)

## 目标

讲清楚 trust boundaries(信任边界)、当前已实现的隔离机制、以及**协议层 auth 尚未在代码中确认**——这一节会显式标注。

---

## 16.1 F17. 信任边界图

**F17. 信任边界图** — 谁信任谁,边界在哪

```mermaid
flowchart TB
  subgraph TRUST1["信任域 1:Public Internet"]
    U["最终用户 / Browser"]
    API["Client API"]
  end

  subgraph TRUST2["信任域 2:Cloudflare Edge"]
    W["Worker"]
    DO["Durable Object<br/>+ SQLite"]
  end

  subgraph TRUST3["信任域 3:Cloudflare Container"]
    CD["computerd"]
    C["bash / npm / 用户态进程"]
  end

  U -->|"HTTPS<br/>(DO URL / worker URL)"| W
  W -->|"Workers RPC<br/>(同一 Cloudflare 账户内)"| DO
  DO -->|"capnweb WS<br/>(egress-interceptor 路由)"| CD
  CD -->|"spawn child<br/>(/workspace FUSE)| C

  classDef t1 fill:#ffe2e2,stroke:#b83b3b,color:#3d1414
  classDef t2 fill:#dbe9ff,stroke:#3b6db8,color:#1a2c4e
  classDef t3 fill:#dff5d8,stroke:#3b8a3a,color:#1a3d18
```

### 三层信任域

| 域 | 谁可以进入 | 谁可以出 |
|---|---|---|
| Public Internet | 任何 | HTTPS to Cloudflare |
| Cloudflare Edge | Workers / DO / Container(同一账户) | egress interceptor route |
| Cloudflare Container | 仅 DO 通过 reverse-dial 接入(`POST /connect`) | spawn child / FUSE |

---

## 16.2 已实现的隔离机制

### 16.2.1 路径限制 —— `WorkspaceScopedFS`

`packages/computer/src/runtime/capability.ts:1` 是**所有模块后端 FS 调用的唯一入口**:

- **路径限制**:`workspace.fs.readFile("/foo")` 自动 strip 到 workspace 根;
- **读 / 写权限**:可声明 `readOnly: true`;
- **字节 / 目录条目限额**:防止模块后端单次读过大文件;
- **`exists` swallow `ENOENT`**(`capability.ts:79-86`):统一的 not-found 语义。

**关键不变性**:`WorkerJavaScriptBackend` 跑的 ES module **无法**绕开 `WorkspaceScopedFS`,因为 `node:fs/promises` 在 module backend 中被 patched 指向 `WorkspaceScopedFS`(详见 `module-graph.ts`)。

### 16.2.2 Container 实例隔离

`CloudflareContainerBackend`(`packages/computer/src/backends/container/cloudflare-container.ts:141`)每个 workspace 实例化一个独立 Container instance:

- `container.start()` + `restartAttempts` 重启;
- `instance_type: "standard-2"`(可在 `wrangler.jsonc` 配置);
- `max_instances: 5`(可在 `wrangler.jsonc` 配置)。

> ⚠ Container 是 **per-DO** 的:1 个 DO 持有 1 个 Container 实例。**没有**跨 workspace 共享 Container。

### 16.2.3 FUSE 权限

`computerd` 的 FUSE mount 受 Linux DAC 控制 —— `MOUNT_POINT` 必须是绝对路径,挂载权限由运行 `computerd` 的 user 决定(默认 root / privileged container)。

### 16.2.4 Stub disposal 防资源耗尽

capnweb export table 是有限资源(见 [第 10 章](10_dev_client.md#106-stub-disposal-contract必读))。`using` 强制释放防止恶意 / bug 代码耗尽 export table。

### 16.2.5 R2 Mount 是只读

`packages/computer/src/mounts/` 实现了 R2 只读挂载(`/workspace/r2` 等),写入不会回写到 R2。

---

## 16.3 协议层 auth —— **未在代码中确认**

> ⚠ **重要**:`packages/rpc/src/interface.ts:158` 的 `WireErrorCode` 包含 `"EAUTH"`,但**实际触发 EAUTH 的代码路径**在仓库中**未在代码中确认**。

可能性:

- 由 Cloudflare 平台层(Egress / DO RPC)在 egress interceptor 处强制;
- 由 Container 平台在 `POST /connect` 时强制;
- 由未来的 wire 升级添加。

**架构师行动项**:在升级到 PRODUCTION 之前,**必须**确认 EAUTH 触发路径并补全文档;当前 PREVIEW 阶段假定信任由 Cloudflare 平台保证。

---

## 16.4 资源限制

| 资源 | 限制方式 | 配置位置 |
|---|---|---|
| DO 内存 / 存储 | Cloudflare 平台限制(默认 ~10 GB) | Cloudflare 控制台 |
| Container runtime | `instance_type` | `wrangler.jsonc:containers.instance_type` |
| Container 数量 | `max_instances` | `wrangler.jsonc:containers.max_instances` |
| Exec log buffer | `EXEC_LOG_MAX_BYTES` | `computerd` env |
| Module backend FS 大小 | `WorkspaceScopedFS` 限额 | `WorkspaceOptions.mounts` 配置 |
| Stub 数量 | capnweb export table 上限(平台决定) | 走 `using` 正确释放 |

---

## 16.5 已知安全考量

1. **`WSD_FUSE_BACKEND` 等已废弃 env 拒绝启动**(防止历史漏洞回潮);
2. **`PORT` 必须合法整数**:防止端口扫描 / 提权;
3. **`MOUNT_POINT` 必须绝对路径**:防止相对路径逃逸;
4. **Symbol disposal 强制**:防止 export table 耗尽(DoS 自身);
5. **git operation 的 staged vs linked 守卫**(`8758b51`):防止"manifest 引用不存在 blob"导致的不一致,也是防止"读不到的隐藏文件"边界。

---

## 16.6 未来工作(*未在代码中确认,以下为架构师视角下的"应该考虑"*)

下列是架构师在评审生产化方案时应该要求的:

1. **EAUTH 触发路径的明确文档** —— 当前 PREVIEW 没有 wire-layer auth;
2. **资源限额在多租户下的公平性** —— DO 是 per-tenant 隔离的,但 Container 是 per-workspace;
3. **exec 用户的隔离** —— 当前 Container 是单一 user 运行,未来若多用户需要 user namespace;
4. **审计日志** —— `WorkspaceObserver` 已经接 tracing,但**审计**(谁在什么时间访问了什么路径)目前**未在代码中确认**;
5. **密钥管理** —— 如果未来加 `assets.publish` + SigV4 signing,密钥管理在哪;
6. **wire 升级的回滚路径** —— 当前没有"老 client 不更新会怎样"的策略,只有"wire 错误"的兜底。

---

## 16.7 安全报告

仓库不接 unsolicited PR(见 `CONTRIBUTING.md`),但**安全漏洞报告走** [`cloudflare.com/.well-known/security.txt`](https://www.cloudflare.com/.well-known/security.txt)(参见 `.github/SECURITY.md`),**不走** 公开 issue。

---

## 延伸阅读

- [第 6 章:常见错误与排查](06_user_troubleshooting.md) — 用户视角故障排查
- [第 10 章:客户端与 SDK](10_dev_client.md) — stub 生命周期
- [第 14 章:capnweb 协议](14_arch_protocol.md) — `EAUTH` 在 wire 层的位置
- [第 17 章:性能、成本、扩展性](17_arch_performance.md) — 资源限额与成本
- [第 18 章:演进路线与未决问题](18_arch_roadmap.md) — auth 的未来演进
- [`docs/11_lifecycle.md`](../11_lifecycle.md) — 既有专题:hibernation
- [`.github/SECURITY.md`](../../.github/SECURITY.md) — 安全报告通道