# seekdb 源码 Handbook

> 一本面向**用户、架构师、开发者**三类读者的 seekdb 源码导读。
>
> 覆盖版本：仓库 `CMakeLists.txt` 声明 `OceanBase VERSION 1.3.0.0`；
> 内容基于 `master`/`develop` 合并点 `c5176f7` 时的源码树。

---

## 这本书为什么存在

seekdb 是 OceanBase 团队开源的 AI-native 搜索数据库——约 **281 万行 C++**，
`src/` 下 5,434 个源文件，仓库 1GB。它在 OceanBase 内核底座上叠加了向量索引、
异步索引管线、COW 沙箱、混合检索和库内 AI 模型调用。

但仓库自带的文档只有两端：

- **`README.md`** —— 面向终端用户，讲"能做什么"，不讲"怎么实现的"；
- **`docs/developer-guide/`** —— 14 篇，讲工具链、构建、调试、编码规范，**不讲架构**。

中间那一层——**代码怎么组织、一条 SQL 怎么走完全程、向量索引凭什么快、
seekdb 相对 OceanBase 裁掉了什么**——完全空缺。这本书就是来补这一层的。

---

## 三条阅读路线

不必从头读到尾。按你的身份挑一条：

### 🧑‍💻 我是**用户** —— 我要用 seekdb 建一个 AI 应用

> [0.1 seekdb 是什么](00-orientation/01-what-is-seekdb.md) →
> [1.1 30 秒上手](10-user/01-quickstart.md) →
> [1.2 数据建模](10-user/02-data-modeling.md) →
> [1.3 混合检索](10-user/03-hybrid-search.md) →
> [1.4 FORK/MERGE 沙箱](10-user/04-fork-merge.md) →
> [1.5 库内 AI 函数](10-user/05-in-db-ai.md)

需要上线时再看 [1.7 部署与配置](10-user/07-deploy-config.md) 和
[1.8 可观测性](10-user/08-observability.md)。

### 🏛 我是**架构师** —— 我要判断 seekdb 能不能扛住我的场景

> [0.3 代码地图](00-orientation/03-code-map.md) →
> [2.1 分层与启动](20-architect/01-layering-and-startup.md) →
> [2.2 MTL 之死](20-architect/02-what-seekdb-removed.md) →
> [2.10 向量索引架构](20-architect/10-vector-index.md) →
> [2.11 Change Stream](20-architect/11-change-stream.md) →
> [2.13 FORK/MERGE COW](20-architect/13-fork-merge-cow.md)

想看经典内核（SQL / 存储 / 事务）走 2.3 – 2.9。

### 🔧 我是**开发者** —— 我要改 seekdb 的代码

> [0.3 代码地图](00-orientation/03-code-map.md) →
> [3.1 环境与构建](30-developer/01-build.md) →
> [3.2 oblib 基础设施](30-developer/02-oblib.md) →
> [3.3 编码规范](30-developer/03-conventions.md) →
> [3.5 测试体系](30-developer/05-testing.md) →
> [3.6 实战：新增 SQL 函数](30-developer/06-hands-on-sql-function.md)

---

## 全书目录

### 第 0 篇 · 导览

| 章 | 标题 |
|---|---|
| 0.1 | [seekdb 是什么：从 OceanBase 到 Agent 状态存储](00-orientation/01-what-is-seekdb.md) |
| 0.2 | [三种形态：嵌入式 / 单机 Server / 集群](00-orientation/02-three-modes.md) |
| 0.3 | [代码地图：一张图看懂 1GB 仓库](00-orientation/03-code-map.md) |

### 第 1 篇 · 用户视角

| 章 | 标题 |
|---|---|
| 1.1 | [30 秒上手](10-user/01-quickstart.md) |
| 1.2 | [数据建模：向量列、HEAP 表、两类索引](10-user/02-data-modeling.md) |
| 1.3 | [混合检索：一条 SQL 打通向量 + 全文 + 标量](10-user/03-hybrid-search.md) |
| 1.4 | [FORK / MERGE：给 Agent 的沙箱](10-user/04-fork-merge.md) |
| 1.5 | [库内 AI：AI_EMBED / AI_COMPLETE / AI_RERANK / AI_PROMPT](10-user/05-in-db-ai.md) |
| 1.6 | [生态集成](10-user/06-ecosystem.md) |
| 1.7 | [部署与配置](10-user/07-deploy-config.md) |
| 1.8 | [可观测性与排障](10-user/08-observability.md) |

