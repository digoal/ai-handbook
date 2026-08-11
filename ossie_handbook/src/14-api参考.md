<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
-->

# 第 14 章 · API 参考手册

> **Abstract** — A consolidated reference for the three public surfaces of the Ossie stack: (1) the **Python SDK** (`apache-ossie`, 13 Pydantic v2 model classes plus 3 enums, all exported from `python/src/ossie/__init__.py`); (2) the **Go CLI** (`ossie`, Cobra-based, 7 commands — only `plugin list` fully implemented; `convert`, `validate`, `plugin install`, `plugin remove` are stubs); (3) the **vendor converter CLIs** (11 entries — 5 Python converters with `cli.py`, 4 Python converters as library-only, 2 Java converters with main classes). Each entry lists the entrypoint command, arguments, status, and a hand-curated example.

> **【为用户】** 当你记不清某个 converter 该传什么 flag、或者想知道 SDK 类的所有方法签名时，翻这一章。
>
> **【为开发者】** Python SDK 的所有公共类型（13 个 class + 3 个 enum + 2 个 helper）都在 §14.1 列全；Go CLI 的 7 个 cobra 命令都在 §14.2。**写新 converter 时，先看 §14.3 找最接近的模板克隆-修改**。
>
> **【为架构师】** Go CLI 是 thin dispatcher 设计——只有 `plugin list` 真正工作；其余 4 个命令都是 stub，统一通过 plugin IPC 协议调子进程。详见第 9 章 §9.5 IPC 协议（`cli/internal/plugin/invoke.go:13-83`）。

## 14.1 Python SDK（`apache-ossie`）

**包路径**：`python/src/ossie/`
**入口**：`from ossie import ...`（14 个公共类型，详见下表）
**模式**：Pydantic v2 + `frozen=True`（实例不可变）

### 14.1.1 顶层模型（5 个核心构造）

| 类 | 继承 | 关键字段 | 备注 |
|---|---|---|---|
| `OSIDocument` | `BaseModel` | `version`, `dialects?`, `vendors?`, `semantic_model` | **入口点**——`model_validate(dict)` 加载，`to_osi_yaml()` / `to_osi_json()` 导出 |
| `OSISemanticModel` | `BaseModel` | `name`, `datasets`, `relationships?`, `metrics?` | 一个文档可有多个 semantic model |
| `OSIDataset` | `BaseModel` | `name`, `source`, `primary_key?`, `unique_keys?`, `description?`, `fields?`, `custom_extensions?` | `source` 是 fqn (e.g. `catalog.schema.table`) |
| `OSIField` | `BaseModel` | `name`, `expression: OSIExpression`, `dimension?`, `label?`, `description?`, `datatype?`, `ai_context?`, `custom_extensions?` | 含方法 `is_time_dimension() -> bool` |
| `OSIRelationship` | `BaseModel` | `name`, `from_dataset` (alias `from`), `to`, `from_columns`, `to_columns` | `from` 是 Python 关键字 → 别名 |
| `OSIMetric` | `BaseModel` | `name`, `expression`, `datatype?`, `description?` | metric 不能跨 dataset 引用 field |

### 14.1.2 表达式与多方言（3 个类）

| 类 | 用途 |
|---|---|
| `OSIExpression` | 包装 `dialects: list[OSIDialectExpression]` |
| `OSIDialectExpression` | 单个方言：`dialect: OSIDialect` + `expression: str` |
| `OSIDimension` | 含 `is_time: bool?`（显式优先于 datatype 默认） |

### 14.1.3 三大枚举（7+10+8 = 25 个值）

| 枚举 | 值数 | 值列表 |
|---|---|---|
| `OSIDialect` | 7 | `ANSI_SQL`, `SNOWFLAKE`, `MDX`, `MAQL`, `TABLEAU`, `DATABRICKS`, `BIGQUERY` |
| `OSIDataType` | 10 | `String`, `Integer`, `Decimal`, `Float`, `Boolean`, `Date`, `Time`, `DateTime`, `DateTimeTz`, `Opaque` |
| `OSIVendor` | 8 | `COMMON`, `SNOWFLAKE`, `SALESFORCE`, `DBT`, `DATABRICKS`, `GOODDATA`, `SEMANTIDO`, `WISDOM` |

### 14.1.4 AI 上下文与扩展（3 个 helper）

| 类 | 字段 |
|---|---|
| `OSIAIContext` | wrapper for `OSIAIContextObject`（双形态：string 或 dict） |
| `OSIAIContextObject` | `instructions`, `synonyms`, `examples` |
| `OSICustomExtension` | `vendor_name: str`, `data: str`（任意 JSON 字符串） |

### 14.1.5 关键方法签名

