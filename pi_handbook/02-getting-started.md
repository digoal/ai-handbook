# 02 · 开发者上手

> 本文面向**已经在仓库工作、要运行、改、调试 pi 的开发者**。命令以仓库根为起点。

## 2.1 安装与构建

```bash
# 1) 安装（跳过 lifecycle 脚本——AGENTS.md 强制）
npm install --ignore-scripts

# 2) 完整构建（含模型目录刷新，需联网）
npm run build

# 2') 离线构建（用缓存的 `models.generated.ts` 与 data/*.json）
npm run build:offline

# 3) 校验：biome + pinned-deps + ts-imports + shrinkwrap + tsgo + browser-smoke
npm run check
```

构建顺序是硬约束，按 `packages` 之间的依赖图排序：`tui → telemetry → ai → agent → session-backends/sqlite-node → protocol → client → server → coding-agent`。根 `package.json` 以链式 `cd && npm run build` 显式编排。**不要并行构建**，否则会引用尚未生成的类型。

## 2.2 从源码运行 pi

```bash
# 直接跑源码（不构建）
./pi-test.sh

# 不带任何 API key 启动（本地烟雾测试、模型选择器仍可用）
./pi-test.sh --no-env
```

`pi-test.sh` 内部做几件事：unset 大部分云凭据；按需 `--no-env`/`--offline`/`--verbose`；支持 Node 与 Bun 两种执行形态；把 `packages/*/dist` 切换到 `packages/*/src`。

## 2.3 测试

`npm test` 是 vitest 入口，但它**包含 e2e 测试**，仅在 API key/endpoint 存在时启用——不要直接跑。

```bash
# 默认路径：在隔离 HOME 中跑非 e2e 测试
./test.sh

# 单文件：在包根目录下
node "$(git rev-parse --show-toplevel)/node_modules/vitest/dist/cli.js" --run test/specific.test.ts

# packages/tui 用 node:test
node --test test/specific.test.ts

# coding-agent/test/suite/ — 用 test/suite/harness.ts + faux provider
# 不能用真实 provider API、真实 API key、网络调用、付费 token
# 回归测试放 test/suite/regressions/<issue-number>-<short-slug>.test.ts
```

`test.sh` 内部建立临时 `HOME/TMPDIR/NPM_CONFIG_USERCONFIG`，并 unset 大部分云凭据，保证可重复且不污染用户目录。

## 2.4 交互式 TUI 烟雾测试

驱动 TUI 用 tmux：

```bash
tmux new-session -d -s pi-test -x 80 -y 24
tmux send-keys -t pi-test "./pi-test.sh" Enter
sleep 3 && tmux capture-pane -t pi-test -p     # 启动后截图
tmux send-keys -t pi-test "your prompt here" Enter
tmux send-keys -t pi-test Escape               # 特殊键
tmux kill-session -t pi-test
```

用户视角（`interactive-mode.ts:1009-1100` 主循环）

- 输入 → `CustomEditor.handleInput` 处分流：扩展快捷键 → 截图像 → AppKeybindings（`app.interrupt / app.clear / app.exit …`）→ 历史/撤销/补全 → `tui.input.submit` 键。
- 提交时 `setupEditorSubmitHandler` 先尝试内置 slash 命令，再尝试 `!`/`!!` 形态 bash，再走 `session.prompt`。`/session` 之类的内置不进入扩展事件。

开发者视角

- `InteractiveMode.init` 在 `:839-990` 装配 ScrollView 与 dock 顺序（pending → status → widgets-above → editor → widgets-below → footer）。完成 `KeybindingsManager.setKeybindings` 与 CustomEditor/FooterDataProvider/FooterComponent 构造后调用 `setupKeyHandlers()`（`:2763-2829`）与 `setupEditorSubmitHandler()`（`:2870-3003`）。
- 状态变化都通过 `AgentSession` 的事件订阅推到 UI：`InteractiveMode.handleEvent:3065-3392` 按 `agent_start / queue_update / message_start / message_update / message_end / tool_execution_* / agent_end / agent_settled / *_status` 切换 status indicator 与重建消息组件。

架构师视角

- `TUI_KEYBINDINGS`（`packages/tui/src/keybindings.ts:64-179`）与 `KEYBINDINGS`（`packages/coding-agent/src/core/keybindings.ts:63-206`）是项目刻意分两层的默认键：TUI 层只关心通用编辑/选择/alt-screen，`app.*` 命名空间则在 coding-agent 层注入，再用 declaration merging 合并到全局类型表。`KeybindingsManager` 读 `<agentDir>/keybindings.json`（`:339-350`）并把旧版短名（`submit` 等）迁移到新 ID（`:208-268`）。
- 注意：**源码里没有 `DEFAULT_EDITOR_KEYBINDINGS` 与 `DEFAULT_APP_KEYBINDINGS` 这两个常量**——一些旧文档里看到这两个名字要小心，它们是被 2024-Q3 重构掉的旧名。

