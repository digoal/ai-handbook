# Subagents 与 worktrees

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Subagent 用独立 context 处理明确职责，Git worktree 为并行文件修改提供独立工作目录。本章只使用本机 help 中可验证的临时 agent JSON 和 `--worktree` 表面，不复制未经当前文档核验的持久 frontmatter 字段表。

> **Important**：真正启动 subagent 或 worktree session 会产生模型用量并创建 session/worktree state。本章作者只核验 help；实际练习应在 disposable Git 仓库中完成。

---

## 学习目标

- 判断何时使用 subagent，而不是继续扩大主 context。
- 用 `--agents` 定义一个会话级只读 reviewer。
- 理解 `--agent`、`--agents` 和 `claude agents` 是不同入口。
- 在 disposable Git repo 中隔离 worktree session。
- 使用 Git 检查并清理 worktree，不运行 project purge。

## 前置条件

先完成 [09 MCP](../09-mcp/README.md)。

## 场景示范：主线在写，想并行让另一个 agent 审代码

你正在主线写新功能，同时想让一个只读 reviewer agent 去审当前 diff，给出反馈。但你不希望 reviewer 的中间思考挤占主 session 的 context，也不希望它的写入操作污染你的工作区。

### 实操

- 按本章「## 三个入口」先弄清 `--agent`、`--agents` 与 `claude agents` 的差异；本场景用 `--agents <json>` 定义临时只读 reviewer。
- 按「## 设计只读 reviewer」在 JSON 里把 prompt 写成只读形态（不调用写文件工具，只读 + 评论）。
- 按「## Disposable worktree 练习」在 disposable 仓库里跑，确保 reviewer 的工作不污染主工作区。

### 验证

- 主 session 的 context 体积在 reviewer 运行时没有显著增长（reviewer 用的是独立 context）。
- reviewer 的产出落地到预先指定的位置（评论文件 / stdout），不修改主工作区任何源代码文件。
- `git status --short` 在 reviewer 完成后保持不变；reviewer 的写入如果进入 git diff，说明它没遵守只读边界。

## 三个入口

### `--agents <json>`

