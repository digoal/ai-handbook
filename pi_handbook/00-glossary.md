# 00 · 术语表

> 本手册使用的核心术语。每个词条给出：含义 / 关键文件 / 在哪一章展开。术语在文中第一次出现时会再次简要复述。

## 运行模型

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **Agent** | `packages/agent/src/agent.ts` 中的有状态封装。对外暴露 `run / continue / abort / queue` 四类操作，内部维护一个不可变的 `AgentState` 与 runtime 可变字段。 | 第 4 章 |
| **AgentLoop** | `packages/agent/src/agent-loop.ts` 中的 turn-by-turn 状态机。运行一次 `runAgentLoop` → 多轮 `runLoop` → 内部 `streamAssistantResponse`。无自身状态，只对外发 `AgentEvent`。 | 第 4 章 |
| **AgentMessage** | agent 内部统一使用的消息类型（`UserMessage` / `AssistantMessage` / `ToolResultMessage`）。只在 LLM 边界才转成 provider 特定的 `Message[]`。 | 第 4、7 章 |
| **AgentEvent** | 10 段事件的判别联合：`agent_start / turn_start / message_start / message_update / message_end / tool_execution_start / update / end / turn_end / agent_end`。 | 第 4 章 |
| **Lane** | Harness 中**独立分支的状态 + 至多一个激活操作**的运行上下文。三种操作 kind：`run | compaction | navigation`。 | 第 4 章 |
| **Harness** | `packages/agent/src/harness/agent-harness.ts` 定义的契约表面 + reducer。当前实现在 `packages/agent/src/harness/reducer.ts` 与 `session/jsonl/storage.ts`。 | 第 4、5 章 |
| **Turn** | 一次 LLM 调用及其派生出的 tool calls。属于 `agent_start ↔ agent_end` 之内。 | 第 4 章 |
| **Run** | 一次从 user prompt 到 `agent_end` 的完整周期。 | 第 4 章 |

## 会话与持久化

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **SessionEntry** | 会话的一条记录：`message` / `compaction` / `branchSummary` / `custom` 四种类型之一。 | 第 5 章 |
| **SessionTree** | 以 `SessionEntry` 为节点的树；任何 entry 都可被切到 `leaf`。 | 第 5 章 |
| **Leaf** | 当前选中的 entry id（指针）。`/tree` 切 leaf、`/fork` 分叉。 | 第 5 章 |
| **Branch** | 在某个 entry 上分叉出的子树。 | 第 5 章 |
| **JSONL storage** | `packages/agent/src/harness/session/jsonl/storage.ts` 实现的 append-only 持久化：每条 mutation 一次 `appendFile`，按 tail promise chain 串行化。 | 第 5 章 |
| **Compaction** | 把历史消息摘要成 `CompactionEntry`，释放 token 预算。 | 第 12 章 |
| **BranchSummary** | 跨多个 leaf 生成的更上层摘要。 | 第 12 章 |
| **Record log corruption** | `reducer.ts:22-44` 列举的可恢复失败原因：`multiple_open_operations` / `record_after_finish` / `non_consecutive_attempt` 等。 | 第 5 章 |
| **Torn tail** | 崩溃留下的 JSONL 半截行；由 `storage.ts:64-105` 截断或修补。 | 第 5、18 章 |

