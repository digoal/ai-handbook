# examples/ch-40-flow-a-text-to-graph.py
# Handbook chapter: Flow A — 文本 → 实体 → 图谱 → 查询 → 可视化
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-40-flow-a-text-to-graph"
CHAPTER_TITLE = "Flow A — 文本 → 实体 → 图谱 → 查询 → 可视化"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
