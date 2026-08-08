# §53 REST API 索引

> 🧑‍💻 开发者 · 👤 用户
>
> **一句话定位**:按类别列出所有 `/api/*` 路由,标注方法、用途、版本要求、是否 Enterprise 专属。

---

## 1. 公共端点

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/health` | GET | 健康检查 | v4.3.0+ |
| `/api/capabilities` | GET | 当前 Principal 可用能力 | v4.3.0+ |
| `/api/auth/login` | POST | 用户登录 | v4.3.0+ |
| `/api/auth/logout` | POST | 登出 | v4.3.0+ |
| `/api/auth/refresh` | POST | 刷新 Session | v4.3.0+ |
| `/api/auth/bootstrap` | POST | 首次创建 Admin | v4.3.0+ |
| `/api/auth/mfa/enroll` | POST | 注册 MFA | v4.3.0+ |
| `/api/auth/mfa/confirm` | POST | 确认 MFA | v4.3.0+ |
| `/api/auth/password-reset` | POST | 密码重置 | v4.3.0+ |

---

## 2. Capability 管理(v4.3.5)

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/platform/capabilities` | GET | 读取能力 + 历史 | v4.3.5+ |
| `/api/platform/capabilities/{key}` | PUT | 启用/禁用(带 reason + version) | v4.3.5+ |

---

## 3. Agent 与注册

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/admin/agent/register` | POST | 注册或幂等刷新 | v4.1.0+ |
| `/api/admin/agent/heartbeat` | POST | 心跳 | v4.1.0+ |
| `/api/admin/agent/disable` | POST | 禁用 | v4.1.0+ |
| `/api/admin/agent/enable` | POST | 启用 | v4.1.0+ |
| `/api/admin/agent/revoke` | POST | 撤销 | v4.1.0+ |
| `/api/admin/agent/rotate` | POST | 凭据轮换 | v4.1.0+ |
| `/api/admin/token` | POST | 获取 Admin Token | v4.1.0+ |
| `/api/agents/registry` | GET | 列出安全元数据 | v4.1.0+ |
| `/api/agents/{id}` | GET | 详情 | v4.1.0+ |
| `/api/agents/{id}/posture` | GET | 合规姿态 ⚠️企业版 | v4.3.4+ |
| `/api/agents/{id}/compliance-control` | POST | 控制状态 ⚠️企业版 | v4.3.4+ |
| `/api/agents/{id}/compliance-profile` | POST | 分配 Profile ⚠️企业版 | v4.3.4+ |
| `/api/enrollment/redeem` | POST | 一次性 Token 兑换 | v4.1.0+ |
| `/api/gateway/activate` | POST | 凭据激活 ⚠️企业版 | v4.3.4+ |
| `/api/gateway/evidence` | POST | 提交 Evidence ⚠️企业版 | v4.3.4+ |
| `/api/gateway/remediations/{id}/respond` | POST | 整改 ⚠️企业版 | v4.3.4+ |

---

## 4. 用户与会话

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/users` | GET/POST | 列出/创建用户 | v4.3.0+ |
| `/api/users/{id}` | GET/PATCH | 详情/修改 | v4.3.0+ |
| `/api/users/{id}/mfa` | POST | 强制 MFA | v4.3.0+ |
| `/api/users/{id}/access` | GET | 访问日志 | v4.3.0+ |
| `/api/users/me` | GET | 当前用户信息 | v4.3.0+ |
| `/api/roles` | GET/POST | 角色管理 | v4.3.0+ |
| `/api/sessions` | GET | 我的会话 | v4.3.0+ |
| `/api/sessions/{id}` | DELETE | 终止会话 | v4.3.0+ |
| `/api/delegations` | GET/POST | 委托管理 | v4.3.0+ |

---

