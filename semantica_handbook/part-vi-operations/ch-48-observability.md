---
title: 可观测性 — 日志 / 指标 / 追踪
slug: ch-48-observability
part: part-vi-operations
audience: all
reading_time: 8
prerequisites: [ch-32-lifecycle-errors-config]
semantica_version: 0.6.0
---

# ch-48 可观测性 — 日志 / 指标 / 追踪

> Semantica 通过 `utils/logging` (loguru + structlog) + `utils/progress_tracker` (560 行) + LifecycleManager.get_health_summary() 提供可观测性。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 结构化日志: 每条 log 含 `timestamp / level / module / message`。
- 进度跟踪: CLI 自动启用, 长操作显示阶段 + 进度条。
- 健康检查: `fw.get_status() -> {state, health, modules, plugins, config}`。
- 错误码: 5 类异常带 `error_code` (SEM001-005), 便于日志聚合。

### 1.2 一段最小可跑示例

```bash
# 启用 DEBUG 日志
export SEMANTICA_LOGGING__LEVEL=DEBUG

# JSON 输出给日志聚合 (Datadog/Loki)
export SEMANTICA_LOGGING__FORMAT=json

# 跑一次, 看到完整日志
semantica kg build --sources ./docs/intro.pdf
```

### 1.3 何时不用

- 你已有 OpenTelemetry → 在 FastAPI middleware 加 OTLP exporter。
- 你只要 print → 用 `from semantica.utils.logging import get_logger; log = get_logger(__name__); log.info("hi")`。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.utils.logging.get_logger(name)
semantica.utils.logging.log_execution_time
semantica.utils.progress_tracker.get_progress_tracker()
semantica.utils.progress_tracker.ProgressTracker()
semantica.core.Semantica.get_status()
semantica.core.LifecycleManager.get_health_summary()
semantica.core.LifecycleManager.health_check()
```

### 2.2 关键代码路径

- `semantica/utils/logging.py` — loguru + structlog 双后端 + 自定义 formatters。
- `semantica/utils/progress_tracker.py:560` — `ProgressTracker`。
- `semantica/core/lifecycle.py:317` — `health_check()`。
- `semantica/core/lifecycle.py:530` — `get_health_summary()`。

### 2.3 最小复现脚本

```python
# examples/ch-48-obs.py mirror
from semantica import Semantica
from semantica.utils.logging import get_logger

log = get_logger("ch-48")
fw = Semantica()
try:
    log.info("starting build")
    fw.build_knowledge_base(sources=["./README.md"], graph=True)
    log.info("status", extra=fw.get_status())
finally:
    fw.shutdown()
```

### 2.4 已知陷阱

- **loguru 与 stdlib logging 冲突**: 避免在第三方库中混用。
- **JSON 格式在 CLI 中不可读**: 用户场景用 pretty, CI 场景用 JSON。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么不用 OpenTelemetry?**
- OTEL 强制 SDK 依赖 (~20 MB), 与 Semantica "extras 化" 不符。
- loguru + structlog 给 90% 用户够用, OTEL 用户可加 middleware。

**为什么 progress_tracker 是全局单例?**
- CLI 启动时启用, 所有模块共享一个进度条, 避免"双重进度条"。

### 3.2 与同类对比

| 维度 | Semantica 可观测性 | LangSmith | LlamaIndex Observability |
|---|---|---|---|
| 内置 logger | ✅ loguru+structlog | ❌ | ⚠ |
| 进度条 | ✅ | ❌ | ❌ |
| 健康检查 | ✅ | ⚠ | ❌ |

### 3.3 何时重新设计

- 日志量 > 1GB/天 → 切 OTEL + sampling。

## 跨章引用

- 上一章: [[ch-47-performance-benchmark]]
- 下一章: [[ch-49-security]]