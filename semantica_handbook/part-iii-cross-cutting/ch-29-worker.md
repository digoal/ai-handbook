---
title: Worker 任务模型 — 当前与未来
slug: ch-29-worker
part: part-iii-cross-cutting
audience: all
reading_time: 7
prerequisites: [ch-27-cli, ch-28-server-api]
semantica_version: 0.6.0
---

# ch-29 Worker 任务模型 — 当前与未来

> 当前 `worker.py` 是简化轮询骨架, 未来会接入 Redis / Celery / Kafka / Pulsar。本章讲解现状与扩展路径。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 当前: 启动后台进程做轮询, 准备好接外部队列。
- 启动方式: `semantica-worker` (entry-point)。
- 优雅关闭: 收到 SIGINT/SIGTERM 触发 `handle_exit`。

### 1.2 一段最小可跑示例

```bash
# 启动 (默认 5 秒轮询)
semantica-worker

# 优雅停止 (Ctrl-C 或 SIGTERM)
# 打印 "Shutting down worker..."
```

### 1.3 何时不用

- 你已有消息队列 → 直接接入 Celery / RQ, 不必用 Semantica worker。
- 单进程够用 → 直接 `python -m semantica.worker`。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.worker.SemanticaWorker()        # 主类
semantica.worker.main()                    # entry point
semantica.worker.handle_exit(signum, frame)  # SIGINT/SIGTERM 钩子
semantica.worker.run()                     # 轮询主循环 (内部使用)
```

### 2.2 关键代码路径

- `semantica/worker.py:18` — `SemanticaWorker` 类 (含 `framework = Semantica()`)。
- `semantica/worker.py:34` — `run()` 轮询循环 (`time.sleep(5)`, 错误时 `time.sleep(10)`)。
- `semantica/worker.py` — `signal.signal(SIGINT/SIGTERM, handle_exit)`。
- `pyproject.toml:entry-points` — `semantica-worker = "semantica.worker:main"`。
- `pyproject.toml:[project.optional-dependencies] infra` — `kafka-python / pulsar-client / pika / celery` 队列依赖 (未安装时不报错, 仅 worker 不工作)。

### 2.3 最小复现脚本

```python
# examples/ch-29-worker-mock.py mirror
import os
os.environ.setdefault("SEMANTICA_LOGGING__LEVEL", "INFO")

from semantica.worker import SemanticaWorker

w = SemanticaWorker()
# w.run()  # 阻塞轮询, 仅在测试时 break
print("worker ready (state):", w.framework.lifecycle_manager.get_state())
w.framework.shutdown()
```

### 2.4 扩展点

- **接 Celery**: 在 `worker.py:run` 替换为 Celery `app.task` 注册, broker 走 Redis/RabbitMQ/SQS。
- **接 Kafka**: 用 `aiokafka` 替换 `time.sleep`, 走 consumer loop; topic 与 `semantica.framework.ingest.kafka_ingest` 配对。
- **接 Redis Stream**: 用 `redis.asyncio` 替换; 适合"低延迟 + 已有 Redis 栈"场景。
- **接 RabbitMQ (pika)**: 用 `pika.SelectConnection` 替换, 适合传统企业 AMQP 协议。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么当前是 stub?**
- v0.6 优先做框架核心, worker 故意留 stub, 让用户按业务选队列。
- 一旦默认实现写死 (比如 Celery), 用户迁移成本高。

### 3.2 与同类对比

| 维度 | Semantica worker | Celery | Dramatiq | RQ |
|---|---|---|---|---|
| Broker 抽象 | 无 (stub) | Redis / RabbitMQ / SQS | Redis / RabbitMQ | Redis |
| 任务签名 | N/A | `@app.task` | `@dramatiq.actor` | `@job` |
| 重试 / 死信 | N/A | ✅ | ✅ | ⚠ |

### 3.3 何时重新设计

- 用户开始抱怨"为什么 worker 不工作" → 至少落一个 Celery 实现。
- 出现"实时任务"需求 → 引入 Dramatiq / arq。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-28-server-api]]
- 下一章: [[ch-30-mcp-server]]
- 部署 worker: [[ch-44-k8s-helm]]