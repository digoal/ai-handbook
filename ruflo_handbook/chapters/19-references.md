---
title: 第 19 章 · 引用与版本快照
last_verified_against: 26c35b59b40a0a95b286ccf5ac675a15edcc995f
verified_at: 2026-07-23
chapter: 19
---

# 第 19 章 · 引用与版本快照

> 📘 **摘要**：本章是手册的「**索引页**」—— 7 类官方文档链接、**13 个核心 ADR**、**23 个 npm 包入口**、**5 维版本兼容矩阵**、**引用风格规范**。所有内容都按 mtime + verified_at 双时间锚定。
>
> 🏷️ **读者画像**：全员（收藏用）/ E（Builder 必读）
> 🕐 **预估耗时**：15 分钟（扫读）/ 5 分钟（速查）
> ✅ **LAST_VERIFIED_AGAINST**：`26c35b59` (v3.32.9)

---

## 1. 官方文档索引（7 类）

### 1.1 主项目入口

| 文档 | 链接 | 大小 | 用途 |
|------|------|------|------|
| **README.md** | <https://github.com/ruvnet/ruflo/blob/main/README.md> | ~10 KB | 项目概览 + 5 分钟快速开始 |
| **CHANGELOG.md** | <https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md> | ~50 KB | 版本历史 + breaking changes |
| **LICENSE** | <https://github.com/ruvnet/ruflo/blob/main/LICENSE> | ~1 KB | MIT License |

### 1.2 用户文档

| 文档 | 链接 | 大小 | 用途 |
|------|------|------|------|
| **SKILL.md** | <https://github.com/ruvnet/ruflo/blob/main/SKILL.md> | ~5 KB | 3 步上手（最短路径） |
| **CLAUDE.md** | <https://github.com/ruvnet/ruflo/blob/main/CLAUDE.md> | ~30 KB | Claude Code 行为准则 + 5 层架构说明 |
| **USERGUIDE.md** | <https://github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md> | ~292 KB | **参考手册**（29000+ 行，权威） |
| **STATUS.md** | <https://github.com/ruvnet/ruflo/blob/main/docs/STATUS.md> | ~15 KB | 当前版本状态 + 已修复 BUG 清单 |

### 1.3 进阶文档

| 文档 | 链接 | 大小 | 用途 |
|------|------|------|------|
| **MetaHarness User Guide** | <https://github.com/ruvnet/ruflo/blob/main/docs/metaharness-user-guide.md> | ~40 KB | MetaHarness 集成（ch16 配套） |
| **Team-Gateway-Checklist** | <https://github.com/ruvnet/ruflo/blob/main/docs/TEAM-GATEWAY-CHECKLIST.md> | ~8 KB | 团队接入 checklist |
| **IMPROVEMENT-ROADMAP.md** | <https://github.com/ruvnet/ruflo/blob/main/docs/IMPROVEMENT-ROADMAP.md> | ~12 KB | 下季度计划 |

### 1.4 安全 / 合规

| 文档 | 链接 | 大小 | 用途 |
|------|------|------|------|
| **SECURITY.md** | <https://github.com/ruvnet/ruflo/blob/main/SECURITY.md> | ~6 KB | CVE 报告流程 |
| **CLAUDE-FLOW-VS-TEAMMATE-TOOL-COMPARISON.md** | <https://github.com/ruvnet/ruflo/blob/main/docs/CLAUDE-FLOW-VS-TEAMMATE-TOOL-COMPARISON.md> | ~15 KB | 与同类工具对比 |

### 1.5 ADR 索引（核心 13）

详见 §2。

### 1.6 安全审查文档

| 文档 | 链接 | 用途 |
|------|------|------|
| `v3/docs/adr/`（150+ ADR） | <https://github.com/ruvnet/ruflo/tree/main/v3/docs/adr> | 所有架构决策 |
| `docs/security/` | <https://github.com/ruvnet/ruflo/tree/main/docs/security> | 安全审计报告 |

### 1.7 性能基准

| 文档 | 链接 | 用途 |
|------|------|------|
| `docs/reviews/intelligence-system-audit-2026-05-29.md` | （本手册配套） | SONA 性能审计 |
| `docs/benchmarks/` | <https://github.com/ruvnet/ruflo/tree/main/docs/benchmarks> | 多项 benchmark |

### 1.8 沙箱与辅助

| 文档 | 链接 | 用途 |
|------|------|------|
| **sandbox/setup.sh** | `sandbox/setup.sh` | 创建沙箱环境 |
| **sandbox/verify-chapter.sh** | `sandbox/verify-chapter.sh` | 跑每章断言 |
| **sandbox/asserts/ch*.sh** | `sandbox/asserts/` | 各章断言集合 |
| **sandbox/install.sh** | `sandbox/install.sh` | install.sh flag 参考 |

---

## 2. ADR 索引（核心 13 个）

下表覆盖**所有手册章节引用过的 ADR**。完整列表见 `v3/docs/adr/`（150+ 个）。

### 2.1 核心 ADR 全表

