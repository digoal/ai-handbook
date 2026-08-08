# 上下文与会话

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

一次 Claude Code session 同时包含可恢复的 transcript 和当前模型正在使用的 context。两者相关但不相同：恢复 session 可以找回历史，`/compact` 则压缩当前 context。本章用命名、退出和恢复建立最小闭环。

> **Important**：启动、恢复或压缩交互式会话会向模型服务发送请求，并可能计入订阅或 API 用量。本章作者不自动执行这些步骤。

---

## 学习目标

- 区分 session transcript、当前 context 和长期 memory。
- 正确选择 continue、resume 和 fork。
- 给重要会话命名，而不是依赖自动标题。
- 理解 clear、compact 和开始新会话的区别。
- 避免直接删除内部 transcript 文件。

## 前置条件

先完成 [02 第一次会话](../02-first-session/README.md)。进入练习仓库：

```bash
cd ~/claude-code-handbook-lab/first-session
```

## 场景示范：想续上昨天中断的会话

你昨天和 Claude Code 讨论到一个有意义的中间状态，今天想接着那个思路继续推进，但不想从零讲一遍背景。

### 实操

- 在练习仓库目录里按本章「## Continue 与 resume」先用 `claude --continue` 让 Claude 选最近的会话；若不是目标，用 `--resume` 进入选择器。
- 按「## 给会话命名」回看一下目标会话有没有显式名字；没有的话在本次给它命名，方便下次直接锁定。
- 按「## Fork：保留原会话尝试另一条路径」如果想从同一节点分叉尝试另一种思路，使用 fork 而不是 `clear` 或新会话。

### 验证

- 恢复后会话里能看到昨天的对话历史（`claude --resume` 的选择器列出时显示正确标题或显式名字）。
- 当前 context 已加载昨天的文件修改状态，不需要你重新描述"昨天改了什么"。
- 给会话命名后退出，下次启动 `claude --resume <name>` 能直接定位到该会话，不会命中别的同名项目。

## Session 与 context

- **Session**：一次可保存、恢复和分支的会话记录。
- **Context**：当前请求实际发送给模型的信息，包括 instructions、历史摘要和工具结果。
- **Memory**：跨当前对话加载的项目或自动记忆，下一章单独讨论。

不要用“context 变短”推导“session 历史已删除”。`/compact` 压缩 context，但 session 仍是可恢复记录的一部分。

## Continue 与 resume

本机 2.1.214 提供：

```bash
claude -c
claude -r
```

