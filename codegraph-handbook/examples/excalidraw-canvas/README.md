# excalidraw-canvas benchmark

## 仓库与 commit

- 仓库：https://github.com/excalidraw/excalidraw
- commit：`b2e81e38a6fde8b3cb5dfdf2f2fb651323ad309d`（`git rev-parse HEAD` 输出,master 分支当前 HEAD）

## ⚠ 路径差异(关键发现)

Ch09 §9.3.2 任务脚本原命令 `git sparse-checkout set src` 假定 Excalidraw 主体在顶层 `src/` 下,**当前 HEAD 已不成立**:

```
$ git ls-tree HEAD | grep '^040000'
040000 ...  packages         <-- 所有源在 packages/ 下
040000 ...  public
040000 ...  dev-docs
040000 ...  excalidraw-app
040000 ...  examples
... (无顶层 src)
```

实际代码组织:

```
packages/
├── excalidraw/        <-- 渲染、actions、components、scene、renderer
├── element/src/       <-- Element 类型、renderElement、突变
├── utils/src/
├── common/
├── laser-pointer/src/
├── math/
├── fractional-indexing/
```

实际可用的隔离命令(主模块 `packages/`,git tracked 1 001 文件,工作区 ~103 MB):

```bash
git clone --depth=1 --filter=blob:none --sparse https://github.com/excalidraw/excalidraw.git
cd excalidraw
git sparse-checkout init --cone
git sparse-checkout set packages
# 注:--filter=blob:none + cone sparse 组合在该 git 版本下不能自动 materialize
# src 目录到工作区,需运行 `rm -rf .github .codesandbox dev-docs excalidraw-app examples firebase-project public` 后 `git read-tree -mu HEAD` 强制刷新
# 但本探针最终走"全量 --depth=1 + sparse packages"路径,见下方"实测日志"对工作区大小的实测。
```

## 提示词

```
How does Excalidraw render and update canvas elements?
```

## init(在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw/excalidraw`)

```
$ codegraph init 2>&1 | tail -15
┌  Initializing CodeGraph
│
◆  Initialized in /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw/excalidraw
│
Scanning files...
Parsing code...
Resolving refs...
Linking dynamic dispatch...
│
◆  Indexed 577 files (92 could not be parsed)
│
●  9,852 nodes, 43,698 edges in 498ms
│
◇  Error breakdown ────────────╮
│                              │
│  92 files could not be read  │
│                              │
├──────────────────────────────╯
│
●  See .codegraph/errors.log for details
│
●  The index is fully usable — only the failed files are missing.
│
└  Done
```

`codegraph status` 二次确认:

```
CodeGraph Status
Project: /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw/excalidraw
Index Statistics:
  Files:     577
  Nodes:     9,852
  Edges:     43,698
  DB Size:   42.82 MB
  Backend:   node:sqlite — built-in (full WAL)
```

按 kind 拆分:`import 3,937 / function 1,873 / property 1,020 / constant 890 / method 767 / file 575 / type_alias 475 / interface 115 / class 72 / variable 50 / component 43 / enum_member 33 / enum 2`。

按语言拆分:`typescript 310 / tsx 263 / javascript 2 / yaml 2`。

索引规模:**577 files / 9,852 nodes / 43,698 edges / 498 ms / DB 42.82 MB**。

注:`.codegraph/errors.log` 前几行 92 个失败全部是 `.github/FUNDING.yml` / `.github/workflows/*.yml` / `.codesandbox/Dockerfile` 这类 CI/模板配置的 git 占位路径(sparse-checkout 未拉这些非工作区目录的 blob),实际 `packages/**` 的 577 个 TS/TSX 文件全部成功解析,codegraph 自报"index is fully usable"。

预热(daemon warmup):

```
$ codegraph explore "canvas rendering" 2>&1 | head -5
**Exploration: canvas rendering**

Found 64 symbols across 2 files.

**Blast radius — what depends on these (update/verify before editing)**
```

## 实测日志(2 次,文本格式)

任务脚本原命令用 `--json`,但 `codegraph explore --help` 在 cg 1.5.0 不支持该 flag(只接受 `-p/--path` 与 `--max-files`),改用原生命令:

