# §22 SQL 迁移脚本导览

> 🧑‍💻 开发者
>
> **一句话定位**:理解 28+ SQL 迁移文件的执行顺序、依赖图、关键表。本章以 Community Edition 为准,Enterprise 扩展用 ⚠️ 标注。

---

## 1. 总体顺序图

```mermaid
flowchart TB
    S1["1_schema.sql<br/>199 张表 - 71 张"]
    S1 --> S2["2_api.sql<br/>96 个 PL/pgSQL 函数"]
    S2 --> S3["3_jobs.sql<br/>pg_cron 任务"]
    S3 --> S4["4_harness_templates.sql<br/>5 个内置 Harness"]
    S4 --> S7["7_v4_0_1_migration.sql<br/>11 张表 + Schema Owner"]
    S7 --> S8R["8_v4_1_0_registration.sql<br/>注册边界"]
    S8R --> S9["9_v4_2_0_graph_engineering.sql<br/>7 张表 - Graph 基础"]
    S9 --> S10["10_v4_2_0_graph_runtime.sql<br/>14 张表 - Runtime"]
    S10 --> S11["11_v4_2_0_graph_control.sql<br/>6 张表 - 控制"]
    S11 --> S12["12_v4_2_0_graph_edge_scope.sql<br/>ALTER - 边作用域"]
    S12 --> S14["14_v4_2_0_graph_triggers.sql<br/>1 张表 - 触发器"]
    S14 --> S15["15_v4_2_1_executor_registry.sql<br/>2 张表 - 内部 closure"]
    S15 --> S16["16_v4_3_0_identity_channels.sql<br/>31 张表 - Identity"]
    S16 --> S17["17_v4_3_0_governance_lifecycle.sql<br/>3 张表"]
    S17 --> S18["18_v4_3_0_security_lifecycle.sql<br/>12 张表"]
    S18 --> S19["19_v4_3_1_organization_governance.sql<br/>13 张表"]
    S19 --> S20["20-22<br/>v4.3.1 辅助 (无新表)"]
    S20 --> S23["23_v4_3_2_memory_lifecycle.sql<br/>13 张表"]
    S23 --> S24["24-27<br/>v4.3.2 辅助"]
    S24 --> S28["28_v4_3_3_graph_assurance.sql<br/>8 张表"]
    S28 --> S31["31_v4_3_5_platform_capabilities.sql<br/>3 张表"]

    style S1 fill:#ffd
    style S31 fill:#9f9
```

> ⚠️ 数字 5、6、13、29、30 故意跳过,留给 Enterprise 或未来扩展。

---

## 2. 迁移文件索引