为当前 session 提供一个 JSON object，定义临时 agents。Root help 给出的对象包含 agent name、description 和 prompt。见 [CC-057](../SOURCES.md#cc-057)。

### `--agent <name>`

选择当前 session 使用的 agent，并覆盖 settings 中的 `agent`。它要求该名称已经能被当前 session 解析。

### `claude agents`

管理 background sessions/agents；`--json` 可在非 TTY 环境输出状态数组。它不是创建持久 agent definition 的命令。见 [CC-059](../SOURCES.md#cc-059)。

## 设计只读 reviewer

下面的定义只适用于这一次启动：

```bash
claude \
  --agents '{
    "handbook-reviewer": {
      "description": "Review one Markdown file without editing it",
      "prompt": "Read only the requested Markdown file. Return correctness risks and do not edit files or run shell commands."
    }
  }' \
  --agent handbook-reviewer \
  --permission-mode plan
```

该命令会启动模型 session，产生订阅或 API 用量；本手册不自动执行。

Prompt 必须写清：

- 只处理一个文件。
- 返回什么格式。
- 不编辑、不运行 shell。
- 发现范围外问题时只报告。

临时 JSON 的完整可接受字段以当前 help 和官方 [Subagents](https://code.claude.com/docs/en/sub-agents) 为准，不从旧教程复制。

## Worktree session

本机 root help 提供：

```bash
claude --worktree handbook-review
```

`-w`/`--worktree [name]` 为 session 创建 Git worktree。`--tmux` 需要配合 worktree，可选择 iTerm2 native pane 或 classic tmux。见 [CC-058](../SOURCES.md#cc-058)。

## Disposable worktree 练习

### 1. 创建独立 Git repo

```bash
mkdir -p ~/claude-code-handbook-lab
WORKTREE_LAB=~/claude-code-handbook-lab/worktree-session

if [ -e "$WORKTREE_LAB" ]; then
  printf '%s\n' "Stop: inspect or rename the existing lab directory: $WORKTREE_LAB"
  exit 1
fi

mkdir "$WORKTREE_LAB"
cd "$WORKTREE_LAB"

git init
printf '# Worktree lab\n' > README.md
git add README.md
git commit -m 'chore: initialize worktree lab'
```

该步骤需要本机 Git user 配置。若 commit 失败，先在这个临时仓库配置测试身份，不要修改全局 Git 配置。

### 2. 查看基线

```bash
git status --short
git worktree list
```

### 3. 可选：启动隔离 session

```bash
claude --worktree handbook-review --permission-mode manual
```

这会创建 worktree 并启动模型 session，因此只在理解用量和目录变化后执行。进入后要求只修改 worktree 中的 README，不触碰主工作区。

### 4. 在主工作区观察

在原 repo Terminal 中运行：

```bash
git worktree list
git status --short
```

主工作区应保持干净；worktree 修改应出现在另一个目录/branch。

## 清理 worktree

先在 worktree session 中 `/exit`。然后从主 repo 检查：

```bash
git worktree list
```

找到练习 worktree 的准确路径后：

```bash
git -C <worktree-path> status --short
git worktree remove <worktree-path>
git worktree prune
git worktree list
```

如果 worktree 有未提交修改，先检查和决定保留方式；不要用 `--force` 隐藏不理解的状态。

## Background agents

本机 `claude agents --help` 支持：

- `--json` 输出 active sessions。
- `--all` 在 JSON 中包含已完成 sessions。
- 为 dispatched sessions 指定 model、effort、permission mode、settings、MCP 和 `--plugin-dir`。

见 [CC-059](../SOURCES.md#cc-059) 与 [CC-060](../SOURCES.md#cc-060)。

不要把真实 `agents --json` 输出提交到 evidence；它可能包含 session 或路径信息。第 [13 章](../13-background-agents-and-workflows/README.md) 再讨论 orchestration。

## Project state 不是 worktree cleanup

`claude project purge` 删除 transcripts、tasks、file history 和 config entry。它不是 worktree 删除工具。虽然提供 `--dry-run`，本章只读取 help，不执行 purge。见 [CC-061](../SOURCES.md#cc-061)。

## 结果检查

- 主工作区在并行实验期间保持干净。
- Reviewer 的 prompt 明确只读与返回格式。
- worktree 路径和 branch 可以通过 Git 查看。
- 清理前先退出 session 并检查未提交修改。
- 没有删除 Claude Code project state。

## 常见问题

### `--agent` 找不到名称

`--agent` 选择已解析的 agent。若用 `--agents` 临时定义，确保两个参数在同一次启动中，并且 JSON name 一致。

### Worktree 创建失败

确认当前目录是有 commit 的 Git repo，并检查同名 worktree/branch。不要直接删除 `.git/worktrees`。

### 主工作区也出现修改

先停止两个 session，使用 `git status` 和 `git worktree list` 确认各自 cwd。并行任务若写同一外部路径，worktree 也无法隔离该副作用。

### 能否同时启动很多 agents

并发会放大费用、冲突和审查负担。先证明两个独立任务确实没有文件/状态依赖，再逐步增加。

## 本章事实与证据

- [CC-057](../SOURCES.md#cc-057) — `--agent` 与 `--agents`
- [CC-058](../SOURCES.md#cc-058) — worktree 与 tmux flags
- [CC-059](../SOURCES.md#cc-059) — `claude agents --json`
- [CC-060](../SOURCES.md#cc-060) — dispatched session 配置
- [CC-061](../SOURCES.md#cc-061) — project purge 边界
- [CC-062](../SOURCES.md#cc-062) — worktree 与 agent definition 的边界
- [CC-068](../SOURCES.md#cc-068) — 顶层 `--plugin-dir` 与 `--plugin-url` 的 session-only 边界

## 下一章

继续学习 [11 Plugins](../11-plugins/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