## LLM 与协议

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **Provider** | LLM 厂商身份：id、name、baseUrl、auth、catalog。`packages/ai/src/providers/*.ts`。 | 第 8 章 |
| **API** | 与具体协议对应的流式实现：`anthropic-messages` / `openai-completions` / `openai-responses` / `bedrock-converse` 等。 | 第 8 章 |
| **Lazy load** | `*.lazy.ts` shim 推迟 SDK 装载。`@anthropic-ai/sdk` 等重依赖仅在用户选定对应 provider 时才 require。 | 第 8 章 |
| **streamSimple** | `packages/ai` 的统一流入口：调用方只传 `model + context + options`。 | 第 8 章 |
| **Model catalog** | 由 `packages/ai/scripts/generate-models.ts` 抓取 `models.dev/api.json` + 4 个 live API + 本地 override 表生成。 | 第 8 章 |
| **Models.dev** | 上游厂商目录源。 | 第 8 章 |
| **Deferred tools** | commit e47b8e3 新增：模型在工具清单中只见到摘要/名称，按需触发 `tool_reference` 时由 host 注入完整 schema。`packages/ai/src/utils/deferred-tools.ts:8-39`。 | 第 8 章 |
| **OAuth provider** | 订阅型凭证流（如 Anthropic Claude Pro/Max）；浏览器或本地回调两形态，分别由 `oauth.ts` / `bun-oauth.ts` 实现。 | 第 8 章 |
| **Faux provider** | `packages/ai/src/providers/faux.ts` 零网络测试 provider。`packages/coding-agent/test/suite/harness.ts` 必用。 | 第 8、17 章 |
| **Protocol** | `packages/protocol`：CBOR + length-prefixed framing + TypeBox schemas。三层防御：MAX_UINT32 / bounded error / one-shot decoder。 | 第 9 章 |
| **CBOR** | 二进制编码，相对 JSON 在大 `AgentMessage[]` 数组上体积更小；自实现（不依赖 npm `cbor`）。 | 第 9 章 |
| **Snapshot** | `packages/server/src/snapshots.ts` 周期性发布的状态 diff，供客户端订阅。 | 第 10 章 |

## 扩展系统

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **Extension** | 通过 `core/extensions/` host 加载的 TypeScript 模块。 | 第 6 章 |
| **ExtensionAPI** | `pi.on / registerTool / registerCommand / registerShortcut / registerFlag` 等等一系列注册方法的表面。 | 第 6 章 |
| **RegisteredTool** | 扩展作者声明的工具：`name / label / description / parameters / execute / renderCall / renderResult / …`，比 agent-core `AgentTool` 字段更丰富。 | 第 6 章 |
| **wrapRegisteredTool** | 把 `RegisteredTool` 转成 `AgentTool`，**保留** `name/label/description/parameters/constrainedSampling/prepareArguments/executionMode/execute`，**略去** 5 个 prompt 与渲染字段，再附 `addedToolNames`。 | 第 6 章 |
| **addedToolNames** | 在工具执行后，agent 检测到有新工具被加入 active-tools 集合时，自动写到 `AgentToolResult.addedToolNames`，为 deferred tools 提供端到端路径。 | 第 6、8 章 |
| **Loader** | `core/extensions/loader.ts`：扫描 `cwd/${CONFIG_DIR}/extensions/` → `agentDir/extensions/` → configured paths，按解析后路径去重。 | 第 6 章 |
| **Runner** | `core/extensions/runner.ts`：执行器与事件 emit，merge 规则（tool/flag first-wins；command 拼接后缀；shortcut 后者覆盖 + 警告；renderer first-wins；handler 链）。 | 第 6 章 |
| **HandlerFn** | `(event, ctx) => Promise<R | void> | R | void` 单个事件订阅句柄。 | 第 6 章 |
| **ExtensionUIContext** | 13 个 UI 方法（`select / confirm / input / notify / setStatus / setWidget / …`）。RPC / print 模式有降级形态。 | 第 6、16 章 |
| **Custom overlay** | `ui.custom(factory, { overlay: true, ...overlayOptions })`：真 TUI overlay 路径，与 `ui.select` 那种 focus-replacing modal 截然不同。 | 第 6、11 章 |

## 用户 / TUI / 模式

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **TUI_KEYBINDINGS** | `packages/tui/src/keybindings.ts:64-179` 默认键：tui.editor.* / tui.input.* / tui.select.* / tui.altScreen.*。 | 第 11 章 |
| **KEYBINDINGS** | `packages/coding-agent/src/core/keybindings.ts:63-206` 默认键：`{ ...TUI_KEYBINDINGS, app.* }`。 | 第 11 章 |
| **AppKeybinding** | 全局注册表中 `app.*` 命名空间所有 ID 的 TypeScript declaration-merged 接口（第 12–55 行）。 | 第 11 章 |
| **showSelector** | `interactive-mode.ts:4347-4374`：把内置组件**替换到 editor 容器**里再 focus；不走 `showOverlay`。包含 `/model /scoped-models /fork /tree /resume /trust /login` 等。 | 第 11 章 |
| **showOverlay** | `tui.ts:549-658` 的真 overlay stack。仅有 `ctx.ui.custom({ overlay: true })` 能进。 | 第 11 章 |
| **BUILTIN_SLASH_COMMANDS** | `packages/coding-agent/src/core/slash-commands.ts:18-41`：22 个内置命令。注意：**不含 `/edit`**。 | 第 2、18 章 |
| **InteractiveMode** | `modes/interactive/interactive-mode.ts`：仓库最大单文件，构造器 527-587、init 839-990、run 1009-1100。 | 第 2 章 |
| **Print mode** | `modes/print-mode.ts:74-76`：单次发送 prompt，附加 stdout takeover。 | 第 16 章 |
| **RPC mode** | `modes/rpc/rpc-mode.ts`：行分隔 JSON 协议；与 `client/server` 包的 CBOR 协议不同。 | 第 16 章 |
| **JSON mode** | `--mode json`：event 流到 stdout，配合 CI 与脚本嵌入。 | 第 16 章 |

