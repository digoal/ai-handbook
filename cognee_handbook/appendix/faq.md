# FAQ

> 本附录汇总 30 章正文中读者最常问到的 28 个问题。主题覆盖安装、ECL（Extract–Cognify–Load，抽取—认知化—加载）/API、SearchType（搜索类型）、集成、性能和故障排查。以下说明以 Cognee v1.4.0 为基线；代码中的 `cognee` 默认指 `<COGNEE_REPO>`。

## 一、安装与环境

### Q1: Python 版本要求？为什么需要 3.10+？

Cognee v1.4.0 的发布元数据要求 Python `>=3.10,<3.15`，不是文档随意约定。类型注解、异步上下文管理和若干依赖的 wheel 都以这一范围为测试边界；低于 3.10 时，安装解析器会拒绝项目或退回没有兼容 wheel 的源码构建。依据见 `<COGNEE_REPO>/pyproject.toml` 第 10 行，以及 Ch02。

先创建隔离环境并确认解释器，再安装：

```bash
cd <COGNEE_REPO>
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
pip install cognee==1.4.0
python -c "import sys, cognee; print(sys.version); print(cognee.__file__)"
```

如果系统只有 3.9，最稳妥的解决办法是安装 3.10–3.14 中一个受支持版本，而不是强行改 `pyproject.toml`。生产环境还应把 Python 版本写入 Docker 镜像或 CI 矩阵，避免开发机和部署机解析出不同依赖。

### Q2: 能否离线安装？有没有 wheel 包？

可以，但离线安装解决的是 Python 包下载，不会自动解决首次运行所需的 LLM、embedding 模型或数据库镜像。先在联网且同平台的机器上下载 Cognee 及依赖到目录，再把整个目录带到隔离网络；`--no-index` 会禁止 pip 联网，只从指定目录找 wheel。

```bash
python -m pip download --dest /tmp/cognee-wheels "cognee==1.4.0"
# 将 /tmp/cognee-wheels 复制至离线机后执行
python -m pip install --no-index --find-links /tmp/cognee-wheels "cognee==1.4.0"
```

Ch02 的离线说明和 `<COGNEE_REPO>/pyproject.toml` 的 wheel 约束都表明，下载时必须使用与目标 Python、操作系统和架构匹配的 wheel。若某个依赖只有源码包，离线机还需预装编译器和系统库；这也是 Docker 方案常比裸 pip 更可重复的原因。

### Q3: 默认后端有哪些？如何切换到 Postgres 全栈？

开发默认通常采用本地 SQLite（元数据）加 LanceDB（向量）和 Ladybug（图），优点是零服务启动，缺点是并发和运维能力有限。Ch10 的后端表说明了关系、向量、图三类存储可以分别替换；配置本身集中在 `<COGNEE_REPO>/cognee/api/v1/config/config.py`（通过 `cognee.config` 导入），而不是散落在业务函数中。

可以在环境变量中切换连接信息，再用同一套 ECL 调用：

```bash
export DB_PROVIDER=postgres
export VECTOR_DB_PROVIDER=pgvector
export GRAPH_DATABASE_PROVIDER=postgres
export DB_NAME=cognee
export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_USERNAME=cognee
export DB_PASSWORD=<你的数据库密码>
python -c "import cognee; print('backend configured')"
```

Ch10 的原则是先配置后导入 API；不要在已经写入数据后随意更换 provider 并期待旧数据自动迁移。上线前执行迁移命令、确认权限并做一次 add/cognify/search 烟测。

### Q4: Docker 镜像和 pip 安装的区别？

`pip install` 只安装 Python 包，进程、数据库和端口仍由你负责；Docker Compose 则把应用、依赖服务、环境变量和网络编排在一起。Ch02 的安装示例与 Ch28 的 `<COGNEE_REPO>/docker-compose.yml` 分别代表库模式和服务模式，二者调用的 Cognee API 可以相同。

