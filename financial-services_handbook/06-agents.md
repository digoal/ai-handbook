# 06. 命名代理 — 10 个端到端工作流深度拆解

> **本节定位** [用户向][开发者向] — 仓库里 10 个命名代理的完整拆解:定位、工具权限、Workflow、Guardrails、bundled skills、Managed Agent 拓扑。

> **术语外行?** 本章出现的 finance 术语(DCF / LBO / MOIC / IC memo / CIM / NAV / AUM / GP / LP / carry / KYC 等)详见 [`00.5-finance-primer.md`](./00.5-finance-primer.md)。

## TL;DR

- **10 个 agent** = 仓库的核心工作流单位。**每个 agent 一份系统提示词** + 一组 vendored skills + 一个 Managed Agent cookbook(orchestrator + 3 subagent)。
- **典型 agent 都有 9 节模板**:定位 → 适用 → 工具 → Workflow → 输入/输出 → bundled skills → Guardrails → cookbook 拓扑 → 跨 agent handoff。
- **安全模式**:orchestrator 几乎从不直写文件,**恰好一个** subagent 是 Write-holder(deck-writer / resolver / note-writer / pack-writer / poster / publisher / flagger / escalator / builder 之一)。
- **untrusted document**:触达外部文档的 agent(reader / doc-reader / package-reader / statement-reader / transcript-reader / ledger-reader / profiler / news-reader / sector-reader / data-puller)都只读不写,tools=read+grep,output_schema 严约束 JSON。

## What you'll learn

- 10 个 agent 的能力边界与典型用法
- 每个 agent 的工具权限(`tools:` 行)
- 每个 agent 在 Managed Agent 模式下的 orchestrator + 3 subagent 拓扑
- 跨 agent handoff 链路
- 安全护栏(Guardrails)与不可信文档处理

## 第一个 agent — 在 Cowork 跑 pitch-agent

```bash
# 1. 装 agent(前置要装 financial-analysis)
claude plugin install financial-analysis@claude-for-financial-services
claude plugin install pitch-agent@claude-for-financial-services

# 2. 进入 session
claude

# 3. 用自然语言让 agent 跑起来
> 帮我用 pitch-agent 给 CRWD 出 first-draft pitch book,
  thesis 是 platform consolidation in security
```

预期产出:`./pitch-CRWD-<date>.xlsx` + `./pitch-CRWD-<date>.pptx`,每个数字 traceable 到 Excel cell。详细见 `01-quickstart.md` 与 `09-cookbooks.md`。

---

## 6.1 [用户向] pitch-agent(旗舰示例)

**一句话定位**: 投行 end-to-end pitch agent — 给 target + situation,自动拉 comps + precedents + LBO + DCF + football field,产出一份 Excel + 一份品牌化 PPT deck。

- **适用**: MD/资深 banker 要"first-draft pitch on a name"
- **不适用**: 编辑已有 deck(用 `pitch-deck` skill)
- **版本**: 0.1.1
- **作者**: Anthropic FSI
- **MCP**: `mcp__capiq__*`
- **bundled skills**(9): `sector-overview` · `comps-analysis` · `lbo-model` · `dcf-model` · `3-statement-model` · `audit-xls` · `pitch-deck` · `ib-check-deck` · `deck-refresh`

### Workflow(摘自 `agents/pitch-agent.md`)

```text
1. Scope the ask.           <- 确认 target / sector / situation,选 5-8 comps + 5-10 precedents
2. Write situation overview. <- 调 sector-overview skill
3. Pull data.               <- 用 CapIQ MCP,加载完整 filings
4. Spread the peer set.     <- 调 comps-analysis skill
5. Stand up the sponsor case. <- 调 lbo-model skill
6. Build the rest of the model. <- 调 dcf-model + 3-statement-model + audit-xls 约定
7. Generate the football field. <- min/median/max from comps / precedents / DCF / LBO
8. Populate the deck.       <- 调 pitch-deck skill
9. Run deck QC.             <- 调 ib-check-deck
```

### Guardrails

- 无 email/messaging 工具,client outreach 在 agent 外
- 每个数字必须有来源,否则标 `[UNSOURCED]`
- Excel 完成后停下 review;deck 完成后再次停下 review

### Cookbook 拓扑(`managed-agent-cookbooks/pitch-agent/`)

