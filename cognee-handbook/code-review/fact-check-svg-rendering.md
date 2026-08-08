# SVG 渲染 fact-check 报告

> 工作目录:`<HANDBOOK_REPO>`
> 代码基线:cognee v1.4.0(2026-07-26)
> 触发日期:2026-07-26
> M13 路径核查批 1 暴露问题:用户发现 SVG 引用相对路径错

---

## 1. 触发

M13 路径核查批 1(Ch01/Ch02/Ch03,3 subagent 并行)后,用户在审查阶段指出:**"svg 的引用地址错了呀, 相对路径位置错了"** — 触发器是肉眼巡视第 1 章 README 中引用 SVG 的形态,而非 subagent 报告。

M11/M12 的 SVG 审计报告(见 `code-review/svg-audit-report.md`)只看"文件名引用 vs 实际文件存在性",**未实际验证 Pandoc 编译时能否解析**。M13 批 1 三个 subagent 同样基于错误前提(38:38 全对齐)pass-过 SVG 维度。

---

## 2. 根因(实证复盘)

### 2.1 文件与引用关系

| 项 | 实际位置 |
|---|---|
| Chapter markdown | `<HANDBOOK_REPO>/chapters/part-XX-foundation/chapter-XX-...md`(深度 2) |
| SVG 资产 | `<HANDBOOK_REPO>/assets/diagrams/chXX-NN-...svg`(仓库根,深度 0) |
| Markdown image 引用 | `(assets/diagrams/chXX-NN-...svg)` |
| 期望相对路径 | `(../../assets/diagrams/chXX-NN-...svg)`(从 chapter dir 上溯 2 级) |

### 2.2 Pandoc 默认 image 解析

Pandoc 默认按 **input file 所在目录**解析 markdown 内的 `<img src>`,而非调用 cwd。

测试结果(独立章节文件 + `--embed-resources --standalone`):

| Markdown 引用形式 | Pandoc 嵌入 SVG? |
|---|---|
| `(assets/diagrams/foo.svg)`(M12 前形态) | ✗ `Could not fetch resource`(找 `chapters/part-XX/assets/diagrams/...`) |
| `(../../assets/diagrams/foo.svg)`(修复后) | ✓ 嵌入 1 个 `data:image/svg+xml;base64` |
| `(file:///.../assets/diagrams/foo.svg)`(绝对) | ✓ 嵌入,但不写 commit 信息会泄漏本地路径 |

### 2.3 影响面

- `dist/cognee-handbook.html`(3.85 MB)重构前 7.5 KB,38 个 `<img>` 标签 **0 个**(SVG 全部丢失)
- `dist/cognee-handbook.epub`(828 KB)重构前 `EPUB/media/` 不含 SVG
- `dist/cognee-handbook.pdf`(9.4 MB)文字内容完整,**但 mermaid 图全无**
- 修后:`dist/cognee-handbook.html` 内嵌 38 SVG(~2.6 MB inline),`dist/cognee-handbook.epub` 含 38 SVG 文件,`cognee-handbook.pdf` 经 chrome headless 把 SVG 转矢量 path 渲染

---

## 3. 修复(A + C 同时修)

### 3.1 A 部分:批量替换 markdown 引用

```bash
find chapters -name "chapter-*.md" -exec perl -pi -e \
  's|\(assets/diagrams/|(../../assets/diagrams/|g' {} +
```

| 项 | 值 |
|---|---|
| 替换前 `assets/diagrams/` 命中数 | 38(全在 `chapters/`,深度 2 路径) |
| 替换后 `(../../assets/diagrams/...)` 命中数 | 38 |
| Python 反向核对(`md.parent / rel.resolve()`) | 38/38 全部可达 |

### 3.2 C 部分:预防下次跑错

**1. `shared-context/mermaid_to_svg.py`**(`script` 写回 inline mermaid 块时):

把 `Path("assets") / "diagrams" / (mmd.stem + ".svg")` 改为 `Path("..", "..", "assets", "diagrams", mmd.stem + ".svg")` — 让脚本下次写出的 image 引用默认就是基于 chapter file 视角的相对路径。

**2. `Makefile` 三处 Pandoc 调用加 `--resource-path`**:

```makefile
PANDOC_RP := --resource-path=. \
  --resource-path=chapters/part-01-foundation \
  --resource-path=chapters/part-02-architecture \
  --resource-path=chapters/part-03-api \
  --resource-path=chapters/part-04-integrations \
  --resource-path=chapters/part-05-production
```

`epub` / `pdf` / `html` 三处 pandoc 调用都加 `$(PANDOC_RP)` 与 `--embed-resources`(替代 `--self-contained`,后者在 pandoc 3.5 已 deprecated)。

