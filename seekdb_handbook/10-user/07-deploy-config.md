# 1.7 部署与配置

> **一句话**：284 个参数听着吓人，但真正常调的不到 20 个；
> 先搞清楚端口、目录、内存三件事，其余按需再看。

---

## 部署方式一览

| 方式 | 入口 | 适合 |
|---|---|---|
| Docker | `oceanbase/seekdb:latest` | 快速试用 |
| 一键脚本 | `seekdb_install.sh` | Linux 主机 |
| Homebrew | `brew install seekdb` | macOS |
| RPM / DEB | `rpm/`、`package/deb/` | 离线、生产 |
| systemd | `tools/systemd/` | Linux 服务化 |
| OBD | `tools/deploy/obd.sh` | 开发测试集群 |
| Windows MSI | `tools/windows/installer/` | Windows |

---

## 端口

默认值来自 `src/share/parameter/ob_parameter_seed.ipp`：

| 参数 | 默认 | 行 | 用途 |
|---|---|---|---|
| `mysql_port` | **2881** | 54 | MySQL 协议，客户端连这个 |
| `rpc_port` | **2882** | 51 | 内部 RPC |

两者取值范围都是 `(1024, 65536)`。

> ⚠️ **最容易踩的坑**：用 `tools/deploy/obd.sh` 以**非 root** 用户部署时，
> 端口不是 2881。`obd.sh` 里的 `port_gen` 按
> `100 * (uid % 500) + 10000` 计算，通常落在 **10000**。
>
> 这就是为什么官方开发者指南里写的是：
> ```bash
> mysql -uroot -h127.0.0.1 -P10000
> ```
> 而不是 2881。两者都对，取决于你怎么部署的。

---

## 目录

| 参数 | 默认 | 行 | 说明 |
|---|---|---|---|
| `data_dir` | `"store"` | 26 | 数据文件目录 |
| `redo_dir` | `""`（空，跟随 data_dir） | 28 | redo / clog 目录 |
| `datafile_size` | `32M` | 32 | 数据文件初始大小 |

日志默认在 `<安装目录>/log/seekdb.log`。

macOS 通过 pkg 安装时的固定布局（`tools/macpkg/`）：

```
/opt/seekdb/bin/seekdb                    二进制
/opt/seekdb/etc/seekdb/                   配置
/opt/seekdb/var/seekdb/data/              数据
/opt/seekdb/var/seekdb/data/log/          日志
/opt/seekdb/var/seekdb/run/               pid
```

---

## 内存与 CPU

| 参数 | 说明 |
|---|---|
| `memory_limit` | 进程内存上限，`0M` 表示自动 |
| `memory_budget` | 内存预算 |
| `cpu_count` | 可用 CPU 数，`0` 表示自动探测 |
| `workers_per_cpu_quota` | 每 CPU 配额的工作线程数 |
| `net_thread_count` | 网络线程数 |

向量场景要特别关注一个：

```sql
alter system set ob_vector_memory_limit_percentage = 44;
```
*出处：`vector_index/t/vector_index_basic.test`*

向量索引常驻内存，这个百分比决定了它能占多少。默认值偏保守，
大规模向量场景需要调高。

---

## 日志

7 个 syslog 参数（`ob_parameter_seed.ipp` 行 136-151）：

| 参数 | 默认 | 说明 |
|---|---|---|
| `syslog_level` | `INFO`（编译期默认） | `DEBUG`/`TRACE`/`WDIAG`/`EDIAG`/`INFO`/`WARN`/`ERROR` |
| `enable_syslog_recycle` | `False` | 是否自动回收旧日志 |
| `max_syslog_file_count` | `2` | 回收时保留几个文件 |
| `enable_syslog_wf` | — | 是否单独输出 WARN+ 到 `.wf` 文件 |
| `enable_async_syslog` | `True` | 异步写日志 |
| `syslog_io_bandwidth_limit` | `5MB` | 日志 IO 带宽上限 |
| `diag_syslog_per_error_limit` | `200` | 每种错误的诊断日志条数上限 |

> ⚠️ `max_syslog_file_count` 默认 **2** 太小了。
> 官方的单机场景配置 `standalone_default_parameter.extra` 把它调到了 **80**，
> 并同时开启 `enable_syslog_recycle=1`、把 `syslog_level` 降到 `WARN`。
> 注释原文："80 is an empirical value"。生产部署建议对齐这套值。

---

## 参数是怎么组织的

理解这套机制比记住单个参数更有价值。

### 定义：一个 `.ipp` 文件

全部 **284** 个参数定义在
`src/share/parameter/ob_parameter_seed.ipp`，形如：

```cpp
DEF_PARAM(mysql_port, INT, OB_CLUSTER_PARAMETER, "2881", "(1024,65536)",
          "the port number for MySQL protocol", ...);
```

宏（`ob_parameter_macro.h`）会为每个参数生成一个
`ObConfig<type>Item_<name>` 类。用 `.ipp` 而非 `.h` 是为了
不把这堆定义传染给 gtest 的使用者。

### 分类：Section / Scope / EditLevel

`ob_parameter_attr.h` 定义了几个正交维度：

