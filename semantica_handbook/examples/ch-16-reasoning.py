# examples/ch-16-reasoning.py
# Handbook chapter: 推理引擎 (Reasoning) — Rete + Datalog + SPARQL
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-16-reasoning"
CHAPTER_TITLE = "推理引擎 (Reasoning) — Rete + Datalog + SPARQL"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
