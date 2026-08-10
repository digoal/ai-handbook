---
title: 数据源适配 — file / web / db / cloud / stream / HF
slug: ch-37-data-sources
part: part-iv-integrations
audience: all
reading_time: 11
prerequisites: [ch-08-ingest]
semantica_version: 0.6.0
---

# ch-37 数据源适配 — file / web / db / cloud / stream / HF

> 9 大类数据源统一 facade。本章给出适配矩阵 + 接入步骤 + 已知陷阱。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 9 大类数据源: file / web / db / cloud / stream / repo / email / MCP / HuggingFace Hub。
- 自动格式嗅探 (PDF / DOCX / HTML / MD / CSV / Parquet / Excel)。
- Web 接入内置 robots.txt 合规。
- Kafka / Pulsar / RabbitMQ 三流引擎支持。

### 1.2 适配矩阵

| 类别 | 后端 | extras |
|---|---|---|
| **file** | FileIngestor | (内置) |
| **web** | WebIngestor / ContentExtractor / SitemapCrawler | (内置) |
| **db** | DBIngestor (PostgreSQL / MySQL / SQLite) | (内置) |
| **cloud** | SnowflakeIngestor / DatabricksIngestor / S3 / GCS / Azure Blob | `db-snowflake` / `db-databricks` / `cloud` |
| **stream** | StreamIngestor (Kafka / Pulsar / RabbitMQ) | `infra` |
| **repo** | RepoIngestor (Git) | (内置) |
| **email** | EmailIngestor (IMAP / POP3) | (内置) |
| **MCP** | MCPIngestor | (内置) |
| **HuggingFace** | HuggingFaceIngestor | `models-huggingface` |

### 1.3 一段最小可跑示例

```python
from semantica.ingest import (
    FileIngestor, WebIngestor, DBIngestor, SnowflakeIngestor,
    StreamIngestor, HuggingFaceIngestor,
)

# file
FileIngestor().ingest(["./docs/intro.pdf"])

# web (含 robots.txt)
WebIngestor().ingest(["https://example.com/paper.pdf"], respect_robots=True)

# db
DBIngestor(connection="postgresql://u:p@h/db").ingest("SELECT * FROM papers LIMIT 100")

# Snowflake
SnowflakeIngestor().ingest(query="SELECT * FROM papers", warehouse="COMPUTE_WH")

# Kafka
StreamIngestor(broker="kafka:9092", topic="papers").ingest(timeout=30)

# HuggingFace Hub
HuggingFaceIngestor().ingest(repo="openai/whisper-large-v3", kind="dataset")
```

### 1.4 何时不用

- 你的数据是单一格式 → 直接用 `FileIngestor`, 不必装 extras。
- 你的数据要"实时 + 高吞吐" → 用专用 ETL (Fivetran / Airbyte)。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/ingest/__init__.py` — 8 个 ingestor 导出。
- `semantica/ingest/registry.py` — `method_registry [[ch-55-glossary]].register` reader 注册。
- `semantica/ingest/file_ingestor.py` — 格式嗅探 + reader 路由。
- `semantica/ingest/web_ingestor.py` — robots / sitemap / content extraction。
- `semantica/ingest/db_ingestor.py` — psycopg2 / sqlalchemy。
- `semantica/ingest/stream_ingestor.py` — kafka-python / pulsar-client / pika。
- `semantica/ingest/snowflake_ingestor.py` — `db-snowflake` extras。
- `semantica/ingest/databricks_ingestor.py` — `db-databricks` extras。
- `semantica/ingest/huggingface_ingestor.py` — `models-huggingface` extras。

### 2.2 最小复现脚本

```python
# examples/ch-37-data-smoke.py mirror
from semantica.ingest import FileIngestor, check_available_ingestors

docs = FileIngestor().ingest(["./README.md"])
print(check_available_ingestors())  # {'file': True, 'web': True, ...}
```

### 2.3 已知陷阱

- **PDF 扫描版**: 需先 OCR, 否则抽不到字。
- **Snowflake 网络**: 需出站到 snowflakecomputing.com:443, VPC 要放行。
- **Kafka SSL**: 默认 PLAINTEXT, 生产需 SASL_SSL。
- **HuggingFace rate limit**: 免费账号有 60 RPM。
- **DB 大表**: 千万行一次性 ingest 会爆, 用分页 + cursor。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 9 类分开, 不做统一 `Ingestor.from_uri(uri)`?**
- 不同源的"凭证 + 协议 + 数据模型"差异巨大, 强行统一会变成"最小公倍数"丑陋 API。
- 分类后, 用户可按场景选, 不必理解所有 URI scheme。

### 3.2 与同类对比

| 维度 | Semantica ingest | LangChain DocumentLoaders | LlamaIndex Readers |
|---|---|---|---|
| 源数 | 9 大类 / ~30 具体 | 100+ | 100+ |
| Robots 检查 | ✅ | ❌ | ⚠ |
| Kafka/Pulsar/RabbitMQ | ✅ | ⚠ 弱 | ⚠ |

### 3.3 何时重新设计

- reader 数 > 200 → 拆 `semantica-ingest-files` / `semantica-ingest-cloud` 子包。
- 出现"实时流"需求 → 引入消息队列背压。

## 跨章引用

- 上一章: [[ch-36-triple-stores-compat]]
- 下一章: [[ch-38-agent-frameworks]]