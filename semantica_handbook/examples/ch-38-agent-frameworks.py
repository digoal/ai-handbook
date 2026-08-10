# examples/ch-38-agent-frameworks.py
# Handbook chapter: Agent Frameworks 集成 — Agno 原生 + 6 家二等
#
# This is a stub that prints the chapter metadata. For real usage, install
# semantica first: `pip install semantica` (see [[ch-03-install]]).
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

CHAPTER_SLUG = "ch-38-agent-frameworks"
CHAPTER_TITLE = "Agent Frameworks 集成 — Agno 原生 + 6 家二等"

print(f"handbook example for: {CHAPTER_SLUG}")
print(f"  title: {CHAPTER_TITLE}")
print(f"  → see docs/chapter for details")

try:
    import semantica  # noqa: F401
    print("semantica: importable")
except ImportError:
    print("semantica: SKIPPED (pip install semantica)")
