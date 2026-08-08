# Claude Code 深度分析教程

> **面向用户与架构师的全面技术指南**
>
> 本教程基于 2026 年 3 月 31 日泄露的 Claude Code 源代码编写，旨在为开发者用户和架构师提供一份深入浅出的技术文档。

---

## 目录

1. [背景与概述](#1-背景与概述)
2. [技术架构深度解析](#2-技术架构深度解析)
3. [核心设计模式](#3-核心设计模式)
4. [使用指南](#4-使用指南)
5. [最佳实践](#5-最佳实践)
6. [FAQ 与故障排除](#6-faq-与故障排除)
7. [高级特性深度剖析](#7-高级特性深度剖析)

---

## 1. 背景与概述

### 1.1 Claude Code 是什么

Claude Code 是 **Anthropic 官方推出的 CLI（命令行界面）工具**，它允许开发者直接在终端中与 Claude 对话，执行各种软件工程任务。

#### 产品定位

在 AI 时代，Claude Code 定位为**命令行开发伴侣**——它不是一个简单的聊天机器人，而是一个能够：

- **读写文件** - 创建、编辑、搜索代码文件
- **执行命令** - 运行 shell 命令、git 操作、构建脚本
- **搜索代码** - 使用正则表达式和 glob 模式搜索代码库
- **管理任务** - 创建任务清单、跟踪进度
- **协作开发** - 多 Agent 并行工作、团队协作

#### 核心价值

| 价值维度 | 说明 |
|---------|------|
| **效率提升** | 自然语言描述即可完成复杂编码任务 |
| **上下文感知** | 理解项目结构、Git 状态、代码关系 |
| **工具集成** | 40+ 内置工具 + MCP 扩展生态 |
| **可扩展性** | 支持自定义技能和插件 |

#### 与其他工具的差异化

| 特性 | Claude Code | GitHub Copilot | ChatGPT |
|------|-------------|----------------|---------|
| 交互方式 | CLI 终端 | IDE 插件 | Web/API |
| 工具调用 | 原生支持 | 有限 | 需 Plus |
| 文件编辑 | 直接修改 | 建议 | 需复制 |
| Git 集成 | 深度 | 基础 | 无 |
| 多 Agent | 支持 | 不支持 | 不支持 |

### 1.2 发展历程与泄露背景

#### 泄露事件

2026 年 3 月 31 日，Claude Code 的完整源代码通过一个意外暴露的 **`.map` 文件**被公开。事件经过：

1. **发现者**：Chaofan Shou (@Fried_rice)
2. **泄露途径**：Anthropic npm 包中的 source map 文件包含对原始 TypeScript 源码的引用
3. **源码规模**：约 1,900 个文件，512,000+ 行代码
4. **技术价值**：这是了解 AI Agent 系统设计的珍贵案例

#### 技术意义

泄露的源码揭示了：
- **LLM Agent 的工程实现** - 如何构建可靠的工具调用循环
- **权限安全模型** - 如何在灵活性和安全性间取得平衡
- **前端架构** - 如何用 React 构建 CLI UI
- **设计模式** - 懒加载、并行预取、Dead Code Elimination 等

### 1.3 核心能力一览

#### 文件操作能力

```
┌─────────────────────────────────────────────────────────────┐
│                     文件操作工具矩阵                          │
├──────────────┬──────────────────────────────────────────────┤
│ FileReadTool │ 读取文件，支持图片、PDF、Jupyter notebook     │
│ FileWriteTool│ 创建新文件或覆盖现有文件                       │
│ FileEditTool │ 字符串替换式编辑，保留文件其余内容              │
│ GlobTool     │ 文件模式匹配（*.ts, **/*.js 等）              │
│ GrepTool     │ 正则表达式内容搜索，基于 ripgrep               │
└──────────────┴──────────────────────────────────────────────┘
```

#### Shell 执行能力

**BashTool** 是 Claude Code 最强大的工具，它能够：
- 执行任意 shell 命令
- 支持超时控制
- 后台运行模式
- 沙箱隔离执行

**命令分类识别**（自动标记为只读）：
```typescript
// 搜索命令
find, grep, rg, ag, ack, locate, which, whereis
// 读取命令
cat, head, tail, less, more, wc, stat, file, jq, awk
// 列表命令
ls, tree, du
```

#### Git 工作流

| 命令 | 功能 |
|------|------|
| `/commit` | 智能创建 commit，自动分析 diff |
| `/diff` | 查看工作区变更 |
| `/branch` | 分支管理 |
| `/review` | PR 审查 |

#### Web 能力

- **WebSearchTool** - 网页搜索
- **WebFetchTool** - 获取 URL 内容
- **API 调用** - 访问外部服务

#### 多 Agent 协作

```
用户
  │
  ├─► 主 Agent（直接执行）
  │
  └─► 子 Agent（通过 AgentTool spawn）
         │
         ├─► Agent A（并行任务 1）
         ├─► Agent B（并行任务 2）
         └─► Agent C（并行任务 3）
```

---

## 2. 技术架构深度解析

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              main.tsx                                    │
│                     (Commander.js CLI 入口 ~804KB)                       │
│                                                                         
│  启动流程:                                                                │
│  1. profileCheckpoint('main_tsx_entry')                                  │
│  2. startMdmRawRead()        ←─ MDM 设置并行读取                          │
│  3. startKeychainPrefetch()  ←─ Keychain 并行预取                         │
│  4. 并行初始化: GrowthBook, API Preconnect, Settings                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│  QueryEngine  │         │   Commands    │         │     Tools     │
│    (~46K行)   │         │    (~25K行)   │         │    (~29K行)   │
├───────────────┤         ├───────────────┤         ├───────────────┤
│ • submitMessage()│       │ • slash 命令   │         │ • 40+ 内置工具│
│ • 流式响应处理  │         │ • 注册中心     │         │ • MCP 工具    │
│ • 工具调用循环  │         │ • 懒加载       │         │ • 权限模型    │
│ • 重试逻辑     │         │ • Fork 模式    │         │ • Schema 验证 │
└───────────────┘         └───────────────┘         └───────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │         Services Layer         │
                    │  ┌─────────────────────────┐  │
                    │  │  api/  - Anthropic SDK  │  │
                    │  │  mcp/  - MCP 协议       │  │
                    │  │  lsp/  - 语言服务器     │  │
                    │  │  analytics/ - Feature   │  │
                    │  │  compact/ - 上下文压缩  │  │
                    │  └─────────────────────────┘  │
                    └───────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│   components/ │         │    hooks/     │         │    screens/   │
│  (~140 组件)  │         │  (~90 Hooks)  │         │  REPL/Doctor  │
│  React + Ink  │         │   状态管理    │         │  Resume/...   │
└───────────────┘         └───────────────┘         └───────────────┘
```

### 2.2 核心模块解析

#### 2.2.1 main.tsx - CLI 入口

**职责**：命令行参数解析、应用初始化、REPL 启动

**关键代码结构**：

```typescript
// 入口点 - 所有导入之前必须执行的副作用
profileCheckpoint('main_tsx_entry');
startMdmRawRead();        // MDM 子进程并行启动
startKeychainPrefetch();  // Keychain 并行预取

// 条件导入 - Dead Code Elimination
const coordinatorModeModule = feature('COORDINATOR_MODE')
  ? require('./coordinator/coordinatorMode.js')
  : null;

const assistantModule = feature('KAIROS')
  ? require('./assistant/index.js')
  : null;

// Commander.js 命令定义
const program = new Command();
program
  .name('claude')
  .description('Claude Code CLI')
  .argument('[prompt]', 'Initial prompt')
  .option('-c, --continue', 'Continue last session')
  .option('--model <model>', 'Specify model')
  // ... 更多选项
```

**启动优化机制**：

```typescript
// 并行预取的秘密
// 在 Node.js 单线程环境中，这些 I/O 操作并行执行
await Promise.all([
  startMdmRawRead(),      // ~50ms
  startKeychainPrefetch(), // ~65ms
  prefetchApiConnections(), // ~40ms
]);
// 总计节省 ~135ms 启动时间
```

#### 2.2.2 QueryEngine.ts - LLM 查询引擎

**职责**：管理对话生命周期、调用 LLM API、处理工具调用循环

**类结构**：

```typescript
export class QueryEngine {
  private config: QueryEngineConfig;
  private mutableMessages: Message[];      // 对话历史
  private abortController: AbortController; // 中断控制
  private permissionDenials: SDKPermissionDenial[]; // 权限拒绝记录
  private totalUsage: NonNullableUsage;    // API 使用统计
  private readFileState: FileStateCache;   // 文件状态缓存
  private discoveredSkillNames: Set<string>; // 已发现技能
  
  // 核心方法
  async *submitMessage(prompt, options): AsyncGenerator<SDKMessage>;
  interrupt(): void;
  getMessages(): Message[];
}
```

**API 调用流程**：

```
QueryEngine.submitMessage()
    │
    ▼
query()  ← 核心查询循环 (query.ts)
    │
    ▼
deps.callModel()  ← API 调用入口 (services/api/claude.ts)
    │
    ▼
withRetry()  ← 重试逻辑包装器
    │
    ▼
anthropic.beta.messages.create()  ← 实际 HTTP 请求
```

**流式响应处理**：

```typescript
// 支持 SSE 流式响应
const stream = await anthropic.beta.messages.create({
  model: config.model,
  messages: normalizedMessages,
  max_tokens: 8192,
  stream: true,  // ← 关键：流式模式
});

// AsyncGenerator 逐块处理
for await (const event of stream) {
  switch (event.type) {
    case 'message_start':
      // 消息开始
    case 'content_block_start':
      // 内容块开始
    case 'content_block_delta':
      // 内容块增量（可能是 text 或 tool_use）
    case 'message_delta':
      // 消息结束
  }
}
```

#### 2.2.3 Tool.ts - 工具类型系统

**职责**：定义工具接口契约、构建工厂函数、权限模型

**核心类型定义**：

```typescript
export type Tool<
  Input extends AnyObject = AnyObject,
  Output = unknown,
  P extends ToolProgressData = ToolProgressData,
> = {
  // 身份
  name: string;
  aliases?: string[];
  searchHint?: string;  // ToolSearch 关键字匹配
  
  // 核心方法
  call(args, context, canUseTool, parentMessage, onProgress?): Promise<ToolResult<Output>>;
  description(input, options): Promise<string>;
  prompt(options): Promise<string>;
  
  // Schema 定义
  readonly inputSchema: Input;
  readonly inputJSONSchema?: ToolInputJSONSchema;
  outputSchema?: z.ZodType<unknown>;
  
  // 能力声明
  isConcurrencySafe(input): boolean;  // 是否可并行
  isEnabled(): boolean;
  isReadOnly(input): boolean;         // 是否只读
  isDestructive?(input): boolean;     // 是否有破坏性
  isOpenWorld?(input): boolean;       // 是否访问外部世界
  
  // 权限
  checkPermissions(input, context): Promise<PermissionResult>;
  validateInput?(input, context): Promise<ValidationResult>;
  
  // 渲染
  mapToolResultToToolResultBlockParam(content, toolUseID): ToolResultBlockParam;
  renderToolResultMessage?(content, progressMessages, options): React.ReactNode;
}
```

**工具构建工厂**：

```typescript
export function buildTool<D extends ToolDef>(def: D): BuiltTool<D> {
  return {
    ...def,
    // 提供默认值
    isEnabled: () => true,
    isConcurrencySafe: () => false,
    isReadOnly: () => false,
    checkPermissions: () => ({ behavior: 'allow', updatedInput }),
  };
}
```

#### 2.2.4 query.ts - 查询管道

**职责**：消息处理、工具编排、上下文压缩

**核心循环结构**：

```typescript
// query.ts:307-1728
while (true) {
  // 1. 上下文压缩检查
  if (shouldAutoCompact()) {
    await performAutoCompact();
  }
  
  // 2. 调用模型 API
  const stream = await callModel(messages, config);
  
  // 3. 处理流式响应
  for await (const event of stream) {
    if (event.type === 'content_block_delta') {
      if (event.delta.type === 'tool_use') {
        // 收集工具调用
        toolUseBlocks.push(event.delta);
      }
    }
  }
  
  // 4. 执行工具
  if (toolUseBlocks.length > 0) {
    const toolResults = await runTools(toolUseBlocks, ...);
    messages.push(...toolResults);
    continue; // 继续循环
  }
  
  // 5. 返回最终响应
  return finalResponse;
}
```

### 2.3 工具系统架构

#### 工具注册机制

```typescript
// tools.ts
export function getAllBaseTools(): Tools {
  return [
    AgentTool,
    TaskOutputTool,
    BashTool,
    ...(hasEmbeddedSearchTools() ? [] : [GlobTool, GrepTool]),
    ExitPlanModeV2Tool,
    FileReadTool,
    FileEditTool,
    FileWriteTool,
    // ... 更多工具
  ];
}

// 条件编译
...(process.env.USER_TYPE === 'ant' ? [ConfigTool] : []),
...(isEnvTruthy(process.env.ENABLE_LSP_TOOL) ? [LSPTool] : []),
```

#### BashTool 深度解析

**设计特点**：

```typescript
// 输入 Schema
const inputSchema = z.object({
  command: z.string(),           // 要执行的命令
  timeout: z.number().optional(), // 超时时间（毫秒）
  description: z.string().optional(), // 描述
  run_in_background: z.boolean().optional(), // 后台运行
  dangerouslyDisableSandbox: z.boolean().optional(), // 禁用沙箱
});

// 命令分类 - 识别只读命令
isSearchOrReadCommand(command: string): { isSearch: boolean; isRead: boolean; isList: boolean } {
  // 搜索命令
  const searchCommands = ['find', 'grep', 'rg', 'ag', 'ack', 'locate', 'which', 'whereis'];
  // 读取命令
  const readCommands = ['cat', 'head', 'tail', 'less', 'more', 'wc', 'stat', 'file', 'jq', 'awk'];
  // 列表命令
  const listCommands = ['ls', 'tree', 'du'];
}
```

#### GrepTool 深度解析

```typescript
// 基于 ripgrep 的高效搜索
const inputSchema = z.object({
  regex: z.string(),                    // 正则表达式
  file_pattern: z.string().optional(),  // glob 模式
  cwd: z.string().optional(),           // 工作目录
  case_sensitive: z.boolean().optional(),
  head_limit: z.number().optional().default(250), // 结果限制
  output_format: z.enum(['content', 'files_with_matches', 'count']).default('content'),
});

// 并发安全 - 可并行执行
isConcurrencySafe: () => true,
isReadOnly: () => true,

// 使用 ripgrep 参数
const args = [
  '--hidden',           // 搜索隐藏文件
  '--max-columns 500',  // 限制每行长度
  '--no-ignore-vcs',    // 不忽略 VCS 目录
];
```

### 2.4 命令系统架构

#### 命令类型

```typescript
// 三种命令类型（区分联合）
type Command = CommandBase & (PromptCommand | LocalCommand | LocalJSXCommand);

// 1. prompt 命令 - 展开为模型提示
type PromptCommand = {
  type: 'prompt';
  getPromptForCommand(args, context): Promise<PromptContent[]>;
  allowedTools?: string[];  // 权限上下文
};

// 2. local 命令 - 本地执行
type LocalCommand = {
  type: 'local';
  call(args, context): Promise<LocalCommandResult>;
};

// 3. local-jsx 命令 - 全屏 React UI
type LocalJSXCommand = {
  type: 'local-jsx';
  load(): Promise<LocalJSXCommandModule>;  // 懒加载
};
```

#### 命令注册流程

```typescript
// commands.ts
const COMMANDS = memoize((): Command[] => [
  addDir, advisor, agents, branch, btw, chrome, clear, commit, compact,
  // ... 更多命令
  
  // 条件导入的命令
  ...(webCmd ? [webCmd] : []),
  ...(forkCmd ? [forkCmd] : []),
]);

// 命令加载管道
loadAllCommands = memoize(async (cwd) => [
  ...bundledSkills,       // 内置技能
  ...builtinPluginSkills, // 插件技能
  ...skillDirCommands,    // ~/.claude/skills/
  ...workflowCommands,    // 工作流脚本
  ...pluginCommands,      // 外部插件
  ...COMMANDS(),          // 内置命令
]);
```

#### 核心命令示例：/commit

```typescript
const commit: Command = {
  type: 'prompt',
  name: 'commit',
  description: 'Create a git commit',
  allowedTools: [
    'Bash(git add:*)',
    'Bash(git status:*)',
    'Bash(git commit:*)',
  ],
  async getPromptForCommand(_args, context) {
    // 1. 获取 git status
    const status = await execGit('status --short');
    // 2. 获取 git diff
    const diff = await execGit('diff --staged');
    // 3. 获取当前分支
    const branch = await execGit('branch --show-current');
    
    return [{
      type: 'text',
      text: `Create a git commit for the following changes:
      
Branch: ${branch}
Status: ${status || '(clean)'}
Diff: ${diff || '(no staged changes)'}

Provide a concise commit message following conventional commits.`,
    }];
  },
};
```

### 2.5 服务层架构

#### API 服务 (services/api/)

```
api/
├── claude.ts         # Anthropic API 客户端
├── bootstrap.ts      # 启动引导数据
├── errors.ts         # 错误分类
├── filesApi.ts       # 文件上传/下载
├── logging.ts        # 使用日志
└── withRetry.ts      # 重试逻辑
```

**API 调用入口**：

```typescript
// services/api/claude.ts
export async function callModel(
  params: MessageParams,
  config: CallModelConfig
): Promise<AsyncIterable<StreamEvent>> {
  const client = getAnthropicClient();
  
  // 流式调用
  return client.beta.messages.create(
    { ...params, stream: true },
    { signal: config.signal }
  );
}
```

**重试策略**：

```typescript
// withRetry.ts
const DEFAULT_MAX_RETRIES = 10;
const BASE_DELAY_MS = 500;

// 指数退避 + 抖动
function getRetryDelay(attempt: number): number {
  const baseDelay = Math.min(
    BASE_DELAY_MS * Math.pow(2, attempt - 1),
    32000  // 最大 32 秒
  );
  const jitter = Math.random() * 0.25 * baseDelay;
  return baseDelay + jitter;
}
```

#### 扩展服务总览（src/services/）

| 服务 | 路径 | 功能 |
|------|------|------|
| **API** | `api/` | Anthropic SDK 封装、重试、错误分类 |
| **MCP** | `mcp/` | Model Context Protocol 服务器管理 |
| **OAuth** | `oauth/` | OAuth 2.0 认证流程 |
| **LSP** | `lsp/` | Language Server Protocol 管理 |
| **Analytics** | `analytics/` | GrowthBook Feature Flag 与埋点 |
| **Compact** | `compact/` | 对话上下文压缩 |
| **Plugins** | `plugins/` | 插件加载与生命周期 |
| **Policy Limits** | `policyLimits/` | 组织策略限制（企业） |
| **Remote Managed Settings** | `remoteManagedSettings/` | 远程托管设置（企业） |
| **Settings Sync** | `settingsSync/` | 跨环境设置同步 |
| **Team Memory Sync** | `teamMemorySync/` | 团队记忆共享 |
| **Extract Memories** | `extractMemories/` | 自动会话记忆提取 |
| **Magic Docs** | `MagicDocs/` | 自动文档维护 |
| **Auto Dream** | `autoDream/` | 后台记忆合并 |
| **Prompt Suggestion** | `PromptSuggestion/` | 下一步提示建议 |
| **Agent Summary** | `AgentSummary/` | 协调器 Agent 进度摘要 |
| **Tips** | `tips/` | 启动提示管理 |
| **Session Memory** | `SessionMemory/` | 会话级结构化摘要 |
| **Prevent Sleep** | `preventSleep.ts` | 防止系统休眠 |
| **Internal Logging** | `internalLogging.ts` | 内部日志 |
| **Rate Limit Mocking** | `rateLimitMocking.ts` | 速率限制模拟（测试） |
| **Diagnostic Tracking** | `diagnosticTracking.ts` | 诊断追踪 |
| **Token Estimation** | `tokenEstimation.ts` | Token 估算 |

#### MCP 服务 (services/mcp/)

```
mcp/
├── client.ts          # MCP 客户端
├── types.ts           # 类型定义
├── officialRegistry.ts # 官方服务器 registry
└── serverManager.ts   # 服务器管理
```

**MCP 集成**：

```typescript
// MCP 服务器连接
interface MCPServerConnection {
  name: string;
  tools: MCPTool[];
  resources: ServerResource[];
}

// 工具调用
const result = await mcpClient.callTool({
  name: 'tool_name',
  arguments: { arg1: 'value1' },
});
```

### 2.6 Bridge 系统架构

Bridge 系统实现 CLI 与 IDE 的双向通信：

```
┌─────────────────┐         ┌─────────────────┐
│   VS Code       │         │   JetBrains     │
│   Extension     │         │   Plugin        │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │    Bridge Protocol        │
         │    (WebSocket/JWT)        │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │      bridgeMain.ts      │
         │   - 消息协议处理         │
         │   - 会话管理             │
         │   - 权限回调             │
         └─────────────────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │     REPL Session        │
         │   - 命令执行             │
         │   - 工具调用             │
         │   - 状态同步             │
         └─────────────────────────┘
```

---

## 3. 核心设计模式

### 3.1 启动优化：并行预取

**问题**：CLI 工具启动延迟影响体验

**解决方案**：在单线程环境中并行执行独立的 I/O 操作

```typescript
// main.tsx - 在所有模块导入之前触发
// 这些函数启动后台进程，不阻塞主线程

// 1. MDM 读取（macOS 设备管理）
startMdmRawRead();  
// 内部实现：spawn plutil subprocesses

// 2. Keychain 预取（OAuth + API key）
startKeychainPrefetch();
// 内部实现：并行读取 macOS keychain

// 3. 后续在 REPL 初始化时等待完成
await ensureKeychainPrefetchCompleted();
```

**性能收益**：

| 操作 | 串行耗时 | 并行耗时 |
|------|---------|---------|
| MDM 读取 | ~50ms | ~50ms |
| Keychain | ~65ms | ~65ms |
| API 预连接 | ~40ms | ~40ms |
| **总计** | ~155ms | **~50ms** |

### 3.2 懒加载与 Dead Code Elimination

**问题**：包含所有特性会导致二进制过大

**解决方案**：使用 `bun:bundle` feature flags 条件编译

```typescript
// 特性标志定义
const FEATURE_FLAGS = [
  'PROACTIVE',      // 主动模式
  'KAIROS',         // Assistant 模式
  'BRIDGE_MODE',    // IDE 桥接模式
  'DAEMON',         // 守护进程模式
  'VOICE_MODE',     // 语音输入
  'AGENT_TRIGGERS', // Agent 触发器
  'COORDINATOR_MODE', // 协调器模式
];

// 使用方式
const voiceCommand = feature('VOICE_MODE')
  ? require('./commands/voice/index.js').default
  : null;

// 运行时检查
if (feature('DEBUG_MODE')) {
  enableDebugLogging();
}
```

**效果**：
- 未启用的特性代码完全从 bundle 中移除
- 减小发布包体积
- 降低加载时间

### 3.3 工具调用循环

**核心模式**：ReAct（Reasoning + Acting）

```
┌──────────────────────────────────────────────────────────────┐
│                    工具调用循环                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   User Input                                                 │
│       │                                                      │
│       ▼                                                      │
│   ┌─────────┐    No    ┌─────────────┐                       │
│   │ Has Tool│─────────►│   Output    │                       │
│   │  Call?  │          │   Result    │                       │
│   └────┬────┘          └─────────────┘                       │
│        │ Yes                                                 │
│        ▼                                                     │
│   ┌─────────────┐                                            │
│   │ Execute Tool│                                            │
│   └──────┬──────┘                                            │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────┐    Yes   ┌─────────────┐                   │
│   │ More Tools? │─────────►│   Continue  │                   │
│   └──────┬──────┘          │   Loop     │                   │
│          │ No              └──────▲──────┘                   │
│          ▼                          │                        │
│   ┌─────────────┐                   │                        │
│   │ Return to   │───────────────────┘                        │
│   │   LLM       │                                            │
│   └─────────────┘                                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**流式工具执行**：

```typescript
// 传统模式：等待完整响应后才执行工具
const response = await callModel(messages);
// 等待所有 tool_use 生成
for (const tool of response.tool_use) {
  await executeTool(tool);
}

// 流式模式：模型生成 tool_use 时立即执行
const streamingExecutor = new StreamingToolExecutor(tools, canUseTool, context);
for await (const event of stream) {
  if (event.type === 'content_block_delta' && event.delta.type === 'tool_use') {
    streamingExecutor.addToolUse(event.delta);  // 立即加入执行队列
  }
}
```

### 3.4 权限模型

**多层防御架构**：

```
┌─────────────────────────────────────────────────────────────┐
│                    权限检查流程                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 规则匹配阶段                                              │
│     ├─► 工具级 deny 规则检查                                  │
│     ├─► 工具级 ask 规则检查                                   │
│     └─► alwaysAllowRule 检查                                  │
│                                                              │
│  2. 工具自身检查                                              │
│     ├─► tool.checkPermissions()                              │
│     └─► tool.isDestructive()                                 │
│                                                              │
│  3. 交互式检查                                                │
│     ├─► requiresUserInteraction()                            │
│     └─► content-specific ask 规则                            │
│                                                              │
│  4. 安全检查                                                  │
│     └─► 路径约束（.git/, .claude/）                          │
│                                                              │
│  5. 模式处理                                                  │
│     ├─► bypassPermissions: 完全允许                          │
│     ├─► auto: AI 分类器决策                                  │
│     ├─► plan: 计划模式限制                                   │
│     └─► dontAsk: 自动拒绝                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**BashTool 专用权限**：

```typescript
// bashPermissions.ts - 多层检查

// 1. 精确匹配
exactMatch('Bash(rm -rf /)');

// 2. 前缀匹配
prefixMatch('Bash(rm:*)');

// 3. 命令分类（只读命令自动允许）
const classified = classifyCommand('ls -la');
if (classified.isReadOnly) return 'allow';

// 4. AST 解析（检测命令注入）
const ast = parseCommandTree(command);
if (ast.hasInjection) return 'deny';

// 5. 路径约束
if (!isPathAllowed(filePath)) return 'deny';
```

### 3.5 上下文管理

**三层上下文架构**：

```typescript
// 1. 系统上下文（自动收集）
const systemContext = {
  gitStatus: await getGitStatus(),      // Git 状态
  currentDate: new Date().toISOString(), // 当前日期
  // ...
};

// 2. 用户上下文（.claude.md 文件）
const userContext = {
  claudeMd: getClaudeMds(memoryFiles),  // 内存文件内容
  // ...
};

// 3. 会话上下文（消息历史）
const sessionContext = {
  messages: mutableMessages,             // 对话历史
  recentToolResults: recentResults,      // 最近工具结果
  // ...
};
```

**上下文压缩**：

```typescript
// compact.ts - 对话历史压缩

// 触发条件
if (tokenCount > model.contextWindow * 0.8) {
  await performCompact();
}

// 压缩策略
async function performCompact() {
  // 1. 识别压缩边界
  const boundary = findCompactBoundary(messages);
  
  // 2. 保留边界附近的完整消息
  const preserved = messages.slice(-5);
  
  // 3. 压缩中间消息为摘要
  const summary = await summarizeMessages(messages.slice(0, -5));
  
  // 4. 替换为压缩后的消息
  messages = [summary, ...preserved];
}
```

### 3.6 Agent 协作模式

**单 Agent 模式**：

```
用户 → 主 Agent → 工具调用循环 → 结果
```

**子 Agent 模式**：

```
用户 → 主 Agent → AgentTool → 子 Agent A → 工具
                              → 子 Agent B → 工具
                              → 子 Agent C → 工具
```

**Team 模式**：

```typescript
// TeamCreateTool 创建团队
const team = await createTeam({
  name: 'code-review-team',
  agents: [
    { role: 'reviewer', model: 'claude-opus-4-8' },
    { role: 'tester', model: 'claude-sonnet-5' },
    { role: 'writer', model: 'claude-haiku-4-5' },
  ],
});

// 并行执行任务
const results = await Promise.all([
  team.reviewer.review(pullRequest),
  team.tester.runTests(changes),
  team.writer.updateDocs(changes),
]);
```

---

## 4. 使用指南

### 4.1 安装与配置

#### 环境要求

| 要求 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Node.js | 18.0+ | 20.0+ |
| Bun | 1.0+ | 1.1+ |
| macOS | 12.0+ | 14.0+ |
| Linux | Ubuntu 20.04+ | Ubuntu 22.04+ |

#### 安装步骤

```bash
# macOS / Linux
npm install -g @anthropic-ai/claude-code

# 或使用 Bun
bun install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

#### 认证配置

```bash
# 启动交互式登录
claude auth login

# 或使用 API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# 查看认证状态
claude auth status
```

#### 基础配置

Claude Code 的配置通过 `~/.claude/settings.json` 文件管理，或在启动时通过参数指定：

```bash
# 启动时指定模型
claude --model claude-opus-4-8

# 启动时指定权限模式
claude --permission-mode auto

# 启动时指定努力程度
claude --effort high

# 加载自定义设置文件
claude --settings /path/to/settings.json
```

> 主题等可在交互会话中使用 `/theme` 命令设置，配置写入 `~/.claude/settings.json`。

### 4.2 日常使用流程

#### 启动会话

```bash
# 交互式模式
claude

# 带初始提示
claude "解释这个函数的用途"

# 非交互式模式（输出后退出）
claude -p "解释这个函数的用途"

# 继续上次会话
claude --continue
claude -c

# 恢复指定会话
claude -r <session-id>
# 无参数则打开交互式选择器
claude --resume

# 从 PR 恢复会话（PR 编号或 URL）
claude --from-pr 123
claude --from-pr https://github.com/owner/repo/pull/456

# 恢复时创建新会话 ID（fork）
claude -r <session-id> --fork-session

# 添加额外目录（可重复）
claude --add-dir /path/to/project
claude --add-dir /docs --add-dir /scripts
```

#### 对话交互

```
用户: 帮我创建一个用户注册 API

Claude: 我来帮你创建用户注册 API。首先让我查看一下项目结构。

[调用 BashTool: ls -la]
[调用 GlobTool: **/routes/*.js]
[调用 FileReadTool: src/routes/index.js]

好的，我看到项目使用 Express.js。让我为你创建注册 API：

1. 创建路由: src/routes/auth.js
2. 创建控制器: src/controllers/authController.js  
3. 创建验证中间件: src/middleware/validate.js

是否继续？
```

#### 权限确认

```
[权限请求]
┌────────────────────────────────────────┐
│ BashTool: npm install express-validator│
│                                        │
│ 描述: 安装 npm 包                       │
│                                        │
│ [允许] [拒绝] [始终允许]                │
└────────────────────────────────────────┘
```

### 4.3 效率技巧

#### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `Ctrl+L` | 清屏 |
| `Tab` | 自动补全 |
| `↑/↓` | 命令历史 |

#### 多会话管理

```bash
# 恢复指定会话
claude -r <session-id>

# 继续上次会话
claude --continue

# 管理后台 Agent（包含会话信息）
claude agents --json

# 列出所有后台 Agent
claude agents
```

#### 上下文注入

```bash
# 添加额外上下文目录
claude --add-dir /path/to/docs

# 启用安全模式（禁用所有自定义配置）
claude --safe-mode

# 启用最小化模式
claude --bare
```

### 4.4 MCP 服务器集成

#### 什么是 MCP

MCP（Model Context Protocol）是一种开放协议，允许 AI 模型与外部工具和服务交互。

#### 安装 MCP 服务器

> **说明**：Claude Code `2.1.215` 提供 `claude mcp add` 子命令（不是 `install`）。所有添加操作使用 `--` 分隔符，后跟实际的服务器启动命令。

```bash
# 添加文件系统 MCP 服务器（stdio 传输，默认）
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/dir

# 添加 GitHub MCP 服务器（使用 -e/--env 设置环境变量）
claude mcp add github -e GITHUB_TOKEN=your-token -- npx -y @modelcontextprotocol/server-github

# 添加 HTTP 传输的 MCP 服务器
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 添加 HTTP 服务器时附带自定义 Header
claude mcp add --transport http corridor https://app.corridor.dev/api/mcp --header "Authorization: Bearer ..."

# 指定作用域（local | user | project），默认 local
claude mcp add -s user my-server -- my-command --some-flag arg1

# 列出已安装服务器
claude mcp list

# 查看服务器详情
claude mcp get <server-name>

# 移除服务器（指定 -s 可限定作用域）
claude mcp remove <server-name>

# MCP 服务器认证（OAuth）
claude mcp login <server-name>

# 清除 MCP 服务器 OAuth 凭据
claude mcp logout <server-name>
```

#### 配置示例

```json
// ~/.claude/mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "github": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

### 4.5 技能开发

#### 技能文件结构

```
~/.claude/skills/
├── my-skill/
│   ├── skill.json    # 技能定义
│   └── README.md     # 技能文档
```

#### 技能定义

```json
{
  "name": "code-review",
  "description": "执行代码审查并提供改进建议",
  "prompt": "你是一个代码审查专家。请审查以下代码，关注：\n\n1. 代码质量\n2. 安全性\n3. 性能\n4. 可维护性\n\n为每个问题提供具体的修复建议。",
  "tools": ["Read", "Grep", "Bash"],
  "allowedCommands": ["git diff", "npm test"]
}
```

#### 使用技能

> **说明**：插件是 Claude Code 的扩展机制（区别于简单的 skill 文件）。`plugin init` 会在 `~/.claude/skills/<name>/` 下创建脚手架并自动加载。

```bash
# 在交互会话中调用技能
# 输入 / 后跟技能名称，例如：
# /code-review

# 启动一个新插件（脚手架）
claude plugin init my-plugin
# 等价于
claude plugin new my-plugin

# 安装插件（来自 marketplace）
claude plugin install <plugin>
# 安装指定 marketplace 的插件
claude plugin install plugin@marketplace

# 列出已安装插件
claude plugin list

# 查看插件详细信息（含组件清单与预估 token 成本）
claude plugin details <name>

# 启用 / 禁用已安装插件
claude plugin enable <plugin>
claude plugin disable <plugin>

# 卸载插件
claude plugin uninstall <plugin>
# 等价于
claude plugin remove <plugin>
```

---

## 5. 最佳实践

### 5.1 提示词工程

#### 有效提示词原则

| 原则 | 示例 |
|------|------|
| **明确具体** | ❌ "修复这个 bug"<br>✅ "修复 src/api/user.ts:45 的空指针异常" |
| **提供上下文** | 包含相关代码片段、文件路径、错误信息 |
| **分解任务** | 复杂任务分步骤执行 |
| **指定格式** | "用表格展示结果" / "用 JSON 格式输出" |

#### 提示词模板

```typescript
// 通用任务模板
const taskTemplate = `
任务: {task_description}

背景信息:
- 项目: {project_name}
- 技术栈: {tech_stack}
- 相关文件: {relevant_files}

约束条件:
{constraints}

请执行任务并报告结果。
`;

// 代码审查模板  
const reviewTemplate = `
审查以下代码变更:

Diff:
{diff_content}

重点关注:
1. {focus_area_1}
2. {focus_area_2}

请提供具体的改进建议。
`;
```

### 5.2 权限管理

#### 权限模式选择

| 场景 | 推荐模式 | 说明 |
|------|---------|------|
| 日常开发 | `auto` | AI 辅助决策，只读操作自动允许 |
| 代码审查 | `default` | 每次写入操作确认 |
| 演示环境 | `bypass` | 完全信任，快速执行 |
| 生产环境 | `default` + 严格规则 | 最大安全性 |

#### 自定义权限规则

```json
// ~/.claude/config.json
{
  "permissions": {
    "alwaysAllow": [
      "Bash(git status:*)",
      "Bash(ls:*)",
      "Read(src/**)",
      "Glob"
    ],
    "alwaysDeny": [
      "Bash(sudo:*)",
      "Bash(chmod 777:*)",
      "Write(/etc/**)"
    ],
    "alwaysAsk": [
      "Bash(rm -rf:*)",
      "Bash(docker rmi:*)",
      "Write(/tmp/**)"
    ]
  }
}
```

### 5.3 上下文管理

#### 高效上下文使用

```bash
# 1. 利用 .claude.md 文件
# 在项目根目录创建 .claude.md
echo "# 项目上下文

## 技术栈
- Node.js 20
- Express.js
- PostgreSQL 15

## 约定
- 使用 async/await
- 错误处理使用自定义 Error 类

## 关键文件
- src/routes/ - API 路由
- src/services/ - 业务逻辑
" > ./.claude.md

# 2. 定期压缩对话（在交互会话内输入）
# /compact

# 3. 开新会话处理独立任务
claude  # 新会话
```

#### 上下文压缩策略

| 阶段 | Token 占比 | 策略 |
|------|-----------|------|
| 0-50% | 正常 | 无需处理 |
| 50-80% | 警告 | 注意提示词长度 |
| 80-90% | 危险 | 使用 /compact |
| 90%+ | 临界 | 自动压缩触发 |

### 5.4 多 Agent 协作

#### 适用场景

| 场景 | 适用 | 不适用 |
|------|------|--------|
| 并行代码生成 | ✅ | |
| 独立模块开发 | ✅ | |
| 大规模重构 | ✅ | |
| 简单修复 | | ❌ |
| 单文件修改 | | ❌ |

#### 团队协作示例

```bash
# 在交互会话中定义子 Agent（在提示中要求 Claude 创建）：
# "请创建一个代码审查团队，包含安全审查、性能审查、风格审查三个角色"

# 使用 --agents 参数定义自定义 Agent（JSON 格式）
claude --agents '{"reviewer": {"description": "Reviews code", "prompt": "You are a code reviewer"}}'

# 启动后台 Agent（立即返回，通过 claude agents 管理）
claude --bg "运行后台任务"
# 等价于
claude --background "运行后台任务"

# 查看后台 Agent（交互式 TTY 必需）
claude agents

# JSON 格式查看所有会话（脚本化，非 TTY 友好）
claude agents --json

# 包含已完成的会话
claude agents --json --all

# 仅显示指定 cwd 的会话
claude agents --cwd /path/to/project

# 设置后台会话的默认模型
claude agents --model claude-sonnet-5
```

### 5.5 会话管理

#### 会话持久化

```bash
# 自动保存
# 所有会话自动保存在 ~/.claude/ 目录下

# 列出后台 Agent（交互式 TTY）
claude agents

# JSON 格式查看所有会话（脚本化）
claude agents --json

# 恢复指定会话
claude -r <session-id>

# 继续上次会话（当前目录最近一次）
claude --continue

# 恢复时创建新 session ID（不覆盖原 session）
claude -r <session-id> --fork-session

# 禁用会话持久化（仅 -p/--print 模式）
claude -p "..." --no-session-persistence
```

#### 最佳实践

1. **重要任务开新会话** - 保持会话主题清晰
2. **定期保存** - 使用 /compact 压缩上下文
3. **善用 resume** - 中断后可继续
4. **会话归档** - 完成后使用 /clear 清屏

---

## 6. FAQ 与故障排除

### 6.1 常见问题

#### Q: 权限被拒绝怎么办？

**A:** 按以下步骤排查：

```bash
# 1. 使用 safe-mode 排除配置问题
claude --safe-mode

# 2. 启动会话时指定权限模式（可选: acceptEdits | auto | bypassPermissions | manual | dontAsk | plan）
claude --permission-mode auto
claude --permission-mode acceptEdits
claude --permission-mode plan

# 3. 启动时允许特定工具（支持逗号或空格分隔）
claude --allowedTools "Bash(git *) Edit"
claude --allowed-tools Read,Glob,Grep

# 4. 显式拒绝某些工具
claude --disallowedTools "Bash(rm *) Write"
claude --disallowed-tools WebFetch

# 5. 对于特定工具，可以在会话中使用 /permissions 配置
```

#### Q: 对话太长变慢怎么办？

**A:** 上下文膨胀会导致性能下降：

```bash
# 1. 在会话内手动压缩（输入 / 后回车）
/compact

# 2. 启动会话时使用 --bare 最小化模式（跳过 CLAUDE.md 等）
claude --bare

# 3. 开新会话（复杂任务的最后手段）
claude  # 新会话
```

#### Q: 如何恢复意外中断的会话？

```bash
# 恢复指定会话
claude -r <session-id>

# 继续上次会话（当前目录最近一次）
claude --continue

# 从 PR 恢复会话（PR 编号）
claude --from-pr 123

# 从 PR 恢复会话（URL）
claude --from-pr https://github.com/owner/repo/pull/456

# 无参数打开交互式选择器
claude --resume

# 恢复时创建新 session ID
claude -r <session-id> --fork-session
```

#### Q: 工具执行失败怎么办？

**A:** 常见原因和解决方案：

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| 超时 | 命令执行时间过长 | 增加 timeout 参数 |
| 权限拒绝 | 未授权操作 | 检查权限规则 |
| 路径不存在 | 文件/目录不存在 | 确认路径正确 |
| 依赖缺失 | 缺少依赖项 | 先安装依赖 |

### 6.2 架构相关问题

#### Q: 为什么选择 Ink 而非原生 TUI 库？

**A:** Ink 的优势：

1. **React 生态** - 140+ 组件复用
2. **声明式 UI** - 更容易维护复杂界面
3. **社区活跃** - 大量第三方组件
4. **开发效率** - 热更新支持

```typescript
// Ink 组件示例
import { Text, Box } from 'ink';
const Component = () => (
  <Box>
    <Text color="green">Success!</Text>
  </Box>
);
```

#### Q: 为什么使用 Bun 而非 Node.js？

**A:** Bun 的优势：

| 方面 | Bun | Node.js |
|------|-----|---------|
| 启动速度 | ~50ms | ~200ms |
| TypeScript | 原生支持 | 需要编译 |
| Bundle | 内置 | 需要 esbuild |
| 包管理 | 高性能 | 较慢 |

#### Q: Feature Flag 如何工作？

**A:** 基于 GrowthBook 的 feature flags：

```typescript
// 定义特性
const FEATURES = {
  VOICE_MODE: 'voice-mode',
  PROACTIVE: 'proactive-mode',
  // ...
};

// 使用特性
if (feature('VOICE_MODE')) {
  enableVoiceInput();
}

// 远程配置（GrowthBook）
const gb = new GrowthBook({
  apiHost: 'https://cdn.growthbook.io',
  clientKey: 'sdk-xxx',
});
gb.loadFeatures();

// 特性实验
gb.setAttributes({ userId: '123', plan: 'pro' });
if (gb.isOn('pro-mode')) {
  // Pro 用户专属功能
}
```

#### Q: 工具调用循环如何避免无限循环？

**A:** 多种保护机制：

```typescript
// 1. 最大轮次限制
const MAX_TURNS = 100;
if (turnCount >= MAX_TURNS) {
  throw new Error('Maximum turns exceeded');
}

// 2. 预算控制
const MAX_TOTAL_TOKENS = 100000;
if (totalTokens > MAX_TOTAL_TOKENS) {
  yield { type: 'budget_exceeded' };
  break;
}

// 3. 重复检测
const seenToolSeq = new Set<string>();
const toolSeq = toolCalls.map(t => t.name).join(',');
if (seenToolSeq.has(toolSeq)) {
  yield { type: 'loop_detected' };
  break;
}
seenToolSeq.add(toolSeq);
```

### 6.3 性能优化

#### 启动慢

```bash
# 诊断安装环境
claude doctor

# 使用最小化模式启动（跳过 CLAUDE.md、插件、预取等）
claude --bare

# 常见原因:
# 1. 网络问题 - 检查 API 连接
# 2. 认证问题 - 重新登录
claude auth status        # 先查看认证状态
claude auth logout        # 登出现有会话
claude auth login         # 重新登录（默认 Claude 订阅）

# Console 模式登录（API 用量计费）
claude auth login --console
# 或使用 API Key（避免登录）
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### 工具执行慢

```bash
# 在会话内查看使用统计（输入 / 后选择 cost）
/cost

# 使用更小的模型处理简单任务（支持别名或完整模型名）
claude --model haiku
claude --model claude-haiku-4-5-20251001

# 设置主模型 + 回退模型（仅 --print 模式）
claude -p "..." --fallback-model haiku,sonnet

# 压缩对话历史（在会话内）
/compact
```

#### 内存占用高

```bash
# 查看后台 Agent 数量
claude agents --json | jq 'length'

# 删除项目状态（谨慎操作，建议先 dry-run）
claude project purge /path/to/project --dry-run   # 仅列出，不删除
claude project purge /path/to/project -y          # 跳过确认

# 清理所有项目状态
claude project purge --all -y

# 启用调试日志定位问题（逗号分隔多个分类）
claude --debug api,hooks
```

---

## 附录

### A. 关键文件路径

| 功能 | 路径 |
|------|------|
| CLI 入口 | `src/main.tsx` |
| 查询引擎 | `src/QueryEngine.ts` |
| 查询管道 | `src/query.ts` |
| 工具注册 | `src/tools.ts` |
| 命令注册 | `src/commands.ts` |
| 工具基类 | `src/Tool.ts` |
| API 客户端 | `src/services/api/claude.ts` |
| MCP 客户端 | `src/services/mcp/client.ts` |
| 权限系统 | `src/hooks/useCanUseTool.tsx` |
| 上下文压缩 | `src/services/compact/compact.ts` |
| IDE 桥接 | `src/bridge/` |
| 自动记忆 | `src/services/extractMemories/` |
| 记忆存储 | `src/memdir/` |
| 自动文档 | `src/services/MagicDocs/` |
| 后台记忆合并 | `src/services/autoDream/` |
| 提示建议 | `src/services/PromptSuggestion/` |
| 协调器模式 | `src/coordinator/` |
| 任务系统 | `src/tasks/` |
| LSP 管理 | `src/services/lsp/` |
| 远程托管设置 | `src/services/remoteManagedSettings/` |
| 组织策略限制 | `src/services/policyLimits/` |
| 团队记忆同步 | `src/services/teamMemorySync/` |
| 跨环境设置同步 | `src/services/settingsSync/` |
| 输出样式 | `src/outputStyles/` |
| 键盘绑定 | `src/keybindings/` |
| Vim 模式 | `src/vim/` |
| 语音输入 | `src/voice/` + `src/services/voice.ts` |
| 远程会话 | `src/remote/` |
| Server 模式 | `src/server/` |
| REPL 启动 | `src/screens/REPL.tsx` |
| 启动状态 | `src/bootstrap/state.ts` |

### B. 内置工具清单

| 工具 | 功能 | 只读 |
|------|------|------|
| `AgentTool` | 生成子 Agent | ❌ |
| `AskUserQuestionTool` | 向用户提问 | ✅ |
| `BashTool` | 执行 Shell 命令 | ❌ |
| `BriefTool` | 生成摘要 | ✅ |
| `ConfigTool` | 配置管理 | ❌ |
| `EnterPlanModeTool` | 进入计划模式 | ✅ |
| `ExitPlanModeTool` | 退出计划模式 | ✅ |
| `ExitWorktreeTool` | 退出 Git Worktree | ✅ |
| `FileEditTool` | 编辑文件 | ❌ |
| `FileReadTool` | 读取文件 | ✅ |
| `FileWriteTool` | 写入文件 | ❌ |
| `GlobTool` | 文件模式匹配 | ✅ |
| `GrepTool` | 内容搜索 | ✅ |
| `ListMcpResourcesTool` | 列出 MCP 资源 | ✅ |
| `MCPTool` | 调用 MCP 工具 | ❌ |
| `NotebookEditTool` | 编辑 Notebook | ❌ |
| `PowerShellTool` | PowerShell 命令（Windows） | ❌ |
| `ReadMcpResourceTool` | 读取 MCP 资源 | ✅ |
| `RemoteTriggerTool` | 远程触发 | ❌ |
| `REPLTool` | REPL 执行 | ❌ |
| `ScheduleCronTool` | 定时任务 | ❌ |
| `SendMessageTool` | Agent 通信 | ❌ |
| `SkillTool` | 执行技能 | ❌ |
| `SleepTool` | 延迟执行 | ✅ |
| `SyntheticOutputTool` | 结构化输出 | ✅ |
| `TaskCreateTool` | 创建任务 | ❌ |
| `TaskGetTool` | 获取任务详情 | ✅ |
| `TaskListTool` | 列出任务 | ✅ |
| `TaskOutputTool` | 任务输出 | ✅ |
| `TaskStopTool` | 停止任务 | ❌ |
| `TaskUpdateTool` | 更新任务 | ❌ |
| `TeamCreateTool` | 创建团队 | ❌ |
| `TeamDeleteTool` | 删除团队 | ❌ |
| `TodoWriteTool` | 写入 Todo 列表 | ❌ |
| `ToolSearchTool` | 延迟发现工具 | ✅ |
| `McpAuthTool` | MCP OAuth 认证 | ❌ |

### C. Slash 命令清单

| 命令 | 功能 | 类型 |
|------|------|------|
| `/add-dir` | 添加上下文目录 | prompt |
| `/advisor` | 配置顾问模型 | local |
| `/agents` | Agent 管理 | prompt |
| `/branch` | 分支操作 | prompt |
| `/btw` | 插入注释 | local |
| `/chrome` | Chrome 集成 | local-jsx |
| `/clear` | 清屏 | local |
| `/commit` | 创建提交 | prompt |
| `/compact` | 压缩上下文 | prompt |
| `/config` | 配置管理 | local-jsx |
| `/context` | 查看上下文 | local |
| `/copy` | 复制内容 | local |
| `/cost` | 查看成本 | local |
| `/diff` | 查看变更 | prompt |
| `/doctor` | 诊断检查 | local-jsx |
| `/effort` | 设置努力程度 | local |
| `/init` | 初始化项目 | prompt |
| `/login` | 登录 | local |
| `/logout` | 登出 | local |
| `/memory` | 内存管理 | prompt |
| `/mcp` | MCP 管理 | local-jsx |
| `/pr_comments` | PR 评论 | prompt |
| `/resume` | 恢复会话 | local-jsx |
| `/review` | 代码审查 | prompt |
| `/share` | 分享会话 | local |
| `/skills` | 技能管理 | local-jsx |
| `/tasks` | 任务管理 | prompt |
| `/theme` | 主题设置 | local |
| `/version` | 版本信息 | local |
| `/vim` | Vim 模式 | local |

---

**文档版本**: 1.3
**编写日期**: 2026-07-21
**基于源码版本**: 2026-03-31 (泄露版)
**本地验证版本**: claude 2.1.215 (darwin-arm64)

---

## 命令验证摘要（v1.3 更新）

本版本针对教程中所有可执行命令逐一通过本地 `claude --help` 及子命令 `claude <subcommand> --help` 进行了**实际验证**：

| 命令类别 | 验证方式 | 关键修正 |
|---------|---------|---------|
| 主 CLI 选项 | `claude --help` | 确认 `--add-dir`、`--continue`、`--resume/-r`、`--from-pr`、`--fork-session`、`--allowedTools`、`--disallowedTools`、`--bare`、`--safe-mode`、`--debug`、`--bg`、`--agents`、`--permission-mode`、`--model`、`--effort` 均存在 |
| 认证 | `claude auth --help` | 修正 `claude auth login`（不是 `claude login`），新增 `--console`、`--sso`、`--claudeai` 选项 |
| MCP | `claude mcp --help` | 完整补全 `add/list/get/remove/login/logout/serve` 子命令；修正 `--transport`、`-e`、`-s`、`-H` 选项 |
| Plugin | `claude plugin --help` | 修正 `plugin init` 路径（`~/.claude/skills/<name>/`），新增 `details/enable/disable/install/uninstall/list` |
| Agents | `claude agents --help` | 修正 `--json`、`--all`、`--cwd`、`--model`、`--permission-mode` 选项 |
| Project | `claude project purge --help` | 补全 `--dry-run`、`-y`、`--all` 选项 |
| 模型 ID | `claude --help` 中 `--model` 说明 | 支持别名 `fable/opus/sonnet` 或完整名称如 `claude-fable-5` |
| Session 恢复 | `claude --help` | 修正 `--fork-session` 用法（与 `-r`/`--continue` 配合）|

---

## 7. 高级特性深度剖析

本章聚焦代码扫描中发现的**教程前六章未覆盖**的关键子系统，面向架构师与高级开发者。

### 7.1 自动记忆系统（memdir/）

Claude Code 具备**自动记忆提取与持久化**能力，无需用户手动维护笔记。

#### 核心机制

```
会话结束 (handleStopHooks)
    │
    ▼
extractMemories 服务
    │
    ▼
fork 子 Agent（runForkedAgent）  ← 共享父 prompt cache
    │
    ▼
扫描 ~/.claude/projects/<path>/memory/
    │
    ▼
写入新的 MEMORY.md / topic 文件
```

#### 三种记忆类型

| 类型 | 文件 | 说明 |
|------|------|------|
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | 用户全局偏好 |
| **项目记忆** | `<project>/CLAUDE.md` | 项目级上下文 |
| **自动记忆** | `~/.claude/projects/<hash>/memory/` | 会话自动提炼的知识 |

#### 代码核心

```typescript
// src/services/extractMemories/extractMemories.ts
// 在每个查询循环结束（无工具调用的最终响应）触发
// 使用 forked agent 模式，确保与父对话共享 prompt cache
export function initExtractMemories(): void {
  handleStopHooks.push(async (messages, context) => {
    const memPath = getAutoMemPath()
    if (!isAutoMemoryEnabled()) return
    if (!hasToolCallsInLastAssistantTurn(messages)) {
      // 调用 forked agent 提取记忆
      await runForkedAgent({
        prompt: buildExtractPrompt(messages),
        cacheSafeParams: createCacheSafeParams(context),
      })
    }
  })
}
```

#### SessionMemory（会话级摘要）

`src/services/SessionMemory/` 维护会话级别的**结构化摘要**，用于 `/resume` 时恢复上下文：

```typescript
// src/services/SessionMemory/prompts.ts - 默认摘要模板
const DEFAULT_SESSION_MEMORY_TEMPLATE = `
# Session Title
_A short and distinctive 5-10 word descriptive title..._

# Current State
_What is actively being worked on right now?_

# Files and Functions
_What are the important files? Why are they relevant?_

# Errors & Corrections
_Errors encountered and how they were fixed._

# Worklog
_Step by step, what was attempted, done?_
`
```

#### autoDream（自动记忆合并）

后台定期触发 `/dream` 命令，将多个会话的记忆合并整理：

```typescript
// src/services/autoDream/autoDream.ts
// 三重门控（cheap → expensive）：
// 1. 时间门：距离上次合并 ≥ minHours
// 2. 会话门：自上次合并以来有 ≥ minSessions 个新会话
// 3. 锁门：没有其他进程正在合并
```

#### Magic Docs（自动文档维护）

支持特殊标记的 Markdown 文件（`# MAGIC DOC: [title]`），Claude Code 会在后台周期性地用 forked subagent 自动更新内容。

#### 适用场景

- **长期项目**：自动积累项目知识，无需每次重新告知 Claude
- **跨会话工作**：通过 `/resume` 加载 SessionMemory 摘要
- **团队协作**：通过 Team Memory Sync 在组织内共享

### 7.2 Forked Agent 模式

这是 Claude Code **极其重要**的内部模式，用于运行后台任务并共享父 prompt cache，显著降低成本。

#### 核心优势

- **共享 Prompt Cache**：fork 出的子 agent 与父 agent 共享前 N 个 token 的缓存，避免重复计费
- **状态隔离**：可变状态独立，防止干扰主循环
- **完整用量追踪**：递归追踪整棵 fork 树的 token 使用

#### 关键代码

```typescript
// src/utils/forkedAgent.ts
export type CacheSafeParams = {
  systemPrompt: SystemPrompt    // 必须与父相同
  tools: Tools[]                // 必须与父相同
  model: string                 // 必须与父相同
  userContext: UserContext      // 必须与父相同
  thinkingConfig: ThinkingConfig
}

export async function runForkedAgent(params: {
  prompt: string
  cacheSafeParams: CacheSafeParams
  abortController: AbortController
}): Promise<...>
```

#### 哪些场景使用 fork

| 场景 | 实现 |
|------|------|
| 自动记忆提取 | `extractMemories` |
| Magic Docs 更新 | `MagicDocs` |
| AutoDream 合并 | `autoDream` |
| Agent 进度摘要 | `AgentSummary`（协调器模式） |
| Prompt 建议 | `PromptSuggestion` |

### 7.3 企业与团队功能

#### Remote Managed Settings（远程托管设置）

企业管理员可通过 API 强制推送配置：

```
src/services/remoteManagedSettings/
├── index.ts            # 主流程
├── types.ts            # 类型定义
```

- **Eligibility**：Console 用户全部可用；OAuth 用户仅 Enterprise/Team 订阅可用
- **Fail open**：API 失败时不阻塞
- **ETag 缓存**：基于校验和减少网络流量

#### Policy Limits（组织策略限制）

管理员可禁用某些 CLI 功能（`src/services/policyLimits/`）：

- 仅 Team / Enterprise 用户可用
- 失败开放（非阻塞）
- 与 Remote Managed Settings 共享架构

#### Team Memory Sync（团队记忆同步）

按 Git remote 哈希**作用域化**的团队记忆共享：

```typescript
// src/services/teamMemorySync/index.ts
// API 契约：
// GET  /api/claude_code/team_memory?repo={owner/repo}
// PUT  /api/claude_code/team_memory?repo={owner/repo}
```

- **Pull 语义**：服务端胜出
- **Push 语义**：增量上传（基于内容哈希）
- **删除不传播**：避免误删团队数据

#### Settings Sync（设置同步）

跨环境同步用户设置和记忆文件：

```typescript
// src/services/settingsSync/index.ts
// 交互式 CLI：增量上传本地设置到远端
// CCR：插件安装前下载远端设置到本地
```

### 7.4 Prompt Suggestion（提示建议）

在每轮对话结束后，预测并显示下一个可能的用户提示。

```typescript
// src/services/PromptSuggestion/index.ts
// 启用条件：
// 1. 环境变量 CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION 未设为 false
// 2. 用户启用了 speculation（启动时预热下一个请求）
```

**关键价值**：

- 减少用户输入摩擦
- 通过预热下一个请求（speculation）**隐藏网络延迟**

### 7.5 协调器模式（Coordinator Mode）

> 由 `feature('COORDINATOR_MODE')` 控制，通过环境变量 `CLAUDE_CODE_COORDINATOR_MODE=1` 启用

#### 设计目标

当面对**大型复杂任务**（如大型代码库迁移）时，由一个协调器 Agent 调度多个内部 Worker Agent 协作。

#### 内部工具集

```typescript
// src/coordinator/coordinatorMode.ts
const INTERNAL_WORKER_TOOLS = new Set([
  TEAM_CREATE_TOOL_NAME,
  TEAM_DELETE_TOOL_NAME,
  SEND_MESSAGE_TOOL_NAME,
  SYNTHETIC_OUTPUT_TOOL_NAME,
])
```

#### AgentSummary（后台摘要）

协调器模式下，每 ~30 秒 fork 子 agent 一次，生成 1-2 句进度摘要供 UI 显示：

```typescript
// src/services/AgentSummary/index.ts
const SUMMARY_INTERVAL_MS = 30_000
```

### 7.6 任务系统（tasks/）

Claude Code 提供**多类型后台任务**抽象：

| 类型 | 路径 | 用途 |
|------|------|------|
| `LocalShellTask` | `tasks/LocalShellTask/` | 本地 Shell 后台任务 |
| `LocalAgentTask` | `tasks/LocalAgentTask/` | 本地 Agent 任务 |
| `InProcessTeammateTask` | `tasks/InProcessTeammateTask/` | 进程内团队成员 |
| `RemoteAgentTask` | `tasks/RemoteAgentTask/` | 远程 Agent 任务 |
| `DreamTask` | `tasks/DreamTask/` | 记忆合并任务 |

#### 任务工具（面向 LLM）

工具层通过以下工具让模型管理任务：

| 工具 | 功能 |
|------|------|
| `TaskCreateTool` | 创建任务 |
| `TaskUpdateTool` | 更新任务 |
| `TaskGetTool` | 获取任务 |
| `TaskListTool` | 列出任务 |
| `TaskOutputTool` | 读取任务输出 |
| `TaskStopTool` | 停止任务 |
| `TodoWriteTool` | 写入 Todo 列表 |

### 7.7 LSP 集成（Language Server Protocol）

Claude Code 集成 LSP 以提供**语义级代码理解**：

```
src/services/lsp/
├── LSPManager.ts          # LSP 连接管理
├── LSPServerProcess.ts    # 服务器进程包装
├── claudeCodeLspDefs.ts   # 内置 LSP 定义
└── lspClients/            # 各语言客户端
```

**关键能力**：
- 跳转到定义（Go to Definition）
- 查找引用（Find References）
- 重命名符号（Rename Symbol）
- 诊断信息（Diagnostics）
- 代码补全（Completions）

启用：`ENABLE_LSP_TOOL=true`

### 7.8 输出样式系统（outputStyles/）

支持自定义**输出风格**，影响 Claude 的回应方式：

```
~/.claude/output-styles/
├── explanatory.md          # 详细解释模式
├── learning.md             # 学习模式
└── ...
```

每个 `.md` 文件的 frontmatter 定义名称和描述，内容成为输出风格提示词。

### 7.9 键盘绑定系统（keybindings/）

Claude Code 提供完整的**键绑定配置**系统：

```typescript
// src/keybindings/schema.ts - Zod schema
// src/keybindings/defaultBindings.ts - 默认绑定
// src/keybindings/loadUserBindings.ts - 用户绑定加载
```

配置文件：`~/.claude/keybindings.json`

### 7.10 Vim 模式（vim/）

完整的 Vim 模拟层：

```
src/vim/
├── motions.ts        # 动作（h/j/k/l/w/b/e 等）
├── operators.ts      # 操作符（d/y/c）
├── textObjects.ts    # 文本对象（iw/aw/i"/a" 等）
├── transitions.ts    # 模式切换
└── types.ts          # 类型定义
```

### 7.11 语音输入（voice/）

> 由 `feature('VOICE_MODE')` 控制

支持**实时语音转文字**输入：

```
src/services/
├── voice.ts              # 语音服务主流程
├── voiceKeyterms.ts      # 关键字识别
└── voiceStreamSTT.ts     # 流式 STT
```

### 7.12 远程会话（remote/）

支持通过远程服务器托管 Claude Code 会话：

```
src/remote/
├── RemoteSession.ts      # 远程会话管理
└── ...
```

`--remote-control` 启动远程控制模式。

### 7.13 IDE 集成（hooks/）

Claude Code 提供丰富的 **React Hooks** 用于 UI 与 IDE 集成：

| Hook | 用途 |
|------|------|
| `useIDEIntegration` | IDE 连接管理 |
| `useDiffInIDE` | 在 IDE 中显示 diff |
| `useIdeSelection` | 读取 IDE 当前选中 |
| `useIdeAtMentioned` | 检测 @ 提及 |
| `useChromeExtensionNotification` | Chrome 扩展通知 |
| `usePromptsFromClaudeInChrome` | 从 Chrome 接收提示 |
| `useMailboxBridge` | 邮箱桥接 |
| `useSSHSession` | SSH 会话支持 |
| `useTeleportResume` | 跨设备恢复会话 |

### 7.14 上下文压缩策略详解

源码中识别到**多种压缩策略**：

```typescript
// src/services/compact/compact.ts
type PartialCompactDirection =
  | 'system_reminder'   // 系统提醒式压缩
  | 'microcompact'      // 微压缩（snip 旧工具结果）
  | 'full'              // 完整压缩
```

#### 触发条件

| 触发器 | 行为 |
|--------|------|
| Token 使用 ≥ 80% | 警告，建议压缩 |
| Token 使用 ≥ 92% | 自动完整压缩 |
| 用户输入 `/compact` | 手动完整压缩 |
| 工具结果过大 | snip（截断） |
| 注入 `<system-reminder>` | 上下文微调 |

#### 关键技术

- **MICROCOMPACT**：保留工具调用，但截断工具结果文本
- **Boundary 标记**：注入 `SystemCompactBoundaryMessage` 标识压缩点
- **附件消息**：使用 `AttachmentMessage` 携带压缩后注入的文件内容

### 7.15 PowerShell 工具

Windows 平台专用 Shell 工具：

```typescript
// src/tools/PowerShellTool/prompt.ts
// 自动检测 PowerShell 版本（5.1 vs 7+）
// 根据版本应用不同的命令模式
```

启用：`process.platform === 'win32'` 时自动加载。

### 7.16 安全与审计

#### 配置验证（schemas/）

所有配置使用 **Zod schema** 严格验证：

```typescript
// src/schemas/settings.schema.ts
// 失败的配置文件默认静默忽略（非交互模式）
// 交互模式下显示 InvalidConfigDialog
```

#### Telemetry 与日志

| 系统 | 路径 | 说明 |
|------|------|------|
| GrowthBook | `services/analytics/growthbook.ts` | Feature Flag 服务 |
| OpenTelemetry | `services/api/logging.ts` | 链路追踪 |
| Statsig | `services/analytics/statsig.ts` | 指标统计 |
| VCR | `services/vcr.ts` | API 录制回放 |
| DiagLogs | `utils/diagLogs.ts` | 诊断日志 |

#### 错误分类

```typescript
// src/services/api/errors.ts
// 细粒度错误分类：
// - rate_limit
// - overloaded
// - authentication
// - billing
// - server_error
// - network
// - invalid_request
```

每类错误都有独立的重试策略和用户提示。

### 7.17 文件状态缓存（FileStateCache）

Claude Code 维护**文件状态缓存**以加速读取：

```typescript
// src/utils/fileStateCache.ts
type FileStateCache = {
  [path: string]: {
    content: string
    mtime: number
    hash: string
  }
}
```

**关键用途**：
- `FileReadTool` 命中缓存时返回 `FILE_UNCHANGED_STUB`，避免重新读取
- 工具调用循环判断文件是否被修改
- Forked agent 克隆缓存以避免污染

### 7.18 启动时序细节

源码中识别到的**详细启动序列**：

```typescript
// src/main.tsx 启动顺序（精简版）
async function bootstrap() {
  // 第一阶段：副作用（不阻塞）
  profileCheckpoint('main_tsx_entry')
  startMdmRawRead()           // 并行读取 MDM 设置
  startKeychainPrefetch()     // 并行预取 Keychain
  startInitDataPrefetch()     // 并行预取初始化数据
  startAnalyticsPrefetch()    // 并行预取分析配置
  
  // 第二阶段：核心初始化
  await loadCliConfig()
  await initGrowthBook()
  await ensureKeychainPrefetchCompleted()
  await waitForRemoteManagedSettingsToLoad()
  
  // 第三阶段：应用启动
  await startApp()
}
```

**并行预取节省时间**：~135-200ms

### 7.19 Bootstrap 与状态管理

```
src/bootstrap/
└── state.ts            # 全局启动状态

src/state/
├── AppState.ts         # 应用级状态
└── ...
```

`bootstrap/state.ts` 维护**进程级不可变状态**：

```typescript
// 通过 getter 函数访问，避免模块间循环依赖
export const getOriginalCwd = () => originalCwd
export const getKairosActive = () => kairosActive
export const getIsRemoteMode = () => isRemoteMode
export const getSessionId = () => sessionId
```

### 7.20 性能监控

源码内置**性能监控点**：

| 监控点 | 说明 |
|--------|------|
| `profileCheckpoint(name)` | 标记启动阶段 |
| `logForDebugging(category)` | 调试日志分类 |
| `withDiagnosticsTiming()` | 自动测量函数耗时 |
| `tokenStatsToStatsigMetrics()` | Token 使用上报 |
| `useMemoryUsage()` Hook | 内存监控 |

### 7.21 Server 模式（server/）

> 由 `feature('DAEMON')` 控制

```typescript
// src/server/
// - createDirectConnectSession.ts
// - directConnectManager.ts
// - types.ts
```

允许 Claude Code 作为后台守护进程运行，供其他客户端连接。

### 7.22 Buddy（吉祥物彩蛋）

```
src/buddy/
├── Buddy.tsx          # 吉祥物组件
└── ...
```

包含**复活节彩蛋**：当用户输入特定命令时显示吉祥物动画。

### 7.23 本章小结

源码中**实际存在但官方文档较少提及**的子系统：

| 模块 | 用户可见性 | 架构意义 |
|------|-----------|----------|
| 自动记忆 | 高 | 长期任务连续性 |
| Forked Agent | 内部 | 成本与延迟优化 |
| Team Memory Sync | 中 | 团队协作 |
| Remote Managed Settings | 低（企业） | 企业治理 |
| Policy Limits | 低（企业） | 合规与限制 |
| Prompt Suggestion | 中 | UX 优化 |
| Coordinator Mode | 实验性 | 大型任务调度 |
| LSP 集成 | 高 | 语义级代码理解 |
| Output Styles | 中 | 输出定制 |
| Keybindings | 中 | 高级用户定制 |
| Vim 模式 | 中 | 键盘流用户 |
| 语音输入 | 中 | 多模态 |
| 远程会话 | 中 | 云端运行 |
| Magic Docs | 低 | 自动文档 |
| PowerShell 工具 | 低（Windows） | 跨平台 |

这些模块展现了 Claude Code 作为产品**远不止是一个 CLI 聊天工具**，而是一个**可扩展、多模态、可治理的企业级 AI 开发平台**。