库内快速试用可以这样做：

```bash
python -m pip install "cognee==1.4.0"
python -c "import asyncio, cognee; asyncio.run(cognee.add('hello'))"
```

需要 Postgres、Neo4j 或对外 HTTP 服务时使用 Compose 更合适：

```bash
cd <COGNEE_REPO>
docker compose up -d
curl http://127.0.0.1:8000/health
```

Docker 并不会替你配置有效的 API key、持久化卷和备份策略。开发时 pip 较快，团队集成和生产环境则应固定镜像 tag、挂载数据卷并检查健康检查。

### Q5: `uv`、`poetry`、`pip` 哪个推荐？

三者都是包管理方案，不是三套 Cognee API。Ch02 对比指出：pip 最普及，适合已有 requirements/venv 流程；Poetry 把锁文件、发布和虚拟环境统一起来；uv 解析和同步速度快，适合从 `pyproject.toml` 建立可复现环境。团队应选一种作为 CI 唯一入口，避免混用生成互不一致的锁文件。

例如使用 uv：

```bash
cd <COGNEE_REPO>
uv venv --python 3.12
uv pip install "cognee==1.4.0"
uv run python -c "import cognee; print(cognee.__file__)"
```

使用 pip 也完全受支持：

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install -U pip
python -m pip install "cognee==1.4.0"
```

关键不是工具品牌，而是锁定 Python、Cognee 和底层模型版本，并在干净环境执行一次 smoke test。

## 二、ECL 与 API

### Q6: `add` 和 `remember` 的差别？何时用哪个？

`add` 是 v1 API 的摄取入口，适合把文本、文件或 URL 放入一个数据集，随后显式调用 `cognify` 建图并 `search` 查询。`remember` 是 v2 memory API 的语义入口，表达“把这条经验或事件记入长期记忆”，可携带来源、用户和记忆策略。Ch13 与 Ch14 分别解释了这两个抽象，不能只按函数名判断它们完全等价。

```python
import asyncio
import cognee

async def main():
    await cognee.add("退款规则：订单完成后七日内可申请。")
    await cognee.cognify()
    print(await cognee.search("退款期限"))

asyncio.run(main())
```

面向 agent 事件可用 v2 入口（具体签名以安装版本的 `help` 为准）：

```python
import asyncio, cognee
asyncio.run(cognee.remember("用户偏好使用中文回答"))
```

迁移旧资料或批量文档优先使用 add/cognify；会话中的事实、偏好和反馈优先使用 remember。两者最终都依赖配置的数据集和存储后端。

### Q7: `cognify` 为什么慢？能不能并行？

`cognify` 不是一次简单的写入，它要执行抽取、分块/嵌入、实体关系识别、图构建和落盘等 pipeline（流水线）步骤。Ch03 描述的五步链路中，LLM 和 embedding 请求、图写入都可能成为瓶颈；因此 add 很快而 cognify 较慢是正常现象。

先把任务并发度配置在 pipeline 层，而不是同时启动大量无控制的 Python 进程：

```python
import asyncio, cognee

# 常规调用会使用已配置的 pipeline
asyncio.run(cognee.cognify())
```

Ch08 介绍了 pipeline 并发调优的方法。并发提高吞吐，也会提高 API 限流、数据库连接和内存压力；从 2 或 4 开始压测，结合 Ch11 trace 观察哪一步真正耗时。具体并发参数请以当前版本 pipeline 配置文档为准。

### Q8: `memify` 一定要调吗？

不一定。`memify` 是在已有数据和图之上运行记忆增强 pipeline 的动作，用来生成适合特定 agent/领域的摘要、规则或结构化记忆。Ch16 说明 v1.4.0 默认提供七个预定义 memify pipeline；普通文档问答只需 add → cognify → search，不必每次重复 memify。

需要长期偏好、用户画像或领域规则时再调用：

```python
import asyncio, cognee