| # | 文件 | 表数 | 主题 | 版本 |
|---|---|---|---|---|
| 1 | `1_schema.sql` | 71 | 核心 schema | v1.0.0 起 |
| 2 | `2_api.sql` | 0 | PL/pgSQL API | v1.0.0 起 |
| 3 | `3_jobs.sql` | 0 | pg_cron 任务 | v1.0.0 起 |
| 4 | `4_harness_templates.sql` | 0 | Harness 模板 | v1.0.0 起 |
| 5 | (跳过) | - | - | - |
| 6 | (跳过) | - | - | - |
| 7 | `7_v4_0_1_migration.sql` | 11 | baseline | v4.0.1 |
| 8 | `8_v4_1_0_registration.sql` | 1 | 注册边界 | v4.1.0 |
| 9 | `9_v4_2_0_graph_engineering.sql` | 7 | Graph 基础 | v4.2.0 |
| 10 | `10_v4_2_0_graph_runtime.sql` | 14 | Graph Runtime | v4.2.0 |
| 11 | `11_v4_2_0_graph_control.sql` | 6 | Graph 控制 | v4.2.0 |
| 12 | `12_v4_2_0_graph_edge_scope.sql` | 0 (ALTER) | 边作用域 | v4.2.0 |
| 13 | `13_v4_2_0_scheduler_ha.sql` | - | ⚠️ Enterprise only | v4.2.0 |
| 14 | `14_v4_2_0_graph_triggers.sql` | 1 | Graph 触发器 | v4.2.0 |
| 15 | `15_v4_2_1_executor_registry.sql` | 2 | Executor 注册 | v4.2.1 |
| 16 | `16_v4_3_0_identity_channels.sql` | 31 | Identity | v4.3.0 |
| 17 | `17_v4_3_0_governance_lifecycle.sql` | 3 | 治理生命周期 | v4.3.0 |
| 18 | `18_v4_3_0_security_lifecycle.sql` | 12 | 安全生命周期 | v4.3.0 |
| 19 | `19_v4_3_1_organization_governance.sql` | 13 | 组织治理 | v4.3.1 |
| 20 | `20_v4_3_1_human_display_name.sql` | 0 | 显示名 | v4.3.1 |
| 21 | `21_v4_3_1_entry_access.sql` | 0 | 入口访问 | v4.3.1 |
| 22 | `22_v4_3_1_identity_organization_alignment.sql` | 0 | 对齐约束 | v4.3.1 |
| 23 | `23_v4_3_2_memory_lifecycle.sql` | 13 | Memory 生命周期 | v4.3.2 |
| 24 | `24_v4_3_2_memory_digest_alignment.sql` | 0 | 摘要对齐 | v4.3.2 |
| 25 | `25_v4_3_2_disable_legacy_memory_fusion.sql` | 0 | 关闭旧融合 | v4.3.2 |
| 26 | `26_v4_3_2_snapshot_subject_fencing.sql` | 0 (ALTER) | 快照围栏 | v4.3.2 |
| 27 | `27_v4_3_2_memory_governance_completion.sql` | 3 | 治理补全 | v4.3.2 |
| 28 | `28_v4_3_3_graph_assurance.sql` | 8 | Graph 保障 | v4.3.3 |
| 29 | `29_v4_3_4_compliance.sql` | - | ⚠️ Enterprise only | v4.3.4 |
| 30 | `30_v4_3_4_compliance_hardening.sql` | - | ⚠️ Enterprise only | v4.3.4 |
| 31 | `31_v4_3_5_platform_capabilities.sql` | 3 | Platform Capabilities | v4.3.5 |

> 📌 总表数:**199 张**(71 + 0 + 0 + 0 + 11 + 1 + 7 + 14 + 6 + 0 + 1 + 2 + 31 + 3 + 12 + 13 + 0 + 0 + 0 + 13 + 0 + 0 + 0 + 3 + 8 + 3)。

---

## 3. 关键表按域分组

### 3.1 身份与认证

```mermaid
erDiagram
    CX_PRINCIPALS ||--o| CX_HUMAN_IDENTITIES : "HUMAN"
    CX_PRINCIPALS ||--o| AGENT_REGISTRATIONS : "AGENT"
    CX_PRINCIPALS ||--o{ CX_USER_ROLES : "has"
    CX_PRINCIPALS ||--o{ CX_WEB_SESSIONS : "active"
    CX_PRINCIPALS ||--o{ CX_SECURITY_EVENTS : "subject"

    CX_PRINCIPALS {
        string principal_id PK
        string principal_type "HUMAN/AGENT/SERVICE"
        string display_name
        bool portal_access
        bool app_access
        bool organization_required
    }
    AGENT_REGISTRATIONS {
        string agent_id PK
        string owner_ref
        string runtime
        string environment
        string node_id
        jsonb capabilities
        int credential_version
        string status
        timestamp last_seen_at
    }
```

### 3.2 实体多态

```mermaid
erDiagram
    ENTITIES ||--o{ ENTITY_EMBEDDINGS : "has"
    ENTITIES ||--o{ ENTITY_TAGS : "tagged"
    ENTITIES ||--o{ ENTITY_EDGES : "source"
    ENTITIES ||--o{ KNOWLEDGE_META : "KNOWLEDGE subtype"
    ENTITIES ||--o{ HARNESS_META : "HARNESS subtype"
    ENTITIES ||--o{ SPEC_META : "SPEC subtype"

    ENTITIES {
        string entity_id PK
        string entity_type "MEMORY/KNOWLEDGE/SKILL/SPEC/HARNESS/TASK_OUTPUT/EXPERIENCE/OTHER"
        string title
        text content
        text summary
        string category
        int importance
        string status
        string visibility
        string owned_by_agent
        timestamp created_at
        timestamp updated_at
    }
```

> 📌 `entities` 表按 `entity_type` LIST + `created_at` RANGE 双重分区,详见 [`docs/architecture.md:215-260`](../architecture.md)。

### 3.3 Graph Runtime