`-c`/`--continue` 继续当前项目最近会话；`-r`/`--resume` 打开恢复选择器，也可以带 session ID 或显式名称恢复。选择器和 ID 查找具有项目范围，不应把一个项目的 session ID 当成全局句柄。见 [CC-019](../SOURCES.md#cc-019)。

## 给会话命名

启动时命名：

```bash
claude --name handbook-session
```

会话内也可使用 `/rename handbook-session`。显式名称可作为恢复句柄：

```bash
claude --resume handbook-session
```

自动显示标题不等同于显式名称；课程统一使用你自己设置的名称。见 [CC-021](../SOURCES.md#cc-021)。

## 最小恢复练习

### 1. 启动命名会话

```bash
claude --name handbook-session --permission-mode manual
```

发送：

```text
只读取 README.md，用一句话说明它的用途。不要修改文件，不要运行 shell 命令。
```

记录回答后输入：

```text
/exit
```

### 2. 按名称恢复

```bash
claude --resume handbook-session
```

检查：

- 当前目录是否仍是练习仓库。
- 上一条只读请求是否出现在 history 中。
- `README.md` 是否仍无 diff。

在另一个 Terminal 中确认：

```bash
git diff -- README.md
```

### 3. 退出而不删除

再次 `/exit`。退出只结束当前交互，不等于删除 transcript。

## Fork：保留原会话尝试另一条路径

`--fork-session` 与 `--continue` 或 `--resume` 组合，为分支创建新 session ID，原 session 保持不变：

```bash
claude --resume handbook-session --fork-session
```

Fork 不应被描述成 Git branch；它分支的是 conversation/session。新分支也不继承会话期临时批准。见 [CC-020](../SOURCES.md#cc-020)。

该命令会创建额外 session 记录，本章只给出官方核对步骤，不自动执行。

## 不持久化的 print mode

本机 help 显示 `--no-session-persistence` 只适用于 `--print`，使该次非交互运行不写入可恢复 session：

```bash
claude -p --no-session-persistence "只回答 OK"
```

该命令会产生模型用量；这里只核验 help，不执行。见 [CC-022](../SOURCES.md#cc-022)。

## Clear、compact 与新会话

### `/clear`

清空当前 context，开始同一进程中的新 conversation 边界；之前的 session 仍可通过恢复入口找到。它不是删除历史文件的命令。见 [CC-023](../SOURCES.md#cc-023)。

### `/compact [instructions]`

把历史压缩为摘要，可附带聚焦说明，例如：

```text
/compact 保留已确认的需求、修改文件和未完成验证
```

`/context` 用于查看当前 context 的组成。Compact 会改变后续请求使用的 context 和 prompt cache，不修改磁盘文件。见 [CC-024](../SOURCES.md#cc-024)。

### 新会话

当目标已经变化、旧假设会干扰新任务，或你需要干净的权限/说明边界时，退出后重新运行 `claude` 通常比继续 compact 更清楚。

## 不要直接解析内部 transcript

官方记录了 session transcript 的本机存储位置，但 JSONL 属于内部格式，可能随版本变化。不要把脚本建立在该格式上，也不要为了“清理上下文”删除 `~/.claude/projects/`。需要机器输出时使用 [12 Headless 与自动化](../12-headless-and-automation/README.md) 中的正式 output formats。

## 结果检查

完成练习后，你应该能回答：

- 哪个命令继续最近 session？
- 哪个命令打开恢复选择器？
- 显式 session name 与自动标题有什么不同？
- Fork 分支的是 conversation 还是 Git？
- Compact 是否删除磁盘文件？

## 回退与清理

本章没有修改项目文件，因此只需退出会话。不要运行 `claude project purge`；它会删除项目的 Claude Code state，留到 [14 安全、调试与维护](../14-security-debugging-and-maintenance/README.md) 说明危险边界。

## 常见问题

### `claude -c` 恢复了错误会话

`-c` 按当前项目选择最近会话。需要确定目标时使用显式名称或 `-r` 选择器。

### 用 session ID 在另一个项目恢复失败

Session 查找受当前项目和相关 worktrees 限制。先回到创建会话的项目目录。

### Compact 后第一条回复变慢

Compact 会重建会话层 cache，这是预期边界；不要把延迟误判成 session 丢失。

### 能否用删除 JSONL 清空历史

不要。内部格式不是稳定 API，删除项目 state 也不可逆。使用 `/clear`、新 session 或正式 purge 流程，并先理解影响。

## 本章事实与证据

- [CC-019](../SOURCES.md#cc-019) — continue、resume 与项目范围
- [CC-020](../SOURCES.md#cc-020) — fork session
- [CC-021](../SOURCES.md#cc-021) — 显式会话名称
- [CC-022](../SOURCES.md#cc-022) — 非持久化 print mode
- [CC-023](../SOURCES.md#cc-023) — clear 的边界
- [CC-024](../SOURCES.md#cc-024) — compact 与 context
- [CC-061](../SOURCES.md#cc-061) — `claude project purge` 删除范围与 `--dry-run`
- [CC-086](../SOURCES.md#cc-086) — `claude project purge` 的 `--all` / `--interactive` / `--yes` 边界

## 下一章

继续学习 [04 指令与记忆](../04-instructions-and-memory/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
