---
title: 术语表 (权威定义)
slug: ch-55-glossary
part: part-vii-reference
audience: all
reading_time: 8
prerequisites: []
semantica_version: 0.6.0
---

# ch-55 术语表 (权威定义)

> 本章是全手册的权威术语定义。`GLOSSARY.md` 是骨架版, 本章是完整版。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 遇到陌生术语时翻查权威定义。
- 按字母顺序快速定位 (A-Z 章节)。
- 关联术语用 "见 ..." 引导到其它词条, 无需重复定义。

### 1.2 阅读约定

- **粗体英文** 是术语本身。
- **破折号 —** 后面是定义。
- **链接** 用 `semantica.x.y` 形式指向源码位置。
- 关联术语用 "见 [[#章节]]" 形式反链。

### 1.3 何时不用

- 找 API 用法 → 看 [[ch-XX-YYY]] 对应模块章。
- 找错误码 → 看 [[ch-53-troubleshooting]]。
- 找变更历史 → 看 [[ch-56-changelog-references]]。

## A

- **AgentContext** — `semantica.context.AgentContext`, 把 ContextGraph 包装为单个 Agent 可用的运行时上下文。
- **ArrowExporter** — `semantica.export.ArrowExporter`, 出 Apache Arrow IPC 格式 (与 Pandas / Polars / DuckDB 互操作)。
- **AssociativeClass** — `semantica.ontology.AssociativeClass`, OWL 中"通过关系连接两个类"的关联类。
- **Athena** — 不在 Semantica 内, 仅在第三方集成中提到 (AWS Athena 查询 S3)。

## B

- **BiTemporal** — 双时态模型, `valid_time` (业务时间) + `recorded_at` (记录时间)。
- **BaseIngestor** — `semantica.ingest.BaseIngestor`, 所有数据接入器的基类。
- **BaseProvider** — `semantica.semantic_extract.providers.BaseProvider`, LLM provider 抽象层。
- **BGP** — Background Protocol (MCP 旧称)。

## C

- **ContextGraph** — `semantica.context.context_graph.ContextGraph`, 框架的内存图数据模型 (Explorer 后端的 source of truth)。
- **CausalChain** — 因果链, `add_causal_relationship` 串接的决策图链路。
- **ConflictDetector** — `semantica.conflicts.ConflictDetector`, 5 类冲突检测器。
- **ConflictResolver** — `semantica.conflicts.ConflictResolver`, 4 种解决策略。
- **Conflict** — 冲突, 5 类: value / type / temporal / relationship / logical。
- **ContextGraphMutationBridge** — ContextGraph 变更 → WebSocket 广播的桥接器。

## D

- **Decision** — `semantica.context.decision_models.Decision`, 一等决策图节点。
- **DecisionRecorder** — `semantica.context.DecisionRecorder`, 决策记录器。
- **DecisionQuery** — `semantica.context.DecisionQuery`, 决策查询。
- **Dedup** — 去重, 见 [ch-22-deduplication]。
- **Datalog** — 基于规则的查询语言, `semantica.reasoning.DatalogReasoner`。
- **DDL** — Data Definition Language, 暂不主要使用。
- **Docling** — 高级 PDF / DOCX 解析器 (`ingest-docling` extras)。

## E

- **Entity** — `Entity`, 图节点, `semantic_extract` 抽出。
- **EntityResolver** — `semantica.kg.EntityResolver`, 实体对齐 (Acme ≡ Acme Inc.)。
- **Endpoint** — REST 端点, 共 ~100 个。
- **ErrorCode** — `SEM001-SEM005`, 5 个错误码。
- **Extras** — `pyproject.toml:[project.optional-dependencies]`, 11 大类 / 80+ 子组。
- **Explorer** — Knowledge Explorer, React 19 + Sigma.js 工作台。
- **Extras** — 见 [[ch-03-install]]。

## F

