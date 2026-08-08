# 1.2 数据建模：向量列、HEAP 表、两类索引

> **一句话**：seekdb 的建模就是普通 MySQL 建表，外加三样东西——
> `VECTOR(n)` 列类型、`VECTOR INDEX` / `FULLTEXT INDEX` 两类索引、
> 以及可选的 `ORGANIZATION = HEAP` 表组织方式。

> 📌 本章所有 SQL 语法均摘自 `tools/deploy/mysql_test/test_suite/` 下的官方测试用例，
> 出处逐条标注。⚠️ 本书未实机执行。

---

## 向量列：`VECTOR(n)`

```sql
create table t1(
  c1 int,
  c2 int,
  c3 vector(3),
  primary key(c1)
);
```
*出处：`vector_index/t/vector_index_basic.test`*

`VECTOR(n)` 中的 `n` 是维度，建表时固定。在语法层面它属于一族"集合类型"
（`src/sql/parser/sql_parser_mysql_mode.y`）：

| 类型 | 说明 |
|---|---|
| `VECTOR(n)` | 稠密向量，最常用 |
| `SPARSEVECTOR` | 稀疏向量，配合 SPIV 索引 |
| `ARRAY(...)` | 数组 |
| `MAP(k, v)` | 映射 |

### 距离函数

| SQL 函数 | 语义 |
|---|---|
| `l2_distance(a, b)` | 欧氏距离 |
| `cosine_distance(a, b)` | 余弦距离 |
| `inner_product(a, b)` | 内积 |
| `l1_distance(a, b)` | 曼哈顿距离 |
| `vector_dims(v)` | 维度 |
| `vector_norm(v)` | 模长 |
| `vector_distance(a, b [, metric])` | 通用形式，`metric` ∈ `COSINE`/`DOT`/`EUCLIDEAN`/`MANHATTAN` |

实现在 `src/sql/engine/expr/ob_expr_vector.cpp`，
底层 SIMD 计算在 `src/storage/vector_type/`。

---

## 向量索引：`CREATE VECTOR INDEX`

真实语法（注意 README 里的 `LIB=vsag` 写法是大写，测试用例里用小写，都可以）：

```sql
-- HNSW，最常用
create vector index idx_hnsw1 on t1(c2) with (distance=l2, type=hnsw);

-- 显式指定底层库
create vector index cafe on t_vec(c3) with (distance=l2, type=hnsw, lib=vsag);

-- 内积距离
create vector index idx_2 on t_vec(c6) with (distance=inner_product, type=hnsw);

-- IVF 系列
create vector index idx_ivf_flat on t1(c3) with (distance=l2, type=ivf_flat);
create vector index idx_ivf_sq8  on t1(c4) with (distance=l2, type=ivf_sq8);
create vector index idx_ivf_pq   on t1(c5) with (distance=l2, type=ivf_pq, m=1);

-- 表达式索引也支持
create vector index idx_1 on t_vec((c1 + c2)) with (distance=l2, type=hnsw);
```
*出处：`vector_index/t/` 下的 `vector_index_basic.test`、`create_table_with_vector_index.test` 等*

### `WITH (...)` 里能写什么

参数解析在 `ObVectorIndexUtil::parser_params_from_string`
（`src/observer/vector_index/ob_vector_index_util.cpp`）。

**`type=` 支持的算法**（枚举 `ObVectorIndexAlgorithmType`）：

| 值 | 说明 |
|---|---|
| `hnsw` | 图索引，默认首选，召回率高 |
| `hnsw_sq` | HNSW + 标量量化，省内存 |
| `hnsw_bq` | HNSW + 二值量化，更省内存 |
| `hgraph` | 带附加信息时使用的图索引 |
| `ivf_flat` | 倒排 + 原始向量 |
| `ivf_sq8` | 倒排 + 8bit 标量量化 |
| `ivf_pq` | 倒排 + 乘积量化，需配 `m=` |
| `spiv` | 稀疏向量索引 |
| `ipivf` | 内积倒排 |

**`distance=` 支持的度量**（枚举 `ObVectorIndexDistAlgorithm`）：
`l2` / `inner_product` / `cosine`。

**`lib=`**：`vsag`（默认，走 `deps/oblib/src/lib/vector/ob_vsag_adaptor`）
或内置实现。

**其他常见参数**：`m`、`ef_construction`、`ef_search`（HNSW 调参），
`model` / `dim` / `sync_mode`（配合库内 embedding 使用）。

> 💡 **一个向量索引 ≠ 一张表。** HNSW 索引在底层会展开成 **5 张辅助表**
> （rowkey↔vid 映射、增量缓冲、索引元信息、快照数据）。
> 这正是两级索引架构的物理基础，详见
> [2.10 向量索引架构](../20-architect/10-vector-index.md)。

### 索引维护：`dbms_vector` 系统包

```sql
call dbms_vector.refresh_index('idx_hnsw1', 't1', 'c2', 1, 'FAST');
call dbms_vector.rebuild_index('new_idx_ivf_flat', 't1', 'c3', 0);
```
*出处：`vector_index/t/vector_index_basic.test`*

包定义在 `src/share/inner_table/sys_package/dbms_vector_mysql.sql`，
实现在 `src/pl/sys_package/ob_dbms_vector_mysql.cpp`。

---

## 全文索引：`FULLTEXT INDEX`

```sql
-- 建表时定义
create table articles (
  id int primary key,
  title varchar(200),
  body text,
  fulltext index idx_fts(body)
);

-- 后加，并指定分词器与分词器参数
alter table create_index_with_parser_properties
  add fulltext index fidx2(b)
  WITH PARSER ngram PARSER_PROPERTIES=(ngram_token_size=4);
```
*出处：`fts_index/t/` 下多个用例*

