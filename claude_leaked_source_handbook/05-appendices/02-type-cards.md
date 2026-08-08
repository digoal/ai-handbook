# 附录 B · 关键 TypeScript 类型卡片(Type Cards)

> **本附录定位**:为整本 handbook 准备一份"翻得到、可对照、含真实行号"的**类型字典**。每张卡片包含:**完整定义 + 用途 + 关键字段 + 引用位置 + 反模式**。读者可以从 `Tool` 一路查到 `RemoteAgentTaskState`。
>
> 词汇以 [`00-front/03-glossary.md`](../00-front/03-glossary.md) 为准;分层坐标见 [`04-architect/25-layered-arch.md`](../04-architect/25-layered-arch.md) 的 L3/L4 边界。

## B.1 摘要

Claude Code 内部 20+ 关键类型构成"骨架图"——**Tool 合约族**定义 L4 抽象,**Message 联合**串联 L2↔L3↔L5 的数据流,**AppState 仓库**统一横切状态。**注意**:`src/types/message.ts` 在当前快照中已被合并到 `src/utils/mailbox.ts` 与 `src/components/Message.tsx`,消费方多以 `import type { Message } from 'src/types/message.js'` 的路径;`src/types/message.ts` 不再是真实文件,本附录按实际消费方列举子类型。

## B.2 速赢

1. **L4 合约层**:`Tool`、`Tools`、`ToolUseContext`、`ToolPermissionContext`、`ToolResult`。
2. **L4 命令层**:`Command`、`PromptCommand`、`LocalCommand`、`LocalJSXCommand`、`CommandBase`、`CommandAvailability`。
3. **L3 调度**:`QueryEngineConfig`、`QueryEngine` 类。
4. **L3 工具调度**:`StreamingToolExecutor`、内部 `TrackedTool`、`ToolStatus`。
5. **权限判别**:`PermissionBehavior`、`PermissionDecision`、`PermissionResult`、`PermissionDecisionReason`(11 种类型)。
6. **状态/会话**:`AppState`、`AppStateStore`、`Store<T>`(原生通用)、`SessionKind`、`SessionStatus`、`TaskContext`、`TaskStateBase`、`RemoteAgentTaskState`。
7. **Agent 体系**:`BaseAgentDefinition`、`BuiltInAgentDefinition`、`CustomAgentDefinition`、`PluginAgentDefinition`、`AgentDefinition`、`AgentDefinitionsResult`、`ResolvedAgentTools`。
8. **Hook/Memory/事件**:`HookExecutionEvent`、`MemoryType`(7 种值)。

## B.3 目录卡片

### B.3.1 `Tool<Input, Output, P>` — 工具合约的母类型

**完整定义**(`src/Tool.ts:362-695`):

```typescript
export type Tool<
  Input extends AnyObject = AnyObject,
  Output = unknown,
  P extends ToolProgressData = ToolProgressData,
> = {
  aliases?: string[]
  searchHint?: string                            // ToolSearch 关键词
  call(
    args: z.infer<Input>,
    context: ToolUseContext,
    canUseTool: CanUseToolFn,
    parentMessage: AssistantMessage,
    onProgress?: ToolCallProgress<P>,
  ): Promise<ToolResult<Output>>
  description(
    input: z.infer<Input>,
    options: {
      isNonInteractiveSession: boolean
      toolPermissionContext: ToolPermissionContext
      tools: Tools
    },
  ): Promise<string>
  readonly inputSchema: Input
  readonly inputJSONSchema?: ToolInputJSONSchema  // MCP 工具直接用 JSON Schema
  outputSchema?: z.ZodType<unknown>
  inputsEquivalent?(a: z.infer<Input>, b: z.infer<Input>): boolean
  isConcurrencySafe(input: z.infer<Input>): boolean
  isEnabled(): boolean
  isReadOnly(input: z.infer<Input>): boolean
  isDestructive?(input: z.infer<Input>): boolean
  interruptBehavior?(): 'cancel' | 'block'       // 用户敲新消息时是否终止
  isSearchOrReadCommand?(input): { isSearch: boolean; isRead: boolean; isList?: boolean }
  isOpenWorld?(input: z.infer<Input>): boolean
  requiresUserInteraction?(): boolean
  isMcp?: boolean
  isLsp?: boolean
  shouldDefer?: boolean                          // ToolSearch 延迟加载
  alwaysLoad?: boolean                           // 永远不延迟(MCP `_meta['anthropic/alwaysLoad']`)
  mcpInfo?: { serverName: string; toolName: string }
  readonly name: string
  maxResultSizeChars: number                     // 超过此值则持久化到磁盘
  readonly strict?: boolean                       // tengu_tool_pear 启用时严格遵循 schema
  backfillObservableInput?(input: Record<string, unknown>): void
  validateInput?(input, context): Promise<ValidationResult>
  checkPermissions(input, context): Promise<PermissionResult>
  getPath?(input): string
  preparePermissionMatcher?(input): Promise<(pattern: string) => boolean>
  prompt(options: { ... }): Promise<string>
  userFacingName(input): string
  userFacingNameBackgroundColor?(input): keyof Theme | undefined
  isTransparentWrapper?(): boolean
  getToolUseSummary?(input): string | null
  getActivityDescription?(input): string | null
  toAutoClassifierInput(input): unknown
  mapToolResultToToolResultBlockParam(content: Output, toolUseID: string): ToolResultBlockParam
  renderToolResultMessage?(content, progressMessagesForMessage, options): React.ReactNode
  extractSearchText?(out: Output): string
  renderToolUseMessage(input, options): React.ReactNode
  isResultTruncated?(output): boolean
  renderToolUseTag?(input): React.ReactNode
  renderToolUseProgressMessage?(progressMessagesForMessage, options): React.ReactNode
  renderToolUseQueuedMessage?(): React.ReactNode
  renderToolUseRejectedMessage?(input, options): React.ReactNode
  renderToolUseErrorMessage?(result, options): React.ReactNode
  renderGroupedToolUse?(toolUses, options): React.ReactNode | null
}
```

