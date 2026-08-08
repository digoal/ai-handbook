# tokio-runtime benchmark

- 仓库：https://github.com/tokio-rs/tokio
- commit：`6a058770e9bd0944acf40fca6b3d5e59c3ca413a`
- clone：`git clone --depth=1 --filter=blob:none --sparse https://github.com/tokio-rs/tokio.git`，随后 `git sparse-checkout set tokio/src/runtime tokio/src/task`（Tokio 当前版本把 scheduler 编入 `tokio/src/runtime/scheduler/`，不单独存在顶层目录）
- 提示词：`How does tokio schedule and run async tasks on its runtime?`
- 探针命令：`codegraph explore "How does tokio schedule and run async tasks on its runtime?" --max-files 12`（`codegraph explore` 当前 CLI 不支持 `--json`，输出文本直接落盘统计字节）

## init 实测

```
$ cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/tokio/tokio
$ codegraph init 2>&1 | tail -15
┌  Initializing CodeGraph
│
◆  Initialized in /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/tokio/tokio
│
Scanning files...
Parsing code...
Resolving refs...
Linking dynamic dispatch...
│
◆  Indexed 140 files (661 could not be parsed)
│
●  2,601 nodes, 7,800 edges in 220ms
│
◇  Error breakdown ─────────────╮
│                               │
│  661 files could not be read  │
│                               │
├───────────────────────────────╯
│
●  See .codegraph/errors.log for details
│
●  The index is fully usable — only the failed files are missing.
│
└  Done
```

索引统计：**140 files / 2,601 nodes / 7,800 edges / 220 ms**。661 文件无法读取来自 sparse-checkout 未下到 blob 的依赖项（tokio 子模块 `tokio/src/sync`、`tokio/src/io` 等）；核心调度路径 `runtime/scheduler/{current_thread,multi_thread,inject}` 与 `runtime/task` 均成功索引。

## 预热

```
$ codegraph explore "async runtime" 2>&1 | head -5
**Exploration: async runtime**

Found 42 symbols across 4 files.

**Blast radius — what depends on these (update/verify before editing)**
```

daemon 启动并预热就绪。42 symbols / 4 files。

## 实测日志（2 次）

`tokens~` = `响应字节 / 4`（探针约定估算，不是 API token，也不是 cost）。

| run | symbols | files | bytes | tokens~ | time | cost |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 78 | 5 | 15899 | 3974 | 0.206s | N/A |
| 2 | 78 | 5 | 15899 | 3974 | 0.201s | N/A |

### Run 1 响应（前 50 行 / 全文 488 行）

