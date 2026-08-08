# 附录 G · 术语反向索引(Glossary Index)

> **本附录定位**:`00-front/03-glossary.md` 定义了 **50 个核心术语**,但分散在多个 7 章主章节中;本附录按字母顺序把所有术语汇总到一页,每个术语一行(中文名 / 英文名 / 类别 / 主要章节)。
>
> 完整定义见 [`00-front/03-glossary.md`](../00-front/03-glossary.md);类型细节见 [`05-appendices/02-type-cards.md`](02-type-cards.md);命令行相关术语见 [`05-appendices/03-commands.md`](03-commands.md)。

## G.1 摘要

50 个术语按 7 大类别组织:**A. 核心抽象(8)** / **B. 引擎核心(8)** / **C. 配置与持久化(8)** / **D. 子系统(8)** / **E. 模式与策略(8)** / **F. UI 交互(5)** / **G. 消息与内容(5)**。所有术语在 glossary 中按编号引用(A.1~G.5),本附录便于"想到英文名反查中文"。

## G.2 速赢

1. **A 核心抽象**:Tool、buildTool、Permission/PermissionResult、PermissionMode、Command、Skill、Plugin、Hook。
2. **B 引擎核心**:QueryEngine、submitMessage、query/queryLoop、StreamingToolExecutor、processUserInput、fetchSystemPromptParts、getUserContext/getSystemContext、recordTranscript。
3. **C 配置与持久化**:settings.json、CLAUDE.md、keybindings.json、sessionId、transcript、MCP、.mcp.json、feature flag。
4. **D 子系统**:MCP / Bridge / Coordinator / Memory / Plugin-Skill / Remote-Server / LSP / Compact。
5. **E 模式与策略**:Plan / Bypass / Auto / PermissionRule / Worktree / Sandbox / Transcript Classifier / Speculative Classifier。
6. **F UI 交互**:REPL / Ink / Vim Mode / Status Line / Output Style。
7. **G 消息与内容**:Message、tool_use/tool_result、SDKMessage、PermissionRequest、Tombstone。

## G.3 术语索引(按中文)