- **用途**:所有内建工具(Bash、Read、Edit、Grep...)以及 MCP 接入的外部工具都实现 `Tool<Input, Output, P>`。约 40 个可选方法,围绕"LLM 可见契约 + 宿主渲染反馈"两个轴展开。
- **关键字段**:
  - `call`:主执行函数,返回 `ToolResult<Output>`。
  - `isConcurrencySafe`:决定 `StreamingToolExecutor` 是否并行(返回 `true`)还是串行(返回 `false`)。
  - `interruptBehavior`:用户敲新消息时的行为(`cancel` 丢弃 / `block` 等待,默认 `block`)。
  - `isSearchOrReadCommand`:UI 把"grep/find/cat/head"折叠成紧凑行。
  - `isDestructive`:决定是否高危提示。
  - `maxResultSizeChars`:超过阈值则改写为文件路径引用,避免 token 爆炸。
- **引用位置**:81 个工具实现都基于此类型(`src/cli/print.ts`、`src/components/PromptInput/PromptInput.tsx` 等)。

### B.3.2 `Tools` — 工具集合类型

**完整定义**(`src/Tool.ts:701`):

```typescript
export type Tools = readonly Tool[]
```

- **用途**:替代 `Tool[]`,让"在哪里组装工具集"显式可追踪。所有上层(`query.ts`、`ToolUseContext.options.tools` 等)都使用 `Tools` 而非 `Tool[]`。
- **引用位置**:`src/QueryEngine.ts:39`(`type Tools` 导入)、`src/services/tools/toolExecution.ts:343`、`src/tools.ts` 等。

### B.3.3 `ToolUseContext` — 工具调用上下文

**完整定义**(`src/Tool.ts:158-300`):

```typescript
export type ToolUseContext = {
  options: {
    commands: Command[]
    debug: boolean
    mainLoopModel: string
    tools: Tools
    verbose: boolean
    thinkingConfig: ThinkingConfig
    mcpClients: MCPServerConnection[]
    mcpResources: Record<string, ServerResource[]>
    isNonInteractiveSession: boolean
    agentDefinitions: AgentDefinitionsResult
    maxBudgetUsd?: number
    customSystemPrompt?: string
    appendSystemPrompt?: string
    querySource?: QuerySource
    refreshTools?: () => Tools                  // 中途 MCP 工具变更后回调
  }
  abortController: AbortController
  readFileState: FileStateCache
  getAppState(): AppState
  setAppState(f: (prev: AppState) => AppState): void
  setAppStateForTasks?: (f: (prev: AppState) => AppState) => void
  handleElicitation?: (serverName, params, signal) => Promise<ElicitResult>
  setToolJSX?: SetToolJSXFn
  addNotification?: (notif: Notification) => void
  appendSystemMessage?: (msg: Exclude<SystemMessage, SystemLocalCommandMessage>) => void
  sendOSNotification?: (opts: { message: string; notificationType: string }) => void
  nestedMemoryAttachmentTriggers?: Set<string>
  loadedNestedMemoryPaths?: Set<string>
  dynamicSkillDirTriggers?: Set<string>
  discoveredSkillNames?: Set<string>
  userModified?: boolean
  setInProgressToolUseIDs: (f: (prev: Set<string>) => Set<string>) => void
  setHasInterruptibleToolInProgress?: (v: boolean) => void
  setResponseLength: (f: (prev: number) => number) => void
  pushApiMetricsEntry?: (ttftMs: number) => void       // ant-only OTPS 追踪
  setStreamMode?: (mode: SpinnerMode) => void
  onCompactProgress?: (event: CompactProgressEvent) => void
  setSDKStatus?: (status: SDKStatus) => void
  openMessageSelector?: () => void
  updateFileHistoryState: (updater) => void
  updateAttributionState: (updater) => void
  setConversationId?: (id: UUID) => void
  agentId?: AgentId                                     // 仅 subagent 设置
  agentType?: string
  requireCanUseTool?: boolean
  messages: Message[]
  fileReadingLimits?: { maxTokens?: number; maxSizeBytes?: number }
  globLimits?: { maxResults?: number }
  toolDecisions?: Map<string, { source: string; decision: 'accept' | 'reject'; timestamp: number }>
  queryTracking?: QueryChainTracking
  requestPrompt?: (sourceName, toolInputSummary?) => (request) => Promise<PromptResponse>
  toolUseId?: string
  criticalSystemReminder_EXPERIMENTAL?: string
  preserveToolUseResults?: boolean
  localDenialTracking?: DenialTrackingState
  contentReplacementState?: ContentReplacementState
  renderedSystemPrompt?: SystemPrompt
}
```

- **用途**:工具 `call()` 函数能拿到的"宿主 API"——`abortController`、`appState`、`notifications`、`mcpClients`、`agentDefinitions` 等。是 L3 调度层→L4 工具实现的桥。
- **关键字段**:
  - `options.tools` 工具集;`options.refreshTools` 让 MCP 中途新增时也能刷新。
  - `setAppState` vs `setAppStateForTasks`:`createSubagentContext` 用后者把状态变更穿透到根 store(用于 background agent 注册)。
  - `localDenialTracking`:本地拒绝计数器,异步 subagent 也能累加(因为它们的 `setAppState` 是 no-op)。
  - `contentReplacementState` + `renderedSystemPrompt`:fork subagent 用以继承父线程 prompt cache。
- **引用位置**:225 个调用方,遍布 L2↔L3↔L4↔L5。

### B.3.4 `ToolPermissionContext` — 权限上下文(DeepImmutable)

**完整定义**(`src/Tool.ts:123-138`):

```typescript
export type ToolPermissionContext = DeepImmutable<{
  mode: PermissionMode
  additionalWorkingDirectories: Map<string, AdditionalWorkingDirectory>
  alwaysAllowRules: ToolPermissionRulesBySource
  alwaysDenyRules: ToolPermissionRulesBySource
  alwaysAskRules: ToolPermissionRulesBySource
  isBypassPermissionsModeAvailable: boolean
  isAutoModeAvailable?: boolean
  strippedDangerousRules?: ToolPermissionRulesBySource
  shouldAvoidPermissionPrompts?: boolean
  awaitAutomatedChecksBeforeDialog?: boolean
  prePlanMode?: PermissionMode
}>
```

- **用途**:权限检查时的"当前态快照"。每条规则都带 source(`userSettings` / `projectSettings` / `localSettings` / `flagSettings` / `policySettings` / `cliArg` / `command` / `session`),用于判断命中顺序。
- **关键字段**:
  - `mode`:用户当前模式(`default` / `acceptEdits` / `plan` / `bypassPermissions` / `dontAsk` / `auto` / `bubble`)。
  - `additionalWorkingDirectories`:`/add-dir` 加入的目录,经规则匹配后允许操作。
  - `shouldAvoidPermissionPrompts`:background agent 设置,自动拒绝。
  - `prePlanMode`:plan → implement 切换时记录原模式,退出后还原。
