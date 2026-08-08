# 安装与健康检查

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

本章只覆盖 macOS Terminal CLI。目标不是列出所有安装方式，而是选择一个可维护的渠道，完成认证，并确认当前安装能够正常工作。

---

## 学习目标

- 选择 Native Install 或 Homebrew，而不是混用多个渠道。
- 确认 macOS、Claude Code 和账户满足基本要求。
- 使用 version、help、auth 和 doctor 检查安装状态。
- 理解不同安装渠道的更新方式。

## 前置条件

官方列出的 macOS 最低版本为 13.0，内存要求为 4 GB 以上，并需要网络连接。见 [CC-004](../SOURCES.md#cc-004)。

Claude Code 还需要受支持的 Claude 订阅、Anthropic Console 账户或受支持的第三方云提供商。免费 Claude.ai 计划不包含 Claude Code 访问。见 [CC-006](../SOURCES.md#cc-006)。

## 场景示范：第一次在 Mac 上安装 Claude Code

你第一次在 Mac 上准备 Claude Code，还没选定安装渠道。你想挑一个可维护的方式完成安装和首次认证，并能用一两条命令确认安装是健康的。

### 实操

- 按本章「## 先检查是否已经安装」先跑 `claude --version`，避免为已经安装的环境重复安装。
- 按「## 选择安装渠道」在 Native Install 和 Homebrew 之间二选一，不要混用两个渠道。
- 按「## 完成首次认证」运行 `claude` 进入首次登录流程；macOS 凭据存进 Keychain。
- 按「## 运行健康检查」跑 `claude doctor`，确认没有阻止启动的问题。

### 验证

- `claude --version` 输出确定版本号（如 `2.1.214 (Claude Code)`）。
- `claude auth status`（或本机 help 提供的等价命令）显示已登录状态。
- `claude doctor` 没有报错；如有 warning，记录下来以便后续章节对照处理。

## 先检查是否已经安装

如果 `claude` 已经可用，不要为了跟随教程重复安装：

```bash
claude --version
claude --help
```

本手册基线输出为：

```text
2.1.214 (Claude Code)
```

你的版本可以更新，但必须记录实际输出。`--version` 与当前本机证据见 [CC-007](../SOURCES.md#cc-007)。

## 选择安装渠道

### Native Install

Claude Code 官方把 Native Install 标为推荐方式：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

运行前确认 URL 是官方 `claude.ai` 域名。该命令会下载并执行安装脚本，因此不要从第三方文章复制经过改写的地址。

Native Install 默认在后台检查并下载更新，已下载版本在下次启动时生效。官方没有承诺固定检查间隔。见 [CC-001](../SOURCES.md#cc-001) 和 [CC-002](../SOURCES.md#cc-002)。

### Homebrew

如果你已经统一使用 Homebrew 管理开发工具，可以选择 stable cask：

```bash
brew install --cask claude-code
```

也可以明确选择 latest cask：

```bash
brew install --cask claude-code@latest
```

两个 cask 是不同渠道。Homebrew 安装不会由 Claude Code 自动更新，后续应升级同一个 cask：

```bash
# stable cask
brew upgrade claude-code

# latest cask
brew upgrade claude-code@latest
```

对应官方边界见 [CC-003](../SOURCES.md#cc-003)。不要同时安装 Native、stable cask 和 latest cask；多渠道并存会让“当前执行的是哪个二进制”难以判断。

## 完成首次认证

安装后，在练习目录中启动：

```bash
mkdir -p ~/claude-code-handbook-lab
cd ~/claude-code-handbook-lab
claude
```

首次交互式运行会进入登录流程。macOS 上的登录凭据存储在加密的 macOS Keychain 中。浏览器流程可能受环境变量认证、组织策略或已有凭据影响，因此不要把某一版 UI 的完整文字当作固定接口。见 [CC-005](../SOURCES.md#cc-005)。

需要查看当前版本提供的认证子命令时，运行：

```bash
claude auth --help
```

本机 2.1.214 显示 `login`、`logout` 和 `status`。见 [CC-009](../SOURCES.md#cc-009)。不要在教程核验时随意执行 `logout`，它会改变现有认证状态。

## 运行健康检查

先运行终端级只读诊断：

```bash
claude doctor
```

本机 help 说明，`claude doctor` 检查 Claude Code 安装健康状态，并在不显示工作区信任提示的情况下读取当前目录中的 settings 文件。会话内 `/doctor` 才是可以执行修复的完整检查。见 [CC-010](../SOURCES.md#cc-010)。

检查结果应重点回答：

- 当前安装是否可执行。
- 是否发现无效 settings。
- 是否给出明确 warning 或修复建议。

不要把包含私人路径或配置细节的完整 doctor 输出提交到公开仓库。

## 理解更新与重装

### 更新 Native Install

本机 2.1.214 help 把 `claude update` 列为手动检查更新入口，描述为“检查更新，并在有更新时安装”：

```bash
claude update --help
```

本机还显示 `upgrade` 作为同一命令入口，但课程统一使用官方文档列出的 `claude update`。这里只读取 help，没有实际升级。见 [CC-012](../SOURCES.md#cc-012)。

### 安装指定版本

本机 help 显示 `claude install [target]` 的 `target` 可以是 `stable`、`latest` 或具体版本：

```bash
claude install --help
```

这是安装或重装操作，不是普通健康检查。本手册只记录 help，不自动执行。见 [CC-011](../SOURCES.md#cc-011)。

### 更新 Homebrew

Homebrew 安装使用 `brew upgrade`，不要同时依赖 Claude Code 自更新机制。升级哪个 cask，取决于最初安装的是 stable 还是 latest。

## 最小验收

完成本章时，至少能够观察到：

```bash
claude --version
claude --help
claude auth --help
claude doctor
```

成功标准：

- `claude --version` 输出明确版本。
- `claude --help` 能显示 Usage、Options 和 Commands。
- `claude auth --help` 能显示当前版本支持的认证子命令。
- `claude doctor` 没有报告阻止启动的问题；若有，应先处理其明确建议。

## 保留或回退安装

健康检查通过后，保留你明确选择的唯一渠道，并记录它是 Native、Homebrew stable 还是 Homebrew latest。不要为了“确保成功”再叠加第二个渠道。

如果安装失败或误选渠道：

1. 停止继续安装其他渠道。
2. 用 `command -v claude` 和 `claude doctor` 检查当前 launcher。
3. 只按实际安装渠道卸载，再重新选择一种方式。

Native Install 的官方卸载命令为：

```bash
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

Homebrew stable 与 latest 分别使用：

```bash
brew uninstall --cask claude-code
brew uninstall --cask claude-code@latest
```

只运行与你实际安装渠道对应的一组命令。它们用于移除 Claude Code binary/version files，不等于删除 user settings 和 session state；不要把 `rm -rf ~/.claude` 当成普通安装回退。见 [CC-088](../SOURCES.md#cc-088)。

## 常见问题

### `claude: command not found`

先关闭并重新打开 Terminal，再运行：

```bash
command -v claude
```

仍无输出时，回到你实际选择的安装渠道排查，不要叠加第二种安装方式“碰碰运气”。

### 已安装，但版本不是手册基线

这是正常情况。记录 `claude --version`，然后核对 [官方 changelog](https://code.claude.com/docs/en/changelog)。不要为了匹配教程盲目降级。

### doctor 显示 settings 错误

先修复它指出的具体文件。不要直接删除整个 `~/.claude` 目录，也不要把真实 settings 复制到 issue 或公开仓库。

### 浏览器没有出现预期登录页面

可能已经登录，也可能使用环境变量、Console 或组织认证。先查看 `claude auth --help` 和官方 [Authentication](https://code.claude.com/docs/en/authentication)，不要清空 Keychain 作为第一步。

## 本章事实与证据

- [CC-001](../SOURCES.md#cc-001) — Native Install 命令与官方推荐
- [CC-002](../SOURCES.md#cc-002) — Native Install 自动更新边界
- [CC-003](../SOURCES.md#cc-003) — Homebrew stable/latest 与更新方式
- [CC-004](../SOURCES.md#cc-004) — macOS 系统要求
- [CC-005](../SOURCES.md#cc-005) — 首次认证与 Keychain
- [CC-006](../SOURCES.md#cc-006) — 账户条件
- [CC-007](../SOURCES.md#cc-007) — 本机版本与 help 证据
- [CC-009](../SOURCES.md#cc-009) — 本机 auth 子命令
- [CC-010](../SOURCES.md#cc-010) — doctor 职责边界
- [CC-011](../SOURCES.md#cc-011) — install help
- [CC-012](../SOURCES.md#cc-012) — update help
- [CC-088](../SOURCES.md#cc-088) — macOS 卸载与安装回退

## 下一章

继续学习 [02 第一次会话](../02-first-session/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
