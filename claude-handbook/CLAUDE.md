# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是一份**中文 Markdown 课程手册**，不是可编译/可测试的代码工程。没有 `package.json`、`Cargo.toml`、`pytest` 或 CI 配置。仓库结构是：

- `README.md` — 总入口与基线（Claude Code 2.1.214 / macOS 15.7.7）
- `GLOSSARY.md` — 统一术语表
- `SOURCES.md` — **唯一事实台账**，所有版本敏感声明通过 `CC-xxx` ID 引用
- `VERIFICATION.md` — 核验、写作与发布规范
- `00-…/README.md` … `14-…/README.md` — 15 个章节（每章结构：学习目标 → 前置条件 → 正文 → 本章事实与证据 → 下一章 → 基线页脚）
- `evidence/<version>/` — 本机只读 CLI help 输出存档（如 `claude-version.txt`、`claude-help.txt`）

## 编辑前必读

改任何章节前先读这两份，因为它们定义了正文准入门槛：

- `VERIFICATION.md` — 证据等级、采集流程、脱敏要求、发布清单
- `SOURCES.md` — 已登记的事实 ID；新增声明必须在这里加 ID，再写进正文

不要为了"看起来完整"在正文里编写未在台账登记的事实。

## 核心约定（违反即视为回归）

### 事实与版本边界
- 任何版本敏感句子（命令、flag、默认值、路径、限制、生命周期声明）必须链接到 `SOURCES.md` 中的 `CC-xxx`。
- 一个 ID 只表达一条独立事实；不要把多条塞进同一 ID。
- 易变长表只保留一份权威正文，其他章节用相对链接引用。
- 章节末尾的"本章事实与证据"块必须列出本章节引用的全部 ID。
- 章节底部三行页脚（`Last Updated` / `Claude Code Baseline` / `Platform`）不能删。

### 证据等级
正文只能使用四级之一，且必须紧邻条件：
- **已实测** — 仅当 `evidence/<version>/` 里有对应无敏感输出。
- **官方核对** — 仅当有具体官方页面 URL（`https://code.claude.com/docs/...`）。
- **条件性** — 必须显式写出订阅 / 认证 / feature gate / 组织策略条件。
- **待验证** — 不允许进入正文，只能留在章节骨架的"待核验问题"。

### 写作与结构
- 每章只有一个 H1，标题不跳级。
- 所有代码 fence 必须声明语言；纯输出用 `text`。
- 内部链接用相对路径（`../SOURCES.md#cc-007`），不要用绝对路径。
- Mermaid 仅在能解释流程时使用，并配文字说明。
- 简体中文表达遵守 `GLOSSARY.md` 的统一术语，不要自己造新词。
- 章节内示例命令若涉及破坏性操作（安装、升级、`logout`、`rm`、`claude install`），正文必须明确"未实际执行"并链接到对应 `CC-xxx`。

### 严禁提交
- `~/.claude/settings.json` 或其他真实用户配置。
- API key、OAuth token、cookie、Keychain 内容、debug 日志、session transcript。
- 用户名、主目录绝对路径、私有仓库名、组织信息。
- `claude doctor` 等含私人路径的完整输出；只保留脱敏片段。

练习命令必须在 `~/claude-code-handbook-lab` 这类隔离目录中运行；不要拿生产仓库或 home 目录当实验对象。

## 改一手后的发布前自检

参照 `VERIFICATION.md` 的发布清单逐项核对，重点检查：

- 命令拼写、大小写与 `evidence/<version>/*.txt` 一致。
- 同一事实没有在多个章节漂移。
- 条件紧邻结论，没有把"已实测"泛化成"所有用户"。
- `pre-commit run --all-files` 通过；最终 diff 未修改与本次任务无关的旧章节正文。
- 新增的 `CC-xxx` 已登记在 `SOURCES.md` 且只表达一条声明。

## 不要做的事

- 不要把 Agent SDK、Anthropic API、Desktop、Web、IDE 集成、Windows / Linux / WSL 当作主线写入。
- 不要复述通用开发建议（"写单测""提供友好报错"等）—— 这类内容不归本手册管。
- 不要替章节补"常见开发任务""小贴士""支持与文档"之类的板块，除非原章节骨架已有等价小节。
- 不要靠记忆补齐 flag、参数、默认值；拿不准就回 `evidence/2.1.214/` 对应 help 文本核对。

## 范围之外

旧 01–10 课程、第三方文章、搜索摘要和 AI 回答只能提供**待核验线索**，不能单独支撑正文事实。`claude` 本身的安装、升级、登录、发布、有 API 费用的命令**不得**为了核验文档而自动执行。