- **引用位置**:160 个调用方,`useCanUseTool`、`components/permissions/*` 等。

### B.3.5 `ToolResult<T>` — 工具返回值

**完整定义**(`src/Tool.ts:321-336`):

```typescript
export type ToolResult<T> = {
  data: T
  newMessages?: (
    | UserMessage
    | AssistantMessage
    | AttachmentMessage
    | SystemMessage
  )[]
  contextModifier?: (context: ToolUseContext) => ToolUseContext
  mcpMeta?: {
    _meta?: Record<string, unknown>
    structuredContent?: Record<string, unknown>
  }
}
```

- **用途**:工具 `call()` 的标准返回。`data` 业务结果;`newMessages` 增量消息(注入对话);`contextModifier` 仅对非并发工具生效,用于修改 `toolUseContext`。
- **引用位置**:`src/services/tools/toolExecution.ts:337`(`runToolUse` 生成器)等。

### B.3.6 `Command` 联合类型 — 斜杠命令契约

**完整定义**(`src/types/command.ts:204-205`):

```typescript
export type Command = CommandBase & (
  | PromptCommand
  | LocalCommand
  | LocalJSXCommand
)
```

三种实现模式:

#### `PromptCommand`(`src/types/command.ts:24-57`)

```typescript
export type PromptCommand = {
  type: 'prompt'
  progressMessage: string
  contentLength: number         // 字符数,用于 token 估算
  argNames?: string[]
  allowedTools?: string[]
  model?: string
  source: SettingSource | 'builtin' | 'mcp' | 'plugin' | 'bundled'
  pluginInfo?: { pluginManifest: PluginManifest; repository: string }
  disableNonInteractive?: boolean
  hooks?: HooksSettings
  skillRoot?: string
  context?: 'inline' | 'fork'                  // inline 直接展开;fork 走 sub-agent
  agent?: string                                // fork 时的 agent 类型
  effort?: EffortValue
  paths?: string[]                              // glob 触发门
  getPromptForCommand(args, context): Promise<ContentBlockParam[]>
}
```

#### `LocalCommand`(`src/types/command.ts:73-78`)

```typescript
type LocalCommand = {
  type: 'local'
  supportsNonInteractive: boolean
  load: () => Promise<LocalCommandModule>
}
```

#### `LocalJSXCommand`(`src/types/command.ts:143-152`)

```typescript
type LocalJSXCommand = {
  type: 'local-jsx'
  load: () => Promise<LocalJSXCommandModule>     // 模块导出 call(onDone, ctx, args) => ReactNode
}
```

#### `CommandBase`(`src/types/command.ts:174-202`)

```typescript
export type CommandBase = {
  availability?: CommandAvailability[]          // 'claude-ai' | 'console'
  description: string
  hasUserSpecifiedDescription?: boolean
  isEnabled?: () => boolean                     // 条件启用
  isHidden?: boolean
  name: string
  aliases?: string[]
  isMcp?: boolean
  argumentHint?: string
  whenToUse?: string
  version?: string
  disableModelInvocation?: boolean
  userInvocable?: boolean
  loadedFrom?: 'commands_DEPRECATED' | 'skills' | 'plugin' | 'managed' | 'bundled' | 'mcp'
  kind?: 'workflow'
  immediate?: boolean                           // local-jsx 抢跑 queryGuard
  isSensitive?: boolean                         // args 在历史中打码
  userFacingName?: () => string
}
```

- **用途**:60+ 内置命令 + 插件/Skill 提供的命令统一类型,经 `loadAllCommands` 合并后供 `PromptInput` typeahead、REPL 执行、SDK 消费。
- **关键字段**:`availability` 静态(按 auth/provider 决定可见性);`isEnabled` 运行时重算(动态 GrowthBook);`context: 'fork'` 触发 `executeForkedSlashCommand` 走子 agent。
- **引用位置**:`src/commands.ts:206-220`、`src/utils/processUserInput/processSlashCommand.tsx:309` 等。

### B.3.7 `LocalCommandResult` — local 命令返回值

**完整定义**(`src/types/command.ts:15-22`):

```typescript
export type LocalCommandResult =
  | { type: 'text'; value: string }
  | { type: 'compact'; compactionResult: CompactionResult; displayText?: string }
  | { type: 'skip' }
```

- **用途**:`local` 命令的返回值。`text` → 包装成 `<local-command-stdout>` user message;`compact` → 调 `buildPostCompactMessages`;`skip` → 空消息。
- **引用位置**:`src/utils/processUserInput/processSlashCommand.tsx:657-722`。

### B.3.8 `LocalJSXCommandContext` — JSX 命令的扩展上下文

**完整定义**(`src/types/command.ts:79-97`):

```typescript
export type LocalJSXCommandContext = ToolUseContext & {
  canUseTool?: CanUseToolFn
  setMessages: (updater: (prev: Message[]) => Message[]) => void
  options: {
    dynamicMcpConfig?: Record<string, ScopedMcpServerConfig>
    ideInstallationStatus: IDEExtensionInstallationStatus | null
    theme: ThemeName
  }
  onChangeAPIKey: () => void
  onChangeDynamicMcpConfig?: (config) => void
  onInstallIDEExtension?: (ide: IdeType) => void
  resume?: (sessionId, log, entrypoint) => Promise<void>
}
```

- **用途**:`local-jsx` 命令在 `ToolUseContext` 之上额外获得 `setMessages`、`onChangeAPIKey`、IDE 集成等能力。
- **引用位置**:`src/utils/processUserInput/processSlashCommand.tsx`。

### B.3.9 `QueryEngineConfig` — 引擎配置

**完整定义**(`src/QueryEngine.ts:130-173`):