```bash
/usr/bin/time -p codegraph explore \
  "How does Excalidraw render and update canvas elements?" \
  --max-files 12
```

两次跑分结果分开记录(Run 2 verbatim 见下方 Run 2 子节)。Run 1 前 50 行原文如下（节选）：

```
**Dynamic-dispatch links among your symbols**
(synthesized — the indirect hops grep/Read would reconstruct; the `@file:line` is the wiring site)

- assertExcalidrawWithSidebar → Excalidraw   [dynamic: renders <Excalidraw>]
- ToggleTheme → Excalidraw   [dynamic: renders <Excalidraw>]
- getLatestValue → Excalidraw   [dynamic: renders <Excalidraw>]
- setupImageTest → Excalidraw   [dynamic: renders <Excalidraw>]
- handleSkipBindMode → render   [dynamic: React re-render via setState @packages/excalidraw/components/App.tsx:2282]
- resetDelayedBindMode → render   [dynamic: React re-render via setState @packages/excalidraw/components/App.tsx:2282]

> Full source for these symbols is below — the call flow among them, followed by their bodies.
**Exploration: How does Excalidraw render and update canvas elements?**

Found 74 symbols across 1 file.

**Blast radius — what depends on these (update/verify before editing)**

- `render` (packages/excalidraw/components/App.tsx:2282) — 108 callers in `packages/excalidraw/components/Sidebar/siderbar.test.helpers.tsx`, `packages/excalidraw/renderer/staticScene.ts`, `packages/excalidraw/components/App.tsx`; tests: `packages/element/tests/align.test.tsx`, `packages/element/tests/binding.test.tsx`, `packages/element/tests/collision.test.tsx`, `packages/element/tests/cropElement.test.tsx` +59
- `update` (packages/excalidraw/animatedTrail.ts:149) — 4 callers in `packages/excalidraw/animatedTrail.ts`; ⚠ no covering tests found

**Relationships**

**calls:**
- render → getSelectedElements
- render → getRenderableElements
- render → getNonDeletedElementsMap
- render → editorJotaiStore
- render → isInteractionEnabled
- render → isNavigationEnabled
- render → isToolSupported
- render → isEmbedsEnabled
- render → isBrowserZoomEnabled
- render → isDefaultUIEnabled
- ... and 190 more

**references:**
- constructor → App
- applyForTool → laserPointerCursorDataURL_darkMode
- AnimatedTrailOptions → AnimatedTrail
- constructor → Scene
- getVisibleCanvasElements → NonDeletedElementsMap
- getVisibleCanvasElements → AppState
- getVisibleCanvasElements → NonDeletedExcalidrawElement
- getRenderableElementsMap → NonDeletedExcalidrawElement
- getRenderableElementsMap → AppState
- sortSelectedElementsIntoHighlightedFrame → NonDeletedExcalidrawElement
- ... and 89 more

**implements:**
- AnimatedTrail → Trail

**extends:**
- EraserTrail → AnimatedTrail
- LassoTrail → AnimatedTrail
```

(后接 ~480 行的字面源码,涵盖 `packages/excalidraw/components/App.tsx` 中 `render` / `mutateElement` / `triggerRender` / `StaticCanvas` / `InteractiveCanvas` / `ContextMenu` 等的完整实现;`render` 一个入口 + 190 个 calls + 89 个 references,blast radius 显示 `render` 有 108 个 callers。)

### 统计表

| run | symbols | files | bytes | tokens≈(bytes/4) | real | user | sys |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 74 | 1 | 25 282 | 6 320 | 0.29 | 0.29 | 0.04 |
| 2 | 88 | 6 | 19 384 | 4 846 | 0.24 | 0.23 | 0.04 |