```python
# 入口：YAML/JSON dict → OSS document
OSIDocument.model_validate(data: dict | str | bytes) -> OSIDocument
# ↑ Pydantic 自动校验；失败抛 pydantic.ValidationError

# 出口：OSSI document → 字节级一致 YAML/JSON
OSIDocument.to_osi_yaml(**kwargs) -> str
OSIDocument.to_osi_json(**kwargs) -> str
# ↑ 默认 by_alias=True, exclude_none=True, allow_unicode=True

# 字段辅助方法
OSIField.is_time_dimension() -> bool
# ↑ 显式 dimension.is_time 优先；否则从 datatype 推导（见 §2.4）

# 私有常量（不要直接 import）
_TEMPORAL_DATA_TYPES = frozenset({
    OSIDataType.DATE, OSIDataType.TIME,
    OSIDataType.DATE_TIME, OSIDataType.DATE_TIME_TZ,
})
# 但 converter 内部经常需要（见 §8.9）
```

### 14.1.6 完整工作流示例

```python
import yaml
from ossie import (
    OSIDocument, OSISemanticModel, OSIDataset, OSIField, OSIMetric,
    OSIExpression, OSIDialectExpression, OSIDataType, OSIDialect,
)

# 1. 加载
with open("model.yaml") as f:
    raw = yaml.safe_load(f)
doc = OSIDocument.model_validate(raw)

# 2. 遍历
for sm in doc.semantic_model:
    for ds in sm.datasets:
        for field in (ds.fields or []):
            print(f"{ds.name}.{field.name} | time={field.is_time_dimension()}")

# 3. 修改
doc.semantic_model[0].metrics = (
    doc.semantic_model[0].metrics or []
) + [
    OSIMetric(
        name="new_metric",
        expression=OSIExpression(dialects=[
            OSIDialectExpression(
                dialect=OSIDialect.ANSI_SQL,
                expression="SUM(orders.amount)",
            )
        ]),
        datatype=OSIDataType.DECIMAL,
    )
]

# 4. 写出
print(doc.to_osi_yaml())
```

## 14.2 Go CLI（`ossie`）

**源码**：`cli/`
**入口**：`ossie`（cobra root）
**框架**：Cobra + JSON-over-stdin/stdout IPC

### 14.2.1 命令树

| 命令 | Use | 状态 | 关键 flags |
|---|---|---|---|
| `ossie` | (root) | ✅ | `--verbose` / `-v` (persistent) |
| `ossie convert` | `--from <p> --input <path>` 或 `--to <p> --input <path>` | 🚧 STUB | `--from`, `--to`, `--input`/`-i` (required), `--output`/`-o`, `--plugin`, `--timeout` (60), `--max-input-size` (100MB) |
| `ossie validate` | `validate [flags] <path> [<path>...]` | 🚧 STUB | `--strict`, `--output` (text/json) |
| `ossie plugin list` | `list` | ✅ | (no flags) |
| `ossie plugin install` | `install [name[@version] \| url]` | 🚧 STUB | `--all` |
| `ossie plugin remove` | `remove <name>` | 🚧 STUB | (no flags) |

> **STUB 现状**：`cli/cmd/{convert,validate,plugin/install,plugin/remove}.go`
> 当前打印 `"not yet implemented"`。**今天请用各 converter 自带 CLI 或
> `validation/validate.py`**。

### 14.2.2 `ossie plugin list` 输出示例

```bash
$ ossie plugin list
NAME       PLATFORM     SPEC
snowflake  Snowflake    0.1.0
dbt        dbt Labs     0.1.0
```

### 14.2.3 手工安装 plugin（绕过 stub）

```bash
mkdir -p ~/.ossie/plugins/snowflake
cat > ~/.ossie/plugins/snowflake/plugin.yaml <<EOF
ossie_plugin_spec: "0.1.0"
ossie_spec_version: ">=0.2.0"
name: snowflake
platform: Snowflake
convert:
  to_ossie:
    invoke: ["ossie-snowflake", "to-ossie"]
    accepts: [".yaml", ".json"]
  from_ossie:
    invoke: ["ossie-snowflake", "from-ossie"]
EOF
ossie plugin list  # 应能看到 snowflake
```

### 14.2.4 Cobra 陷阱

来源：`cli/cmd/root.go:30-32`

```go
// NOTE: Cobra does NOT automatically chain PersistentPreRunE from parent to
// child. If any subcommand defines its own PersistentPreRunE or PreRunE, this
// function will not run for that subcommand.
```

未来子命令若自定义 `PreRunE`，必须显式调用 `ossiedir.EnsurePluginDir()`。

## 14.3 Vendor Converter CLI

11 个 converter 中：**5 个有 Python CLI**（databricks/dbt/omni/orionbelt/wisdom），
**4 个 Python converter 是 library-only**（gooddata/gsf/honeydew/snowflake），
**2 个 Java converter 是 main class**（polaris/salesforce）。

