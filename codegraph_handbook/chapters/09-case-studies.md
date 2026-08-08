# 第 9 章 · 真实场景案例库（7 仓 7 问）

> **面向读者**：用户 · **预计阅读**：30 分钟  
> **前置依赖**：{{chapter:6}}  
> **本章目标**：复现 README 的 7 个真实 benchmark，并理解如何核验结果。

## 9.1 引言

合成示例只能证明工具“能跑”，真实仓库才会暴露索引规模、跨语言调用和框架边界的问题。本章把同一组自然语言问题放进 VS Code、Excalidraw、Django、Tokio、OkHttp、Gin 和 Alamofire，先用统一命令建立索引，再各调用两次 `codegraph_explore`。结果记录在 `examples/` 下；README 的原始对照是四次运行的中位数，本章的两次运行是复现性检查，不冒充同一统计量。

## 9.2 概念铺垫

**方法论。** 每个仓库使用 depth-1、blobless、sparse clone；`codegraph init` 完成后预热 daemon，再以 `MODEL=sonnet`、`EFFORT=high` 的评估设置执行至少两次（本文的 MCP 探针本身不调用模型，因此模型字段标为 N/A）。每次保持问题、`maxFiles=12` 和项目路径不变。冷启动时间不能混入查询时间。

**指标。** `calls` 是 MCP 请求数；`symbols/files` 是响应中实际返回的符号和文件；`tokens≈响应字节/4` 只是探针输出的可复核估算，不是模型账单；`cost` 只有完整 `claude -p` run 才有意义，探针记为 N/A；`time` 是 wall-clock。完整 agent 评估应以 session 的 `total_cost_usd` 和总 token 为准。

## 9.3 正文：7 个真实场景

以下 commit 是 shallow clone 当日 HEAD；每节的逐次日志和 JSON 响应见对应 example README。

