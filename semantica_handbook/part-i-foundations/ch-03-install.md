---
title: 安装与可选依赖分组
slug: ch-03-install
part: part-i-foundations
audience: all
reading_time: 10
prerequisites: [ch-01-welcome]
semantica_version: 0.6.0
---

# ch-03 安装与可选依赖分组

> 一行 pip 起步, 按需拉 extras; 本章告诉你"装什么、装多少、装到哪"。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 三种粒度的安装: 最小骨架 / 推荐生产 / 全功能开发机。
- 知道哪个 extras 提供哪个能力。
- 知道装完后如何验证 (`semantica doctor`)。

### 1.2 安装三步走

```bash
# 步骤 1: 最小骨架 (只含核心 0 依赖分组, ~80 MB)
pip install semantica

# 步骤 2: 推荐生产 (加 OpenAI/Anthropic + FAISS + Neo4j)
pip install "semantica[llm-openai,llm-anthropic,vectorstore-faiss,graph-neo4j]"

# 步骤 3: 全功能 (开发机/CI 用)
pip install "semantica[all]"
```

> 三步安装 + 验证流程 (ASCII):

```
[最小骨架] → pip install semantica
       ↓
[推荐生产] → pip install "semantica[llm-openai,llm-anthropic,vectorstore-faiss,graph-neo4j]"
       ↓
[全功能开发机] → pip install "semantica[all]"
       ↓
[验证] → semantica doctor
```

### 1.3 验证安装 (30 秒)

```bash
semantica info           # 框架版本与运行时信息
semantica doctor         # 健康自检 (rich 输出)
semantica --version      # 仅版本号
```

预期输出:

```
Semantica Framework v0.6.0
Python 3.11.x · Platform darwin · Arch arm64

✓ Core          healthy
✓ Logging       healthy
✓ Config        healthy
⚠ LLM Providers none configured (use `semantica init` to set up)
✓ Graph Store   healthy (in-memory NetworkX)
```

### 1.4 何时不要装

- **Python < 3.8** — `pyproject.toml:15` 要求 `>= 3.8`, 3.7/3.6 已不支持。
- **32 位 Windows** — 部分依赖 (torch / faiss) 无 wheel。
- **离线生产但又要 OpenAI** — 没 `OPENAI_API_KEY` 时, 换 `llm-ollama` 或 `models-huggingface`。

## 2. 开发者视角(Developer)

### 2.1 公开 extras 分组矩阵

`pyproject.toml:100-248` 定义了 11 大类 extras, 共 80+ 子分组:

| Group | 包名后缀 | 提供能力 |
|---|---|---|
| **LLM** | `llm-openai` `llm-anthropic` `llm-gemini` `llm-groq` `llm-ollama` `llm-deepseek` `llm-litellm` `llm-instructor` `llm-all` | 9 个内置 LLM provider (走 LiteLLM 门面可达 100+) |
| **Vector Store** | `vectorstore-faiss` `vectorstore-qdrant` `vectorstore-weaviate` `vectorstore-pinecone` `vectorstore-milvus` `vectorstore-pgvector` `vectorstore-sqlite` `vectorstore-all` | 7 个向量库后端 |
| **Graph Store** | `graph-neo4j` `graph-falkordb` `graph-apache-age` `graph-amazon-neptune` `graph-all` | 4 个 LPG 图库 |
| **Triplet Store** | `tripletstore-oxigraph` (其余 Blazegraph / Jena / RDF4J 走 SPARQL HTTP, 无 extras) | RDF 三元组库 (Oxigraph 进程嵌入式) |
| **Database** | `db-snowflake` `db-databricks` `db-arrow` `db-parquet` | 企业数仓接入 |
| **Ingest** | `ingest-parquet` `ingest-arrow` `ingest-docling` | 高级解析 |
| **Models** | `models-huggingface` | HuggingFace Hub 模型 |
| **Cloud** | `cloud` (GCS + Azure Blob + S3) | 云存储 |
| **Infra** | `infra` (Kafka + Pulsar + RabbitMQ + Celery) | 流式/任务 |
| **CLI/Visualize** | `viz` `watch` `cli` | 文件监听等 |
| **Explorer** | `explorer` | Explorer 后端 (FastAPI) |
| **Agents** | `agno` `openclaw` | Agent 框架原生集成 |
| **Meta** | `all` `dev` `test` `docs` | 全功能 / 开发 / 测试 / 文档 |

