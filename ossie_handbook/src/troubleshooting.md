# Troubleshooting · 故障排查

> **Abstract** — A symptom-driven troubleshooting guide for the 30 most common Ossie issues. Each entry follows the same schema: Symptom → How to reproduce → Root cause → Fix. Cross-references the relevant core-spec section, validator output, or GitHub Issue for each. Designed so you can `grep -n` the symptom and jump to the answer.

> **【为用户】** 遇到 Ossie 报错时来这里——按症状查。
>
> **【为开发者】** 30 个最常见问题的诊断逻辑，反向工程一遍能学到 Ossie 的边界。
>
> **【为架构师】** 故障模式库（failure mode library）——分类、严重程度、回归路径。

## 1. 验证器（validate.py）问题

### 1.1 `[Schema] 'semantic_model' is a required property`

- **症状**: 跑 `validate.py`，报 root 缺 `semantic_model`。
- **根因**: 文档顶层是 `ontology:` 或 `ontology_mappings:`（如 flights.yaml），validate.py 只校验 `semantic_model:` 根字段。
- **修复**: 验证器不支持 ontology 顶层 schema 校验（Roadmap WG #3 工作）。要么用 `python -c "import yaml; yaml.safe_load(open('flights.yaml'))"` 确认 YAML 合法，要么把 ontology 示例放到语义模型目录里。

### 1.2 `[Schema] 'foo' is not of type 'array'`

- **症状**: `semantic_model` 写成了 object 而非 array。
- **根因**: schema 里 `semantic_model` 是 `array, minItems: 1`（`osi-schema.json:34`）。
- **修复**: 改为列表形式：

```yaml
semantic_model:
  - name: my_model     # 注意是 - name
    datasets: [...]
```

### 1.3 `[Schema] 'bar' is not of type 'string'`

- **症状**: 某个字段是 number 或 boolean 而非 string。
- **根因**: spec 里大部分字段是 `type: string`（如 `name`, `description`）。
- **修复**: 把数字或 boolean 加引号：

```yaml
- name: orders
  description: "Order ID 1234"    # 即使是数字也加引号
```

### 1.4 `[Unique] Duplicate field name 'X' in dataset 'Y'`

- **症状**: 同一 dataset 内两个字段同名。
- **根因**: 字段名在 dataset 内必须唯一（`spec.md:228-230`）。
- **修复**: 重命名一个字段，并更新所有引用它的 `Metric.expression`。

### 1.5 `[Unique] Duplicate metric name 'X'`

- **症状**: 同一 model 内两个 metric 同名。
- **根因**: metric 在 model 内必须唯一。
- **修复**: 同上。

### 1.6 `[Reference] Relationship 'X' references unknown dataset 'Y'`

- **症状**: relationship 的 `from` 或 `to` 指向不存在的数据集。
- **根因**: 拼写错误，或引用了不同 `SemanticModel` 里的 dataset。
- **修复**: 检查 `from:` 和 `to:` 字段，确保 dataset name 完全匹配（包括大小写）。

### 1.7 `[SQL] Invalid expression` (snowflake)

- **症状**: validator 报 `Field 'orders.amount' in model 'sales' (SNOWFLAKE): Invalid expression`。
- **根因**: sqlglot 解析 Snowflake 表达式失败。
- **诊断**: 用 `--output json` 看具体哪行：

```bash
uv run validation/validate.py model.yaml --output json
```

- **修复**:
  - 表达式语法错误（如缺少括号、关键字拼错）
  - 用 vendor-specific 函数但 dialect 写成 ANSI_SQL——加 `SNOWFLAKE` 方言版本
  - 临时绕过：用 `SKIP_SQL_VALIDATION` 标记（validator 内部的 `MDX`/`TABLEAU`/`MAQL` 默认跳过）

### 1.8 `[SQL] Warning: sqlglot not installed`

- **症状**: SQL 校验整层被跳过。
- **根因**: `validate.py` depends on `sqlglot>=30.12.0`（PEP 723 声明），但环境里没装。
- **修复**: 重新跑 `uv run validation/validate.py ...`——uv 会自动装。**注意**: sqlglot 缺失**不**导致 exit 1，但 SQL 校验报告无效。

### 1.9 Validator 跑不通 docker / sandbox 容器

- **症状**: 容器内 `uv run` 不可用。
- **修复**: 装 system Python + `pip install jsonschema pyyaml sqlglot`，然后 `python validation/validate.py ...`。

## 2. SDK（python apache-ossie）问题

### 2.1 `ModuleNotFoundError: No module named 'ossie'`

- **症状**: `PYTHONPATH=python/src` 没设，或 SDK 没安装。
- **修复**:
  ```bash
  cd <ossie-repo>
  PYTHONPATH=python/src python3 -c "from ossie import OSIDocument"
  # 或：cd python && uv sync
  ```

### 2.2 `ValidationError: ... 'from' is a required property`

