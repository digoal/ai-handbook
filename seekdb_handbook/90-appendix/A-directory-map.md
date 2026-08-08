# 附录 A · 目录速查表

> 按目录查"这是干什么的"。配合 [0.3 代码地图](../00-orientation/03-code-map.md) 使用。

---

## 仓库顶层

| 目录 / 文件 | 说明 |
|---|---|
| `src/` | 数据库内核（5,434 个源文件） |
| `deps/oblib/` | 基础库（layer 0-1） |
| `deps/init/` | 第三方依赖清单与下载脚本 |
| `cmake/` | 构建配置、打包、模块分层检查 |
| `rust/sql-nio/` | Rust 网络引擎（静态库） |
| `unittest/` | gtest 单元测试 |
| `tools/` | 部署、测试、平台工具 |
| `docs/` | 官方文档 + 本 handbook |
| `script/` | 运维小脚本 |
| `gdb-macros/` | GDB 辅助 |
| `profile/` | AutoFDO 采样数据 |
| `package/` `rpm/` | 打包 |
| `build.sh` `build.ps1` | 构建入口 |
| `AGENTS.md` | ⭐ 新类去 `Ob` 前缀的新规 |
| `CONTRIBUTING.md` | 贡献流程 |

---

## `src/` 内核

### `src/observer/`（layer 5，6.8MB）

| 子目录 / 文件 | 说明 |
|---|---|
| `main.cpp` | 进程入口 |
| `ob_server.cpp` | `ObServer` 生命周期 |
| `ob_srv_xlator.cpp` | 请求分发 |
| `mysql/` | MySQL 协议、`ObMP*` 命令处理器 |
| `omt/` | `ObServerRuntime`、工作线程、AI 服务缓存 |
| `virtual_table/` | 154 个 `__all_virtual_*` |
| **`change_stream/`** | ⭐ 异步索引管线 |
| **`vector_index/`** | ⭐ 向量索引插件、调度、IVF、KMeans |
| **`ai_service/`** | ⭐ AI 模型 endpoint 管理 |
| `scheduler/` | DAG 调度 |
| `schema/` | schema 服务 SQL 实现 |
| `dbms_job/` `dbms_scheduler/` | 作业调度 |

### `src/sql/`（layer 3，47MB — 最大）

| 子目录 | 说明 |
|---|---|
| `parser/` | Bison / Flex 语法、`ObFastParser` |
| `resolver/` | 语法树 → 语义树 |
| `rewrite/` | 等价改写（~98 文件） |
| `optimizer/` | 代价优化（~147 文件） |
| `code_generator/` | `ObStaticEngineCG` |
| `engine/` | 向量化算子 |
| `engine/expr/` | 表达式实现 |
| **`engine/expr/ob_expr_ai/`** | ⭐ AI_EMBED / COMPLETE / RERANK / PROMPT |
| `engine/vector/` | 向量执行原语 |
| `plan_cache/` | 计划缓存 |
| `das/` | 数据访问服务 |
| **`das/iter/`** | ⭐ 向量 / 全文检索迭代器 |
| `dtl/` | 数据传输层 |
| **`hybrid_search/`** | ⭐ 混合检索 DSL 与翻译 |
| `session/` | 会话管理 |
| `monitor/` | 算子统计 |
| `printer/` | EXPLAIN 输出 |

### `src/storage/`（layer 3，26MB）

| 子目录 | 说明 |
|---|---|
| `memtable/` | MemTable |
| `memtable/mvcc/` | MVCC 引擎 |
| `blocksstable/` | SSTable、宏块微块、编码 |
| `blocksstable/encoding/` | 字典 / RLE / 位压缩 |
| `tablet/` | `ObTablet`、table store |
| `ls/` | 日志流 |
| `tx/` | 事务（~114 文件） |
| `tx_table/` | 提交信息持久化 |
| `tx_storage/` | `ObLSService`、访问服务 |
| `compaction/` | 合并框架（~102 文件） |
| `access/` | 读路径多路归并 |
| `ddl/` | DDL 执行 |
| **`ddl/ob_tablet_fork_task.cpp`** | ⭐ FORK 快照扫描 |
| **`fts/`** | ⭐ 全文分词器 |
| **`retrieval/`** | ⭐ 稀疏检索、BM25、block-max |
| **`vector_index/`** | ⭐ 向量索引刷新 |
| **`vector_type/`** | ⭐ SIMD 距离函数 |
| `lob/` | 大对象 |
| `tablelock/` | 表锁 |
| `deadlock/` | 死锁检测 |
| `multi_data_source/` | MDS 元信息变更 |
| `tmp_file/` | 临时文件（溢出） |
| `slog/` `slog_ckpt/` | 启动日志与检查点 |

### `src/share/`（layer 2，13MB）

| 子目录 / 文件 | 说明 |
|---|---|
| `schema/` | 多版本 schema（~107 文件） |
| `inner_table/` | `__all_*` 内部表定义 |
| `inner_table/sys_package/` | DBMS_* 系统包 SQL |
| `parameter/` | 284 个配置参数 |
| `system_variable/` | 系统变量 |
| `config/` | 参数加载与热更新 |
| `cache/` | KV Cache、危险指针 |
| **`rc/ob_module_provider.h`** | ⭐ `g_mp` 全局模块提供者 |
| **`ai_service/`** | ⭐ AI 模型元信息类型 |
| **`ob_fork_table_info.h`** | ⭐ FORK 元信息 |
| `text_analysis/` | 文本分析 |
| `io/` | IO 框架 |
| `location_cache/` | 位置缓存 |
| `scn.h` | SCN 类型 |
| `ob_errno.def` | 错误码定义 |

### 其他

| 目录 | 说明 |
|---|---|
| `src/logservice/palf/` | Paxos 日志（~106 文件） |
| `src/logservice/applyservice/` | 提交回调 |
| `src/logservice/replayservice/` | 重启回放 |
| `src/rootserver/` | DDL 服务、本地管控 |
| **`src/rootserver/fork_table/`** | ⭐ FORK 服务 |
| `src/rootserver/ddl_task/` | 异步 DDL 任务 |
| `src/rootserver/freeze/` | 冻结与合并 |
| `src/pl/` | PL 引擎 |
| `src/pl/sys_package/` | DBMS_* 实现 |
| `src/objit/` | JIT 支持 |

---

## `deps/oblib/src/lib/`（layer 0）

| 子目录 | 说明 |
|---|---|
| `alloc/` `allocator/` | 内存分配器全家桶 |
| `container/` | `ObArray`、`ObSEArray` 等 |
| `hash/` | `ObHashMap` 等 |
| `string/` | `ObString`（非拥有语义） |
| `oblog/` | 日志宏、级别、模块 |
| **`vector/`** | ⭐ VSAG 适配层 |
| `lock/` | 各种锁，含 `TCRWLock` |
| `charset/` | 字符集 |
| `compress/` | 压缩 |
| `json/` | JSON |
| `net/` | `ObAddr` |
| `thread/` | 线程池 |
| `signal/` | 崩溃捕获 |
| `ob_name_def.h` | 函数名常量 |
| `ob_errno.h` | 错误码 |

---

## `tools/`

| 目录 | 说明 |
|---|---|
| `deploy/obd.sh` | OBD 部署包装 |
| `deploy/mysql_test/test_suite/` | 53 个集成测试套件 |
| `systemd/` | Linux 服务化 |
| `macpkg/` | macOS 安装包 + 菜单栏 App |
| `windows/` | Windows WPF 配置器 + WiX |
| `ob_error/` | 错误码查询工具 |

⭐ = seekdb 相对 OceanBase 新增或强化的部分
