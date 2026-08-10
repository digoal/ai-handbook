---
title: 本体管理 (Ontology) — OWL + SHACL + SKOS
slug: ch-15-ontology
part: part-ii-core-modules
audience: all
reading_time: 12
prerequisites: [ch-14-knowledge-graph]
semantica_version: 0.6.0
---

# ch-15 本体管理 (Ontology)

> 给 KG 套上"业务约束": 类 / 属性 / 继承 / SHACL 校验 / SKOS 词表。本章讲解 22 个 ontology 文件的统一 facade。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 从 KG 自动生成 OWL 本体 (类 / 属性推断)。
- 写 SHACL Shapes 校验数据合规性 (例: "Person 必须有 birth_year")。
- 管理 SKOS 词表 (scheme / concept / hierarchy)。
- 本体对齐 (ontology alignment) — 找两个 ontology 间的等价类。

### 1.2 一段最小可跑示例

```python
from semantica.ontology import OntologyGenerator, OntologyValidator, OWLGenerator

# 1) 从 KG 自动生成本体
onto = OntologyGenerator().from_knowledge_graph(knowledge_graph)

# 2) 校验数据合规性
validator = OntologyValidator(shapes_path="./shapes.ttl")
report = validator.validate(entities, relationships)
print(report.conform, report.violations)

# 3) 导出 OWL
OWLGenerator().to_file(onto, "./ontology.ttl", format="turtle")
```

### 1.3 何时不用

- 你的图是纯无结构 (无业务约束) → 跳过 Ontology。
- 你已经有 Protégé 管理的本体 → 直接 import TTL 文件即可。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.ontology.OntologyGenerator()       # 6 阶段 pipeline
semantica.ontology.OntologyValidator(shapes_path)
semantica.ontology.OWLGenerator()
semantica.ontology.ClassInferrer()
semantica.ontology.PropertyGenerator()
semantica.ontology.Engine()
semantica.ontology.NamespaceManager()
semantica.ontology.DomainOntologies()
semantica.ontology.ReuseManager()
semantica.ontology.AssociativeClass [[ch-55-glossary]]()
semantica.ontology.CompetencyQuestions()
semantica.ontology.RequirementsSpec()
semantica.ontology.OntologyEvaluator()
semantica.ontology.OntologyDocumentation()
semantica.ontology.ontology_methods.ingest_ontology(...)
```

### 2.2 关键代码路径

- `semantica/ontology/ontology_generator.py` — 6 阶段 pipeline (extract → normalize → infer → validate → align → document)。
- `semantica/ontology/ontology_validator.py` — 基于 `pyshacl` (extras `shacl`)。
- `semantica/ontology/owl_generator.py` — 输出 RDF/XML / Turtle / JSON-LD。
- `semantica/ontology/class_inferrer.py` — 基于图结构推断类层次。
- `semantica/ontology/property_generator.py` — 自动生成 OWL property。
- `semantica/ontology/methods.py:179` — `ingest_ontology` facade。
- `semantica/ontology/methods.py:169-174` — `get_ontology_method / list_available_methods`。

### 2.3 最小复现脚本

```python
# examples/ch-15-ontology-minimal.py mirror
from semantica.ontology import OntologyGenerator

kg = ...  # 假设有 KG
onto = OntologyGenerator().from_knowledge_graph(kg)
print(f"Classes: {len(onto.classes)}  ObjectProperties: {len(onto.object_properties)}")
```

### 2.4 扩展点

- **加新推理器**: 继承 `BaseReasoner`, 注入 `Engine.inferencer`。
- **加 SHACL 自定义函数**: 用 `sh:JS` / `sh:SPARQL` 自定义约束。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 ontology 与 KG 拆开?**
- KG 是"实例数据", ontology 是"模式约束"。两者演进节奏不同 (ontology 稳定, KG 频繁)。
- 拆开后允许: 同一份 ontology 跨多 KG 复用, 同一 KG 跨多 ontology 验证。

### 3.2 与同类对比

| 维度 | Semantica ontology | Protégé (手动) | Owlready2 |
|---|---|---|---|
| 自动生成 | ✅ 6 阶段 | ❌ 手工 | ⚠ 半自动 |
| SHACL 校验 | ✅ | ⚠ 插件 | ❌ |
| SKOS | ✅ | ⚠ 插件 | ❌ |

### 3.3 何时重新设计

- 本体数 > 50 → 引入 ontology module 化 (docket / module URI)。
- SHACL shapes > 200 → 引入 shapes 模板 (`sh:NodeShape` + `sh:property` 复用)。

## 本章图表

> 本章无 Mermaid 图。

## 跨章引用

- 上一章: [[ch-14-knowledge-graph]]
- 下一章: [[ch-16-reasoning]]
- RDF 存储: [[ch-19-triplet-store]]
- 数据流位置: [[ch-04-architecture-30kft]] FIG-02 步骤后