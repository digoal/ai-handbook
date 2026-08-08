# 00 · 术语表(Glossary)

> **目标读者**:首次接触 Cortrix 的所有读者。
> **阅读时间**:5 分钟。
> **关键事实**:看到代号不懵;术语在 handbook 全篇用法一致。

---

## 0. 关于代号体系

Cortrix 内部使用**特征代号**(feature ID)+ **规格代号**(spec ID)命名模块与文件:

| 类别 | 代号示例 | 含义 |
|---|---|---|
| Feature | `F02` / `F04` / `F07` / `F08` / `F14` / `F36` / `F37` / `F41` / `F42` / `F48` | 已上线的功能模块 |
| Phase | `P08` / `P09` / `P12` / `P14` / `P04` | 设计阶段(spec 阶段) |
| Wave | `R9` / `R11+` | 测试覆盖阶段 |
| TD | `TD-F42-BULK` | Tech-Debt / 批量子任务 |

**约定**:在 handbook 与源码中,这些代号通常以 `#` / `:` 后跟功能名出现,例如 `F04 query pipeline`、`P12 MCP tool`、`MEM02 extraction`。

---

## 1. 核心领域概念

| 术语 | 英文 | 一句话定义 | 出现位置 |
|---|---|---|---|
| **命名空间** | Namespace | 文档 / 块 / 记忆 / 查询的逻辑边界,等价于一个独立的"数据集"。 | `README.md:138` |
| **文档** | Document | 上传到 Namespace 的原始素材(PDF / Word / 图片),经过解析后产生可检索块。 | `README.md:139` |
| **块** | Block | 由 Document 切分出的可检索单元,含 `content` + 元数据。 | `README.md:140`、`sdk/python/cortrix/types/_generated.py` 内 `QueryResultItem` |
| **查询** | Query | 对一个或多个 Namespace 的检索请求,可包含 top_k / rerank / filter。 | `README.md:141` |
| **记忆** | Memory | 跨会话的长期信息,既可显式写入也可从交互中抽取(MEM01–05)。 | `README.md:142` |
| **Tenant** | Tenant | 多租户隔离单元;每个 API Key 绑定一个 Tenant,跨 Tenant 默认拒绝。 | `README.md:118`、config.yaml 第 33 行 |
| **ACL** | Namespace ACL | 在 Namespace 上的细粒度授权(给某个 Tenant 读写权限)。 | `api/examples/acl/` |
| **配额** | Quota | 每 Tenant 的调用上限。 | `README.md:118`、`_exceptions.py:206-207` |

---

## 2. 模块代号速查

