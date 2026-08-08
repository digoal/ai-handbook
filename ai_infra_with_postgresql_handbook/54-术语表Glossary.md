# §54 术语表 Glossary

> 🏛️ 架构师 · 👤 用户 · 🧑‍💻 开发者
>
> **一句话定位**:Handbook 中涉及的所有关键术语的精确定义 — 读源码和文档时的"标准字典"。

---

## A

### Action Card
Channel 内可执行的"动作卡片",成员点击触发特定操作(部署/审批/查询)。需要 `require_approval` 可选。

来源:[`16_v4_3_0_identity_channels.sql`](../../scripts/deploy/16_v4_3_0_identity_channels.sql) - `cx_action_cards`

### Agent
平台管理的"业务主体",可以是平台托管或外部运行时(OpenClaw/Hermes)。Agent 必须先注册才能进入治理范围。

### Agent Principal
`cx_principals` 表中 `principal_type='AGENT'` 的行,代表一个注册过的 Agent 身份。

### Apache AGE
PostgreSQL 的图扩展,提供 Cypher 查询能力。在本平台**只用作属性图投影**,关系表仍是权威。

来源:[`docs/architecture.md:588`](architecture.md)

### Approval(N-of-M)
高风险决策的多人审批机制,需要至少 N 个人 ALLOW 才能放行,职责分离 + 不可变 + 幂等。

来源:[§17 Enterprise 治理](17-Enterprise治理与合规控制面.md)

### Argon2id
密码哈希算法,默认 `time_cost=3, memory_cost=65536 KB, parallelism=1`,输出 PHC 字符串格式。

---

## B

### Barrier
协作关卡,多个 Agent 报到后由唯一胜出者获得结果。不可变参与快照、不可变角色要求、幂等证据。

来源:[§40 频道-关卡-审批](40-频道-关卡-审批.md)

### Branch(上下文分支)
Git 风格的上下文分支,支持 fork/merge/abandon/pause/resume。Parent 通过 `parent_branch_id` 形成链。

来源:[`lib/branch_api.py`](../../scripts/lib/branch_api.py)

### Bridge
跨域 Channel 之间的有策略通道,用于跨域传递消息。需要 explicit classification_check 和 redaction_policy。

来源:[§40 频道-关卡-审批](40-频道-关卡-审批.md)

### Business Agent
平台"业务"使用的 Agent,使用独立 PostgreSQL LOGIN 角色,**永远不**获取 Schema Owner 凭据。

---

## C

### Capability
平台功能单元(如 `memory`、`compliance`),可用性 = 包内物理存在 + 数据库启用 + Principal 授权三交集。

来源:[§19 Profile 与 Capability 配置平面](19-Profile与Capability配置平面.md)

### Channel
协调面,用于成员(人类+Agent)间消息传递。**不是**权限放大器。

来源:[§40 频道-关卡-审批](40-频道-关卡-审批.md)

### Checkpoint
Graph Runtime 的状态快照,记录到 `graph_checkpoints`。Worker 替换时从最近 Checkpoint 恢复。

来源:[§14 Graph Runtime 架构](14-Graph-Runtime架构.md)

### Compliance Controller ⚠️企业版
v4.3.4 引入的确定性后台线程,30 秒周期评估 Agent 合规姿态,**不**做模型调用,只对高置信规则自动处置。

来源:[§41 合规控制面 v4.3.4](41-合规控制面v4.3.4.md)

### CSRF
Cross-Site Request Forgery 防护。客户端从 Cookie 读取 csrf 值,放进 `X-CSRF-Token` header。

### Current Pointer
Memory Family 指向当前 Version 的指针。迁移"删除"只是改指针,不物理删除。

---

## D

### Data Grant ⚠️ Oracle
Oracle Deep Security 的细粒度访问控制,功能上等同 PostgreSQL RLS,但**强**于 RLS(MAC 强制)。

### Dynamic Graph
v4.3.3 起的**预览**能力,允许运行时修改 Graph Definition(创建子 Version,不能改源)。**默认关闭**。

来源:[`lib/graph_dynamic.py`](../../scripts/lib/graph_dynamic.py)

---

## E

### Ed25519
一种椭圆曲线签名算法,在 v4.3.4+ 用于 Gateway 凭据激活证明。

