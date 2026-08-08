# 第 10 章 `Storage Backends: 存储后端`

> 本章目标:读完本章,你将能够
> - 解释关系、向量、图三类存储各自承担的职责及公共抽象层
> - 在嵌入式、Postgres 与云托管方案之间完成生产选型
> - 通过 `cognee.config` 切换三栈后端,并理解迁移、隔离与子进程约束

## 前置知识

- 已读完 [[chapter-07-data-model|第 7 章 数据模型与实体:DataPoint / Entity / NodeSet / KnowledgeGraph]](./chapter-07-data-model.md)
- 需要的基础库:`cognee>=1.4.0`、`pydantic>=2.0`、`asyncio`
- 环境:Python 3.10–3.14

## 本章导览

- 10.1 从统一接口理解三栈,避免业务代码绑定具体数据库
- 10.2–10.5 比较图、向量、关系及 Hybrid 后端
- 10.6–10.7 处理子进程、WAL checkpoint 与会话缓存
- 10.8 用决策表把规模、运维能力和隔离要求转成选型

---

## 10.1 三栈架构与抽象层

为什么不把所有数据塞进同一种数据库?因为三类访问模式不同:关系层保存 Dataset、用户、权限和
PipelineRun 等控制面状态;向量层回答“语义上最相近的内容是什么”;图层回答“实体之间如何连接”。
三者共同组成持久化平面,而不是三份互相替代的数据副本。

![Ch10 — Cognee 关系、向量、图三栈架构](../../assets/diagrams/ch10-01-cognee.svg)

公共抽象的价值是把上层 Pipeline 与厂商 SDK 解耦。图契约定义节点、边、邻居、子图、原始查询及删除
等能力,见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/graph_db_interface.py`;
图工厂根据 provider 创建并缓存适配器,见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/get_graph_engine.py`。向量契约统一
collection、写入、检索、批量检索、删除和 embedding,见
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/vector_db_interface.py`;
其工厂入口见
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/get_vector_engine.py`。

关系层通过
`<COGNEE_REPO>/cognee/infrastructure/databases/relational/get_relational_engine.py`
解析配置。文本到向量的模型选择独立于向量库,由
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/embeddings/get_embedding_engine.py`
负责。也就是说,更换 OpenAI、FastEmbed 或 LiteLLM 路由的 embedding 模型,不等于更换向量数据库。

多租户场景还多一层 Dataset DB Handler。它为每个 Dataset 创建、解析和删除数据库连接信息,实现
逻辑或物理隔离;注册表位于
`<COGNEE_REPO>/cognee/infrastructure/databases/dataset_database_handler/`。选型时应同时检查
provider 与对应 handler,不能只改连接 URL。

---

## 10.2 图数据库: Ladybug / Kuzu / Neo4j / Neptune / PG / Turso

为什么默认选择 Ladybug?本地开发需要零服务依赖、低启动成本和可携带的数据目录。Ladybug 是 Kuzu
的官方 fork,以嵌入式方式工作;默认适配器实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/ladybug/adapter.py`。旧部署仍可使用
`kuzu` provider,其兼容实现位于
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/kuzu/adapter.py`。两者适合单机和边缘
部署,但共享同一数据库目录时必须认真处理进程锁。需要远程实例时可选
`ladybug-remote` / `kuzu-remote`(同一适配器实现下 `RemoteLadybugAdapter`),它们走 HTTP
而非本地文件,适配器入口见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/ladybug/remote_ladybug_adapter.py`。

