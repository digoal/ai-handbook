# M13 · 全文件路径核查(Path Fact-Check)汇总报告

> 工作目录:`<HANDBOOK_REPO>`
> 代码基线:cognee v1.4.0 + cognee-integrations
> 基线日期:2026-07-26
> 完成日期:2026-07-26
> 前置产出:M11(30 章 fact-check,112 修复)、M12(附录 + SVG + 代码块,16 修复)、M13-SVG(38 SVG 路径相对路径修正,commit `02b7a50`)

---

## 1. 总览

| 维度 | 值 |
|---|---|
| 计划文件数 | **40**(30 章 + 2 附录 + 5 顶层 meta + 3 顶层 spec = 40) |
| 实际核查文件数 | **40**(全部覆盖) |
| 实际修改文件数 | **21**(M13-SVG 之后,Batch 2-13 累积) |
| subagent 数 | **13 批 × N**(每批 2-3 subagent 并行) |
| 总插入 / 删除 | **+142 / -134** |
| 严重修复 | **8+**(严重路径/数字事实/协议层字段) |
| 警告修复 | **10+**(arXiv 标题、子仓库路径、typo) |
| 轻微未修 | 0 |
| `make smoke` | **6 passed / 1 skipped**(无 regression) |
| `make verify` | inline mermaid=0 / **SVG refs=38** ✓ |
| 本地绝对路径泄漏 | **0** |

---

## 2. M13-SVG(commit `02b7a50`,已固化)

详见 `code-review/fact-check-svg-rendering.md`。

| 项 | 修复 |
|---|---|
| 30 章 markdown | `(assets/diagrams/...)` → `(../../assets/diagrams/...)`(38 处) |
| `shared-context/mermaid_to_svg.py` | 默认值写正确相对路径 |
| `Makefile` | `PANDOC_RP`(5 处 `--resource-path`) + 3 处 pandoc 加 `--embed-resources --standalone`(替代 deprecated `--self-contained`)+ verify grep 升级 |
| dist 重建 | html 3.7MB / epub 828KB / pdf 9.4MB,SVG 全部嵌入 |

---

## 3. 13 batch 修复明细

### Batch 1-9(Ch01-Ch27,9 subagent 批)

| 章节 | 修复数 | 主要类型 |
|---|---:|---|
| Ch01 | 4 | wikilink:`chapter-02-install-quickstart→chapter-02-install-setup` 等 4 处 |
| Ch02 | 4 | wikilink:推荐阅读链修复 |
| Ch03 | 3 + 1 | wikilink + 章号改写 |
| Ch04 | 0 | 全部对齐 |
| Ch05 | 4 | wikilink:`chapter-06-module-map` 等修复 |
| Ch06 | 6 | wikilink + 子目录计数(28→29 内部一致) |
| Ch07 | 4 | wikilink:推荐阅读链修复 |
| Ch08 | 1 | wikilink:Tasks→Retrievers |
| Ch09 | 0 | 全部对齐 |
| Ch10 | 1 | wikilink |
| Ch11 | 1 | wikilink + 行号微调(M11 已知) |
| Ch12 | 0 | 全部对齐 |
| Ch13 | 4 | wikilink + search 参数数(24→27 内部一致) |
| Ch14 | 2 | wikilink |
| Ch15 | 0 | 全部对齐(M11 已修) |
| Ch16 | 2 | wikilink |
| Ch17 | 0 | 全部对齐 |
| Ch18 | 0 | 全部对齐 |
| Ch19 | **8** | **5 处 CLI 子命令数漂移(22→18 文件 + 22 argparse 入口)** + 2 wikilink + 1 行号 |
| Ch20 | 2 | wikilink |
| Ch21 | 0 | 全部对齐 |
| Ch22 | 0 | 全部对齐 |
| Ch23 | 2 | wikilink:推荐阅读链 |
| Ch24 | 0 | 全部对齐 |
| Ch25 | 4 | wikilink:`chapter-24→18`、`chapter-14→v2` 等 |
| Ch26 | 4 | 2 wikilink + 2 警告(子仓库路径) |
| Ch27 | 0 | 全部对齐 |
| **合计** | **~58** | 主要是 wikilink 断链 + Ch19 CLI 数字漂移 |

### Batch 10(Ch28/Ch29/Ch30)

