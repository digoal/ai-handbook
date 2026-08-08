# 指令与记忆

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

`CLAUDE.md` 保存你明确编写的 instructions，auto memory 保存 Claude 在工作中积累的项目经验。两者都会进入 context，但都不是强制权限规则。本章只在练习仓库创建项目级 instructions，不修改真实用户 memory。

> **Warning**：不要把 token、密码、客户数据或私有路径写进 `CLAUDE.md` 或 auto memory。它们会进入后续模型 context。

---

## 学习目标

- 区分 user、project、local 与目录级 instructions。
- 理解上层文件、子目录文件和 imports 的加载时机。
- 编写短小、可观察、不会与权限系统混淆的规则。
- 理解 auto memory 的存储和加载上限。
- 使用 `/memory` 检查来源，并安全清理练习文件。

## 前置条件

先完成 [03 上下文与会话](../03-context-and-sessions/README.md)。进入练习仓库：

```bash
cd ~/claude-code-handbook-lab/first-session
```

## 场景示范：新成员首次接触项目，把规则写进 CLAUDE.md

团队来了一个新成员，第一次跑这个练习项目时 Claude 会问很多重复的入门问题（怎么跑测试、目录约定是什么）。你想把项目级规则沉淀进 `CLAUDE.md`，让后续每个新会话自动遵守。

### 实操

- 按本章「## 创建可观察的项目规则」在练习仓库根创建 `CLAUDE.md`，每条规则都写成"短、具体、可验证"的形态（不要写"保持高质量"这种无法验收的口号）。
- 按「## Imports」如果你已有的规则文件比较长，把可复用的部分用 `@path` 拆出去。
- 按「## 使用 `/memory` 检查来源」启动一个新会话，用 `/memory` 确认 `CLAUDE.md` 已被加载。

### 验证

- 在练习仓库开一个新会话，先让 Claude 读 README，再问"这个项目用什么命令测试"，回答应直接引用 `CLAUDE.md` 而非问回去。
- 把 `CLAUDE.md` 临时改成错别字或删一条规则，Claude 的回答应随之变化，确认规则真的进入了 context 而不是缓存。
- `git diff -- CLAUDE.md` 只显示你刚写的那几条规则，没有意外夹杂真实凭证或私人路径。

## 两类持久信息

| 类型 | 谁维护 | 适合内容 |
|------|--------|----------|
| `CLAUDE.md` | 你和团队 | 构建命令、代码规范、架构约束、验证要求 |
| Auto memory | Claude Code | 项目中反复出现的命令、模式和调试经验 |

Instructions 表达“应该怎么做”，permissions 决定“是否允许调用工具”。如果要硬性阻止命令，使用 [05 设置与权限](../05-settings-and-permissions/README.md) 或 [08 Hooks](../08-hooks/README.md)，不要只写一句“禁止”。

## CLAUDE.md 的作用域

