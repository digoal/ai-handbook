# 附录 C · 参数与虚拟表速查

---

## 参数体系

- **定义**：`src/share/parameter/ob_parameter_seed.ipp`（**284** 条 `DEF_PARAM`）
- **宏**：`ob_parameter_macro.h`
- **属性**：`ob_parameter_attr.h`（Section / Scope / Source / EditLevel）
- **场景默认值**：`default_parameter.json`
- **单机覆盖**：`standalone_default_parameter.extra`

修改方式：

```sql
ALTER SYSTEM SET <参数名> = <值>;
```

`EditLevel` 决定是否需要重启：

| 级别 | 含义 |
|---|---|
| `READONLY` | 只读 |
| `STATIC_EFFECTIVE` | 改完要重启 |
| `DYNAMIC_EFFECTIVE` | 立即生效 |

---

## 常用参数

### 网络

| 参数 | 默认 | 行 |
|---|---|---|
| `mysql_port` | 2881 | 54 |
| `rpc_port` | 2882 | 51 |
| `net_thread_count` | — | — |
| `enable_rpc_tls` | — | — |

### 存储

| 参数 | 默认 | 行 |
|---|---|---|
| `data_dir` | `"store"` | 26 |
| `redo_dir` | `""` | 28 |
| `datafile_size` | `32M` | 32 |
| `datafile_maxsize` | `1T` | — |
| `datafile_next` | — | — |
| `datafile_disk_percentage` | — | — |
| `_datafile_usage_upper_bound_percentage` | 90 | — |

### 内存与 CPU

| 参数 | 默认 |
|---|---|
| `memory_limit` | `0M`（自动） |
| `memory_budget` | — |
| `cpu_count` | 0（自动） |
| `workers_per_cpu_quota` | — |
| **`ob_vector_memory_limit_percentage`** | 向量索引内存占比，向量场景需调 |

### 日志

| 参数 | 默认 | 行 |
|---|---|---|
| `syslog_level` | 编译期默认 | 136 |
| `syslog_io_bandwidth_limit` | `5MB` | 139 |
| `max_syslog_file_count` | **2**（建议调到 80） | 145 |
| `enable_async_syslog` | `True` | 151 |
| `enable_syslog_recycle` | `False`（建议开） | — |
| `enable_syslog_wf` | — | — |
| `diag_syslog_per_error_limit` | 200 | — |

> ⚠️ 官方单机场景推荐：`syslog_level=WARN`、
> `enable_syslog_recycle=1`、`max_syslog_file_count=80`。
> 见 `standalone_default_parameter.extra`。

### 压缩与行格式

| 参数 | 取值 |
|---|---|
| `default_compress_func` | `zstd_1.3.8`（默认）/ `zlib_1.0` / `none` |
| `default_row_format` | `REDUNDANT`/`COMPACT`/`DYNAMIC`/`COMPRESSED`/`CONDENSED` |
| `storage_rowsets_size` | — |
| `default_table_organization` | 默认表组织方式（HEAP / INDEX） |

### 诊断

| 参数 | 默认 |
|---|---|
| `enable_sql_audit` | — |
| `sql_audit_size` | — |
| `trace_log_slow_query_watermark` | 1s |
| `enable_record_trace_log` | — |
| `enable_record_trace_id` | — |
| `enable_rich_error_msg` | — |
| `enable_perf_event` | — |
| `debug_sync_timeout` | 测试用 |

---

## 系统变量

与参数是**两套**东西：

```sql
SET [GLOBAL] <变量名> = <值>;
```

定义：`src/share/system_variable/ob_system_variable_init.json`，
经 `gen_ob_sys_variables.py` 生成代码。
单机覆盖：`standalone_default_system_variable.extra`。

测试用例里常见：

```sql
SET ob_query_timeout = 100000000;
SET ob_trx_timeout   = 100000000;
SET wait_timeout     = 30000000;
SET ob_global_debug_sync = '...';
```

---

## 虚拟表

实现：`src/observer/virtual_table/`（**154** 个头文件）。
基类 `ObVirtualTableScannerIterator`。

```sql
select * from oceanbase.__all_virtual_<name>;
```

### 常用

| 虚拟表 | 看什么 |
|---|---|
| `__all_virtual_sql_audit` | SQL 执行历史 |
| `__all_virtual_plan_cache_stat` | 计划缓存 |
| `__all_virtual_memory_info` | 内存按 label |
| `__all_virtual_ctx_memory_info` | 内存按 ctx |
| `__all_virtual_memstore_info` | MemTable 状态 |
| `__all_virtual_tablet_memstore_info` | tablet 级 MemTable |
| `__all_virtual_compaction_diagnose_info` | 合并诊断 |
| `__all_virtual_dag` | DAG 任务 |
| `__all_virtual_dtl_channel` | 数据通道 |
| `__all_virtual_dtl_memory` | DTL 内存 |
| `__all_virtual_dml_stats` | DML 统计 |
| **`__all_virtual_vector_index_info`** | ⭐ 向量索引状态 |
| `__all_virtual_checkpoint` | 检查点 |
| `__all_virtual_charset` | 字符集 |
| `__all_virtual_tracepoint_info` | 测试注入点 |