async def main():
    await cognee.add("产品手册：管理员可以重置成员密码")
    await cognee.cognify()
    await cognee.memify()

asyncio.run(main())
```

实际部署应先确认当前版本暴露的 pipeline 名称和配置，再为 memify 结果单独做回归评估。它会带来额外 LLM 成本和写入时间，故不应把它当作 cognify 的别名。

### Q9: `delete` 和 `prune` 的差别？

`delete` 是有权限边界的定向删除，目标是明确移除一批数据及其派生索引；`prune` 是高危全局维护操作，清空图、向量和 cache 并准备重建，不是按 Truth Subspace（真值子空间）逐节点剪枝。Ch03、Ch12 强调两者的风险不同：delete 更像生命周期删除，prune 更像派生存储重置。

```python
import cognee

async def delete_one(dataset_id, data_id):
    # 传入已授权的 dataset_id 和 data_id
    await cognee.datasets.delete_data(dataset_id=dataset_id, data_id=data_id)
    # prune_data 删除原始文件；prune_system 全局重置派生存储，均须先备份并停写
    # await cognee.prune.prune_data()  # 或 prune_system(...)
```

不要把 prune 当作数据库回收站，也不要在没有快照的生产库直接试验。先导出、在测试数据集运行，再检查 search 结果和图规模。

### Q10: 数据集（dataset）隔离怎么做？

数据集是租户或工作空间边界，不只是一个显示名称。Ch24 的 `<COGNEE_REPO>/cognee/modules/users/` 与 permissions（权限）模块负责用户、数据集和访问授权的关联；查询时必须在同一 dataset 上下文中执行，不能靠提示词要求模型“不要看别人的数据”。

最小调用模式如下：

```python
import asyncio, cognee

async def main():
    await cognee.add("仅供团队 A 使用的设计文档", dataset_name="team-a")
    await cognee.cognify(datasets=["team-a"])
    result = await cognee.search("设计文档", datasets=["team-a"])
    print(result)

asyncio.run(main())
```

API 服务中还要把认证用户映射到允许的数据集，并让数据库账号只拥有必要权限。跨租户查询应由服务层明确授权、审计和限流。

### Q11: 能否同时跑多个数据集的 cognify？

可以排队或在受控 worker 中处理，但不能假设同一进程内多个 cognify 完全独立。Ch24 提到 dataset 级进程内锁，目的是防止同一数据集的并发 pipeline 破坏状态；不同数据集仍共享 LLM 限额、CPU、连接池和缓存。

```python
import asyncio, cognee

async def run_one(name, text):
    await cognee.add(text, dataset_name=name)
    await cognee.cognify(datasets=[name])

async def main():
    await asyncio.gather(
        run_one("a", "A 的资料"),
        run_one("b", "B 的资料"),
    )

asyncio.run(main())
```

生产上更推荐任务队列按 dataset key 串行化、按租户限额并发，并在失败时记录 pipeline 状态。若两个任务共享默认本地 SQLite，仍可能受文件锁限制，应改用适合并发的后端。

## 三、SearchType

### Q12: 18 种 SearchType 该怎么选？

先按问题形状选，而不是追求“最强”：向量检索适合语义相似，关键词适合精确术语，图完成适合实体关系，多跳/组合问题使用图与向量混合；不确定时才用 `FEELING_LUCKY`。Ch15 的决策树给出了从事实查找、关系追踪到复杂推理的选择顺序。

```python
import asyncio, cognee
from cognee.modules.search.types import SearchType

async def main():
    result = await cognee.search(
        "谁负责发布？", query_type=SearchType.GRAPH_COMPLETION
    )
    print(result)

