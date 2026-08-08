# 23 · 业务场景 — 6 个端到端用例

> **目标读者**:用户、想 demo 的开发者。
> **阅读时间**:25 分钟。
> **关键事实**:每个用例都基于 `api/examples/` 中真实存在的样例;**唯一手精可运行的 Python 示例是 `api/examples/query/success/python.py`**,其他用例以 curl / SDK 调用示意为主。

---

## 用例地图

| # | 场景 | 关键端点 | 状态 |
|---|---|---|---|
| 1 | 合同检索(跨 NS) | `POST /query` | 🟡 |
| 2 | 文档异步上传 + 进度 | `POST /documents` + `GET /documents/tasks/{id}/progress` | 🟡 |
| 3 | Memory 个性化召回 | `POST /memory/search` | 🟡(MEM02 🚫) |
| 4 | Agent 对话(SSE) | `POST /api/v1/agent/chat` | 🟡 |
| 5 | 跨 Namespace ACL | `POST /namespaces/{ns}/acl` | 🚫 Blocked |
| 6 | GDPR 导出 / 删除 | `POST /gdpr/export` / `POST /gdpr/delete` | 🟡 |

---

## 1. 合同检索(跨 NS)

> 状态:🟡 Verification required。**唯一手精可运行示例**(`api/examples/query/success/python.py`)。

```python
"""POST /api/v1/query — success (Python SDK, cross-NS semantic query)."""
from cortrix import Client

client = Client(api_key="cx_live_xxx")

result = client.query.run(
    query="Party A breach-of-contract clause",
    namespaces=["contracts", "support_docs"],
    top_k=10,
    rerank=True,
)

# Class-A meta: returns results + coverage even if some NS fail (degradation path)
for item in result.results:
    print(item.score, item.namespace, item.content[:50])
print("coverage:", result.meta.coverage_ratio, "failed:", result.meta.namespaces_failed)
```

**步骤**:

1. 创建两个 NS:`contracts`、`support_docs`。
2. 上传合同 PDF 到 `contracts`(见 §2)。
3. 上传工单 / 知识库文档到 `support_docs`。
4. 调用上面这段代码,跨 NS 检索"Party A 违约条款"。
5. 即使其中一个 NS 临时不可用,返回仍含 `coverage_ratio` 与 `namespaces_failed`(Class-A 元数据)。

> 注:`api/examples/query/success/python.py` 是手精的(`api/examples/README.md:40-42`),其他用例以示意为主。

---

## 2. 文档异步上传 + 进度

来自 `api/examples/documents/upload_success/python.py`、`F42 tasks`。

```python
# 上传并轮询
task = client.documents.upload(
    "contracts",                              # namespace
    "/path/to/contract_001.pdf",              # file path
    filename="contract_001.pdf",              # 可选
    metadata={"party": "A", "year": 2026},    # 可选,JSON
)

# 同步:task.document_id 即可;异步:轮询 task_id
while True:
    progress = client.documents.task_status(task.task_id)
    if progress.status in {"completed", "failed"}:
        break
    time.sleep(2)

# 或一键等待
client.documents.upload_and_wait(
    "contracts",
    "/path/to/contract_002.pdf",
    poll_interval=2.0,
    timeout=300.0,
)
```

**批量上传(F42 bulk)**:

```python
result = client.documents.batch_submit(
    "contracts",
    docs=[
        {"filename": "c1.pdf", "content": open("c1.pdf","rb").read(), "metadata": {...}},
        {"filename": "c2.pdf", "content": open("c2.pdf","rb").read()},
    ],
    async_=True,                 # 默认 True
    on_duplicate="skip",         # skip | replace | error
)
# 返回部分成功信封:{"accepted": [...], "skipped": [...], "errors": [...]}
```

**错误信封样例**(`api/examples/documents/upload_error_category_auth/curl.sh`、`upload_error_category_quota_429_rate_limit/curl.sh`):

- auth 错:`401` + `category=auth` + `CX_ERR_AUTH_*`
- quota 错:`429` + `category=quota` + `retry_after_ms`

---

## 3. Memory 个性化召回(MEM05)

> 状态:MEM01 / MEM03 / MEM04 / MEM05 是 🟡 Verification required;**MEM02 自动抽取是 🚫 Blocked**。

```python
"""POST /api/v1/memory/search — success (Python SDK, user_id isolation required)."""
from cortrix import Client

client = Client(api_key="cx_live_xxx")

result = client.memory.search(
    query="the project progress the user mentioned last time",
    namespace="user_memory",
    user_id="user_001",    # MEM05:必填,user 隔离
    top_k=5,
)
for m in result.memories:
    print(m.memory_type, m.status, m.content)
```

**Memory CRUD(MEM03)**:

