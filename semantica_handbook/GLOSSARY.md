---
title: Semantica Handbook 术语表
slug: glossary
part: part-i-foundations
audience: all
reading_time: 5
prerequisites: []
semantica_version: 0.6.0
---

# 术语表 (Glossary)

> 本表为全手册的权威术语定义。后续章节中首次出现的术语应在此先登记。

## 框架与项目

- **Semantica** — 项目名, 同时指 Python 框架主类 `semantica.core.Semantica`。口号 "Accountability & Context Layer for AI Agents"。
- **Knowledge Explorer (Explorer)** — Semantica 自带的 React/Vite/Sigma.js 单页可视化工作台, 启动后通过 `semantica-explorer` CLI 入口。
- **ContextGraph** — `semantica.context.context_graph.ContextGraph`, 框架的内存图数据模型, 是 Explorer 后端的"事实来源 (source of truth)"。

## 数据模型

- **SourceDocument** — 原始接入文档的统一抽象, 经 `ingest` 产生。
- **Entity (实体)** — 图谱中的节点, 由 `semantic_extract` 抽出, 具备 `id / type / name / properties / confidence` 等字段。
- **Relationship (关系)** — 图谱中的边, 持有 `source_id / target_id / type / properties / confidence / provenance_ref`。
- **Triplet (三元组)** — RDF 风格的 `(subject, predicate, object)`, 是 `triplet_store` 的最小数据单元。
- **Decision (决策)** — 框架一等公民, `context/decision_methods.py:Decision`, 描述一个 AI 决策及其因果链。
- **Policy (策略)** — 合规/审计规则, `context/policy_engine.py:Policy`, 与 Decision 一同进入决策图。
- **Provenance (溯源)** — W3C PROV-O 兼容的来源链, 每个实体/边/决策都可问"哪里来"。

## 模块与包

- **`semantica`** — 顶层包, 0.6.0 版本。提供 `_ModuleProxy` 实现 `semantica.kg.xxx` 的点符号访问。
- **`semantica.core`** — 编排核心, 含 `Semantica` 主类 (1026 行)、`Config` / `ConfigManager`、`LifecycleManager`、`PluginRegistry`、`core/methods.py` 框架级 facade。
- **`semantica.ingest`** — 数据接入(文件/Web/DB/Cloud/Stream)。
- **`semantica.parse`** — 格式解析(PDF/HTML/MD/DOCX 等)。
- **`semantica.normalize`** — 标准化(编码/字段名/单位)。
- **`semantica.split`** — 分块, 含 graph-aware chunk。
- **`semantica.semantic_extract`** — NER、关系抽取、三元组抽取; 支持 pattern / regex / rules / ml / huggingface / llm 六种策略。
- **`semantica.kg`** — 知识图构建、分析、解析、时序模型。
- **`semantica.embeddings`** — Embedding 抽象层, 含 `EmbeddingGenerator`、`GraphEmbeddingManager`、`VectorEmbeddingManager`。
- **`semantica.vector_store`** — 向量库适配(FAISS/Qdrant/Weaviate/Pinecone/Milvus/pgvector/sqlite-vec)。
- **`semantica.graph_store`** — 图库适配(Neo4j/FalkorDB/Apache AGE/Amazon Neptune)。
- **`semantica.triplet_store`** — RDF 三元组库(Oxigraph 内置 + Blazegraph/Jena/RDF4J/Anzo 远程)。
- **`semantica.ontology`** — 本体(OWL/SHACL/SKOS)生成、验证、对齐。
- **`semantica.reasoning`** — 推理引擎, 含 Rete、Datalog、SPARQL、演绎/溯因、时序。
- **`semantica.provenance`** — 来源管理, 输出 W3C PROV-O。
- **`semantica.context`** — ContextGraph + AgentContext + DecisionRecorder + PolicyEngine。
- **`semantica.deduplication`** — 去重(精确/模糊/语义)。
- **`semantica.conflicts`** — 冲突检测与解决。
- **`semantica.pipeline`** — PipelineBuilder DSL + ExecutionEngine。
- **`semantica.change_management`** — 版本/回滚/checksum。
- **`semantica.visualization`** — KG / Ontology / Embedding / Analytics / Temporal / Semantic-Network 可视化。
- **`semantica.export`** — 导出器(RDF/Parquet/Arrow/CSV/JSON-LD/OWL/SHACL/GraphML/Neo4j-CSV/ArangoDB-AQL)。
- **`semantica.llms`** — LLM 提供商薄封装(OpenAI/Anthropic/Gemini/Groq/Mistral/Llama/Cohere/Azure/Bedrock/Ollama/DeepSeek/HuggingFace)。
- **`semantica.mcp_server`** — Model Context Protocol stdio 服务, 12 个 tool + 3 个 resource。
- **`semantica.explorer`** — Knowledge Explorer 的 FastAPI 后端, ~100 个 REST 端点 + WebSocket。
- **`semantica.cli`** — Click + Rich 命令行, ~80 个子命令。

## 集成与协议

- **MCP (Model Context Protocol)** — 让 LLM/IDE 通过 stdio 调用 Semantica 工具的标准协议。
- **RRF (Reciprocal Rank Fusion)** — 倒数排名融合, `semantica.vector_store.hybrid_search` 用以合并 dense + sparse + metadata 检索结果。
- **SHACL** — W3C Shapes Constraint Language, 用于本体数据校验。
- **SKOS** — Simple Knowledge Organization System, 词表管理标准。
- **PROV-O** — W3C Provenance Ontology, 溯源数据模型。
- **W3C PROV-O export** — ProvenanceManager 输出 Turtle/JSON 的能力。

## 部署与运维

- **extras** — `pyproject.toml` 中的可选依赖分组, 如 `llm-openai` / `vectorstore-qdrant` / `graph-neo4j`。
- **Helm / Kustomize** — Kubernetes 部署模板位于 `deploy/helm/` 与 `deploy/kubernetes/`。
- **air-gap** — 无网环境; Semantica 提供 `--no-color` / 离线 LLM (Ollama/HuggingFace) 选项。

## 占位章节

> 本节在 ch-55-glossary 完整化; 后续章节每次引入新术语应先在此登记。