asyncio.run(main())
```

先用小集合比较命中率、延迟和 token 成本，再固定类型。SearchType 还受数据是否已 cognify、图质量和 embedding 模型影响，单换枚举值不能弥补数据管线问题。

### Q13: `FEELING_LUCKY` 是什么原理？

它不是随机抽签，而是让 LLM 根据问题和可用检索器自动选择策略。Ch15 将它定位为探索性入口：面对问题类型不稳定的 agent 很方便，但多一次决策调用，延迟、成本和可解释性都不如显式 SearchType。

```python
import asyncio, cognee
from cognee.modules.search.types import SearchType

async def main():
    print(await cognee.search("总结这批资料的关键关系",
                              query_type=SearchType.FEELING_LUCKY))
asyncio.run(main())
```

生产系统可在开发阶段记录自动选择结果，统计哪类问题总被选中，再把高频路径改成显式类型；同时限制输入长度和可用检索器，避免模型选择不适合的昂贵路径。

### Q14: `GRAPH_COMPLETION_COT` 比 `GRAPH_COMPLETION` 慢多少？

不能给一个对所有模型都成立的固定倍数。两者都做图完成，但 COT（Chain of Thought，思维链）会要求模型展开中间推理，通常增加 prompt/output token 和一次或多次推理时间；Ch15 的结论是它换取复杂问题的解释性与召回，具体倍率取决于图大小、模型和网络。

```python
import asyncio, cognee
from cognee.modules.search.types import SearchType

async def main():
    for kind in (SearchType.GRAPH_COMPLETION, SearchType.GRAPH_COMPLETION_COT):
        answer = await cognee.search("项目依赖谁？", query_type=kind)
        print(kind, answer)
asyncio.run(main())
```

用相同问题集记录 p50/p95 延迟、token 和正确率，不要只测单个问题。若只是单跳事实，使用普通 GRAPH_COMPLETION；只有复杂关系链确实改善质量时才为 COT 付费。

### Q15: `GRAPH_COMPLETION_DECOMPOSITION` 何时用？

它适合一个问题包含多个可分解子问题，例如“哪些服务依赖 X 且由团队 Y 维护”。Ch15 的子查询分解会先拆问题，再分别检索图，最后合并答案；因此比单次图完成更适合多条件查询，但调用次数和合并错误机会也更多。

```python
import asyncio, cognee
from cognee.modules.search.types import SearchType

async def main():
    print(await cognee.search(
        "哪些服务依赖 X 且由 Y 维护？",
        query_type=SearchType.GRAPH_COMPLETION_DECOMPOSITION,
    ))
asyncio.run(main())
```

先确认图中确实有团队、服务和依赖边。若查询本来只有一个关系，分解只会徒增延迟；对生产结果保存子查询和证据，便于审计合并答案。

### Q16: 能自定义 SearchType 吗？

可以。Ch15 的扩展点是 `cognee.modules.retrieval.register_retriever.use_retriever`：实现一个继承 `BaseRetriever` 的类，把它登记到一个新的 `SearchType` 上，然后让搜索路由发现它。不要直接改内置枚举或复制核心搜索分派逻辑，否则升级 v1.4.0 时容易冲突。

```python
from cognee.modules.retrieval.base_retriever import BaseRetriever
from cognee.modules.retrieval.register_retriever import use_retriever
from cognee.modules.search.types import SearchType

class MyRetriever(BaseRetriever):
    def __init__(self, **kwargs):
        pass

    async def get_retrieved_objects(self, query=None, query_batch=None):
        return [{"text": "来自自定义检索器", "score": 1.0}]

    async def get_context_from_objects(
        self, query=None, query_batch=None, retrieved_objects=None
    ):
        return retrieved_objects or []

    async def get_completion_from_context(
        self, query=None, query_batch=None, retrieved_objects=None, context=None
    ):
        return retrieved_objects or []

