# §25 MCP Server 与 SKILL 契约

> 🧑‍💻 开发者
>
> **一句话定位**:`SKILL.md` 是 Agent 操作手册,`mcp_server.py` 是外部 Agent 与平台交互的标准协议层;两者共同构成"Skill-first / 框架中立"的接入边界。

---

## 1. Skill-first 集成模型

来源:[`SKILL.md:16-22`](../SKILL.md)、[`README.md:24-29`](../README.md)

```mermaid
flowchart LR
    A["任何 Agent 运行时<br/>OpenClaw/Hermes/自研"] -->|读取| B["SKILL.md<br/>(操作手册)"]
    A -->|调用| C["HTTP / MCP"]
    C --> D["web_app.py<br/>(或 mcp_server.py)"]
    D --> E["lib/*.py 业务"]
    E --> F[("PostgreSQL")]
    B -->|凭据| A
    A -->|首次注册| G["agent_registration"]
    G --> H["cx_enrollment_grants"]
    style A fill:#ffd
    style D fill:#9f9
```

> 📌 **任何能读 SKILL.md 并执行 HTTP/MCP/CLI 的 Agent 都可以接入**,**不需要**是平台创建的。

---

## 2. SKILL.md 是什么

来源:[`SKILL.md`](../SKILL.md)

`SKILL.md` 不是普通 README,而是给 **AI Agent 用的操作手册**。它包含:

| 节 | 内容 |
|---|---|
| §1 Overview | 产品定位 + 边界契约 |
| §2 Package Contents | 文件清单 |
| §3 Prerequisites | PostgreSQL 18.3+, Python 3.14+, 扩展 |
| §4 Installation | `install_offline.sh` + `verify_deps.py` |
| §5 Configuration | `config_wizard.sh` + 自动加密 |
| §6 Schema Deployment | `psql -f` 顺序 |
| §7 Start Server | `start_web_server.sh` |
| §8 Business Agent Registration | `agent_bootstrap.py` |
| §9 API Reference | 完整 HTTP 路由表 |
| §10 Security Model | RLS / pgcrypto / LDAP |
| §11 Testing | pytest |
| §12 Troubleshooting | 9 类症状 |
| §13-14 | Offline deployment + Graph Engineering |

---

## 3. MCP Server

来源:[`lib/mcp_server.py`](../../scripts/lib/mcp_server.py)

### 3.1 启动方式

```bash
# stdio 模式(本地 CLI)
python -m lib.mcp_server

# SSE 模式(远程)
python -m lib.mcp_server --transport sse --port 18081
```

### 3.2 协议层

```mermaid
sequenceDiagram
    participant EA as 外部 Agent
    participant MC as MCP Server
    participant Auth as auth 校验
    participant Tool as 工具函数
    participant DB as PostgreSQL

    EA->>MC: initialize {protocolVersion, capabilities}
    MC-->>EA: {serverInfo, capabilities}
    EA->>MC: tools/list
    MC-->>EA: [tool1, tool2, ...]
    EA->>MC: tools/call {name, arguments}
    MC->>Auth: 验证 Bearer Token
    Auth->>DB: 查 cx_agent_credentials
    DB-->>Auth: hash 匹配
    Auth-->>MC: OK + Agent info
    MC->>Tool: tool_function(**arguments)
    Tool->>DB: 业务 SQL
    DB-->>Tool: 数据
    Tool-->>MC: result
    MC-->>EA: {content, isError}
```

### 3.3 暴露的工具

| 工具 | 输入 | 输出 | 关键约束 |
|---|---|---|---|
| `memory_lifecycle_create` | `{type, scope, content}` | `{family_id}` | 调用者 Principal 必须是 owner |
| `memory_lifecycle_chain` | `{family_id, max_depth}` | `{chain: [...]}` | 受 Principal 授权 |
| `memory_lifecycle_feedback` | `{family_id, score, comment}` | `{event_id}` | 反馈是 **untrusted data**,不作为授权 |
| `memory_lifecycle_candidate` | `{family_id, proposed_content}` | `{candidate_id}` | 候选需 review 后才能 activate |
| `graph_create_run` | `{definition_id, inputs}` | `{run_id, lease_token}` | 需 Principal 拥有 graph.manage |
| `graph_claim` | `{run_id, lease_token}` | `{node_payload, fencing_token}` | lease 必须有效 |
| `graph_complete` | `{run_id, lease_token, fencing_token, result}` | `{transition_id}` | fencing 必须 ≥ 当前 |
| `skill_discover` | `{query, category}` | `[skill_meta]` | 公开 Skill 元数据 |
| `skill_acquire` | `{skill_id, version}` | `{skill_text, resources[]}` | 需要 acquire token |
| `agent_heartbeat` | `{instance_id}` | `{next_heartbeat_in}` | 需注册过 |

