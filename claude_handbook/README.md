# Claude Code CLI 系统学习手册

> 一套面向 macOS Terminal CLI 的简体中文课程。每条易变事实都要能追溯到本机证据或 Claude Code 官方资料。

> **建设状态**：00–14 章已全部完成，并按 Claude Code 2.1.214 与 macOS 15.7.7 建立版本化证据。

---

---

## 手册范围

本手册从第一次运行 `claude` 开始，逐步讲到会话、memory、permissions、skills、hooks、MCP、subagents、plugins 和自动化工作流。

首期遵守以下边界：

- 只讲 macOS 上的 Terminal CLI。
- 不把 Agent SDK、API、Desktop、Web 或 IDE 当作主线内容。
- 不直接复用仓库现有 01–10 课程中的产品事实。
- 不使用第三方文章证明命令、参数、默认值或版本行为。
- 未核验内容只保留在章节骨架中，不写成确定结论。

## 当前基线

| 项目 | 基线 |
|------|------|
| **Claude Code** | 2.1.214 |
| **操作系统** | macOS 15.7.7 |
| **验证日期** | 2026-07-20 |
| **证据范围** | 本机只读 CLI 帮助 + Claude Code 官方文档 |

基线会随重验结果滚动更新，而不是宣称 2.1.214 永远是“最新版”。详情见 [事实台账](SOURCES.md#cc-000) 和 [核验规范](VERIFICATION.md)。

## 学习路线

按编号顺序学习。所有章节均已完成当前基线核验；遇到更高或更低版本时，先从事实 ID 回溯来源再执行。

| 阶段 | 章节 | 状态 |
|------|------|------|
| 起步 | [00 如何使用本手册](00-how-to-use-this-handbook/README.md) | 已发布 |
| 起步 | [01 安装与健康检查](01-installation-and-health/README.md) | 已发布 |
| 起步 | [02 第一次会话](02-first-session/README.md) | 已发布 |
| 基础 | [03 上下文与会话](03-context-and-sessions/README.md) | 已发布 |
| 基础 | [04 指令与记忆](04-instructions-and-memory/README.md) | 已发布 |
| 基础 | [05 设置与权限](05-settings-and-permissions/README.md) | 已发布 |
| 进阶 | [06 Skills 与 slash commands](06-skills-and-slash-commands/README.md) | 已发布 |
| 进阶 | [07 Checkpoints 与安全迭代](07-checkpoints-and-safe-iteration/README.md) | 已发布 |
| 进阶 | [08 Hooks](08-hooks/README.md) | 已发布 |
| 集成 | [09 MCP](09-mcp/README.md) | 已发布 |
| 集成 | [10 Subagents 与 worktrees](10-subagents-and-worktrees/README.md) | 已发布 |
| 集成 | [11 Plugins](11-plugins/README.md) | 已发布 |
| 专家 | [12 Headless 与自动化](12-headless-and-automation/README.md) | 已发布 |
| 专家 | [13 Background agents 与 workflows](13-background-agents-and-workflows/README.md) | 已发布 |
| 专家 | [14 安全、调试与维护](14-security-debugging-and-maintenance/README.md) | 已发布 |
    
附: [Claude Code CLI 泄密源代码解读](CLAUDE_CODE_TUTORIAL.md)  
  
## 使用方法

1. 先读 [00 如何使用本手册](00-how-to-use-this-handbook/README.md)，理解证据等级和版本边界。
2. 在独立练习目录中完成每章步骤，不要直接拿重要项目试验陌生配置。
3. 看到事实 ID 时，打开 [事实台账](SOURCES.md) 检查验证版本、日期和来源。
4. 若本机版本不同，先运行 `claude --version`，再核对官方 changelog 和对应功能页。
5. 只把章节中标为“已实测”或“官方核对”的内容用于实际配置。

## 证据等级

| 等级 | 含义 |
|------|------|
| **已实测** | 在记录的 macOS 与 Claude Code 版本上实际观察到 |
| **官方核对** | 官方文档或官方 changelog 明确说明，但本机未执行对应行为 |
| **条件性** | 受订阅、认证、安装渠道或 feature gate 影响 |
| **待验证** | 不能进入已发布课程正文 |

完整规则、脱敏要求和发布清单见 [VERIFICATION.md](VERIFICATION.md)。统一术语见 [GLOSSARY.md](GLOSSARY.md)。

## 暂不包含

- Windows、Linux 或 WSL 的操作步骤
- 未经本机或官方资料确认的版本历史
- 第三方插件、MCP server 或 marketplace 的质量背书
- Agent SDK 和 Anthropic API 开发教程

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
**Sources**: [本手册事实台账](SOURCES.md)
