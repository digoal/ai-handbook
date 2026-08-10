---
title: CI/CD — GitHub Actions 9 大工作流
slug: ch-46-cicd
part: part-vi-operations
audience: all
reading_time: 9
prerequisites: [ch-44-k8s-helm]
semantica_version: 0.6.0
---

# ch-46 CI/CD — GitHub Actions 9 大工作流

> Semantica 仓库 `. `.github/workflows/` 有 9 个 yml, 覆盖 PR/release/docs/benchmark/codeql/security 六大场景。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- PR / push 到 main → 自动跑 ci.yml (前端测试 + Python build + wheel 校验)。
- 推 `v*` tag → 自动 release.yml (OIDC/SLSA attestation + PyPI Trusted Publishing)。
- docs 改动 → docs.yml (Mintlify 校验 + 部署到 GitHub Pages)。
- 手动触发 benchmark.yml → Python 3.12 跑基准 (`BENCHMARK_REAL_LIBS=1`)。
- 每周一 cron + 手动 → security.yml (`pip-audit` 依赖审计)。
- verify-action-pins.yml → 校验所有 GitHub Actions 都被 pin 到 commit SHA (防供应链攻击)。

### 1.2 工作流适配矩阵

| 文件 | 触发 | 用途 |
|---|---|---|
| `ci.yml` | PR / push main | 装 + Explorer 测试 + Python build + wheel 校验 |
| `release.yml` | `v*` tag | SLSA attestation + GitHub Release + PyPI 发布 |
| `docs.yml` | docs/** 改动 | `docs_check.py` + Mintlify export + Pages 部署 |
| `benchmark.yml` | 手动 | Python 3.12 基准 |
| `codeql.yml` | CodeQL 安全扫描 | GitHub 默认 |
| `defender-for-devops.yml` | Microsoft Defender 集成 | 企业合规 |
| `security-scan.yml` | 综合 SCA/SBOM 流程 | 9 KB, 多工具 |
| `security.yml` | 每周一 cron + 手动 | `pip-audit` 审计 |
| `verify-action-pins.yml` | PR | 防供应链攻击 |

### 1.3 一段最小可跑示例

本地复刻 ci.yml 的 3 步:

```bash
# 1) 装
pip install ".[all]"

# 2) 前端测试
cd explorer
npm run test:graph-store
npm run test:graph-workspace
npm run test:plugin-registry
cd ..

# 3) Python build + wheel 校验
python -m build
python -c "import zipfile; z=zipfile.ZipFile('dist/semantica-0.6.0-py3-none-any.whl'); print('semantica/static/index.html' in z.namelist())"
```

### 1.4 何时不用

- 你不用 GitHub → fork 这些 yml 改用 GitLab CI / Jenkins。
- 你只跑前端 → 用 `explorer/tests/` 的 3 个 node --test 文件。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `.github/workflows/ci.yml` — 主 CI (PR + main)。
- `.github/workflows/release.yml` — 发布 (tag 触发, OIDC + SLSA)。
- `.github/workflows/docs.yml` — 文档 (Mintlify 部署)。
- `.github/workflows/benchmark.yml` — 基准。
- `.github/workflows/codeql.yml` — CodeQL 扫描。
- `.github/workflows/security-scan.yml` — 综合扫描 (9 KB)。
- `.github/workflows/security.yml` — pip-audit。
- `.github/workflows/defender-for-devops.yml` — Defender 集成。
- `.github/workflows/verify-action-pins.yml` — Action 锁定校验。

### 2.2 最小复现脚本

```bash
# 模拟 ci.yml 在本地的 3 步
pip install ".[test]"
cd explorer && npm ci && npm run test:graph-store && cd ..
python -m build
```

### 2.3 扩展点

- **加新工作流**: 在 `.github/workflows/` 加 `xxx.yml`, 复用 `actions/checkout@v4` (SHA-pin)。
- **改触发**: 在 `on:` 加 `pull_request` / `schedule` / `workflow_dispatch`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 SLSA attestation?**
- 供应链安全 (Supply Chain Levels for Software Artifacts) 是 PyPI 信任发布的未来方向。
- Semantica 提前支持, 给企业客户提供可信保证。

**为什么 Action pin 到 commit SHA?**
- 防止 Action 被恶意篡改 (e.g., tj-actions/changed-files 2025 事件)。
- `verify-action-pins.yml` 强制所有 PR 不能引入 unpinned action。

### 3.2 与同类对比

| 维度 | Semantica CI | LangChain CI | LlamaIndex CI |
|---|---|---|---|
| Workflow 数 | 9 | 4 | 3 |
| SLSA | ✅ | ❌ | ❌ |
| Action pinning | ✅ 自动校验 | ⚠ 手动 | ❌ |

### 3.3 何时重新设计

- workflow > 15 → 拆 `.github/workflows/release/` 子目录。
- 引入 monorepo → 引入 path-based trigger。

## 跨章引用

- 上一章: [[ch-45-cloud-platforms]]
- 下一章: [[ch-47-performance-benchmark]]
- 安全: [[ch-49-security]]