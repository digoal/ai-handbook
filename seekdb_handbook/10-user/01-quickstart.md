# 1.1 30 秒上手

> **一句话**：四条安装路径任选其一；Python 用户 `pip install pyseekdb` 后三行代码就能跑起来。

---

## 先选一条路

| 路径 | 适合谁 | 代价 |
|---|---|---|
| **Python SDK** | AI / ML 开发者，想立刻写代码 | 需要 Python 环境 |
| **Docker** | 想快速试一下完整 server | 需要 Docker |
| **二进制包** | 要装到主机上长期跑 | 需要匹配的 OS |
| **Cloud** | 什么都不想装 | 免费 7 天 |

以下命令均来自仓库 `README.md`。⚠️ 本书写作时未实机执行，请以官方文档为准。

---

## 路径一：Python SDK（推荐给 AI 开发者）

```bash
pip install -U pyseekdb
```

`pyseekdb` 是 seekdb 的 Python SDK，**不在本仓库内**，
源码在 [github.com/oceanbase/pyseekdb](https://github.com/oceanbase/pyseekdb)。

最小可用示例（来源：`images/demo.py`，仓库自带的演示脚本）：

```python
import pyseekdb

client = pyseekdb.Client(path="./agent_state.db")
memory = client.get_or_create_collection(name="episodic")

memory.upsert(
    ids=["1", "2", "3"],
    documents=[
        "user prefers dark mode",
        "user speaks English and Chinese",
        "user timezone is UTC+8",
    ],
)
memory.refresh_index()

results = memory.query(query_texts="ui preferences?", n_results=2)
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  {doc}  (distance: {dist:.4f})")
```

注意这里**没有**建表、没有定义 schema、没有配置 embedding 模型——
这是 SDK 层做的封装。等你需要精细控制时，再落到 SQL（见 [1.2 数据建模](02-data-modeling.md)）。

> 💡 `memory.refresh_index()` 这一行值得留意。它对应 seekdb 的**异步索引**设计：
> 写入提交后索引是异步构建的，`refresh_index` 用来确保索引已追上。
> 背后的机制见 [2.11 Change Stream](../20-architect/11-change-stream.md)。

---

## 路径二：Docker

```bash
docker run -d \
  --name seekdb \
  -p 2881:2881 \
  -p 2886:2886 \
  -v ./data:/var/lib/oceanbase \
  oceanbase/seekdb:latest
```

> ⚠️ README 映射的是 `2881` 和 `2886`。而源码里
> `src/share/parameter/ob_parameter_seed.ipp` 的默认值是
> `mysql_port = 2881`、`rpc_port = 2882`。`2886` 应是该镜像的额外约定，
> 详见[镜像文档](https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md)。

连接：

```bash
mysql -h127.0.0.1 -P2881 -uroot
```

---

## 路径三：二进制安装

```bash
# Linux 一键安装（可能需要 sudo）
curl -fsSL https://obportal.s3.ap-southeast-1.amazonaws.com/download-center/opensource/seekdb/seekdb_install.sh | bash

# macOS
brew tap oceanbase/seekdb
brew install seekdb
```

macOS 安装后会带一套管理工具（源码在 `tools/macpkg/`）：

```bash
seekdb_start      # 启动
seekdb_status     # 查看状态
seekdb_paths      # 看安装路径
seekdb_stop       # 停止
```

底层是 `seekdbctl` 脚本 + launchd 守护 + 一个菜单栏 App。
默认安装到 `/opt/seekdb`，详见 [1.7 部署与配置](07-deploy-config.md)。

---

## 路径四：Cloud（零安装）

```bash
curl -X POST https://d0.seekdb.ai/api/v1/instances
```

免费 7 天，无需注册。

---

## 路径五：从源码构建（开发者）

如果你要改代码，见 [3.1 环境与构建](../30-developer/01-build.md)。简版：

```bash
git clone https://github.com/oceanbase/seekdb.git
cd seekdb
bash build.sh debug --init --make
mkdir -p ~/seekdb/bin
cp build_debug/src/observer/seekdb ~/seekdb/bin
cd ~/seekdb && ./bin/seekdb
```

> ⚠️ 首次构建会下载全部第三方依赖并编译约 281 万行 C++，
> 耗时以**小时**计，磁盘占用可观。别在赶时间的时候做这件事。

---

## 第一条 SQL

连上之后，验证向量能力是否可用。以下语法取自官方测试用例
`tools/deploy/mysql_test/test_suite/vector_index/t/vector_index_basic.test`：

```sql
create table t1(
  c1 int,
  c2 int,
  c3 vector(3),
  primary key(c1)
);

create vector index idx_ivf_flat on t1(c3) with (distance=l2, type=ivf_flat);
```

查看索引确实被展开成了辅助表（这条也来自同一个测试用例）：

```sql
select table_name from oceanbase.__all_table where table_name like "%idx_ivf%";
```

你会看到形如 `__idx_<id>_...` 的内部表——一个向量索引在底层对应**多张**辅助表。
为什么这样设计，见 [2.10 向量索引架构](../20-architect/10-vector-index.md)。

---

## 代码锚点

| 位置 | 职责 |
|---|---|
| `images/demo.py` | 仓库自带的 Python 演示脚本 |
| `README.md` | 四种安装方式的官方说明 |
| `src/share/parameter/ob_parameter_seed.ipp` | `mysql_port` / `rpc_port` 默认值 |
| `tools/macpkg/seekdbctl/seekdbctl` | macOS 管理脚本（726 行 bash） |
| `tools/deploy/mysql_test/test_suite/vector_index/t/vector_index_basic.test` | 向量索引基础用例，本章 SQL 出处 |
| `docs/developer-guide/en/build-and-run.md` | 官方构建与运行指南 |

---

## 动手验证

看仓库里真实可用的向量索引语法（不看 README 的营销示例，看测试用例）：

```bash
grep -h "create vector index" -r tools/deploy/mysql_test/test_suite/vector_index/t/ | sort -u | head -20
```

看官方默认端口：

```bash
grep -n "mysql_port\|rpc_port" src/share/parameter/ob_parameter_seed.ipp | head
```

---

## 延伸阅读

- 下一章：[1.2 数据建模](02-data-modeling.md)
- [0.2 三种形态](../00-orientation/02-three-modes.md) —— 嵌入式和 server 有什么区别
- [3.1 环境与构建](../30-developer/01-build.md) —— 从源码构建的完整流程
