#!/usr/bin/env python3
"""阶段 4 P2 标点统一(修复版):中文字符间的半角标点 → 全角"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"

# 半角 → 全角映射(用 Unicode 码点显式声明)
PUNCT_MAP = {
    ',': '，',   # ，
    ':': '：',   # :
    ';': '；',   # ;
    '?': '？',   # ?
    '!': '！',   # !
}


def normalize_punctuation(text: str) -> tuple[str, int]:
    """中文字符间的半角标点 → 全角(跳过代码块)"""
    count = 0
    lines = text.split('\n')
    in_code = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code:
            new_lines.append(line)
            continue

        new_line = line
        for half, full in PUNCT_MAP.items():
            # 匹配中文字符后跟半角标点
            pattern = re.compile(rf'([一-鿿]){re.escape(half)}')
            matches = pattern.findall(new_line)
            count += len(matches)
            new_line = pattern.sub(rf'\1{full}', new_line)

        new_lines.append(new_line)

    return '\n'.join(new_lines), count


def main():
    print("=== P2 全角标点统一 ===\n")
    total = 0
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        text = ch_file.read_text(encoding='utf-8')
        new_text, count = normalize_punctuation(text)
        if count > 0:
            ch_file.write_text(new_text, encoding='utf-8')
            total += count
            print(f"  {ch_file.name}: {count} 处")
    print(f"\n=== 共 {total} 处标点统一 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
