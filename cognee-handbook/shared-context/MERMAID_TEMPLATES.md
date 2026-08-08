# mermaid 模板与规范

## 配色

```css
/* 节点类型 */
fill_concept: #3B82F6    /* 概念 */
fill_data: #10B981       /* 数据 */
fill_api: #F59E0B        /* API */
fill_external: #A855F7   /* 外部系统 */
fill_error: #EF4444      /* 错误 */

/* 字体与背景 */
font_family: "PingFang SC", "Microsoft YaHei", system-ui
background: #FAFAFA
text_color: #1F2937
```

## 模板 1:流程图(flowchart)

```mermaid
%% title: Ch01 — add → cognify → search 流程
graph LR
    A([用户输入]) --> B["cognee.add"]
    B --> C["resolve_data_directories"]
    C --> D["ingest_data"]
    D --> E["cognee.cognify"]
    E --> F["classify_documents"]
    F --> G["extract_chunks"]
    G --> H["extract_graph"]
    H --> I["summarize"]
    I --> J["add_data_points"]
    J --> K[(SQLite + LanceDB + Ladybug)]
    K --> L["cognee.search"]
    L --> M([LLM 回答])

    classDef concept fill:#3B82F6,color:#fff,stroke:#1E40AF
    classDef data fill:#10B981,color:#fff,stroke:#065F46
    classDef api fill:#F59E0B,color:#fff,stroke:#92400E
    classDef external fill:#A855F7,color:#fff,stroke:#6B21A8

    class A,M concept
    class K data
    class B,E,L api
```

## 模板 2:时序图(sequence)

```mermaid
%% title: Ch20 — Claude Code ↔ cognee-mcp 时序
sequenceDiagram
    actor User as 用户
    participant CC as Claude Code
    participant MCP as cognee-mcp
    participant Cog as cognee server
    participant DB as 存储后端

    User->>CC: 输入问题
    CC->>MCP: mcp__cognee__recall(query)
    MCP->>Cog: POST /v1/recall
    Cog->>DB: 向量 + 图检索
    DB-->>Cog: 检索结果
    Cog-->>MCP: MemoryEntry[]
    MCP-->>CC: RecallResponse
    CC-->>User: 注入上下文 + 生成回答
```

## 模板 3:ER 图

```mermaid
%% title: Ch07 — DataPoint 与子类 ER
erDiagram
    DataPoint ||--o{ Entity : "is_a"
    DataPoint ||--o{ Chunk : "is_a"
    DataPoint ||--o{ Skill : "is_a"
    Entity ||--|| EntityType : "分类"
    Entity ||--o{ Edge : "源/目标"
    DataPoint ||--o{ DataPoint : "metadata.identity_fields"

    DataPoint {
        string id PK
        string type
        datetime created_at
        json metadata
        float feedback_weight
        float importance_weight
    }

    Entity {
        string name
        string description
    }

    Edge {
        string source_node_id FK
        string target_node_id FK
        string relationship_type
        float weight
    }
```

## 模板 4:DAG(pipeline)

```mermaid
%% title: Ch08 — cognify 默认 pipeline DAG
graph TD
    Start([start]) --> A[classify_documents]
    A --> B[extract_chunks_from_documents]
    B --> C[extract_graph_and_summarize]
    C --> D[add_data_points]
    D --> E[extract_dlt_fk_edges]
    E --> End([done])

    classDef task fill:#F59E0B,color:#fff,stroke:#92400E
    class A,B,C,D,E task
```

## 模板 5:决策树

```mermaid
%% title: Ch15 — SearchType 选型决策树
graph TD
    Start{问题类型?}
    Start -->|代码相关| Code{具体?}
    Start -->|时序相关| T[TEMPORAL]
    Start -->|图谱探索| Graph{深度?}
    Start -->|纯文本检索| RAG[RAG_COMPLETION]
    Start -->|不知道| FL[FEELING_LUCKY]

    Code -->|规则| CR[CODING_RULES]
    Code -->|上下文| C[CODE]

    Graph -->|一跳| GC[GRAPH_COMPLETION]
    Graph -->|思维链| COT[GRAPH_COMPLETION_COT]
    Graph -->|子查询分解| DEC[GRAPH_COMPLETION_DECOMPOSITION]
    Graph -->|上下文扩展| EXT[GRAPH_COMPLETION_CONTEXT_EXTENSION]

    classDef opt fill:#3B82F6,color:#fff,stroke:#1E40AF
    classDef leaf fill:#10B981,color:#fff,stroke:#065F46
    class Start,Code,Graph opt
    class T,RAG,FL,CR,C,GC,COT,DEC,EXT leaf
```

## 模板 6:状态机

```mermaid
%% title: Ch14 — v2 内存 API 状态机
stateDiagram-v2
    [*] --> Remembered
    Remembered --> Recalled : recall()
    Recalled --> Improved : improve(feedback)
    Improved --> Recalled : 再次 recall
    Remembered --> Forgotten : forget()
    Recalled --> Forgotten : forget()
    Improved --> Forgotten : forget()
    Forgotten --> [*]
```

