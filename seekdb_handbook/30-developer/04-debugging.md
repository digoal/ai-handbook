# 3.4 调试武器库

> **一句话**：除了常规的 gdb/lldb，seekdb 还有两件专用武器——
> **debug sync**（在内核任意点插入断点，让测试精确控制时序）
> 和 **gdb-macros**（core 文件自动分析）。

---

## 常规调试

### 附加到进程

```bash
gdb -p $(pidof seekdb)
# macOS
lldb -p $(pgrep seekdb)
```

### 版本信息

```bash
./bin/seekdb -V
```

输出 `REVISION` / `BUILD_BRANCH` / `BUILD_TIME` / `BUILD_FLAGS`——
报 bug 时务必附上。

### 常见启动问题

`docs/developer-guide/en/debug.md` 提到：
如果报缺 `libmariadb.so.3`，设置：

```bash
export LD_LIBRARY_PATH=../lib:$LD_LIBRARY_PATH
```

### Debug 构建

```bash
bash build.sh debug --make        # 带断言与符号
bash build.sh debug_no_unity --make   # 报错位置更准
```

---

## 武器一：Debug Sync（内核级断点）

这是 seekdb 最强大的调试/测试机制，值得单独学。

### 它解决什么问题

想复现"fork 进行到 BUILD_DATA 阶段时恰好触发 major merge"这种时序 bug，
靠 sleep 撞运气是不行的。Debug sync 让你**在内核代码里预埋同步点**，
测试时精确控制"执行到这里就停住，等我发信号"。

### 怎么用

真实用法（来自 `fork_table` 测试套件）：

```sql
-- 1. 设置超时
alter system set debug_sync_timeout = '60s';

-- 2. 让内核执行到 FORK_TABLE_BUILD_DATA 点时停住，
--    等待 build_data_signal 信号，最多等 10000 (ms)
set ob_global_debug_sync = 'FORK_TABLE_BUILD_DATA wait_for build_data_signal execute 10000';

-- 3. ... 在另一个会话做点别的事 ...

-- 4. 清除同步点
set ob_global_debug_sync = 'FORK_TABLE_BUILD_DATA clear';
set ob_global_debug_sync = 'reset';
```

真实测试里还有这些同步点用法：

```sql
set ob_global_debug_sync = 'FORK_TABLE_BUILD_DATA wait_for add_column_signal execute 10000';
set ob_global_debug_sync = 'FORK_TABLE_BUILD_DATA wait_for add_partition_signal execute 10000';
```

*出处：`tools/deploy/mysql_test/test_suite/fork_table/t/` 多个用例*

### 同步点在哪定义

`src/share/ob_debug_sync_point.h` 里是所有同步点的枚举。
在内核代码里插一个点：

```cpp
DEBUG_SYNC(FORK_TABLE_BUILD_DATA);
```

Release 构建下这些点会被编译掉，不影响生产性能。

### 什么时候用

| 场景 | 用法 |
|---|---|
| 复现并发时序 bug | 让 A 线程停在关键点，操作 B 线程 |
| 测试 DDL 中途的行为 | 停在 DDL 某阶段，观察表状态 |
| 验证异常路径 | 停住后 kill 进程，测试恢复逻辑 |

---

## 武器二：gdb-macros（core 分析）

```bash
./gdb-macros/auto-analysis.sh
```

它会：
1. 定位 `observer` 二进制和 core 文件
2. 用批处理模式跑 GDB
3. 输出 `bt-all.txt`（全部线程栈）和 `bt.txt`

`gdb-macros/all.gdb` 里有针对 seekdb 数据结构的辅助宏，
比如 `hashmap-print-kvcnt` 打印自研 hashmap 的键值数量。
直接 `p` 这些结构体是看不懂的，得靠这些宏。

---

## 武器三：错误注入（errsim）

```bash
bash build.sh errsim --make
```

errsim 构建允许在指定位置人为注入错误，测试异常处理路径。
相关设施：

- `src/share/ob_ddl_sim_point.h` / `ob_ddl_sim_point_define.h` —— DDL 错误模拟点
- 测试里可以通过 `set_tp`（test point）注入

`tools/deploy/init.sql` 里就有 `set_tp` 的用法。

---

## 日志调试

