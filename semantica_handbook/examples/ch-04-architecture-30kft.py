# examples/ch-04-architecture-30kft.py
# Handbook chapter: 30,000 英尺架构图 — 6 大层与端到端数据流
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-04-architecture-30kft"
CHAPTER_TITLE = "30,000 英尺架构图 — 6 大层与端到端数据流"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
