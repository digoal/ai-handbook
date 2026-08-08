# SVG 资源审计报告

## SUMMARY

存在性 38 = 38 ✓ | 内容错配 0 处(全部对齐,无需修复)

## EXISTENCE_CHECK

| 指标 | 数值 |
|---|---|
| `assets/diagrams/` 下 SVG 文件总数 | 38 |
| 章节文件 `assets/diagrams/*.svg` 唯一引用路径数 | 38 |
| 差集(被引但缺失) | 0 |
| 差集(有但未被引) | 0 |

**结论:** 所有 38 个 SVG 均被唯一引用,且每个引用都能在 `assets/diagrams/` 中找到对应文件。零差集。

## 章节号-文件名匹配检查(38 项逐一核对)

| # | 章节文件 | 引用 SVG | 文件名章号 | 章节实际号 | 是否一致 |
|---|---|---|---|---|---|
| 1 | part-01/chapter-01-why-memory.md | ch01-01-rag-vs-cognee-ecl.svg | Ch01 | Ch01 | ✓ |
| 2 | part-01/chapter-02-install-quickstart.md | ch02-01-cognee.svg | Ch02 | Ch02 | ✓ |
| 3 | part-01/chapter-03-add-cognify-search.md | ch03-01-add-cognify-search.svg | Ch03 | Ch03 | ✓ |
| 4 | part-01/chapter-04-core-concepts.md | ch04-01-cognee.svg | Ch04 | Ch04 | ✓ |
| 5 | part-01/chapter-05-vs-alternatives.md | ch05-01-diagram.svg | Ch05 | Ch05 | ✓ |
| 6 | part-02/chapter-06-module-map.md | ch06-01-cognee.svg | Ch06 | Ch06 | ✓ |
| 7 | part-02/chapter-07-data-model.md | ch07-01-datapoint-entity-edge-dataset.svg | Ch07 | Ch07 | ✓ |
| 8 | part-02/chapter-08-pipelines.md | ch08-01-cognify-pipeline-dag.svg | Ch08 | Ch08 | ✓ |
| 9 | part-02/chapter-09-retrievers.md | ch09-01-retriever.svg | Ch09 | Ch09 | ✓ |
| 10 | part-02/chapter-10-storage-backends.md | ch10-01-cognee.svg | Ch10 | Ch10 | ✓ |
| 11 | part-02/chapter-11-observability.md | ch11-01-trace.svg | Ch11 | Ch11 | ✓ |
| 12 | part-02/chapter-12-graph-governance.md | ch12-01-dataset.svg | Ch12 | Ch12 | ✓ |
| 13 | part-03/chapter-13-v1-api.md | ch13-01-add-cognify-search.svg | Ch13 | Ch13 | ✓ |
| 14 | part-03/chapter-14-v2-memory-api.md | ch14-01-remember-recall-improve-forget.svg | Ch14 | Ch14 | ✓ |
| 15 | part-03/chapter-14-v2-memory-api.md | ch14-02-v1-vs-v2.svg | Ch14 | Ch14 | ✓ |
| 16 | part-03/chapter-14-v2-memory-api.md | ch14-03-improve.svg | Ch14 | Ch14 | ✓ |
| 17 | part-03/chapter-15-search-type-tour.md | ch15-01-searchtype.svg | Ch15 | Ch15 | ✓ |
| 18 | part-03/chapter-16-memify.md | ch16-01-session-distillation.svg | Ch16 | Ch16 | ✓ |
| 19 | part-03/chapter-16-memify.md | ch16-02-session.svg | Ch16 | Ch16 | ✓ |
| 20 | part-03/chapter-17-custom-pipelines.md | ch17-01-cognify-pipeline-dag.svg | Ch17 | Ch17 | ✓ |
| 21 | part-03/chapter-18-agent-memory.md | ch18-01-agent-agent-memory-cognee.svg | Ch18 | Ch18 | ✓ |
| 22 | part-04/chapter-19-cli-manual.md | ch19-01-cognee-cli-ui.svg | Ch19 | Ch19 | ✓ |
| 23 | part-04/chapter-20-claude-code.md | ch20-01-claude-code-cognee-mcp-cognee-server.svg | Ch20 | Ch20 | ✓ |
| 24 | part-04/chapter-20-claude-code.md | ch20-02-claude-agent-sdk-mcp.svg | Ch20 | Ch20 | ✓ |
| 25 | part-04/chapter-21-frameworks.md | ch21-01-agent-cognee.svg | Ch21 | Ch21 | ✓ |
| 26 | part-04/chapter-22-chat-tools.md | ch22-01-chat-tool-cognee.svg | Ch22 | Ch22 | ✓ |
| 27 | part-04/chapter-23-nocode-ide.md | ch23-01-diagram.svg | Ch23 | Ch23 | ✓ |
| 28 | part-04/chapter-23-nocode-ide.md | ch23-02-skill-self-improve-loop.svg | Ch23 | Ch23 | ✓ |
| 29 | part-04/chapter-23-nocode-ide.md | ch23-03-11.svg | Ch23 | Ch23 | ✓ |
| 30 | part-05/chapter-24-config-datasets.md | ch24-01-diagram.svg | Ch24 | Ch24 | ✓ |
| 31 | part-05/chapter-25-migration.md | ch25-01-5-cogxarchive.svg | Ch25 | Ch25 | ✓ |
| 32 | part-05/chapter-26-evals-beam.md | ch26-01-cognee-eval.svg | Ch26 | Ch26 | ✓ |
| 33 | part-05/chapter-26-evals-beam.md | ch26-02-vs-beam.svg | Ch26 | Ch26 | ✓ |
| 34 | part-05/chapter-27-performance-cache.md | ch27-01-diagram.svg | Ch27 | Ch27 | ✓ |
| 35 | part-05/chapter-28-api-server-deploy.md | ch28-01-api-server.svg | Ch28 | Ch28 | ✓ |
| 36 | part-05/chapter-29-frontend-ui.md | ch29-01-cognee-frontend.svg | Ch29 | Ch29 | ✓ |
| 37 | part-05/chapter-29-frontend-ui.md | ch29-02-semantic-memory-map.svg | Ch29 | Ch29 | ✓ |
| 38 | part-05/chapter-30-contributing.md | ch30-01-cognee.svg | Ch30 | Ch30 | ✓ |

