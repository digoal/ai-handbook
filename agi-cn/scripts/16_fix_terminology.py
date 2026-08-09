#!/usr/bin/env python3
"""
scripts/16_fix_terminology.py
=============================
根据 config/terminology.yaml 中的 forbidden 列表,做 find/replace,
修复术语违规。

注意:Chinese 字符不是 \\w,word boundary \\b 对中文无效,改用直接字符串匹配。

替换规则(考虑上下文,避免误伤):
  全局(无歧义):
    提示词 → 提示
    多代理 → 多智能体
    嵌入向量 → 嵌入
    提示串联/链接/流水线 → 提示链
    人在闭环 → 人在回路

  上下文相关:
    人机交互 → 人在回路(HITL 语境)
    反射 → 反思(Reflection 语境)
    映射 → 反思(Reflection 语境,语义为"reflect on")
    臆想/虚构 → 幻觉(Hallucination 语境)
    批评者/评论家 → 评审器(Critic 语境)
    守卫/防护栏 → 护栏(Guardrails 语境)
    制定计划 → 规划(Planning 语境)
    并行 → 并行化(Parallelization 语境,且不是"并行计算/并行执行"等通用短语)
    计划 → 规划(Planning 语境,且不是"计划"作为普通名词)
    代理 → 智能体(Agent 语境,排除"代理服务器/反向代理/HTTP代理"等)

输入/输出:修改原地文件,先备份为 .bak
"""

import json
import re
import shutil
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
CHAPTERS_DIR = ROOT / "chapters"
TERMINOLOGY_YAML = ROOT / "config" / "terminology.yaml"
FULL_MD = ROOT / "output" / "agi-zh.md"


# === 全局替换规则(简单字符串替换) ===
GLOBAL_RULES = [
    ("提示词", "提示"),
    ("多代理", "多智能体"),
    ("嵌入向量", "嵌入"),
    ("提示串联", "提示链"),
    ("提示链接", "提示链"),
    ("提示流水线", "提示链"),
    ("人在闭环", "人在回路"),
]


# === 上下文检测函数 ===
def has_any(context: str, keywords: list[str]) -> bool:
    return any(kw in context for kw in keywords)


def ctx_hitl(c: str) -> bool:
    return has_any(c, ["HITL", "人在回路", "人机", "Human-in-the-Loop", "Human-in"])


def ctx_reflection(c: str) -> bool:
    return has_any(c, ["Reflection", "反思", "Self-Reflection", "自我反思"])


def ctx_agent(c: str) -> bool:
    return has_any(c, ["智能体", "Agent", "智能体式", "代理类", "代理程序", "代理者"])


def ctx_guardrail(c: str) -> bool:
    return has_any(c, ["Guardrail", "护栏", "安全"])


def ctx_critic(c: str) -> bool:
    return has_any(c, ["Critic", "评审", "批评", "评论"])


def ctx_hallucination(c: str) -> bool:
    return has_any(c, ["Hallucination", "幻觉"])


def ctx_planning(c: str) -> bool:
    return has_any(c, ["Planning", "规划", "Planner"])


def ctx_parallelization(c: str) -> bool:
    """Parallelization 语境:讨论"并行化模式"本身"""
    return has_any(c, [
        "Parallelization", "并行化",
        "并行模式", "并行执行", "并行处理",
        "并行计算", "并发执行", "并行的",
        "并行任务", "并行方法", "并行生成", "并行化化化",
        "并行运行", "并行调用", "并行实现", "并行的",
        "并行工作流", "并行操作", "并行执行",
    ])


# === 上下文规则:(pattern, replacement, context_check_fn) ===
CONTEXT_RULES = [
    # 人机交互 → 人在回路(HITL 上下文)
    ("人机交互", "人在回路", ctx_hitl),
    # 反射 → 反思(Reflection 上下文)
    ("反射", "反思", ctx_reflection),
    # 映射 → 反思(Reflection 上下文)
    ("映射", "反思", ctx_reflection),
    # 臆想/虚构 → 幻觉(Hallucination 上下文)
    ("臆想", "幻觉", ctx_hallucination),
    ("虚构", "幻觉", ctx_hallucination),
    # 批评者/评论家 → 评审器(Critic 上下文)
    ("批评者", "评审器", ctx_critic),
    ("评论家", "评审器", ctx_critic),
    # 守卫/防护栏 → 护栏(Guardrails 上下文)
    ("守卫", "护栏", ctx_guardrail),
    ("防护栏", "护栏", ctx_guardrail),
    # 制定计划 → 规划(Planning 上下文)
    ("制定计划", "规划", ctx_planning),
    # 计划 → 规划(Planning 上下文,但避免误伤通用"计划"如"工作计划/项目计划")
    # 仅在明确 Planning 语境下替换
    ("计划", "规划", ctx_planning),
    # 代理 → 智能体(Agent 上下文)
    # 注意:会保留"代理服务器/反向代理/HTTP代理/代理池"等通用短语
    # 我们用 negative lookbehind 实现,但 Python re 不支持变长 lookbehind
    # 所以采用两阶段:先全局替换为智能体,然后恢复通用短语
    ("代理", "智能体", ctx_agent),
    # 并行 → 并行化(Parallelization 模式语境)
    ("并行", "并行化", ctx_parallelization),
]