```mermaid
erDiagram
    GRAPH_DEFINITIONS ||--o{ GRAPH_VERSIONS : "versioned"
    GRAPH_VERSIONS ||--o{ GRAPH_NODES : "has"
    GRAPH_VERSIONS ||--o{ GRAPH_EDGES : "has"
    GRAPH_VERSIONS ||--|| GRAPH_COMPILE_PLANS : "compiled"
    GRAPH_RUNS ||--o{ GRAPH_NODE_RUNS : "has"
    GRAPH_NODE_RUNS ||--o{ GRAPH_ATTEMPTS : "attempts"
    GRAPH_RUNS ||--o{ GRAPH_STATE_EVENTS : "events"
    GRAPH_RUNS ||--o{ GRAPH_CHECKPOINTS : "checkpoints"
    GRAPH_RUNS ||--o{ GRAPH_TRANSITIONS : "transitions"
    GRAPH_RUNS ||--o{ GRAPH_ARTIFACTS : "artifacts"

    GRAPH_RUNS {
        string run_id PK
        string graph_version_id FK
        string status "PENDING/RUNNING/COMPLETED/FAILED/CANCELLED"
        string node_id
        timestamp created_at
    }
    GRAPH_ATTEMPTS {
        string attempt_id PK
        string run_id FK
        string node_run_id FK
        string fencing_token
        string lease_token_hash
        timestamp lease_expires_at
        string idempotency_key
        string effect_idempotency_key
        string status
    }
```

### 3.4 Memory Lifecycle (v4.3.2)

```mermaid
erDiagram
    CX_MEMORY_FAMILIES ||--o{ CX_MEMORY_VERSIONS : "has versions"
    CX_MEMORY_FAMILIES ||--|| CX_MEMORY_CURRENT : "points to current"
    CX_MEMORY_VERSIONS ||--o{ CX_MEMORY_REPRESENTATIONS : "representations"
    CX_MEMORY_VERSIONS ||--o{ CX_MEMORY_SNAPSHOTS : "snapshotted"
    CX_MEMORY_FAMILIES ||--o{ CX_MEMORY_CANDIDATES : "candidate edits"
    CX_MEMORY_FAMILIES ||--o{ CX_MEMORY_JOBS : "jobs"

    CX_MEMORY_VERSIONS {
        string version_id PK
        string family_id FK
        int version_no
        string lifecycle_state "CANDIDATE/ACTIVE/STALE/CONFLICTED/SUPERSEDED/EXPIRED/MIGRATED/ARCHIVED/QUARANTINED/UNAVAILABLE"
        string memory_type "EPISODIC/FACT/PREFERENCE/DECISION/PROCEDURAL/EXPERIENCE"
        string memory_scope "RUNTIME_CONTEXT/CHANNEL_MEMORY/AGENT_MEMORY/WORKSPACE_MEMORY/ENTERPRISE_KNOWLEDGE"
        string content_digest
        string policy_version
        bool immutable
    }
```

### 3.5 Organization (v4.3.1)

```mermaid
erDiagram
    CX_ORGANIZATIONS ||--o{ CX_ORGANIZATION_MEMBERS : "has"
    CX_ORGANIZATIONS ||--o{ CX_REPORTING : "edges"
    CX_ORGANIZATIONS ||--|| CX_ORGANIZATION_CLOSURE : "closure"
    CX_ORGANIZATIONS ||--o{ CX_ORG_VERSIONS : "history"
    CX_ORGANIZATIONS ||--o{ CX_ORG_CHANGESETS : "changes"

    CX_ORGANIZATIONS {
        string organization_id PK
        string organization_code
        string organization_type
        bool is_legal_entity
        int sort_order
        string responsible_principal_id
        string security_domain_id
        timestamp valid_from
        timestamp valid_until
        int row_version
    }
```

### 3.6 Platform Capabilities (v4.3.5)

```mermaid
erDiagram
    CX_PLATFORM_CAPABILITIES ||--o{ CX_PLATFORM_CAPABILITY_HISTORY : "history"
    CX_PLATFORM_CAPABILITIES ||--o{ CX_PLATFORM_CAPABILITY_DEPENDENCIES : "depends"

    CX_PLATFORM_CAPABILITIES {
        string capability_key PK
        char enabled "Y/N"
        char mandatory "Y/N"
        string edition_available "community/enterprise/both"
        int expected_version
        text description
        string updated_by
        timestamp updated_at
    }
    CX_PLATFORM_CAPABILITY_HISTORY {
        string history_id PK
        string capability_key FK
        char old_enabled
        char new_enabled
        text reason
        string actor_principal_id
        int expected_version
        timestamp created_at
    }
```