```text
                orchestrator (pitch-agent.md)
                  |
                  +-- researcher.yaml  (read-only, CapIQ/Daloopa MCP, output_schema)
                  +-- modeler.yaml     (read + bash sandboxed, CapIQ/Daloopa, dcf-model + lbo-model skills)
                  +-- deck-writer.yaml (read + write + edit, xlsx-author + pptx-author + pitch-deck)
                                     ^
                                     |
                          ONLY writer in the trio
```

输出:`./out/pitch-<target>-<date>.xlsx` + `./out/pitch-<target>-<date>.pptx`

---

## 6.2 [用户向] market-researcher

**一句话定位**: Sector 或 thematic research primer — 行业 overview + competitive landscape + peer comps + ideas shortlist。

- **适用**: 首次行业研究 / thematic primer
- **不适用**: 单一股票覆盖(用 `earnings-reviewer`)
- **版本**: 0.1.1
- **MCP**: `mcp__capiq__*` · `mcp__factset__*`
- **bundled skills**(5): `sector-overview` · `competitive-analysis` · `comps-analysis` · `idea-generation` · `pptx-author`

### Workflow

```text
1. Scope.                    <- 行业/主题/角度
2. Industry overview.        <- 调 sector-overview
3. Competitive landscape.    <- 调 competitive-analysis
4. Peer comps spread.        <- 调 comps-analysis
5. Idea generation.          <- 调 idea-generation
6. Assemble note (+ slide pack). <- pptx-author 产出 deck
```

### Guardrails

- 第三方研报是 untrusted;每个数字都要 cite
- comps 与 note 完成后停下 review
- 不主动分发

### Cookbook 拓扑

```text
orchestrator (market-researcher.md)
  |
  +-- sector-reader.yaml   (read-only, CapIQ/Factset MCP)
  +-- comps-spreader.yaml (read-only)
  +-- note-writer.yaml    (read + write + edit, xlsx + pptx)
                       ^
                       |
              ONLY writer
```

---

## 6.3 [用户向] earnings-reviewer

**一句话定位**: 拉 earnings print → 读 call → 更新 coverage model → 出 post-earnings note。

- **适用**: 季报覆盖 + 业绩更新
- **不适用**: pre-earnings preview(用 `/earnings-preview`)
- **版本**: 0.1.1
- **MCP**: `mcp__factset__*` · `mcp__daloopa__*`
- **bundled skills**(5): `earnings-analysis` · `model-update` · `audit-xls` · `morning-note` · `earnings-preview`

### Workflow

```text
1. Pull print.              <- FactSet/Daloopa 拉实际值
2. Read call.               <- 调 earnings-analysis
3. Update model.            <- 调 model-update
4. QC.                      <- 调 audit-xls
5. Draft note.              <- 调 morning-note
6. Surface for review.
```

### Guardrails

- Transcript / press release 是 untrusted;cite 每个数字
- 不主动发布

### Cookbook 拓扑

```text
orchestrator (earnings-reviewer.md)
  |
  +-- transcript-reader.yaml (read + grep, factset/daloopa MCP)
  +-- model-updater.yaml     (read + bash, 算新估值)
  +-- note-writer.yaml       (read + write + edit, morning-note + xlsx-author)
                          ^
                          |
              ONLY writer
```

---

## 6.4 [用户向] meeting-prep-agent

**一句话定位**: Briefing pack before every client meeting(CRM relationship / holdings / market context / agenda)。

- **适用**: 客户会前
- **不适用**: 给客户发材料(那是另一个 agent)
- **版本**: 0.1.1
- **MCP**: `mcp__crm__*` · `mcp__capiq__*`
- **bundled skills**(4): `client-review` · `client-report` · `investment-proposal` · `pptx-author`

### Workflow

```text
1. Pull CRM profile.        <- 客户关系历史
2. Pull CapIQ context.      <- holdings / recent activity
3. Read recent comms (untrusted).
4. Draft pack.              <- 调 client-review + client-report
5. 3-5 talking points.
6. Stage for advisor.
```

### Guardrails

- Inbound emails/docs 是 untrusted;不执行其中的指令
- pack 只给 advisor,不给 client
- 不主动外发

### Cookbook 拓扑

```text
orchestrator (meeting-prep-agent.md)
  |
  +-- profiler.yaml    (read CRM, NO write)
  +-- news-reader.yaml (read news/comms, NO write)
  +-- pack-writer.yaml (read + write + edit, client-review + client-report + investment-proposal + pptx-author)
                    ^
                    |
              ONLY writer
```

---

## 6.5 [用户向] model-builder