| 代号 | 全名 / 含义 | 引用 |
|---|---|---|
| `F02` | Cross-encoder reranker(bge-reranker-v2-m3 ONNX) | `config.yaml.example:83-99`、`deploy/model-manifest.tsv` |
| `F04` | Query pipeline(向量 + BM25 + rerank + CRAG) | `src/query/`、`src/retrieval/`、`src/reranker/` |
| `F07` | Docling / PaddleOCR 解析桥接 | `scripts/{docling_bridge,paddleocr_bridge}.py` |
| `F08` | 数据库迁移(初始 schema) | `db/migrations/f08_*.sql` |
| `F14` | pgcortrix / SQL 扩展 filter | `_exceptions.py:177-178` |
| `F36` | RAG-Fusion Expand Queries | `_exceptions.py:182-183` |
| `F37` | CRAG(Corrective RAG)LLM 评估 | `_exceptions.py:186-187` |
| `F41` | Doc Summary(摄取时生成摘要) | `_exceptions.py:190-191` |
| `F42` | 文档异步任务 / 批量提交 | `db/migrations/f42_*.sql`、`api/examples/documents/` |
| `F48` | 内置 Agent(ChatExecutor) | `_exceptions.py:194-195`、`cortrix-agent/agent_core/executor.py:95` |
| `MEM01` | Memory 写入 / 抽取 | `api/examples/memory/` |
| `MEM02` | Memory LLM 抽取(自动) | `cortrix-agent/agent_core/mem_coprocess.py:27` |
| `MEM03` | Memory CRUD(create/list/edit/invalidate) | `cortrix-skills/src/cortrix_skills/toolkit.py:39-77`(#26-29) |
| `MEM04` | Memory opt-out(用户撤回) | `_exceptions.py:23-26`(`db/migrations/023_mem04_opt_out`) |
| `MEM05` | Memory user_id 隔离(必须) | `api/examples/memory/search_success/python.py:1-14` |
| `P-HNSW` | Persistent HNSW(向量化索引持久化方案) | `src/store/phnsw/`、`src/store/phnsw/hnswlib/`(vendored fork) |
| `P12` | MCP tool 命名规范(SoT) | `cortrix-skills/src/cortrix_skills/toolkit.py:1-10` |
| `P14` | Skills 框架适配规范 | `cortrix-skills/src/cortrix_skills/adapters/` |
| `P04` | SDK 错误信封规范 | `sdk/python/cortrix/_exceptions.py:1-13` |
| `GEN-Agent` | "Agent 友好"错误协议(4 字段) | `sdk/python/cortrix/_exceptions.py:9-12`(`AGENT_FRIENDLY.md` issue 4) |

---

## 3. 错误代号(`CX_ERR_*`)

`CX_ERR_*` 是 Cortrix 服务端返回的错误 `code` 字段的稳定标识。SDK 的 `_exceptions.py:218-246` 中的 `CODE_EXCEPTION_MAP` 是其权威映射。

| 代号 | SDK 异常类 | HTTP 状态 |
|---|---|---|
| `CX_ERR_NAMESPACE_NOT_FOUND` | `NamespaceNotFoundError` | 404 |
| `CX_ERR_AUTH_INVALID_CREDENTIALS` | `AuthInvalidCredentialsError` | 401 |
| `CX_ERR_AUTH_TOKEN_EXPIRED` | `AuthTokenExpiredError` | 401 |
| `CX_ERR_AUTH_INVALID_API_KEY` | `AuthInvalidApiKeyError` | 401 |
| `CX_ERR_AUTH_ADMIN_REQUIRED` | `AuthAdminRequiredError` | 403 |
| `CX_ERR_AUTH_CSRF_MISMATCH` | `CsrfMismatchError` | 403 |
| `CX_ERR_STORE_NOT_FOUND` | `StoreNotFoundError` | 404 |
| `CX_ERR_STORE_DB_ERROR` | `StoreDbError` | 503 |
| `CX_ERR_F14_INVALID_FILTER` | `F14InvalidFilterError` | 400 |
| `CX_ERR_F36_EXPAND_TIMEOUT` | `F36ExpandQueriesTimeoutError` | timeout |
| `CX_ERR_F37_CRAG_EVAL_FAILED` | `F37CragEvaluationFailedError` | 500 |
| `CX_ERR_F41_DOC_SUMMARY_FAILED` | `F41DocSummaryFailedError` | 500 |
| `CX_ERR_F48_TOOL_NOT_FOUND` | `F48AgentToolNotFoundError` | 404 |
| `CX_ERR_MEM02_EXTRACTION_FAILED` | `MEM02ExtractionFailedError` | 500 |
| `CX_ERR_LLM_CIRCUIT_OPEN` | `LlmCircuitOpenError` | 503 |
| `CX_ERR_QUOTA_*` | `QuotaExceededError`(按前缀) | 429 |

> ⚠️ **`CX_ERR_AUTH_*` 当前 `Blocked`**(`README.md:71`),表中异常类已定义,但运行时一致性未在生产验证。

---

## 4. GEN-Agent 4 字段(Agent 友好错误协议)

每个 `CortrixError` 必带(`sdk/python/cortrix/_exceptions.py:32-55`、`_base_client.py:172-200`):

| 字段 | 类型 | 含义 | Agent 用途 |
|---|---|---|---|
| `retryable` | `Optional[bool]` | 服务端声明此错误可重试 | 自动重试判定 |
| `category` | `Literal["auth", "quota", "transient", "permanent", "timeout"]` | 错误类别 | 路由决策 |
| `retry_after_ms` | `Optional[int]` | 服务端建议等待毫秒数 | 退避策略 |
| `structured_data` | `Optional[dict]` | 服务端携带的结构化数据 | 自动修复输入 |

Agent 框架(Claude Tools / OpenAI Functions / LangChain)收到错误时,这 4 个字段**不丢失**,而是包装成 `tool_result is_error` / `role:"tool"` JSON / `ToolException` 文本,见 `cortrix-skills/src/cortrix_skills/adapters/*`。

---

## 5. 端口与进程

| 进程 | 默认端口 | 备注 |
|---|---|---|
| `cortrix-server`(C++) | **8420** | 主 API,前缀 `/api/v1` |
| `cortrix-agent`(FastAPI) | **8001** | 内置 Agent chat(SSE) |
| Web UI | dev 端口由 Vite 决定 | 容器化后通过 Caddy 反代 |
| `cortrix-mcp` | **stdio** | 默认是 stdio transport,远程 Streamable HTTP 是 Roadmap |
| PostgreSQL(可选 + pgcortrix) | 5432 | 与 `cortrix-server` 物理分离 |

---

## 6. SDK 资源命名空间

12 个挂在 `Cortrix` / `AsyncCortrix` 上的属性(`sdk/python/cortrix/_client.py:38-73`):

| 属性 | 文件 | 领域 |
|---|---|---|
| `client.documents` | `resources/documents.py` | 文档上传 / 列表 / 任务 / 批量 |
| `client.namespaces` | `resources/namespaces.py` | 命名空间 CRUD + ACL |
| `client.query` | `resources/query.py` | 语义检索(快捷方式:`client.search`) |
| `client.memory` | `resources/memory.py` | MEM01–05 |
| `client.sql` | `resources/sql.py` | Text-to-SQL(扩展部署) |
| `client.watchers` | `resources/watchers.py` | 文件监听 |
| `client.sync` | `resources/sync.py` | 批量同步(扩展部署) |
| `client.auth` | `resources/auth.py` | 注册 / 登录 / 刷新 |
| `client.system` | `resources/system.py` | 健康检查 / 版本 |
| `client.tenants` | `resources/tenants.py` | 多租户管理 |
| `client.ops.gc` | `resources/ops/gc.py` | GC + 维护 |
| `client.import_database(...)` | `resources/imports.py` | 手动 DB 导入(F16a) |

---

## 7. 状态标签(本手册核心约定)

来自 `README.md:55-61`:

| 标签 | 英文 | 含义 | 手册中的承诺 |
|---|---|---|---|
| ✅ 已验证 | `Verified` | 当前代码 + spec + 测试均支撑 | 可以放心用,手册描述了完整用法 |
| �️ 需复核 | `Verification required` | 代码存在,但 public-readiness 仍需 e2e 验证 | 描述存在性与接口,**不保证生产可用** |
| 🚫 阻塞中 | `Blocked` | 当前运行时不工作或与文档不一致 | 只描述"计划 / 路线",不描述"怎么用" |
| 🗺️ 路线图 | `Roadmap` | 未来版本 | 只描述设计意图 |

> 状态细节见 **[01-status-matrix.md](01-status-matrix.md)**。

---

## 8. 配置文件 / 部署关键文件

| 文件 | 用途 |
|---|---|
| `config.yaml.example` | 服务端配置模板(15KB,涵盖 server/auth/log/namespace/embedding/reranker/llm 5 角色) |
| `VERSION` | SemVer(当前 `1.0.0-rc.1`) |
| `deploy/docker-compose.yml` | CPU 默认部署 |
| `deploy/docker-compose.cuda.yml` | CUDA 部署 |
| `deploy/Dockerfile` / `Dockerfile.cuda` | 镜像构建 |
| `deploy/model-manifest.tsv` | 模型清单(SHA-256 锁定) |
| `deploy/caddy/Caddyfile` | 反向代理 |
| `deploy/supervisord.conf` | 进程监管 |
| `db/migrations/*.sql` | 数据库 schema 迁移 |
| `api/openapi.yaml` | OpenAPI 契约 |
| `redocly.yaml` / `swagger_ui.config.yaml` | OpenAPI 校验 |

---

## 下一步

👉 **[01-status-matrix.md](01-status-matrix.md)** — 把"现在能用什么"一次理清
