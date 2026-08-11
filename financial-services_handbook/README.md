# Handbook — Claude for Financial Services

> **Pinned to repo state**: `38652224c10610fa52eee2acee3ac712dcff01f2` (2026-08-11)
>
> 一本 ~200+ 页的用户手册,涵盖 20 个插件 / 66 个 skill(55 vertical + 11 partner)/ 56 个 slash command / 12 个 MCP connector / 10 个 Managed Agent cookbook。

## 这是什么?

`docs/handbook/` 目录下是为 [`/Users/digoal/new/financial-services`](https://github.com/anthropics/financial-services) 仓库编写的用户手册。该仓库是 **"Claude for Financial Services"** —— 面向金融行业(投行 / 股权研究 / PE / WM / 基金会计 / 运营)的参考代理、技能与数据连接器。

同一个 source 既可作为 [Claude Cowork](https://claude.com/product/cowork) 插件安装,也可通过 [Claude Managed Agents API](https://docs.claude.com/en/api/managed-agents) 部署到企业后端。本 handbook 完整覆盖两种使用方式。

## 谁适合读?

| 角色 | 标签 | 看什么 |
|---|---|---|
| **终端用户**(分析师 / 运营) | `[用户向]` | 安装、命令调用、skill 自动触发、典型场景 |
| **开发者 / 二次定制 / 贡献者** | `[开发者向]` | 文件结构、manifest schema、CI / hooks、加新内容 |
| **IT 管理员**(M365 部署) | `[运维向]` | Claude Office add-in 配置 |

## 怎么读?三档路径

```text
速通 (5 分钟)                  实用 (1 小时)                    进阶 (1 天开发者)
00-introduction                00-introduction                  00-introduction
00.5-finance-primer ★         00.5-finance-primer ★           00.5-finance-primer ★
01-quickstart                  01-quickstart                    02-architecture
03-marketplace-catalog         02-architecture (Lite)           04-plugin-anatomy
                               05-verticals (你用的)            12-development-workflow
                               07-commands (你用的)             13-troubleshooting
                               08-skills (你用的)               09-cookbooks
                                                            + 全部章节

★ 如果你是财务外行(不懂 BS/IS/CF、DCF、LBO、CIM、MOIC、IC memo 等),
  强烈建议先读 00.5-finance-primer(零基础入门,15-20 分钟)。
  已经在金融行业的读者可跳过。
```

## 目录(每章节一句话 + 角色标签)

| 章节 | 标题 | 角色 | 字数目标 |
|---|---|---|---|
| [`00-introduction.md`](./00-introduction.md) | 仓库是什么 / 谁适合读 / 三种分发渠道 | both | 1800 |
| **[`00.5-finance-primer.md`](./00.5-finance-primer.md)** | **财务入门 — 给非财务背景读者(财报/估值/角色/IB/PE/WM/Fund Admin)** | **用户向** | **5000** |
| [`01-quickstart.md`](./01-quickstart.md) | 5 分钟跑通第一个命令(Cowork / Code / Managed Agent) | 用户向 | 2200 |
| [`02-architecture.md`](./02-architecture.md) | 插件模型 / One source two wrappers / 同步机制 / 版本管理 | both | 2500 |
| [`03-marketplace-catalog.md`](./03-marketplace-catalog.md) | 全部 20 个插件速查 + 选型决策树 | 用户向 | 1800 |
| [`04-plugin-anatomy.md`](./04-plugin-anatomy.md) | 目录结构 / manifest 字段 / version / frontmatter | 开发者向 | 2200 |
| [`05-verticals.md`](./05-verticals.md) | 7 个 vertical + 2 个 partner 完整拆解 | both | 2500 |
| [`06-agents.md`](./06-agents.md) | 10 个命名代理深度拆解(含 Managed Agent 拓扑) | both | 2800 |
| [`07-commands.md`](./07-commands.md) | 56 个 slash command 目录与两种模板 | both | 2000 |
| [`08-skills.md`](./08-skills.md) | 66 个 skill 目录与 3 种 archetype(55 vertical + 11 partner)| both | 2200 |
| [`09-cookbooks.md`](./09-cookbooks.md) | Managed Agent 部署实战(orchestrator + subagent + handoff) | both | 2500 |
| [`10-mcp-connectors.md`](./10-mcp-connectors.md) | 12 个数据连接器 | both | 2200 |
| [`11-microsoft-365-install.md`](./11-microsoft-365-install.md) | IT 管理员部署 Claude Office add-in | 运维向 | 1800 |
| [`12-development-workflow.md`](./12-development-workflow.md) | Fork / 加 skill / 加 agent / 加 vertical / CI / hooks | 开发者向 | 2200 |
| [`13-troubleshooting.md`](./13-troubleshooting.md) | 常见问题 + 已知 bug | both | 2000 |
| [`appendix-a-glossary.md`](./appendix-a-glossary.md) | 术语表(金融 / 技术 / 仓库 / Legal) | both | 1500 |
| [`appendix-b-references.md`](./appendix-b-references.md) | 命令/技能反向索引 + 源文件映射表 + 外部资源 | both | 1000 |
| [`appendix-c-changelog.md`](./appendix-c-changelog.md) | 修订记录 + 不可变约束清单 | both | 600 |

**预计总字数**: ~31–42K 字(原计划 30–40K,加入 00.5 财务入门)→ ~210+ 页。

## 仓库统计速览

| 维度 | 数量 |
|---|---|
| 全部 .md 文件 | 228 |
| SKILL.md 总数(含 vendored) | ~88 |
| 独特 skill | 66 |
| Slash command 总数 | ~50(FSI)+ 9(M365 admin) |
| `.mcp.json` 总数 | 5 |
| cookbook | 10 |
| subagent yaml | 30 |
| 7 个 repo 脚本 | `check.py` · `deploy-managed-agent.sh` · `validate.py` · `orchestrate.py` · `sync-agent-skills.py` · `version_bump.py` · `test-cookbooks.sh` |
| 3 个 GitHub workflow | `plugin-validate.yml` · `secret-scan.yml` · `version-bump.yml` |
| 1 个 git hook | `pre-commit` (自动 bump version) |

## 重要免责声明

> **!IMPORTANT** 本仓库与本 handbook 都不构成投资、法律、税务或会计建议。这些 agent 起草分析师工作产出(模型、备忘录、研究笔记、对账结果),由合格专业人士复核。它们不做投资建议、不执行交易、不承担风险、不入账、不批准 onboarding。每个产物都待人工签字。你负责验证输出与遵守适用的法律法规。

(此声明与仓库根 `README.md` L7–9 完全一致,完整 License 见仓库根 `/LICENSE`。)

## 图表与代码风格约定

- **ASCII 框图**:每个章节起始位置
- **Mermaid 块**:用于流程 / 时序 / 状态图(` ```mermaid ` 栅栏,GitHub/Cowork 原生渲染)
- **复杂 Mermaid**:放在 `assets/mermaid/*.mmd` 文件,章节内用 ` ![diagram](assets/mermaid/foo.mmd) ` 引用
- **ASCII 重复图**:放在 `assets/ascii/*.txt`
- **代码块**:用 ASCII 字符(`.ps1` 红线扩展到 handbook 的代码块)
- **角色标签**:`[用户向]` / `[开发者向]` / `[运维向]` / `both`
- **中文 / 英文混排**:中文叙述 + 英文术语原文,无 emoji

## 版本绑定与新鲜度

本 handbook 与仓库 commit SHA 绑定:

```bash
# 当前绑定
git rev-parse HEAD
# 38652224c10610fa52eee2acee3ac712dcff01f2
```

当仓库有新 commit(尤其是 plugin.json version bump 或新 skill/command/cookbook),受影响章节需要同步更新。详见 `12-development-workflow.md` 的 "PR review checklist" 段。

## Cross-references

- 完整术语 → `appendix-a-glossary.md`
- 反向索引 + 源文件映射 → `appendix-b-references.md`
- 修订记录 → `appendix-c-changelog.md`
- 仓库根 README(开发者向) → `/Users/digoal/new/financial-services/README.md`
- 仓库根 CLAUDE.md(贡献者向) → `/Users/digoal/new/financial-services/CLAUDE.md`

## Source files

本 handbook 内容蒸馏自以下源文件(每个章节的"Source files"段也列出):

- `README.md`(仓库根)
- `CLAUDE.md`(仓库根)
- `LICENSE`(仓库根,Apache-2.0)
- `.claude-plugin/marketplace.json`
- `plugins/agent-plugins/<slug>/{agents,skills,.claude-plugin}/` × 10
- `plugins/vertical-plugins/<slug>/{commands,skills,.claude-plugin,.mcp.json,hooks}/` × 7
- `plugins/partner-built/{lseg,spglobal}/` × 2
- `managed-agent-cookbooks/<slug>/{agent.yaml,README.md,steering-examples.json,subagents/}` × 10
- `claude-for-msft-365-install/{commands,scripts,examples}/`
- `scripts/{check,deploy-managed-agent.sh,validate,orchestrate,sync-agent-skills,version_bump,test-cookbooks}.{py,sh}`
- `.githooks/pre-commit`
- `.github/workflows/{plugin-validate,secret-scan,version-bump}.yml`