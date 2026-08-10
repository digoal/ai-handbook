---
title: 配置极简 — YAML + 环境变量 + 关键字参数
slug: ch-07-configuration-primer
part: part-i-foundations
audience: all
reading_time: 10
prerequisites: [ch-03-install]
semantica_version: 0.6.0
---

# ch-07 配置极简 — YAML + 环境变量 + 关键字参数

> 三种配置方式按优先级叠加, deep-merge, 不冲突。本章教你怎么写最小配置 + 怎么 override。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 5-9 行 YAML 把生产配置搞定。
- 知道优先级: CLI kwargs > 环境变量 > config.yaml > DEFAULT_CONFIG。
- 知道怎么 override 某个嵌套键 (如 `processing.batch_size=64`)。

### 1.2 三种配置方式

#### 方式 1: YAML 文件

`~/.semantica/config.yaml`:

```yaml
api_keys:
  openai: sk-your-key-here
  anthropic: sk-ant-your-key-here
embedding:
  provider: openai
  model: text-embedding-3-large
  dimensions: 3072
knowledge_graph:
  backend: networkx      # networkx | neo4j | falkordb | age | neptune
  temporal: true
processing:
  batch_size: 32
  max_workers: 4
quality:
  min_confidence: 0.7
logging:
  level: INFO
```

CLI 自动加载: `semantica info` 会打印"loaded config from ~/.semantica/config.yaml"。

#### 方式 2: 环境变量 (覆盖 YAML)

```bash
# 路径约定: SEMANTICA_<SECTION>__<KEY>=value
export SEMANTICA_PROCESSING__BATCH_SIZE=64
export SEMANTICA_EMBEDDING__PROVIDER=ollama
export SEMANTICA_KNOWLEDGE_GRAPH__BACKEND=falkordb
export SEMANTICA_API_KEYS__OPENAI=sk-replaced
export SEMANTICA_LOGGING__LEVEL=DEBUG
```

环境变量自动合并, 优先级高于 YAML。

#### 方式 3: Python 关键字参数 (覆盖一切)

```python
from semantica import Semantica

fw = Semantica(
    embedding={"provider": "ollama", "model": "nomic-embed-text"},
    knowledge_graph={"backend": "falkordb"},
    processing={"batch_size": 64},
)
```

### 1.3 优先级

```
DEFAULT_CONFIG (semantica/utils/constants.py)
   ↓ 被
~/.semantica/config.yaml (或显式 path)
   ↓ 被
SEMANTICA_*__* 环境变量
   ↓ 被
Semantica(**kwargs)
   ↓ 被
Semantica(config=cfg_dict) (显式 Config 对象, 优先级最高)
```

### 1.4 何时用

- **本地开发**: 写 `~/.semantica/config.yaml`, 不设环境变量。
- **CI / 临时实验**: 临时 `export SEMANTICA_*`。
- **生产**: 全部走 YAML 文件 + Helm ConfigMap (`SEMANTICA_*` 走 K8s Secret)。
- **单元测试**: 走 `Semantica(**kwargs)` 或 `pytest` fixture。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
from semantica.core import Semantica, Config, ConfigManager

# 工厂
fw = Semantica()                                       # 自动加载 ~/.semantica/config.yaml + env
fw = Semantica(config_dict={"processing": {"batch_size": 64}})
fw = Semantica(config=Config(...), processing={"batch_size": 64})  # 关键字作为叠加层

# Config 直接构造
cfg = Config(processing={"batch_size": 64}, embedding={"provider": "openai"})
print(cfg.get("processing.batch_size"))    # 64
print(cfg.to_dict())                       # 全配置 dump

