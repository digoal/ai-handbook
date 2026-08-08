# 附录 C · 命令速查(Commands Quick Reference)

> **本附录定位**:一份**完整、紧凑、可索引**的 `/` 命令清单,按 `src/commands.ts:258-346` 实际注册顺序排列,含别名、类型、argumentHint、隐藏标记与源码位置。读者可以"看到 `/foo` 就在这里找到对应行"。
>
> 用户视角的详细用法见 [`02-user/06-commands.md`](../02-user/06-commands.md);开发者视角的注册/解析/调度机制见 [`03-developer/18-commands.md`](../03-developer/18-commands.md);条件命令的内部名单见 [`05-appendices/06-conditional-commands.md`](06-conditional-commands.md)。

## C.1 摘要

Claude Code CLI 共注册 **63 个内置命令 + 6 个 stub 占位 + 2 个 ant-only internal 数组**。命令执行模型有 3 种:`prompt` 展开文本 / `local` 同步函数 / `local-jsx` 异步 React。`COMMANDS` 数组经 `memoize()` 缓存,`INTERNAL_ONLY_COMMANDS` 仅在 `process.env.USER_TYPE === 'ant' && !IS_DEMO` 时挂载。

## C.2 速赢

1. **63 内置命令**(按 `src/commands.ts:258-346` 顺序)。
2. **3 种执行模型**:`prompt` / `local` / `local-jsx`(`src/types/command.ts:205-206`)。
3. **17 个 REMOTE_SAFE 命令** + **6 个 BRIDGE_SAFE 命令**(`commands.ts:619-637, 651-660`)。
4. **15 个 conditional 命令**(依赖 `feature()` 构建期守门)。
5. **2 个 stub-only 内部命令**(ant 构建才挂真实实现,见 §C.4)。
6. **2-3 个 immediate 命令**(`btw`、`fast`、`model`、`effort`、`passes` 等 `immediate: true`)。

## C.3 内置命令清单(按注册顺序)

> **格式说明**:`/name` | 别名 | 类型 | argumentHint | 描述 | 源码位置
> - **类型列**:`prompt` = 展开文本到对话;`local` = 同步函数返回 `LocalCommandResult`;`local-jsx` = 异步 React 组件
> - **🔒** = 隐藏命令(`isHidden: true`),不出现在 typeahead/help
> - **⚡** = `immediate: true`,在 `queryGuard` 占用时同步 setToolJSX
> - **3P=No** = 3P 提供商(Bedrock/Vertex/Foundry)不可用

### C.3.1 第一批(目录 / Agent)

| 命令 | 类型 | 描述 / argumentHint | 源码 |
|---|---|---|---|
| `/add-dir` (`/add-dir`) | local-jsx | `Add a new working directory`(无 hint) | `src/commands/add-dir/index.ts` |
| `/advisor` | local | `Configure the advisor model`(`[<model>\|off]`) | `src/commands/advisor.ts` |
| `/agents` | local-jsx | `Manage agent configurations` | `src/commands/agents/index.ts` |
| `/branch` (`/branch`) | local-jsx | `Create a branch of the current conversation at this point` | `src/commands/branch/index.ts`(`FORK_SUBAGENT`) |
| `/btw` ⚡ | local-jsx | `Ask a quick side question without interrupting the main conversation`(`<question>`) | `src/commands/btw/index.ts` |
| `/chrome` | local-jsx | `Claude in Chrome (Beta) settings` | `src/commands/chrome/index.ts` |
| `/clear` | local | `Clear conversation history and free up context` | `src/commands/clear/index.ts` |
| `/color` | local-jsx | `Set the prompt bar color for this session` | `src/commands/color/index.ts` |

### C.3.2 第二批(上下文/会话)

