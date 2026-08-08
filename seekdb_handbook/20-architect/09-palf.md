# 2.9 日志服务 palf 与单副本裁剪

> **一句话**：palf 是 OceanBase 的 Paxos 日志库，seekdb 完整保留了它，
> 但以单副本模式运行——选举、多数派这些机制在代码里，只是不被行使。

---

## palf 是什么

PALF = Paxos-backed Append-only Log File system。
`src/logservice/palf/`（约 106 个文件）。

它提供三件事：

1. **持久化** —— redo 日志落盘，崩溃后能恢复
2. **复制** —— 多副本间通过 Paxos 达成一致（seekdb 不用）
3. **回放** —— 重启后按日志重建内存状态

---

## 核心对象

```
PalfEnv          环境，进程级
 └── PalfEnvImpl     实现：IO 线程、共享队列、块 GC
      └── PalfHandle     每个 LS 一个句柄
           └── PalfHandleImpl
                ├── LogSlidingWindow   滑动窗口（复制用）
                ├── LogEngine          日志引擎
                ├── LogMeta            元信息
                └── LogState
```

| 类 | 文件 |
|---|---|
| `PalfEnv` | `palf_env.cpp` |
| `PalfEnvImpl` | `palf_env_impl.h:194` |
| `PalfHandle` | `palf_handle.cpp` |
| `LogEntry` | `log_entry.cpp` |
| `LogBlock` | `log_block.cpp`（4MB 一个块） |
| `LogCache` / `LogHotCache` | `log_cache.cpp` |
| `LogReconfirm` | `log_reconfirm.cpp`（leader 重确认） |
| `LogSlidingWindow` | `log_sliding_window.cpp` |

---

## 日志的组织

```
LogEntry           单条日志：header + payload
 └── LogEntryHeader  含 SCN、data_len、type
LogGroupEntry      批量日志（提高吞吐）
LogBlock           4MB 磁盘块
```

批量（group entry）是吞吐优化：
多条日志攒一批一起 fsync，摊薄同步开销。

---

## 两种访问模式

`AccessMode` 枚举：

| 模式 | 用途 |
|---|---|
| `APPEND` | 正常写入新日志 |
| `RAW_WRITE` | 只回放，不产生新日志（恢复/备库用） |

seekdb 正常运行在 `APPEND` 模式。

---

## 上层封装

`src/logservice/`：

| 组件 | 职责 |
|---|---|
| `ObLogService` | 门面，持有 PalfEnv、apply、replay 服务 |
| `ObLogHandler` | 每个 LS 一个，包装 PalfHandle |
| `ObLogApplyService` | 日志提交后的回调链（`ObApplyStatus`） |
| `ObLogReplayService` | 重启时按日志重建状态 |
| `ObLSAdapter` | 桥接 LS 生命周期与 palf |

### Apply vs Replay

容易混的两个概念：

| | Apply | Replay |
|---|---|---|
| 时机 | 日志提交成功后 | **重启后** |
| 作用 | 触发回调（如回填 `trans_version_`） | 重建内存状态 |
| 组件 | `ObLogApplyService` | `ObLogReplayService` |

Replay 时会把日志分发给一组 `ObIReplaySubHandler` 实现者：
`ObLSTabletService`、`ObDDLServiceLauncher`、
`ObTxCtxMemtableMgr` 等——每个模块自己负责重建自己的状态。

---

## seekdb 的裁剪

### 硬编码 LEADER

`ObDDLServiceLauncher::get_sys_palf_role_and_epoch`
（`src/rootserver/ob_ddl_service_launcher.cpp`）
直接返回 `role = LEADER, proposal_id = 1`。

单节点没有选举对象，直接宣布自己是 leader。

### MajorFreeze 简化

`ObMajorFreezeService` 在单副本下：
- `flush()` 直接返回 `OB_SUCCESS`
- `get_rec_scn()` 返回 `max_scn`
- replay 是桩实现

实际合并由 `ObLocalMajorFreeze` 在 tablet 层面触发。

### 拒绝 STANDBY

`ObService::start()`（`src/observer/ob_service.cpp:211`）
对 STANDBY 数据目录返回 `OB_NOT_SUPPORTED`。

---

## 那 palf 还有什么用

即使单副本，palf 仍然承担着关键职责：

| 职责 | 说明 |
|---|---|
| **持久化** | 事务提交必须先写日志，这是 D（Durability）的保证 |
| **崩溃恢复** | 重启后 replay 重建 MemTable |
| **Change Stream 的数据源** | ⭐ 见下 |

### 与 Change Stream 的关系（重要）

这是 seekdb 架构里一个漂亮的复用：

```
事务提交 → 写 palf 日志 → 返回客户端
                ↓
        ObCSFetcher 消费同一份日志
                ↓
        异步更新向量索引
```

**Change Stream 读的就是 palf 的日志**。
这意味着向量索引的异步构建不需要额外的"变更捕获"机制——
数据库为了持久化本来就要写日志，Change Stream 顺便消费它。

这也是为什么写路径可以"提交即返回"：
索引构建所需的信息已经在日志里了，不会丢。

详见 [2.11 Change Stream](11-change-stream.md)。

---

## 归档与恢复

代码里保留了日志归档与恢复的设施
（`ObRestoreMajorFreezeService`、`ObLogRestoreNetDriver`），
主要服务于集群形态。

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/logservice/palf/palf_env.cpp` | `PalfEnv` |
| `src/logservice/palf/palf_env_impl.h:194` | `PalfEnvImpl` |
| `src/logservice/palf/palf_handle.cpp` | `PalfHandle` |
| `src/logservice/palf/log_entry.cpp` | `LogEntry` |
| `src/logservice/palf/log_block.cpp` | 4MB 日志块 |
| `src/logservice/palf/log_sliding_window.cpp` | 滑动窗口 |
| `src/logservice/palf/log_reconfirm.cpp` | leader 重确认 |
| `src/logservice/ob_log_service.cpp` | 日志服务门面 |
| `src/logservice/ob_log_handler.cpp` | 每 LS 句柄 |
| `src/logservice/applyservice/ob_log_apply_service.h` | Apply |
| `src/logservice/replayservice/ob_log_replay_service.cpp` | Replay |
| `src/logservice/ob_log_base_type.h` | `ObIReplaySubHandler` 等接口 |
| `src/rootserver/ob_ddl_service_launcher.cpp` | 硬编码 LEADER |
| `src/observer/ob_service.cpp:211` | 拒绝 STANDBY |

---

## 动手验证

看 palf 的规模：

```bash
ls src/logservice/palf/*.cpp | wc -l
```

看日志条目结构：

```bash
grep -n "class LogEntry\|class LogEntryHeader" src/logservice/palf/log_entry.h src/logservice/palf/log_entry_header.h
```

看回放子处理器接口：

```bash
grep -n "ObIReplaySubHandler\|ObICheckpointSubHandler" src/logservice/ob_log_base_type.h | head
```

---

## 延伸阅读

- 下一章：[★ 2.10 向量索引架构](10-vector-index.md)
- [2.8 事务与 MVCC](08-transaction-mvcc.md) —— 日志与事务提交的关系
- [2.2 seekdb 裁掉了什么](02-what-seekdb-removed.md)
