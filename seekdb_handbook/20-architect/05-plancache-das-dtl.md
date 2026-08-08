# 2.5 计划缓存与执行框架：DAS / DTL / PX

> **一句话**：计划缓存省掉重复的解析优化；DAS 把"怎么访问数据"从算子树里剥离；
> DTL 负责并行执行时的数据搬运。

---

## 计划缓存

### 为什么需要

解析 + 优化一条复杂 SQL 可能耗时毫秒级，而执行只要微秒级。
OLTP 场景同一条 SQL 反复执行，每次重新优化是巨大浪费。

### 两层缓存

| 缓存 | 类 | 键 | 位置 |
|---|---|---|---|
| SQL 计划缓存 | `ObPlanCache` | 参数化后的 SQL 文本 | `src/sql/plan_cache/ob_plan_cache.cpp` |
| 预处理语句缓存 | `ObPsCache` | `stmt_id` | `src/sql/plan_cache/ob_ps_cache.cpp` |

### 参数化：命中的前提

```sql
SELECT * FROM t WHERE id = 42;
SELECT * FROM t WHERE id = 99;
```

这两条如果按原文做键，永远不会互相命中。
`ObSqlParameterization`（`ob_sql_parameterization.cpp`）把字面量替换成 `?`：

```sql
SELECT * FROM t WHERE id = ?;
```

于是共用一个计划。配合 [2.3](03-select-lifecycle-1.md) 提到的
`ObFastParser`（SIMD 加速），高频 SQL 可以极快地走到缓存。

### 一个 SQL 可能有多个计划

`ObPCVSet` / `ObPlanSet`（`ob_pcv_set.cpp` / `ob_plan_set.cpp`）：
同一条参数化 SQL，不同的参数**值**可能需要不同计划。

比如 `WHERE status = ?`：
`status='deleted'` 命中 1% 的行（该走索引），
`status='active'` 命中 90%（该全表扫）。
所以一个 SQL 键下会挂多个计划，按参数特征选。

### 失效

schema 变更时 `ObPlanCacheCallback` 会让相关计划失效。

> ⚠️ 这里有个已知缺口：AI 函数（`AI_EMBED` 等）与计划缓存的
> schema 版本匹配**尚未实现**，源码里有明确的
> `// TODO: support schema version match in plan cache for ai func`
> （`src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:159`）。
> 如果你修改了 AI 模型 endpoint 的配置，可能需要手动清计划缓存。

### 观察

```sql
select * from oceanbase.__all_virtual_plan_cache_stat;
```

---

## DAS：数据访问服务

`src/sql/das/`（约 52 个文件）。

### 它解决什么问题

朴素做法是让 `ObTableScanOp` 直接调存储接口。
但这样一来，"重试""跨节点""索引回表""事务挂钩"这些逻辑
就全糊在算子里了。

DAS（Data Access Service）把**数据访问**抽象成独立的一层任务：

```
ObTableScanOp（算子）
    ↓ 提交任务
ObDASScanOp（DAS 任务）
    ↓
storage::ObTableScanIterator
```

### 任务类型

全部继承 `ObIDASTaskOp`：

| 类 | 用途 |
|---|---|
| `ObDASScanOp` | 表 / 索引扫描 |
| `ObDASInsertOp` / `ObDASUpdateOp` / `ObDASDeleteOp` | DML |
| `ObDASLockOp` | 加锁 |
| `ObDASIndexLookupOp` | 索引回表 |
| `ObDASDomainOp` | 域索引（全文 / 向量） |

### 迭代器体系

`src/sql/das/iter/` 是理解向量与全文检索的关键入口：

| 迭代器 | 用途 |
|---|---|
| `ObDASScanIter` | 基础扫描 |
| `ObDASMergeIter` | 多路归并 |
| `ObDASLookupIter` | 回表 |
| **`ObDASHNSWScanIter`** | **HNSW 向量检索** |
| **`ObDASIvfScanIter`** 系列 | **IVF 向量检索** |
| **`ObDASTRMergeIter`** | **全文检索归并** |
| **`ObDASMatchIter`** | **MATCH AGAINST top-k** |

seekdb 的向量和全文能力，在执行层就是**这些迭代器**。
它们被组织成 `ObDASIterTree`，一棵迭代器树对应一个复杂的访问计划。

