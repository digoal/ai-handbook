#!/usr/bin/env python3
"""
scripts/13_qa_check.py
=====================
自动化 QA:检查翻译结果的完整性、术语一致性、代码完整性、Markdown 结构

输出: qa/qa-report.json + 控制台摘要
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
TERMINOLOGY_YAML = ROOT / "config" / "terminology.yaml"
CHAPTERS_DIR = ROOT / "chapters"
OUTPUT_FILE = ROOT / "qa" / "qa-report.json"


def load_chapters() -> list[dict]:
    return yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]


def load_terminology() -> dict:
    return yaml.safe_load(TERMINOLOGY_YAML.read_text(encoding="utf-8"))


def check_chapter(chapter: dict, terminology: dict) -> dict:
    """单章 QA"""
    cid = chapter["id"]
    slug = chapter["slug"]
    ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"

    blocks_file = ch_dir / "blocks.jsonl"
    translated_file = ch_dir / "translated.jsonl"

    issues = []
    stats = {
        "blocks_total": 0,
        "blocks_translated": 0,
        "blocks_failed": 0,
        "blocks_passthrough": 0,
        "code_chars": 0,
        "text_chars": 0,
    }

    if not blocks_file.exists():
        issues.append({"type": "missing_blocks_file", "severity": "high"})
        return {"chapter_id": cid, "issues": issues, "stats": stats}

    blocks = [json.loads(line) for line in blocks_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    stats["blocks_total"] = len(blocks)

    if not translated_file.exists():
        issues.append({"type": "missing_translated_file", "severity": "high"})
        return {"chapter_id": cid, "issues": issues, "stats": stats}

    translated = {json.loads(line)["block_id"]: json.loads(line)
                    for line in translated_file.read_text(encoding="utf-8").splitlines() if line.strip()}

    # 检查每个块
    for blk in blocks:
        bid = blk["block_id"]
        if bid not in translated:
            issues.append({"type": "missing_translation", "block_id": bid, "severity": "high"})
            continue

        rec = translated[bid]
        status = rec.get("status")
        if status == "translated":
            stats["blocks_translated"] += 1
            stats["text_chars"] += len(rec.get("translated", ""))
        elif status == "passthrough":
            stats["blocks_passthrough"] += 1
            stats["code_chars"] += len(rec.get("translated", ""))
        elif status == "failed":
            stats["blocks_failed"] += 1
            issues.append({"type": "translation_failed", "block_id": bid, "severity": "high"})

        # 检查代码块 SHA256 一致性
        if blk["type"] == "code":
            src_sha = blk["source_sha256"]
            trans_sha = rec.get("source_sha256")
            if src_sha != trans_sha:
                issues.append({"type": "code_sha_mismatch", "block_id": bid, "severity": "high"})

        # 检查文本块:不能空,不能纯英文(>50% 字符)
        if blk["type"] == "text" and status == "translated":
            content = rec.get("translated", "")
            if not content:
                issues.append({"type": "empty_translation", "block_id": bid, "severity": "high"})
            else:
                # 中文字符比例
                chinese_chars = len(re.findall(r"[一-鿿]", content))
                total = len(content)
                if total > 100 and chinese_chars / total < 0.3:
                    issues.append({
                        "type": "low_chinese_ratio",
                        "block_id": bid,
                        "severity": "medium",
                        "ratio": round(chinese_chars / total, 2),
                    })

    # 术语一致性检查(粗略)
    chapter_text = ""
    for bid, rec in translated.items():
        if rec.get("status") == "translated":
            chapter_text += rec.get("translated", "") + "\n"

    # 检查禁止词
    forbidden_terms = []
    for term in terminology.get("core_terms", []):
        for fb in term.get("forbidden", []):
            if fb in chapter_text:
                forbidden_terms.append(fb)
    if forbidden_terms:
        # 重复项只报告一次
        unique = list(set(forbidden_terms))
        for fb in unique:
            issues.append({"type": "forbidden_term", "term": fb, "severity": "medium"})

    return {
        "chapter_id": cid,
        "zh_title": chapter["zh_title"],
        "issues": issues,
        "stats": stats,
    }


def main():
    chapters = load_chapters()
    terminology = load_terminology()

    print("=== QA 检查 ===")
    all_results = []
    total_issues = 0
    total_failed_blocks = 0
    total_text_chars = 0
    total_code_chars = 0

    for ch in chapters:
        result = check_chapter(ch, terminology)
        all_results.append(result)

        issues = result["issues"]
        total_issues += len(issues)
        total_failed_blocks += result["stats"]["blocks_failed"]
        total_text_chars += result["stats"]["text_chars"]
        total_code_chars += result["stats"]["code_chars"]

        # 状态
        stats = result["stats"]
        status_emoji = "✓" if not issues else "✗"
        if result["stats"]["blocks_failed"] > 0:
            status_emoji = "✗"
        print(f"  [{status_emoji}] Ch {result['chapter_id']:>2} {result.get('zh_title',''):<28} "
              f"翻译 {stats['blocks_translated']:>2} / passthrough {stats['blocks_passthrough']:>2} / "
              f"失败 {stats['blocks_failed']:>2} / 问题 {len(issues):>2}")

    # 输出汇总
    print(f"\n=== 汇总 ===")
    print(f"总章节: {len(chapters)}")
    print(f"翻译文本字符: {total_text_chars:,}")
    print(f"代码块字符: {total_code_chars:,}")
    print(f"失败块总数: {total_failed_blocks}")
    print(f"问题总数: {total_issues}")

    if total_issues > 0:
        print(f"\n=== 问题分布 ===")
        issue_types = {}
        for r in all_results:
            for issue in r["issues"]:
                t = issue.get("type", "unknown")
                issue_types[t] = issue_types.get(t, 0) + 1
        for t, n in sorted(issue_types.items(), key=lambda x: -x[1]):
            print(f"  {t}: {n}")

    # 写入报告
    report = {
        "summary": {
            "total_chapters": len(chapters),
            "total_text_chars": total_text_chars,
            "total_code_chars": total_code_chars,
            "total_failed_blocks": total_failed_blocks,
            "total_issues": total_issues,
        },
        "chapters": all_results,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n详细报告: {OUTPUT_FILE}")

    return 0 if total_failed_blocks == 0 else 1


if __name__ == "__main__":
    sys.exit(main())