> 💡 完整列表见 [`lib/mcp_server.py:_get_exposed_tools`](../../scripts/lib/mcp_server.py)。

---

## 4. SKILL.md 与 MCP 的关系

```mermaid
flowchart LR
    A["SKILL.md<br/>(文档)"] -->|告诉 Agent| B["MCP Server URL"]
    A -->|告诉 Agent| C["工具清单"]
    A -->|告诉 Agent| D["认证流程"]
    A -->|告诉 Agent| E["故障排查"]
    B --> F["mcp_server.py"]
    C --> F
    D --> F
    E --> F
    style A fill:#ffd
```

> SKILL.md 是 **文档契约**,MCP Server 是 **协议实现**。

---

## 5. 凭据与认证

来源:[`SKILL.md:93-103`](../SKILL.md)、[`docs/architecture.md:91-103`](architecture.md)

### 5.1 首次注册

```mermaid
sequenceDiagram
    participant User
    participant Admin
    participant API
    participant EA as 外部 Agent
    participant DB

    User->>Admin: 申请注册外部 Agent
    Admin->>API: POST /api/admin/agent/register
    API->>DB: INSERT cx_registration_requests + cx_enrollment_grants
    DB-->>API: token (one-time)
    API-->>Admin: enrollment_token
    Admin->>EA: 配置 token + 启动 Agent
    EA->>API: POST /api/enrollment/redeem {token, agent_id, public_key}
    API->>DB: 验证 token 一次性 + 哈希公钥
    DB-->>API: ok
    API-->>EA: {access_token, refresh_token}
    EA->>API: Authorization: Bearer {access_token}
```

### 5.2 后续请求

```text
GET /api/mcp HTTP/1.1
Host: chuanxu.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
X-Agent-Id: agent_001
X-Agent-Instance: instance_abc
```

> 🔐 服务端校验:`Bearer Token + X-Agent-Id` 必须匹配数据库 `cx_agent_credentials`。

---

## 6. 工具调用示例

### 6.1 创建 Memory

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "memory_lifecycle_create",
    "arguments": {
      "memory_type": "FACT",
      "scope": "AGENT_MEMORY",
      "content": "巴黎是法国首都"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{"type": "text", "text": "{\"family_id\": \"MEM_a1b2...\"}"}]
  }
}
```

### 6.2 提交 Graph Run

```json
// Request
{
  "method": "tools/call",
  "params": {
    "name": "graph_create_run",
    "arguments": {
      "definition_id": "graph_xyz",
      "inputs": {"query": "分析销售数据"}
    }
  }
}
```

---

## 7. 错误码

| 错误码 | 含义 | 处理 |
|---|---|---|
| `UNAUTHENTICATED` | 401,无凭据 | 重新注册 |
| `FORBIDDEN` | 403,权限不足 | 联系 Admin |
| `CAPABILITY_DISABLED` | 409,能力被禁用 | 联系 Admin 启用 |
| `STALE_LEASE` | 409,Lease 过期 | 重新 claim |
| `INVALID_INPUT` | 400,参数错误 | 检查 schema |
| `RATE_LIMITED` | 429 | 退避 |

---

## 8. 自定义 MCP 工具

来源:[`lib/mcp_server.py:_load_dynamic_tools`](../../scripts/lib/mcp_server.py)

```python
# 注册新工具
@register_tool(
    name="my_tool",
    description="工具描述",
    input_schema={
        "type": "object",
        "properties": {"arg1": {"type": "string"}},
        "required": ["arg1"]
    }
)
def my_tool(arg1: str, principal_id: str) -> dict:
    # principal_id 由 MCP Server 注入(来自认证)
    result = your_business_logic(arg1, principal_id=principal_id)
    return {"content": [{"type": "text", "text": json.dumps(result)}]}
```

> ⚠️ **永远不要在工具函数中接受来自客户端的 `agent_id` 或 `principal_id`** — 必须用 `principal_id` 参数(由服务端注入)。

---

## 9. 故障排查(MCP 视角)

| 症状 | 排查 |
|---|---|
| `UNAUTHENTICATED` | 检查 Bearer Token 是否过期 |
| `CAPABILITY_DISABLED` | Admin → 功能配置页启用 |
| `INVALID_INPUT` | 检查 input_schema |
| 工具未列出 | 检查 `_get_exposed_tools()` 返回值 |
| 工具调用超时 | 检查 `app.current_agent_id` GUC 是否设置 |

---

## 10. 交叉引用

- 注册 Agent:[§32 Agent 注册与管理](32-Agent注册与管理.md)
- 外部框架:[§48 外部框架 Gateway 接入](48-外部框架Gateway接入.md)
- 现有文档:[`SKILL.md`](../SKILL.md) 全文

> 📌 **下一章**:[§26 Web 前端架构](26-Web前端架构.md) — React 19 + TypeScript SPA 的结构与 20 个 nav 页面。