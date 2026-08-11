# Appendix B — 引用清单与外部资源

> **本节定位** [用户向][开发者向] — 章节反向索引、仓库源文件映射表、外部资源链接。

## 命令 → 章节反向索引

| Command | 所在 vertical | 触发 skill | 章节 |
|---|---|---|---|
| `/3-statement-model` | financial-analysis | 3-statement-model | `./05-verticals.md` |
| `/ai-readiness` | private-equity | ai-readiness | `./05-verticals.md` |
| `/analyze-bond-basis` | lseg | bond-futures-basis | `./05-verticals.md` |
| `/analyze-bond-rv` | lseg | bond-relative-value | `./05-verticals.md` |
| `/analyze-fx-carry` | lseg | fx-carry-trade | `./05-verticals.md` |
| `/analyze-option-vol` | lseg | option-vol-analysis | `./05-verticals.md` |
| `/analyze-swap-curve` | lseg | swap-curve-strategy | `./05-verticals.md` |
| `/buyer-list` | investment-banking | buyer-list | `./05-verticals.md` |
| `/catalysts` | equity-research | catalyst-calendar | `./05-verticals.md` |
| `/cim` | investment-banking | cim-builder | `./05-verticals.md` |
| `/client-report` | wealth-management | client-report | `./05-verticals.md` |
| `/client-review` | wealth-management | client-review | `./05-verticals.md` |
| `/competitive-analysis` | financial-analysis | competitive-analysis | `./05-verticals.md` |
| `/comps` | financial-analysis | comps-analysis | `./05-verticals.md` |
| `/dcf` | financial-analysis | dcf-model | `./05-verticals.md` |
| `/dd-checklist` | private-equity | dd-checklist | `./05-verticals.md` |
| `/dd-prep` | private-equity | dd-meeting-prep | `./05-verticals.md` |
| `/deal-tracker` | investment-banking | deal-tracker | `./05-verticals.md` |
| `/debug-model` | financial-analysis | audit-xls | `./05-verticals.md` |
| `/earnings` | equity-research | earnings-analysis | `./05-verticals.md` |
| `/earnings-preview` | equity-research | earnings-preview | `./05-verticals.md` |
| `/financial-plan` | wealth-management | financial-plan | `./05-verticals.md` |
| `/ic-memo` | private-equity | ic-memo | `./05-verticals.md` |
| `/initiate` | equity-research | initiating-coverage | `./05-verticals.md` |
| `/lbo` | financial-analysis | lbo-model | `./05-verticals.md` |
| `/macro-rates` | lseg | macro-rates-monitor | `./05-verticals.md` |
| `/merger-model` | investment-banking | merger-model | `./05-verticals.md` |
| `/model-update` | equity-research | model-update | `./05-verticals.md` |
| `/morning-note` | equity-research | morning-note | `./05-verticals.md` |
| `/one-pager` | investment-banking | strip-profile | `./05-verticals.md` |
| `/portfolio` | private-equity | portfolio-monitoring | `./05-verticals.md` |
| `/ppt-template` | financial-analysis | ppt-template-creator | `./05-verticals.md` |
| `/process-letter` | investment-banking | process-letter | `./05-verticals.md` |
| `/proposal` | wealth-management | investment-proposal | `./05-verticals.md` |
| `/rebalance` | wealth-management | portfolio-rebalance | `./05-verticals.md` |
| `/research-equity` | lseg | equity-research | `./05-verticals.md` |
| `/returns` | private-equity | returns-analysis | `./05-verticals.md` |
| `/review-fi-portfolio` | lseg | fixed-income-portfolio | `./05-verticals.md` |
| `/screen` | equity-research | idea-generation | `./05-verticals.md` |
| `/screen-deal` | private-equity | deal-screening | `./05-verticals.md` |
| `/sector` | equity-research | sector-overview | `./05-verticals.md` |
| `/source` | private-equity | deal-sourcing | `./05-verticals.md` |
| `/teaser` | investment-banking | teaser | `./05-verticals.md` |
| `/thesis` | equity-research | thesis-tracker | `./05-verticals.md` |
| `/tlh` | wealth-management | tax-loss-harvesting | `./05-verticals.md` |
| `/unit-economics` | private-equity | unit-economics | `./05-verticals.md` |
| `/value-creation` | private-equity | value-creation-plan | `./05-verticals.md` |

## Skill → 章节反向索引

按 vertical 分组。详见 `./08-skills.md`。

## Agent → 章节反向索引

| Agent | 章节 | Write-holder |
|---|---|---|
| `pitch-agent` | `./06-agents.md` | `deck-writer` |
| `market-researcher` | `./06-agents.md` | `note-writer` |
| `earnings-reviewer` | `./06-agents.md` | `note-writer` |
| `meeting-prep-agent` | `./06-agents.md` | `pack-writer` |
| `model-builder` | `./06-agents.md` | `builder` |
| `gl-reconciler` | `./06-agents.md` | `resolver` |
| `month-end-closer` | `./06-agents.md` | `poster` |
| `statement-auditor` | `./06-agents.md` | `flagger` |
| `valuation-reviewer` | `./06-agents.md` | `publisher` |
| `kyc-screener` | `./06-agents.md` | `escalator` |

## 章节 → 源文件映射表