```typescript
export type QueryEngineConfig = {
  cwd: string
  tools: Tools
  commands: Command[]
  mcpClients: MCPServerConnection[]
  agents: AgentDefinition[]
  canUseTool: CanUseToolFn
  getAppState: () => AppState
  setAppState: (f: (prev: AppState) => AppState) => void
  initialMessages?: Message[]
  readFileCache: FileStateCache
  customSystemPrompt?: string
  appendSystemPrompt?: string
  userSpecifiedModel?: string
  fallbackModel?: string
  thinkingConfig?: ThinkingConfig
  maxTurns?: number
  maxBudgetUsd?: number
  taskBudget?: { total: number }
  jsonSchema?: Record<string, unknown>
  verbose?: boolean
  replayUserMessages?: boolean
  handleElicitation?: ToolUseContext['handleElicitation']
  includePartialMessages?: boolean
  setSDKStatus?: (status: SDKStatus) => void
  abortController?: AbortController
  orphanedPermission?: OrphanedPermission
  snipReplay?: (yieldedSystemMsg, store) => { messages: Message[]; executed: boolean } | undefined
}
```

- **用途**:`QueryEngine` 构造函数的全部输入。覆盖 SDK 模式与 headless 模式共用的配置面。
- **关键字段**:`taskBudget` ant-only 与 `output_config.task_budget` 对齐;`snipReplay` 是 `HISTORY_SNIP` feature 下的边界回调,让 SDK 路径在 snip 触发时裁剪历史。
- **引用位置**:`src/QueryEngine.ts:200`(构造函数)。

### B.3.10 `QueryEngine` 类 — 会话状态容器

**完整定义**(`src/QueryEngine.ts:184-207`):

```typescript
export class QueryEngine {
  private config: QueryEngineConfig
  private mutableMessages: Message[]
  private abortController: AbortController
  private permissionDenials: SDKPermissionDenial[]
  private totalUsage: NonNullableUsage
  private hasHandledOrphanedPermission = false
  private readFileState: FileStateCache
  private discoveredSkillNames = new Set<string>()    // 跨 submitMessage 复用,被 tengu_skill_tool_invocation 引用
  private loadedNestedMemoryPaths = new Set<string>()

  constructor(config: QueryEngineConfig) { ... }

  async *submitMessage(
    prompt: string | ContentBlockParam[],
    options?: { uuid?: string; isMeta?: boolean },
  ): AsyncGenerator<SDKMessage, void, unknown>
}
```

- **用途**:封装一次会话的可变状态。`submitMessage()` 是 `AsyncGenerator<SDKMessage>`,内部顺序完成:**解析用户输入 → 拼装系统提示 → 处理 slash 命令 → UserPromptSubmit hooks → LLM → 工具 → 循环**。
- **关键字段**:
  - `discoveredSkillNames`:turn-scoped,每次 `submitMessage` 开头清空(避免 SDK 长会话无界增长),但同一次提交的两轮重建间复用。
  - `permissionDenials`:SDK 出口用,统计非 allow 结果。
  - `mutableMessages`:消息累积,转写为 `recordTranscript`。
- **引用位置**:`src/QueryEngine.ts:1249`(实例化于 `query()` 入口)、`src/cli/print.ts`(headless 模式)、`src/bridge/bridgeMain.ts`(bridge 模式)。

### B.3.11 `StreamingToolExecutor` — 流式工具调度器

**完整定义**(`src/services/tools/StreamingToolExecutor.ts:40-477`):

```typescript
type ToolStatus = 'queued' | 'executing' | 'completed' | 'yielded'
type TrackedTool = {
  id: string
  block: ToolUseBlock
  assistantMessage: AssistantMessage
  status: ToolStatus
  isConcurrencySafe: boolean
  promise?: Promise<void>
  results?: Message[]
  pendingProgress: Message[]
  contextModifiers?: Array<(context: ToolUseContext) => ToolUseContext>
}

export class StreamingToolExecutor {
  private tools: TrackedTool[] = []
  private toolUseContext: ToolUseContext
  private hasErrored = false
  private erroredToolDescription = ''
  private siblingAbortController: AbortController
  private discarded = false
  private progressAvailableResolve?: () => void

  constructor(
    private readonly toolDefinitions: Tools,
    private readonly canUseTool: CanUseToolFn,
    toolUseContext: ToolUseContext,
  )

  discard(): void                          // 流式回退时丢弃
  addTool(block: ToolUseBlock, assistantMessage: AssistantMessage): void
  *getCompletedResults(): Generator<MessageUpdate, void>
  async *getRemainingResults(): AsyncGenerator<MessageUpdate, void>
}
```

- **用途**:把 LLM 流式返回的多个 `tool_use` block 顺序入队,按 `isConcurrencySafe` 决定并行/串行。Bash 错误时通过 `siblingAbortController` 级联中止同侪(Read/WebFetch 不触发)。
- **关键字段**:
  - `siblingAbortController`:Bash 错误子控制;不冒泡到 query 主循环(只让子进程死)。
  - `discarded`:流式回退时设为 `true`,所有未完成工具注入 `<tool_use_error>Streaming fallback - tool execution discarded</tool_use_error>`(Tombstone)。
  - `pendingProgress`:进度消息,立即 yield,不等工具完成。
- **引用位置**:`src/query.ts:675`(L3 主循环调用)、1 个消费方。

### B.3.12 `PermissionBehavior` / `PermissionDecision` / `PermissionResult` — 权限判别联合

**完整定义**(`src/types/permissions.ts`):

```typescript
// 行为枚举
export type PermissionBehavior = 'allow' | 'deny' | 'ask'

// 规则来源
export type PermissionRuleSource =
  | 'userSettings' | 'projectSettings' | 'localSettings'
  | 'flagSettings' | 'policySettings' | 'cliArg'
  | 'command' | 'session'

// 规则值
export type PermissionRuleValue = {
  toolName: string
  ruleContent?: string                       // e.g. "Bash(git *)" 的 git *
}

// 规则
export type PermissionRule = {
  source: PermissionRuleSource
  ruleBehavior: PermissionBehavior
  ruleValue: PermissionRuleValue
}

// Allow 决策
export type PermissionAllowDecision<Input = { [key: string]: unknown }> = {
  behavior: 'allow'
  updatedInput?: Input
  userModified?: boolean
  decisionReason?: PermissionDecisionReason
  toolUseID?: string
  acceptFeedback?: string
  contentBlocks?: ContentBlockParam[]
}

// Ask 决策
export type PermissionAskDecision<Input = { [key: string]: unknown }> = {
  behavior: 'ask'
  message: string
  updatedInput?: Input
  decisionReason?: PermissionDecisionReason
  suggestions?: PermissionUpdate[]
  blockedPath?: string
  metadata?: PermissionMetadata
  isBashSecurityCheckForMisparsing?: boolean
  pendingClassifierCheck?: PendingClassifierCheck
  contentBlocks?: ContentBlockParam[]
}

// Deny 决策
export type PermissionDenyDecision = {
  behavior: 'deny'
  message: string
  decisionReason: PermissionDecisionReason
  toolUseID?: string
}

// 判别联合
export type PermissionDecision<Input = { [key: string]: unknown }> =
  | PermissionAllowDecision<Input>
  | PermissionAskDecision<Input>
  | PermissionDenyDecision

// 完整结果(加 passthrough 中间态)
export type PermissionResult<Input = { [key: string]: unknown }> =
  | PermissionDecision<Input>
  | {
      behavior: 'passthrough'
      message: string
      decisionReason?: PermissionDecision<Input>['decisionReason']
      suggestions?: PermissionUpdate[]
      blockedPath?: string
      pendingClassifierCheck?: PendingClassifierCheck
    }
```

