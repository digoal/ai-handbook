# 39 · 端到端追踪 — 一段 prompt 跨 6 组件

> **目标读者**:开发者、SRE、想看完整 trace 的人。
> **阅读时间**:10 分钟。
> **关键事实**:把"上季度的退款政策是怎么说的?"作为示例,追踪它如何穿过 **Web UI → Agent → SDK → Server → ONNX → 回传 → 落 Memory** 的完整链路,看到每一步的字段传播与失败兜底。

---

## 1. 完整时序

```mermaid
sequenceDiagram
    autonumber
    participant U as 用户
    participant W as Web UI
    participant AG as cortrix-agent :8001
    participant SDK as AsyncCortrix
    participant SRV as cortrix-server :8420
    participant E as F04 Pipeline<br/>(embed / BM25 / rerank / CRAG)
    participant LLM as LLM provider<br/>(agent_llm)
    participant MEM as Memory store

    U->>W: 输入:"上季度的退款政策是怎么说的?"
    W->>W: span = tracer.start_span("ui.chat")
    Note over W: @opentelemetry/api<br/>trace_id=t1, span_id=s1
    W->>AG: POST /chat?explain=true<br/>Headers: X-Cortrix-Namespace=default,<br/>traceparent=00-t1-s1-01
    Note over AG: routes/chat.py:85 接 SSE
    AG->>SDK: await client.search("default", "退款政策", top_k=10, rerank=True)
    Note over SDK: AsyncBaseClient._request<br/>X-Request-ID=u2(uuid4)<br/>traceparent 继承(t1, 新 s2)
    SDK->>SRV: POST /api/v1/query<br/>httpx + headers
    SRV->>SRV: 读 NS 元数据 + 鉴权
    SRV->>E: query_pipeline.run({query, ns, top_k, rerank})
    E->>E: embed(query) [BGE-M3 ONNX]
    E->>E: P-HNSW top-N=200 + BM25 top-N=200
    E->>E: RRF 融合 → top-M=50
    E->>E: bge-reranker-v2-m3 重排 → top-K=10
    E->>E: CRAG(F37)评估:keep / drop
    E-->>SRV: QueryResult(results=[10 items], meta)
    SRV-->>SDK: 200 + JSON<br/>X-Request-ID=u2 回传
    SDK-->>AG: dataclass QueryResult
    AG->>AG: prompt.build(injection-hardened + 8 hex suffix)<br/>chunks 带 source_path 前缀
    AG->>LLM: stream_chat(system, user)
    loop 每个 delta
        LLM-->>AG: delta token
        AG-->>W: data: {"chunk": "..."}
    end
    LLM-->>AG: done
    AG-->>W: data: {"meta": {session_id, chunk_ids, rag_status, ...}}
    AG-->>W: data: [DONE]
    AG->>W: span.end()
    AG-->>U: 流式显示完毕
    par 异步(fire-and-forget)
        AG->>SDK: client.memory.log(session_id, query, response, user_id)
        SDK->>SRV: POST /memory/sessions/{id}/interactions
        SRV->>MEM: 写交互日志(SQLite)
    end
    par 异步(MEM02 触发, 当前 🚫)
        AG->>SDK: client.memory.extract(...)
        SDK->>SRV: POST /memory/extract
        SRV-->>SDK: CX_ERR_MEM02_EXTRACTION_FAILED<br/>(500, fallback)
    end
```

---

## 2. 字段在链路中的传播

| 字段 | 起点 | 中间 | 终点 |
|---|---|---|---|
| **trace_id** | Web UI span | traceparent → SDK → SRV 日志 | AG meta.frame |
| **X-Request-ID** | SDK `uuid4()` | SRV 日志 / 错误回带 | AG logs / UI |
| **session_id** | request body | AG SessionStore(N=10) | meta.frame |
| **chunk_ids** | F04 pipeline | SDK dataclass → AG prompt | AG meta.frame |
| **rag_status** | ChatExecutor(`success` / `degraded`) | prompt + meta | AG meta.frame |
| **explain tier** | `?explain=true` | `explain.py` A/B/C | meta.frame |
| **user_id** | MEM05(必填) | memory.log | Memory store |
| **request_id** | SDK 错误回带(`X-Request-ID`/`x-cortrix-trace-id`/body) | error.frame | UI 错误展示 |

---

## 3. 失败路径示例(LLM 调用失败 + RAG 成功)

