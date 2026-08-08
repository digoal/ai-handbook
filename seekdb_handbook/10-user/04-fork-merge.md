# 1.4 FORK / MERGE：给 Agent 的沙箱

> **一句话**：`FORK` 秒级复制一张表或一个库——不拷贝数据，只记一个快照版本号；
> Agent 在副本里随便折腾，满意就 `MERGE` 回主线，不满意就 `DROP`。

![FORK COW](../assets/fork-cow.svg)

---

## 问题：Agent 需要能后悔

Agent 干活的方式是试错：改一批数据、跑一轮、发现不对、回滚重来。
在传统数据库上这很别扭：

- **用事务**？Agent 的一轮探索可能持续几分钟到几小时，长事务会拖垮系统。
- **应用层 save/restore**？要自己序列化状态，容易漏，而且数据量一大就慢。
- **物理复制一份**？几百万行的表，复制一次就是分钟级和双倍存储。

seekdb 的答案是把"分支"下沉到内核，用写时复制（COW）实现。

---

## 基本用法

### FORK TABLE —— 这是测试覆盖最扎实的形式

```sql
fork table t_src to t_fork;
```
*出处：`tools/deploy/mysql_test/test_suite/fork_table/t/` 下 17 个用例*

真实用例里覆盖的场景包括：

| 用例 | 覆盖点 |
|---|---|
| `fork_table_basic.test` | 基本功能，含 range 分区表 |
| `fork_table_cow.test` | 写时复制语义 |
| `fork_table_chain.test` | 链式 fork（`t_a1 → t_b1 → ...`） |
| `fork_table_snapshot.test` | 快照可见性 |
| `fork_table_partition.test` | 分区表 |
| `fork_table_fulltext.test` | 带全文索引的表 |
| `fork_table_lock.test` | 加锁行为 |
| `fork_table_privilege.test` | 权限 |
| `fork_table_ddl.test` / `fork_table_error.test` | DDL 与错误路径 |

甚至连系统表都能 fork（`fork table oceanbase.__all_table to __all_table;`）。

### FORK DATABASE 与 MERGE TABLE

README 的旗舰示例是这样的：

```sql
FORK DATABASE agent_state TO agent_sandbox_42;

USE agent_sandbox_42;
INSERT INTO memory (session_id, embedding, content) VALUES (...);

MERGE TABLE agent_sandbox_42.memory INTO agent_state.memory STRATEGY THEIRS;
-- 或者
DROP DATABASE agent_sandbox_42;
```
*出处：`README.md`*

语法确实存在，在 `src/sql/parser/sql_parser_mysql_mode.y`：

```
FORK DATABASE database_factor TO database_factor          → T_FORK_DATABASE  (行 4409)
MERGE TABLE relation_factor INTO relation_factor          → T_MERGE_TABLE    (行 4439)
MERGE TABLE ... INTO ... STRATEGY FAIL                    → (行 4441)
MERGE TABLE ... INTO ... STRATEGY THEIRS                  → (行 4448)
MERGE TABLE ... INTO ... STRATEGY OURS                    → (行 4455)
```

> ⚠️ **重要提示：这两条语句在仓库里没有测试覆盖。**
>
> 我在 `tools/deploy/mysql_test/` 全量搜索后确认：
> - `FORK DATABASE` —— **0 个用例**
> - `MERGE TABLE ... INTO ...` —— **0 个用例**
> - `STRATEGY FAIL/THEIRS/OURS` —— **0 个用例**
>
> 有测试覆盖的只有 `FORK TABLE`（17 个用例）。
>
> 换句话说，**README 首页的旗舰示例，其中两条语句未被官方测试套件验证**。
> 语法、resolver（`ObMergeTableResolver`）、枚举（`ObMergeTableStrategy`）都实实在在存在，
> 但你在生产里用之前，最好自己先充分验证。
>
> 自行核对：
> ```bash
> grep -rniE "fork database|merge +[a-z_.]+ +into|strategy +(fail|theirs|ours)" tools/deploy/mysql_test/
> ```

---

## 三种 MERGE 策略

定义在 `src/sql/resolver/cmd/ob_merge_table_stmt.h:28`：

```cpp
enum ObMergeTableStrategy
{
  MERGE_STRATEGY_FAIL   = 0,
  MERGE_STRATEGY_THEIRS = 1,
  MERGE_STRATEGY_OURS   = 2,
};
```

| 策略 | 行为 | 什么时候用 |
|---|---|---|
| `FAIL`（默认） | 主键冲突就报错，整体失败 | 期望无冲突，出现冲突说明逻辑有问题 |
| `THEIRS` | 沙箱侧的值覆盖主线 | 相信 Agent 的产出 |
| `OURS` | 保留主线的值，忽略沙箱 | 主线优先，沙箱只补充新行 |

不写 `STRATEGY` 时默认是 `FAIL`（语法文件里的 `strategy_node` 默认取 0）。

