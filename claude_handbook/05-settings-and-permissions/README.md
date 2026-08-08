# 设置与权限

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Settings 决定 Claude Code 如何启动和组合功能，permissions 决定工具调用是否允许，sandbox 为 Bash 提供操作系统级隔离。三者互补，不能用一个宽松开关替代全部边界。

> **Warning**：本章不使用 `bypassPermissions`，不修改 user 或 managed settings，也不把真实 doctor 输出提交到仓库。

---

## 学习目标

- 理解 settings 来源与优先级。
- 区分 permission mode 与 allow/ask/deny rules。
- 知道 protected paths 为什么仍会提示。
- 理解 sandbox 与 permissions 的不同职责。
- 用本地 fixture 和 `claude doctor` 验证配置，并安全删除。

## 前置条件

先完成 [04 指令与记忆](../04-instructions-and-memory/README.md)。进入练习仓库：

```bash
cd ~/claude-code-handbook-lab/first-session
```

## 场景示范：同一命令反复弹授权，想减少摩擦

你在练习仓库里反复跑同一条命令（比如 `npm test`），每次都弹出授权确认。你已经确认这条命令在当前练习仓库是安全的，想把授权决策固化下来，不再每次打断。

### 实操

- 按本章「## Permission rules」在练习仓库的 `.claude/settings.local.json` 里用 `permissions.allow` 列表追加需要放行的命令模式。
- 按「## Plan mode 只读练习」先在 `--permission-mode plan` 下试一次，确认不会真的执行、只是显示计划。
- 按「## 创建本地 deny fixture」的反向思路，再写一条针对危险命令（如 `rm -rf`）的 `permissions.deny`。
- 用 `claude doctor` 验证 settings 文件语法无错。

### 验证

- 在 `--permission-mode manual` 下第二次运行同一条命令，权限弹窗不再出现，但仍能在 `AskUserQuestion` 中临时改主意。
- `cat .claude/settings.local.json` 显示规则已写入；删除规则后授权弹窗重新出现，确认规则确实生效。
- deny 规则覆盖的危险命令仍会被拦截，不会因为 allow 列表而放松。

## Settings 来源

