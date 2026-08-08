# 1.5 库内 AI：AI_EMBED / AI_COMPLETE / AI_RERANK / AI_PROMPT

> **一句话**：seekdb 能在 SQL 里直接调用外部大模型——注册模型、注册 endpoint，
> 然后像普通函数一样 `SELECT AI_EMBED('my_model', content) FROM docs`。

![AI Service 架构](../assets/ai-service.svg)

> 📌 **这是本书唯一一个 README 完全没有提及的重大能力。**
> 如果你只读官方 README，你不会知道 seekdb 能做这件事。

---

## 为什么有意义

典型 RAG 流程里，向量化这一步通常在应用侧：

```
应用读数据 → 调 embedding API → 拿到向量 → 写回数据库
```

数据要往返一圈。库内 AI 把这一步下沉：

```sql
INSERT INTO docs(content, embedding)
SELECT content, AI_EMBED('my_embedding_model', content) FROM staging;
```

数据不出库。对于批量向量化、增量补齐 embedding、
或者在查询时做 rerank，这能省掉大量胶水代码。

---

## 四个函数

实现在 `src/sql/engine/expr/ob_expr_ai/`，都继承自 `ObFuncExprOperator`：

| 函数 | 类 | 用途 |
|---|---|---|
| `AI_EMBED(model, content [, dim])` | `ObExprAIEmbed` | 生成稠密向量 |
| `AI_COMPLETE(...)` | `ObExprAIComplete` | 文本补全 / 对话 |
| `AI_RERANK(...)` | `ObExprAIRerank` | 对候选结果重排 |
| `AI_PROMPT(template, args...)` | `ObExprAIPrompt` | 模板化提示词拼装 |

### `AI_EMBED` 的签名细节

从 `ObExprAIEmbed::calc_result_typeN`（`ob_expr_ai_embed.cpp:43`）可以读出精确约束：

- **参数个数**：2 或 3，否则报 `OB_ERR_PARAM_SIZE`
- **参数 0**（模型名）：转成 `VARCHAR`，字符集 `utf8mb4_bin`
- **参数 1**（内容）：同上
- **参数 2**（维度，可选）：必须是**整数**，浮点会报错
  （错误信息原文：`ai_embed, dimension parameter must be an integer, not a decimal or float`）
- **返回值**：`VARCHAR`

维度参数会被包装成 JSON `{"dimensions": n}` 传给模型服务——
这对应 OpenAI embedding API 的 `dimensions` 参数。

### `AI_PROMPT` 的实际行为

这个函数有官方测试覆盖（`ai_function/t/ai_prompt.test`），
所以约束最清楚：

```sql
-- 正确
select ai_prompt('{0}+{1}={2} 吗？请回答true或false','1');

-- 无参数 → 报错 1582
select ai_prompt();

-- 类型错误 → 报错 5083（只接受字符串类型）
select ai_prompt(1);
select ai_prompt(1.2);
select ai_prompt(json_object("a","1"));

-- 可以作用在表列上
select ai_prompt(nr) from t1;   -- char/varchar/binary/varbinary 都行
```

测试注释写得很明确：

> 支持任意数量的输入，要求都是 varchar 长度内的字符串，
> 不支持其他类型，不允许输入 null

`text` / `blob` 类型**不支持**。

---

## 用之前：注册模型和 endpoint

AI 函数不能凭空调用，得先告诉数据库"模型在哪、怎么连"。
这是两步，通过 `DBMS_AI_SERVICE` 系统包完成。

以下语法全部来自官方测试用例
`tools/deploy/mysql_test/test_suite/ai_function/t/ai_model_endpoint_ddl.test`。

### 第一步：注册模型

```sql
call DBMS_AI_SERVICE.CREATE_AI_MODEL(
  'my_ai_model_1', '{
    "type": "dense_embedding",
    "model_name": "text-embedding-v1"
  }');
```

`type` 的取值对应 `EndpointType::TYPE` 枚举
（`src/share/ai_service/ob_ai_model_info.h`）：

| `type` 值 | 枚举 | 配套函数 |
|---|---|---|
| `dense_embedding` | `DENSE_EMBEDDING = 1` | `AI_EMBED` |
| `sparse_embedding` | `SPARSE_EMBEDDING = 2` | 稀疏向量场景 |
| `completion` | `COMPLETION = 3` | `AI_COMPLETE` / `AI_PROMPT` |
| `rerank` | `RERANK = 4` | `AI_RERANK` |

查看已注册的模型：

```sql
select NAME, TYPE, MODEL_NAME from oceanbase.DBA_OB_AI_MODELS where NAME = 'my_ai_model_1';
```

### 第二步：注册 endpoint（连接信息）

```sql
call DBMS_AI_SERVICE.CREATE_AI_MODEL_ENDPOINT (
  'my_model_endpoint1', '{
    "ai_model_name": "my_model1",
    "url": "https://api.example.com/v1/embeddings",
    "access_key": "sk-xxxxxxxxxxxx",
    "request_model_name": "text-embedding-v2",
    "provider": "openai"
  }');
```

字段含义：

| 字段 | 说明 |
|---|---|
| `ai_model_name` | 关联到第一步注册的模型名 |
| `url` | 模型服务的 HTTP 地址 |
| `access_key` | API Key |
| `request_model_name` | 实际发给服务方的模型名（可与本地别名不同） |
| `provider` | 协议方言，如 `openai` |

查看 endpoint：

```sql
select ENDPOINT_NAME, AI_MODEL_NAME, SCOPE, URL, PROVIDER,
       REQUEST_MODEL_NAME, PARAMETERS,
       REQUEST_TRANSFORM_FN, RESPONSE_TRANSFORM_FN
from oceanbase.DBA_OB_AI_MODEL_ENDPOINTS
where ENDPOINT_NAME = 'my_model_endpoint1';
```