| 中文 | 英文 | 类别 | 编号 | 主要章节 |
|---|---|---|---|---|
| Agent 后台线程 | QueryEngine + AgentTool | D/E | B.1 / E.3 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| AppState | AppState | 横切 | — | [`05-appendices/02-type-cards.md`](02-type-cards.md) |
| Bash 工具 | BashTool | L4/L5 | — | [`03-developer/16-tool-contract.md`](../03-developer/16-tool-contract.md) |
| Bridge 子系统 | Bridge subsystem | D | D.2 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| Bypass 权限 | Bypass Permissions | E | E.2 | [`02-user/07-permissions.md`](../02-user/07-permissions.md) |
| Build-time 开关 | bun:bundle feature() | C | C.8 | [`01-foundation/03-feature-flags.md`](../01-foundation/03-feature-flags.md),[`05-appendices/05-build-flags.md`](05-build-flags.md) |
| CLAUDE.md 记忆 | CLAUDE.md | C | C.2 | [`02-user/08b-claudemd.md`](../02-user/08b-claudemd.md) |
| Compact 子系统 | Compact subsystem | D | D.8 | [`04-architect/31-performance.md`](../04-architect/31-performance.md) |
| Command 命令 | Command / Slash Command | A | A.5 | [`03-developer/18-commands.md`](../03-developer/18-commands.md),[`05-appendices/03-commands.md`](03-commands.md) |
| Coordinator 子系统 | Coordinator subsystem | D | D.3 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| Death cycle / 中断 | abortController / interrupt | B | — | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| Hook 扩展点 | Hook | A | A.8 | [`02-user/08d-hooks.md`](../02-user/08d-hooks.md) |
| Ink 渲染器 | Ink | F | F.2 | [`04-architect/34-patterns.md`](../04-architect/34-patterns.md) |
| LSP 集成 | LSP subsystem | D | D.7 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| Memory 子系统 | Memory subsystem | D | D.4 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| Message 联合 | Message | G | G.1 | [`04-architect/26-data-flow.md`](../04-architect/26-data-flow.md) |
| MCP 协议 | MCP | C | C.6 | [`02-user/13a-mcp.md`](../02-user/13a-mcp.md) |
| MCP 子系统 | MCP subsystem | D | D.1 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| Output Style 输出样式 | Output Style | F | F.5 | [`02-user/10d-output-styles.md`](../02-user/10d-output-styles.md) |
| Permission 结果 | Permission / PermissionResult | A | A.3 | [`04-architect/29-permission.md`](../04-architect/29-permission.md) |
| Permission 模式 | PermissionMode | A | A.4 | [`04-architect/29-permission.md`](../04-architect/29-permission.md) |
| Permission 规则 | Permission Rule | E | E.4 | [`02-user/07-permissions.md`](../02-user/07-permissions.md) |
| PermissionRequest | PermissionRequest | G | G.4 | [`04-architect/29-permission.md`](../04-architect/29-permission.md) |
| Plan 模式 | Plan Mode | E | E.1 | [`02-user/07-permissions.md`](../02-user/07-permissions.md) |
| Plugin 插件 | Plugin | A | A.7 | [`02-user/13c-plugins.md`](../02-user/13c-plugins.md) |
| Plugin-Skill 子系统 | Plugin/Skill subsystem | D | D.5 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| QueryEngine 引擎 | QueryEngine | B | B.1 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| query / queryLoop | query() / queryLoop() | B | B.5 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| REPL 主界面 | REPL | F | F.1 | [`04-architect/34-patterns.md`](../04-architect/34-patterns.md) |
| recordTranscript 持久化 | recordTranscript | B | B.10 | [`04-architect/26-data-flow.md`](../04-architect/26-data-flow.md) |
| Remote / Server 子系统 | Remote/Server subsystem | D | D.6 | [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) |
| SDKMessage SDK 消息 | SDKMessage | G | G.3 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| Session ID | sessionId | C | C.4 | [`04-architect/26-data-flow.md`](../04-architect/26-data-flow.md) |
| Settings 配置 | settings.json | C | C.1 | [`02-user/08a-settings.md`](../02-user/08a-settings.md) |
| Skill 工作流片段 | Skill | A | A.6 | [`02-user/13b-skills.md`](../02-user/13b-skills.md) |
| Speculative Classifier | Speculative Classifier | E | E.8 | [`04-architect/29-permission.md`](../04-architect/29-permission.md) |
| Status Line 状态栏 | Status Line | F | F.4 | [`04-architect/34-patterns.md`](../04-architect/34-patterns.md) |
| StreamingToolExecutor | StreamingToolExecutor | B | B.6 | [`03-developer/16-tool-contract.md`](../03-developer/16-tool-contract.md),[`04-architect/28-streaming.md`](../04-architect/28-streaming.md) |
| submitMessage 一轮 | submitMessage | B | B.3 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| Sandbox 沙箱 | Sandbox | E | E.6 | [`04-architect/30b-sandboxing.md`](../04-architect/30b-sandboxing.md) |
| Tool 工具合约 | Tool | A | A.1 | [`03-developer/16-tool-contract.md`](../03-developer/16-tool-contract.md) |
| Tool Permission Context | ToolPermissionContext | L4 | — | [`05-appendices/02-type-cards.md`](02-type-cards.md) |
| tool_use / tool_result | tool_use / tool_result | G | G.2 | [`04-architect/26-data-flow.md`](../04-architect/26-data-flow.md) |
| Tool Builder | buildTool | A | A.2 | [`03-developer/17-build-a-tool.md`](../03-developer/17-build-a-tool.md) |
| Tombstone 占位消息 | Tombstone | G | G.5 | [`04-architect/28-streaming.md`](../04-architect/28-streaming.md) |
| Transcript Classifier | Transcript Classifier | E | E.7 | [`04-architect/29-permission.md`](../04-architect/29-permission.md) |
| transcript JSONL | transcript | C | C.5 | [`02-user/09-session-history.md`](../02-user/09-session-history.md) |
| UserContext / SystemContext | getUserContext / getSystemContext | B | B.9 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| Vim 模式 | Vim Mode | F | F.3 | [`02-user/05-daily-use.md`](../02-user/05-daily-use.md) |
| Worktree 工作树 | Worktree | E | E.5 | [`02-user/14-memory.md`](../02-user/14-memory.md) |
| 自动决策模式 | Auto Mode | E | E.3 | [`02-user/07-permissions.md`](../02-user/07-permissions.md) |
| 子 Agent 上下文 | createSubagentContext | B | — | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| 快捷键 | keybindings.json | C | C.3 | [`02-user/05-daily-use.md`](../02-user/05-daily-use.md) |
| 提示拼装 | fetchSystemPromptParts | B | B.8 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| 输入处理 | processUserInput | B | B.7 | [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) |
| 项目级 MCP 配置 | .mcp.json | C | C.7 | [`02-user/08c-mcp-config.md`](../02-user/08c-mcp-config.md) |

## G.4 术语索引(按英文)

