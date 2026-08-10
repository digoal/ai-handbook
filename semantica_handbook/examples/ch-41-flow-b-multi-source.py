# examples/ch-41-flow-b-multi-source.py
# Handbook chapter: Flow B — 多源 → 去重 → 冲突 → 推理 → 决策
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-41-flow-b-multi-source"
CHAPTER_TITLE = "Flow B — 多源 → 去重 → 冲突 → 推理 → 决策"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