```mermaid
sequenceDiagram
    participant U
    participant AG
    participant SDK
    participant SRV
    participant LLM

    U->>AG: POST /chat
    AG->>SDK: client.search (成功,200)
    SDK-->>AG: QueryResult(10 chunks)
    AG->>LLM: stream_chat
    LLM-->>AG: raise timeout
    Note over AG: LLM 失败,RAG 成功<br/>→ L2 fallback:返回 raw chunks<br/>rag_status='degraded'
    AG-->>U: data: {chunk: "[1] (path): ..."}
    AG-->>U: data: {meta: {rag_status: "degraded"}}
    AG-->>U: data: [DONE]
```

> 用户能看到原始引用片段,但**不会**有 LLM 总结的"上季度的退款政策是 XX"。

---

## 4. 失败路径示例(RAG 三次失败 + LLM 失败)

```mermaid
sequenceDiagram
    participant U
    participant AG
    participant SDK
    participant SRV
    participant LLM

    U->>AG: POST /chat
    loop L1 重试 N=3(500ms / 1000ms backoff)
        AG->>SDK: client.search
        SDK->>SRV: POST /query
        SRV-->>SDK: 503 transient
        SDK-->>AG: ServiceUnavailableError
    end
    Note over AG: L2 fallback:LLM-only<br/>chunks=[], rag_status='degraded'
    AG->>LLM: stream_chat
    LLM-->>AG: raise timeout
    Note over AG: L3:AgentError(CX_ERR_F48_RAG_FAILED)<br/>structured_data:<br/>{cortrix_server_error, fallback_attempted:true, llm_error}
    AG-->>U: data: {error: {code, category, retryable, structured_data, request_id}}
```

---

## 5. 端到端追踪的串联手段

### 5.1 三类 ID

| ID 类型 | 作用 | 传播路径 |
|---|---|---|
| `trace_id`(W3C) | 跨进程 / 跨服务的端到端追踪 | Web UI → traceparent → AG → SDK → SRV → 日志 |
| `X-Request-ID`(UUIDv4) | 单次 HTTP 调用的关联键 | SDK 生成 → SRV 日志 → 错误回带 → AG logs |
| `session_id`(业务) | 一次 chat turn 的语义 ID | body → AG SessionStore → meta.frame |

### 5.2 反代层关联

`deploy/caddy/Caddyfile:69-75` 写 access log(JSON 格式),含 `request_id`、`latency`、`status`。把 access log 与 SRV 日志按 `X-Request-ID` join,可还原单次请求的完整链路。

### 5.3 错误信封的回带

```python
# SDK 错误
e = client.search("ns", "query")  # raises
# e.request_id 是 SRV 回传的 X-Request-ID(也可能是 x-cortrix-trace-id 或 body.request_id)

# Agent error
agent_error = AgentError("CX_ERR_F48_RAG_FAILED", ...)
# agent_error.request_id 来自上游 SDK 的 e.request_id(若可用)
```

---

## 6. 实战:从 UI 报错到后端定位

```text
[UI] 用户看到:"对话失败,请重试"
       ↓ 点击"查看详情"
[UI] 显示 code=CX_ERR_F48_RAG_FAILED, request_id=u2-...
       ↓ 复制 request_id
[Ops] 查 Caddy access log:grep "u2-..." /var/log/caddy/cortrix-access.log
       ↓ 找到 SRV 这条请求的 status / latency
[SRE] 查 SRV 日志:grep "X-Request-ID=u2-..." cortrix.log
       ↓ 看是 F04 哪个阶段失败(CPU/embedding/rerank/CRAG)
[SRE] 查 OTel trace:在 UI 上搜 trace_id=t1
       ↓ 看完整 span tree(ui → agent → sdk → server → embedding → ANN → ...)
```

---

## 7. 一图看所有不变量

```mermaid
graph LR
    T["traceparent<br/>(W3C, 跨进程)"]
    R["X-Request-ID<br/>(SDK uuid4, 单请求)"]
    S["session_id<br/>(业务, 单 turn)"]
    U["user_id<br/>(MEM05, 跨会话)"]
    C["chunk_ids<br/>(引用, 审计)"]

    T -->|贯穿| W["Web UI"]
    T -->|贯穿| AG["Agent"]
    T -->|贯穿| SDK["SDK"]
    T -->|贯穿| SRV["Server"]

    R -->|贯穿| SDK
    R -->|贯穿| SRV

    S -->|贯穿| AG
    U -->|贯穿| MEM["Memory"]
    C -->|贯穿| E["F04 → Agent → UI"]
```

---

## 下一步

👉 **[第四篇 · 40 · 部署](part-4-operator/40-deploy.md)** — 运维视角,部署资产详解。
