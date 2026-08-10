---
title: 故障排查 — 按错误码 / 症状索引
slug: ch-53-troubleshooting
part: part-vii-reference
audience: all
reading_time: 9
prerequisites: [ch-32-lifecycle-errors-config]
semantica_version: 0.6.0
---

# ch-53 故障排查 — 按错误码 / 症状索引

> 本章按"错误码 + 症状"双维度索引常见故障与解决。

## 1. 用户视角(User)

### 1.1 按错误码

| 错误码 | 含义 | 常见原因 | 解决 |
|---|---|---|---|
| **SEM001** | `ValidationError` | 字段缺失 / 越界 | 检查 input schema |
| **SEM001T** | `TemporalValidationError` | 时间冲突 | 用 `BiTemporalFact` 而非 datetime |
| **SEM002** | `ProcessingError` | pipeline 步骤失败 | 查看 traceback |
| **SEM003** | `ConfigurationError [[ch-55-glossary]]` | config 校验失败 | `semantica doctor` 看详细 |
| **SEM004** | `QualityError` | 置信度低于阈值 | 调 `quality.min_confidence` |

### 1.2 按症状

| 症状 | 可能原因 | 第一动作 |
|---|---|---|
| **安装失败** | Python < 3.8 / 网络问题 | `python --version` ≥ 3.8 |
| **`semantica doctor` 红** | LLM key 缺失 / 图库不可达 | 看 doctor 输出 |
| **build_knowledge_base 慢** | LLM 抽调用多 | 改用 `extract_entities_huggingface` |
| **KG 节点数 < 预期** | LLM schema 不匹配 | 检查 `semantic_extract.default_schema` |
| **Neo4j 连接超时** | 防火墙 / 端口 | `bolt://localhost:7687` + 7687 端口开 |
| **FalkorDB 报 "OOM"** | 数据 > 内存 | 升 Redis 实例规格 |
| **OpenAI 401** | key 过期 | `echo $OPENAI_API_KEY` 验证 |
| **Anthropic 429** | RPM 超限 | 调 `processing.batch_size` 或加退避 |
| **PDF 解析空** | 扫描版无 OCR | `DocumentParser(ocr_engine="tesseract")` |
| **WebIngestor 403** | robots 拒绝 | 显式 `respect_robots=False` (谨慎) |
| **Explorer WS 断** | heartbeat 失效 | 重启 explorer |
| **MCP 工具超时** | LLM 慢 | 调 LLM provider 或 chunk 大小 |

### 1.3 一段最小可跑示例

```bash
# 1) 全面自检
semantica doctor

# 2) 看最近日志
semantica info --log-level DEBUG 2>&1 | tail -50

# 3) 跑核心冒烟
semantica kg build --sources ./README.md --dry-run

# 4) 测连接 (Neo4j)
python -c "
from semantica.graph_store import GraphStore [[ch-55-glossary]]
gs = GraphStore(backend='neo4j', uri='bolt://localhost:7687', user='neo4j', password='password')
print('connected:', gs.health_check())
"
```

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/utils/exceptions.py:49` — `SemanticaError` 基类 (含 `to_dict()`)。
- `semantica/utils/exceptions.py:122` — `ValidationError` (SEM001)。
- `semantica/utils/exceptions.py:155` — `TemporalValidationError` (SEM001T)。
- `semantica/utils/exceptions.py:182` — `ProcessingError` (SEM002)。
- `semantica/utils/exceptions.py:215` — `ConfigurationError` (SEM003)。
- `semantica/utils/exceptions.py:248` — `QualityError` (SEM004)。
- `semantica/utils/exceptions.py:281` — `handle_exception`。
- `semantica/utils/exceptions.py:346` — `format_exception`。
- `semantica/cli.py:776` — `doctor` 子命令。
- `semantica/utils/progress_tracker.py` — 错误时回滚进度条。

### 2.2 最小复现脚本

```python
# examples/ch-53-err-catch.py mirror
from semantica.utils.exceptions import (
    SemanticaError, ValidationError, ProcessingError,
    ConfigurationError, QualityError,
)

try:
    Semantica({"processing": {"batch_size": -1}})
except ConfigurationError as e:
    print(f"SEM003 caught: {e} (context={e.context})")
except SemanticaError as e:
    print(f"Other Semantica error: {e.error_code}")
except Exception as e:
    print(f"Unexpected: {type(e).__name__}: {e}")
```

### 2.3 已知陷阱

- **`SemanticaError` 不是 `Exception` 子类**: 实际是 (Python 内置), 但 `except Exception` 能捕获。
- **`error_code` 在 v0.6 后稳定**: 老版本只有 message, 新版本才有 code。
- **ValidationError 聚合**: `Config.validate()` 会把所有错误聚合为 1 个 `ConfigurationError`, 在 `context["errors"]` 列出全部。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么错误码用 "SEM00X" 而非数字?**
- 字符串带语义 (SEM00 = SEmantica, 1/2/3/4 = 子类)。
- 便于日志聚合 (Datadog / Loki 可按 code 分桶)。

**为什么 `ConfigurationError` 聚合而非首个?**
- 用户配错 5 个字段, 看到 1 个修了还有 4 个, 太烦。
- 一次性看到全部, 改一轮到位。

### 3.2 与同类对比

| 维度 | Semantica 异常体系 | LangChain | LlamaIndex |
|---|---|---|---|
| 错误码 | ✅ SEM001-005 | ❌ | ❌ |
| 聚合 | ✅ ConfigurationError | ⚠ | ❌ |
| 上下文 dict | ✅ `context` | ⚠ | ⚠ |

### 3.3 何时重新设计

- 错误码 > 20 → 引入"错误族" (Error family) + 子编码。
- 出现"国际化错误消息" → i18n 字符串。

## 跨章引用

- 上一章: [[ch-52-contributing]]
- 下一章: [[ch-54-faq]]