## 5. Memory

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/memory` | GET/POST | 列表/创建 | v4.3.0+ |
| `/api/memory/{family_id}` | GET | 读 Family | v4.3.0+ |
| `/api/memory/{family_id}/chain` | GET | 关系链 | v4.3.2+ |
| `/api/memory/{family_id}/versions` | POST | 创建 Version | v4.3.2+ |
| `/api/memory/{family_id}/unavailable` | POST | 逻辑不可用 | v4.3.2+ |
| `/api/memory/{family_id}/quarantine` | POST | 隔离(管理员) | v4.3.2+ |
| `/api/memory/{family_id}/candidates` | POST | 提交候选 | v4.3.2+ |
| `/api/memory/snapshots/{id}/refresh` | POST | 后续 snapshot | v4.3.2+ |
| `/api/memory/snapshots/{id}/resolve` | GET | 解析 | v4.3.2+ |
| `/api/memory/candidates/{id}/activate` | POST | 激活候选 | v4.3.2+ |
| `/api/memory/jobs/run-once` | POST | 触发作业 | v4.3.2+ |
| `/api/memory/jobs/{id}/cancel` | POST | 取消 | v4.3.2+ |
| `/api/memory/jobs/{id}/retry` | POST | 重试 | v4.3.2+ |
| `/api/memory/jobs` | GET | 作业列表 | v4.3.2+ |
| `/api/memory/candidates` | GET | 候选列表 | v4.3.2+ |
| `/api/memory/policies` | GET | 策略元数据 | v4.3.2+ |
| `/api/memory/projections/metrics` | GET | 投影度量 | v4.3.2+ |
| `/api/memory/projections/rebuild` | POST | 重建 | v4.3.2+ |
| `/api/memory-candidates/{id}` | GET/PATCH | 候选详情/决定 | v4.3.2+ |

---

## 6. Knowledge

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/knowledge` | GET/POST | 列表/创建 | v4.3.0+ |
| `/api/knowledge/search` | POST | 5 信号搜索 | v4.3.0+ |
| `/api/knowledge/due_reviews` | GET | 待复习 | v4.3.0+ |
| `/api/knowledge/{id}/review` | POST | 记录复习 | v4.3.0+ |
| `/api/knowledge/{id}/deprecate` | POST | 弃用 | v4.3.0+ |
| `/api/knowledge/edges` | POST | 加边 | v4.3.0+ |
| `/api/knowledge/merge` | POST | 合并 | v4.3.0+ |
| `/api/knowledge/{id}/versions` | POST | 创建版本 | v4.3.0+ |
| `/api/knowledge/{id}` | GET/PATCH/DELETE | 详情/修改/删除 | v4.3.0+ |

---

## 7. Workspace

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/workspaces` | GET/POST | 列表/创建 | v4.3.0+ |
| `/api/workspaces/{id}` | GET/PATCH | 详情/修改 | v4.3.0+ |
| `/api/workspaces/{id}/pause` | POST | 暂停 | v4.3.0+ |
| `/api/workspaces/{id}/recover` | POST | 恢复 | v4.3.0+ |
| `/api/workspaces/{id}/archive` | POST | 归档 | v4.3.0+ |
| `/api/workspaces/{id}/contexts` | POST | 保存上下文 | v4.3.0+ |
| `/api/workspaces/{id}/contexts/chain` | GET | 上下文链 | v4.3.0+ |
| `/api/workspaces/{id}/tasks` | POST | 关联任务 | v4.3.0+ |

---

## 8. Task & Branch & Loop

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/task_plans` | GET/POST | 列表/创建 | v4.3.0+ |
| `/api/task_plans/{id}` | GET | 详情 | v4.3.0+ |
| `/api/task_plans/{id}/start` | POST | 启动 | v4.3.0+ |
| `/api/task_plans/{id}/cancel` | POST | 取消 | v4.3.0+ |
| `/api/task_plans/{id}/steps` | GET | 步骤 | v4.3.0+ |
| `/api/task_plans/{id}/snapshots` | POST | 快照 | v4.3.0+ |
| `/api/task_plans/{id}/fork` | POST | Fork | v4.3.0+ |
| `/api/branches` | POST | Fork Branch | v4.3.0+ |
| `/api/branches/{id}/diff` | GET | Diff | v4.3.0+ |
| `/api/branches/{id}/merge` | POST | Merge | v4.3.0+ |
| `/api/branches/{id}/abandon` | POST | Abandon | v4.3.0+ |
| `/api/loops` | GET/POST | 列表/创建 | v4.3.0+ |
| `/api/loops/{id}/start` | POST | 启动 | v4.3.0+ |
| `/api/loops/{id}/pause` | POST | 暂停 | v4.3.0+ |
| `/api/loops/{id}/resume` | POST | 恢复 | v4.3.0+ |
| `/api/loops/{id}/stop` | POST | 停止 | v4.3.0+ |

