#!/usr/bin/env python3
"""
Validate handbook chapter frontmatter against templates/frontmatter.schema.json.

Usage:
    python scripts/validate_frontmatter.py [chapter.md ...]
    # Without arguments, validates every .md file under handbook/part-*/
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HANDBOOK_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = HANDBOOK_ROOT / "templates" / "frontmatter.schema.json"
PARTS = [
    "part-i-foundations",
    "part-ii-core-modules",
    "part-iii-cross-cutting",
    "part-iv-integrations",
    "part-v-workflows",
    "part-vi-operations",
    "part-vii-reference",
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_schema() -> dict:
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(md_text: str) -> tuple[dict | None, str | None]:
    m = FRONTMATTER_RE.match(md_text)
    if not m:
        return None, "missing frontmatter block (must start with --- and end with ---)"
    try:
        # Tiny YAML subset parser: only handles the keys used in our template.
        data = {}
        for line in m.group(1).splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                data[key] = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",") if v.strip()]
            elif value.startswith('"') and value.endswith('"'):
                data[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                data[key] = value[1:-1]
            elif value.lower() in ("true", "false"):
                data[key] = value.lower() == "true"
            else:
                try:
                    data[key] = int(value)
                except ValueError:
                    data[key] = value
        return data, None
    except Exception as e:  # pragma: no cover
        return None, f"YAML parse error: {e}"


def validate_one(md_path: Path, schema: dict) -> list[str]:
    text = md_path.read_text(encoding="utf-8")
    data, err = parse_frontmatter(text)
    errors: list[str] = []
    if err:
        return [f"{md_path}: {err}"]
    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"{md_path}: missing required key '{key}'")
    properties = schema.get("properties", {})
    for key, spec in properties.items():
        if key not in data:
            continue
        value = data[key]
        if "enum" in spec and value not in spec["enum"]:
            errors.append(f"{md_path}: '{key}'={value!r} not in {spec['enum']}")
        if "pattern" in spec and isinstance(value, str):
            if not re.match(spec["pattern"], value):
                errors.append(f"{md_path}: '{key}'={value!r} does not match pattern {spec['pattern']}")
        if spec.get("type") == "integer" and not isinstance(value, int):
            errors.append(f"{md_path}: '{key}' should be integer, got {type(value).__name__}")
        if "minimum" in spec and isinstance(value, (int, float)) and value < spec["minimum"]:
            errors.append(f"{md_path}: '{key}'={value} below minimum {spec['minimum']}")
        # Array element pattern (e.g., prerequisites: [ch-NN-slug, ...])
        if spec.get("type") == "array" and isinstance(value, list):
            item_spec = spec.get("items", {})
            item_pattern = item_spec.get("pattern")
            if item_pattern:
                for i, item in enumerate(value):
                    if not isinstance(item, str) or not re.match(item_pattern, item):
                        errors.append(f"{md_path}: '{key}[{i}]'={item!r} does not match pattern {item_pattern}")
    return errors


def iter_chapters(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    chapters: list[Path] = []
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            chapters.extend(sorted(part_dir.glob("ch-*.md")))
    return chapters


def main() -> int:
    schema = load_schema()
    chapters = iter_chapters(sys.argv[1:])
    all_errors: list[str] = []
    for md in chapters:
        all_errors.extend(validate_one(md, schema))
    if all_errors:
        print(f"✗ {len(all_errors)} frontmatter issue(s) found:")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print(f"✓ {len(chapters)} chapter(s) frontmatter valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())