# 2.4 一条 SELECT 的一生（下）：优化到执行

> **一句话**：`ObSelectStmt` 经过改写、优化、代码生成，
> 变成一棵 `ObOperator` 树；执行时按**批**（而非按行）向上吐数据。

---

## 第 6 站：改写（Rewrite）

`src/sql/rewrite/`（约 98 个文件）。

改写是**等价变换**：不改变语义，但让优化器更容易找到好计划。
典型规则：

| 变换 | 效果 |
|---|---|
| 子查询展开 | `WHERE x IN (SELECT ...)` → semi join |
| 视图合并 | 消除中间视图层 |
| 谓词下推 | 过滤条件尽早执行 |
| OR 展开 | `a=1 OR a=2` → union |
| 常量折叠 | 编译期算掉常量表达式 |
| 外连接消除 | 能证明不产生 NULL 时降级为内连接 |
| 晚期物化 | `ob_transform_late_materialization.cpp`，先取主键再回表 |

> 💡 晚期物化对向量场景有特殊处理——
> 文件里专门 case 了 `INDEX_TYPE_HEAP_ORGANIZED_TABLE_PRIMARY`。

---

## 第 7 站：优化（Optimize）

`src/sql/optimizer/`（约 147 个文件），seekdb 最复杂的模块之一。

入口：

```
ObOptimizer::optimize(stmt, plan)        src/sql/optimizer/ob_optimizer.h:187
  → ObLogPlan::generate_plan()           src/sql/optimizer/ob_log_plan.cpp:10317
```

### 核心问题：选哪条路

优化器要决定：
- 每张表走全表扫描还是索引？走哪个索引？
- 多表 join 的顺序？用 hash join / merge join / nested loop？
- 要不要并行？并行度多少？
- 数据怎么分布？

`ObJoinOrder`（`ob_join_order.h:1307`）负责枚举 join 顺序，
维护 `interesting_paths`（有价值的访问路径）。
代价估算靠统计信息（`ObOptStat`）和动态采样
（`ObAccessPathEstimation`）。

### 计划后处理：18 个 pass

`generate_plan` 之后有一长串遍历阶段，每个做一件事：

```
ALLOC_EXPR                 分配表达式
PROJECT_PRUNING            裁掉用不到的列
OPERATOR_NUMBERING         算子编号
EXCHANGE_NUMBERING         交换算子编号
GEN_SIGNATURE              生成计划签名
GEN_LOCATION_CONSTRAINT    位置约束
EXTRACT_PARAMS_FOR_SUBPLAN 子计划参数抽取
ALLOC_GI                   分配 granule iterator（并行）
PX_PIPE_BLOCKING           并行流水线阻塞点
PX_RESCAN / PX_ESTIMATE_SIZE
RUNTIME_FILTER             运行时过滤器
ALLOC_STARTUP_EXPR
ADJUST_SHARED_EXPR         共享表达式调整
COLLECT_BATCH_EXEC_PARAM
ALLOC_OP                   分配算子
ADJUST_SCAN_DIRECTION      调整扫描方向
```

看到这个列表就明白：**逻辑计划 ≠ 物理计划**，中间有大量精细加工。

### 向量索引在优化器里的位置

向量扫描的代价估算在
`src/sql/optimizer/ob_opt_est_cost_model.cpp`（约 1435 行）
和 `ob_log_table_scan.cpp`。

优化器要在 5 种向量执行策略里选一种
（`ObVecIndexType`，见 [1.3 混合检索](../10-user/03-hybrid-search.md)）——
关键是判断标量过滤的选择性，决定"先过滤还是先 ANN"。

---

## 第 8 站：代码生成（Code Generation）

`ObStaticEngineCG::generate(log_plan, phy_plan)`
（`src/sql/code_generator/ob_static_engine_cg.cpp`）。

把逻辑算子树编译成物理执行结构：

| 逻辑 | 物理 |
|---|---|
| `ObLogTableScan` | `ObTableScanSpec` |
| `ObLogJoin` | `ObHashJoinSpec` / `ObMergeJoinSpec` / `ObNestedLoopJoinSpec` |
| `ObLogGroupBy` | `ObHashGroupBySpec` / `ObMergeGroupBySpec` |
| `ObRawExpr` | `ObExpr`（挂上 `eval_func_`） |

辅助类：`ObDMLCGService`（DML 相关）、`ObTSCCGService`（表扫描相关）。

`ObOpSpec` 是**只读的**算子规格——可以放进计划缓存被多个会话共享。
执行时再按 spec 创建有状态的 `ObOperator`。

这个 spec / operator 分离是计划缓存能工作的前提。

---

## 第 9 站：执行

### 向量化：按批处理

seekdb 的执行引擎是**向量化**的——算子之间传递的不是一行，而是一批：

```cpp
virtual int inner_get_next_rows(int64_t &count, int64_t capacity);
```

关键类型：