| 英文 | 中文 | 类别 | 编号 |
|---|---|---|---|
| AppState | AppState | 横切 | — |
| Auto Mode | 自动决策模式 | E | E.3 |
| BashTool | Bash 工具 | L4/L5 | — |
| Bridge subsystem | Bridge 子系统 | D | D.2 |
| buildTool | Tool Builder | A | A.2 |
| bun:bundle feature() | Build-time 开关 | C | C.8 |
| Bypass Permissions | Bypass 权限 | E | E.2 |
| CLAUDE.md | CLAUDE.md 记忆 | C | C.2 |
| Command | Command 命令 | A | A.5 |
| Compact subsystem | Compact 子系统 | D | D.8 |
| Coordinator subsystem | Coordinator 子系统 | D | D.3 |
| fetchSystemPromptParts | 提示拼装 | B | B.8 |
| getUserContext / getSystemContext | UserContext / SystemContext | B | B.9 |
| Hook | Hook 扩展点 | A | A.8 |
| Ink | Ink 渲染器 | F | F.2 |
| interruptBehavior | Death cycle / 中断 | B | — |
| keybindings.json | 快捷键 | C | C.3 |
| LSP subsystem | LSP 集成 | D | D.7 |
| MCP | MCP 协议 | C | C.6 |
| .mcp.json | 项目级 MCP 配置 | C | C.7 |
| MCP subsystem | MCP 子系统 | D | D.1 |
| Memory subsystem | Memory 子系统 | D | D.4 |
| Message | Message 联合 | G | G.1 |
| Output Style | Output Style 输出样式 | F | F.5 |
| Permission | Permission 结果 | A | A.3 |
| PermissionMode | Permission 模式 | A | A.4 |
| Permission Rule | Permission 规则 | E | E.4 |
| PermissionRequest | PermissionRequest | G | G.4 |
| Plan Mode | Plan 模式 | E | E.1 |
| Plugin | Plugin 插件 | A | A.7 |
| Plugin/Skill subsystem | Plugin-Skill 子系统 | D | D.5 |
| processUserInput | 输入处理 | B | B.7 |
| QueryEngine | QueryEngine 引擎 | B | B.1 |
| query() / queryLoop() | query / queryLoop | B | B.5 |
| recordTranscript | recordTranscript 持久化 | B | B.10 |
| Remote/Server subsystem | Remote / Server 子系统 | D | D.6 |
| REPL | REPL 主界面 | F | F.1 |
| Sandbox | Sandbox 沙箱 | E | E.6 |
| SDKMessage | SDKMessage SDK 消息 | G | G.3 |
| sessionId | Session ID | C | C.4 |
| settings.json | Settings 配置 | C | C.1 |
| Skill | Skill 工作流片段 | A | A.6 |
| Speculative Classifier | Speculative Classifier | E | E.8 |
| Status Line | Status Line 状态栏 | F | F.4 |
| StreamingToolExecutor | StreamingToolExecutor | B | B.6 |
| submitMessage | submitMessage 一轮 | B | B.3 |
| Tool | Tool 工具合约 | A | A.1 |
| tool_use / tool_result | tool_use / tool_result | G | G.2 |
| Tombstone | Tombstone 占位消息 | G | G.5 |
| Transcript Classifier | Transcript Classifier | E | E.7 |
| transcript | transcript JSONL | C | C.5 |
| Vim Mode | Vim 模式 | F | F.3 |
| Worktree | Worktree 工作树 | E | E.5 |

## G.5 类别速查(50 个分类汇总)

### A · 核心抽象(8)
A.1 Tool · A.2 buildTool · A.3 Permission/PermissionResult · A.4 PermissionMode · A.5 Command · A.6 Skill · A.7 Plugin · A.8 Hook

### B · 引擎核心(8)
B.1 QueryEngine · B.3 submitMessage · B.5 query/queryLoop · B.6 StreamingToolExecutor · B.7 processUserInput · B.8 fetchSystemPromptParts · B.9 getUserContext/getSystemContext · B.10 recordTranscript

### C · 配置与持久化(8)
C.1 settings.json · C.2 CLAUDE.md · C.3 keybindings.json · C.4 sessionId · C.5 transcript · C.6 MCP · C.7 .mcp.json · C.8 feature flag

### D · 子系统(8)
D.1 MCP subsystem · D.2 Bridge subsystem · D.3 Coordinator subsystem · D.4 Memory subsystem · D.5 Plugin/Skill subsystem · D.6 Remote/Server subsystem · D.7 LSP subsystem · D.8 Compact subsystem

### E · 模式与策略(8)
E.1 Plan Mode · E.2 Bypass Permissions · E.3 Auto Mode · E.4 Permission Rule · E.5 Worktree · E.6 Sandbox · E.7 Transcript Classifier · E.8 Speculative Classifier

### F · UI 交互(5)
F.1 REPL · F.2 Ink · F.3 Vim Mode · F.4 Status Line · F.5 Output Style

### G · 消息与内容(5)
G.1 Message · G.2 tool_use/tool_result · G.3 SDKMessage · G.4 PermissionRequest · G.5 Tombstone

## G.6 引用

- [`00-front/03-glossary.md`](../00-front/03-glossary.md) — 50 术语完整定义(主文档)
- [`00-front/02-three-perspectives.md`](../00-front/02-three-perspectives.md) — 三视角阅读指南
- [`05-appendices/02-type-cards.md`](02-type-cards.md) — 类型卡片(含横切关注点)
- [`05-appendices/01-file-tree.md`](01-file-tree.md) — 文件树索引