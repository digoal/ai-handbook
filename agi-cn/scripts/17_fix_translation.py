#!/usr/bin/env python3
"""
scripts/17_fix_translation.py
=============================
检测未译英文块与英文标题,调用 Claude API 重新翻译,写回。

检测逻辑:
  1. 对每个章节的 translated.jsonl,扫描 type=text 的块
  2. 计算中文字符比例,如果 < 30% 且长度 > 100 字符,标记为"未译"
  3. 对块内容中的英文标题(以 # 开头的英文行),也标记

重译:
  - 复用 scripts/08_translate_blocks.py 的 translate_block 函数
  - 并发数 4(可调)

写回:
  - 更新 chapters/<id>-<slug>/translated.jsonl
  - 重新生成 chapters/<id>-<slug>/source.md 与 output/agi-zh-by-chapter/<id>-<slug>.md
    (实际上,我们只需更新对应块的 translated 字段;然后重新组装 markdown)

依赖:
  - ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY
  - ANTHROPIC_BASE_URL(可选,代理)
  - ANTHROPIC_DEFAULT_OPUS_MODEL(可选,默认 claude-opus-4-8)

参数:
  --chapter N    只处理第 N 章
  --dry-run      只检测,不翻译
  --concurrency N 并发数(默认 4)
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

try:
    import yaml
    from anthropic import Anthropic
except ImportError as e:
    print(f"缺少依赖: {e}", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"

# 复用 08 的翻译函数
sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location("tr", ROOT / "scripts" / "08_translate_blocks.py")
tr_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr_module)


def is_chinese_char(c: str) -> bool:
    return "一" <= c <= "鿿"


def detect_untranslated_blocks(ch_dir: Path) -> list[dict]:
    """检测一个章节中未译的块"""
    jsonl = ch_dir / "translated.jsonl"
    if not jsonl.exists():
        return []
    blocks_file = ch_dir / "blocks.jsonl"
    if not blocks_file.exists():
        return []
    blocks = {
        json.loads(line)["block_id"]: json.loads(line)
        for line in blocks_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    untranslated = []
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("type") != "text" or rec.get("status") != "translated":
            continue
        content = rec.get("translated", "")
        if not content:
            continue
        # 检测未译:中文字符比例 < 30% 且长度 > 80 字符
        chinese = sum(1 for c in content if is_chinese_char(c))
        total = len(content)
        if total < 80:
            continue
        ratio = chinese / total if total else 0
        if ratio < 0.30:
            bid = rec["block_id"]
            untranslated.append({
                "block_id": bid,
                "chapter_id": rec.get("chapter_id"),
                "content_in_blocks": blocks.get(bid, {}).get("content", ""),
                "current_translation": content,
                "chinese_ratio": round(ratio, 2),
                "length": total,
            })
    return untranslated


def retrans_block(client, model: str, block_record: dict, blocks_data: dict, chapter: dict) -> dict:
    """重译单个块"""
    bid = block_record["block_id"]
    blk = blocks_data.get(bid, {})
    src_content = blk.get("content", "")
    if not src_content:
        return {"block_id": bid, "success": False, "error": "no source content"}

    # 调用翻译函数
    result = tr_module.translate_block(client, model, blk, chapter)

    return {
        "block_id": bid,
        "success": result["success"],
        "translated": result.get("translated", ""),
        "error": result.get("error"),
        "source_sha256": blk.get("source_sha256"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, help="只处理第 N 章")
    parser.add_argument("--dry-run", action="store_true", help="只检测,不翻译")
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()

    chapters_data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]
    if args.chapter:
        chapters_data = [c for c in chapters_data if c["id"] == args.chapter]

    # 先检测所有未译块
    print(f"=== 检测未译块 ===")
    all_untranslated = []
    for ch in chapters_data:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"
        untranslated = detect_untranslated_blocks(ch_dir)
        if untranslated:
            print(f"  Ch {cid:>2} {ch['zh_title']:<28}: {len(untranslated)} 块未译")
            for u in untranslated:
                u["chapter"] = ch
                u["ch_dir"] = ch_dir
            all_untranslated.extend(untranslated)

    print(f"\n总未译块: {len(all_untranslated)}")

    if args.dry_run or not all_untranslated:
        if args.dry_run:
            print("(dry-run 模式,不实际翻译)")
        return

    # 初始化 API 客户端
    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: 请设置 ANTHROPIC_AUTH_TOKEN", file=sys.stderr)
        sys.exit(1)
    base_url = os.environ.get("ANTHROPIC_BASE_URL")
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    client = Anthropic(**client_kwargs)
    model = os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", "claude-opus-4-8")

    print(f"\n=== 开始重译 ===")
    print(f"模型: {model}, 并发: {args.concurrency}")

    # 按章节分组处理
    by_chapter = {}
    for u in all_untranslated:
        cid = u["chapter"]["id"]
        by_chapter.setdefault(cid, []).append(u)

    total_success = 0
    total_failed = 0

    for cid, items in by_chapter.items():
        ch = items[0]["chapter"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"

        # 读取原始 blocks
        blocks_data = {}
        for line in (ch_dir / "blocks.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                blocks_data[rec["block_id"]] = rec

        print(f"\n[Ch {cid} {ch['zh_title']}] 重译 {len(items)} 块...")

        # 并发翻译
        success_results = []
        with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
            futures = {
                pool.submit(retrans_block, client, model, item, blocks_data, ch): item
                for item in items
            }
            for future in as_completed(futures):
                item = futures[future]
                try:
                    r = future.result()
                except Exception as e:
                    r = {"block_id": item["block_id"], "success": False, "error": str(e)}
                if r.get("success"):
                    success_results.append(r)
                    print(f"  ✓ {r['block_id']}")
                    total_success += 1
                else:
                    print(f"  ✗ {r['block_id']}: {r.get('error', '')[:100]}")
                    total_failed += 1

        # 写回 translated.jsonl
        if success_results:
            # 读取现有 jsonl
            jsonl_path = ch_dir / "translated.jsonl"
            records = []
            for line in jsonl_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                # 更新成功的块
                for r in success_results:
                    if rec.get("block_id") == r["block_id"]:
                        rec["translated"] = r["translated"]
                        rec["status"] = "translated"
                        rec["usage"] = rec.get("usage", {})
                        rec["usage"]["retranslated_ts"] = time.time()
                        break
                records.append(rec)
            # 写回
            jsonl_path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
                encoding="utf-8",
            )
            print(f"  → 已更新 {ch_dir.name}/translated.jsonl")

    print(f"\n=== 汇总 ===")
    print(f"成功: {total_success}")
    print(f"失败: {total_failed}")


if __name__ == "__main__":
    main()