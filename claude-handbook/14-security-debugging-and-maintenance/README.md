# 安全、调试与维护

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

本章把 doctor、safe mode、bare mode、debug、auto-mode inspection 和 project purge 放进同一排查顺序：先做只读诊断，再缩小自定义配置，最后才考虑破坏性清理。

> **Warning**：Debug logs、heap dumps、transcripts 和 project state 可能包含 prompt、路径、代码或凭证。不要直接上传或提交。

---

## 学习目标

- 区分 doctor、safe mode 和 bare mode。
- 使用 debug filter 与临时日志定位问题，同时完成脱敏。
- 检查 auto mode classifier 表面，而不读取或提交个人 effective config。
- 理解 `project purge` 会删除什么，并优先使用 dry-run。
- 在 Claude Code 升级后重新核验事实台账。

## 前置条件

先完成 [13 Background agents 与 workflows](../13-background-agents-and-workflows/README.md)。

## 场景示范：行为突然异常，想隔离到最小环境复现

你在某个项目里发现 Claude Code 行为突然异常（比如 plan mode 不再只读、或者 hooks 完全不触发），但其他项目正常。你想确认是项目级配置、Claude Code 本身、还是临时缓存导致。

### 实操

- 按本章「## 排查顺序」从步骤 1–4 走：先记 `claude --version` 和 `pwd`，再跑 `claude doctor`，再切换到最小复现目录确认问题仍存在。
- 按「## Safe mode」用 `--safe-mode --permission-mode plan` 试一次。如果异常消失，说明是 customization（CLAUDE.md、skills、plugins、hooks、MCP 等）触发的。
- 按「## Bare mode」进一步用 `--bare` 排除更多启动层。如果 bare mode 也消失，说明问题在更深层（auto-memory、background prefetches、keychain 等）。
- 按「## Debug 与临时日志」必要时再用 `--debug`，把日志写到 `mktemp` 创建的临时文件，记得先脱敏再删除。

### 验证

- safe mode 与正常模式的差异点对应到具体某类 customization，可以按类别逐项恢复定位。
- bare mode 下的最小复现仍异常时，问题很可能不在配置层，需要查看 Claude Code 升级后的 changelog 或重新核验事实台账。
- 调试日志文件在删除前已脱敏（搜索并替换真实路径、token、用户名）。

## 排查顺序

1. 记录版本和 cwd。
2. 运行只读 doctor。
3. 检查最小复现目录。
4. 用 safe mode 排除 customizations。
5. 必要时用 bare mode 排除更多启动层。
6. 最后才开启 debug，并把日志写到临时目录。
7. 删除状态前先 `project purge --dry-run`。

## Doctor

```bash
claude --version
pwd
claude doctor
```