- **用途**:工具调用前的权限检查返回。4 行为(`allow` / `ask` / `deny` / `passthrough`)+ 11 种 `decisionReason` 组合。
- **`passthrough` 中间态**:本层规则没下结论,留给下一层(规则 → 模式 → 子命令 → hook → classifier)继续评估。
- **引用位置**:95 个调用方,`useCanUseTool`、`components/permissions/*` 等。

### B.3.13 `PermissionDecisionReason` — 决策原因(11 种)

**完整定义**(`src/types/permissions.ts:271-324`):

```typescript
export type PermissionDecisionReason =
  | { type: 'rule'; rule: PermissionRule }
  | { type: 'mode'; mode: PermissionMode }
  | { type: 'subcommandResults'; reasons: Map<string, PermissionResult> }
  | { type: 'permissionPromptTool'; permissionPromptToolName: string; toolResult: unknown }
  | { type: 'hook'; hookName: string; hookSource?: string; reason?: string }
  | { type: 'asyncAgent'; reason: string }
  | { type: 'sandboxOverride'; reason: 'excludedCommand' | 'dangerouslyDisableSandbox' }
  | { type: 'classifier'; classifier: string; reason: string }
  | { type: 'workingDir'; reason: string }
  | { type: 'safetyCheck'; reason: string; classifierApprovable: boolean }
  | { type: 'other'; reason: string }
```

- **用途**:在权限对话框与 telemetry 中说明"为什么这样判"。`safetyCheck.classifierApprovable` 决定敏感路径(.claude/、.git/、shell config)是否仍交给 classifier 评估。
- **引用位置**:`components/permissions/PermissionRequest.tsx` 的 `usePermissionRequestLogging`。

### B.3.14 `Message` 联合(实际消费方)

**说明**:`src/types/message.ts` 在当前快照中**不存在**;`Message` 由 `src/components/Message.tsx:626` 处 React 组件 + `src/utils/mailbox.ts:5` re-export 共同定义。消费方都通过 `import type { Message }` 引入。子类型:

| 成员 | 关键字段 | 用途 |
|---|---|---|
| `UserMessage` | `content: string \| ContentBlockParam[]` | 用户输入 |
| `AssistantMessage` | `message: BetaMessage` | LLM 输出(含 `tool_use`、`text` blocks) |
| `SystemMessage` | `content: string \| { type, ... }` | 系统消息(compact_boundary、local_command、hook_*) |
| `AttachmentMessage` | 图片/PDF 附件 | `attaching file` 阶段 |
| `ProgressMessage` | 工具进度 | 立即 yield 给 UI |
| `TombstoneMessage` | 流式回退占位 | `StreamingToolExecutor.discard()` 注入 |

派生别名:
- `MessageRowImpl` / `Message` 组件(`src/components/Message.tsx`)— 渲染层。
- `PromptInputQueuedCommandsImpl` — 入队命令 UI。
- `RemoteSessionDetailDialog` — 远端会话视图。

**完整定义**通过运行时泛型实现:
```typescript
// src/utils/mailbox.ts:5
export type { Message } from 'src/types/message.js'  // re-export
// 实际定义在 src/components/Message.tsx 的 MessageProps 与
// 多个 message 子类型合成。
```

- **引用位置**:346 个调用方,涵盖 UI 渲染、持久化、SDK 消费、权限检查。

### B.3.15 `AppState` — 跨层状态总线

**完整定义**(`src/state/AppStateStore.ts:89-452`,节选关键字段):

