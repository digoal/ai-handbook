---
title: 上下文与决策智能 (Context & Decision)
slug: ch-21-context-decision
part: part-ii-core-modules
audience: all
reading_time: 16
prerequisites: [ch-20-provenance, ch-14-knowledge-graph]
semantica_version: 0.6.0
---

# ch-21 上下文与决策智能 (Context & Decision)

> 把 AI 决策当成图节点, 串成因果链, 让每一笔决策可解释可审计。本章讲解 `ContextGraph [[ch-55-glossary]] / AgentContext / DecisionRecorder / PolicyEngine` 四件套。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 记录决策: `record_decision(category, scenario, reasoning, outcome, confidence, ...)`。
- 因果链: `add_causal_relationship(d1, "caused/enabled/preceded", d2)`。
- 检索判例: `find_similar_decisions(d_id, top_k)` (基于 reasoning 嵌入)。
- 策略闸门: `check_decision_rules(c, [policy_ids])` → 合规/拒绝/需复核。
- 决策追溯: `trace_decision_chain(d_id)` 输出 mermaid 序列。
- 决策图导出: W3C PROV-O Turtle / JSON。

### 1.2 一段最小可跑示例

```python
# A) module-level 函数 (无需 ContextGraph)
from semantica.context.decision_methods import (
    record_decision,           # 记录一笔决策 (返回 dict 含 id)
    find_precedents,           # 找历史判例
    capture_decision_trace,    # 导出 PROV-O
    create_policy_with_versioning,  # 创建策略
    check_decision_compliance, # 决策合规闸门
)

# B) ContextGraph 实例方法 (需先拿 cg)
from semantica.context.context_graph import ContextGraph
cg = ContextGraph()

# 1) 记录决策
d1 = record_decision(
    category="credit_approval",
    scenario="Acme Corp 申请 100 万美元短期贷款",
    reasoning="过去 36 个月无违约, 营收稳定增长",
    outcome={"approved": True, "amount": 1_000_000},
    confidence=0.92,
    decided_by="analyst@bank.com",
)

d2 = record_decision(
    category="credit_approval",
    scenario="Acme Corp 申请长期贷款 200 万美元",
    reasoning="基于 d1 良好信用记录, 扩大授信",
    outcome={"approved": True, "amount": 2_000_000},
    confidence=0.85,
    decided_by="analyst@bank.com",
)

# 2) 因果链 — ContextGraph 实例方法 (语义: Decision 节点之间的边)
cg.add_causal_relationship(d1["id"], "enabled", d2["id"])

# 3) 决策图上做溯源查询 — 也是实例方法
chain = cg.trace_decision_chain(d2["id"])
gate = cg.check_decision_rules(d2["id"], policy_ids=["pol-high-value"])

# 4) 把决策链导出成 mermaid 文本
mermaid = cg.trace_decision_chain(d2["id"], format="mermaid")
print(mermaid)
```

> 关键区别: `record_decision / find_precedents / capture_decision_trace` 是 module-level 函数(无状态、单次调用); `add_causal_relationship / trace_decision_chain / check_decision_rules` 是 `ContextGraph` 实例方法(需要先 `cg = ContextGraph()`)。

### 1.3 何时不用

- 你不需要决策审计 → 直接用 LLM + RAG。
- 你不需要跨决策因果链 → 用普通 KG 即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
# A) module-level 函数 (semantica.context.decision_methods)
semantica.context.decision_methods.record_decision(...)
semantica.context.decision_methods.find_precedents(...)
semantica.context.decision_methods.capture_decision_trace(...)
semantica.context.decision_methods.create_policy_with_versioning(...)
semantica.context.decision_methods.check_decision_compliance(...)
semantica.context.decision_methods.setup_decision_tracking(...)
semantica.context.decision_methods.enhance_agent_context_with_decisions(...)
semantica.context.decision_methods.get_decision_statistics(...)

# B) ContextGraph 实例方法 (semantica.context.context_graph)
semantica.context.context_graph.ContextGraph()
semantica.context.context_graph.ContextGraph.add_causal_relationship(...)     # ~ :2005
semantica.context.context_graph.ContextGraph.trace_decision_chain(...)        # ~ :3326
semantica.context.context_graph.ContextGraph.check_decision_rules(...)         # ~ :3346
semantica.context.context_graph.ContextGraph.find_similar_decisions(...)        # 见 DecisionQuery
semantica.context.context_graph.ContextGraph.multi_hop_query(...)
semantica.context.context_graph.ContextGraph.get_causal_chain(...)
semantica.context.context_graph.ContextGraph.get_applicable_policies(...)

