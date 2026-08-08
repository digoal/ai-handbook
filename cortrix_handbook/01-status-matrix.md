# 01 · 能力状态总表

> **目标读者**:所有读者(尤其用户和决策者)。
> **阅读时间**:5 分钟。
> **关键事实**:Cortrix `v1.0.0-rc.1` 是**预发布**,不是生产就绪。下面这张表是手册全篇"能不能用"问题的唯一答案。

---

## 状态标签的语义

来自 `README.md:55-61`,四个标签是**官方统一答案**:

| 标签 | 含义 | 本手册的态度 |
|---|---|---|
| ✅ `Verified` | 代码 + spec + 测试 + e2e 验证都支撑 | 描述完整用法,可以照做 |
| 🟡 `Verification required` | 代码存在,但 public-readiness 仍待 e2e 验证 | 描述存在性与接口,**不保证生产可用** |
| 🚫 `Blocked` | 当前运行时不工作或与文档不一致 | **只描述计划,不描述"怎么用"** |
| 🗺️ `Roadmap` | 未来版本(V1.5 / V2.0) | 只描述设计意图 |

> ⚠️ **手册的硬规则**:绝不承诺任何 `Blocked` 项的可执行用法。看到「这个能力能做 X」就意味着它至少是 `Verification required`,且用法经过实测。

---

## 1. 顶层能力矩阵

> 综合自 `README.md:64-75`、`docs/compatibility.md`、`sdk/python/README.md:147-155`、`cortrix-agent/README.md`。

| 能力 | 状态 | 备注 |
|---|---|---|
| **OpenAPI 文件存在** | ✅ Verified | `api/openapi.yaml` 已声明完整 API surface |
| **本地 Docker Quickstart** | 🟡 Verification required | Docker compose 可启动,但需 e2e 复核 |
| **本地健康检查** `/api/v1/system/health/ready` | 🟡 Verification required | 端点存在,文档完整 |
| **Namespaces CRUD** | 🟡 Verification required | SDK 接口 + 测试覆盖完整 |
| **Documents 上传 + 异步任务** | 🟡 Verification required | F42 路径完整,异步任务进度接口可用 |
| **Query(混合检索 + rerank)** | 🟡 Verification required | F04 pipeline 存在,实测需自行复核 |
| **跨 Namespace 检索** | � Verification required | `namespaces=["*"]` 接口已声明 |
| **MCP Server(stdio)** | 🟡 Verification required | 29 + 2 工具 + 测试覆盖完整 |
| **Python SDK** | 🟡 Verification required | 12 resource,17 测试模块,httpx mocked |
| **Built-in Agent chat(F48)** | 🟡 Verification required | FastAPI + SSE,固定流 RAG |
| **Auth login** | 🚫 **Blocked** | spec 已定义,但运行时存在契约漂移 |
| **Tenant / Member / ACL / Quota** | � **Blocked** | spec 已定义,运行时与文档待对齐 |
| **MEM02 LLM 自动抽取** | 🚫 **Blocked** | 验证观察到 LLM 传输超时路径 |
| **RBAC + Tenant 隔离拒绝矩阵** | 🚫 **Blocked** | 当前 auth-disabled 本地运行时无法证明 |
| **Full-corpus BEIR 检索质量** | ✅ Verified | SciFact / FiQA / NFCorpus 已发布测量(`README.md:75`) |
| **CUDA 部署路径** | 🟡 Verification required | `docker-compose.cuda.yml` + 文档完整 |
| **远程 MCP Streamable HTTP** | 🗺️ Roadmap | 当前仅 stdio |

---

## 2. SDK 资源状态明细

来自 `sdk/python/README.md:68-82`、`sdk/python/cortrix/resources/` 各文件。

| Resource | 状态 | 备注 |
|---|---|---|
| `client.documents.upload` / `batch_submit` / `upload_and_wait` | � Verification required | 接口 + 测试完整 |
| `client.namespaces.create/list/get/update/delete` | 🟡 Verification required | |
| `client.namespaces.set_permission`(ACL) | 🚫 Blocked | 涉及被 Block 的 ACL 路径 |
| `client.query.run` / `client.search` | 🟡 Verification required | `_adapt_wire_result` 字段翻译已声明 |
| `client.memory.search/log/extract/list/create/edit/invalidate` | 🟡 Verification required | MEM02 抽取本身 `Blocked` |
| `client.memory.opt_out`(MEM04) | 🟡 Verification required | |
| `client.sql.query`(Text-to-SQL) | 🟡 Verification required | 扩展部署可用,403 → `FeatureNotAvailableError` |
| `client.watchers.*` | � Verification required | |
| `client.sync.configure/status/stop/trigger` | 🟡 Verification required | 扩展部署 |
| `client.auth.*` | 🚫 Blocked | Auth login Blocked |
| `client.system.health/version/namespace_stats` | 🟡 Verification required | |
| `client.tenants.*` | 🚫 Blocked | Tenant 管理 Blocked |
| `client.ops.gc.{status,run,restore,purge}` | 🟡 Verification required | `run`/`purge` 需 `X-Ops-Confirm: true` |
| `client.ops.list_operations` | 🟡 Verification required | F18a |
| `client.import_database`(F16a) | 🟡 Verification required | |

---

## 3. Skills(MCP / 框架适配)状态