```typescript
export type AppState = DeepImmutable<{
  settings: SettingsJson
  verbose: boolean
  mainLoopModel: ModelSetting
  mainLoopModelForSession: ModelSetting
  statusLineText: string | undefined
  expandedView: 'none' | 'tasks' | 'teammates'
  isBriefOnly: boolean
  showTeammateMessagePreview?: boolean        // 仅 ENABLE_AGENT_SWARMS
  selectedIPAgentIndex: number                // IP Agent 选择
  coordinatorTaskIndex: number                // -1 pill, 0 main, 1..N agents
  viewSelectionMode: 'none' | 'selecting-agent' | 'viewing-agent'
  footerSelection: FooterItem | null
  toolPermissionContext: ToolPermissionContext
  spinnerTip?: string
  agent: string | undefined                   // --agent CLI flag
  kairosEnabled: boolean                      // 单一可信源
  remoteSessionUrl: string | undefined
  remoteConnectionStatus: 'connecting' | 'connected' | 'reconnecting' | 'disconnected'
  remoteBackgroundTaskCount: number
  replBridgeEnabled: boolean                  // 9 个 bridge 字段
  replBridgeExplicit: boolean
  replBridgeOutboundOnly: boolean
  replBridgeConnected: boolean
  replBridgeSessionActive: boolean
  replBridgeReconnecting: boolean
  replBridgeConnectUrl: string | undefined
  replBridgeSessionUrl: string | undefined
  replBridgeEnvironmentId: string | undefined
  replBridgeSessionId: string | undefined
  replBridgeError: string | undefined
  replBridgeInitialName: string | undefined
  showRemoteCallout: boolean
}> & {
  tasks: { [taskId: string]: TaskState }
  agentNameRegistry: Map<string, AgentId>     // name → AgentId
  foregroundedTaskId?: string
  viewingAgentTaskId?: string
  companionReaction?: string                  // /buddy observer
  companionPetAt?: number                     // /buddy pet 时间戳
  mcp: {
    clients: MCPServerConnection[]
    tools: Tool[]
    commands: Command[]
    resources: Record<string, ServerResource[]>
    pluginReconnectKey: number                // /reload-plugins 触发重连
  }
  plugins: {
    enabled: LoadedPlugin[]
    disabled: LoadedPlugin[]
    commands: Command[]
    errors: PluginError[]
    installationStatus: {
      marketplaces: Array<{ name: string; status: 'pending' | 'installing' | 'installed' | 'failed'; error?: string }>
      plugins: Array<{ id: string; name: string; status: 'pending' | 'installing' | 'installed' | 'failed'; error?: string }>
    }
    needsRefresh: boolean
  }
  agentDefinitions: AgentDefinitionsResult
  fileHistory: FileHistoryState
  attribution: AttributionState
  todos: { [agentId: string]: TodoList }
  remoteAgentTaskSuggestions: { summary: string; task: string }[]
  notifications: { current: Notification | null; queue: Notification[] }
  elicitation: { queue: ElicitationRequestEvent[] }
  thinkingEnabled: boolean | undefined
  promptSuggestionEnabled: boolean
  sessionHooks: SessionHooksState
  tungstenActiveSession?: { sessionName: string; socketName: string; target: string }
  tungstenLastCapturedTime?: number
  tungstenLastCommand?: { command: string; timestamp: number }
  tungstenPanelVisible?: boolean
  tungstenPanelAutoHidden?: boolean
  bagelActive?: boolean                       // WebBrowser pill
  bagelUrl?: string
  bagelPanelVisible?: boolean
  computerUseMcpState?: {                     // CHICAGO_MCP
    allowedApps?: readonly { bundleId: string; displayName: string; grantedAt: number }[]
    grantFlags?: { clipboardRead: boolean; clipboardWrite: boolean; systemKeyCombos: boolean }
    lastScreenshotDims?: { width: number; height: number; displayWidth: number; displayHeight: number; displayId?: number; originX?: number; originY?: number }
    hiddenDuringTurn?: ReadonlySet<string>
    selectedDisplayId?: number
    displayPinnedByModel?: boolean
    displayResolvedForApps?: string
  }
  replContext?: {                            // REPL 工具 VM
    vmContext: import('vm').Context
    registeredTools: Map<string, { name: string; description: string; schema: Record<string, unknown>; handler: (args) => Promise<unknown> }>
    console: { log(); error(); warn(); info(); debug(); getStdout(); getStderr(); clear() }
  }
  teamContext?: {                            // Swarm 共享
    teamName: string
    teamFilePath: string
    leadAgentId: string
    selfAgentId?: string
    selfAgentName?: string
    isLeader?: boolean
    selfAgentColor?: string
    teammates: { [teammateId: string]: { name: string; agentType?: string; color?: string; tmuxSessionName: string; tmuxPaneId: string; cwd: string; worktreePath?: string; spawnedAt: number } }
  }
  standaloneAgentContext?: { name: string; color?: AgentColorName }
  inbox: { messages: Array<{ id: string; from: string; text: string; timestamp: string; status: 'pending' | 'processing' | 'processed'; color?: string; summary?: string }> }
  workerSandboxPermissions: { queue: Array<{ requestId: string; workerId: string; workerName: string; workerColor?: string; host: string; createdAt: number }>; selectedIndex: number }
  pendingWorkerRequest: { toolName: string; toolUseId: string; description: string } | null
  pendingSandboxRequest: { requestId: string; host: string } | null
  promptSuggestion: { text: string | null; promptId: 'user_intent' | 'stated_intent' | null; shownAt: number; acceptedAt: number; generationRequestId: string | null }
  speculation: SpeculationState
  speculationSessionTimeSavedMs: number
  skillImprovement: { suggestion: { skillName: string; updates: { section: string; change: string; reason: string }[] } | null }
  authVersion: number                         // 登录/登出递增
  initialMessage: { message: UserMessage; clearContext?: boolean; mode?: PermissionMode; allowedPrompts?: AllowedPrompt[] } | null
  pendingPlanVerification?: { plan: string; verificationStarted: boolean; verificationCompleted: boolean }
  denialTracking?: DenialTrackingState
  activeOverlays: ReadonlySet<string>         // Escape 协调
  fastMode?: boolean
  advisorModel?: string
  effortValue?: EffortValue
  ultraplanLaunching?: boolean
  ultraplanSessionUrl?: string
  ultraplanPendingChoice?: { plan: string; sessionId: string; taskId: string }
  ultraplanLaunchPending?: { blurb: string }
  isUltraplanMode?: boolean
  replBridgePermissionCallbacks?: BridgePermissionCallbacks
  channelPermissionCallbacks?: ChannelPermissionCallbacks
}
```

- **用途**:**横切状态总线**。`useAppState()` 是 React 组件订阅入口;`setAppState` 走 reducer 通知;`getDefaultAppState` 在 `main.tsx` 启动时构造初始值。
- **关键字段**:`tasks`(后台任务)、`agentNameRegistry`(name → AgentId)、`mcp.pluginReconnectKey`(/reload-plugins 触发)、`inbox`(跨 agent 消息)、`speculation`(猜测生成器)、`teamContext`(swarm 共享)。
- **引用位置**:184 个调用方,`QueryEngine.ts`、`Task.ts`、`Tool.ts`、`CompanionSprite.tsx` 等。

### B.3.16 `AppStateStore` — Store 包装

**完整定义**(`src/state/AppStateStore.ts:454`):

```typescript
export type AppStateStore = Store<AppState>
```

`Store<T>`(`src/state/store.ts:3-7`):

```typescript
export type Store<T> = {
  getState: () => T
  setState: (updater: (prev: T) => T) => void
  subscribe: (listener: Listener) => () => void
}
```

- **用途**:把 `AppState` 包装成可订阅 store。`createStore<T>(initialState, onChange?)` 创建实例,`setState` 通过 `Object.is` 短路;`useAppStateStore`(`src/state/AppState.tsx:177`)是 React hook。
- **引用位置**:2 个调用方(`AppState.tsx` 中)。

### B.3.17 `SessionKind` / `SessionStatus` — 会话并发分类

**完整定义**(`src/utils/concurrentSessions.ts:17-19`):