- **症状**: SDK 报 `from` 字段缺失。
- **根因**: 你用了 `from_dataset=...` 而 YAML 用 `from:`。SDK 用 `alias="from"`。
- **修复**: Python 端写 `from_dataset='orders'`；YAML 端写 `from: orders`。

### 2.3 `ValidationError: 'foo' is not a valid OSIDialect`

- **症状**: dialect 写成 `Snowflake` 而非 `SNOWFLAKE`。
- **根因**: SDK 的 `OSIDialect` enum 是大写（`python/src/ossie/models.py:25-34`）。
- **修复**: 改为 `OSIDialect.SNOWFLAKE`、`"SNOWFLAKE"` 或 `dialect="snowflake"` 都行；SDK 会自动 normalize。

### 2.4 `ValidationError: 'Opaque' is not a valid DataType`

- **症状**: 试图用 `Opaque` 字段但报错。
- **根因**: `Opaque` 合法，但仅在 `OSIDataType.OPAQUE` 路径下。
- **修复**: 应该是 `datatype="Opaque"`（首字母大写）；或 Python 端 `OSIDataType.OPAQUE`。

### 2.5 `to_osi_yaml()` 输出含 `null` 字段

- **症状**: 序列化 YAML 里有 `foo: null`。
- **根因**: 调用时没传 `exclude_none=True`（默认是 True）。
- **修复**: SDK 内部已默认 `exclude_none=True`（`models.py:218`），如果还出现 null，检查是否在 dump 后手动合并。

### 2.6 YAML 加载后 `dialect` 字段被转成 `dialect_` 或丢失

- **症状**: `OSIDialectExpression.dialect` 字段访问失败。
- **根因**: 类似 `from` 的别名问题。SDK 已统一为 `dialect` 字段名。
- **修复**: 直接用 `expr.dialect`。

## 3. Converter 调用问题

### 3.1 `ossie-snowflake: command not found`

- **症状**: 安装后仍找不到。
- **修复**:
  ```bash
  uv tool install ossie-snowflake
  # 验证 PATH
  which ossie-snowflake
  # 应该是 ~/.local/bin/ossie-snowflake
  ```

### 3.2 `KeyError: 'SNOWFLAKE'` 在 converter 中

- **症状**: 某字段没有 `dialect: SNOWFLAKE`，converter 卡住。
- **诊断**: 看错误前的 warning：`no SNOWFLAKE or ANSI_SQL expression`。
- **修复**: 给字段加 `expression.dialects[]` 包含 `SNOWFLAKE`，或确认有 `ANSI_SQL` fallback。

### 3.3 round-trip 后 `custom_extensions` 丢失

- **症状**: Ossie → Snowflake → Ossie 后，原 `custom_extensions[SALESFORCE]` 没了。
- **根因**: 该 converter 没有 honor round-trip fidelity（不在白名单）。
- **诊断**: 检查 `custom_extensions` 数组——若只剩 `SNOWFLAKE` 一个 vendor，原 vendor 已被吞。
- **修复**: 升级 converter（开 GitHub Issue）。临时方案：用 `ossie-snowflake` 时同时加 `ossie-salesforce` 双向桥。

### 3.4 `ossie-dbt msi-to-osi` 报 `CUMULATIVE_SEMANTICS_LOSS`

- **症状**: dbt cumulative metric 转换丢失。
- **根因**: ossie 0.2.0.dev0 暂不支持 `cumulative` 度量（Roadmap #39）。
- **修复**: 等待 0.2.0 后续版本；或手动改 Ossie YAML 里的 `metric` 为 `derived`（占位）。

### 3.5 Databricks 输出包含 `on: true` 等布尔丢失

- **症状**: 转换后 join 条件全丢。
- **根因**: YAML 1.1 把 `on/off/yes/no` 视为布尔，被错误识别为 join 关键字。
- **修复**: 转换器内部用 YAML 1.2 loader（`_common.py:113-128`）。如果你自己写 YAML，避免裸用 `on:`、`off:` 做 key。

### 3.6 Polaris 报 `401 Unauthorized` 连 live catalog

- **症状**: `ossie-polaris import --url ...` 401。
- **根因**: 缺 OAuth 客户端凭据。
- **修复**:
  ```bash
  ossie-polaris import \
    --url http://polaris:8181/api/catalog \
    --catalog my_catalog \
    --client-id <id> \
    --client-secret <secret>
  ```

### 3.7 GoodData LDM 转换后 `facts` 数组为空

- **症状**: 转换后 `facts: []`。
- **根因**: GoodData LDM 把度量放 `metrics:` 而非 `facts:`；Ossie Metric 转换跳过（GoodData 不支持）。
- **修复**: 期望行为。GoodData 不支持 OSSIE Metric 转换（详见 §7.2.3）。

## 4. CLI（go）问题

