---
title: Semantica 错误码全集
slug: error-codes
part: part-vii-reference
audience: all
reading_time: 5
prerequisites: []
semantica_version: 0.6.0
---

# Semantica 错误码全集

> 错误码在 v0.6 引入并稳定。`semantica/utils/exceptions.py` 是单一权威源, 本文档是检索入口。

## 错误码表

| 错误码 | 异常类 | 触发场景 | 详见 |
|---|---|---|---|
| **SEM001** | `ValidationError` | 字段缺失 / 越界 / schema 不匹配 | [[ch-32-lifecycle-errors-config]] §3.2 |
| **SEM001T** | `TemporalValidationError` | 时间冲突 (valid_time / recorded_at) | [[ch-25-change-management]] §时序小节 |
| **SEM002** | `ProcessingError` | pipeline 步骤失败 | [[ch-24-pipeline]] §3.3 |
| **SEM003** | `ConfigurationError` | config 校验失败 (聚合所有错误) | [[ch-07-configuration-primer]] §3.2 |
| **SEM004** | `QualityError` | 置信度低于 `quality.min_confidence` | [[ch-21-context-decision]] §3.3 |
| SEM005 | (预留) | (v0.7 计划: 资源/限流) | - |

## 按异常类查询

### `SemanticaError` (基类, SEM000)

```python
class SemanticaError(Exception):
    error_code: str = "SEM000"
    context: dict[str, Any] = {}
    def to_dict(self) -> dict: ...
```

- 始终有 `error_code` 字段 (默认 "SEM000")。
- 始终有 `context` 字段, 携带上下文 (e.g., `{"field": "batch_size", "value": -1}`)。
- `to_dict()` 可序列化, 配合日志聚合 (Datadog / Loki) 用。

### 5 个子类

| 子类 | 错误码 | 行号 (`utils/exceptions.py`) |
|---|---|---|
| `ValidationError` | SEM001 | 122 |
| `TemporalValidationError` | SEM001T | 155 |
| `ProcessingError` | SEM002 | 182 |
| `ConfigurationError` | SEM003 | 215 |
| `QualityError` | SEM004 | 248 |

## 捕获示例

```python
from semantica.utils.exceptions import (
    SemanticaError, ValidationError, ProcessingError,
    ConfigurationError, QualityError, TemporalValidationError,
)

try:
    Semantica({"processing": {"batch_size": -1}})
except ValidationError as e:
    print(f"SEM001: {e} (field={e.context.get('field')})")
except ConfigurationError as e:
    print(f"SEM003: {e} (聚合 {len(e.context.get('errors', []))} 条)")
except SemanticaError as e:
    print(f"{e.error_code}: {e}")
except Exception as e:
    print(f"unexpected: {type(e).__name__}: {e}")
```

## 检索入口

- 完整异常族: `semantica/utils/exceptions.py:401`
- 故障排查按症状: [[ch-53-troubleshooting]]
- 错误体系架构: [[ch-32-lifecycle-errors-config]] §3

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-53-troubleshooting]]
- 异常体系: [[ch-32-lifecycle-errors-config]]
- 变更管理: [[ch-25-change-management]]