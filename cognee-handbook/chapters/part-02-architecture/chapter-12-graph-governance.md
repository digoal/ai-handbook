# 第 12 章 `Graph Governance: 大图治理`

> 本章目标:读完本章,你将能够
> - 用内容哈希增量同步多个 Dataset,并区分 `sync` 与 `push`
> - 用迁移链、安全剪枝和数据集级锁控制 schema 演进与并发写入
> - 用 Truth Subspace 让检索结果偏向与已确认经验一致的证据

## 前置知识

- 已读完 [[chapter-07-data-model|第 7 章 数据模型与实体:DataPoint / Entity / NodeSet / KnowledgeGraph]](./chapter-07-data-model.md),理解
  DataPoint、Entity、Edge、NodeSet 与 Dataset 的关系
- 需要的基础库:`cognee>=1.4.0`、`pydantic>=2.0`、`asyncio`
- 环境:Python 3.10–3.14,并已配置 LLM 与 Embedding provider

## 本章导览

- 12.1:用哈希差集做多 Dataset 双向增量同步
- 12.2:用 Alembic 语义管理关系、图与向量存储的 schema
- 12.3:构建 Truth Subspace,重排更一致、更可解释的证据
- 12.4:区分全局 `prune` 与有权限边界的定向 `delete`
- 12.5:理解数据集级锁的能力边界
- 12.6:通过 SDK 或 CLI 向 Cognee Cloud 推送知识图

大图治理不是“图太大就删节点”,而是建立四条控制回路:写入前用 Dataset 边界、稳定标识和锁
抑制重复;传输时用哈希差集降低放大效应;发布时用 revision 保证三类存储处于兼容状态;检索与
清理时分别用 Truth Subspace 和 provenance 决定哪些证据应被提升、哪些派生物可以回收。
架构师应为每个 Dataset 记录负责人、真源位置、schema revision、最近同步游标、允许的写入者和
恢复目标。这样节点数异常时,团队能判断问题来自重复摄取、schema 漂移、同步冲突还是正常增长,
而不是直接执行不可逆清空。

---

## 12.1 `modules/sync` 增量同步

当图规模增长时,最昂贵的做法是每次上传全部原始文件并重建知识图。Cognee 的增量单位不是
“最近修改时间”,而是 Data 记录中的 `raw_content_hash`:本地与 Cloud 交换哈希集合,只传输差集。
核心流程位于
`<COGNEE_REPO>/cognee/api/v1/sync/sync.py`,操作状态则由
`<COGNEE_REPO>/cognee/modules/sync/models/SyncOperation.py` 持久化。

![Ch12 — 多 Dataset 增量同步流程](../../assets/diagrams/ch12-01-dataset.svg)

服务端在 `<COGNEE_REPO>/cognee/api/client.py` 将路由挂到
`/api/v1/sync`;路由实现见
`<COGNEE_REPO>/cognee/api/v1/sync/routers/get_sync_router.py`。请求不指定
`dataset_ids` 时同步当前用户可写的全部 Dataset;指定时仍逐一做权限检查。接口立即返回 `run_id`,
后台最多重试三次,同一用户已有运行中任务时返回 409。

```bash
curl -X POST "http://localhost:8000/api/v1/sync" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: <你的API_KEY>" \
  -d '{"dataset_ids":["<你的数据集UUID>"]}'

curl -H "X-Api-Key: <你的API_KEY>" \
  "http://localhost:8000/api/v1/sync/status"
```

这里的“Dataset 间同步”是多个 Dataset 各自与 Cloud 对齐,不是把本地 A 合并进本地 B。当前算法
双向补齐文件,更接近集合并集。源码虽然定义了 `_prune_cloud_dataset()`,但当前没有调用点,因此不要
假设远端多余文件会随本地删除而自动消失。生产上应明确唯一真源、冲突规则与删除传播策略。