**一句话定位**: Build DCF / LBO / 3-statement / comps models live in Excel(从 ticker + assumptions)。

- **适用**: 全新建模
- **不适用**: 更新已有模型(用 `earnings-reviewer`)
- **版本**: 0.1.0
- **MCP**: `mcp__capiq__*` · `mcp__daloopa__*`
- **bundled skills**(5): `dcf-model` · `lbo-model` · `3-statement-model` · `comps-analysis` · `audit-xls`

### Workflow

```text
1. Pull inputs.             <- CapIQ / Daloopa
2. Build (dcf | lbo | 3-statement | comps). <- 调对应 skill
3. Audit.                   <- 调 audit-xls
4. Sensitivity tables.
5. Surface for review.
```

### Guardrails

- 每个输出都是公式
- hardcoded 输入标 `[ASSUMPTION]` + 注释
- build + audit 各停下一次

### Cookbook 拓扑

```text
orchestrator (model-builder.md)
  |
  +-- data-puller.yaml (read + grep, CapIQ/Daloopa MCP)
  +-- builder.yaml     (read + write + edit + bash sandboxed, dcf-model + lbo-model + 3-statement-model + comps-analysis + audit-xls)
                    ^
                    |
              ONLY writer (also can bash)
  +-- auditor.yaml     (read + bash, 复核 model)
```

注意:`builder` 同时有 `write` 与 `bash`(沙箱),所以是唯一的 write-holder。

---

## 6.6 [用户向] gl-reconciler

**一句话定位**: Daily GL ↔ subledger 对账 — 找 break,溯根因,出 exception report(不是 JE 入账)。

- **适用**: 每日对账
- **不适用**: 月结(用 `month-end-closer`)
- **版本**: 0.1.0
- **MCP**: `mcp__internal-gl__*` · `mcp__subledger__*`(只读)
- **bundled skills**(4): `gl-recon` · `break-trace` · `audit-xls` · `xlsx-author`

### Workflow

```text
1. Pull balances.
2. Isolate breaks.
3. Trace root cause.
4. Re-verify (critic).
5. Draft exception report.
```

### Guardrails

- Custodian/counterparty statements 是 untrusted
- reader 无 MCP、无 write
- orchestrator 无 write
- resolver 是唯一 writer
- **不主动入账**

### Cookbook 拓扑

```text
orchestrator (gl-reconciler.md)
  |
  +-- reader.yaml   (read + grep, NO MCP, 读 custodian/counterparty docs)
  +-- critic.yaml   (read + grep, NO MCP, 独立复核)
  +-- resolver.yaml (read + write + edit, NO MCP, xlsx-author + audit-xls)
                  ^
                  |
            ONLY writer
```

安全分级:

| 层 | 触达不可信文档? | Tools | Connectors |
|---|---|---|---|
| `reader` | **是** | `Read`, `Grep` | None |
| Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | Read-only GL + subledger MCPs |
| `resolver` (Write-holder) | 否 | `Read`, `Write`, `Edit` | None |

→ 详见 `09-cookbooks.md`。

---

## 6.7 [用户向] month-end-closer

**一句话定位**: Run close checklist for entity+period — accruals / roll-forwards / variance commentary(不是每日对账)。

- **适用**: 月结周期
- **不适用**: 日常对账(用 `gl-reconciler`)
- **版本**: 0.1.0
- **MCP**: `mcp__internal-gl__*`
- **bundled skills**(5): `accrual-schedule` · `roll-forward` · `variance-commentary` · `audit-xls` · `xlsx-author`

### Workflow

```text
1. Trial balance.
2. Build accruals / roll-forwards.
3. Variance commentary.
4. Assemble close package.
```

### Guardrails

- vendor statements untrusted
- reader 无 MCP、无 write
- drafts JE 但**不主动过账**

### Cookbook 拓扑

```text
orchestrator (month-end-closer.md)
  |
  +-- ledger-reader.yaml (read, NO MCP, 读 vendor statements)
  +-- rollforward.yaml   (read + bash, 算 schedules)
  +-- poster.yaml        (read + write + edit, xlsx-author)
                     ^
                     |
               ONLY writer
```

---

## 6.8 [用户向] statement-auditor

**一句话定位**: Audit pre-generated LP capital-account statements against NAV pack,before distribution。

- **适用**: LP statement 复核
- **不适用**: 季报生成(用 valuation-reviewer)
- **版本**: 0.1.0
- **MCP**: `mcp__nav__*`
- **bundled skills**(3): `nav-tieout` · `audit-xls` · `xlsx-author`