来源:[§41 合规控制面 v4.3.4](41-合规控制面v4.3.4.md)

### Edition
平台版本,分为 Community(Apache 2.0)和 Enterprise(BSL 1.1)。这是**构建期**的物理边界,运行时无法跨越。

来源:[`lib/edition_features.py`](../../scripts/lib/edition_features.py)

### Enrollment Token
一次性 token,绑定 sponsor/owner/runtime/environment/risk tier/quota,Agent 用它兑换凭据。

来源:[§13 注册 Agent 治理平面](13-注册Agent治理平面.md)

### Evidence
带签名的合规证据对象,Agent 提交后受 bounded validity。过期 Evidence 触发 `DEGRADED` 状态。

来源:[§41 合规控制面 v4.3.4](41-合规控制面v4.3.4.md)

### Exception(限时例外)
合规受限时的限时放宽,需要 compensating_controls 和独立 Human 审批。

---

## F

### Family(Memory)
Memory 的"主题",稳定 ID + 当前 Version 指针。Family 有多种 scope(RUNTIME_CONTEXT/CHANNEL_MEMORY/...)。

来源:[§15 Memory Lifecycle 架构](15-Memory-Lifecycle架构.md)

### Fencing Token
单调递增整数,Worker 提交时校验。防止过期 Worker 覆盖新 Attempt。

来源:[§14 Graph Runtime 架构](14-Graph-Runtime架构.md)

### FIVE 信号混合搜索
向量 + 全文 + 关系图 + 标签 + 关系元数据的加权融合,默认权重 0.4/0.25/0.15/0.1/0.1。

来源:[§35 知识库管理](35-知识库管理.md)

---

## G

### Gateway
平台对外部 Agent 的接入层,提供凭据、实例、事件投递、动作执行。节点级 instance fencing。

来源:[§48 外部框架 Gateway 接入](48-外部框架Gateway接入.md)

### Graph Definition
Graph 的 JSON 定义,带 provenance、依赖、签名(可选)。Draft 可编辑,Published 不可变。

来源:[§14 Graph Runtime 架构](14-Graph-Runtime架构.md)

### Graph Runtime
数据库权威的 Graph 执行内核,持久 Run + Checkpoint + Lease + Fencing + Transition。

---

## H

### Harness
可复用的 Agent 执行蓝图,带 input_schema / output_schema / execution_mode。内置 5 个模板。

来源:[§37 技能与规格管理](37-技能与规格管理.md)

### Human Principal
`cx_principals` 表中 `principal_type='HUMAN'` 的行,代表一个人类用户。

---

## I

### Idempotency Key
保证重放安全的唯一键。同 key + 同 payload 的重复请求返回同一结果。

来源:[§14 Graph Runtime 架构](14-Graph-Runtime架构.md)

### Instance(Agent 实例)
`cx_agent_instances` 表的一行,代表 Agent 在某节点上的运行实例,带 fencing token。

来源:[§13 注册 Agent 治理平面](13-注册Agent治理平面.md)

### Isolation Mode
Workspace 的隔离模式:SHARED(Entity 可选 workspace_id) 或 ISOLATED(Entity 必须带 workspace_id)。

来源:[§34 工作区与上下文连续性](34-工作区与上下文连续性.md)

---

## K

### KDF
Key Derivation Function。从主密钥派生加密密钥,本平台用 PBKDF2-HMAC-SHA512。

来源:[§43 加密机制与密钥管理](43-加密机制与密钥管理.md)

### Knowledge
长期验证过的事实,与 Memory 的"短期/未验证"相对。

来源:[§35 知识库管理](35-知识库管理.md)

---

## L

### Legal Hold ⚠️企业版
合规证据的"法律保留"状态,**永不**被自动清理。

来源:[§42 审计与证据导出](42-审计与证据导出.md)

### Lease Token
短期 token,Worker claim 后持有,过期失效。配合 fencing token 双重保护。

来源:[§14 Graph Runtime 架构](14-Graph-Runtime架构.md)

### Loop
"持续迭代 + 自评估"的执行单元,4 代 AI 方法论。带 Intent → Context → Action → Observation → Adjustment 循环。

来源:[§38 协作分支与循环工程](38-协作分支与循环工程.md)

---

## M

### Mandatory(强制受保护)
Capability 标志,`mandatory='Y'` 不能被禁用(身份/授权/安全/审计/Agent/用户/平台配置)。

