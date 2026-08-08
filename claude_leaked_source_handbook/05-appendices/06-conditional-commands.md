# 附录 F · 内部命令索引(`INTERNAL_ONLY_COMMANDS`)

> **本附录定位**:列出 `src/commands.ts:225-254` 中 `INTERNAL_ONLY_COMMANDS` 数组定义的**所有内部命令**,含名称、启用条件、预期用途与源码位置。不展开实现细节 — handbook 不覆盖内部命令。
>
> 详细 ant-only 命令机制与 feature flag 守门见 [`03-developer/16a-conditional-commands.md`](../03-developer/16a-conditional-commands.md);命令总览见 [`05-appendices/03-commands.md`](03-commands.md)。

## F.1 摘要

**共 28 项** `INTERNAL_ONLY_COMMANDS`(其中 3 项受 `feature()` 条件守门)。它们仅在 `process.env.USER_TYPE === 'ant' && !process.env.IS_DEMO` 时挂入 `COMMANDS` 数组。绝大多数是 `index.js` 中的 stub 占位(`{ isEnabled: () => false, isHidden: true, name: 'stub' }`),ant 构建时被真实模块替换。

## F.2 速赢

1. **数量**:**28 个**内部命令,绝大多数是 stub。
2. **条件**:`USER_TYPE === 'ant' && !IS_DEMO`(`src/commands.ts:342`)。
3. **守门 feature**:3 个(`ULTRAPLAN`、`KAIROS_GITHUB_WEBHOOKS`、`HISTORY_SNIP`)。
4. **DCE 影响**:外部构建下整个数组本身被 DCE,引用消失。
5. **真实命令**:仅 `/commit`、`/commit-push-pr`、`/init-verifiers`、`/bridge-kick`、`/version`、`/reset-limits*` 有真实实现。

## F.3 INTERNAL_ONLY_COMMANDS 完整列表(28 项)

> 表格字段:**命令名 | 类型 | 启用条件 | 预期用途 | 源码位置**

| 命令 | 类型 | 启用条件 | 预期用途 | 源码 |
|---|---|---|---|---|
| `/backfill-sessions` | stub | `ant && !IS_DEMO` | 会话回填(占位) | `src/commands/backfill-sessions/index.js` |
| `/break-cache` | stub | `ant && !IS_DEMO` | 失效 prompt cache(占位) | `src/commands/break-cache/index.js` |
| `/bughunter` | stub | `ant && !IS_DEMO` | Bug Hunter 实验性功能(占位) | `src/commands/bughunter/index.js` |
| `/commit` | prompt | `ant && !IS_DEMO` | **真实命令**:基于 git diff 生成 commit message + 执行 commit | `src/commands/commit.ts` |
| `/commit-push-pr` | prompt | `ant && !IS_DEMO` | **真实命令**:commit + push + open PR(自动 reviewer、attribution、Slack 联动) | `src/commands/commit-push-pr.ts` |
| `/ctx_viz` | stub | `ant && !IS_DEMO` | 上下文可视化调试(占位) | `src/commands/ctx_viz/index.js` |
| `/good-claude` | stub | `ant && !IS_DEMO` | 内部 prompt 调优(占位) | `src/commands/good-claude/index.js` |
| `/issue` | stub | `ant && !IS_DEMO` | 内部 issue 跟踪(占位) | `src/commands/issue/index.js` |
| `/init-verifiers` | prompt | `ant && !IS_DEMO` | **真实命令**:生成自动化验证 skill(Playwright/Tmux/HTTP) | `src/commands/init-verifiers.ts` |
| `/force-snip` | (内) | `feature('HISTORY_SNIP')` | **真实命令**:手动触发 snip 压缩 | `src/commands/force-snip.js` |
| `/mock-limits` | stub | `ant && !IS_DEMO` | 模拟 rate limit(占位) | `src/commands/mock-limits/index.js` |
| `/bridge-kick` | local | `ant && !IS_DEMO` | **真实命令**:注入 bridge 失败状态测试恢复路径(close/poll/register/heartbeat/reconnect) | `src/commands/bridge-kick.ts` |
| `/version` | local | `ant && !IS_DEMO` | **真实命令**:显示当前会话版本(含 build time) | `src/commands/version.ts` |
| `/ultraplan` | local-jsx | `feature('ULTRAPLAN')` | **真实命令**:远端多 agent 探索 + plan 批准 | `src/commands/ultraplan.tsx` |
| `/subscribe-pr` | (内) | `feature('KAIROS_GITHUB_WEBHOOKS')` | 订阅 GitHub PR webhook(占位/内部) | `src/commands/subscribe-pr.js` |
| `/reset-limits` | stub | `ant && !IS_DEMO` | **真实命令 stub**:重置 rate limit(`reset-limits/index.js` 导出 stub) | `src/commands/reset-limits/index.js` |
| `/reset-limits-noninteractive` | stub | `ant && !IS_DEMO` | **真实命令 stub**:非交互式重置 | `src/commands/reset-limits/index.js`(同源) |
| `/onboarding` | stub | `ant && !IS_DEMO` | 内部 onboarding 流程(占位) | `src/commands/onboarding/index.js` |
| `/share` | stub | `ant && !IS_DEMO` | 共享会话(占位) | `src/commands/share/index.js` |
| `/summary` | stub | `ant && !IS_DEMO` | 会话摘要(占位) | `src/commands/summary/index.js` |
| `/teleport` | stub | `ant && !IS_DEMO` | 会话迁移(占位) | `src/commands/teleport/index.js` |
| `/ant-trace` | stub | `ant && !IS_DEMO` | 内部 trace 调试(占位) | `src/commands/ant-trace/index.js` |
| `/perf-issue` | stub | `ant && !IS_DEMO` | 性能问题报告(占位) | `src/commands/perf-issue/index.js` |
| `/env` | stub | `ant && !IS_DEMO` | 内部环境变量(占位) | `src/commands/env/index.js` |
| `/oauth-refresh` | stub | `ant && !IS_DEMO` | OAuth token 强制刷新(占位) | `src/commands/oauth-refresh/index.js` |
| `/debug-tool-call` | stub | `ant && !IS_DEMO` | 工具调用调试(占位) | `src/commands/debug-tool-call/index.js` |
| `/agents-platform` | (内) | `process.env.USER_TYPE === 'ant'` | Agents platform UI(条件 require) | `src/commands.ts:47-51` |
| `/autofix-pr` | stub | `ant && !IS_DEMO` | 自动修 PR(占位) | `src/commands/autofix-pr/index.js` |

