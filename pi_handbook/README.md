# pi-handbook · 开发者手册

> 从**用户、开发者、架构师**三视角对 `pi`（`@earendil-works/*` monorepo）的源码做系统化深度解读。每章采用三段并列结构（用户视角 / 开发者视角 / 架构师视角），纯 Mermaid 配图。

## 阅读路径

### 🟢 按角色读

- **我想用好 pi**：
  1. [01-overview.md](01-overview.md) —— 项目全景
  2. [02-getting-started.md](02-getting-started.md) —— 安装、构建、测试
  3. [11-tui.md](11-tui.md) —— 终端 UI（特别是"modal vs overlay"与键位）
  4. [16-print-rpc.md](16-print-rpc.md) —— print / rpc / json 三种入口
  5. [18-debug-and-recovery.md](18-debug-and-recovery.md) —— cookbook

- **我想给 pi 写扩展 / 修工具 / 调 bug**：
  1. [03-architecture.md](03-architecture.md) —— 分层与契约
  2. [04-agent-runtime.md](04-agent-runtime.md) —— Agent / AgentLoop / Harness
  3. [06-extensions.md](06-extensions.md) —— 最厚章节：完整描述 100 契约 + 事件 + UI API + 5 个示例拆解
  4. [07-tools.md](07-tools.md) —— 工具系统与 mutation queue
  5. [08-llm-providers.md](08-llm-providers.md) —— Provider/API 双层 + deferred tools
  6. [05-sessions-and-storage.md](05-sessions-and-storage.md) —— 会话树与 JSONL append-only

- **我想评估 pi、为团队引入或扩展核心**：
  1. [01-overview.md](01-overview.md) —— 全景
  2. [03-architecture.md](03-architecture.md) —— 依赖矩阵 + 已知 3 处例外
  3. [04-agent-runtime.md](04-agent-runtime.md) —— reducer / turn / harness 设计与权衡
  4. [09-protocol.md](09-protocol.md) —— CBOR + framing 的三层防御
  5. [10-client-server.md](10-client-server.md) —— client/server 与 Harness 桩
  6. [17-deployment.md](17-deployment.md) —— lockstep 版本 + 供应链硬化

### 🔵 按章节读

| # | 章节 | 重点内容 |
| - | - | - |
| 00 | [glossary](00-glossary.md) | 术语表 |
| 01 | [overview](01-overview.md) | 项目全景 + 设计原则 + 仓库布局 |
| 02 | [getting-started](02-getting-started.md) | 安装 / 构建 / 测试 |
| 03 | [architecture](03-architecture.md) | 9 包依赖矩阵 + 分层 + 启动流（Mermaid #1） |
| 04 | [agent-runtime](04-agent-runtime.md) | Agent / AgentLoop / reducer / Harness（Mermaid #2） |
| 05 | [sessions-and-storage](05-sessions-and-storage.md) | append-only JSONL + 崩溃恢复（Mermaid #8） |
| 06 | [extensions](06-extensions.md) | 100 契约 + 钩子 + UI API（2 Mermaid 图） |
| 07 | [tools](tools.md) | 工具系统 + mutation queue |
| 08 | [llm-providers](08-llm-providers.md) | Provider/API 双层 + deferred tools（Mermaid #5） |
| 09 | [protocol](09-protocol.md) | CBOR + framing 三层防御（Mermaid #6） |
| 10 | [client-server](10-client-server.md) | SDK / 服务端 / 快照 |
| 11 | [tui](11-tui.md) | 渲染管线 + 键盘 + modal/overlay/startup（Mermaid #7） |
| 12 | [compaction](12-compaction.md) | 触发 / 异步中止 / 树指针 |
| 13 | [telemetry](13-telemetry.md) | 契约 + span lifecycle + in-memory 测试 |
| 14 | [settings-and-config](14-settings-and-config.md) | settings / trust / migrations / model runtime |
| 15 | [resources](15-resources.md) | skills / prompts / themes / system prompt 注入 |
| 16 | [print-rpc](16-print-rpc.md) | print / rpc / json 三模式 + 嵌入式 |
| 17 | [deployment](17-deployment.md) | Bun binary / lockstep / CI（Mermaid #9） |
| 18 | [debug-and-recovery](debug-and-recovery.md) | 6 大真实工作流 + cookbook（Mermaid 附 9） |

## 设计约定

1. 每章固定三段并列：`### 用户视角` / `### 开发者视角` / `### 架构师视角`。
2. 每章至少 1 张 Mermaid 图（关键的章节 ≥ 2 张）。
3. 关键代码片段引用绝对 path + 行号：`packages/agent/src/agent.ts:544-591`。
4. 修订了 4 处过时的事实（tool 签名 / deferred tools / release:major / "下层不知上层"过于绝对）。
5. 覆盖 13 处主题盲点（settings / resource discovery / auth & model runtime / compaction / telemetry / protocol robustness / evals / image pipeline / 完整 prompt 管线 / settings 完整生命周期 / project trust 完整生命周期 / deferred tools / 扩展 host 100 契约）。

## 不在范围内

- 历史变更日志：`packages/*/CHANGELOG.md` 自有维护。
- RFC：见 https://rfc.earendil.com/keyword/pi/。
- TUI 长期设计：`tui-plan.md` 在仓库根。
- 第三方集成示例：`packages/coding-agent/examples/`。

## 反馈

- **事实错误**：开 issue / PR。
- **表述不清**：开 issue，标注"handbook" 标签。
- **新增章节**：提 RFC 看是否值得收入。
