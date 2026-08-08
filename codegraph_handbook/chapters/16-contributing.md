# 第 16 章 · 贡献者指南:加语言 / 加 tool / 改 schema

> **面向读者**:开发者 · **预计阅读**:30 分钟
> **前置依赖**:{{chapter:12}}, {{chapter:15}}
> **本章目标**:让贡献者跑通三件事

## 16.1 引言

codegraph 是棵越长越大的"语言树"。每多支持一种语法,就多一群仓库能享受 `codegraph_explore` 的红利;每加一个 MCP tool,agent 就多一种低 token 检索姿势;每动一次 schema,既有 `.codegraph/` 要么被 migration 接住、要么就地重建。本章讲清三条路径的关键卡点(ABI 不匹配、wasm parity 失败、migration 漏索引)及验证步骤。

## 16.2 概念铺垫

### 16.2.1 skill / slash command

`add-lang` 是 **skill**(`.claude/skills/add-lang/SKILL.md`),由 `/add-lang <lang>` 触发。同目录还有 `agent-eval`(A/B 评测)、`corpus.json`(语料)、`scripts/add-lang/` 下四个脚本:`check-grammar.mjs / dump-ast.mjs / verify-extraction.mjs / bench.sh`。skill 不是文档,是 Claude Code 内部直接执行的工作流。

### 16.2.2 contribution tax

贡献有**三层成本**:

1. **kernel ABI**:`Cargo.toml:13-15` 钉 `tree-sitter = "0.25"`、ABI v2。改 ABI 后所有 wasm 端必须重对齐——见 `Cargo.toml:19-22` 注释。
2. **wasm parity**:wasm 端节点表必须与 kernel 端 C 语法完全相同,否则 dual-extract 给出不同节点名,SQLite 写入直接挂。
3. **evaluation gate**:`/agent-eval` 跑 paid `claude -p` 双臂,任何一臂 `recall<0.5` 不算"加完"。

## 16.3 正文

### 16.3.1 加新语言端到端(add-lang skill)

`/add-lang lua` 触发后,`SKILL.md` 按 10 步推进:

1. **解析 + 短路**——查 `LANGUAGES`(本仓 42 项)与 `EXTRACTORS`;已在则跳到 7-8 步。
2. **找语法 + 健康检查**——`ls node_modules/tree-sitter-wasms/out/` 后先跑 `check-grammar.mjs`。**Present 不代表可用**:tree-sitter-wasms 的 Lua 是 ABI 13,共享 wasm heap 时 ERROR,需 vendor ABI 14/15 新构建(`npm pack @tree-sitter-grammars/tree-sitter-<lang>` 或 `npx tree-sitter build --wasm`)。
3. **AST 节点发现**——`dump-ast.mjs` 输出节点频次 + 字段名,对照现有 extractor 模板(`rust.ts`/`scala.ts` 函数式,`java.ts`/`csharp.ts` OO,`python.ts`/`ruby.ts` 脚本,`go.ts` top-level)。
4. **连线 4 文件**——`src/types.ts` 加 `<lang>` 到 `LANGUAGES` **和** `DEFAULT_CONFIG.include`(漏 glob → `init` 找 0 文件);`grammars.ts` 三张表全加;新增 `languages/<lang>.ts`;`languages/index.ts` 注册。**5th 文件偶尔**:`tree-sitter.ts` 的 `extractVariable` 在 Lua 嵌套声明上需单写一支 `else if`。
5-6. **build + verify + 测试**——`npm run build` → `verify-extraction.mjs` 通 → `vitest run` 加 `describe('<Lang> Extraction')`。
7-8. **3 仓 benchmark**——`gh search repos --language=<lang>` 自选 S/M/L,`bench.sh <lang> <name> <url> "<q>" headless` 每仓跑 `with`/`without`。
9-10. **更新 README + CHANGELOG,只报告不 commit**——house rule 禁止自动 commit/push,release 走 GitHub Actions。

### 16.3.2 Rust 端:加 tree-sitter grammar crate

`codegraph-kernel/Cargo.toml:23-59` 列了 **14 个编译 crate**:5 个 registry caret(`typescript 0.23`/`javascript 0.25`/`java 0.23`/`python 0.23`/`go 0.23` 等)、9 个 `=` 精确钉(`c=0.24.2`/`cpp=0.23.4`/`rust=0.24.2`/`csharp=0.23.5`/`ruby=0.23.1`/`php=0.24.2`/`swift=0.7.3`/`r=1.2.0`/`luau=1.2.0`)。精确钉原因:wasm 端 .wasm 是从这些 tag 的 `parser.c` sha-matched build 的,patch bump 不重 vendor 破匹配。

### 16.3.3 Wasm 端:加 web-tree-sitter grammar

`src/extraction/grammars.ts:20-53` 是 `WASM_GRAMMAR_FILES`,**当前 32 项**;`EXTENSION_MAP` 把后缀映射到 language token。**vendored wasm**(pascal/scala/lua 等)在文件下方有 `(lang === 'pascal' || …)` 分支指向 `src/extraction/wasm/tree-sitter-<lang>.wasm`。`copy-assets`(`npm run build` 触发)拷 vendored wasm 到 `dist/`,**不放进 `src/extraction/wasm/` 就不会出现在发布物里**。

### 16.3.4 ABI 校验机制

`Cargo.toml:19-22` 注释解释 gate:kernel-grammar-parity test 在 CI 读 wasm 端 node-kind table 与 Rust crate 编译产物对比,完全相等才放行。Ch12 §12.4.2 演示过 `contractInfo()` 返回 `{abiVersion:2, languages:20, node_kinds:22, edge_kinds:12}`——`languages:20` 与 LANGUAGES 42 项差异来自非 tree-sitter 语言(yaml/twig/xml 等走 custom extractor)。