```
**Dynamic-dispatch links among your symbols**
(synthesized — the indirect hops grep/Read would reconstruct; the `@file:line` is the wiring site)

- schedule → schedule   [dynamic: interface → impl @tokio/src/runtime/tests/task.rs:460]

> Full source for these symbols is below — the call flow among them, followed by their bodies.
**Exploration: How does tokio schedule and run async tasks on its runtime?**

Found 78 symbols across 5 files.

**Blast radius — what depends on these (update/verify before editing)**

- `Task` (tokio/src/runtime/task/mod.rs:233) — 8 callers in `tokio/src/runtime/blocking/schedule.rs`, `tokio/src/runtime/scheduler/current_thread/mod.rs`, `tokio/src/runtime/scheduler/multi_thread/handle.rs`, `tokio/src/runtime/task/harness.rs` +2 more; tests: `tokio/src/runtime/tests/mod.rs`, `tokio/src/runtime/tests/task.rs`
- `Task` (tokio/src/runtime/blocking/pool.rs:124) — 21 callers in `tokio/src/runtime/blocking/pool.rs`, `tokio/src/runtime/task/mod.rs`, `tokio/src/runtime/blocking/schedule.rs`, `tokio/src/runtime/dump.rs` +5 more; tests: `tokio/src/runtime/tests/mod.rs`, `tokio/src/runtime/tests/task.rs`

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`tokio/src/runtime/task/mod.rs`** — references(references), Notified(references), calls(calls), header(calls), Task(references), +21 more

```rust
230
231	/// An owned handle to the task, tracked by ref count.
232	#[repr(transparent)]
233	pub(crate) struct Task<S: 'static> {
234	    raw: RawTask,
235	    _p: PhantomData<S>,
236	}
237
238	unsafe impl<S> Send for Task<S> {}
239	unsafe impl<S> Sync for Task<S> {}
240
241	/// A task was notified.
242	#[repr(transparent)]
243	pub(crate) struct Notified<S: 'static>(Task<S>);
244
245	impl<S> Notified<S> {
246	    #[cfg(all(tokio_unstable, feature = "rt-multi-thread"))]
247	    #[inline]
248	    pub(crate) fn task_meta<'meta>(&self) -> crate::runtime::TaskMeta<'meta> {
249	        self.0.task_meta()
250	    }
251
252	    pub(crate) fn set_scheduled_at(&self, scheduled_at: ScheduleLatencyInstant) {
253	        // SAFETY: There are no concurrent writes because there is only ever one `Notified`
254	        // reference per task. There are no concurrent reads because this field is only read
255	        // when polling the task, which can only happen after it's scheduled.
256	        unsafe {
257	            self.0.header().set_scheduled_at(scheduled_at);
```

### Run 2（2026-07-27 09:44:52 +0800）响应（前 50 行 / 全文 488 行；78 symbols / 5 files / 15899 bytes / tokens~ 3974）

```text
**Dynamic-dispatch links among your symbols**
(synthesized — the indirect hops grep/Read would reconstruct; the `@file:line` is the wiring site)

- schedule → schedule   [dynamic: interface → impl @tokio/src/runtime/tests/task.rs:460]

> Full source for these symbols is below — the call flow among them, followed by their bodies.
**Exploration: How does tokio schedule and run async tasks on its runtime?**

Found 78 symbols across 5 files.

**Blast radius — what depends on these (update/verify before editing)**

- `Task` (tokio/src/runtime/task/mod.rs:233) — 8 callers in `tokio/src/runtime/blocking/schedule.rs`, `tokio/src/runtime/scheduler/current_thread/mod.rs`, `tokio/src/runtime/scheduler/multi_thread/handle.rs`, `tokio/src/runtime/task/harness.rs` +2 more; tests: `tokio/src/runtime/tests/mod.rs`, `tokio/src/runtime/tests/task.rs`
- `Task` (tokio/src/runtime/blocking/pool.rs:124) — 21 callers in `tokio/src/runtime/blocking/pool.rs`, `tokio/src/runtime/task/mod.rs`, `tokio/src/runtime/blocking/schedule.rs`, `tokio/src/runtime/dump.rs` +5 more; tests: `tokio/src/runtime/tests/mod.rs`, `tokio/src/runtime/tests/task.rs`

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`tokio/src/runtime/task/mod.rs`** — references(references), Notified(references), calls(calls), header(calls), Task(references), +21 more

```rust
230
231	/// An owned handle to the task, tracked by ref count.
232	#[repr(transparent)]
233	pub(crate) struct Task<S: 'static> {
234	    raw: RawTask,
235	    _p: PhantomData<S>,
236	}
237
238	unsafe impl<S> Send for Task<S> {}
239	unsafe impl<S> Sync for Task<S> {}
240
241	/// A task was notified.
242	#[repr(transparent)]
243	pub(crate) struct Notified<S: 'static>(Task<S>);
244
245	impl<S> Notified<S> {
246	    #[cfg(all(tokio_unstable, feature = "rt-multi-thread"))]
247	    #[inline]
248	    pub(crate) fn task_meta<'meta>(&self) -> crate::runtime::TaskMeta<'meta> {
249	        self.0.task_meta()
250	    }
251
252	    pub(crate) fn set_scheduled_at(&self, scheduled_at: ScheduleLatencyInstant) {
253	        // SAFETY: There are no concurrent writes because there is only ever one `Notified`
254	        // reference per task. There are no concurrent reads because this field is only read
255	        // when polling the task, which can only happen after it's scheduled.
256	        unsafe {
257	            self.0.header().set_scheduled_at(scheduled_at);
```

## 期望路径

期望路径（Ch09 §9.3.4）：`worker → scheduler → task` 的调度与 poll 路径。

实测命中：**5 个文件** — `tokio/src/runtime/task/mod.rs`、`tokio/src/runtime/task/harness.rs`、`tokio/src/runtime/blocking/pool.rs`、`tokio/src/runtime/scheduler/current_thread/mod.rs`、`tokio/src/runtime/scheduler/multi_thread/handle.rs`，blast radius 覆盖 `Task<S>`、`Notified<S>`、blocking pool 中的同名 `Task`、current_thread 与 multi_thread 两条 scheduler 入口，以及 `schedule` 的动态分派（`tokio/src/runtime/tests/task.rs:460`）。响应给出了 `Task<S>` 的 repr(transparent) 包装与 `Notified<S>` 的标记类型实现，能直接串出 `spawn → Notified → scheduler::schedule → harness::poll` 的完整证据链。

## 与 Ch09 §9.3.4 / README 自报数据 对比

| metric | 探针本次 | Ch09 §9.3.4 引用 | README 自报 WITH |
|---|---:|---:|---:|
| symbols / files | 78 / 5 | 0 / 0 | n/a (报告 tools) |
| bytes | 15899 | n/a | n/a |
| tokens~ (bytes/4) | 3974 | ~41 | 386 000 (k = 1000) |
| time | 0.20s (两次均值) | 0.14s | 46s (含整轮 agent) |
| tools 调用次数 | 2 (固定) | n/a | 3 |
| cost | N/A | N/A | $0.44 |

### 差异说明

1. **与 Ch09 §9.3.4 的 0/0 / 41 tokens 差异最大**：Ch09 章节写的是 "0/0，约 41 tokens，0.14s（未找到相关代码）"，本次真实探针命中 **78 symbols / 5 files / ~3974 tokens / 0.20s**。可能原因：
   - Ch09 的 0/0 来自未限定 sparse-checkout 的 init（whole-repo clone 加上当时索引器对 Rust `pub(crate)` 关联的处理与 1.5.0 不同），导致 `Task<S>` 这种内部符号被剪掉；
   - 41 tokens / 0.14s 的响应规模对应"未命中、返回空 blast radius 与空 source"，本次因加了 `tokio/src/runtime/scheduler` 显式 sparse-checkout，命中关键调度文件；
   - 章节引用的 0.14s 是 daemon 命中缓存后的稳定延迟，本次预热后两次分别为 0.206 / 0.201 s，仍在同一量级。
2. **与 README 自报的 386k tokens / 3 tools / $0.44 不可直接相减**：README 的 386k tokens / $0.44 是 **Claude `claude -p` agent arm**（4 次中位数，WITH），含整个 agent reasoning + 多次 tool 往返 + API 计费 token；本探针只测 `codegraph explore` 单次响应字节估算，不是账单 token。3 tools 是 agent arm 内部工具调用次数，本探针固定 2 次 MCP 调用。
3. **time 不可比**：46s 是整轮 `claude -p` wall clock（含 LLM 推理、网络、agent loop），0.20s 是索引查询本地耗时。
4. **索引规模 140 files / 2,601 nodes / 7,800 edges** 也只在 sparse-checkout 后的子集下成立；tokio 整仓索引会更大（但本次只关心 scheduler 与 task 子树，符合"按场景定数据集"的 Ch09 §9.4 方法论）。

## Ch09 章节引用更正建议

- §9.3.4 当前行 "2 次均为 0/0，约 41 tokens，0.14s（未找到相关代码）" 应替换为 "2 次均为 **78/5，约 3974 tokens，0.20s**"（仍为探针约定，非 API token / cost）。
- §9.4 表 "Tokio 3 tools / 386k / $0.44" 保留即可，那是 README 的 agent arm 数据，与本探针并列陈述而非相减。

## 复现命令

```bash
mkdir -p /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/tokio
cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/tokio
git clone --depth=1 --filter=blob:none --sparse https://github.com/tokio-rs/tokio.git
cd tokio
git sparse-checkout set tokio/src/runtime tokio/src/task
codegraph init                           # → Indexed 140 files, 2,601 nodes, 7,800 edges in 220ms
codegraph explore "async runtime"        # warm up daemon
START=$(date +%s.%N)
codegraph explore "How does tokio schedule and run async tasks on its runtime?" --max-files 12 > run.txt
END=$(date +%s.%N)
awk -v s="$START" -v e="$END" 'BEGIN { printf "%.3f s\n", e-s }'
wc -c run.txt                            # → 15899 bytes
```