`ObMergeTableStmt` 内部持有三段 SQL——`insert_sql_`、`update_sql_`、
`conflict_check_sql_`——由 `ObMergeTableResolver::build_merge_sqls_` 合成。
也就是说，`MERGE TABLE` 在实现上被翻译成了常规 DML 组合，而非一个独立的存储层原语。

---

## COW 到底怎么做到"不拷贝数据"

这是本章最值得理解的一点。

`FORK` 时 seekdb **不复制任何行**，只记录两样东西：

```cpp
// src/share/ob_fork_table_info.h
class ObForkTableInfo {
  uint64 fork_src_table_id_;        // 源表是谁
  int64  fork_snapshot_version_;    // 在哪个版本上分叉
};
```

每个 tablet（分区）再记一条 `ObForkTabletInfo`，指向源 tablet。

后续读取副本时，`ObForkSnapshotRowScan`
（`src/storage/ddl/ob_tablet_fork_task.cpp`）按 `fork_snapshot_version`
去扫**源 tablet 的多版本 SSTable**，并过滤掉
`trans_version > fork_snapshot_version_` 的行。

这就是为什么 fork 是秒级的：**它复用了 LSM-Tree 本来就有的多版本数据**。
存储引擎为 MVCC 保留的历史版本，恰好就是快照隔离需要的东西。

> 💡 这也解释了一个限制：fork 依赖源表的多版本数据仍然存在。
> 如果发生了 major compaction 把老版本合并掉，快照就取不到了。
> `fork_table_merge.test` 专门测试的正是
> "fork 在 BUILD_DATA 阶段遭遇 major merge" 这个场景。

完整机制见 [2.13 FORK / MERGE 的 COW 实现](../20-architect/13-fork-merge-cow.md)。

---

## 典型工作流

```sql
-- 1. 主线状态
USE agent_state;

-- 2. 开一个沙箱（秒级，无数据拷贝）
FORK TABLE memory TO memory_sandbox_42;

-- 3. Agent 在沙箱里自由读写
INSERT INTO memory_sandbox_42 VALUES (...);
UPDATE memory_sandbox_42 SET ... WHERE ...;
DELETE FROM memory_sandbox_42 WHERE ...;

-- 4a. 满意 → 合并回主线
MERGE TABLE memory_sandbox_42 INTO memory STRATEGY THEIRS;

-- 4b. 不满意 → 直接丢弃
DROP TABLE memory_sandbox_42;
```

> ⚠️ 步骤 4a 未被官方测试覆盖，见上文提示。
> 保守做法是先用 `FORK TABLE` + 应用层可控的合并逻辑。

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/sql/parser/sql_parser_mysql_mode.y:4402` | `FORK TABLE` → `T_FORK_TABLE` |
| `src/sql/parser/sql_parser_mysql_mode.y:4409` | `FORK DATABASE` → `T_FORK_DATABASE` |
| `src/sql/parser/sql_parser_mysql_mode.y:4439-4460` | `MERGE TABLE` 四种形式 |
| `src/sql/resolver/ddl/ob_fork_table_resolver.cpp` | FORK TABLE 解析 |
| `src/sql/resolver/ddl/ob_fork_database_resolver.cpp` | FORK DATABASE 解析 |
| `src/sql/resolver/cmd/ob_merge_table_stmt.h:28` | `ObMergeTableStrategy` 枚举 |
| `src/sql/resolver/cmd/ob_merge_table_resolver.cpp` | `build_merge_sqls_` 合成三段 SQL |
| `src/rootserver/fork_table/ob_fork_table_service.cpp` | FORK TABLE 服务 |
| `src/rootserver/fork_table/ob_fork_database_service.cpp` | FORK DATABASE 服务 |
| `src/rootserver/fork_table/ob_fork_table_task.cpp` | 异步 DDL 任务 |
| `src/share/ob_fork_table_info.h` | `ObForkTableInfo` / `ObForkTabletInfo` |
| `src/storage/ddl/ob_tablet_fork_task.cpp` | `ObForkSnapshotRowScan` 快照扫描 |
| `src/storage/ddl/ob_table_fork_info.cpp` | `ObTableForkInfo`、`generate_fork_params` |

---

## 动手验证

看 FORK 语法的完整定义：

```bash
sed -n '4395,4462p' src/sql/parser/sql_parser_mysql_mode.y
```

看官方 fork 用例覆盖了哪些场景：

```bash
ls tools/deploy/mysql_test/test_suite/fork_table/t/
```

亲自确认 MERGE TABLE 没有测试覆盖：

```bash
grep -rniE "fork database|merge +[a-z_.]+ +into|strategy +(fail|theirs|ours)" tools/deploy/mysql_test/ || echo "确实没有"
```

看 COW 的核心——快照版本过滤：

```bash
grep -n "fork_snapshot_version" src/storage/ddl/ob_tablet_fork_task.cpp | head
```

---

## 延伸阅读

- 下一章：[1.5 库内 AI 函数](05-in-db-ai.md)
- [2.13 FORK / MERGE 的 COW 实现](../20-architect/13-fork-merge-cow.md) —— 存储层细节
- [2.6 一行数据的一生](../20-architect/06-lsm-tree.md) —— 多版本数据从哪来
