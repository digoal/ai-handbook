#!/usr/bin/env python3
"""Scan all Python code blocks in chapters/ for syntax errors, Unicode quotes,
and API mismatches."""
import ast
import re
import os
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # <HANDBOOK_REPO> 根
CHAPTERS = ROOT / "chapters"

# Patterns of API mismatches that MUST be fixed
API_DRIFT_PATTERNS = [
    # cognee.prune() bare call vs prune_data/prune_system
    (re.compile(r"(?:await\s+)?cognee\.prune\(\s*\)"), "cognee.prune()", "cognee.prune.prune_data() or prune_system()"),
    # cognee.search(search_type=...) in Python context
    (re.compile(r"cognee\.search\([^)]*search_type\s*="), "search_type=", "query_type="),
    # cognee.search(query="...") in v1 Python context
    (re.compile(r"cognee\.search\([^)]*query\s*=\s*[\"']"), "query=", "query_text="),
    # cognee.add(data, dataset_name=...) → dataset=
    (re.compile(r"cognee\.add\([^)]*dataset_name\s*="), "dataset_name=", "dataset="),
]

CURVY_QUOTES = "‘’“”"

results = {
    "blocks": [],          # list of {file, start_line, block_index, content, syntax_ok, curly_hits, drifts}
    "summary": {
        "total": 0,
        "syntax_fail": 0,
        "curly_hits": 0,
        "A_severe": 0,
        "B_warn": 0,
    },
    "by_file": {},
}

def extract_blocks(text):
    """Yield (start_line_1based, code) for each ```python ... ``` block."""
    lines = text.split("\n")
    in_block = False
    block_start = 0
    block_lines = []
    for i, line in enumerate(lines, 1):
        if not in_block:
            if line.strip() == "```python":
                in_block = True
                block_start = i
                block_lines = []
        else:
            if line.strip() == "```":
                code = "\n".join(block_lines)
                yield block_start, code
                in_block = False
                block_lines = []
            else:
                block_lines.append(line)

def check_curly(content, base_offset):
    """Return list of (line, char) tuples for curly quotes."""
    hits = []
    for m in re.finditer(r"[‘’“”]", content):
        abs_line = base_offset + content[:m.start()].count("\n")
        hits.append((abs_line, m.group()))
    return hits

def check_drifts(content, base_offset, surrounding_text=""):
    """Detect API drift patterns in code block; return list of findings."""
    findings = []
    # Determine protocol layer from surroundings
    # Look back up to 30 lines in surrounding_text to find "shell/curl/fetch/API URL" markers
    surrounding = surrounding_text.lower()
    is_http = any(kw in surrounding for kw in ["curl", "shell", "fetch(", "api url", "http://", "https://", "rest api", "post ", "get "])
    for pat, wrong, right in API_DRIFT_PATTERNS:
        for m in pat.finditer(content):
            abs_line = base_offset + content[:m.start()].count("\n")
            if "search_type=" in wrong and is_http:
                # legal in HTTP examples
                continue
            findings.append({
                "line": abs_line,
                "match": m.group(),
                "wrong": wrong,
                "right": right,
                "context": "http" if is_http else "python",
            })
    return findings

# Walk all chapter files
chapter_files = sorted(CHAPTERS.rglob("chapter-*.md"))
for cf in chapter_files:
    rel = cf.relative_to(ROOT)
    text = cf.read_text(encoding="utf-8")
    # find all python blocks with their surrounding context (whole file for context)
    for start_line, code in extract_blocks(text):
        block_index = len(results["blocks"]) + 1
        # syntax
        syntax_ok = True
        syntax_err = None
        try:
            ast.parse(code)
        except SyntaxError as e:
            syntax_ok = False
            syntax_err = str(e)
        # curly
        curly = check_curly(code, start_line)
        # drifts
        drifts = check_drifts(code, start_line, text)
        rec = {
            "file": str(rel),
            "start_line": start_line,
            "block_index": block_index,
            "syntax_ok": syntax_ok,
            "syntax_err": syntax_err,
            "curly": curly,
            "drifts": drifts,
            "code": code,
        }
        results["blocks"].append(rec)
        # accum summary
        results["summary"]["total"] += 1
        if not syntax_ok:
            results["summary"]["syntax_fail"] += 1
        if curly:
            results["summary"]["curly_hits"] += 1
        # A severe: syntax fail or curly quote
        if not syntax_ok or curly:
            results["summary"]["A_severe"] += 1
        if drifts:
            # B warn unless already A
            if syntax_ok and not curly:
                results["summary"]["B_warn"] += len(drifts)
        # by_file
        results["by_file"].setdefault(str(rel), []).append(rec)

# Write results as JSON for further processing
out = ROOT / "code-review" / "scan_results.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(f"Total blocks: {results['summary']['total']}")
print(f"Syntax fail:  {results['summary']['syntax_fail']}")
print(f"Curly hits:   {results['summary']['curly_hits']}")
print(f"A severe:     {results['summary']['A_severe']}")
print(f"B warn:       {results['summary']['B_warn']}")
print(f"JSON written: {out}")