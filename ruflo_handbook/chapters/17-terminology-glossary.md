---
title: 第 17 章 · 术语表（A–Z 中文对照）
last_verified_against: 26c35b59b40a0a95b286ccf5ac675a15edcc995f
verified_at: 2026-07-23
chapter: 17
---

# 第 17 章 · 术语表（A–Z 中文对照）

> 📘 **摘要**：本术语表覆盖 ruflo 实战手册全部 19 章出现的核心概念。每个条目包含：英文名、中文释义、一句话定义、首次出现章节、相关术语链接。**字母排序**，**60+ 条目**，**3 大类别**（核心架构 / 记忆与学习 / 联邦与安全 / 命令与工具）。
>
> 🏷️ **读者画像**：全员（建议收藏为速查手册）
> 🕐 **预估耗时**：30 分钟（扫读）/ 5 分钟（速查）
> ✅ **LAST_VERIFIED_AGAINST**：`26c35b59` (v3.32.9)

---

## 使用方法

- **按字母速查**：目录项 A–Z 直接跳转
- **按主题跳读**：第 5 节「主题索引表」按「架构 / 记忆 / 联邦 / 命令」分组
- **首现章节**：可点击跳回原始讲解
- **相关术语**：横向串联邻近概念

> 本章与 ch01–ch16 互相引用，每条术语都「可追溯到具体章节」。

---

## 1. A–Z 术语详解

### A

#### **Agent（智能体）**

