---
title: 推理引擎 (Reasoning) — Rete + Datalog + SPARQL
slug: ch-16-reasoning
part: part-ii-core-modules
audience: all
reading_time: 13
prerequisites: [ch-15-ontology]
semantica_version: 0.6.0
---

# ch-16 推理引擎 (Reasoning)

> 基于已有 KG + ontology 做演绎 / 溯因 / 时序推理。本章讲解 Rete / Datalog / SPARQL / 解释生成 五大引擎。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 加规则 (Rete) 自动推导新事实: `grandparent(X, Z) :- parent(X, Y), parent(Y, Z)`。
- 跑 Datalog 查询 / SPARQL 查询。
- 演绎推理 (deductive) 与溯因推理 (abductive)。
- 时序推理 (valid_time + recorded_at 双时态)。
- 生成解释 (ExplanationGenerator) — 让"为什么"可追溯。

### 1.2 一段最小可跑示例

```python
from semantica.reasoning import Reasoner, DatalogReasoner, ExplanationGenerator

# 规则推理
r = Reasoner()
r.add_rule("grandparent(X, Z) :- parent(X, Y), parent(Y, Z).")
r.add_fact("parent", "alice", "bob")
r.add_fact("parent", "bob", "carol")
r.infer_facts()
print(r.query("grandparent(alice, Z)"))  # [Z=carol]

# Datalog 查询
d = DatalogReasoner()
d.load_from_graph(knowledge_graph)
print(d.query("path(X, Y) :- edge(X, Z), edge(Z, Y)."))

# 解释
ex = ExplanationGenerator(r)
print(ex.explain("grandparent(alice, carol)"))
```

### 1.3 何时不用

- 你不需要规则推导 → 用更简单的 Cypher / SPARQL 查询。
- 你的规则数 > 100k → 考虑 Drools / Clara 工业规则引擎。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.reasoning.Reasoner()                # 高层 facade
semantica.reasoning.GraphReasoner()
semantica.reasoning.ReteEngine()              # Rete 算法
semantica.reasoning.DatalogReasoner()         # Datalog
semantica.reasoning.SPARQLReasoner()
semantica.reasoning.ExplanationGenerator(reasoner)
semantica.reasoning.AbductiveReasoner()
semantica.reasoning.DeductiveReasoner()
semantica.reasoning.TemporalReasoningEngine()
```

### 2.2 关键代码路径

- `semantica/reasoning/reasoner.py:57` — `Reasoner` 主类。
- `semantica/reasoning/reasoner.py:149` — `infer_facts`。
- `semantica/reasoning/reasoner.py:204` — `forward_chain`。
- `semantica/reasoning/reasoner.py:271` — `backward_chain`。
- `semantica/reasoning/rete_engine.py:120` — `ReteEngine.build_network(rules)`。
- `semantica/reasoning/datalog_reasoner.py:39` — `DatalogReasoner`。
- `semantica/reasoning/datalog_reasoner.py:242` — `derive_all`。
- `semantica/reasoning/datalog_reasoner.py:344` — `query`。
- `semantica/reasoning/datalog_reasoner.py:404` — `load_from_graph`。
- `semantica/reasoning/sparql_reasoner.py` — SPARQL endpoint 适配。
- `semantica/reasoning/abductive_reasoner.py` — 反向假设生成。
- `semantica/reasoning/deductive_reasoner.py` — 前向规则链。
- `semantica/reasoning/temporal_reasoning.py` — 双时态推理。
- `semantica/reasoning/graph_reasoner.py` — 基于图遍历的路径推理。

### 2.3 最小复现脚本

```python
# examples/ch-16-reasoning-minimal.py mirror
from semantica.reasoning import Reasoner

r = Reasoner()
r.add_fact("parent", "alice", "bob")
r.add_fact("parent", "bob", "carol")
r.add_rule("grandparent(X, Z) :- parent(X, Y), parent(Y, Z).")
r.infer_facts()
print("grandparents:", r.query("grandparent(X, Y)"))
```

### 2.4 扩展点

- **加新规则语言**: 在 `ReteEngine._rule_parser` 加分支 (Datalog / Prolog / Jess 语法)。
- **加新解释格式**: 在 `ExplanationGenerator` 加 `_format_method`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 5 个引擎而不是 1 个?**
- 不同推理范式适用场景不同: 规则 (确定性, 业务) vs SPARQL (语义, 异构) vs 路径 (动态)。
- 拆开后允许按需激活, 不必强求"什么都能用一个引擎"。

### 3.2 与同类对比

| 维度 | Semantica reasoning | Drools | Jena |
|---|---|---|---|
| 范式数 | 5 (Rete/Datalog/SPARQL/演绎/溯因/时序) | 1 (Drools 规则) | 1 (SPARQL/RDF) |
| 解释生成 | ✅ 内置 | ⚠ audit log | ⚠ 弱 |
| 时序 | ✅ 双时态 | ❌ | ❌ |

### 3.3 何时重新设计

- 规则数 > 10k → 引入 Rete 网络分片。
- 出现跨图推理 → 引入联邦推理 (federated reasoning)。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-15-ontology]]
- 下一章: [[ch-17-vector-store]]