建议把同步验收定义为可核对指标,而不是只看 HTTP 200:比较本地与远端哈希集合、上传与下载字节数、
失败 Dataset 列表、后台状态和认知化结果。`SyncOperation.dataset_sync_hashes` 会记录各 Dataset 本次
上传与下载的哈希,可以作为数据血缘证据;但公开路由目前只有运行中任务概览,没有按 `run_id` 查询的
完整端点。需要长期审计时,应从关系库采集该记录或补充受权限保护的运维接口。

---

## 12.2 `alembic` 数据库迁移

schema 演进不能只改关系表:Node/Edge 标识、向量 payload 与迁移账本可能必须同时变化。
`<COGNEE_REPO>/cognee/alembic/versions/` 保存关系库 Alembic revision;
`<COGNEE_REPO>/cognee/modules/migrations/startup.py` 再编排跨存储迁移。升级顺序是
**关系 schema → 图/向量数据链**;降级顺序相反,避免先删除迁移账本。

| 命令 | 作用 | 治理注意点 |
|---|---|---|
| `history` | 按新到旧列出数据迁移链 | 标记 head 与是否可逆 |
| `current` | 显示每个数据库已 stamp 的 revision | 同时暴露最近失败信息 |
| `upgrade` | 关系库先升级,再变换图/向量 | 已到目标的库跳过 |
| `downgrade` | 先回退数据,可选回退关系 schema | 只允许所有步骤都有 `down()` 的区间 |
| `stamp` | 只修订账本,不执行迁移 | 仅用于已人工验证的恢复场景 |

完整运维命令如下。本文按产品命令写作;若安装包只暴露 `cognee-cli`,将开头的 `cognee`
替换为 `cognee-cli`,参数不变。

```bash
cognee history
cognee current
cognee upgrade head --alembic head
cognee downgrade base --alembic base --force
cognee stamp base --dataset <你的数据集UUID> --force
```

`cognee upgrade` 可在 `ENABLE_AUTO_MIGRATIONS=false` 时显式执行。新库会由 `create_all` 创建
当前 schema 后 `stamp head`;旧库才回放 revision。发布时先备份三类存储,再运行 `history` 与
`current`,在影子环境升级并验证节点数、边数与检索结果,最后升级生产。升级期间要暂停目标
Dataset 的写入,并把应用版本与数据库 revision 作为同一个发布单元;否则旧 worker 可能在新 schema
上写入旧格式。若某个 Dataset 迁移失败,写入口会阻止继续混写,应先保留失败日志与备份快照,修复后
重试,而不是跳过该库。

`stamp` 不会修数据,错误地 stamp 到 head 会永久跳过必要变换。CLI 入口与五个子命令分别见
`<COGNEE_REPO>/cognee/cli/_cognee.py` 和
`<COGNEE_REPO>/cognee/cli/commands/migrate_command.py`。

---

## 12.3 Truth Subspace

节点越多,向量相似并不等于证据与已确认经验一致。Truth Subspace(真值子空间)把
`session_learnings` 中接受过的经验嵌入为最多 8 个确定性 centroid slot,再把所有
DocumentChunk 投影为 `truth_alignment` 坐标。查询也投影到同一基底,HYBRID 检索按一致度把
原 RRF 分数乘以 0.75–1.25 的因子。

它并不直接返回一个独立“真理子图”;当前实现只重排 HYBRID 的 chunk 通道。被选中的 chunk、
Entity 与 fact 共同组成更一致的可解释证据子图。缺少 centroid、坐标过期或读取失败时会
fail-open 到中性因子 1.0,不会破坏基线排序。构建逻辑见
`<COGNEE_REPO>/cognee/modules/truth_subspace/build.py`,数学函数见
`<COGNEE_REPO>/cognee/modules/truth_subspace/align.py`,接入点见
`<COGNEE_REPO>/cognee/modules/retrieval/hybrid_retriever.py`。