```python
# 显式写一条记忆(不依赖 LLM 抽取)
client.memory.create(
    namespace="user_memory",
    user_id="user_001",
    content="用户偏好 markdown 格式",
    memory_type="preference",
)

# 列表 / 编辑 / 撤销
items = client.memory.list(namespace="user_memory", user_id="user_001")
client.memory.edit(memory_id=items[0].id, content="...")
client.memory.invalidate(memory_id=items[0].id)
```

**错误信封样例**(`api/examples/memory/search_error_category_auth/`、`search_error_category_transient/`):

- auth 错:`401` + `category=auth`
- transient 错:`503` + `category=transient` + `retry_after_ms`

---

## 4. Agent 对话(SSE)

来自 `cortrix-agent/README.md:62-94`、`api/examples/agent/agentChat/success/curl.sh`。

```bash
curl -N -X POST 'http://localhost:8001/chat?explain=true' \
  -H 'Content-Type: application/json' \
  -H 'X-Cortrix-Namespace: default' \
  -d '{"message": "find privacy documents", "session_id": "s-001"}'
```

**SSE 帧样例**(来自 README):

```text
data: {"chunk": "Based on"}
data: {"chunk": " the retrieved documents..."}
data: {"meta": {"session_id": "s-001", "chunk_ids": [], "rag_status": "success"}}
data: [DONE]
```

**Query 参数**:

| 参数 | 用途 |
|---|---|
| `explain=true` | 在 meta 中返回 explain 元数据 |
| `debug=true` | 返回详细失败信息 |

**Headers**:

| Header | 用途 |
|---|---|
| `Authorization: Bearer <key>` | 当 server 启用 auth |
| `X-Cortrix-Tenant-Id` | 多租户 |
| `X-Cortrix-Namespace` | 覆盖默认 NS |

**错误**:`data: {"error": {"code": "...", "category": "...", ...}}`(SSE error event)。

详细见 [25-agent-chat.md](25-agent-chat.md)。

---

## 5. 跨 Namespace ACL

> 状态:🚫 **Blocked**(`README.md:72`)。spec 已定义,运行时与文档待对齐。
>
> 本节只展示**接口形状**,不承诺当前能用。

```bash
# Grant
curl -X POST "https://api.cortrix.io/api/v1/namespaces/{ns_id}/acl" \
  -H "X-API-Key: cx_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "grantee_tenant_id": "tenant_B",
    "permission": "read"   # read | write | admin
  }'

# List
curl -X GET "https://api.cortrix.io/api/v1/namespaces/{ns_id}/acl" \
  -H "X-API-Key: cx_live_xxx"

# Revoke
curl -X DELETE "https://api.cortrix.io/api/v1/namespaces/{ns_id}/acl/{grantee_tenant_id}" \
  -H "X-API-Key: cx_live_xxx"
```

**SDK 入口**:`client.namespaces.set_permission(name, grantee_tenant_id, *, permission)`。

> 决策:**生产跨租户授权不要走 ACL 路径**,等升 ✅。

---

## 6. GDPR 导出 / 删除

> 状态:🟡 Verification required。

```bash
# Export
curl -X POST "https://api.cortrix.io/api/v1/gdpr/export" \
  -H "X-API-Key: cx_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": "user_001",
    "include": ["memories", "documents", "blocks"]
  }'
# → 200 + JSON envelope with download URLs / manifest

# Delete
curl -X POST "https://api.cortrix.io/api/v1/gdpr/delete" \
  -H "X-API-Key: cx_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": "user_001",
    "scope": "all"
  }'
# → 200 + job_id;软删除,经 GC 阶段最终物理删除
```

**GDPR 三阶段 GC**(配合 §6):

| 阶段 | 时间窗 | 行为 |
|---|---|---|
| Stage 1 | 30 天(默认) | 软删除,可恢复 |
| Stage 2 | 30 → 90 天 | 硬删除 + ref_count fix-up(blob enqueued) |
| Stage 3 | 90 天 → 物理 unlink | blob 二次确认后才真删 |

GC 配置见 [21-config.md §2.13](21-config.md)。

---

## 7. 用例决策速查

| 你想做的事 | 用例 | 关键 SDK 入口 |
|---|---|---|
| 跨 NS 检索 / 合同 / 工单 | §1 | `client.query.run(namespaces=[...], query=..., top_k=..., rerank=True)` |
| 上传 PDF / DOCX / 图片 | §2 | `client.documents.upload` / `upload_and_wait` / `batch_submit` |
| 显式写记忆 / 按 user 召回 | §3 | `client.memory.create` / `client.memory.search(user_id=...)` |
| 跟 LLM 聊天(流式) | §4 | `curl /chat`(SSE) |
| 跨租户授权 | §5 | `client.namespaces.set_permission`(🚫 Blocked) |
| 数据主体导出 / 删除 | §6 | `POST /gdpr/export` / `POST /gdpr/delete` |

---

## 下一步

👉 **[24 · Web UI](24-web-ui.md)** — 浏览器里怎么用 Cortrix。
