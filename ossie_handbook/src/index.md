<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
-->

# Apache Ossie 全景手册

> **Abstract** — Apache Ossie (formerly OSI) is a vendor-neutral semantic-model specification backed by 11 vendor converters (9 Python + 2 Java), a Python Pydantic v2 SDK, and a Go CLI dispatcher. This handbook is a 22-chapter deep-dive (14 spec/SDK/CLI/governance chapters + 6 v1.1 supplementary chapters + 2 v1.3 reference chapters: error catalog + API reference) into the spec, the converters, the Python SDK, the Go CLI, the ontology layer, and Apache governance — aimed at three audiences (users, developers, architects) with 30+ Mermaid diagrams, 60+ code blocks, and 56 glossary terms. v1.3 adds 5 root governance files (CHANGELOG/SECURITY/CoC/GOVERNANCE/RELEASE_NOTES), a handbook CI workflow (mkdocs strict + lychee + codespell), and discoverability (sitemap + RSS + Open Graph). Generated from the apache/ossie repository at tag handbook-v1.3.

> **语义互操作规范、转换器与生态实践**

[![License](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Spec](https://img.shields.io/badge/spec-0.2.0.dev0-orange.svg)](https://github.com/apache/ossie)
[![Repo](https://img.shields.io/badge/repo-apache%2Fossie-blueviolet)](https://github.com/apache/ossie)

本手册基于 apache/ossie 仓库当前内容（commit `88e0011` 及以后）系统分析 Apache Ossie（前身 **OSI — Open Semantic Interchange**）。Ossie 是 Apache 孵化中的供应商中立语义模型规范，旨在解决数据分析、AI、BI 生态中长期存在的"语义碎片化"问题。

## 这本手册面向谁

| 读者 | 你将获得的收获 |
|---|---|
| 🧑‍💻 **用户**（数据工程师、分析师） | 从零写出一份合规的 Ossie 语义模型；用 `validate.py` 校验；用 converter 部署到 Snowflake / dbt / Databricks / GoodData 等工具 |
| 🛠️ **开发者**（converter 作者、SDK 贡献者） | 深入理解核心规范、Pydantic 类型系统、Java pipeline 架构、CLI 插件协议；获得"如何写一个新 converter"的完整 recipe |
| 🏛 **架构师**（技术负责人、治理者） | 理解 hub-and-spoke 设计取舍、spec 演进路线图、Apache 治理流程、与 dbt Semantic Layer / Cube / LookML 的对比定位 |

每个章节顶部都有三类读者的 **【为用户】【为开发者】【为架构师】** 一句话侧栏；章末是三栏速查表。读者可以只看侧栏决定要不要深入。

## 阅读路径

> 阅读路径图（含三类读者侧栏）详见 [00-序章.md](00-序章.md) §0.3。简版导航：

- **用户最小集**：序章 → 第 1 章 → 第 2 章 → 第 4 章 → [quickstart](quickstart.md) → 第 7 章（选 1–2 个） → 第 10 章 → [troubleshooting](troubleshooting.md)（按需）
- **开发者最小集**：序章 → 第 1 章 → 第 2 章 → 第 5 章 → 第 6 章 → 第 7 章（全部） → 第 8 章 → 第 9 章 → [comparisons](comparisons.md)
- **架构师最小集**：序章 → 第 1 章 → 第 2 章 → 第 6 章 → 第 7 章 → 第 10 章 → 第 11 章 → [reference-architectures](reference-architectures.md) → [performance-and-scale](performance-and-scale.md) → [case-studies](case-studies.md)

## 关于仓库当前状态

> ⚠️ **实现状态提醒**：仓库当前 spec 版本 `0.2.0.dev0`（开发中），已发布版本 `0.1.1`（2025-12-11）。`core-spec/spec.md:22` 明确标注 "DRAFT version — schema may change before 0.2.0 is released"。Go CLI 中的 `convert`/`validate`/`plugin install`/`plugin remove` 仍是 stub（`cli/cmd/*.go`），仅有 `plugin list` 是已实现功能。`compliance/` 目录仅有 20 行占位 README。本手册所有引用都基于仓库当前文件；任何"未实现"或"DRAFT"部分都已显式标注。

## 仓库关键数字（2026 年 8 月快照）

| 维度 | 数值 |
|---|---|
| Converter 总数 | **11**（9 Python + 2 Java） |
| 总测试数（converter） | **699** |
| 核心规范 JSON Schema | 352 行（Draft 2020-12） |
| 表达式语言提案 | 780 行（`Ossie_SQL_2026` Proposed Final） |
| TPC-DS 示例 | 631 行 / 5 dataset / 5 metric |
| Flights 本体示例 | 1111 行 / 44 concept / 12 entity + 32 value type |
| Python SDK 模型 | 223 行 / 14 公开类型 |
| CI 工作流 | 11 条（CLI 1 条 + converter 10 条；Wisdom 暂无 CI） |
| 参与者组织 | **50+**（见 [docs/index.md](https://ossie.apache.org/)） |

## 鸣谢

本手册内容基于 Apache Ossie 仓库的开放规范、源代码与社区文档整理，遵循 Apache License 2.0。所有 verbatim 引用均标注 `path:line` 溯源，便于读者跳转 GitHub 验证。

— 手册维护：仓库分析自动生成于 2026-08-10