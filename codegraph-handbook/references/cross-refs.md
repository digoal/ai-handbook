# 跨章引用表

本表记录所有 `{{chapter:NN}}` 形式的内部引用,确保每条引用都指向已存在的章节文件。

## 引用清单(扫描自 chapters/*.md)

> 扫描时间:2026-07-27 · 引用总数:48 条(16 个不同目标)

| 源章节 | 引用目标 | 目标文件 | 引用类型 |
|--------|----------|----------|----------|
| 00-preface | {{chapter:1}} | 01-background.md | 跳转 |
| 00-preface | {{chapter:2}} | 02-quickstart.md | 跳转 |
| 00-preface | {{chapter:6}} | 06-mcp-tools-manual.md | 跳转 |
| 00-preface | {{chapter:9}} | 09-case-studies.md | 跳转 |
| 00-preface | {{chapter:10}} | 10-process-topology.md | 跳转 |
| 00-preface | {{chapter:11}} | 11-schema-deep-dive.md | 跳转 |
| 00-preface | {{chapter:12}} | 12-rust-kernel.md | 跳转 |
| 00-preface | {{chapter:13}} | 13-context-pipeline.md | 跳转 |
| 00-preface | {{chapter:14}} | 14-mcp-three-modes.md | 跳转 |
| 00-preface | {{chapter:15}} | 15-evaluation.md | 跳转 |
| 00-preface | {{chapter:16}} | 16-contributing.md | 跳转 |
| 01-background | {{chapter:2}} | 02-quickstart.md | 跳转 |
| 02-quickstart | {{chapter:3}} | 03-install-and-integrate.md | 跳转 |
| 03-install-and-integrate | {{chapter:2}} | 02-quickstart.md | 回引 |
| 03-install-and-integrate | {{chapter:4}} | 04-config-reference.md | 跳转 |
| 04-config-reference | {{chapter:3}} | 03-install-and-integrate.md | 回引 |
| 04-config-reference | {{chapter:5}} | 05-claude-code-patterns.md | 跳转 |
| 05-claude-code-patterns | {{chapter:6}} | 06-mcp-tools-manual.md | 跳转 |
| 07-cli-manual | {{chapter:6}} | 06-mcp-tools-manual.md | 跳转 |
| 07-cli-manual | {{chapter:8}} | 08-sync-and-watcher.md | 跳转 |
| 08-sync-and-watcher | {{chapter:9}} | 09-case-studies.md | 跳转 |
| 08-sync-and-watcher | {{chapter:10}} | 10-process-topology.md | 跳转 |
| 09-case-studies | {{chapter:6}} | 06-mcp-tools-manual.md | 跳转 |
| 09-case-studies | {{chapter:10}} | 10-process-topology.md | 跳转 |
| 10-process-topology | {{chapter:6}} | 06-mcp-tools-manual.md | 跳转 |
| 10-process-topology | {{chapter:11}} | 11-schema-deep-dive.md | 跳转 |
| 10-process-topology | {{chapter:14}} | 14-mcp-three-modes.md | 跳转 |
| 11-schema-deep-dive | {{chapter:12}} | 12-rust-kernel.md | 跳转 |
| 12-rust-kernel | {{chapter:11}} | 11-schema-deep-dive.md | 跳转 |
| 12-rust-kernel | {{chapter:13}} | 13-context-pipeline.md | 跳转 |
| 13-context-pipeline | {{chapter:11}} | 11-schema-deep-dive.md | 跳转 |
| 13-context-pipeline | {{chapter:14}} | 14-mcp-three-modes.md | 跳转 |
| 14-mcp-three-modes | {{chapter:10}} | 10-process-topology.md | 跳转 |
| 14-mcp-three-modes | {{chapter:15}} | 15-evaluation.md | 跳转 |
| 15-evaluation | {{chapter:11}} | 11-schema-deep-dive.md | 跳转 |
| 15-evaluation | {{chapter:16}} | 16-contributing.md | 跳转 |
| 16-contributing | {{chapter:12}} | 12-rust-kernel.md | 跳转 |
| 16-contributing | {{chapter:15}} | 15-evaluation.md | 跳转 |
| 16-contributing | {{chapter:17}} | 17-glossary.md | 跳转 |
| 18-faq | {{chapter:16}} | 16-contributing.md | 跳转 |

## 引用规则

1. 任何指向其他章节的内部链接统一用 `{{chapter:NN}}` 形式(NN 为两位数,补零)
2. 主会话在每次 subagent 返回后扫描 `chapters/*.md`,提取所有 `{{chapter:NN}}` 引用
3. 引用更新后必须用 `ls chapters/` 验证目标文件存在
4. 失效引用(目标文件缺失)必须修复或在下一轮 plan 中标注

## 叶子章节(无引用,作为被引用末端)

- **Ch07** CLI 命令手册 — 叶子(除外部被引外)
- **Ch17** 术语表 — 叶子(被 Ch16 引用)
- **Ch18** FAQ — 叶子(只引用 Ch16)
- **Ch06** MCP 工具手册 — 多次被引(Ch05/Ch07/Ch09/Ch10)

## 验证状态

- 2026-07-27: 16 个目标全对应存在文件(ls chapters/ 19 个 .md 全部存在)
- 0 失效引用
- 48 条已分类引用