```python
import asyncio
import cognee
from cognee.modules.truth_subspace.build import build_truth_subspace
from cognee.modules.users.methods import get_default_user

async def main():
    dataset = "governance_demo"
    await cognee.add(
        ["合同退款期为七天。", "企业合同退款需由财务复核。"],
        dataset_name=dataset,
        node_set=["corpus"],
    )
    await cognee.add(
        ["已确认经验:企业退款必须经过财务复核。"],
        dataset_name=dataset,
        node_set=["session_learnings"],
    )
    await cognee.cognify(datasets=[dataset])

    user = await get_default_user()
    print(await build_truth_subspace(dataset, session_ids=None, user=user))
    result = await cognee.search(
        "企业客户如何退款?",
        query_type=cognee.SearchType.HYBRID_COMPLETION,
        datasets=[dataset],
        retriever_specific_config={"use_truth_weight": True},
    )
    print(result)

asyncio.run(main())
```

若经验来自真实 session,优先使用
`cognee.improve(dataset=..., session_ids=[...], build_truth_subspace=True)`;它会先蒸馏经验再建
子空间。每次 centroid 变化都会提升 `truth_epoch`,检索只使用当前 epoch 的节点坐标,防止
schema 或学习集合变化后混用旧分数。

可解释性不应只展示最终答案。审计记录至少应包含查询文本、候选 chunk 的基线 RRF 分数、
`truth_epoch`、使用的 centroid slot、乘法因子以及重排前后名次。这样当某条错误经验把证据推高时,
可以追溯到具体 `session_learnings` 并重新构建子空间。由于权重范围被限制在 0.75–1.25,Truth
Subspace 是温和校准器,不能替代事实校验、权限过滤或来源可信度判断。

---

## 12.4 `cognee.prune` 反向剪枝

这里的 prune 不是“按低权重逐节点修枝”。它是从衍生存储反向清空并准备重建的维护工具。
`<COGNEE_REPO>/cognee/api/v1/prune/prune.py` 暴露的是 namespace 风格接口:
`prune_data()` 删除原始文件,`prune_system()` 清空图、向量与 cache;包装层默认
`metadata=False`,所以关系元数据默认保留。底层明确说明它没有权限检查,仅适合开发、测试或
已停写的灾难恢复窗口。

```python
import asyncio
import cognee

async def main():
    # 高危:清空所有 Dataset 的图、向量和 cache,但默认保留关系元数据。
    await cognee.prune.prune_system(
        graph=True,
        vector=True,
        metadata=False,
        cache=True,
    )

asyncio.run(main())
```

不要写成 `await cognee.prune()`:当前 `prune` 是类式 namespace,不是可等待函数。若只想删除一份
数据及其派生节点/边,应使用 Ch03 已介绍的定向删除。删除路径会依据 provenance 清理图、向量、
关系账本,并回收孤立 EdgeType 与失效 NodeSet 标签,关键实现见
`<COGNEE_REPO>/cognee/modules/graph/methods/delete_from_graph_and_vector.py`。

| 维度 | `cognee.datasets.delete_data()` / `cognee.delete()` | `cognee.prune.*()` |
|---|---|---|
| 范围 | 指定 Dataset 中的指定 Data | 全局存储后端 |
| 权限 | 校验 delete 权限 | 无权限检查 |
| 用途 | 正常业务删除、回收关联孤儿 | 测试重置、全量重建 |
| 风险 | 可控制;旧 `cognee.delete()` 已弃用 | 极高,不应在线调用 |

因此,节点爆炸时先修正 Ch07 的 identity_fields、Dataset 边界与重复摄取源,再定向删除;只有
派生存储已无法可信修复时,才备份、停写、prune 并全量 `cognify` 重建。

---

## 12.5 数据集级锁

同一 Dataset 的两个 pipeline 若同时写入,可能重复创建节点、覆盖状态或让回滚边界交错。
`<COGNEE_REPO>/cognee/modules/pipelines/operations/pipeline.py` 为每个 Dataset UUID
维护一个 `asyncio.Lock`:同 Dataset 串行,不同 Dataset 可并行。嵌套 pipeline 通过
`ContextVar` 识别已持锁 Dataset,避免同一执行链重复加锁而自锁。