## 工具与执行

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **AgentTool** | `packages/agent/src/types.ts:385-400`：`{ name, label, description, parameters, execute(toolCallId, params, signal?, onUpdate?) }`。 | 第 4、7 章 |
| **ToolDefinition** | 比 `AgentTool` 多 5 个渲染字段：`promptSnippet / promptGuidelines / renderShell / renderCall / renderResult`。 | 第 6、7 章 |
| **defineTool** | `core/extensions/types.ts:508` 的 identity helper，保留参数类型推导。 | 第 6 章 |
| **File mutation queue** | `core/tools/file-mutation-queue.ts`：把跨工具的写操作串行化，避免交错失败。 | 第 7 章 |
| **Truncate** | `core/tools/truncate.ts`：单条消息可见长度限制。 | 第 7 章 |
| **Output accumulator** | `core/tools/output-accumulator.ts`：把流式 stdout/stderr 累积到 turn 边界。 | 第 7 章 |
| **Bash executor** | `core/tools/bash.ts`：前台 / 后台 / timeout / 信号 / 输出截断。 | 第 7 章 |
| **Edit tool** | `core/tools/edit.ts` + `edit-diff.ts`：基于唯一锚点的精确替换 + diff 渲染。 | 第 7 章 |

## 设置与资源

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **SettingsManager** | `core/settings-manager.ts`：分层 global / project / CLI，schema migration、原子写、错误处理。 | 第 14 章 |
| **Project trust** | `core/project-trust.ts`：扩展能 hook 的 yes/no/undecided；首启问询由 `resolveProjectTrusted` 走 `ctx.ui.select` 路径。 | 第 14 章 |
| **Migrations** | `core/migrations.ts`：配置 schema 版本升级。 | 第 14 章 |
| **Model runtime** | `core/model-runtime.ts`：模型目录解析 + 凭证绑定 + 网关；`agent-session-services.ts:135-192` 完成构造。 | 第 14 章 |
| **Resource loader** | `core/resource-loader.ts`：扫描 skills / prompts / themes；来自 npm 与 git。 | 第 15 章 |
| **Skills / Prompts / Themes** | 三类资源类型，由 `pi-manifest` 中的对应字段声明。 | 第 15 章 |
| **System prompt** | 默认 + 项目 `.pi/system-prompt.md`（可选）+ 扩展注入 + skill expansion 的拼接结果。 | 第 4、15 章 |

## 发布与运维

| 术语 | 含义 | 关键位置 |
| --- | --- | --- |
| **Lockstep version** | 所有 workspace 包共享一个版本号。`patch` = fix + add，`minor` = breaking；项目另有 `release:major`，发布约定与 npm 不完全一致。 | 第 17 章 |
| **Shrinkwrap** | `packages/coding-agent/npm-shrinkwrap.json`：发布时锁住 transitive deps。 | 第 17 章 |
| **`save-exact=true`** | `.npmrc` 强制直连依赖精确锁版本。 | 第 17 章 |
| **Bun binary** | `packages/coding-agent/build:binary` 用 `bun build --compile` 产出单文件可执行。 | 第 17 章 |
| **Browser smoke** | `scripts/check-browser-smoke.mjs` 在 CI 上跑最小浏览器自检。 | 第 17 章 |

## 给读者的提示

- 同一术语在不同层可能有不同含义：`session` 在 `coding-agent` 是用户面对的会话，在 `agent` 是底层 `SessionEntry` 抽象。保持上下文。
- 不在文中以英文缩写代替汉语：例如不写"tty is detached"，而是写"TTY 未挂接"。
