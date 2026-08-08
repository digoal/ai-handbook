# Python 代码块静态扫描报告

扫描时间: 2026-07-26
扫描范围: `<HANDBOOK_REPO>/chapters/**/chapter-*.md` 中所有 ```` ```python ```` 代码块
扫描器: `<HANDBOOK_REPO>/code-review/scan_blocks.py`

---

## SUMMARY

总块数 **142** | 语法失败 **9 → 0** | 弯引号 **1 → 0** | A 严重错配 **9 → 0** | B 警告错配 **15**(未改,见 NOTES) | C 轻微 **3**(未修)

---

## BLOCK_STATS

- 章节文件数: 30
- 总代码块数: 142
- 语法解析成功(修复后): 142 / 142 (100%)
- Unicode 弯引号命中(修复后): 0
- A 严重已修: **9**
- B 警告已修: **0**(全部留待主会话裁决,见 NOTES)
- C 轻微未修: 3 处 `top_k=10`(默认偏差)

---

## DRIFTS_FIXED

### [A 严重] 弯引号

**chapters/part-03-api/chapter-17-custom-pipelines.md:343** —— 整段代码块大量使用 U+201C/U+201D 作为字符串定界符。
- 章节引述(节选): `if enable_steps.get(“prune_data”):` / `query_text=”Who has experience in design tools?”` / `asyncio.run(main(steps, [“Alice: Python, Spark”, …]))`
- 修复: 把 26 处 U+201C/U+201D 全部替换为 ASCII `"`,涉及 `“prune_data”` / `“prune_system”` / `“add_text”` / `“cognify”` / `“retriever”` / `query_text=…` / 字典字面量键名 / `asyncio.run(...)` 列表字面量。

### [A 严重] 语法失败(1)

**chapters/part-01-foundation/chapter-03-add-cognify-search.md:92** —— `default_tasks` 列表第 3、4 项存在 `positional argument follows keyword argument`。
- 章节引述:
  ```python
  Task(extract_graph_and_summarize, graph_model=KnowledgeGraph, ...),  # 3
  Task(add_data_points, embed_triplets=embed_triplets, ...),            # 4
  ```
  第一个调用 `extract_graph_and_summarize(data_chunks, graph_model, ...)` 的 `graph_model` 实际是位置参数,写成 `graph_model=KnowledgeGraph` 后再加位置 `...` 直接破语法。
- 修复:
  ```python
  Task(extract_graph_and_summarize, KnowledgeGraph, ...),              # 3
  Task(add_data_points, embed_triplets=embed_triplets),                  # 4
  ```
  顺带把第 4 项的尾随 `, ...` 删掉,使其语法干净。

### [A 严重] 语法失败(函数签名无 body)

下列 7 处代码块只展示函数签名/类型注解 + docstring,缺函数体,`ast.parse` 拒绝:

| 文件:行号 | 函数 |
|---|---|
| chapters/part-03-api/chapter-14-v2-memory-api.md:61 | `remember(...) -> Union["RememberResult", "DryRunEstimate"]:` |
| chapters/part-03-api/chapter-14-v2-memory-api.md:196 | `recall(...) -> list[RecallResponse]:` |
| chapters/part-03-api/chapter-14-v2-memory-api.md:323 | `improve(...):` |
| chapters/part-03-api/chapter-14-v2-memory-api.md:403 | `forget(...) -> dict:` |
| chapters/part-03-api/chapter-14-v2-memory-api.md:589 | 决策树伪代码 |
| chapters/part-03-api/chapter-16-memify.md:33 | `memify(...):` |
| chapters/part-05-production/chapter-29-frontend-ui.md:312 | `get_memory_provenance_graph(...)` / `visualize_memory_provenance(...)` |

- 修复方式(4 处 v2 签名 + memify): 在闭合 `:` 后追加一行 `    pass  # 源码位置 <COGNEE_REPO>/...,签名节选`,保持节选意图。
- 修复方式(决策树伪代码 chapter-14:589): 把 5 行伪代码 `use v2` / `use v1` 改成可解析的 `api = "v2"` / `api = "v1"`,原注释保持不变。
- 修复方式(chapter-29:312): 两个函数都补 `pass`。`visualize_memory_provenance(...)` 改成 `(*args, **kwargs)` 因为 ast 不能接受 `...` 作为参数名(它会被识别为 Ellipsis 字面量)。

---

## DEFERRED_TO_MAIN

### [B 警告] `dataset_name=` 出现在 15 处 Python 代码块

| 文件:行号 | 上下文 |
|---|---|
| chapters/part-01-foundation/chapter-01-why-memory.md:77 | cognee.add(..., dataset_name="langchain_intro") |
| chapters/part-01-foundation/chapter-01-why-memory.md:201 | cognee.add([...], dataset_name=...) |
| chapters/part-01-foundation/chapter-03-add-cognify-search.md:72 | cognee.add([...], dataset_name=...) |
| chapters/part-01-foundation/chapter-03-add-cognify-search.md:258 | cognee.add([...], dataset_name=...) |
| chapters/part-01-foundation/chapter-04-core-concepts.md:51 | cognee.add(..., dataset_name="ecl_overview") |
| chapters/part-02-architecture/chapter-12-graph-governance.md:130 | cognee.add([...], dataset_name=dataset) |
| chapters/part-02-architecture/chapter-12-graph-governance.md:135 | cognee.add([...], dataset_name=dataset) |
| chapters/part-03-api/chapter-13-v1-api.md:72 | cognee.add(data=[...], dataset_name="agent_arch_research") |
| chapters/part-03-api/chapter-13-v1-api.md:85 | cognee.add(data=[...], dataset_name=...) |
| chapters/part-03-api/chapter-13-v1-api.md:102 | cognee.add("fastapi 长文...", dataset_name=...) |
| chapters/part-03-api/chapter-17-custom-pipelines.md:72 | cognee.add("...", dataset_name=...) |
| chapters/part-05-production/chapter-24-config-datasets.md:165 | cognee.add("SRE 团队...", dataset_name="sre_payments") |
| chapters/part-05-production/chapter-24-config-datasets.md:259 | cognee.add("退款规则...", dataset_name="support_refunds") |
| chapters/part-05-production/chapter-27-performance-cache.md:190 | cognee.add([...], dataset_name=dataset) |
| chapters/part-05-production/chapter-27-performance-cache.md:244 | cognee.add(documents, dataset_name=dataset) |