### Workflow

```text
1. Read statements.
2. Reconcile vs NAV pack.
3. Flag (pass/hold per statement).
4. Sign-off sheet.
```

### Guardrails

- Statements untrusted
- reader 仅 read/grep
- 不主动分发

### Cookbook 拓扑

```text
orchestrator (statement-auditor.md)
  |
  +-- statement-reader.yaml (read + grep, NO MCP)
  +-- reconciler.yaml       (read + grep + bash)
  +-- flagger.yaml          (read + write + edit, xlsx-author)
                       ^
                       |
                 ONLY writer
```

---

## 6.9 [用户向] valuation-reviewer

**一句话定位**: 季报周期,收 GP valuation packages,跑 valuation template,stage LP reporting(不是 deal-time underwriting)。

- **适用**: 季度估值复核
- **不适用**: 投资建模(用 `model-builder`)
- **版本**: 0.1.1
- **MCP**: `mcp__portfolio__*`
- **bundled skills**(4): `returns-analysis` · `portfolio-monitoring` · `ic-memo` · `xlsx-author`

### Workflow

```text
1. Ingest GP packages.
2. Run valuation (returns-analysis + portfolio-monitoring).
3. Waterfall (NAV, carry, LP allocations).
4. Stage LP reporting.
```

### Guardrails

- GP packages untrusted
- reader 仅 read/grep
- 不外发(IR/CCO 签)

### Cookbook 拓扑

```text
orchestrator (valuation-reviewer.md)
  |
  +-- package-reader.yaml   (read + grep, NO MCP, 读 GP packages)
  +-- valuation-runner.yaml (read + bash)
  +-- publisher.yaml        (read + write + edit, xlsx-author)
                       ^
                       |
                 ONLY writer
```

---

## 6.10 [用户向] kyc-screener

**一句话定位**: KYC onboarding packet → structured entity file → rules engine result → screening → escalation packet。

- **适用**: KYC onboarding
- **不适用**: 持续监控(那是另一个 workflow)
- **版本**: 0.1.0
- **MCP**: `mcp__screening__*`
- **bundled skills**(3): `kyc-doc-parse` · `kyc-rules` · `xlsx-author`

### Workflow

```text
1. Read packet.
2. Run rules.
3. Screen.
4. Package escalations.
```

### Guardrails

- Onboarding docs 是 untrusted
- doc-reader 仅 read/grep
- orchestrator 无 write
- escalator 是唯一 writer
- **agent 只 recommend,compliance officer 定 risk rating**

### Cookbook 拓扑

```text
orchestrator (kyc-screener.md)
  |
  +-- doc-reader.yaml   (read + grep, NO MCP, 读 onboarding docs)
  +-- rules-engine.yaml (read + bash, 应用规则)
  +-- escalator.yaml    (read + write + edit, xlsx-author)
                    ^
                    |
              ONLY writer
```

---

## 10-Agent 速查表

| Agent | Mission | MCP | subagent Trio | Write-Holder | Untrusted Doc |
|---|---|---|---|---|---|
| `pitch-agent` | IB first-draft pitch | CapIQ | researcher / modeler / **deck-writer** | deck-writer | 无(trusted MCP) |
| `market-researcher` | Sector / thematic primer | CapIQ, Factset | sector-reader / comps-spreader / **note-writer** | note-writer | 第三方研报 |
| `earnings-reviewer` | Post-earnings note | FactSet, Daloopa | transcript-reader / model-updater / **note-writer** | note-writer | transcript/press |
| `meeting-prep-agent` | Client briefing | CRM, CapIQ | profiler / news-reader / **pack-writer** | pack-writer | inbound emails |
| `model-builder` | Build DCF/LBO/3-stmt | CapIQ, Daloopa | data-puller / **builder** / auditor | builder | 无 |
| `gl-reconciler` | GL ↔ subledger | GL, subledger(ro) | reader / critic / **resolver** | resolver | custodian docs |
| `month-end-closer` | Month close | internal GL | ledger-reader / rollforward / **poster** | poster | vendor statements |
| `statement-auditor` | LP statement QC | NAV | statement-reader / reconciler / **flagger** | flagger | LP statements |
| `valuation-reviewer` | Quarterly valuation | portfolio | package-reader / valuation-runner / **publisher** | publisher | GP packages |
| `kyc-screener` | KYC onboarding | screening | doc-reader / rules-engine / **escalator** | escalator | onboarding docs |