**3. `Makefile verify` 目标 grep 升级**:

```diff
-  grep -rho 'assets/diagrams/[^)"]*\.svg'
+  grep -rEho '(?:\.\./)?(?:\.\./)?assets/diagrams/[^)"]*\.svg'
```

同时识别 `assets/diagrams/...` 和 `../../assets/diagrams/...` 两种形式。

---

## 4. 验证

### 4.1 渲染验证(3 形态各 1)

| 产物 | 验证 | 结果 |
|---|---|---|
| `dist/cognee-handbook.html` | `<img src="data:image/svg+xml;base64,...">` 计数 | **38 / 38** |
| `dist/cognee-handbook.epub` | `EPUB/media/*.svg` 文件计数 | **38 / 38** |
| `dist/cognee-handbook.pdf` | chrome headless 渲染 | 通过(`--print-to-pdf` 9.8 MB) |

注:PDF 的 SVG 经 chrome 转矢量 path 后写入 PDF page object,**`pdfimages -list` 不会列出 raster 图**;PDF 文字与矢量 SVG path 都由 chrome 同一次渲染整合到 PDF 页面。

### 4.2 smoke / verify

```bash
$ make smoke
6 passed, 1 skipped in 8.07s  ✓

$ make verify
==> Inline mermaid blocks: 0
==> SVG refs count: 38      ✓
==> dist/ artifacts: 4 文件
```

### 4.3 路径泄漏

```bash
$ git diff chapters/ shared-context/ Makefile | grep -E "^\+" | grep -E "/Users/|/home/"
(empty)
```

---

## 5. 触及的文件清单

| 文件 | 改动 | 行数变化 |
|---|---|---|
| `chapters/part-XX/chapter-XX-*.md`(30 章) | `(assets/diagrams/...)` → `(../../assets/diagrams/...)` | 每章 1-3 处,共 38 处 |
| `shared-context/mermaid_to_svg.py` | `svg_rel` 默认加上 `..`/`..` 前缀 + 解释性注释 | 1 处 + 6 行注释 |
| `Makefile` | 新增 `PANDOC_RP` 变量 + 3 处 pandoc 调用加 `$(PANDOC_RP)` + `--embed-resources`(替代 `--self-contained`) + `verify` 目标 grep 升级 | 约 18 处改动 |

合计:**32 文件**,**+82 / -61**。

---

## 6. Batch 1 subagent 视角的失真

3 个 M13 批 1 subagent 都报告了"SVG 资产 1/0 缺失"(基于 `ls 验证文件存在` 层面的核对)。它们**不知道**本次根因(相对路径错配)因为:

1. 它们各自的 prompt(见 plan 模板)只让"ls 验证文件存在",未让"用 pandoc 实跑一次 chapter 看 SVG 真的被嵌入"
2. 它们没有共享 SVG 渲染上下文,各看各的

后续 M13 batch 2-13 subagent 需要新增维度:**"用 pandoc --embed-resources 单跑 target chapter,看嵌入的 `data:image/svg+xml;base64` 数 = 章节里 SVG 引用数"**。

---

## 7. 风格规约沉淀(主会话在 commit 后追加 style-guide.md)

新增 `<HANDBOOK_REPO>/style-guide.md` §15:

```markdown
## 15. SVG / 图片引用相对路径(M13 沉淀)

cognee-handbook 的 chapter markdown 位于 `chapters/part-XX/`(深度 2),SVG 在 `<HANDBOOK_REPO>/assets/diagrams/`(仓库根)。

- **正确写法**:`(../../assets/diagrams/chXX-NN-...svg)` — 上溯两级到仓库根
- **错误写法**:`(assets/diagrams/...)` — Pandoc 找 `chapters/part-XX/assets/...`,失败
- **绝对路径**:`(file:///Users/...)` — **禁止**(commit 信息会泄漏本地路径)
- **Makefile 兜底**:三处 Pandoc 调用已加 `--resource-path=. --resource-path=chapters/part-XX` 5 路
- **写新章节或重 extract 时**:`make verify` 应报 SVG refs = 38;若实际 < 38,查是否有 orphan 章节未引图
```

---

## 8. 同步约束

- 全程占位符 `<COGNEE_REPO>` / `<HANDBOOK_REPO>` — 无本地绝对路径泄漏
- 修复风格保留:不重写段落,只做最小化单 patch
- 不动 cognee / cognee-integrations / SVG 二进制
- dist/ 在 .gitignore,但工作树里 4 个产物已重建,作为本次修复的证据
