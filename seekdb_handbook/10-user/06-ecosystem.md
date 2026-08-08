# 1.6 生态集成

> **一句话**：seekdb 说 MySQL 协议，所以整个 MySQL 生态直接可用；
> AI 框架侧则通过 OceanBase 的官方 connector 接入。

---

## 为什么"兼容 MySQL 协议"是最大的集成优势

向量数据库通常有自己的私有协议和 SDK，这意味着：
每接一个框架就要等对方写一个 connector，出问题也难排查。

seekdb 走的是另一条路——**它就是一个 MySQL**。
任何能连 MySQL 的东西都能连它：

| 类别 | 例子 |
|---|---|
| 驱动 | `mysqlclient`、`PyMySQL`、JDBC、Go `go-sql-driver/mysql`、Node `mysql2` |
| ORM | SQLAlchemy、Django ORM、MyBatis、GORM、Prisma |
| 客户端 | `mysql` CLI、`obclient`、DBeaver、Navicat、TablePlus |
| BI / ETL | 任何支持 MySQL 数据源的工具 |

```bash
mysql -h127.0.0.1 -P2881 -uroot
```

这条命令能用，意味着你现有的运维习惯、监控、备份思路大部分可以复用。

---

## AI 框架集成

README 列出的已集成框架（徽章链接均指向对应仓库的 oceanbase 相关 PR）：

| 框架 | 说明 |
|---|---|
| **LangChain** | VectorStore 集成 |
| **LangGraph** | Agent 状态存储 |
| **LlamaIndex** | 向量索引后端 |
| **Dify** | 向量数据库选项 |
| **Coze** | 知识库后端 |
| **HuggingFace** | 数据集/模型生态 |

README 还提到：Camel-AI、DB-GPT、FastGPT、Firecrawl、
Spring-AI-Alibaba、Cloudflare Workers AI、Jina AI、Ragas、Instructor、Baseten。

> ⚠️ 这些集成的代码**不在本仓库内**，位于各自框架的上游仓库。
> 集成成熟度、版本兼容性请以对应框架的文档为准。
> 本书不对这些集成做验证。

---

## Python SDK：pyseekdb

```bash
pip install -U pyseekdb
```

`pyseekdb` 提供的是 Chroma 风格的 collection API：

```python
import pyseekdb
client = pyseekdb.Client(path="./agent_state.db")
memory = client.get_or_create_collection(name="episodic")
memory.upsert(ids=[...], documents=[...])
results = memory.query(query_texts="...", n_results=5)
```

源码在 [github.com/oceanbase/pyseekdb](https://github.com/oceanbase/pyseekdb)，
**不在本仓库**。完整用法见其 User Guide。

### 什么时候用 SDK，什么时候直接写 SQL

| 场景 | 建议 |
|---|---|
| 快速原型、简单的存取与检索 | pyseekdb（自动处理 embedding、schema） |
| 需要精细控制索引参数、混合检索、事务 | 直接写 SQL（用任意 MySQL 驱动） |
| 已有 SQLAlchemy / ORM 代码库 | 直接用 ORM，把 seekdb 当 MySQL |

两者可以混用——SDK 建的表就是普通表，SQL 照样能查。

---

## 仓库内的客户端相关代码

虽然 SDK 在外部，仓库里有几处与客户端交互相关：

| 位置 | 说明 |
|---|---|
| `src/observer/mysql/` | MySQL 协议服务端实现，`ObMP*` 系列命令处理器 |
| `deps/oblib/src/rpc/obmysql/` | 协议包结构（`ObMySQLPacket`、`ObMySQLRow`） |
| `rust/sql-nio/` | Rust 重写的网络引擎（见下） |

### `rust/sql-nio`：一个正在进行时的重写

`rust/sql-nio/Cargo.toml` 里的自述是：

> Rust reimplementation of seekdb's ObSqlNioImpl network engine,
> exposed over a C ABI.

它是一个 staticlib（`libsql_nio.a`），用 `mio` 做跨平台事件循环
（epoll / kqueue / IOCP），`flate2` 做协议压缩，涵盖握手、登录、
命令分发、结果编码、预处理语句、TLS 等模块。

CI 里有独立的检查流水线（`.github/workflows/rust-checks.yml`，
clippy `-D warnings` + RustSec 审计）。

> 💡 对使用者而言这暂时没有影响——C++ 路径仍在服务。
> 但它说明 seekdb 在网络层有长期演进计划，值得关注。

---

## 代码锚点

| 位置 | 职责 |
|---|---|
| `src/observer/mysql/obmp_*.cpp` | 各 MySQL 命令的处理器 |
| `src/observer/ob_srv_xlator.cpp` | 按 pcode 分发到 `ObMP*` |
| `deps/oblib/src/rpc/obmysql/ob_mysql_packet.h` | 协议包结构 |
| `rust/sql-nio/` | Rust 网络引擎（`reactor.rs`、`codec.rs`、`handshake.rs` 等） |
| `rust/Cargo.toml` | workspace 定义 |
| `.github/workflows/rust-checks.yml` | Rust 侧 CI |
| `README.md` | 生态集成清单 |

---

## 动手验证

看服务端支持哪些 MySQL 命令：

```bash
ls src/observer/mysql/obmp_*.h | sed 's|.*/obmp_||;s|\.h||'
```

看 Rust 网络引擎的模块构成：

```bash
ls rust/sql-nio/src/
```

---

## 延伸阅读

- 下一章：[1.7 部署与配置](07-deploy-config.md)
- [2.3 一条 SELECT 的一生（上）](../20-architect/03-select-lifecycle-1.md) —— 协议层怎么工作
