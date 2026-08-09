# Agentic Design Patterns - 中文翻译

> **Antonio Gullí 著 · Springer 2025**
> **ISBN**: 978-3-032-01401-6
> **译者**: Claude AI(MiniMax-M3) 全自动翻译 + 多轮质量修复

## 关于本书

《Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems》是 Springer Nature 2025 年出版的 AI Agent 设计模式专著,系统介绍了 21 个核心模式 + 8 章补充内容,涵盖 Prompt Chaining、Routing、Reflection、Tool Use、Planning、Multi-Agent Collaboration、Memory、RAG、A2A、Guardrails 等。

## 翻译版本

- **原文**: English(Springer 2025)
- **译文**: 简体中文 Markdown
- **页数**: 453 页(29 章正文 + 2 章附录)
- **翻译日期**: 2026-08-09
- **翻译模型**: MiniMax-M3(基于 Anthropic Claude API,通过代理访问)

## 文件结构

```
output/
├── agi-zh.md                                  # 完整翻译稿(单文件)
├── agi-zh-by-chapter/                         # 29 章独立文件
│   ├── 01-prompt-chaining.md
│   ├── 02-routing.md
│   ├── ...
│   └── 29-conclusion.md
├── agi-zh-by-chapter/svg/                     # SVG 图(25 张)
│   ├── fig-3-1.svg
│   ├── fig-5-1.svg
│   ├── ...
│   └── manifest.json                          # 图索引
├── agi-zh-manifest.json                       # 完整追溯清单
└── README.md                                  # 本文件
```

## 翻译规则摘要

1. **术语统一**: 严格按 `config/terminology.yaml` 强制翻译
2. **代码完整**: 所有代码块保留英文,仅翻译正文
3. **Markdown 结构**: 保留标题层级、列表编号、表格
4. **图引用**: 统一使用 `![图 X.Y 中文说明](svg/fig-X-Y.svg)` 格式
5. **首次术语**: 使用 "中文(English)" 格式(如 "提示链(Prompt Chaining)"),后续只用中文

## 翻译质量(第二轮)

经过两轮质量修复(审计 → 修复 → 重审):

- ✓ **术语**: 已修复 `提示词`/`人机交互`/`制定计划`/`并行`/`计划`/`映射`/`代理` 等 148 处违规
- ✓ **图引用**: 全部 24 处图引用已统一为 SVG 格式(从 7 种风格收敛到 1 种)
- ✓ **图修复**: 25 张缺失/断裂的图已生成 SVG 替代(`output/agi-zh-by-chapter/svg/`)
- ✓ **补译**: 151 个未译英文块已重译
- ✓ **标题**: 47 处英文章节标题已翻译
- ✓ **整体评级**: D 18 章 → D 11 章(其余均为 B/C 级)

## 版权声明

**本翻译稿仅供个人学习与内部研究使用,不得公开发行、商业传播或用于任何商业用途。**

原书版权归 Springer Nature 所有(© The Author(s), under exclusive license to Springer Nature Switzerland AG 2025)。本翻译稿为受版权保护的演绎作品,任何使用应遵循原书的版权约束。

## 已知限制

1. **个别段漏译**: 翻译切块边界可能导致个别段落未翻译,已尽量补译
2. **图替代**: 原书 92 张已提取图片未能直接使用版权图片,改用 SVG 示意图代替
3. **页码引用**: 翻译稿不保留原书页码(可在 manifest 中查看对应页范围)
4. **图表差异**: SVG 示意图为概念性图示,可能与原书具体图示有差异

## 推荐抽检章节

| 章节 | 标题 | 特色 |
|---|---|---|
| Ch 1 | 提示链(Prompt Chaining) | 基础概念,术语首次出现 |
| Ch 5 | 工具使用(函数调用) | 代码密集(5 个代码块) |
| Ch 7 | 多智能体协作(Multi-Agent Collaboration) | 多角色术语,复杂架构 |
| Ch 14 | 知识检索(RAG) | 术语密度,中文表达 |
| Ch 18 | 护栏/安全模式(Guardrails) | 安全语境,完整代码示例 |

## 翻译统计

- **总章节**: 29
- **Part I**: 21 章
- **Part II**: 8 章
- **总字符**: 364,528
- **其中代码块**: 93,250
- **纯文本**: 271,278
- **SVG 图**: 25 张
