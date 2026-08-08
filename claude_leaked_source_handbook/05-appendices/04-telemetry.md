# 附录 D · Telemetry 事件目录(`tengu_*` 全清单)

> **本附录定位**:Claude Code CLI 上报的**全量 `tengu_*` 事件索引**(727 个 unique 事件 / 1,053 个 logEvent 调用点)。每个事件一行:**事件名 + 触发时机 + 关键字段 + 文件位置**。读者可以从产品/分析视角快速查到"哪个事件在哪个模块触发"。
>
> 字段的隐私契约与 PII 规则见 [`03-developer/22-telemetry.md`](../03-developer/22-telemetry.md) 与 [`04-architect/33-observability.md`](../04-architect/33-observability.md)。

## D.1 摘要

**实测总数**:`grep -rE "logEvent\s*\(\s*['\"]tengu_"` 命中 **1,053 个调用点**,对应 **727 个 unique 事件名**。事件命名遵循 `tengu_<verb>_<subject>` 模式,部分前缀带 `internal_` 或 `session_` 表示生命周期/会话阶段。本附录按主题分类列举所有 727 个事件。

## D.2 速赢

1. **总量**:**727 unique 事件 / 1,053 logEvent 调用点**。
2. **错误类 ~92**:以 `_error`、`_failed`、`parse_error`、`crash` 结尾的事件最多。
3. **工具类 ~51**:`tool_use_*` 与 `*_tool_*` 子集是 L3 调度最热的可观测面。
4. **会话/输入 ~32**:`session_*` / `input_*` / `message_*` 跨越 REPL ↔ LLM 主链路。
5. **权限 ~12**:permission decision、ask 频次、auto mode circuit breaker。
6. **ant-only 内部 4 个**:`tengu_internal_*` 前缀,仅 ant 构建发出。
7. **采样**:OTel trace 默认 1%(可调 `OTEL_TRACES_SAMPLER_ARG`),metric 100%。

## D.3 事件分类索引

> 表格字段:**事件名 | 触发时机 | 关键字段 | 文件位置**。
> "调用数"指 `logEvent(...)` 出现次数(影响聚合字段的权重)。

### D.3.1 启动与初始化(startup / init)(3)

| 事件 | 触发时机 | 关键字段 | 文件位置 |
|---|---|---|---|
| `tengu_startup_telemetry` | CLI 启动时一次性 | 版本、commit、env 维度 | `main.tsx` 等多文件 |
| `tengu_startup_perf` | 启动时性能基线 | 阶段计时 | (启动探针) |
| `tengu_init_*` | `/init` 命令执行 | 文件路径 | `src/commands/init.ts` |

### D.3.2 工具执行(tool use / execution)(51)

| 事件 | 触发时机 | 关键字段 | 文件位置 |
|---|---|---|---|
| `tengu_tool_use_*` 系列(20+) | 工具调用前/中/后 | `toolName`、`toolUseID`、`durationMs`、`isError` | `src/services/tools/toolExecution.ts`、`StreamingToolExecutor.ts` |
| `tengu_tool_use_cancelled` | 工具被 abort | `toolName`、`isMcp`、`toolUseID` | `src/services/tools/toolExecution.ts:415` |
| `tengu_tool_use_error` | 工具不存在 / 抛出 | `toolName`、`error` | `src/services/tools/toolExecution.ts:372` |
| `tengu_tool_use_success` | 工具正常完成 | `toolName`、`latencyMs` | (各处) |
| `tengu_tool_use_show_permission_request` | 弹出权限请求 UI | `toolName`、`decision` | `components/permissions/...` |
| `tengu_tool_use_search_*` | ToolSearch 命中/未命中 | `query`、`resultCount` | `src/utils/toolSearch.ts` |
| `tengu_tool_use_completed` | 工具返回 | `toolName`、`durationMs`、`toolUseID` | (多处) |
| `tengu_tool_pear` *(GrowthBook 守门)* | strict 工具模式 | `toolName` | `services/api/claude.ts` |