来源:[§19 Profile 与 Capability 配置平面](19-Profile与Capability配置平面.md)

### Master Key
config.json 加密的主密钥,默认存储在 `$XDG_DATA_HOME/chuanxu/master.key`。

### Memory
短期/Agent 私有的内容。v4.3.2 起版本化为 Family + Version。

来源:[§15 Memory Lifecycle 架构](15-Memory-Lifecycle架构.md)

### Memory Type
EPISODIC / FACT / PREFERENCE / DECISION / PROCEDURAL / EXPERIENCE 六种类型。

### Memory Scope
RUNTIME_CONTEXT / CHANNEL_MEMORY / AGENT_MEMORY / WORKSPACE_MEMORY / ENTERPRISE_KNOWLEDGE 五种作用域。

### Memory Lifecycle State
CANDIDATE / ACTIVE / STALE / CONFLICTED / SUPERSEDED / EXPIRED / MIGRATED / ARCHIVED / QUARANTINED / UNAVAILABLE 十种状态。

### MCP
Model Context Protocol,平台通过 `mcp_server.py` 暴露 10+ 工具给外部 Agent。

来源:[§25 MCP Server 与 SKILL 契约](25-MCP-Server与SKILL契约.md)

---

## N

### N-of-M Approval
高风险决策需要 N 个 Approver 同意的机制。

---

## O

### OAuth
本平台**不直接**使用 OAuth,但通过 OIDC connector 链接外部身份(预留)。

来源:[§12 身份与 Principal 控制面](12-身份与Principal控制面.md)

### Organization
数据库权威的组织架构,带闭包授权,支持主/兼职、汇报关系、变更草稿。

来源:[§16 Organization Governance 架构](16-Organization-Governance架构.md)

---

## P

### PENDING_ACTIVATION
Agent 注册后必须通过的"凭据激活"状态(v4.3.4+)。完成 Gateway 激活证明后转为 ACTIVATED。

### Permission Version
会话携带的权限快照版本,角色变更时自动失效所有旧会话。

来源:[§12 身份与 Principal 控制面](12-身份与Principal控制面.md)

### pgcrypto
PostgreSQL 的加密扩展,用于数据库列级加密(`pgp_sym_encrypt` / `pgp_sym_decrypt`)。

### pgvector
PostgreSQL 的向量扩展,提供 `vector` 类型与 `<=>`(余弦距离)操作符。

### Pipeline Profile
社区版支持 4 种:`production` / `graph-preview` / `development` / `experimental-4.2`。

来源:[`docs/architecture.md:84-86`](architecture.md)

### Principal
经过认证的"主体",可以是 HUMAN/AGENT/SERVICE。所有 API 请求必须解算到 Principal,失败 fail-closed。

来源:[§12 身份与 Principal 控制面](12-身份与Principal控制面.md)

### Profile ⚠️企业版
不可变、合规约束模板。Profile 永远**不**授予 Principal/DB/Tool/API/Model/Secret/Network 权限。

来源:[§41 合规控制面 v4.3.4](41-合规控制面v4.3.4.md)

---

## R

### Reachable(可达)
Graph 中从某节点出发的多跳可达节点集合,最大跳数受防护(默认 ≤ 6)。

来源:[§39 图探索与可视化](39-图探索与可视化.md)

### RESTRICTED
Agent 的合规控制状态,保留心跳/Evidence/整改/恢复能力,失去正常业务能力。

来源:[§41 合规控制面 v4.3.4](41-合规控制面v4.3.4.md)

### Retention
数据留存期,可配置。Legal Hold 状态不受 retention 限制。

来源:[§42 审计与证据导出](42-审计与证据导出.md)

### RLS
Row-Level Security,PostgreSQL 的行级安全。本平台用于 Agent 隔离。

### Run(Graph Run)
Graph Runtime 的运行时实例,带 state_hash、Run context、Checkpoint 链。

---

## S

### Schema Owner
数据库管理员用户,Business Agent 永远拿不到它的凭据。

来源:[§12 身份与 Principal 控制面](12-身份与Principal控制面.md)

### Session
Web 会话,带 session_id / permission_version / csrf_token / expires_at。

### Snapshot(Memory)
绑 Principal/Instance 的上下文快照,带 subject_fencing。

