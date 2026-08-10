---
title: 标准化 (Normalize) — 文本/实体/日期/数字
slug: ch-10-normalize
part: part-ii-core-modules
audience: all
reading_time: 8
prerequisites: [ch-09-parse]
semantica_version: 0.6.0
---

# ch-10 标准化 (Normalize)

> 把 `ParsedDocument` 清洗成下游 (split / extract) 直接消费的"干净文本 + 标准实体 + 标准日期 + 标准数字"。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 统一文本编码 (UTF-8 → NFC)、去除零宽字符、合并空白。
- 把"Jan 1, 2024" / "2024-01-01" / "1/1/2024" 都规整到 ISO 8601。
- 把 "1k" / "1,000" / "$1000" 都规整到 `1000.0` + currency 字段。
- 把同名异构的实体对齐 ("Albert Einstein" ≡ "Einstein, A.")。

### 1.2 一段最小可跑示例

```python
from semantica.normalize import TextNormalizer, DateNormalizer, NumberNormalizer, EntityNormalizer

# 文本
clean = TextNormalizer().normalize(" Hello​  world!  ")  # "Hello world!"

# 日期
iso = DateNormalizer().normalize("Jan 1, 2024")  # "2024-01-01T00:00:00"

# 数字
amt = NumberNormalizer().normalize("$1.5M")  # {"value": 1_500_000.0, "currency": "USD"}

# 实体对齐
canon = EntityNormalizer().canonicalize([
    {"name": "Albert Einstein"},
    {"name": "Einstein, A."},
])
```

### 1.3 何时不用

- 原始数据已经是干净结构化 (如 Parquet) → 跳过 Normalize, 直接进 split。
- 你的应用不需要实体对齐 → 仅用 `TextNormalizer`, 跳过 `EntityNormalizer` (它是 NLP 重活)。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.normalize.TextNormalizer()      # 编码 + 空白 + 控制字符
semantica.normalize.EntityNormalizer()    # 实体名规范化 / 同义词合并
semantica.normalize.DateNormalizer()      # 多格式日期 → ISO 8601
semantica.normalize.NumberNormalizer()    # 多格式数字 + 货币
semantica.normalize.DataCleaner()         # 通用清洗 (去空行/空字段/默认值填充)
```

### 2.2 关键代码路径

- `semantica/normalize/text_normalizer.py` — Unicode NFKC + 去除零宽。
- `semantica/normalize/entity_normalizer.py` — 同义词表 + 别名映射。
- `semantica/normalize/date_normalizer.py` — 基于 `dateutil` + 自定义 hint。
- `semantica/normalize/number_normalizer.py` — 基于 `babel` 货币解析。
- `semantica/normalize/data_cleaner.py` — 通用管道。

### 2.3 最小复现脚本

```python
# examples/ch-10-normalize-minimal.py mirror
from semantica.normalize import TextNormalizer, DateNormalizer, NumberNormalizer

print(repr(TextNormalizer().normalize(" H​éllo  ")))   # 'Hello'
print(DateNormalizer().normalize("01/01/2024"))                   # '2024-01-01T00:00:00'
print(NumberNormalizer().normalize("US$ 1.5 million"))            # {'value': 1500000.0, 'currency': 'USD'}
```

### 2.4 扩展点

- **加自定义同义词表**: 给 `EntityNormalizer(synonyms={"Acme": "Acme Corporation"})`。
- **加日期 hint**: 给 `DateNormalizer(default_timezone="America/Los_Angeles")`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 Normalize 与 Parse 拆开?**
- Parse 是"读懂格式", Normalize 是"消除歧义"。前者依赖格式文档, 后者依赖业务域知识。
- 拆开允许 Normalize 在多 Parse 输出后共享 (例: PDF 与 DOCX 都解析后, 同一种 Normalize 复用)。

### 3.2 与同类对比

| 维度 | Semantica normalize | LangChain DocumentTransformers | spaCy / Stanza |
|---|---|---|---|
| 内置 normalizer 数 | 5 | 3 | N/A |
| 实体对齐 | ✅ (同义词) | ❌ | ✅ (但属于 NER) |
| 日期/数字归一化 | ✅ (强) | ❌ | ❌ |

### 3.3 何时重新设计

- 用户业务出现"行业词表" → 引入 `DomainLexicon` 概念, 在 `EntityNormalizer` 注入。
- normalize 性能成为瓶颈 → 引入 parallel pipeline。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-09-parse]]
- 下一章: [[ch-11-split]]