### 14.3.1 Python CLI（5 个）

| Converter | 包名 | 子命令 | 关键 flags |
|---|---|---|---|
| **Databricks** | `ossie-databricks` | `export`, `import` | `-i`, `-o` |
| **dbt** | `ossie-dbt` | `msi-to-osi`, `osi-to-msi` | `-i`, `-o` (required) |
| **Omni** | `osi-omni` | `export`, `import` | `-i`, `-o`, `--base-view`, `--dialect` |
| **OrionBelt** | `ossie-orionbelt` | `obml-to-osi`, `osi-to-obml` | `-i`, `-o`, `--ontology`, `--no-validate`, `--database`, `--schema` |
| **WisdomAI** | `ossie-wisdom` | `wisdom-to-osi`, `osi-to-wisdom` | `-i`, `-o` |

```bash
# Databricks
ossie-databricks export -i model.yaml -o mv.yaml
ossie-databricks import -i mv.yaml -o model.yaml

# dbt (MetricFlow)
ossie-dbt msi-to-osi -i semantic_manifest.json -o model.yaml
ossie-dbt osi-to-msi -i model.yaml -o semantic_manifest.json

# Omni
osi-omni export -i model.yaml -o omni_model/ --base-view orders --dialect ANSI_SQL

# OrionBelt
ossie-orionbelt obml-to-osi -i obml.yaml -o model.yaml --ontology
ossie-orionbelt osi-to-obml -i model.yaml -o obml.yaml --database db --schema s

# WisdomAI
ossie-wisdom wisdom-to-osi -i domain-export.json -o model.yaml
ossie-wisdom osi-to-wisdom -i model.yaml -o domain-export.json
```

### 14.3.2 Python Library（4 个，无 CLI）

| Converter | 包名 | 用作库 |
|---|---|---|
| **GoodData** | `ossie-gooddata` | `from ossie_gooddata import convert_ldm_to_osi, convert_osi_to_ldm` |
| **NVIDIA GSF** | `ossie-gsf` | `from ossie_gsf import convert_osi_to_gsf, convert_gsf_to_osi` |
| **Honeydew** | `honeydew-osi` | `from honeydew_osi import ...` |
| **Snowflake** | `ossie-snowflake` | `from ossie_snowflake import export_to_snowflake` |

```python
# 示例：Snowflake 作为库
from ossie_snowflake import export_to_snowflake
import yaml

with open("model.yaml") as f:
    raw = yaml.safe_load(f)
snowflake_yaml = export_to_snowflake(raw)
with open("snowflake_model.yaml", "w") as f:
    f.write(snowflake_yaml)
```

### 14.3.3 Java Main Class（2 个）

#### Polaris

```bash
java -jar ossie-polaris-converter.jar import \
  --url http://polaris:8181/api/catalog \
  --catalog my_catalog

java -jar ossie-polaris-converter.jar export \
  --url http://polaris:8181/api/catalog \
  --catalog my_catalog \
  -o model.yaml
```

**关键 flag**：`--url`, `--catalog`, `--client-id`, `--client-secret`, `--token`

> **安全注意**：`--client-secret` 在命令行传值会被 `ps` 看到。优先用
> `--token`（短期 OAuth bearer）。详见 `SECURITY.md`。

#### Salesforce

```bash
# Ossie → Salesforce
java -jar ossie-salesforce-converter.jar toSF -i model.yaml -o sf_model.json

# Salesforce → Ossie
java -jar ossie-salesforce-converter.jar toOSI -i sf_model.json -o model.yaml
```

**特点**：Pipeline 架构——5 个 Handler 通过 `osi-salesforce-converter-config.yaml` 串联：
`DatasetMappingHandler` → `FieldMappingHandler` → `RelationshipMappingHandler`
→ `MetricMappingHandler` → `SemanticModelMappingHandler`。

## 14.4 错误处理快速跳转

| 错误类型 | 详见 |
|---|---|
| `ConverterIssueType` enum 值 | 第 13 章 §13.1 |
| Python 自定义异常（4 个） | 第 13 章 §13.2.1 |
| Java 自定义异常（3 个） | 第 13 章 §13.2.2 |
| CLI 退出码 | 第 13 章 §13.4 |

## 14.5 📌 章节要点速查

| 读者 | 一句话要点 |
|---|---|
| 用户 | 13 个 SDK 类 + 3 个 enum 在 §14.1；Go CLI 7 个命令在 §14.2（仅 `plugin list` 真正能用） |
| 开发者 | Python CLI 模板 = `_common.py + cli.py + <vendor>_to_osi.py + osi_to_<vendor>.py` |
| 架构师 | Go CLI 是 thin dispatcher；converter 自己负责业务逻辑；IPC 协议见第 9 章 §9.5 |