use_retriever(SearchType.CODE, MyRetriever)  # 仅作示意，新 SearchType 需在枚举中先定义
```

上面的片段展示注册形状；实际参数以 `<COGNEE_REPO>/cognee/modules/retrieval/` 中 v1.4.0 的接口为准。为自定义检索器补充空结果、超时和权限测试，并在日志中标注版本。

## 四、集成

### Q17: Claude Code 怎么挂载 Cognee？需要重启吗？

Ch20 的插件机制通过 MCP（Model Context Protocol，模型上下文协议）或项目级配置把 Cognee 工具暴露给 Claude Code；Claude Code 本身并不直接加载 Python 模块。首次增加或修改 MCP server 配置后，通常需要重新启动会话，至少要让客户端重新建立 server 连接；已经运行的旧进程不会自动读取新配置。

示例是启动 cognee-mcp 的命令形状：

```bash
claude mcp add cognee -- uv --directory <COGNEE_REPO>/cognee-mcp run cognee-mcp
claude mcp list
```

`cognee-mcp` 在 `<COGNEE_REPO>/cognee-mcp/` 独立维护，console script 入口为 `cognee-mcp`（定义在 `<COGNEE_REPO>/cognee-mcp/pyproject.toml` 的 `[project.scripts]`）。具体模块入口以 `<COGNEE_REPO>/cognee-mcp/` 和 Ch20 的配置为准。重启后先在 Claude Code 中列出工具并做一次只读 search；不要一上来给生产 MCP 进程写权限。

### Q18: `cognee-mcp` 是必须的吗？

不是。若应用直接 `import cognee`，不需要 MCP；MCP 只是让外部 agent 以标准工具协议访问 Cognee。Ch20 区分 stdio（标准输入输出，适合本机子进程）、SSE（Server-Sent Events，适合长连接服务）和 HTTP 三种模式，应按部署边界选择。

本地 stdio 的测试方式：

```bash
cd <COGNEE_REPO>/cognee-mcp
uv run cognee-mcp --transport stdio
```

`cognee-mcp` 的 Python 模块位于 `<COGNEE_REPO>/cognee-mcp/src/`，通过项目的 console script 启动：`uv run cognee-mcp`。

远程服务则由 HTTP/SSE server 监听地址，Claude Code 配置 URL。stdio 不需要开放端口，但生命周期跟客户端绑定；远程模式要配置认证、TLS、超时和健康检查。不要因为能启动 MCP 就认为底层数据库和 LLM 已经可用。

### Q19: n8n 节点能跑自定义 LLM 吗？

可以，前提是集成节点把 provider 配置传给 Cognee。Ch23 说明 n8n 等 no-code（无代码）集成通过 `LLM_PROVIDER` 及相应模型、endpoint 和 key 环境变量选择模型；节点本身不是固定只能调用某一家 LLM。

```bash
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o-mini
export LLM_API_KEY="$OPENAI_API_KEY"
```

```json
{"query":"项目负责人是谁？","search_type":"FEELING_LUCKY"}
```

变量名称和节点字段必须以 `<COGNEE_INTEGRATIONS_REPO>/` 的 v1.4.0 示例为准。自定义兼容 OpenAI API 的服务要验证 embedding 维度、超时和结构化输出；密钥应放在 n8n credential，不要写入 workflow JSON。

### Q20: VS Code 扩展和 CLI 共享数据吗？

默认可以共享：Ch23 指出两者通常使用用户目录下的 `$HOME/.cognee`，并且只要 provider、dataset 和数据库配置相同，就能看到同一存储中的数据。它们不会共享内存中的 pipeline 状态，也不代表不同虚拟环境自动使用相同配置。

```bash
ls -la "$HOME/.cognee"
cognee config list
```

若 CLI 使用项目环境变量而扩展使用自己的进程环境，结果会看似“不共享”。分别检查 `HOME`、dataset、数据库 URL、API key 和版本；多人或多工作区场景应显式指定 dataset，不要依赖默认目录。

### Q21: Strands、LangGraph、CrewAI、Google ADK 哪个最容易接入？

没有脱离场景的唯一答案。Ch21 对比表的共同结论是：若框架支持 Python async tool/function，直接把 `cognee.add/search/remember` 包成工具最简单；LangGraph 更适合把记忆作为节点和状态边，CrewAI/Strands 适合把检索包装为 tool，Google ADK 则要遵循其 tool/context 生命周期。

```python
async def memory_tool(query: str) -> str:
    import cognee
    result = await cognee.search(query)
    return str(result)