| 章节 | 源文件 |
|---|---|
| `00-introduction.md` | `README.md`, `CLAUDE.md`, `.claude-plugin/marketplace.json`, `managed-agent-cookbooks/README.md` |
| `00.5-finance-primer.md` | (原创教学性内容,不引用源文件 — 涵盖 BS/IS/CF、DCF/comps/precedents、LBO/IRR/MOIC 等基础概念) |
| `01-quickstart.md` | `README.md`, `.claude-plugin/marketplace.json`, `scripts/deploy-managed-agent.sh`, `managed-agent-cookbooks/README.md` |
| `02-architecture.md` | `README.md`, `CLAUDE.md`, `marketplace.json`, `scripts/sync-agent-skills.py`, `scripts/check.py`, `scripts/orchestrate.py`, `.githooks/pre-commit`, `.github/workflows/*.yml` |
| `03-marketplace-catalog.md` | `.claude-plugin/marketplace.json`, 各 plugin `plugin.json` × 20 |
| `04-plugin-anatomy.md` | 各 `plugin.json` × 20, `hooks/hooks.json`, `.claude/<slug>.local.md.example`, `scripts/check.py`, `scripts/version_bump.py`, `CLAUDE.md` |
| `05-verticals.md` | 9 vertical/partner 插件全部 |
| `06-agents.md` | `plugins/agent-plugins/*/agents/*.md` × 10, `managed-agent-cookbooks/<slug>/{agent.yaml, README.md, steering-examples.json, subagents/*.yaml}` × 10 |
| `07-commands.md` | `plugins/vertical-plugins/*/commands/*.md` × 47, `plugins/partner-built/lseg/commands/*.md` × 8, `claude-for-msft-365-install/commands/*.md` × 9 |
| `08-skills.md` | `plugins/vertical-plugins/*/skills/*/SKILL.md` × 55 + `plugins/partner-built/*/skills/*/SKILL.md` × 11 = 66, `skill-creator`, `scripts/sync-agent-skills.py`, `scripts/check.py` |
| `09-cookbooks.md` | `managed-agent-cookbooks/<slug>/*`, `scripts/deploy-managed-agent.sh`, `scripts/orchestrate.py`, `scripts/validate.py`, `scripts/test-cookbooks.sh` |
| `10-mcp-connectors.md` | `plugins/vertical-plugins/financial-analysis/.mcp.json`, `plugins/partner-built/{lseg,spglobal}/.mcp.json`, `comps-analysis/SKILL.md` |
| `11-microsoft-365-install.md` | `claude-for-msft-365-install/README.md`, `commands/*.md` × 9, `scripts/`, `examples/python-bootstrap/` |
| `12-development-workflow.md` | `CLAUDE.md`, `README.md`, `scripts/check.py`, `scripts/sync-agent-skills.py`, `scripts/version_bump.py`, `.githooks/pre-commit`, `.github/workflows/*.yml` |
| `13-troubleshooting.md` | `scripts/check.py`, `scripts/deploy-managed-agent.sh`, `scripts/orchestrate.py`, `scripts/validate.py`, `.github/workflows/*.yml` |

## 外部资源

### Claude 产品与 API

- [Claude Cowork](https://claude.com/product/cowork)
- [Claude Code CLI](https://claude.com/product/claude-code)
- [Claude Managed Agents API](https://docs.claude.com/en/api/managed-agents)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

### MCP Provider 官网

| Provider | 网址 |
|---|---|
| Daloopa | https://www.daloopa.com/ |
| Morningstar | https://www.morningstar.com/ |
| S&P Global / Kensho | https://www.spglobal.com/ |
| FactSet | https://www.factset.com/ |
| Moody's | https://www.moodys.com/ |
| MT Newswires | https://www.mtnewswires.com/ |
| Aiera | https://www.aiera.com/ |
| LSEG | https://www.lseg.com/ |
| PitchBook | https://pitchbook.com/ |
| Chronograph | https://www.chronograph.pe/ |
| Egnyte | https://www.egnyte.com/ |
| Box | https://www.box.com/home |

### Partner 资源

- S&P Global marketplace: https://www.marketplace.spglobal.com/
- Kensho Technologies GitHub: https://github.com/kensho-technologies
- LSEG analytics: https://www.lseg.com/

### 仓库地址

- 主仓库:https://github.com/anthropics/financial-services
- Marketplace 注册名:`claude-for-financial-services`
- License:Apache 2.0(详见仓库根 `LICENSE`)

## Source files

本附录由以下源文件衍生:

- `.claude-plugin/marketplace.json`(plugin 清单)
- `plugins/vertical-plugins/*/commands/*.md` × 47(slash command 索引)
- `plugins/partner-built/*/commands/*.md` × 8
- `claude-for-msft-365-install/commands/*.md` × 9
- `plugins/vertical-plugins/*/skills/*/SKILL.md` × 55
- `plugins/partner-built/*/skills/*/SKILL.md` × 11
- `plugins/agent-plugins/*/agents/*.md` × 10
- `managed-agent-cookbooks/<slug>/{agent.yaml, README.md, steering-examples.json, subagents/*.yaml}` × 10
- `scripts/check.py`、`scripts/deploy-managed-agent.sh`、`scripts/orchestrate.py`、`scripts/validate.py`、`scripts/sync-agent-skills.py`、`scripts/version_bump.py`、`scripts/test-cookbooks.sh`、`scripts/count-entities.sh`
- `.githooks/pre-commit`
- `.github/workflows/{plugin-validate,secret-scan,version-bump,doc-lint}.yml`

## License & Disclaimer 镜像

> **!IMPORTANT** 本仓库与本 handbook 都不构成投资、法律、税务或会计建议。这些 agent 起草分析师工作产出(模型、备忘录、研究笔记、对账结果),由合格专业人士复核。它们不做投资建议、不执行交易、不承担风险、不入账、不批准 onboarding。每个产物都待人工签字。你负责验证输出与遵守适用的法律法规。

License: Apache License 2.0 — 详见仓库根 `/LICENSE`。

## Cross-references

- 回到 handbook 起点 → `./README.md`
- 仓库地址 → 上方"仓库地址"段
- 完整术语表 → `./appendix-a-glossary.md`
- 修订记录 → `./appendix-c-changelog.md`