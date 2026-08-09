#!/usr/bin/env python3
"""阶段 4: 清理残存的旧英文参考文献条目(来自之前修复的残留)"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


def cleanup_old_english_refs(text: str) -> tuple[str, int]:
    """清理不在 ## 参考文献 下的旧英文参考文献条目"""
    count = 0
    lines = text.split('\n')
    new_lines = []
    in_refs = False
    in_code = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code:
            new_lines.append(line)
            continue

        # 检测 ## 参考文献 / ## Bibliography
        if re.match(r'^##\s+(?:参考文献|Bibliography)\s*$', stripped):
            in_refs = True
            new_lines.append(line)
            continue

        # 在 ## 参考文献 之外的英文参考文献条目
        if not in_refs:
            # 匹配 "O'Neill, V. (2022). Improving..." 这种
            if re.match(r'^[A-Z][a-z\']+,\s+[A-Z]\.\s+\(\d{4}\)\.', stripped):
                count += 1
                continue  # 删除
            # 匹配 "Shi, Y., Pei, H., ..." 这种
            if re.match(r'^[A-Z][a-z\']+,\s+[A-Z]\.[^.]*,\s*[A-Z]\.\s+[A-Z][a-z\']+\s*&\s*[A-Z]\.\s+[A-Z][a-z\']+\.\s+\(\d{4}\)\.', stripped):
                count += 1
                continue
            # 匹配 "Inference Scaling Laws: An Empirical Analysis..." 这种裸论文标题
            if re.match(r'^Inference Scaling Laws', stripped):
                count += 1
                continue
            # 匹配 "arXiv preprint" 开头
            if stripped.startswith('*arXiv preprint'):
                count += 1
                continue
            # 空行(连续多个)
            if not stripped:
                # 只保留一个空行(后面有内容时)
                if new_lines and not new_lines[-1].strip():
                    continue

        # 离开参考文献节(下一个 ## 标题)
        if in_refs and re.match(r'^##\s+', stripped):
            in_refs = False

        new_lines.append(line)

    return '\n'.join(new_lines), count


def main():
    print("=== 清理残存旧英文参考文献 ===\n")
    total = 0
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        text = ch_file.read_text(encoding='utf-8')
        new_text, count = cleanup_old_english_refs(text)
        if count > 0:
            ch_file.write_text(new_text, encoding='utf-8')
            total += count
            print(f"  {ch_file.name}: {count} 行清理")
    print(f"\n=== 共清理 {total} 行 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