> 💡 `REQUEST_TRANSFORM_FN` / `RESPONSE_TRANSFORM_FN` 两个字段说明
> seekdb 预留了请求/响应改写钩子——用来适配非标准协议的模型服务。

### 清理

```sql
call DBMS_AI_SERVICE.DROP_AI_MODEL_ENDPOINT('my_model_endpoint1');
call DBMS_AI_SERVICE.DROP_AI_MODEL('my_model1');
```

### 相关错误码

从测试用例的 `--error` 标注可以反推：

| 错误码 | 含义 |
|---|---|
| 11112 | endpoint 不存在 |
| 11113 | endpoint 参数非法 |
| 11118 | 模型不存在 |
| 1582 | 函数参数个数错误 |
| 5083 | 函数参数类型错误 |

---

## 底层怎么发请求

调用链（详见 [2.14](../20-architect/14-ai-service.md)）：

```
ObExprAIEmbed::eval_ai_embed          表达式求值
  → ObAIFuncUtils::get_ai_func_info   取模型元信息
  → omt::ObAiService / ObAiServiceGuard  从缓存拿 endpoint
  → ObAIFuncModel::call_dense_embedding
  → ObAIFuncClient::send_post          libcurl 发 HTTP
  → 外部模型服务
```

`ObAIFuncClient`（`src/sql/engine/expr/ob_expr_ai/ob_ai_func_client.cpp`）
的默认行为值得知道：

| 行为 | 默认值 | 来源 |
|---|---|---|
| 重试次数 | 3 | `max_retry_times_ = 3` |
| 超时 | 60 秒 | `timeout_sec_ = 60` |
| 批量 | 支持 | `send_post_batch` / `send_post_batch_no_wait`（curl multi） |

> ⚠️ **性能与稳定性提醒**：AI 函数会在 SQL 执行过程中发起**同步 HTTP 请求**。
> 一条扫描 100 万行的 `SELECT AI_EMBED(...)` 意味着大量外部调用，
> 受限于模型服务的 QPS 和延迟。生产使用务必：
> - 用 `LIMIT` / 分批处理控制规模
> - 关注 60 秒超时是否够用
> - 考虑用生成列 + 异步刷新代替实时调用

另外，源码里有一处 `TODO` 值得留意
（`ob_expr_ai_embed.cpp:159`）：

```cpp
// TODO: support schema version match in plan cache for ai func
```

即 AI 函数与计划缓存的 schema 版本匹配尚未完成，相关代码段被注释掉了。

---

## 另一条路：库内 embedding 自动生成

除了显式调用 `AI_EMBED`，seekdb 还支持在**建索引时**指定模型，
让引擎自动为新写入的行生成向量：

```sql
create vector index vec_idx1 on t_vec(c2)
  with (distance=l2, type=hnsw, model=ob_embed, dim=1024, sync_mode=immediate);
```
*出处：`vector_index/t/` 用例（该行在测试中被注释，说明依赖外部模型服务，CI 里不跑）*

对应实现是 `ObEmbeddingTask`
（`src/observer/vector_index/ob_vector_embedding_handler.cpp`），
内部是个阶段状态机：`INIT → HTTP_SENT → HTTP_COMPLETED → PARSED → DONE`。

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:43` | `AI_EMBED` 参数校验 |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:78` | `eval_ai_embed` 求值主逻辑 |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_complete.cpp` | `ObExprAIComplete` |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_rerank.cpp` | `ObExprAIRerank` |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_prompt.cpp` | `ObExprAIPrompt` |
| `src/sql/engine/expr/ob_expr_ai/ob_ai_func.h:34` | `ObAIFuncExprInfo`、四个接口基类 |
| `src/sql/engine/expr/ob_expr_ai/ob_ai_func_client.h:28` | `ObAIFuncClient`（libcurl） |
| `src/sql/engine/expr/ob_expr_ai/ob_ai_func_client.cpp:25` | 重试 3 次 / 超时 60s |
| `src/observer/ai_service/ob_ai_service_executor.h:34` | endpoint 增删改查 |
| `src/share/ai_service/ob_ai_model_info.h` | `EndpointType` 四种类型 |
| `src/observer/omt/ob_ai_service.cpp` | endpoint 运行时缓存 |
| `src/pl/sys_package/ob_dbms_ai_service.cpp` | `DBMS_AI_SERVICE` 包实现 |
| `src/share/inner_table/sys_package/dbms_ai_service_mysql.sql` | 包声明 |
| `src/observer/vector_index/ob_vector_embedding_handler.cpp` | 索引侧自动 embedding |

---

## 动手验证

看四个 AI 函数的实现文件：

```bash
ls src/sql/engine/expr/ob_expr_ai/
```

看 endpoint 类型枚举：

```bash
grep -n -A 10 "struct EndpointType" src/share/ai_service/ob_ai_model_info.h
```

看官方注册语法（最权威的用法参考）：

```bash
sed -n '1,60p' tools/deploy/mysql_test/test_suite/ai_function/t/ai_model_endpoint_ddl.test
```

看 HTTP 客户端的重试与超时默认值：

```bash
sed -n '25,35p' src/sql/engine/expr/ob_expr_ai/ob_ai_func_client.cpp
```

---

## 延伸阅读

- 下一章：[1.6 生态集成](06-ecosystem.md)
- [2.14 库内 AI Service 架构](../20-architect/14-ai-service.md) —— 完整调用链与缓存设计
- [1.3 混合检索](03-hybrid-search.md) —— 用 `AI_RERANK` 给混合检索结果重排
