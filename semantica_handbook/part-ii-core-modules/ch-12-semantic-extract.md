---
title: 实体/关系抽取 (Semantic Extract) — LLM + 规则 + ML
slug: ch-12-semantic-extract
part: part-ii-core-modules
audience: all
reading_time: 14
prerequisites: [ch-11-split]
semantica_version: 0.6.0
---

# ch-12 实体/关系抽取 (Semantic Extract)

> 从 chunk 中抽出 (实体 / 关系 / 三元组)。本章讲解 6 种抽取策略 + 5 个 LLM provider 的统一门面。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 6 种抽取策略: `pattern / regex / rules / ml / huggingface / llm`。
- 选 LLM provider: `OpenAI / Anthropic / Gemini / Groq / Ollama`。
- 跑"实体 → 关系 → 三元组"三段式抽取, 还能做事件检测、共指消解、语义网络构建。

### 1.2 一段最小可跑示例

```python
from semantica.semantic_extract.methods import (
    extract_entities_llm, extract_relations_llm, extract_triplets_llm,
)

text = "Einstein discovered relativity in 1905 at the Swiss patent office."

ents = extract_entities_llm(text, provider="openai", model="gpt-4o-mini")
# -> [{'id': '...', 'name': 'Einstein', 'type': 'PERSON', ...}, ...]

rels = extract_relations_llm(text, entities=ents, provider="anthropic", model="claude-3-5-haiku")
# -> [{'source_id': '...', 'type': 'discovered', 'target_id': '...', ...}, ...]

tris = extract_triplets_llm(text, provider="ollama", model="llama3.1")
# -> [{'subject': 'Einstein', 'predicate': 'discovered', 'object': 'relativity', ...}, ...]
```

### 1.3 何时用哪个

- 想要"快 + 离线": `pattern` / `regex` / `rules`。
- 想要"准确 + 不需 LLM": `ml` (基于 sklearn CRF / SVM)。
- 想要"通用 + 离线": `huggingface` (BERT / RoBERTa NER 模型)。
- 想要"高准确 + 复杂关系": `llm` (gpt-4o / claude-3.5 / llama3.1)。

### 1.4 何时不用

- 你的领域没有结构化文本 (如纯图像) → 先 OCR 再 NER。
- 你的预算不允许 LLM → 用 `huggingface` 本地模型。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
# 函数式 facade (推荐)
semantica.semantic_extract.methods.extract_entities_*(text, ...)
semantica.semantic_extract.methods.extract_relations_*(text, entities=..., ...)
semantica.semantic_extract.methods.extract_triplets_*(text, ...)

# 类式 API
semantica.semantic_extract.NamedEntityRecognizer(method="llm")
semantica.semantic_extract.RelationExtractor()
semantica.semantic_extract.EventDetector()
semantica.semantic_extract.CoreferenceResolver()
semantica.semantic_extract.TripletExtractor()
semantica.semantic_extract.SemanticAnalyzer()
semantica.semantic_extract.SemanticNetworkExtractor()
semantica.semantic_extract.LLMExtraction()
```

### 2.2 关键代码路径

- `semantica/semantic_extract/methods.py:571-1192` — `extract_entities_{pattern,regex,rules,ml,huggingface,llm}` 6 个。
- `semantica/semantic_extract/methods.py:1192-2105` — `extract_relations_*` 6 个。
- `semantica/semantic_extract/methods.py:2185-2670` — `extract_triplets_*` 6 个。
- `semantica/semantic_extract/providers.py:94` — `BaseProvider.generate / generate_structured` 抽象。
- `semantica/semantic_extract/providers.py:563-935` — 5 个 LLM provider 实现 (OpenAI/Anthropic/Gemini/Groq/Ollama)。
- `semantica/semantic_extract/llm_extraction.py:87` — `LLMExtraction` (提供 `enhance_entities / enhance_relations`)。

### 2.3 最小复现脚本

```python
# examples/ch-12-extract-minimal.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "ERROR")

from semantica.semantic_extract.methods import extract_entities_pattern

text = "Einstein and Bohr debated quantum mechanics in 1927."
ents = extract_entities_pattern(text)
for e in ents:
    print(f"- {e['name']:20s} ({e['type']})")
```

### 2.4 扩展点

- **加新 LLM provider**: 继承 `BaseProvider.generate / generate_structured`, 在 `semantic_extract/providers.py:_registry` 注册。
- **加新抽取策略**: 在 `methods.py:_extract_dispatch` 加分支, 实现 `_xxx_extract(text) -> dict`。
- **加自定义 schema**: 用 `generate_structured(json_schema=...)` (依赖 Pydantic / Instructor)。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 6 种策略, 不只 LLM?**
- LLM 准确但贵: 1k 文档 + LLM = $20-200。pattern/regex/rules 几乎免费。
- 离线场景必须 fallback: 没有 OpenAI key 时, huggingface 兜底。
- 6 种策略可以"组合": 先 pattern 抽结构化字段 (邮箱、日期), 再 LLM 抽语义关系 — 是 cookbook 中常见 pipeline。

**为什么 provider 用 thin wrapper 而非 litellm 通用门面?**
- litellm 增加 ~30 MB 依赖, 与 Semantica "extras 化" 哲学不符。
- 自己写 wrapper 让 provider-specific 优化 (如 Anthropic prompt caching) 更容易落地。
- 用户可选 `llm-litellm` extras 切到 litellm 门面, 但默认路径是 thin wrapper。

### 3.2 与同类对比

| 维度 | Semantica semantic_extract | LangChain Extractors | LlamaIndex Extractors |
|---|---|---|---|
| 策略数 | 6 (含 5 个 LLM) | 3 (LLM / 自定义 / Markdown) | 3 (LLM / 自定义 / 手工) |
| Provider 数 | 5 内置 | 30+ via litellm | 30+ via litellm |
| 结构化输出 | ✅ via Instructor | ⚠ 弱 | ⚠ 弱 |
| 同义消解 | ✅ CoreferenceResolver | ❌ | ❌ |

### 3.3 何时重新设计

- 出现"非英语"场景为主 → 加 stanza / jieba 后端。
- LLM 成本成为瓶颈 → 引入 "小型 LLM (3B) 预筛 + 大型 LLM 复核" 二段式。

## 本章图表

> 本章无 Mermaid 图。provider 适配见 [[ch-33-llm-providers]]。

## 跨章引用

- 上一章: [[ch-11-split]]
- 下一章: [[ch-13-embeddings]]
- LLM 适配矩阵: [[ch-33-llm-providers]]
- 数据流位置: [[ch-04-architecture-30kft]] FIG-02 第 6 步