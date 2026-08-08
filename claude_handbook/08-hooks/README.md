# Hooks

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Hooks 在 Claude Code 生命周期事件发生时运行自定义处理。本章只创建一个无源码副作用的 command hook：它从 JSON stdin 提取事件名并写入练习日志。你将先独立测试脚本，再让 `claude doctor` 检查配置。

> **Warning**：Hooks 会自动执行本地命令。只使用你已经阅读、理解并限制作用域的脚本；不要从网络复制后直接启用。

---

## 学习目标

- 理解 event → matcher group → handler 的三层模型。
- 区分 command、HTTP、MCP tool、prompt 和 agent handlers。
- 正确处理 command hook 的 JSON stdin、stdout 和 exit code。
- 先用 fixture 测试脚本，再接入 Claude Code。
- 安全删除 hook、日志和本地 settings。

## 前置条件

先完成 [07 Checkpoints 与安全迭代](../07-checkpoints-and-safe-iteration/README.md)。进入练习仓库：

```bash
cd ~/claude-code-handbook-lab/first-session
```

## 场景示范：想拦截一类危险命令

你担心 Claude Code 在某个 prompt 下会执行危险命令（比如 `rm -rf` 或向生产分支 `git push`），单靠 deny rule 不够灵活——你希望在命令真正执行前做一次上下文判断（工作目录、目标分支、参数模式），决定是否放行。

### 实操

- 按本章「## 创建最小脚本」写一个 command hook：读 JSON stdin，检查 `tool_name` 与 `tool_input.command` 字段，按你的规则决定 exit code。
- 按「## 先用固定 fixture 测试」用准备好的 JSON fixture 独立运行脚本，确认对危险命令返回非零退出码。
- 按「## 配置 SessionStart hook」或 PreToolUse 的方式把 hook 挂到 `.claude/settings.local.json`，按「## 先运行 doctor」验证配置无错。

### 验证

- 触发一个含 `rm -rf` 的 prompt，hook 拦截，命令不真正执行，且 Claude 看到 hook 的拒绝信号。
- 同一个 hook 对合法命令（如 `ls`、`cat README.md`）不影响，不产生误拦。
- `cat .claude/settings.local.json` 能看到 hook 配置；删除 hook 后危险命令恢复为正常工具调用行为。

## Hook 配置放在哪里

