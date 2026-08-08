# M12 · 附录 / SVG / 示例代码 fact-check 收尾报告

> 工作目录:`<HANDBOOK_REPO>`
> 代码基线:cognee v1.4.0 + cognee-integrations
> 基线日期:2026-07-26
> 验证日期:2026-07-26

## 总览

M11 完成后,按 `fact-check-report.md` 列出的 4 项"边界外"待办 + "已知遗留" 的 3 项做收尾:**3 个 general-purpose subagent 并行**完成。

| 维度 | 结果 |
|---|---|
| 并行 subagent 数 | **3**(同时启动,同步等待) |
| 附录 fact-check(2 文件) | 16 drift 发现并全部修复 |
| SVG 资源核对(38 资源) | **零差集**(38=38)+ 章号-文件名 100% 对齐,**零修改** |
| 示例代码扫描(142 块) | 9 严重(语法/弯引号/签名错)全修;3 轻微未修;**15 处 B 警告按用户决策保持原状** |
| 触及章节文件 | **5 个**(代码块扫描):ch03 / ch14 / ch16 / ch17 / ch29 |
| 触及附录文件 | **2 个**:faq.md / references.md |
| 修改 `make smoke` 结果 | 仍 6 passed / 1 skipped(无 regression) |
| `make verify` | inline mermaid=0 / SVG refs=38 |
| 本地绝对路径泄漏 | 0 命中 |

## Subagent #1:附录 fact-check(8 严重 + 8 警告 = **16 修复**)

### faq.md(11 修复)

| 类型 | 位置 | 摘要 | 现状 |
|---|---|---|---|
| 严重 | L38 | `<COGNEE_REPO>/cognee/config.py` → `cognee/api/v1/config/config.py`(走 `cognee.config` 导入) | ✓ |
| 严重 | L232/Q12 | `search_type=` → `query_type=`(v1 Python) | ✓ |
| 严重 | L251/Q13 | 同上 | ✓ |
| 严重 | L267/Q14 | 同上 | ✓ |
| 严重 | L285/Q15 | 同上 | ✓ |
| 严重 | L294–307/Q16 | `@register_retriever("my_retriever")` 完全错;改为 `cognee.modules.retrieval.register_retriever.use_retriever(SearchType, RetrieverClass)` | ✓ |
| 严重 | L319/Q17 | `python -m cognee_mcp` → `uv run cognee-mcp`(cognee-mcp 是独立 console script) | ✓ |
| 严重 | L333/Q18 | 同上 | ✓ |
| 严重 | L397–407/Q23 | `os.environ["SESSION_POSTGRES_CACHE_PLAN"]="1"` → `CACHE_BACKEND=postgres` + `CACHE_DB_URL` | ✓ |
| 警告 | L139/Q7 | `task_concurrency` 配置项在 v1.4.0 不存在 | ✓ |
| 警告 | L443/Q26 | `cognee cognify --debug` → `cognee --debug cognify` | ✓ |

### references.md(1 修复)

| 类型 | 位置 | 摘要 | 现状 |
|---|---|---|---|
| 警告 | L11 | arXiv 2505.24478 论文标题错(WebFetch 实证) | ✓ |

### 完整触发但**未动**的项目

- **HTTP/JSON 上下文用 `search_type=` 是对的**:n8n 节点 Q19 L351 `"search_type":"FEELING_LUCKY"` + `"query":"..."` 符合 HTTP 字段规约,**已留在原文**
- **`references.md` "24 类集成"**:inventory.yml 计数匹配(24 entry 含 strands 重),边界情形,不动
- **`references.md` cognee-mcp 项目归属**:cognee-mcp 是 cognee 主仓内独立子包 `<COGNEE_REPO>/cognee-mcp/`,不是独立仓,与 faq Q17 描述一致

## Subagent #2:SVG 资源核对(**零修改**)

### 存在性核对

| 项 | 数值 |
|---|---|
| `assets/diagrams/` 实际文件数 | 38 |
| 章节文件唯一引用 SVG 数 | 38 |
| 缺失(被引但文件无) | **0** |
| 孤儿(文件有但未被引) | **0** |

### 章号-文件名匹配

100% 对齐(38/38)。6 处高风险抽查全部语义一致:

- `ch03-01-add-cognify-search.svg` vs `ch13-01-add-cognify-search.svg`:文件名同但分别服务**入门时序图** vs **v1 状态机**两个语境,M11 已确认两 SVG 二进制各自独立绘制,**不是错配**
- `ch23-03-11.svg` 的 "11" = 23.5 节速查表的 11 项集成
- `ch25-01-5.svg` 的 "5" = 5 个迁移源

### 结论:**零修改任务**

`assets/diagrams/` 全对齐,无需改动。

## Subagent #3:示例代码静态扫描(9 严重修复 + 15 警告留存 + 3 轻微未修)

### 严重 (A 类) - 9 处已修

| 章节:行号 | 错配类型 | 修复 |
|---|---|---|
| ch17-cp:343 | 弯引号(26 处 U+201C/U+201D) | 全部换 ASCII `"` |
| ch03-add-cognify:92 | `default_tasks` 第 3/4 项语法 | 修复列表元素 |
| ch14-v2-memory:61 / 196 / 323 / 403 | 4 个 v2 函数签名缺 `pass` | 补 `pass` |
| ch14-v2-memory:589 | 决策树伪代码 `use v2`/`use v1` | 改成 `api = "v2"`/`"v1"` |
| ch16-memify:33 | memify 签名缺 `pass` | 补 `pass` |
| ch29-frontend:312 | 2 个 visualize 函数缺 `pass`;`...` 不能作参数名 | 补 `pass`,改 `(*args, **kwargs)` |

