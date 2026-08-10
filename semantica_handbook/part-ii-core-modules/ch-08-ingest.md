---
title: 数据接入 (Ingest) — 文件/网络/数据库/云/流
slug: ch-08-ingest
part: part-ii-core-modules
audience: all
reading_time: 12
prerequisites: [ch-04-architecture-30kft, ch-05-data-models]
semantica_version: 0.6.0
---

# ch-08 数据接入 (Ingest)

> Semantica 的"零号层" — 把任何源的原始数据变成统一的 `SourceDocument`。本章讲解 8 大 ingestor 的分工与注册机制。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 把本地文件、网页、数据库、雪花/Databricks、Kafka 流、HuggingFace Hub 接入。
- 自动判定类型 (PDF / DOCX / HTML / Markdown / Parquet) — 不必显式指定。
- 在 CI 中监听文件夹 (watchdog) 自动 ingest。

### 1.2 一段最小可跑示例

```python
from semantica.ingest import FileIngestor, WebIngestor, DBIngestor, register_reader

# 1) 文件接入
docs = FileIngestor().ingest("./docs/whitepaper.pdf")
print(f"Got {len(docs)} SourceDocument(s)")

# 2) 网络接入 (含 robots.txt 合规)
docs = WebIngestor().ingest(["https://example.com/paper.pdf"])

# 3) 数据库接入
docs = DBIngestor(connection="postgresql://u:p@h/db").ingest("SELECT * FROM papers LIMIT 100")

# 4) 自定义 Reader 注册
class MyCSVReader:
    def read(self, path): ...  # 返回 SourceDocument
register_reader("csv", MyCSVReader())
```

### 1.3 常见坑 / 何时不用

- **巨型 PDF (>500 MB)**: 先用 `pdf2text` 预处理, 否则内存爆炸。
- **网络反爬**: 先调 `WebIngestor` 的 `respect_robots=True`, 别绕开 robots.txt。
- **数据库敏感数据**: 接入前先做 PII 脱敏, 否则 `provenance` 会原样落库。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
# 主类
semantica.ingest.FileIngestor()           # 文件
semantica.ingest.WebIngestor()            # 网页 / RSS
semantica.ingest.DBIngestor(connection)   # PG / MySQL / SQLite
semantica.ingest.ParquetIngestor()        # Parquet / Arrow
semantica.ingest.SnowflakeIngestor()      # Snowflake (extras: db-snowflake)
semantica.ingest.DatabricksIngestor()     # Databricks (extras: db-databricks)
semantica.ingest.StreamIngestor()         # Kafka / Pulsar / RabbitMQ
semantica.ingest.RepoIngestor()           # Git 仓库
semantica.ingest.EmailIngestor()          # IMAP / POP3
semantica.ingest.MCPIngestor()            # MCP 资源

# 注册/查找 (走 method_registry [[ch-55-glossary]])
from semantica.method_registry import method_registry
method_registry.register("ingest_file", "csv", MyCSVReader)   # registry.py:73
```

### 2.2 关键代码路径

- `semantica/ingest/__init__.py` — 8 个 ingestor 导出。
- `semantica/ingest/registry.py:73` — `method_registry.register("ingest_file", ext, reader_cls)`。
- `semantica/ingest/file_ingestor.py` — `FileIngestor` (按扩展名 sniff → reader 路由)。
- `semantica/ingest/web_ingestor.py` — `WebIngestor / ContentExtractor / SitemapCrawler / RobotsChecker`。
- `semantica/ingest/db_ingestor.py` — `DBIngestor` (psycopg2 / sqlite3 / sqlalchemy)。
- `semantica/ingest/stream_ingestor.py` — `StreamIngestor` (Kafka / Pulsar / pika)。
- `semantica/ingest/snowflake_ingestor.py` — `SnowflakeIngestor` (extras `db-snowflake`)。
- `semantica/ingest/databricks_ingestor.py` — `DatabricksIngestor` (extras `db-databricks`)。
- `semantica/ingest/huggingface_ingestor.py` — `HuggingFaceIngestor` (extras `models-huggingface`)。
- `semantica/ingest/parquet_ingestor.py` — `ParquetIngestor / ArrowIngestor`。

### 2.3 最小复现脚本

```python
# examples/ch-08-ingest-minimal.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica.ingest import FileIngestor

docs = FileIngestor().ingest(["./README.md"])
for d in docs:
    print(f"- {d.source_id[:8]}... ({d.source_type})")
```

### 2.4 扩展点

- **加新数据源**: 实现 reader 类 (含 `read(path) -> SourceDocument`), 然后 `method_registry.register("ingest_file", "csv", MyCSVReader)`。
- **加新的存储后端 (e.g. S3)**: 实现 reader 类, 在 `boto3` 回调里取 bytes, 返回 `SourceDocument`, 然后注册到对应 `ingest_*` 域。
- **加 watch 模式**: 在 `cli.py:951 watch` 实现中复用 `method_registry` + watchdog `Observer`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 ingest 不直接消费 LLM?**
- ingest 层职责单一: "字节 → SourceDocument", 不做语义理解。
- 这让 ingest 可以在没有 LLM key 的环境运行 (CI / 离线 ETL), 也让 semantic_extract 可以独立替换 LLM provider。

**为什么 reader 注册走 `method_registry` 而非全局函数?**
- 用户从 notebook 调 `method_registry.register("ingest_file", "csv", MyCSVReader)` 就能扩展, 复用 framework 的统一注册表, 避免每模块各搞一套。
- 代价: 跨域注册 (如 ingest 与 kg) 共享同一 namespace, 命名需加前缀 ("ingest_file" / "kg_*")。

### 3.2 与同类对比

| 维度 | Semantica ingest | LangChain DocumentLoaders | LlamaIndex Readers |
|---|---|---|---|
| 数据源数 | 10 大类 / ~30 具体 reader | 100+ | 100+ |
| Robots 检查 | ✅ 内置 | ❌ | ⚠ 少数 |
| 注册机制 | 全局函数 | 类继承 | `reader.py` registry |

### 3.3 何时重新设计

- reader 数 > 200 → 拆 `semantica-ingest-files` / `semantica-ingest-cloud` 子包。
- ingest 成为瓶颈 → 引入并行 ingest pipeline (semantica.pipeline)。
- 用户要"流批一体" → `StreamIngestor` 与 `FileIngestor` 统一接口, 共享下游。

## 本章图表

> 本章无 Mermaid 图。数据流位置见 [[ch-04-architecture-30kft]] FIG-01 第 ① 层。

## 跨章引用

- 上一章: [[ch-07-configuration-primer]]
- 下一章: [[ch-09-parse]] 解析 SourceDocument
- 多数据源集成剧本: [[ch-37-data-sources]]
- 多源主轴: [[ch-41-flow-b-multi-source]]