这个锁只在**单进程事件循环**内有效,不能保护多个 API worker、多个容器或多台主机。文件型
SQLite + LanceDB + Ladybug 部署应收敛到单写服务;CLI 并发场景通过 `--api-url` 委托给同一
服务。真正的多副本生产部署仍需要数据库 advisory lock 或分布式租约,并以 Dataset UUID 作为
锁键。锁也不替代幂等键:内容哈希与稳定节点 ID 仍是崩溃重试后的最后防线。

---

## 12.6 Cognee Cloud 推送

`sync` 传原始文件差集并在两端认知化;`push` 则把已经构建好的图导出为 COGX archive,上传后
直接导入远端。`cognee.push()` 位于
`<COGNEE_REPO>/cognee/api/v1/push/push.py`,CLI 位于
`<COGNEE_REPO>/cognee/cli/commands/push_command.py`。它不调用 `/v1/sync`,而是复用
CloudClient 的 `remember` 上传通道。

```bash
export COGNEE_SERVICE_URL="https://<你的CogneeCloud地址>"
export COGNEE_API_KEY="<你的API_KEY>"

cognee push governance_demo \
  --target-dataset production_graph \
  --mode preserve \
  --background
```

`preserve` 直接映射 entity/fact,不调用 LLM;`hybrid` 保留图并认知化原文;`re-derive` 忽略导出
图并在远端重建。大图推荐 `--background`,记录返回的 `pipeline_run_id`。SDK 用法如下:

```python
import asyncio
import cognee

async def main():
    result = await cognee.push(
        "governance_demo",
        target_dataset="production_graph",
        mode="preserve",
        run_in_background=True,
        url="https://<你的CogneeCloud地址>",
        api_key="<你的API_KEY>",
    )
    print(result.pipeline_run_id, result.num_nodes, result.num_edges)

asyncio.run(main())
```

选择原则很简单:需要持续对齐原始文件时用 `/api/v1/sync`;需要发布一份已审核、无需重新抽取的
知识图快照时用 `cognee push`。推送前先 `cognify`,因为零节点 archive 会被拒绝;也应保留本地
revision、导出时间与远端 Dataset 名,形成可审计发布记录。

## 小结

- 哈希差集让多 Dataset 同步只传变化文件,但当前删除传播不是自动镜像语义。
- `upgrade` 先关系后图/向量,`downgrade` 反向执行;`stamp` 只修账本,不修数据。
- Truth Subspace 用已确认经验轻量重排 HYBRID 证据,失败时回退基线。
- `delete` 用于有权限边界的定向回收;`prune` 是高危全局重置工具。
- 数据集级锁仅限单进程;跨 worker 必须引入统一写入口或分布式锁。

## 实践作业

1. **(基础)** 创建两个 Dataset,调用 `/api/v1/sync`,记录首次与再次同步的上传数量及 `run_id`。
2. **(进阶)** 运行 `history`、`current` 与 `upgrade`;再完成 12.3 示例,比较 Truth 权重开关前后的结果。
3. **(挑战)** 设计一份生产治理方案:包含跨进程 Dataset 锁、三存储备份、可逆迁移验证、
   `sync` 删除冲突策略,以及禁止在线 `prune` 的审批规则。

## 推荐阅读

- [[chapter-27-performance-cache|第 27 章 性能调优与缓存:Postgres Session Cache / LanceDB 索引]](../part-05-production/chapter-27-performance-cache.md):把图治理延伸到索引、缓存与容量规划。
- [[chapter-03-add-cognify-search|第 3 章 Hello World:`add` / `cognify` / `search` 三步走]](../part-01-foundation/chapter-03-add-cognify-search.md):复习正常数据生命周期与定向删除边界。
- 源码:`<COGNEE_REPO>/cognee/modules/sync/`
- 示例:`<COGNEE_REPO>/examples/python/truth_subspace_reranking_demo.py`

## 下一章预告

第 13 章将进入 v1 底层 API,系统拆解 `add`、`cognify` 与 `search` 的参数、返回值和扩展点。
