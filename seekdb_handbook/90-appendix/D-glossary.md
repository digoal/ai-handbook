# 附录 D · 术语表

> seekdb / OceanBase 有大量自造术语。这里按主题归类，
> 每条给出"是什么 + 在哪看"。

---

## 架构与进程

**observer / seekdb**
　数据库服务进程。二进制名是 `seekdb`，但代码里大量沿用 `observer` 命名
（目录 `src/observer/`、构建产物路径）。

**MTL（Multi-Tenant Library）**
　OceanBase 的多租户框架。**seekdb 已整体移除**，`src/` 中 `MTL_` 出现 0 次。
见 [2.2](../20-architect/02-what-seekdb-removed.md)。

**`g_mp` / ObIModuleProvider**
　⭐ 全局模块提供者。低层代码通过它访问高层模块，避免反向依赖。
`src/share/rc/ob_module_provider.h:214`。

**GCTX**
　全局上下文（`ObServerStruct`），存放 `is_embedded_mode()` 等进程级状态。

**omt**
　目录名，原意 OceanBase Multi-Tenant。seekdb 单租户后名字是历史遗留，
里面装的是 `ObServerRuntime`（服务运行时）。

**module layering DAG**
　⭐ 模块分层有向无环图。`cmake/module_check/module_layers.conf` 定义，
CI 强制执行，违反则构建失败。

---

## 存储

**LS（Log Stream，日志流）**
　复制与日志的组织单元，包含一组 tablet。类 `ObLS`。

**Tablet**
　表的一个分区，数据组织的基本单元。类 `ObTablet`。

**MemTable**
　内存中的写入缓冲，按 rowkey 组织成 MVCC 链表。

**SSTable**
　磁盘上的有序数据文件。分 Minor（转储产物）和 Major（合并产物）。

**转储 / Mini Merge**
　冻结的 MemTable 写成 Minor SSTable。

**合并 / Major Compaction**
　多个 Minor SSTable 合并成一个 Major SSTable。

**宏块（Macro Block）**
　磁盘 IO 与空间分配单位，典型 2MB。

**微块（Micro Block）**
　压缩与缓存单位，16-64KB。读一行只需解压所在微块。

**SCN（System Change Number）**
　全局单调递增的版本号/时间戳。`src/share/scn.h`。

**MDS（Multi-Data-Source）**
　多源数据机制，用于非行数据的元信息变更（如 DDL 提交版本）。

**palf**
　Paxos-backed Append-only Log File system，OceanBase 的日志库。
seekdb 单副本运行。

**Apply vs Replay**
　Apply = 日志提交后的回调；Replay = 重启后按日志重建状态。两者不同。

---

## 事务

**MVCC**
　多版本并发控制。每行是一条 `ObMvccTransNode` 链表。

**`trans_version_` vs `scn_`**
　⭐ 易混：`scn_` 是**写入**时的日志序号；
`trans_version_` 是**提交**版本，写入时为 `min_scn()`，提交时回填。
可见性判据是后者。

**GTS（Global Timestamp Service）**
　全局时间戳服务，提供提交版本号。`ObTimestampService`。

**快照读**
　按一个版本号读取，跳过 `trans_version_` 大于该版本的节点。

**tx_table**
　持久化事务提交信息的表。SSTable 里可能有未提交数据，靠它判定可见性。

---

## SQL 引擎

**resolver**
　把语法树（`ParseNode`）转成语义树（`ObSelectStmt`）的组件。

**`ObRawExpr` vs `ObExpr`**
　⭐ 易混：前者是解析/优化期表达式（树，带类型信息）；
后者是执行期表达式（扁平，带函数指针）。代码生成负责转换。

**DAS（Data Access Service）**
　数据访问服务，把"怎么访问数据"从算子里剥离。`src/sql/das/`。

**DTL（Data Transfer Layer）**
　数据传输层，并行执行时的数据搬运通道。`src/sql/dtl/`。

**PX（Parallel eXecution）**
　并行执行框架。

**DFO（Data Flow Object）**
　并行执行的调度单元。

**unity build**
　把多个 `.cpp` 合并编译以加速。副作用是报错位置不准，
调试用 `debug_no_unity`。

**向量化执行**
　算子间传递一批行（`ObBatchRows`）而非单行。
注意：**和"向量检索"完全是两回事**，中文都叫"向量"容易混。

**`skip_` 位图**
　向量化过滤的实现：不删除行，只在位图里标记跳过。

---

## ⭐ 向量检索

**HNSW**
　Hierarchical Navigable Small World，一种图结构的近似最近邻索引。

**两级 HNSW / delta + snapshot**
　⭐ seekdb 的核心设计：增量索引（`incr_data_`）+ 快照索引（`snap_data_`）。
查询查两个再归并。索引数量恒定为 2。

**incr / delta**
　同一个东西。源码叫 `incr_data_`，博客叫 delta。

**vid（Vector ID）**
　向量的整数标识。HNSW 内部用整数，表主键可能是任意类型，故需双向映射表。

**VSAG**
　⭐ 外部向量索引库，seekdb 的默认底层实现（`lib=vsag`）。
**不在本仓库**，是 `deps/init/*.deps` 拉取的依赖。