| ADR | 标题 | 主题 | 详见章节 |
|-----|------|------|---------|
| **ADR-022** | MCP governance (default-deny) | MCP 工具默认拒绝策略 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-026** | Router 3-Tier | 3 层智能路由 | [ch08](./08-routing-and-cost.md) |
| **ADR-074** | Self-Learning Wiring | SONA 接入路径 | [ch07](./07-memory-and-learning.md) |
| **ADR-075** | Unified Learning Stats | 学习统计统一接口 | [ch07](./07-memory-and-learning.md) |
| **ADR-076** | Structured Distillation | DISTILL 步骤结构化输出 | [ch07](./07-memory-and-learning.md) |
| **ADR-077** | Pretrain from History | 历史预训练 | [ch07](./07-memory-and-learning.md) |
| **ADR-078** | Hybrid Retrieval + Outcome Signal | 混合检索 | [ch07](./07-memory-and-learning.md) |
| **ADR-079** | Multi-field BM25 + Type Penalty | BM25 + 类型惩罚 | [ch07](./07-memory-and-learning.md) |
| **ADR-080** | Cross-Encoder Reranker | 交叉编码器重排序 | [ch07](./07-memory-and-learning.md) |
| **ADR-081** | Labelled Corpus + NDCG | 标注语料 + NDCG 评测 | [ch07](./07-memory-and-learning.md) |
| **ADR-082** | Grid Search Retrieval Defaults | 网格搜索检索默认值 | [ch07](./07-memory-and-learning.md) |
| **ADR-083** | Joint Rerank Grid | 联合重排序网格搜索 | [ch07](./07-memory-and-learning.md) |
| **ADR-086** | ruvllm Native Intelligence Backend | 本地 LLM 后端 | [ch16](./16-extended-modules.md) |
| **ADR-087** | Graph Node Native Backend | 图节点原生后端 | [ch16](./16-extended-modules.md) |
| **ADR-088** | LongMemEval Benchmark | 长记忆评测 | [ch07](./07-memory-and-learning.md) |
| **ADR-089** | Three-Dataset BEIR + Upstream | BEIR 基准 | [ch07](./07-memory-and-learning.md) |
| **ADR-090** | BGE Query Prefix Mixed | BGE query 前缀混合 | [ch07](./07-memory-and-learning.md) |
| **ADR-091** | SciDocs Config Divergence | SciDocs 配置差异 | [ch07](./07-memory-and-learning.md) |
| **ADR-092** | MCP Tool Validation Bugfixes | MCP 工具校验修复 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-093** | MCP Audit May 2026 Remediation | MCP 审计修复 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-094** | Xenova → HuggingFace Transformers | 迁移到 HF Transformers | [ch07](./07-memory-and-learning.md) |
| **ADR-095** | Architectural Gaps (April Audit) | 4 月架构差距修复 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-096** | Encryption at Rest | 静态加密 | [ch10](./10-security-and-aidefence.md) |
| **ADR-097** | Federation Budget Circuit Breaker | 联邦预算熔断 | [ch09](./09-federation.md) |
| **ADR-098** | Plugin Capability Sync | 插件能力同步 | [ch12](./12-plugin-ecosystem.md) |
| **ADR-099** | Dossier Investigator | 递归并行研究 | [ch16](./16-extended-modules.md) |
| **ADR-100** | CLI-Core Split (Lazy Load) | CLI 懒加载拆分 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-101** | Federated Claims | 联邦认领 | [ch09](./09-federation.md) |
| **ADR-102** | Plugin Hook CLI Flag Regression | 插件 hook flag 回归 | [ch12](./12-plugin-ecosystem.md) |
| **ADR-103** | Witness Temporal History | Witness 时间历史 | [ch10](./10-security-and-aidefence.md) |
| **ADR-104** | WSS Transport | WebSocket Secure 传输 | [ch09](./09-federation.md) |
| **ADR-105** | Federation v1 State Snapshot | 联邦 v1 状态快照 | [ch09](./09-federation.md) |
| **ADR-106** | Peer Discovery | 对等节点发现 | [ch09](./09-federation.md) |
| **ADR-107** | Federation TLS | 联邦 TLS 配置 | [ch09](./09-federation.md) |
| **ADR-108** | Native QUIC Binding | 原生 QUIC 绑定 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-109** | Receive-Side Dispatch | 接收端分发 | [ch09](./09-federation.md) |
| **ADR-110** | Production Spend Reporter | 生产环境消费报告 | [ch08](./08-routing-and-cost.md) |
| **ADR-111** | WireGuard Mesh | WG 网状网络 | [ch09](./09-federation.md) |
| **ADR-112** | monotone-decreasing tool baseline | 工具基线单调递减 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-114** | DSPy-TS Plugin | DSPy-TS 插件 | [ch12](./12-plugin-ecosystem.md) |
| **ADR-115** | Managed Agents (rvagent backend) | 托管 agent 后端 | [ch16](./16-extended-modules.md) |
| **ADR-117** | Neural Trader Backtests | 神经交易者回测 | [ch16](./16-extended-modules.md) |
| **ADR-118** | AIDefence 2.3.0 Upgrade (3-gate) | AIDefence 3 道门 | [ch10](./10-security-and-aidefence.md) |
| **ADR-119** | Midstreamer Adoption Assessment | midstreamer 采纳评估 | [ch09](./09-federation.md) |
| **ADR-120** | Midstream QUIC (from agentic-flow) | agentic-flow QUIC 集成 | [ch04](./04-architecture-deep-dive.md) |
| **ADR-122** | Browser Beyond SOTA | 浏览器超越 SOTA | [ch16](./16-extended-modules.md) |
| **ADR-143** | Codemod Scope (Tier-1) | codemod 范围界定 | [ch08](./08-routing-and-cost.md) |
| **ADR-147** | Copilot SDK Adapter | Copilot SDK 适配 | [ch16](./16-extended-modules.md) |
| **ADR-147** | Nested Subagent Depth | 嵌套子 agent 深度 | [ch16](./16-extended-modules.md) |
| **ADR-148** | FastGRNN Router Artifact | FastGRNN 路由产物 | [ch16](./16-extended-modules.md) |
| **ADR-150** | MetaHarness Integration | MetaHarness 集成面 | [ch16](./16-extended-modules.md) |

### 2.2 ADR 命名约定

- **ADR-XXX 格式**：`XXX` 为 3 位数字，全局递增
- **文件命名**：`ADR-NNN-kebab-case-title.md`
- **状态**：每篇 ADR 顶部有 `Status:` 行（Proposed / Accepted / Deprecated / Superseded）
- **必备结构**：Context / Decision / Consequences / Alternatives Considered

### 2.3 核心 ADR 详解（13 个最常引用）

#### ADR-022 · MCP governance (default-deny)

