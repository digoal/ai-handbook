---
title: 格式解析 (Parse) — PDF/HTML/MD/DOCX
slug: ch-09-parse
part: part-ii-core-modules
audience: all
reading_time: 10
prerequisites: [ch-08-ingest]
semantica_version: 0.6.0
---

# ch-09 格式解析 (Parse)

> 把 `SourceDocument` 的字节流变成 `ParsedDocument` (text + tables + metadata)。本章讲解 `DocumentParser` 的多模态解析能力。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 从 PDF / DOCX / PPTX / HTML / Markdown / 代码文件抽出"正文 + 表格 + 元数据"。
- 选不同 parser: `DocumentParser` (默认) / `StructuredDataParser` / `CodeParser` / `WebParser` / `EmailParser`。
- 在 notebook 中通过 `framework.document_parser.parse(doc)` 调用。

### 1.2 一段最小可跑示例

```python
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser

docs = FileIngestor().ingest(["./docs/intro.pdf"])
parsed = DocumentParser().parse(docs[0])
print(parsed.text[:500])      # 纯文本
print(parsed.tables)           # DataFrame 列表
print(parsed.metadata)         # 标题 / 作者 / 页数 / 创建时间
```

### 1.3 何时不用

- **扫描版 PDF (图像)**: 用 `DocumentParser(ocr_engine="tesseract")`, 但需先装 `tesseract`。
- **超复杂表格**: 用 `docling` (extras `ingest-docling`)。
- **流式 XML**: 用 `StructuredDataParser` 显式指定 schema。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.parse.DocumentParser()          # 默认多模态解析器
semantica.parse.StructuredDataParser()    # CSV / Excel / Parquet
semantica.parse.CodeParser()              # 50+ 编程语言
semantica.parse.WebParser()               # HTML + boilerplate 去除
semantica.parse.EmailParser()             # EML / MBOX
semantica.parse.PDFParser(ocr_engine=...) # PDF 含 OCR
```

### 2.2 关键代码路径

- `semantica/parse/document_parser.py` — `DocumentParser.parse(SourceDocument) -> ParsedDocument`。
- `semantica/parse/structured_data_parser.py` — 表格型。
- `semantica/parse/code_parser.py` — 基于 tree-sitter / pygments。
- `semantica/parse/web_parser.py` — 基于 trafilatura / BeautifulSoup。
- `semantica/parse/email_parser.py` — email / mailbox 库。

### 2.3 最小复现脚本

```python
# examples/ch-09-parse-minimal.py mirror
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser, CodeParser

# 文档
docs = FileIngestor().ingest(["./README.md"])
parsed = DocumentParser().parse(docs[0])
print(f"text len={len(parsed.text)} tables={len(parsed.tables)}")

# 代码
code_docs = FileIngestor().ingest(["./semantica/__init__.py"])
code = CodeParser(language="python").parse(code_docs[0])
print(f"functions={len(code.functions)} classes={len(code.classes)}")
```

### 2.4 扩展点

- **加新格式**: 继承 `BaseParser.parse(SourceDocument) -> ParsedDocument`, 在 `parser_factory` 注册。
- **加新 OCR 引擎**: 扩展 `PDFParser.ocr_engine` 字段, 注入自己的 `tesseract` / `paddleocr` 包装。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 Parse 与 Ingest 拆开?**
- Ingest 关心"如何拿到字节", Parse 关心"如何理解字节"。两者演进节奏不同 (Ingest 受传输协议影响, Parse 受格式影响)。
- 拆开后, 用户可"用 Ingest 但自定义 Parse" (例如从 S3 拉一个我没特殊适配的格式)。

### 3.2 与同类对比

| 维度 | Semantica parse | Unstructured.io | LlamaIndex Readers |
|---|---|---|---|
| 格式数 | ~15 | ~30 | ~50 (含数据源) |
| OCR 内置 | ✅ (tesseract) | ✅ (多引擎) | ⚠ 仅文档型 |
| 代码解析 | ✅ (50+ 语言) | ❌ | ⚠ |

### 3.3 何时重新设计

- 格式种类 > 30 → 拆 `parse-document` / `parse-structured` / `parse-code` 子包。
- 用户自定义 parser 数 > 100 → 提供 `parser_decorator` 自动注册。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-08-ingest]]
- 下一章: [[ch-10-normalize]]
- 数据流位置: [[ch-04-architecture-30kft]] FIG-02 时序图第 4 步