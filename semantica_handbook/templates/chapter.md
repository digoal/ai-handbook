---
title: <章节标题>
slug: ch-NN-slug
part: <part-i ~ part-vii>
audience: all | primary | developer | architect
reading_time: <分钟>
prerequisites: [ch-NN-slug, ...]
semantica_version: 0.6.0
---

# <章节中文标题>

> 一句话导语: 用一句话点出本章解决什么问题 / 解决到什么程度。

## 1. 用户视角(User)

[站在"我要用它做什么"的视角, 5-9 步可跑通示例, 子项列表、可复制命令、截图占位、典型场景。不展开 API。]

### 1.1 我能用它做什么
- ...
- ...

### 1.2 一段最小可跑示例
```bash
# 安装 + 启动 + 第一个可见结果
```

```python
# 5-9 行 Python
```

[图位: assets/images/ch-NN-*.png 或 FIG-NN 引用]

### 1.3 常见坑 / 何时不用
- ...
- ...

## 2. 开发者视角(Developer)

[站在"我要改它/集成它"的视角: API、类、方法签名、调用路径、扩展点、最小修改示例。代码块、API 表、step-by-step。]

### 2.1 公开 API 表
| API | 签名 | 返回 | 异常 |
|---|---|---|---|
| `xxx.yyy(...)` | `(arg: Type) -> Return` | `{...}` | `ValidationError` |

### 2.2 关键代码路径
- `semantica/<pkg>/<file>.py:LINENO` — 关键类/方法
- ...

### 2.3 最小复现脚本
```python
# handbook/examples/ch-NN-*.py mirror
```

### 2.4 扩展点
- 想加 X, 改 `semantica/<pkg>/<file>.py`
- ...

## 3. 架构师视角(Architect)

[站在"它为什么这样设计"的视角: 设计取舍、扩展边界、与同类系统对比、ADR 片段、Trade-offs。决策矩阵、ADR、扩展点列举。]

### 3.1 设计取舍
- 选了 A 而不是 B, 因为 ...
- 代价是 ...

### 3.2 与同类对比
| 维度 | Semantica | 对手 X | 对手 Y |
|---|---|---|---|
| ... | ... | ... | ... |

### 3.3 何时重新设计
- 当 X 增长到 Y 阈值时, 应该考虑 ...

## 本章图表

### FIG-NN <图名>
```mermaid
[Mermaid 源码]
```
图说: 一句话点明本图意图。

## 跨章引用
- 前置章节: [[ch-NN-slug]]
- 同卷章节: [[ch-NN-slug]]
- 相关图表: [[fig-NN]]