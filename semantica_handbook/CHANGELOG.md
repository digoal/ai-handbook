# Handbook CHANGELOG

## [1.0.0] - 2026-08-10

### Added
- **56 章 handbook** 覆盖 7 个 Part (入门 / 核心模块 / 横切面 / 集成 / 工作流 / 部署 / 参考)。
- **15 张 mermaid 图** 渲染到 `assets/diagrams/*.svg` (14 张 + FIG-07 在 ch-33)。
- **56 个 examples stub** 在 `examples/`, 每个 ≤30 行, 抑制日志, try/except ImportError 兜底。
- **`docs/error-codes.md`** 错误码全集 (SEM001-005 + 行号)。
- **8 个 CI 校验脚本** (新增 4 个 + 改进 4 个):
  - `validate_frontmatter.py` — array element pattern
  - `lint_perspectives.py` — 高风险 token 加权 + unique ≥ 7
  - `check_links.py` — 去 KNOWN_FIGURES 回退 + Markdown 普通链接
  - `check_figures.py` — GHOST/ORPHAN/COLLISION 三态检测
  - `check_glossary_backlinks.py` — `--fix` 自动补链
  - `check_slug_filename.py` — stem 与 frontmatter slug 严格相等
  - `check_chapter_sections.py` — 三视角 + 跨章引用 必需节
  - `render_mmd.sh` — zsh 兼容 + puppeteer config fallback
- **5 个 ch-55 词条**: `method_registry` / `_ModuleProxy` / `build_knowledge_base` / `ConfigurationError` / `TypeError`。

### Fixed
- ch-14 `build_graph` → `build_kg` (同步 ch-42)
- ch-21 module-level API 拆分 (ContextGraph 实例方法走 `context_graph.py:2005/3326/3346`)
- ch-08 `register_reader` → `method_registry.register` (`ingest/registry.py:73`)
- ch-04 行号 `_ModuleProxy` 47→48 + `config_manager.py:658` → `:585 merge_configs`
- ch-30 `_handler` → `_tool_*`
- ch-03 LLM extras 14→9 (删 llama/azure/bedrock/cohere 等)
- ch-03 tripletstore extras 5→1 (其余走 SPARQL HTTP)
- ch-40/41/42 文件名 `flow-A` → `flow-a` 全小写
- **FIG-07 幽灵图**补到 ch-33 (LLM/向量库/图库 适配矩阵)
- **FIG-10 ch-43 错位**重归属 ch-44
- **FIG-11 编号冲突** ch-07 删重号, ch-32 保留
- ch-04 FIG-02 sequenceDiagram → flowchart TB (mermaid sequenceDiagram 解析失败回退)
- 32 处术语反链缺失全部自动补齐

### Changed
- README §6 维护脚本列表 4 → 8 项
- README §4 FIG 索引重排 (ch-43 / ch-44 分开)
- `lint_perspectives.py` 阈值从 ≥3 改为 unique ≥ 7 + weighted ≥ 14
- `validate_frontmatter.py` 增 array element pattern 校验
- `check_links.py` 去 `KNOWN_FIGURES` 静态回退, 用实际扫描
- `render_mmd.sh` 加 zsh glob 兼容 (`-print0 | while read -d ''`) + mmdc 缺失 WARN
- `check_glossary_backlinks.py` 加 `--fix` 选项

### Out of Scope
- mcp_server `SERVER_INFO["version"] = "0.4.0"` 不一致 (源码问题, 非 handbook)
- assets/images 真实产品截图 (需产品团队提供)
- 旧 `.png` 图位 (4 处已改为 ASCII / 反链描述)
- handbook 与 docs.getsemantica.ai 的同步 (Mintlify 站外)

## [0.9.0] - 2026-08-08 (内部测试版)

### Added
- 56 章初稿 + 1 README + 1 CONTRIBUTING + 1 GLOSSARY
- 4 个原始脚本 (validate / lint / check_links / render)

### Notes
- 内部测试用, 不发布, 已知 7 处硬错 + 3 处结构冲突

---

## 后续计划

### [1.1.0] 目标
- CI workflow 接入 (`.github/workflows/handbook-lint.yml`)
- handbook v0.7 同步 (Semantica v0.7 计划: `SEM005` 限流错误 + Knowledge 节点)
- 接入 Mintlify docs 自动同步
- 国际化 (i18n) 启动 zh-CN / en-US 双语

### [1.2.0] 目标
- 渲染精度: SVG 中文字体兼容
- 图像资产: 真实产品截图 (需产品团队)
- 教学视频: 嵌入关键章节