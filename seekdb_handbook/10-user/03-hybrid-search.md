# 1.3 混合检索：一条 SQL 打通向量 + 全文 + 标量

> **一句话**：向量相似度、全文匹配、标量过滤在同一个执行计划里完成，
> 不需要客户端做 N+1 合并。

![混合检索](../assets/hybrid-search.svg)

---

## 问题：为什么"分别查再合并"不够好

典型 RAG 检索要同时满足三个条件：语义相近、包含关键词、符合业务过滤。
如果向量存在 Milvus、全文在 Elasticsearch、业务数据在 MySQL，你要写这样的胶水：

```
1. 去向量库查 top-100 语义相近的 id
2. 去搜索引擎查匹配关键词的 id
3. 回 MySQL 按 id 捞出来，再过滤 author_id / created_at
4. 客户端合并、重排、截断
```

问题不只是慢。更麻烦的是**召回率不可控**：
第 1 步取 top-100，但过滤完可能只剩 3 条；想要 10 条就得反复放大 K 值重试。

seekdb 的答案是把这三件事放进一个执行计划，让优化器决定过滤和召回的顺序。

---

## 写法一：直接写 SQL

```sql
SELECT id, title, l2_distance(emb, '[0.12,0.34,...]') AS dist
FROM docs
WHERE MATCH(content) AGAINST('quarterly report')
  AND author_id = 42
  AND created_at > '2026-01-01'
ORDER BY dist APPROXIMATE LIMIT 10;
```
*出处：`README.md`。⚠️ 未实机验证。*

三个关键字各司其职：

| 成分 | 作用 |
|---|---|
| `MATCH(content) AGAINST(...)` | 全文召回，BM25 打分 |
| `author_id = 42 AND created_at > ...` | 标量过滤，下推到扫描 |
| `ORDER BY dist APPROXIMATE LIMIT 10` | 向量近似最近邻（ANN） |

### `APPROXIMATE` 是整条语句的开关

这个关键字才是"走不走向量索引"的分水岭：

- **写了** `APPROXIMATE` → 走 ANN 索引，近似结果，快
- **不写** → 暴力精确计算，全表算距离，慢但精确

语法上它是 `SELECT` 的一个独立槽位
（`PARSE_SELECT_APPROX`，`src/sql/parser/parse_node.h`），
解析入口是 `ObSelectResolver::resolve_approx_clause`
（`src/sql/resolver/dml/ob_select_resolver.cpp` 约 998 行）。
`APPROX` 和 `APPROXIMATE` 两种拼写等价。

> ⚠️ **限制**：`FOR UPDATE` 不能和 `APPROXIMATE` 一起用，
> resolver 里会直接报错（`ob_select_resolver.cpp` 约 1280 行）。

### 优化器如何安排"过滤"与"召回"的先后

这是混合检索最关键的一个决策，seekdb 定义了 5 种执行策略
（`ObVecIndexType`，`src/sql/das/ob_das_vec_define.h`）：

| 策略 | 含义 | 适用 |
|---|---|---|
| `VEC_INDEX_POST_WITHOUT_FILTER` | 纯 ANN，无过滤 | 没有标量条件 |
| `VEC_INDEX_PRE` | 先过滤，再在结果里算距离 | 过滤选择性极高（命中很少） |
| `VEC_INDEX_POST_ITERATIVE_FILTER` | 先 ANN 取一批，过滤，不够再取 | 过滤中等选择性 |
| `VEC_INDEX_ADAPTIVE_SCAN` | 运行时自适应 | 选择性未知 |

这解决了前面说的"取 top-100 过滤完只剩 3 条"的问题——
迭代式过滤会自动补足，不用你在客户端调 K 值。

代价估算在 `src/sql/optimizer/ob_opt_est_cost_model.cpp`。

---

## 写法二：`dbms_hybrid_vector.SEARCH` 的 JSON DSL

如果你更习惯 Elasticsearch 风格的查询 DSL，seekdb 提供了系统包：

```sql
-- 直接执行并返回 JSON 结果
SELECT dbms_hybrid_vector.SEARCH('docs', '<查询 JSON>');

-- 只要翻译出来的 SQL，不执行（调试神器）
SELECT dbms_hybrid_vector.GET_SQL('docs', '<查询 JSON>');
```

包声明在 `src/share/inner_table/sys_package/dbms_hybrid_vector_mysql.sql`，
实现链路是：

```
ObESQueryParser  解析 JSON DSL       src/sql/hybrid_search/ob_query_parse.cpp
      ↓
ObQueryReqFromJson  请求中间表示      src/sql/hybrid_search/ob_query_request.h
      ↓
ObQueryTranslator  翻译成单条 SQL     src/sql/hybrid_search/ob_query_translator.cpp
      ↓
ObHybridSearchExecutor  执行          src/sql/hybrid_search/ob_hybrid_search_executor.cpp
```

