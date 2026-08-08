# 2. 五分钟跑通最小回路

> **读者**:用户 / 开发者
> **预计阅读**:5 分钟
> **前置依赖**:Node 22+,一个 Cloudflare 账号(若要部署到 Workers),可选 Docker(若要跑 Container backend)

## 目标

不读所有源码、不学所有概念,在本机启动 `computerd` 守护进程并通过 HTTP 完成一次"写文件 → 读文件 → 执行命令"的最短回路。

> 本章只展示**本地 dev** 形态。三种部署形态(本地 / Cloudflare Workers / 混合)的决策见 [第 3 章](03_user_install.md)。

---

## 2.1 准备环境

| 工具 | 版本要求 | 说明 |
|---|---|---|
| Node.js | ≥ 22 | `computerd` 在 `package.json:engines.node` 明确声明 |
| npm | 任意 | 仓库用 npm workspaces,**不接受** pnpm / yarn |
| Docker | 可选 | 仅 Container backend 与真实 FUSE 测试需要 |
| macFUSE | macOS 上跑 `computerd` 真实 FUSE 时需要 | Linux 上对应 `libfuse-dev` |

Linux arm64 用户额外注意(`AGENTS.md` 强调):

```bash
# 1) 缺 build toolchain
apt-get install build-essential libfuse-dev

# 2) 想跳过 native build
npm install --ignore-scripts

# 3) Linux arm64 host 替换 fuse-native 内置的 libfuse
cp /usr/lib/aarch64-linux-gnu/libfuse.so.2 \
   node_modules/fuse-shared-library-linux/libfuse/lib/libfuse.so
cd node_modules/fuse-native && npx node-gyp rebuild
```

---

## 2.2 克隆与安装

```bash
git clone https://github.com/cloudflare/computer.git
cd computer
npm install
```

> ⚠ 整个 monorepo **只 install 一次**;不要在子包内单独 `npm install`,会生成嵌套 lockfile。

---

## 2.3 启动 `computerd`

`computerd` 没有传统 CLI flags,所有配置都是**环境变量**(详见 [`packages/computerd/README.md`](../../packages/computerd/README.md))。

```bash
PORT=45678 \
MOUNT_POINT=/workspace \
FUSE_MOUNT=auto \
LOG_FILE=/tmp/computerd.log \
npx -p @cloudflare/computerd computerd
```

合法 `FUSE_MOUNT` 值(`packages/computerd/src/cli/computerd.ts:448-528` + `packages/computerd/src/fuse/options.ts`):

- `auto`(默认):有 `/dev/fuse` 就用 FUSE,否则回退到 shim
- `fuse`:强制使用真 FUSE
- `macfuse`:macOS 上强制 macFUSE
- `shim`:永远用用户态 shim(无 kernel mount)
- `none`:不挂载任何东西,只暴露 HTTP / WebSocket

> ⚠ 已废弃的环境变量(`DISABLE_FUSE` / `FUSE_SHIM` / `WSD_FUSE_BACKEND`)出现即拒绝启动并提示替代值。

---

## 2.4 自检三连

```bash
# 健康检查
curl http://127.0.0.1:45678/health
# → ok

# 进程信息
curl http://127.0.0.1:45678/__computerd/info
# → {"backend":"fuse","mountPoint":"/workspace","port":45678}

# 运行时统计
curl http://127.0.0.1:45678/__computerd/stats
# → DOFS 表行数、blob 总字节、RSS / heapUsed / external
```

---

## 2.5 最小 HTTP 回路

直接对 `computerd` 发 HTTP batch RPC 太底层。最简办法是跑一个 examples,然后用 curl 触发它:

```bash
# 终端 A:启动 examples/container 的 Worker
cd examples/container
npm install
npx wrangler dev --local --persist-to .wrangler
# → http://127.0.0.1:8787

# 终端 B:写文件
echo 'hello' | curl -X PUT --data-binary @- \
  http://127.0.0.1:8787/c/demo/file/workspace/hello.txt

# 读回来
curl http://127.0.0.1:8787/c/demo/file/workspace/hello.txt
# → hello

# 执行命令
curl -X POST http://127.0.0.1:8787/c/demo/exec \
  -H 'content-type: application/json' \
  -d '{"command":"cat /workspace/hello.txt && uname -a","encoding":"utf8"}'
```

这套路径基于 `examples/container/src/index.ts:50-97` 的 `ContainerExample` DO,具体 fetch 路由由 backend 的 `handleFetch(request)` 暴露。

---

## 2.6 Hello World:在不启动 Container 的情况下

只想跑通核心抽象,不需要 Container?直接用 `Workspace` + `TestBackend`:

```ts
import { Workspace, TestBackend } from "@cloudflare/computer";

const ws = new Workspace({
  storage /* DO 的 ctx.storage 或 Testing 提供的 SQLiteTestStorage */,
  backends: [new TestBackend({ id: "test" })],
});

await ws.fs.writeFile("/notes.md", "- [ ] ship it\n");
console.log(await ws.fs.readFile("/notes.md", "utf8"));
// → - [ ] ship it

await ws.runtime.exec("cat /notes.md", { backend: "test", encoding: "utf8" });
```

`TestBackend` (`packages/computer/src/backends/test.ts`) 是无副作用、纯内存的假后端,适合 vitest 与本地 dev loop。

---

## 2.7 出错怎么办?

快速对照表:

| 现象 | 最可能原因 | 修法 |
|---|---|---|
| `fuse-native` 编译失败 | 缺 build toolchain | `apt-get install build-essential libfuse-dev`,或 `npm install --ignore-scripts` |
| `file in wrong format` link 错 | Linux arm64 host 用了 x86 预编译 libfuse | 按 §2.1 步骤替换 aarch64 libfuse |
| `DISABLE_FUSE is no longer supported; use FUSE_MOUNT=none instead` | 用了已废弃 env | 改用 `FUSE_MOUNT` 取值 |
| `PORT must be an integer between 0 and 65535` | `PORT` 不是合法整数 | 改成合法整数 |
| `/__computerd/stubs` 返回 404 | 没开启 stub 跟踪 | `export CAPNWEB_TRACK_STUBS=1` |
| PR 被自动关闭 | 仓库不接 unsolicited PRs | 走 issue / discussions |

完整故障排查见 [第 6 章](06_user_troubleshooting.md) 和 [第 22 章](22_ref_errors.md)。

---

## 延伸阅读

- [第 3 章:安装、配置、4 选 1 后端决策](03_user_install.md) — 三种部署形态 + 决策树
- [第 4 章:基础操作:创建、读写、执行](04_user_basics.md) — `Workspace` 构造与 `fs.*` / `runtime.exec` 详细说明
- [`docs/07_injected_service.md`](../07_injected_service.md) — 既有专题:`computerd` 注入服务规范
- [`packages/computerd/README.md`](../../packages/computerd/README.md) — `computerd` 完整 README