| 命令 | 类型 | 描述 / argumentHint | 源码 |
|---|---|---|---|
| `/compact` | local | `Clear conversation history but keep a summary in context. Optional: /compact [instructions for summarization]`(`<optional custom summarization instructions>`) | `src/commands/compact/index.ts` |
| `/config` (`/settings`) | local-jsx | `Open config panel` | `src/commands/config/index.ts` |
| `/copy` | local-jsx | `Copy Claude's last response to clipboard (or /copy N for the Nth-latest)` | `src/commands/copy/index.ts` |
| `/desktop` | local-jsx | `Continue the current session in Claude Desktop` | `src/commands/desktop/index.ts` |
| `/context` | local-jsx | `Visualize current context usage as a colored grid` | `src/commands/context/index.ts:3-9` |
| `/context` (非交互) | local | `Show current context usage`(🔒 在交互模式) | `src/commands/context/index.ts:11-23` |
| `/cost` | local | `Show the total cost and duration of the current session` | `src/commands/cost/index.ts` |
| `/diff` | local-jsx | `View uncommitted changes and per-turn diffs` | `src/commands/diff/index.ts` |
| `/doctor` | local-jsx | `Diagnose and verify your Claude Code installation and settings` | `src/commands/doctor/index.ts` |
| `/effort` ⚡ | local-jsx | `Set effort level for model usage` | `src/commands/effort/index.ts` |

### C.3.3 第三批(工具 / 工作流)

| 命令 | 类型 | 描述 / argumentHint | 源码 |
|---|---|---|---|
| `/exit` | local-jsx | `Exit the REPL` | `src/commands/exit/index.ts` |
| `/fast` ⚡ | local-jsx | `Toggle fast mode (<model> only)`(`[on\|off]`;🔒 不可用时) | `src/commands/fast/index.ts` |
| `/files` | local | `List all files currently in context` | `src/commands/files/index.ts` |
| `/heapdump` | local | `Dump the JS heap to ~/Desktop` | `src/commands/heapdump/index.ts` |
| `/help` | local-jsx | `Show help and available commands` | `src/commands/help/index.ts` |
| `/ide` | local-jsx | `Manage IDE integrations and show status` | `src/commands/ide/index.ts` |
| `/init` | prompt | `Initialize a new CLAUDE.md file with codebase documentation`(内容由 `feature('NEW_INIT')` 切换) | `src/commands/init.ts` |
| `/keybindings` | local | `Open or create your keybindings configuration file` | `src/commands/keybindings/index.ts` |
| `/install-github-app` | local-jsx | `Set up Claude GitHub Actions for a repository` | `src/commands/install-github-app/index.ts` |
| `/install-slack-app` | local | `Install the Claude Slack app` | `src/commands/install-slack-app/index.ts` |
| `/mcp` | local-jsx | `Manage MCP servers` | `src/commands/mcp/index.ts` |
| `/memory` | local-jsx | `Edit Claude memory files` | `src/commands/memory/index.ts` |
| `/mobile` | local-jsx | `Show QR code to download the Claude mobile app` | `src/commands/mobile/index.ts` |
| `/model` ⚡ | local-jsx | `Set the AI model for Claude Code (currently <model>)`(`[model]`) | `src/commands/model/index.ts` |
| `/output-style` | local-jsx | `Deprecated: use /config to change output style` | `src/commands/output-style/index.ts` |
| `/remote-env` | local-jsx | `Configure the default remote environment for teleport sessions` | `src/commands/remote-env/index.ts` |
| `/plugin` | local-jsx | `Manage Claude Code plugins` | `src/commands/plugin/index.tsx` |
| `/pr_comments` | local-jsx | `View GitHub PR comments`(实现细节在 `pr_comments/index.ts`) | `src/commands/pr_comments/index.ts` |
| `/release-notes` | local | `View release notes` | `src/commands/release-notes/index.ts` |
| `/reload-plugins` | local | `Activate pending plugin changes in the current session` | `src/commands/reload-plugins/index.ts` |
| `/rename` | local-jsx | `Rename the current conversation` | `src/commands/rename/index.ts` |
| `/resume` | local-jsx | `Resume a previous conversation` | `src/commands/resume/index.ts` |
| `/session` | local-jsx | `Show remote session URL and QR code` | `src/commands/session/index.ts` |
| `/skills` | local-jsx | `List available skills` | `src/commands/skills/index.ts` |
| `/stats` | local-jsx | `Show your Claude Code usage statistics and activity` | `src/commands/stats/index.ts` |
| `/status` | local-jsx | `Show Claude Code status including version, model, account, API connectivity, and` | `src/commands/status/index.ts` |
| `/statusline` | prompt | `Set up Claude Code's status line UI` | `src/commands/statusline.tsx` |

