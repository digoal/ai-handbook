# Skills 与 slash commands

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

本章把“输入 `/` 看到的入口”分成两类：CLI 自带的 built-in commands，以及由 prompt 驱动的 skills。你将创建一个只读 skill，验证它能被发现、显式调用并安全删除。

> **Important**：调用 skill 会向模型服务发送请求，并可能计入订阅或 API 用量。本手册只核验文件结构和官方行为，不自动替你执行模型调用。

---

## 学习目标

- 区分 built-in command、bundled skill 和自定义 skill。
- 理解 skill 的项目级与用户级作用域。
- 编写最小 `SKILL.md`，让 description 清楚表达使用时机。
- 显式调用 skill，并检查它是否遵守只读边界。
- 安全删除练习 skill，不影响真实用户配置。

## 前置条件

先完成 [05 设置与权限](../05-settings-and-permissions/README.md)。本章沿用练习目录：

```bash
cd ~/claude-code-handbook-lab/first-session
```

## 场景示范：同一组 prompt 用了 N 次，想封装为 skill

你在工作中经常重复同一组 prompt（比如"审 README，提出不超过 3 条结构问题"），每次手动打字很烦，复制粘贴又容易漏掉前置条件。你想把它封装为 skill，让以后用 `/skill-name` 就能复用。

### 实操

- 按本章「## 创建只读 skill」在 `.claude/skills/<name>/SKILL.md` 创建最小骨架；frontmatter 的 `description` 要同时说明能力和使用时机，正文只放指令。
- 在新会话中用 `/<skill-name>` 显式调用，确认 Claude 按 `SKILL.md` 里的指令执行，没有偷偷改文件或跑命令。
- 按「## 回退练习」删除练习 skill，确认不会污染真实用户配置。

### 验证

- 输入 `/` 时 `<skill-name>` 出现在当前 session 的入口列表中。
- 调用后 Claude 的行为严格遵守 `SKILL.md` 的指令边界（比如只读 skill 不应修改文件）。
- 删除 `.claude/skills/<name>/` 后该 skill 从入口列表消失，且 `~/.claude/skills/` 没有残留。

## 两类 slash 入口

输入 `/` 时，Claude Code 会列出当前环境中可用的入口：

- **Built-in command**：由 CLI 直接实现，例如会话控制和配置界面。
- **Skill**：一组可复用 instructions；Claude 在相关时可以使用，也可以由你用 `/skill-name` 显式调用。