> 💡 `GET_SQL` 非常有用：它让你看到 DSL 到底被翻译成了什么 SQL，
> 便于理解和调优。

### 融合算法

两路召回（向量 + 全文）的结果需要融合成一个排序。
seekdb 支持两种（`ObFusionMethod`，`src/sql/hybrid_search/ob_query_parse.h`）：

| 方法 | 说明 |
|---|---|
| `WEIGHT_SUM` | 加权求和，给两路分数各配权重 |
| `RRF` | Reciprocal Rank Fusion，按**排名**而非分数融合，配 `rank_const` |

RRF 的好处是不用担心两路分数量纲不一致——
BM25 分数和向量距离本来就不在一个尺度上。

融合过程中可用的内部列（`is_inner_column` 白名单）：

| 列名 | 含义 |
|---|---|
| `_keyword_score` | 全文相关性分数 |
| `_semantic_score` | 向量相似度分数 |
| `_keyword_rank` | 全文召回排名 |
| `_semantic_rank` | 向量召回排名 |

---

## 底层发生了什么

一次混合检索会启动两类迭代器，在同一个计划里并行推进：

| 召回路 | 迭代器 | 位置 |
|---|---|---|
| 向量 | `ObDASHNSWScanIter`（或 IVF 系列） | `src/sql/das/iter/ob_das_hnsw_scan_iter.h` |
| 全文 | `ObDASTRMergeIter` / `ObDASMatchIter` | `src/sql/das/iter/sparse_retrieval/` |

全文侧用了检索领域的标准优化：
DAAT（Document-at-a-Time）、TAAT（Term-at-a-Time）、
以及 block-max 剪枝（`ObBlockMaxScoreIter`，`src/storage/retrieval/ob_block_max_iter.cpp`）。

向量侧的 `ObDASHNSWScanIter` 内部是个状态机，
要同时查增量索引和快照索引再归并——那是
[2.10](../20-architect/10-vector-index.md) 和
[2.12](../20-architect/12-hybrid-search-internals.md) 的主题。

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `src/sql/parser/sql_parser_mysql_mode.y` | `opt_approx` → `T_APPROX`；`MATCH ... AGAINST` |
| `src/sql/parser/parse_node.h` | `PARSE_SELECT_APPROX` 槽位 |
| `src/sql/resolver/dml/ob_select_resolver.cpp` | `resolve_approx_clause`（约 998 行） |
| `src/sql/das/ob_das_vec_define.h` | `ObVecIndexType` 五种执行策略 |
| `src/sql/das/iter/ob_das_hnsw_scan_iter.h` | HNSW 查询迭代器 |
| `src/sql/das/iter/sparse_retrieval/ob_das_tr_merge_iter.h` | 全文归并迭代器 |
| `src/sql/hybrid_search/ob_query_parse.cpp` | JSON DSL 解析、`ObFusionMethod` |
| `src/sql/hybrid_search/ob_query_translator.cpp` | DSL → SQL 翻译 |
| `src/sql/hybrid_search/ob_hybrid_search_executor.cpp` | `SEARCH` / `GET_SQL` |
| `src/storage/retrieval/ob_block_max_iter.cpp` | block-max 剪枝 |
| `src/sql/engine/expr/ob_expr_bm25.cpp` | BM25 打分 |
| `src/sql/optimizer/ob_opt_est_cost_model.cpp` | 向量扫描代价估算 |

---

## 动手验证

看 `APPROXIMATE` 在语法里的定义：

```bash
grep -n "APPROX" src/sql/parser/sql_parser_mysql_mode.y | head
```

看五种向量执行策略：

```bash
grep -n "VEC_INDEX_PRE\|VEC_INDEX_POST\|VEC_INDEX_ADAPTIVE" src/sql/das/ob_das_vec_define.h
```

看融合方法与内部列白名单：

```bash
grep -n "WEIGHT_SUM\|RRF\|_keyword_score\|_semantic_score" src/sql/hybrid_search/ob_query_parse.h
```

看官方全文检索用例怎么写：

```bash
ls tools/deploy/mysql_test/test_suite/fts_index/t/
```

---

## 延伸阅读

- 下一章：[1.4 FORK / MERGE 沙箱](04-fork-merge.md)
- [2.12 混合检索的算子融合](../20-architect/12-hybrid-search-internals.md) —— 内部实现
- [1.5 库内 AI 函数](05-in-db-ai.md) —— 用 `AI_RERANK` 对结果重排
