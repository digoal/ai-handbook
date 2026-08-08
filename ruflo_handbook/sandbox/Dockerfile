# sandbox/Dockerfile — Docker 沙箱镜像（可选）
# 用法（在 ruflo_handbook 根目录）：
#   docker build -t ruflo-sandbox sandbox/
#   docker run --rm -it -v $(pwd):/handbook ruflo-sandbox bash
#
# 适用：用户主机有 Docker daemon 时；否则用 sandbox/setup.sh（本地模式）。

FROM node:20-bookworm-slim

LABEL org.opencontainers.image.title="ruflo-handbook-sandbox"
LABEL org.opencontainers.image.description="Sandbox for ruflo handbook hands-on verification"
LABEL org.opencontainers.image.source="https://github.com/ruvnet/ruflo"

# 必要工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl jq ca-certificates bash ripgrep \
    && rm -rf /var/lib/apt/lists/*

# pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9 --activate

# ruflo CLI（latest）
RUN npm install -g ruflo@latest

# mock LLM 默认开
ENV MOCK_LLM=1
ENV RUFLO_LOG_LEVEL=info
ENV CLAUDE_FLOW_HOOKS_ENABLED=true
ENV CI=true

WORKDIR /handbook

# 容器内入口脚本（覆盖启动时）
COPY entrypoint.sh /usr/local/bin/sbx-entrypoint
RUN chmod +x /usr/local/bin/sbx-entrypoint

ENTRYPOINT ["/usr/local/bin/sbx-entrypoint"]
CMD ["bash"]