| 维度 | 取值 |
|---|---|
| `Section` | ROOT_SERVICE、LOAD_BALANCE、DAILY_MERGE、LOCATION_CACHE、SSTABLE、LOGSERVICE、CACHE、TRANS、RUNTIME、RPC、OBSERVER、RESOURCE_LIMIT、**AI** |
| `Scope` | CLUSTER / RUNTIME |
| `Source` | DEFAULT / FILE / OBADMIN / CMDLINE / CLUSTER / RUNTIME |
| `EditLevel` | READONLY / STATIC_EFFECTIVE（需重启）/ DYNAMIC_EFFECTIVE（立即生效） |

`EditLevel` 是最实用的一个——它告诉你改完要不要重启。

### 场景化默认值

`src/share/parameter/default_parameter.json` 为不同负载预置了参数组合：
`express_oltp`、`complex_oltp`、`kv`、`ap`、`htap`、`olap`、
`tpcc`、`append_only`、`restore` 等。

`standalone_default_parameter.extra` 是 seekdb 单机形态的额外覆盖。

---

## 系统变量 vs 参数

两套东西，别搞混：

| | 参数（Parameter） | 系统变量（System Variable） |
|---|---|---|
| 改法 | `ALTER SYSTEM SET x = y` | `SET [GLOBAL] x = y` |
| 作用域 | 集群 / 服务端 | 全局 / 会话 |
| 定义位置 | `src/share/parameter/` | `src/share/system_variable/` |
| 例子 | `mysql_port`、`memory_limit` | `ob_query_timeout`、`autocommit` |

系统变量由 `ob_system_variable_init.json` 定义，
经 `gen_ob_sys_variables.py` 生成代码。
单机形态的覆盖在 `standalone_default_system_variable.extra`。

会话级常用的几个（测试用例里频繁出现）：

```sql
SET ob_query_timeout = 100000000;
SET ob_trx_timeout   = 100000000;
SET wait_timeout     = 30000000;
```

---

## systemd 部署

`tools/systemd/` 提供了完整的服务化方案：

| 文件 | 用途 |
|---|---|
| `seekdb.service` | systemd unit |
| `profile/seekdb.cnf` | 配置文件 |
| `pre_install.sh.template` 等 | 安装钩子 |
| `seekdb_systemd_start` / `_stop` | 启停脚本 |

配置文件路径约定为 `/etc/seekdb/seekdb.cnf`。

---

## macOS 与 Windows 的图形化管理

seekdb 在桌面平台上下了不少功夫，这在数据库里挺少见：

**macOS**（`tools/macpkg/`）：
- `seekdbctl` —— 726 行 bash，子命令有
  `start`/`stop`/`restart`/`status`/`logs`/`doctor`/`paths`/`config`/
  `setup`/`boot-status`/`enable-boot`/`disable-boot`/`uninstall`
- 菜单栏 App（SwiftUI，`SeekDBMenuBar.swift`）——状态轮询、一键启停
- 特权 helper（`SeekDBHelper.swift`，XPC）——处理需要 root 的操作
- launchd 守护（`com.seekdb.server.plist`）

`seekdbctl doctor` 是个值得记住的排障入口。

**Windows**（`tools/windows/`）：
- `seekdbConfigurator` —— C# WPF 图形配置向导
- WiX 打包成 MSI
- `seekdb_manage.ps1` —— PowerShell 服务管理

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/share/parameter/ob_parameter_seed.ipp:26` | `data_dir` 默认 `"store"` |
| `src/share/parameter/ob_parameter_seed.ipp:51` | `rpc_port` 默认 2882 |
| `src/share/parameter/ob_parameter_seed.ipp:54` | `mysql_port` 默认 2881 |
| `src/share/parameter/ob_parameter_seed.ipp:136-151` | syslog 系列参数 |
| `src/share/parameter/ob_parameter_macro.h` | `DEF_PARAM` 宏族 |
| `src/share/parameter/ob_parameter_attr.h` | Section / Scope / EditLevel |
| `src/share/parameter/default_parameter.json` | 场景化默认值 |
| `src/share/parameter/standalone_default_parameter.extra` | 单机形态覆盖 |
| `src/share/config/ob_config_manager.cpp` | 参数加载与热更新 |
| `src/share/system_variable/` | 系统变量定义与生成 |
| `tools/deploy/obd.sh` | OBD 包装，含 `port_gen` |
| `tools/systemd/` | systemd 服务化 |
| `tools/macpkg/seekdbctl/seekdbctl` | macOS 管理脚本 |
| `tools/windows/seekdbConfigurator/` | Windows 配置器 |

---

## 动手验证

数一数到底有多少参数：

```bash
grep -c "DEF_" src/share/parameter/ob_parameter_seed.ipp
```

查某个参数的默认值与说明：

```bash
grep -n "DEF_PARAM(memory_limit" src/share/parameter/ob_parameter_seed.ipp
```

看单机形态推荐的日志配置：

```bash
head -30 src/share/parameter/standalone_default_parameter.extra
```

看 OBD 的端口计算逻辑：

```bash
grep -n "port_gen\|10000" tools/deploy/obd.sh | head
```

---

## 延伸阅读

- 下一章：[1.8 可观测性与排障](08-observability.md)
- [0.2 三种形态](../00-orientation/02-three-modes.md)
- [3.1 环境与构建](../30-developer/01-build.md)