- **FalkorDB** — Redis 一体图库 (60 MB 镜像)。
- **FAISS** — Facebook AI Similarity Search, 嵌入式向量索引。
- **FileIngestor** — `semantica.ingest.FileIngestor`, 文件接入。
- **ForceAtlas2** — 图布局算法, Explorer 默认。

## G

- **GLOSSARY.md** — 顶层骨架术语表, 本章是完整版。
- **GraphBuilder** — `semantica.kg.GraphBuilder`, 知识图构建器。
- **GraphStore** — `semantica.graph_store.GraphStore`, 图库 facade。
- **graphology** — JS 库, Explorer 的 in-memory 图。
- **GraphAwareChunker** — `semantica.split.GraphAwareChunker`, GraphRAG 友好分块。

## H

- **HybridSearch** — `semantica.vector_store.HybridSearch`, dense + sparse + metadata 三源融合。

## I

- **Ingest** — 数据接入, 见 [ch-08-ingest]。
- **Instructor** — 结构化输出库, `llm-instructor` extras。
- **InvestigatorGuide** — `generate_investigation_guide`, 冲突调查向导。

## J

- **JSON-LD** — JSON for Linking Data, 一种 RDF 序列化。

## K

- **KG** — Knowledge Graph, 知识图。
- **KGBuilder** — `semantica.kg.GraphBuilder` 别名。
- **KGVisualizer** — `semantica.visualization.KGVisualizer`, KG 可视化器。

## L

- **LLMExtraction** — `semantica.semantic_extract.LLMExtraction`, LLM 抽取包装。
- **LLM** — Large Language Model, 大语言模型。
- **Layer1/Layer2/Layer3 Provenance** — `semantica.provenance.bridge_axiom` 三层公理。
- **LiteLLM** — 100+ LLM 统一门面, `llm-litellm` extras。

## M

- **MCP** — Model Context Protocol, stdio 协议。
- **MCP Server** — `semantica.mcp_server`, 12 tools + 3 resources。
- **mermaid** — 图表语言, 用于因果链 / 决策图导出。
- **merge_strategy** — `first` / `latest` / `merge` / `voting`, 4 种合并策略。

## N

- **NamespaceManager** — `semantica.ontology.NamespaceManager`, 本体命名空间管理。
- **Neptune** — Amazon Neptune, AWS 一体图库。
- **NetworkX** — Python 图库, 默认内存图。
- **Neo4j** — 业界标准图库, GDS 算法齐全。

## O

- **OntologyGenerator** — `semantica.ontology.OntologyGenerator`, 6 阶段本体生成。
- **OntologyValidator** — `semantica.ontology.OntologyValidator`, SHACL 校验。
- **OWL** — Web Ontology Language, W3C 本体语言。
- **Ollama** — 本地 LLM 框架, `llm-ollama` extras。
- **Oxigraph** — 嵌入式 RDF 三元组库, `tripletstore-oxigraph` extras。

## P

- **PipelineBuilder** — `semantica.pipeline.PipelineBuilder`, DAG DSL。
- **ParquetExporter** — `semantica.export.ParquetExporter`, Parquet 列式导出。
- **PDFParser** — `semantica.parse.PDFParser`, 含 OCR。
- **PROV-O** — W3C Provenance Ontology, 溯源数据模型。
- **Policy** — `semantica.context.decision_models.Policy`, 策略。
- **PolicyEngine** — `semantica.context.policy_engine.PolicyEngine`, 策略引擎。
- **PostgreSQL** — Postgres, 通过 psycopg2 接入。
- **ProvenanceManager** — `semantica.provenance.ProvenanceManager`, 溯源管理。

## Q

- **QualityError** — `SEM004`, 置信度低于阈值。
- **QueryEngine** — `semantica.graph_store.QueryEngine`, Cypher 查询引擎。

## R

