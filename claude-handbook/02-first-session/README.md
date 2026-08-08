# 第一次会话

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

本章用一个独立练习目录完成最小闭环：启动 Claude Code、建立工作区信任、先读取再修改、检查 diff，并明确保留或回退结果。

> **Important**：运行交互式 Claude Code 会向模型服务发送请求，并可能计入你的订阅或 API 用量。只在你理解账户计费方式后执行本章练习。

---

## 学习目标

- 从正确的项目目录启动交互式会话。
- 理解工作区信任与工具权限不是同一件事。
- 用范围明确的 prompt 约束读取、修改和验证步骤。
- 在离开会话前检查 diff，并决定保留或回退。
- 退出后继续最近会话。

## 前置条件

完成 [01 安装与健康检查](../01-installation-and-health/README.md)，并确认：

```bash
claude --version
claude doctor
```

本章不会使用 memory、skills、hooks、MCP 或 subagents。

## 场景示范：第一次打开项目，建立最小工作流

你刚拿到一个项目，第一次和 Claude Code 一起工作。你希望先用只读方式理解项目结构，再决定要不要修改，并避免一次性授权过多工具。

### 实操

- 按本章「## 1. 创建隔离练习目录」建立一棵独立的练习目录并初始化 Git，便于稍后用 diff 验证。
- 按「## 2. 以 Manual mode 启动」用 `claude --permission-mode manual` 启动，保留每一步的授权决策。
- 按「## 3. 处理工作区信任」确认路径无误后信任它。
- 按「## 4. 先做只读检查」先让 Claude 读 README 和目录结构，不进入修改阶段。
- 按「## 5. 请求一个最小修改」给一个范围明确的 prompt，完成后按「## 6. 在 Terminal 检查结果」用 `git diff` 校验。

### 验证

- `git status --short` 与 `git diff` 显示只包含你明确请求的那项修改，没有意外改动其他文件。
- 整个会话没有触发 `bypassPermissions` 模式，所有工具调用都经过你显式授权。
- 按「## 8. 退出与继续」退出后能干净地用 `claude --continue` 接续，下次再回来时工作区状态一致。

## 1. 创建隔离练习目录

在 Terminal 中运行：

```bash
mkdir -p ~/claude-code-handbook-lab
FIRST_SESSION_LAB=~/claude-code-handbook-lab/first-session

if [ -e "$FIRST_SESSION_LAB" ]; then
  printf '%s\n' "Stop: inspect or rename the existing lab directory: $FIRST_SESSION_LAB"
  exit 1
fi

mkdir "$FIRST_SESSION_LAB"
cd "$FIRST_SESSION_LAB"

git init
printf '# Demo project\n\nA minimal project for learning Claude Code.\n' > README.md
git add README.md
```

`git add` 在这里把初始文件放入 index，方便稍后使用 `git diff` 查看工作区变化；本章不要求创建 commit。

确认当前目录：

```bash
pwd
git status --short
```

不要在 home 目录、真实生产仓库或包含凭证的目录中完成第一次练习。

## 2. 以 Manual mode 启动

为了让首次修改的授权过程可观察，使用本机 2.1.214 已验证的参数：

```bash
claude --permission-mode manual
```