```

选择标准应是现有团队栈、异步支持、状态持久化和可观测性，而不是框架名称。先做一个只读检索工具，再接入写入和 cognify；这样能把集成问题与记忆质量问题分开定位。

## 五、性能与运维

### Q22: BEAM 是什么？100K=0.79 怎么解读？

BEAM（Benchmark for Evaluating Agent Memory，agent 记忆评测基准）用于比较记忆系统在任务中的效果，而不是数据库 QPS。Ch26 引用 Markovic 2025 的结果时，`100K=0.79` 表示在 100K 规模条件下的某项评测得分约 0.79；它不是“每秒处理 0.79 万条”，也不能直接换算成你的业务准确率。

阅读时要同时看任务定义、上下文规模、模型、检索预算和指标分母。生产评估可先固定问题集：

```python
scores = [0.8, 0.7, 0.9]
print(sum(scores) / len(scores))
```

真实系统还应记录召回、引用正确性、延迟、token 成本和遗忘/删除合规性。不要用一个 BEAM 数字替代领域回归测试。

### Q23: cognify worker 怎么并行？

Ch08 介绍了 pipeline 并发调优的方法，Ch27 的 `CACHE_BACKEND=postgres` 则针对会话/缓存路径把缓存换到 Postgres，减少重复数据库工作；二者作用层级不同。worker 数量加倍不一定加倍吞吐，还可能让 LLM 限流、Postgres 连接池和本地内存先耗尽。

```python
import os
# 把会话/缓存切到 Postgres（需 cognee[postgres]）；同时给 CACHE_DB_URL
os.environ["CACHE_BACKEND"] = "postgres"
# os.environ["CACHE_DB_URL"] = "postgresql+asyncpg://user:pass@host:5432/db"
# pipeline 并发参数按 Ch08 配置入口传入，具体字段名以当前版本为准
import asyncio, cognee
asyncio.run(cognee.cognify())
```

先测单 worker 基线，再逐步提高 pipeline 并发度，观察 Ch11 trace、数据库连接和 p95。多进程部署时确保每个 worker 使用一致配置，并避免多个 worker 同时处理同一 dataset。

### Q24: LanceDB 索引参数怎么调？

LanceDB 的 `index_params` 要围绕数据量、召回率和查询延迟调节，不能照搬某个示例数字。Ch27 的建议是先建立无索引或小样本基线，再调整向量索引类型、分区/子图规模和训练样本；数据分布变化后要重建或维护索引。

```python
from lancedb import connect

db = connect("/tmp/cognee-lance")
# 真实表名、向量列和参数需以当前 Cognee 表结构为准
# table.create_index(vector_column_name="vector", **index_params)
```

不要凭空把这段注释参数复制到生产。先从 `<COGNEE_REPO>/cognee/infrastructure/` 的 LanceDB adapter 和 Ch27 配置读取当前列名，再用固定查询集比较 recall@k、p95 和索引大小。

### Q25: 大图怎么 prune？

大图场景不要把 `prune` 理解为按低价值节点逐项修枝。当前 `cognee.prune.prune_system(...)` 会全局清空所选的图、向量、元数据或 cache；若只删除某个数据集或数据项，应使用 `cognee.datasets.empty_dataset()` 或 `delete_data()`。Ch12 的 Truth Subspace（真值子空间）用于检索重排，不是 prune 筛选器。

```python
import asyncio, cognee

async def main():
    # 先停写并备份，确认需要全局清空的派生存储
    await cognee.prune.prune_system(graph=True, vector=True, metadata=False, cache=True)