## F.4 真实 vs stub 命令

### F.4.1 真实命令(8 个)

| 命令 | 行为简述 |
|---|---|
| `/commit` | prompt 类:让模型读取 git status/diff/branch/log,生成 commit message,执行 `git commit` |
| `/commit-push-pr` | prompt 类:commit → push → `gh pr create`;可选 Slack 推送 |
| `/init-verifiers` | prompt 类:分析项目类型 → 推荐 Playwright/Tmux/HTTP verifier → 自动安装 |
| `/bridge-kick` | local 类:11 个子命令(close/poll/register/heartbeat/reconnect/status),注入 bridge 失败状态测试恢复路径 |
| `/version` | local 类:显示版本号与构建时间 |
| `/ultraplan` | local-jsx 类:启动远端多 agent 探索任务(30min 超时) |
| `/force-snip` | 手动触发 snip 压缩(`HISTORY_SNIP` feature 守门) |
| `/reset-limits*` | stub 复用 — 当前是 stub |

### F.4.2 Stub 占位(20 个)

20 个命令的 `index.js` 内容相同:

```javascript
export default { isEnabled: () => false, isHidden: true, name: 'stub' };
```

含义:
- 公开版构建下:`bun:bundle` 在 ant 构建中替换为真实实现;外部构建连 stub 都不打包(DCE 整个 `INTERNAL_ONLY_COMMANDS` 数组)。
- ant 构建中:stub 进一步被真实实现替换(由内部构建脚本注入)。
- 当前快照下:即便 ant 用户也看到 `isEnabled: () => false`,**未启用任何行为**。

涉及 stub:`backfill-sessions`、`break-cache`、`bughunter`、`ctx_viz`、`good-claude`、`issue`、`mock-limits`、`onboarding`、`share`、`summary`、`teleport`、`ant-trace`、`perf-issue`、`env`、`oauth-refresh`、`debug-tool-call`、`autofix-pr`、`reset-limits`、`reset-limits-noninteractive`。

## F.5 启用条件

### F.5.1 顶层闸门

```typescript
// src/commands.ts:342
...(process.env.USER_TYPE === 'ant' && !process.env.IS_DEMO
  ? INTERNAL_ONLY_COMMANDS
  : []),
```

