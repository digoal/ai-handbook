# 第 7 章 · CLI 命令完全手册

> **面向读者**:用户 / 开发者 · **预计阅读**:30 分钟
> **前置依赖**:{{chapter:6}}
> **本章目标**:精通所有 CLI 命令,知道何时走 CLI 何时走 MCP

## 7.1 引言

CodeGraph CLI 既管理安装与索引，也把图查询带进终端、脚本和 CI。本章以 1.5.0 源码及实跑帮助为准。标题所称“20 个”指 `--help` 默认列出的 20 个业务子命令；另说明 Commander 自动提供的 `help`，以及隐藏的 `serve`、`prompt-hook`。

## 7.2 概念铺垫

命令采用 Commander 风格：`codegraph <command> [options] [arg]`；`<x>` 必填，`[x]` 可选，`[files...]` 可变长。全局选项是 `-V/--version`、`--color`、`--no-color`、`-h/--help`；颜色选项可放任意位置。多数项目命令会从当前目录向上寻找最近的 `.codegraph/codegraph.db`，也可用 `--path` 指定。

交互探索优先 MCP：代理一次调用即可获得源码、调用路径和影响面。CLI 适合人类终端、无 MCP 的子代理、Shell/CI 与批处理。

| MCP tool | 等价 CLI | 默认可见 |
|---|---|---|
| `codegraph_explore` | `codegraph explore` | 是 |
| `codegraph_node` | `codegraph node` | 否 |
| `codegraph_search` | `codegraph query` | 否 |
| `codegraph_callers` | `codegraph callers` | 否 |
| `codegraph_callees` | `codegraph callees` | 否 |
| `codegraph_impact` | `codegraph impact` | 否 |
| `codegraph_files` | `codegraph files` | 否 |
| `codegraph_status` | `codegraph status` | 否 |

除 explore 外，MCP 工具默认不列出，但可用 `CODEGRAPH_MCP_TOOLS` 重启用。

## 7.3 正文

### 7.3.1 install / uninstall（关联 Ch3）

**install** 配置代理，不索引项目。`--target auto|all|none|csv`、`--location global|local`、`--yes` 支持自动化；`--no-permissions` 不写 Claude 权限；`--print-config <id>` 只打印；`--refresh` 仅刷新已配置代理。

```text
Usage: codegraph install [options]
```

**uninstall** 移除代理配置，默认还会移除 CLI；`--target`、`--location`、`--yes` 控制范围，`--keep-cli` 保留 CLI；不删除项目索引（用 `uninit`）。

```text
Usage: codegraph uninstall [options]
```

### 7.3.2 init / uninit / index / sync（关联 Ch8）

**init** 创建 `.codegraph/` 并立即全量建图；`--index` 仅为兼容旧脚本，现已无额外作用；`--force` 允许危险根目录，`--verbose` 输出工作线程细节。

```text
Usage: codegraph init [options] [path]
```

**uninit** 永久删除项目 `.codegraph/`，并清理安装过的 Git 同步钩子；`--force` 跳过确认。

```text
Usage: codegraph uninit [options] [path]
```

**index** 丢弃并重建完整数据库，结果等同新 init；`--quiet` 静默，`--verbose` 展开进度，`--force` 覆盖根目录保护。

```text
Usage: codegraph index [options] [path]
```

**sync** 仅增量吸收新增、修改、删除；`--quiet` 适合 Git hook。MCP watcher 正常时通常不必手跑。

```text
Usage: codegraph sync [options] [path]
```

### 7.3.3 status / query / explore / node（关联 Ch6）

**status** 显示文件、节点、边、数据库、WAL、语言、待同步与索引健康度；`--json` 给稳定机器输出。

```text
Usage: codegraph status [options] [path]
```

**query** 搜符号；`--path`、`--limit`（默认 10）、`--kind`、`--json`。它对应 MCP search，而非自然语言架构探索。

```text
Usage: codegraph query [options] <search>
```

**explore** 接受多词查询，返回相关符号的当前源码、调用路径与影响面；`--max-files` 限制源码文件数。其 handler 与 MCP explore 相同。

```text
Usage: codegraph explore [options] <query...>
```

**node** 查一个符号，或读一个文件；`--file` 可进入文件模式/消歧，`--offset`、`--limit` 分页，`--symbols-only` 只看符号图和依赖者。路径型位置参数也按文件处理。

```text
Usage: codegraph node [options] [name]
```

### 7.3.4 files / callers / callees / impact / affected

**files** 从索引列目录；`--filter` 前缀、`--pattern` glob、`--format tree|flat|grouped`、`--max-depth`、`--no-metadata`、`--json`。

```text
Usage: codegraph files [options]
```

**callers** 查谁调用符号；`--limit` 默认 20，支持 `--path/--json`。

