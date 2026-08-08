# 贡献指南（CONTRIBUTING）

欢迎为 Ruflo 实战手册添砖加瓦。本手册与 [ruflo 主项目](https://github.com/ruvnet/ruflo) 互补，专注**场景化教程**。

## 协作流程

### 1. Fork 与分支

```bash
git fork https://github.com/your-org/ruflo_handbook
git clone <your-fork>
git checkout -b chapter-XX-topic
```

### 2. 修改对应章节

每章文件命名固定为 `chapters/NN-kebab-case-name.md`，编号严格递增。

### 3. 编写断言（必做）

每个新加的 Hands-on 必须在 `sandbox/asserts/ch{N}.sh` 注册断言。例如：

```bash
# sandbox/asserts/ch14.sh
assert "场景 14.1 PR 审查触发 reviewer agent" 0 bash -c '
  cd /tmp/ruflo-sandbox-default
  timeout 120 npx --yes ruflo@latest agent spawn -t reviewer --name pr-bot
'
```

`assert` 函数定义在 `sandbox/verify-chapter.sh`，签名：

```bash
assert "描述" <期望退出码> <命令...>
```

### 4. 更新 frontmatter（必做）

每章顶部加/更新：

```markdown
---
title: 第 14 章 · 场景 Cookbook
last_verified_against: 26c35b59b40a0a95b286ccf5ac675a15edcc995f
verified_at: 2026-07-23
chapter: 14
---
```

`last_verified_against` 必须是当前 ruflo HEAD 的完整 commit SHA，可这样取：

```bash
git -C /Users/digoal/new/ruflo rev-parse HEAD
```

### 5. 跑通断言

```bash
bash sandbox/verify-chapter.sh 14
```

直到 `PASS=N FAIL=0` 才能提 PR。

### 6. 提 PR

PR 描述必须包含：

- 修改章节列表（chXX: 简述）
- `verify-chapter.sh` 输出（前 30 行 + 末尾 PASS/FAIL 行）
- 若改文档，截图前后对比
- 若发现 CLI 行为与文档不一致，**单独**开 issue 标签 `docs-drift`

---

## 写作规范

### 语言与术语

- **正文**：简体中文，技术名词保留英文（agent / swarm / hook / witness 等不译）
- **首次出现**的中英对照术语，链接到 `chapters/17-terminology-glossary.md`
- **避免编造**：所有断言必须可追溯到 `/Users/digoal/new/ruflo/` 内具体文件 + 行号

### 代码块

- 所有 CLI 默认使用 `npx --yes ruflo@latest <cmd>`（沙箱内）或 `ruflo <cmd>`（已全局安装）
- 关键命令加 ANSI 颜色说明或截图
- 长输出（前 20 行）放在 `### Verify H{N}.{M}` 段

### 图示

- 优先 **Mermaid**（GitHub 原生支持）：graph TD / sequenceDiagram / stateDiagram-v2
- 关键架构图额外提供 SVG（存 `assets/diagrams/`）

### 章节统一 6 段

```markdown
# 第 NN 章 · <章名>

> 📘 摘要（200–300 字）
> 🏷️ 读者画像：A/B/C/D/E/F 标记
> 🕐 预估耗时：XX 分钟
> ✅ LAST_VERIFIED_AGAINST: <sha>

## 1. 背景与动机
## 2. 核心概念
## 3. 架构/原理（必要时配 Mermaid 图）
## 4. Hands-on（2–4 个真实可跑场景）
## 5. 沙箱验证（Run / Observe / Expect 三段式）
## 6. 小结 + 术语锚点 + 参考链接
```

---

## 版本兼容矩阵

| 手册版本 | Ruflo 版本 | Node | pnpm | 验证日期 |
|---------|-----------|------|------|---------|
| v0.1 (M0-M2) | 3.32.9 | ≥ 20 | ≥ 9 | 2026-07-23 |

> 若手册 v0.1 之外出现新章节未带 `last_verified_against` 字段，CI 拦截。

---

## drift 防护（CI）

`.github/workflows/drift-check.yml`（建议）：

```yaml
name: Drift Check
on: [push, pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: bash sandbox/setup.sh
      - run: bash sandbox/verify-chapter.sh all
      - name: 检查每章 frontmatter
        run: |
          for f in chapters/*.md; do
            grep -q "last_verified_against:" "$f" || { echo "$f 缺 last_verified_against"; exit 1; }
          done
```

---

## 联系方式

- 主项目 issue: <https://github.com/ruvnet/ruflo/issues>
- 手册专属 issue: <https://github.com/your-org/ruflo_handbook/issues>
- 标签约定：`docs-drift`、`chapter-XX`、`builder-question`

---

## License

MIT © 2026