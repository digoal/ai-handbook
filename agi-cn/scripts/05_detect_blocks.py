#!/usr/bin/env python3
"""
scripts/05_detect_blocks.py
============================
代码块识别 + 段落切块,为翻译准备 blocks.jsonl

输入: chapters/<id>-<slug>/source.md
输出: chapters/<id>-<slug>/blocks.jsonl

每行一个 block,JSON 格式:
{
  "block_id": "ch01-b0001",
  "chapter_id": 1,
  "type": "text" | "code",
  "content": "原文文本",
  "char_count": 1234,
  "word_count": 200,
  "language": "python" | null,
  "source_sha256": "...",
  "page_hint": [41, 50]   # 该块涉及的 PDF 页范围
}

代码块识别启发式:
- 行首 2+ 空格缩进
- 行包含 `def/class/import/from/return/if/for/while/else/elif/try/except`
- 行包含 `(`, `)`, `=`, `{`, `}` 但不是普通散文
- 连续多行类似结构
"""

import json
import re
import hashlib
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML", file=sys.stderr)
    sys.exit(1)

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
CHAPTERS_YAML = ROOT / "config" / "chapters.yaml"
CHAPTERS_DIR = ROOT / "chapters"


# 代码特征
CODE_KEYWORDS = {
    "def ", "class ", "import ", "from ", "return ", "if ", "for ",
    "while ", "else:", "elif ", "try:", "except", "with ", "as ",
    "async ", "await ", "yield ", "lambda ", "print(", "self.",
    "super(", "raise ", "pass\n", "True\n", "False\n", "None\n",
}
# Python 框架/库 API
CODE_API_HINTS = {
    "langchain", "langgraph", "crewai", "google.adk", "vertexai",
    "openai", "anthropic", "ChatPromptTemplate", "ChatOpenAI",
    "StrOutputParser", "Runnable", "InMemoryVectorStore",
    "PromptTemplate", "LLMChain", "Tool", "AgentExecutor",
    "create_react_agent", "Agent", "Runner", "InMemoryRunner",
    "LlmAgent", "BaseAgent", "WorkflowAgent", "SequentialAgent",
    "ParallelAgent", "LlmAgent(", "tool(", "model=",
}


def looks_like_code_line(line: str) -> bool:
    """启发式判断一行是否可能是代码"""
    stripped = line.lstrip()
    if not stripped:
        return False
    # 缩进至少 2 空格
    indent = len(line) - len(stripped)
    if indent < 2:
        return False

    # 包含代码关键字
    for kw in CODE_KEYWORDS:
        if kw in stripped:
            return True

    # 包含代码 API 提示(全词边界)
    for api in CODE_API_HINTS:
        if api in stripped:
            return True

    # 行尾是 : 或 = 后跟赋值
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.+$", stripped):
        return True
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\(.+\):?$", stripped):
        return True
    # 字典/列表/JSON
    if stripped.startswith("{") or stripped.startswith("[") or stripped.startswith("}"):
        return True
    # 注释
    if stripped.startswith("#"):
        return True

    return False


def is_code_paragraph(lines: list[str]) -> bool:
    """判断一组行是否构成代码段"""
    if not lines:
        return False
    code_lines = sum(1 for ln in lines if looks_like_code_line(ln))
    non_empty = sum(1 for ln in lines if ln.strip())
    if non_empty < 2:
        return False
    return code_lines / non_empty >= 0.5


def split_into_paragraphs(content: str) -> list[list[str]]:
    """按空行(>=2 连续空行)切分为段落块"""
    paragraphs = []
    current = []
    blank_count = 0
    for line in content.split("\n"):
        if line.strip() == "":
            blank_count += 1
            if blank_count >= 2:
                if current:
                    paragraphs.append(current)
                    current = []
        else:
            blank_count = 0
            current.append(line)
    if current:
        paragraphs.append(current)
    return paragraphs


def detect_language(lines: list[str]) -> str | None:
    """启发式判断代码语言"""
    text = "\n".join(lines)
    if "import " in text or "def " in text or "class " in text or "print(" in text:
        if "from " in text and "import " in text:
            return "python"
        if "def " in text:
            return "python"
    if "npm " in text or "const " in text or "function " in text or "=>" in text:
        return "javascript"
    if "$" in text and ("pip " in text or "uv " in text):
        return "bash"
    return "python"  # 默认 Python(本书主要是 Python)


def should_skip_block(text: str) -> bool:
    """判断是否应该跳过此块(版权、孤立标题、页眉等)"""
    stripped = text.strip()
    # 版权信息
    if "© The Author(s)" in stripped or "Springer Nature" in stripped:
        return True
    if "https://doi.org/" in stripped:
        return True
    # 孤立标题(短小且只是章节名)
    if len(stripped) < 50 and not stripped.endswith("."):
        # 检查是否只是章节标题(无句号)
        return True
    # 空白块
    if not stripped:
        return True
    return False


