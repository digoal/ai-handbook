# 贡献与投稿指南

## 投稿流程

1. **先建章节骨架**: 复制 `templates/chapter.md` 到目标 part 目录, 命名 `ch-NN-slug.md`, 替换 frontmatter。
2. **frontmatter 必须包含**: `title / slug / part / audience / reading_time / prerequisites / semantica_version`。
3. **正文必须分三节**: 用户视角 / 开发者视角 / 架构师视角, 顺序固定。
4. **本地校验**: 提交前跑以下命令全部返回 0:

```bash
python scripts/validate_frontmatter.py
python scripts/lint_perspectives.py
python scripts/check_links.py
bash scripts/render_mmd.sh --check
```

## 风格约定

- 使用中文(简体), 技术名词保留英文原拼写(如 `_ModuleProxy`、`ConfigManager`、`KG`)。
- 代码块必须附文件名 / 行号 / 上下文; 不可裸引用 `def foo()` 而不说在哪。
- Mermaid 图标题统一 `### FIG-NN <图名>`, 编号与本手册 FIG 清单一致。
- 跨章引用统一 `[[ch-NN-slug]]` 与 `[[fig-NN]]` 双向链接, 不用裸文本。
- 截图暂用占位 `![ch-NN-name](assets/images/ch-NN-name.png)`, 渲染阶段替换。

## Commit 信息

格式:

```
<part>: <ch-NN> <一句话变更>

[可选 body: 列出具体改动 + 关联 issue]
```

例:

```
part-i-foundations: ch-04 补 FIG-2 sequenceDiagram 时序
```

## PR 模板

```markdown
## 章节
- ch-NN-slug

## 改动
- 新增 / 修订 / 删除
- ...

## 自查
- [ ] frontmatter 通过 validate_frontmatter.py
- [ ] 三视角分层通过 lint_perspectives.py
- [ ] 所有 [[]] 引用可达
- [ ] 新术语已加入 GLOSSARY.md
- [ ] 代码示例在 handbook/examples/ 下 mirror 且可跑
```