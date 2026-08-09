#!/usr/bin/env python3
"""阶段 4 残存未译段落重译(直接编辑 .md,不走 jsonl)。

audit 报告的 line_start/line_end 是 .md 文件中的行号。
本脚本按行号提取原文,调用 LLM 重译,直接修改 .md。
"""
import json
import os
import re
import sys
import time
from pathlib import Path
import yaml
from anthropic import Anthropic

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
BY_CHAPTER_DIR = ROOT / "output" / "agi-zh-by-chapter"


def call_llm(client: Anthropic, model: str, prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text.strip()
        except Exception as e:
            print(f"  LLM 错误(尝试 {attempt + 1}): {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise


def main() -> int:
    chapters_data = yaml.safe_load(CHAPTERS_YAML.read_text())["chapters"]
    slug_by_id = {ch["id"]: ch["slug"] for ch in chapters_data}

    audit = json.loads((ROOT / "qa" / "quality-audit.json").read_text())
    targets = []
    for ch in audit["chapters"]:
        for issue in ch.get("issues", {}).get("untranslated_paragraphs", []):
            targets.append({
                "chapter_id": ch["chapter_id"],
                "file": ch["file"],
                "line_start": issue["line_start"],
                "line_end": issue["line_end"],
                "preview": issue["preview"],
            })

    # 过滤:跳过参考文献/URL/术语清单
    skip_keywords = [
        "Improving Fault Tolerance", "Towards Fault Tolerance",
        "Inference Scaling Laws", "https://", "google.github.io",
    ]
    targets_to_translate = []
    for t in targets:
        if any(kw in t["preview"] for kw in skip_keywords):
            print(f"  跳过 Ch{t['chapter_id']} L{t['line_start']}: 参考文献/URL")
            continue
        if "有效的动词包括" in t["preview"]:
            print(f"  跳过 Ch{t['chapter_id']} L{t['line_start']}: 术语清单")
            continue
        targets_to_translate.append(t)

    print(f"待重译: {len(targets_to_translate)} / {len(targets)} 段")
    if not targets_to_translate:
        return 0

    client = Anthropic(
        api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
        base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
    )
    model = os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", "claude-opus-4-8")

    # 按章节分组(每章一次合并调用)
    by_chapter = {}
    for t in targets_to_translate:
        by_chapter.setdefault(t["chapter_id"], []).append(t)

    success_count = 0
    for cid in sorted(by_chapter.keys()):
        ch_targets = by_chapter[cid]
        file_path = Path(ch_targets[0]["file"])
        if not file_path.is_absolute():
            file_path = ROOT / file_path
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=False)

        # 提取每个 target 的原文
        originals = []
        for t in ch_targets:
            ls, le = t["line_start"], t["line_end"]
            text = "\n".join(lines[ls - 1:le])
            originals.append(text)

        # 合并 prompt
        prompt = "你是一位专业的中英翻译。请将以下多个段落翻译为简体中文,保留技术术语(产品/框架/API 名用英文)和代码格式。每段前标注 `---段落N---`,翻译后也用相同分隔符。\n\n"
        for i, orig in enumerate(originals, 1):
            prompt += f"---段落{i} (Ch{cid} L{ch_targets[i-1]['line_start']}-{ch_targets[i-1]['line_end']})---\n{orig}\n\n"
        prompt += "直接返回翻译,不要解释:"

        print(f"\n>>> Ch {cid}: 合并 {len(ch_targets)} 段")
        try:
            response = call_llm(client, model, prompt)
        except Exception as e:
            print(f"  LLM 失败: {e}")
            continue

        # 解析响应
        parts = re.split(r'---段落(\d+)---', response)
        translations = {}
        if len(parts) >= 3:
            for i in range(1, len(parts), 2):
                idx = int(parts[i])
                content = parts[i + 1].strip() if i + 1 < len(parts) else ""
                translations[idx] = content

        # 写回 .md(从后往前替换,避免行号偏移)
        new_lines = list(lines)
        for i in range(len(ch_targets), 0, -1):
            t = ch_targets[i - 1]
            if i not in translations or not translations[i]:
                print(f"  ✗ L{t['line_start']}-{t['line_end']}: 未获取翻译")
                continue
            new_text = translations[i]
            # 用单行或多行替换
            new_lines[t["line_start"] - 1:t["line_end"]] = [new_text]
            print(f"  ✓ L{t['line_start']}-{t['line_end']}: {new_text[:60]}...")
            success_count += 1

        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    print(f"\n=== 阶段 4 完成:成功 {success_count} / {len(targets_to_translate)} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())