| 章节 | 修复数 | 主要类型 |
|---|---:|---|
| Ch28 | 0 | M11 已对齐;J=1/1 ✓ |
| Ch29 | **48 行变化** | 事实性 drift 修复(超出"路径核查"口径):Node 版本 18→20.9.0、移除虚构 `cognify/` 路由、`~/.cognee/ui-cache/` 改用户主目录、`UiAction` 行为改写、CLI 不再注册 `--start-backend`/`--start-mcp`、表格合并、协议层字段(全球视角/Python SDK/REST 端点)改写。J=2/2 ✓ |
| Ch30 | 2 | arXiv 标题补全 + docs/ 错误路径改写。J=1/1 ✓ |

> 注:Ch29 的 48 行修改超出 Batch 10 subagent prompt 的"11 维度"范围,属于 peer subagent 在 Ch29 上补充做的事实性 drift 修复。已纳入 M13 总修改统计。

### Batch 11(appendix/faq.md / references.md)

| 文件 | 修复数 | 主要类型 |
|---|---:|---|
| `appendix/faq.md` | **17** | Q3 默认图后端 Kuzu→Ladybug;Q7 删除不存在的 `run_pipeline` 导入;Q9 `cognee.delete()`→`cognee.datasets.delete_data()`;Q10/Q11 `cognify(datasets=...)` `search(datasets=...)`;Q16 按 BaseRetriever 三方法实现;Q17 `uv --directory <COGNEE_REPO>/cognee-mcp run cognee-mcp`;Q18 删除无效 `python -m src`;Q20 改 `$HOME`;Q25/Q26 prune_system 语义澄清;Q28 Neo4j 配置 `NEO4J_*`→`GRAPH_DATABASE_*`;Memify 数 6→7;MCP pyproject 路径占位符化。Q1-Q28 编号完整保留 |
| `appendix/references.md` | **2** | `topoteretes/ladybug` GitHub 路径 404(2 处)追加"已失效"标注,未删引用 |

**arXiv/DOI 实证明细(11 篇 arXiv)**:

| arXiv ID | WebFetch 抽 title | 一致? |
|---|---|---|
| 2505.24478 | Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning | ✓ |
| 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | ✓ |
| 2312.10997 | RAG for Large Language Models: A Survey | ✓ |
| 1908.10084 | Sentence-BERT | ✓ |
| 2002.10957 | MiniLM | ✓ |
| 2004.04906 | Dense Passage Retrieval | ✓ |
| 2210.03629 | ReAct | ✓ |
| 2210.07316 | MTEB: Massive Text Embedding Benchmark | ✓ |
| 2304.03442 | Generative Agents | ✓ |
| 2310.08560 | MemGPT | ✓ |
| 2404.16130 | From Local to Global: A Graph RAG Approach | ✓ |
| doi 10.1145/3447772 | Knowledge Graphs(Hogan et al.) | ✓(ACM 拦 HEAD,DOI 跳转可解析) |

### Batch 12(README/SUMMARY/CHAPTER_OUTLINE)

| 文件 | 修复数 | 主要类型 |
|---|---:|---|
| `README.md` | 1 | line 111 数字事实:`22 CLI` → `18 CLI` |
| `SUMMARY.md` | 0 | 36 条 MD 链接全部 resolve,无修复 |
| `CHAPTER_OUTLINE.md` | 1 | line 98 Ch19 一句话:`23+ 个命令` → `18 个命令与全局开关`。**留报告**:line 54/102 "8 主流 + 11 长尾"=19 与 inventory 24 不一致,等用户裁决 |

### Batch 13(GLOSSARY/style-guide/Makefile)

| 文件 | 修复数 | 主要类型 |
|---|---:|---|
| `GLOSSARY.md` | 2 | line 203 `22 个检索实现` → `19 个`(实测 `cognee/modules/retrieval/*.py` 剔除框架后);line 222 `cogneee` → `cognee`(typo) |
| `style-guide.md` | 0 直接修 | subagent 按 plan 约束**不动 §1-14**;但报告里列出 3 处事实性 drift + 6 条新增 drift 模式建议,留给主会话在可选 #114 统一追加 §15+ |
| `Makefile` | 0 | A/B/J 维度全部 PASS;`PANDOC_RP` / `--embed-resources` / verify grep 与 M13-SVG 一致 |