---

## 9. Skill / Spec / Harness

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/skills` | POST/GET | 创建/列表 | v4.3.0+ |
| `/api/skills/{id}` | GET/DELETE | 详情/删除 | v4.3.0+ |
| `/api/skills/{id}/acquire` | POST | 获取 Skill | v4.3.0+ |
| `/api/specs` | POST/GET | 创建/列表 | v4.3.0+ |
| `/api/specs/{id}/validate` | POST | 验证 | v4.3.0+ |
| `/api/specs/{id}/versions` | POST | 新版本 | v4.3.0+ |
| `/api/harness/templates` | GET/POST | 模板列表 | v4.3.0+ |
| `/api/harness/templates/{id}/instantiate` | POST | 实例化 | v4.3.0+ |

---

## 10. Collab & Channel & Barrier

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/collab/groups` | POST | 创建协作组 | v4.3.0+ |
| `/api/collab/groups/{id}/members` | POST | 加成员 | v4.3.0+ |
| `/api/channels` | POST/GET | 创建/列表 | v4.3.0+ |
| `/api/channels/{id}/messages` | POST/GET | 消息 | v4.3.0+ |
| `/api/channels/{id}/members` | POST | 加成员 | v4.3.0+ |
| `/api/channels/{id}/archive` | POST | 归档 | v4.3.0+ |
| `/api/channels/{id}/legal-hold` | POST | 法律保留 ⚠️企业版 | v4.3.0+ |
| `/api/barriers` | POST | 创建 Barrier | v4.3.0+ |
| `/api/barriers/{id}/arrive` | POST | 报到 | v4.3.0+ |

---

## 11. Graph

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/graph/neighbors` | POST | 邻接 | v4.3.0+ |
| `/api/graph/reachable` | POST | 可达 | v4.3.0+ |
| `/api/graph/shortest_path` | POST | 最短路径 | v4.3.0+ |
| `/api/graph/context` | POST | 上下文 | v4.3.0+ |
| `/api/graph/stats` | GET | 统计 | v4.3.0+ |
| `/api/graph/subgraph` | POST | 子图 | v4.3.0+ |
| `/api/graph/communities` | POST | 社区 | v4.3.0+ |
| `/api/graph/search` | POST | 搜索 | v4.3.0+ |
| `/api/graph/pagerank` | POST | PageRank | v4.3.0+ |
| `/api/graphs` | GET/POST | Graph 定义列表/创建 | v4.2.0+ |
| `/api/graphs/{id}/versions` | POST | 创建版本 | v4.2.0+ |
| `/api/graphs/{id}/compile` | POST | 编译 | v4.2.0+ |
| `/api/graphs/{id}/publish` | POST | 发布 | v4.2.0+ |
| `/api/graph-runs` | GET/POST | Run 列表/创建 | v4.2.0+ |
| `/api/graph-runs/{id}` | GET | 详情 | v4.2.0+ |
| `/api/graph-runs/{id}/cancel` | POST | 取消 | v4.2.0+ |
| `/api/graph-runs/{id}/claim` | POST | Worker claim | v4.2.0+ |
| `/api/graph-runs/{id}/complete` | POST | Worker complete | v4.2.0+ |
| `/api/graph-executors` | GET | 列出执行器 | v4.2.0+ |
| `/api/graph-triggers` | GET/POST | 触发器 | v4.2.0+ |

---

## 12. Organization ⚠️企业版部分

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/organization/roots` | GET | 根组织 | v4.3.1+ |
| `/api/organization/graph` | GET | 完整图 | v4.3.1+ |
| `/api/organization/search` | GET | 搜索 | v4.3.1+ |
| `/api/organization/nodes/{id}` | GET | 单个详情 | v4.3.1+ |
| `/api/organization/changes` | GET/POST | 变更草稿 | v4.3.1+ |
| `/api/organization/changes/{id}/operations` | POST | 加操作 | v4.3.1+ |
| `/api/organization/changes/{id}/validate` | POST | 校验 | v4.3.1+ |
| `/api/organization/changes/{id}/submit` | POST | 提交 | v4.3.1+ |
| `/api/organization/changes/{id}/undo` | POST | 撤销 | v4.3.1+ |
| `/api/organization/changes/{id}/redo` | POST | 重做 | v4.3.1+ |
| `/api/organization/history` | GET | 历史 | v4.3.1+ |
| `/api/organization/sync/conflicts` | GET | 同步冲突 | v4.3.1+ |