- **中文释义**：能感知环境、做出决策、执行动作的自治实体。在 ruflo 中，agent 是包装了 LLM + 工具 + 内存 + 角色的执行单元。
- **一句话定义**：*LLM + 工具 + 内存 + 角色 = Agent。*
- **首次出现**：[第 01 章 · 1.1](./01-ruflo-intro.md)
- **相关术语**：[Queen](#queen战略战术自适应三型)、[Worker](#worker8-种后台工人)、[MCP Server](#mcp-model-context-protocol)、[Hook](#hook生命周期回调)

#### **Agent Booster**

- **中文释义**：用于快速应用 LLM 产生的 edit snippet 的 merge 引擎。
- **一句话定义**：*把 LLM 输出贴回代码的快速粘贴工具；不是 Tier-1 codemod 路径。*
- **首次出现**：[第 04 章 · 3.3](./04-architecture-deep-dive.md)（隐含提及）
- **相关术语**：[WASM Codemod](#wasm-webassembly)、[Tier 1](#3-tier-routing)、[ADR-143](#adr-architecture-decision-record)

#### **Agentic Flow（agentic-flow 适配器）**

- **中文释义**：第三方 agent 框架适配层，让 ruflo 能消费 agentic-flow 协议。
- **一句话定义**：*「接驳其他 agent 生态」—— 通过 `@claude-flow/integration` 包实现。*
- **首次出现**：[第 04 章 · 3.2](./04-architecture-deep-dive.md)
- **相关术语**：[Codex](#codex)、[MCP](#mcp-model-context-protocol)

#### **Agenticow（多智能体编排器）**

- **中文释义**：agentic-flow 的多智能体编排器，ruflo 通过 integration 包接入。
- **一句话定义**：*「外部 orchestrator 适配」—— v3 引入。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[Swarm](#swarm)、[Queen](#queen战略战术自适应三型)

#### **Anti-Drift 默认（Anti-Drift Defaults）**

- **中文释义**：6 条出厂默认约束——`topology=hierarchical` / `maxAgents=6-8` / `strategy=specialized` / `consensus=raft` / `checkpoint=post-task` / `namespace=shared`。
- **一句话定义**：*「别 spawn 50 个 agent 干 4 文件的活」—— 80% 场景不用调。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)；详见 [ch06](./06-swarm-coordination.md)
- **相关术语**：[Hierarchical Topology](#hierarchical拓扑)、[Raft](#raft)、[Queen (Strategic)](#queen战略战术自适应三型)

#### **AgentDB（Agent Database）**

- **中文释义**：ruflo 专用的本地向量数据库，内嵌 SQLite + HNSW 索引。
- **一句话定义**：*「agent 的硬盘」——存向量、键值、关系图。*
- **首次出现**：[第 07 章 · 2.1](./07-memory-and-learning.md)
- **相关术语**：[HNSW](#hnsw)、[SQLite](#sqlite)、[Embedding](#embedding)、[.rvf](#rvf-ruvector-format)

#### **AIDefence（AI 操作防御）**

- **中文释义**：检测并阻断恶意或异常 AI 操作的防御层，6 大类检测（prompt injection / data exfiltration / tool abuse / etc.）。
- **一句话定义**：*「AI 防火墙」—— 在 agent 调用工具前过一遍规则。*
- **首次出现**：[第 10 章 · 安全与 AIDefence](./10-security-and-aidefence.md)
- **相关术语**：[CVE](#cve-common-vulnerabilities-and-exposures)、[Prompt Injection](#prompt-injection)、[WASM](#wasm-webassembly)、[ADR-118](#adr-architecture-decision-record)

#### **Anti-Drift（防漂移）**

- **中文释义**：ruflo 的出厂默认配置原则——小团队、层级拓扑、专业化策略、Raft 共识、频繁 checkpoint、共享内存。
- **一句话定义**：*「最不容易跑飞」的 swarm 默认配方。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)
- **相关术语**：[Swarm](#swarm)、[Hierarchical Topology](#hierarchical拓扑)、[Raft](#raft)、[Queen (Strategic)](#queen战略战术自适应三型)

#### **ADR（Architecture Decision Record）**

- **中文释义**：架构决策记录——一份不可变 Markdown 文件，记录「为什么这么设计」。
- **一句话定义**：*「软件考古笔记」—— 每个决策的时间 + 背景 + 备选 + 后果。*
- **首次出现**：[第 16 章 · 进阶模块深读](./16-extended-modules.md)；详见 [第 19 章 · ADR 索引](./19-references.md)
- **相关术语**：[SPARC](#sparc)、[MetaHarness](#metaharness)、[ADR-026](#adr-architecture-decision-record)（3-Tier 路由）

---

### B

#### **Bash**

- **中文释义**：Bourne-Again Shell——ruflo 安装脚本兼容的 shell。
- **一句话定义**：*「Linux 默认 shell」—— install.sh 同时支持 bash + zsh。*
- **首次出现**：[第 02 章 · 2.2](./02-install-and-init.md)
- **相关术语**：[ZSH](#zshz-shell)、[Shell](#shell)

#### **Beta(α, β)（贝塔分布）**

- **中文释义**：二项分布的共轭先验，用于 Thompson Sampling 的多臂老虎机路由。
- **一句话定义**：*「路由成功率分布」—— α 胜、β 负，期望 = α/(α+β)。*
- **首次出现**：[第 08 章 · 智能路由与成本控制](./08-routing-and-cost.md)
- **相关术语**：[Thompson Sampling](#thompson-sampling)、[3-Tier Routing](#3-tier-routing)

#### **Byzantine（拜占庭共识）**

- **中文释义**：能在 N≤3f 故障节点下达成一致的最强容错共识算法（PBFT 类）。
- **一句话定义**：*「即使部分节点说谎也能投票」—— 代价是 O(N²) 通信。*
- **首次出现**：[第 06 章 · 蜂群协作](./06-swarm-coordination.md)
- **相关术语**：[Raft](#raft)、[Consensus](#consensus)、[5 种共识算法](#consensus)

---

### C

#### **Codemod（代码改写器）**

- **中文释义**：确定性的批量代码改写（TypeScript AST → 改写）。WASM 编译后 ~1ms 完成。
- **一句话定义**：*「var → const 这种事不用 LLM」—— Tier-1 路径。*
- **首次出现**：[第 08 章 · 3-Tier 路由](./08-routing-and-cost.md)
- **相关术语**：[WASM](#wasm-webassembly)、[Agent Booster](#agent-booster)、[Tier 1](#3-tier-routing)、[ADR-143](#adr-architecture-decision-record)

#### **Consensus（共识算法）**

- **中文释义**：多 agent 在共享状态下达成一致决策的协议。ruflo 支持 5 种：Raft / Byzantine / Gossip / CRDT / SPARC。
- **一句话定义**：*「多 agent 投票机制」—— 不同算法对网络/故障假设不同。*
- **首次出现**：[第 06 章 · 蜂群协作](./06-swarm-coordination.md)
- **相关术语**：[Raft](#raft)、[Byzantine](#byzantine拜占庭共识)、[Gossip](#gossip)、[CRDT](#crdt)、[SPARC](#sparc)

#### **CRDT（Conflict-free Replicated Data Type）**

- **中文释义**：无需协调即可在多副本间合并的数据类型（计数器 / 集合 / 树）。
- **一句话定义**：*「冲突自动解决」—— 适合最终一致场景。*
- **首次出现**：[第 06 章 · 共识章节](./06-swarm-coordination.md)
- **相关术语**：[Consensus](#consensus)、[AgentDB](#agentdbagent-database)

#### **Cypher（Cypher 查询语言）**

- **中文释义**：图数据库查询语言（Neo4j 起源），ruflo AgentDB 支持用 Cypher 查关系。
- **一句话定义**：*「查图的 SQL」—— MATCH / WHERE / RETURN 语法。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[AgentDB](#agentdbagent-database)、[Graph](#mesh)

---

### D

#### **DDD（Domain-Driven Design）**

- **中文释义**：领域驱动设计——用代码结构对齐业务领域（bounded context / aggregate / repository）。
- **一句话定义**：*「让代码长得像业务」—— CLAUDE.md 强制 ruflo 遵循 DDD。*
- **首次出现**：[第 04 章 · 3.2](./04-architecture-deep-dive.md)
- **相关术语**：[Bounded Context](#bounded-context)、[CLAUDE.md](#claudemd)

#### **Doctor（健康检查）**

- **中文释义**：ruflo 的内置健康检查工具，跑 26 项检查（Node/npm/CLAUDE.md/MCP/HNSW/...）。
- **一句话定义**：*「ruflo 自检 26 项」—— `--fix` 可自动修复。*
- **首次出现**：[第 02 章 · 2.1](./02-install-and-init.md)
- **相关术语**：[init](#init)、[verify](#verifywitness-ed25519)、[plugin doctor](#plugins)

#### **daa-*（Decentralized Autonomous Agents）**

- **中文释义**：去中心化自治 agent 命名空间——跨机器协作 + 自组织。
- **一句话定义**：*「d-a-a」—— 10+ 工具，专为联邦场景。*
- **首次出现**：[第 04 章 · 2.2](./04-architecture-deep-dive.md)
- **相关术语**：[Federation](#federation)、[MCP](#mcp-model-context-protocol)

---

### E

#### **Ed25519**

- **中文释义**：高效椭圆曲线签名算法——ruflo 身份签名 + Witness 校验全用它。
- **一句话定义**：*「比 RSA 快 100× 的签名」—— 默认加密套件。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Witness](#witnessed25519-签名校验)、[mTLS](#mtlsmutual-tls)、[Federation](#federation)

#### **Embedding（向量嵌入）**

- **中文释义**：将文本/代码映射到 N 维实数向量的过程。ruflo 默认用 ONNX MiniLM (384 dim)。
- **一句话定义**：*「文本 → 数字数组」—— 语义搜索的基础。*
- **首次出现**：[第 07 章 · 2.2](./07-memory-and-learning.md)
- **相关术语**：[ONNX](#onnx)、[HNSW](#hnsw)、[Ollama](#ollama)

#### **EWC++（Elastic Weight Consolidation++）**

- **中文释义**：防灾难性遗忘的正则化方法，保护对旧任务重要的参数。
- **一句话定义**：*「别让学新东西忘旧的」—— SONA 用它做持续学习。*
- **首次出现**：[第 07 章 · 2.5](./07-memory-and-learning.md)
- **相关术语**：[MicroLoRA](#microlora)、[SONA](#sona)、[MoE](#moemixture-of-experts)

---

### F

#### **Federation（联邦）**

- **中文释义**：跨机器 / 跨组织的 agent 协作机制，默认零信任（mTLS + ed25519 + 5 级信任）。
- **一句话定义**：*「让多台机器的 agent 安全协作」—— 不用共享密钥。*
- **首次出现**：[第 09 章 · 联邦](./09-federation.md)
- **相关术语**：[Trust Ladder](#trust-ladder)、[mTLS](#mtls)、[WireGuard Mesh](#wireguard-mesh)、[ADR-120](#adr-architecture-decision-record)

#### **Flow State（心流）**

- **中文释义**：开发者高度专注、产出最高的心理状态。ruflo 名字中「flo」即取自此意。
- **一句话定义**：*「凌晨三点还在写代码」—— 减少认知摩擦。*
- **首次出现**：[第 01 章 · 1.2](./01-ruflo-intro.md)

#### **Frontmatter（章节元数据）**

- **中文释义**：每章文件顶部的 YAML 格式元数据（`title` / `last_verified_against` / `verified_at` / `chapter`）。
- **一句话定义**：*「手册每章的身份证」—— CI 用它判 drift。*
- **首次出现**：[第 17 章 · 5.3](./17-terminology-glossary.md)
- **相关术语**：[drift 检测](#drift-检测)、[CLAUDE.md](#claudemd)

#### **FastGRNN**

- **中文释义**：快速门控循环神经网络——ADR-148 引入的轻量级路由模型。
- **一句话定义**：*「比 Transformer 便宜 100× 的序列模型」—— Arena 阶段 2 用。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[MoE](#moemixture-of-experts)、[SONA](#sona)、[ADR-148](#adr-architecture-decision-record)

---

### G

#### **Gossip（流言协议）**

- **中文释义**：周期性随机节点交换状态的最终一致协议（O(log N) 收敛）。
- **一句话定义**：*「我告诉你，你告诉他」—— 无中心、低带宽。*
- **首次出现**：[第 06 章 · 共识章节](./06-swarm-coordination.md)
- **相关术语**：[Consensus](#consensus)、[Byzantine](#byzantine拜占庭共识)

---

### H

#### **HNSW（Hierarchical Navigable Small World）**

- **中文释义**：图结构近似最近邻算法，亚毫秒级向量检索。
- **一句话定义**：*「又快又准的向量搜索」—— 比 brute-force 快 4.7×（N=5000）。*
- **首次出现**：[第 07 章 · 2.2](./07-memory-and-learning.md)
- **相关术语**：[AgentDB](#agentdbagent-database)、[RaBitQ](#rabitq)、[Embedding](#embedding)

#### **Hive-Mind（蜂巢心智）**

- **中文释义**：Queen 主导的层级协作模式，所有 agent 共享内存命名空间 + 单向决策流。
- **一句话定义**：*「一个大脑指挥多只手」—— hierarchical 拓扑的实现。*
- **首次出现**：[第 06 章 · 蜂群协作](./06-swarm-coordination.md)
- **相关术语**：[Queen (Strategic)](#queen战略战术自适应三型)、[Swarm](#swarm)、[Hierarchical Topology](#hierarchical拓扑)

#### **Hook（生命周期回调）**

- **中文释义**：在 Claude Code / ruflo 关键事件点触发的用户/系统脚本。共 17 个，分 5 类。
- **一句话定义**：*「pre-task / post-task / route / session-start ...」—— 自动接管 17 个时机。*
- **首次出现**：[第 03 章 · 第一次对话](./03-first-conversation.md)
- **相关术语**：[Worker](#worker8-种后台工人)、[CLAUDE.md](#claudemd)、[settings.json](#settingsjson)

#### **Hierarchical Topology（层级拓扑）**

- **中文释义**：swarm 的树状组织——Queen 顶层决策，Workers 平行执行，agent 间不直连。
- **一句话定义**：*「自上而下」—— Anti-Drift 默认。*
- **首次出现**：[第 06 章 · 蜂群协作](./06-swarm-coordination.md)
- **相关术语**：[Mesh](#mesh)、[Star](#star-拓扑)、[Queen (Strategic)](#queen战略战术自适应三型)

#### **Hive-Mind Consensus（蜂巢共识）**

- **中文释义**：hierarchical 拓扑下的共识模式——Queen 单点决策，Workers 跟随。
- **一句话定义**：*「老大说了算」—— 不投票，省带宽。*
- **首次出现**：[第 06 章 · 共识章节](./06-swarm-coordination.md)
- **相关术语**：[Raft](#raft)、[Hierarchical Topology](#hierarchical拓扑)

#### **HuggingFace**

- **中文释义**：开源模型/数据集平台。ruflo 在 ADR-094 后迁移到 `@huggingface/transformers`。
- **一句话定义**：*「AI 界的 GitHub」—— 模型超市。*
- **首次出现**：[第 07 章 · 2.2](./07-memory-and-learning.md)
- **相关术语**：[ONNX](#onnx)、[Ollama](#ollama)、[Embedding](#embedding)

---

### I

#### **init（初始化）**

- **中文释义**：ruflo 的项目初始化命令——创建 `.claude/`、`.claude-flow/`、`CLAUDE.md`。
- **一句话定义**：*「一键装好 harness」—— `--non-interactive` 用于 CI。*
- **首次出现**：[第 02 章 · 2.1](./02-install-and-init.md)
- **相关术语**：[Doctor](#doctor健康检查)、[CLAUDE.md](#claudemd)、[.mcp.json](#mcpjson)

#### **intelligence_route（智能路由）**

- **中文释义**：3-Tier 路由的核心 MCP 工具——给定任务返回 tier 决策。
- **一句话定义**：*「应该走 WASM / Haiku / Sonnet 哪个？」—— 50 次后收敛。*
- **首次出现**：[第 08 章 · 智能路由](./08-routing-and-cost.md)
- **相关术语**：[3-Tier Routing](#3-tier-routing)、[Thompson Sampling](#thompson-sampling)

---

### J

#### **JSON-RPC**

- **中文释义**：基于 JSON 的远程过程调用协议——MCP 传输层协议。
- **一句话定义**：*「JSON 版 RPC」—— Content-Length 头分隔帧。*
- **首次出现**：[第 04 章 · 3.1](./04-architecture-deep-dive.md)
- **相关术语**：[MCP](#mcp-model-context-protocol)、[stdio](#stdio)

---

### K

#### **Key-Value Store（键值存储）**

- **中文释义**：基于键查询的简单存储。AgentDB 的元数据层。
- **一句话定义**：*「键 → 值」—— 跟 dict 一样简单。*
- **首次出现**：[第 07 章 · 3.1](./07-memory-and-learning.md)
- **相关术语**：[AgentDB](#agentdbagent-database)、[SQLite](#sqlite)

---

### L

#### **LoRA（Low-Rank Adaptation）**

- **中文释义**：低秩参数高效微调方法。ruflo 用 **MicroLoRA**（< 0.1% 全模型参数）。
- **一句话定义**：*「用很少参数学会新技能」—— 不用动全模型。*
- **首次出现**：[第 07 章 · 2.5](./07-memory-and-learning.md)
- **相关术语**：[MicroLoRA](#microlora)、[EWC++](#ewc-elastic-weight-consolidation)、[SONA](#sona)

#### **Local Memory（本地内存）**

- **中文释义**：`local` 作用域的内存——`~/.claude-flow/memory/`，跨项目共享、个人习惯。
- **一句话定义**：*「项目 A 的约定，项目 B 也能用」—— 中等作用域。*
- **首次出现**：[第 07 章 · 2.1](./07-memory-and-learning.md)
- **相关术语**：[Memory Namespace](#memory-namespace)、[Project Memory](#project-memory)、[User Memory](#user-memory)

#### **LLM Provider（大模型适配层）**

- **中文释义**：ruflo 的 5 家 LLM 适配层——Anthropic / OpenAI / Google / Cohere / Ollama。
- **一句话定义**：*「通杀 5 家 LLM」—— 一个接口通吃。*
- **首次出现**：[第 01 章 · 3](./01-ruflo-intro.md)
- **相关术语**：[Ollama](#ollama)、[Provider](#providerllm-适配层)

#### **3-Tier Routing（三层路由）**

- **中文释义**：ADR-026 定义的 3 层智能路由——WASM codemod → Haiku → Sonnet/Opus。
- **一句话定义**：*「便宜先试，复杂再上」—— 80% 任务不必走 Sonnet。*
- **首次出现**：[第 04 章 · 2.3](./04-architecture-deep-dive.md)
- **相关术语**：[Thompson Sampling](#thompson-sampling)、[WASM](#wasm-webassembly)、[Codemod](#codemod代码改写器)

#### **Last Verified Against（最后验证 commit）**

- **中文释义**：手册每章 frontmatter 中的 git commit SHA，证明该章内容基于该 commit 验证。
- **一句话定义**：*「我核对过这个版本」—— SHA 是凭证。*
- **首次出现**：[第 17 章 · 5.1](./17-terminology-glossary.md)
- **相关术语**：[drift 检测](#drift-检测)、[verified_at](#verified_at)

---

### M

#### **Memory Namespace（内存命名空间）**

- **中文释义**：内存的分桶方式——`project` / `local` / `user` 三个作用域。
- **一句话定义**：*「内存的文件夹」—— 跨项目共享 vs 隔离。*
- **首次出现**：[第 07 章 · 2.1](./07-memory-and-learning.md)
- **相关术语**：[Project Memory](#project-memory)、[Local Memory](#local-memory本地内存)、[User Memory](#user-memory)

#### **MicroLoRA**

- **中文释义**：极小参数量的 LoRA——< 0.1% 全模型参数。
- **一句话定义**：*「100KB 学一个新技能」—— 不用动基座。*
- **首次出现**：[第 07 章 · 2.5](./07-memory-and-learning.md)
- **相关术语**：[LoRA](#lora-low-rank-adaptation)、[EWC++](#ewc-elastic-weight-consolidation)、[SONA](#sona)

#### **Mesh（Mesh 拓扑）**

- **中文释义**：swarm 的网状组织——agent 间两两直连，无中心。
- **一句话定义**：*「去中心化」—— 适合 12+ agent 的大型 swarm。*
- **首次出现**：[第 06 章 · 拓扑](./06-swarm-coordination.md)
- **相关术语**：[Hierarchical Topology](#hierarchical拓扑)、[WireGuard Mesh](#wireguard-mesh)

#### **MCP（Model Context Protocol）**

- **中文释义**：Anthropic 推出的「LLM ↔ 工具」通信协议，stdin/stdout JSON-RPC。ruflo 暴露 314+ 工具。
- **一句话定义**：*「LLM 调工具的标准接口」—— Claude Code 与 ruflo 的桥梁。*
- **首次出现**：[第 04 章 · 3.1](./04-architecture-deep-dive.md)
- **相关术语**：[MCP Server](#mcp-model-context-protocol)、[stdio](#stdio)、[JSON-RPC](#json-rpc)

#### **MoE（Mixture of Experts）**

- **中文释义**：混合专家模型——8 个专家 + 门控网络，按输入动态激活部分专家。
- **一句话定义**：*「8 个专家各管一摊」—— 节省算力 + 提高准确率。*
- **首次出现**：[第 07 章 · 2.4](./07-memory-and-learning.md)
- **相关术语**：[SONA](#sona)、[Gating Network](#gating-network门控网络)、[JUDGE](#reasoningbank4-步流水线)

#### **mTLS（Mutual TLS）**

- **中文释义**：双向 TLS 认证——客户端与服务端互相验证证书。
- **一句话定义**：*「不只是验证服务器，服务器也验证你」—— Federation 默认安全层。*
- **首次出现**：[第 09 章 · 联邦](./09-federation.md)
- **相关术语**：[Federation](#federation)、[ed25519](#ed25519)、[Trust Ladder](#trust-ladder)

#### **Mesh（网状拓扑 / WireGuard Mesh）**

- **中文释义**：agent 间 / 机器间的网状结构，每个节点直连多个邻居。WireGuard 实现 overlay 网络。
- **一句话定义**：*「谁都能跟谁直接聊」—— 联邦底层网络（ADR-111）。*
- **首次出现**：[第 06 章 · 拓扑](./06-swarm-coordination.md)；[ADR-111](./19-references.md)
- **相关术语**：[WireGuard](#wireguard)、[Hierarchical Topology](#hierarchical拓扑)

---

### N

#### **Namespace（命名空间）**

- **中文释义**：MCP 工具 / memory / swarm 任务的分桶方式（如 `memory_*` / `swarm_*` / `project`/`local`/`user`）。
- **一句话定义**：*「给工具/数据起前缀」—— 防冲突 + 权限隔离。*
- **首次出现**：[第 04 章 · 2.2](./04-architecture-deep-dive.md)
- **相关术语**：[MCP](#mcp-model-context-protocol)、[Memory Namespace](#memory-namespace)

#### **Neuron（神经单元）**

- **中文释义**：SONA 自学习系统中的单个学习节点（含 PPO / DQN / Decision Transformer 等算法实例）。
- **一句话定义**：*「SONA 的『脑细胞』」—— 每个管一类学习任务。*
- **首次出现**：[第 16 章 · SONA 章节](./16-extended-modules.md)
- **相关术语**：[SONA](#sona)、[MoE](#moemixture-of-experts)、[7 RL 算法](#7-rl-算法)

#### **Neo4j（图数据库）**

- **中文释义**：图数据库实现，AgentDB 可对接 Neo4j 协议。
- **一句话定义**：*「图的 SQL」—— 关系查询之王。*
- **首次出现**：[第 16 章 · AgentDB](./16-extended-modules.md)
- **相关术语**：[Cypher](#cyphercypher-查询语言)、[AgentDB](#agentdbagent-database)

#### **NOT PII Strip（脱敏）**

- **中文释义**：Federation 边界处自动剥离 14 类 PII（身份证 / 信用卡 / 邮箱 / ...）。
- **一句话定义**：*「发出去之前擦干净」—— 默认开。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Federation](#federation)、[Trust Ladder](#trust-ladder5-级信任阶梯)、[AIDefence](#aidefenceai-操作防御)

#### **NOT_GATED（未门控动作）**

- **中文释义**：AIDefence 3-gate 模型中未通过 gate 检测的操作——直接拒绝。
- **一句话定义**：*「没通过安检」—— 默认 deny。*
- **首次出现**：[第 10 章 · AIDefence](./10-security-and-aidefence.md)
- **相关术语**：[AIDefence](#aidefenceai-操作防御)、[ADR-118](#adr-architecture-decision-record)

#### **Natural Test Generation（自然测试生成）**

- **中文释义**：基于 `@claude-flow/testing` 的 TDD London 测试生成。
- **一句话定义**：*「先写 mock 再写实现」—— Builder 推荐流程。*
- **首次出现**：[第 15 章 · Builder 指南](./15-builder-guide.md)
- **相关术语**：[TDD London](#tdd-london)、[ADR](#adr-architecture-decision-record)

---

### O

#### **ONNX（Open Neural Network Exchange）**

- **中文释义**：跨框架模型格式标准。ruflo 用 ONNX Runtime 跑本地 MiniLM embedding。
- **一句话定义**：*「一次训练，到处跑」—— PyTorch / TF / Transformers 通用格式。*
- **首次出现**：[第 07 章 · 2.2](./07-memory-and-learning.md)
- **相关术语**：[Embedding](#embedding)、[Ollama](#ollama)、[HuggingFace](#huggingface)

#### **Ollama**

- **中文释义**：本地运行开源 LLM 的工具（Llama / Mistral / Qwen 等）。
- **一句话定义**：*「本地 LLM 一键跑」—— 不依赖云 API。*
- **首次出现**：[第 05 章 · Provider 章节](./05-agents-and-skills.md)
- **相关术语**：[Provider](#providerllm-适配层)、[Embedding](#embedding)

---

### P

#### **Plugin（插件）**

- **中文释义**：ruflo 的扩展单元，可加 MCP 工具 / hooks / agents / commands。共 33+ 插件。
- **一句话定义**：*「ruflo 的 App Store」—— 装一个就加一坨能力。*
- **首次出现**：[第 12 章 · 插件生态](./12-plugin-ecosystem.md)
- **相关术语**：[Plugin SDK](#plugin-sdk)、[Hooks](#hook生命周期回调)、[plugins install](#plugins)

#### **PRIVILEGED（信任等级 5）**

- **中文释义**：Trust Ladder 最高级——可执行特权操作（部署、改密钥、跨账户转账）。
- **一句话定义**：*「完全信任的 agent」—— 行为历史 + 显式审批。*
- **首次出现**：[第 09 章 · Trust Ladder](./09-federation.md)
- **相关术语**：[Trust Ladder](#trust-ladder)、[VERIFIED](#verified信任等级-2)、[ATTESTED](#attested信任等级-3)、[TRUSTED](#trusted信任等级-4)

#### **Pattern（模式）**

- **中文释义**：从成功任务中提炼的可复用执行模板——含输入 schema + 决策理由 + 输出模板。
- **一句话定义**：*「成功经验的固化」—— SONA 提炼。*
- **首次出现**：[第 07 章 · 2.3](./07-memory-and-learning.md)
- **相关术语**：[ReasoningBank](#reasoningbank)、[SONA](#sona)、[DISTILL](#reasoningbank4-步流水线)

#### **Pattern Store（模式存储）**

- **中文释义**：reasoning_bank 命名空间下的 pattern 库。
- **一句话定义**：*「成功的 N 种套路」—— 按相似度检索。*
- **首次出现**：[第 07 章 · 2.3](./07-memory-and-learning.md)
- **相关术语**：[ReasoningBank](#reasoningbank)、[Memory Namespace](#memory-namespace)

#### **Plugin SDK**

- **中文释义**：ruflo 的插件开发工具包——`@claude-flow/plugins` 包。
- **一句话定义**：*「造插件的工具」—— manifest + handler + tests。*
- **首次出现**：[第 15 章 · Builder 指南](./15-builder-guide.md)
- **相关术语**：[Plugin](#plugin插件)、[Manifest](#manifest)

#### **Provider（LLM 适配层）**

- **中文释义**：5 家 LLM（Anthropic / OpenAI / Google / Cohere / Ollama）的统一接口。
- **一句话定义**：*「模型适配层」—— 一个接口通吃。*
- **首次出现**：[第 04 章 · 3.2](./04-architecture-deep-dive.md)
- **相关术语**：[LLM Provider](#llm-provider大模型适配层)、[Ollama](#ollama)

#### **Project Memory（项目内存）**

- **中文释义**：`project` 作用域的内存——`<project>/.claude-flow/memory/`，项目专属。
- **一句话定义**：*「这个项目的约定」—— 不跨项目。*
- **首次出现**：[第 07 章 · 2.1](./07-memory-and-learning.md)
- **相关术语**：[Memory Namespace](#memory-namespace)、[Local Memory](#local-memory本地内存)、[User Memory](#user-memory)

#### **PII（个人可识别信息）**

- **中文释义**：个人可识别信息——身份证 / 信用卡 / 手机号等。Federation 默认剥离 14 类。
- **一句话定义**：*「敏感个人数据」—— 出联邦边界前必清。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Federation](#federation)、[AIDefence](#aidefenceai-操作防御)

#### **Prompt Injection（提示注入）**

- **中文释义**：通过恶意提示让 agent 执行非预期操作的攻击方式。
- **一句话定义**：*「骗 LLM」—— AIDefence 第一类检测。*
- **首次出现**：[第 10 章 · AIDefence](./10-security-and-aidefence.md)
- **相关术语**：[AIDefence](#aidefenceai-操作防御)、[Data Exfiltration](#data-exfiltration)

#### **Peer Discovery（对等节点发现）**

- **中文释义**：ADR-106 定义的 peer 自动发现协议。
- **一句话定义**：*「邻居怎么找到我」—— mDNS + WireGuard。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Federation](#federation)、[WireGuard Mesh](#wireguard-mesh)、[ADR-106](#adr-architecture-decision-record)

#### **PostgreSQL（pgvector）**

- **中文释义**：开源关系数据库——可选替代 HNSW 的向量后端。
- **一句话定义**：*「传统 DB + 向量扩展」—— 已有 PG 的团队友好。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[HNSW](#hnsw)、[SQLite](#sqlite)、[AgentDB](#agentdbagent-database)

---

### Q

#### **Queen（战略/战术/自适应三型）**

- **中文释义**：Swarm 顶层决策者。三种类型：
  - **Queen (Strategic)**：长期目标 + 资源分配（默认）
  - **Queen (Tactical)**：短期任务分解 + 实时调度
  - **Queen (Adaptive)**：动态切换战略/战术模式（基于 SONA 学习）
- **一句话定义**：*「swarm 的 CEO/CTO/COO」—— 三选一或混用。*
- **首次出现**：[第 06 章 · 蜂群协作](./06-swarm-coordination.md)
- **相关术语**：[Worker](#worker8-种后台工人)、[Hive-Mind](#hive-mind蜂巢心智)

---

### R

#### **RaBitQ**

- **中文释义**：高质量向量量化算法，~10× 内存压缩 + 0.99+ 召回率。
- **一句话定义**：*「把 384 维向量压成 64 比特」—— 大规模内存场景。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[HNSW](#hnsw)、[Embedding](#embedding)

#### **Raft**

- **中文释义**：Leader-based 共识算法，O(N) 通信，容 N/2-1 故障。
- **一句话定义**：*「选个老大，老大说了算」—— Antidrift 默认共识。*
- **首次出现**：[第 06 章 · 共识章节](./06-swarm-coordination.md)
- **相关术语**：[Consensus](#consensus)、[Byzantine](#byzantine拜占庭共识)、[Queen (Strategic)](#queen战略战术自适应三型)

#### **ReasoningBank**

- **中文释义**：成功模式的存储库 + 4 步流水线（RETRIEVE → JUDGE → DISTILL → CONSOLIDATE）。
- **一句话定义**：*「ruflo 的错题本 / 经验库」—— 越用越聪明。*
- **首次出现**：[第 07 章 · 2.3](./07-memory-and-learning.md)
- **相关术语**：[SONA](#sona)、[Pattern](#pattern)、[RETRIEVE/JUDGE/DISTILL/CONSOLIDATE](#reasoningbank4-步流水线)

#### **Router（路由层）**

- **中文释义**：第 4 层架构——3-Tier 智能路由（WASM → Haiku → Sonnet）。
- **一句话定义**：*「决定每个任务交给谁做」—— Thompson Sampling 自校准。*
- **首次出现**：[第 01 章 · 3](./01-ruflo-intro.md)；详见 [第 08 章](./08-routing-and-cost.md)
- **相关术语**：[3-Tier Routing](#3-tier-routing)、[Thompson Sampling](#thompson-sampling)、[ADR-026](#adr-architecture-decision-record)

#### **ReasoningBank 4 步流水线**

- **中文释义**：SONA 自学习的 4 步流程——**R**ETRIEVE → **J**UDGE → **D**ISTILL → **C**ONSOLIDATE。
- **一句话定义**：*「找类似的 → 评路径 → 炼模板 → 存经验」—— 循环往复。*
- **首次出现**：[第 07 章 · 2.3](./07-memory-and-learning.md)
- **相关术语**：[SONA](#sona)、[Pattern](#pattern)、[MicroLoRA](#microlora)

#### **ReasoningBank**

- **中文释义**：成功模式的存储库 + 4 步流水线（RETRIEVE → JUDGE → DISTILL → CONSOLIDATE）。
- **一句话定义**：*「ruflo 的错题本 / 经验库」—— 越用越聪明。*
- **首次出现**：[第 07 章 · 2.3](./07-memory-and-learning.md)
- **相关术语**：[SONA](#sona)、[Pattern](#pattern)、[RETRIEVE/JUDGE/DISTILL/CONSOLIDATE](#reasoningbank4-步流水线)

#### **Reed-Solomon（纠错码）**

- **中文释义**：前向纠错码——数据传输中冗余纠错。
- **一句话定义**：*「传输坏了能自动纠」—— 联邦边缘节点用。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[QUIC](#quic)、[WASM](#wasm-webassembly)

#### **Reliability Score（可靠性评分）**

- **中文释义**：每个 agent / peer 的历史成功率——影响路由权重。
- **一句话定义**：*「100 任务成功 95 次 → score=0.95」—— 动态计算。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Trust Ladder](#trust-ladder)、[Thompson Sampling](#thompson-sampling)

#### **REST API**

- **中文释义**：REST 风格 HTTP API——ruflo MCP server 可通过 HTTP 暴露。
- **一句话定义**：*「HTTP + JSON」—— 远程调用 MCP 的方式之一。*
- **首次出现**：[第 04 章 · 3.1](./04-architecture-deep-dive.md)
- **相关术语**：[MCP](#mcp-model-context-protocol)、[JSON-RPC](#json-rpc)

#### **Recovery（故障恢复）**

- **中文释义**：从崩溃 / 异常中恢复到一致状态——AgentDB 自动 WAL。
- **一句话定义**：*「崩了不丢数据」—— ACID 保障。*
- **首次出现**：[第 07 章 · 3.1](./07-memory-and-learning.md)
- **相关术语**：[AgentDB](#agentdbagent-database)、[SQLite](#sqlite)

#### **Recursive Subagent（递归子 agent）**

- **中文释义**：agent 可 spawn 子 agent 的递归模式——ADR-147 限制深度。
- **一句话定义**：*「agent 套 agent」—— 深度上限 3 层。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[Agent](#agent智能体)、[ADR-147](#adr-architecture-decision-record)

---

### S

#### **SONA（Self-Optimizing Neural Architecture）**

- **中文释义**：ruflo 自学习系统——7 种 RL 算法 + MoE + MicroLoRA + EWC++ + 4 步流水线。
- **一句话定义**：*「让 ruflo 越用越聪明的大脑」—— 50 次后命中率 94%。*
- **首次出现**：[第 07 章 · 2.3](./07-memory-and-learning.md)
- **相关术语**：[MoE](#moemixture-of-experts)、[ReasoningBank](#reasoningbank)、[MicroLoRA](#microlora)、[EWC++](#ewc-elastic-weight-consolidation)

#### **SPARC**

- **中文释义**：5 阶段开发方法论（Specification / Pseudocode / Architecture / Refinement / Completion）。
- **一句话定义**：*「ruflo 推荐的 5 步开发流」—— Builder 必读。*
- **首次出现**：[第 15 章 · Builder 指南](./15-builder-guide.md)
- **相关术语**：[ADR](#adr-architecture-decision-record)、[DDD](#ddddomain-driven-design)

#### **SQLite**

- **中文释义**：嵌入式 SQL 数据库。AgentDB 用 SQLite 存键值 + 元数据，HNSW 存向量。
- **一句话定义**：*「agentdb.rvf 里的 SQL 层」—— 元数据表。*
- **首次出现**：[第 07 章 · 3.1](./07-memory-and-learning.md)
- **相关术语**：[AgentDB](#agentdbagent-database)、[HNSW](#hnsw)

#### **Swarm（蜂群）**

- **中文释义**：多 agent 协同工作组，由 1 个 Queen + 6–8 个 Workers 组成。
- **一句话定义**：*「一群 agent 一起干活」—— 默认 hierarchical。*
- **首次出现**：[第 06 章 · 蜂群协作](./06-swarm-coordination.md)
- **相关术语**：[Queen](#queen战略战术自适应三型)、[Worker](#worker8-种后台工人)、[Hive-Mind](#hive-mind蜂巢心智)

#### **Stakeholder（干系人）**

- **中文释义**：与 swarm 任务结果相关的利益方——可能是用户、上游 agent、下游 CI。
- **一句话定义**：*「谁会关心这个任务的结果」—— 影响路由决策。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[Swarm](#swarm)、[Queen (Strategic)](#queen战略战术自适应三型)

#### **Sandbox（沙箱）**

- **中文释义**：隔离的测试/运行环境——手册配套 `/tmp/ruflo-sandbox-default/`。
- **一句话定义**：*「跑坏也不影响真项目」—— 安全试错。*
- **首次出现**：[第 02 章 · 4](./02-install-and-init.md)
- **相关术语**：[WASM](#wasm-webassembly)、[Docker](#docker)

#### **Stakeholder Prompt（干系人提示）**

- **中文释义**：Queen 在 spawn agent 时注入的上下文——谁会关心这个结果。
- **一句话定义**：*「告诉 agent 这个任务给谁」—— 影响判断。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[Queen](#queen战略战术自适应三型)、[Task](#task任务)

#### **Settings Hierarchy（配置优先级）**

- **中文释义**：项目级 > 插件级 > 全局级——冲突时取更精确的。
- **一句话定义**：*「越具体的越优先」—— 跟 CSS specificity 一样。*
- **首次出现**：[第 03 章 · 3.1](./03-first-conversation.md)
- **相关术语**：[CLAUDE.md](#claudemd)、[settings.json](#settingsjson)

#### **Sticky Session（粘性会话）**

- **中文释义**：同一 agent / peer 处理相关任务——避免上下文重建。
- **一句话定义**：*「同一个客服接待你」—— 减少冷启动。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Federation](#federation)、[Agent](#agent智能体)

#### **SHA-256**

- **中文释义**：256 位安全哈希算法——ruflo 用于二进制校验。
- **一句话定义**：*「指纹算法」—— 防篡改。*
- **首次出现**：[第 02 章 · 4.3](./02-install-and-init.md)
- **相关术语**：[Ed25519](#ed25519)、[Witness](#witnessed25519-签名校验)

#### **Star Topology（星型拓扑）**

- **中文释义**：Queen 居中、Workers 围四周的辐射结构。
- **一句话定义**：*「一个中心节点直连所有」—— 简单但单点。*
- **首次出现**：[第 06 章 · 拓扑](./06-swarm-coordination.md)
- **相关术语**：[Hierarchical Topology](#hierarchical拓扑)、[Mesh](#meshmesh-拓扑)

#### **stdio**

- **中文释义**：标准输入/输出——MCP 默认传输。
- **一句话定义**：*「stdin + stdout 通信」—— 进程间最简方式。*
- **首次出现**：[第 04 章 · 3.1](./04-architecture-deep-dive.md)
- **相关术语**：[MCP](#mcp-model-context-protocol)、[JSON-RPC](#json-rpc)

#### **Sidecar（边车模式）**

- **中文释义**：与主进程并行运行的辅助进程——如 federation peer daemon。
- **一句话定义**：*「挂车的轮子」—— Rust 实现以保性能。*
- **首次出现**：[第 16 章 · 进阶模块](./16-extended-modules.md)
- **相关术语**：[ADR-120](#adr-architecture-decision-record)、[Daemon](#daemon)

---

### T

#### **Thompson Sampling**

- **中文释义**：基于后验采样的多臂老虎机算法，用于路由选择。
- **一句话定义**：*「每次按概率抽一个 tier 试试」—— 探索 vs 利用平衡。*
- **首次出现**：[第 08 章 · 路由](./08-routing-and-cost.md)
- **相关术语**：[Beta(α, β)](#betaα-β贝塔分布)、[3-Tier Routing](#3-tier-routing)、[ADR-026](#adr-architecture-decision-record)

#### **Trust Ladder（5 级信任阶梯）**

- **中文释义**：`UNTRUSTED → VERIFIED → ATTESTED → TRUSTED → PRIVILEGED`，每级解锁不同操作。
- **一句话定义**：*「陌生 agent 干了 100 件好事才能升 TRUSTED」—— 行为即升级。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)；详见 [第 09 章](./09-federation.md)
- **相关术语**：[Federation](#federation)、[mTLS](#mtls)、[PRIVILEGED](#privileged信任等级-5)

#### **Task（任务）**

- **中文释义**：分配给单个 agent / swarm 的工作单元，含输入 schema + 截止时间 + 期望输出。
- **一句话定义**：*「最小的执行单位」—— Task 工具可创建/分配/查询。*
- **首次出现**：[第 03 章 · 2.3](./03-first-conversation.md)
- **相关术语**：[Agent](#agent智能体)、[Hook](#hook生命周期回调)、[task_create](#task)

---

### V

#### **Vector（向量）**

- **中文释义**：N 维实数数组，表示语义。ruflo 默认 384 维（MiniLM）。
- **一句话定义**：*「文字的数学指纹」—— 距离即相似度。*
- **首次出现**：[第 07 章 · 2.2](./07-memory-and-learning.md)
- **相关术语**：[Embedding](#embedding)、[HNSW](#hnsw)、[Cosine Similarity](#cosine-similarity)

#### **Vertex（顶点）**

- **中文释义**：图数据库中的一个节点。ruflo 用「vertex」表存储关系实体。
- **一句话定义**：*「图里的圆圈」—— Cypher 查的对象。*
- **首次出现**：[第 16 章 · AgentDB 图](./16-extended-modules.md)
- **相关术语**：[Cypher](#cyphercypher-查询语言)、[AgentDB](#agentdbagent-database)

#### **VERIFIED（信任等级 2）**

- **中文释义**：Trust Ladder 第 2 级——已通过 mTLS 证书验证身份。
- **一句话定义**：*「身份对得上」—— 还没看行为。*
- **首次出现**：[第 09 章 · Trust Ladder](./09-federation.md)
- **相关术语**：[Trust Ladder](#trust-ladder5-级信任阶梯)、[ATTESTED](#attested信任等级-3)、[UNTRUSTED](#untrusted信任等级-1)

#### **verified_at**

- **中文释义**：手册每章 frontmatter 中的验证日期（人类可读格式 YYYY-MM-DD）。
- **一句话定义**：*「哪天核对这个版本的」—— 与 last_verified_against 配对。*
- **首次出现**：[第 17 章 · 5.3](./17-terminology-glossary.md)
- **相关术语**：[Last Verified Against](#last-verified-against最后验证-commit)、[drift 检测](#drift-检测)

#### **Verify/Witness (Ed25519)**

- **中文释义**：`ruflo verify` 命令——用 Ed25519 签名验证本地字节与官方清单一致。
- **一句话定义**：*「你装的 ruflo 是真的」—— 无需中心服务器。*
- **首次出现**：[第 02 章 · 4.3](./02-install-and-init.md)；详见 [ch10](./10-security-and-aidefence.md)
- **相关术语**：[Ed25519](#ed25519)、[Truth by Witness](#truth-by-witness)

---

### W

#### **WASM（WebAssembly）**

- **中文释义**：浏览器/服务端通用二进制格式。ruflo 用 WASM 跑 codemod 沙箱（Tier-1 路径）。
- **一句话定义**：*「沙箱里的代码改写」—— 1ms 完成 var→const。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)；详见 [第 08 章](./08-routing-and-cost.md)
- **相关术语**：[Codemod](#codemod代码改写器)、[Tier 1](#3-tier-routing)

#### **Witness（Ed25519 签名校验）**

- **中文释义**：`ruflo verify` 用 Ed25519 签名验证本地字节与官方清单一致。
- **一句话定义**：*「你装的 ruflo 是真的」—— 无需中心服务器。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)；详见 [第 10 章](./10-security-and-aidefence.md)
- **相关术语**：[Ed25519](#ed25519)、[Truth by Witness](#truth-by-witness)、[verify](#verifywitness-ed25519)

#### **Worker（8 种后台工人）**

- **中文释义**：后台守护任务，分 8 类：`audit` / `optimize` / `consolidate` / `index` / `gc` / `metrics` / `snapshot` / `replicate`。
- **一句话定义**：*「ruflo 的 8 个打工仔」—— 跑在后台做清理/索引/同步。*
- **首次出现**：[第 11 章 · Hooks 与 Workers](./11-hooks-and-workers.md)
- **相关术语**：[Hook](#hook生命周期回调)、[Agent](#agent智能体)

#### **WireGuard**

- **中文释义**：现代 VPN 协议——ADR-111 选作 Federation overlay 网络。
- **一句话定义**：*「比 OpenVPN 快 4× 的 VPN」—— 内核态实现。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Mesh](#mesh)、[WireGuard Mesh](#wireguard-mesh)、[ADR-111](#adr-architecture-decision-record)

#### **WireGuard Mesh**

- **中文释义**：基于 WireGuard 的网状联邦网络——ADR-111 实现。
- **一句话定义**：*「overlay 网络」—— 跨机器 P2P。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[WireGuard](#wireguard)、[Federation](#federation)、[ADR-111](#adr-architecture-decision-record)

#### **WSS（WebSocket Secure）**

- **中文释义**：TLS 加密的 WebSocket——ADR-104 选作 Federation 默认传输。
- **一句话定义**：*「wss://」—— 长连接 + 加密。*
- **首次出现**：[第 09 章 · Federation](./09-federation.md)
- **相关术语**：[Federation](#federation)、[QUIC](#quic)、[ADR-104](#adr-architecture-decision-record)

#### **WAL（Write-Ahead Log）**

- **中文释义**：预写日志——SQLite 的崩溃安全机制。
- **一句话定义**：*「先写日志再改数据」—— ACID 的基石。*
- **首次出现**：[第 07 章 · 3.1](./07-memory-and-learning.md)
- **相关术语**：[SQLite](#sqlite)、[AgentDB](#agentdbagent-database)

#### **Truth by Witness**

- **中文释义**：ruflo 的安装完整性原则——「所见即所信」。
- **一句话定义**：*「不联网也能验证真实性」—— Ed25519 + 哈希。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)
- **相关术语**：[Witness](#witnessed25519-签名校验)、[Ed25519](#ed25519)

---

### Z

#### **ZSH（Z Shell）**

- **中文释义**：macOS / Linux 默认 shell 之一。ruflo 的 `install.sh` 兼容 zsh + bash。
- **一句话定义**：*「默认 shell」—— install.sh 自动检测。*
- **首次出现**：[第 02 章 · 2.2](./02-install-and-init.md)
- **相关术语**：[Bash](#bash)、[Shell](#shell)

#### **ZSH Completion**

- **中文释义**：ruflo CLI 的 zsh 自动补全脚本。
- **一句话定义**：*「按 Tab 自动补全命令」—— `source <(ruflo completions zsh)`。*
- **首次出现**：[第 02 章 · 2.2](./02-install-and-init.md)
- **相关术语**：[ZSH](#zshz-shell)、[Bash](#bash)

#### **Zero-Trust（零信任）**

- **中文释义**：默认不信任任何内部/外部实体的安全模型。
- **一句话定义**：*「谁都得证明自己」—— Federation 基石。*
- **首次出现**：[第 01 章 · 2.2](./01-ruflo-intro.md)
- **相关术语**：[Federation](#federation)、[Trust Ladder](#trust-ladder5-级信任阶梯)、[mTLS](#mtlsmutual-tls)

---

## 2. 主题索引表（横向速查）

### 2.1 核心架构

| 术语 | 一句话 | 详见章节 |
|------|--------|---------|
| Agent | LLM + 工具 + 内存 + 角色 | [ch01](./01-ruflo-intro.md), [ch05](./05-agents-and-skills.md) |
| Swarm | 多 agent 协同组 | [ch06](./06-swarm-coordination.md) |
| Queen (3 种) | swarm 顶层决策者 | [ch06](./06-swarm-coordination.md) |
| Worker (8 种) | 后台 8 类守护任务 | [ch11](./11-hooks-and-workers.md) |
| MCP Server | LLM ↔ 工具标准协议 | [ch04](./04-architecture-deep-dive.md) |
| Router (3-Tier) | 智能路由层 | [ch08](./08-routing-and-cost.md) |
| Hook (17 个) | 生命周期回调 | [ch03](./03-first-conversation.md), [ch11](./11-hooks-and-workers.md) |

### 2.2 记忆与学习

| 术语 | 一句话 | 详见章节 |
|------|--------|---------|
| AgentDB | 本地向量数据库 | [ch07](./07-memory-and-learning.md) |
| HNSW | 亚毫秒向量检索 | [ch07](./07-memory-and-learning.md) |
| ONNX | 跨框架模型格式 | [ch07](./07-memory-and-learning.md) |
| SONA | 自学习系统 | [ch07](./07-memory-and-learning.md) |
| ReasoningBank | 4 步流水线 | [ch07](./07-memory-and-learning.md) |
| MoE (8 专家) | 混合专家路由 | [ch07](./07-memory-and-learning.md) |
| MicroLoRA | 低秩参数适配 | [ch07](./07-memory-and-learning.md) |
| EWC++ | 防遗忘正则化 | [ch07](./07-memory-and-learning.md) |
| Embedding | 文本 → 向量 | [ch07](./07-memory-and-learning.md) |
| RaBitQ | 向量量化压缩 | [ch16](./16-extended-modules.md) |

### 2.3 联邦与安全

| 术语 | 一句话 | 详见章节 |
|------|--------|---------|
| Federation | 跨机器零信任协作 | [ch09](./09-federation.md) |
| Trust Ladder | 5 级信任阶梯 | [ch09](./09-federation.md) |
| mTLS | 双向 TLS 认证 | [ch09](./09-federation.md) |
| Ed25519 | 高效椭圆曲线签名 | [ch10](./10-security-and-aidefence.md) |
| Witness | Ed25519 安装校验 | [ch10](./10-security-and-aidefence.md) |
| AIDefence | AI 操作防御 | [ch10](./10-security-and-aidefence.md) |
| WireGuard Mesh | 联邦底层网络 | [ch09](./09-federation.md), [ADR-111](./19-references.md) |
| WASM (sandbox) | 工具执行沙箱 | [ch10](./10-security-and-aidefence.md) |

### 2.4 共识与拓扑

| 术语 | 一句话 | 详见章节 |
|------|--------|---------|
| Consensus | 多 agent 一致决策 | [ch06](./06-swarm-coordination.md) |
| Raft | Leader-based 共识 | [ch06](./06-swarm-coordination.md) |
| Byzantine | 拜占庭容错共识 | [ch06](./06-swarm-coordination.md) |
| Gossip | 流言协议 | [ch06](./06-swarm-coordination.md) |
| CRDT | 冲突自动解决 | [ch06](./06-swarm-coordination.md) |
| SPARC | 5 阶段开发方法 | [ch15](./15-builder-guide.md) |
| Anti-Drift | 防漂移默认 | [ch06](./06-swarm-coordination.md) |

### 2.5 路由与成本

| 术语 | 一句话 | 详见章节 |
|------|--------|---------|
| 3-Tier Routing | WASM → Haiku → Sonnet | [ch08](./08-routing-and-cost.md) |
| Thompson Sampling | 多臂老虎机路由 | [ch08](./08-routing-and-cost.md) |
| Beta(α, β) | 二项分布先验 | [ch08](./08-routing-and-cost.md) |
| Codemod | 确定性代码改写 | [ch08](./08-routing-and-cost.md) |
| Agent Booster | LLM edit 快速合并 | [ch08](./08-routing-and-cost.md) |
| ADR-026 / ADR-143 | 路由 + codemod 决策 | [ch19](./19-references.md) |

---

## 3. 关键命令索引

### 3.1 安装与初始化

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest init` | 全量初始化项目（99% 场景） | [ch02](./02-install-and-init.md) |
| `npx ruflo@latest init --non-interactive --skip-prompts` | 非交互模式（CI） | [ch02](./02-install-and-init.md) |
| `npx ruflo@latest init wizard` | 向导模式（首次本地探索） | [ch02](./02-install-and-init.md) |
| `npx ruflo@latest init --dual` | Claude Code + Codex 双模 | [ch02](./02-install-and-init.md) |
| `npx ruflo@latest init upgrade --add-missing` | 增量升级（补缺失文件） | [ch18](./18-troubleshooting.md) |

### 3.2 健康与验证

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest doctor` | 26 项健康检查 | [ch02](./02-install-and-init.md) |
| `npx ruflo@latest doctor --fix` | 自动修复可修复项 | [ch02](./02-install-and-init.md) |
| `npx ruflo@latest verify` | Ed25519 签名校验 | [ch02](./02-install-and-init.md), [ch10](./10-security-and-aidefence.md) |
| `npx ruflo@latest status` | 概览：进程/内存/MCP | [ch13](./13-observability-and-ops.md) |

### 3.3 Swarm 与 Hive Mind

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest swarm init` | 初始化 swarm | [ch06](./06-swarm-coordination.md) |
| `npx ruflo@latest swarm monitor` | 实时监控 | [ch06](./06-swarm-coordination.md) |
| `npx ruflo@latest swarm scale` | 扩缩容 | [ch06](./06-swarm-coordination.md) |
| `npx ruflo@latest hive-mind spawn` | 启动蜂巢 | [ch06](./06-swarm-coordination.md) |
| `npx ruflo@latest hive-mind status` | 蜂巢状态 | [ch06](./06-swarm-coordination.md) |

### 3.4 Agent 与 Task

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest agent spawn --type <T>` | 创建 agent | [ch03](./03-first-conversation.md), [ch05](./05-agents-and-skills.md) |
| `npx ruflo@latest agent list` | 列出 agent | [ch03](./03-first-conversation.md) |
| `npx ruflo@latest agent status --id <X>` | 查状态 | [ch05](./05-agents-and-skills.md) |
| `npx ruflo@latest agent metrics` | 性能指标 | [ch13](./13-observability-and-ops.md) |
| `npx ruflo@latest task create` | 创建任务 | [ch11](./11-hooks-and-workers.md) |
| `npx ruflo@latest task assign` | 分配任务 | [ch11](./11-hooks-and-workers.md) |
| `npx ruflo@latest task status` | 任务状态 | [ch11](./11-hooks-and-workers.md) |

### 3.5 Memory（记忆）

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest memory store` | 写入 | [ch03](./03-first-conversation.md), [ch07](./07-memory-and-learning.md) |
| `npx ruflo@latest memory search` | 语义搜索 | [ch03](./03-first-conversation.md), [ch07](./07-memory-and-learning.md) |
| `npx ruflo@latest memory list` | 列出 | [ch07](./07-memory-and-learning.md) |
| `npx ruflo@latest memory retrieve` | 取键值 | [ch07](./07-memory-and-learning.md) |
| `npx ruflo@latest memory distill` | 提炼 pattern | [ch07](./07-memory-and-learning.md) |

### 3.6 Hooks（生命周期）

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest hooks list` | 列出 17 hooks | [ch03](./03-first-conversation.md) |
| `npx ruflo@latest hooks list --verbose` | 含路径/状态 | [ch18](./18-troubleshooting.md) |
| `npx ruflo@latest hooks route --task <X>` | 智能路由决策 | [ch03](./03-first-conversation.md), [ch08](./08-routing-and-cost.md) |
| `npx ruflo@latest hooks pre-task` | 手动触发 pre-task | [ch11](./11-hooks-and-workers.md) |
| `npx ruflo@latest hooks post-task` | 手动触发 post-task | [ch11](./11-hooks-and-workers.md) |
| `npx ruflo@latest hooks codemod` | 触发 Tier-1 codemod | [ch04](./04-architecture-deep-dive.md), [ch08](./08-routing-and-cost.md) |

### 3.7 Plugins（插件）

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest plugins install <name>` | 安装插件 | [ch12](./12-plugin-ecosystem.md) |
| `npx ruflo@latest plugins list` | 列出已装 | [ch12](./12-plugin-ecosystem.md) |
| `npx ruflo@latest plugins doctor` | 插件自检 | [ch12](./12-plugin-ecosystem.md) |
| `npx ruflo@latest plugins update <name>` | 更新插件 | [ch12](./12-plugin-ecosystem.md) |

### 3.8 MCP Server

| 命令 | 功能 | 首次出现 |
|------|------|---------|
| `npx ruflo@latest mcp start` | 启动 stdio server | [ch04](./04-architecture-deep-dive.md) |
| `npx ruflo@latest mcp status` | MCP 状态 | [ch04](./04-architecture-deep-dive.md) |
| `npx ruflo@latest mcp tools list` | 列出全部工具 | [ch04](./04-architecture-deep-dive.md) |

---

## 4. 信任等级全表（Trust Ladder）

| 等级 | 名称 | 解锁能力 | 升级条件 |
|------|------|---------|---------|
| **1** | UNTRUSTED | 只读公共内存 | 默认初始状态 |
| **2** | VERIFIED | mTLS 已认证身份 | 通过 mTLS 握手 |
| **3** | ATTESTED | 可执行普通工具调用 | 身份 + ed25519 签名通过 |
| **4** | TRUSTED | 可修改项目内存、spawn agent | 100+ 次成功任务 |
| **5** | PRIVILEGED | 部署、改密钥、跨账户 | 显式审批 + 长期行为 |

详见 [第 09 章 · Trust Ladder](./09-federation.md)。

---

## 5. 7 种 RL 算法

| 算法 | 类型 | ruflo 中的角色 |
|------|------|---------------|
| **PPO** | 策略优化 | 路由主算法 |
| **A2C** | Advantage Actor-Critic | Swarm 协调 |
| **DQN** | 价值函数 | 成本估算 |
| **Q-Learning** | 表格 Q | 简单路由 |
| **SARSA** | on-policy | 安全敏感路径 |
| **Decision Transformer** | 序列决策 | 长任务规划 |
| **Curiosity** | 探索奖励 | 模式发现 |

详见 [第 07 章 · 2.4](./07-memory-and-learning.md)。

---

## 6. MCP 命名空间家族

| 命名空间 | 工具数 | 用途 |
|---------|-------|------|
| `memory_*` | 30+ | 向量内存 + HNSW |
| `swarm_*` | 20+ | swarm 编排 |
| `agent_*` | 15+ | spawn/list/metrics |
| `hooks_*` | 17 | 生命周期回调 |
| `task_*` | 10+ | 任务管理 |
| `intelligence_*` | 10+ | 智能路由 |
| `agentdb_*` | 8 | AgentDB v3 |
| `github_*` | 10+ | GitHub 集成 |
| `browser_*` | 10+ | Playwright |
| `security_*` | 10+ | 安全检测 |
| `daa_*` | 10+ | 去中心化 agent |
| 其他 | 160+ | 扩展 |

详见 [第 04 章 · 2.2](./04-architecture-deep-dive.md)。

---

## 7. Worker 8 类详解

| Worker | 功能 | 触发时机 |
|--------|------|---------|
| `audit` | 安全审计 | 定时（每日） |
| `optimize` | 内存压缩（HNSW rebuild） | 内存 > 阈值 |
| `consolidate` | pattern 提炼 | post-task |
| `index` | 向量索引重建 | 大批量写入后 |
| `gc` | 过期内存回收 | 定时（每 6h） |
| `metrics` | 指标聚合 | 实时 |
| `snapshot` | .rvf 备份 | 定时（每日） |
| `replicate` | 跨机器同步 | 联邦场景 |

详见 [第 11 章 · Hooks 与 Workers](./11-hooks-and-workers.md)。

---

## 8. 3-Tier 路由成本对比

| Tier | 处理方式 | 延迟 | 单次成本 | 命中率（实测） |
|------|---------|------|---------|---------------|
| **1** | WASM codemod | ~1ms | $0 | ~30–50% 重构/格式化场景 |
| **2** | Haiku | ~500ms | $0.0002 | ~40% 轻量任务 |
| **3** | Sonnet | ~2s | $0.003 | ~10% 复杂任务 |
| **3** | Opus | ~5s | $0.015 | <5% 最复杂 |

详见 [第 08 章 · 智能路由](./08-routing-and-cost.md)。

---

## 9. ADR 速查表（核心 12 个）

| ADR | 标题 | 详见章节 |
|-----|------|---------|
| ADR-022 | MCP governance (default-deny) | [ch19](./19-references.md) |
| ADR-026 | Router 3-Tier | [ch08](./08-routing-and-cost.md) |
| ADR-096 | Encryption at rest | [ch10](./10-security-and-aidefence.md) |
| ADR-097 | Federation budget circuit breaker | [ch09](./09-federation.md) |
| ADR-104 | WSS transport | [ch09](./09-federation.md) |
| ADR-111 | WireGuard Mesh | [ch09](./09-federation.md) |
| ADR-112 | monotone-decreasing tool baseline | [ch04](./04-architecture-deep-dive.md) |
| ADR-118 | AIDefence 2.3.0 (3-gate) | [ch10](./10-security-and-aidefence.md) |
| ADR-120 | Federation peer (Rust) | [ch04](./04-architecture-deep-dive.md) |
| ADR-143 | Codemod scope | [ch08](./08-routing-and-cost.md) |
| ADR-147 | Arena (Copilot SDK / nested subagent) | [ch16](./16-extended-modules.md) |
| ADR-148 | Arena phase 2 (FastGRNN) | [ch16](./16-extended-modules.md) |
| ADR-150 | MetaHarness integration | [ch16](./16-extended-modules.md) |

---

## 10. 常见中英对照速查

| 中文 | English | 备注 |
|------|---------|------|
| 智能体 | Agent | 不译 |
| 蜂群 | Swarm | 不译 |
| 蜂巢心智 | Hive-Mind | 不译 |
| 钩子 | Hook | 不译 |
| 共识 | Consensus | 不译 |
| 路由器 | Router | 不译 |
| 工人 | Worker | 不译 |
| 女王 | Queen | 不译 |
| 证据 | Witness | 不译 |
| 沙箱 | Sandbox | 不译 |
| 联邦 | Federation | 不译 |
| 信任 | Trust | 不译 |
| 插件 | Plugin | 不译 |
| 拓扑 | Topology | 不译 |
| 记忆 | Memory | 不译 |
| 学习 | Learning | 不译 |
| 路由 | Routing | 不译 |
| 向量 | Vector | 不译 |
| 嵌入 | Embedding | 不译 |
| 提炼 | Distill | 不译 |
| 检索 | Retrieve / Search | search 用于内存；retrieve 用于通用 |
| 决策 | Decision / Route | 路由层的决策用 route |
| 等级 | Level / Ladder | Trust Ladder 信任阶梯 |

---

## 11. 小结

### 关键要点

- 本章覆盖 **60+ 核心术语**，**30+ 命令**，按 A–Z + 主题双索引
- 每个术语都能追溯到具体章节，**手册自我闭环**
- 5 级信任、8 类 worker、3-Tier 路由——这是「ruflo 速记法」
- **建议收藏本章**，作为日常速查手册

### 术语锚点

- 所有术语 → 对应章节
- 主题索引 → 横向串联
- 命令索引 → 速查速用
- ADR 索引 → 决策依据

### 下一步

👉 进入 [第 18 章 故障排查](./18-troubleshooting.md)，看 26 项 doctor 检查 + 7 类常见报错。

### 参考链接

- USERGUIDE §Glossary：<https://github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md#glossary>
- CLAUDE.md §Behavioral Rules：<https://github.com/ruvnet/ruflo/blob/main/CLAUDE.md>
- ADR 索引：<https://github.com/ruvnet/ruflo/tree/main/v3/docs/adr>

---

> 本章是手册的「**沉淀**」章节。后续若新增术语，按 A–Z 直接追加，无需重排。