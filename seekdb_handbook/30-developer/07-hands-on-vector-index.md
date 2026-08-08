# 3.7 实战二：读懂并扩展向量索引

> **一句话**：向量索引是 seekdb 最复杂的子系统，横跨 6 个目录。
> 这一章给你一条阅读路线，以及"加一个新索引类型"要动哪些地方。

---

## 先建立地图

向量索引的代码**没有集中在一个目录**，这是读它最大的障碍
（README 还指错了路，见 [0.3 代码地图](../00-orientation/03-code-map.md)）。

实际分布：

| 目录 | 职责 |
|---|---|
| `src/observer/vector_index/` | **核心**：插件适配器、调度器、IVF、KMeans、embedding |
| `src/storage/vector_index/` | 索引刷新、调度作业、刷新事务 |
| `src/storage/vector_type/` | SIMD 距离函数 |
| `src/sql/das/iter/` | 查询迭代器（HNSW / IVF） |
| `src/sql/resolver/ddl/ob_vec_index_builder_util.cpp` | DDL 展开辅助表 |
| `deps/oblib/src/lib/vector/` | VSAG 库适配层 |

外加：`src/rootserver/ddl_task/` 里的异步构建任务、
`src/pl/sys_package/ob_dbms_vector_mysql.cpp` 的 PL 包。

---

## 推荐阅读顺序

### 第 1 站：枚举定义（10 分钟）

`src/observer/vector_index/ob_vector_index_util.h`

先把词汇表建立起来：

```cpp
enum ObVectorIndexAlgorithmType {
  VIAT_HNSW, VIAT_HNSW_SQ, VIAT_IVF_FLAT, VIAT_IVF_SQ8,
  VIAT_IVF_PQ, VIAT_HNSW_BQ, VIAT_HGRAPH, VIAT_SPIV, VIAT_IPIVF, VIAT_MAX
};

enum ObVectorIndexType { VIT_HNSW_INDEX = 0, VIT_IVF_INDEX = 1, VIT_SPIV_INDEX = 2 };
enum ObVectorIndexAlgorithmLib { VIAL_VSAG = 0, VIAL_OB, VIAL_MAX };
enum ObVectorIndexDistAlgorithm { VIDA_L2 = 0, VIDA_IP = 1, VIDA_COS = 2 };
```

注意有**两层**分类：细粒度的 `AlgorithmType`（9 种）
和粗粒度的 `IndexType`（3 类）。很多逻辑按粗粒度分支。

### 第 2 站：两级索引的数据结构（核心）

`src/observer/vector_index/ob_plugin_vector_index_adaptor.h`

这是整个子系统的心脏。两个类：

**`ObVectorIndexMemData`（约 401 行起）**——一份索引的内存态：

```cpp
void   *index_;                  // 不透明句柄，指向 VSAG 的索引对象
ObVectorIndexRoaringBitMap *bitmap_;   // 可见性位图
TCRWLock mem_data_rwlock_;       // 保护 index_ (459 行)
TCRWLock bitmap_rwlock_;         // 保护 bitmap_ (458 行)
uint64_t ref_cnt_;               // 引用计数 (461 行)
SCN      scn_;
int64_t  last_dml_scn_, last_read_scn_;
```

**`ObPluginVectorIndexAdaptor`（545 行）**——容器，持有三份：

```cpp
ObVectorIndexMemData *incr_data_;      // 892 行：增量（delta）
ObVectorIndexMemData *snap_data_;      // 893 行：快照（snapshot）
ObVectorIndexMemData *vbitmap_data_;   // 894 行：可见性位图
```

**这就是"两级 HNSW"的物理形态**：`incr_data_` 接收新写入，
`snap_data_` 存量数据，查询两边都查再归并。

### 关键设计：两把独立的读写锁

`mem_data_rwlock_` 和 `bitmap_rwlock_` 是**分开的**。
索引结构和可见性位图可以独立加锁，粒度更细——
这是并发下 P99 稳定的原因之一。

引用计数用原子操作（`ATOMIC_INC` / `ATOMIC_SAF`，441-446 行），
支持跨任务传递索引句柄而不用长期持锁。

快照重建时的换手是：先对旧 `incr_data_` 加**读锁**，
再对新的加**写锁**，完成原子切换。

### 第 3 站：查询路径

`src/sql/das/iter/ob_das_hnsw_scan_iter.h`