## 语义上下文抽检(重要引用对齐核查)

抽 6 个高风险点逐一核对:

| 章节 | SVG 名 | 章节上下文节 | 引用语义 | 判定 |
|---|---|---|---|---|
| Ch03 | ch03-01-add-cognify-search.svg | 3.1 完整流程一览 | "add → cognify → search 三步走时序" | 一致 ✓ |
| Ch13 | ch13-01-add-cognify-search.svg | 13.7 状态机 | "v1 add / cognify / search / update / delete 状态机" | 一致 ✓ |
| Ch22 | ch22-01-chat-tool-cognee.svg | 22 节引子 | "三种 Chat Tool 与 Cognee 双层记忆拓扑" | 一致 ✓ |
| Ch23 | ch23-03-11.svg | 23.6 选型决策 | "长尾 11 集成选型决策"(章节上方 23.5 节列了 11 项集成) | 一致 ✓(命名偏短但语义对得上) |
| Ch25 | ch25-01-5-cogxarchive.svg | 25.6 迁移管道 | "5 个源迁入与 COGXArchive 反向导出" | 一致 ✓(5 数字对应迁移源数) |
| Ch29 | ch29-02-semantic-memory-map.svg | 29.4 节末 | "Semantic Memory Map 数据流"(上文 29.4 全节讲该组件) | 一致 ✓ |

## MISMATCHES_FOUND

| 章节文件 | 行号 | 引用的 SVG | 章节目录 | 期望章节 | 处置 |
|---|---|---|---|---|---|
| 无 | — | — | — | — | — |

**零内容错配。** 全部 38 处引用与所在章节上下文语义对齐,文件名章号与章节目录前缀 100% 对应。

## NOTES

### 通用观察

1. **文件名命名风格有差异(留观,无需修改)**:
   - "通用 / 章节首图"多采用 `chNN-01-cognee.svg`(如 ch02、ch04、ch06、ch10、ch19、ch21、ch28、ch30)或 `chNN-01-diagram.svg`(如 ch05、ch23、ch24、ch27)。
   - "专题图"采用主题化命名,如 ch07-01-datapoint-entity-edge-dataset.svg / ch20-01-claude-code-cognee-mcp-cognee-server.svg。
   - 风格不统一但每张图与所在章节语义均对得上,**没有"语义错位"的错配**。

2. **跨章同名复用(已确认是合理设计,非冗余)**:
   - `ch03-01-add-cognify-search.svg`(Ch03,3.1 节 add→cognify→search 时序图)和 `ch13-01-add-cognify-search.svg`(Ch13,13.7 节 v1 三动词状态机)文件名相同但内容分别服务"入门总览"与"v1 API 状态机"两个语境,并非误引。M11 已确认两个 SVG 二进制是各自独立绘制。

3. **数字/缩写命名(`ch23-03-11` / `ch25-01-5-cogxarchive`)**:
   - `ch23-03-11` 中的 `11` 指 23.5 节"11 集成速查表"中的 11 项集成;章节上下文也确实是"长尾 11 集成选型决策",语义自洽。
   - `ch25-01-5-cogxarchive` 中的 `5` 指迁移部分的 5 个外部源;章节上下文确实在讲 5 源迁入 + COGXArchive 反向导出,语义自洽。
   - 命名偏简但与上下文链接清楚,无需改名。

4. **SVG 二进制未读**:出于"二进制只读"原则,本审计只校验引用名/路径/章节上下文,**未对 SVG 内部坐标系或图层做 diff**。视觉一致性须由 M12 视觉验收处理。

5. **`assets/diagrams/` 完全未触碰**:整个审计期间没有对 SVG 二进制做任何新增/删除/重命名/修改。

### 已落地变更

- 无(因审计结论为 0 错配)