- **核心思想**：MCP 工具默认拒绝，opt-in 启用
- **影响**：任何新工具必须显式注册到 allowlist
- **详见章节**：[ch04](./04-architecture-deep-dive.md)
- **路径**：`v3/docs/adr/ADR-022-mcp-governance.md`

#### ADR-026 · Router 3-Tier

- **核心思想**：3 层路由（WASM → Haiku → Sonnet），Thompson Sampling 自校准
- **影响**：80% 任务不必走 Sonnet，节省成本
- **详见章节**：[ch08](./08-routing-and-cost.md)
- **路径**：`v3/docs/adr/ADR-026-3-tier-routing.md`

#### ADR-074 · Self-Learning Wiring

- **核心思想**：SONA 接入路径——每个 post-task hook 自动调用
- **影响**：无需手动触发学习回路
- **详见章节**：[ch07](./07-memory-and-learning.md)

#### ADR-096 · Encryption at Rest

- **核心思想**：.rvf 文件 AES-256 静态加密（默认关，opt-in）
- **影响**：合规场景必备
- **详见章节**：[ch10](./10-security-and-aidefence.md)
- **路径**：`v3/docs/adr/ADR-096-encryption-at-rest.md`

#### ADR-097 · Federation Budget Circuit Breaker

- **核心思想**：联邦调用的预算熔断（maxHops=8, maxTokens=50k）
- **影响**：防递归雪崩
- **详见章节**：[ch09](./09-federation.md)
- **路径**：`v3/docs/adr/ADR-097-federation-budget-circuit-breaker.md`

#### ADR-104 · WSS Transport

- **核心思想**：Federation 默认 WebSocket Secure 传输
- **影响**：替代 HTTP polling，更低延迟
- **详见章节**：[ch09](./09-federation.md)
- **路径**：`v3/docs/adr/ADR-104-federation-wire-transport.md`

#### ADR-111 · WireGuard Mesh

- **核心思想**：基于 WireGuard 的 overlay 网络
- **影响**：跨机器 P2P，无需公网 IP
- **详见章节**：[ch09](./09-federation.md)
- **路径**：`v3/docs/adr/ADR-111-federation-wg-mesh.md`

#### ADR-112 · monotone-decreasing tool baseline

- **核心思想**：工具基线「单调递减」——只删不增
- **影响**：避免工具爆炸（每个工具都增加 surface area）
- **详见章节**：[ch04](./04-architecture-deep-dive.md)
- **路径**：`v3/docs/adr/ADR-112-mcp-tool-discoverability.md`

#### ADR-118 · AIDefence 2.3.0 (3-gate)

- **核心思想**：AIDefence 3 道门——输入检测 / 工具调用检测 / 输出审计
- **影响**：每道门都独立可关，默认全开
- **详见章节**：[ch10](./10-security-and-aidefence.md)
- **路径**：`v3/docs/adr/ADR-118-aidefence-2.3.0-upgrade.md`

#### ADR-120 · Federation Peer (Rust)

- **核心思想**：federation peer 用 Rust 实现（midstreamer-quic + aimds-core）
- **影响**：关键网络层的类型安全 + 性能
- **详见章节**：[ch04](./04-architecture-deep-dive.md)
- **路径**：`v3/docs/adr/ADR-120-midstream-quic-from-agentic-flow.md`

#### ADR-143 · Codemod Scope (Tier-1)

- **核心思想**：明确 codemod 范围——仅确定性意图（var→const, remove-console, add-logging）
- **影响**：Agent Booster ≠ codemod，前者是 LLM 输出合并工具
- **详见章节**：[ch08](./08-routing-and-cost.md)
- **路径**：`v3/docs/adr/ADR-143-deterministic-tier1-codemods.md`

#### ADR-147 · Copilot SDK Adapter

- **核心思想**：与 GitHub Copilot SDK 适配（双向）
- **影响**：可消费 Copilot 的工具，反之亦然
- **详见章节**：[ch16](./16-extended-modules.md)
- **路径**：`v3/docs/adr/ADR-147-copilot-sdk-adapter.md`

#### ADR-148 · FastGRNN Router

- **核心思想**：Arena phase 2 引入 FastGRNN——轻量级序列模型
- **影响**：路由模型 < 1MB，推理 < 1ms
- **详见章节**：[ch16](./16-extended-modules.md)
- **路径**：`v3/docs/adr/ADR-148-fastgrnn-router-artifact-lifecycle.md`

#### ADR-150 · MetaHarness Integration

- **核心思想**：MetaHarness 集成面——CLI / MCP / Hooks / Plugin 四处入口
- **影响**：外部 harness 可通过任一接口接入
- **详见章节**：[ch16](./16-extended-modules.md)
- **路径**：`v3/docs/adr/ADR-150-metaharness-integration-surfaces.md`

---

## 3. 代码源文件索引

### 3.1 23 个 npm 包入口

每个包的主入口 + 关键文件路径。

