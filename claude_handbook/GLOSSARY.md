# 术语表

本术语表统一课程中的中文表达。版本敏感命令、字段和限制不在此重复，统一链接到对应章节和 [事实台账](SOURCES.md)。

---

## Agent

根据目标选择工具、观察结果并继续工作的模型执行过程。具体 agent 类型和运行入口见 [10 Subagents 与 worktrees](10-subagents-and-worktrees/README.md) 与 [13 Background agents 与 workflows](13-background-agents-and-workflows/README.md)。

## Agent view

由 `claude agents` 打开的多 session 管理界面。其本机 CLI 表面和隐私边界见 [13 Background agents 与 workflows](13-background-agents-and-workflows/README.md)。

## Background session

离开当前前台交互后继续运行的 Claude Code session。本机可通过 `--background` 启动，并通过 `claude agents` 管理。

## Checkpoint

每个 user prompt 前创建的会话级回退点，用于恢复 Claude 编辑工具跟踪的 code、conversation 或两者。它不跟踪全部文件系统变化，也不替代 Git。见 [07 Checkpoints 与安全迭代](07-checkpoints-and-safe-iteration/README.md)。

## CLI

*Command-line interface*，即通过终端启动和控制 Claude Code 的命令行界面。本手册默认指 macOS Terminal 中的 `claude` 命令。

## Context

当前请求实际提供给模型的信息，包括 instructions、conversation、摘要和工具结果。Context 可以 compact；它不等同于可恢复的 session transcript 或长期 memory。

## Headless mode

不进入交互式终端 UI 的命令行用法。本手册主要指 `--print` 及其 text、JSON、stream-json 输入输出。见 [12 Headless 与自动化](12-headless-and-automation/README.md)。

## Hook

在 Claude Code lifecycle event 发生时执行的 handler。配置由 event、matcher group 和 handler 组成，可能运行本地命令、HTTP、MCP 或模型判断。见 [08 Hooks](08-hooks/README.md)。

## MCP

*Model Context Protocol*，用于把 Claude Code 连接到外部 tools 或 data sources 的协议。Server transport、scope、project approval 与 OAuth 边界见 [09 MCP](09-mcp/README.md)。

## Memory

跨当前对话加载的明确 instructions 或自动积累的项目经验。本手册区分 `CLAUDE.md` 与 auto memory；二者都是 context，不是强制 permission policy。见 [04 指令与记忆](04-instructions-and-memory/README.md)。

## Permission

Claude Code 对 tool call 应用的授权规则。Permission mode、allow/ask/deny、workspace trust、protected paths 和 sandbox 是相关但不同的边界。见 [05 设置与权限](05-settings-and-permissions/README.md)。

## Plugin

把 skills、agents、hooks、MCP 等组件组织成可校验、安装和更新的分发单元。Manifest 合法不等于组件安全。见 [11 Plugins](11-plugins/README.md)。

## Sandbox

针对 Bash 的操作系统级 filesystem/network 隔离。它与 permission rules 独立且可组合，不控制所有非 Bash tools。见 [05 设置与权限](05-settings-and-permissions/README.md)。

## Session

一次 Claude Code interaction 及其可保存、恢复、命名和 fork 的记录。Session transcript 与当前 context 不是同一概念。见 [03 上下文与会话](03-context-and-sessions/README.md)。

## Settings

控制 Claude Code 启动与功能组合的配置。User、project、local、managed 与 CLI scopes 的优先级和 permission 合并规则见 [05 设置与权限](05-settings-and-permissions/README.md)。

## Skill

由 `SKILL.md` 定义的可复用 instructions。Skill 可以显式 slash 调用，也可在 description 与任务相关时由 Claude 选择；正文按需加载。见 [06 Skills 与 slash commands](06-skills-and-slash-commands/README.md)。

## Slash command

在交互式会话中以 `/` 开头的入口。它可能是 CLI built-in command、bundled skill、workflow 或自定义 skill；不要只根据斜杠外观推断实现。

## Subagent

由主任务委派、使用独立 context 处理明确职责的 agent。它适合边界清楚的只读探索或独立工作单元，不自动解决文件冲突。见 [10 Subagents 与 worktrees](10-subagents-and-worktrees/README.md)。

## Workflow

把多个 agent calls 或步骤按依赖组织成可重复执行过程的机制。使用前应定义输入、owner、预算、停止条件和结果汇总。见 [13 Background agents 与 workflows](13-background-agents-and-workflows/README.md)。

## Workspace trust

对首次使用的代码库及其项目级授权来源进行的信任确认。它不等同于批准所有 tool calls，也不替代 MCP project approval。

## Worktree

Git 提供的独立工作目录。Claude Code 可用 `--worktree` 启动隔离 session，但外部路径和共享服务仍可能产生跨 worktree 副作用。见 [10 Subagents 与 worktrees](10-subagents-and-worktrees/README.md)。

---

**Last Updated**: July 20, 2026
**Status**: 00–14 章节术语已核验