### C.3.4 第四批(主题 / 反馈 / 注释)

| 命令 | 类型 | 描述 / argumentHint | 源码 |
|---|---|---|---|
| `/tag` | local-jsx | `Toggle a searchable tag on the current session` | `src/commands/tag/index.ts` |
| `/theme` | local-jsx | `Change the theme` | `src/commands/theme/index.ts` |
| `/feedback` (`/bug`) | local-jsx | `Submit feedback about Claude Code`(`[report]`) | `src/commands/feedback/index.ts` |
| `/review` | prompt | `Review a pull request`(可选 PR 号) | `src/commands/review.ts:32-42` |
| `/ultrareview` | local-jsx | `~10–20 min · Finds and verifies bugs in your branch. Runs in Claude Code on the web.`(依赖 `isUltrareviewEnabled()`) | `src/commands/review.ts:47-53` |
| `/rewind` (`/checkpoint`) | local | `Restore the code and/or conversation to a previous point` | `src/commands/rewind/index.ts` |
| `/security-review` | prompt | `Review the code for security vulnerabilities` | `src/commands/security-review.ts` |
| `/terminal-setup` | local-jsx | `Install Shift+Enter key binding for newlines`(macOS 终端另有差异) | `src/commands/terminalSetup/index.ts` |
| `/upgrade` | local-jsx | `Upgrade to Max for higher rate limits and more Opus` | `src/commands/upgrade/index.ts` |
| `/extra-usage` | local-jsx | `Configure extra usage to keep working when limits are hit` | `src/commands/extra-usage/index.ts:12-18` |
| `/extra-usage` (非交互) | local | 同上描述(`supportsNonInteractive`) | `src/commands/extra-usage/index.ts:20-30` |
| `/rate-limit-options` 🔒 | local-jsx | `Show options when rate limit is reached`(claude-ai 订阅者) | `src/commands/rate-limit-options/index.ts` |
| `/usage` | local-jsx | `Show plan usage limits` | `src/commands/usage/index.ts` |
| `/insights` | prompt | `Generate a report analyzing your Claude Code sessions`(懒加载 113KB 模块) | `src/commands/insights.ts` |
| `/vim` | local | `Toggle between Vim and Normal editing modes` | `src/commands/vim/index.ts` |

### C.3.5 第五批(条件命令 — 依赖 `feature()`)

| 命令 | 条件 `feature()` | 类型 | 描述 | 源码 |
|---|---|---|---|---|
| `/web-setup` | `CCR_REMOTE_SETUP` | local-jsx | `Setup Claude Code on the web (requires connecting your GitHub account)` | `src/commands/remote-setup/index.ts` |
| `/fork` | `FORK_SUBAGENT` | local-jsx | Create a branch of the current conversation at this point | `src/commands/branch/index.ts` |
| `/buddy` | `BUDDY` | local-jsx | CompanionSprite 协作功能 | `src/commands/buddy/index.ts` |
| `/proactive` | `PROACTIVE` 或 `KAIROS` | local-jsx | Proactive 主动触发模式 | `src/commands/proactive.js` |
| `/brief` | `KAIROS` 或 `KAIROS_BRIEF` | local-jsx | 切换 brief-only 模式 | `src/commands/brief.ts` |
| `/assistant` | `KAIROS` | local-jsx | Assistant 模式 | `src/commands/assistant/index.ts` |
| `/remote-control` | `BRIDGE_MODE` | local-jsx | `Connect this terminal for remote-control sessions`(别名 `/bridge`) | `src/commands/bridge/index.ts` |
| `/remote-control-server` | `DAEMON && BRIDGE_MODE` | local-jsx | 后台守护进程模式 | `src/commands/remoteControlServer/index.ts` |
| `/voice` | `VOICE_MODE` | local | `Toggle voice mode` | `src/commands/voice/index.ts` |
| `/force-snip` | `HISTORY_SNIP` | (internal) | 手动触发 snip 压缩 | `src/commands/force-snip.js` |
| `/workflows` | `WORKFLOW_SCRIPTS` | local-jsx | 工作流脚本入口(动态 `getWorkflowCommands()`) | `src/commands/workflows/index.ts` |
| `/clear-skill-index-cache` | `EXPERIMENTAL_SKILL_SEARCH` | (internal) | 清理 skill 索引缓存 | `src/services/skillSearch/localSearch.js` |
| `/subscribe-pr` | `KAIROS_GITHUB_WEBHOOKS` | (internal) | 订阅 PR webhook | `src/commands/subscribe-pr.js` |
| `/ultraplan` | `ULTRAPLAN` | local-jsx | 启动多 Agent 探索任务(30min 超时) | `src/commands/ultraplan.tsx` |
| `/torch` | `TORCH` | (internal) | 实验性 Torch 命令 | `src/commands/torch.js` |
| `/peers` | `UDS_INBOX` | local-jsx | Unix Domain Socket inbox(`claude peers`) | `src/commands/peers/index.ts` |