### D.3.3 权限(permissions)(12)

| 事件 | 触发时机 | 关键字段 | 文件位置 |
|---|---|---|---|
| `tengu_permission_decision` | 权限检查做出决定 | `toolName`、`decision`、`reason` | `src/utils/permissions/PermissionResult.ts` |
| `tengu_permission_request` | 弹出权限 UI | `toolName` | `components/permissions/PermissionRequest.tsx` |
| `tengu_permission_modal_*` | 模式切换 | `from`、`to` | `useCanUseTool.ts` |
| `tengu_permission_rule_added` / `_removed` | 用户增删规则 | `rule`、`destination` | `src/utils/permissions/PermissionUpdate.ts` |
| `tengu_auto_mode_*` | Auto 模式开/关/circuit break | `mode`、`reason` | `src/utils/permissions/autoModeState.ts` |
| `tengu_ask_user_question_*` | AskUserQuestion 选择 | `toolUseID`、`accepted` | `components/PromptInput/AskUserQuestion.tsx` |
| `tengu_permission_denied_*` | 拒绝统计 | `toolName`、`count` | `useCanUseTool.ts` |
| `tengu_bash_permission_*` | Bash 权限决策 | `command`、`decision` | `src/tools/BashTool/bashPermissions.ts` |
| `tengu_classifier_*` | Classifier 评估结果 | `decision`、`confidence` | (Auto Mode 路径) |

### D.3.4 错误 / 失败(errors / failures)(92)

> 命名约定:`*_error`、`*_failed`、`*_failure`、`parse_error`、`*_crash`、`*_parse`、`recover_*`。统计包含:`tengu_tool_use_error`、`tengu_agent_parse_error`、`tengu_agent_stop_hook_error`、`tengu_session_*_error`、`tengu_command_*_error`、`tengu_settings_*_error`、`tengu_oauth_*_error`、`tengu_mcp_*_error`、`tengu_compact_*_error`、`tengu_image_*_error`、`tengu_bridge_*_error` 等。完整列表见 §D.4。

### D.3.5 性能 / 时延(performance / timing)(9)

| 事件 | 触发时机 | 关键字段 | 文件位置 |
|---|---|---|---|
| `tengu_api_query` / `_success` / `_error` / `_retry` | API 调用阶段 | `model`、`durationMs`、`tokens` | `src/services/api/claude.ts` |
| `tengu_compact_*_latency` | 压缩各阶段耗时 | `stage`、`ms` | `src/services/compact/...` |
| `tengu_api_cache_breakpoints` | 缓存断点变更 | `count`、`trigger` | `services/api/claude.ts` |
| `tengu_compact_*_duration` | 压缩耗时 | `durationMs` | `src/services/compact/autoCompact.ts` |
| `tengu_microcompact_*` | microcompact 行为 | `tokens`、`durationMs` | `src/services/compact/microCompact.ts` |
| `tengu_api_persistent_retry_wait` | 重试等待 | `attempt`、`waitMs` | `services/api/withRetry.ts` |

### D.3.6 会话 / 输入 / 消息(session / input / message)(32)

| 事件 | 触发时机 | 关键字段 | 文件位置 |
|---|---|---|---|
| `tengu_session_init` | 新会话初始化 | `sessionId`、`cwd` | `main.tsx` |
| `tengu_session_resume_*` | `/resume` 恢复 | `sessionId`、`messageCount` | `src/utils/processUserInput/processSlashCommand.tsx` |
| `tengu_session_cwd_changed` | cwd 变更 | `from`、`to` | `src/utils/Shell.ts` |
| `tengu_session_cwd_skip` | cwd 变更被跳过 | `reason` | (同上) |
| `tengu_session_persistence_disabled` | 关闭持久化 | `reason` | `bootstrap/state.ts` |
| `tengu_input_command` | `/` 命令触发 | `command_name`、`_PROTO_plugin_*` | `src/utils/processUserInput/processSlashCommand.tsx:469` |
| `tengu_input_slash_missing` | 未以 `/` 开头 | `{}` | `src/utils/processUserInput/processSlashCommand.tsx:305` |
| `tengu_input_slash_invalid` | 未知命令名 | `input` | `src/utils/processUserInput/processSlashCommand.tsx:258` |
| `tengu_user_prompt_submit` | 用户提交 prompt | `length` | `src/utils/hooks.ts` |
| `tengu_message_*` | 消息计数 | `type`、`count` | `utils/messages.ts` |
| `tengu_session_history_count` | 历史计数 | `count` | `utils/sessionStorage.ts` |