# C) 类与数据结构
semantica.context.AgentContext(context_graph)
semantica.context.DecisionRecorder()
semantica.context.DecisionQuery()                  #  :213 (find_similar_decisions)
semantica.context.CausalChainAnalyzer()
semantica.context.policy_engine.PolicyEngine()
semantica.context.decision_models.Decision
semantica.context.decision_models.Policy
semantica.context.decision_models.Precedent
```

### 2.2 关键代码路径

#### module-level 函数 (`decision_methods.py`)

- `semantica/context/decision_methods.py:23` — `record_decision`。
- `semantica/context/decision_methods.py:87` — `find_precedents`。
- `semantica/context/decision_methods.py:218` — `capture_decision_trace`。
- `semantica/context/decision_methods.py:650` — `create_policy_with_versioning`。
- `semantica/context/decision_methods.py:698` — `check_decision_compliance`。
- `semantica/context/decision_methods.py:840` — `setup_decision_tracking`。
- `semantica/context/decision_methods.py:879` — `enhance_agent_context_with_decisions`。

#### ContextGraph 实例方法 (`context_graph.py`)

- `semantica/context/context_graph.py:2005` — `add_causal_relationship(source_id, type, target_id)`。
- `semantica/context/context_graph.py:3326` — `trace_decision_chain(decision_id)`。
- `semantica/context/context_graph.py:3346` — `check_decision_rules(decision_id, policy_ids)`。

#### DecisionQuery 类

- `semantica/context/decision_query.py:67` — `find_similar_decisions` (基于 reasoning 嵌入余弦相似度)。

#### 决策模型

- `semantica/context/decision_models.py` — `Decision / Policy / Precedent / PolicyException / ApprovalChain` dataclass。
- `semantica/context/decision_methods.py:879` — `enhance_agent_context_with_decisions`。
- `semantica/context/decision_models.py` — `Decision / Policy / Precedent / PolicyException / ApprovalChain`。
- `semantica/context/context_graph.py` — `ContextGraph` (内存图)。
- `semantica/context/policy_engine.py` — `PolicyEngine`。

### 2.3 最小复现脚本

```python
# examples/ch-21-decision-minimal.py mirror
from semantica.context.decision_methods import (
    record_decision, add_causal_relationship, trace_decision_chain,
)

d1 = record_decision(category="demo", scenario="x", reasoning="y",
                     outcome={"ok": True}, confidence=0.9, decided_by="me")
d2 = record_decision(category="demo", scenario="x2", reasoning="y2",
                     outcome={"ok": True}, confidence=0.8, decided_by="me")
add_causal_relationship(d1["id"], "caused", d2["id"])
print(trace_decision_chain(d2["id"], format="mermaid"))
```

### 2.4 扩展点

- **加新决策类别**: 在 `Decision.category` 加值, 注册到 `DecisionRecorder._category_policies`。
- **加新因果类型**: 扩 `add_causal_relationship(type=...)` 支持新谓词 (e.g., "precedent_for")。
- **加新策略语言**: 扩 `Policy.rule` 支持 CEL / JSONLogic / 自定义 DSL。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么决策图与 KG 共享 ContextGraph?**
- 决策节点 (Decision) 与实体节点 (Entity) 在同一张图上, 可以互相建关系 (如 "decision.d2 cites entity.e1")。
- 共用图遍历 / 嵌入 / 检索基础设施, 减少双写。
- 代价: 决策语义与实体语义混在同张图, 需 schema 区分 (Decision.label = "decision")。

**为什么 `decision_methods.py` 而不是 `decision/` 子包?**
- 决策模块在 v0.4 才出现, 当时希望小步快跑, 用一个 878 行 facade 文件而非 10+ 类。
- 后续 v0.6 重构时考虑拆 `decision/` 子包。
- API 已稳定, 重构需保持向后兼容。

### 3.2 与同类对比

| 维度 | Semantica decision | LangSmith | Helicone |
|---|---|---|---|
| 决策记录 | ✅ 一等图节点 | ⚠ trace | ⚠ log |
| 因果链 | ✅ add_causal | ❌ | ❌ |
| 策略闸门 | ✅ check_decision_rules | ❌ | ❌ |
| 判例检索 | ✅ find_similar_decisions | ⚠ 弱 | ❌ |
| 导出 PROV-O | ✅ | ❌ | ❌ |

### 3.3 何时重新设计

- 决策数 > 10M → 必上独立 graph backend (Neo4j cluster)。
- 出现"实时决策" (sub-100ms) → 引入决策图缓存层。

## 本章图表

> 本章无 Mermaid 图。决策时序见 [[ch-42-flow-c-decision-intel]] FIG-08。

## 跨章引用

- 上一章: [[ch-20-provenance]]
- 下一章: [[ch-22-deduplication]]
- 决策主轴: [[ch-42-flow-c-decision-intel]]
- 与 Agent 集成: [[ch-38-agent-frameworks]]