### C.3.6 第六批(动态命令 / 与 3P 互斥)

| 命令 | 条件 | 类型 | 描述 | 源码 |
|---|---|---|---|---|
| `/think-back` | (无) | local-jsx | `Your 2025 Claude Code Year in Review` | `src/commands/thinkback/index.ts` |
| `/thinkback-play` | (无) | local | `Play the thinkback animation` | `src/commands/thinkback-play/index.ts` |
| `/permissions` | (无) | local-jsx | `Manage allow & deny tool permission rules` | `src/commands/permissions/index.ts` |
| `/plan` | (无) | local-jsx | `Enable plan mode or view the current session plan` | `src/commands/plan/index.ts` |
| `/privacy-settings` | (无) | local-jsx | `View and update your privacy settings` | `src/commands/privacy-settings/index.ts` |
| `/hooks` | (无) | local-jsx | `View hook configurations for tool events` | `src/commands/hooks/index.ts` |
| `/export` | (无) | local-jsx | `Export the current conversation to a file or clipboard` | `src/commands/export/index.ts` |
| `/sandbox-toggle` | (无) | local-jsx | 切换 Bash 沙箱 | `src/commands/sandbox-toggle/index.ts` |
| `/logout` | `!isUsing3PServices()` | local-jsx | `Sign out from your Anthropic account`(3P=No) | `src/commands/logout/index.ts` |
| `/login` | `!isUsing3PServices()` | local-jsx | `Switch Anthropic accounts` / `Sign in with your Anthropic account`(3P=No) | `src/commands/login/index.ts` |
| `/passes` ⚡ | (无) | local-jsx | `Share a free week of Claude Code with friends`(🔒 不可邀请时) | `src/commands/passes/index.ts` |
| `/tasks` | (无) | local-jsx | `List and manage background tasks` | `src/commands/tasks/index.ts` |
| `/workflows`(已计) | `WORKFLOW_SCRIPTS` | local-jsx | 动态加载的工作流 | (同上) |
| `/torch`(已计) | `TORCH` | (internal) | 实验性 | (同上) |
| `/stickers` | (无) | local | `Order Claude Code stickers` | `src/commands/stickers/index.ts` |

### C.3.7 INTERNAL_ONLY_COMMANDS(ant 内部)

仅在 `process.env.USER_TYPE === 'ant' && !IS_DEMO` 时挂载(详见 [`05-appendices/06-conditional-commands.md`](06-conditional-commands.md)):

```
/backfill-sessions
/break-cache
/bughunter
/commit
/commit-push-pr
/ctx_viz
/good-claude
/issue
/init-verifiers
/force-snip         (仅 HISTORY_SNIP)
/mock-limits
/bridge-kick
/version
/ultraplan          (仅 ULTRAPLAN 守门)
/subscribe-pr        (仅 KAIROS_GITHUB_WEBHOOKS)
/reset-limits
/reset-limits-noninteractive
/onboarding
/share
/summary
/teleport
/ant-trace
/perf-issue
/env
/oauth-refresh
/debug-tool-call
/agents-platform
/autofix-pr
```

