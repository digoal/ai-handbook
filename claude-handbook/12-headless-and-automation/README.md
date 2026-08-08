# Headless 与自动化

> **版本基线**:Claude Code 2.1.214 · macOS 15.7.7 · 核验 2026-07-20

Print mode 让 Claude Code 作为非交互 CLI 参与 pipe、script 和 CI。本章只核验本机 flags 与官方边界；示例命令会发起模型请求并产生订阅或 API 用量，因此不会由手册作者自动执行。

> **Warning**：非交互不等于更安全。`--print` 会跳过 workspace trust dialog，而且无效 settings 在该模式下可能被静默忽略。

---

## 学习目标

- 区分交互式 session 与 `--print`。
- 选择 text、JSON 或 stream-json output。
- 使用 JSON Schema 约束最终结果。
- 设置预算、fallback 和 session persistence 边界。
- 在自动化中显式处理 trust、permissions、stderr 和临时输出。

## 前置条件

先完成 [11 Plugins](../11-plugins/README.md)。不要在不信任的仓库中运行 headless command。

## 场景示范：在 CI 里跑结构化输出

你希望在 CI 流水线里加一步：让 Claude Code 检查当前 PR 的 diff 是否符合某个约束（比如"不得引入新的 print 语句"），并以 JSON 形式输出结果供后续步骤消费，而不是把整段对话文本塞进 CI 日志。

### 实操

- 按本章「## Print mode」使用 `--print` 启动非交互模式，避免触发 workspace trust 对话框。
- 按「## Output formats」选择 `json` 或 `stream-json`，按「## Structured output」配 `--json-schema` 约束最终输出的字段。
- 按「## Workspace trust 与 settings」预先决定信任策略（CI 场景通常已在 sandbox 内，但需要明确）。
- 把命令包进一个本地脚本或 Makefile，先在 disposable 仓库里手动跑通，再接入 CI。

### 验证

- 命令退出码为 0 时，stdout 是合法 JSON 且字段匹配 schema；非 0 时退出码能被 CI 步骤正确捕获。
- stderr 不会污染 stdout（不会把对话文本混入 JSON 输出）。
- 在 disposable 仓库里跑通后，把同样命令接到 CI 工作流，先用 dry-run 模式观察一次再启用。

## Print mode

