# examples/ch-12-semantic-extract.py
# Handbook chapter: 实体/关系抽取 (Semantic Extract) — LLM + 规则 + ML
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-12-semantic-extract"
CHAPTER_TITLE = "实体/关系抽取 (Semantic Extract) — LLM + 规则 + ML"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