普通 settings 的优先级从高到低是 managed、命令行参数、local、project、user。Permissions 是重要例外：跨 scope 的规则会合并，并按更严格的结果执行，而不是让高层文件简单覆盖全部低层规则。见 [CC-029](../SOURCES.md#cc-029)。

| Scope | 代表位置 | 用途 |
|-------|----------|------|
| User | `~/.claude/settings.json` | 个人跨项目偏好 |
| Project | `.claude/settings.json` | 团队共享配置 |
| Local | `.claude/settings.local.json` | 当前项目的个人配置 |
| Managed | 组织管理位置 | 管理员强制策略 |

本章只使用 Local scope。

## Permission modes

本机 2.1.214 的 `--permission-mode` help 列出：

- `manual`
- `acceptEdits`
- `plan`
- `auto`
- `dontAsk`
- `bypassPermissions`

这些名字不代表每个账户都能使用全部行为。`auto` 受账户、模型、provider 和组织策略影响；`bypassPermissions` 会绕过关键检查，本手册不使用。见 [CC-030](../SOURCES.md#cc-030)。

最常用的学习边界：

- **Manual**：观察每次需要批准的操作。
- **Plan**：只读探索和制定方案。
- **Accept edits**：减少文件编辑提示，但不等于无限 Bash 权限。

## Permission rules

Rules 使用 allow、ask 和 deny 表达工具匹配。一个 scope 的永久 Bash 批准通常写入仓库根 `.claude/settings.local.json`；文件编辑的会话期批准不会自动变成永久跨会话规则。Workspace trust 还会影响项目 allow rules 是否生效。见 [CC-031](../SOURCES.md#cc-031)。

不要从宽泛规则开始。优先：

1. 先 deny 明确禁止的操作。
2. 对不确定操作保持 ask。
3. 只为稳定、最小的命令前缀增加 allow。

## 创建本地 deny fixture

### 1. 确认是否已有 local settings

```bash
if [ -e .claude/settings.local.json ]; then
  printf '%s\n' 'Stop: this exercise requires a clean practice repository.'
  exit 1
fi
```

如果文件已存在，换一个新练习目录，不要覆盖。

### 2. 写入最小配置

```bash
mkdir -p .claude
cat > .claude/settings.local.json <<'EOF'
{
  "permissions": {
    "deny": [
      "Bash(git push *)"
    ]
  }
}
EOF
```

该 fixture 只用于验证配置结构；本章不会运行 `git push`。

### 3. 运行 doctor

```bash
claude doctor
```

本机 help 明确说明，终端级 doctor 会读取当前目录 settings，但不显示 workspace trust prompt；会话内 `/doctor` 才可能执行修复。见 [CC-010](../SOURCES.md#cc-010)。

成功标准：doctor 不报告 JSON/settings schema 错误。不要把包含用户路径或配置细节的完整输出保存到公开 evidence。

## Protected paths

部分配置、VCS 和 shell 启动文件属于 protected paths，即使 permission rules 看似允许，Claude Code 仍会要求额外确认；除 bypass mode 外，这层保护不会被普通 allow rule 消除。见 [CC-032](../SOURCES.md#cc-032)。

`.claude/settings.local.json` 本身属于敏感配置。让 Claude 修改自己的权限规则前，应逐次审查，而不是预批准整个 `.claude/**`。

## Sandbox 与 permissions

Sandbox 为 Bash 提供 macOS Seatbelt 级文件系统/网络隔离；permissions 控制工具是否能被调用。Sandbox 不替代 Edit/Write 等非 Bash 工具的权限，也不取消 protected paths 和 deny rules。见 [CC-033](../SOURCES.md#cc-033)。

会话内可通过 `/sandbox` 查看或配置当前状态。第一次学习只查看，不要把 `sandbox.enabled` 写入真实项目；依赖 Docker、系统工具或本地服务的项目可能需要额外例外。

## Plan mode 只读练习

> **Important**：以下交互式步骤会向模型服务发送请求，并可能计入订阅或 API 用量。本手册作者不自动执行。

启动：

```bash
claude --permission-mode plan
```

发送：

```text
只读取 README.md 和 .claude/settings.local.json。
说明当前 deny rule 的目标，并提出一个验证方案。
不要修改文件，不要运行 git push。
```

观察：

- 是否只做读取与分析。
- 是否准确识别 `Bash(git push *)`。
- 是否没有提出绕过 deny rule。

## 回退与清理

退出会话后：

```bash
rm .claude/settings.local.json
rmdir .claude 2>/dev/null || true
git status --short
```

如果 `.claude` 还有其他练习内容，`rmdir` 会安全失败；不要改成递归删除整个目录。

## 常见问题

### Doctor 接受 JSON，但规则没有生效

检查 workspace trust、scope、matcher 和更高层 managed rules。Schema 有效不等于当前操作必然匹配。

### Allow 与 deny 同时匹配

Permissions 跨 scope 合并，并按更严格结果执行。不要期望 local allow 覆盖 managed/project deny。

### 为什么 Plan mode 仍能读文件

Plan mode 的目标是只读探索，而不是“完全没有工具”。真正可用范围仍受 permission rules、workspace 边界和 sandbox 影响。

### 是否应该使用 bypassPermissions 提高效率

不应把 bypass 当成日常便利模式。它只适合已隔离、无敏感凭证且明确承受风险的环境，本手册练习不使用。

### Sandbox 开启后是否无需 permissions

不是。Sandbox 主要限制 Bash 的 OS 访问；permissions 仍控制所有工具调用和用户批准。

## 本章事实与证据

- [CC-029](../SOURCES.md#cc-029) — settings 优先级与 permission 合并
- [CC-030](../SOURCES.md#cc-030) — permission modes
- [CC-031](../SOURCES.md#cc-031) — rules、持久化与 workspace trust
- [CC-032](../SOURCES.md#cc-032) — protected paths
- [CC-033](../SOURCES.md#cc-033) — sandbox 与 permissions
- [CC-010](../SOURCES.md#cc-010) — doctor 边界

## 下一章

继续学习 [06 Skills 与 slash commands](../06-skills-and-slash-commands/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