```typescript
export type SessionKind = 'interactive' | 'bg' | 'daemon' | 'daemon-worker'
export type SessionStatus = 'busy' | 'idle' | 'waiting'
```

- **用途**:
  - `SessionKind`:写入 `<configHome>/sessions/<pid>.json`,`claude ps` 列出;`envSessionKind()` 从 `CLAUDE_CODE_SESSION_KIND` 读取,被 `BG_SESSIONS` feature 守门。
  - `SessionStatus`:`updateSessionActivity()` 实时刷给 `claude ps` 的 sparkline。
- **引用位置**:2 个调用方(自身模块);`SessionId` 在 `src/types/ids.ts:10`(branded string)。
- **相关**:**当前快照无统一 `Session` 类型**。会话元数据通过 `SessionLogResult`(`src/utils/sessionStorage.ts:4064`)+ `SerializedMessage`(`src/types/logs.ts:7`)+ `LogOption`(`src/types/logs.ts:18`)组合表达。

### B.3.18 `TaskContext` / `TaskStateBase` / `TaskType` / `TaskStatus`

**完整定义**(`src/Task.ts:6-76`):

```typescript
export type TaskType =
  | 'local_bash' | 'local_agent' | 'remote_agent'
  | 'in_process_teammate' | 'local_workflow'
  | 'monitor_mcp' | 'dream'

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'killed'

export type SetAppState = (f: (prev: AppState) => AppState) => void

export type TaskContext = {
  abortController: AbortController
  getAppState: () => AppState
  setAppState: SetAppState
}

export type TaskStateBase = {
  id: string                       // 8 字符 base36,带类型前缀(b/a/r/t/w/m/d)
  type: TaskType
  status: TaskStatus
  description: string
  toolUseId?: string
  startTime: number
  endTime?: number
  totalPausedMs?: number
  outputFile: string               // 任务输出 JSONL
  outputOffset: number             // 增量读取偏移
  notified: boolean
}

export type Task = {
  name: string
  type: TaskType
  kill(taskId: string, setAppState: SetAppState): Promise<void>
}
```

- **用途**:后台任务(本地 shell、subagent、远端、in-process teammate、workflow、monitor、dream)的统一生命周期;`isTerminalTaskStatus()` 判定终态。
- **关键字段**:ID 36^8 ≈ 2.8 万亿组合防 symlink 暴力;`outputOffset` 支持增量读取。
- **引用位置**:`src/services/AgentSummary/agentSummary.ts`、`src/tasks/LocalShellTask/LocalShellTask.tsx`、`src/tasks/RemoteAgentTask/RemoteAgentTask.tsx`(9 调用方)。

### B.3.19 `RemoteAgentTaskState`

**完整定义**(`src/tasks/RemoteAgentTask/RemoteAgentTask.tsx:22-59`):

```typescript
export type RemoteAgentTaskState = TaskStateBase & {
  type: 'remote_agent'
  remoteTaskType: RemoteTaskType                  // 'remote-agent' | 'ultraplan' | 'ultrareview' | 'autofix-pr' | 'background-pr'
  remoteTaskMetadata?: RemoteTaskMetadata         // { owner; repo; prNumber }
  sessionId: string                               // 原始 session ID for API
  command: string
  title: string
  todoList: TodoList
  log: SDKMessage[]
  isLongRunning?: boolean
  pollStartedAt: number                           // 防止 restore 立即超时
  isRemoteReview?: boolean
  reviewProgress?: { stage?: 'finding' | 'verifying' | 'synthesizing'; bugsFound: number; bugsVerified: number; bugsRefuted: number }
  isUltraplan?: boolean
  ultraplanPhase?: Exclude<UltraplanPhase, 'running'>    // 'needs_input' | 'plan_ready'
}
```

- **用途**:`/ultraplan`、`/ultrareview`、autofix-pr 等远端执行任务的状态机。`pollStartedAt` 记录本地 poller 启动时间,避免 restore 后立即超时。
- **引用位置**:`src/commands/ultraplan.tsx`、`src/components/tasks/BackgroundTasksDialog.tsx`、`src/tasks.ts` 等。

### B.3.20 `BaseAgentDefinition` / `AgentDefinition`

**完整定义**(`src/tools/AgentTool/loadAgentsDir.ts:106-184`):

```typescript
export type BaseAgentDefinition = {
  agentType: string
  whenToUse: string
  tools?: string[]
  disallowedTools?: string[]
  skills?: string[]
  mcpServers?: AgentMcpServerSpec[]
  hooks?: HooksSettings
  color?: AgentColorName
  model?: string
  effort?: EffortValue
  permissionMode?: PermissionMode
  maxTurns?: number
  filename?: string
  baseDir?: string
  criticalSystemReminder_EXPERIMENTAL?: string
  requiredMcpServers?: string[]
  background?: boolean
  initialPrompt?: string
  memory?: AgentMemoryScope
  isolation?: 'worktree' | 'remote'
  pendingSnapshotUpdate?: { snapshotTimestamp: string }
  omitClaudeMd?: boolean
}

export type BuiltInAgentDefinition = BaseAgentDefinition & {
  source: 'built-in'
  baseDir: 'built-in'
  callback?: () => void
  getSystemPrompt: (params: { toolUseContext: Pick<ToolUseContext, 'options'> }) => string
}

export type CustomAgentDefinition = BaseAgentDefinition & {
  getSystemPrompt: () => string
  source: SettingSource
  filename?: string
  baseDir?: string
}

export type PluginAgentDefinition = BaseAgentDefinition & {
  getSystemPrompt: () => string
  source: 'plugin'
  filename?: string
  plugin: string
}

export type AgentDefinition =
  | BuiltInAgentDefinition
  | CustomAgentDefinition
  | PluginAgentDefinition
```

- **用途**:所有 Agent 类型的统一抽象。`omitClaudeMd` 让只读 agent (Explore/Plan) 节省 ~5-15 Gtok/周。
- **引用位置**:114 调用方,`QueryEngine.ts`、`Tool.ts`、`components/PromptInput/PromptInput.tsx` 等。

### B.3.21 `ResolvedAgentTools` — Agent 工具解析结果

**完整定义**(`src/tools/AgentTool/agentToolUtils.ts:62-68`):

