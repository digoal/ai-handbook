# 事实与来源台账

本文件是手册中版本敏感事实的唯一台账。章节通过稳定 ID 引用这里的声明；来源变化时先更新台账，再更新课程正文。

---

## 核验基线

### CC-000

- **声明**：首期内容在 Claude Code 2.1.214、macOS 15.7.7 上建立本机基线。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[Claude Code 版本](evidence/2.1.214/claude-version.txt)、[macOS 版本](evidence/2.1.214/macos-version.txt)
- **边界**：这是本手册的验证版本，不代表官方最新版本。

## 安装与认证

### CC-001

- **声明**：Claude Code 官方为 macOS 提供 Native Install，安装命令为 `curl -fsSL https://claude.ai/install.sh | bash`，并将其标为推荐方式。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Advanced setup — Install Claude Code](https://code.claude.com/docs/en/setup#install-claude-code)
- **边界**：本手册没有为了核验而重装 Claude Code。

### CC-002

- **声明**：Native Install 会在后台自动检查和安装更新，已下载的版本在下次启动时生效。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Advanced setup — Auto-updates](https://code.claude.com/docs/en/setup#auto-updates)
- **边界**：官方没有承诺固定检查间隔。

### CC-003

- **声明**：macOS 可以通过 Homebrew 安装 `claude-code` stable cask 或 `claude-code@latest` latest cask；Homebrew 安装不会由 Claude Code 自动更新。
- **等级**：官方核对、条件性
- **日期**：2026-07-19
- **来源**：[Advanced setup — Homebrew](https://code.claude.com/docs/en/setup#homebrew)
- **边界**：更新命令取决于安装时选择的 cask。

### CC-004

- **声明**：官方列出的 macOS 最低版本为 macOS 13.0，内存要求为 4 GB 以上，并需要网络连接。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Advanced setup — System requirements](https://code.claude.com/docs/en/setup#system-requirements)

### CC-005

- **声明**：首次交互式运行 `claude` 时会进入登录流程；macOS 上的登录凭据存储在加密的 macOS Keychain 中。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Authentication — Log in to Claude Code](https://code.claude.com/docs/en/authentication#log-in-to-claude-code)、[Credential management](https://code.claude.com/docs/en/authentication#credential-management)
- **边界**：浏览器打开方式、组织策略和环境变量认证可能改变具体流程。

### CC-006

- **声明**：Claude Code 访问需要受支持的 Claude 订阅、Anthropic Console 账户或受支持的第三方云提供商；免费 Claude.ai 计划不包含 Claude Code 访问。
- **等级**：官方核对、条件性
- **日期**：2026-07-19
- **来源**：[Authentication — Log in to Claude Code](https://code.claude.com/docs/en/authentication#log-in-to-claude-code)

## 本机 CLI

### CC-007

- **声明**：本机 `claude` 版本为 `2.1.214 (Claude Code)`；`-v` 和 `--version` 用于输出版本号。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[claude-version.txt](evidence/2.1.214/claude-version.txt)、[claude-help.txt](evidence/2.1.214/claude-help.txt)

### CC-008

- **声明**：直接运行 `claude` 默认启动交互式会话；`-p` 或 `--print` 用于非交互输出。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：`--print` 会跳过工作区信任对话框，不能把交互式课程步骤原样套用到它。

### CC-009

- **声明**：本机 `claude auth` 提供 `login`、`logout` 和 `status` 子命令。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[auth-help.txt](evidence/2.1.214/auth-help.txt)

### CC-010

- **声明**：本机 `claude doctor` 检查 Claude Code 安装健康状态，读取当前目录中的 settings 文件时不显示工作区信任提示；会话内 `/doctor` 才是可执行修复的完整检查。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[doctor-help.txt](evidence/2.1.214/doctor-help.txt)

### CC-011

- **声明**：本机 `claude install [target]` 安装 Claude Code native build，`target` 可以是 `stable`、`latest` 或具体版本；本机还显示 `--force` 选项。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[install-help.txt](evidence/2.1.214/install-help.txt)
- **边界**：仅验证了 help，没有执行安装或重装。

### CC-012

- **声明**：本机 `claude update` 与 `claude upgrade` 检查更新，并在有更新时安装。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[update-help.txt](evidence/2.1.214/update-help.txt)
- **边界**：仅验证了 help，没有执行更新；安装渠道可能影响实际更新路径。

### CC-013

- **声明**：本机 `-c`/`--continue` 继续当前目录最近的会话，`-r`/`--resume` 可以按 session ID 恢复，或打开带可选搜索词的选择器。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)

## 首次会话

### CC-014

- **声明**：首次在代码库中运行 Claude Code 时会进行工作区信任验证；信任按 git 仓库根目录保存，不在 git 仓库中时按启动目录处理。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Configure permissions — Project allow rules and workspace trust](https://code.claude.com/docs/en/permissions#project-allow-rules-and-workspace-trust)
- **边界**：直接从 home 目录启动时，信任只在当前会话保持，不会写入磁盘；每次启动都会重新询问，且没有设置可以持久化该信任。

### CC-015

- **声明**：Claude Code 的权限系统区分读取、文件修改和 Bash 命令等操作；是否提示取决于当前 permission mode 与已配置规则。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Configure permissions — Permission system](https://code.claude.com/docs/en/permissions#permission-system)
- **边界**：首期不复制完整模式表或内置只读命令列表，它们留到权限章节单独核验。

### CC-016

- **声明**：官方 quickstart 的首次改动流程会先定位文件、展示拟议变更，并按当前权限模式请求批准后再执行编辑。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Quickstart — Make your first code change](https://code.claude.com/docs/en/quickstart#step-5-make-your-first-code-change)
- **边界**：不同 permission mode、预批准规则或账户功能会改变是否显示提示。

### CC-017

- **声明**：官方 quickstart 提供 `/exit` 退出当前会话；本机 CLI 提供 `claude -c` 和 `claude -r` 继续或恢复会话。
- **等级**：官方核对、已实测
- **日期**：2026-07-19
- **来源**：[Quickstart — Essential commands](https://code.claude.com/docs/en/quickstart#essential-commands)
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)

### CC-018

- **声明**：本机 Claude Code 2.1.214 接受 `--permission-mode manual`，用于以 Manual permission mode 启动会话。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：这里只验证本机 2.1.214 的 CLI 可选值；完整 permission mode 行为留到权限章节核验。

## 上下文与会话

### CC-019

- **声明**：`-c`/`--continue` 继续当前项目最近会话；`-r`/`--resume` 打开恢复选择器，也可带 session ID 或显式名称恢复。
- **等级**：已实测、官方核对
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **来源**：[Manage sessions — Resume a session](https://code.claude.com/docs/en/sessions#resume-a-session)
- **边界**：Session 查找受当前项目及其 Git worktrees 限制；不要把 ID 当成全局句柄。

### CC-020

- **声明**：`--fork-session` 与 `--continue` 或 `--resume` 组合时创建新 session ID，原 session 保持不变。
- **等级**：已实测、官方核对
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **来源**：[Manage sessions — Branch a session](https://code.claude.com/docs/en/sessions#branch-a-session)
- **边界**：Fork 分支 conversation，不创建 Git branch；会话期临时批准不继承。

### CC-021

- **声明**：`-n`/`--name` 在启动时设置显式 session name；会话内可用 `/rename`，显式名称可供 `--resume <name>` 使用。
- **等级**：已实测、官方核对
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **来源**：[Manage sessions — Name your sessions](https://code.claude.com/docs/en/sessions#name-your-sessions)
- **边界**：自动显示标题不是显式恢复句柄。

### CC-022

- **声明**：`--no-session-persistence` 只适用于 `--print`，禁用该次运行的 session persistence，使其不能恢复。
- **等级**：已实测
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：只核验 help，没有执行会产生模型用量的 print 请求。

### CC-023

- **声明**：`/clear` 清空当前 context，但之前的 session 仍可通过恢复入口找到；它不是删除 transcript 的命令。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Manage sessions — Manage context within a session](https://code.claude.com/docs/en/sessions#manage-context-within-a-session)

### CC-024

- **声明**：`/compact [instructions]` 把 conversation 压缩为摘要，`/context` 显示当前 context 组成；compact 会重建会话层 prompt cache，但不修改磁盘文件。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Manage sessions — Manage context within a session](https://code.claude.com/docs/en/sessions#manage-context-within-a-session)、[Prompt caching — Compacting the conversation](https://code.claude.com/docs/en/prompt-caching#compacting-the-conversation)

## 指令与记忆

### CC-025

- **声明**：CLAUDE.md instructions 由 managed、user、project、local 等作用域组成；启动时从上层目录到工作目录追加加载，子目录 instructions 在访问对应文件时按需加载。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[How Claude remembers your project — Choose where to put CLAUDE.md files](https://code.claude.com/docs/en/memory#choose-where-to-put-claudemd-files)、[How CLAUDE.md files load](https://code.claude.com/docs/en/memory#how-claudemd-files-load)
- **边界**：Instructions 是 context，不是强制 permission policy。

### CC-026

- **声明**：CLAUDE.md 可用 `@path` 导入其他文件；相对路径按引用文件解析，递归导入最多 4 hops，项目首次外部 import 可能要求批准。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[How Claude remembers your project — Import additional files](https://code.claude.com/docs/en/memory#import-additional-files)
- **边界**：Import 内容仍进入 context，不是节省 token 的机制。

### CC-027

- **声明**：Auto memory 默认开启；项目 memory 包含 `MEMORY.md` 与可选主题文件，启动时加载 `MEMORY.md` 前 200 行或 25 KB，以先达到者为准。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[How Claude remembers your project — Auto memory](https://code.claude.com/docs/en/memory#auto-memory)
- **边界**：同一 Git 仓库的 worktrees 和子目录共享项目 memory；不得存储凭证。

### CC-028

- **声明**：`/memory` 列出 instruction 与 auto memory 位置并提供管理入口；会话中修改已加载的 CLAUDE.md 后，需要 `/clear`、`/compact` 或新会话重新加载。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[How Claude remembers your project — View and edit with /memory](https://code.claude.com/docs/en/memory#view-and-edit-with-memory)、[Prompt caching — Editing CLAUDE.md mid-session](https://code.claude.com/docs/en/prompt-caching#editing-claudemd-mid-session)

## 设置与权限

### CC-029

- **声明**：普通 settings 的优先级为 managed、命令行、local、project、user；permission rules 跨 scope 合并，并采用更严格结果，而不是简单覆盖。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Claude Code settings — Configuration scopes](https://code.claude.com/docs/en/settings#configuration-scopes)、[Configure permissions](https://code.claude.com/docs/en/permissions)

### CC-030

- **声明**：本机 2.1.214 的 `--permission-mode` 接受 `manual`、`acceptEdits`、`plan`、`auto`、`dontAsk` 和 `bypassPermissions`。
- **等级**：已实测、条件性
- **日期**：2026-07-19
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **来源**：[Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- **边界**：`auto` 受账户、模型、provider 和组织策略影响；本手册不使用 `bypassPermissions`。

### CC-031

- **声明**：永久 Bash 批准通常写入仓库根 `.claude/settings.local.json`；file-edit 批准只在当前 session 有效；workspace trust 影响项目 allow rules 是否应用。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Configure permissions — Permission system](https://code.claude.com/docs/en/permissions#permission-system)、[Project allow rules and workspace trust](https://code.claude.com/docs/en/permissions#project-allow-rules-and-workspace-trust)

### CC-032

- **声明**：Claude Code 对 settings、VCS 元数据和 shell 启动文件等 protected paths 应用额外写入确认；普通 allow rule 不能消除该保护。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Choose a permission mode — Protected paths](https://code.claude.com/docs/en/permission-modes#protected-paths)
- **边界**：`bypassPermissions` 的行为不属于本手册练习范围。

### CC-033

- **声明**：Sandbox 为 Bash 提供 macOS Seatbelt 文件系统和网络隔离；permissions 控制全部工具调用，两者独立且可组合。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)
- **边界**：Sandbox 不替代 Edit/Write permissions、deny rules 或 protected paths。

## Skills 与 slash commands

### CC-035

- **声明**：Built-in commands 由 CLI 实现；skills 是按需加载的 instructions，可由用户显式调用或由 Claude 在相关时选择。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Commands](https://code.claude.com/docs/en/commands)、[Extend Claude with skills](https://code.claude.com/docs/en/skills)

### CC-036

- **声明**：Custom commands 已合并到 skills；`.claude/commands/deploy.md` 与 `.claude/skills/deploy/SKILL.md` 都可创建 `/deploy`，旧 commands 文件继续工作。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Extend Claude with skills](https://code.claude.com/docs/en/skills)

### CC-037

- **声明**：项目级 skill 位于 `.claude/skills/<name>/SKILL.md`，用户级 skill 位于 `~/.claude/skills/<name>/SKILL.md`，作用范围不同。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Extend Claude with skills — Where skills live](https://code.claude.com/docs/en/skills#where-skills-live)

### CC-038

- **声明**：Skill 使用 `SKILL.md`，由 YAML frontmatter 和 Markdown instructions 组成；description 用于发现，正文在 skill 使用时才加载。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Extend Claude with skills — Create a skill](https://code.claude.com/docs/en/skills#create-a-skill)

### CC-039

- **声明**：Skill 可用 `/skill-name` 显式调用，也可在 description 与任务相关时由 Claude 自动选择；frontmatter 可控制调用方。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Extend Claude with skills — Control who invokes a skill](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill)
- **边界**：调用会产生模型用量；本手册不复制完整 frontmatter 字段表。

## Checkpoints

### CC-040

- **声明**：每个 user prompt 创建 checkpoint；Claude Code 跟踪其文件编辑工具所做的修改，checkpoint 与 session 一起保存。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Checkpointing — Automatic tracking](https://code.claude.com/docs/en/checkpointing#automatic-tracking)

### CC-041

- **声明**：`/rewind` 或空 prompt 时 double Esc 打开 rewind menu；输入框有文字时 double Esc 先清空输入。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Checkpointing — Rewind and summarize](https://code.claude.com/docs/en/checkpointing#rewind-and-summarize)

### CC-042

- **声明**：Rewind 可恢复 code、conversation 或两者，也可从选定点开始或截至选定点 summarize；code restore 只在存在 tracked file changes 时出现。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Checkpointing — Rewind and summarize](https://code.claude.com/docs/en/checkpointing#rewind-and-summarize)

### CC-043

- **声明**：Checkpoint 不跟踪 Bash 命令、手工编辑和其他并发 session 的普通文件变化，也不替代 Git version control。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Checkpointing — Limitations](https://code.claude.com/docs/en/checkpointing#limitations)

## Hooks

### CC-044

- **声明**：Hooks 可来自 user、project、local、managed settings 和 plugins；部分 skill/subagent hooks 只在组件激活期间生效。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Hooks reference — Configuration](https://code.claude.com/docs/en/hooks)

### CC-045

- **声明**：当前 hooks reference 定义 `command`、`http`、`mcp_tool`、`prompt` 和 `agent` handler 类型。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Hooks reference — Hook handler fields](https://code.claude.com/docs/en/hooks)
- **边界**：HTTP、MCP、prompt 和 agent handlers 引入额外网络、连接或模型边界。

### CC-046

- **声明**：Hook 配置按 event、matcher group、handler 三层组织；matcher 语义取决于事件类型。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)

### CC-047

- **声明**：Command hook 从 stdin 接收 JSON；exit code 为 0 时 stdout 才按 hook JSON output 处理，`${CLAUDE_PROJECT_DIR}` 可引用项目根。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Hooks reference — Command hooks](https://code.claude.com/docs/en/hooks)

### CC-048

- **声明**：许多事件中 exit code 2 表示阻断并把 stderr 反馈给 Claude；其他非零 code 通常是非阻断错误，且不同事件效果不同。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Hooks reference — Exit code output](https://code.claude.com/docs/en/hooks)
- **边界**：工具执行后的事件无法撤销已经发生的操作。

### CC-049

- **声明**：Hook handler 有默认 timeout，也可用 `timeout` 覆盖；高频事件不应执行长任务、递归 Claude 调用或无界网络请求。
- **等级**：官方核对
- **日期**：2026-07-19
- **来源**：[Hooks reference — Hook handler fields](https://code.claude.com/docs/en/hooks)

## MCP

### CC-050

- **声明**：本机 `claude mcp` 提供 add、add-from-claude-desktop、add-json、get、help、list、login、logout、remove、reset-project-choices 和 serve 等管理入口。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[mcp-help.txt](evidence/2.1.214/mcp-help.txt)

### CC-051

- **声明**：本机 `claude mcp add` 接受 `stdio`、`sse`、`http` transport，默认 stdio；scope 接受 `local`、`user`、`project`，默认 local。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[mcp-add-help.txt](evidence/2.1.214/mcp-add-help.txt)
- **边界**：`add-json` help 只声明 stdio 或 SSE，不假设两个入口完全对称。

### CC-052

- **声明**：`mcp get` 和 `list` 不连接未批准的 project `.mcp.json` server，而是显示 pending approval；已批准 server 会进行 health check。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[mcp-help.txt](evidence/2.1.214/mcp-help.txt)、[mcp-get-help.txt](evidence/2.1.214/mcp-get-help.txt)

### CC-053

- **声明**：本机 `mcp login` 对 HTTP、SSE 或 claude.ai connector server 发起认证，`logout` 清除已存 OAuth 凭据。
- **等级**：已实测、条件性
- **日期**：2026-07-20
- **证据**：[mcp-help.txt](evidence/2.1.214/mcp-help.txt)、[mcp-login-help.txt](evidence/2.1.214/mcp-login-help.txt)
- **边界**：未执行登录或登出，不记录 token 存储细节。

### CC-054

- **声明**：`mcp remove --scope <scope> <name>` 从指定 scope 删除 server；省略 scope 时，help 声明从包含该名称的 scope 中删除。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[mcp-remove-help.txt](evidence/2.1.214/mcp-remove-help.txt)

### CC-055

- **声明**：顶层 `--mcp-config` 为 session 加载 MCP JSON 文件或字符串，`--strict-mcp-config` 忽略其他 MCP 来源。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：显式配置文件仍不得包含提交到仓库的真实凭证。

### CC-056

- **声明**：`claude mcp reset-project-choices` 重置当前项目 `.mcp.json` servers 的批准和拒绝选择。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[mcp-help.txt](evidence/2.1.214/mcp-help.txt)
- **边界**：未执行该命令；它不等于重置 workspace trust 或 settings。

## Subagents 与 worktrees

### CC-057

- **声明**：顶层 `--agent <agent>` 选择当前 session agent，`--agents <json>` 用 JSON object 临时定义 custom agents。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：真正启动 agent 会产生模型用量；持久 agent schema 以官方 [Subagents](https://code.claude.com/docs/en/sub-agents) 为准。

### CC-058

- **声明**：本机 `-w`/`--worktree [name]` 为 session 创建 Git worktree；`--tmux` 需要与 worktree 配合，可使用 iTerm2 native pane 或 classic tmux。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：未在当前仓库实际创建 worktree session。

### CC-059

- **声明**：`claude agents --json` 输出 active interactive/background sessions 的 JSON array，`--all` 让输出也包含已完成 sessions。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[agents-help.txt](evidence/2.1.214/agents-help.txt)
- **边界**：未保存真实 JSON 输出，避免泄露 session 与路径。

### CC-060

- **声明**：`claude agents` 可为 dispatched sessions 指定 model、effort、permission mode、settings、MCP config 和 plugin directories 等启动配置。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[agents-help.txt](evidence/2.1.214/agents-help.txt)
- **边界**：这些 flags 作用于 agent view 与 dispatched sessions，不是持久定义 schema。

### CC-061

- **声明**：`claude project purge` 删除项目 transcripts、tasks、file history 和 config entry；`--dry-run` 只列出待删内容。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[project-purge-help.txt](evidence/2.1.214/project-purge-help.txt)
- **边界**：未执行 purge；它不是 Git worktree cleanup 工具。

### CC-062

- **声明**：Worktree session 由顶层 `--worktree` 启动；本机 `claude agents --help` 没有 `--isolation` flag，agent definition 与 worktree CLI 是不同配置面。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)、[agents-help.txt](evidence/2.1.214/agents-help.txt)
- **边界**：不从 help 缺失推导持久 subagent frontmatter 的完整能力。

## Plugins

### CC-063

- **声明**：本机 `claude plugin` 提供 details、enable/disable、help、init、install、list、marketplace、prune、update、uninstall、validate、tag 和 eval 等入口。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[plugin-help.txt](evidence/2.1.214/plugin-help.txt)

### CC-064

- **声明**：`plugin init <name>` 在 `~/.claude/skills/<name>/` scaffold plugin，并在下次 session 作为 `<name>@skills-dir` 自动加载；可显式设置 author、email 和 description。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[plugin-init-help.txt](evidence/2.1.214/plugin-init-help.txt)
- **边界**：练习必须使用临时 HOME，避免写入真实用户目录。

### CC-065

- **声明**：`plugin validate <path>` 校验 plugin 或 marketplace manifest；`--strict` 把 warning 当作 exit 1。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[plugin-validate-help.txt](evidence/2.1.214/plugin-validate-help.txt)
- **边界**：结构校验不替代脚本、hook、MCP 或依赖安全审计。

### CC-066

- **声明**：`plugin marketplace` 提供 add、list、remove 和 update；add source 可为 URL、path 或 GitHub repo。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[plugin-marketplace-help.txt](evidence/2.1.214/plugin-marketplace-help.txt)
- **边界**：未添加任何 marketplace；添加来源会扩大供应链信任。

### CC-067

- **声明**：Plugin CLI 区分 install、enable/disable、update、uninstall 和 prune；update help 提示重启后应用。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[plugin-help.txt](evidence/2.1.214/plugin-help.txt)
- **边界**：未执行安装、更新或卸载。

### CC-068

- **声明**：顶层 `--plugin-dir` 和 `--plugin-url` 只为当前 session 加载 plugin，可重复指定；它们与 marketplace 持久安装不同。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)

### CC-069

- **声明**：`plugin tag` 创建 plugin release Git tag并校验 manifest/marketplace version 一致性；`plugin eval` 运行评测并可能产生模型用量。
- **等级**：已实测、条件性
- **日期**：2026-07-20
- **证据**：[plugin-help.txt](evidence/2.1.214/plugin-help.txt)
- **边界**：未执行 tag、eval 或发布操作。

## Headless 与自动化

### CC-070

- **声明**：本机 `-p`/`--print` 发送 prompt、打印结果并退出，不启动交互式 UI。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：真正调用会产生模型或 API 用量，本手册只核验 help。

### CC-071

- **声明**：本机 `--output-format` 在 print mode 下接受 `text`、`json` 和 `stream-json`，默认 text。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)

### CC-072

- **声明**：`--input-format stream-json`、`--include-partial-messages` 和实时 stream output 都要求 print mode，partial messages 还要求 stream-json output。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **来源**：[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)

### CC-073

- **声明**：本机 `--json-schema <schema>` 使用 JSON Schema 验证 structured output。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：Schema 只约束输出形状，不保证内容事实正确。

### CC-074

- **声明**：`--max-budget-usd` 和 `--fallback-model` 只适用于 print mode，分别限制 API call budget 和指定主模型不可用时的 fallback 列表。
- **等级**：已实测、条件性
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)

### CC-076

- **声明**：Print/non-TTY mode 跳过 workspace trust dialog；校验失败的 settings 会被静默忽略，不显示交互式错误 dialog。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：自动化应先在可信目录运行 doctor，不能把“无提示”当成已获信任。

## Background agents 与 workflows

### CC-077

- **声明**：本机 `--background`/`--bg` 启动 background agent 并立即返回，之后通过 `claude agents` 管理。
- **等级**：已实测、条件性
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：真正 dispatch 会产生模型用量，本手册未执行。

### CC-079

- **声明**：Agent view 处于 research preview，要求 Claude Code 2.1.139+；agent teams 为 experimental 且默认关闭，需设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`；dynamic workflows 要求 2.1.154+ 和受支持的付费/API/provider 环境，Pro 还需在 `/config` 启用。
- **等级**：官方核对、条件性
- **日期**：2026-07-20
- **来源**：[Run agents in parallel](https://code.claude.com/docs/en/agents)、[Agent view](https://code.claude.com/docs/en/agent-view)、[Agent teams](https://code.claude.com/docs/en/agent-teams)、[Workflows](https://code.claude.com/docs/en/workflows)
- **边界**：本机 root help 没有独立 `workflow` 或 `--teammate-mode` 入口；不要从文档页面存在推导当前账户一定可用。

### CC-080

- **声明**：`claude agents` 可为 dispatched sessions 指定 add-dir、agent、model、effort、permission mode、settings、setting sources、MCP config 和 plugin directories；`--cwd` 只过滤显示指定路径下启动的 background sessions。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[agents-help.txt](evidence/2.1.214/agents-help.txt)

## 安全、调试与维护

### CC-082

- **声明**：本机 `--safe-mode` 禁用 CLAUDE.md、skills、plugins、hooks、MCP、custom commands/agents、output styles、workflows、themes、keybindings 等 customizations；managed settings、auth、model、built-in tools 和 permissions 仍正常应用。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)

### CC-083

- **声明**：本机 `--bare` 跳过 hooks、LSP、plugin sync、attribution、auto-memory、background prefetch、keychain reads 和 CLAUDE.md auto-discovery，并要求显式提供 context/customization。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：Bare auth 与普通 safe mode 不同，不把两者视为强弱别名。

### CC-084

- **声明**：`--debug [filter]` 启用带可选类别 filter 的 debug，`--debug-file <path>` 写入指定日志并隐式启用 debug。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：Debug log 可能含 prompt、路径和敏感上下文，不保存为公开 evidence。

### CC-085

- **声明**：本机 `claude auto-mode` 提供 config、defaults、critique 和 reset；config/defaults 输出 JSON，critique 使用 AI，reset 删除 user settings 中的 autoMode section。
- **等级**：已实测、条件性
- **日期**：2026-07-20
- **证据**：[auto-mode-help.txt](evidence/2.1.214/auto-mode-help.txt)
- **边界**：未执行 effective config、critique 或 reset。

### CC-086

- **声明**：`claude project purge` 的 `--all` 影响全部 projects 并与 path 互斥；`--interactive` 逐项确认，`--yes` 跳过确认。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[project-purge-help.txt](evidence/2.1.214/project-purge-help.txt)
- **边界**：删除范围和 dry-run 统一见 [CC-061](#cc-061)；未执行任何 purge。

### CC-087

- **声明**：本机 `--tools <tools...>` 可把可用 built-in tools 限定为显式列表；传 `""` 禁用全部，传 `default` 使用默认集合。
- **等级**：已实测
- **日期**：2026-07-20
- **证据**：[claude-help.txt](evidence/2.1.214/claude-help.txt)
- **边界**：Tool 列表限制不验证模型输出事实，也不替代可信工作目录。

### CC-088

- **声明**：macOS Native Install 使用 `rm -f ~/.local/bin/claude` 和 `rm -rf ~/.local/share/claude` 卸载 binary/version files；Homebrew stable/latest 分别使用 `brew uninstall --cask claude-code` 与 `brew uninstall --cask claude-code@latest`。
- **等级**：官方核对
- **日期**：2026-07-20
- **来源**：[Advanced setup — Uninstall Claude Code](https://code.claude.com/docs/en/setup#uninstall-claude-code)
- **边界**：这些命令不删除 `~/.claude` user settings/session state；删除配置是独立且破坏性的步骤，本手册不建议作为安装回退。

---

## 官方来源索引

- [Claude Code 文档索引](https://code.claude.com/docs/llms.txt)
- [Overview](https://code.claude.com/docs/en/overview)
- [Advanced setup](https://code.claude.com/docs/en/setup)
- [Quickstart](https://code.claude.com/docs/en/quickstart)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Authentication](https://code.claude.com/docs/en/authentication)
- [Sessions](https://code.claude.com/docs/en/sessions)
- [Context window](https://code.claude.com/docs/en/context-window)
- [Prompt caching](https://code.claude.com/docs/en/prompt-caching)
- [Memory](https://code.claude.com/docs/en/memory)
- [Settings](https://code.claude.com/docs/en/settings)
- [Permissions](https://code.claude.com/docs/en/permissions)
- [Permission modes](https://code.claude.com/docs/en/permission-modes)
- [Sandboxing](https://code.claude.com/docs/en/sandboxing)
- [Skills](https://code.claude.com/docs/en/skills)
- [Commands](https://code.claude.com/docs/en/commands)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- [Hooks reference](https://code.claude.com/docs/en/hooks)
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [MCP](https://code.claude.com/docs/en/mcp)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Worktrees](https://code.claude.com/docs/en/worktrees)
- [Plugins](https://code.claude.com/docs/en/plugins)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Headless](https://code.claude.com/docs/en/headless)
- [Agents](https://code.claude.com/docs/en/agents)
- [Agent view](https://code.claude.com/docs/en/agent-view)
- [Agent teams](https://code.claude.com/docs/en/agent-teams)
- [Workflows](https://code.claude.com/docs/en/workflows)
- [Security](https://code.claude.com/docs/en/security)
- [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- [Error reference](https://code.claude.com/docs/en/errors)
- [Changelog](https://code.claude.com/docs/en/changelog)

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