---

## 13. 治理与合规 ⚠️企业版

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/governance/probe` | GET | 验证 Enterprise 对象 | v4.1.0+ |
| `/api/governance/resources` | GET/POST | 资源目录 | v4.1.0+ |
| `/api/governance/policies` | GET/POST | 策略 | v4.1.0+ |
| `/api/governance/decide` | POST | 计算决策 | v4.1.0+ |
| `/api/governance/approvals` | GET/POST | 审批 | v4.1.0+ |
| `/api/governance/approvals/{id}/decision` | POST | 提交决策 | v4.1.0+ |
| `/api/governance/grants` | GET/POST | 限时授权 | v4.1.0+ |
| `/api/governance/grants/{id}/revoke` | POST | 撤销 | v4.1.0+ |
| `/api/governance/emergency` | GET/POST | 应急控制 | v4.1.0+ |
| `/api/governance/emergency/{id}/retry` | POST | 重试 | v4.1.0+ |
| `/api/governance/audit` | GET | 审计 | v4.1.0+ |
| `/api/governance/evidence/export` | GET | 证据导出 | v4.1.0+ |
| `/api/governance/legal-holds` | GET/POST | 法律保留 | v4.1.0+ |
| `/api/compliance/summary` | GET | 合规总览 | v4.3.4+ |
| `/api/compliance/findings` | GET | Findings | v4.3.4+ |
| `/api/compliance/profiles` | GET/POST | Profiles | v4.3.4+ |
| `/api/compliance/profiles/{id}/publish` | POST | 发布 | v4.3.4+ |
| `/api/compliance/exceptions` | GET/POST | 例外 | v4.3.4+ |
| `/api/compliance/exceptions/{id}/{decision}` | POST | 例外决策 | v4.3.4+ |

---

## 14. 审计与日志

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/audit/access` | GET | Entity 访问审计 | v4.3.0+ |
| `/api/audit/workspace` | GET | Workspace 审计 | v4.3.0+ |
| `/api/audit/security-events` | GET | 安全事件 | v4.3.0+ |
| `/api/audit/governance-decisions` | GET | 治理决策 ⚠️企业版 | v4.3.0+ |
| `/api/audit/logs` | GET | 通用日志 | v4.3.0+ |

---

