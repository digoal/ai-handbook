---
title: Cookbook 索引 — 37 个 notebook 导航
slug: ch-50-cookbook-index
part: part-vii-reference
audience: all
reading_time: 10
prerequisites: []
semantica_version: 0.6.0
---

# ch-50 Cookbook 索引 — 37 个 notebook 导航

> `cookbook/` 下有 21 个入门 + 13 个进阶 + 3 个 Agno 集成 = 37 个 Jupyter notebook, 全部带 Colab 一键运行徽章。本章给出主题导航。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 跑任意 notebook (`jupyter nbconvert --execute` 或 Colab)。
- 复制代码到自己的项目。
- 按场景找最近 demo。

### 1.2 Introduction (21 个)

| # | notebook | 主题 | 关联手册章 |
|---|---|---|---|
| 01 | `01_Welcome_to_Semantica` | 5 行 demo | [[ch-01-welcome]] |
| 02 | `02_Data_Ingestion` | 8 类 ingestor | [[ch-08-ingest]] |
| 03 | `03_Document_Parsing` | parse 全套 | [[ch-09-parse]] |
| 04 | `04_Data_Normalization` | normalize | [[ch-10-normalize]] |
| 05 | `05_Entity_Extraction` | 6 种策略 | [[ch-12-semantic-extract]] |
| 06 | `06_Relation_Extraction` | 关系抽取 | [[ch-12-semantic-extract]] |
| 07 | `07_Building_Knowledge_Graphs` | kg.GraphBuilder [[ch-55-glossary]] | [[ch-14-knowledge-graph]] |
| 08 | `08_Your_First_Knowledge_Graph` | 端到端 | [[ch-40-flow-a-text-to-graph]] |
| 09 | `09_Graph_Store` | Neo4j 等 | [[ch-18-graph-store]] |
| 10 | `10_Graph_Analytics` | pagerank/community | [[ch-14-knowledge-graph]] |
| 11 | `11_Chunking_and_Splitting` | 7 chunker | [[ch-11-split]] |
| 12 | `12_Embedding_Generation` | EmbeddingGenerator | [[ch-13-embeddings]] |
| 13 | `13_Vector_Store` | FAISS/Qdrant | [[ch-17-vector-store]] |
| 14 | `14_Ontology` | OWL/SHACL/SKOS | [[ch-15-ontology]] |
| 15 | `15_Export` | 12 类导出 | [[ch-26-visualization-export]] |
| 16 | `16_Visualization` | KG/Ontology/Embedding | [[ch-26-visualization-export]] |
| 17 | `17_Conflict_Detection_and_Resolution` | 5 类冲突 | [[ch-23-conflicts]] |
| 18 | `18_Deduplication` | 3 种去重 | [[ch-22-deduplication]] |
| 19 | `19_Context_Module` | 决策图 | [[ch-21-context-decision]] / [[ch-42-flow-c-decision-intel]] |
| 20 | `20_Triplet_Store` | RDF / SPARQL | [[ch-19-triplet-store]] |
| 21 | `21_Amazon_Neptune_Store` | Neptune | [[ch-35-graph-stores-compat]] |

### 1.3 Advanced (13 个)

| # | notebook | 主题 | 关联手册章 |
|---|---|---|---|
| 01 | `01_Advanced_Extraction` | LLM + 自定义 schema | [[ch-12-semantic-extract]] |
| 02 | `02_Advanced_Graph_Analytics` | GNN / link prediction | [[ch-14-knowledge-graph]] |
| 03 | `03_Complete_Visualization_Suite` | 6 类可视化 | [[ch-26-visualization-export]] |
| 05 | `05_Multi_Format_Export` | 12 类导出 | [[ch-26-visualization-export]] |
| 06 | `06_Multi_Source_Data_Integration` (66 KB) | 多源端到端 | [[ch-41-flow-b-multi-source]] |
| 07 | `Advanced_Vector_Store_and_Search` | hybrid search + RRF | [[ch-17-vector-store]] |
| 08 | `08_Reasoning_and_Inference` | Rete / Datalog | [[ch-16-reasoning]] |
| 09 | `09_Semantic_Layer_Construction` | 本体 + 推理 | [[ch-15-ontology]] |
| 10 | `10_Temporal_Knowledge_Graphs` | BiTemporal | [[ch-25-change-management]] |
| 11 | `11_Advanced_Context_Engineering` | 决策上下文 | [[ch-21-context-decision]] |
| 12 | `12_Unstructured_to_to_ontology` | 文本 → OWL | [[ch-15-ontology]] |
| 13 | `13_Manual_Ontology_Snowflake_Mapping` | 本体映射 | [[ch-37-data-sources]] |
| 14 | `14_Datalog_Style_Reasoning` | Datalog 推理 | [[ch-16-reasoning]] |

### 1.4 Integrations (3 个, Agno)

| # | notebook | 主题 | 关联手册章 |
|---|---|---|---|
| 01 | `agno_decision_intelligence` | Agno + 决策 | [[ch-21-context-decision]] / [[ch-38-agent-frameworks]] |
| 02 | `agno_graphrag_context` | Agno + GraphRAG | [[ch-38-agent-frameworks]] |
| 03 | `agno_multi_agent_shared_context` | 多 agent 共享 | [[ch-38-agent-frameworks]] |

### 1.5 辅助资产

- `introduction/config.yaml` — 教学版默认配置。
- `introduction/neptune-setup.yaml` — Neptune 连接参考。
- `introduction/corporate_ontology.ttl` — 企业本体示例。
- `advanced/knowledge_graph.ttl` — 知识图 TTL 示例。
- `advanced/quantum_ontology.ttl` — 物理本体示例。
- `advanced/snowflake_ingestion_examples.py` — Snowflake 接入剧本。

## 2. 开发者视角(Developer)

### 2.1 公开资源

```python
# 入口 (cookbook 在仓库根目录, 不在 Python 包内)
import subprocess
subprocess.run(["jupyter", "nbconvert", "--execute",
                "cookbook/introduction/08_Your_First_Knowledge_Graph.ipynb"])
```

### 2.2 关键路径

- `cookbook/introduction/` — 21 个 `.ipynb`。
- `cookbook/advanced/` — 13 个 `.ipynb`。
- `cookbook/integrations/` — 3 个 `.ipynb`。

### 2.3 已知陷阱

- notebook 默认用 LLM key, 需 `~/.semantica/config.yaml` 配。
- 部分 notebook 需 FalkorDB / Neo4j 启动。
- `06_Multi_Source_Data_Integration` 66 KB, 含大量数据, 跑慢。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 notebook 在仓库, 不在 docs site?**
- notebook 是"代码", 与源码同步维护。
- docs site 是"文档", 单独部署 (Mintlify)。

**为什么 37 个 notebook 不拆子包?**
- 一个目录 (`cookbook/`) 集中, 避免路径混乱。
- 子目录按"难度 + 主题"分。

### 3.2 与同类对比

| 维度 | Semantica Cookbook | LangChain Cookbook | LlamaIndex Examples |
|---|---|---|---|
| notebook 数 | 37 | 50+ | 100+ |
| Colab 一键运行 | ✅ | ⚠ | ✅ |
| 与代码同仓 | ✅ | ❌ | ⚠ |

## 跨章引用

- 上一章: [[ch-49-security]]
- 下一章: [[ch-51-testing]]
- 端到端剧本: [[ch-40-flow-a-text-to-graph]]