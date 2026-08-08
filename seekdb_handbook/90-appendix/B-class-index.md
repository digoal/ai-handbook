# 附录 B · 关键类速查表

> 按类名查"它在哪、干什么"。带 `:行号` 的是本书正文引用过并核对过的位置。

---

## 进程与框架

| 类 | 位置 | 职责 |
|---|---|---|
| `ObServer` | `src/observer/ob_server.cpp:183` | 进程主体，`init`/`start`/`wait`/`destroy` |
| `ObService` | `src/observer/ob_service.cpp:211` | bootstrap，拒绝 STANDBY |
| `ObIModuleProvider` | `src/share/rc/ob_module_provider.h:214` | ⭐ 全局模块提供者 `g_mp` |
| `ObServerRuntime` | `src/observer/omt/ob_server_runtime.h:173` | 运行时（原租户位），自适应线程池 |
| `ObThWorker` | `src/observer/omt/ob_th_worker.cpp` | 工作线程 |
| `ObSrvMySQLXlator` | `src/observer/ob_srv_xlator.cpp` | 按 pcode 分发 |

---

## MySQL 协议

| 类 | 位置 | 职责 |
|---|---|---|
| `ObMPBase` | `src/observer/mysql/obmp_base.h` | 命令处理器基类 |
| `ObMPQuery` | `src/observer/mysql/obmp_query.cpp:818` | COM_QUERY |
| `ObMPStmtPrepare` / `ObMPStmtExecute` | `src/observer/mysql/` | 预处理语句 |
| `ObQueryDriver` | `src/observer/mysql/ob_query_driver.cpp` | 执行驱动 + 重试 |
| `ObMPPacketSender` | `src/observer/mysql/obmp_packet_sender.cpp` | 回包 |
| `ObSMConnectionCallback` | `src/observer/mysql/obsm_conn_callback.cpp` | 连接回调 |
| `ObMySQLPacket` | `deps/oblib/src/rpc/obmysql/ob_mysql_packet.h` | 协议包 |

---

## SQL 引擎

| 类 | 位置 | 职责 |
|---|---|---|
| `ObSql` | `src/sql/ob_sql.cpp` | 门面：`stmt_resolve` / `handle` |
| `ObParser` | `src/sql/parser/ob_parser.cpp` | 解析入口 |
| `ObFastParser` | `src/sql/parser/ob_fast_parser.cpp` | SIMD 快速解析 |
| `ObSelectResolver` | `src/sql/resolver/dml/ob_select_resolver.cpp:998` | SELECT 语义解析 |
| `ObSelectStmt` | `src/sql/resolver/dml/ob_select_stmt.h` | SELECT 语义树 |
| `ObRawExpr` | `src/sql/resolver/expr/ob_raw_expr.h` | 解析期表达式 |
| `ObOptimizer` | `src/sql/optimizer/ob_optimizer.h:187` | 优化器入口 |
| `ObLogPlan` | `src/sql/optimizer/ob_log_plan.cpp:10317` | 逻辑计划生成 |
| `ObJoinOrder` | `src/sql/optimizer/ob_join_order.h:1307` | join 枚举 |
| `ObStaticEngineCG` | `src/sql/code_generator/ob_static_engine_cg.cpp` | 代码生成 |
| `ObOperator` / `ObOpSpec` | `src/sql/engine/ob_operator.cpp` | 物理算子 / 规格 |
| `ObExpr` | `src/sql/engine/expr/ob_expr.cpp:247` | 执行期表达式 |
| `ObEvalCtx` | `src/sql/engine/expr/ob_expr.h:152` | 求值上下文 |
| `ObBatchRows` | `src/sql/engine/ob_batch_rows.h:30` | 向量化批 |
| `ObTableScanOp` | `src/sql/engine/table/ob_table_scan_op.cpp` | 表扫描算子 |
| `ObPlanCache` | `src/sql/plan_cache/ob_plan_cache.cpp` | 计划缓存 |
| `ObPsCache` | `src/sql/plan_cache/ob_ps_cache.cpp` | 预处理语句缓存 |
| `ObSQLSessionInfo` | `src/sql/session/ob_sql_session_info.cpp` | 会话 |

---

## DAS / DTL