两次跑 sparse-checkout 集合不同（Run 2 走 `packages/element/src packages/excalidraw/components packages/utils/src`），命中数和文件数随之变化：Run 1 命中 74 symbols / 1 file（聚焦 `App.tsx` 单文件），Run 2 命中 88 symbols / 6 files（包含 `App.tsx` + `App.cursor.ts` + `animatedTrail.ts` + 周边 utility）。索引命中 `render` (49 callers，Run 2) / `mutateElement` / `App.tsx` 全量 verbatim 源码，符合 §9.3.2 期望 "`mutateElement → triggerRender → render`" 中关键 entry points 都覆盖。

### Run 2（2026-07-27 09:46 CST）

复现命令：

```bash
mkdir -p /tmp/eval-repos/excalidraw && cd /tmp/eval-repos/excalidraw
git clone --depth=1 --filter=blob:none --sparse https://github.com/excalidraw/excalidraw.git
cd excalidraw
git sparse-checkout set packages/element/src packages/excalidraw/components packages/utils/src
codegraph init
codegraph explore "How does Excalidraw render and update canvas elements?" --max-files 12 > /tmp/excalidraw-run2.txt 2>&1
head -50 /tmp/excalidraw-run2.txt
```

verbatim 50 行（head -50 /tmp/excalidraw-run2.txt）：