不要根据命令数量判断版本。命令会受版本、平台、订阅、plugin 和本地配置影响；需要完整清单时查看官方 [Commands](https://code.claude.com/docs/en/commands)。边界见 [CC-035](../SOURCES.md#cc-035)。

## Skills 与旧 custom commands

当前官方文档说明，custom commands 已合并到 skills：

- `.claude/commands/deploy.md` 仍可创建 `/deploy`。
- `.claude/skills/deploy/SKILL.md` 也可创建 `/deploy`。
- skill 目录还能容纳 supporting files，并支持 invocation control 等扩展能力。

旧 `.claude/commands/` 文件继续工作，但新课程统一使用 skills，避免同时维护两种结构。见 [CC-036](../SOURCES.md#cc-036)。

## Skill 的作用域

本章只使用项目级目录：

```text
.claude/skills/<skill-name>/SKILL.md
```

它适合与项目一起评审和共享。用户级 skill 位于 home 配置范围，会影响多个项目；第一次练习不要写入真实 `~/.claude`。作用域与发现行为见 [CC-037](../SOURCES.md#cc-037)。

## 创建只读 skill

### 1. 确认练习仓库

```bash
pwd
git status --short
```

确认路径位于 `~/claude-code-handbook-lab/first-session` 后再继续。

### 2. 创建目录

```bash
mkdir -p .claude/skills/readme-outline
```

### 3. 编写 `SKILL.md`

```bash
cat > .claude/skills/readme-outline/SKILL.md <<'EOF'
---
name: readme-outline
description: Analyze README.md and propose a clearer outline without editing files.
---

# README outline

Read only README.md in the current project.

Return:

1. The current heading structure.
2. At most three structural problems.
3. A proposed outline.

Do not edit files and do not run shell commands.
EOF
```

`SKILL.md` 由 YAML frontmatter 和 Markdown instructions 组成。`name` 提供稳定标识，`description` 应同时说明能力和使用时机；正文只在 skill 被使用时加载。见 [CC-038](../SOURCES.md#cc-038)。

## 检查文件再调用

先在 shell 中检查：

```bash
find .claude/skills/readme-outline -maxdepth 1 -type f -print
git diff --no-index /dev/null .claude/skills/readme-outline/SKILL.md || true
```

启动新会话，使项目 skill discovery 从干净边界开始：

```bash
claude --permission-mode manual
```

在会话中先输入 `/`，确认是否能找到 `readme-outline`，然后显式调用：

```text
/readme-outline
```

Skill 可以由用户显式调用；若 description 与任务匹配，Claude 也可以自动选择它。是否允许哪一方调用还可由 frontmatter 控制，但完整字段留给官方 [Skills](https://code.claude.com/docs/en/skills)，本章不复制易漂移字段表。见 [CC-039](../SOURCES.md#cc-039)。

## 结果检查

合格结果应满足：

- 只分析 `README.md`。
- 没有修改文件。
- 没有运行 shell 命令。
- 输出包含当前结构、最多三个问题和建议 outline。

在另一个 Terminal 中确认：

```bash
git status --short
git diff -- README.md
```

如果 `README.md` 出现修改，拒绝结果并检查 skill instructions 是否存在模糊授权。

## 回退练习

退出 Claude Code 后，删除本章创建的项目级 skill：

```bash
rm -rf .claude/skills/readme-outline
git status --short
```

`rm -rf` 仅用于刚创建且已确认路径的练习目录。不要把命令改成 `.claude/skills` 或 `~/.claude/skills`。

## 何时使用 CLAUDE.md，何时使用 skill

| 内容 | 更适合的位置 |
|------|--------------|
| 每次会话都应遵守的短规则 | `CLAUDE.md` |
| 重复使用的多步骤过程 | Skill |
| CLI 自带的会话或设置操作 | Built-in command |
| 需要一起分发多种组件 | Plugin |

Skill body 按需加载，而 `CLAUDE.md` 是持续性 instructions。不要把同一流程同时复制到两处。

## 常见问题

### 输入 `/` 后找不到 skill

确认目录名、文件名 `SKILL.md` 和 frontmatter 格式；然后开启新会话。不要先复制到用户级目录绕过项目问题。

### Skill 自动触发得太频繁

收窄 `description`，明确它“何时使用”和“何时不使用”。不要用“帮助开发”这类覆盖所有任务的描述。

### Skill 没有遵守只读要求

把目标文件、允许动作和禁止动作写成可观察条目，并在 Manual mode 检查每次工具请求。Skill instructions 不是权限系统的替代品。

### 是否需要维护完整内置命令表

不需要。输入 `/` 查看当前环境，并使用官方 Commands 页面核对。静态复制长表会很快过期。

## 本章事实与证据

- [CC-035](../SOURCES.md#cc-035) — built-in commands 与 skills 的边界
- [CC-036](../SOURCES.md#cc-036) — custom commands 已合并到 skills
- [CC-037](../SOURCES.md#cc-037) — skill 存放位置与作用域
- [CC-038](../SOURCES.md#cc-038) — `SKILL.md` 结构与按需加载
- [CC-039](../SOURCES.md#cc-039) — 显式调用、自动选择和 invocation control

## 下一章

继续学习 [07 Checkpoints 与安全迭代](../07-checkpoints-and-safe-iteration/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
