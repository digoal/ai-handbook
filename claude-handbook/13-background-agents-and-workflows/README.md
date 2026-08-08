# Background agents 与 workflows

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Background session 让任务离开当前交互前台继续运行；agent view 用于观察和派发 sessions；agent teams 与 workflows 进一步组织协作。本章只把本机 CLI 可见入口写成确定事实，受订阅或 feature gate 影响的能力明确标为条件性。

> **Important**：后台和多 agent 工作会并行产生模型用量。没有停止条件、预算和独立验收标准时，不要派发。

---

## 学习目标

- 区分 foreground session、background session、subagent、agent team 和 workflow。
- 使用本机 help 检查 background/agent view 入口。
- 把任务拆成无文件冲突的工作单元。
- 先定义状态、停止点和结果汇总，再考虑并发。
- 避免保存可能包含 session 或路径的状态 JSON。

## 前置条件

先完成 [12 Headless 与自动化](../12-headless-and-automation/README.md) 和 [10 Subagents 与 worktrees](../10-subagents-and-worktrees/README.md)。

## 场景示范：在前台继续工作时，让 review 在后台跑

你正在写新功能的同时，想让另一个 review agent 去审当前 diff 或跑 lint。但不想为了等 review 而停下手上的活，也不想把 review 的中间产物混进主工作区。

### 实操

- 按本章「## Background session」用 `--background`/`--bg` 启动后台 agent，立即拿到 session id，不在前台阻塞。
- 按「## Agent view 与状态输出」用 `claude agents` 观察活跃 sessions 的当前状态。
- 按「## 先设计任务图」先把 review 任务拆成无文件冲突的工作单元（明确输入、停止条件、产出格式），再派发。

### 验证

- `claude agents --json` 显示后台 session 处于 active 状态，主交互会话仍可继续输入新 prompt。
- 后台任务完成时，其产出落到你预先指定的位置，不与主工作区的文件冲突。
- 你随时可通过 `claude agents` 选中该 session 查看结果，再决定保留、终止或 fork。

## Background session