### 第 2 篇 · 架构师视角

| 章 | 标题 |
|---|---|
| 2.1 | [总体分层与启动生命周期](20-architect/01-layering-and-startup.md) |
| 2.2 | [seekdb 裁掉了什么：MTL 之死](20-architect/02-what-seekdb-removed.md) |
| 2.3 | [一条 SELECT 的一生（上）：协议到 resolve](20-architect/03-select-lifecycle-1.md) |
| 2.4 | [一条 SELECT 的一生（下）：优化到执行](20-architect/04-select-lifecycle-2.md) |
| 2.5 | [计划缓存与执行框架：DAS / DTL / PX](20-architect/05-plancache-das-dtl.md) |
| 2.6 | [一行数据的一生：LSM-Tree](20-architect/06-lsm-tree.md) |
| 2.7 | [存储格式：宏块、微块、编码压缩](20-architect/07-storage-format.md) |
| 2.8 | [事务与 MVCC](20-architect/08-transaction-mvcc.md) |
| 2.9 | [日志服务 palf 与单副本裁剪](20-architect/09-palf.md) |
| 2.10 | [★ 向量索引架构：两级 HNSW 与 VSAG](20-architect/10-vector-index.md) |
| 2.11 | [★ Change Stream：P99 为何是平的](20-architect/11-change-stream.md) |
| 2.12 | [★ 混合检索的算子融合](20-architect/12-hybrid-search-internals.md) |
| 2.13 | [★ FORK / MERGE 的 COW 实现](20-architect/13-fork-merge-cow.md) |
| 2.14 | [★ 库内 AI Service 架构](20-architect/14-ai-service.md) |

### 第 3 篇 · 开发者视角

| 章 | 标题 |
|---|---|
| 3.1 | [环境与构建](30-developer/01-build.md) |
| 3.2 | [oblib 基础设施：内存、容器、日志](30-developer/02-oblib.md) |
| 3.3 | [编码规范](30-developer/03-conventions.md) |
| 3.4 | [调试武器库](30-developer/04-debugging.md) |
| 3.5 | [测试体系](30-developer/05-testing.md) |
| 3.6 | [实战一：新增一个 SQL 内建函数](30-developer/06-hands-on-sql-function.md) |
| 3.7 | [实战二：读懂并扩展向量索引](30-developer/07-hands-on-vector-index.md) |

### 附录

| # | 标题 |
|---|---|
| A | [目录速查表](90-appendix/A-directory-map.md) |
| B | [关键类速查表](90-appendix/B-class-index.md) |
| C | [参数与虚拟表速查](90-appendix/C-config-and-views.md) |
| D | [术语表](90-appendix/D-glossary.md) |

---

## 关于本书的可信度

技术书最大的风险是"看起来很懂，其实在编"。本书采取三条自律：

1. **每个论断都落到文件路径。** 每章都有"代码锚点"表，
   给出 `文件:行` 与它负责什么。你可以直接打开核对。
2. **示例区分来源。** 每段 SQL / 命令都标注出处：
   来自 `README.md`、来自某个 mysqltest 用例、还是作者构造的说明性示例。
3. **没跑过的就说没跑过。** 本书写作时**未编译、未启动** seekdb
   （完整 C++ 工具链构建成本高）。所有标注 `⚠️ 未实机验证` 的示例，
   表示它源自源码与测试用例的推导，但作者没有真正执行过。
   四个重点主题在 `tools/deploy/mysql_test/test_suite/` 下有 **86 个官方用例**，
   是本书示例最可靠的来源。

发现错误请开 issue —— 尤其是那些"路径对不上"的地方，那说明代码演进了。

---

## 图例约定

本书所有插图以 Mermaid 编写、预渲染为 SVG：

- 源码：`assets/mmd/*.mmd`（可 diff、可增量维护）
- 产物：`assets/*.svg`（GitHub / mkdocs / IDE / 离线均可显示）

重新渲染全部插图：

```bash
cd docs/handbook/assets
for f in mmd/*.mmd; do
  mmdc -i "$f" -o "$(basename "$f" .mmd).svg" -b transparent
done
```