| 类 | 位置 | 职责 |
|---|---|---|
| `ObDataAccessService` | `src/sql/das/ob_data_access_service.cpp` | DAS 入口 |
| `ObDASScanOp` | `src/sql/das/ob_das_scan_op.cpp` | 扫描任务 |
| **`ObDASHNSWScanIter`** | `src/sql/das/iter/ob_das_hnsw_scan_iter.h` | ⭐ HNSW 查询状态机 |
| **`ObDASIvfScanIter`** | `src/sql/das/iter/ob_das_ivf_scan_iter.h` | ⭐ IVF 查询 |
| **`ObDASTRMergeIter`** | `src/sql/das/iter/sparse_retrieval/ob_das_tr_merge_iter.h` | ⭐ 全文归并 |
| **`ObDASMatchIter`** | `src/sql/das/iter/sparse_retrieval/ob_das_match_iter.h` | ⭐ MATCH top-k |
| `ObDtlChannel` | `src/sql/dtl/ob_dtl_channel.cpp` | 数据通道 |
| `ObDtlFlowControl` | `src/sql/dtl/ob_dtl_flow_control.cpp` | 流控 |

---

## 存储

| 类 | 位置 | 职责 |
|---|---|---|
| `ObMemtable` | `src/storage/memtable/ob_memtable.h` | MemTable |
| `ObMvccTransNode` | `src/storage/memtable/mvcc/ob_mvcc_row.h:64` | ⭐ 多版本节点 |
| `ObMvccRowCallback` | `src/storage/memtable/mvcc/ob_mvcc_trans_ctx.h:425` | 事务回调 |
| `ObTablet` | `src/storage/tablet/ob_tablet.h` | 分区 |
| `ObTabletTableStore` | `src/storage/tablet/ob_tablet_table_store.h:83` | SSTable 集合 |
| `ObLS` | `src/storage/ls/ob_ls.cpp:57` | 日志流 |
| `ObLSService` | `src/storage/tx_storage/ob_ls_service.cpp:45` | LS 管理 |
| `ObLSTabletService` | `src/storage/ls/ob_ls_tablet_service.h:97` | tablet CRUD |
| `ObSSTable` | `src/storage/blocksstable/ob_sstable.h` | SSTable |
| `ObSSTableMeta` | `src/storage/blocksstable/ob_sstable_meta.h` | SSTable 元信息 |
| `ObTabletScheduler` | `src/storage/compaction/ob_tablet_scheduler.cpp` | 合并调度 |
| **`ObForkSnapshotRowScan`** | `src/storage/ddl/ob_tablet_fork_task.h:70` | ⭐ FORK 快照扫描 |

---

## 事务与日志

| 类 | 位置 | 职责 |
|---|---|---|
| `ObTransService` | `src/storage/tx/ob_trans_service.cpp:40` | 事务服务 |
| `ObPartTransCtx` | `src/storage/tx/ob_part_trans_ctx.cpp` | 事务状态机 |
| `ObTimestampService` | `src/storage/tx/ob_timestamp_service.cpp` | 全局时间戳 |
| `PalfEnv` | `src/logservice/palf/palf_env.cpp` | Paxos 日志环境 |
| `PalfEnvImpl` | `src/logservice/palf/palf_env_impl.h:194` | 实现 |
| `ObLogService` | `src/logservice/ob_log_service.cpp` | 日志服务门面 |
| `ObLogApplyService` | `src/logservice/applyservice/ob_log_apply_service.h` | 提交回调 |
| `ObLogReplayService` | `src/logservice/replayservice/ob_log_replay_service.cpp` | 重启回放 |

---

## ⭐ 向量索引

| 类 | 位置 | 职责 |
|---|---|---|
| `ObVectorIndexMemData` | `src/observer/vector_index/ob_plugin_vector_index_adaptor.h:401` | 一份内存索引 |
| `ObPluginVectorIndexAdaptor` | 同上 `:545` | 容器：incr/snap/bitmap |
| — `incr_data_` | 同上 `:892` | 增量（delta）索引 |
| — `snap_data_` | 同上 `:893` | 快照索引 |
| — `vbitmap_data_` | 同上 `:894` | 可见性位图 |
| `ObPluginVectorIndexHelper` | `ob_plugin_vector_index_utils.cpp` | 两路归并 |
| `ObVectorIndexAsyncTaskScheduler` | `ob_vector_index_async_task.cpp` | 异步任务调度 |
| `ObEmbeddingTask` | `ob_vector_embedding_handler.cpp` | 库内 embedding |
| `ObVecIndexBuilderUtil` | `src/sql/resolver/ddl/ob_vec_index_builder_util.cpp` | 辅助表展开 |
| `ObVsagAdaptor` | `deps/oblib/src/lib/vector/ob_vsag_adaptor.h` | VSAG C 接口 |

---

## ⭐ Change Stream