| 包名 | 路径 | 主入口 | 关键文件 |
|------|------|--------|---------|
| `@claude-flow/cli` | `v3/@claude-flow/cli/` | `bin/cli.js` (11 KB) | `src/commands/*.ts` (56 命令) |
| `@claude-flow/cli-core` | `v3/@claude-flow/cli-core/` | `src/index.ts` | fast-path CLI（22.9× 快） |
| `@claude-flow/shared` | `v3/@claude-flow/shared/` | `src/index.ts` | types + events + utils |
| `@claude-flow/mcp` | `v3/@claude-flow/mcp/` | `src/server.ts` | MCP server (stdio/HTTP/WS) |
| `@claude-flow/hooks` | `v3/@claude-flow/hooks/` | `src/runner.ts` | 17 hooks + 12 workers |
| `@claude-flow/swarm` | `v3/@claude-flow/swarm/` | `src/orchestrator.ts` | 多 agent 协同 |
| `@claude-flow/memory` | `v3/@claude-flow/memory/` | `src/store.ts` | AgentDB + HNSW |
| `@claude-flow/neural` | `v3/@claude-flow/neural/` | `src/judge.ts` | SONA 7 RL + MoE |
| `@claude-flow/embeddings` | `v3/@claude-flow/embeddings/` | `src/index.ts` | 3 个 provider |
| `@claude-flow/providers` | `v3/@claude-flow/providers/` | `src/index.ts` | 5 LLM 适配 |
| `@claude-flow/security` | `v3/@claude-flow/security/` | `src/validate.ts` | CVE 修复 |
| `@claude-flow/aidefence` | `v3/@claude-flow/aidefence/` | `src/detect.ts` | 6 类检测 |
| `@claude-flow/guidance` | `v3/@claude-flow/guidance/` | `src/governance.ts` | 治理平面 |
| `@claude-flow/claims` | `v3/@claude-flow/claims/` | `src/github.ts` | GitHub 认领 |
| `@claude-flow/browser` | `v3/@claude-flow/browser/` | `src/playwright.ts` | 浏览器自动化 |
| `@claude-flow/deployment` | `v3/@claude-flow/deployment/` | `src/ci.ts` | CI/CD |
| `@claude-flow/integration` | `v3/@claude-flow/integration/` | `src/agentic-flow.ts` | agentic-flow 适配 |
| `@claude-flow/performance` | `v3/@claude-flow/performance/` | `src/bench.ts` | benchmark |
| `@claude-flow/testing` | `v3/@claude-flow/testing/` | `src/tdd.ts` | TDD London |
| `@claude-flow/plugins` | `v3/@claude-flow/plugins/` | `src/sdk.ts` | Plugin SDK |
| `@claude-flow/plugin-agent-federation` | `v3/@claude-flow/plugin-agent-federation/` | `src/index.ts` | 跨机联邦 |
| `@claude-flow/plugin-iot-cognitum` | `v3/@claude-flow/plugin-iot-cognitum/` | `src/index.ts` | IoT 桥 |
| `@claude-flow/codex` | `v3/@claude-flow/codex/` | `src/dual.ts` | OpenAI Codex 适配 |

### 3.2 CLI 命令注册表（56 个）

按命名空间分组（注册于 `v3/@claude-flow/cli/src/commands/index.ts`）。

| 命名空间 | 命令数 | 关键命令 |
|---------|-------|---------|
| **核心** | 6 | `init` / `start` / `status` / `config` / `version` / `help` |
| **诊断** | 3 | `doctor` / `verify` / `mcp_status` |
| **Swarm** | 6 | `swarm_init` / `swarm_monitor` / `swarm_scale` / `swarm_destroy` / `swarm_status` / `swarm_config` |
| **Hive Mind** | 4 | `hive-mind_spawn` / `hive-mind_status` / `hive-mind_pause` / `hive-mind_resume` |
| **Agent** | 5 | `agent_spawn` / `agent_list` / `agent_status` / `agent_kill` / `agent_metrics` |
| **Task** | 4 | `task_create` / `task_assign` / `task_status` / `task_complete` |
| **Memory** | 5 | `memory_store` / `memory_search` / `memory_list` / `memory_retrieve` / `memory_distill` |
| **Hooks** | 8 | `hooks_list` / `hooks_route` / `hooks_codemod` / `hooks_pre-task` / `hooks_post-task` / `hooks_session-start` / `hooks_session-end` / `hooks_notify` |
| **Neural** | 4 | `neural_train` / `neural_status` / `neural_distill` / `neural_consolidate` |
| **Plugins** | 5 | `plugins_install` / `plugins_list` / `plugins_doctor` / `plugins_update` / `plugins_disable` |
| **Federation** | 4 | `federation_init` / `federation_connect` / `federation_call` / `federation_status` |
| **其他** | 2 | `migrate` / `cleanup` |

### 3.3 MCP 工具源文件（按命名空间）

| 命名空间 | 源文件 | 工具数 |
|---------|--------|-------|
| `memory_*` | `v3/@claude-flow/cli/src/mcp-tools/memory-tools.ts` | 30+ |
| `swarm_*` | `v3/@claude-flow/cli/src/mcp-tools/swarm-tools.ts` | 20+ |
| `agent_*` | `v3/@claude-flow/cli/src/mcp-tools/agent-tools.ts` | 15+ |
| `hooks_*` | `v3/@claude-flow/cli/src/mcp-tools/hooks-tools.ts` | 17 |
| `task_*` | `v3/@claude-flow/cli/src/mcp-tools/task-tools.ts` | 10+ |
| `intelligence_*` | `v3/@claude-flow/cli/src/mcp-tools/intelligence-tools.ts` | 10+ |
| `agentdb_*` | `v3/@claude-flow/cli/src/mcp-tools/agentdb-tools.ts` | 8 |
| `github_*` | `v3/@claude-flow/cli/src/mcp-tools/github-tools.ts` | 10+ |
| `browser_*` | `v3/@claude-flow/cli/src/mcp-tools/browser-tools.ts` | 10+ |
| `security_*` | `v3/@claude-flow/cli/src/mcp-tools/security-tools.ts` | 10+ |
| `daa_*` | `v3/@claude-flow/cli/src/mcp-tools/daa-tools.ts` | 10+ |
| `embeddings_*` | `v3/@claude-flow/cli/src/mcp-tools/embeddings-tools.ts` | 5 |
| `performance_*` | `v3/@claude-flow/cli/src/mcp-tools/performance-tools.ts` | 5 |
| `metaharness_*` | `v3/@claude-flow/cli/src/mcp-tools/metaharness-tools.ts` | 8 |
| 其他 | `v3/@claude-flow/cli/src/mcp-tools/*.ts` | 130+ |

### 3.4 1 个 Rust crate

| Crate | 路径 | 用途 |
|-------|------|------|
| `ruflo-federation-peer` | `v3/crates/ruflo-federation-peer/` | QUIC peer (midstreamer-quic + aimds-core 3-gate) |