# "代理" 排除白名单(在替换为"智能体"后,再恢复这些)
# 只保留明确是网络代理含义的短语。
# "代理设置"、"代理连接" 等语义模糊,不保留,交由 LLM/人工判断。
PROXY_KEEP = [
    "代理服务器", "反向代理", "正向代理", "代理池",
    "代理请求", "代理地址", "代理端口", "代理IP", "代理网络",
    "代理转发", "代理缓存", "代理认证",
    "HTTP代理", "HTTPS代理", "SOCKS代理", "Web代理",
    "代理模式", "代理链", "代理网关", "透明代理",
    "代理软件", "代理工具", "代理协议",
    "代理角色", "代理节点",
]


def apply_global_rules(text: str) -> tuple[str, Counter]:
    """应用全局替换规则"""
    counter = Counter()
    for old, new in GLOBAL_RULES:
        n = text.count(old)
        if n > 0:
            text = text.replace(old, new)
            counter[old] += n
    return text, counter


def apply_context_rules(text: str) -> tuple[str, Counter]:
    """应用上下文相关规则"""
    counter = Counter()

    for old, new, ctx_fn in CONTEXT_RULES:
        # 找出所有出现位置,逐个判断上下文
        indices = []
        start = 0
        while True:
            i = text.find(old, start)
            if i == -1:
                break
            indices.append(i)
            start = i + len(old)

        if not indices:
            continue

        # 从后往前替换(避免索引偏移)
        new_text = text
        replace_count = 0
        for i in reversed(indices):
            # 取 ±50 字符作为上下文
            ctx_start = max(0, i - 50)
            ctx_end = min(len(new_text), i + len(old) + 50)
            context = new_text[ctx_start:ctx_end]
            if ctx_fn(context):
                # 替换
                new_text = new_text[:i] + new + new_text[i + len(old):]
                replace_count += 1

        if replace_count > 0:
            counter[old] += replace_count
            text = new_text

    return text, counter


def restore_proxy(text: str) -> Counter:
    """恢复"代理"相关的网络代理短语(如果误转为"智能体")"""
    counter = Counter()
    for phrase in PROXY_KEEP:
        wrong = phrase.replace("代理", "智能体")
        n = text.count(wrong)
        if n > 0:
            text = text.replace(wrong, phrase)
            counter[wrong] += n
    return text, counter


def apply_all_rules(text: str) -> tuple[str, Counter]:
    """应用所有规则"""
    counter = Counter()

    # 1. 全局规则
    text, c = apply_global_rules(text)
    counter.update(c)

    # 2. 上下文规则
    text, c = apply_context_rules(text)
    counter.update(c)

    # 3. 恢复被误伤的"代理"相关短语
    text, c = restore_proxy(text)
    counter.update(c)

    return text, counter


def make_backup(path: Path):
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)


def fix_file(path: Path) -> Counter:
    make_backup(path)
    text = path.read_text(encoding="utf-8")
    new_text, counter = apply_all_rules(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return counter


def fix_translated_jsonl(ch_dir: Path) -> Counter:
    jsonl = ch_dir / "translated.jsonl"
    if not jsonl.exists():
        return Counter()
    make_backup(jsonl)

    counter = Counter()
    records = []
    changed = False
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("type") == "text" and rec.get("translated"):
            old = rec["translated"]
            new, c = apply_all_rules(old)
            if new != old:
                rec["translated"] = new
                changed = True
                counter.update(c)
        records.append(rec)

    if changed:
        with open(jsonl, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return counter


def main():
    print("=== 术语替换(第二轮,含并行/计划/映射/代理)===")

    total_counter = Counter()

    print("\n[1] 修复章节 markdown 文件")
    for ch_file in sorted(BY_CHAPTER_DIR.glob("*.md")):
        c = fix_file(ch_file)
        if c:
            # 简化输出:只显示有变化的
            short = {k: v for k, v in c.items() if v > 0}
            if short:
                print(f"  {ch_file.name}: {dict(short)}")
            total_counter.update(c)

    print("\n[2] 修复完整 markdown")
    if FULL_MD.exists():
        c = fix_file(FULL_MD)
        if c:
            short = {k: v for k, v in c.items() if v > 0}
            if short:
                print(f"  agi-zh.md: {dict(short)}")
            total_counter.update(c)

    print("\n[3] 修复 translated.jsonl")
    for ch_dir in sorted(CHAPTERS_DIR.iterdir()):
        if not ch_dir.is_dir():
            continue
        c = fix_translated_jsonl(ch_dir)
        if c:
            short = {k: v for k, v in c.items() if v > 0}
            if short:
                print(f"  {ch_dir.name}: {dict(short)}")
            total_counter.update(c)

    print(f"\n=== 汇总 ===")
    print(f"总替换次数: {sum(total_counter.values())}")
    for pattern, n in sorted(total_counter.items(), key=lambda x: -x[1]):
        if n > 0:
            print(f"  {pattern}: {n}")

    stats_file = ROOT / "qa" / "terminology-fixes.json"
    stats_file.write_text(
        json.dumps(dict(total_counter), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n统计: {stats_file}")


if __name__ == "__main__":
    main()