> 其中 `break-cache`、`bughunter`、`good-claude`、`issue`、`ant-trace`、`autofix-pr`、`ctx_viz`、`debug-tool-call`、`env`、`mock-limits`、`oauth-refresh`、`onboarding`、`perf-issue`、`reset-limits`、`share`、`summary`、`teleport`、`backfill-sessions` 在 `src/commands/<name>/index.js` 中是 `stub: { isEnabled: () => false, isHidden: true, name: 'stub' }` 占位 — 外部构建下完全不可见。

## C.4 安全白名单(bridge / remote 模式)

### C.4.1 `REMOTE_SAFE_COMMANDS`(17 项)— `src/commands.ts:619-637`

允许在 `--remote` 模式下执行的命令(session、exit、clear、help、theme、color、vim、cost、usage、copy、btw、feedback、plan、keybindings、statusline、stickers、mobile)。`/status`、`/bughunter` 等不在内。

### C.4.2 `BRIDGE_SAFE_COMMANDS`(6 项)— `src/commands.ts:651-660`

bridge(手机/网页)来源的 `local` 命令白名单:compact、clear、cost、summary、releaseNotes、files。

### C.4.3 `isBridgeSafeCommand(cmd)`

- `prompt` → 默认安全
- `local-jsx` → **永远禁止**
- `local` → 需在 `BRIDGE_SAFE_COMMANDS` 内

## C.5 速查:按类型分组

### C.5.1 `prompt` 类(11 个,展开文本)

| 命令 | 描述 |
|---|---|
| `/init` | 引导生成 CLAUDE.md |
| `/review` | PR 代码 review |
| `/statusline` | 配置状态栏命令 |
| `/security-review` | 安全审查 |
| `/insights` | 报告分析 |
| `/insights` 等 | 详情见上 |
| `/init-verifiers` (ant) | 创建 verifier skill |
| `/commit` (ant) | 创建 git commit |
| `/commit-push-pr` (ant) | commit + push + open PR |

### C.5.2 `local` 类(8 个,同步)

| 命令 | 描述 |
|---|---|
| `/advisor` | 配置 advisor 模型 |
| `/clear` | 清除上下文 |
| `/compact` | 压缩 |
| `/context`(非交互) | 文本版 context 报告 |
| `/cost` | 显示费用 |
| `/extra-usage`(非交互) | 配置超额 |
| `/files` | 列出文件 |
| `/heapdump` | 堆转储 |
| `/install-slack-app` | 安装 Slack app |
| `/keybindings` | 快捷键 |
| `/release-notes` | release notes |
| `/reload-plugins` | 刷新插件 |
| `/reset-limits-noninteractive` (ant) | 重置限速 |
| `/rewind` (`/checkpoint`) | 回退 |
| `/stickers` | 贴纸订购 |
| `/thinkback-play` | 播放动画 |
| `/version` (ant) | 显示版本 |
| `/vim` | Vim 模式 |
| `/voice` | 语音模式 |

### C.5.3 `local-jsx` 类(40+ 个,异步 React)

涵盖 REPL 主屏 UI 渲染:`/add-dir`、`/agents`、`/branch`、`/btw`、`/chrome`、`/color`、`/config`、`/copy`、`/desktop`、`/context`、`/diff`、`/doctor`、`/effort`、`/exit`、`/fast`、`/help`、`/ide`、`/install-github-app`、`/login`、`/logout`、`/mcp`、`/memory`、`/mobile`、`/model`、`/output-style`、`/passes`、`/permissions`、`/plan`、`/plugin`、`/pr_comments`、`/privacy-settings`、`/rate-limit-options`、`/rename`、`/resume`、`/sandbox-toggle`、`/session`、`/skills`、`/stats`、`/status`、`/tag`、`/tasks`、`/terminal-setup`、`/theme`、`/upgrade`、`/usage`、`/web-setup`、`/workflows`、`/buddy`、`/proactive`、`/brief`、`/assistant`、`/bridge`、`/remote-control-server`、`/peers`、`/feedback`、`/hooks`、`/export`、`/ultraplan`、`/fork` 等。