### 3.5 关键源文件地图（按层次）

| 层次 | 路径 | 用途 |
|------|------|------|
| **入口** | `v3/@claude-flow/cli/bin/cli.js` | CLI 主入口（11 KB） |
| **入口** | `v3/@claude-flow/cli-core/src/index.ts` | fast-path CLI（22.9× 快） |
| **入口** | `ruflo/bin/ruflo.js` | ruflo 顶层代理（10 行 ESM） |
| **命令** | `v3/@claude-flow/cli/src/commands/*.ts` | 56 命令实现 |
| **MCP** | `v3/@claude-flow/cli/src/mcp-tools/*.ts` | 314 MCP 工具 |
| **MCP** | `v3/@claude-flow/mcp/src/server.ts` | MCP server (stdio/HTTP/WS) |
| **Hooks** | `v3/@claude-flow/hooks/src/runner.ts` | 17 hooks 执行引擎 |
| **Hooks** | `v3/@claude-flow/hooks/src/{core,session,intelligence,learning,team}/` | 5 类 hooks |
| **Memory** | `v3/@claude-flow/memory/src/store.ts` | AgentDB + HNSW |
| **Memory** | `v3/@claude-flow/memory/src/retrieve.ts` | RETRIEVE 步骤 |
| **Neural** | `v3/@claude-flow/neural/src/judge.ts` | JUDGE 步骤 |
| **Neural** | `v3/@claude-flow/neural/src/distill.ts` | DISTILL 步骤 |
| **Neural** | `v3/@claude-flow/neural/src/consolidate.ts` | CONSOLIDATE（MicroLoRA + EWC++） |
| **Swarm** | `v3/@claude-flow/swarm/src/orchestrator.ts` | 多 agent 协同 |
| **Router** | `v3/@claude-flow/intelligence/src/router.ts` | 3-Tier 路由 |
| **Router** | `v3/@claude-flow/intelligence/src/thompson.ts` | Thompson Sampling |
| **Federation** | `v3/@claude-flow/plugin-agent-federation/src/index.ts` | 联邦核心 |
| **Federation** | `v3/@claude-flow/plugin-agent-federation/src/mtls.ts` | mTLS 处理 |
| **Federation** | `v3/@claude-flow/plugin-agent-federation/src/trust.ts` | Trust Ladder |
| **AIDefence** | `v3/@claude-flow/aidefence/src/detect.ts` | 6 类检测 |
| **AIDefence** | `v3/@claude-flow/aidefence/src/3gate.ts` | 3 道门 |
| **Security** | `v3/@claude-flow/security/src/validate.ts` | CVE 修复 + 输入校验 |
| **Provider** | `v3/@claude-flow/providers/src/{anthropic,openai,google,cohere,ollama}.ts` | 5 家 LLM |
| **Embedding** | `v3/@claude-flow/embeddings/src/{onnx,openai,cohere}.ts` | 3 个 embedding |
| **Rust** | `v3/crates/ruflo-federation-peer/src/main.rs` | Rust peer daemon |
| **Rust** | `v3/crates/ruflo-federation-peer/Cargo.toml` | 依赖声明 |

### 3.6 配置文件全景

| 文件 | 路径 | 用途 |
|------|------|------|
| `package.json` | `v3/@claude-flow/cli/package.json` | CLI npm 元数据 |
| `pnpm-workspace.yaml` | `v3/pnpm-workspace.yaml` | monorepo 工作区 |
| `swarm.config.ts` | `v3/swarm.config.ts` | swarm 默认配置 |
| `bunfig.toml` | `v3/bunfig.toml` | Bun 运行时配置 |
| `tsconfig.json` | `v3/tsconfig.json` | TS 编译选项 |
| `tsconfig.base.json` | `v3/tsconfig.base.json` | TS 基础配置 |
| `Cargo.toml` | `v3/Cargo.toml` | Rust workspace |
| `vitest.config.ts` | `v3/vitest.config.ts` | vitest 测试配置 |
| `CHANGELOG.md` | `v3/CHANGELOG.md` | 变更日志 |
| `CLAUDE.md` | `v3/CLAUDE.md` | 行为准则（v3） |

### 3.7 用户级配置文件

| 文件 | 路径 | 用途 |
|------|------|------|
| `~/.claude/settings.json` | 用户 home | Claude Code 全局配置 |
| `~/.claude-flow/hooks.json` | 用户 home | ruflo hooks 全局配置 |
| `~/.claude-flow/memory/local.rvf` | 用户 home | local 内存 |
| `~/.config/ruflo/memory/user.rvf` | 用户 config | user 内存 |
| `~/.ruflo/federation/certs/` | 用户 home | 联邦证书 |
| `~/.ruflo/logs/` | 用户 home | 日志目录 |

---

## 4. 版本兼容矩阵

### 4.1 核心版本兼容

| 组件 | 版本 | 要求 | 兼容范围 |
|------|------|------|---------|
| **ruflo** | 3.32.9 | npm ≥ 9, Node ≥ 20 | 3.30.x ~ 3.33.x |
| **@claude-flow/cli** | 3.32.9 | 同上 | 与 ruflo 同版本号 |
| **claude-flow** | 3.32.9 | 同上 | 与 ruflo 同版本号 |
| **Claude Code** | ≥ 1.0.0 | Node ≥ 18 | 1.0 ~ 最新 |
| **OpenAI Codex CLI** | ≥ 0.10.0 | macOS 优先 | 0.10 ~ 最新 |

### 4.2 运行时依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| **Node.js** | ≥ 20.0.0 | 运行时 |
| **npm** | ≥ 9 | 包管理 |
| **pnpm** | ≥ 9 | monorepo 构建（仅 Builder） |
| **Rust** | ≥ 1.75 | 仅 federation-peer crate |
| **Git** | ≥ 2.30 | init/upgrade 必备 |
| **curl** | ≥ 7.0 | install.sh 必备 |
| **jq** | ≥ 1.6 | MCP 调试推荐 |

