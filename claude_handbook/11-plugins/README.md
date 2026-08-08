# Plugins

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Plugin 把 skills、agents、hooks、MCP 等组件组织成可验证、可安装和可更新的分发单元。本章只在临时 HOME 中运行 scaffold 与 strict validation，不添加 marketplace、不安装第三方 plugin，也不创建发布 tag。

> **Warning**：Plugin 可能携带自动执行 hooks、MCP servers 和 agents。安装前审查完整内容，而不仅是名称和 README。

---

## 学习目标

- 区分会话级 plugin 加载与持久 marketplace 安装。
- 使用 `plugin init` 创建最小 scaffold。
- 使用 `plugin validate --strict` 把 warning 变成失败。
- 理解 enable/disable、update 和 uninstall 的不同生命周期。
- 在临时 HOME 中清理全部练习状态。

## 前置条件

先完成 [10 Subagents 与 worktrees](../10-subagents-and-worktrees/README.md)。

## 场景示范：用 `plugin init` 验一个最小 scaffold

你团队在评估要不要把内部的 hooks+agents+commands 收成一个 plugin，但还没决定分发方式。需要先确认最简骨架长什么样、validate 严格度够不够，再决定是否继续投入打包工作。

### 实操

- 按本章「## 临时 scaffold 练习」在临时 HOME 中创建 scaffold。
- 按 `plugin validate --strict` 把 warning 变成 CI 失败的退出码。
- 按「## 生命周期操作」走 enable/disable、update、uninstall 路径，确认本地行为符合预期。

### 验证

- `claude plugin validate --strict <path>` 退出码为 0；带未识别字段或缺 metadata 时退出码非 0。
- 临时 HOME 下能完整列出 scaffold 文件，且 `~/.claude/plugins/` 之外没有持久残留。
- `claude plugin list`（在临时 HOME 下）显示 scaffold 已被识别，但不影响真实安装。

## 查看 CLI 表面

```bash
claude plugin --help
claude plugin init --help
claude plugin validate --help
claude plugin marketplace --help
```

本机 2.1.214 提供 help、init、validate、details、list、install、enable/disable、prune、update、uninstall、marketplace、tag、eval 等入口。见 [CC-063](../SOURCES.md#cc-063)。

## 持久安装与会话级加载

- `claude plugin install` 从已配置 marketplace 持久安装。
- 顶层 `--plugin-dir <path>` 或 `--plugin-url <url>` 只为当前 session 加载，可重复指定。

会话级不等于可信：本地目录和 zip 仍可能包含 hooks 或外部连接。见 [CC-068](../SOURCES.md#cc-068)。

## 临时 scaffold 练习

### 1. 创建临时 HOME

```bash
export HANDBOOK_PLUGIN_HOME="$(mktemp -d)"
printf '%s\n' "$HANDBOOK_PLUGIN_HOME"
```

### 2. 生成最小 plugin

```bash
HOME="$HANDBOOK_PLUGIN_HOME" \
  claude plugin init handbook-demo \
  --author 'Example Author' \
  --author-email 'example@example.invalid' \
  --description 'Temporary handbook validation fixture'
```

本机 help 说明，`plugin init <name>` 在 `~/.claude/skills/<name>/` scaffold plugin，并在下次 session 作为 `<name>@skills-dir` 自动加载。这里的 `~` 被临时 HOME 隔离。见 [CC-064](../SOURCES.md#cc-064)。

### 3. 检查生成内容

```bash
find "$HANDBOOK_PLUGIN_HOME/.claude/skills/handbook-demo" \
  -maxdepth 3 -type f -print
```

逐个阅读文件。不要假设 scaffold 默认值就是你的发布策略。

### 4. Strict validation

```bash
HOME="$HANDBOOK_PLUGIN_HOME" \
  claude plugin validate --strict \
  "$HANDBOOK_PLUGIN_HOME/.claude/skills/handbook-demo"
```

`--strict` 把 unrecognized fields、missing metadata 等 warning 当作 exit 1，适合在 CI 阻止不完整 manifest。见 [CC-065](../SOURCES.md#cc-065)。

### 5. 清理

```bash
rm -rf "$HANDBOOK_PLUGIN_HOME"
unset HANDBOOK_PLUGIN_HOME
```

确认变量指向刚创建的临时目录后再删除。

## Marketplace

本机 `plugin marketplace` 提供 add、list、remove 和 update；source 可以是 URL、path 或 GitHub repo。见 [CC-066](../SOURCES.md#cc-066)。

添加 marketplace 会建立新的供应链信任边界，可能下载和更新代码。本章不运行：

```text
claude plugin marketplace add <source>
claude plugin install <plugin>
```

只有在审查 marketplace source、plugin manifest、组件和更新策略后才执行。

## 生命周期操作

- **Install**：从 marketplace 安装。
- **Disable**：停止启用，不等于删除文件。
- **Enable**：重新启用。
- **Update**：更新到最新版本；本机 help 提示重启后生效。
- **Uninstall**：卸载 plugin。
- **Prune**：清理不再需要的自动安装依赖。

这些入口的本机表面见 [CC-067](../SOURCES.md#cc-067)。不要用 uninstall 代替临时排查；先 disable 更容易回退。

## 发布与 eval 边界

`plugin tag` 会创建 Git tag，`plugin eval` 会运行评测并可能产生模型用量。两者都会改变状态或花费资源，本章只核验 help。见 [CC-069](../SOURCES.md#cc-069)。

发布前至少要求：

- `plugin validate --strict` 通过。
- 所有 hooks 和 scripts 已代码审查。
- 没有硬编码 token、用户路径或私有 URL。
- 版本、manifest 与 marketplace entry 一致。
- 安装和卸载都在 disposable 环境验证。

## 结果检查

- Plugin 只生成在临时 HOME。
- Strict validation 返回成功。
- 没有新增真实 marketplace 或安装项。
- 没有运行 update、uninstall、tag 或 eval。
- 临时 HOME 已删除。

## 常见问题

### `plugin init` 写到了真实 home

立即停止，不要继续加载 session。检查命令是否给每次 `claude plugin` 调用都带了 `HOME="$HANDBOOK_PLUGIN_HOME"`，确认内容后再删除练习目录。

### Validate 成功是否代表 plugin 安全

不代表。Validate 检查 manifest/结构，不替代脚本、hook、MCP 和依赖审计。

### 为什么不用 public marketplace 做示例

公开可访问不代表已经审查，也不能保证未来更新保持相同行为。教程不应默默扩大供应链信任。

### Update 后为什么行为没变化

本机 help 标明 restart required。先退出旧 session，再在受控环境验证新版本。

## 本章事实与证据

- [CC-063](../SOURCES.md#cc-063) — plugin CLI 表面
- [CC-064](../SOURCES.md#cc-064) — scaffold 位置与参数
- [CC-065](../SOURCES.md#cc-065) — strict validation
- [CC-066](../SOURCES.md#cc-066) — marketplace 生命周期
- [CC-067](../SOURCES.md#cc-067) — install/disable/update/uninstall
- [CC-068](../SOURCES.md#cc-068) — 会话级 plugin 加载
- [CC-069](../SOURCES.md#cc-069) — tag 与 eval 边界

## 下一章

继续学习 [12 Headless 与自动化](../12-headless-and-automation/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