### D.3.7 MCP(28)

包括 `tengu_mcp_server_connected`、`tengu_mcp_server_failed`、`tengu_mcp_server_pending`、`tengu_mcp_auth_*`、`tengu_mcp_resource_*`、`tengu_mcp_tool_*`、`tengu_mcp_ide_*`、`tengu_mcp_reconnect_*` 等。覆盖连接生命周期(connected/failed/pending/disabled)、OAuth 流程、IDE 集成、tool/resource 解析。

### D.3.8 Bridge(29)

包括 `tengu_bridge_*` 系列与 `tengu_repl_bridge_*`,覆盖:
- `tengu_bridge_session_created`、`tengu_bridge_session_connected`、`tengu_bridge_session_disconnected`
- `tengu_bridge_message_sent`、`tengu_bridge_message_received`
- `tengu_bridge_permission_*`、`tengu_bridge_control_*`
- `tengu_repl_bridge_*`(本地 REPL ↔ 远端)

### D.3.9 Plugins / Skills(22)

- `tengu_plugin_loaded`、`tengu_plugin_unloaded`、`tengu_plugin_install_*`、`tengu_plugin_marketplace_*`
- `tengu_skill_loaded`、`tengu_skill_invoked`、`tengu_skill_search_*`、`tengu_skill_improvement_*`

### D.3.10 OAuth(30)

`/login` → `OAuthFlow` 流程:授权 URL、token 交换、刷新、撤销、3P 切换。详细 30 个事件贯穿 `src/utils/auth.ts` 与 `src/services/oauth/`。

### D.3.11 Team / Teammate(16)

`tengu_team_created`、`tengu_team_deleted`、`tengu_teammate_spawned`、`tengu_teammate_idle`、`tengu_teammate_killed`、`tengu_team_message_*`、`tengu_swarm_*`、`tengu_inbox_*` 等。

### D.3.12 工具相关子集

- **Memory(3)**:`tengu_memory_loaded`、`tengu_memory_extracted`、`tengu_memory_written`
- **Compact(11)**:`tengu_compact_start`、`tengu_compact_end`、`tengu_compact_failure`、`tengu_compact_latency`、`tengu_auto_compact_*`、`tengu_reactive_compact_*`、`tengu_session_memory_compact_*`、`tengu_microcompact_*`、`tengu_snippet_*`
- **API client(10)**:`tengu_api_query`、`tengu_api_success`、`tengu_api_error`、`tengu_api_retry`、`tengu_api_after_normalize`、`tengu_api_before_normalize`、`tengu_api_529_*`、`tengu_api_opus_fallback_triggered`、`tengu_api_persistent_retry_wait`、`tengu_api_cache_breakpoints`
- **Settings(6)**:`tengu_settings_changed`、`tengu_settings_sync_*`、`tengu_settings_load_failed`、`tengu_settings_save_failed`、`tengu_settings_reload_*`
- **Voice(5)**:`tengu_voice_enabled`、`tengu_voice_disabled`、`tengu_voice_transcribed`、`tengu_voice_error`、`tengu_voice_wakeword`
- **Worktree(5)**:`tengu_worktree_created`、`tengu_worktree_removed`、`tengu_worktree_failed`、`tengu_worktree_resumed`、`tengu_worktree_archived`
- **Rate limit(3)**:`tengu_rate_limit_hit`、`tengu_rate_limit_options_*`、`tengu_rate_limit_recovered`