asyncio.run(main())
```

当前 v1.4.0 接口只有 `graph`、`vector`、`metadata`、`cache` 四个布尔开关，没有 dataset 或节点筛选参数；调用前运行 `python -c "import cognee; help(cognee.prune)"`。生产流程应先备份并停写，完成 prune 后全量 cognify 重建，再对关键问题做查询回归。

## 六、故障排查

### Q26: `cognify` 卡住怎么办？

先区分“仍在等待外部服务”和“pipeline 死锁/异常未上报”。Ch19 建议使用 CLI 的 `--debug`（全局选项须置于子命令前），Ch11 则通过 OpenTelemetry（开放遥测）trace 查看每个 pipeline stage 的开始、结束和异常；不要只看终端最后一行。

```bash
cognee --debug cognify
# 若通过服务运行，再检查日志和 trace exporter
```

按顺序检查 LLM/embedding endpoint、API key、网络超时、数据库连接池、输入文件是否无限大，以及 dataset 锁。用一条短文本重试；若短文本成功，再二分定位批次。生产应设置任务超时和可重试边界，避免无限重试把配额耗尽。

### Q27: 报 “Connection refused” 怎么办？

这通常意味着目标端口没有进程监听，或容器网络/地址写错，不是 Cognee 的搜索算法错误。Ch28 的 FastAPI 服务默认示例使用 8000 端口，先确认服务启动、绑定地址和 Docker 端口映射，再做健康检查。

```bash
curl -v http://127.0.0.1:8000/health
lsof -nP -iTCP:8000 -sTCP:LISTEN
cd <COGNEE_REPO>
docker compose ps
```

若客户端在容器内，`127.0.0.1` 指向客户端容器而非宿主机，应使用 Compose service name；若服务监听 `0.0.0.0` 但防火墙阻断，也会得到类似现象。修复后再检查 `/docs` 或一个只读 API 请求。

### Q28: Neo4j 连接失败怎么办？

Neo4j 连接失败通常来自 URI、密码、端口或容器网络不一致。Ch10 要求检查 `GRAPH_DATABASE_PROVIDER`、`GRAPH_DATABASE_URL`、`GRAPH_DATABASE_PASSWORD` 等配置，并确认 Cognee 实际选择了 Neo4j graph provider，而不是仍在使用默认 Kuzu。

```bash
export GRAPH_DATABASE_PROVIDER=neo4j
export GRAPH_DATABASE_URL=bolt://127.0.0.1:7687
export GRAPH_DATABASE_USERNAME=neo4j
export GRAPH_DATABASE_PASSWORD=<你的 Neo4j 密码>
python -c 'import os; print(os.getenv("GRAPH_DATABASE_URL"))'
```

随后检查 Neo4j 日志和端口：

```bash
nc -vz 127.0.0.1 7687
docker compose ps neo4j
docker compose logs --tail=80 neo4j
```

不要把浏览器 HTTP 地址 `http://...:7474` 当成 Bolt URI；也不要把真实密码提交到 shell history、仓库或日志。确认连接后先运行小数据集 cognify，再验证图查询。

## 索引：本 FAQ 涉及章节

- Q1 → Ch02
- Q2 → Ch02
- Q3 → Ch10
- Q4 → Ch02、Ch28
- Q5 → Ch02
- Q6 → Ch13、Ch14
- Q7 → Ch03、Ch08
- Q8 → Ch16
- Q9 → Ch03、Ch12
- Q10 → Ch24
- Q11 → Ch24
- Q12 → Ch15
- Q13 → Ch15
- Q14 → Ch15
- Q15 → Ch15
- Q16 → Ch15
- Q17 → Ch20
- Q18 → Ch20
- Q19 → Ch23
- Q20 → Ch23
- Q21 → Ch21
- Q22 → Ch26
- Q23 → Ch08、Ch27
- Q24 → Ch27
- Q25 → Ch12
- Q26 → Ch19、Ch11
- Q27 → Ch28
- Q28 → Ch10
