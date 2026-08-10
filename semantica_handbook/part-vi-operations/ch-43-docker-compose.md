---
title: Docker / Compose — 一键拉起
slug: ch-43-docker-compose
part: part-vi-operations
audience: all
reading_time: 10
prerequisites: [ch-03-install]
semantica_version: 0.6.0
---

# ch-43 Docker / Compose — 一键拉起

> 用 Docker 在本地或生产跑 Semantica。本章讲解多阶段 Dockerfile、Compose 编排、dev / prod 两套模板。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- `docker compose up` 拉起 Explorer + FalkorDB 一键生产栈。
- `docker compose -f docker-compose.dev.yml up` 拉起开发栈 (含前端热重载)。
- 单容器: `docker run semantica/explorer` 仅跑 Explorer API。

### 1.2 一段最小可跑示例

```bash
# 生产编排 (1 Explorer + 1 FalkorDB)
docker compose up -d
docker compose ps
curl http://localhost:8000/health

# 开发编排 (含前端热重载)
docker compose -f docker-compose.dev.yml up
# Explorer: http://localhost:8000
# Vite dev server: http://localhost:5173
```

### 1.3 何时不用

- 你的部署平台是 K8s → 用 [ch-44-k8s-helm]。
- 你要 FaaS 部署 → 用 [ch-45-cloud-platforms] (Azure Container Apps / Fly)。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `Dockerfile` (多阶段):
  - Stage 1: `node:26-alpine` 编译 Explorer 前端。
  - Stage 2: `python:3.14-slim` 安装 `semantica` + run `uvicorn semantica.explorer.app:app`。
  - 默认用户 `semantica`, 暴露 8000, 健康检查 `/api/health`。
- `docker-compose.yml` (生产):
  - 1 explorer 服务 + 1 falkordb 服务。
  - 端口 6379 暴露, 命名网络 `semantica`, 卷 `falkordb_data`。
- `docker-compose.dev.yml` (开发):
  - explorer 加 `--reload --reload-dir /app/semantica`。
  - 新增 frontend 服务 (Node 22 + Vite, 5173 端口), 支持热重载。

### 2.2 Dockerfile 关键片段

```dockerfile
# Stage 1: 前端
FROM node:26-alpine AS frontend
WORKDIR /app/explorer
COPY explorer/package*.json ./
RUN npm ci
COPY explorer/ ./
RUN npm run build

# Stage 2: 后端
FROM python:3.14-slim
RUN useradd -m -u 1000 semantica
WORKDIR /app
COPY --from=frontend /app/explorer/dist ./semantica/static
COPY semantica/ ./semantica/
COPY pyproject.toml ./
RUN pip install --no-cache-dir .
USER semantica
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health
CMD ["uvicorn", "semantica.explorer.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.3 最小复现脚本

```bash
# build & run
docker build -t semantica-explorer:dev .
docker run -p 8000:8000 semantica-explorer:dev
```

### 2.4 扩展点

- **加 GPU 支持**: 改 base image 为 `python:3.14-slim` + `nvidia/cuda:*-runtime`。
- **加非 root 用户**: 已默认, 改 UID 通过 `--build-arg UID=...`。
- **加 healthcheck probe**: 在 Dockerfile `HEALTHCHECK` 加 `wget` / `python -c`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么多阶段 build?**
- 前端 build 需要 Node + npm (~ 400 MB), 但运行时只需静态文件 (~ 30 MB)。
- 多阶段把前端产物 copy 到 Python image, 最终镜像只 ~500 MB (vs 1.2 GB 单阶段)。

**为什么 Compose 用 FalkorDB 而不是 Neo4j?**
- FalkorDB 镜像 60 MB, Neo4j 镜像 800 MB。
- Compose 编排强调"轻 + 快", FalkorDB 更适合。

### 3.2 与同类对比

| 维度 | Semantica Compose | LangChain Serve | LlamaIndex Deploy |
|---|---|---|---|
| 编排 | docker-compose (2 服务) | docker-compose (1 服务) | 无 |
| Dev 模式 | ✅ Vite 热重载 | ❌ | ❌ |
| 多镜像体积 | 500 MB (FalkorDB 60) | 800 MB | N/A |

### 3.3 何时重新设计

- 服务数 > 5 → 拆多个 compose 文件 (`compose-falkordb.yml` / `compose-neo4j.yml`)。
- 镜像 > 1 GB → 用 `slim` / `alpine` base + 清理 `pip cache`。

## 跨章引用

- 上一章: [[ch-42-flow-c-decision-intel]]
- 下一章: [[ch-44-k8s-helm]]
- 云平台: [[ch-45-cloud-platforms]]