来自 `cortrix-skills/src/cortrix_skills/toolkit.py:39-77`、`cortrix-mcp/src/cortrix_mcp/tools/`。

| 工具组 | 数量 | 状态 | 备注 |
|---|---|---|---|
| MVP 工具组(`cortrix_*`) | 12 | 🟡 Verification required | `health` / `query` / `upload` / `list_*` / `create_namespace` / `memory_search` / `log_interaction` / `document_status` / `add_watcher` / 等 |
| Extended 工具组 | 4 | 🟡 Verification required | `cross_ns_query` / `async_upload` / `memory_search_filter` / `memory_extract_trigger` |
| New 工具组 | 4 | 🟡 Verification required | `memory_extract` / `task_status` / `cancel_task` / `query_explain` |
| MEM02 反向 | 2 | 🚫 Blocked | `memory_get_audit` / `memory_revoke_fact` 受 MEM02 Blocked 影响 |
| MEM04 反向 | 1 | 🟡 Verification required | `memory_opt_out` |
| TD-F42-BULK | 1 | 🟡 Verification required | `batch_submit` |
| F18a | 1 | 🟡 Verification required | `list_operations` |
| MEM03 CRUD | 4 | 🟡 Verification required | `memory_list` / `_create` / `_edit` / `_invalidate` |
| **总计工具方法** | **29** | — | 与 MCP P12 SoT 1:1 对应 |
| Admin 工具(MCP only) | 2 | 🟡 Verification required | `admin_*` |

---

## 4. Built-in Agent(F48)状态

来自 `cortrix-agent/README.md`、`cortrix-agent/agent_core/executor.py:95`。

| 能力 | 状态 | 备注 |
|---|---|---|
| `ChatExecutor`(固定 RAG 流) | 🟡 Verification required | V1.0 默认,L1/L2/L3 降级 |
| `ToolUseExecutor`(LLM 工具调用) | 🗺️ Roadmap | V1.5 |
| `PlanExecuteExecutor`(规划 + 执行) | 🗺️ Roadmap | V2 |
| 6 个 LLM 适配器 | 🟡 Verification required | OpenAI / Claude / Ollama / GLM / DeepSeek / Mock |
| SSE 流式 chat | � Verification required | `routes/chat.py:85` |
| Memory 联动(MEM02 触发) | 🚫 Blocked | 受 MEM02 Blocked 影响 |
| Session 持久化 | � Verification required | `SessionStore` 内存,N=10 滑动窗口 |
| 注入硬化 prompt | 🟡 Verification required | `prompt.py:64-131` |
| `?explain=true` 元数据 | 🟡 Verification required | A/B/C 三档 |
| `?debug=true` | 🟡 Verification required | |

---

## 5. 部署形态状态

来自 `deploy/`。

| 部署形态 | 状态 | 备注 |
|---|---|---|
| Docker Compose(CPU) | 🟡 Verification required | `deploy/docker-compose.yml` |
| Docker Compose(CUDA) | 🟡 Verification required | `deploy/docker-compose.cuda.yml`,需 NVIDIA runtime |
| 源码构建 | 🟡 Verification required | `dev.sh` + CMake |
| macOS 源码构建 | 🟡 Verification required | Apple Silicon + CoreML 自动检测 |
| Caddy 反代 | 🟡 Verification required | `deploy/caddy/Caddyfile` |
| supervisord | 🟡 Verification required | `deploy/supervisord.conf` |
| 模型下载 | ✅ Verified | 约 1.17 GB,SHA-256 锁定(`README.md:101`) |

---

## 6. 兼容性细节

来自 `docs/compatibility.md`、`sdk/python/README.md:147-155`。

| 项目 | 状态 |
|---|---|
| Python `>=3.9` | ✅ Verified |
| httpx `>=0.25,<1.0` | ✅ Verified |
| AGPL-3.0-only | ✅ Verified |
| 状态:Auth login 与文档不一致 | 🚫 Blocked |
| 状态:Tenant / RBAC / Quota | 🚫 Blocked |
| 状态:MEM02 提取 | 🚫 Blocked |
| 状态:远程 MCP Streamable HTTP | 🗺️ Roadmap |
| 状态:V1.5 / V2 Executor | �️ Roadmap |

---

## 7. 怎么读这张表

| 你想做的事 | 状态门槛 | 该读哪一章 |
|---|---|---|
| 跑一个本地 demo | 🟡 Verification required 即可 | [20-quickstart.md](part-2-user/20-quickstart.md) |
| 在生产里跑多租户 | 至少要等 Auth / Tenant 升到 ✅ | [40-deploy.md](part-4-operator/40-deploy.md)+ 等升级 |
| 集成到自家 Agent | 🟡 Verification required 即可,使用 SDK / Skills | [30-sdk-overview.md](part-3-developer/30-sdk-overview.md) |
| 自动抽取 Memory | 等 MEM02 解 Block | [31-resources.md §memory](part-3-developer/31-resources.md) |
| 远程 MCP 部署 | 等 Streamable HTTP 上线 | [35-mcp-server.md](part-3-developer/35-mcp-server.md) |

---

## 下一步

👉 **[第一篇 · 10 · Cortrix 是什么](part-1-architect/10-what-is-cortrix.md)** — 架构师视角,从全貌开始