### 警告 (B 类) - 15 处**未修**(用户决定:保持原状)

`cognee.add(data, dataset_name=...)` 在 8 个章节 / 15 处代码块出现。

**关键发现**:**`dataset_name=` 是 v1.4.0 的真名,`dataset=` 不存在**(实测 `inspect.signature(cognee.add)`)。

涉及章节:
- ch01-why-memory:77, 201
- ch03-add-cognify:72, 258
- ch04-core-concepts:51
- ch12-graph-governance:130, 135
- ch13-v1-api:72, 85, 102
- ch17-custom-pipelines:72
- ch24-config-datasets:165, 259
- ch27-performance-cache:190, 244

**历史教训记录**(规约沉淀):M12 prompt 规则表错误地把 `dataset_name=` 列为需要修复的错配。已根据用户裁决 + 实证 API 签名,确认维持 `dataset_name=`,并把这条加入 handbook 写作规约。

### 轻微 (C 类) - 3 处记入报告,未修

`top_k=10` 出现在 3 处代码块:
- ch03-add-cognify:172, 275
- ch13-v1-api:297

默认值偏差(实际默认 15),属于风格项,读者传入时会运行但查到的结果条数不同。本次不动。

## 跨子代理发现:协议层边界规约

**核心规约(必须加进 CONTRIBUTING.md / style-guide.md)**:

> cognee API 示例代码块必须在**协议层**明确标注:
> - **v1 Python SDK**:使用 `query_type=`、`query_text=`、`top_k=` 等关键字
> - **v2 memory API**:使用 `query_text=`(记忆层)、`cognee.remember / recall / improve / forget`
> - **HTTP / JSON payload**:使用 `search_type=`、`query=`(field 名不同)
> - **CLI**:`cognee --debug cognify`、`cognee search ...` 等

混淆规则表的关键例子:`search_type=GRAPH_COMPLETION` 在 Python SDK 错配(应是 `query_type`),但出现在 n8n 节点 JSON 载荷是合法。M12 修复时已严格按此规则判断。

## 最终验证

```bash
# 本地绝对路径扫描(零命中)
$ grep -rn "/Users/digoal" chapters/ appendix/ | grep -v "chapters-inline-mermaid.bak"
(empty)

# smoke
$ make smoke
6 passed, 1 skipped in 9.06s  ✓

# verify
$ make verify
Inline mermaid: 0  ✓
SVG refs: 38     ✓
```

## 沉淀的写作规约(供后续 CONTRIBUTING 修订)

1. **API 示例必须标注协议层**:v1 Python / v2 memory / HTTP / CLI 区分清楚,禁止混用字段名(示例:`search_type=` 仅 HTTP 合法)
2. **代码块先过语法 + Unicode 引号扫描**:U+2018/2019/201C/201D 在字符串字面量中必须换 ASCII `"` `'`。AST 解析作为入门关
3. **cognee.add 实参是 `dataset_name=`**:v1.4.0 的真参,不要套 v2 API 名词
4. **arXiv / DOI 引用必须 WebFetch 实证**:title 字段不能手填
5. **数字事实附核验命令**:`18 SearchType`、`22 CLI`、`24 inventory` 等数字必须由脚本生成或附 echo+grep 复核命令
6. **dist 重建需要"从工作树"**证明**:单看 mtime 不够;应附带构建时间戳或 git HEAD 信息嵌入 dist
7. **附录与正文纳入同次 fact-check 范围**:faq.md / references.md 不应被遗漏

## 触及的文件清单

| 文件 | 改动类型 | 行数 |
|---|---|---|
| `appendix/faq.md` | 严重+警告 + 14 处编辑 | 11 修复 |
| `appendix/references.md` | arXiv 标题修正 | 1 修复 |
| `chapters/part-01-foundation/chapter-03-add-cognify-search.md` | default_tasks 列表语法 | 1 严重 |
| `chapters/part-03-api/chapter-14-v2-memory-api.md` | 4 个 v2 签名 + 决策树 | 5 严重 |
| `chapters/part-03-api/chapter-16-memify.md` | memify 签名 | 1 严重 |
| `chapters/part-03-api/chapter-17-custom-pipelines.md` | 弯引号 26 处 | 1 严重 |
| `chapters/part-05-production/chapter-29-frontend-ui.md` | 2 个 visualize 签名 | 1 严重 |
| `code-review/svg-audit-report.md` | 新建(子产物) | — |
| `code-review/codeblocks-static-scan.md` | 新建(子产物) | — |
| `code-review/scan_blocks.py` | 新建(子产物) | — |
| `code-review/scan_results.json` | 新建(子产物) | — |
| `code-review/fact-check-m12.md` | 新建(本报告) | — |

## 已知遗留(不属于本次修复范围)

1. **3 处 `top_k=10`**(C 轻微未修):读者传入值合法,结果数量偏差属于风格项
2. **`make all` 重生成 dist**:M11 + M12 的所有修复未在 EPUB/PDF/HTML 反映。等用户决定是否重生成
3. **`appendix/faq.md` 28 个 Q 全量"运行验证"**:M12 修的是事实性 drift,不是端到端示例运行测试
4. **dist 内容已证明源自最新源的证据**:M12 仅基于 mtime 判断;若用户需要严格构建证明,需在 dist 内部嵌入 commit hash + 构建时间

## 同步约束

- ✅ 全程用 `<COGNEE_REPO>` / `<COGNEE_INTEGRATIONS_REPO>` / `<HANDBOOK_REPO>` 占位符
- ✅ 仅修改目标章节 / 附录文件;**未触碰** cognee、cognee-integrations、SVG 二进制、templates、dist
- ✅ 风格保留:不重写段落,只最小化 Edit