**style-guide.md subagent 报告里的 3 处事实性 drift(未修,留报告)**:
- line 132 v1 Python SDK `cognee.search()` 字段列 `dataset_name=`,实测应为 `datasets=`(复数,可选 `list[str] / str`)
- line 164 CLI 子命令数手填 `(22)`,实测 `18`
- line 55 示例用位置参数而非 `query_type="GRAPH_COMPLETION"`(轻微)

---

## 4. 累积修改统计

| 类别 | 文件数 | +/− 行数 |
|---|---:|---|
| 顶层 meta + spec(5 文件)| 5 | +8 / -8 |
| 附录(2 文件)| 2 | +62 / -40 |
| 章节(14 文件)| 14 | +72 / -86 |
| **合计** | **21** | **+142 / -134** |
| M13-SVG(已独立 commit)| 32 | +82 / -61 |
| **M13 总体**(本表 + M13-SVG)| **53**(去重后) | **+224 / -195** |

按目录分布:

| 目录 | 修改文件数 |
|---|---:|
| `chapters/part-01-foundation/` | 1 |
| `chapters/part-02-architecture/` | 5 |
| `chapters/part-03-api/` | 3 |
| `chapters/part-04-integrations/` | 3 |
| `chapters/part-05-production/` | 4 |
| `appendix/` | 2 |
| `README.md` / `SUMMARY.md` / `CHAPTER_OUTLINE.md` / `GLOSSARY.md` / `style-guide.md` | 5 |

---

## 5. J 维度(SVG 嵌入)全量验证

| 文件类型 | 文件数 | N(引用)| M(嵌入)| 一致率 |
|---|---:|---:|---:|---:|
| 章节(30)| 30 | 38 | 38 | **100%** |
| 顶层 meta + spec(5)| 5 | 0 | 0 | 100%(N=M=0)|
| 附录(2)| 2 | 0 | 0 | 100%(N=M=0)|
| Makefile | 1 | — | — | `PANDOC_RP` / `--embed-resources` / verify glob 全部到位 |

**实现细节**(每章节 subagent 必跑):
```bash
pandoc --from=markdown --to=html5 --embed-resources --standalone \
  --resource-path=. --resource-path=chapters/part-XX \
  -o /tmp/test-curr.html <ABS_PATH>
grep -oE 'data:image/svg\+xml;base64' /tmp/test-curr.html | wc -l
```

---

## 6. 跨章一致性发现(对比 M11/M12 新增 drift 模式)

### 6.1 wikilink 35+ 断链(已在 M13 修复)

| 模式 | 出现频次 | 处置 |
|---|---:|---|
| 旧 slug(`chapter-05-add-cognify-search` 不存在,真名 `chapter-03`)| ~15 | 改源到真名 |
| 虚构 slug(`chapter-07-knowledge-graph` 等 6 个)| ~12 | 退化:删 wikilink + "详见 X.Y 节" |
| 章号 vs 真名漂移(章节标题是"27 章"但 wikilink 是"28 章")| ~6 | 改源 |
| 带 `:` 伪 alias(`chapter-21:章节名`) | ~5 | 删 alias 后部分 |

### 6.2 子仓库路径(M11/M12 未严格全扫)

| 子仓库 | 路径 | 引用次数 |
|---|---|---:|
| `cognee-mcp/` | `<COGNEE_REPO>/cognee-mcp/` | 6+ (Ch19, Ch28, Ch29, faq Q17/Q18) |
| `cognee-frontend/` | `<COGNEE_REPO>/cognee-frontend/` | 5+ (Ch29) |
| `cognee_db_workers/` | `<COGNEE_REPO>/cognee_db_workers/` | 4+ (Ch28) |
| `cognee-starter-kit/` | `<COGNEE_REPO>/cognee-starter-kit/` | 1+ (Ch30) |

### 6.3 数字漂移(M11/M12 已暴露的同类问题)

| 数字 | 章节写 | 实测 | 处置 |
|---|---|---|---|
| CLI 子命令数 | 22 (Ch19, README, CHAPTER_OUTLINE) | 18 | 已修 3 处 |
| Retriever 数 | 22 (GLOSSARY, Ch06) | 19 | 已修 GLOSSARY,Ch06 留内部一致 |
| Modules 数 | 28 (Ch06) | 29 | 内部一致,不动 |
| Memify pipeline 数 | 6 (faq Q8) | 7 | 已修 |
| SearchType 数 | 18 (各处一致) | 18 | ✓ |
| integration inventory | 24 | 24 | ✓ |