本机 help 接受 `--permission-mode manual`。见 [CC-018](../SOURCES.md#cc-018)。完整 permission modes 将在 [05 设置与权限](../05-settings-and-permissions/README.md) 中单独核验。

直接运行 `claude` 默认也会启动交互式会话；`--print` 则是非交互模式，并会跳过工作区信任对话框。见 [CC-008](../SOURCES.md#cc-008)。本章不要使用 `--print`。

## 3. 处理工作区信任

首次在该目录启动时，Claude Code 会进行工作区信任验证。这个练习目录由你刚刚创建，可以在确认路径无误后信任它。

工作区信任和工具权限解决不同问题：

- **工作区信任**：决定是否信任该仓库中的项目级规则。
- **工具权限**：决定某次读取、修改或命令执行是否允许。

信任按 git 仓库根目录保存；直接从 home 目录启动是例外，只在当前会话保持。见 [CC-014](../SOURCES.md#cc-014)。

> **Warning**：不要因为课程建议而信任来源不明的仓库。先检查项目文件、settings、hooks 和启动脚本。

## 4. 先做只读检查

进入会话后发送：

```text
只读取当前目录的 README.md，并回答：
1. 这个练习项目目前有什么内容？
2. 如果要增加一个“使用方法”小节，最小改动是什么？
不要修改文件，不要运行 shell 命令。
```

这个 prompt 包含四个必要元素：

- 目标文件：`README.md`
- 目标结果：说明现状和最小改动
- 范围：当前目录
- 禁止项：不修改、不运行命令

先检查回答是否只描述现状。如果模型提出额外重构、创建文件或安装依赖，不要继续；重新收紧范围。

## 5. 请求一个最小修改

确认只读分析合理后，发送：

```text
只修改 README.md：
- 在末尾增加二级标题“使用方法”
- 标题下增加一句“运行本项目不需要安装依赖。”
- 不修改现有文字，不创建其他文件
修改完成后说明改了什么，并提醒我检查 git diff。
```

官方 quickstart 描述的首次改动流程会先定位文件、展示拟议变更，并按当前权限模式请求批准后执行编辑。不同 settings、预批准规则或 permission mode 会改变是否提示。见 [CC-015](../SOURCES.md#cc-015) 和 [CC-016](../SOURCES.md#cc-016)。

在 Manual mode 中看到修改授权请求时：

1. 检查目标是否只有 `README.md`。
2. 检查操作是否与 prompt 一致。
3. 不理解时拒绝，并要求先解释。
4. 只有在范围正确时才批准。

## 6. 在 Terminal 检查结果

可以在另一个 Terminal 窗口进入同一目录，运行：

```bash
cd ~/claude-code-handbook-lab/first-session
git diff -- README.md
```

预期 diff 只包含新增的“使用方法”标题和一句说明。继续检查：

```bash
git status --short
```

如果 Claude Code 修改了其他文件、改写了现有段落，或结果与 prompt 不符，不要直接接受。

## 7. 明确保留或回退

如果结果正确，用 index 接受当前版本：

```bash
git add README.md
```

如果结果不正确，从练习开始时保存的 index 恢复：

```bash
git restore README.md
```

然后再次运行：

```bash
git diff -- README.md
```

没有输出表示工作区与 index 一致。这里的 Git 流程是课程练习，不等同于 Claude Code checkpoint；后者将在 [07 Checkpoints 与安全迭代](../07-checkpoints-and-safe-iteration/README.md) 中核验。

## 8. 退出与继续

在 Claude Code 会话中输入：

```text
/exit
```

回到 shell 后，可以继续当前目录最近的会话：

```bash
claude -c
```

也可以打开恢复选择器：

```bash
claude -r
```

`-c`、`-r` 的本机语义和 `/exit` 的官方来源见 [CC-013](../SOURCES.md#cc-013) 与 [CC-017](../SOURCES.md#cc-017)。恢复会话的完整行为留到 [03 上下文与会话](../03-context-and-sessions/README.md)。

## 结果检查

完成本章后，你应该能回答：

- 我是从哪个目录启动 Claude Code 的？
- 我为什么信任或拒绝信任这个目录？
- 本次 prompt 明确允许和禁止了什么？
- 哪个文件发生了变化？
- 我用什么命令观察 diff？
- 我最终保留还是回退了结果？

如果任何答案不明确，先重复练习，不要进入真实项目。

## 常见问题

### 没有出现工作区信任提示

该工作区可能已经被信任，或你启动的不是交互式流程。`--print` 会跳过工作区信任对话框；本章应使用交互式 `claude --permission-mode manual`。

### 读取文件时没有提示权限

这不一定是异常。权限系统会根据操作类型、permission mode 和已配置规则决定是否提示。不要把“读取未提示”推导成“所有操作都已授权”。

### 修改时没有出现预期提示

先退出，再确认启动命令和当前 settings。不要为了制造提示而删除整个 `~/.claude` 目录；权限配置将在后续章节系统讲解。

### diff 包含意外修改

先拒绝或回退，再把 prompt 缩小到单个文件和单个可观察结果。不要用第二个模糊 prompt 修复第一个模糊 prompt。

## 本章事实与证据

- [CC-008](../SOURCES.md#cc-008) — 交互式会话与 `--print` 边界
- [CC-013](../SOURCES.md#cc-013) — `-c` 与 `-r`
- [CC-014](../SOURCES.md#cc-014) — 工作区信任
- [CC-015](../SOURCES.md#cc-015) — 权限系统边界
- [CC-016](../SOURCES.md#cc-016) — 官方首次修改流程
- [CC-017](../SOURCES.md#cc-017) — `/exit` 与恢复入口
- [CC-018](../SOURCES.md#cc-018) — 本机 Manual mode 启动参数

## 下一章

继续学习 [03 上下文与会话](../03-context-and-sessions/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
