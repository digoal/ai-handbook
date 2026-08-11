# Appendix A — 术语表(Glossary)

> **本节定位** [用户向][开发者向] — 仓库涉及的所有缩写与术语的快速查询。

## 金融术语

| Term | Definition |
|---|---|
| **DCF** | Discounted Cash Flow,现金流贴现估值方法 |
| **LBO** | Leveraged Buyout,杠杆收购模型 |
| **MOIC** | Multiple on Invested Capital,投资倍数(总退出价值 / 总投入) |
| **IRR** | Internal Rate of Return,内部收益率 |
| **NRR** | Net Revenue Retention,净收入留存率 |
| **TLH** | Tax-Loss Harvesting,税收损失收割(年末常用) |
| **ARR** | Annual Recurring Revenue,年度经常性收入 |
| **Rule of 40** | SaaS 指标:增长率 + 利润率 ≥ 40% |
| **EV** | Enterprise Value,企业价值(= 股权市值 + 净负债) |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization,息税折旧摊销前利润 |
| **WACC** | Weighted Average Cost of Capital,加权平均资本成本 |
| **Beta** | 股票相对市场的波动性 |
| **Sharpe / Sortino** | 风险调整后收益指标 |
| **IC** | Investment Committee,投资委员会 |
| **CIM** | Confidential Information Memorandum,保密信息备忘录 |
| **OM** | Offering Memorandum,发行备忘录 |
| **DAC** | Days After Close,交割后天数 |
| **GP / LP** | General Partner / Limited Partner,基金普通合伙人 / 有限合伙人 |
| **NAV** | Net Asset Value,净资产价值 |
| **PE / VC** | Private Equity / Venture Capital |
| **IB / ER / WM** | Investment Banking / Equity Research / Wealth Management |
| **KYC / AML** | Know Your Customer / Anti-Money Laundering |
| **GL recon** | General Ledger Reconciliation,总账对账 |
| **Break trace** | 对账差异的根因追溯 |

## 技术 / 仓库术语

| Term | Definition |
|---|---|
| **MCP** | Model Context Protocol,让 Claude 调外部数据源的协议 |
| **CLI** | Command-Line Interface |
| **Hook** | Git hook / Claude hook,在事件触发时执行 |
| **pre-commit** | commit 前的 git hook |
| **Cowork** | Anthropic 的 SaaS 协作产品,装 plugin 后用 |
| **Claude Code** | Anthropic 的 CLI 工具 |
| **Managed Agent** | Anthropic 的 headless agent 部署 API(`POST /v1/agents`) |
| **steering event** | 喂给 agent session 的输入事件 |
| **`handoff_request`** | 一个 agent 在输出里请求路由到另一个 agent 的 JSON 事件 |
| **`callable_agents`** | 在 agent.yaml 里声明可调的 subagent 列表 |
| **Orchestrator** | 顶层 agent,负责调度 |
| **Leaf worker** | depth-1 子代理,不调其他 subagent |
| **depth-1** | 调用深度 = 1(orchestrator → worker,worker 不再调) |
| **Write-holder** | cookbook 里唯一有 `write` 工具的 worker |

## 仓库特定术语