终端级 doctor 检查安装与 settings，不显示 workspace trust prompt；会话内 `/doctor` 才可执行修复。见 [CC-010](../SOURCES.md#cc-010)。

不要直接运行会话内修复。先阅读建议和目标文件，确保有备份或 Git diff。

## Safe mode

本机 `--safe-mode` 关闭 CLAUDE.md、skills、plugins、hooks、MCP servers、custom commands/agents、output styles、workflows、themes、keybindings 等 customizations；managed settings 仍应用，auth、model、built-in tools 和 permissions 正常工作。见 [CC-082](../SOURCES.md#cc-082)。

可选诊断会产生模型用量：

```bash
claude --safe-mode --permission-mode plan
```

如果问题在 safe mode 消失，按组件逐类恢复，而不是一次全部开启。

## Bare mode

`--bare` 是面向显式、最小启动配置的更窄运行方式。本机 help 说明它跳过 hooks、LSP、plugin sync、attribution、auto-memory、background prefetch、keychain reads 和 CLAUDE.md auto-discovery，并要求通过显式 flags 提供 context/customization。见 [CC-083](../SOURCES.md#cc-083)。

Bare mode 的认证边界与普通 safe mode 不同。不要在不理解 API key/provider 凭据来源时使用它，也不要把它简称为“更强 safe mode”。

## Debug 与临时日志

本机 root help 提供：

```bash
claude --debug '<filter>'
claude --debug-file <path>
```

`--debug-file` 会隐式启用 debug。Filter 可包含或排除类别，例如 help 中的 `api,hooks` 或 `!1p,!file`。见 [CC-084](../SOURCES.md#cc-084)。

安全模板：

```bash
DEBUG_FILE="$(mktemp -t claude-handbook-debug.XXXXXX)"
printf '%s\n' "$DEBUG_FILE"

# 仅在理解模型用量后执行
claude --safe-mode --debug 'hooks,mcp' --debug-file "$DEBUG_FILE"
```

完成后先人工脱敏，再删除：

```bash
rm -f "$DEBUG_FILE"
unset DEBUG_FILE
```

不要把 raw debug file 写进 `handbook/evidence/`。

## Auto mode inspection

本机 `claude auto-mode --help` 提供 config、defaults、critique 和 reset：

- `config` 打印 effective config。
- `defaults` 打印 shipped defaults。
- `critique` 使用 AI 反馈 custom rules。
- `reset` 从 user settings 删除 autoMode section。

见 [CC-085](../SOURCES.md#cc-085)。本章只保存 help：effective config 可能包含个人 settings；critique 会产生模型用量；reset 会修改 user settings。

## Project purge

本机 help 明确说明，`claude project purge` 会删除 project transcripts、tasks、file history 和 config entry；`--dry-run` 只列出范围。见 [CC-061](../SOURCES.md#cc-061)。

```bash
claude project purge --dry-run <path>
```

真正 purge 可用 `--interactive` 逐项确认，也可用 `--yes` 跳过确认；`--all` 影响全部 projects 并与 path 互斥。见 [CC-086](../SOURCES.md#cc-086)。

本手册不执行 purge。优先：

1. `--dry-run` 查看范围。
2. 导出或备份必须保留的信息。
3. 确认 path 不是其他 worktree/shared project。
4. 使用 interactive confirmation，而不是 `--all --yes`。

## 配置二分排查

如果 safe mode 解决问题，按以下顺序恢复：

1. Project `CLAUDE.md`。
2. Project/local settings。
3. Skills 与 agents。
4. Hooks。
5. MCP servers。
6. Plugins 和其他 UI customizations。

每次只恢复一类，重现一次问题并记录结果。不要同时移动真实 `~/.claude` 整个目录。

## 升级后的事实复核

Claude Code 更新后：

```bash
claude --version
claude --help
claude doctor
```

然后按 [VERIFICATION.md](../VERIFICATION.md) 更新：

- `evidence/<version>/`
- [SOURCES.md](../SOURCES.md) 中受影响 CC claims
- 各章节 baseline 与日期
- 命令、flags、默认值和 feature-gated 条件

不应只修改手册首页版本号而不重跑证据。

## 结果检查

- 你能说明 safe 与 bare 关闭范围的不同。
- Debug file 只存在于临时目录，并已删除。
- 没有保存 effective auto-mode config。
- Purge 只运行 help/dry-run，没有删除 state。
- 排查每次只改变一个 customization 类别。

## 常见问题

### Safe mode 中问题仍存在

检查 managed settings、auth、model、built-in tools、permissions 和安装本身。Safe mode 不关闭这些层。

### Bare mode 无法登录

Bare mode 不读取普通 OAuth/keychain。按本机 help 检查显式 API key、apiKeyHelper 或第三方 provider 凭据，不要导出整个环境。

### Debug log 太大

缩小 filter、复现一次后立即停止。不要先采集所有类别再尝试脱敏。

### 想直接删除项目状态重新开始

先用 `/clear`、新 session、safe mode 和 `project purge --dry-run`。Purge 是最后手段，不是通用 cache clean。

## 本章事实与证据

- [CC-010](../SOURCES.md#cc-010) — doctor
- [CC-082](../SOURCES.md#cc-082) — safe mode
- [CC-083](../SOURCES.md#cc-083) — bare mode
- [CC-084](../SOURCES.md#cc-084) — debug flags
- [CC-085](../SOURCES.md#cc-085) — auto-mode subcommands
- [CC-061](../SOURCES.md#cc-061) — project purge 删除范围与 dry-run
- [CC-086](../SOURCES.md#cc-086) — purge 确认与全项目 flags

## 返回入口

[返回手册目录](../README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