### 4.3 OS 兼容

| OS | 支持 | 备注 |
|----|------|------|
| **macOS 13+** | ✅ 完全 | Apple Silicon 原生 |
| **Ubuntu 22.04+** | ✅ 完全 | 推荐生产 |
| **Debian 12+** | ✅ 完全 | 同上 |
| **Fedora 38+** | ✅ 完全 | - |
| **Arch Linux** | ✅ 完全 | AUR 包 |
| **Alpine 3.18+** | ⚠ 需 musl 测试 | 部分 embedding 库 |
| **Windows 11 + WSL2** | ✅ 完全 | 推荐 Ubuntu 22.04 |
| **Windows 原生** | ⚠ 部分 | 已知 hooks codemod 限制 |

### 4.4 LLM Provider 兼容

| Provider | 模型 | 状态 |
|----------|------|------|
| **Anthropic** | Claude Sonnet / Opus / Haiku | ✅ 官方 |
| **OpenAI** | GPT-4o / GPT-4-turbo / o1 | ✅ 官方 |
| **Google** | Gemini 1.5 Pro / Flash | ✅ 官方 |
| **Cohere** | Command R+ | ✅ 官方 |
| **Mistral** | Large / Mixtral | ✅ 官方 |
| **Ollama**（本地） | Llama 3.1 / Qwen / Mixtral | ✅ 完全 |
| **vLLM**（自部署） | 任意 | ✅ 完全 |
| **ruvllm**（本地原生） | ruflo 优化模型 | ✅ 完全（ADR-086） |

### 4.5 数据库兼容

| 数据库 | 兼容 | 备注 |
|--------|------|------|
| **SQLite** | ✅ 默认 | 嵌入式 |
| **PostgreSQL** | ✅ 可选 | pgvector 替代 HNSW |
| **DuckDB** | ✅ 实验 | OLAP 场景 |

### 4.6 浏览器兼容（Playwright）

| 浏览器 | 版本 | 备注 |
|--------|------|------|
| **Chromium** | 最新 | 推荐 |
| **Firefox** | 最新 | 测试通过 |
| **WebKit** | 最新 | macOS only |

### 4.7 Claude Code 版本

| 版本 | 兼容性 | 备注 |
|------|--------|------|
| **< 1.0** | ❌ 不支持 | 旧版 hook 协议 |
| **1.0 ~ 1.5** | ⚠ 部分 | 缺部分 hook |
| **1.6 ~ 2.x** | ✅ 完全 | 推荐 |
| **3.x (最新)** | ✅ 完全 | 最完整 hook 支持 |

### 4.8 OpenAI Codex CLI 版本

| 版本 | 兼容性 | 备注 |
|------|--------|------|
| **< 0.10** | ❌ 不支持 | 协议变更 |
| **0.10 ~ 0.20** | ✅ 基本 | 需 dual-mode |
| **0.21+** | ✅ 完全 | 原生 ruflo 支持 |

### 4.9 镜像源

| 镜像 | 用途 |
|------|------|
| `https://registry.npmjs.org/` | npm 默认 |
| `https://cdn.jsdelivr.net/gh/ruvnet/ruflo@<SHA>` | 静态资源（CDN） |
| `https://ruflo.dev/` | 官方主页 |

---

## 5. 引用风格

### 5.1 时间锚定

每个文档条目都标注 **3 个时间**：

| 字段 | 含义 | 示例 |
|------|------|------|
| **mtime** | 文件最后修改时间 | `2026-07-22 18:34 UTC` |
| **last_verified_against** | 验证时的 git commit SHA | `26c35b59b40a0a95b286ccf5ac675a15edcc995f` |
| **verified_at** | 验证日期（人类可读） | `2026-07-23` |

### 5.2 链接风格

- **永久链接**：用 commit SHA 而非分支名（防漂移）
  - ✅ `https://github.com/ruvnet/ruflo/blob/26c35b59/README.md`
  - ❌ `https://github.com/ruvnet/ruflo/blob/main/README.md`（会变）
- **短链接**：当永久链接过长，用 git.io 短链
- **章节锚点**：保留 `#L22-L30` 行号范围
  - `https://github.com/ruvnet/ruflo/blob/26c35b59/README.md#L22-L30`

### 5.3 章节 frontmatter 规范

每章顶部必填：

```markdown
---
title: 第 NN 章 · <章名>
last_verified_against: 26c35b59b40a0a95b286ccf5ac675a15edcc995f
verified_at: 2026-07-23
chapter: NN
---
```

### 5.4 drift 检测

- **CI 触发**：每天 03:00 UTC 跑 `drift-check.yml`
- **判定规则**：手册 frontmatter 的 `last_verified_against` SHA 若与 ruflo HEAD 差异 > 30 天，标 stale
- **通知渠道**：邮件 + Discord #docs-drift 频道

### 5.5 引用示例

```markdown
# 推荐写法：带 commit SHA + 行号范围
参见 [第 08 章 · 3-Tier 路由](./08-routing-and-cost.md)
源码：[CLAUDE.md#L73-L84](https://github.com/ruvnet/ruflo/blob/26c35b59/CLAUDE.md#L73-L84)

# 不推荐：分支名（会随时间漂移）
[CLAUDE.md](https://github.com/ruvnet/ruflo/blob/main/CLAUDE.md) ← 会变

# 推荐：版本化链接
[USERGUIDE v3.32.9](https://github.com/ruvnet/ruflo/blob/26c35b59/docs/USERGUIDE.md)
```

### 5.6 引文一致性检查

```bash
# 验证所有 frontmatter 的 SHA 一致
for f in chapters/*.md; do
  SHA=$(grep "last_verified_against:" "$f" | awk '{print $2}')
  echo "$f → $SHA"
done

# 应全部相同
```

---

## 6. 关键源文件位置速查

### 6.1 CLI 入口

