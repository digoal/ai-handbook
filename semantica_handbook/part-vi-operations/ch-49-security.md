---
title: 安全 — 密钥 / PII / 审计 / SBOM
slug: ch-49-security
part: part-vi-operations
audience: all
reading_time: 10
prerequisites: [ch-32-lifecycle-errors-config, ch-46-cicd]
semantica_version: 0.6.0
---

# ch-49 安全 — 密钥 / PII / 审计 / SBOM

> Semantica 提供 4 层安全: 密钥管理 + PII 脱敏 + W3C PROV-O 审计 + SBOM 漏洞扫描。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 密钥管理: API key 走 env / Secret, 不入 git。
- PII 脱敏: ingest 阶段内置 `redact_pii=True`。
- 审计导出: 一键出 W3C PROV-O 标准格式的溯源文件, 监管方可直接消费。
- SBOM: 安全扫描工作流生成 CycloneDX, 配合 `pip-audit` 扫描已知漏洞。

### 1.2 一段最小可跑示例

```bash
# 1) 配置密钥 (不入 git)
export SEMANTICA_API_KEYS__OPENAI=sk-xxx
export SEMANTICA_API_KEYS__ANTHROPIC=sk-ant-xxx

# 2) PII 脱敏 (可选)
export SEMANTICA_INGEST__REDACT_PII=true

# 3) 审计导出
python -c "
from semantica.provenance import ProvenanceManager
pm = ProvenanceManager(storage_path='./prov.db')
# ... 各种操作 ...
pm.export_prov(format='turtle', output_path='./audit.ttl')
"
```

### 1.3 何时不用

- 你要 SOC2 / HIPAA 合规 → 用 [ch-45-cloud-platforms] 的 Azure HIPAA + 合规模板。
- 你要"零信任网络" → 在 K8s NetworkPolicy ([ch-44-k8s-helm]) 显式禁止 egress。

## 2. 开发者视角(Developer)

### 2.1 公开 API

```python
semantica.utils.exceptions.SemanticaError
semantica.provenance.ProvenanceManager.export_prov
semantica.provenance.integrity.compute_checksum
semantica.provenance.integrity.verify_checksum
semantica.utils.validators.Validator.email
semantica.utils.validators.Validator.url
semantica.ingest.FileIngestor(redact_pii=True)
```

### 2.2 关键代码路径

- `semantica/utils/exceptions.py:49` — `SemanticaError` (含 error_code)。
- `semantica/utils/validators.py` — 数据 / 配置 / schema / entity / relationship / path / URL / email 校验。
- `semantica/utils/helpers.py` — 安全相关 helper。
- `semantica/provenance/integrity.py` — checksum 校验。
- `semantica/provenance/manager.py:1203` — `export_prov` 出 PROV-O。
- `.github/workflows/security.yml` — `pip-audit` 依赖审计。
- `.github/workflows/security-scan.yml` — 综合 SCA/SBOM。
- `.github/workflows/codeql.yml` — CodeQL 静态扫描。
- `.github/workflows/verify-action-pins.yml` — 防供应链攻击。
- `SECURITY.md` — 漏洞披露流程。

### 2.3 最小复现脚本

```python
# examples/ch-49-pii-redact.py mirror
from semantica.ingest import FileIngestor
from semantica.normalize import TextNormalizer

docs = FileIngestor(redact_pii=True).ingest(["./data/with_pii.txt"])
clean = TextNormalizer().normalize(docs[0].content)
# -> 邮箱 / 手机 / 身份证号被替换为 [REDACTED]
```

### 2.4 已知陷阱

- **PII 脱敏依赖 regex**: 复杂模式 (中文身份证 / 复杂邮箱) 可能漏。
- **密钥入 commit 历史**: 即便删除文件, 历史仍有, 需 `git filter-repo`。
- **PROV-O 公开化**: 导出前要确认不含敏感信息, 或用 `pm.export_prov(redact=True)`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么内置 PII 脱敏而不靠外部工具?**
- PII 脱敏是"靠近数据"的活, 在 ingest 层做效率最高。
- 但内置 regex 是基础版, 复杂场景用户可接 Presidio / AWS Comprehend。

**为什么 PROV-O 而不是自研审计格式?**
- W3C 标准, 监管方可直接消费。

### 3.2 与同类对比

| 维度 | Semantica 安全 | LangChain Hub | LlamaIndex |
|---|---|---|---|
| 内置 PII 脱敏 | ✅ (regex) | ❌ | ❌ |
| W3C PROV-O | ✅ | ❌ | ❌ |
| SBOM | ✅ | ⚠ | ❌ |

### 3.3 何时重新设计

- 出现"跨组织联邦" → 引入签名 + W3C VC。
- PII 漏判率 > 5% → 接 Presidio / Comprehend。

## 跨章引用

- 上一章: [[ch-48-observability]]
- 上一章 (Part V 末): [[ch-42-flow-c-decision-intel]]
- 漏洞披露: [SECURITY.md](https://github.com/semantica-agi/semantica/blob/main/SECURITY.md)