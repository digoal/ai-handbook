# Handbook Examples

`examples/` 目录为 handbook 每个章节提供最小可跑示例, 对应 56 章。

## 运行方式

```bash
# 1) 跑单个示例
python examples/ch-01-welcome.py

# 2) 跑全部
for f in examples/ch-*.py; do echo "== $f =="; python "$f"; done

# 3) 完整 import semantica (推荐)
pip install semantica
```

## 模板

每个 stub 默认行为:

```python
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-NN-name"
CHAPTER_TITLE = "..."

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")

try:
    import semantica
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
```

## 生成方式

`scripts/generate_examples.py` 扫描 `part-*/ch-*.md` 的 frontmatter (title / slug),为每章生成 stub。重新生成:

```bash
python scripts/generate_examples.py
```

stub 已存在则跳过, 不覆盖手工补充的真实示例 (如 ch-04 完整 archetype test)。

## 索引

| Chapter | Stub |
|---|---|
| ch-01-welcome | `ch-01-welcome.py` |
| ch-02-three-perspectives | `ch-02-three-perspectives.py` |
| ... | ... |
| ch-56-changelog-references | `ch-56-changelog-references.py` |