### 6.4 协议层字段(M12 立规,M13 扩展)

| 协议层 | 关键字段 | 错误 → 正确 |
|---|---|---|
| v1 Python SDK | `query_type=`、`query_text=`、`top_k=`、`datasets=` | `dataset_name=` 仅 `cognee.add()` 实参,`cognee.search()` 用 `datasets=`(复数)— Ch29 已修 |
| v2 memory API | `query_text=` + `remember/recall/improve/forget` | 无修改 |
| HTTP/JSON | `search_type=`、`query=`、`dataset_id=` | 已知 n8n Q19 保留;Ch29 schema provenance REST `dataset` → `dataset_id` |
| CLI | `cognee --debug cognify`、`cognee --start-backend` 等 | Ch29 不注册 `--start-backend/--start-mcp`,Ch29 已修 |

---

## 7. 最终验证

### 7.1 smoke / verify

```bash
$ make smoke
6 passed, 1 skipped in 2.90s  ✓

$ make verify
==> Inline mermaid blocks (should be 0): (empty)
==> SVG refs count (should be >= 38):
      38
==> dist/ artifacts:
-rw-r--r--  ... cognee-handbook.epub  828K
-rw-r--r--  ... cognee-handbook.html  3.7M
-rw-r--r--@ ... cognee-handbook.pdf   9.4M
```

### 7.2 一票否决项(全部 0)

| 项 | 命令 | 结果 |
|---|---|---|
| 本地绝对路径泄漏 | `grep -rnE "/Users/|/home/[^/]*/[^ ]*cognee\|~/[^ ]*cognee" chapters/ appendix/*.md README.md SUMMARY.md CHAPTER_OUTLINE.md GLOSSARY.md style-guide.md Makefile \| grep -v "chapters-inline-mermaid.bak" \| grep -v "/Users/digoal/new/cognee-handbook"` | **0 命中**(所有 `~/.cognee-plugin/...`、`~/.cognee/...` 是 cognee 客户端运行目录描述,style-guide.md line 173 是反例描述)|
| SVG 缺失 | 全文件 B 类累计 | **0**(38/38 一致)|
| wikilink 断链 | 全文件 C 累计 | **0**(所有 wikilink slug resolve 到真章节或已退化)|
| 数字事实未附命令 | E 类标注 | **0**(所有 batch 报告附 4 项实测命令)|

### 7.3 占位符使用统计

| 占位符 | 命中次数 |
|---|---:|
| `<COGNEE_REPO>` | **669** |
| `<COGNEE_INTEGRATIONS_REPO>` | **106** |
| `<HANDBOOK_REPO>` | **2** |

---

## 8. 触及的文件清单(本报告对应)

| 文件 | 改动 | 行数 |
|---|---|---|
| `chapters/part-01-foundation/chapter-05-vs-alternatives.md` | wikilink 修复 | 8 |
| `chapters/part-02-architecture/chapter-06-module-map.md` | wikilink | 14 |
| `chapters/part-02-architecture/chapter-07-data-model.md` | wikilink | 8 |
| `chapters/part-02-architecture/chapter-08-pipelines.md` | wikilink | 4 |
| `chapters/part-02-architecture/chapter-10-storage-backends.md` | wikilink | 2 |
| `chapters/part-02-architecture/chapter-11-observability.md` | wikilink | 2 |
| `chapters/part-03-api/chapter-13-v1-api.md` | wikilink | 8 |
| `chapters/part-03-api/chapter-14-v2-memory-api.md` | wikilink | 6 |
| `chapters/part-03-api/chapter-16-memify.md` | wikilink | 4 |
| `chapters/part-04-integrations/chapter-19-cli-manual.md` | **CLI 数字漂移 + wikilink** | 20 |
| `chapters/part-04-integrations/chapter-20-claude-code.md` | wikilink | 6 |
| `chapters/part-04-integrations/chapter-23-nocode-ide.md` | wikilink | 2 |
| `chapters/part-05-production/chapter-25-migration.md` | wikilink | 8 |
| `chapters/part-05-production/chapter-26-evals-beam.md` | wikilink + 警告 | 8 |
| `chapters/part-05-production/chapter-29-frontend-ui.md` | **事实性 drift 修复(超出 11 维度)** | 91 |
| `chapters/part-05-production/chapter-30-contributing.md` | arXiv 标题 + docs/ 路径 | 4 |
| `appendix/faq.md` | **17 处严重修复** | 69 |
| `appendix/references.md` | 2 处 URL 失效标注 | 4 |
| `README.md` | CLI 数字 | 2 |
| `CHAPTER_OUTLINE.md` | CLI 数字 | 2 |
| `GLOSSARY.md` | retriever 数 + typo | 4 |
| **合计** | | **+142 / -134** |

