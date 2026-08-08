# 章节模板(给所有写作子 Agent)

> 每个章节文件必须遵循开头/结尾固定块,中间自由发挥。
> 引用代码、文件、章节必须使用绝对路径。

## 章节开头模板(必须)

```markdown
# 第 X 章 `<英文标题>`

> 本章目标:读完本章,你将能够
> - 能力 1
> - 能力 2
> - 能力 3

## 前置知识
- 已读完 Ch0X:`<章节中文名>`(链接:`./chapter-XX-...md`)
- 需要的基础库:`cognee>=1.4.0`、`pydantic>=2.0`、`asyncio`
- 环境:Python 3.10–3.14

## 本章导览
- 一级节 1:简短说明
- 一级节 2:简短说明
- 一级节 3:简短说明

---

## X.1 一级节 1

正文段落,先讲 Why 再讲 How。

### X.1.1 二级节

代码示例:

\`\`\`python
import asyncio
import cognee

async def main():
    await cognee.add("LangChain 是一个 LLM 编排框架")
    await cognee.cognify()
    results = await cognee.search("LangChain 是什么", "GRAPH_COMPLETION")
    print(results)

asyncio.run(main())
\`\`\`

引用源码(给出绝对路径):
> 关键实现见 `<COGNEE_REPO>/cognee/api/v1/cognify/cognify.py` 第 80–120 行。

### X.1.2 mermaid 图

\`\`\`mermaid
%% title: ChXX — 图名
graph LR
    A[概念] --> B[数据]
\`\`\`

---

## X.2 一级节 2

...

---

## X.3 一级节 3

...

---

## 小结

- 关键要点 1
- 关键要点 2
- 关键要点 3

## 实践作业

1. **(基础)** 完成 X.X 节的代码示例
2. **(进阶)** 在 `examples/guides/...` 上跑通修改版
3. **(挑战)** 把代码改成自定义 SearchType

## 推荐阅读

- [[chapter-XX-related|第 X 章 相关章节]](./chapter-XX-...md)
- 源码:`<COGNEE_REPO>/cognee/...`
- 论文:Markovic 2025, *Optimizing the Interface Between Knowledge Graphs and LLMs*, arXiv:2505.24478
- 示例:`<COGNEE_REPO>/examples/...`
```

## 章节结尾模板(必须)

```markdown
## 下一章预告

第 X+1 章将介绍 ...(用一句话引出下一章主题)。
```

## 章节长度规范

| 篇 | 章节 | 推荐字数 |
|---|---|---|
| Part I · 基础认知 | Ch01-Ch05 | 2000-3000 字/章 |
| Part II · 架构深潜 | Ch06-Ch12 | 3000-4500 字/章 |
| Part III · API 与检索 | Ch13-Ch18 | 2500-3500 字/章 |
| Part IV · 集成与生态 | Ch19-Ch23 | 2500-4000 字/章 |
| Part V · 实战与运维 | Ch24-Ch30 | 2500-3500 字/章 |

全书目标 ~12-15 万字,30 章。

## 必须出现的元素

- [ ] mermaid 图(每章至少 1 张,Ch15/Ch20 至少 2 张)
- [ ] 至少 2 个可运行的 Python 代码片段(可在默认主路径跑通)
- [ ] 至少 3 个真实代码路径引用(`<COGNEE_REPO>/...`)
- [ ] "前置知识"区块指向具体章节文件
- [ ] "推荐阅读"双向链接
- [ ] "小结"3-5 条要点
- [ ] "实践作业"基础 + 进阶 + 挑战三档

## 写作风格

- 段落以"为什么这样做"开头,再讲"怎么做"
- 术语首次出现给中英文对照
- 代码必须可运行,不要出现虚构的 API 名
- 不要长篇引用英文 docstring,而是提炼要点
- 对比/选型用表格呈现
- 实战场景以"我有一个 X 问题 → 用 cognee 的 Y API 解决"叙述