### D.3.13 Hooks(2)

- `tengu_hook_executed`(任意 hook)
- `tengu_hook_failed`(hook 退出非零)

### D.3.14 Resume(2)

`/resume` 相关事件:`tengu_resume_started`、`tengu_resume_completed`。

### D.3.15 Slash command(1)

- `tengu_slash_command_forked`(`context: 'fork'` 启动)

### D.3.16 Ant-only internal(4)

| 事件 | 触发时机 | 关键字段 | 文件位置 |
|---|---|---|---|
| `tengu_internal_*`(4 个) | 内部构建专属行为 | 见代码 | ant 构建仅 |

### D.3.17 其他分类

| 分类 | 数量 | 代表事件 |
|---|---:|---|
| Cost | 2 | `tengu_cost_*` |
| Status | 4 | `tengu_status_*` |
| Query | 4 | `tengu_query_*` |
| Remote | 4 | `tengu_remote_*` |
| Review | 4 | `tengu_review_*` |
| Ultraplan | 4 | `tengu_ultraplan_*` |
| Bash | 3 | `tengu_bash_*` |
| Insight | 2 | `tengu_insights_*` |
| Exit | 1 | `tengu_exit_*` |
| Fork | 1 | `tengu_fork_*` |
| Image | 1 | `tengu_image_*` |
| Keybindings | 1 | `tengu_keybinding_*` |
| Mode | 1 | `tengu_mode_*` |
| Speculation | 1 | `tengu_speculation_*` |
| Resilience | 1 | `tengu_recovery_*` |

## D.4 全量 `tengu_*` 事件名(727 个 unique)

> 完整列表以**事件名 + 触发文件:行号**格式给出。源码定位可直接 `codegraph_explore` 或 `git grep`。以下按字母顺序展示,完整 727 项见原文清单。

```
tengu_1p_event_batch_config                          services/analytics/firstPartyEventLogger.ts:87
tengu_accept_feedback_mode_collapsed                 components/permissions/PermissionPrompt.tsx:153
tengu_accept_feedback_mode_entered                   components/permissions/PermissionPrompt.tsx:157
tengu_accept_submitted                               components/permissions/PermissionPrompt.tsx:204
tengu_advisor_tool_call                              services/api/claude.ts:2011
tengu_advisor_tool_interrupted                       services/api/claude.ts:2444
tengu_advisor_tool_token_usage                       cost-tracker.ts:306
tengu_agent_color_set                                utils/sessionStorage.ts:2853
tengu_agent_created                                  components/agents/new-agent-creation/wizard-steps/ConfirmStepWrapper.tsx:51
tengu_agent_definition_generated                     components/agents/generateAgent.ts:187
tengu_agent_flag                                     main.tsx:2069
tengu_agent_memory_loaded                            main.tsx:2158
tengu_agent_name_set                                 utils/sessionStorage.ts:2832
tengu_agent_parse_error                              tools/AgentTool/loadAgentsDir.ts:332
tengu_agent_stop_hook_error                          utils/hooks/execAgentHook.ts:257
tengu_agent_stop_hook_max_turns                      utils/hooks/execAgentHook.ts:242
tengu_agent_stop_hook_success                        utils/hooks/execAgentHook.ts:287
tengu_agent_tool_completed                           tools/AgentTool/agentToolUtils.ts:322
tengu_agent_tool_remote_launched                     tools/AgentTool/AgentTool.tsx:466
tengu_agent_tool_selected                            tools/AgentTool/AgentTool.tsx:419
tengu_agent_tool_terminated                          tools/AgentTool/AgentTool.tsx:997
tengu_agentic_search_cancelled                       components/LogSelector.tsx:973
tengu_agentic_search_completed                       components/LogSelector.tsx:815
tengu_agentic_search_error                           components/LogSelector.tsx:828
tengu_agentic_search_started                         components/LogSelector.tsx:801
tengu_api_529_background_dropped                     services/api/withRetry.ts:319
tengu_api_after_normalize                            services/api/claude.ts:1318
tengu_api_before_normalize                           services/api/claude.ts:1314
tengu_api_cache_breakpoints                          services/api/claude.ts
tengu_api_custom_529_overloaded_error                services/api/withRetry.ts
tengu_api_error                                      services/api/claude.ts
tengu_api_key_keychain_error                         utils/auth.ts
tengu_api_key_saved_to_config                        utils/auth.ts
tengu_api_key_saved_to_keychain                      utils/auth.ts
tengu_api_opus_fallback_triggered                    services/api/claude.ts
tengu_api_persistent_retry_wait                      services/api/withRetry.ts
tengu_api_query                                      services/api/claude.ts
tengu_api_retry                                      services/api/withRetry.ts
tengu_api_success                                    services/api/claude.ts
tengu_ask_user_question_accepted                     components/PromptInput/AskUserQuestion.tsx
tengu_ask_user_question_finish_plan_interview        utils/planModeV2.ts
tengu_ask_user_question_rejected                     components/PromptInput/AskUserQuestion.tsx
tengu_ask_user_question_respond_to_claude            components/PromptInput/AskUserQuestion.tsx
tengu_at_mention_agent_not_found                     utils/teammateMailbox.ts
tengu_at_mention_agent_success                       utils/teammateMailbox.ts
... (其余 ~680 个事件名略,可由 grep -rEo "tengu_[a-z0-9_]+" 还原完整列表)
```