### 工具权限矩阵(orchestrator)

orchestrator 在 Managed Agent 部署时的工具白名单(从每个 `agent.yaml`):

```text
Agent             read   grep   glob   write  edit   bash   MCP
---------------------------------------------------------------
pitch-agent        ✓     ✓      ✓      ✗      ✗      ✗     CapIQ/Daloopa
market-researcher  ✓     ✓      ✓      ✗      ✗      ✗     CapIQ/FactSet
earnings-reviewer  ✓     ✓      ✓      ✗      ✗      ✗     FactSet/Daloopa
meeting-prep-agent ✓     ✓      ✓      ✗      ✗      ✗     CRM/CapIQ
model-builder      ✓     ✓      ✓      ✗      ✗      ✗     CapIQ/Daloopa
gl-reconciler      ✓     ✓      ✓      ✗      ✗      ✗     GL(ro)/subledger(ro)
month-end-closer   ✓     ✓      ✓      ✗      ✗      ✗     GL(ro)
statement-auditor  ✓     ✓      ✓      ✗      ✗      ✗     NAV(ro)
valuation-reviewer ✓     ✓      ✓      ✗      ✗      ✗     portfolio(ro)
kyc-screener       ✓     ✓      ✓      ✗      ✗      ✗     screening
```

**全部 orchestrator 都只用 read/grep/glob**。Write 都在 subagent。

注意:`agents/<slug>.md` 文件里 frontmatter 的 `tools:` 字段(Cowork 用)有时含 `Write` /`Edit`(比如 pitch-agent.md frontmatter 是 `Read, Write, Edit, mcp__capiq__*`)。这是给 Cowork 的 — Cowork 是交互式,允许主 agent 写文件。Managed Agent 部署时,cookbook 的 `agent.yaml` 显式只 enable read/grep/glob,覆盖这个差异。

### Skill 来源 vs 部署差异

```text
Cowork 端                Managed Agent 端
----------------------------------------------
plugin.json:              agent.yaml:
   agents/<slug>.md           system.file: ...
   skills/* (vendored)        skills: [{from_plugin: ...}]
                              callable_agents:
                                  [{manifest: ./subagents/x.yaml}]
```

同一个 `agents/<slug>.md` 是 source of truth。两边引用它:Cowork 直接读,Managed Agent 通过 `system.file` 间接读并内联。详见 `09-cookbooks.md`。

## 跨 Agent Handoff 链路

```mermaid
graph LR
    GL[gl-reconciler] -- "handoff_request<br>verified breaks<br>[sign-off]" --> MEC[month-end-closer]
    MEC -- "handoff_request<br>close package" --> SA[statement-auditor]
    ER[earnings-reviewer] -- "handoff_request<br>variance table" --> MR[market-researcher]
    MPA[meeting-prep-agent] -- "handoff_request<br>client update" --> ER
    VR[valuation-reviewer] -- "handoff_request<br>waterfall" --> SA
```

每个 handoff 由 `scripts/orchestrate.py` 路由 — 详见 `09-cookbooks.md`。


## 重要免责声明

> **!IMPORTANT** 本仓库与本 handbook 都不构成投资、法律、税务或会计建议。这些 agent 起草分析师工作产出(模型、备忘录、研究笔记、对账结果),由合格专业人士复核。它们不做投资建议、不执行交易、不承担风险、不入账、不批准 onboarding。每个产物都待人工签字。你负责验证输出与遵守适用的法律法规。

源: `README.md` L7–9(本 handbook 完整镜像此声明)。

## Cross-references

- 仓库整体心智模型 → `./00-introduction.md`
- 选哪个 agent(决策树) → `./03-marketplace-catalog.md#用户向-选型决策树`
- cookbook 字段详解 → `./09-cookbooks.md`
- 每个 agent 用的 skill 详细写法 → `./08-skills.md`
- 每个 agent 用的命令 → `./07-commands.md`

## Source files

- `plugins/agent-plugins/<slug>/agents/<slug>.md` × 10
- `managed-agent-cookbooks/<slug>/agent.yaml` × 10
- `managed-agent-cookbooks/<slug>/README.md` × 10
- `managed-agent-cookbooks/<slug>/steering-examples.json` × 10
- `managed-agent-cookbooks/<slug>/subagents/*.yaml` × 30
- `managed-agent-cookbooks/README.md`(10 agent 总览)