# examples/ch-06-quickstart-three-flows.py
# Handbook chapter: 三主轴最小可跑示例 (Flow A/B/C)
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-06-quickstart-three-flows"
CHAPTER_TITLE = "三主轴最小可跑示例 (Flow A/B/C)"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
