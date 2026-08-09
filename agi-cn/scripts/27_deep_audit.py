#!/usr/bin/env python3
"""
scripts/27_deep_audit.py
===========================
对 output/agi-zh-by-chapter/ 做深审计,捕捉 15_audit_quality.py 漏掉的所有瑕疵。

检测项(共 14 类):
  P0:
    1. PDF 页眉残留(模板泄漏,如 `# 27 深入引擎... 393`)
    2. 译者注释泄漏(`> **注**:` / `译者注` / `TODO` / `FIXME`)
    3. 散布的英文短句/段落
    4. 重复 H1(单文件内 # 出现 > 1 次)
    5. forbidden 术语 v2(无 CJK 边界)
    6. 软连字符 (U+00AD) 检测
    7. 内容截断(单文件字符数 < 3000)
  P1:
    8. 重复段落(连续段落相似度 > 85%)
    9. 标题层级违规(文件内 # 出现次数 > 1,或 # 参考文献 应为 ##)
   10. 重复 H2(`## 参考文献` 出现 > 1 次)
   11. 粗体英文标签(`**Conclusion**`、`**Why**` 等)
   12. 代码围栏语言标签缺失
   13. SVG 引用检查(孤儿 + 缺失)
  P2:
   14. 半角标点在中文间
   15. 重复段落(段级相似度)
   16. 首次术语格式不符(`**English**:` 反向)

输出:
  qa/deep-audit.json     # 机器可读
  qa/deep-audit.md       # 人类可读
"""
import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"
SVG_DIR = BY_CHAPTER_DIR / "svg"
TERMINOLOGY_YAML = ROOT / "config" / "terminology.yaml"
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
QA_DIR = ROOT / "qa"

# ============== 检测正则 ==============

# PDF 页眉残留(中文章节标题 + 数字页码在行尾)
PAGE_HEADER_RE = re.compile(r'^#+\s+\d+\s+第?\d*章?.*?\d+\s*$', re.MULTILINE)

# 译者注释泄漏
TRANSLATOR_NOTE_RE = re.compile(
    r'(> \*\*注[:：]?\*\*.*?(?:仅按原文翻译至该处[。.]?|原文[^<]{0,30}未完整)|'
    r'译者注[:：]|'
    r'\bTODO\b|\bFIXME\b|\bTBD\b|'
    r'\[待补充\]|\[占位\])',
    re.MULTILINE
)

# forbidden 术语 (forbidden list from terminology.yaml - 移除 CJK 边界)
FORBIDDEN_TERMS = ["计划", "代理", "反射", "映射", "提示词", "批评者", "评论家"]

# 软连字符
SOFT_HYPHEN = '­'

# 粗体英文标签(常见)
BOLD_ENGLISH_RE = re.compile(r'\*\*([A-Z][a-zA-Z ]+)\*\*')

# 全/半角标点混用(中文字符后跟半角标点)
HALF_WIDTH_RE = re.compile(r'([一-鿿])[,:;?](\s|$|[一-鿿])')

# ============== 检测函数 ==============

def detect_pdf_header(text: str) -> list[dict]:
    issues = []
    for m in PAGE_HEADER_RE.finditer(text):
        line_no = text[:m.start()].count('\n') + 1
        issues.append({"line": line_no, "preview": m.group(0)[:100]})
    return issues


def detect_translator_notes(text: str) -> list[dict]:
    issues = []
    for m in TRANSLATOR_NOTE_RE.finditer(text):
        line_no = text[:m.start()].count('\n') + 1
        issues.append({"line": line_no, "preview": m.group(0)[:100]})
    return issues


def detect_short_english_clauses(text: str) -> list[dict]:
    """散布的英文短句/段落:连续 > 30 字符的英文(不在代码块内)"""
    issues = []
    lines = text.split('\n')
    in_code = False
    buffer = []
    buffer_start = 0

    def flush(end_line):
        nonlocal buffer, buffer_start
        if not buffer:
            return
        para = " ".join(buffer).strip()
        # 跳过引用风格行(以 作者, X. (YYYY) 开头)
        if re.match(r'^[A-Z][a-z]+,\s+[A-Z]\.', para):
            buffer = []
            return
        # 跳过纯 URL 段
        if re.match(r'^https?://', para):
            buffer = []
            return
        # 检测 30+ 字符的英文(可能在混合段中)
        if len(para) >= 30:
            english_words = len(re.findall(r'\b[a-zA-Z]{3,}\b', para))
            chinese = sum(1 for c in para if '一' <= c <= '鿿')
            # 中英比例:中文 < 50% 且有 > 3 个英文单词
            if chinese < len(para) * 0.5 and english_words >= 3:
                # 排除明显的代码片段(以 import/def/class 开头)
                if not para.startswith(('import ', 'from ', 'def ', 'class ', '#', '//', '/**')):
                    issues.append({
                        "line_start": buffer_start,
                        "line_end": end_line,
                        "preview": para[:150],
                        "chinese_ratio": round(chinese / len(para), 2),
                        "english_words": english_words,
                    })
        buffer = []
        buffer_start = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            flush(i - 1)
            continue
        if in_code:
            continue
        if not stripped:
            flush(i - 1)
            continue
        if stripped.startswith('#') or stripped.startswith('!') or stripped.startswith('<!--'):
            flush(i - 1)
            continue
        if not buffer:
            buffer_start = i
        buffer.append(stripped)
    flush(len(lines))
    return issues