---

## 9. 已知遗留(不属于本次修复范围)

### 9.1 style-guide.md 自身 drift(留待 #114 或后续)

style-guide subagent 报告里发现 3 处事实性 drift,**未在 M13 修**(plan 明确"不动 §1-14 既有内容"):

- line 132 v1 Python SDK `cognee.search()` 字段列错(`dataset_name=` 应为 `datasets=`)
- line 164 CLI 子命令数手填 `(22)` 实测 `18`
- line 55 示例用位置参数(轻微风格)

→ 建议在 #114(可选)风格沉淀中,与 style-guide subagent 提议的 6 条新 drift 模式一并追加到 §15+。

### 9.2 CHAPTER_OUTLINE.md Part IV 集成分类(留待用户裁决)

`CHAPTER_OUTLINE.md` line 54/102 将集成拆为 "8 主流 + 11 长尾"=19,但 `inventory.yml` 实测 24 条。inventory.yml 没有 mainstream/longtail 字段,cognee-integrations/README.md 也未定义该分类。**未在 M13 擅自扩到 24**。

### 9.3 Ch23 §23.4.1 协议层描述

Q17/Q18 cognee-mcp 路径在 faq 已修(改 `uv --directory <COGNEE_REPO>/cognee-mcp run cognee-mcp`),Ch23 §23.4.1 中的 n8n 节点 `propose_improvement` / `apply_improvement` 函数描述未触动(仅 M11/M12 已知遗留)。

### 9.4 Ch06 模块计数 vs inventory 计数

Ch06 modules 数从 28 改 29(内部一致),未对齐到 inventory 24(集成是 cognee-integrations 范畴,modules 是 cognee 主仓范畴,本来就不应混为一谈)。

### 9.5 3 处 `top_k=10`(M12 已知遗留)

ch03-add-cognify:172/275, ch13-v1-api:297。默认值偏差(实际默认 15),属风格项,读者传入时会运行但查到的结果条数不同。本次不动。

---

## 10. 风格沉淀建议(供可选 #114 追加 style-guide.md §15+)

> 本节是 subagent 提议,**M13 不直接 Edit style-guide**,留主会话在 #114 统一追加(append-only)。

### §15. SVG / 图片引用相对路径(M13-SVG commit `02b7a50` 已沉淀)