## 模板 7:部署拓扑

```mermaid
%% title: Ch28 — 生产部署拓扑
graph TB
    subgraph K8s["Kubernetes Cluster"]
        subgraph App["应用 Pod"]
            API1[cognee API 1]
            API2[cognee API 2]
            API3[cognee API 3]
        end
        subgraph Worker["Worker Pod"]
            W1[cognify worker 1]
            W2[cognify worker 2]
        end
    end

    subgraph Storage["存储集群"]
        PG[(Postgres)]
        VDB[(LanceDB / PGVector)]
        GDB[(Neo4j / Ladybug)]
    end

    subgraph External["外部"]
        OAI[OpenAI / Anthropic]
        User[终端用户]
    end

    User --> API1
    User --> API2
    User --> API3
    API1 --> PG
    API2 --> PG
    API3 --> PG
    API1 --> VDB
    API1 --> GDB
    API1 --> OAI
    W1 --> PG
    W1 --> VDB
    W1 --> GDB
    W1 --> OAI

    classDef pod fill:#3B82F6,color:#fff
    classDef store fill:#10B981,color:#fff
    classDef ext fill:#A855F7,color:#fff
    class API1,API2,API3,W1,W2 pod
    class PG,VDB,GDB store
    class OAI,User ext
```

## 模板 8:四步生命周期

```mermaid
%% title: Ch14 — remember/recall/improve/forget 生命周期
graph LR
    A([remember]) --> B[(Memory)]
    B --> C([recall])
    C --> D{反馈?}
    D -->|有| E([improve])
    E --> B
    D -->|无| F([forget?])
    F -->|是| G([forget])
    G --> H[(Memory 删除)]

    classDef step fill:#F59E0B,color:#fff
    class A,C,E,G step
```

## 模板 9:迁移管道

```mermaid
%% title: Ch25 — Mem0/Zep 迁移到 Cognee
graph LR
    A[Mem0 / Zep<br/>原始数据] --> B[Mem0Source<br/>ZepSource]
    B --> C[Transform]
    C --> D[add]
    D --> E[cognify]
    E --> F[(Cognee 图谱)]

    subgraph Reverse["反向导出"]
        F --> G[export]
        G --> H[Mem0 JSON /<br/>COGXArchive]
    end

    classDef src fill:#A855F7,color:#fff
    classDef step fill:#F59E0B,color:#fff
    classDef store fill:#10B981,color:#fff
    class A,H src
    class B,C,D,E,G step
    class F store
```

## 模板 10:对比图

```mermaid
%% title: Ch01 — 传统 RAG vs Cognee ECL
graph TB
    subgraph RAG["传统 RAG"]
        R1[文档] --> R2[切片]
        R2 --> R3[向量化]
        R3 --> R4[(向量库)]
        R4 --> R5[相似度检索]
        R5 --> R6[Top-K 段落]
        R6 --> R7[LLM]
    end

    subgraph Cog["Cognee ECL"]
        C1[原始数据] --> C2[add]
        C2 --> C3[classify]
        C3 --> C4[chunk]
        C4 --> C5[extract graph]
        C5 --> C6[summarize]
        C6 --> C7[(图 + 向量 + 关系)]
        C7 --> C8[structured retrieval]
        C8 --> C9[多路重排]
        C9 --> C10[LLM]
    end

    classDef rag fill:#EF4444,color:#fff
    classDef cog fill:#10B981,color:#fff
    class R1,R2,R3,R4,R5,R6,R7 rag
    class C1,C2,C3,C4,C5,C6,C7,C8,C9,C10 cog
```

## 渲染规范

```bash
# 使用 mmdc 渲染(需要先安装)
mmdc -i chapter-XX-diagram.mmd -o assets/diagrams/chXX-name.svg \
     -b transparent \
     -t neutral \
     --configFile templates/mermaid-config.json

# 颜色通过 templates/mermaid-config.json 配置:
# {
#   "theme": "neutral",
#   "themeVariables": {
#     "background": "#FAFAFA",
#     "primaryColor": "#3B82F6",
#     "primaryTextColor": "#fff",
#     "primaryBorderColor": "#1E40AF",
#     "lineColor": "#6B7280",
#     "fontFamily": "PingFang SC, Microsoft YaHei, system-ui"
#   }
# }
```

## 限制

- 节点最大宽度 220px,超出文字必须分行(`<br/>`)
- 不使用 emoji,使用 `[A]` `[B]` 等 letter group
- 必须有标题 `%% title: <章节名> — <图名>`
- 箭头方向明确:`graph LR` / `graph TD` / `graph BT` / `graph RL`
- 子图用 `subgraph Name["显示名"] ... end` 包裹
- 节点标签中的特殊字符必须用双引号 `["含 (括号) 的文本"]`