`ObDASHNSWScanIter` 是个状态机：

```cpp
enum ObVidAdaLookupStatus {
  STATES_INIT,
  QUERY_INDEX_ID_TBL,      // 查索引元信息表
  QUERY_SNAPSHOT_TBL,      // 查快照
  QUERY_ROWKEY_VEC,        // 由 vid 反查主键和向量
  STATES_SET_RESULT,
  STATES_ERROR, STATES_FINISH, STATES_REFRESH
};
```

它持有一串子迭代器：`delta_buf_iter_`、`snapshot_iter_`、
`index_id_iter_`、`vid_rowkey_iter_`、`data_filter_iter_`、
`pre_filter_iter_` 等——对应那 5 张辅助表。

归并两路结果的函数在
`src/observer/vector_index/ob_plugin_vector_index_utils.cpp`：
`driect_merge_delta_and_snap_vids` 和 `sort_merge_delta_and_snap_vids`。

### 第 4 站：DDL 展开

`src/sql/resolver/ddl/ob_vec_index_builder_util.cpp`

`ObVecIndexBuilderUtil::append_vec_args` 按算法类型分派：

```
append_vec_hnsw_args()        HNSW → 5 张辅助表
append_vec_ivfflat_args()     IVF-Flat
append_vec_ivfsq8_args()      IVF-SQ8
append_vec_ivfpq_args()       IVF-PQ
append_vec_spiv_args()        稀疏向量
append_hybrid_vec_hnsw_args() 混合（带 embedding）
```

HNSW 的 5 张辅助表，索引类型码定义在
`src/share/schema/ob_schema_struct.h`：

| 码 | 类型 | 用途 |
|---|---|---|
| 23 | `VEC_ROWKEY_VID_LOCAL` | 主键 → 向量 ID |
| 24 | `VEC_VID_ROWKEY_LOCAL` | 向量 ID → 主键 |
| 25 | `VEC_DELTA_BUFFER_LOCAL` | 增量缓冲 |
| 26 | `VEC_INDEX_ID_LOCAL` | 索引元信息 |
| 27 | `VEC_INDEX_SNAPSHOT_DATA_LOCAL` | 快照序列化数据 |

### 第 5 站：VSAG 适配层

`deps/oblib/src/lib/vector/ob_vsag_adaptor.h`

```cpp
enum IndexType {
  HNSW_TYPE = 0, HNSW_SQ_TYPE = 1, HNSW_BQ_TYPE = 5,
  HGRAPH_TYPE = 6, IPIVF_TYPE = 8
};
```

C 风格接口：`create_index` / `build_index` / `add_index` /
`knn_search` / `serialize` / `deserialize_bin` / `delete_index` /
`estimate_memory`。

seekdb 枚举 → VSAG 枚举的映射在
`ob_vector_index_util.cpp`（`VIAT_HNSW` → `HNSW_TYPE`，
有 extra_info 时改走 `HGRAPH_TYPE`，等等）。

> ⚠️ **VSAG 本身不在这个仓库**，是外部依赖
> （见 `deps/init/oceanbase.*.deps` 里的 `vsag-abiv1`）。
> HNSW 的图构建、剪枝、量化这些算法细节要去 VSAG 项目看。
> seekdb 这边只负责：数据怎么喂进去、索引怎么持久化、
> 查询怎么归并、生命周期怎么管。

---

## 场景：加一个新的向量索引类型

假设你要加一个 `VIAT_MYALGO`。要动的地方：

### 1. 枚举
`src/observer/vector_index/ob_vector_index_util.h`
在 `ObVectorIndexAlgorithmType` 里加值（放 `VIAT_MAX` 之前），
必要时也在 `ObVectorIndexType` 里归类。

### 2. 参数解析
`ob_vector_index_util.cpp` 的 `parser_params_from_string`：
让 `type=myalgo` 能被识别。若有专属参数（像 IVF-PQ 的 `m=`），
在这里解析并校验。

### 3. 辅助表展开
`src/sql/resolver/ddl/ob_vec_index_builder_util.cpp`：
写一个 `append_vec_myalgo_args()`，决定这个算法需要几张辅助表。
如果结构和 HNSW 一样，可以复用 `append_vec_hnsw_args`。