Neo4j 适合已有 Neo4j 运维体系、需要 Bolt 连接和成熟图工具链的团队,适配器见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/neo4j_driver/adapter.py`。AWS Neptune
适合 AWS 托管环境及 IAM、VPC 治理要求,见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/neptune_driver/adapter.py`。Neptune
Analytics 同时承担图与向量角色,适配器见
`<COGNEE_REPO>/cognee/infrastructure/databases/hybrid/neptune_analytics/NeptuneAnalyticsAdapter.py`,
通过 `graph_database_provider=neptune_analytics` 接入。PostgreSQL Graph 把节点、边落在
Postgres 表中,便于复用备份、监控与连接池,见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/postgres/adapter.py`。Turso Graph 则面向
libSQL/边缘场景,见
`<COGNEE_REPO>/cognee/infrastructure/databases/graph/turso/adapter.py`(当前仅支持本地
libSQL 文件,远程 embedded-replica 同步尚未开放)。

图后端不是“连接成功就等价”。上线前至少用自己的 workload 验证 Cypher/查询方言、批量写吞吐、深度
遍历延迟、provenance 删除能力、备份恢复以及并发模型。尤其不要把嵌入式数据库文件放到多个 Pod
共享写入,然后期待网络文件系统自动提供数据库级一致性。

---

## 10.3 向量数据库: LanceDB / PGVector / Turso

为什么 LanceDB 是默认值?它与本地默认栈一样无需单独服务,适合开发、测试和单机应用。实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/lancedb/LanceDBAdapter.py`。当系统已经
以 Postgres 为主数据库,PGVector 可减少运维种类,并利用统一备份和 SQL 观测;实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/pgvector/PGVectorAdapter.py`。Turso Vector
适合 libSQL 及边缘部署,实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/turso/TursoVectorAdapter.py`。

下面用七个常见图/向量后端作架构级比较。结论是起点,不是替代压测的基准数字。

| 后端 | 类型 | 部署形态 | 主要优势 | 主要代价 | 推荐场景 |
|---|---|---|---|---|---|
| Ladybug / Kuzu | 图 | 嵌入式 | 默认、零外部服务、开发体验好 | 多进程共享文件需锁与生命周期管理 | 本地、单机、边缘 |
| Neo4j | 图 | 独立服务/托管 | 图生态成熟、运维工具丰富 | 新增服务与许可/容量规划 | 中大型知识图 |
| AWS Neptune | 图 | AWS 托管 | IAM、VPC 与托管运维 | 云绑定、成本及网络延迟 | AWS 生产环境 |
| PostgreSQL Graph | 图 | Postgres | 复用 SQL 运维体系 | 深图遍历需按真实负载验证 | Postgres 优先团队 |
| LanceDB | 向量 | 嵌入式 | 默认、轻量、无需服务 | 多实例共享与扩展需设计 | 开发与单机生产 |
| PGVector | 向量 | Postgres 扩展 | 事务、备份、监控体系统一 | 索引参数与资源竞争需调优 | 已有 Postgres 的生产系统 |
| Turso Vector | 向量 | libSQL/边缘 | 边缘友好、关系栈可协同 | 能力边界与延迟需验证 | 分布式边缘应用 |