| Term | Definition |
|---|---|
| **Vertical** | 业务领域(投行 / 股权研究 / PE / WM / 基金会计 / 运营) |
| **Agent plugin** | `plugins/agent-plugins/<slug>/`,Cowork 端的端到端工作流 |
| **Partner-built** | `plugins/partner-built/<slug>/`,外部 partner 维护 |
| **cookbook** | `managed-agent-cookbooks/<slug>/`,Managed Agent 部署清单 |
| **subagent** | cookbook 下的 leaf worker(`subagents/*.yaml`) |
| **Vendored copy** | agent bundle 下的 skill,与 vertical source 是同一份 |
| **Source of truth** | vertical 下的 skill,被 agent bundle 引用 |
| **Skill** | `SKILL.md` 里的领域知识 + 工作流 |
| **Command** | slash command(`/commands/<cmd>.md`),显式触发 |
| **plugin** | `.claude-plugin/plugin.json` 注册的元数据 |
| **Marketplace** | `.claude-plugin/marketplace.json` 注册的 plugin 集合 |
| **Marketplace slug** | `claude plugin install <slug>@<marketplace-name>` |
| **Anthropic FSI** | Anthropic Financial Services Internal(主流作者) |
| **Anthropic** | `investment-banking` vertical 独有作者字段 |
| **LSEG** | partner `lseg` 的作者 |
| **Kensho Technologies** | partner `sp-global` 的作者 |
| **Skill sync** | `scripts/sync-agent-skills.py`,vertical → bundle 单向同步 |
| **Drift detection** | `check.py` 检测 bundle 与 source 不一致 |
| **One source two wrappers** | 同一份源同时给 Cowork 与 Managed Agent 用 |
| **Output schema** | `subagents/*.yaml` 里的 `output_schema:` 块,强制 JSON 结构 |
| **Allowed targets** | `scripts/orchestrate.py` 里允许的 handoff 目标 agent 集合 |
| **version-bump** | `scripts/version_bump.py` + pre-commit hook,自动 patch bump |
| **Patch bump** | 0.1.0 → 0.1.1,修复 / 文案 |
| **Minor bump** | 0.1.0 → 0.2.0,新功能 |
| **Major bump** | 0.1.0 → 1.0.0,破坏性变更 |

## plugin slug ↔ displayName

| Slug | displayName |
|---|---|
| financial-analysis | Financial Analysis |
| investment-banking | Investment Banking |
| equity-research | Equity Research |
| private-equity | Private Equity |
| wealth-management | Wealth Management |
| fund-admin | Fund Administration |
| operations | Operations |
| pitch-agent | Pitch Agent |
| market-researcher | Market Researcher |
| earnings-reviewer | Earnings Reviewer |
| meeting-prep-agent | Meeting Prep Agent |
| model-builder | Model Builder |
| gl-reconciler | GL Reconciler |
| kyc-screener | KYC Screener |
| valuation-reviewer | Valuation Reviewer |
| month-end-closer | Month-End Closer |
| statement-auditor | Statement Auditor |
| lseg | LSEG |
| sp-global | S&P Global |
| claude-for-msft-365-install | Claude for Microsoft 365 Install |

## ASCII 词汇卡(速记)

```text
+-------+          +-------+          +-------+
|  FSI  |  ====>   | Skill |  ====>   |  MCP  |
| User  |   runs   | file  |   reads  |  data |
+-------+          +-------+          +-------+
   |                  |                  |
   v                  v                  v
/comps           audit-xls        CapIQ / FactSet
/dcf             lbo-model         Daloopa / Moody's
/earnings        dcf-model        LSEG / MT Newswires
```

## Legal

> **!IMPORTANT** 本仓库与本 handbook 都不构成投资、法律、税务或会计建议。这些 agent 起草分析师工作产出(模型、备忘录、研究笔记、对账结果),由合格专业人士复核。它们不做投资建议、不执行交易、不承担风险、不入账、不批准 onboarding。每个产物都待人工签字。你负责验证输出与遵守适用的法律法规。

(此声明与仓库根 `README.md` L7–9 完全一致。)

## Cross-references

- 仓库整体心智 → `./README.md`
- 完整 20 插件 → `./03-marketplace-catalog.md`
- 每个 agent 的安全 tier → `./06-agents.md`
- cookbook 字段详解 → `./09-cookbooks.md`

## Source files

- `README.md`(L1–L262,基本所有术语源头)
- `.claude-plugin/marketplace.json`(20 个 plugin 名字)
- `scripts/orchestrate.py`(L23–L27,Allowed targets 列表)
- `managed-agent-cookbooks/README.md`(L7–L18,10 agent 总览)