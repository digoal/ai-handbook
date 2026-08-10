---
title: 云平台模板 — Azure / Fly / GCP / Railway / Render
slug: ch-45-cloud-platforms
part: part-vi-operations
audience: all
reading_time: 9
prerequisites: [ch-43-docker-compose, ch-44-k8s-helm]
semantica_version: 0.6.0
---

# ch-45 云平台模板 — Azure / Fly / GCP / Railway / Render

> 5 个云平台的一键部署模板。本章讲解 IaC 模板、参数化、运维成本。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- 5 平台一键部署: Azure Container Apps / Fly.io / GCP Cloud Run / Railway / Render。
- 每个平台都给完整模板 + 部署说明。
- 默认 `0.5 CPU + 512 MB`, 可按需扩。

### 1.2 平台适配矩阵

| 平台 | 模板路径 | 部署方式 | 起步成本 |
|---|---|---|---|
| **Azure Container Apps** | `deploy/azure/main.bicep` + `main.parameters.json` + `azure.yaml` | `az containerapp up` | 免费层 |
| **Fly.io** | `deploy/fly/fly.toml` | `flyctl deploy` | 免费层 (shared-cpu-1x, 512 MB) |
| **GCP Cloud Run** | `deploy/gcp/cloudrun-service.yaml` + `cloudbuild.yaml` | `gcloud run deploy` | 免费层 (2M req/月) |
| **Railway** | `deploy/railway/railway.toml` | `railway up` | $5/月试用金 |
| **Render** | `deploy/render/render.yaml` | Git push | 免费层 (会休眠) |

### 1.3 一段最小可跑示例

#### Fly.io

```bash
# 1) 安装 flyctl
brew install flyctl

# 2) 在 deploy/fly/ 目录部署
cd deploy/fly
flyctl launch      # 初始化 app
flyctl deploy      # 部署
```

#### GCP Cloud Run

```bash
# 1) 构建镜像
gcloud builds submit --config cloudbuild.yaml

# 2) 部署
gcloud run deploy semantica \
  --image gcr.io/$PROJECT/semantica \
  --region us-central1 \
  --min-instances 0 --max-instances 10 \
  --concurrency 80 \
  --allow-unauthenticated
```

### 1.4 何时不用

- 你要 K8s 自定义 → 用 [ch-44-k8s-helm]。
- 你要"全球分布" → 用 Cloud Run / Fly 自动多 region。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `deploy/azure/main.bicep` — Azure IaC (managed environment + Log Analytics + VNet)。
- `deploy/azure/main.parameters.json` — 参数化 (envName, location, sku)。
- `deploy/azure/azure.yaml` — Azure Developer CLI 配置。
- `deploy/fly/fly.toml` — Fly 配置 (shared-cpu-1x + 512 MB + `/api/health` probe)。
- `deploy/gcp/cloudrun-service.yaml` — Knative Service (min/maxScale 0/10, containerConcurrency 80)。
- `deploy/gcp/cloudbuild.yaml` — 自动 build (Dockerfile → GCR)。
- `deploy/railway/railway.toml` — Railway 配置 (一键部署)。
- `deploy/render/render.yaml` — Render 配置 (Git push 触发)。

### 2.2 最小复现脚本 (Azure)

```bash
# 1) 登录
az login

# 2) 部署
cd deploy/azure
az deployment group create \
  --resource-group semantica-rg \
  --template-file main.bicep \
  --parameters @main.parameters.json
```

### 2.3 已知陷阱

- **Azure Container Apps 冷启动**: 第一次请求慢 ~3s, 适合"非高频"。
- **Fly.io free tier**: 3 shared-cpu-1x + 256 MB, 内存吃紧时 OOM。
- **GCP Cloud Run 闲置**: min-instances 0 时会休眠, 第一次请求慢。
- **Railway 免费层**: $5/月 试用金, 超出按量计费。
- **Render free tier**: 15 分钟无活动休眠, 不适合生产。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么给 5 个平台?**
- 用户在任一云上都有"试一下"的需求, 一键模板能极大降低 PoC 门槛。
- 模板是"最小可行", 真实生产需用户按业务改 (VPC / IAM / WAF)。

**为什么不直接走 Terraform?**
- Terraform 太重, 用户要为 Semantica 学一套 HCL。
- 各平台原生 IaC (Bicep / GCP Deployment Manager) 更直接。

### 3.2 与同类对比

| 维度 | Semantica 云模板 | LangChain Cloud | LlamaIndex Deploy |
|---|---|---|---|
| 平台数 | 5 | 1 (LangChain Cloud) | 0 |
| IaC 完整度 | 中 (Bicep/原生) | 闭源 | N/A |
| 免费层 | ✅ (大部分) | ⚠ | N/A |

### 3.3 何时重新设计

- 平台 > 10 → 抽 `deploy-template-generator` 工具。
- 出现"金丝雀" → 引入云平台原生 traffic splitting。

## 跨章引用

- 上一章: [[ch-44-k8s-helm]]
- 下一章: [[ch-46-cicd]]
- 安全: [[ch-49-security]]