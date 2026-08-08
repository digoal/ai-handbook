# Checkpoints 与安全迭代

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Claude Code checkpoints 提供会话级快速回退，Git 提供长期、可协作的版本历史。本章把两者组合起来：先建立 Git baseline，再完成一个小修改，最后分别理解 rewind 与 Git restore 的职责。

> **Important**：checkpoint 练习需要交互式 Claude Code，并可能计入订阅或 API 用量。Git 部分可以独立完成。

---

## 学习目标

- 理解 checkpoint 自动创建和跟随 session 保存的边界。
- 区分恢复 code、conversation 和两者同时恢复。
- 识别 checkpoint 无法跟踪的 Bash 与外部文件修改。
- 使用 Git 独立检查和恢复工作区。
- 知道何时使用 summarize、branch 或新会话。

## 前置条件

先完成 [06 Skills 与 slash commands](../06-skills-and-slash-commands/README.md)。进入练习仓库：

```bash
cd ~/claude-code-handbook-lab/first-session
```

## 场景示范：改坏了想回到刚才那次对话

你刚让 Claude Code 改了一个文件，结果改坏了或者方向不对。你想先把磁盘状态退回到上一次对话的状态，再决定换种思路，但当前会话本身可以保留以便对照。

### 实操

- 在交互式 Claude Code 会话中按本章「## Checkpoint 如何工作」确认每个 prompt 前都有 checkpoint。
- 按「## 打开 rewind menu」使用 `/rewind`（或空 prompt + double Esc）选择恢复 code、conversation 或两者。
- 按「## 三种练习路径」对应恢复类型独立验证，不假设三种 restore 选项等价。

### 验证

- `git status --short` 与 `git diff -- <file>` 显示被改坏的修改已不在工作区中。
- 会话内的对话历史已回退到选择的那个 prompt 之前；之后 Claude 看到的"上下文"是回退点之后的版本。
- 已提交的文件版本（如 `git log` 中的最近 commit）不受 checkpoint 操作影响；只有工作区 + 会话被回退。

## Checkpoint 如何工作

Claude Code 在每个 user prompt 前自动记录 checkpoint，并跟踪其文件编辑工具所做的改动。checkpoint 与 conversation 一起保存，所以恢复 session 后仍可以使用 `/rewind`。见 [CC-040](../SOURCES.md#cc-040)。

它不是文件系统快照，也不是 Git commit：

- Bash 命令造成的文件变化不由 checkpoint 跟踪。
- 你在 Claude Code 外手工修改的文件通常不由当前 session checkpoint 跟踪。
- 其他并发 session 的修改也不属于当前 session 的可靠回退边界。

限制见 [CC-043](../SOURCES.md#cc-043)。

## 先建立 Git baseline

确认初始内容并放入 index：

```bash
printf '# Checkpoint lab\n\nInitial state.\n' > checkpoint-lab.md
git add checkpoint-lab.md
git diff -- checkpoint-lab.md
```

最后一条命令应没有输出。Git index 现在是独立于 Claude Code checkpoint 的恢复点。

## 完成最小修改

以 Manual mode 启动：

```bash
claude --permission-mode manual
```

发送：

```text
只修改 checkpoint-lab.md：
在末尾增加二级标题“实验”，并增加一句“这是可回退的练习。”
不要修改其他文件，不要运行 shell 命令。
```

批准前确认目标只有 `checkpoint-lab.md`。完成后在另一个 Terminal 检查：

```bash
git diff -- checkpoint-lab.md
```

## 打开 rewind menu

在 prompt 输入为空时运行：

```text
/rewind
```

也可以在空 prompt 时按两次 `Esc`。如果输入框中已有文字，double `Esc` 的行为不同，因此教程统一推荐显式 `/rewind`。见 [CC-041](../SOURCES.md#cc-041)。

选择本次修改前的 prompt 后，当前官方页面可能提供：

- 恢复 code 与 conversation。
- 只恢复 conversation，保留当前 code。
- 只恢复 code，保留当前 conversation。
- 从选定点开始 summarize，或 summarize 到选定点。
- 取消并返回。

只有存在可恢复的 tracked file changes 时，code restore 选项才会出现。完整行为见 [CC-042](../SOURCES.md#cc-042)。

## 三种练习路径

### 路径 A：只恢复 code

选择只恢复 code，然后运行：

```bash
git diff -- checkpoint-lab.md
```

预期工作区恢复到 Git index baseline，而 conversation 保留。

### 路径 B：只恢复 conversation

选择只恢复 conversation。文件应保持修改状态：

```bash
git diff -- checkpoint-lab.md
```

这适合重新提问但保留当前代码。

### 路径 C：恢复两者

选择同时恢复 code 和 conversation。完成后既检查文件，也确认会话位置回到目标 prompt。

每次只练习一条路径。若要重复，重新发送同一个最小修改 prompt。

## Git 兜底回退

如果 checkpoint 不可用、选项与当前版本不一致，或修改来自 Bash，使用已建立的 Git baseline：

```bash
git restore checkpoint-lab.md
git diff -- checkpoint-lab.md
```

没有输出表示工作区已恢复。checkpoint 官方明确不是 version control 的替代品；长期历史、协作和跨 session 恢复仍应使用 Git。见 [CC-043](../SOURCES.md#cc-043)。

## Summarize、branch 与 rewind

- **Restore**：回退 code、conversation 或两者。
- **Summarize**：压缩选定部分 conversation，不修改磁盘文件。
- **Branch/fork**：保留原 session，尝试另一条路径。
- **Git branch/commit**：形成长期可审查历史。

不要用 summarize 代替文件回退，也不要用 checkpoint 代替 commit。

## 清理练习

退出会话后：

```bash
git restore checkpoint-lab.md
git rm --cached checkpoint-lab.md
rm checkpoint-lab.md
git status --short
```

`git restore` 先恢复工作区，`git rm --cached` 再撤销本章创建的新文件在 index 中的记录。确认文件已回到 baseline 后才删除；不要对已有项目文件机械套用这组命令。

## 常见问题

### `/rewind` 中没有 code restore

选定 checkpoint 之后可能没有 Claude 编辑工具跟踪到的文件变化。Bash、手工编辑和其他 session 的变化不会自动成为当前 checkpoint 的可恢复内容。

### Double Esc 只是清空输入

只有空 prompt 才打开 rewind menu。为减少快捷键上下文差异，直接输入 `/rewind`。

### 恢复 conversation 后文件仍然修改

这是“只恢复 conversation”的预期结果。用 `git diff` 判断磁盘状态，不要只凭对话位置推断文件已恢复。

### 需要永久保留一个可靠版本

创建 Git commit，而不是依赖 session checkpoint。

## 本章事实与证据

- [CC-040](../SOURCES.md#cc-040) — checkpoint 自动创建与 session 保存
- [CC-041](../SOURCES.md#cc-041) — `/rewind` 与空 prompt 的 double Esc
- [CC-042](../SOURCES.md#cc-042) — restore 与 summarize 选项
- [CC-043](../SOURCES.md#cc-043) — 跟踪限制与 Git 边界

## 下一章

继续学习 [08 Hooks](../08-hooks/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