| 类型 | 位置 | 作用 |
|---|---|---|
| `ObBatchRows` | `src/sql/engine/ob_batch_rows.h:30` | `skip_` 位图 + `size_` + `all_rows_active_` |
| `ObDatum` | `src/sql/engine/expr/ob_datum.h` | 扁平的定长值，没有 `ObObj` 的头部开销 |
| `ObEvalCtx` | `src/sql/engine/expr/ob_expr.h:152` | 求值上下文：`batch_idx_`、`batch_size_`、frames |
| `ObExpr` | `src/sql/engine/expr/ob_expr.cpp:247` | 带 `eval_func_` / `eval_batch_func_` |

**`skip_` 位图**是向量化过滤的核心技巧：
过滤不是真的删除行，而是在位图里标记"这行跳过"。
后续算子看位图决定处理哪些行——避免了数据搬移。

### 表达式求值

```cpp
// 单行
rt_expr.eval_func_(expr, ctx, datum);
// 一批
rt_expr.eval_batch_func_(expr, ctx, skip, size);
```

一个表达式实现两个函数，向量化路径能显著减少函数调用开销。
（写新函数时至少要实现 `eval_func_`，见
[3.6 实战一](../30-developer/06-hands-on-sql-function.md)。）

### 存储访问

`ObTableScanOp`（`src/sql/engine/table/ob_table_scan_op.cpp`）
不直接读存储，而是通过 DAS：

```
ObTableScanOp → ObDASScanOp → storage::ObTableScanIterator
                              → access → memtable + blocksstable
```

DAS 的意义见 [2.5](05-plancache-das-dtl.md)。

---

## 第 10 站：回包

`ObMPPacketSender`（`src/observer/mysql/obmp_packet_sender.cpp`）
把结果按 MySQL 协议编码写回。

`ObResultSet`（`src/sql/ob_result_set.cpp`）代表一次查询的执行实例，
持有物理计划和执行上下文。

---

## 完整链路回顾

```
ObSelectStmt                       [上篇产物]
  → rewrite/          等价变换
  → ObOptimizer::optimize
      → ObLogPlan::generate_plan   逻辑计划 + 18 个后处理 pass
  → ObStaticEngineCG::generate     ObOpSpec 树 + ObExpr
  → 存入 ObPlanCache
  → ObOperator 树执行
      inner_get_next_rows(count, capacity)   按批
      ├─ ObTableScanOp → DAS → storage
      ├─ ObHashJoinSpec / ObGroupBySpec / ...
      └─ ObExpr::eval_batch_func → ObEvalCtx
  → ObMPPacketSender                回包
```

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/sql/rewrite/` | 改写规则（~98 文件） |
| `src/sql/rewrite/ob_transform_late_materialization.cpp` | 晚期物化，含 HEAP 表特判 |
| `src/sql/optimizer/ob_optimizer.h:187` | `ObOptimizer::optimize` |
| `src/sql/optimizer/ob_log_plan.cpp:10317` | `ObLogPlan::generate_plan` |
| `src/sql/optimizer/ob_join_order.h:1307` | `ObJoinOrder` |
| `src/sql/optimizer/ob_opt_est_cost_model.cpp` | 代价模型，含向量扫描 |
| `src/sql/code_generator/ob_static_engine_cg.cpp` | 代码生成 |
| `src/sql/engine/ob_operator.cpp` | `ObOperator` / `ObOpSpec` |
| `src/sql/engine/ob_operator_factory.h:35` | 算子工厂 |
| `src/sql/engine/ob_batch_rows.h:30` | `ObBatchRows` |
| `src/sql/engine/expr/ob_expr.h:152` | `ObEvalCtx` |
| `src/sql/engine/expr/ob_expr.cpp:247` | `ObExpr` |
| `src/sql/engine/table/ob_table_scan_op.cpp` | 表扫描算子 |
| `src/sql/ob_result_set.cpp` | `ObResultSet` |
| `src/observer/mysql/obmp_packet_sender.cpp` | 回包 |

---

## 动手验证

看优化器后处理的 pass 列表：

```bash
grep -n "ALLOC_EXPR\|PROJECT_PRUNING\|OPERATOR_NUMBERING\|ALLOC_OP" src/sql/optimizer/ob_log_plan.h | head
```

看向量化批的结构：

```bash
sed -n '25,60p' src/sql/engine/ob_batch_rows.h
```

看有多少种物理算子：

```bash
ls src/sql/engine/*/ | grep -c "_op\.h"
```

用 EXPLAIN 观察真实计划（需要运行中的实例）：

```sql
EXPLAIN SELECT * FROM t1 ORDER BY l2_distance(c3, '[1,2,3]') APPROXIMATE LIMIT 10;
```

---

## 延伸阅读

- 下一章：[2.5 计划缓存与执行框架](05-plancache-das-dtl.md)
- [3.6 实战一：新增 SQL 函数](../30-developer/06-hands-on-sql-function.md) —— 表达式怎么接进这套体系
- [2.10 向量索引架构](10-vector-index.md) —— 向量扫描算子的内部
