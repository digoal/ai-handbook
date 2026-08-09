#!/usr/bin/env python3
"""阶段 2 P0 残留瑕疵修复:
- 重复 H1 (在代码块外的)
- `# 参考文献` → `## 参考文献` 标题层级
- 粗体英文标签翻译 (**Conclusion**, **Why**, **What**, **Visual Summary** 等)
- 散布英文短句翻译 (LLM 辅助)
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


# ============== 通用修复函数 ==============

def fix_duplicate_h1_outside_code(text: str) -> tuple[str, list[dict]]:
    """删除代码块外的重复 H1(保留第一个)"""
    fixes = []
    lines = text.split('\n')
    in_code = False
    h1_count = 0
    keep_indices = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            keep_indices.append(i)
            continue
        if in_code:
            keep_indices.append(i)
            continue
        if re.match(r'^# [^#]', line):
            h1_count += 1
            if h1_count == 1:
                keep_indices.append(i)  # 保留第一个
            else:
                # 删除多余的 H1
                fixes.append({"line": i + 1, "content": stripped})
        else:
            keep_indices.append(i)

    new_lines = [lines[i] for i in keep_indices]
    # 清理空行
    new_text = '\n'.join(new_lines)
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)
    return new_text, fixes


def fix_heading_h1_references(text: str) -> tuple[str, int]:
    """`# 参考文献` → `## 参考文献`(在代码块外)"""
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
        if not in_code and re.match(r'^# 参考文献\s*$', line):
            new_lines.append('## 参考文献')
            count += 1
        else:
            new_lines.append(line)
    return '\n'.join(new_lines), count


def fix_bold_english_labels(text: str) -> tuple[str, list[dict]]:
    """翻译 `**EnglishLabel**` 类的粗体英文标签(常见 5 个)"""
    fixes = []
    label_map = {
        '**Conclusion**': '**结论**',
        '**Visual Summary**': '**可视化总结**',
        '**Rule of Thumb**': '**经验法则**',
        '**Why**': '**为什么**',
        '**What**': '**是什么**',
        '**How**': '**如何**',
        '**When**': '**何时**',
        '**Where**': '**何地**',
        '**At a Glance**': '**速览**',
        '**Key Takeaways**': '**关键要点**',
        '**Note**': '**注**',
        '**Tip**': '**提示**',
        '**Warning**': '**警告**',
        '**Example**': '**示例**',
    }
    new_text = text
    for old, new in label_map.items():
        if old in new_text:
            fixes.append({"old": old, "new": new, "count": new_text.count(old)})
            new_text = new_text.replace(old, new)
    return new_text, fixes


def fix_specific_english_clauses(text: str, file_name: str) -> tuple[str, list[dict]]:
    """修复特定英文短句残留"""
    fixes = []
    replacements = {
        # Ch 4 line 33
        'Repeat until the post meets quality\nstandards.': '重复上述过程,直至文章达到质量标准。',
        'Repeat until the post meets quality standards.': '重复上述过程,直至文章达到质量标准。',
        # Ch 12 line 109
        'Essential points to remember:': '需要铭记的关键要点:',
        # Ch 13 line 5
        'The 人在回路': '人在回路',
        # Ch 17 line 178
        "An example is the use of external tools within Google's ADK for generating code.":
            "一个示例是在 Google ADK 中使用外部工具来生成代码。",
        # Ch 21 line 215-220 (完整英文段)
        'Reviewer Agents Reviewer agents perform critical evaluations of research outputs from the PostDoc Agent, assessing the quality, validity, and scientific rigor of papers and experimental results. This evaluation phase emulates the peer-review process in academic settings to ensure a high standard of research output before finalization.':
            '评审智能体(Reviewer Agents)对 PostDoc 智能体的研究输出进行关键评估,评估论文与实验结果的质量、有效性与科学严谨性。这一评估阶段模拟了学术环境中的同行评审流程,以确保最终发布前研究输出达到高标准。',
        # Ch 4 line 128 (Python 语法错误)
        'if i = = 0:': 'if i == 0:',
        # Ch 26 line 13-14
        '并能够执行复杂的多步骤任务,从而自动化开发生命周期中的大量环节\n## Gemini CLI':
            '并能够执行复杂的多步骤任务,从而自动化开发生命周期中的大量环节。\n\n## Gemini CLI',
        # Ch 28 (已经在阶段 1 修复)
        # Ch 29 (translator note 已在阶段 1 修复)
        # Ch 17 line 214 'Fig. 17.3 推理与行动' - 图标题 prefix 修复
        'Fig. 17.3 推理与行动(Reasoning and Act)': '图 17.3 推理与行动(Reasoning and Act)',
        # Ch 17 line 21-26 重复标题块(将在下一步处理)
        # Ch 23 duplicate H1
        '# AI 智能体交互:从图形用户界面到真实世界环境': '# AI 智能体交互:从 GUI 到真实世界环境',
    }

    new_text = text
    for old, new in replacements.items():
        if old in new_text:
            fixes.append({"old": old[:50], "new": new[:50], "count": new_text.count(old)})
            new_text = new_text.replace(old, new)

    return new_text, fixes


def fix_ch17_duplicate_h1_block(text: str) -> tuple[str, str]:
    """修复 Ch 17 line 21-26 重复标题块"""
    # 找到 `# 推理技术(Reasoning Techniques)` 后到 `## 引言` 整段删除
    pattern = re.compile(
        r'^# 推理技术\(Reasoning Techniques\)\s*\n'
        r'(?:.*\n)*?'
        r'## 引言\s*\n'
        r'(?:.*\n)*?'
        r'\.\.\.\s*\n',
        re.MULTILINE
    )
    new_text = pattern.sub('', text)
    return new_text, 'fixed'


def fix_ch2_duplicate_bibliography(text: str) -> tuple[str, str]:
    """修复 Ch 2 line 329-336 重复参考文献节"""
    lines = text.split('\n')
    # 找到第二个 ## 参考文献开始,删除从那里到文末的整个块
    found_indices = []
    for i, line in enumerate(lines):
        if re.match(r'^##\s+参考文献\s*$', line.strip()):
            found_indices.append(i)
    if len(found_indices) >= 2:
        # 删除从第二个到文末的所有 ## 参考文献 内容
        # 实际策略:删除第二个 ## 参考文献 直到文件末尾
        del lines[found_indices[1]:]
        # 清理末尾空行
        while lines and not lines[-1].strip():
            lines.pop()
        return '\n'.join(lines) + '\n', f'fixed (removed {len(found_indices) - 1} duplicate)'
    return text, 'no duplicate'


# ============== 主流程 ==============

def main():
    print("=== 阶段 2 P0 残留瑕疵修复 ===\n")
    all_fixes = {}

    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        text = ch_file.read_text(encoding='utf-8')
        orig = text
        chapter_fixes = {}

        # 1. 删除代码块外的重复 H1
        new_text, fixes = fix_duplicate_h1_outside_code(text)
        if fixes:
            chapter_fixes['duplicate_h1'] = fixes
            text = new_text

        # 2. `# 参考文献` → `## 参考文献`
        new_text, count = fix_heading_h1_references(text)
        if count:
            chapter_fixes['heading_h1_refs'] = count
            text = new_text

        # 3. 粗体英文标签
        new_text, fixes = fix_bold_english_labels(text)
        if fixes:
            chapter_fixes['bold_english'] = fixes
            text = new_text

        # 4. 特定英文短句
        new_text, fixes = fix_specific_english_clauses(text, ch_file.name)
        if fixes:
            chapter_fixes['english_clauses'] = fixes
            text = new_text

        # 5. Ch 17 重复标题块
        if ch_file.name == "17-reasoning-techniques.md":
            new_text, status = fix_ch17_duplicate_h1_block(text)
            if status == 'fixed':
                chapter_fixes['ch17_duplicate_block'] = 'fixed'
                text = new_text

        # 6. Ch 2 重复参考文献节
        if ch_file.name == "02-routing.md":
            new_text, status = fix_ch2_duplicate_bibliography(text)
            if 'fixed' in status:
                chapter_fixes['ch2_duplicate_refs'] = status
                text = new_text

        # 写回
        if text != orig:
            ch_file.write_text(text, encoding='utf-8')
            all_fixes[ch_file.name] = chapter_fixes
            fix_count = sum(
                len(v) if isinstance(v, list) else (1 if isinstance(v, str) else v)
                for v in chapter_fixes.values()
            )
            print(f"  {ch_file.name}: {fix_count} 处修复")
            for k, v in chapter_fixes.items():
                if isinstance(v, list):
                    print(f"    - {k}: {len(v)} 项")
                else:
                    print(f"    - {k}: {v}")

    print(f"\n=== 共修复 {len(all_fixes)} 章 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
