# 第 13 章 `v1 API: add / cognify / search 详解`

> 本章目标:读完本章,你将能够
> - 根据业务场景精确控制 `cognee.add` 的数据类型、目标 dataset 与并发模型
> - 区分 `cognee.cognify` 的同步/异步模式、默认 pipeline 与 temporal pipeline
> - 熟练使用 `cognee.search` 的全部 27 个参数并按需组合
> - 理解 `cognee.update` / `cognee.delete` / `cognee.memify` / `cognee.prune` 的回滚语义
> - 掌握 `visualize_graph` 与 `start_visualization_server` 的图谱导出

## 前置知识
- 已读完 [[chapter-03-add-cognify-search|第 3 章 Hello World:`add` / `cognify` / `search` 三步走](../part-01-foundation/chapter-03-add-cognify-search.md)
- 已读完 [[chapter-04-core-concepts|第 4 章 核心概念速览:ECL、SearchType、Retriever 三段式]](../part-01-foundation/chapter-04-core-concepts.md)
- 需要的基础库:`cognee>=1.4.0`、`pydantic>=2.0`、`asyncio`
- 环境:Python 3.10–3.14,默认栈 SQLite + LanceDB + Ladybug

## 本章导览
- 13.1 `cognee.add` 全参数:数据集、增量、阻塞、数据类型、加载器与缓存
- 13.2 `cognee.cognify` 全参数:graph_model、chunk、temporal、dry_run
- 13.3 `cognee.search` 全参数:27 个参数全表 + SearchType 枚举一览
- 13.4 `cognee.update` 与 `cognee.delete`:回滚语义与迁移指南
- 13.5 `cognee.visualize_graph` 与 `start_visualization_server`
- 13.6 `cognee.memify` 与 `cognee.prune`:记忆化管道与系统剪枝
- 13.7 状态机:摄取/认知化/检索的交互状态
- 13.8 常见错误与边界

---

## 13.1 `cognee.add` 全参数

`cognee.add` 是 ECL(Extract → Cognify → Load)中的 **Extract** 入口,把"原料"装入 dataset;真正把原料变成图的是 `cognify`。定义见 `<COGNEE_REPO>/cognee/api/v1/add/add.py`,签名在第 25–49 行,默认参数收敛为一句话:**"用 `main_dataset`、20 条/批、增量模式、同步等待地把任意数据送进 pipeline"**。

### 13.1.1 完整参数表

| 参数 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `data` | `Union[BinaryIO, list[BinaryIO], str, list[str], DataItem, list[DataItem], Any]` | 必填 | 摄取的数据,支持 str、文件路径、`file://`、`s3://`、`BinaryIO`、`DataItem`、DLT Resource |
| `dataset_name` | `str` | `"main_dataset"` | 目标 dataset 名 |
| `user` | `User` | `None` | 用户上下文,None 时自动用 default user |
| `node_set` | `Optional[List[str]]` | `None` | 图节点分组标签,可用于后续按 node_name 过滤 |
| `vector_db_config` | `dict` | `None` | 自定义向量库配置 |
| `graph_db_config` | `dict` | `None` | 自定义图库配置 |
| `dataset_id` | `Optional[UUID]` | `None` | 用 UUID 替代 dataset_name 定位 dataset |
| `preferred_loaders` | `Optional[List[Union[str, dict]]]` | `None` | 强制指定某种文件类型的 loader,如 `["text", {"pdf": {"chunk_size": 800}}]` |
| `incremental_loading` | `bool` | `True` | 已存在的 document 是否只更新增量,避免全量重做 |
| `data_per_batch` | `Optional[int]` | `20` | 每批送入 pipeline 的数据条数 |
| `importance_weight` | `Optional[float]` | `0.5` | 该批数据的初始 importance_weight(0–1) |
| `run_in_background` | `bool` | `False` | 是否后台执行,True 时立刻返回不阻塞 |
| `llm_config` | `Optional[LLMConfig]` | `None` | 临时覆盖 LLM(用于分类/OCR 等需要 LLM 的 loader) |
| `embedding_config` | `Optional[EmbeddingConfig]` | `None` | 临时覆盖 embedding 模型 |
| `data_cache` | `bool` | `True` | 是否复用上一次 add 的原始文件缓存 |

### 13.1.2 数据类型识别规则

`add()` 内部通过 `resolve_dlt_sources` 与 `resolve_data_directories` 走"先识别再分发"的路径(`<COGNEE_REPO>/cognee/tasks/ingestion/resolve_dlt_sources.py`)。经验规则:

| 输入 | 路由 |
|---|---|
| `"LangChain 是..."` 这种**不以 `/` 或 `file://` 开头的 str** | 当作 raw text 直接写入 |
| `"/abs/path.pdf"`、`"file:///abs/x.pdf"` | 走本地文件 loader,按后缀选 loader |
| `"s3://bucket/key"` | 走 S3 loader |
| `open("x", "rb")` | BinaryIO,按文件名或 `name` 属性推断 loader |
| `"https://example.com"` | 走 Tavily(优先)或 BeautifulSoup |
| `dlt` resource / source | 先用 DLT 拉取,再喂给 ingestion pipeline |

### 13.1.3 完整示例:多源、增量、自定义权重

```python
import asyncio
import cognee

async def main():
    # 1) 摄取多源混合数据到自定义 dataset
    await cognee.add(
        data=[
            "项目背景:本系统用于分析 LLM Agent 记忆架构。",
            "<COGNEE_REPO>/README.md",          # 本地文件
            "s3://my-bucket/specs/v1.pdf",                  # S3
        ],
        dataset_name="agent_arch_research",
        importance_weight=0.8,
        preferred_loaders=["text", {"pdf": {"chunk_size": 800}}],
        data_per_batch=10,
    )

    # 2) 再摄一次,只更新增量(已有文件不会被重复处理)
    await cognee.add(
        data=["更新:新增两篇论文摘要..."],
        dataset_name="agent_arch_research",
        incremental_loading=True,
    )

asyncio.run(main())
```

### 13.1.4 阻塞 vs 后台

`run_in_background=False` 适合 Web API 等同步等待的场景;`True` 时通过 `get_pipeline_executor(run_in_background=True)` 切到后台 pipeline,会立刻返回 PipelineRunInfo(`<COGNEE_REPO>/cognee/modules/pipelines/layers/pipeline_execution_mode.py`)。后台模式还会先把流式输入 materialize 成内存 buffer,避免请求作用域结束后流被关闭(`<COGNEE_REPO>/cognee/tasks/ingestion/utils.py` 中的 `materialize_stream_for_background`)。

```python
import asyncio, cognee

async def main():
    info = await cognee.add(
        "fastapi 长文...",
        dataset_name="long_docs",
        run_in_background=True,
        data_per_batch=50,
    )
    print(f"pipeline_run_id={info.pipeline_run_id}")

asyncio.run(main())
```

> 关键实现见 `<COGNEE_REPO>/cognee/api/v1/add/add.py` 第 190–270 行。

---

## 13.2 `cognee.cognify` 全参数

`cognee.cognify` 是 **Cognify** 入口,把已 ingest 的原料跑完分类→切块→抽取图谱→summarize→写库。定义见 `<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py`,签名在第 43–62 行。

### 13.2.1 完整参数表

| 参数 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `datasets` | `Union[str, list[str], list[UUID]]` | `None` | 要处理的 dataset;None 表示处理当前用户所有 dataset |
| `user` | `User` | `None` | 用户上下文 |
| `graph_model` | `BaseModel` | `KnowledgeGraph` | LLM 抽取时使用的 Pydantic schema,决定节点/边结构 |
| `chunker` | `Callable` | `TextChunker` | 切块策略,可选 `LangchainChunker` |
| `chunk_size` | `int` | `None` | 单 chunk 最大 token 数,None 时按 LLM 上限自动计算 |
| `chunks_per_batch` | `int` | `None` | 单批送入 LLM 的 chunk 数,默认从 `cognify_config` 读,空则 100 |
| `config` | `Config` | `None` | 本体(ontology)配置,默认从环境变量/默认解析器生成 |
| `vector_db_config` | `dict` | `None` | 自定义向量库 |
| `graph_db_config` | `dict` | `None` | 自定义图库 |
| `run_in_background` | `bool` | `False` | 是否后台执行 |
| `incremental_loading` | `bool` | `True` | 增量模式,已抽取的 chunk 不重复抽取 |
| `custom_prompt` | `Optional[str]` | `None` | 自定义 LLM 抽取 prompt,覆盖默认 `EXTRACT_GRAPH_PROMPT` |
| `temporal_cognify` | `bool` | `False` | 切换到时序 pipeline(事件→时间戳→图谱) |
| `data_per_batch` | `int` | `20` | 持久化阶段每批写库大小 |
| `llm_config` | `Optional[LLMConfig]` | `None` | 临时覆盖 LLM |
| `embedding_config` | `Optional[EmbeddingConfig]` | `None` | 临时覆盖 embedding |
| `data_cache` | `bool` | `True` | 是否复用 add 阶段的文件缓存 |
| `dry_run` | `bool` | `False` | True 时返回 DryRunEstimate(token 数估算),不做实际 LLM 调用 |

### 13.2.2 默认 pipeline vs temporal pipeline

`<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py` 第 315–426 行的 `get_default_tasks` 与 `get_temporal_tasks` 给出了两套 DAG。

**默认 pipeline**(`temporal_cognify=False`):

```
classify_documents
  → extract_chunks_from_documents
  → extract_graph_and_summarize
  → add_data_points
  → extract_dlt_fk_edges
```

**Temporal pipeline**(`temporal_cognify=True`):

```
classify_documents
  → extract_chunks_from_documents
  → extract_events_and_timestamps
  → extract_knowledge_graph_from_events
  → add_data_points
```

时序模式会用 `cognee/tasks/temporal_graph/extract_events_and_entities.py` 把 chunk 拆成"事件 + 时间戳",再让 LLM 从事件序列里抽取知识图,因此节点带有时间属性。

### 13.2.3 自定义 graph_model 与 dry_run

```python
from typing import List
from pydantic import BaseModel
from cognee.shared.data_models import KnowledgeGraph
import cognee, asyncio

class SciPaperGraph(BaseModel):
    title: str
    authors: List[str]
    findings: List[str]

async def main():
    await cognee.add("Transformer 是 Vaswani 等人 2017 年提出的...")
    await cognee.cognify(
        graph_model=SciPaperGraph,
        chunk_size=1024,
        chunks_per_batch=20,
        custom_prompt="只抽取作者、标题、核心发现,忽略其它元数据。",
    )

    # 估算 token 用量,不真的调 LLM
    estimate = await cognee.cognify(dry_run=True)
    print(estimate)  # DryRunEstimate 对象

asyncio.run(main())
```

> 关键实现见 `<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py` 第 252–264 行的 dry_run 分支,与第 266–283 行的 default/temporal 分支。

### 13.2.4 同步 vs 异步执行

```python
import asyncio, cognee

async def main():
    # 同步:阻塞直到所有 dataset 处理完
    await cognee.cognify(datasets=["docs"], run_in_background=False)

    # 异步:立刻返回 PipelineRunInfo,pipeline 在后台跑
    run_infos = await cognee.cognify(
        datasets=["big_corpus"],
        run_in_background=True,
        chunks_per_batch=50,
    )
    print([r.pipeline_run_id for r in run_infos])

asyncio.run(main())
```

---

## 13.3 `cognee.search` 全参数

`cognee.search` 是 **Load** 之后的查询入口,定义见 `<COGNEE_REPO>/cognee/api/v1/search/search.py`,签名在第 31–59 行,是全框架签名最长的 API(27 个参数)。

### 13.3.1 完整参数表

| 参数 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `query_text` | `str` | 必填 | 自然语言查询 |
| `query_type` | `SearchType` | `GRAPH_COMPLETION` | 检索模式枚举,共 18 种(下文列表) |
| `user` | `Optional[User]` | `None` | 用户上下文 |
| `datasets` | `Optional[Union[list[str], str]]` | `None` | 按名称限定 dataset |
| `dataset_ids` | `Optional[Union[list[UUID], UUID]]` | `None` | 按 UUID 限定 dataset |
| `system_prompt_path` | `str` | `"answer_simple_question.txt"` | 系统 prompt 模板路径 |
| `system_prompt` | `Optional[str]` | `None` | 直接覆盖 system prompt |
| `top_k` | `int` | `15` | 主检索通道返回的条目上限 |
| `node_type` | `Optional[Type]` | `NodeSet` | 限定节点类型过滤 |
| `node_name` | `Optional[List[str]]` | `None` | 限定节点名列表 |
| `node_name_filter_operator` | `str` | `"OR"` | `"AND"` 或 `"OR"` |
| `only_context` | `bool` | `False` | True 时只返回上下文,不走 LLM |
| `session_id` | `Optional[str]` | `None` | 会话 ID,用于缓存 Q&A |
| `wide_search_top_k` | `Optional[int]` | `100` | 宽搜通道(扩展召回)的 top_k |
| `triplet_distance_penalty` | `Optional[float]` | `6.5` | 三元组检索的距离惩罚系数 |
| `feedback_influence` | `float` | 由 `base_config.default_feedback_influence` 决定 | 用户反馈对排序的影响权重 |
| `verbose` | `bool` | `False` | True 时返回包含图表示的详细结果 |
| `retriever_specific_config` | `Optional[dict]` | `None` | 透传到具体 retriever 的私有参数 |
| `neighborhood_depth` | `Optional[int]` | `None` | 图遍历的 k-hop 深度 |
| `neighborhood_seed_top_k` | `Optional[int]` | `None` | 邻居展开的种子节点上限 |
| `skills` | `Optional[List[Union[str, Skill]]]` | `None` | Agentic 检索时挂载的 Skill 列表 |
| `tools` | `Optional[List[str]]` | `None` | Agentic 检索时可用工具白名单 |
| `max_iter` | `Optional[int]` | `None` | Agentic 检索的最大工具调用轮数 |
| `include_references` | `bool` | `False` | 是否在结果里附加引用 |
| `llm_config` | `Optional[LLMConfig]` | `None` | 临时覆盖 LLM |
| `embedding_config` | `Optional[EmbeddingConfig]` | `None` | 临时覆盖 embedding |
| `code_query` | `Optional[dict[str, Any]]` | `None` | `query_type=CODE` 时的结构化查询参数 |

### 13.3.2 SearchType 枚举全表

定义见 `<COGNEE_REPO>/cognee/modules/search/types/SearchType.py`,共 **18** 种:

| SearchType | 中文 | 一句话用途 |
|---|---|---|
| `CHUNKS` | 片段检索 | 返回原始 chunk 列表 |
| `CHUNKS_LEXICAL` | 词法片段检索 | BM25 风格 |
| `SUMMARIES` | 摘要检索 | 返回 summary 节点 |
| `RAG_COMPLETION` | RAG 补全 | 经典 RAG,向量检索 + LLM |
| `HYBRID_COMPLETION` | 混合补全 | 向量 + 图混合 |
| `TRIPLET_COMPLETION` | 三元组补全 | 实体-关系-实体三元组 |
| `GRAPH_COMPLETION` | 图补全(默认) | 图遍历 + LLM |
| `GRAPH_COMPLETION_COT` | 图补全 CoT | 带思维链 |
| `GRAPH_COMPLETION_DECOMPOSITION` | 图补全分解 | 子查询分解 |
| `GRAPH_COMPLETION_CONTEXT_EXTENSION` | 图补全上下文扩展 | 上下文窗口扩展 |
| `GRAPH_SUMMARY_COMPLETION` | 图摘要补全 | 基于 summary 节点 |
| `CYPHER` | Cypher 检索 | 直接返回 Cypher 结果 |
| `NATURAL_LANGUAGE` | NL → Cypher | 自然语言转 Cypher |
| `TEMPORAL` | 时序检索 | 时间感知 |
| `FEELING_LUCKY` | 自动选型 | 让 cognee 决定 SearchType |
| `CODING_RULES` | 代码规则检索 | 程序性约束 |
| `CODE` | 代码检索 | 源代码上下文 |
| `AGENTIC_COMPLETION` | Agent 补全 | 多轮推理,可挂 skill/tool |

### 13.3.3 三组典型用法

**A. 快速问答 / 图补全**

```python
import asyncio, cognee
from cognee import SearchType

async def main():
    results = await cognee.search(
        "LangChain 与 LlamaIndex 的核心区别是什么?",
        query_type=SearchType.GRAPH_COMPLETION,
        top_k=10,
        datasets=["llm_frameworks"],
    )
    for r in results:
        print(r)

asyncio.run(main())
```

**B. 取上下文不调 LLM**

```python
import asyncio, cognee
from cognee import SearchType

async def main():
    chunks = await cognee.search(
        "向量数据库选型",
        query_type=SearchType.CHUNKS,
        only_context=True,
        top_k=5,
    )
    for c in chunks:
        print(c["text"][:120])

asyncio.run(main())
```

**C. Agentic 检索 + Skill/Tool**

```python
import asyncio, cognee
from cognee import SearchType

async def main():
    results = await cognee.search(
        "根据最新论文比较 RAG 与 GraphRAG",
        query_type=SearchType.AGENTIC_COMPLETION,
        datasets=["research_papers"],
        skills=["paper_summarizer", "citation_lookup"],
        tools=["web_search"],
        max_iter=5,
        include_references=True,
    )
    print(results)

asyncio.run(main())
```

> 注意:`skills`/`tools`/`max_iter` 必须配合 `AGENTIC_COMPLETION`,否则会抛 `InvalidAgenticSearchConfig`(`<COGNEE_REPO>/cognee/api/v1/search/search.py` 第 268–274 行);`code_query` 必须配合 `CODE`,否则抛 `InvalidCodeSearchConfig`(第 79–83 行)。

### 13.3.4 neighborhood_depth 与邻居展开

`GRAPH_COMPLETION_CONTEXT_EXTENSION` 与 `GRAPH_COMPLETION` 都会用到 `neighborhood_depth`(k-hop 深度)与 `neighborhood_seed_top_k`(种子上限)。`neighborhood_depth < 1` 会抛 `InvalidNeighborhoodDepth`。最稳的写法:

```python
await cognee.search(
    "城市间的物流关系",
    query_type="GRAPH_COMPLETION_CONTEXT_EXTENSION",
    neighborhood_depth=2,
    neighborhood_seed_top_k=20,
)
```

---

## 13.4 `cognee.update` 与 `cognee.delete`

### 13.4.1 `cognee.update`:delete-then-add-then-cognify

定义见 `<COGNEE_REPO>/cognee/api/v1/update/update.py`。**它不是 in-place 编辑**,而是:

1. `datasets.delete_data(dataset_id, data_id)` 删除旧条目
2. `add(data, dataset_id=..., incremental_loading=...)` 重新 ingest
3. `cognify(datasets=[dataset_id], incremental_loading=...)` 重跑该 dataset

这意味着 **update 等价于"删了再加再 cognify"**,会产生新的 document/chunk/实体,因此 update 后旧的图节点会被孤立成"孤儿"——需要靠 `cognee.prune` 清理。

```python
import asyncio, cognee
from uuid import UUID

async def main():
    # 假设已有 data_id
    run_info = await cognee.update(
        data_id=UUID("...uuid..."),
        data="/path/to/updated_file.pdf",
        dataset_id=UUID("...dataset-uuid..."),
    )
    print(run_info)

asyncio.run(main())
```

### 13.4.2 `cognee.delete`:已弃用

`<COGNEE_REPO>/cognee/api/v1/delete/__init__.py` 自 0.3.9 起标注 `@deprecated`,推荐迁移到 `cognee.datasets.delete_data(dataset_id, data_id, mode)`。

```python
import asyncio, cognee
from uuid import UUID

async def main():
    # 推荐写法
    await cognee.datasets.delete_data(
        dataset_id=UUID("...dataset-uuid..."),
        data_id=UUID("...data-uuid..."),
        mode="soft",   # 或 "hard"
    )

asyncio.run(main())
```

> 关键实现见 `<COGNEE_REPO>/cognee/api/v1/update/update.py` 第 78–108 行的"delete → add → cognify"三步走。

---

## 13.5 `cognee.visualize_graph` 与 `start_visualization_server`

### 13.5.1 `visualize_graph`:渲染自包含 HTML

`<COGNEE_REPO>/cognee/api/v1/visualize/visualize.py` 的 `visualize_graph` 会把当前 dataset 的知识图导出成单文件 HTML,适合发邮件、做 demo。**默认渲染种子邻居子图**(neighborhood 模式),不是全图。种子选择优先级:`seed_node_ids` > `recall_result` 溯源 > `query` 向量命中 > 度最高节点。

```python
import asyncio, cognee

async def main():
    path = await cognee.visualize_graph(
        destination_file_path="./graph.html",
        dataset="agent_arch_research",
        query="RAG 与 GraphRAG 的关系",
        neighborhood_depth=2,
        neighborhood_seed_top_k=10,
        max_nodes=300,
    )
    print(path)

asyncio.run(main())
```

### 13.5.2 `start_visualization_server`:本地 HTTP 服务

定义见 `<COGNEE_REPO>/cognee/api/v1/visualize/start_visualization_server.py`,返回一个 shutdown 句柄。常用于 Jupyter 内联查看。

```python
import asyncio, cognee

async def main():
    shutdown = cognee.start_visualization_server(port=8000)
    try:
        await asyncio.sleep(3600)   # 阻塞 1 小时
    finally:
        shutdown()                  # 关闭服务

asyncio.run(main())
```

---

## 13.6 `cognee.memify` 与 `cognee.prune`

### 13.6.1 `cognee.memify`:对已有图做"二次加工"

`<COGNEE_REPO>/cognee/modules/memify/memify.py` 的 `memify` 不重新 ingest,而是把 **已有知识图** 当输入,跑一组 extraction/enrichment tasks(默认 extraction 为 `get_triplet_datapoints`,仅当开启 `triplet_embedding` 时才有;默认 enrichment 为 `index_data_points`,见 `<COGNEE_REPO>/cognee/memify_pipelines/memify_default_tasks.py`)。`<COGNEE_REPO>/cognee/memify_pipelines/` 下还提供 `apply_feedback_weights`、`apply_frequency_weights`、`create_triplet_embeddings`、`global_context_index` 等可自定义任务。

```python
import asyncio, cognee

async def main():
    await cognee.add("用户问题:Transformer 的核心创新是什么?\n回答:自注意力机制...")
    await cognee.cognify()
    # 对图谱做二次记忆化:把短期使用记录固化为长期权重
    await cognee.memify(dataset="main_dataset", run_in_background=False)

asyncio.run(main())
```

支持 `extraction_tasks` / `enrichment_tasks` 列表,可以完全自定义管道,详见 `<COGNEE_REPO>/cognee/memify_pipelines/`。

### 13.6.2 `cognee.prune`:系统级剪枝

`<COGNEE_REPO>/cognee/api/v1/prune/prune.py` 把 prune 封装成两个静态方法:

| 方法 | 作用 |
|---|---|
| `cognee.prune.prune_data()` | 只清空业务数据(document/chunk),保留 schema |
| `cognee.prune.prune_system(graph=True, vector=True, metadata=False, cache=True)` | 清空图/向量/元数据/缓存,适合"重置但不删库" |

```python
import asyncio, cognee

async def main():
    await cognee.prune.prune_system(graph=True, vector=True, metadata=True, cache=True)
    # 等价于 cognee delete --all --dataset-name=main_dataset 之类 CLI

asyncio.run(main())
```

---

## 13.7 状态机

下图把 `add` / `cognify` / `search` / `update` / `delete` 的交互状态画成一个状态机,可以看到 **状态之间大多需要 dataset 已存在且数据已 ingest**:

![Ch13 — add / cognify / search 状态机](../../assets/diagrams/ch13-01-add-cognify-search.svg)

---

## 13.8 常见错误与边界

| 现象 | 根因 | 修复 |
|---|---|---|
| `SearchPreconditionError: no database/default user found` | 库未初始化、未跑过 `add` | 先 `await cognee.add(...)` 再 `search` |
| `InvalidAgenticSearchConfig` | 用 `skills`/`tools` 但 `query_type != AGENTIC_COMPLETION` | 改用 `AGENTIC_COMPLETION` 或去掉 skills |
| `InvalidCodeSearchConfig` | `code_query` 配了非 `CODE` | 改 `query_type=CODE` 或移除 `code_query` |
| `InvalidNeighborhoodDepth` | `neighborhood_depth < 1` | 给正整数 |
| `ValueError: dry_run not supported ... remote instance` | 远端模式下不允许 dry_run | `cognee.disconnect()` 后再估算 |
| `DatasetNotFoundError` | `datasets=` 名字拼错,或无权限 | 改用 `dataset_ids=`,或先 `cognee.datasets.list()` |
| update 后图谱出现重复实体 | update 等价于删了再加,旧实体成为孤儿 | 定期 `cognee.prune.prune_system(graph=True)` 清理 |

---

## 小结

- `cognee.add` 用 15 个参数控制"摄取":dataset 名/UUID、增量、后台、批大小、importance_weight、LLM/embedding 临时覆盖都给了独立旋钮。
- `cognee.cognify` 在 `temporal_cognify=False/True` 之间切换默认/temporal 两套 pipeline,`graph_model` 决定 LLM 输出的 schema,`dry_run=True` 可零成本估算 token。
- `cognee.search` 的 27 个参数覆盖了 18 种 SearchType、图遍历深度、Agentic skill/tool、CODE 结构化查询;`query_type` 与 `skills`/`code_query` 的兼容性由源代码层校验。
- `cognee.update` 实质是"delete→add→cognify"三步,会留下孤儿节点,需要 `prune` 清理;`cognee.delete` 已弃用,统一改用 `datasets.delete_data`。
- `cognee.memify` 在已有图上做 enrichment,`cognee.prune` 提供数据级与系统级两种剪枝。
- `visualize_graph` 默认渲染邻居子图,`start_visualization_server` 用于本地 HTTP 浏览。

## 实践作业

1. **(基础)** 把 `cognee.add` 的 `preferred_loaders` 设成 `["text", {"pdf": {"chunk_size": 800}}]`,用一段 PDF 跑通完整 add → cognify → search 流程。
2. **(进阶)** 写一个 `cognee.cognify(dry_run=True)` 的小工具,根据估算 token 数决定是否走后台模式(`run_in_background`)运行真实 cognify。
3. **(挑战)** 在 `AGENTIC_COMPLETION` 下挂一个自定义 Skill(`<COGNEE_REPO>/cognee/modules/engine/models/Skill.py`),实现"先召回再调用 web_search 验证"的多步检索。

## 推荐阅读

- 详见 [[chapter-12-graph-governance|第 12 章 大图治理:Sync / Migrations / Truth Subspace / Prune](../part-02-architecture/chapter-12-graph-governance.md)
- 详见 [[chapter-14-v2-memory-api|第 14 章 v2 内存 API:`remember` / `recall` / `improve` / `forget`]](./chapter-14-v2-memory-api.md)
- 源码:`<COGNEE_REPO>/cognee/api/v1/add/add.py`、`<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py`、`<COGNEE_REPO>/cognee/api/v1/search/search.py`
- 源码:`<COGNEE_REPO>/cognee/modules/search/types/SearchType.py`
- 示例:`<COGNEE_REPO>/examples/demos/simple_cognee_example.py`、`<COGNEE_REPO>/examples/guides/custom_graph_model.py`

## 下一章预告

第 14 章将展开 **18 种 SearchType 的选型决策树与典型 prompt**,并讲解 `retriever_specific_config` 的私有参数细节。