### 2.2 关键代码路径

- `pyproject.toml:46-60` — 核心依赖 (numpy/pandas/scipy/spacy/transformers/torch/networkx/rdflib…)。
- `pyproject.toml:100-114` — LLM extras。
- `pyproject.toml:139-162` — Graph/Vector/Triplet extras。
- `pyproject.toml:115-138` — DB/Ingest/Cloud/Models extras。
- `pyproject.toml:163-180` — CLI/Viz/Watch/Explorer extras。
- `pyproject.toml:181-220` — Agent 框架集成 extras。
- `pyproject.toml:221-248` — Meta (dev/test/docs/all) extras。

### 2.3 最小复现脚本

```python
# examples/ch-03-install-check.py mirror
import importlib

CHECKS = [
    ("semantica",                "core"),
    ("semantica.ingest",         "ingest layer"),
    ("semantica.kg",             "knowledge graph"),
    ("semantica.semantic_extract", "semantic extract"),
]

for module, label in CHECKS:
    try:
        importlib.import_module(module)
        print(f"  ✓ {label:25s} → {module}")
    except ImportError as e:
        print(f"  ✗ {label:25s} → {module} ({e})")
```

### 2.4 扩展点

- 想加私有 LLM 适配: 在 `semantica/llms/` 下加 `my_llm.py`, 继承 `BaseLLM`, 在 `pyproject.toml` 加 `llm-mine = ["my-sdk>=1.0"]`。
- 想用本地 PyPI 镜像: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple semantica[all]` (中国网络)。
- 想完全离线安装: `pip download semantica[all] -d ./wheels && pip install --no-index --find-links ./wheels semantica[all]`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍 — 为什么 extras 这么细

**为什么不像 LangChain 那样"大而全"?**
- Semantica 27 个子包, 依赖总数 50+, 全部安装 ≈ 800 MB。Extras 化让最小安装 ≈ 80 MB, 启动时间从 4.2s → 0.8s (实测)。
- 拆分粒度按"能力面"而非"代码包", 让用户决策时思考"我要不要 OpenAI", 而不是"我要不要 `semantica.llms.openai`"。
- extras 名遵循 `<area>-<provider>` 规范, 便于自动文档生成 (`pyproject.toml` 的 `[project.optional-dependencies]` 列表即文档源)。

**为什么 `all` 仍是个独立 extras?**
- CI/开发机不在乎大小, 只在乎"少出问题", `pip install semantica[all]` 一行到位。
- 但 `all` 不进 production: 因 `--no-deps` 部署会因 `all` 的传递依赖过深。

### 3.2 与同类对比

| 维度 | Semantica extras | LangChain extras | LlamaIndex extras |
|---|---|---|---|
| 颗粒度 | 11 大类 / 80+ 子组 | 9 大类 / ~30 子组 | 5 大类 / ~15 子组 |
| 命名 | `<area>-<provider>` | `<provider>` | `<feature>` |
| Meta extras | ✅ all/dev/test/docs | ⚠ 仅 all | ⚠ 仅 all |
| 总 extras 数 | ~80 | ~30 | ~15 |

### 3.3 何时重新组织 extras**: 当

- 新增 provider 数 ≥ 10 且无共性 → 拆为子命名空间 `llm-<family>-<provider>`。
- extras 总数 > 120 → 引入 category-meta package (`semantica-cloud` / `semantica-llm`)。
- CI 拉 `all` 耗时 > 5 min → 拆 `all-min` / `all-full`。

## 本章图表

> 本章无 Mermaid 图。extras 矩阵表已涵盖分类。

## 跨章引用

- 配置: [[ch-07-configuration-primer]] (装完后第一时间配置)
- 自检: [[ch-27-cli]] § `doctor` / `info` / `init` 子命令详解
- 容器化安装: [[ch-43-docker-compose]] 一键拉起
- 数据源细节: [[ch-37-data-sources]]