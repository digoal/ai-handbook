#!/usr/bin/env python3
"""阶段 3+4 P1+P2 综合修复:
- P1: 重复段落删除、代码围栏语言标签、段落级修复
- P2: 全角标点统一(中文字符间的半角标点 → 全角)
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


# ============== P2 全角标点统一 ==============

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
        # 在中文字符之间(中文字符后)出现的半角标点
        # ,→  ,
        # .→ 。
        # :→ :
        # ;→ ;
        # ?→ ?
        # !→ !

        # 中文字符后的半角标点
        # 我们要确保不破坏 URL/邮箱/代码
        # 简单启发式:只在 [中文字符][半角标点] 处替换
        for half, full in [(',', ','), (':', ':'), (';', ';'), ('?', '?'), ('!', '!')]:
            new_line2 = re.sub(rf'([一-鿿]){re.escape(half)}', rf'\1{full}', new_line)
            if new_line2 != new_line:
                count += new_line.count(f'[一-鿿]{half}')
                new_line = new_line2

        # 中文字符前的半角标点(实际很少见)
        # . 后跟中文字符 → 。
        new_line2 = re.sub(r'([一-鿿])\.', r'\1。', new_line)
        # 但这会破坏 "v1.0" 等,跳过

        new_lines.append(new_line)

    return '\n'.join(new_lines), count


# ============== P1 段落重复删除 ==============

def remove_duplicate_paragraphs(text: str) -> tuple[str, list[dict]]:
    """删除完全重复的段落"""
    lines = text.split('\n')
    in_code = False
    paragraphs = []  # list of (start, end, text, is_code)
    para_buffer = []
    para_start = 0
    is_in_code_block = False

    def flush(end_line):
        nonlocal para_buffer, para_start, is_in_code_block
        if para_buffer:
            para = '\n'.join(para_buffer)
            paragraphs.append((para_start, end_line, para, is_in_code_block))
        para_buffer = []
        para_start = 0
        is_in_code_block = False

    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if not is_in_code_block:
                flush(i - 1)
                is_in_code_block = True
            else:
                flush(i)
                is_in_code_block = False
            continue
        if not para_buffer:
            para_start = i
        para_buffer.append(line)
    flush(len(lines))

    # 检测完全重复(非代码块)
    seen = {}
    dup_ranges = []  # (start, end, original_start)
    for start, end, para, in_code in paragraphs:
        if in_code:
            continue
        stripped = para.strip()
        if len(stripped) < 50:
            continue
        sig = stripped[:200]  # 用前 200 字做签名
        if sig in seen:
            # 重复了
            orig_start = seen[sig]
            dup_ranges.append((start, end, orig_start))
        else:
            seen[sig] = start

    # 删除重复(从后往前)
    fixes = []
    if dup_ranges:
        # 构建要删除的行集合
        lines_to_remove = set()
        for start, end, orig_start in dup_ranges:
            for i in range(start, end + 1):
                lines_to_remove.add(i - 1)  # 0-indexed
            fixes.append({"original_line": orig_start, "duplicate_range": f"{start}-{end}"})

        new_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
        # 清理多余空行
        new_text = '\n'.join(new_lines)
        new_text = re.sub(r'\n{3,}', '\n\n', new_text)
        return new_text, fixes

    return text, []


# ============== P1 代码围栏语言标签 ==============

def fix_code_fence_tags(text: str) -> tuple[str, int]:
    """为无标签的代码块添加 python 标签(基于内容启发式)"""
    count = 0
    lines = text.split('\n')
    new_lines = []
    in_code = False
    block_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```') and not in_code:
            # 开围栏
            if re.match(r'^```(\w*)', stripped):
                tag = re.match(r'^```(\w*)', stripped).group(1)
                if not tag:
                    # 无标签 - 启发式判断
                    # 看接下来 10 行内容
                    block_content = '\n'.join(lines[i+1:i+11])
                    if 'def ' in block_content or 'class ' in block_content or 'import ' in block_content or 'print(' in block_content:
                        new_tag = 'python'
                    elif '{' in block_content and '}' in block_content and ':' in block_content and not 'def ' in block_content:
                        new_tag = 'json'
                    elif 'pip install' in block_content:
                        new_tag = 'bash'
                    else:
                        new_tag = 'text'
                    new_lines.append(f'```{new_tag}')
                    count += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            in_code = True
            block_start = i
        elif stripped.startswith('```') and in_code:
            new_lines.append(line)
            in_code = False
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), count


# ============== P1 Ch 22 标题层级 ==============

def fix_ch22_heading_hierarchy(text: str) -> tuple[str, list[dict]]:
    """Ch 22: L91/95/102/121 `# 构造提示` → `## 构造提示` 等"""
    fixes = []
    new_lines = []
    for line in text.split('\n'):
        # 跳过代码块
        if line.strip().startswith('```'):
            new_lines.append(line)
            continue
        m = re.match(r'^(#)\s+([^#].*?)$', line)
        if m:
            content = m.group(2)
            # 不改 H1 (章节标题)
            if re.match(r'^第 \d+ 章', content):
                new_lines.append(line)
                continue
            # 改 `# XXX` → `## XXX`(如果不是 `# 第 X 章`)
            new_lines.append(f'## {content}')
            fixes.append({"from": line, "to": f"## {content}"})
        else:
            new_lines.append(line)
    return '\n'.join(new_lines), fixes


# ============== Ch 25 tone consistency ==============

def fix_ch25_tone(text: str) -> tuple[str, int]:
    """Ch 25: `您的` → `你的`(去掉敬语)"""
    count = 0
    for old, new in [('您的', '你的'), ('您可以', '你可以'), ('请', '请')]:
        if old in text:
            count += text.count(old)
            text = text.replace(old, new)
    return text, count


# ============== 主流程 ==============

def main():
    print("=== 阶段 3+4 P1+P2 综合修复 ===\n")
    stats = {
        'punctuation': 0,
        'duplicate_paragraphs': 0,
        'code_fence_tags': 0,
        'ch22_headings': 0,
        'ch25_tone': 0,
    }

    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        text = ch_file.read_text(encoding='utf-8')
        orig = text

        # 1. P2: 全角标点
        text, c = normalize_punctuation(text)
        stats['punctuation'] += c

        # 2. P1: 段落重复
        text, fixes = remove_duplicate_paragraphs(text)
        if fixes:
            stats['duplicate_paragraphs'] += len(fixes)

        # 3. P1: 代码围栏标签
        text, c = fix_code_fence_tags(text)
        stats['code_fence_tags'] += c

        # 4. P1: Ch 22 标题层级
        if ch_file.name == "22-advanced-prompting-techniques.md":
            text, fixes = fix_ch22_heading_hierarchy(text)
            stats['ch22_headings'] += len(fixes)

        # 5. P1: Ch 25 语气统一
        if ch_file.name == "25-building-an-agent-with-agentspace.md":
            text, c = fix_ch25_tone(text)
            stats['ch25_tone'] += c

        if text != orig:
            ch_file.write_text(text, encoding='utf-8')
            print(f"  ✓ {ch_file.name}")

    print(f"\n=== 修复汇总 ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