Hooks 可以来自用户 settings、项目 settings、本地项目 settings、managed settings 或 plugin；部分 skill/subagent 也能在其激活期间带入 hooks。团队共享与本地私有配置的边界不同。见 [CC-044](../SOURCES.md#cc-044)。

本章只使用 `.claude/settings.local.json`，避免把练习自动化共享给其他人。

## Handler 类型

当前官方 reference 定义多种 handler：

- `command`：执行本地命令。
- `http`：向 URL POST JSON。
- `mcp_tool`：调用已连接的 MCP tool。
- `prompt`：让模型做单轮判断。
- `agent`：派生 agent 验证条件。

后四种会引入网络、MCP、模型用量或更复杂生命周期，本章只使用 `command`。见 [CC-045](../SOURCES.md#cc-045)。

## 三层匹配模型

Hook 配置按三层组织：

1. **Event**：何时触发。
2. **Matcher group**：哪些事件实例匹配。
3. **Handler**：匹配后执行什么。

Matcher 语义会随事件类型变化，不能把 tool matcher 规则机械套到所有事件。完整 event/matcher reference 只链接官方 [Hooks reference](https://code.claude.com/docs/en/hooks)，不在本章复制长表。见 [CC-046](../SOURCES.md#cc-046)。

## 创建最小脚本

### 1. 创建目录

```bash
mkdir -p .claude/hooks
```

### 2. 编写只记录事件名的脚本

```bash
cat > .claude/hooks/log-event-name.sh <<'EOF'
#!/bin/sh
set -eu

EVENT=$(
  grep -o '"hook_event_name"[[:space:]]*:[[:space:]]*"[^"]*"' |
    cut -d '"' -f 4
)

umask 077
printf '%s\n' "${EVENT:-unknown}" >> "${CLAUDE_PROJECT_DIR}/.claude/hook-events.log"
EOF

chmod +x .claude/hooks/log-event-name.sh
```

脚本只写 event name，不保存 prompt、transcript、cwd 或环境变量全集。

## 先用固定 fixture 测试

```bash
printf '%s\n' '{"hook_event_name":"SessionStart"}' |
  CLAUDE_PROJECT_DIR="$PWD" .claude/hooks/log-event-name.sh

cat .claude/hook-events.log
```

预期输出：

```text
SessionStart
```

再检查 exit code：

```bash
printf '%s\n' '{"hook_event_name":"Fixture"}' |
  CLAUDE_PROJECT_DIR="$PWD" .claude/hooks/log-event-name.sh
printf '%s\n' "$?"
```

预期为 `0`。

## 配置 SessionStart hook

先确认练习仓库没有已有 local settings：

```bash
if [ -e .claude/settings.local.json ]; then
  printf '%s\n' 'Stop: this exercise requires clean local settings.'
  exit 1
fi
```

如果文件存在，换一个新练习仓库；不要覆盖或自动合并未知配置。

创建本地 settings：

```bash
cat > .claude/settings.local.json <<'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/log-event-name.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
EOF
```

这里省略 matcher，表示不额外过滤 SessionStart。`${CLAUDE_PROJECT_DIR}` 由 Claude Code 在 hook command 中解析为项目根。具体路径占位符和 handler schema 见 [CC-047](../SOURCES.md#cc-047)。

## 先运行 doctor

```bash
claude doctor
```

若 doctor 报告 JSON 或 settings 错误，先修复配置，不要直接启动带错误 hook 的会话。

## 可选：观察实际触发

启动新的交互式会话可能产生模型用量：

```bash
claude --permission-mode manual
```

进入后立即 `/exit`，再检查：

```bash
cat .claude/hook-events.log
```

实际 UI 和 session 行为受认证、settings 与版本影响；本手册只把脚本 fixture 和 doctor 结果视为无副作用实测。

## Command hook 的输入输出

Command hook 从 stdin 接收 JSON。exit code 为 `0` 时，stdout 才按 hook JSON output 处理；如果脚本不需要控制 Claude，保持 stdout 安静最简单。见 [CC-047](../SOURCES.md#cc-047)。

阻断策略必须特别谨慎：

- 在许多事件中，exit code `2` 表示阻断，并把 stderr 反馈给 Claude。
- 其他非零 exit code 通常只是非阻断错误。
- 不同事件对 exit `2` 的效果不同；工具执行后的事件已经不能撤销工具结果。

不要把 `exit 1` 当成通用阻断。事件级语义见 [CC-048](../SOURCES.md#cc-048)。

## Timeout 与自动化边界

Handler 有默认 timeout，也可用 `timeout` 覆盖。不要在高频事件中执行长时间测试、网络请求或递归调用 Claude Code。本章显式使用 10 秒，并只写一行本地日志。见 [CC-049](../SOURCES.md#cc-049)。

## 回退与清理

确认路径后删除本章内容：

```bash
rm -f .claude/hook-events.log
rm -f .claude/hooks/log-event-name.sh
rm -f .claude/settings.local.json
rmdir .claude/hooks 2>/dev/null || true

git status --short
```

如果 `.claude/settings.local.json` 在本章前已经存在，不要覆盖或删除它；改用全新的练习仓库，或手工合并后只移除本章新增块。

## 常见问题

### Hook 脚本直接运行成功，但 Claude Code 中没有触发

先检查 event 名、settings 路径和 doctor 结果。脚本可执行不代表 matcher 和配置结构正确。

### 想阻止危险命令，能否用 `exit 1`

不能把它当作可靠阻断。对支持阻断的事件使用官方定义的 exit `2` 或结构化 decision，并确认该事件的具体语义。

### 是否应该记录完整 stdin 方便调试

不建议。stdin 可能包含 transcript path、cwd、tool input 或 prompt。优先记录最少字段，并在练习结束后删除日志。

### 为什么不使用 HTTP、prompt 或 agent hook

它们引入网络、模型用量或额外信任边界。先掌握可独立测试的 command hook，再按实际需求升级。

## 本章事实与证据

- [CC-044](../SOURCES.md#cc-044) — hook 配置来源与作用域
- [CC-045](../SOURCES.md#cc-045) — handler 类型
- [CC-046](../SOURCES.md#cc-046) — event、matcher 与 handler 模型
- [CC-047](../SOURCES.md#cc-047) — command hook JSON 与路径占位符
- [CC-048](../SOURCES.md#cc-048) — exit code 和阻断边界
- [CC-049](../SOURCES.md#cc-049) — timeout 与高频 hook 风险

## 下一章

继续学习 [09 MCP](../09-mcp/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
