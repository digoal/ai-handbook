# 第 18 章 · FAQ

> **面向读者**:全员 · **预计阅读**:10 分钟(查词)
> **前置依赖**:无
> **本章目标**:集中回答 17 个最常被问的问题

## 18.1 与同类方案对比

### Q1. codegraph 和 ctags / LSP / Sourcegraph 各有什么不同?

| 方案 | 范围 | 实时性 | 跨仓 | AI 友好 |
|------|------|--------|------|---------|
| **ctags** | 单文件 | 静态 | ✗ | ✗(仅行号) |
| **LSP**(gopls 等) | 当前项目 | 实时 | ✗ | ✗(IDE 协议) |
| **Sourcegraph** | 全网 | 索引慢 | ✓ | ✓(但要服务) |
| **codegraph** | 本地 | 准实时(增量) | ✓(per-project) | ✓(MCP 原生) |

**codegraph 的独特定位**:100% 本地 + 准实时同步 + MCP 原生暴露给 AI agent,无需 server/无需 cloud。

---

## 18.2 安装与环境

### Q2. Node 25 为什么不能装?

codegraph 在 `src/bin/codegraph.ts:91-107` 硬拦 Node ≥25,因为 V8 25+ 的 Turboshaft Zone 在 tree-sitter wasm 调用栈里有 OOM 风险。同时 Node <20 不支持 `node:sqlite`(`engines.node: ">=20 <25"`)。用 Node 20-24 任一 LTS 版本即可。

### Q3. 装了 codegraph 但 Claude Code 没看到 MCP tool,怎么排查?

按这个顺序排查:
1. `codegraph --version` 确认 CLI 可执行
2. `cat ~/.claude.json | jq .mcpServers.codegraph` 确认配置存在
3. `cat ~/.claude/settings.json | jq .permissions.allow` 确认有 `mcp__codegraph__*`
4. 重启 Claude Code 会话(MCP 配置改了需要重启)
5. 在 Claude Code 里 `/mcp` 命令看当前生效的 server 列表

### Q4. `~/.claude.json` 还是 `./.mcp.json`?历史坑 #207

- **全局安装**(`codegraph install` 不带 `--location`):写 `~/.claude.json`
- **本地安装**(`codegraph install --location=local`):写 `./.mcp.json`(注意**不是** `./.claude.json`)
- pre-#207 版本错误地写 `./.claude.json`,Claude Code 实际不读它,配置永不生效 — 新版会自动迁移

---

## 18.3 Prompt Hook

### Q5. `CODEGRAPH_NO_PROMPT_HOOK=1` 关掉 hook 之后还能升级自动开吗?

**不会**。这是 session/进程级 kill switch,设了之后本进程不再触发 hook 检测。升级时的 `selfHealPromptHook`(`src/upgrade/index.ts:529-539`)只检测"完全没有 hook 配置"的情况,如果你曾拒绝过(答 No),它也不会强制开。要永久关,卸载时答 No。

### Q6. 多 Claude Code 进程同时跑会重复索引吗?

**不会**。daemon 模式共享一个 `CodeGraph` 实例 + 一个 `SQLite` writer:第一个 launcher spawn daemon,后续 launcher 通过 Unix socket 复用。`codegraph serve --mcp` 的进程列表通常只看到 1 个 detached daemon + N 个 launcher(proxy)。

---

## 18.4 多项目 / Monorepo

### Q7. 一个项目里多个子仓,`codegraph_explore` 怎么知道查哪个?

每个 MCP tool 都支持 `projectPath` 参数。`codegraph_explore` 等价于:

```json
{ "query": "...", "maxFiles": 12, "projectPath": "/path/to/subproject" }
```

`server-instructions.ts:84-103` 给出 `SERVER_INSTRUCTIONS_NO_ROOT_INDEX` 变体,引导 agent 在跨仓时显式传 `projectPath`。

### Q8. 索引很慢怎么办?

按以下优先级尝试:
1. 在 `codegraph.json` 里加 `includeIgnoredPatterns` 屏蔽 vendor/build 目录
2. 用 `codegraph status` 看 `Pending sync:` 是否一直涨
3. 调高 `CODEGRAPH_WATCH_DEBOUNCE_MS`(默认 ~1s,可调到 5s)
4. 大仓考虑拆仓或先 init 子目录
5. macOS 上 FSEvents 单递归 fs.watch 通常最快,Linux inotify 在多文件时可能满

---

## 18.5 同步与可见性

### Q9. 我改了文件,多久能在工具里看到?

默认 ~1s(watcher debounce + adaptive)。FSEvents(macOS)/inotify(Linux)/ReadDirectoryChangesW(Windows)各自延迟不同,Linux 上如果是 NFS 可能有 5-10s。

### Q10. ⚠️ staleness banner 出现了,我应该重新读文件吗?