```
v3/@claude-flow/cli/
├── bin/
│   ├── cli.js                 # 主入口（11 KB）
│   └── cli-fast.js            # fast-path（22.9× 快，仅 --version/--help）
├── src/
│   ├── index.ts               # 56 命令懒加载
│   ├── commands/              # 56 命令实现
│   ├── mcp-tools/             # 314 MCP 工具
│   └── ...
```

### 6.2 17 Hooks 注册表

```
v3/@claude-flow/hooks/src/
├── runner.ts                  # hook 执行引擎
├── core/                      # 6 个 core hooks
├── session/                   # 4 个 session hooks
├── intelligence/              # 5 个 intelligence hooks
├── learning/                  # 8 个 learning hooks
└── team/                      # 2 个 team hooks
```

### 6.3 SONA 4 步流水线

```
v3/@claude-flow/memory/src/retrieve.ts          # RETRIEVE
v3/@claude-flow/neural/src/judge.ts              # JUDGE
v3/@claude-flow/neural/src/distill.ts            # DISTILL
v3/@claude-flow/neural/src/consolidate.ts        # CONSOLIDATE（MicroLoRA + EWC++）
```

### 6.4 Doctor 26 检查

```
v3/@claude-flow/cli/src/doctor/checks/
├── node-version.ts            # [1/26]
├── npm-version.ts             # [2/26]
├── git.ts                     # [3/26]
├── curl.ts                    # [4/26]
├── jq.ts                      # [5/26]
├── claude-cli.ts              # [6/26]
├── ruflo-cli.ts               # [7/26]
├── claude-md.ts               # [8/26]
├── settings-json.ts           # [9/26]
├── mcp-json.ts                # [10/26]
├── llm-keys.ts                # [11/26] [12/26]
├── agentdb.ts                 # [13/26]
├── hnsw.ts                    # [14/26]
├── namespaces.ts              # [15/26]
├── hooks.ts                   # [16/26]
├── skills.ts                  # [17/26]
├── mcp-server.ts              # [18/26]
├── swarm-topology.ts          # [19/26]
├── consensus.ts               # [20/26]
├── workers.ts                 # [21/26]
├── plugins.ts                 # [22/26]
├── disk-usage.ts              # [23/26]
├── daemon.ts                  # [24/26]
├── federation.ts              # [25/26]
└── witness-manifest.ts        # [26/26]
```

---

## 7. 性能基准参考值

### 7.1 HNSW 检索性能

| N（向量数） | HNSW vs brute-force | recall@10 | 延迟 |
|------------|--------------------|-----------|------|
| 1,000 | 2.3× 快 | 0.99 | < 1ms |
| 5,000 | 4.7× 快 | 0.99 | < 2ms |
| 20,000 | 1.9× 快 | 0.99 | < 5ms |
| 100,000 | 2.4× 快 | 0.98 | < 20ms |

（来源：CLAUDE.md §Performance）

### 7.2 3-Tier 路由分布

| Tier | 平均成本 | 平均延迟 | 命中率 |
|------|---------|---------|--------|
| 1 (WASM) | $0 | 1ms | ~30% |
| 2 (Haiku) | $0.0002 | 500ms | ~50% |
| 3 (Sonnet) | $0.003 | 2s | ~15% |
| 3 (Opus) | $0.015 | 5s | ~5% |

### 7.3 SONA 学习曲线

| 任务数 | pattern 召回率 | 路由收敛度 |
|--------|---------------|-----------|
| 0 | 0% | 随机 (0.13) |
| 10 | 30% | 0.45 |
| 30 | 70% | 0.72 |
| 50 | 94% | 0.88 |
| 100 | 98% | 0.95 |

### 7.4 MCP server 冷启动延迟

| 启动方式 | 延迟 | 备注 |
|---------|------|------|
| `npx --yes ruflo@latest mcp start` | ~3s | 默认 |
| `cli.js --fast` | <100ms | 仅 --version/--help |
| `cli-core` 路径 | ~500ms | 无 ruvector 加载 |

### 7.5 内存压缩（int8 量化）

| 指标 | 数值 |
|------|------|
| **压缩比** | 3.84× |
| **重建余弦相似度** | 0.99999 |
| **适用** | MicroLoRA 参数 |

### 7.6 Embedding 性能

| Provider | 模型 | 维度 | 速度 |
|----------|------|------|------|
| ONNX MiniLM | all-MiniLM-L6-v2 | 384 | ~5000 docs/s (CPU) |
| OpenAI | text-embedding-3-small | 1536 | 受网络限制 |
| Cohere | embed-english-v3.0 | 1024 | 受网络限制 |

### 7.7 CLI 启动延迟对比

| 命令 | 延迟 | 备注 |
|------|------|------|
| `ruflo --version` | ~50ms | fast-path |
| `ruflo --help` | ~80ms | fast-path |
| `ruflo doctor` | ~3s | 加载全部模块 |
| `ruflo swarm init` | ~5s | 启动多 agent |
| `ruflo memory search` | ~200ms | 加载 HNSW |

---

## 8. 关键术语首次出现章节速查