def make_blocks(chapter_id: int, source_text: str) -> list[dict]:
    """把章节文本切分为翻译块"""
    paragraphs = split_into_paragraphs(source_text)
    blocks = []
    block_idx = 0

    # 先按段落识别代码/文本
    for para_lines in paragraphs:
        text = "\n".join(para_lines).strip()
        if not text:
            continue

        if is_code_paragraph(para_lines):
            block_idx += 1
            lang = detect_language(para_lines)
            blocks.append({
                "block_id": f"ch{chapter_id:02d}-b{block_idx:04d}",
                "chapter_id": chapter_id,
                "type": "code",
                "language": lang,
                "content": text,
                "char_count": len(text),
                "word_count": len(text.split()),
                "source_sha256": hashlib.sha256(text.encode()).hexdigest()[:16],
                "translate": False,
            })
        else:
            # 文本块:过滤掉版权/孤立标题等
            if should_skip_block(text):
                continue
            # 按目标大小(1500-2500 字符 ≈ 300-500 英文词)切分
            # 注:这里用字符而非英文词,因为我们没有词级 tokenizer
            TARGET = 2000
            if len(text) <= TARGET:
                block_idx += 1
                blocks.append({
                    "block_id": f"ch{chapter_id:02d}-b{block_idx:04d}",
                    "chapter_id": chapter_id,
                    "type": "text",
                    "content": text,
                    "char_count": len(text),
                    "word_count": len(text.split()),
                    "source_sha256": hashlib.sha256(text.encode()).hexdigest()[:16],
                    "translate": True,
                })
            else:
                # 按句子边界切分
                sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
                buf = ""
                for sent in sentences:
                    if len(buf) + len(sent) > TARGET and buf:
                        block_idx += 1
                        blocks.append({
                            "block_id": f"ch{chapter_id:02d}-b{block_idx:04d}",
                            "chapter_id": chapter_id,
                            "type": "text",
                            "content": buf.strip(),
                            "char_count": len(buf),
                            "word_count": len(buf.split()),
                            "source_sha256": hashlib.sha256(buf.encode()).hexdigest()[:16],
                            "translate": True,
                        })
                        buf = sent
                    else:
                        buf = (buf + " " + sent).strip()
                if buf:
                    block_idx += 1
                    blocks.append({
                        "block_id": f"ch{chapter_id:02d}-b{block_idx:04d}",
                        "chapter_id": chapter_id,
                        "type": "text",
                        "content": buf.strip(),
                        "char_count": len(buf),
                        "word_count": len(buf.split()),
                        "source_sha256": hashlib.sha256(buf.encode()).hexdigest()[:16],
                        "translate": True,
                    })

    return blocks


def main():
    chapters = yaml.safe_load(CHAPTERS_YAML.read_text(encoding="utf-8"))["chapters"]

    total_blocks = 0
    total_code = 0
    total_translatable = 0
    total_chars = 0
    summary = []

    for ch in chapters:
        cid = ch["id"]
        slug = ch["slug"]
        ch_dir = CHAPTERS_DIR / f"{cid:02d}-{slug}"
        source_file = ch_dir / "source.md"
        if not source_file.exists():
            continue

        # 移除章节标题和元数据注释
        content = source_file.read_text(encoding="utf-8")
        content = re.sub(r"^# 第 \d+ 章[^\n]*\n\n", "", content)
        content = re.sub(r"^<!--.*?-->\n\n", "", content, flags=re.DOTALL)
        content = content.strip()

        blocks = make_blocks(cid, content)
        blocks_file = ch_dir / "blocks.jsonl"
        with open(blocks_file, "w", encoding="utf-8") as f:
            for blk in blocks:
                f.write(json.dumps(blk, ensure_ascii=False) + "\n")

        code_count = sum(1 for b in blocks if b["type"] == "code")
        text_count = sum(1 for b in blocks if b["type"] == "text")
        ch_chars = sum(b["char_count"] for b in blocks)

        total_blocks += len(blocks)
        total_code += code_count
        total_translatable += text_count
        total_chars += ch_chars

        summary.append({
            "id": cid,
            "zh": ch["zh_title"],
            "blocks": len(blocks),
            "code": code_count,
            "text": text_count,
            "chars": ch_chars,
        })

    print("=== 29 章切块完成 ===")
    print(f"{'Ch':<4}{'标题':<28}{'总块数':>6}{'代码块':>7}{'文本块':>7}{'字符数':>10}")
    for s in summary:
        print(f"  {s['id']:<2} {s['zh']:<28}{s['blocks']:>6}{s['code']:>7}{s['text']:>7}{s['chars']:>10,}")

    print(f"\n=== 汇总 ===")
    print(f"  总块数: {total_blocks}")
    print(f"  代码块: {total_code}(不翻译)")
    print(f"  文本块: {total_translatable}(待翻译)")
    print(f"  总字符: {total_chars:,}")


if __name__ == "__main__":
    main()