> **完整 727 事件列表**:由于体量限制(>50KB),完整表以 grep 结果为准。运行:
> ```bash
> cd /Users/digoal/new/claude-code-main
> grep -rohE "logEvent\(\s*['\"]tengu_[a-z0-9_]+['\"]" src/ | sort -u | wc -l   # → 727
> grep -rohE "logEvent\(\s*['\"]tengu_[a-z0-9_]+['\"]" src/ | sort | uniq -c | sort -rn | head -20
> ```
> 可在本地环境完整复制此清单。

## D.5 隐私与采样约束

- **PII 守门**:所有 metadata 必须 cast 为 `AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS = never`(`src/services/analytics/index.ts:18`)。
- **`_PROTO_*` 字段**:plugin metadata 通过 `stripProtoFields` 自动剥离(`src/services/analytics/index.ts:44-57`),只透传给 SDK consumer。
- **采样**:OTel trace 默认 1%;`OTEL_TRACES_SAMPLER_ARG` 可调;`parent_based` + `traceidratio` 组合。
- **Privacy level**:`essential`(默认开)、`optional`(受 settings 控制)、`off`(`DISABLE_TELEMETRY=1` 或 settings.telemetry = 'off')。
- **Sink killswitch**:`src/services/analytics/sinkKillswitch.ts:1-25` 紧急下线某个 sink。

## D.6 反模式

### ❌ 不 cast marker

```typescript
// 错误:绕过类型检查,容易塞进代码/路径
logEvent('custom_event', { anything: x })

// 正确
logEvent('custom_event', { anything: x } as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS)
```

### ❌ 不 strip `_PROTO_*`

```typescript
// 错误:plugin metadata 被上报 Datadog
logEvent('tengu_input_command', { command_name, plugin_name })
// 正确(由 stripProtoFields 在 analytics/index.ts:44-57 自动剥离)
```

### ❌ 高频阻塞

```typescript
// 错误:每 token 一次,会拖慢主循环
function onToken(t: Token) { logEvent('token', { t }) }
// 正确:聚合上报
setInterval(() => logEvent('token_batch', { count: tokenBatch.length }), 1000)
```

## D.7 引用

- [`03-developer/22-telemetry.md`](../03-developer/22-telemetry.md) — 体系结构、采样、隐私门控
- [`04-architect/33-observability.md`](../04-architect/33-observability.md) — tracing 后端(session / beta / Perfetto / BigQuery)
- [`05-appendices/05-build-flags.md`](05-build-flags.md) — 同步的 GrowthBook 软开关(`tengu_*` 键)