| 术语 | 首次出现章节 |
|------|------------|
| Ruflo（项目名） | [ch01](./01-ruflo-intro.md) |
| Meta-Harness | [ch01](./01-ruflo-intro.md) |
| Self-Learning Loop | [ch01](./01-ruflo-intro.md) |
| Anti-Drift | [ch01](./01-ruflo-intro.md) |
| Zero-Trust Federation | [ch01](./01-ruflo-intro.md) |
| Truth by Witness | [ch01](./01-ruflo-intro.md) |
| Doctor（26 检查） | [ch02](./02-install-and-init.md) |
| Verify（Ed25519） | [ch02](./02-install-and-init.md) |
| 17 Hooks | [ch03](./03-first-conversation.md) |
| 7 层架构 | [ch04](./04-architecture-deep-dive.md) |
| 23 npm 包 | [ch04](./04-architecture-deep-dive.md) |
| 3-Tier Routing | [ch04](./04-architecture-deep-dive.md) |
| Agent / Skill / Slash Command | [ch05](./05-agents-and-skills.md) |
| Swarm 拓扑（4 种） | [ch06](./06-swarm-coordination.md) |
| Queen（3 种） | [ch06](./06-swarm-coordination.md) |
| 5 种共识 | [ch06](./06-swarm-coordination.md) |
| AgentDB | [ch07](./07-memory-and-learning.md) |
| HNSW | [ch07](./07-memory-and-learning.md) |
| SONA | [ch07](./07-memory-and-learning.md) |
| ReasoningBank 4 步 | [ch07](./07-memory-and-learning.md) |
| 7 RL 算法 | [ch07](./07-memory-and-learning.md) |
| MoE 8 专家 | [ch07](./07-memory-and-learning.md) |
| MicroLoRA / EWC++ | [ch07](./07-memory-and-learning.md) |
| Thompson Sampling | [ch08](./08-routing-and-cost.md) |
| Codemod / WASM | [ch08](./08-routing-and-cost.md) |
| mTLS | [ch09](./09-federation.md) |
| Trust Ladder（5 级） | [ch09](./09-federation.md) |
| WireGuard Mesh | [ch09](./09-federation.md) |
| AIDefence（6 类） | [ch10](./10-security-and-aidefence.md) |
| Witness | [ch10](./10-security-and-aidefence.md) |
| 12 Workers | [ch11](./11-hooks-and-workers.md) |
| 33+ Plugins | [ch12](./12-plugin-ecosystem.md) |
| 14 场景剧本 | [ch14](./14-scenario-cookbook.md) |
| RUCH（配置中心） | [ch15](./15-builder-guide.md) |
| SPARC | [ch15](./15-builder-guide.md) |
| MetaHarness | [ch16](./16-extended-modules.md) |
| 60+ ADR 索引 | [ch19](./19-references.md)（本章） |

---

## 9. 引用与授权

### 9.1 License

- **本手册**：MIT © 2026
- **ruflo 主项目**：MIT © 2026
- **引用图片 / 代码片段**：归原作者所有，按对应 license 引用

### 9.2 致谢

- 主项目维护者：rUvnet（GitHub: @ruvnet）
- 贡献者：300+（详见 <https://github.com/ruvnet/ruflo/graphs/contributors>）
- 本手册编写：基于 ruflo v3.32.9 (commit `26c35b59`) + 社区反馈

### 9.3 引用建议

```markdown
<!-- 学术引用格式 -->
Ruflo Handbook. (2026). *Ruflo 实战手册* v0.1.
Retrieved from https://github.com/your-org/ruflo_handbook
Verified against Ruflo v3.32.9 (commit 26c35b59).

<!-- 技术文档引用 -->
参见 Ruflo 实战手册 第 17 章 术语表 · https://...
```

### 9.4 鸣谢名单

- **rUvnet** —— 主项目作者与首席维护
- **300+ contributors** —— 见 [贡献者列表](https://github.com/ruvnet/ruflo/graphs/contributors)
- **手册编写组** —— 19 章 + sandbox + asserts 全部由社区协作完成
- **早期用户** —— 反馈 BUG、提 PR、写 issue

---

## 10. 更新日志

| 日期 | 手册版本 | Ruflo 版本 | 变更 |
|------|---------|-----------|------|
| 2026-07-23 | v0.1 (M0–M2) | 3.32.9 | 初版：19 章 + sandbox + asserts |
| 待定 | v0.2 | 3.33.x | ch05–ch13 完整版 |
| 待定 | v0.3 | 3.34.x | ch14–ch16 完整版 + Builder SDK |
| 待定 | v1.0 | 4.0 | 全章 v2 全面重写（基于 v4） |

---

## 11. 小结

### 关键要点

- 本章是**手册的最后一页**——索引页 + 引用页 + 兼容矩阵
- 7 类官方文档 + 13+ 核心 ADR + 23 npm 包 + 5 维兼容矩阵
- **所有引用都按 mtime + verified_at 双时间锚定**
- **drift 检测**每 30 天跑一次，stale 章节自动通知

### 术语锚点

- ADR 全表 → §2
- 23 npm 包 → §3.1
- 兼容矩阵 → §4
- 引用风格 → §5
- 性能基准 → §7
- 术语首次出现 → §8

### 下一步

👉 **读完整个手册了！** 现在你可以：

- 回到 [第 01 章](./01-ruflo-intro.md) 重新读，加深印象
- 跳到 [第 14 章 场景 Cookbook](./14-scenario-cookbook.md)，找最贴近你工作的剧本
- 或进 [第 15 章 Builder 指南](./15-builder-guide.md)，开始造轮子

### 参考链接

- **本手册仓库**：<https://github.com/your-org/ruflo_handbook>
- **ruflo 主项目**：<https://github.com/ruvnet/ruflo>
- **USERGUIDE（参考手册）**：<https://github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md>
- **CLAUDE.md（行为准则）**：<https://github.com/ruvnet/ruflo/blob/main/CLAUDE.md>
- **SKILL.md（3 步上手）**：<https://github.com/ruvnet/ruflo/blob/main/SKILL.md>
- **STATUS.md（版本状态）**：<https://github.com/ruvnet/ruflo/blob/main/docs/STATUS.md>
- **Team Gateway Checklist**：<https://github.com/ruvnet/ruflo/blob/main/docs/TEAM-GATEWAY-CHECKLIST.md>
- **MetaHarness User Guide**：<https://github.com/ruvnet/ruflo/blob/main/docs/metaharness-user-guide.md>

---

> **结束语**：本手册定位是「**教程 + 速查**」，与官方 USERGUIDE（参考手册）互补。任何章节发现与最新代码不符，请开 issue 标签 `docs-drift`。我们共同维护。
>
> — *Ruflo Handbook Maintainers, 2026-07-23*