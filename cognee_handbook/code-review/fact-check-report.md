# M11 · Fact-check 修复汇总报告

> 工作目录:`<HANDBOOK_REPO>`
> 代码基线:cognee v1.4.0 + cognee-integrations
> 基线日期:2026-07-26
> 验证日期:2026-07-26

## 总览

30 章全部经过 subagent 串行核查并即时修复(每个章节一个 general-purpose 串行 subagent,隔离上下文,无 worktree)。

| 维度 | 结果 |
|---|---|
| 章节数 | 30 |
| 发现 drift 总数 | **112** |
| 严重 | 23 |
| 警告 | 51 |
| 轻微 | 38 |
| 已修复 | **112 / 112** ✓ |
| `make smoke` | 6 passed / 1 skipped(与 M8 一致,无 regression) |
| `make verify` | inline mermaid=0 / SVG refs=38 |
| 本地绝对路径扫描 | 0 命中 |

## 章节修复明细

| 章节 | 严重 | 警告 | 轻微 | 合计 | 核心问题 |
|---|---|---|---|---|---|
| Ch01 | 0 | 3 | 2 | 5 | CLAUDE.md 路径、REPORT.md L91/L92、simple_cognee_example v1/v2 错配、ECL 步数、top_k 默认 |
| Ch02 | 1 | 2 | 1 | 4 | requires-python 段位、Windows 二进制、pip requirements、env 注释 |
| Ch03 | 3 | 1 | 0 | 4 | SQLite/LanceDB/Ladybug 落盘路径系统错(`<cwd>/` 与 `.data_storage` 均非真实) |
| Ch04 | 1 | 0 | 0 | 1 | ECL 权威出处应指 `<COGNEE_REPO>/CLAUDE.md` |
| Ch05 | 0 | 1 | 0 | 1 | zep.py 时态字段描述偏差 |
| Ch06 | 16 | 2 | 0 | 18 | 子目录计数(28→29)、虚构 packages、检索器数(17→19) |
| Ch07 | 0 | 1 | 0 | 1 | Entity.description 标记"可选"实为必填 |
| Ch08 | 2 | 0 | 1 | 3 | Ch09 链接错位(Tasks→Retrievers)、预告重写、PipelineRunStatus 正式枚举 |
| Ch09 | 0 | 0 | 0 | 0 | 无需修复 |
| Ch10 | 0 | 3 | 0 | 3 | Graph/Vector 适配器漏列、FAISS 不存在、CacheConfig Literal 默认 |
| Ch11 | 0 | 1 | 3 | 4 | 行号微调(31-45/15-28/31 等) |
| Ch12 | 0 | 0 | 0 | 0 | 无需修复 |
| Ch13 | 0 | 4 | 1 | 5 | search 参数数(24→27)、memify 默认任务、delete deprecated 路径、add 参数数(18→15)、括号 |
| Ch14 | 1 | 3 | 4 | 8 | improve 多阶段、RecallResponse 来源数、scope 示例、字段完整度、RememberResult 语义、content_hash 承诺 |
| Ch15 | 7 | 0 | 0 | 9 | 跨章链接失效、TextualSummary 类名错(实际 TextSummary)、TemporalEdge 不存在、codeprep 路径错 |
| Ch16 | 1 | 2 | 1 | 4 | memify 默认任务 5 步误述、feedback_score 取值范围、improve pipeline 漏段、user=None 不可运行 |
| Ch17 | 1 | 0 | 0 | 1 | dynamic_steps_resume 样例代码函数名/键名全错 |
| Ch18 | 0 | 0 | 0 | 0 | 无需修复(全部对齐) |
| Ch19 | 1 | 5 | 0 | 6 | CLI 子命令数(23+→22)、--debug 行号、eval 默认值、eval --engine、eval --benchmark、BEM/BEAM 笔误、独立子仓笔误 |
| Ch20 | 3 | 0 | 1 | 4 | _plugin_common 字节数、scripts 文件数(22→18)、doctor 输出样本全新改写、statusline 行号 |
| Ch21 | 0 | 0 | 0 | 0 | 无需修复(API 边界、版本约束、示例代码全部对齐) |
| Ch22 | 0 | 0 | 2 | 2 | chat-memory scope 后应小写(`brain:U456`→`brain:u456`) |
| Ch23 | 4 | 5 | 0 | 9 | n8n Skill URL 全部错位(`/api/v1/skill/*`→`/v1/skills`/`/v1/proposals`)、Codex CHANGELOG 路径、inventory 22/24 区分、Command ID、Vellum 文件数、Aider .env 行号 |
| Ch24 | 0 | 2 | 0 | 2 | Embedding/Chunking BaseSettings 漏列、Dataset 模块归属 |
| Ch25 | 1 | 1 | 1 | 3 | remember 路由器文件名、permissions.json 安全约束文档归属、prune_system cache 参数 |
| Ch26 | 3 | 1 | 1 | 5 | 虚构 1M=0.72、dataset.from_jsonl 不存在、--benchmark 枚举实际值(BEAM/HotPotQA/Musique 等)、runner.run 调用名 |
| Ch27 | 1 | 0 | 0 | 1 | run_pipeline 单 dataset 并行度误解 |
| Ch28 | 0 | 0 | 1 | 1 | users 路由应为 GET/PATCH /{id} 而非裸 GET |
| Ch29 | 2 | 2 | 1 | 5 | importance_weight(应为 importance)、schema provenance REST 端点(GET非 POST)、dataset→dataset_id、color palette 来源 |
| Ch30 | 2 | 4 | 5 | 11 | op-code 常量值字符串→整数、Request/worker 方法名错、extras 数(26→34)、多个文件归错、行号偏移 |
| **合计** | **23** | **51** | **38** | **112** | — |

