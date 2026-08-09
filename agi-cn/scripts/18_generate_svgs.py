#!/usr/bin/env python3
"""
scripts/18_generate_svgs.py
===========================
根据 config/figures.yaml,为缺失/断裂的图生成 SVG 文件。

输出:
  output/agi-zh-by-chapter/svg/fig-X-Y.svg       # SVG 文件
  output/agi-zh-by-chapter/svg/manifest.json     # 索引

实现:
  - 调用 Claude API,给定图描述与 SVG 规范,生成 SVG 代码
  - 用 xml.etree.ElementTree 验证 SVG 合法性
  - 失败重试 3 次
  - 并发 4

SVG 规范:
  - viewBox="0 0 800 600"
  - 字体: font-family="sans-serif"
  - 配色:
    背景: #FFFFFF
    节点边框: #1F2937
    节点填充: #DBEAFE
    文本: #111827
    主箭头: #374151
  - 节点: <rect> 圆角 8px
  - 箭头: <marker> 定义三角箭头
  - 文本: <text> 居中,14-16px
  - 不使用 <foreignObject>

参数:
  --figure ID     只生成某张图(如 "3-1")
  --dry-run       检测但不生成
"""

import argparse
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import yaml
    from anthropic import Anthropic
except ImportError as e:
    print(f"缺少依赖: {e}", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
FIGURES_YAML = ROOT / "config" / "figures.yaml"
SVG_DIR = ROOT / "output" / "agi-zh-by-chapter" / "svg"
MANIFEST = SVG_DIR / "manifest.json"


SVG_PROMPT_TEMPLATE = """你是一位专业的技术插画师,擅长为 AI/Agent 技术书籍绘制简洁清晰的架构示意图。

## 任务
基于以下描述,生成符合规范的 SVG 图。

## 图信息
- 标题: {title_zh}
- 类型: {diagram_type}
- 描述: {description}

## SVG 规范(严格遵守)
- viewBox="0 0 800 600"
- 字体: font-family="sans-serif, Microsoft YaHei, 微软雅黑"
- 配色:
  - 背景: #FFFFFF
  - 节点边框: #1F2937 (深灰)
  - 节点填充: #DBEAFE (浅蓝)
  - 文本颜色: #111827 (近黑)
  - 主箭头: #374151 (深灰)
  - 强调节点: 用 #FEF3C7 (浅黄) 填充,#B45309 (橙) 边框
- 节点: <rect> 圆角 8px (rx="8" ry="8"),边框宽 2px
- 箭头: 用 <defs><marker id="arrow-{id}"> 定义三角箭头,通过 marker-end 引用
- 文本: <text> text-anchor="middle",font-size 在 14-18px 之间
- 文字要支持中文,确保 XML 转义正确(<>& 等)
- 不使用 <foreignObject>
- 节点之间用 <line> 或 <path> 连接,加 marker-end
- 整体布局:从左到右或从上到下,留有合理边距(20-40px)
- 图标题放在 SVG 顶部,居中,字号 18-20px
- 图说明(可选)放在底部,字号 12-14px,灰一些 (#6B7280)

## 输出要求
- 仅输出完整的 <svg>...</svg> 代码
- 不要 markdown 代码围栏
- 不要任何额外说明文字
- 确保 SVG 是合法 XML(用 xml.etree.ElementTree 可解析)

## 开始生成
"""


def is_valid_svg(content: str) -> tuple[bool, str]:
    """验证 SVG 是否合法 XML"""
    try:
        # 提取 <svg>...</svg> 部分(去除可能的围栏或前后空白)
        m = re.search(r"<svg[\s\S]*?</svg>", content)
        if not m:
            return False, "No <svg> tag found"
        svg_text = m.group(0)
        ET.fromstring(svg_text)
        return True, ""
    except ET.ParseError as e:
        return False, f"Parse error: {e}"


def generate_one(client, model: str, fig: dict, max_retries: int = 3) -> dict:
    """生成单张图的 SVG"""
    fig_id = fig["id"]
    title = fig["title_zh"]
    dtype = fig.get("diagram_type", "overview")
    desc = fig.get("description", "")

    prompt = SVG_PROMPT_TEMPLATE.format(
        title_zh=title,
        diagram_type=dtype,
        description=desc,
        id=fig_id.replace("-", "_"),
    )

    last_error = ""
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )
            content = ""
            for blk in response.content:
                if blk.type == "text":
                    content += blk.text

            valid, err = is_valid_svg(content)
            if valid:
                return {"id": fig_id, "success": True, "content": content, "attempts": attempt + 1}

            last_error = err
            # 调整 prompt 强调格式
            if attempt < max_retries - 1:
                prompt += f"\n\n注意:上一次的输出有错误({err}),请确保输出合法的 XML。"
        except Exception as e:
            last_error = f"API error: {e}"
            time.sleep(2)

    return {
        "id": fig_id,
        "success": False,
        "content": None,
        "error": last_error,
        "attempts": max_retries,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", help="只生成某张图(如 '3-1')")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()

    # 加载图清单
    data = yaml.safe_load(FIGURES_YAML.read_text(encoding="utf-8"))
    figures = data.get("figures", [])
    if args.figure:
        figures = [f for f in figures if f["id"] == args.figure]

    print(f"=== SVG 生成 ===")
    print(f"待生成: {len(figures)} 张")

    if args.dry_run:
        for f in figures:
            print(f"  - fig-{f['id']} (Ch {f['chapter']}): {f['title_zh']}")
        return

    # 初始化客户端
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

    SVG_DIR.mkdir(parents=True, exist_ok=True)

    # 加载已有 manifest
    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    success_count = 0
    fail_count = 0

    # 并发生成
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {pool.submit(generate_one, client, model, f): f for f in figures}
        for future in as_completed(futures):
            f = futures[future]
            try:
                r = future.result()
            except Exception as e:
                r = {"id": f["id"], "success": False, "error": str(e)}

            fig_id = f["id"]
            if r["success"]:
                # 保存 SVG
                svg_path = SVG_DIR / f"fig-{fig_id}.svg"
                # 提取 <svg> 标签
                m = re.search(r"<svg[\s\S]*?</svg>", r["content"])
                if m:
                    svg_text = m.group(0)
                    # 确保是合法 XML
                    try:
                        ET.fromstring(svg_text)
                        svg_path.write_text(svg_text, encoding="utf-8")
                        manifest[fig_id] = {
                            "file": f"svg/fig-{fig_id}.svg",
                            "chapter": f["chapter"],
                            "title": f["title_zh"],
                            "diagram_type": f.get("diagram_type"),
                            "valid": True,
                            "attempts": r.get("attempts", 1),
                        }
                        print(f"  ✓ fig-{fig_id} ({r.get('attempts', 1)} 试) → {svg_path.name}")
                        success_count += 1
                    except ET.ParseError:
                        manifest[fig_id] = {
                            "chapter": f["chapter"],
                            "title": f["title_zh"],
                            "valid": False,
                            "error": "Parse error after generation",
                        }
                        print(f"  ✗ fig-{fig_id}: parse error after generation")
                        fail_count += 1
            else:
                manifest[fig_id] = {
                    "chapter": f["chapter"],
                    "title": f["title_zh"],
                    "valid": False,
                    "error": r.get("error", "unknown"),
                    "attempts": r.get("attempts", 0),
                }
                print(f"  ✗ fig-{fig_id}: {r.get('error', 'unknown')[:100]}")
                fail_count += 1

            # 增量保存 manifest
            MANIFEST.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    print(f"\n=== 汇总 ===")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()