本机 2.1.214 的 `-p`/`--print` 发送 prompt、打印结果并退出；交互式 UI 不会启动。见 [CC-070](../SOURCES.md#cc-070)。

最小示例：

```bash
claude -p "只列出当前目录中 README.md 的一级标题，不修改文件"
```

即使 prompt 写“只读”，仍应使用权限、sandbox 和受控工作目录形成真正边界。

## Output formats

本机 help 提供：

- `text`：默认纯文本结果。
- `json`：单个 JSON result。
- `stream-json`：实时 JSON event stream。

它们只适用于 print mode。见 [CC-071](../SOURCES.md#cc-071)。

### Text

```bash
claude -p --output-format text "用一句话说明这个仓库的用途"
```

适合人类读取，不适合依赖自然语言解析的自动化。

### JSON

```bash
claude -p --output-format json \
  "只分析 README.md，返回简短摘要"
```

脚本应使用 JSON parser，不要用 `grep` 猜字段。具体 response schema 以当前官方 [Headless](https://code.claude.com/docs/en/headless) 页面为准。

### Stream JSON

```bash
claude -p --verbose --output-format stream-json \
  "只读取 README.md，说明分析步骤"
```

Stream JSON 适合实时观察 text/tool events，但 consumer 必须能处理多种 event。`--include-partial-messages` 只在 print + stream-json 下生效。见 [CC-072](../SOURCES.md#cc-072)。

## Structured output

`--json-schema` 让最终输出按 JSON Schema 验证。本机 help 示例使用 JSON object：

```bash
claude -p --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "summary": {"type": "string"},
      "needs_changes": {"type": "boolean"}
    },
    "required": ["summary", "needs_changes"]
  }' \
  "只评估 README.md，不修改文件"
```

Schema 约束输出形状，不保证分析事实正确；仍要验证输入范围和结果。见 [CC-073](../SOURCES.md#cc-073)。

## Streaming input

`--input-format stream-json` 允许通过 stdin 输入 realtime JSON messages，并且只适用于 print mode。普通单 prompt 继续使用默认 `text`。见 [CC-072](../SOURCES.md#cc-072)。

不要把任意外部 JSON 直接 pipe 给有写权限的 Claude Code；先验证来源、大小和 schema。

## Budget 与 fallback

本机 help 中：

- `--max-budget-usd <amount>` 只适用于 print mode，用于限制 API call 预算。
- `--fallback-model <models>` 只适用于 print mode，在主模型不可用时按列表尝试。

见 [CC-074](../SOURCES.md#cc-074)。预算是保护栏，不是费用预测；脚本仍应记录任务数量、模型和失败重试。

## Session persistence

Print mode 默认可以产生 session state；`--no-session-persistence` 禁止保存该次运行，使其不能 resume。见 [CC-022](../SOURCES.md#cc-022)。

一次性 CI 分析通常应显式选择不持久化：

```bash
claude -p --no-session-persistence \
  "只读取 README.md，输出三个文档风险"
```

如果后续需要 resume，则不要使用该 flag，并建立清晰的 session ID 管理。

## Workspace trust 与 settings

本机 help 明确提示：print mode 或 stdout 非 TTY 时，workspace trust dialog 会被跳过；校验失败的 settings 会被静默忽略，没有交互式错误 dialog。见 [CC-076](../SOURCES.md#cc-076)。

因此自动化必须：

1. 只在预先信任、固定 revision 的目录运行。
2. 在进入 print mode 前用 `claude doctor` 验证 settings。
3. 显式传入最小 `--allowed-tools`/`--disallowed-tools` 或 `--tools`。
4. 不依赖交互确认修复错误配置。

## 一个安全 shell 模板

```bash
#!/bin/sh
set -eu

claude doctor >/dev/null

claude -p \
  --no-session-persistence \
  --tools "Read" \
  --output-format json \
  "只读取 README.md，返回文档结构摘要"
```

`--tools "Read"` 把该运行可用的 built-in tools 限定为 Read，避免 print mode 等待无人能够批准的 Plan-mode 交互。见 [CC-087](../SOURCES.md#cc-087)。

该模板仍会产生模型用量。使用前先在 disposable repository 中人工运行一次并检查输出。

## 结果检查与清理

- 确认 stdout 格式与声明一致。
- 确认没有修改工作区：`git status --short`。
- 临时输出文件用明确路径保存，检查后删除。
- 不把 prompt、response、费用或 stream event 当作公开 evidence。

## 常见问题

### JSON 输出仍包含不想要的文字

使用 `--json-schema` 约束最终结构，并用 JSON parser 校验。不要在 prompt 中只写“请输出 JSON”后依赖字符串处理。

### CI 中没有出现 trust prompt

这是 print mode 的已知边界，不是已经获得信任。把仓库来源验证放在调用 Claude Code 之前。

### Settings 写错但命令仍运行

非交互模式可能静默忽略校验失败的 settings。先运行 doctor，并让 CI 对 doctor failure 直接停止。

### Stream consumer 卡住

确认 input/output format 是否匹配，是否启用了 verbose，以及 consumer 是否逐条读取 newline-delimited events。

## 本章事实与证据

- [CC-070](../SOURCES.md#cc-070) — print mode
- [CC-071](../SOURCES.md#cc-071) — output formats
- [CC-072](../SOURCES.md#cc-072) — stream input/output 与 partial messages
- [CC-073](../SOURCES.md#cc-073) — JSON Schema
- [CC-074](../SOURCES.md#cc-074) — budget 与 fallback
- [CC-022](../SOURCES.md#cc-022) — session persistence
- [CC-076](../SOURCES.md#cc-076) — trust 与无效 settings 边界
- [CC-087](../SOURCES.md#cc-087) — 限定 built-in tools

## 下一章

继续学习 [13 Background agents 与 workflows](../13-background-agents-and-workflows/README.md)。

---

**Last Updated**: July 20, 2026
**Claude Code Baseline**: 2.1.214
**Platform**: macOS 15.7.7
