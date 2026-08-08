# 0.1 seekdb 是什么：从 OceanBase 到 Agent 状态存储

> **一句话**：seekdb 是把 OceanBase 的分布式数据库内核裁剪成单机/嵌入式形态，
> 再叠加向量索引、异步索引管线、COW 沙箱和库内 AI 调用，专门服务 AI Agent 的状态存储。

---

## 为什么需要它：Agent 的负载和传统数据库不一样

一个 AI Agent 的主循环长这样：

```
观察 → 写入记忆 → 几毫秒后检索相关上下文 → 决策 → 行动 → 观察 → ...
```

这个循环对存储系统提出了四个组合起来很少见的要求：

| 要求 | 传统方案的问题 |
|---|---|
| **持续写 + 立刻读** | 向量数据库通常批量建索引，新写入要等下一轮 rebuild 才可检索 |
| **能分叉、能回滚** | Agent 试错需要沙箱；应用层做 save/restore 既慢又容易漏状态 |
| **向量 + 全文 + 标量一起查** | 分别存在向量库和搜索引擎里，客户端做 N+1 合并 |
| **事务与一致性** | 纯向量库大多没有 ACID，Agent 的业务状态没法放心存 |

seekdb 的设计出发点，就是把这四件事放进**同一个**引擎里。

---

## 它从哪来：OceanBase 的血统

seekdb 不是从零写的。打开 `CMakeLists.txt` 第一眼就能看到：

```cmake
project(OceanBase VERSION 1.3.0.0 LANGUAGES CXX C ASM)
```

命名空间是 `oceanbase::`，类名以 `Ob` 开头，错误码是 `OB_SUCCESS`。
这意味着你**白拿**了一整套生产级数据库能力：

- MySQL 协议兼容 —— 整个 MySQL 生态的驱动、ORM、BI 工具直接可用
- 完整 ACID 事务 + MVCC 快照读
- LSM-Tree 存储引擎，读写分离、行列混存
- 成熟的 SQL 优化器（代价模型、join 重排、计划缓存）

代价是：这也意味着你要面对一个**为分布式集群设计**的代码库。
seekdb 做了大量裁剪，其中最激进的一刀是**整体移除多租户框架**
（详见 [2.2 seekdb 裁掉了什么](../20-architect/02-what-seekdb-removed.md)）。

---

## 它加了什么：四块 AI-native 能力

这是 seekdb 区别于"OceanBase 单机版"的全部理由。

### 1. 向量索引 + Change Stream 异步管线

写入路径**不碰索引**：事务提交只写 redo 日志就返回。
一条独立的 Change Stream 管线异步消费日志，更新内存中的增量 HNSW。
查询永远只命中**两个**索引——增量（delta）+ 快照（snapshot）。

索引数量恒定为 2，是官方博客解释 P99 平稳的核心论据。

- 源码：`src/observer/change_stream/`、`src/observer/vector_index/`
- 详见 [2.10 向量索引架构](../20-architect/10-vector-index.md)、
  [2.11 Change Stream](../20-architect/11-change-stream.md)

### 2. FORK / MERGE 的 COW 沙箱

```sql
FORK DATABASE agent_state TO agent_sandbox_42;
-- Agent 在沙箱里随便折腾
MERGE TABLE agent_sandbox_42.memory INTO agent_state.memory STRATEGY THEIRS;
-- 或者直接丢弃
DROP DATABASE agent_sandbox_42;
```

关键在于**不拷贝数据**：fork 只记录一个快照版本号，
后续按该版本号扫描源 tablet 的多版本 SSTable。

- 源码：`src/rootserver/fork_table/`、`src/storage/ddl/ob_tablet_fork_task.cpp`
- 详见 [2.13 FORK/MERGE 的 COW 实现](../20-architect/13-fork-merge-cow.md)

### 3. 混合检索：一条 SQL 打通三种召回

向量相似度、全文匹配、标量过滤在**同一个执行计划**里完成，
融合方式支持加权求和与 RRF（Reciprocal Rank Fusion）。

- 源码：`src/sql/hybrid_search/`、`src/storage/retrieval/`
- 详见 [2.12 混合检索的算子融合](../20-architect/12-hybrid-search-internals.md)

### 4. 库内 AI 函数

这是 README **完全没提**、但可能最有意思的一块：
seekdb 可以在 SQL 里直接调用外部模型服务。

```sql
SELECT AI_EMBED('my_embedding_model', content) FROM docs;
```

四个函数——`AI_EMBED`、`AI_COMPLETE`、`AI_RERANK`、`AI_PROMPT`——
底层通过 libcurl 直连模型 endpoint。

- 源码：`src/sql/engine/expr/ob_expr_ai/`、`src/observer/ai_service/`
- 详见 [1.5 库内 AI 函数](../10-user/05-in-db-ai.md)、
  [2.14 库内 AI Service 架构](../20-architect/14-ai-service.md)

---

## 代码锚点

| 位置 | 职责 |
|---|---|
| `CMakeLists.txt` | 工程根，声明 `project(OceanBase VERSION 1.3.0.0)` |
| `README.md` | 官方能力介绍与性能宣称 |
| `docs/blog/launch_blog_en.md` | 官方架构解读（两级索引、流式基准） |
| `src/observer/change_stream/` | 异步索引管线 |
| `src/observer/vector_index/` | 向量索引插件适配、调度、IVF、KMeans |
| `src/storage/vector_index/` | 向量索引刷新与调度作业 |
| `src/rootserver/fork_table/` | FORK DATABASE / TABLE 服务 |
| `src/sql/hybrid_search/` | 混合检索 JSON DSL 解析与翻译 |
| `src/sql/engine/expr/ob_expr_ai/` | AI_EMBED / AI_COMPLETE / AI_RERANK / AI_PROMPT |
| `src/observer/ai_service/` | AI 模型 endpoint 的增删改查 |

---

## 关于官方性能数据

README 首屏的宣称是：

> 1,523 QPS streaming write+search（10.7× Milvus，3.2× Elasticsearch），
> 并发 P99 21.7 ms，压力上升时 P99 抖动仅 1.1×。

这些数字来自官方在 VectorDBBench StreamingPerformanceCase（Cohere 10M / 768 维，
16 vCPU / 64 GiB）上的测试，复现脚本在
[vdb-streambench](https://github.com/oceanbase/vdb-streambench)。

**本书不复现、也不背书这些数字。** 本书关心的是另一个问题：
*架构上什么设计让这个结果成为可能* —— 那是
[2.11 Change Stream](../20-architect/11-change-stream.md) 的内容。

---

## 延伸阅读

- 下一章：[0.2 三种形态](02-three-modes.md) —— 嵌入式、单机、集群怎么选
- [0.3 代码地图](03-code-map.md) —— 1GB 仓库的导航图
- 官方博客：`docs/blog/launch_blog_zh.md`（中文版）