来源:[§15 Memory Lifecycle 架构](15-Memory-Lifecycle架构.md)

### Spec
规范文档,Spec-Driven Development 的核心工件。可链接到 Plan,Plan 可被 Spec 验证。

来源:[§37 技能与规格管理](37-技能与规格管理.md)

### SP/Sub-partition
`entities` 表按 LIST(ENTITY_TYPE) + RANGE(CREATED_AT)双重分区,共 6 × 7 = 42 子分区。

### State Event
Graph Runtime 的 delta 事件,append-only,带 state_hash。

来源:[§14 Graph Runtime 架构](14-Graph-Runtime架构.md)

---

## T

### Task Plan
Agent 任务的"有序步骤集合",带依赖、工具调用、上下文快照。

来源:[§33 任务计划与执行](33-任务计划与执行.md)

### TOTP
Time-based One-Time Password,RFC 6238。MFA 因子之一。

来源:[§12 身份与 Principal 控制面](12-身份与Principal控制面.md)

### Transition
Graph Runtime 的状态变更事件,与 State Event / Checkpoint / budget accounting 在同一事务。

### TRIGGERED vs CONTINUOUS
Graph 触发器的两种模式:MANUAL/API/SCHEDULE 触发,vs DATABASE 持续监听。

---

## U

### UNAVAILABLE
Memory Lifecycle State 之一,逻辑不可用,物理行保留。

来源:[§15 Memory Lifecycle 架构](15-Memory-Lifecycle架构.md)

---

## V

### Version(Memory Version)
不可变的 Memory 内容快照,每次更新创建新 Version,旧 Version 永远在历史。

### Version(Graph Version)
Graph Definition 的版本化,带 version_no, status, signature 等。

---

## W

### Workspace
Agent 协作的"项目空间",支持 Context Chain 和 Handoff。

来源:[§34 工作区与上下文连续性](34-工作区与上下文连续性.md)

### Worker
执行 Graph Node 的进程,持 Lease + Fencing Token。

---

## Z

### Zero Trust
零信任架构。本平台通过 Principal 解算 + Capability 检查 + RLS + 审计实现。

---

## 缩写对照表

| 缩写 | 全称 |
|---|---|
| AGE | Apache Graph Extensions |
| API | Application Programming Interface |
| BSL | Business Source License |
| CAP | Capability |
| CSRF | | Cross-Site Request Forgery |
| DB | Database |
| DSL | Domain-Specific Language |
| DTO | Data Transfer Object |
| FQDN | Fully Qualified Domain Name |
| HA | High Availability |
| HTTP | HyperText Transfer Protocol |
| HTTPS | HTTP Secure |
| ID | Identifier |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| KDF | Key Derivation Function |
| LDAP | Lightweight Directory Access Protocol |
| LLM | Large Language Model |
| MAC | Mandatory Access Control |
| MCP | Model Context Protocol |
| MFA | Multi-Factor Authentication |
| N-of-M | N-out-of-M (Approval) |
| OIDC | OpenID Connect |
| OTP | One-Time Password |
| PG | PostgreSQL |
| POC | Proof of Concept |
| PII | Personally Identifiable Information |
| PL/pgSQL | PostgreSQL Procedural Language |
| RBAC | Role-Based Access Control |
| RLS | Row-Level Security |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SCIM | System for Cross-domain Identity Management |
| SHA | Secure Hash Algorithm |
| SLA | Service Level Agreement |
| SQL | Structured Query Language |
| SSL | Secure Sockets Layer |
| SSO | Single Sign-On |
| TCP | Transmission Control Protocol |
| TLS | Transport Layer Security |
| TOTP | Time-based One-Time Password |
| UI | User Interface |
| UUID | Universally Unique Identifier |
| VPD | Virtual Private Database (Oracle) |
| WAL | Write-Ahead Log |
| WASM | WebAssembly |
| WIP | Work In Progress |
| YAML | YAML Ain't Markup Language |

---

## 交叉引用

- 所有其他章节:本术语表是 handbook 的"字典",可随时查阅
- 现有文档:[`docs/`](../) 中各文档有章节级术语说明

> 📌 **Part VI 完。Handbook 已完成**。回到 [§00 总目录](00-总目录.md) 或根据你的角色继续阅读。