**不要**。banner 是 `formatStaleBanner`(`tools.ts:389`)在 explore 返回里加的提示,意思是"下面这段代码在被引用前已经被改过,内容可能跟磁盘不一样"。信任 codegraph 内的源码,不要用 Read 工具重读,这会破坏 89% 工具调用下降的红利。

### Q11. ⚠️ CodeGraph auto-sync is DISABLED banner 意味着什么?

意思是 watcher 停了(典型场景:你在 WSL2 跨 FS 启动了 codegraph,inotify 失效)。解决:
- 改 `CODEGRAPH_WATCH_DEBOUNCE_MS` 或检查 FS
- 装 git hooks 替代:`codegraph install` 检测到 watch 失败时会提示
- 临时绕过:用 `codegraph sync` 手动同步

**注意**:`CODEGRAPH_NO_WATCH=1` 不会触发这个 banner,因为它是在 start 前拒绝(`watch-policy.ts`),与真正 runtime degrade 区分开。

---

## 18.6 数据库与性能

### Q12. SQLite 数据库会不会无限增长?

不会,但 `.codegraph/codegraph.db-wal` 可能。codegraph 在长 indexing 时累积 WAL,周期性 checkpoint(`src/db/wal-valve.ts`)把 WAL 内容合并回主 db 并截断。手动触发:`codegraph index --force`(完整重建 + 隐式 checkpoint)。监控:`codegraph status` 看 `Database size:` 和 `WAL size:`。

### Q13. 想屏蔽 vendor/ 和 build/,怎么配?

三层兜底(按优先级):
1. **.gitignore 自动继承**:codegraph 默认遵守项目根的 `.gitignore`,`vendor/` 和 `build/` 大概率已在其中
2. **codegraph.json 团队共享**:在项目根加 `codegraph.json`,写 `includeIgnoredPatterns`(让 .gitignore 被忽略的文件可被索引)或自定义忽略
3. **CODEGRAPH_DIR 环境变量**:把索引目录指定到非项目路径,实现物理隔离(很少用)

---

## 18.7 MCP 工具选择

### Q14. 8 个 tool 我只用了 1 个,要不要开其他 7 个?

**默认推荐保持 1 tool**。原因:
- `server-instructions.ts:20-70` 强引导 agent 用 `codegraph_explore`,1 个 tool 让决策路径最短
- 7 个 tool 让 agent 决策分叉,可能调错工具

什么时候开多个:
- 想强制 agent 走精确搜索(配合 `codegraph_search` + `codegraph_callers`)
- 想做批量分析(配合 `codegraph_impact`)
- 做 benchmark / A/B 对比

开启方式:`~/.claude.json` 的 codegraph entry 加 `env.CODEGRAPH_MCP_TOOLS=explore,node,search,callers`。

---

## 18.8 贡献与扩展

### Q15. 怎么贡献一个新语言?

用 `.claude/skills/add-lang` slash command,Claude Code 会引导你走完整端到端流程:
1. 选语言(看 `codegraph-kernel/Cargo.toml` 当前支持清单)
2. Rust 端加 tree-sitter grammar crate
3. Wasm 端加 web-tree-sitter grammar
4. 跑 ABI 校验 + 3 仓库 A/B 评测
5. 提 PR

详细清单见 {{chapter:16}}。

### Q16. 评测里 PASS_THRESHOLD=0.5,这是宽松还是严格?

**中等偏严**。回顾/MRR 都用 0.5 阈值(单测失败率 ~5%);edgeDensity 是纯诊断信号无阈值。这意味着你新加的语言 / 改的 schema 可能因为"半数符号召回"门槛过不去 CI。建议 CI 上先跑 `search-deliberate-miss` 套件确认基线,再放开。

---

## 18.9 升级与回滚

### Q17. 升级后我之前的版本还能用吗?

可以,codegraph 用 `~/.codegraph/versions/<v>/` 装多个版本,`~/.local/bin/codegraph` 是 symlink 指向当前激活版本。`codegraph upgrade <version>` 钉版本;`codegraph upgrade` 升 latest。回滚:`codegraph upgrade 1.4.0`。

---

## 18.10 本章小结

17 题覆盖安装、prompt hook、monorepo、同步、数据库、工具选择、贡献、升级 8 大主题。遇到新问题可在以下资源找答案:
- `references/validation-log.md` — 所有验证记录
- `chapters/02-quickstart.md` — 入门
- `chapters/06-mcp-tools-manual.md` — 工具集
- 官方 `README.md` 全文 + `site/src/content/docs/`

## 18.11 下一章预告

无 — 这是全书最后一章。感谢阅读。

## 18.12 参考

- `docs/SEARCH_QUALITY_LOOP.md` — 评测电池细节
- `CHANGELOG.md` — 各版本变更与历史坑(#207、#636 等)
- `src/installer/targets/claude.ts:44-72` — Claude Code 集成路径表