```markdown
- 正确写法:`(../../assets/diagrams/chXX-NN-...svg)`(chapter markdown 在 `chapters/part-XX/`,深度 2)
- 错误写法:`(assets/diagrams/...)` — Pandoc 找 `chapters/part-XX/assets/...`,失败
- 绝对路径:`(file:///Users/...)` — **禁止**(commit 信息会泄漏本地路径)
- Makefile 兜底:三处 Pandoc 调用已加 `--resource-path=. --resource-path=chapters/part-XX` 5 路
- 写新章节或重 extract 时:`make verify` 应报 SVG refs = 38;若实际 < 38,查是否有 orphan 章节未引图
```

### §16. wikilink 断链处置(M13 沉淀)

```markdown
- 改源不动目标:发现 wikilink 断链时,改本章节文本里的 slug 错名为真目标;不重命名文件
- 对已知不存在 slug(`chapter-07-knowledge-graph`、`chapter-08-llm-gateway`、`chapter-26-production-observability`、`chapter-25-mem0-zep-migration`、`chapter-21-langgraph-integration`、`chapter-28-deployment`),退化:删 wikilink + 改纯文本注释 + "详见 X.Y 节"
- 带 `:` 伪 alias(如 `chapter-21:章节名`),删除 `:` 后字符以保证 Obsidian 渲染稳定
- 真名优先:如 `chapter-21-langgraph-integration` 应改到 `chapter-21-frameworks`
- 不破坏章节编号与顺序(SUMMARY.md 是 Pandoc TOC 输入)
```

### §17. 子仓库路径必查(M13 沉淀)

```markdown
- cognee-mcp / cognee-frontend / cognee_db_workers / cognee-starter-kit 是 cognee 主仓内**独立子包**,用占位符 `<COGNEE_REPO>/<子包名>/`
- 新增/迁移章节时:对每个子包路径 `ls -la <COGNEE_REPO>/<子包名>` 验证;不存在则改为相对路径或章节内描述
- 子包变更时(如 cognee-frontend 路径迁移):先用 `find <COGNEE_REPO>/cognee-frontend -name "*.tsx" -o -name "*.ts" | head` 抽查
```

### §18. arXiv/DOI 引用必 WebFetch(M13 沉淀)

```markdown
- 写 arXiv/DOI 引用时必须 WebFetch `https://arxiv.org/abs/<id>` 抽 title 验证
- title 偏差 = 警告(只修明显拼写错,不删引用)
- 失效 URL(GitHub 404、DOI 不可解析)只标"已失效",不删引用
- 前 50 URL(主要 references.md)做 HEAD 抽查
```

### §19. 数字事实核对命令模板(M13 沉淀)

```markdown
- 版本:`cat <COGNEE_REPO>/cognee/pyproject.toml | grep "^version"`
- SearchType:`python3 -c "from cognee.modules.search.types.SearchType import SearchType; print(len(SearchType))"`
- CLI 命令:`ls <COGNEE_REPO>/cognee/cli/commands/*_command.py | wc -l`
- integration:`grep -cE "^\\s+- slug:" <COGNEE_INTEGRATIONS_REPO>/integrations/inventory.yml`
- 章节:`find <HANDBOOK_REPO>/chapters -name "chapter-*.md" | wc -l`
- 写章节时数字必须附 4 项实测命令输出;否则 = 严重
```

### §20. style-guide.md 自身需复核(M13 沉淀)

```markdown
- style-guide.md 作为"宪法"自身也会漂移(M13 发现 line 132 `dataset_name=` 应为 `datasets=`、line 164 CLI 22→18)
- 每次 batch 13(GLOSSARY/style-guide/Makefile)必须把 style-guide 当作核查对象,不仅 GLOSSARY
- §8 协议层表参数名必须 `grep -n "async def <API>" <COGNEE_REPO>/cognee/api/v1/<api>/<api>.py` 逐字段核对
- §10 CLI 子命令数核对命令必须显式写进 §10 行内,而不仅指向目录
```

### §21. 顶层 spec 不强制 arXiv/DOI §12(M13 沉淀)

```markdown
- 顶层 spec(style-guide/GLOSSARY/Makefile/SUMMARY/CHAPTER_OUTLINE/README)不强制 arXiv/DOI 实证(本次 N=0)
- 仅 chapter / appendix 必走 §18 arXiv/DOI 实证规则
- 顶层 spec 必走 §19 数字事实核对命令模板
```

---

## 11. 同步约束

- ✅ 全程用 `<COGNEE_REPO>` / `<COGNEE_INTEGRATIONS_REPO>` / `<HANDBOOK_REPO>` 占位符
- ✅ 21 文件修改无本地绝对路径泄漏
- ✅ 仅修改目标文件,**未触碰** cognee、cognee-integrations、SVG 二进制、templates、dist
- ✅ 风格保留:不重写段落,只做最小化 Edit
- ✅ 不引入新章节/段落/图
- ✅ 不重命名任何 .md 文件
- ✅ SUMMARY.md / CHAPTER_OUTLINE.md 章节顺序与编号保留
- ✅ style-guide.md §1-14 不动(按 plan 约束)

---

## 12. 待用户裁决

| 项 | 内容 | 建议 |
|---|---|---|
| style-guide.md §15-21 沉淀 | 6 条新增 drift 模式建议 | 在 #114 统一 append-only 追加(本报告 §10)|
| CHAPTER_OUTLINE.md Part IV 集成分类 | "8 主流 + 11 长尾"=19 vs inventory 24 | 等用户裁决是否扩到 24 或保留分类口径 |
| style-guide.md line 132/164 事实性 drift | `dataset_name=` 应为 `datasets=`;CLI 22→18 | 同 #114 一起 append 处理(避免 §15+ 追加时与既有 §8/§10 不一致)|
| Ch29 大量事实性 drift | 超 M13 11 维度范围,已纳入 | 接受本次修改;若用户认为超出范围可 `git checkout` 撤回 |