---

## DTL：数据传输层

`src/sql/dtl/`（约 44 个文件）。

并行执行时，数据要在不同线程/DFO 之间流动。DTL 提供这条管道。

| 组件 | 作用 |
|---|---|
| `ObDtlChannel` | 通道抽象 |
| `ObDtlLocalChannel` | 进程内通道（seekdb 单机主要走这个） |
| `ObDtlLinkedBuffer` | 缓冲区管理 |
| `ObDtlChannelLoop` | 事件循环 |
| `ObDtlFlowControl` / `ObDtlFcServer` | **流控**：防止上游打爆下游 |
| `ObDtlIntermResultManager` | 中间结果共享 |

对应的算子：

| 算子 | 作用 |
|---|---|
| `ObPxTransmitOp` | 发送端 |
| `ObPxReceiveOp` | 接收端 |
| `ObPxFifoReceiveOp` | FIFO 接收 |
| `ObPxRepartTransmitOp` | 重分区发送 |

流控是这里最值得注意的设计——没有它，
一个快速的扫描算子会把内存打爆。

---

## PX：并行执行

即使单机，seekdb 也能并行执行查询（多线程）。

- `ObPxPool` —— PX 专用线程池
- DFO（Data Flow Object）—— 并行执行的调度单元
- `ObAdaptiveAutoDop` —— 自动决定并行度
- 优化器阶段的 `ALLOC_GI`（granule iterator）负责切分数据

单机并行的收益在分析型查询上很明显；
OLTP 短查询通常不并行（并行本身有开销）。

---

## 三者怎么配合

```
ObOperator 树
   │
   ├── ObTableScanOp ──→ DAS ──→ storage
   │                      └─ ObDASHNSWScanIter（向量）
   │                      └─ ObDASTRMergeIter（全文）
   │
   └── ObPxTransmitOp ──→ DTL ──→ ObPxReceiveOp
                          （流控 + 缓冲）
```

- **DAS** 管"纵向"：算子 → 存储
- **DTL** 管"横向"：算子 ↔ 算子（跨线程）
- **计划缓存** 管"时间"：这次 → 下次

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `src/sql/plan_cache/ob_plan_cache.cpp` | `ObPlanCache` |
| `src/sql/plan_cache/ob_ps_cache.cpp` | `ObPsCache` |
| `src/sql/plan_cache/ob_sql_parameterization.cpp` | 参数化 |
| `src/sql/plan_cache/ob_pcv_set.cpp` / `ob_plan_set.cpp` | 多计划管理 |
| `src/sql/das/ob_data_access_service.cpp` | `ObDataAccessService` |
| `src/sql/das/ob_das_scan_op.cpp` | `ObDASScanOp` |
| `src/sql/das/iter/ob_das_hnsw_scan_iter.h` | HNSW 迭代器 |
| `src/sql/das/iter/ob_das_ivf_scan_iter.h` | IVF 迭代器 |
| `src/sql/das/iter/sparse_retrieval/ob_das_tr_merge_iter.h` | 全文归并 |
| `src/sql/das/ob_das_vec_define.h` | 向量执行策略 |
| `src/sql/das/ob_das_ir_define.h` | 全文检索定义 |
| `src/sql/dtl/ob_dtl_channel.cpp` | DTL 通道 |
| `src/sql/dtl/ob_dtl_flow_control.cpp` | 流控 |
| `src/sql/dtl/ob_dtl_interm_result_manager.cpp` | 中间结果 |
| `src/sql/engine/px/` | PX 算子 |

---

## 动手验证

看 DAS 迭代器全集（向量/全文能力的执行层入口）：

```bash
ls src/sql/das/iter/
ls src/sql/das/iter/sparse_retrieval/
```

看计划缓存状态：

```sql
select * from oceanbase.__all_virtual_plan_cache_stat;
```

确认 AI 函数的计划缓存 TODO：

```bash
sed -n '154,190p' src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp
```

---

## 延伸阅读

- 下一章：[2.6 一行数据的一生：LSM-Tree](06-lsm-tree.md)
- [2.10 向量索引架构](10-vector-index.md) —— `ObDASHNSWScanIter` 的内部状态机
- [2.12 混合检索的算子融合](12-hybrid-search-internals.md)