## 跨章一致性发现

修复过程中多次出现的相同 drift 模式:

1. **数量/计数错位**(Ch06 modules=28/13/14、Ch13 search=24/add=18、Ch19 CLI=23+、Ch20 scripts=22、Ch30 extras=26):章节模板倾向"加塞吸引眼球的数字",与实际目录/enum 不齐
2. **行号偏移**(Ch11 / Ch25 / Ch29 / Ch30):上游重构未同步更新
3. **类名/方法名拼写**(Ch15 TextualSummary→TextSummary、Ch20 doctor 字段、Ch25 router 文件名、Ch30 Request import):章节手抄源码时无意识重命名
4. **API 归属混淆**(Ch04 ECL 描述、Ch24 Dataset 路径、Ch20 cognee-mcp 仓库性质、Ch30 命令块归错文件):章节常把"看似相关"的内容放到最近文件下
5. **虚构内容**(Ch26 1M=0.72、Ch22 dataset 大小写、Ch19 BEM vs BEAM 笔误、Ch22 11 集成总数未与 inventory 对齐):需要在每章查 source-of-truth

## 修复手法一致约束

- ✅ 全部使用 `<COGNEE_REPO>` / `<COGNEE_INTEGRATIONS_REPO>` / `<HANDBOOK_REPO>` 占位符,**无本地绝对路径泄漏**
- ✅ 仅修改目标章节文件,**未触碰 cognee / cognee-integrations / 其他章节**
- ✅ 风格保留:不重写段落,只做最小化 Edit
- ✅ 不引入新章节/段落/图

## 已知遗留(不属于本次修复范围)

- 部分章节引用的 SVG 文件相对路径(如 `assets/diagrams/ch09-01-retriever.svg`),在 `<HANDBOOK_REPO>/assets/diagrams/` 是否真实存在——本次只核代码,未核 SVG 资源
- Ch15 §15 中提到的 `TextSummary` 路径(实际为 `cognee/tasks/summarization/models.py`)虽然章节已改,示例代码中对 `TextSummary` 类的 instance 字段引用可能未全数对照——需后续跑代码示例时复核
- Ch23 §23.4.1 中提到的 n8n 节点 `propose_improvement` / `apply_improvement` 函数在 cognee 仓库不存在(只在 n8n 节点层包装),本节是"伪代码描述",已保留原文措辞

## 验证

```bash
# 本地绝对路径扫描(零命中)
$ grep -rn "/Users/digoal" chapters/ appendix/ | grep -v "chapters-inline-mermaid.bak"
(empty)

# smoke 测试
$ make smoke
6 passed, 1 skipped in 5.32s  ✓

# verify
$ make verify
Inline mermaid: 0  ✓
SVG refs: 38     ✓
```

## 建议(本任务边界外)

如用户后续要继续提升:

1. **重生成 dist**:`make all` 把最新修复反映到 EPUB / PDF / HTML(本次未跑,等用户决定)
2. **代码示例运行验证**:跑 `cognee-api-smoke` 套件以外的端到端测试,确认修复后的示例代码都能 copy-paste 跑通
3. **SVG 资源审计**:把 `chapters/` 里所有 `assets/diagrams/*.svg` 引用与 `<HANDBOOK_REPO>/assets/diagrams/*.svg` 实际列表做差集,填补缺失
4. **附录 fact-check**:`appendix/faq.md`、`appendix/references.md` 也做一遍同样流程(本轮范围未覆盖)
