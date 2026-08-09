#!/usr/bin/env python3
"""阶段 1 通用正则修复(无 LLM)。

修复:
  1. "并行化化化化" / "并行化化化" / "并行化化" → "并行化"(链式)
  2. 行首 en-dash "– " → "- "(只针对 04/22/27 三章)
  3. 陈旧 <!-- TRANSLATION_NOTE: ... --> 注释清理
"""
import re
import pathlib
import sys

CH_DIR = pathlib.Path('output/agi-zh-by-chapter')
EN_DASH_FILES = [
    '04-reflection.md',
    '22-advanced-prompting-techniques.md',
    '27-under-the-hood-reasoning-engines.md',
]


def fix_repetitions(text: str) -> tuple[str, int]:
    """链式替换并行化化*,由长到短。"""
    count = 0
    new = text
    for pattern in (r'并行化化化化', r'并行化化化', r'并行化化'):
        before = new
        new = re.sub(pattern, '并行化', new)
        count += len(re.findall(pattern, before))
    return new, count


def fix_translation_notes(text: str) -> tuple[str, int]:
    """清理 <!-- TRANSLATION_NOTE: ... --> 注释。"""
    pattern = r'<!--\s*TRANSLATION_NOTE:[^>]*-->'
    matches = re.findall(pattern, text)
    new = re.sub(pattern, '', text)
    # 移除紧跟着的空行
    new = re.sub(r'\n\n+', '\n\n', new)
    return new, len(matches)


def fix_en_dash(text: str) -> tuple[str, int]:
    """行首 en-dash 转为 hyphen。"""
    pattern = r'^– '
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    new = re.sub(pattern, '- ', text, flags=re.MULTILINE)
    return new, len(matches)


def main() -> int:
    if not CH_DIR.is_dir():
        print(f"错误:找不到目录 {CH_DIR}", file=sys.stderr)
        return 1

    rep_total = note_total = en_dash_total = 0
    files_changed = 0

    # 1. 全部 .md 处理重复 + TRANSLATION_NOTE
    for md in sorted(CH_DIR.glob('*.md')):
        text = md.read_text()
        new, rep_count = fix_repetitions(text)
        new, note_count = fix_translation_notes(new)
        if new != text:
            md.write_text(new)
            files_changed += 1
            rep_total += rep_count
            note_total += note_count

    # 2. en-dash 只针对 3 章
    for fn in EN_DASH_FILES:
        p = CH_DIR / fn
        if not p.exists():
            print(f"警告:跳过不存在文件 {fn}")
            continue
        text = p.read_text()
        new, count = fix_en_dash(text)
        if new != text:
            p.write_text(new)
            files_changed += 1
            en_dash_total += count

    print(f"=== 阶段 1 完成 ===")
    print(f"修改文件: {files_changed}")
    print(f"消除 '并行化化*' 重复: {rep_total}")
    print(f"清理 TRANSLATION_NOTE 注释: {note_total}")
    print(f"转换 en-dash 项目符号: {en_dash_total}")
    return 0


if __name__ == '__main__':
    sys.exit(main())