## 2.5 新增 Provider

`packages/ai/src/providers/` 下每家 provider 通常成对存在：

```
anthropic.ts            anthropic.models.ts
openai.ts               openai.models.ts
google.ts               google.models.ts
…
```

- `*.models.ts`：模型目录数据。**不要手编**——`packages/ai/scripts/generate-models.ts` 会从 `models.dev/api.json`、4 个 live API（OpenRouter、Vercel、NVIDIA NIM、…）与本地 override 表生成；改生成脚本即可。
- `*.ts`：provider 适配器（身份、凭证、catalog 映射）。整个文件通常 < 100 行。

接入新身份（OAuth、Azure 风格 API）：参考 `cloudflare.ts`、`openai-responses.ts`、`amazon-bedrock.ts` 等。鉴权相关常量放在 `env-api-keys.ts`；新增 key 名要在 `pi-test.sh --no-env` 的 `unset` 列表里同步登记。

## 2.6 新增内置工具

内置工具位于 `packages/coding-agent/src/core/tools/`：

- `read.ts` / `write.ts` / `edit.ts` / `edit-diff.ts`：文件读写与差异编辑
- `bash.ts`：执行 shell（前/后台、timeout、信号、输出截断）
- `grep.ts` / `find.ts` / `ls.ts`：ripgrep 风格搜索
- `truncate.ts` / `output-accumulator.ts` / `file-mutation-queue.ts`：跨工具一致性

新建工具的最小骨架（按当前类型签名）：

```ts
import { Type } from "typebox";
import type { AgentTool } from "@earendil-works/pi-agent-core";

const schema = Type.Object({ path: Type.String() });

export const createMyTool = (): AgentTool<typeof schema> => ({
    name: "my_tool",
    label: "My Tool",
    description: "…",
    parameters: schema,
    execute: async (toolCallId, params, signal, onUpdate) => ({
        content: [{ type: "text", text: "result" }],
        details: {},
    }),
});
```

参数顺序是 `(toolCallId, params, signal?, onUpdate?)`，来自 `packages/agent/src/types.ts:385-400`。并在 `core/tools/index.ts` 注册。

## 2.7 写扩展（更轻量的方式）

绝大多数功能都应该写成扩展，而不是改核心。`CONTRIBUTING.md` 的开篇原则：

> pi's core is minimal. If your feature does not belong in the core, it should be an extension.

`packages/coding-agent/examples/extensions/` 给出完整例子：

- `with-deps/` — 携带 npm 依赖的扩展
- `custom-provider-anthropic/` / `custom-provider-gitlab-duo/` — 自定义 provider
- `sandbox/` / `gondolin/` — 把工具与 `!` 命令路由到 micro-VM
- `rpc-extension-ui.ts` — 通过 RPC 在 TUI 上弹出 overlay

扩展 API 表面在 `core/extensions/types.ts`。第 6 章详解。

## 2.8 Git 协作约束

多个 pi session 可能在同一 cwd 并发：

- `git add` 你改过的文件；**不要 `git add -A`**。
- 严禁 `git reset --hard` / `git checkout .` / `git clean -fd` / `git stash` / `git commit --no-verify`。
- rebase 冲突只解决自己改过的文件，其它先 abort 再问。
- 提交消息：`{feat,fix,docs}[(ai,tui,agent,coding-agent)]: <commit message>`。
- 若提交信息要包含 `models.generated.ts` 的变动，那是可以的，但要清楚标注。

## 2.9 常见任务速查

| 任务 | 命令 / 入口 |
| --- | --- |
| 跑主交互 CLI | `./pi-test.sh` |
| 跑单文件测试 | `cd packages/<pkg> && node …/vitest/dist/cli.js --run test/<file>.ts`（或 `node --test test/<file>.ts` 对 tui） |
| 干净产物重建 | `npm run build:offline` |
| 给 AI agent 查本仓 | `mcp__codegraph__codegraph_explore` / 启用 shell 的 `codegraph explore "<query>"` |
| 进入设计模式 | `EnterPlanMode` |
| 跑变更后类型/格式化检查 | `npm run check`（不等于 `npm test`） |