### 16.3.5 写新 MCP tool

`src/mcp/tools.ts` 注册了 8 个 tool,默认只开 `codegraph_explore`(Ch06 §6.3.1)。注册链:

1. 在 `TOOL_HANDLERS` 加 `{ name, description, inputSchema, handler }`,静态 schema 用于 `tools/list`。
2. 字段进 `MAX_INPUT_LENGTH=10000` / `MAX_PATH_LENGTH=4096` 约束(`tools.ts:65-`)。
3. 错误走 `NotIndexedError` / `PathRefusalError` 两类——前者 SUCCESS 给可恢复场景(没索引),后者 `isError:true` 给安全拒绝。
4. 加 `DEFAULT_MCP_TOOLS` 前权衡 token:每个 schema 都进 system prompt。

### 16.3.6 改 schema

`src/database/migrations.ts` 加 `migration_N_<desc>`,在 `migrations` 数组尾部追加;**索引必须同步加**(CREATE INDEX IN migration 体,不要等运行时补)。新加 node_kinds:① Rust `NodeKind` 枚举加值;② wasm extractor 产出对应 kind;③ migrations 给对应表加列;④ Ch11 同步更新。

### 16.3.7 跑 /agent-eval

`corpus.json` 按规模分层语料,`/agent-eval <lang>` 调用 `run-all.sh` 跑 paid 双臂。关注 `parse-run.mjs`:tool calls、Read 数、cost;判定 pass 看 Ch15 `recall>=0.5`。

## 16.4 真实场景实战

### 场景 16.1: 跑 /add-lang nix

nix 已在 LANGUAGES(`src/types.ts:107`),走短路,跳过 2-6 步直接 7-8 benchmark。

**等价验证**:
- `Cargo.toml:1-67` 不含 `tree-sitter-nix` → 推断 nix **仅 wasm 端**走 `tree-sitter-wasms/nix.wasm`,不在 kernel ABI 编译列表(languages:20 印证)。
- `grammars.ts:52` `nix: 'tree-sitter-nix.wasm'` 确认 wasm 端存在。
- 预期选 nixpkgs(L)/NixOS config(M)/nix flake 模板(S)三档。

### 场景 16.2: 写新 MCP tool hello_world

```typescript
// src/mcp/tools.ts (示意追加)
const helloWorldTool = {
  name: 'codegraph_hello',
  description: 'Return hello + indexed stats',
  inputSchema: { type: 'object', properties: { name: { type: 'string', maxLength: 100 } } },
  handler: async ({ name }) => `Hello ${name}!`,
};
```

注册链:① 加 `TOOL_HANDLERS`;② `CODEGRAPH_MCP_TOOLS=codegraph_hello,codegraph_explore` 启用;③ `tools/list` 验证 schema;④ `tools/call codegraph_hello {"name":"world"}`。

### 场景 16.3: 跑 /agent-eval 看 A/B

`/agent-eval rust` 预期选 tokio(大)/axum(中)/CLI 小工具(S);每仓 `with` 臂 codegraph tool 数显著高于 `without`(Ch01 Rust 91% 调用节省)。任何 fixture 召回失败 → 回 `__tests__/evaluation/` 修 extractor。

## 16.5 本章小结

- **加语言**:跑 `/add-lang <lang>`,卡点是 wasm ABI 健康与节点名映射。
- **加 tool**:`tools.ts` 的 `TOOL_HANDLERS` 加 handler,`CODEGRAPH_MCP_TOOLS` 控制曝光。
- **改 schema**:`migrations.ts` 追加 `migration_N`,索引同步加。
- **评测门**:`/agent-eval` 双臂必须全 fixture `recall>=0.5`。

## 16.6 常见踩坑

- **ABI 不匹配**:wasm 用 ABI 13 旧 grammar,`check-grammar.mjs` FAIL——vendor ABI 14/15 新构建。表现:首文件正常,后续 ERROR tree。
- **wasm parity 失败**:kernel bump patch 不重 vendor,CI `kernel-grammar-parity` 挂。修法:同步 vendor,或参考 ruby/r/luau 注释明确"same-revision not same-ABI"(`Cargo.toml:39-54`)。
- **migration 忘加索引**:大索引 query 退化,Ch15 评测 latencyMs 飙升。**所有 migration 必须 `CREATE INDEX IF NOT EXISTS`**。
- **漏改 DEFAULT_CONFIG.include**:`init` 找 0 文件但不报错,`SKILL.md` step 4 第 1 项专门提醒。
- **vendor wasm 不在 `src/extraction/wasm/`**:`copy-assets` 不拷,发布物里没有,wasm fallback 路径直接挂。

## 16.7 下一章预告

{{chapter:17}} 进入**部署与运维**——打包 npm、跨平台 prebuilds、release workflow、回滚路径,以及 daemon 在大型 monorepo 的实战。

## 16.8 参考

- `.claude/skills/add-lang/SKILL.md:1-50`——10 步工作流。
- `codegraph-kernel/Cargo.toml:1-50`——14 个 grammar crate 与 ABI 注释。
- `src/extraction/grammars.ts:20-53`——WASM_GRAMMAR_FILES(33 项)。
- `src/types.ts:77-120`——LANGUAGES(42 项)。
- `src/mcp/tools.ts:1-200`——tool 注册框架。
- `src/database/migrations.ts`——migration 模板。
- Ch12 · Rust 内核与 ABI 契约;Ch15 · 评估体系。