---

## 4. 加性原则

所有迁移都遵循:

| 原则 | 体现 |
|---|---|
| ✅ 不修改已部署表结构 | 极少有 ALTER 列名/类型 |
| ✅ 不删除列 | 即使列不再使用 |
| ✅ 不改索引名 | 保持兼容 |
| ✅ 加性加表 | 新功能 = 新表 + 新 PL/pgSQL 函数 |
| ✅ 幂等 | `IF NOT EXISTS`、`OR REPLACE` |

> 因此从 v4.0.x 升级到 v4.3.5 **不需要数据迁移**,只需按顺序应用新迁移。

---

## 5. 关键 PL/pgSQL 函数

来源:[`scripts/deploy/2_api.sql`](../../scripts/deploy/2_api.sql)

| Schema | 函数示例 | 用途 |
|---|---|---|
| `memory_fusion` | `fuse_similar`, `extract_knowledge` | 旧版 Memory 整合(已弃用) |
| `knowledge_api` | `schedule_review`, `record_review`, `validate_concept` | 知识复习 |
| `agent_perm` | `check_entity_access`, `check_workspace_access`, `log_access` | RLS 补充 |
| `session_cleanup` | `purge_access_logs`, `archive_old_entities` | 清理 |
| `workspace_manager` | `create`, `save_context`, `get_context_chain` | Workspace |
| `spec_manager` | `create`, `validate`, `derive` | Spec |
| `branch_manager` | `fork`, `merge`, `abandon`, `detect_conflicts` | Branch |
| `skill_manager` | `register`, `update`, `search` | Skill |
| `user_manager` | `create`, `authenticate`, `update_last_login` | User |
| `audit_api` | `log_access_event`, `get_compliance_report` | Audit |
| `ldap_auth` | `configure`, `test_connection` | LDAP (⚠️企业版) |
| `loop_manager` | `check_stop_conditions`, `cleanup_old_runs` | Loop |

> 💡 **设计原则**:业务逻辑优先放在 Python (`lib/`),只在需要"近数据"计算(如 RLS 谓词、批量清理)时用 PL/pgSQL。

---

## 6. 跨数据库差异

| 特性 | Oracle 26ai | PostgreSQL 18 | YashanDB 23.5.4 |
|---|---|---|---|
| 数据类型 | `VARCHAR2`, `CLOB`, `NUMBER` | `VARCHAR`, `TEXT`, `INTEGER` | 类似 Oracle |
| 触发器 | DML triggers | Row-level + statement-level | DML triggers |
| 序列 | `CREATE SEQUENCE` | `CREATE SEQUENCE` / `SERIAL` | `CREATE SEQUENCE` |
| 分区 | LIST + RANGE | LIST + RANGE | LIST + RANGE |
| 全文搜索 | Oracle Text | tsvector + GIN | 内置 |
| 向量 | VECTOR 类型 | pgvector | VECTOR 类型 |
| 图 | Native Property Graph | Apache AGE | Native Property Graph |

> ⚠️ 同一份 Python 代码在三数据库上行为一致,只有 `connection.py` 的 SQL 方言不同。

---

## 7. 迁移测试与回滚

### 7.1 测试

```bash
# 应用到测试库
psql -U ai_agent_runtime -d test_db_clone -f scripts/deploy/1_schema.sql

# 验证
"$PYTHON_BIN" scripts/live_db_validator.py --version 4.3.5
```

### 7.2 回滚

```sql
-- 谨慎使用,平台不支持自动回滚
-- 通常:创建新版本(同事务),应用反向迁移
DROP TABLE IF EXISTS cx_platform_capabilities_history;
DROP TABLE IF EXISTS cx_platform_capability_dependencies;
DROP TABLE IF EXISTS cx_platform_capabilities;
```

> ⚠️ **官方不推荐回滚**,推荐"应用下一版本修复"。

---

## 8. 交叉引用

- 迁移运行:[§47 数据库迁移运维](47-数据库迁移运维.md)
- 现有文档:[`docs/migration.md`](../migration.md)
- 完整索引:[§51 SQL 迁移索引](51-SQL迁移索引.md)

> 📌 **下一章**:[§23 Python 业务模块导览](23-Python业务模块导览.md) — `scripts/lib/` 60+ 模块按领域讲解。