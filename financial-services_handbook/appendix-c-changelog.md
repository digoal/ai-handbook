# Appendix C — 修订记录(Changelog)

> **本节定位** [both] — handbook 与仓库 commit SHA 绑定。本附录记录每次重大修订的差异。

## 修订记录

### 2026-08-11 — Top-tier follow-up (Phase 2): P0-X7/X8 + P1 casing

**Repo SHA bound**: `38652224c10610fa52eee2acee3ac712dcff01f2`

**Phase** — User-confirmed "进入下一步"。修复 top-tier-report.md 中 deferred 的 2 个 P0 + P1 casing sweep。

**P0 fixes applied**:

| ID | 修复内容 | 影响文件 |
|---|---|---|
| P0-X7 | ch.11 补齐 M365 Admin Center 部署步骤(prerequisites / Step 7 上传 / propagation SLA / rollback)— 解决 2-hour plan 不可行的根因 | 11-microsoft-365-install.md |
| P0-X8 | ch.13 替换 fabricated `<Scope>Group.<guid>.Read.All</Scope>` 危险指导 — 新版 5 条按概率排序的真实诊断路径 | 13-troubleshooting.md |

**P1 fixes applied (casing sweep)**:

| 类别 | 数量 | 修复 |
|---|---|---|
| Cookbook → cookbook(正文) | 14 | body 中 `Cookbook` → `cookbook` |
| Subagent → subagent | 5 | 全部 → `subagent` |
| Plugin → plugin(正文) | 6 | 全部 → `plugin` |
| MCPs 保留 | 0 | 7 处保留(都是真正复数语境) |

**统计**:

- ch.11 字数: 1,312 → 1,630(+318,24%)
- ch.13 字数: 1,551 → 1,695(+144,9%)
- handbook 总字数: 32,776 → 33,197(+421,1.3%)

### 2026-08-11 — Top-tier review batch (Phase 1)

**Repo SHA bound**: `38652224c10610fa52eee2acee3ac712dcff01f2`

**Phase** — 7-lens review + 3 persona simulation → 134 findings (32 P0 / 50 P1 / 52 P2)

**P0 fixes applied**:

| ID | 修复内容 | 影响文件 |
|---|---|---|
| P0-X1 | 149 个 `../XX.md` → `./XX.md` 同级 cross-ref 修复(全局 sed) | 所有 main chapter |
| P0-X2 | `.mcp.json` line 50 box 块**正确**无需逗号(line 46 egnyte 才缺)— 修正 4 章节误述 | 04/05/10/13 |
| P0-X3 | 13 个 main chapter 新增 `## 重要免责声明` 段(替代 inline 一行) | 01–13 |
| P0-X4 | 14 个 main chapter 顶部加 primer cross-ref callout | 00/01–13 |
| P0-X5 | 4 个 Managed Agents API curl 示例修正(URL/version/beta header/body) | 01-quickstart (×2) + 09-cookbooks (×2) |
| P0-X6 | skill count 55 → 66(55 vertical + 11 partner)在 12 处统一 | 00/01/03/08/appendix-b/README |
| P0-X9 | 5 个 broken anchor 修复(`#开发者向-部署流水线` 等) | 01/02/09 |
| P0-L4-1 | `AUM / AUM` 重复 → `AUM / carry` | 00.5-primer |
| P0-L4-2 | `标的的 CFO` 重复字 → `标的方的 CFO` | 00.5-primer |
| P0-L4-3 | `cook book` 拼写 → `cookbook` | 00-introduction |

**新增文件**:

| 文件 | 用途 |
|---|---|
| `docs/handbook/appendix-c-changelog.md` | 本附录 |
| `scripts/count-entities.sh` | 中心化 entity count(README/00/02 引用) |
| `.github/workflows/doc-lint.yml` | markdownlint + cspell + lychee CI gate |
| `review/baseline-top-tier.txt` | Phase 1 inventory snapshot |
| `review/lens-1-accuracy.md` ~ `review/lens-7-xrefs.md` | 7 维度 review |
| `review/persona-p1-finance-naive.md` ~ `review/persona-p3-m365-admin.md` | 3 persona walkthroughs |
| `review/findings-aggregated.md` | Phase 5 consolidated findings |
| `review/top-tier-report.md` | 最终交付报告 |

### 2026-08-11 — Finance primer + mermaid v11.16.0 audit (previous batch)

**Phase** — Primer chapter + mermaid batch validation

**P0 fixes applied**:

- 新增 `docs/handbook/00.5-finance-primer.md`(5,242 字,13 sections,21 ASCII 框图)
- Mermaid v11.16.0 全量校验 24/24 PASS(修复 3 个 syntax errors:asset-05 multi-word edge label / inline-01 `/comps AAPL` parallelogram / inline-08 嵌套引号)
- 更新 `README.md` TOC + `appendix-b-references.md` chapter→source 映射

### 2026-08-11 — R6 sign-off (earlier batch)

**Phase** — 4 reviewer parallel audit + R6 final verification

**P0 fixes applied (16)**:

- `.mcp.json` 行号声明(line 46 / line 50)
- `comcap.com` → `kensho.com`
- `Anthropic FS` → `Anthropic FSI`
- `你你` → `你负责`(4 处)
- `language / /` 维度补齐
- Step numbering IB workflow
- `|  |` empty cell 修复
- `/  /` empty token 修复
- `pre-commit(commit` 截断修复
- 6-backtick fence → 3-backtick
- 13 章 awkward 中文重写
- 13-troubleshooting 增 `## What you'll learn`
- 04/05/12 增 Mermaid 块
- 06-agents 增 hands-on code

**Final R6 verdict**: 26,205 字 / 0 P0 / 0 P1 / 0 P2 remaining / 24/24 mermaid PASS / 100% coverage of 20 plugins / 66 skills / 56 commands / 12 MCPs / 10 cookbooks.

---

## 修订约定

每次重大修订在本附录加一段:

```
### <date> — <phase name>

**Repo SHA bound**: <sha>

**Phase** — <一句话描述>

**P0 fixes applied**:
[Table: ID | 修复 | 影响文件]

**新增文件**:
[Table: 文件 | 用途]
```

## 不可变约束(任何修订都遵守)

1. **ASCII-only `.ps1`** — Windows PowerShell 5.1 默认 ANSI 编码页,非 ASCII 字符变 mojibake,可能终止字符串(`scripts/check.py` 强制)
2. **Chinese narrative + English term in parens** on first mention
3. **Role tag** `[用户向]` / `[开发者向]` / `[运维向]` 在每个章节首行
4. **No emoji** in any handbook file
5. **No `.codegraph` references**(索引元数据,不是文档)
6. **Mermaid v11.16.0** 兼容(每章 ≥ 1 块,全 PASS)
7. **TL;DR + What you'll learn + Source files + Cross-references** 4 段骨架
8. **`## 重要免责声明`** 在所有 14 个 main chapter
9. **3 档阅读路径**(速通 5min / 实用 1h / 进阶 1d)在 README 显式
10. **SHA pin** 在 README 与本附录

## Cross-references

- 仓库根 README → `financial-services/README.md`
- Handbook 总入口 → `./README.md`
- 上一附录(反向索引 + 源文件映射)→ `./appendix-b-references.md`
- 术语表 → `./appendix-a-glossary.md`