**IVF（Inverted File）**
　另一族向量索引：先 KMeans 聚类，查询时只搜最近的几个簇。
变体 `ivf_flat` / `ivf_sq8` / `ivf_pq`。

**SQ / PQ / BQ**
　标量量化 / 乘积量化 / 二值量化——压缩向量以省内存的手段。

**SPIV**
　稀疏向量索引。

**ANN（Approximate Nearest Neighbor）**
　近似最近邻。SQL 里用 `ORDER BY ... APPROXIMATE` 触发。

**`APPROXIMATE`**
　⭐ SELECT 的一等成分（`PARSE_SELECT_APPROX` 槽位），
决定走 ANN 索引还是暴力精确计算。

---

## ⭐ Change Stream

**Change Stream**
　⭐ 异步索引管线：消费 redo 日志，异步更新向量索引，
使写路径与索引构建解耦。`src/observer/change_stream/`。

**IDLE / ACTIVE**
　⭐ Fetcher 的状态机。没有异步索引表时 IDLE（睡眠，零开销），
建了索引才 ACTIVE。

**`refresh_scn`**
　索引已追上的版本号。`wait_refresh_scn` 用于等待索引追平，
对应 pyseekdb 的 `refresh_index()`。

**最终一致**
　⭐ 向量索引不在事务路径上，写入提交后有一个索引可见性延迟窗口。

---

## ⭐ FORK / MERGE

**FORK**
　⭐ 秒级复制表/库。不拷贝数据，只记 `(源表 ID, 快照版本号)`。

**COW（Copy-on-Write）**
　写时复制。seekdb 的实现是 LSM 多版本能力的副产品。

**`fork_snapshot_version_`**
　⭐ 分叉时的版本号。读副本时按它过滤源表的多版本数据。

**BUILD_DATA**
　FORK 之后的异步数据构建阶段。`is_complete_` 标志追踪其完成状态。

**MERGE 策略**
　`FAIL`（冲突报错，默认）/ `THEIRS`（沙箱覆盖）/ `OURS`（主线保留）。
⚠️ 无测试覆盖。

---

## ⭐ 全文与混合检索

**FTS（Full-Text Search）**
　全文检索。

**分词器 / parser**
　`space` / `ngram` / `ngram2` / `beng` / `ik`（中文智能分词）。

**BM25**
　全文相关性打分算法。`ObExprBM25`。

**DAAT / TAAT**
　Document-at-a-Time / Term-at-a-Time——检索的两种推进方式。

**block-max**
　top-k 剪枝优化：块的得分上界低于门槛就整块跳过。

**RRF（Reciprocal Rank Fusion）**
　⭐ 融合算法：按**排名**而非分数融合，免疫量纲差异。
`score = Σ 1/(rank_const + rank_i)`。

**WEIGHT_SUM**
　加权求和融合。需要处理两路分数量纲不一致的问题。

---

## ⭐ 库内 AI

**AI MODEL / AI MODEL ENDPOINT**
　⭐ 两级注册：模型是逻辑对象（类型、模型名），
endpoint 是物理连接（URL、Key、provider）。

**EndpointType**
　`DENSE_EMBEDDING` / `SPARSE_EMBEDDING` / `COMPLETION` / `RERANK`。

**AI_EMBED / AI_COMPLETE / AI_RERANK / AI_PROMPT**
　⭐ 四个库内 AI SQL 函数。README 完全未提及。

---

## 表与索引

**HEAP 表**
　`ORGANIZATION = HEAP`，数据按写入顺序堆放，无主键时自动加隐藏主键
`__pk_increment`。适合无天然主键的 AI 表。

**索引组织表**
　默认方式，数据按主键有序存放。

**辅助表**
　⭐ 一个向量索引在底层展开成的多张内部表（HNSW 是 5 张）。

**域索引（domain index）**
　全文索引、向量索引的统称。

---

## 开发

**oblib**
　基础库，layer 0-1。`deps/oblib/`。

**`ObMemAttr`**
　⭐ 内存归属三元组 `(tenant_id, ctx_id, label)`，
让内存诊断能精确到模块。

**`ObArenaAllocator`**
　最常用的分配器：只分配不释放，析构时统一回收。

**`ObSEArray`**
　Small Efficient Array，栈上预留 N 个元素，超了才上堆。

**`ObString`**
　⚠️ **非拥有**内存，没有结尾 `\0`，语义接近 `std::string_view`。

**`K()` 宏**
　日志里自动打印"变量名=值"。`K_(x)` 用于成员变量。

**`OB_SUCC` / `OB_FAIL` / `FALSE_IT`**
　错误处理宏族。seekdb 不用异常，全靠返回码 + else-if 链。

**WDIAG / EDIAG**
　OceanBase 特有的诊断日志级别，记录错误现场但不代表服务异常。

**debug sync**
　⭐ 内核级同步点，让测试能精确控制并发时序。
`set ob_global_debug_sync = '...'`。

**errsim**
　错误注入构建模式，测试异常路径。

**mysqltest**
　集成测试框架：`t/x.test` 是输入，`r/x.result` 是期望输出。
⭐ **读新特性最好的文档来源**。

**obd**
　OceanBase Deployer，部署工具。`tools/deploy/obd.sh`。
⚠️ 非 root 部署时端口是 `100*(uid%500)+10000`，通常 10000 而非 2881。