| 类 | 位置 | 职责 |
|---|---|---|
| `ObChangeStreamMgr` | `src/observer/change_stream/ob_change_stream_mgr.h:34` | 管理器、`wait_refresh_scn:53` |
| `ObCSFetcher` | `ob_change_stream_fetcher.h:119` | 单线程消费日志 |
| — `RunningMode` | 同上 `:161` | IDLE / ACTIVE 状态机 |
| `ObCSDispatcher` | `ob_change_stream_dispatcher.h` | 拆解组批、`ObCSRow` |
| `ObCSExecutor` | `ob_change_stream_worker.h` | 并行执行 |
| `ObCSPlugin` | `ob_change_stream_plugin.h:43` | 插件基类 |
| `ObCSPluginRegistry` | 同上 `:67` | 插件工厂 |
| `ObCSPluginAsyncIndex` | `ob_cs_plugin_async_index.cpp` | 异步索引插件 |

---

## ⭐ FORK / MERGE

| 类 | 位置 | 职责 |
|---|---|---|
| `ObForkTableInfo` | `src/share/ob_fork_table_info.h:32` | 表级 COW 元信息 |
| `ObForkTabletInfo` | 同上 `:52` | 分区级 |
| `ObForkTableResolver` | `src/sql/resolver/ddl/ob_fork_table_resolver.cpp` | 解析 |
| `ObMergeTableStrategy` | `src/sql/resolver/cmd/ob_merge_table_stmt.h:28` | FAIL/THEIRS/OURS |
| `ObMergeTableResolver` | `src/sql/resolver/cmd/ob_merge_table_resolver.cpp` | 合成三段 SQL |
| `ObForkTableService` | `src/rootserver/fork_table/ob_fork_table_service.cpp` | FORK 服务 |
| `ObTableForkInfo` | `src/storage/ddl/ob_table_fork_info.cpp` | 存储层参数 |

---

## ⭐ 库内 AI

| 类 | 位置 | 职责 |
|---|---|---|
| `ObExprAIEmbed` | `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:29` | `AI_EMBED` |
| `ObExprAIComplete` | `ob_expr_ai_complete.cpp` | `AI_COMPLETE` |
| `ObExprAIRerank` | `ob_expr_ai_rerank.cpp` | `AI_RERANK` |
| `ObExprAIPrompt` | `ob_expr_ai_prompt.cpp` | `AI_PROMPT` |
| `ObAIFuncExprInfo` | `ob_ai_func.h:34` | 表达式额外信息 |
| `ObAIFuncIEmbed` / `IComplete` / `IRerank` | `ob_ai_func.h:74-117` | 接口抽象 |
| `ObAIFuncClient` | `ob_ai_func_client.h:28` | libcurl 客户端 |
| `ObAiServiceExecutor` | `src/observer/ai_service/ob_ai_service_executor.h:34` | endpoint CRUD |
| `EndpointType` | `src/share/ai_service/ob_ai_model_info.h` | 四种模型类型 |

---

## ⭐ 全文与混合检索

| 类 | 位置 | 职责 |
|---|---|---|
| `ObFTParseHelper` | `src/storage/fts/ob_fts_parser_helper.cpp` | 分词入口 |
| `ObFTParserProperty` | 同上 | 分词器参数 |
| `ObExprBM25` | `src/sql/engine/expr/ob_expr_bm25.cpp` | BM25 打分 |
| `ObBlockMaxScoreIter` | `src/storage/retrieval/ob_block_max_iter.cpp` | block-max 剪枝 |
| `ObHybridSearchExecutor` | `src/sql/hybrid_search/ob_hybrid_search_executor.cpp` | SEARCH / GET_SQL |
| `ObESQueryParser` | `src/sql/hybrid_search/ob_query_parse.cpp` | JSON DSL 解析 |
| `ObQueryTranslator` | `src/sql/hybrid_search/ob_query_translator.cpp` | DSL → SQL |
| `ObRankFusion` | `ob_query_parse.h` | WEIGHT_SUM / RRF |

---

## oblib 基础设施

| 类 | 位置 | 职责 |
|---|---|---|
| `ObArenaAllocator` | `deps/oblib/src/lib/allocator/page_arena.h` | 最常用分配器 |
| `ObMallocAllocator` | `deps/oblib/src/lib/alloc/ob_malloc_allocator.cpp` | 全局分配器 |
| `ObMemoryDump` | `deps/oblib/src/lib/alloc/memory_dump.cpp` | 内存统计 |
| `ObSEArray` | `deps/oblib/src/lib/container/ob_se_array.h` | 栈上小数组 |
| `ObHashMap` | `deps/oblib/src/lib/hash/ob_hashmap.h` | 哈希表 |
| `ObString` | `deps/oblib/src/lib/string/ob_string.h` | ⚠️ 非拥有语义 |
| `TCRWLock` | `deps/oblib/src/lib/lock/` | 向量索引用的读写锁 |