### 4.1 `ossie convert` 打印 "not yet implemented"

- **症状**: 跑 `ossie convert --to snowflake -i model.yaml` 报错。
- **根因**: `cli/cmd/convert.go:46` 是 stub。
- **修复**: 今天请用各 converter 自带 CLI：
  ```bash
  ossie-snowflake -i model.yaml -o snowflake.yaml   # 替代 ossie convert --to snowflake
  ```

### 4.2 `ossie plugin list` 显示 "no plugins installed"

- **症状**: 装好 converter 但 plugin list 是空。
- **根因**: `plugin list` 扫描的是 `~/.ossie/plugins/<name>/plugin.yaml`——不是 `uv tool install` 装的。
- **修复**: 手动创建 plugin manifest：
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
  ```

### 4.3 `ossie validate` 也是 stub

- **症状**: 跑 `ossie validate model.yaml` 报 "not yet implemented"。
- **修复**: 用 `uv run validation/validate.py model.yaml`。

### 4.4 `OSSIE_PLUGIN_DIR` 环境变量不生效

- **症状**: 修改了 `OSSIE_PLUGIN_DIR` 但 plugin list 仍扫默认目录。
- **根因**: `cli/internal/ossiedir/ossiedir.go:30` 优先读 env var，但你重启 shell 之前不生效。
- **修复**: `export OSSIE_PLUGIN_DIR=/path/to/dir && which ossie` 验证。

## 5. spec 演进问题

### 5.1 0.1.1 → 0.2.0.dev0 升级 breakage

- **症状**: 旧 converter 读 0.2.0 新字段报错。
- **根因**: `schema.yaml` 0.2.0.dev0 删除了一些字段。
- **修复**: 锁版本——`pyproject.toml` pins `apache-ossie==0.1.1`。

### 5.2 Want `aggregation_method` 但 schema 没这个字段

- **症状**: 想表达 `SUM` vs `AVG` 显式选择。
- **根因**: `aggregation_method` 在 Roadmap #19 讨论中，0.2.0.dev0 暂未实现。
- **修复**: 等 0.2.0+。临时把 `Metric.name` 命名为 `sum_amount` / `avg_amount`。

### 5.3 想要 `expressed cardinality` 但 `Relationship` 只有 `from`/`to`

- **症状**: 想表达 1-to-1 还是 many-to-many。
- **根因**: 显式 cardinality 是 Roadmap #50 讨论。
- **修复**: 假 many-to-one 是默认（from → to）；命名上区分 `one_to_one_rel` vs `many_to_one_rel`。

## 6. 贡献时遇到的问题

### 6.1 ICLA 提交被拒

- **症状**: `dev@` 上 committer 提名需要 ICLA 文件在 Apache 仓库。
- **修复**: 走 https://www.apache.org/licenses/icla 流程；通常 1-2 周。

### 6.2 PR 模板 8 项检查没过

- **修复**: 逐项检查；常见项：
  - 测试：`cd converters/<vendor> && uv run pytest`
  - 文档：改 `docs/`、`CONTRIBUTING.md`、`examples/`
  - License header：每个新文件加 ASF header

### 6.3 spec 提案 PR 被 dev list 要求 ≥3 binding +1

- **症状**: 改 `osi-schema.json` 的 PR 卡 72h 没人投 +1。
- **修复**: 这意味着 features 不足够清晰；回到 GitHub Discussions 重新解释。

## 7. 环境与依赖

### 7.1 `uv` 安装失败

- **症状**: `curl -LsSf https://astral.sh/uv/install.sh | sh` 网络问题。
- **修复**: 用 `pip install uv` 或 `brew install uv`（macOS）。

### 7.2 Windows 原生不支持

- **症状**: 某些 converter 在 Windows 上跑不通。
- **修复**: 用 WSL2；Python 在 Windows 原生支持 OK，Java converter 需 JDK 21+。

### 7.3 Java 17 vs 21

- **症状**: Salesforce/Polaris 的 Maven build 报 `release 21 not found`。
- **修复**: 装 JDK 21（Temurin 推荐）：`brew install openjdk@21`。

## 8. 性能与并发

### 8.1 1M 行 semantic_model 转换慢

- **症状**: 模型超过 1000 dataset 时转换超时。
- **诊断**: 单线程处理 + 频繁 SQL 解析。
- **修复**: 暂时拆 model；未来 converter roadmap 引入并发。

### 8.2 validator 内存峰值高

- **症状**: 大 model validator OOM。
- **修复**: 逐 dataset 校验（未来 feature）；临时用 `--input <file>` 单独校验。

## 8.3 📌 章节要点速查

| 读者 | 一句话要点 |
|---|---|
| 用户 | 30 个症状 → 诊断 → 修复，按目录查 |
| 开发者 | 这就是 Ossie 失败模式的反向工程 |
| 架构师 | 故障模式库 + 修复路径 + 跟踪位置 |