### AI 相关视图

| 视图 | 内容 |
|---|---|
| `oceanbase.DBA_OB_AI_MODELS` | 已注册的 AI 模型 |
| `oceanbase.DBA_OB_AI_MODEL_ENDPOINTS` | 已注册的 endpoint |

---

## ⚠️ GV$ / V$ 视图已被删除

单租户化过程中 **81 个** GV$/V$ 视图被移除
（`src/share/inner_table/ob_inner_table_schema_def.py` 里
81 处 `single-tenant GV/V collapse` 注释）。

| 老写法 | 新写法 |
|---|---|
| `GV$OB_SQL_AUDIT` / `V$OB_SQL_AUDIT` | `oceanbase.__all_virtual_sql_audit` |
| `GV$OB_PLAN_CACHE_STAT` | `oceanbase.__all_virtual_plan_cache_stat` |
| `GV$OB_MEMSTORE` / `V$OB_MEMSTORE` | `oceanbase.__all_virtual_memstore_info` |
| `GV$OB_MEMORY` | `oceanbase.__all_virtual_memory_info` |
| `GV$OB_MEMSTORE_INFO` | `oceanbase.__all_virtual_tablet_memstore_info` |

**从 OceanBase 迁移监控脚本时必须替换。**

仓库自带的 `script/sqlaudit/sqlaudit.py` 仍在用 `V$OB_SQL_AUDIT`，
已失效（见 [1.8 可观测性](../10-user/08-observability.md)）。

---

## 内部表 ID 段位

`src/share/inner_table/ob_inner_table_schema_def.py`：

| 范围 | 用途 |
|---|---|
| `(0, 100)` | 核心表 |
| `(0, 10000)` | 系统表 |
| `(10000, 15000)` | MySQL 虚拟表 |
| `(15000, 20000)` | 扩展虚拟表 |
| `(20000, 25000)` | MySQL 系统视图 |
| `(25000, 30000)` | 扩展系统视图 |
| `(50000, 60000)` | LOB meta |
| `(60000, 70000)` | LOB piece |
| `(100000, 200000)` | 系统索引 |
| `(500000, …)` | 用户表 |

---

## 索引类型码

`src/share/schema/ob_schema_struct.h`：

| 码 | 类型 |
|---|---|
| 23 | `INDEX_TYPE_VEC_ROWKEY_VID_LOCAL` |
| 24 | `INDEX_TYPE_VEC_VID_ROWKEY_LOCAL` |
| 25 | `INDEX_TYPE_VEC_DELTA_BUFFER_LOCAL` |
| 26 | `INDEX_TYPE_VEC_INDEX_ID_LOCAL` |
| 27 | `INDEX_TYPE_VEC_INDEX_SNAPSHOT_DATA_LOCAL` |
| 28–38 | IVF 系列 |
| 39 | `INDEX_TYPE_HEAP_ORGANIZED_TABLE_PRIMARY` |
| 40 | `INDEX_TYPE_VEC_SPIV_DIM_DOCID_VALUE_LOCAL` |
| 41 | `INDEX_TYPE_HYBRID_INDEX_LOG_LOCAL` |
| 42 | `INDEX_TYPE_HYBRID_INDEX_EMBEDDED_LOCAL` |

---

## 错误码

定义：`src/share/ob_errno.def`
工具：`./ob_error <码>`（源码 `tools/ob_error/`）

本书正文提到过的：

| 码 | 含义 |
|---|---|
| 1582 | 函数参数个数错误 |
| 5083 | 函数参数类型错误 |
| 11112 | AI endpoint 不存在 |
| 11113 | AI endpoint 参数非法 |
| 11118 | AI 模型不存在 |
| -4379 | `OB_HEAP_TABLE_EXAUSTED` |

---

## 系统包

`src/share/inner_table/sys_package/`：

| 包 | 用途 |
|---|---|
| **`dbms_vector`** | ⭐ 向量索引维护（refresh / rebuild） |
| **`dbms_hybrid_vector`** | ⭐ 混合检索 SEARCH / GET_SQL |
| **`dbms_ai_service`** | ⭐ AI 模型与 endpoint 管理 |
| `dbms_index_manager` | 索引管理 |
| `dbms_stats` | 统计信息 |
| `dbms_scheduler` / `dbms_ischeduler` | 作业调度 |
| `dbms_session` | 会话 |
| `dbms_monitor` | 监控 |
| `dbms_space` | 空间 |
| `dbms_application` | 应用信息 |
| `dbms_ob_limit_calculator` | 资源上限计算 |
| `dbms_trusted_certificate_manager` | 证书 |