- **Reasoner** — `semantica.reasoning.Reasoner`, 规则推理。
- **RDFExporter** — `semantica.export.RDFExporter`, Turtle / N-Triples / JSON-LD。
- **Relationship** — 图边, `semantic_extract` 抽出。
- **Redis** — FalkorDB / cache 后端。
- **ReteEngine** — `semantica.reasoning.ReteEngine`, Rete 算法。
- **RRF** — Reciprocal Rank Fusion, dense + sparse + metadata 融合。

## S

- **SageMaker** — AWS SageMaker, 不在 Semantica 默认集成。
- **SHACL** — W3C Shapes Constraint Language, 数据校验。
- **Sigma** — Sigma.js, WebGL 图渲染。
- **SKOS** — Simple Knowledge Organization System, 词表管理。
- **SLSA** — Supply Chain Levels for Software Artifacts, 供应链安全。
- **SPARQL** — W3C RDF 查询语言。
- **Snowflake** — 企业数仓, `db-snowflake` extras。
- **SourceDocument** — ingest 输出的统一抽象。
- **StreamIngestor** — Kafka / Pulsar / RabbitMQ 接入。

## T

- **Triplet** — RDF 风格 `(subject, predicate, object)`。
- **TripletStore** — `semantica.triplet_store.TripletStore`, RDF 三元组库 facade。
- **TemporalValidationError** — `SEM001T`, 时态冲突。
- **TemporalVisualizer** — `semantica.visualization.TemporalVisualizer`, 时序可视化。
- **Tiktoken** — OpenAI tokenizer, 间接依赖。

## U

- **UMAP** — Uniform Manifold Approximation and Projection, 嵌入降维。
- **UMAP-learn** — Python 包, `semantica` 内置依赖。

## V

- **VectorStore** — `semantica.vector_store.VectorStore`, 向量库 facade。
- **VectorIndexer** — `semantica.vector_store.VectorIndexer`。
- **Visualization** — `semantica.visualization`, 6 类可视化。

## W

- **WebIngestor** — `semantica.ingest.WebIngestor`, 网页接入 (含 robots)。
- **W3C PROV-O** — 溯源数据模型。
- **WebSocket** — `/ws/graph-updates`, Explorer 实时推送。

## Y

- **YAML** — `~/.semantica/config.yaml`, 默认配置文件格式。

## Z

- **zvec** — sqlite-vec, `vectorstore-sqlite` extras。

## 补充词条 (E.1)

- **method_registry** — `semantica.core.registry.MethodRegistry`, 框架统一方法注册表 (替代早期各模块自有的 `register_*` 全局函数), 见 `semantica/ingest/registry.py:73` 与 `semantica/core/registry.py:128`。
- **`_ModuleProxy`** — `semantica/__init__.py:48`, lazy loader, 让用户写 `semantica.kg.xxx` 而无需先 `import semantica.kg`。
- **`build_knowledge_base`** — `semantica/core/methods.py:94` 框架级 facade, 一站式 `Semantica().build_knowledge_base(...)`。
- **ConfigurationError** — `semantica/utils/exceptions.py:215`, `error_code="SEM003"`, 配置校验失败。
- **TypeError** — Python 内置, 在 Semantica 中用于类型不匹配 (e.g., `EmbeddingGenerator(provider=...)` 收到未知 provider)。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `GLOSSARY.md` (顶层) — 骨架版, 约 100 词条。
- 本章 `ch-55-glossary.md` — 完整版, 约 200 词条。
- 全文所有 `[[ch-NN-slug]]` 跨章引用在术语首次出现时链接。

### 2.2 扩展点

- 加新术语: 先在本章登记, 再在引用章节首次出现处用 `[[ch-55-glossary]]` 反链。

## 3. 架构师视角(Architect)

### 3.1 术语治理

- 单一权威源 (this chapter), 避免散落多章导致冲突。
- 新术语纳入前必须经 maintainer 审查, 防止语义漂移。
- 关联术语用 "见 ...", 不重复定义。

## 跨章引用

- 上一章: [[ch-54-faq]]
- 下一章: [[ch-56-changelog-references]]