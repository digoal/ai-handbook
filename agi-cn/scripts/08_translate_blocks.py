#!/usr/bin/env python3
"""
scripts/08_translate_blocks.py
==============================
核心翻译脚本:逐块调用 Claude API 翻译

输入: chapters/<id>-<slug>/blocks.jsonl
输出:
  chapters/<id>-<slug>/translated.jsonl     # 翻译结果
  chapters/<id>-<slug>/translation_state.json # 状态(断点续跑)
  translation/usage.jsonl                     # token 用量日志
  translation/failures.jsonl                  # 失败块

参数:
  --chapter N          只翻译第 N 章
  --block-id ID        只翻译特定块
  --retry-failed       重试失败块
  --concurrency N      并发数(默认 2)
  --model NAME         模型名(默认 claude-opus-4-8)
  --dry-run            仅显示请求,不实际调用

依赖:
  pip install anthropic pyyaml
  设置环境变量 ANTHROPIC_API_KEY
"""

import argparse
import json
import os
import re
import sys
import time
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    import yaml
except ImportError:
    print("缺少 PyYAML, pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import anthropic
except ImportError:
    print("缺少 anthropic SDK, pip install anthropic", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
PROMPT_SYSTEM = (ROOT / "config" / "prompt" / "system.txt").read_text(encoding="utf-8")
PROMPT_USER_TPL = (ROOT / "config" / "prompt" / "user.txt").read_text(encoding="utf-8")
TERMINOLOGY = (ROOT / "config" / "terminology.yaml").read_text(encoding="utf-8")
CHAPTERS_DIR = ROOT / "chapters"
USAGE_FILE = ROOT / "translation" / "usage.jsonl"
FAILURES_FILE = ROOT / "translation" / "failures.jsonl"

# 环境变量适配(支持 minimax 代理)
DEFAULT_MODEL = os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", "claude-opus-4-8")
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL")


def base_url_is_proxy() -> bool:
    """判断是否为代理 URL(minimax 等)"""
    if not BASE_URL:
        return False
    return "minimaxi" in BASE_URL.lower() or "proxy" in BASE_URL.lower()


def load_chapters() -> list[dict]:
    return yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]


def get_chapter_meta(cid: int) -> dict:
    chapters = load_chapters()
    for ch in chapters:
        if ch["id"] == cid:
            return ch
    return None


def build_user_prompt(block: dict, chapter: dict, prev_tail: str = "", next_head: str = "") -> str:
    """构造 user prompt"""
    template = PROMPT_USER_TPL
    section_path = f"第 {chapter['id']} 章 > {chapter['zh_title']}"

    # 转义用户模板中的 Python 占位符
    content = template.format(
        chapter_id=chapter["id"],
        chapter_title=chapter["zh_title"],
        en_title=chapter["en_title"],
        section_path=section_path,
        page_start=chapter["pdf_start_page"],
        page_end=chapter["pdf_end_page"],
        block_id=block["block_id"],
        total_blocks="?",
        chapter_blocks="?",
        prev_block_tail=prev_tail or "(无)",
        source_text=block["content"],
        next_block_head=next_head or "(无)",
    )
    return content


def translate_block(client, model: str, block: dict, chapter: dict,
                    prev_tail: str = "", next_head: str = "") -> dict:
    """翻译单个块"""
    user_prompt = build_user_prompt(block, chapter, prev_tail, next_head)

    # 添加术语表到 system prompt 末尾
    system = PROMPT_SYSTEM + "\n\n# 术语表原文(来自 terminology.yaml)\n\n" + TERMINOLOGY

    start = time.time()
    try:
        # 构造请求参数(基础版,不启用 thinking 以适配代理)
        kwargs = {
            "model": model,
            "max_tokens": 8000,
            "system": system,
            "messages": [{"role": "user", "content": user_prompt}],
        }
        # 如果是 Claude 官方 API,启用 thinking
        if "claude" in model.lower() and not base_url_is_proxy():
            kwargs["thinking"] = {"type": "adaptive"}

        response = client.messages.create(**kwargs)

        elapsed = time.time() - start

        # 提取文本输出
        translated_text = ""
        for block_out in response.content:
            if block_out.type == "text":
                translated_text += block_out.text

        # 记录用量
        usage = {
            "ts": datetime.now().isoformat(),
            "block_id": block["block_id"],
            "chapter_id": block["chapter_id"],
            "model": model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "elapsed_sec": round(elapsed, 2),
            "stop_reason": response.stop_reason,
        }

        return {
            "success": True,
            "block_id": block["block_id"],
            "translated": translated_text,
            "usage": usage,
            "source_sha256": block["source_sha256"],
        }
    except Exception as e:
        return {
            "success": False,
            "block_id": block["block_id"],
            "error": str(e),
            "error_type": type(e).__name__,
            "source_sha256": block["source_sha256"],
        }


def load_state(ch_dir: Path) -> dict:
    state_file = ch_dir / "translation_state.json"
    if state_file.exists():
        return json.loads(state_file.read_text(encoding="utf-8"))
    return {"translated_blocks": [], "failed_blocks": []}


def save_state(ch_dir: Path, state: dict):
    state_file = ch_dir / "translation_state.json"
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def translate_chapter(client, model: str, chapter: dict, concurrency: int = 2,
                       dry_run: bool = False, retry_failed: bool = False) -> dict:
    """翻译一章"""
    cid = chapter["id"]
    slug = chapter["slug"]
    ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"
    blocks_file = ch_dir / "blocks.jsonl"
    translated_file = ch_dir / "translated.jsonl"

    if not blocks_file.exists():
        return {"chapter": cid, "status": "no_blocks"}

    blocks = [json.loads(line) for line in blocks_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    state = load_state(ch_dir)
    translated_ids = set(state.get("translated_blocks", []))

    # 加载已翻译结果(用于断点续跑)
    translated_map = {}
    if translated_file.exists():
        for line in translated_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                translated_map[rec["block_id"]] = rec

    # 待翻译块
    pending = []
    for blk in blocks:
        if blk["type"] == "code":
            # 代码块不翻译,直接写入
            if blk["block_id"] not in translated_map:
                translated_map[blk["block_id"]] = {
                    "block_id": blk["block_id"],
                    "type": "code",
                    "source_sha256": blk["source_sha256"],
                    "translated": blk["content"],  # 原样保留
                    "translate": False,
                    "status": "passthrough",
                }
            continue
        if retry_failed:
            if blk["block_id"] in translated_map and translated_map[blk["block_id"]].get("status") != "failed":
                continue
        else:
            if blk["block_id"] in translated_map:
                continue
        pending.append(blk)

    if dry_run:
        return {"chapter": cid, "pending": len(pending), "dry_run": True}

    print(f"[Ch {cid:>2} {chapter['zh_title']}] 待翻译 {len(pending)} 块,已翻译 {len(translated_map) - len(pending)} 块")

    # 顺序翻译(并发初期建议 2-4)
    chapter_start = time.time()
    for i, blk in enumerate(pending, 1):
        # 上一块末尾 + 下一块开头(各 200 字符)
        prev_tail = ""
        next_head = ""
        blk_idx_in_chapter = blocks.index(blk)
        if blk_idx_in_chapter > 0:
            prev_block = blocks[blk_idx_in_chapter - 1]
            prev_tail = prev_block["content"][-200:]
        if blk_idx_in_chapter < len(blocks) - 1:
            next_block = blocks[blk_idx_in_chapter + 1]
            next_head = next_block["content"][:200]

        result = translate_block(client, model, blk, chapter, prev_tail, next_head)

        if result["success"]:
            translated_map[blk["block_id"]] = {
                "block_id": blk["block_id"],
                "type": "text",
                "source_sha256": blk["source_sha256"],
                "translated": result["translated"],
                "translate": True,
                "status": "translated",
                "usage": result["usage"],
            }
            state["translated_blocks"].append(blk["block_id"])
            # 记录用量
            with open(USAGE_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(result["usage"], ensure_ascii=False) + "\n")
            elapsed = result["usage"]["elapsed_sec"]
            in_t = result["usage"]["input_tokens"]
            out_t = result["usage"]["output_tokens"]
            print(f"  [{i:>3}/{len(pending)}] {blk['block_id']} ✓ ({elapsed:.1f}s, in={in_t}, out={out_t})")
        else:
            translated_map[blk["block_id"]] = {
                "block_id": blk["block_id"],
                "type": "text",
                "source_sha256": blk["source_sha256"],
                "translated": None,
                "translate": True,
                "status": "failed",
                "error": result["error"],
            }
            state["failed_blocks"].append(blk["block_id"])
            with open(FAILURES_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "ts": datetime.now().isoformat(),
                    "block_id": blk["block_id"],
                    "chapter_id": cid,
                    "error": result["error"],
                    "error_type": result["error_type"],
                }, ensure_ascii=False) + "\n")
            print(f"  [{i:>3}/{len(pending)}] {blk['block_id']} ✗ {result['error_type']}: {result['error'][:80]}")
            time.sleep(5)  # 失败后等待

        # 每块翻译后保存状态(支持断点续跑)
        # 按 block_id 顺序写入
        with open(translated_file, "w", encoding="utf-8") as f:
            for b in blocks:
                if b["block_id"] in translated_map:
                    f.write(json.dumps(translated_map[b["block_id"]], ensure_ascii=False) + "\n")
        save_state(ch_dir, state)

    elapsed_total = time.time() - chapter_start
    success_count = sum(1 for v in translated_map.values() if v.get("status") == "translated")
    fail_count = sum(1 for v in translated_map.values() if v.get("status") == "failed")

    return {
        "chapter": cid,
        "title": chapter["zh_title"],
        "success": success_count,
        "failed": fail_count,
        "elapsed_sec": round(elapsed_total, 1),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, help="只翻译第 N 章")
    parser.add_argument("--block-id", help="只翻译特定块")
    parser.add_argument("--retry-failed", action="store_true", help="重试失败块")
    parser.add_argument("--concurrency", type=int, default=2, help="并发数(默认 2)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    parser.add_argument("--dry-run", action="store_true", help="仅显示请求,不调用")
    args = parser.parse_args()

    api_key = API_KEY
    if not api_key and not args.dry_run:
        print("ERROR: 请设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    # 创建客户端(支持代理)
    client_kwargs = {"api_key": api_key} if api_key else {}
    if BASE_URL:
        client_kwargs["base_url"] = BASE_URL
    client = anthropic.Anthropic(**client_kwargs) if api_key else None

    chapters = load_chapters()
    if args.chapter:
        chapters = [c for c in chapters if c["id"] == args.chapter]
    if not chapters:
        print(f"未找到章节 {args.chapter}")
        sys.exit(1)

    USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USAGE_FILE.exists():
        USAGE_FILE.write_text("")

    print(f"=== 翻译任务开始 ===")
    print(f"模型: {args.model}")
    print(f"并发: {args.concurrency}")
    print(f"章节: {[c['id'] for c in chapters]}")
    print(f"模式: {'DRY RUN' if args.dry_run else 'LIVE'}\n")

    results = []
    for ch in chapters:
        result = translate_chapter(
            client, args.model, ch,
            concurrency=args.concurrency,
            dry_run=args.dry_run,
            retry_failed=args.retry_failed,
        )
        results.append(result)
        print()

    print(f"\n=== 翻译汇总 ===")
    for r in results:
        if "error" in r:
            print(f"  Ch {r['chapter']}: {r['error']}")
        elif "dry_run" in r:
            print(f"  Ch {r['chapter']}: 待翻译 {r['pending']} 块 (dry run)")
        else:
            print(f"  Ch {r['chapter']} {r.get('title',''):<24} ✓ {r['success']} / ✗ {r['failed']} / {r['elapsed_sec']}s")


if __name__ == "__main__":
    main()