- **`USER_TYPE === 'ant'`** — 构建期常量字面量,bundler 把外部构建下的 `true` 分支 DCE 掉。
- **`!IS_DEMO`** — 演示模式(`claude` 内部 demo 二进制)下不挂载。

### F.5.2 命令级 `feature()` 守门

3 个命令额外受 `feature()` 控制,ant 构建中也需注入对应 feature 才挂真实模块:

```typescript
// src/commands.ts:90-105
const agentsPlatform = process.env.USER_TYPE === 'ant'
  ? require('./commands/agents-platform/index.js').default
  : null
const forceSnip = feature('HISTORY_SNIP') ? require('./commands/force-snip.js').default : null
const subscribePr = feature('KAIROS_GITHUB_WEBHOOKS') ? require('./commands/subscribe-pr.js').default : null
const ultraplan = feature('ULTRAPLAN') ? require('./commands/ultraplan.jsx').default : null
```

`agents-platform` 不走 feature 而是 `USER_TYPE` 直接 require。

## F.6 为什么需要 `INTERNAL_ONLY_COMMANDS`

设计意图(`src/commands.ts:223-253`):

```typescript
// Commands that get eliminated from the external build
export const INTERNAL_ONLY_COMMANDS = [
  backfillSessions,
  breakCache,
  bughunter,
  ...
].filter(Boolean)
```

- **内部构建里这些命令仍被注册**(在 `COMMANDS` memoize 数组里)。
- **外部构建通过 `bun:bundle` DCE 整体剔除** `INTERNAL_ONLY_COMMANDS` 数组本身的引用,从而它们就不进入 COMMANDS 数组。
- 这是 "**黑名单 + DCE**" 而非 "条件 import",因为这些命令仍需要在 ant 内部被人与人/Agent 用到。

## F.7 用户视角:为什么 `/xyz` 不可见

最常见原因(按概率):

| 原因 | 表现 | 怎么验证 |
|---|---|---|
| 1. 命令在 `INTERNAL_ONLY_COMMANDS` 里 | 公开版根本没注册 | `grep -E "name:.*'(xyz)'" src/commands/` |
| 2. 命令被 `feature('X')` 守门 | 当前 build 里 `X=false` | `grep -A2 "feature('X')" src/commands.ts` |
| 3. 命令被 `settings.json` deny | 注册了但禁用 | `cat ~/.claude/settings.json \| jq '.permissions.deny'` |
| 4. 你的订阅不支持该命令 | `isEnabled()` 返回 false | 命令的 `isEnabled` 实现 |
| 5. 你不在 plan mode / 不在 bypass 模式 | 与权限模式有关 | `Tool.ts:493-503` |

诊断脚本:

```bash
# 列当前 build 注册的所有命令
grep -E "name:.*'/" src/commands.ts | head -40

# 看某命令是否被 feature 守门
grep -B3 -A8 "name: 'btw'" src/commands/btw/index.ts 2>/dev/null | head -20

# 看是否在 INTERNAL_ONLY 名单
grep -n "<command_name>" src/commands.ts
```

## F.8 反模式

### ❌ 用 `INTERNAL_ONLY_COMMANDS` 当权限列表

`INTERNAL_ONLY_COMMANDS` 是 build-time DCE 提示符,不是运行时的 ACL。运行时拦截命令请用:

- `getCommandName()` + `isCommandEnabled()` 做用户层 ACL
- `permissions.ts` 做权限规则匹配
- `feature()` 在 `isEnabled()` / `getCommandName()` 路径内做最终拒绝

### ❌ 修改公开版 CLI 暴露内部命令

公开版构建是用 `bun:bundle` 静态链接进字面量 `false` 的 `feature()` 调用。即使 fork 源码改了 `commands.ts`,这些命令还需要它们的 `require` 模块不打 DCE — 这意味着还要把它们的 feature 全部开启,并修改 `INTERNAL_ONLY_COMMANDS` 移除。**通常违反内部分发协议**。

## F.9 引用

- [`03-developer/16a-conditional-commands.md`](../03-developer/16a-conditional-commands.md) — conditional command 实战分析
- [`05-appendices/03-commands.md`](03-commands.md) — 全量命令速查
- [`05-appendices/05-build-flags.md`](05-build-flags.md) — 90 个 `bun:bundle` 开关