ChromaDB、Qdrant、Weaviate、Milvus 可通过自定义或社区 `adapter` 接入公共向量接口(参考
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/create_vector_engine.py` 文档字符串,
链接到 cognee-community 仓库)。这里要区分两件事:LiteLLM 可统一 embedding 提供方调用;
向量库接入仍须实现并注册 `VectorDBInterface` 适配器,不能仅把 provider 名写入配置就获得支持。
工厂的扩展入口与内置 provider 分支见
`<COGNEE_REPO>/cognee/infrastructure/databases/vector/create_vector_engine.py`。

---

## 10.4 关系数据库: SQLite / Postgres / Turso

为什么关系层是控制面?Dataset、用户、权限和执行记录需要约束、事务及可迁移 schema,并不适合只存于
图或向量索引。默认 SQLite 让最小示例无需部署数据库;Postgres 适合多实例服务和生产并发;Turso
Relational 适合 libSQL 远端或边缘方案。

SQLite 与 Postgres 共用 SQLAlchemy 路径,核心实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/relational/sqlalchemy/SqlAlchemyAdapter.py`;
Turso 特化适配器见
`<COGNEE_REPO>/cognee/infrastructure/databases/relational/sqlalchemy/TursoAdapter.py`。关系 schema
迁移由 Alembic 管理,迁移目录为 `<COGNEE_REPO>/cognee/alembic/`。生产切换不是简单改 URL:
应先备份,在预发布库执行迁移,验证版本和回滚,再切换应用流量。图表和向量 collection 可能由各适配器
自行初始化,不要误认为 Alembic 会迁移整个三栈。

以下程序在默认栈上可直接运行,同时展示配置应在首次获取引擎、`add` 或 `cognify` 之前完成:

```python
import asyncio
import tempfile

import cognee


async def main():
    root = tempfile.mkdtemp(prefix="cognee-ch10-")
    cognee.config.system_root_directory(root)
    cognee.config.set_relational_db_config({"db_provider": "sqlite"})
    cognee.config.set_vector_db_provider("lancedb")
    cognee.config.set_graph_database_provider("ladybug")
    cognee.config.set_vector_db_subprocess_enabled(True)
    cognee.config.set_graph_database_subprocess_enabled(True)

    await cognee.add("Ladybug 保存实体关系,LanceDB 保存语义向量。")
    await cognee.cognify()
    results = await cognee.search("哪一层保存语义向量?", "GRAPH_COMPLETION")
    print(results)


asyncio.run(main())
```

---

## 10.5 Hybrid 一体化:Postgres / Neptune Analytics

为什么考虑 Hybrid(混合后端)?当图与向量位于同一引擎,系统可能减少网络往返、连接配置和跨库故障点。
Postgres Hybrid 组合 Postgres Graph 与 PGVector,并为联合 SQL 留出空间,实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/hybrid/postgres/adapter.py`。Neptune Analytics
同时实现图与向量接口,向量存储在图节点层,实现见
`<COGNEE_REPO>/cognee/infrastructure/databases/hybrid/neptune_analytics/NeptuneAnalyticsAdapter.py`。

一体化不意味着没有边界。Postgres 中图表、向量表和关系模型仍有不同 schema 与索引;Neptune Analytics
也有 Top-K、区域、凭证和服务能力限制。当前代码中的 Hybrid adapter 还不等于所有版本都提供稳定的
单一 `cognee.config` 开关;采用前应检查工厂实际 wiring,并以当前版本集成测试为准。保守做法是分别配置
Postgres Graph、PGVector 与关系 Postgres,先获得统一运维面,再评估启用联合能力。

下面是完整的 Postgres 三栈切换示例。它要求本机已有启用 `vector` 扩展的 Postgres、安装
`cognee[postgres]`,并设置真实密码;代码本身可直接执行。

```python
import asyncio
import os

import cognee


async def main():
    password = os.environ["COGNEE_DB_PASSWORD"]
    common = {
        "db_provider": "postgres",
        "db_host": "127.0.0.1",
        "db_port": "5432",
        "db_name": "cognee_db",
        "db_username": "cognee",
        "db_password": password,
    }
    cognee.config.set_relational_db_config(common)
    cognee.config.set_graph_db_config({
        "graph_database_provider": "postgres",
        "graph_database_host": "127.0.0.1",
        "graph_database_port": 5432,
        "graph_database_name": "cognee_db",
        "graph_database_username": "cognee",
        "graph_database_password": password,
        "graph_dataset_database_handler": "postgres_graph",
    })
    cognee.config.set_vector_db_config({
        "vector_db_provider": "pgvector",
        "vector_db_host": "127.0.0.1",
        "vector_db_port": 5432,
        "vector_db_name": "cognee_db",
        "vector_db_username": "cognee",
        "vector_db_password": password,
        "vector_dataset_database_handler": "pgvector",
        "vector_db_subprocess_enabled": False,
    })

    await cognee.add("Postgres 可以承载关系、图与向量三类持久化数据。")
    await cognee.cognify()
    print(await cognee.search("Postgres 承载哪些数据?", "HYBRID_COMPLETION"))


asyncio.run(main())
```

运行中切换已创建并缓存的引擎容易留下旧连接;生产上应把配置视为进程启动参数,完成迁移后滚动重启,
而不是在请求处理中反复切换。

---

## 10.6 Subprocess Mode

为什么图库和向量库默认运行在独立子进程?Ladybug/Kuzu 与 LanceDB 含原生资源、文件句柄和 WAL
(write-ahead log,预写日志)。把数据库生命周期隔离到 worker,可在关闭 worker 时可靠释放句柄并促使
WAL 正确 checkpoint,也避免长生命周期 API 进程积累原生内存。默认配置中
`graph_database_subprocess_enabled` 与 `vector_db_subprocess_enabled` 均为 `True`。

这并不是“并发共享同一文件”的许可证。多 worker、多 Pod 访问同一 Ladybug 路径时,仍需独占文件锁;
共享锁模式还依赖支持分布式锁的缓存后端。关闭 subprocess mode 只适合明确的单进程脚本、调试或经过
验证的生命周期模型。生产验收应包含:异常终止后重启、连续认知化、WAL 大小、checkpoint 后磁盘占用、
文件锁竞争和优雅停机。相关开关的公共实现见
`<COGNEE_REPO>/cognee/api/v1/config/config.py`。

---

## 10.7 SESSION_POSTGRES_CACHE_PLAN 与 SqlCacheAdapter

为什么会话缓存要单独讨论?它保存 QA 条目、Agent trace、usage log 和小型 KV,生命周期和一致性要求与
三栈主存储不同。设计计划
`<COGNEE_REPO>/SESSION_POSTGRES_CACHE_PLAN.md` 提出以 `CacheDBInterface` 增加 Postgres
后端,通过 `CACHE_BACKEND=postgres` 和 `CACHE_DB_URL` 接入,同时保留其它后端。

计划的关键点不是“第四层永久数据库”,而是把短期会话从 Redis 依赖中解耦:以 `expires_at` 实现滑动
TTL,读时过滤过期行,写时刷新会话 TTL,用 `FOR UPDATE` 保护 read-modify-write,并让 `prune()` 只清理
Cognee 自身 cache 表。计划还明确指出:关系库中的持久会话生命周期记录与 TTL cache 不设外键。

当前实现已经把计划落地。具体状态(对照 `<COGNEE_REPO>/cognee/infrastructure/databases/cache/`):

- `CacheConfig.cache_backend` 的 `Literal` 已扩展为 `("redis", "fs", "tapes", "sqlite", "postgres")`,
  默认值由计划里的 `"fs"` 改为 `"sqlite"`(`<COGNEE_REPO>/cognee/infrastructure/databases/cache/config.py`)。
- 工厂分支 `cache_backend in ("sqlite", "postgres")` 共用 `SqlCacheAdapter`,内部走
  `sqlalchemy.ext.asyncio.create_async_engine`,表结构由私有 `MetaData` 通过 `create_all(checkfirst=True)`
  在初始化时建好,**不走 Alembic**。这与计划中 PostgresCacheAdapter 的设计一致,
  适配器入口见
  `<COGNEE_REPO>/cognee/infrastructure/databases/cache/sql/SqlCacheAdapter.py`。
- `cache_db_url` 未设置时,`sqlite` 模式会写入 `<relational.db_path>/cache.db`,
  `postgres` 模式会自动回落到关系库 `DB_*` 配置(同库多表)。

架构师仍需注意:即便 SQL 后端已经可用,`SHARED_LADYBUG_LOCK` 的 Postgres advisory lock
仍属计划 Phase 6,目前并未落地;开启 Ladybug 共享锁仍应使用 Redis,或等待后续版本。

设置示例(需安装 `cognee[postgres]` 并配置好 `CACHE_DB_URL`):

```bash
export CACHE_BACKEND=postgres
export CACHE_DB_URL=postgresql+asyncpg://cognee:cognee@localhost:5432/cognee_db
```

---

## 10.8 选型决策

为什么先问约束而不是先问数据库品牌?存储方案的失败通常来自部署模型、并发和恢复目标不匹配。可按
下表从约束反推组合:

| 条件 | 关系层 | 向量层 | 图层 | 决策理由 |
|---|---|---|---|---|
| 本地开发、PoC、单机 | SQLite | LanceDB | Ladybug | 默认栈,最少依赖 |
| 单机生产且数据规模可控 | SQLite 或 Postgres | LanceDB | Ladybug | 简化运维,但必须演练备份和锁 |
| 多实例 API、团队熟悉 Postgres | Postgres | PGVector | PostgreSQL Graph 或 Neo4j | 事务与运维统一;深遍历需压测 |
| 图查询复杂、已有图平台团队 | Postgres | PGVector/LanceDB | Neo4j | 让专用图平台承担主要复杂度 |
| AWS 原生、要求 IAM/VPC | Postgres/RDS | PGVector 或 Neptune Analytics | Neptune/Neptune Analytics | 与云治理体系对齐 |
| 边缘/低延迟分布式节点 | Turso | Turso Vector | Turso Graph | 统一 libSQL 路线,先验证能力边界 |
| Dataset 需要物理隔离 | Postgres | PGVector 或独立实例 | Neo4j/Postgres/Ladybug 独立库 | 同时配置对应 Dataset DB Handler |

最终评审清单应包含六项:峰值写入量、向量规模与维度、图遍历深度、RPO/RTO、租户隔离级别、团队可
运维的服务数量。再以同一数据集运行 `add → cognify → search → delete` 回归,记录 P95 延迟、资源占用、
备份恢复时间和故障后的数据一致性。只有功能测试通过而没有恢复演练,不能算生产可用。

---

## 小结

- Cognee 以关系、向量、图三栈分别承载控制面、语义相似度和实体关系,公共接口隔离上层业务与厂商实现。
- 默认 SQLite + LanceDB + Ladybug 适合低门槛启动;多实例生产通常应评估 Postgres、PGVector 和托管图服务。
- Hybrid 能减少跨库往返,但不会消除 schema、索引、配额和版本 wiring 的验证工作。
- Subprocess Mode 负责隔离原生资源并保障 WAL checkpoint,不能替代跨进程锁和正确的部署拓扑。
- 选型必须用真实 workload、迁移与恢复演练验证,并同时考虑 Dataset DB Handler 和会话缓存。

## 实践作业

1. **(基础)** 运行 10.4 的默认栈示例,确认关系、向量、图目录均生成,再执行一次检索。
2. **(进阶)** 在测试 Postgres 上运行 10.5 示例,记录默认栈与 Postgres 三栈的认知化和检索 P95 延迟,
   并完成一次备份恢复。
3. **(挑战)** 为 ChromaDB、Qdrant、Weaviate 或 Milvus 实现一个最小 `VectorDBInterface` adapter,
   注册到向量工厂,补齐 collection、写入、search、delete 和 prune 的契约测试。

## 推荐阅读

- 可观测性:详见 [[chapter-11-observability|第 11 章 可观测性与追踪:OpenTelemetry / Langfuse / Trace]](./chapter-11-observability.md)
- 图工厂:`<COGNEE_REPO>/cognee/infrastructure/databases/graph/get_graph_engine.py`
- 向量工厂:`<COGNEE_REPO>/cognee/infrastructure/databases/vector/get_vector_engine.py`
- Dataset 隔离:`<COGNEE_REPO>/cognee/infrastructure/databases/dataset_database_handler/`
- Postgres 会话缓存计划:`<COGNEE_REPO>/SESSION_POSTGRES_CACHE_PLAN.md`

## 下一章预告

第 11 章将介绍检索与搜索架构,说明三栈中的数据如何被组织为不同 `SearchType` 的上下文。
