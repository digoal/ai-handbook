---
title: IDE 插件 — 8 个 IDE 全部支持
slug: ch-39-ide-plugins
part: part-iv-integrations
audience: all
reading_time: 7
prerequisites: [ch-30-mcp-server, ch-38-agent-frameworks]
semantica_version: 0.6.0
---

# ch-39 IDE 插件 — 8 个 IDE 全部支持

> Semantica 通过 MCP + `.plugin` 清单 + agents/hooks/skills 资源覆盖 Claude Code / Codex / Continue / Cline / Cursor / Windsurf / VS Code / OpenClaw。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 8 个 IDE 都装 Semantica 插件, 在 IDE 中直接调 record_decision / add_entity / query_graph。
- 走 MCP stdio 协议 (无网络依赖, 本地启动)。

### 1.2 适配矩阵

| IDE | 插件路径 | 接入方式 |
|---|---|---|
| **Claude Code** | `plugins/.claude-plugin/` | MCP stdio |
| **Cursor** | `plugins/.cursor-plugin/` | MCP stdio |
| **Codex** | `plugins/.codex-plugin/` | MCP stdio |
| **Windsurf** | `plugins/.windsurf-plugin/` | MCP stdio |
| **Cline** | `plugins/.cline-plugin/` | MCP stdio |
| **Continue** | `plugins/.continue-plugin/` | MCP stdio |
| **VS Code** | `plugins/.vscode-plugin/` | MCP stdio |
| **OpenClaw** | `plugins/.openclaw-plugin/` | MCP + REST |

### 1.3 一段最小可跑示例 (Claude Code)

```bash
# 1) 克隆 / 安装 semantica
pip install "semantica[llm-anthropic]"

# 2) 在 Claude Code 配置 MCP server
cat > ~/.claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "semantica": {"command": "semantica-mcp"}
  }
}
EOF

# 3) 在 Claude Code 对话框输入
# "用 semantica 的 record_decision 记录一笔贷款决策"
```

### 1.4 何时不用

- 你不用 AI IDE → 直接用 SDK。
- 你要"IDE 多账号 + 团队共享" → 用 Semantica Server + Web ([ch-28-server-api])。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `plugins/.claude-plugin/` — Claude Code 插件清单 (`plugin.json` + commands + agents + hooks + README)。
- `plugins/.cursor-plugin/` — Cursor 插件清单。
- `plugins/.codex-plugin/` — Codex 插件清单。
- `plugins/.windsurf-plugin/` — Windsurf 插件清单。
- `plugins/.cline-plugin/` — Cline 插件清单。
- `plugins/.continue-plugin/` — Continue 配置 (config.json + models / tools / context providers)。
- `plugins/.vscode-plugin/` — VS Code `package.json` + 注册 MCP。
- `plugins/.openclaw-plugin/` — OpenClaw 插件 (MCP + REST 双通道)。
- `plugins/agents/` — 通用 agent 定义 (跨 IDE 复用)。
- `plugins/hooks/` — pre/post 命令钩子。
- `plugins/skills/` — 领域 skill (如 "credit_approval_skill")。

### 2.2 最小复现脚本

```bash
# 1) 列出所有 IDE 插件
ls plugins/ | grep '\.plugin'

# 2) 看 Claude Code 插件清单
cat plugins/.claude-plugin/plugin.json | jq .
```

### 2.3 已知陷阱

- **每个 IDE 的 schema 不一样**: Continue 用 config.json, Cursor 用 .cursorrules, 要分别维护。
- **MCP stdio 重启**: IDE 重启后 MCP server 自动重启, 偶发需手动重启。
- **权限**: 某些 IDE 默认拒绝 MCP 网络权限, 需白名单 `semantica-mcp`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么不学 LangChain 那样做一个"统一 plugin manifest"?**
- 每个 IDE 的元数据 schema 是闭源的、变动的, 强行统一维护成本爆炸。
- Semantica 走"分 IDE 适配 + 共享 MCP server" 的折中路径。

**为什么 plugins/skills/ 与 cookbooks 分开?**
- `plugins/skills/` 是"IDE 提示词+工具绑定", 用户场景化。
- `cookbooks/` 是"完整 Python 教程", 开发者学习用。

### 3.2 与同类对比

| 维度 | Semantica IDE 插件 | LangChain IDE | LlamaIndex IDE |
|---|---|---|---|
| 支持 IDE 数 | 8 | 3 | 2 |
| 协议 | MCP stdio | 各自 | 各自 |
| 共享 skill | ✅ plugins/skills | ❌ | ❌ |

### 3.3 何时重新设计

- IDE > 15 → 抽象 `plugin_generator` 自动生成 8 份模板。
- 出现"插件版本管理" → 引入 semver。

## 跨章引用

- 上一章: [[ch-38-agent-frameworks]]
- 上一章: [[ch-30-mcp-server]]