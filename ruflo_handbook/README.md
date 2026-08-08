# Ruflo 实战手册

> *An agent meta-harness for Claude Code and Codex — 从理念到造轮子的 19 章中文实战教程*

[![Ruflo](https://img.shields.io/badge/ruflo-v3.32.9-blue)](https://github.com/ruvnet/ruflo)
[![Claude Code](https://img.shields.io/badge/claude--code-compatible-green)](https://claude.ai/code)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Sandbox](https://img.shields.io/badge/sandbox-verified-orange)](#sandbox)

---

## 这是什么？

一本**场景化、可验证的中文教程**，配套 ruflo（开源 agent 元框架）使用。

- 📖 **19 章**：从理念（ch01）→ 安装（ch02）→ 跑通（ch03）→ 拆原理（ch04）→ 协作（ch06）→ 记忆（ch07）→ 安全（ch10）→ 联邦（ch09）→ 场景剧本（ch14）→ 自己造轮子（ch15-16）
- 🧪 **沙箱可验证**：每章 Hands-on 都通过 `sandbox/verify-chapter.sh <N>` 真实跑通
- 🎯 **6 类读者路径**：选你对应的身份，按推荐章节阅读

> 📘 与 [USERGUIDE.md](https://github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md)（292KB 参考手册）互补：本手册是「教程」，USERGUIDE 是「参考」。

---

## 我该读哪些章？（6 类读者路径）

| 你是… | 关注点 | 推荐章节 | 耗时 |
|------|--------|---------|------|
| 🅰️ **好奇的 Claude Code 用户** | 想让 Claude Code 变聪明一点 | 01 → 02 → 03 → 07 → 14（场景 1/2）→ 17 | 2–3 h |
| 🅱️ **个人开发者 / Indie Hacker** | 想用本地 Ollama + agent | 01 → 02 → 03 → 05 → 07 → 08 → 14（场景 3/10）→ 17 | 4–5 h |
| 🅲️ **小团队 Lead（5–10 人）** | 想给团队上 agent 协作 + 联邦 | 01 → 02 → 03 → 04 → 06 → 07 → 09 → 12 → 13 → 14（场景 5/12）→ 17 | 1–2 d |
| 🅳️ **平台工程师 / SRE** | 关心可观测、成本、安全 | 01 → 02 → 04 → 08 → 09 → 10 → 11 → 13 → 17 → 18 | 1–2 d |
| 🅴️ **Plugin Builder** | 想自己造插件 / agent / MCP | 01 → 02 → 04 → 05 → 11 → 15 → 16 → 19 | 2–3 d |
| 🅵️ **安全/合规审计员** | 看 AIDefence、加密、合规 | 01 → 09 → 10 → 13 → 17 | 半天 |

---

## 快速开始（5 分钟看到回报）

```bash
# 1. 克隆本手册（你已经在里面）
cd /Users/digoal/new/ruflo_handbook

# 2. 初始化沙箱
bash sandbox/setup.sh

# 3. 跑一遍通用断言（确认 ruflo CLI 可用；首次会下载 ruflo npm 包，1-3 分钟）
bash sandbox/verify-chapter.sh 0

# 4. 进入沙箱并跑通第 2 章（init/doctor/verify）
cd /tmp/ruflo-sandbox-default
bash bootstrap.sh
bash verify-chapter.sh 2

# 5. 开始读 Chapter 02，跟着做
open ../chapters/02-install-and-init.md   # 或用你喜欢的编辑器
```

---

## 术语速查

> 完整术语表见 [Chapter 17](./chapters/17-terminology-glossary.md)

| 术语 | 一句话 | 详见 |
|------|--------|------|
| **Swarm** | 多 agent 协同工作组 | ch06 |
| **Hive Mind** | Queen 主导的层级协作 | ch06 |
| **Queen** | Swarm 战略决策者（3 种类型） | ch06 |
| **MCP Server** | Model Context Protocol 服务端 | ch04 |
| **AgentDB** | Agent 专用向量数据库（HNSW） | ch07 |
| **SONA** | Self-Optimizing Neural Architecture | ch07 |
| **MoE** | Mixture of Experts（8 专家路由） | ch07 |
| **ReasoningBank** | 模式存储 + 4 步流水线 | ch07 |
| **Anti-Drift** | 防漂移默认配置（小团队 + 层级 + Raft） | ch06 |
| **Federation** | 跨机器零信任 agent 协作 | ch09 |
| **Trust Ladder** | 5 级信任阶梯 | ch09 |
| **WASM** | WebAssembly 沙箱模块 | ch10/ch16 |
| **Hook** | 生命周期事件回调 | ch11 |
| **Worker** | 后台 12 种 worker（audit/optimize/...） | ch11 |
| **3-Tier Routing** | codemod → Haiku → Sonnet 三层路由 | ch08 |
| **Witness** | Ed25519 签名安装校验 | ch10 |
| **AIDefence** | AI 操作防御（6 类检测） | ch10 |
| **SPARC** | 5 阶段开发方法论 | ch16 |
| **ADR** | Architecture Decision Record | ch16/ch19 |
| **RUCH** | *R*uflo *U*niversal *C*onfiguration *H*ub | ch15 |

---

## 目录

| 编号 | 标题 | 读者 | 预估 |
|------|------|------|------|
| 01 | [认识 Ruflo](./chapters/01-ruflo-intro.md) | 全部 | 15 min |
| 02 | [安装与初始化](./chapters/02-install-and-init.md) | 全部 | 30 min |
| 03 | [第一次对话：Hooks 自动接管](./chapters/03-first-conversation.md) | A/B/C | 20 min |
| 04 | [架构深潜](./chapters/04-architecture-deep-dive.md) | C/D/E | 60 min |
| 05 | [Agent、Skill、Slash Command 三件套](./chapters/05-agents-and-skills.md) | B/C/E | 45 min |
| 06 | [蜂群协作：拓扑、共识、Worktree](./chapters/06-swarm-coordination.md) | C | 60 min |
| 07 | [记忆与学习](./chapters/07-memory-and-learning.md) | A/B/C/D | 75 min |
| 08 | [智能路由与成本控制](./chapters/08-routing-and-cost.md) | B/D | 45 min |
| 09 | [联邦：mTLS + ed25519 + 五级信任](./chapters/09-federation.md) | C/D/F | 60 min |
| 10 | [安全与 AIDefence](./chapters/10-security-and-aidefence.md) | D/F | 60 min |
| 11 | [Hooks 与后台 Workers](./chapters/11-hooks-and-workers.md) | D/E | 45 min |
| 12 | [插件生态：33+ 插件选型](./chapters/12-plugin-ecosystem.md) | C | 60 min |
| 13 | [可观测性与运维](./chapters/13-observability-and-ops.md) | D | 60 min |
| 14 | [场景 Cookbook（14 剧本）](./chapters/14-scenario-cookbook.md) | 全部 | 180 min |
| 15 | [Builder 指南](./chapters/15-builder-guide.md) | E | 90 min |
| 16 | [进阶模块深读](./chapters/16-extended-modules.md) | E | 90 min |
| 17 | [术语表](./chapters/17-terminology-glossary.md) | 全部 | 30 min |
| 18 | [故障排查](./chapters/18-troubleshooting.md) | D | 30 min |
| 19 | [引用与版本快照](./chapters/19-references.md) | 全部 | 15 min |

---

## Sandbox

本手册的每一章 Hands-on 都通过 `sandbox/verify-chapter.sh <N>` 验证。

- **本地模式**（推荐）：`bash sandbox/setup.sh` → 工作区在 `/tmp/ruflo-sandbox-default/`
- **Docker 模式**：`docker build -t ruflo-sandbox sandbox/ && docker run --rm -it -v $(pwd):/handbook ruflo-sandbox`

详见 [sandbox/README.md](./sandbox/README.md)

---

## 交付物清单

| 文件 | 大小 | 用途 |
|------|------|------|
| `manual.md` | 454 KB / 12,407 行 | 聚合版（可转 PDF/HTML/EPUB） |
| `ruflo-handbook.html` | 1.0 MB | 离线阅读版（浏览器直接打开） |
| `ruflo-handbook.epub` | 282 KB | 电子书版（iBooks / Calibre / Kindle） |
| `chapters/NN-*.md` | 19 个文件 / 446 KB | 单章节源文件（按章阅读/PR 编辑） |

### 生成/重新生成

```bash
# 重新聚合 manual.md
node tools/build-manual.mjs

# 生成 HTML（无需 LaTeX）
pandoc manual.md -o ruflo-handbook.html --toc --toc-depth=2 --standalone

# 生成 EPUB
pandoc manual.md -o ruflo-handbook.epub --toc --toc-depth=2 \
  --metadata title="Ruflo 实战手册"

# 生成 PDF（需先 brew install --cask mactex）
pandoc manual.md -o ruflo-handbook.pdf --toc --toc-depth=2 \
  -V geometry:margin=2.5cm -V mainfont="PingFang SC" \
  --pdf-engine=xelatex
```

> ⚠️ 本环境未安装 xelatex（macOS 默认无 LaTeX）；HTML/EPUB 版本已生成可直接使用。装 [MacTeX](https://tug.org/mactex/) 后即可生成 PDF。

---

## 版本快照

| 字段 | 值 |
|------|-----|
| **Ruflo 版本** | 3.32.9 |
| **Ruflo Commit** | `26c35b59b40a0a95b286ccf5ac675a15edcc995f` |
| **手册版本** | v0.1（M0–M2 已完成） |
| **验证日期** | 2026-07-23 |
| **Node 要求** | ≥ 20.0.0 |
| **pnpm 要求** | ≥ 9 |

> 📘 章节顶部会标注 `LAST_VERIFIED_AGAINST:` 字段；若与该 commit 差异 > 30 天，需更新。

---

## 贡献

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。简要：

1. Fork → 创建分支 `chapter-XX-topic`
2. 在 `sandbox/asserts/chXX.sh` 增加断言
3. 在对应 `chapters/NN-*.md` 加 `LAST_VERIFIED_AGAINST: <commit>`
4. 跑 `bash sandbox/verify-chapter.sh XX` 全绿后提 PR

---

## License

MIT © 2026 — 与 ruflo 主项目一致。