### 内置分词器

定义在 `src/storage/fts/`（X-macro `FTS_BUILD_IN_PARSER_LIST`）：

| 名称 | 实现文件 | 适用 |
|---|---|---|
| `space` | `ob_whitespace_ft_parser.cpp` | 按空白切分，英文 |
| `ngram` | `ob_ngram_ft_parser.cpp` | N-gram，中日韩通用 |
| `ngram2` | `ob_ngram2_ft_parser.cpp` | N-gram 改进版 |
| `beng` | `ob_beng_ft_parser.cpp` | 英文专用 |
| `ik` | `ob_ik_ft_parser.cpp` | 中文智能分词，支持用户词典 |

分词器参数（`ObFTParserProperty`）支持
`min_token_size`、`max_token_size`、`ngram_token_size`、
`stopword_table`、`dict_table`、`quantifier_table`。

### 检索

```sql
select * from create_index_with_parser_properties where match(a, b) against('2aa');
select * from articles where match(title, body) against('content article data');
```
*出处：`fts_index/t/`*

相关性打分用 BM25（`src/sql/engine/expr/ob_expr_bm25.cpp`）。

> ⚠️ 注意 `MATCH(a, b)` 的列顺序有意义——测试用例里专门有
> `MATCH(b,c)` 与 `MATCH(c,b)` 的对比（`fts_col_orders`）。

---

## HEAP 表：`ORGANIZATION = HEAP`

```sql
CREATE TABLE articles (
  id        INT PRIMARY KEY,
  content   TEXT,
  embedding VECTOR(384),
  FULLTEXT INDEX idx_fts (content) WITH PARSER ik,
  VECTOR   INDEX idx_vec (embedding) WITH (DISTANCE=l2, TYPE=hnsw, LIB=vsag)
) ORGANIZATION = HEAP;
```
*出处：`README.md`*

### 它在改什么

seekdb 表有两种组织方式（`ObTableOrganizationMode`，
`src/share/schema/ob_table_schema.h:197`）：

| 模式 | 含义 |
|---|---|
| `TOM_INDEX_ORGANIZED` (0) | 索引组织表，数据按主键有序存放（默认） |
| `TOM_HEAP_ORGANIZED` (1) | 堆表，数据按写入顺序堆放 |

选 HEAP 且没有显式主键时，seekdb 会**自动加一个隐藏主键 `__pk_increment`**
（`src/sql/resolver/ddl/ob_create_table_resolver.cpp:374-380`）。

### 为什么 AI 场景常用它

- AI 表（文档块、embedding）往往**没有天然主键**，强行造一个没意义
- 省掉主键 B+ 树的维护开销，写入更快
- 向量索引本来就用行 ID（`vid`）做映射，和堆表的隐藏自增主键天然契合

服务端默认可用 `default_table_organization` 参数配置
（`src/share/config/ob_server_config.h`）。

---

## 一个完整的建模示例

把上面几件事组合起来——这是 README 给出的典型 AI 表：

```sql
CREATE TABLE articles (
  id        INT PRIMARY KEY,
  title     TEXT,
  content   TEXT,
  embedding VECTOR(384),
  FULLTEXT INDEX idx_fts (content) WITH PARSER ik,
  VECTOR   INDEX idx_vec (embedding) WITH (DISTANCE=l2, TYPE=hnsw, LIB=vsag)
) ORGANIZATION = HEAP;
```

一张表同时具备：关系列、全文索引、向量索引。
下一章讲怎么用**一条 SQL** 同时查这三样。

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `src/sql/parser/sql_parser_mysql_mode.y` | `VECTOR(n)`、`SPARSEVECTOR`、`FULLTEXT`、`ORGANIZATION` 语法 |
| `src/sql/resolver/ddl/ob_create_index_resolver.cpp` | 识别 `VEC_KEY` 并分派 |
| `src/observer/vector_index/ob_vector_index_util.cpp` | `parser_params_from_string` 解析 `WITH (...)` |
| `src/observer/vector_index/ob_vector_index_util.h` | 算法/库/距离枚举定义 |
| `src/sql/resolver/ddl/ob_vec_index_builder_util.cpp` | `append_vec_args` 展开辅助表 |
| `src/sql/engine/expr/ob_expr_vector.cpp` | 距离函数表达式 |
| `src/storage/vector_type/` | SIMD 距离计算 |
| `src/storage/fts/` | 五种分词器 |
| `src/sql/engine/expr/ob_expr_bm25.cpp` | BM25 打分 |
| `src/share/schema/ob_table_schema.h:197` | `ObTableOrganizationMode` 枚举 |
| `src/sql/resolver/ddl/ob_create_table_resolver.cpp:374` | HEAP 表隐藏主键 |

---

## 动手验证

看真实可用的向量索引语法全集：

```bash
grep -rh "create vector index" tools/deploy/mysql_test/test_suite/vector_index/t/ \
  | grep -v '^#' | sed 's/^ *//' | sort -u
```

看支持哪些分词器：

```bash
grep -rn "FTS_BUILD_IN_PARSER_LIST" -A 12 src/storage/fts/ | head -20
```

看向量算法枚举：

```bash
grep -n "VIAT_\|VIDA_\|VIAL_" src/observer/vector_index/ob_vector_index_util.h | head -25
```

---

## 延伸阅读

- 下一章：[1.3 混合检索](03-hybrid-search.md)
- [2.10 向量索引架构](../20-architect/10-vector-index.md) —— 5 张辅助表到底怎么配合
- [2.12 混合检索的算子融合](../20-architect/12-hybrid-search-internals.md)