### 4. 底层库映射
- 走 VSAG：在 `ob_vector_index_util.cpp` 的映射函数里加分支，
  对应 `obvsag::` 的某个 `IndexType`
- 自己实现：在 `ObVectorIndexAlgorithmLib` 加 `VIAL_XXX`，
  并实现建索引/查询接口

### 5. 查询迭代器
如果查询流程和 HNSW / IVF 都不同，
在 `src/sql/das/iter/` 加一个迭代器（参考 `ObDASIvfScanIter` 系列）。

### 6. 异步任务
`src/observer/vector_index/ob_vector_index_async_task.h` 的
`ObVecIndexAsyncTaskType`，看是否需要新的任务类型。

### 7. 测试
`tools/deploy/mysql_test/test_suite/vector_index/`：
建 DDL、写数据、查询、重建、drop 全流程都要覆盖。
参考 `vector_index_basic.test` 的组织方式。

---

## 读代码的几个提醒

1. **"plugin" 是命名习惯不是热插拔**。`ObPluginVectorIndexAdaptor` 里的
   "plugin" 指的是对接外部向量库（VSAG）的适配层，不是运行时可加载插件。

2. **`incr` = 增量 = delta**。源码里叫 `incr_data_`，
   博客里叫 delta HNSW，是同一个东西。

3. **索引不落在数据表上**。向量索引是**独立的辅助表 + 内存索引结构**，
   理解这一点才能理解为什么 fork、DDL、合并都要特殊处理向量索引。

4. **先读测试再读实现**。`vector_index/` 套件 22 个用例覆盖了
   绝大多数行为边界，比读实现快得多。

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/observer/vector_index/ob_vector_index_util.h` | 全部枚举定义 |
| `src/observer/vector_index/ob_vector_index_util.cpp` | 参数解析、枚举映射 |
| `src/observer/vector_index/ob_plugin_vector_index_adaptor.h:401` | `ObVectorIndexMemData` |
| `src/observer/vector_index/ob_plugin_vector_index_adaptor.h:458-461` | 两把 `TCRWLock` + `ref_cnt_` |
| `src/observer/vector_index/ob_plugin_vector_index_adaptor.h:545` | `ObPluginVectorIndexAdaptor` |
| `src/observer/vector_index/ob_plugin_vector_index_adaptor.h:892-894` | `incr_data_` / `snap_data_` / `vbitmap_data_` |
| `src/observer/vector_index/ob_plugin_vector_index_utils.cpp` | 两路归并 |
| `src/observer/vector_index/ob_vector_kmeans_ctx.cpp` | IVF 的 KMeans |
| `src/observer/vector_index/ob_vector_embedding_handler.cpp` | 库内 embedding |
| `src/sql/das/iter/ob_das_hnsw_scan_iter.h` | HNSW 查询状态机 |
| `src/sql/das/iter/ob_das_ivf_scan_iter.h` | IVF 查询迭代器 |
| `src/sql/das/ob_das_vec_define.h` | 5 种执行策略 |
| `src/sql/resolver/ddl/ob_vec_index_builder_util.cpp` | 辅助表展开 |
| `src/share/schema/ob_schema_struct.h` | 索引类型码 23-27 等 |
| `deps/oblib/src/lib/vector/ob_vsag_adaptor.h` | VSAG C 接口 |
| `src/storage/vector_type/` | SIMD 距离函数 |

---

## 动手验证

看全部算法枚举：

```bash
grep -n "VIAT_\|VIT_\|VIAL_\|VIDA_" src/observer/vector_index/ob_vector_index_util.h | head -25
```

看两级索引的三个成员：

```bash
sed -n '888,900p' src/observer/vector_index/ob_plugin_vector_index_adaptor.h
```

看查询状态机：

```bash
grep -n -A 12 "enum ObVidAdaLookupStatus" src/sql/das/iter/ob_das_hnsw_scan_iter.h
```

看辅助表索引类型码：

```bash
grep -n "INDEX_TYPE_VEC_" src/share/schema/ob_schema_struct.h
```

---

## 延伸阅读

- 第 3 篇到此结束。
- [2.10 向量索引架构](../20-architect/10-vector-index.md) —— 架构视角的完整拆解
- [2.11 Change Stream](../20-architect/11-change-stream.md) —— 增量索引是怎么被喂数据的
- [3.5 测试体系](05-testing.md) —— 怎么跑 vector_index 套件