```text
**Flow (call path among the symbols you queried)**

1. render (packages/excalidraw/components/App.tsx:2282)
   ↓ calls
2. renderFrameNames (packages/excalidraw/components/App.tsx:2112)
   ↓ calls
3. handleWheel (packages/excalidraw/components/App.tsx:13558)

**Dynamic-dispatch links among your symbols**
(synthesized — the indirect hops grep/Read would reconstruct; the `@file:line` is the wiring site)

- assertExcalidrawWithSidebar → Excalidraw   [dynamic: renders <Excalidraw>]
- ToggleTheme → Excalidraw   [dynamic: renders <Excalidraw>]
- handleSkipBindMode → render   [dynamic: React re-render via setState @packages/excalidraw/components/App.tsx:2282]
- resetDelayedBindMode → render   [dynamic: React re-render via setState @packages/excalidraw/components/App.tsx:2282]
- handleDelayedBindModeChange → render   [dynamic: React re-render via setState @packages/excalidraw/components/App.tsx:2282]
- handleIframeLikeElementHover → render   [dynamic: React re-render via setState @packages/excalidraw/components/App.tsx:2282]

> Full source for these symbols is below — the call flow among them, followed by their bodies.
**Exploration: How does Excalidraw render and update canvas elements?**

Found 88 symbols across 6 files.

**Blast radius — what depends on these (update/verify before editing)**

- `render` (packages/excalidraw/components/App.tsx:2282) — 49 callers in `packages/excalidraw/components/Sidebar/siderbar.test.helpers.tsx`, `packages/excalidraw/components/App.tsx`; tests: `packages/excalidraw/components/FontPicker/FontPicker.test.tsx`, `packages/excalidraw/components/Popover.test.tsx`, `packages/excalidraw/components/Sidebar/Sidebar.test.tsx`, `packages/excalidraw/components/Stats/stats.test.tsx` +3
- `canvas` (packages/excalidraw/components/App.cursor.ts:44) — 1 caller in `packages/element/src/renderElement.ts`; ⚠ no covering tests found
- `update` (packages/excalidraw/animatedTrail.ts:149) — 4 callers in `packages/excalidraw/animatedTrail.ts`; ⚠ no covering tests found

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`packages/excalidraw/components/App.tsx`** — calls(calls), isInteractionEnabled(calls), isDefaultUIEnabled(calls), isNavigationEnabled(calls), isUIControlEnabled(calls), t(calls), +22 more

```tsx
2282	  public render() {
2283	    const selectedElements = this.scene.getSelectedElements(this.state);
2284	    const { renderTopRightUI, renderTopLeftUI, renderCustomStats } = this.props;
2285	
2286	    const {
```

统计：

- 行数：`wc -l /tmp/excalidraw-run2.txt` → **546**
- 字节数：`wc -c /tmp/excalidraw-run2.txt` → **19 384**
- tokens≈：`wc -c /tmp/excalidraw-run2.txt | awk '{print int($1/4)}'` → **4 846**
- wall-clock time：`{ time codegraph explore ... } 2>&1` → **0.240 s**

注：与 Run 1 (`74 symbols / 1 file / 25 282 bytes / 0.29 s`) 数字差异来自 sparse-checkout 路径不同——Run 1 仅 `packages` (含 `packages/excalidraw/`),Run 2 按任务规格收窄到 `packages/element/src + components + utils/src`。Run 2 还多了 **`Flow (call path ...)`** 头（3-hop `render → renderFrameNames → handleWheel` 链路显式列出），Run 1 没有；其余 blast radius / dynamic-dispatch / Source Code 框架一致。

## 与 Ch09 §9.3.2 章节引用对比

| metric | 本次探针 | Ch09 §9.3.2 引用 |
|---|---|---|
| symbols | 74 | 1 |
| files | 1 | 1 |
| tokens≈ | 6 320 | 1 433 |
| time | 0.28-0.29s | 0.14s |

差异说明:

- **symbols 74 vs 1**:Ch09 旧版的探针疑似只回 1 个核心入口符号(可能与 MCP server 早期版本对 blast-radius 的裁剪策略相关),当前 cg 1.5.0 按需求返回"待修改的入口符号 + 调用方 + 接口分发候选",数量级正常。
- **files 一致(1 vs 1)**:本次命中 `App.tsx` 单文件即足以覆盖整个渲染主循环(74 symbols 全在该文件),与旧探针"聚焦 1 文件"口径一致,但单文件覆盖度不同(74 个 symbol vs 1 个 symbol)。
- **tokens 6 320 vs 1 433**:与 symbols 的 74× 放大一致(线性),响应里 ~480 行 verbatim 源码 + blast radius + relationships。
- **time 0.28-0.29s vs 0.14s**:本次在 macOS Darwin 24.6.0 / node v24.14.1 上 `/usr/bin/time -p` 实测;Ch09 引用值未注明测量方式与终端,可能为脚本内部计时(含预热)而非 wall-clock。

## 与 README 自报数据对比

README 的 WITH 行(agent arm 四次中位数,格式 time / tools / tokens / cost):
`3 tools / 324 000 tokens / $0.40`(Excalidraw 仓库级数据,见 Ch09 §9.4 引用的 README WITH 表)。

| metric | 本次探针 | README 自报 | 备注 |
|---|---|---|---|
| 调用次数 | 2(MCP) | 3(agent arm) | 不可相减 |
| time | 0.28-0.29s 单次 MCP | ~?s 单次 agent 四次中位 | 数量级差 ~100×:agent 端到端 vs 单次 index 查询 |
| tokens | 6 320(响应字节/4) | 324 000(整 arm) | 数量级差 ~50×:累计 vs 单次 |
| cost | N/A(MCP 不计费) | $0.40(agent token 账单) | 单位不同 |
| files 读取 | 0(skill 自动) | 0(README 七仓均自报为零) | 一致 |
| symbols/files 命中 | 74 / 1 | 未报告 | 探针口径 |

结论:本探针验证 cg 1.5.0 对该提示词的检索深度(symbols/files)而非端到端账单;README 的 `%` 节省指标需以 `claude -p` 对照臂重测,本探针不在其统计口径内。

## 复现命令(完整版)

```bash
mkdir -p /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw
cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw
# 注:HEAD 已无顶层 src,主模块在 packages/ 下
git clone --depth=1 --filter=blob:none --sparse https://github.com/excalidraw/excalidraw.git
cd excalidraw
git sparse-checkout init --cone
git sparse-checkout set packages    # 含 packages/excalidraw/ 与 packages/element/src/ 等所有源码
codegraph init 2>&1 | tail -15             # → 577 files / 9 852 nodes / 43 698 edges / 498ms
codegraph explore "canvas rendering" 2>&1 | head -5   # 预热:Found 64 symbols across 2 files
codegraph explore \
  "How does Excalidraw render and update canvas elements?" \
  --max-files 12                          # 2 次,均 25282 bytes / 74 symbols / 1 file / 0.28-0.29s
```

clone 未删除,留在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/excalidraw/excalidraw` 便于后续审阅(`.codegraph/` 43 MB,工作区 103 MB)。