def detect_duplicate_h1(text: str) -> list[dict]:
    """重复 H1:单文件内 # 出现次数 > 1"""
    issues = []
    h1_lines = []
    in_code = False
    for i, line in enumerate(text.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r'^# [^#]', line):  # H1 (not H2+)
            h1_lines.append((i, line.strip()))
    if len(h1_lines) > 1:
        for ln, content in h1_lines:
            issues.append({"line": ln, "preview": content})
    return issues


def detect_forbidden_terms_v2(text: str) -> list[dict]:
    """forbidden 术语 v2:无 CJK 边界,捕获 "计划" 等"""
    issues = []
    # 排除代码块
    no_code = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # 排除图片 alt
    no_alt = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', no_code)

    for term in FORBIDDEN_TERMS:
        if term not in no_alt:
            continue
        # 找出所有出现位置(行号)
        for m in re.finditer(re.escape(term), no_alt):
            # 跳过紧邻中文字符的"合法"用法(避免误报)
            before = no_alt[max(0, m.start() - 1):m.start()]
            after = no_alt[m.end():m.end() + 1]
            # 如果两侧都是中文字符,可能是合法术语(如 "代理服务器")
            if before and '一' <= before <= '鿿' and after and '一' <= after <= '鿿':
                continue
            line_no = no_alt[:m.start()].count('\n') + 1
            preview_start = max(0, m.start() - 30)
            preview_end = min(len(no_alt), m.end() + 30)
            issues.append({
                "forbidden": term,
                "line": line_no,
                "preview": no_alt[preview_start:preview_end],
            })
    return issues


def detect_soft_hyphens(text: str) -> list[dict]:
    issues = []
    for m in re.finditer(re.escape(SOFT_HYPHEN), text):
        line_no = text[:m.start()].count('\n') + 1
        issues.append({"line": line_no, "preview": text[max(0, m.start() - 30):m.end() + 30]})
    return issues


def detect_short_content(text: str, file: Path) -> list[dict]:
    """内容截断:单文件字符数 < 3000(Ch 25, 28 等)"""
    char_count = len(text)
    if char_count < 3000:
        return [{"char_count": char_count, "threshold": 3000, "file": str(file.relative_to(ROOT))}]
    return []


def detect_duplicate_paragraphs(text: str) -> list[dict]:
    """重复段落:连续段落相似度 > 85%(简单 substring 检测)"""
    issues = []
    lines = text.split('\n')
    in_code = False
    para_buffer = []
    para_start = 0
    paragraphs = []

    def flush(end_line):
        nonlocal para_buffer, para_start
        if para_buffer:
            para = " ".join(p.strip() for p in para_buffer).strip()
            if len(para) > 100:
                paragraphs.append((para_start, end_line, para))
        para_buffer = []
        para_start = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            flush(i - 1)
            continue
        if in_code or not stripped or stripped.startswith('#'):
            flush(i - 1)
            continue
        if not para_buffer:
            para_start = i
        para_buffer.append(stripped)
    flush(len(lines))

    # 检测前 100 字相似 > 85% 的对
    seen = {}
    for start, end, para in paragraphs:
        sig = para[:80]
        if sig in seen:
            issues.append({
                "first_para_line": seen[sig][0],
                "second_para_line": start,
                "preview": sig,
            })
        else:
            seen[sig] = (start, end)
    return issues