```text
Usage: codegraph callers [options] <symbol>
```

**callees** 查符号调用谁；选项与 callers 相同。

```text
Usage: codegraph callees [options] <symbol>
```

**impact** 从符号向依赖者遍历；`--depth` 默认 2、有效范围 1–10，支持 `--path/--json`。

```text
Usage: codegraph impact [options] <symbol>
```

**affected** 从变更文件反向遍历依赖，筛出测试；可传文件或 `--stdin`，`--depth` 默认 5，`--filter` 自定义测试 glob，`--quiet` 仅路径，亦可 `--json`。

```text
Usage: codegraph affected [options] [files...]
```

### 7.3.5 daemon / serve / unlock

**daemon**（别名 `daemons`）列出后台 MCP daemon；TTY 中选择并停止，管道/CI 中只打印。

```text
Usage: codegraph daemon|daemons [options]
```

**serve** 是隐藏的代理入口；`--mcp` 使用 stdio，`--path` 固定项目，`--no-watch` 关闭 watcher。人类通常不直接运行。

```text
Usage: codegraph serve [options]
```

**unlock** 删除阻塞索引的 stale `codegraph.lock`；只在确认无索引进程后使用。

```text
Usage: codegraph unlock [options] [path]
```

### 7.3.6 telemetry / upgrade / version / help

**telemetry** 接受 `status|on|off`；环境变量 `DO_NOT_TRACK`、`CODEGRAPH_TELEMETRY` 可覆盖保存值。

```text
Usage: codegraph telemetry [options] [action]
```

**upgrade** 默认升最新版，也可指定版本；`--check` 只检查，`--force` 强制重装。

```text
Usage: codegraph upgrade [options] [version]
```

**version** 输出安装版本；同义入口有 `-v`、`-V`、`-version`、`--version`。

```text
Usage: codegraph version [options]
```

**help** 是 Commander 自动命令，可显示总帮助或指定命令帮助。

```text
help [command]                 display help for command
```

### 7.3.7 隐藏命令：prompt-hook（关联 Ch5）

读取 stdin 的 `{prompt,cwd}` JSON；结构性问题命中时注入 explore 上下文。它是可降级钩子：禁用、无索引或失败都静默成功；`CODEGRAPH_NO_PROMPT_HOOK=1` 或 `CODEGRAPH_PROMPT_HOOK=0` 可关闭。

```text
Usage: codegraph prompt-hook [options]
```

## 7.4 真实场景实战

### 场景 7.1：用 CLI 做 MCP 等价的批量分析

```bash
while read -r q; do codegraph explore --path "$PWD" "$q"; done < questions.txt
```

本章验证查询返回 19 个相关符号、调用路径和当前源码；仓库根无索引时会明确报错，本机真实索引位于 `src/.codegraph/`，故使用 `--path .../codegraph/src` 完成验证。

### 场景 7.2：在脚本里用 --json 解析输出

```bash
codegraph status --json | jq '{files:.fileCount,nodes:.nodeCount}'
codegraph query WatchOptions --json | jq '.[].node.filePath'
```

不要混入进度文本；支持 `--json` 的命令是 status、query、files、callers、callees、impact、affected。

### 场景 7.3：用 affected 找出某次 PR 应该跑哪些测试

```bash
git diff --name-only origin/main...HEAD |
  codegraph affected --stdin --quiet |
  xargs -r npx vitest run
```

在 macOS/BSD `xargs` 无 `-r` 时，先判断输出非空；必要时用 `--filter 'e2e/*.spec.ts'`。

## 7.5 本章小结

生命周期用 install/init/index/sync；交互理解首选 MCP explore；终端与 CI 用 CLI，结构化消费选 `--json`/`--quiet`。先 `status` 判断图是否健康，再查询。

## 7.6 常见踩坑

- 无参数会启动交互安装器，不等于 help；用 `codegraph --help`。
- `init` 已自动索引；重复传 `--index` 不会改变行为。
- `index` 是完整重建，日常更新应靠 watcher 或 `sync`。
- `uninstall` 不删项目图；`uninit` 才删 `.codegraph/`。
- `serve --mcp` 等待 JSON-RPC，不是普通交互服务。
- `unlock` 不检查锁所属进程，误删活锁可能导致并发写。
- `--quiet` 并非所有命令都有；机器读取优先 `--json`。
- 项目根没数据库时，显式 `--path` 指向实际已初始化根。

## 7.7 下一章预告

{{chapter:8}} 将深入初始化、全量索引、增量同步与 watcher 的完整生命周期。

## 7.8 参考

- `src/bin/codegraph.ts`（1.5.0）
- `README.md` 的 CLI Reference、MCP Tools
- 本机 `codegraph --help` 与全部子命令 `--help`（2026-07-26）