官方定义了从广到窄的来源：managed settings、user、project 和 local。启动时，工作目录上层路径中的相关 instructions 会从广到窄追加，而不是简单用后者覆盖前者；子目录的 instructions 在 Claude 读取该目录中的文件时按需加载。见 [CC-025](../SOURCES.md#cc-025)。

本章只创建仓库根 `CLAUDE.md`：

```text
~/claude-code-handbook-lab/first-session/CLAUDE.md
```

不要为了练习修改 `~/.claude/CLAUDE.md` 或 managed settings 路径。

## 创建可观察的项目规则

### 1. 写入最小文件

```bash
cat > CLAUDE.md <<'EOF'
# Project instructions

- Before proposing a change, name the target file.
- Do not modify files unless the user explicitly asks.
- Use `git diff -- <file>` as the final verification step.
EOF
```

规则应短、具体、能观察。不要写“保持高质量”这类无法验收的口号。

### 2. 检查 Git 状态

```bash
git status --short
git diff --no-index /dev/null CLAUDE.md || true
```

### 3. 启动只读验证

> **Important**：启动交互式 Claude Code 会向模型服务发送请求，并可能计入订阅或 API 用量。

```bash
claude --permission-mode manual
```

发送：

```text
先列出当前项目 instructions 中与文件修改有关的规则。
然后只读取 README.md，提出一个最小改进建议。
不要修改文件，不要运行 shell 命令。
```

检查回答是否复述了目标文件、显式授权和 diff 验证要求。

## Imports

`CLAUDE.md` 可用 `@path` 导入其他文件。相对路径相对于包含 import 的文件解析，并有递归深度限制（最多 4 hops）；项目首次遇到外部 import 时还可能要求批准。见 [CC-026](../SOURCES.md#cc-026)。

本章不需要 import。只有当一个长期规则文件已经难以阅读时才拆分；import 仍会进入启动 context，并不节省 token。

## Auto memory

Auto memory 默认开启。官方说明每个项目 memory 目录包含 `MEMORY.md` 索引和可选主题文件；启动时只加载 `MEMORY.md` 的前 200 行或 25 KB，以先达到者为准。Git worktrees 和同仓库子目录共享项目 memory 范围。见 [CC-027](../SOURCES.md#cc-027)。

Auto memory 适合记录：

- 已验证的 build/test 命令。
- 反复出现的目录或架构模式。
- 可靠的调试经验。

不适合记录：

- 凭证和个人信息。
- 一次性任务进度。
- 未验证的猜测。
- 应由 Git 保存的代码内容。

## 使用 `/memory` 检查来源

在交互式会话中输入：

```text
/memory
```

官方页面说明，该入口列出 instruction 和 auto memory 位置，并提供开关或编辑入口。修改已加载的 `CLAUDE.md` 不会立即改变当前 cached context；使用 `/clear`、`/compact` 或新会话重新加载。见 [CC-028](../SOURCES.md#cc-028)。

不要在教程中复制 `/memory` 的完整 UI 文案，它可能随版本变化。

## 结果检查

在另一个 Terminal 中运行：

```bash
git diff --no-index /dev/null CLAUDE.md || true
git diff -- README.md
```

预期：

- `CLAUDE.md` 只有三条练习规则。
- `README.md` 没有修改。
- 会话回答能指出目标文件和只读边界。

## 回退与清理

退出会话后：

```bash
if git ls-files --error-unmatch CLAUDE.md >/dev/null 2>&1; then
  git rm -f CLAUDE.md
else
  rm CLAUDE.md
fi

git status --short
```

本章没有要求生成或编辑 auto memory。若你的会话自动产生 memory，不要在不确认项目路径时删除 `~/.claude/projects/`；先用 `/memory` 定位，并只清理练习项目对应内容。

## 编写有效 instructions

- 每条表达一个动作或约束。
- 写出适用范围和验证方式。
- 保持简短；长流程移到 skill。
- 与代码一起变化的规则放 project scope。
- 个人偏好不要提交给团队。
- 权限控制交给 settings/hooks，不交给自然语言愿望。

## 常见问题

### 新增规则没有立即生效

当前 session 可能仍使用旧 cached context。使用 `/clear`、`/compact` 或重启后再检查。

### 子目录 CLAUDE.md 启动时没出现

子目录 instructions 按需加载。只有 Claude 访问对应目录中的文件后，它们才进入 context。

### Import 没有加载

检查相对路径是否以引用文件为基准、是否超过递归深度，以及项目是否拒绝过外部 import。

### CLAUDE.md 能否绝对禁止 `git push`

不能把自然语言当成强制边界。使用 permissions deny 或 PreToolUse hook，并保持 Git remote 权限最小化。

## 本章事实与证据

- [CC-025](../SOURCES.md#cc-025) — CLAUDE.md 作用域与加载顺序
- [CC-026](../SOURCES.md#cc-026) — imports
- [CC-027](../SOURCES.md#cc-027) — auto memory 加载与存储
- [CC-028](../SOURCES.md#cc-028) — `/memory` 与重新加载

## 下一章

继续学习 [05 设置与权限](../05-settings-and-permissions/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