# ConfigManager
cm = ConfigManager()
cfg = cm.load_from_file("./my.yaml")
cfg = cm.load_from_dict({...})
merged = ConfigManager.merge_configs(cfg_a, cfg_b)
```

### 2.2 关键代码路径

- `semantica/core/config_manager.py:89` — `Config.__init__`, `_build_config_dict` deep-merge。
- `semantica/core/config_manager.py:60` — `_load_from_env`, 解析 `SEMANTICA_*`。
- `semantica/core/config_manager.py:236` — `Config.validate`, 聚合 `ConfigurationError [[ch-55-glossary]]`。
- `semantica/core/config_manager.py:331` — `Config.to_dict`。
- `semantica/core/config_manager.py:352` — `Config.get(key_path, default)`, 嵌套路径访问。
- `semantica/utils/constants.py` — `DEFAULT_CONFIG` 内置默认值。
- `semantica/utils/helpers.py` — `merge_dicts / get_nested_value / set_nested_value`。

### 2.3 最小复现脚本

```python
# examples/ch-07-config-demo.py mirror
import os
os.environ["SEMANTICA_PROCESSING__BATCH_SIZE"] = "128"

from semantica.core import Semantica, Config

# 1) 加载默认 + 环境变量
fw = Semantica()
print("batch_size:", fw.config.get("processing.batch_size"))  # 128 (env 覆盖 default)
fw.shutdown()

# 2) 显式 dict + kwargs
fw = Semantica(
    config_dict={"processing": {"max_workers": 2}},
    knowledge_graph={"backend": "networkx"},
)
print("max_workers:", fw.config.get("processing.max_workers"))  # 2
print("backend:", fw.config.get("knowledge_graph.backend"))      # networkx
fw.shutdown()

# 3) 校验会失败的情形
try:
    Config(processing={"batch_size": -1})  # 触发 ConfigurationError
except Exception as e:
    print(f"✓ Validation rejected: {e}")
```

### 2.5 扩展点

- 想加自定义 section: 在 `Config._initialize_sections` (config_manager.py:134) 加属性, 在 `DEFAULT_CONFIG` 加默认值。
- 想加自定义校验: 改写 `Config.validate` (config_manager.py:236)。
- 想从 Vault / 1Password 读 secrets: 替换 `_load_from_env` 实现。

## 3. 架构师视角(Architect)

### 3.1 设计取舍 — 为什么是 YAML+env+kwargs 而非 Pydantic Settings?

**为什么不学 FastAPI / LangChain 用 Pydantic?**
- Pydantic v2 强制 30+ MB 依赖, 与 Semantica "extras 化" 哲学相悖。
- 用户配置多在 YAML / 环境变量层切换, 用纯 stdlib `pyyaml` + dict-merge 更轻, 启动更快。
- 校验在 `Config.validate` 集中, 不依赖模型自带的 validator, 让错误聚合更可控。

**为什么 `SEMANTICA_*__*` 而不是点号路径?**
- 环境变量语法不支持点号, 双下划线是 de-facto 标准 (12-factor app, AWS App Runner 等)。
- `__` 转 `.` 的转换在 `_load_from_env` 内完成, 对用户透明。

### 3.2 与同类对比

| 维度 | Semantica | LangChain (LCEL) | LlamaIndex | Pydantic Settings |
|---|---|---|---|---|
| 配置文件 | YAML/JSON | env only | env + dict | .env / env |
| 多源优先级 | 4 层 | 2 层 | 3 层 | 3 层 |
| 嵌套路径语法 | `__` 分隔 | N/A | `.` 分隔 | `.` 分隔 |
| 校验 | 集中 `validate()` | 分散 dataclass | 分散 dataclass | 自动 (Pydantic) |
| 类型强制 | 手动 (str/int/bool) | 类型注解 | 类型注解 | 自动 |

### 3.3 何时重新设计

- 用户反馈"YAML 不够用, 想 TOML/JSON5" → 扩 `_load_from_file` 支持多格式。
- 配置 schema 经常变动 → 引入 versioned config (类似 Spring Boot `@ConfigurationProperties`)。

## 本章图表

> 本章无 Mermaid 图。同主题的 deep-merge 图见 [[ch-32-lifecycle-errors-config]] FIG-11 (本卷统一在 ch-32 给出, 避免重号)。

## 跨章引用
- CLI 全解: [[ch-27-cli]] § `init` / `config` 子命令
- 错误体系深探: [[ch-32-lifecycle-errors-config]] §3 `ConfigurationError`
- 部署配置: [[ch-44-k8s-helm]] ConfigMap / Secret 注入