```typescript
export type ResolvedAgentTools = {
  hasWildcard: boolean                            // tools === undefined || ['*']
  validTools: string[]
  invalidTools: string[]
  resolvedTools: Tools
  allowedAgentTypes?: string[]                    // Agent tool spec 中 comma 分隔
}
```

- **用途**:`resolveAgentTools()` 在 spawn sub-agent 时把 agent def 的 `tools` 字段解析为实际可用的 `Tools`。`allowedAgentTypes` 用于 `Agent(x,y)` 语法限制子 agent 类型。
- **引用位置**:1 个调用方(`agentToolUtils.ts` 自身)。

### B.3.22 `HookExecutionEvent` — Hook 广播总线

**完整定义**(`src/utils/hooks/hookEvents.ts:50-54`):

```typescript
export type HookStartedEvent = {
  type: 'started'
  hookId: string
  hookName: string
  hookEvent: string
}

export type HookProgressEvent = {
  type: 'progress'
  hookId: string
  hookName: string
  hookEvent: string
  stdout: string
  stderr: string
  output: string
}

export type HookResponseEvent = {
  type: 'response'
  hookId: string
  hookName: string
  hookEvent: string
  output: string
  stdout: string
  stderr: string
  exitCode?: number
  outcome: 'success' | 'error' | 'cancelled'
}

export type HookExecutionEvent =
  | HookStartedEvent
  | HookProgressEvent
  | HookResponseEvent
```

- **用途**:`emitHookStarted` / `emitHookProgress` / `emitHookResponse` 通过 `registerHookEventHandler` 注册 handler;`ALWAYS_EMITTED_HOOK_EVENTS = ['SessionStart', 'Setup']` 之外的 hook 事件需要在 `includeHookEvents` 开启或 `CLAUDE_CODE_REMOTE` 下才转发给 SDK。
- **引用位置**:3 调用方(同文件);订阅方见 SDK/Bridge。

### B.3.23 `MemoryType` — 记忆文件类型

**完整定义**(`src/utils/memory/types.ts:1-11`):

```typescript
export const MEMORY_TYPE_VALUES = [
  'User',
  'Project',
  'Local',
  'Managed',
  'AutoMem',
  ...(feature('TEAMMEM') ? (['TeamMem'] as const) : []),
] as const

export type MemoryType = (typeof MEMORY_TYPE_VALUES)[number]
```

- **用途**:CLAUDE.md 注入时分类。`User` 来自 `~/.claude/CLAUDE.md`,`Project` 来自 `<cwd>/CLAUDE.md`,`Local` 来自 `.claude/CLAUDE.local.md`(gitignored),`Managed` 来自企业托管,`AutoMem` 由 `AUTO_MEM` 自动生成,`TeamMem` 由 `TEAMMEM` feature 守门。
- **引用位置**:12 调用方,`utils/claudemd.ts`、`utils/config.ts` 等。
- **说明**:也存在 `src/memdir/memoryTypes.ts:21` 的次级 `MemoryType` 联合(memory scan 用),两者独立。

### B.3.24 `MCPServerConnection` — MCP 连接 5 态判别

**完整定义**(`src/services/mcp/types.ts:221-226`):

```typescript
export type MCPServerConnection =
  | ConnectedMCPServer
  | FailedMCPServer
  | NeedsAuthMCPServer
  | PendingMCPServer
  | DisabledMCPServer
```

- **用途**:MCP 客户端 5 种连接状态判别。`AppState.mcp.clients` 数组里既有 stdio、又有 sse、http、ws、sdk、sse-ide、ws-ide、claudeai-proxy 多种 transport。
- **引用位置**:贯穿 MCP 子系统与 `useManageMCPConnections`(`src/services/mcp/useManageMCPConnections.ts:1141`)。

### B.3.25 `CompactProgressEvent` — 压缩进度事件

**完整定义**(`src/Tool.ts:150-156`):

```typescript
export type CompactProgressEvent =
  | { type: 'hooks_start'; hookType: 'pre_compact' | 'post_compact' | 'session_start' }
  | { type: 'compact_start' }
  | { type: 'compact_end' }
```

- **用途**:通过 `ToolUseContext.onCompactProgress` 推送给 UI(REPL),触发 Spinner 文本更新。

### B.3.26 `TaskType` 与 `RemoteTaskType`

**完整定义**(`src/tasks/RemoteAgentTask/RemoteAgentTask.tsx:60-61`):

```typescript
const REMOTE_TASK_TYPES = ['remote-agent', 'ultraplan', 'ultrareview', 'autofix-pr', 'background-pr'] as const
export type RemoteTaskType = (typeof REMOTE_TASK_TYPES)[number]
```

- **用途**:限定 `RemoteAgentTaskState.remoteTaskType` 的取值;`isRemoteTaskType` 类型守卫。

## B.4 反模式

### ❌ 用 `Tool[]` 而不是 `Tools`

```typescript
// 错误
function call(tools: Tool[]) { ... }
// 正确
function call(tools: Tools) { ... }  // src/Tool.ts:701
```

### ❌ 自己写 `Message` 子类型

`Message` 联合在 `src/utils/mailbox.ts:5` 集中 re-export;新增消息类型应该走 `utils/mailbox.ts` 而非自定义。

### ❌ 跨边界传递 `Set<T>` 当 `ReadonlySet<T>`

`AppState` 顶层被 `DeepImmutable` 包裹,但下方 `Map` / `Set` / 函数字段被排除。`mcp`、`pluginReconnectKey` 等需要保持只读;`tasks` 例外(含函数)。

### ❌ 给 `AgentDefinition` 缺 `source`

3 个判别子类型(built-in / user-project-managed / plugin)用 `source` 区分,缺失会导致 `isBuiltInAgent` / `isCustomAgent` / `isPluginAgent` 类型守卫失效。

## B.5 引用

- [`00-front/03-glossary.md`](../00-front/03-glossary.md) — 50 术语基线
- [`03-developer/16-tool-contract.md`](../03-developer/16-tool-contract.md) — `Tool` 完整合约说明
- [`04-architect/27-query-engine.md`](../04-architect/27-query-engine.md) — QueryEngine 详细分析
- [`04-architect/30-subsystems.md`](../04-architect/30-subsystems.md) — 各子系统上下游
- [`05-appendices/01-file-tree.md`](01-file-tree.md) — 文件树索引
- [`05-appendices/05-build-flags.md`](05-build-flags.md) — feature flag 全清单