最朴素也最常用的手段。

### 调高日志级别

```sql
alter system set syslog_level = 'DEBUG';
```

或在配置文件里设。注意 DEBUG 级别日志量巨大，
配合 `syslog_io_bandwidth_limit` 使用。

### 打开 trace

| 参数 | 作用 |
|---|---|
| `enable_record_trace_log` | 记录 trace 日志 |
| `enable_record_trace_id` | 记录 trace ID |
| `trace_log_slow_query_watermark` | 慢查询阈值（默认 1s） |
| `enable_rich_error_msg` | 更详细的错误信息 |
| `enable_perf_event` | 性能事件采集 |

### 加临时日志

```cpp
LOG_INFO("DEBUG-ME", K(some_var), K(another_var));
```

记得提交前删掉。

---

## SQL 层调试

### EXPLAIN

```sql
EXPLAIN SELECT * FROM fts_col_orders WHERE MATCH(b,c) AGAINST("aa");
```
*出处：`fts_index` 测试套件*

看优化器选了什么计划——尤其在调向量/全文检索时必用。

### 计划缓存

```sql
select * from oceanbase.__all_virtual_plan_cache_stat;
```

怀疑"改了参数但没生效"时，先看是不是命中了老计划。

### SQL 审计

```sql
select * from oceanbase.__all_virtual_sql_audit order by request_time desc limit 10;
```

> ⚠️ 不是 `V$OB_SQL_AUDIT`——那个视图已被删除，见
> [1.8 可观测性](../10-user/08-observability.md)。

---

## 错误码

```bash
./ob_error 4379
```

源码 `tools/ob_error/`，覆盖 OS / MySQL / OceanBase 三个域。
错误码定义在 `src/share/ob_errno.def`。

---

## 内存问题

```sql
select * from oceanbase.__all_virtual_memory_info;
select * from oceanbase.__all_virtual_ctx_memory_info;
```

因为每次分配都带 `ObMemAttr(tenant_id, ctx_id, label)`，
所以能直接看出是哪个 label 在涨。

还有一套泄漏检查设施：`src/share/leak_checker/`。

---

## 调试速查

| 症状 | 手段 |
|---|---|
| 进程崩溃 | `gdb-macros/auto-analysis.sh` |
| 并发时序 bug | debug sync |
| 异常路径没覆盖 | errsim 构建 |
| 查询计划不对 | `EXPLAIN` + `__all_virtual_plan_cache_stat` |
| 慢查询 | `__all_virtual_sql_audit` + `trace_log_slow_query_watermark` |
| 内存涨 | `__all_virtual_memory_info` |
| 编译报错看不懂 | 换 `debug_no_unity` 重编 |
| 不知道错误码含义 | `ob_error <码>` |
| macOS 环境问题 | `seekdbctl doctor` |

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `src/share/ob_debug_sync.cpp` / `.h` | debug sync 实现 |
| `src/share/ob_debug_sync_point.h` | 同步点枚举 |
| `src/share/ob_ddl_sim_point.h` | DDL 错误模拟点 |
| `src/share/leak_checker/` | 泄漏检查 |
| `gdb-macros/auto-analysis.sh` | core 自动分析 |
| `gdb-macros/all.gdb` | 数据结构辅助宏 |
| `tools/ob_error/` | 错误码查询 |
| `src/share/ob_errno.def` | 错误码定义 |
| `deps/oblib/src/lib/signal/` | 崩溃信号捕获 |
| `docs/developer-guide/en/debug.md` | 官方调试文档 |

---

## 动手验证

看有哪些 debug sync 点：

```bash
grep -c "" src/share/ob_debug_sync_point.h
grep -n "FORK_TABLE" src/share/ob_debug_sync_point.h
```

看真实测试怎么用 debug sync：

```bash
grep -rn "ob_global_debug_sync" tools/deploy/mysql_test/test_suite/fork_table/t/ | head
```

看 gdb 辅助宏：

```bash
grep -n "^define" gdb-macros/all.gdb
```

---

## 延伸阅读

- 下一章：[3.5 测试体系](05-testing.md)
- [1.8 可观测性与排障](../10-user/08-observability.md) —— 用户视角的排障
- 官方文档：`docs/developer-guide/zh/debug.md`
