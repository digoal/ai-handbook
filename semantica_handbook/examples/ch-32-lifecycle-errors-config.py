# examples/ch-32-lifecycle-errors-config.py
# Handbook chapter: 生命周期 / 异常体系 / 配置深探
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-32-lifecycle-errors-config"
CHAPTER_TITLE = "生命周期 / 异常体系 / 配置深探"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