**未改原因(实测 API 与规则表冲突)**:
我对当前安装的 cognee 1.4.0 (`<COGNEE_REPO>/cognee/api/v1/add/add.py:35`) 做了 `inspect.signature(cognee.add)` 验证,实际签名为 `(data, dataset_name='main_dataset', user=None, ...)` —— **`dataset_name=` 才是正确参数名**,没有 `dataset=` 这个参数。如果按本任务给的 B-表把全部 `dataset_name=` 改成 `dataset=`,15 处代码块都会在运行期抛 `TypeError: add() got an unexpected keyword argument 'dataset'`。

请主会话裁决:
- 选项 A: 维持 `dataset_name=`,因为它就是当前 cognee 1.4 v1 API 的真名;把任务规则表里这一行修正掉(或者删除此条)。
- 选项 B: 如果项目预期升级到未来使用 `dataset=` 的 v2 API,把 15 处改成 `dataset=` 并同步升级 cognee 依赖。

### [C 轻微] `top_k=10` 出现在 3 处(默认值偏差,未修)

| 文件:行号 |
|---|
| chapters/part-01-foundation/chapter-03-add-cognify-search.md:172 |
| chapters/part-01-foundation/chapter-03-add-cognify-search.md:275 |
| chapters/part-03-api/chapter-13-v1-api.md:297 |

实际 `cognee.search` 默认 `top_k=15`(已在 search.py:39 验证)。这些示例用 `top_k=10` 是为了演示"显式覆盖默认值",属于 C 轻微风格项,本次不动。

---

## NOTES

1. **协议层误判**: 我最初的扫描器把整个文件出现 `curl/shell/fetch` 即视为 HTTP 层,导致 chapter-12/13/17/24 里 9 个明显是 Python 的代码块被标成 ctx=http。复核后这些块内都是 `async def` / `await cognee.*`,无歧义。规则"整文件含 shell 关键字 → 整文件 HTTP 层"太粗;建议改用块级判断(块内是否有 `import asyncio` / `await`)。

2. **API 形态表正确性核对**:
   - `cognee.search(query_text=..., query_type=SearchType.X)` —— **正确**,所有现存示例都用此形式(大多数还是位置参数)。
   - `cognee.search(query="...")` / `cognee.search(search_type=...)` —— **未发现**;无需修。
   - `cognee.prune()` bare call —— 仅在 chapter-12-graph-governance.md:192 的**散文警告**里出现(`不要写成 await cognee.prune()`),代码块内**未发现**。已无需修。
   - `cognee.prune.prune_data()` / `cognee.prune.prune_system()` —— **正确**,所有现存示例都用此形式。验证:`<COGNEE_REPO>/cognee/api/v1/prune/prune.py` 把 `prune` 定义为一个 `class prune`,含两个 `@staticmethod`,所以 `cognee.prune()` 是 instantiate 不是执行,确实不可 await。
   - `cognee.add(data, dataset_name=...)` —— **正确**;`dataset=` 不存在(见上方 NOTES 末段)。
   - `cognee.visualize_graph(query=...)` —— **正确**,`cognee.visualize_graph` 的 `query` 参数确实存在,与 `cognee.search` 用的 `query_text` 不冲突。chapter-13-v1-api.md:427 / chapter-09-retrievers.md:246/248/253 的 `query=` 都是合法用法,误报。

3. **章节签名节选惯例**: chapter-14 / chapter-16 / chapter-29 大量使用 "只展示签名 + docstring,正文省略"的写法,导致 ast.parse 失败。本次统一用 `pass  # 源码位置 ...` 兜底,读者一眼能看出是节选。如果未来要做 lint 校验,建议在文档风格指南里把这条规范化,比如推荐 `...`(Ellipsis) 而不是 `pass`,但目前 ast 对 async def + 类型注解的 `...` 形式也接受。

4. **chapter-14-v2-memory-api.md:589 的 "use v2"**: 这是文档明确标记的 `### 14.8.2 选型伪代码`,本来意图是流程图式伪代码。改成 `api = "v2"` / `api = "v1"` 是为了让它能过 ast,变量名 `api` 与上文表格列名保持一致,语义清晰可读。如果作者有更优雅的写法(比如 `selected_api: str = ...`),可以替换。

5. **chapter-17-custom-pipelines.md 的弯引号密度极高**: 一个 30 行块里出现 26 处 U+201C/U+201D。修复后整段用标准 ASCII 双引号,中文文本内容(块外的散文部分,如 `这里的"动态分支"`)保持原样,只动了 Python 代码块内部。

6. **未触达的项目**:
   - `<HANDBOOK_REPO>/cognee/`、`<HANDBOOK_REPO>/cognee-integrations/`、`<HANDBOOK_REPO>/appendix/`、`<HANDBOOK_REPO>/diagrams/`、`<HANDBOOK_REPO>/templates/`、`<HANDBOOK_REPO>/dist/` 均未修改。
   - 章节文件改动严格限定在 Python 代码块内的 A 严重错配处,正文 / 表格 / 标题 / 链接全部保持不变。