## C.6 速查:按 feature 守门

| 条件 | 启用命令 | 备注 |
|---|---|---|
| `BRIDGE_MODE` | `/remote-control` | bridge 模式 |
| `BRIDGE_MODE && DAEMON` | `/remote-control-server` | daemon + bridge |
| `VOICE_MODE` | `/voice` | 语音输入 |
| `WORKFLOW_SCRIPTS` | `/workflows` | 动态加载工作流 |
| `CCR_REMOTE_SETUP` | `/web-setup` | Claude Code on the web |
| `FORK_SUBAGENT` | `/fork` | fork subagent |
| `BUDDY` | `/buddy` | CompanionSprite |
| `PROACTIVE \|\| KAIROS` | `/proactive` | 主动模式 |
| `KAIROS \|\| KAIROS_BRIEF` | `/brief` | brief-only 模式 |
| `KAIROS` | `/assistant` | Assistant 模式 |
| `UDS_INBOX` | `/peers` | UDS inbox |
| `ULTRAPLAN` | `/ultraplan` | 远端规划(同时在 INTERNAL_ONLY) |
| `TORCH` | `/torch` | 实验性 |
| `EXPERIMENTAL_SKILL_SEARCH` | `/clear-skill-index-cache` | 清理 skill 索引 |
| `KAIROS_GITHUB_WEBHOOKS` | `/subscribe-pr` | GitHub webhook(同时在 INTERNAL_ONLY) |
| `HISTORY_SNIP` | `/force-snip` | 手动 snip(同时在 INTERNAL_ONLY) |
| `!isUsing3PServices()` | `/logout`, `/login()` | 3P 互斥 |
| `!getIsNonInteractiveSession()` | `/context` | 交互模式可见 |
| `!isEnvTruthy(DISABLE_COMPACT)` | `/compact` | 环境变量可禁用 |
| `!isEnvTruthy(DISABLE_LOGIN_COMMAND)` | `/login` | 环境变量可禁用 |
| `!isEnvTruthy(DISABLE_EXTRA_USAGE_COMMAND)` | `/extra-usage` | 环境变量可禁用 |
| `isEssentialTrafficOnly()` 等 | `/feedback` | 必要流量模式禁用 |

## C.7 速查:按可用性约束

| 命令 | 限定 |
|---|---|
| `/feedback` | `!isEnvTruthy(DISABLE_FEEDBACK_COMMAND) && !isEnvTruthy(DISABLE_BUG_COMMAND) && !isEssentialTrafficOnly() && USER_TYPE !== 'ant' && isPolicyAllowed('allow_product_feedback')` |
| `/fast` | `availability: ['claude-ai', 'console']` + `isFastModeEnabled()` |
| `/model`, `/effort` | `shouldInferenceConfigCommandBeImmediate()` 控制 `immediate` |
| `/rate-limit-options` | `isClaudeAISubscriber()` |
| `/advisor` | `canUserConfigureAdvisor()` + 模型能力检查 |
| `/extra-usage` | `isOverageProvisioningAllowed()` + 交互模式 |
| `/passes` | `checkCachedPassesEligibility()` |
| `/terminal-setup` | `env.terminal` 在支持列表内才显示 |

## C.8 引用

- [`02-user/06-commands.md`](../02-user/06-commands.md) — 用户视角详细命令说明
- [`03-developer/18-commands.md`](../03-developer/18-commands.md) — 开发者视角命令系统
- [`03-developer/16a-conditional-commands.md`](../03-developer/16a-conditional-commands.md) — conditional command 实战
- [`05-appendices/05-build-flags.md`](05-build-flags.md) — 完整 `bun:bundle` 开关清单
- [`05-appendices/06-conditional-commands.md`](06-conditional-commands.md) — `INTERNAL_ONLY_COMMANDS` 内部名单
- [`05-appendices/01-file-tree.md`](01-file-tree.md) — 目录索引
