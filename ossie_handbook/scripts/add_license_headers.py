#!/usr/bin/env python3
"""
add_license_headers.py — batch prepend ASF license header to handbook markdown files.

Usage:
  python3 scripts/add_license_headers.py

Skips files that already start with the ASF license marker.
"""
from pathlib import Path

HEADER = """<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
-->

"""

MARKER = "Licensed to the Apache Software Foundation"

# Files to process (relative to handbook/)
FILES = [
    "README.md",
    "src/index.md",
    "src/00-序章.md",
    "src/01-项目全景.md",
    "src/02-核心规范.md",
    "src/03-表达式语言.md",
    "src/04-编写语义模型.md",
    "src/05-验证工具.md",
    "src/06-转换器架构.md",
    "src/07-converter全谱.md",
    "src/08-python-sdk.md",
    "src/09-go-cli.md",
    "src/10-本体层.md",
    "src/11-治理路线图.md",
    "src/12-附录.md",
]

ROOT = Path(__file__).resolve().parent.parent  # handbook/

added = 0
skipped = 0
failed = []

for relpath in FILES:
    path = ROOT / relpath
    if not path.exists():
        failed.append(f"MISSING: {relpath}")
        continue
    content = path.read_text()
    if content.lstrip().startswith(MARKER):
        skipped += 1
        print(f"  SKIP (already has header): {relpath}")
        continue
    new_content = HEADER + content
    path.write_text(new_content)
    added += 1
    print(f"  ADDED header: {relpath}")

print(f"\nSummary: added={added}, skipped={skipped}, failed={len(failed)}")
if failed:
    for f in failed:
        print(f"  {f}")