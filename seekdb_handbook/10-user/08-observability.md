# 1.8 可观测性与排障

> **一句话**：seekdb 的自省能力靠 154 个虚拟表；但要注意——
> 单租户化过程中 **81 个 GV$/V$ 视图被删除了**，老文档和老脚本会失效。

---

## 核心机制：虚拟表

seekdb 把内部状态暴露成"表"，你用普通 SQL 就能查：

```sql
select * from oceanbase.__all_virtual_plan_cache_stat;
select * from oceanbase.__all_virtual_memory_info;
```

实现在 `src/observer/virtual_table/`，**154 个头文件**，
每个 `__all_virtual_*` 对应一个 `ObVirtualTableScannerIterator` 子类，
迭代时直接读进程内部状态——不落盘、不走存储引擎。

常用的一些：

| 虚拟表 | 看什么 |
|---|---|
| `__all_virtual_sql_audit` | SQL 执行历史（最常用） |
| `__all_virtual_plan_cache_stat` | 计划缓存命中率 |
| `__all_virtual_memory_info` | 各模块内存占用 |
| `__all_virtual_ctx_memory_info` | 按 ctx 的内存分布 |
| `__all_virtual_memstore_info` | MemTable 状态 |
| `__all_virtual_compaction_diagnose_info` | 合并诊断 |
| `__all_virtual_dag` | DAG 任务调度 |
| `__all_virtual_vector_index_info` | **向量索引状态** |
| `__all_virtual_dtl_channel` | 数据传输通道 |
| `__all_virtual_dml_stats` | DML 统计 |

> 💡 向量场景下 `__all_virtual_vector_index_info` 值得重点关注，
> 官方测试里有专门用例
> `vector_index/t/all_virtual_vector_index_info.test`。

---

## ⚠️ 重大变更：GV$ / V$ 视图已被折叠

OceanBase 的传统是提供两套视图：
`GV$xxx`（集群全局）和 `V$xxx`（本节点）。
seekdb 单租户化之后，**这套视图被大规模删除**。

在 `src/share/inner_table/ob_inner_table_schema_def.py` 里可以看到
**81 处**这样的注释：

```python
# 20001: GV$OB_PLAN_CACHE_STAT # removed (single-tenant GV/V collapse; use oceanbase.__all_virtual_plan_cache_stat)
# 21018: GV$OB_MEMSTORE # removed (single-tenant GV/V collapse; use oceanbase.__all_virtual_memstore_info)
# 21014: GV$OB_SQL_AUDIT # removed
# 21026: V$OB_SQL_AUDIT # removed
```

**实际影响**：

| 你想用 | 现在应该用 |
|---|---|
| `GV$OB_SQL_AUDIT` / `V$OB_SQL_AUDIT` | `oceanbase.__all_virtual_sql_audit` |
| `GV$OB_PLAN_CACHE_STAT` | `oceanbase.__all_virtual_plan_cache_stat` |
| `GV$OB_MEMSTORE` | `oceanbase.__all_virtual_memstore_info` |
| `GV$OB_MEMORY` | `oceanbase.__all_virtual_memory_info` |

**照搬 OceanBase 的监控 SQL 会失败。** 迁移时把 `GV$xxx` / `V$xxx`
换成对应的 `__all_virtual_*`。

### 仓库自带的脚本已经过时

一个具体例子：`script/sqlaudit/sqlaudit.py` 第 26 行仍然在查

```sql
select request_time, query_sql from oceanbase.V$OB_SQL_AUDIT where ...
```

而 `V$OB_SQL_AUDIT` 已被标记 `# removed`。
**这个脚本在当前 seekdb 上大概率跑不通**，需要把表名换成
`oceanbase.__all_virtual_sql_audit`。

自行核对：

```bash
grep -n "V\$OB_SQL_AUDIT" script/sqlaudit/sqlaudit.py
grep -n 'V\$OB_SQL_AUDIT.*removed' src/share/inner_table/ob_inner_table_schema_def.py
```

---

## SQL 审计

开关参数：

| 参数 | 说明 |
|---|---|
| `enable_sql_audit` | 是否记录 |
| `sql_audit_size` | 审计缓冲区大小 |

查最近的慢 SQL（把老脚本的视图名换掉之后）：

```sql
select request_time, elapsed_time, query_sql
from oceanbase.__all_virtual_sql_audit
where elapsed_time > 100000
order by request_time desc
limit 20;
```
*⚠️ 未实机验证，列名请以实际 schema 为准。*

相关参数还有 `trace_log_slow_query_watermark`（默认 1 秒），
超过这个阈值的查询会打 trace 日志。

---

## 日志

主日志在 `<安装目录>/log/seekdb.log`。

日志级别 7 档（`syslog_level`）：
`DEBUG` / `TRACE` / `WDIAG` / `EDIAG` / `INFO` / `WARN` / `ERROR`。

其中 `WDIAG` 和 `EDIAG` 是 OceanBase 特有的"诊断"级别，
用于记录错误现场但不代表服务异常。

日志宏定义在 `deps/oblib/src/lib/oblog/ob_log_module.h`：

```cpp
LOG_INFO("...", K(var));      // K() 宏打印变量名=值
LOG_WARN("...", K(ret));
LOG_USER_ERROR(...);          // 返回给客户端的错误
```