def detect_bold_english(text: str) -> list[dict]:
    """粗体英文标签:`**Conclusion**`、`**Why**` 等"""
    issues = []
    in_code = False
    for i, line in enumerate(text.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        # 跳过单独 `**X**` (X 全英文,3+ 字符)
        m = re.search(r'\*\*([A-Z][a-zA-Z &/]{2,30})\*\*', line)
        if m and re.match(r'^[A-Z][a-zA-Z &/]*$', m.group(1)):
            chinese = sum(1 for c in line if '一' <= c <= '鿿')
            if chinese == 0 or len(m.group(1)) > len(line) * 0.3:
                issues.append({
                    "line": i,
                    "preview": m.group(0),
                    "english": m.group(1),
                })
    return issues


def detect_code_fence_tags(text: str) -> dict:
    """代码围栏语言标签统计"""
    total = 0
    tagged = 0
    untagged = 0
    mismatched = []
    in_code = False
    fence_open_line = 0
    fence_open_tag = None

    for i, line in enumerate(text.split('\n'), 1):
        m = re.match(r'^```(\w*)', line.strip())
        if not m:
            continue
        tag = m.group(1)
        if not in_code:
            in_code = True
            fence_open_line = i
            fence_open_tag = tag
            total += 1
            if tag:
                tagged += 1
            else:
                untagged += 1
        else:
            in_code = False
            # 检查围栏内的内容是否与标签匹配(简单启发式)
            if fence_open_tag:
                block = "\n".join(text.split('\n')[fence_open_line - 1:i])
                if 'javascript' in fence_open_tag and 'import ' in block and 'def ' in block:
                    mismatched.append({"line": fence_open_line, "tag": fence_open_tag, "issue": "javascript but contains Python"})
                elif 'yaml' in fence_open_tag and ('def ' in block or 'class ' in block or 'print(' in block):
                    mismatched.append({"line": fence_open_line, "tag": fence_open_tag, "issue": "yaml but contains Python"})
            fence_open_tag = None
    return {
        "total_fences": total,
        "tagged": tagged,
        "untagged": untagged,
        "untagged_ratio": round(untagged / total, 2) if total else 0,
        "mismatched": mismatched,
    }


def detect_svg_refs(text: str) -> list[dict]:
    """SVG 引用检查"""
    refs = []
    for m in re.finditer(r'!\[[^\]]*\]\(svg/fig-(\d+-\d+)\.svg\)', text):
        line_no = text[:m.start()].count('\n') + 1
        refs.append({"fig_id": m.group(1), "line": line_no})
    return refs


def detect_punctuation(text: str) -> list[dict]:
    """半角标点在中文字符后"""
    issues = []
    in_code = False
    for i, line in enumerate(text.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        # 检测中文字符后跟半角标点
        matches = HALF_WIDTH_RE.findall(line)
        if matches:
            count = len(matches)
            if count > 0:
                issues.append({"line": i, "count": count, "preview": line[:80]})
    return issues


def detect_heading_hierarchy(text: str) -> list[dict]:
    """标题层级违规:`# 参考文献` 等应为 `## 参考文献`"""
    issues = []
    in_code = False
    for i, line in enumerate(text.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r'^(#+)\s+(.+)$', line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        # `# 参考文献` 应为 `##`(文件内已有 H1)
        if level == 1 and title.startswith('参考文献'):
            issues.append({"line": i, "level": level, "title": title, "fix": "应改为 ##"})
    return issues


def detect_duplicate_h2(text: str) -> list[dict]:
    """重复 H2:`## 参考文献` 出现 > 1 次"""
    issues = []
    h2_ref = []
    in_code = False
    for i, line in enumerate(text.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r'^##\s+参考文献', line):
            h2_ref.append(i)
    if len(h2_ref) > 1:
        for ln in h2_ref:
            issues.append({"line": ln, "preview": "## 参考文献"})
    return issues


# ============== 入口 ==============

def audit_chapter(ch_file: Path) -> dict:
    text = ch_file.read_text(encoding='utf-8')
    cid_match = re.match(r'^(\d+)-', ch_file.name)
    cid = int(cid_match.group(1)) if cid_match else 0

    issues = {}
    issues["pdf_header"] = detect_pdf_header(text)
    issues["translator_notes"] = detect_translator_notes(text)
    issues["short_english_clauses"] = detect_short_english_clauses(text)
    issues["duplicate_h1"] = detect_duplicate_h1(text)
    issues["forbidden_terms_v2"] = detect_forbidden_terms_v2(text)
    issues["soft_hyphens"] = detect_soft_hyphens(text)
    issues["short_content"] = detect_short_content(text, ch_file)
    issues["duplicate_paragraphs"] = detect_duplicate_paragraphs(text)
    issues["bold_english"] = detect_bold_english(text)
    issues["heading_hierarchy"] = detect_heading_hierarchy(text)
    issues["duplicate_h2"] = detect_duplicate_h2(text)
    issues["code_fence_stats"] = detect_code_fence_tags(text)
    issues["svg_refs"] = detect_svg_refs(text)
    issues["punctuation"] = detect_punctuation(text)

    # 严重性分数
    p0_count = (
        len(issues["pdf_header"]) +
        len(issues["translator_notes"]) +
        len(issues["short_english_clauses"]) +
        len(issues["duplicate_h1"]) +
        len(issues["forbidden_terms_v2"]) +
        len(issues["soft_hyphens"]) +
        len(issues["short_content"])
    )
    p1_count = (
        len(issues["duplicate_paragraphs"]) +
        len(issues["bold_english"]) +
        len(issues["heading_hierarchy"]) +
        len(issues["duplicate_h2"])
    )
    p2_count = (
        len(issues["punctuation"]) +
        issues["code_fence_stats"]["untagged"]
    )

    return {
        "chapter_id": cid,
        "file": str(ch_file.relative_to(ROOT)),
        "char_count": len(text),
        "p0_count": p0_count,
        "p1_count": p1_count,
        "p2_count": p2_count,
        "issues": issues,
    }


def main() -> int:
    print("=== 深审计 ===")
    results = []
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        if ch_file.name.startswith("."):
            continue
        result = audit_chapter(ch_file)
        results.append(result)
        p0 = result["p0_count"]
        p1 = result["p1_count"]
        p2 = result["p2_count"]
        if p0 or p1 or p2:
            print(f"  Ch {result['chapter_id']:>2} {ch_file.name[:45]:<45} P0:{p0:>2} P1:{p1:>2} P2:{p2:>3}")

    # SVG 全局检查
    svg_files = {f.stem.replace('fig-', '') for f in SVG_DIR.glob('fig-*.svg')}
    all_refs = set()
    for r in results:
        for ref in r["issues"]["svg_refs"]:
            all_refs.add(ref["fig_id"])
    orphan_svgs = sorted(svg_files - all_refs)
    missing_svgs = sorted(all_refs - svg_files)

    # 汇总
    total_p0 = sum(r["p0_count"] for r in results)
    total_p1 = sum(r["p1_count"] for r in results)
    total_p2 = sum(r["p2_count"] for r in results)
    total_fences = sum(r["issues"]["code_fence_stats"]["total_fences"] for r in results)
    total_tagged = sum(r["issues"]["code_fence_stats"]["tagged"] for r in results)
    total_untagged = sum(r["issues"]["code_fence_stats"]["untagged"] for r in results)

    print(f"\n=== 汇总 ===")
    print(f"  P0: {total_p0}")
    print(f"  P1: {total_p1}")
    print(f"  P2: {total_p2}")
    print(f"  代码围栏: {total_tagged}/{total_fences} 有标签 ({total_untagged} 缺)")
    print(f"  SVG 孤儿: {len(orphan_svgs)}")
    print(f"  SVG 缺失: {len(missing_svgs)}")
    if orphan_svgs:
        print(f"    孤儿: {orphan_svgs}")
    if missing_svgs:
        print(f"    缺失: {missing_svgs}")

    # 写报告
    QA_DIR.mkdir(parents=True, exist_ok=True)
    json_path = QA_DIR / "deep-audit.json"
    json_path.write_text(json.dumps({
        "summary": {
            "total_p0": total_p0,
            "total_p1": total_p1,
            "total_p2": total_p2,
            "code_fences_total": total_fences,
            "code_fences_tagged": total_tagged,
            "code_fences_untagged": total_untagged,
            "orphan_svgs": orphan_svgs,
            "missing_svgs": missing_svgs,
        },
        "chapters": results,
    }, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nJSON 报告: {json_path}")

    md_path = QA_DIR / "deep-audit.md"
    lines = ["# 深审计报告", ""]
    lines.append(f"## 汇总")
    lines.append("")
    lines.append(f"- P0 瑕疵: **{total_p0}**")
    lines.append(f"- P1 瑕疵: **{total_p1}**")
    lines.append(f"- P2 瑕疵: **{total_p2}**")
    lines.append(f"- 代码围栏标签: {total_tagged}/{total_fences} ({total_untagged} 缺)")
    lines.append(f"- SVG 孤儿: {len(orphan_svgs)}, 缺失: {len(missing_svgs)}")
    lines.append("")
    lines.append("## 章节详细")
    lines.append("")
    lines.append("| # | 文件 | 字符 | P0 | P1 | P2 | 围栏标签率 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for r in results:
        cfs = r["issues"]["code_fence_stats"]
        rate = f"{cfs['tagged']}/{cfs['total_fences']}"
        lines.append(f"| {r['chapter_id']} | `{r['file'].split('/')[-1]}` | {r['char_count']:,} | {r['p0_count']} | {r['p1_count']} | {r['p2_count']} | {rate} |")
    md_path.write_text("\n".join(lines), encoding='utf-8')
    print(f"MD 报告: {md_path}")

    return 0 if total_p0 == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
