# MCP

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Model Context Protocol（MCP）让 Claude Code 连接外部 tools 和 data sources。本章不连接互联网 server，也不执行 OAuth；只在临时 HOME 中演示一个故意无法启动的 stdio 配置，观察 add、get 和 remove 生命周期。

> **Warning**：MCP server 是你授予 Claude 的新执行边界。添加前必须审查 server 来源、命令、网络访问和凭证范围。

---

## 学习目标

- 区分 stdio、HTTP 与 SSE transport 的当前 CLI 表面。
- 选择 local、user 或 project scope。
- 理解 project `.mcp.json` approval 与普通 workspace trust 不同。
- 使用 add、get 和 remove 管理一个隔离 fixture。
- 避免把 token、header 或真实环境变量写进课程证据。

## 前置条件

先完成 [08 Hooks](../08-hooks/README.md)。本章所有 MCP 命令都使用临时 HOME，不读取真实 MCP 配置。

## 场景示范：试用一个 MCP server 但不污染真实 HOME

你刚拿到团队内部的一个 MCP server，想确认 Claude Code 里的接入路径完整可用：能不能 add、能不能 get、能不能干净 remove。但又不想让这次试用留下任何配置——尤其不希望它落到真实 `~/.claude` 里影响后续工作。

### 实操

- 按本章「## 隔离生命周期练习」第 1 步创建临时 HOME 目录，所有 MCP 命令都显式传 `HOME=$HANDBOOK_MCP_HOME`。
- 按第 2 步用 `/usr/bin/false` 作为 fixture 添加 stdio server，故意让 health check 失败以验证生命周期。
- 依次执行第 2、3、4 步完成 add → get → remove 链路。
- 按第 5 步 `rm -rf` 临时 HOME 并 `unset`。

### 验证

- `ls ~/.claude | grep -i handbook-demo` 在真实 home 下应无残留条目。
- `HOME="$HANDBOOK_MCP_HOME" claude mcp get handbook-demo` 应返回失败，fixture 故意不可连接。
- `echo "$HANDBOOK_MCP_HOME"` 输出为空字符串，环境变量已 `unset`。

## 查看当前 CLI

```bash
claude mcp --help
claude mcp add --help
claude mcp get --help
claude mcp remove --help
```

本机 2.1.214 提供 add、add-from-claude-desktop、add-json、get、help、list、login、logout、remove、reset-project-choices 和 serve 等入口。完整表面见 [CC-050](../SOURCES.md#cc-050)。

## Transport 与 scope

`claude mcp add` 当前 help 接受：

- `stdio`：启动本地子进程，未指定 transport 时的默认值。
- `http`：连接 HTTP URL。
- `sse`：兼容 SSE server。

Scope 可选 `local`、`user` 或 `project`，默认是 `local`。见 [CC-051](../SOURCES.md#cc-051)。

不要根据名字推断实际写入位置或共享策略；需要团队共享时先阅读官方 [MCP](https://code.claude.com/docs/en/mcp) 和项目 diff。

## 隔离生命周期练习

### 1. 创建临时 HOME

```bash
export HANDBOOK_MCP_HOME="$(mktemp -d)"
printf '%s\n' "$HANDBOOK_MCP_HOME"
```

确认输出是新的临时目录。后续每条 MCP 命令都显式传 `HOME`。

### 2. 添加故意失败的 stdio fixture

```bash
HOME="$HANDBOOK_MCP_HOME" \
  claude mcp add --scope user handbook-demo -- /usr/bin/false
```

`/usr/bin/false` 不实现 MCP。这样可以验证配置生命周期，而不会下载 package、打开网络连接或接触真实数据。

### 3. 查看详情

```bash
HOME="$HANDBOOK_MCP_HOME" claude mcp get handbook-demo
```

`get` 会对已批准 server 做 health check，因此该 fixture 应显示失败或不可连接；它不应成功提供 tools。未批准的 project `.mcp.json` server 会显示 pending approval，并且不会连接。见 [CC-052](../SOURCES.md#cc-052)。

### 4. 删除指定 scope

```bash
HOME="$HANDBOOK_MCP_HOME" \
  claude mcp remove --scope user handbook-demo
```

删除时显式写 scope。若省略，当前 help 说明会从包含该名称的 scope 中删除，这可能不是你的预期。见 [CC-054](../SOURCES.md#cc-054)。

### 5. 清理临时 HOME

```bash
rm -rf "$HANDBOOK_MCP_HOME"
unset HANDBOOK_MCP_HOME
```

只删除刚由 `mktemp -d` 创建并打印确认的目录。

## Project approval

本机 help 明确区分：

- 未批准的 `.mcp.json` server 显示 pending，不连接。
- 已批准的 server 在 get/list 时进行 health check。
- `reset-project-choices` 重置当前项目的批准/拒绝选择。

这不是 workspace trust 的别名，也不应通过删除整个项目 state 代替。见 [CC-052](../SOURCES.md#cc-052) 与 [CC-056](../SOURCES.md#cc-056)。

## OAuth 边界

本机 `claude mcp login <name>` 针对 HTTP、SSE 或 claude.ai connector 发起认证；`logout` 清除已存 OAuth 凭据。`--no-browser` 面向无浏览器环境。见 [CC-053](../SOURCES.md#cc-053)。

本章不执行 login/logout：它们会打开外部授权流程并落盘 token。不要把 client secret、Authorization header 或 redirect URL 保存进仓库。

## 会话级 MCP 配置

顶层 `--mcp-config` 可以在启动会话时加载 JSON 文件或字符串；`--strict-mcp-config` 使会话只使用显式提供的 MCP 配置。见 [CC-055](../SOURCES.md#cc-055)。

这与 `claude mcp add` 的持久配置入口不同。临时自动化优先考虑显式 `--mcp-config`，但配置文件仍不得包含明文凭证。

## 结果检查

完成练习后确认：

- 真实 home 没有新增 `handbook-demo`。
- 临时 server 从 add 到 get 再到 remove 的 scope 一致。
- Fixture 从未成功建立 MCP 连接。
- 临时 HOME 已删除。

## 常见问题

### `get` 返回失败

本练习使用 `/usr/bin/false`，失败正是预期结果。目标是验证配置生命周期，不是提供 tools。

### 想换成网络上的公共 server

不要把“公共”当成“可信”。先审查运营方、认证、data retention 和 tool 权限，再在单独获准的练习中连接。

### 能否把 API key 写进 `-e KEY=value`

CLI 支持 env 参数不等于应该提交真实 key。使用秘密管理和最小 scope；证据文件只保存 help，不保存实际值。

### `add-json` 是否支持所有 transport

本机 2.1.214 help 只写 stdio 或 SSE，而普通 `add` 列出 stdio、SSE、HTTP。不要假设两者完全对称。见 [CC-051](../SOURCES.md#cc-051)。

## 本章事实与证据

- [CC-050](../SOURCES.md#cc-050) — MCP 子命令
- [CC-051](../SOURCES.md#cc-051) — add transport 与 scope
- [CC-052](../SOURCES.md#cc-052) — get/list 与 project approval
- [CC-053](../SOURCES.md#cc-053) — OAuth login/logout
- [CC-054](../SOURCES.md#cc-054) — remove scope
- [CC-055](../SOURCES.md#cc-055) — 会话级 MCP config
- [CC-056](../SOURCES.md#cc-056) — reset project choices

## 下一章

继续学习 [10 Subagents 与 worktrees](../10-subagents-and-worktrees/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