每个 `.cpp` 开头会 `#define USING_LOG_PREFIX SQL_ENG` 之类，
决定日志的模块前缀。模块列表在 `ob_log_module.ipp`。

日志相关参数见 [1.7 部署与配置](07-deploy-config.md)。

---

## 错误码工具：`ob_error`

seekdb 的错误码是自己的一套（`src/share/ob_errno.def`）。
遇到 `-4379` 这种数字，用自带工具查：

```bash
./ob_error 4379
```

工具源码在 `tools/ob_error/`，支持 OS / MySQL / OceanBase 三个域的错误码。

几个 AI 相关错误码（从测试用例反推）：

| 码 | 含义 |
|---|---|
| 11112 | AI endpoint 不存在 |
| 11113 | AI endpoint 参数非法 |
| 11118 | AI 模型不存在 |
| -4379 | `OB_HEAP_TABLE_EXAUSTED` |

---

## 内存诊断

内存问题是数据库排障的大头。seekdb 的内存按
`(tenant_id, ctx_id, label)` 三元组归类，
所以能精确定位到"哪个模块吃了多少"。

```sql
select * from oceanbase.__all_virtual_memory_info;
select * from oceanbase.__all_virtual_ctx_memory_info;
```

底层实现：

| 组件 | 位置 |
|---|---|
| `ObMallocAllocator` | `deps/oblib/src/lib/alloc/ob_malloc_allocator.cpp` |
| `ObTenantCtxAllocator` | `deps/oblib/src/lib/alloc/ob_ctx_allocator.cpp` |
| `ObMemoryDump` | `deps/oblib/src/lib/alloc/memory_dump.cpp` |

`ObMemoryDump` 是一个单线程池，周期性遍历所有 label 和 ctx 生成统计——
这就是 `__all_virtual_memory_info` 的数据源。

详见 [3.2 oblib 基础设施](../30-developer/02-oblib.md)。

---

## 崩溃分析

`gdb-macros/` 提供了 core 文件的自动分析：

```bash
./gdb-macros/auto-analysis.sh
```

它会定位 `observer` 二进制和 core 文件，跑批处理 GDB，
输出 `bt-all.txt`（所有线程栈）和 `bt.txt`。

`all.gdb` 里还有一些辅助宏，比如 `hashmap-print-kvcnt`
用来打印 seekdb 自己的 hashmap 结构。

---

## 排障速查

| 症状 | 先看 |
|---|---|
| 查询慢 | `__all_virtual_sql_audit`、`EXPLAIN`、`__all_virtual_plan_cache_stat` |
| 内存涨 | `__all_virtual_memory_info`、`__all_virtual_ctx_memory_info` |
| 写入卡 | `__all_virtual_memstore_info`、`__all_virtual_compaction_diagnose_info` |
| 向量检索异常 | `__all_virtual_vector_index_info` |
| 后台任务堆积 | `__all_virtual_dag` |
| 报错看不懂 | `ob_error <码>` |
| 进程崩溃 | `gdb-macros/auto-analysis.sh` |
| macOS 环境问题 | `seekdbctl doctor` |

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `src/observer/virtual_table/` | 154 个虚拟表实现 |
| `src/observer/virtual_table/ob_virtual_table_scanner_iterator.h` | 虚拟表基类 |
| `src/share/inner_table/ob_inner_table_schema_def.py` | 内部表/视图定义，含 81 处 GV/V 折叠注释 |
| `deps/oblib/src/lib/oblog/ob_log_module.h` | `LOG_*` 宏族 |
| `deps/oblib/src/lib/oblog/ob_log_module.ipp` | 日志模块 ID |
| `deps/oblib/src/lib/alloc/memory_dump.cpp` | 内存统计采集 |
| `src/share/ob_errno.def` | 错误码定义 |
| `tools/ob_error/` | 错误码查询工具 |
| `gdb-macros/auto-analysis.sh` | core 自动分析 |
| `script/sqlaudit/sqlaudit.py` | ⚠️ 使用已删除的 `V$OB_SQL_AUDIT` |

---

## 动手验证

数虚拟表数量：

```bash
ls src/observer/virtual_table/*.h | wc -l
```

看有多少视图被折叠了：

```bash
grep -c "single-tenant GV/V collapse" src/share/inner_table/ob_inner_table_schema_def.py
```

确认 SQL_AUDIT 视图确实被删：

```bash
grep -nE '(GV|V)\$OB_SQL_AUDIT' src/share/inner_table/ob_inner_table_schema_def.py
```

看日志级别定义：

```bash
grep -n "DEBUG\|TRACE\|WDIAG\|EDIAG" deps/oblib/src/lib/oblog/ob_log_level.h | head
```

---

## 延伸阅读

- 第 1 篇到此结束。下一步：
  - 想看内部实现 → [2.1 总体分层与启动](../20-architect/01-layering-and-startup.md)
  - 想改代码 → [3.1 环境与构建](../30-developer/01-build.md)
- [3.4 调试武器库](../30-developer/04-debugging.md) —— 开发者视角的排障
- 附录 C：[参数与虚拟表速查](../90-appendix/C-config-and-views.md)
