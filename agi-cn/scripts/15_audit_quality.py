#!/usr/bin/env python3
"""
scripts/15_audit_quality.py
===========================
对 output/agi-zh-by-chapter/ 下所有 29 章节做全面质量审计。

检测项:
  P0 - 未译英文段落(连续 >100 字符英文,中文字符占比 < 30%)
  P0 - 未译英文标题 (^#+ 标题全部英文)
  P0 - 术语违规(terminology.yaml forbidden 词)
  P1 - 图引用断裂(路径不存在或为 #)
  P1 - 图引用路径不规范(7 种风格混乱)
  P2 - At a Glance 小节未翻译
  P2 - 章节字符数偏低(疑似漏译)

输出:
  qa/quality-audit.json     # 机器可读
  qa/quality-audit.md       # 人类可读摘要

不修改任何文件。
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"
TERMINOLOGY_YAML = ROOT / "config" / "terminology.yaml"
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
QA_DIR = ROOT / "qa"


# 保留英文清单(从 terminology.yaml 读取)
PRESERVE_ENGLISH = set()
FORBIDDEN_TERMS = []  # list of (source, forbidden_term, preferred)


def _load_preserve_english():
    """直接加载术语表中的保留英文列表(避免 main() 未调用时为空)"""
    try:
        data = yaml.safe_load(TERMINOLOGY_YAML.read_text(encoding="utf-8"))
        # preserve_english 是 core_terms 列表中的最后一个字典项
        for term in data.get("core_terms", []) or []:
            if isinstance(term, dict) and "preserve_english" in term:
                for p in term["preserve_english"]:
                    if isinstance(p, str):
                        PRESERVE_ENGLISH.add(p)
    except Exception:
        pass


_load_preserve_english()


def load_terminology() -> dict:
    """加载术语表"""
    data = yaml.safe_load(TERMINOLOGY_YAML.read_text(encoding="utf-8"))
    preserve = set()
    forbidden = []  # (forbidden, preferred, source)
    for term in data.get("core_terms", []):
        src = term.get("source", "")
        pref = term.get("preferred", "")
        for fb in term.get("forbidden", []):
            forbidden.append({"forbidden": fb, "preferred": pref, "source": src})
    for p in data.get("preserve_english", []) or []:
        if isinstance(p, str):
            preserve.add(p)
    return {"preserve": preserve, "forbidden": forbidden}


def load_chapters_meta() -> dict:
    """加载章节元数据"""
    data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))
    return {c["id"]: c for c in data["chapters"]}


def is_chinese_char(c: str) -> bool:
    """是否中文字符(CJK 基本区)"""
    return "一" <= c <= "鿿"


def find_untranslated_paragraphs(text: str) -> list[dict]:
    """找出未译的英文段落
    启发式:连续段落(不在代码块、不是列表项)中:
      - 中文字符数 < 总字符数的 30%
      - 段落长度 > 100 字符
      - 含至少 5 个英文单词
    """
    issues = []
    lines = text.split("\n")
    in_code_block = False
    para_buffer = []
    para_start_line = 0

    def flush_buffer(end_line):
        nonlocal para_buffer, para_start_line
        if not para_buffer:
            return
        para = " ".join(para_buffer).strip()
        if len(para) > 100:
            chinese = sum(1 for c in para if is_chinese_char(c))
            total = len(para)
            ratio = chinese / total if total else 0
            english_words = len(re.findall(r"\b[a-zA-Z]{3,}\b", para))
            if ratio < 0.30 and english_words >= 5:
                issues.append({
                    "line_start": para_start_line,
                    "line_end": end_line,
                    "preview": para[:150],
                    "chinese_ratio": round(ratio, 2),
                    "english_words": english_words,
                    "length": total,
                })
        para_buffer = []
        para_start_line = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if para_buffer:
                flush_buffer(i - 1)
            continue
        if in_code_block:
            continue
        if not stripped:
            if para_buffer:
                flush_buffer(i - 1)
            continue
        if stripped.startswith("#") or stripped.startswith("!"):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        if stripped.startswith(("-", "*", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "0.")):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        # 跳过 HTML 注释(含 TRANSLATION_NOTE)
        if stripped.startswith("<!--") or stripped.startswith("-->"):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        # 跳过纯 URL 段落
        if re.match(r"^https?://\S+$", stripped):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        # 跳过参考文献风格段落("Author, A. (YYYY). Title..." 或 "[N] Author...")
        if re.match(r"^\[?\d+\]?\s*[A-Z][a-z]+,\s*[A-Z]\.", stripped):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        # 跳过含 URL 的段落(参考文献、文档链接等)
        if re.search(r"https?://\S+", stripped):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        # 跳过 Markdown 表格行
        if stripped.startswith("|") or re.match(r"^\|?[\s:|-]+\|?$", stripped):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        # 跳过包含典型引用关键词的段落(Bibliography/References/参考文献 后跟 URL 列表)
        if re.match(r"^(Bibliography|References|参考文献|延伸阅读|进一步阅读)", stripped):
            if para_buffer:
                flush_buffer(i - 1)
            continue
        if not para_buffer:
            para_start_line = i
        para_buffer.append(stripped)

    if para_buffer:
        flush_buffer(len(lines))
    return issues


def find_untranslated_headings(text: str) -> list[dict]:
    """找出未译的英文标题(以英文开头,无中文字符)。跳过代码块内容与保留英文术语。"""
    issues = []
    in_code_block = False
    for i, line in enumerate(text.split("\n"), 1):
        stripped = line.strip()
        # 跟踪代码块边界
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        # 跳过代码块内的内容(避免误判 Python 注释/字符串)
        if in_code_block:
            continue
        m = re.match(r"^(#+)\s+(.+)$", line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        if not title:
            continue
        # 跳过单 # H1 标题(只检查 H2 及以上)
        # 单 # 在本书中应是章节级标题(已翻译过),且常被原 PDF 转写时残留为 Python 注释
        if level < 2:
            continue
        chinese = sum(1 for c in title if is_chinese_char(c))
        if chinese == 0 and len(title) > 3:
            # 检查是否在保留英文术语列表中(产品/框架/工具名)
            preserve_set = globals().get("PRESERVE_ENGLISH", set())
            is_preserve = False
            if preserve_set:
                # 检查标题中是否包含任一保留英文术语
                for term in preserve_set:
                    if not term:
                        continue
                    # 1. 完整子串匹配
                    if term in title:
                        is_preserve = True
                        break
                    # 2. 标题首个非标点 token 与 term 前缀匹配(用于 "Google ADK" / "Google Co-scientist")
                    # 取标题的第一个空格前的词
                    first_token = title.split()[0] if title.split() else ""
                    if first_token and term.startswith(first_token) and len(first_token) >= 3:
                        is_preserve = True
                        break
            if not is_preserve:
                issues.append({
                    "line": i,
                    "level": level,
                    "title": title,
                })
    return issues


def find_forbidden_terms(text: str, terminology: dict) -> list[dict]:
    """找出术语违规"""
    issues = []
    # 排除代码块内容
    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # 排除 Markdown 图片 alt 文本(避免误判图题里的英文术语名)
    no_alt = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", no_code)

    for entry in terminology["forbidden"]:
        fb = entry["forbidden"]
        # word boundary 检测:用 negative lookbehind/lookahead 排除紧邻的中文字符
        # 避免 "并行" 误匹配 "并行化", "代理" 误匹配 "代理服务器" 等
        pattern = re.compile(
            r"(?<![一-鿿])" + re.escape(fb) + r"(?![一-鿿])"
        )
        matches = list(pattern.finditer(no_alt))
        if matches:
            for m in matches[:3]:  # 每个 forbidden 词最多报 3 个
                line_no = no_alt[:m.start()].count("\n") + 1
                issues.append({
                    "forbidden": fb,
                    "preferred": entry["preferred"],
                    "source": entry["source"],
                    "line": line_no,
                    "preview": no_alt[max(0, m.start()-30):m.end()+30],
                })
    return issues


def find_image_refs(text: str, by_chapter_dir: Path) -> list[dict]:
    """找出图片引用问题"""
    issues = []
    refs = []
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    for i, line in enumerate(text.split("\n"), 1):
        for m in pattern.finditer(line):
            alt = m.group(1)
            path = m.group(2)
            refs.append({"line": i, "alt": alt, "path": path})

    for ref in refs:
        path = ref["path"]
        # 跳过 http(s) URL
        if path.startswith(("http://", "https://")):
            continue
        # 跳过锚点(虽然 # 是断链,但仍是空 ref)
        if path.startswith("#") or not path.strip():
            issues.append({**ref, "issue": "broken_anchor", "severity": "high"})
            continue
        # 检查文件是否存在(相对当前章节文件)
        full_path = by_chapter_dir / path
        if not full_path.exists():
            # 也尝试相对 normalized/figures/
            alt_path = ROOT / "normalized" / "figures" / Path(path).name
            if not alt_path.exists():
                issues.append({**ref, "issue": "missing_file", "severity": "high"})
            else:
                issues.append({**ref, "issue": "nonstandard_path", "severity": "medium"})
                continue
        # 路径不规范但存在
        if "svg" not in path.lower() and path.endswith((".jpg", ".png", ".ppm")):
            issues.append({**ref, "issue": "legacy_path", "severity": "low"})
    return issues, refs


def find_at_a_glance_issues(text: str) -> list[dict]:
    """找出 At a Glance 小节是否有未译内容"""
    issues = []
    lines = text.split("\n")
    in_glance = False
    glance_start = 0
    glance_lines = []

    for i, line in enumerate(lines, 1):
        if re.search(r"^#+\s+.*At a Glance", line) or re.match(r"^At a Glance", line):
            in_glance = True
            glance_start = i
            glance_lines = []
            continue
        if in_glance:
            # 下一个小标题出现则结束
            if re.match(r"^#+\s+", line):
                break
            if line.strip():
                glance_lines.append(line)

    if in_glance and glance_lines:
        content = "\n".join(glance_lines)
        chinese = sum(1 for c in content if is_chinese_char(c))
        total = len(content)
        ratio = chinese / total if total else 0
        if ratio < 0.50:
            issues.append({
                "line_start": glance_start,
                "preview": content[:200],
                "chinese_ratio": round(ratio, 2),
            })
    return issues


def audit_chapter(ch_file: Path, chapter_meta: dict, terminology: dict) -> dict:
    """审计单个章节"""
    text = ch_file.read_text(encoding="utf-8")
    cid = chapter_meta["id"]
    slug = chapter_meta["slug"]
    zh_title = chapter_meta["zh_title"]

    untranslated_paras = find_untranslated_paragraphs(text)
    untranslated_headings = find_untranslated_headings(text)
    forbidden_terms = find_forbidden_terms(text, terminology)
    image_issues, image_refs = find_image_refs(text, BY_CHAPTER_DIR)
    at_glance_issues = find_at_a_glance_issues(text)

    # 字符数
    char_count = len(text)
    chinese_total = sum(1 for c in text if is_chinese_char(c))

    severity_score = (
        len(untranslated_paras) * 5
        + len(untranslated_headings) * 2
        + len(forbidden_terms) * 3
        + len(image_issues) * 4
        + len(at_glance_issues) * 3
    )

    if severity_score == 0:
        grade = "A"
    elif severity_score < 10:
        grade = "B"
    elif severity_score < 30:
        grade = "C"
    else:
        grade = "D"

    return {
        "chapter_id": cid,
        "slug": slug,
        "zh_title": zh_title,
        "en_title": chapter_meta["en_title"],
        "file": str(ch_file.relative_to(ROOT)),
        "char_count": char_count,
        "chinese_ratio": round(chinese_total / char_count if char_count else 0, 2),
        "grade": grade,
        "severity_score": severity_score,
        "issues": {
            "untranslated_paragraphs": untranslated_paras,
            "untranslated_headings": untranslated_headings,
            "forbidden_terms": forbidden_terms,
            "image_issues": image_issues,
            "image_refs_total": len(image_refs),
            "at_a_glance_untranslated": at_glance_issues,
        },
        "issue_counts": {
            "untranslated_paragraphs": len(untranslated_paras),
            "untranslated_headings": len(untranslated_headings),
            "forbidden_terms": len(forbidden_terms),
            "image_issues": len(image_issues),
            "at_a_glance_untranslated": len(at_glance_issues),
        },
    }


def main():
    print("=== 质量审计 ===")
    terminology = load_terminology()
    chapters_meta = load_chapters_meta()
    QA_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    total_issues = Counter()
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        # 从文件名提取章节 ID
        m = re.match(r"^(\d+)-(.+)\.md$", ch_file.name)
        if not m:
            continue
        cid = int(m.group(1))
        if cid not in chapters_meta:
            continue
        result = audit_chapter(ch_file, chapters_meta[cid], terminology)
        results.append(result)
        counts = result["issue_counts"]
        for k, v in counts.items():
            total_issues[k] += v

    # 汇总
    print(f"\n=== 章节评级 ===")
    for r in results:
        emoji = {"A": "✓", "B": "·", "C": "✗", "D": "✗✗"}[r["grade"]]
        c = r["issue_counts"]
        print(
            f"  {emoji} Ch {r['chapter_id']:>2} {r['zh_title']:<28} "
            f"未译段 {c['untranslated_paragraphs']:>2} | "
            f"未译标题 {c['untranslated_headings']:>2} | "
            f"术语 {c['forbidden_terms']:>2} | "
            f"图问题 {c['image_issues']:>2} | "
            f"At a Glance {c['at_a_glance_untranslated']:>2} | "
            f"评级 {r['grade']}"
        )

    print(f"\n=== 汇总 ===")
    for k, v in total_issues.items():
        print(f"  {k}: {v}")

    grade_count = Counter(r["grade"] for r in results)
    print(f"\n=== 评级分布 ===")
    for g in ["A", "B", "C", "D"]:
        print(f"  {g}: {grade_count.get(g, 0)}")

    # 写入 JSON 报告
    json_report = {
        "summary": {
            "total_chapters": len(results),
            "grade_distribution": dict(grade_count),
            "total_issues": dict(total_issues),
        },
        "terminology": {
            "preserve_count": len(terminology["preserve"]),
            "forbidden_count": len(terminology["forbidden"]),
        },
        "chapters": results,
    }
    json_path = QA_DIR / "quality-audit.json"
    json_path.write_text(
        json.dumps(json_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nJSON 报告: {json_path}")

    # 写入 Markdown 报告
    md_path = QA_DIR / "quality-audit.md"
    lines = ["# 翻译质量审计报告", ""]
    lines.append(f"生成时间: 2026-08-09")
    lines.append(f"审计章节: {len(results)}")
    lines.append("")
    lines.append("## 评级分布")
    lines.append("")
    lines.append("| 评级 | 章节数 | 含义 |")
    lines.append("|---|---|---|")
    lines.append("| A | {} | 无问题或极轻微 |".format(grade_count.get("A", 0)))
    lines.append("| B | {} | 个别问题,可控 |".format(grade_count.get("B", 0)))
    lines.append("| C | {} | 多处问题,需修复 |".format(grade_count.get("C", 0)))
    lines.append("| D | {} | 严重问题,优先修复 |".format(grade_count.get("D", 0)))
    lines.append("")
    lines.append("## 总问题统计")
    lines.append("")
    lines.append("| 问题类型 | 数量 |")
    lines.append("|---|---|")
    for k, v in total_issues.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## 章节详细评级")
    lines.append("")
    lines.append("| # | 章节 | 字符数 | 中文占比 | 未译段 | 未译标题 | 术语 | 图问题 | 评级 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
    for r in results:
        c = r["issue_counts"]
        lines.append(
            f"| {r['chapter_id']} | {r['zh_title']} | "
            f"{r['char_count']:,} | {r['chinese_ratio']:.0%} | "
            f"{c['untranslated_paragraphs']} | {c['untranslated_headings']} | "
            f"{c['forbidden_terms']} | {c['image_issues']} | {r['grade']} |"
        )
    lines.append("")
    lines.append("## P0 严重问题清单(详细)")
    lines.append("")
    for r in results:
        c = r["issue_counts"]
        if c["untranslated_paragraphs"] == 0 and c["forbidden_terms"] == 0:
            continue
        lines.append(f"### 第 {r['chapter_id']} 章 {r['zh_title']} ({r['en_title']})")
        lines.append("")
        if c["untranslated_paragraphs"]:
            lines.append(f"**未译英文段落 ({c['untranslated_paragraphs']})**:")
            for p in r["issues"]["untranslated_paragraphs"][:5]:
                lines.append(f"- 第 {p['line_start']} 行: `{p['preview']}...`")
            lines.append("")
        if c["forbidden_terms"]:
            lines.append(f"**术语违规 ({c['forbidden_terms']})**:")
            for ft in r["issues"]["forbidden_terms"][:5]:
                lines.append(f"- 第 {ft['line']} 行: `{ft['forbidden']}` → 应改为 `{ft['preferred']}` (源术语:{ft['source']})")
            lines.append("")
        if c["at_a_glance_untranslated"]:
            lines.append(f"**At a Glance 未翻译 ({c['at_a_glance_untranslated']})**: 中文占比 < 50%")
            lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown 报告: {md_path}")

    return 0 if grade_count.get("D", 0) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())