本机 root help 提供 `--background`/`--bg`：启动 background agent 并立即返回，之后通过 `claude agents` 管理。见 [CC-077](../SOURCES.md#cc-077)。

示例会产生模型用量，不由手册作者执行：

```bash
claude --background \
  --permission-mode plan \
  "只读取 README.md，列出结构问题，不修改文件"
```

即使后台 prompt 声明只读，也应使用 Plan mode 和受控目录。

## Agent view 与状态输出

```bash
claude agents --help
```

本机 help 显示：

- 默认进入 agent view。
- `--json` 在不需要 TTY 的情况下输出 active sessions array。
- `--all` 让 JSON 也包含 completed sessions。
- 可为 dispatched sessions 指定 cwd、model、effort、permission mode、settings、MCP 与 plugins。

见 [CC-059](../SOURCES.md#cc-059)。

`agents --json` 可能暴露 session 或本机路径。本手册只保存 help，不保存真实状态输出。

## 六个并行工作概念

Agent view 是观察和派发 sessions 的 surface，不是第六种执行模型；这里与其他概念并列，是为了明确它的职责和可用性边界。

| 类型 | 主要用途 | 关键边界 |
|------|----------|----------|
| Foreground session | 当前交互任务 | 由你直接观察和批准 |
| Background session | 独立长任务 | 需要状态与停止点 |
| Subagent | 主任务内委派 | 独立 context，结果回到父任务 |
| Agent view | 查看和派发 background sessions | Research preview，要求 2.1.139+ |
| Agent team | 多 session 协作 | Experimental，默认关闭 |
| Workflow | 确定性编排多个步骤 | 要求 2.1.154+ 与受支持的付费/API/provider 环境 |

当前本机 `claude agents --help` 能证明 background/agent view 表面，但不能单独证明所有账户都能使用 agent teams 或 dynamic workflows。后两者以官方页面和运行时可见性为准。见 [CC-079](../SOURCES.md#cc-079)。

## 先设计任务图

在真正派发前，用 Markdown 写清楚：

```text
目标：检查三份互不依赖的文档。

任务 A：只读 03 章，返回事实引用问题。
任务 B：只读 04 章，返回教学闭环问题。
任务 C：只读 05 章，返回权限风险。

共同限制：不编辑、不运行 shell、不读取其他文件。
汇总：主任务去重后按严重度输出。
停止：任一任务请求扩大范围时停止。
```

只有 A/B/C 不写同一文件、不依赖彼此中间结果时，才适合并行。

## 最小观察练习

不派发任务，先运行只读 help：

```bash
claude agents --help
```

可选地在了解隐私边界后查看当前状态：

```bash
claude agents --json
```

不要把输出重定向到仓库。若有 active session，先通过当前 agent view 显示的控制确认如何停止，再派发新任务。

## Dispatched session 的配置

本机 help 可为 agent view 和 dispatched sessions 设置：

- `--add-dir`
- `--agent`、`--model`、`--effort`
- `--permission-mode`
- `--settings` 与 `--setting-sources`
- `--mcp-config` 与 `--strict-mcp-config`
- `--plugin-dir`

`--cwd` 只过滤 agent view 中显示的 background sessions，不会设置 dispatched session 的工作目录。见 [CC-080](../SOURCES.md#cc-080)。这些 flags 不会自动解决任务冲突；仍要确保目录、权限和输出格式独立。

## Agent teams 与 workflows

官方文档分别提供 [Agent teams](https://code.claude.com/docs/en/agent-teams) 和 [Workflows](https://code.claude.com/docs/en/workflows) 页面。当前明确 gate 为：

- Agent teams 是 experimental，默认关闭；需设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。
- Agent view 是 research preview，要求 Claude Code 2.1.139 或更高版本。
- Dynamic workflows 要求 Claude Code 2.1.154 或更高版本，并需要受支持的付费计划、Anthropic API 或 provider 环境；Pro 还需从 `/config` 启用。

本章不发明一个并不存在于本机 root help 的 `claude workflow` 子命令，也不把 experimental flag 写成所有用户的默认入口。见 [CC-079](../SOURCES.md#cc-079)。

采用它们前确认：

1. 当前 UI/CLI 是否实际显示入口。
2. 每个任务是否有 owner 和验收标准。
3. 依赖是否被显式表达。
4. 并发预算和最大失败范围。
5. 如何停止、恢复和汇总。

## 停止与回退

后台任务的停止入口可能位于 agent view 或当前运行环境。派发前必须先在当前版本确认控制；如果找不到可靠停止方式，不要启动任务。

文件修改型并行任务还必须使用独立 worktree 或完全不重叠的路径，并在合并前运行：

```bash
git status --short
git diff --check
```

不要通过删除 session state、kill 不明进程或 `project purge` 代替正常停止。

## 常见问题

### Background prompt 很短，为什么仍然昂贵

成本取决于 context、模型、工具调用和迭代次数，而不是 prompt 字数。设置只读范围、预算和停止条件。

### `agents --json` 为空

表示当前过滤范围内没有 active sessions，不代表功能损坏。`--all` 是否显示完成项由本机 help 定义。

### 多 agent 修改了同一文件

这不是自动合并问题，而是任务拆分失败。停止新修改，分别审查 diff，再由单一 owner 合并。

### 能否默认使用 bypass permissions 加速后台任务

不能。后台任务更难观察，应使用更窄权限，而不是更宽绕过。

## 本章事实与证据

- [CC-077](../SOURCES.md#cc-077) — background 启动入口
- [CC-059](../SOURCES.md#cc-059) — agent view 与 JSON 状态
- [CC-079](../SOURCES.md#cc-079) — agent teams/workflows 条件边界
- [CC-080](../SOURCES.md#cc-080) — dispatched session 配置

## 下一章

继续学习 [14 安全、调试与维护](../14-security-debugging-and-maintenance/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