### 9.3.1 VS Code：扩展宿主通信

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/vscode-extension-host/README.md`](../examples/vscode-extension-host/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：microsoft/vscode（见 `examples/vscode-extension-host/README.md`）。
- **提示词**：`How does the extension host communicate with the main process?`
- **期望**：找到 ExtensionHost IPC、消息通道以及主进程到 extension host 的调用路径。
- **实测**：2 次均为 **1 symbol/1 file，约 1638 tokens，0.15s**；cost=N/A。详见 `examples/vscode-extension-host/README.md`。最新真实数字见 §9.4.1 复现性声明段。

### 9.3.2 Excalidraw：渲染画布

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/excalidraw-canvas/README.md`](../examples/excalidraw-canvas/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：excalidraw/excalidraw。
- **提示词**：`How does Excalidraw render and update canvas elements?`
- **期望**：`mutateElement → triggerRender → render`，并能跨过三个 React 边界。
- **实测**：2 次均为 **1/1，约 1433 tokens，0.14s**；cost=N/A，详见 `examples/excalidraw-canvas/README.md`。最新真实数字见 §9.4.1 复现性声明段。

### 9.3.3 Django：ORM QuerySet

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/django-orm/README.md`](../examples/django-orm/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：django/django。
- **提示词**：`How does Django's ORM build and execute a query from a QuerySet?`
- **期望**：从 QuerySet 分析进入 SQLCompiler，最终到 execute。
- **实测**：2 次均为 **0/0，约 42 tokens，0.14s**（未找到相关代码）；cost=N/A，详见 `examples/django-orm/README.md`。最新真实数字见 §9.4.1 复现性声明段。

### 9.3.4 Tokio：异步调度

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/tokio-runtime/README.md`](../examples/tokio-runtime/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：tokio-rs/tokio。
- **提示词**：`How does tokio schedule and run async tasks on its runtime?`
- **期望**：worker → scheduler → task 的调度与 poll 路径。
- **实测**：2 次均为 **0/0，约 41 tokens，0.14s**（未找到相关代码）；cost=N/A，详见 `examples/tokio-runtime/README.md`。最新真实数字见 §9.4.1 复现性声明段。

### 9.3.5 OkHttp：拦截器链

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/okhttp-interceptors/README.md`](../examples/okhttp-interceptors/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：square/okhttp。
- **提示词**：`How does OkHttp process a request through its interceptor chain?`
- **期望**：`RealInterceptorChain` 依次驱动 application/network interceptors。
- **实测**：2 次均为 **1/1，约 885 tokens，0.14s**；cost=N/A，详见 `examples/okhttp-interceptors/README.md`。最新真实数字见 §9.4.1 复现性声明段。

### 9.3.6 Gin：路由与中间件

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/gin-middleware/README.md`](../examples/gin-middleware/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：gin-gonic/gin。
- **提示词**：`How does gin route requests through its middleware chain?`
- **期望**：router tree 命中 route，拼接 middleware，最后调用 handler。
- **实测**：2 次均为 **82/3，约 2603 tokens，0.17s**；cost=N/A，详见 `examples/gin-middleware/README.md`。最新真实数字见 §9.4.1 复现性声明段。

### 9.3.7 Alamofire：请求生命周期

> ⚠ **本节"实测参考"为旧探针数据**（基于 2025-07 commit）。当前 commit + cg 1.5.0 的真实跑分见 [`examples/alamofire-request/README.md`](../examples/alamofire-request/README.md)；与本节数字对比见 §9.4.1。

- **仓库/commit**：Alamofire/Alamofire。
- **提示词**：`How does Alamofire build, send, and validate a request?`
- **期望**：Request 构造、URLSession 发送与 validation 的连续路径。
- **实测**：2 次均为 **0/0，约 40 tokens，0.14s**（未找到相关代码）；cost=N/A，详见 `examples/alamofire-request/README.md`。最新真实数字见 §9.4.1 复现性声明段。

## 9.4 综合分析

README 自报的整体数字是 **89% 工具调用下降、69% token 节省、60% 成本下降**（WITH/WITHOUT 的四次中位数汇总）；它还报告七仓均为零文件读取。本文探针只测索引查询，不运行对照 agent，故不能诚实地重算这三个百分比；实测表中的 MCP 查询次数固定为 2，tokens 是响应字节估算，cost 为 N/A。要重测整体数字，应按 README 的 `claude -p` 方法跑四次/臂，并报告中位数。README 的仓库级 WITH 数据为：VS Code 2 tools/265k/$0.36，Excalidraw 3/324k/$0.40，Django 2/254k/$0.35，Tokio 3/386k/$0.44，OkHttp 1/156k/$0.23，Gin 3/246k/$0.27，Alamofire 3/316k/$0.35。

### 9.4.1 复现性声明

9.3 节的"实测"数字为**早期探针参考值**;当前 commit + cg 1.5.0 的真实跑分见 `examples/README.md` 汇总表与各子目录 README。每个子目录提供了:

- 真实 commit SHA + `git rev-parse HEAD` 验证
- 完整 `git clone --depth=1 --filter=blob:none --sparse` + `git sparse-checkout set` 步骤
- `codegraph init` 的真实 stdout(文件数、节点数、边数、耗时)
- `codegraph explore "<原问题>" --max-files 12` 跑 2 次响应(前 50 行原文)
- 统计: symbols / files / tokens≈(响应字节/4) / wall-clock time
- 与 9.3 节引用数字 + README 自报 agent arm 数据的对比表

**已知差异**(2026-07-27 跑分 vs 9.3 引用):

- 9.3 引用基于早期 cg 版本(2025-07 前后 commit + 旧探针),当前已升级到 cg v1.5.0 / 2026-07 HEAD,数字以本汇总表为准
- 当前 `codegraph_explore` 默认回 5–10 个 symbols + 3–4 个文件 + blast radius;旧探针可能只回 1 个入口符号
- 本次按"框架核心目录"做 sparse-checkout;旧探针可能全收
- 因此 9.3 引用数字普遍低于本汇总表;只有 Gin 接近(82/3/2418 vs 82/3/2603,偏差 ~7%)

要严格复现 9.3 数字,需要锁定 2025-07 前后 commit + 旧 cg 版本;新版数字反映 cg 1.5.0 的扩展响应策略,因此更接近"实际生产环境"的 MCP 体验。

## 9.5 本章小结

七个问题覆盖 TypeScript、Python、Rust、Java、Go、Swift 和多层框架调用。稳定的复现流程是：浅克隆、完整索引、预热、固定参数、重复运行、区分探针与 agent 账单。

## 9.6 常见踩坑

- 仓库过大时用 `--depth=1 --filter=blob:none --sparse`，不要把历史和无关 blob 拉满。
- daemon 冷启动会污染 time；先初始化并预热，再开始计时。
- `MODEL=sonnet` 与 Opus/其他模型的工具策略、token 和费用不可直接比较；`EFFORT=high` 也必须固定。
- 响应字节除以 4 仅是估算；不要把它写成 API token 或 cost。

## 9.7 下一章预告

下一章（{{chapter:10}}）进入进程拓扑，解释 CLI、daemon、MCP server 与索引数据库如何协作。

## 9.8 参考

- `/Users/digoal/new/codegraph/README.md:218-248`（方法、表格与原始问题）
- `/Users/digoal/new/codegraph/scripts/agent-eval/`（评估脚本与指标解析）
- `examples/{vscode-extension-host,excalidraw-canvas,django-orm,tokio-runtime,okhttp-interceptors,gin-middleware,alamofire-request}/README.md`（本章逐次日志）