## 15. MCP / Agent Protocol

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/mcp` | POST | MCP JSON-RPC | v3.9.0+ |
| `/api/ap/v1/agent/tasks` | POST | Agent Protocol | v3.9.0+ |
| `/api/agent_gateway/create_instance` | POST | 创建实例 | v4.3.0+ |
| `/api/agent_gateway/heartbeat` | POST | 实例心跳 | v4.3.0+ |
| `/api/agent_gateway/revoke` | POST | 撤销实例 | v4.3.0+ |
| `/api/agent_gateway/claim_events` | POST | 拉取事件 | v4.3.0+ |
| `/api/agent_gateway/acknowledge_event` | POST | 确认事件 | v4.3.0+ |

---

## 16. Approvals

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/approvals` | GET/POST | 列表/创建 | v4.3.0+ |
| `/api/approvals/{id}` | GET | 详情 | v4.3.0+ |
| `/api/approvals/{id}/approve` | POST | 批准 | v4.3.0+ |
| `/api/approvals/{id}/reject` | POST | 拒绝 | v4.3.0+ |

---

## 17. Monitor

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/monitor/overview` | GET | 系统总览 | v4.3.0+ |
| `/api/monitor/agents` | GET | Agent 健康 | v4.3.0+ |
| `/api/monitor/graphs` | GET | Graph Runtime | v4.3.0+ |
| `/api/monitor/stalled` | GET | 卡住 Agent | v4.3.0+ |
| `/api/monitor/alerts` | GET | 告警 | v4.3.0+ |

---

## 18. Deploy / Verify

| 端点 | 方法 | 说明 | 版本 |
|---|---|---|---|
| `/api/deploy/check` | GET | 部署检查 | v4.3.0+ |
| `/api/deploy/version` | GET | 版本 | v4.3.0+ |

---

## 19. 通用规范

| 项 | 规范 |
|---|---|
| **CSRF** | `X-CSRF-Token` header |
| **认证** | `Authorization: Bearer {token}` 或 Cookie |
| **Admin Token** | `X-Admin-Token` header |
| **Agent ID** | `X-Agent-Id` header(MCP/Agent) |
| **Instance** | `X-Agent-Instance` header |
| **Body** | JSON(默认),multipart(上传) |
| **响应** | JSON,`{"result": ..., "error": ...}` |

### 19.1 错误码

| 状态码 | 含义 |
|---|---|
| 200 | OK |
| 400 | INVALID_INPUT |
| 401 | UNAUTHENTICATED |
| 403 | FORBIDDEN / CSRF_FAILED |
| 404 | NOT_FOUND |
| 409 | CAPABILITY_DISABLED / CONFLICT / STALE_LEASE / ALREADY_TERMINAL |
| 429 | RATE_LIMITED |
| 500 | INTERNAL_ERROR |
| 503 | SERVICE_UNAVAILABLE |

---

## 20. 路由总数

| 类别 | 数量 |
|---|---|
| 公共 + 认证 | ~10 |
| Capability | 2 |
| Agent | ~15 |
| User | ~10 |
| Memory | ~20 |
| Knowledge | ~10 |
| Workspace | ~8 |
| Task/Branch/Loop | ~18 |
| Skill/Spec/Harness | ~10 |
| Collab/Channel/Barrier | ~10 |
| Graph | ~20 |
| Organization | ~12 |
| 治理与合规 ⚠️企业版 | ~25 |
| 审计 | ~5 |
| MCP / Agent Protocol | ~8 |
| Approvals | ~4 |
| Monitor | ~5 |
| Deploy | ~2 |
| **总计** | **~194** |

> 📌 与 [`web_app.py`](../../scripts/web_app.py) 实际注册的 ~144 个路由接近(部分通过兼容桥转发到 visualization/server.py)。

---

## 21. 交叉引用

- API 详细文档:[`docs/api-reference.md`](../api-reference.md)
- Web 入口:[§24 FastAPI Web 服务剖析](24-FastAPI-Web服务剖析.md)
- MCP:[§25 MCP Server 与 SKILL 契约](25-MCP-Server与SKILL契约.md)

> 📌 **下一章**:[§54 术语表 Glossary](54-术语表Glossary.md) — Handbook 中涉及的所有术语定义。