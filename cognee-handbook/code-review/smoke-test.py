#!/usr/bin/env python3
"""Cognee v1.4.0 API smoke test for cognee-handbook chapters.

Level 1 checks imports, version, enum members, callability, signatures, and
source paths without invoking an LLM. Level 2 is an opt-in round trip when
OPENAI_API_KEY is configured.
"""
from __future__ import annotations

import inspect
import os
import sys
from pathlib import Path

import pytest

# Resolve the cognee source tree once at import time:
#   1. If $COGNEE_REPO is set, use it (and prepend to sys.path as fallback).
#   2. Otherwise, infer the repo root from `cognee.__file__`
#      (`<COGNEE_REPO>/cognee/__init__.py` → parent.parent).
_env_repo = os.environ.get("COGNEE_REPO")
if _env_repo:
    COGNEE_REPO = Path(_env_repo)
    if str(COGNEE_REPO) not in sys.path:
        sys.path.insert(0, str(COGNEE_REPO))
else:
    # Imported later by individual tests, but we resolve eagerly so the
    # `paths_exist` test can use COGNEE_REPO regardless of import order.
    try:
        import cognee as _cognee_pkg
        COGNEE_REPO = Path(_cognee_pkg.__file__).resolve().parent.parent
    except ImportError:
        COGNEE_REPO = None  # tests will surface the real install issue


def test_cognee_importable():
    import cognee
    assert cognee is not None


def test_cognee_version_1_4():
    import cognee
    ver = getattr(cognee, "__version__", "")
    assert "1.4" in ver, f"Expected 1.4.x, got {ver!r}"


def test_search_type_enums_present():
    from cognee.modules.search.types.SearchType import SearchType

    needed = [
        "GRAPH_COMPLETION", "RAG_COMPLETION", "TRIPLET_COMPLETION",
        "CYPHER", "NATURAL_LANGUAGE", "FEELING_LUCKY", "CODE",
        "CHUNKS", "SUMMARIES", "TEMPORAL",
    ]
    for name in needed:
        assert hasattr(SearchType, name), f"missing SearchType.{name}"
    assert len(SearchType) >= 15


def test_top_level_apis_callable():
    import cognee
    for fn in ("add", "cognify", "search", "remember", "recall", "memify", "prune"):
        assert callable(getattr(cognee, fn, None)), f"cognee.{fn} not callable"


def test_api_signatures():
    import cognee
    assert list(inspect.signature(cognee.add).parameters)[:2] == ["data", "dataset_name"]
    assert "query_type" in inspect.signature(cognee.search).parameters
    assert "data" in inspect.signature(cognee.remember).parameters
    assert "query_text" in inspect.signature(cognee.recall).parameters


def test_cognee_repo_paths_exist():
    paths = [
        "cognee/api/v1/add/add.py", "cognee/api/v1/cognify/cognify.py",
        "cognee/api/v1/search/search.py", "cognee/api/v1/remember/remember.py",
        "cognee/api/v1/recall/recall.py", "cognee/modules/memify/memify.py",
        "cognee/api/v1/prune/prune.py",
    ]
    assert COGNEE_REPO is not None, (
        "COGNEE_REPO could not be resolved. Either pip-install cognee "
        "(`uv pip install cognee`) or set $COGNEE_REPO to the cognee repo root."
    )
    for rel in paths:
        assert (COGNEE_REPO / rel).exists(), f"missing {rel}"


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set — real LLM round-trip skipped")
def test_add_cognify_search_roundtrip():
    import asyncio
    import cognee
    from cognee.modules.search.types.SearchType import SearchType

    async def run():
        await cognee.add("Cognee is a memory framework for LLM agents.", dataset_name="smoke_test")
        await cognee.cognify(datasets=["smoke_test"])
        results = await cognee.search("What is Cognee?", SearchType.GRAPH_COMPLETION)
        assert len(results) >= 1
        await cognee.prune.prune_system()

    asyncio.run(run())


def pytest_sessionfinish(session, exitstatus):
    out = Path(__file__).parent / "smoke-test-report.md"
    outcome = "PASS" if exitstatus == 0 else "FAIL"
    lines = [
        "# Cognee v1.4.0 Smoke Test Report", "",
        f"- Exit code: `{exitstatus}`", f"- Overall result: **{outcome}**",
        f"- Tests collected: `{session.testscollected}`",
        "- Scope: Level 1 API/import/enum/signature/path checks; Level 2 requires OPENAI_API_KEY.", "",
        "## Ten core APIs", "",
        "| API | Verification |", "|---|---|",
        "| `cognee.add(text, dataset_name)` | Level 1 callable/signature |",
        "| `cognee.cognify()` | Level 1 callable |",
        "| `cognee.search(..., GRAPH_COMPLETION)` | Enum/signature; real result Level 2 |",
        "| `cognee.search(..., RAG_COMPLETION)` | Enum/signature; real result Level 2 |",
        "| `cognee.search(..., CYPHER)` | Enum/signature callable |",
        "| `cognee.remember()` / `recall()` | Level 1 callable/signature |",
        "| `cognee.memify()` | Level 1 callable |",
        "| `SearchType.FEELING_LUCKY` / `CODE` | Level 1 enum presence |",
        "| `cognee.prune()` | Export presence; implementation exposes `prune_system` |", "",
        "## Result interpretation", "",
        "Level 1 is designed to pass without LLM access. Level 2 is skipped when `OPENAI_API_KEY` is absent.",
        "Any failed Level 1 check indicates API drift and should be reviewed before revising chapters.", "",
        "## Known drift / follow-up", "",
        "- Source exposes prune as a `prune` class with `prune_data()` and `prune_system()`, not a callable function; this is a documented API-shape drift.",
        "- The requested historical path `cognee/api/v1/prune.py` is a package; the existing implementation is `cognee/api/v1/prune/prune.py`.", "",
        "## Environment", "",
        "- The script prepends the `COGNEE_REPO` env var path to `sys.path` as an import fallback when editable install is unavailable.",
        "- No real LLM call is required for Level 1.", "",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
