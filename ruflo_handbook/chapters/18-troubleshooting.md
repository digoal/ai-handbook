---
title: 第 18 章 · 故障排查与常见报错
last_verified_against: 26c35b59b40a0a95b286ccf5ac675a15edcc995f
verified_at: 2026-07-23
chapter: 18
---

# 第 18 章 · 故障排查与常见报错

> 📘 **摘要**：本章是**实战手册的「急救箱」**。覆盖 **26 项 doctor 检查**、**7 类常见错误**、**3 类性能抖动**、**2 套数据迁移方案**。每条问题给出 **症状 → 排查 → 修复 → 验证** 四段式流程。
>
> 🏷️ **读者画像**：D（平台/SRE）/ F（审计）
> 🕐 **预估耗时**：30 分钟（按需查阅）
> ✅ **LAST_VERIFIED_AGAINST**：`26c35b59` (v3.32.9)

---

## 使用方法

- **遇到报错？** 直接按目录跳到对应小节（每节以**报错信息 / 现象**为标题）
- **想体检？** 看 §1「26 项 doctor 速查」对照结果
- **性能慢？** 跳到 §5「性能抖动」
- **升级报错？** 跳到 §6「数据迁移」

---

## 1. Doctor 报错全集（26 项逐条排查）

`ruflo doctor` 是**第一道防线**。每个 `[N/26]` 检查都可能 FAIL / WARN / EXPECTED。**所有 FAIL 都列在下面**。

### 1.1 [1/26] Node.js version ✗

**症状**：`Node.js version 18.x.x detected (< 20 required)` 或 `node: command not found`

**原因**：ruflo v3.x 要求 Node ≥ 20.0.0。

**修复**：

```bash
# macOS (Homebrew)
brew install node@20
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc

# Linux (nvm 推荐)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20
nvm alias default 20

# 或用 fnm（更快）
curl -fsSL https://github.com/Schniz/fnm/raw/master/.ci/install.sh | bash
fnm install 20
fnm use 20

# 验证
node --version  # 应 ≥ v20.0.0
```

### 1.2 [2/26] npm version ✗

**症状**：`npm version 8.x.x detected (< 9 required)`

**原因**：ruflo v3.x 要求 npm ≥ 9。

**修复**：

```bash
npm install -g npm@latest
npm --version  # 应 ≥ 9
```

### 1.3 [3/26] git / [4/26] curl / [5/26] jq ✗

**症状**：`git: command not found` / `curl: command not found` / `jq: command not found`

**原因**：缺失基础依赖。

**修复**：

```bash
# macOS
brew install git curl jq

# Ubuntu/Debian
sudo apt update && sudo apt install -y git curl jq

# Alpine
apk add git curl jq

# 验证
git --version && curl --version | head -1 && jq --version
```

### 1.4 [6/26] Claude Code CLI ✗

**症状**：`claude: command not found` 或 `Claude Code not detected`

**原因**：未安装 Claude Code，或 PATH 不对。

**修复**：

```bash
# 官方安装
curl -fsSL https://claude.ai/install.sh | bash

# 或 npm
npm install -g @anthropic-ai/claude-code

# 验证
claude --version  # 应 ≥ 1.0
which claude      # 应在 PATH 中
```

### 1.5 [7/26] Ruflo CLI ✗

**症状**：`ruflo: command not found` 或 `Ruflo CLI version mismatch (expected 3.32.9)`

**修复**：

```bash
# 全局装最新
npm install -g ruflo@latest

# 或锁定版本
npm install -g ruflo@3.32.9

# 验证
ruflo --version  # 应 = 3.32.9
```

### 1.6 [8/26] CLAUDE.md ✗

**症状**：`CLAUDE.md missing` 或 `CLAUDE.md invalid format`

**修复**：

```bash
# A. 跑 init 自动生成
npx --yes ruflo@latest init --non-interactive --skip-prompts

# B. 手动检查格式
cat CLAUDE.md  # 应有 frontmatter 或首行 "# Claude Code Configuration"

# C. 缺了就跑 init upgrade
npx --yes ruflo@latest init upgrade --add-missing
```

### 1.7 [9/26] .claude/settings.json ✗

**症状**：`.claude/settings.json missing` / `invalid JSON` / `missing required hook`

**修复**：

```bash
# 1. 检查 JSON 合法性
jq . .claude/settings.json  # 若报错 → 文件被破坏

# 2. 备份 + 重写
cp .claude/settings.json .claude/settings.json.bak
npx --yes ruflo@latest init upgrade --add-missing

# 3. 跑 doctor --fix
npx --yes ruflo@latest doctor --fix
```

### 1.8 [10/26] .mcp.json ✗

**症状**：`.mcp.json missing` / `mcp__ruflo not registered`

**修复**：

```bash
# 1. 写入最小 .mcp.json
cat > .mcp.json <<'MCP'
{
  "mcpServers": {
    "ruflo": {
      "command": "npx",
      "args": ["--yes", "ruflo@latest", "mcp", "start"],
      "env": {
        "CLAUDE_FLOW_HOOKS_ENABLED": "true"
      }
    }
  }
}
MCP

# 2. 验证
cat .mcp.json | jq .

# 3. 重新跑 doctor
npx --yes ruflo@latest doctor --no-color 2>&1 | grep "mcp"
```

### 1.9 [11/26] ANTHROPIC_API_KEY / [12/26] OPENAI_API_KEY ✗

**症状**：`ANTHROPIC_API_KEY missing` 或 `OPENAI_API_KEY missing`

**原因**：这是**常见但不严重**的问题——在沙箱内是 `[EXPECTED]`。

**修复（生产环境）**：

```bash
# 1. 写入 .env
cat >> .env <<EOF
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyXxxxxxxxxxxxxxxxxxxxx
EOF

# 2. 加载到 shell（zsh）
echo 'source .env' >> ~/.zshrc  # 或在 .zshrc 里 export

# 3. 验证
echo "$ANTHROPIC_API_KEY" | head -c 7  # 应 = "sk-ant-"

# 4. 跑 doctor 看是否转 PASS
npx --yes ruflo@latest doctor --no-color 2>&1 | grep "API_KEY"
```

**沙箱**：保持 `[EXPECTED]`，不影响 doctor 通过。

### 1.10 [13/26] AgentDB ✗

**症状**：`AgentDB not initialized` / `agentdb.rvf corrupted`

**修复**：

```bash
# 1. 检查文件
ls -la .claude-flow/memory/agentdb.rvf*

# 2. 若损坏 → 重建
mv .claude-flow/memory/agentdb.rvf .claude-flow/memory/agentdb.rvf.broken
npx --yes ruflo@latest init upgrade --add-missing
npx --yes ruflo@latest doctor --fix

# 3. 若权限问题
chmod -R u+rw .claude-flow/memory/
```

### 1.11 [14/26] HNSW index ✗

**症状**：`HNSW index not built` / `HNSW corruption detected`

**修复**：

```bash
# 触发 worker rebuild
npx --yes ruflo@latest hooks consolidate --target hnsw --no-color

# 或删索引让 agent 重建
rm .claude-flow/memory/*.hnsw
npx --yes ruflo@latest memory search --query "test" --top-k 1  # 触发重建

# 验证
npx --yes ruflo@latest doctor --no-color 2>&1 | grep -i hnsw
```

### 1.12 [15/26] Memory namespaces ✗

**症状**：`Expected 3 namespaces (project/local/user), found 1`

**修复**：

```bash
# 显式初始化缺失命名空间
for ns in project local user; do
  npx --yes ruflo@latest memory init --namespace "$ns" 2>/dev/null || true
done

# 验证
npx --yes ruflo@latest memory list --no-color 2>&1 | tail -10
```

### 1.13 [16/26] Hooks ✗

**症状**：`Expected 17 hooks, found 5` / `hooks.json invalid`

**修复**：

```bash
# 1. 看现状
npx --yes ruflo@latest hooks list --no-color 2>&1 | tail -25

# 2. 重写 hooks.json
npx --yes ruflo@latest init upgrade --add-missing

# 3. 验证数量
npx --yes ruflo@latest hooks list --no-color 2>&1 | grep -cE "active|disabled"
# 应 ≥ 17
```

### 1.14 [17/26] Skills ✗

**症状**：`Expected 134 skills, found 80`

**修复**：

```bash
# 重装 skills
npx --yes ruflo@latest init upgrade --add-missing

# 或显式
npx --yes ruflo@latest plugins install ruflo-core --force

# 验证
ls .claude/skills/ | wc -l  # 应 ≥ 134
```

### 1.15 [18/26] MCP server ✗

**症状**：`MCP server unreachable` / `stdio pipe broken`

详见 §3「MCP server 启动失败」。

### 1.16 [19/26] Swarm topology ✗ / [20/26] Consensus ✗

**症状**：`Invalid topology` / `Consensus not configured`

**修复**：

```bash
# 检查当前配置
npx --yes ruflo@latest swarm config show --no-color 2>&1 | tail -20

# 重置为默认值
npx --yes ruflo@latest swarm config reset --no-color

# 显式设置
npx --yes ruflo@latest swarm init \
  --topology hierarchical \
  --strategy specialized \
  --consensus raft \
  --max-agents 8
```

### 1.17 [21/26] Workers ✗

**症状**：`Expected 12 workers, found 5`

**修复**：

```bash
npx --yes ruflo@latest init upgrade --add-missing
npx --yes ruflo@latest doctor --no-color 2>&1 | grep "Workers"
```

### 1.18 [22/26] Plugins ✗

**症状**：`5 core plugins missing` / `Plugin manifest invalid`

详见 §7「插件问题」。

### 1.19 [23/26] Disk usage ✗

**症状**：`Disk usage 4.2 GB > 1 GB threshold`

**修复**：

```bash
# 1. 看哪些文件大
du -sh .claude-flow/memory/* 2>&1 | sort -hr | head -10

# 2. 清过期内存（默认 30 天）
npx --yes ruflo@latest memory gc --older-than 30d --no-color

# 3. 压缩 HNSW
npx --yes ruflo@latest hooks consolidate --target hnsw --compact

# 4. 手动清 pattern cache
rm -rf .claude-flow/cache/patterns/*.tmp
```

### 1.20 [24/26] Daemon ⚠ / [25/26] Federation ⚠

**症状**：`Daemon not started` / `Federation not configured`

**原因**：这两项是 `[OPTIONAL]`，**不算 FAIL**。

**修复（如需启用）**：

```bash
# Daemon
npx --yes ruflo@latest daemon start --no-color 2>&1 | tail -5
npx --yes ruflo@latest status  # 看是否 running

# Federation（详见 ch09）
npx --yes ruflo@latest federation init --peer wss://peer.example.com:443
```

### 1.21 [26/26] Witness manifest ✗

**症状**：`Ed25519 signature invalid` / `Manifest hash mismatch`

**修复**：

```bash
# 1. 详细输出
npx --yes ruflo@latest verify --verbose --no-color 2>&1 | tail -20

# 2. 若签名失败 → 重新装
npm install -g ruflo@latest --force
npx --yes ruflo@latest verify

# 3. 若 hash 不匹配 → 看哪个文件坏
npx --yes ruflo@latest verify --diff --no-color

# 4. 重装坏的包
npx --yes ruflo@latest plugins install <name> --force
```

---

## 2. Hooks 不触发

### 2.1 症状

- Claude Code 编辑文件后没看到「pre-edit / post-edit」日志
- `route` hook 没返回 topology 决策
- `session-start` 没注入历史偏好

### 2.2 排查（4 步）

```bash
# 1. 看 settings.json 里 hook 路径
cat .claude/settings.json | jq '.hooks'

# 期望：每个 hook 都有 matchers + hooks 数组
# 典型输出：
# {
#   "pre-edit": {
#     "matchers": [{"tools": ["Edit", "Write", "MultiEdit"]}],
#     "hooks": [{"type": "command", "command": "ruflo hooks pre-edit"}]
#   }
# }

# 2. 看 ruflo 自有 hooks
cat .claude-flow/hooks.json | jq .

# 期望：每个 hook 都有 enabled: true

# 3. 列 hooks 详情
npx --yes ruflo@latest hooks list --verbose --no-color 2>&1 | head -40

# 看：每个 hook 是否 active + 路径

# 4. 手动触发验证
npx --yes ruflo@latest hooks route --task "test" --no-color 2>&1 | tail -5
# 应返回 topology / consensus 决策
```

### 2.3 修复（按原因）

| 原因 | 修复 |
|------|------|
| settings.json 里 hook 路径拼错 | 重写：`init upgrade --add-missing` |
| hook 文件不可执行 | `chmod +x .claude/hooks/*.sh` |
| ruflo hooks 没启用 | `echo '{"enabled":true}' > .claude-flow/hooks.json` |
| Claude Code 版本太老（< 1.0） | 升级：`npm i -g @anthropic-ai/claude-code@latest` |
| 用户级 settings.json 覆盖 | `cat ~/.claude/settings.json | jq .` 看是否有 deny |

### 2.4 验证

```bash
# 在 Claude Code 里随便编辑一个文件
# 应该看到类似日志：
# [pre-edit] saving state for src/foo.ts
# [post-edit] pattern stored: edit.foo.ts

# 若没有 → 检查 .claude/hooks/ 下脚本是否被 chmod +x
ls -la .claude/hooks/ | grep -E "^-rwx"
```

---

## 3. MCP server 启动失败

### 3.1 症状

```
Error: MCP server ruflo failed to start
  - transport: stdio
  - exit code: 1
  - stderr: "Error: EADDRINUSE :::3000"
```

### 3.2 排查（按错误类型）

#### 类型 A：端口冲突（HTTP 模式）

**症状**：`EADDRINUSE :::3000` 或 `EADDRINUSE :::3001`

**修复**：

```bash
# 1. 看谁占用
lsof -i :3000
# 或
sudo lsof -iTCP -sTCP:LISTEN -P | grep 3000

# 2. 改端口
export CLAUDE_FLOW_MCP_PORT=3010
echo 'export CLAUDE_FLOW_MCP_PORT=3010' >> ~/.zshrc

# 3. 重启
pkill -f "ruflo mcp"
npx --yes ruflo@latest mcp start

# 4. 验证
curl -s http://localhost:3010/health | jq .
```

#### 类型 B：stdio pipe 错误

**症状**：`pipe broken` / `EPIPE` / `stdio closed`

**修复**：

```bash
# 1. 确认 stdin 没被外部关闭
# Claude Code 通常用 `npx ... | claude-code`，不能有 `< /dev/null`

# 2. 改用 JSON-RPC 直接调用
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  npx --yes ruflo@latest mcp start 2>&1 | jq .

# 3. 若 Claude Code 仍报 → 重启 Claude Code
# macOS: Cmd+Q 重开
# VSCode: Reload Window
```

#### 类型 C：JSON-RPC framing 错误

**症状**：`Parse error: Unexpected token` / `Invalid JSON-RPC 2.0 request`

**修复**：

```bash
# 1. 检查请求格式（必须 Content-Length 头）
printf 'Content-Length: 47\r\n\r\n{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  npx --yes ruflo@latest mcp start

# 2. 或用 ndjson 格式（ruflo 自动接受）
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  npx --yes ruflo@latest mcp start

# 3. 看 MCP 协议版本
npx --yes ruflo@latest mcp status | grep -i version
```

### 3.3 通用重启流程

```bash
# 杀所有 ruflo 进程
pkill -f "ruflo" || true
sleep 2

# 清缓存
rm -rf /tmp/ruflo-* ~/.cache/ruflo/ 2>/dev/null

# 重启 MCP
npx --yes ruflo@latest mcp start --verbose

# 验证
npx --yes ruflo@latest mcp status
```

---

## 4. Federation 连接超时

### 4.1 症状

```
Error: Federation peer unreachable
  - peer: wss://peer.example.com:443
  - timeout: 30s
  - reason: TLS handshake failed: certificate expired
```

或：

```
Error: TRUST_INSUFFICIENT
  - peer trust level: VERIFIED
  - required: TRUSTED
```

或：

```
Error: BUDGET_EXCEEDED
  - maxHops: 8
  - maxTokens: 50000
  - used: 52341 tokens
```

### 4.2 排查（按类型）

#### 类型 A：mTLS 证书过期

```bash
# 1. 看证书到期日
openssl x509 -in ~/.ruflo/federation/certs/peer.crt -noout -dates

# 2. 重新生成
npx --yes ruflo@latest federation cert rotate --peer <X>

# 3. 重连
npx --yes ruflo@latest federation connect <peer>
```

#### 类型 B：信任等级不够

```bash
# 1. 看对方 trust level
npx --yes ruflo@latest federation peer info <peer> 2>&1 | grep "trust"

# 2. 提升信任
# 方式 1：给对方 ATTESTED 证书
npx --yes ruflo@latest federation attest <peer> --reason "需要部署权限"

# 方式 2：基于行为历史自动升（100+ 成功任务后）
# 这会自动发生，无需手动操作

# 3. 重试
npx --yes ruflo@latest federation call <peer> --tool <X>
```

#### 类型 C：预算熔断触发（ADR-097）

```bash
# 1. 看当前预算
npx --yes ruflo@latest federation budget --peer <X> --no-color 2>&1 | tail -10

# 输出示例：
#   maxHops: 8 (used: 8)
#   maxTokens: 50000 (used: 52341)  ← 触发熔断
#   window: 60s

# 2. 等熔断窗口结束（默认 60s）或调大
npx --yes ruflo@latest federation config set \
  --peer <X> \
  --max-tokens 100000 \
  --max-hops 12

# 3. 或拆分任务到多个 peer
npx --yes ruflo@latest federation shard --peer <X> --parts 3
```

### 4.3 网络层排查

```bash
# 1. 看 WireGuard mesh 状态
npx --yes ruflo@latest federation mesh status

# 2. 测连通性
ping <peer-ip>
nc -zv <peer-ip> 443

# 3. 看 wg 接口
sudo wg show

# 4. 重启 mesh
sudo wg-quick down wg0 && sudo wg-quick up wg0
```

---

## 5. 性能抖动

### 5.1 CPU 飙高

**症状**：`top` 显示 `node` 进程 CPU > 80%

**排查**：

```bash
# 1. 找到 ruflo 进程
PID=$(pgrep -f "ruflo" | head -1)
echo "PID: $PID"

# 2. 看 CPU 占用
top -p $PID

# 3. 看哪个线程占
top -H -p $PID

# 4. 取堆栈（macOS）
kill -USR1 $PID  # 触发 heap dump 到 /tmp/

# 5. 看 flamegraph
npx --yes ruflo@latest profile cpu --duration 30s --no-color 2>&1 | tail -30
```

**修复**：

```bash
# A. 关掉没用的 worker
npx --yes ruflo@latest worker stop audit  # 暂时停
npx --yes ruflo@latest worker list       # 看哪些在跑

# B. 降 HNSW efSearch（牺牲精度换速度）
npx --yes ruflo@latest memory config set --ef-search 30  # 默认 50

# C. 限制并发 agent 数
npx --yes ruflo@latest swarm config set --max-concurrent-agents 4
```

### 5.2 内存泄漏

**症状**：Node 进程 RSS 持续增长，> 2GB

**排查**：

```bash
# 1. 看 RSS
ps -o rss= -p $(pgrep -f ruflo)

# 2. Heap dump
kill -USR2 $(pgrep -f ruflo)  # dump 到 ~/.ruflo/dumps/

# 3. 用 clinic.js 分析
npx clinic doctor -- npx ruflo@latest mcp start

# 4. 看哪些对象占内存
node --inspect-brk=0.0.0.0:9229 bin/ruflo.js
# Chrome → chrome://inspect
```

**修复**：

```bash
# A. 重启 MCP server（最快）
pkill -f "ruflo mcp"
npx --yes ruflo@latest mcp start &

# B. 清 .rvf cache
rm -rf .claude-flow/cache/*.tmp
npx --yes ruflo@latest memory gc --older-than 7d

# C. 升 Node（V8 GC 改进）
nvm install 22 && nvm use 22

# D. 显式调小 HNSW 缓存
npx --yes ruflo@latest memory config set --hnsw-cache-mb 256  # 默认 512
```

### 5.3 磁盘占满

**症状**：`No space left on device` / `.claude-flow/memory/*.rvf > 1 GB`

**排查**：

```bash
# 1. 看哪些文件大
du -sh .claude-flow/memory/* 2>&1 | sort -hr | head -10

# 2. 详细到子目录
du -sh .claude-flow/memory/*/ 2>&1 | sort -hr | head -10

# 3. 看 .rvf 内部
npx --yes ruflo@latest memory inspect --file .claude-flow/memory/project.rvf --no-color 2>&1 | tail -20
```

**修复**：

```bash
# A. 清过期内存
npx --yes ruflo@latest memory gc --older-than 30d

# B. 压缩 HNSW
npx --yes ruflo@latest hooks consolidate --target hnsw --compact

# C. 清错误日志（常有冗余）
rm -rf .claude-flow/logs/*.log.gz

# D. 删失败的 pattern
npx --yes ruflo@latest memory delete --where "success=false AND created_at < now-30d"

# E. 终极方案：迁移到新目录
mv .claude-flow/memory .claude-flow/memory.bak
npx --yes ruflo@latest init upgrade --add-missing
```

---

## 6. 数据迁移

### 6.1 USERGUIDE → v3 schema 变更

**背景**：ruflo v3 重写了内存 schema（从 `claude-flow-v2` → `claude-flow-v3`），老的 `.rvf` 文件需要转换。

**症状（升级后）**：

```
Error: Schema mismatch: expected v3, found v2
  - file: .claude-flow/memory/project.rvf
  - migration required
```

**迁移流程**：

```bash
# 1. 备份（重要！）
cp -r .claude-flow/memory .claude-flow/memory.v2.bak

# 2. 跑迁移
npx --yes ruflo@latest migrate v2-to-v3 --no-color 2>&1 | tail -20

# 输出：
#   Migrating: project.rvf ... ✓ (1234 keys)
#   Migrating: local.rvf ... ✓ (567 keys)
#   Migrating: user.rvf ... ✓ (89 keys)
#   ✓ migration complete in 4.2s

# 3. 验证
npx --yes ruflo@latest memory list --no-color 2>&1 | tail -10
npx --yes ruflo@latest doctor --no-color 2>&1 | grep "Memory"

# 4. 删备份（确认 OK 后）
rm -rf .claude-flow/memory.v2.bak
```

### 6.2 增量升级（添加缺失文件）

**背景**：从旧版升级时，新增的 skills / hooks / agents 没装上。

**症状**：`doctor` 报「Expected 134 skills, found 80」。

**修复**：

```bash
# 1. 备份当前配置
cp -r .claude .claude.bak
cp -r .claude-flow .claude-flow.bak

# 2. 增量升级
npx --yes ruflo@latest init upgrade --add-missing --no-color 2>&1 | tail -30

# 输出：
#   [1/12] Adding 54 missing skills ... ✓
#   [2/12] Adding 3 missing hooks ... ✓
#   [3/12] Adding 2 missing agents ... ✓
#   ...
#   ✓ upgrade complete in 12s

# 3. 验证
npx --yes ruflo@latest doctor --no-color 2>&1 | tail -10

# 4. 若升级破坏 → 回滚
rm -rf .claude .claude-flow
mv .claude.bak .claude
mv .claude-flow.bak .claude-flow
```

### 6.3 跨机器迁移（备份恢复）

**场景**：A 机器的内存要搬到 B 机器。

```bash
# A 机器：导出
tar czf ruflo-memory-$(date +%Y%m%d).tgz \
  .claude-flow/memory/ \
  ~/.claude-flow/memory/ \
  ~/.config/ruflo/memory/

# B 机器：导入
tar xzf ruflo-memory-20260723.tgz -C ~/
# 注意：要把 .claude-flow/memory/ 放到当前项目根，~ 路径放到 ~

# 验证
npx --yes ruflo@latest memory list --no-color 2>&1 | tail -10
```

### 6.4 升级失败回滚

```bash
# 1. 看 init 留下的 backup（init 通常自动备份）
ls -la .claude-flow/backup/ 2>&1 | head -10

# 2. 手动回滚
BACKUP=$(ls -t .claude-flow/backup/ | head -1)
mv .claude-flow "$BACKUP.current"
mv ".claude-flow/backup/$BACKUP" .claude-flow

# 3. 重启 MCP
pkill -f "ruflo mcp"
npx --yes ruflo@latest mcp start

# 4. 验证
npx --yes ruflo@latest doctor --no-color
```

---

## 7. 插件问题

### 7.1 插件装不上

**症状**：`plugins install ruflo-federation` 失败。

**修复**：

```bash
# 1. 看错误
npx --yes ruflo@latest plugins install ruflo-federation --verbose --no-color 2>&1 | tail -20

# 2. 检查网络
curl -fsSL https://registry.npmjs.org/ruflo-plugin-federation | jq .

# 3. 清缓存重装
npm cache clean --force
npx --yes ruflo@latest plugins install ruflo-federation --force

# 4. 手动装（最后手段）
npm install -g @claude-flow/plugin-agent-federation
```

### 7.2 插件冲突

**症状**：`Plugin X conflicts with plugin Y: both register hook "post-task"`

**修复**：

```bash
# 1. 禁用冲突的
npx --yes ruflo@latest plugins disable <Y>

# 2. 或选一个优先级更高的
npx --yes ruflo@latest plugins config set <X> --priority high

# 3. 看 hook 注册表
npx --yes ruflo@latest hooks list --verbose 2>&1 | grep "post-task"
```

### 7.3 插件版本不兼容

**症状**：`Plugin ruflo-neural@1.0 requires ruflo >= 3.30, found 3.29`

**修复**：

```bash
# A. 升级 ruflo
npm install -g ruflo@latest

# B. 或降插件
npx --yes ruflo@latest plugins install ruflo-neural@0.9 --force

# C. 看兼容矩阵
npx --yes ruflo@latest plugins compat --no-color 2>&1 | tail -20
```

### 7.4 插件 doctor 失败

**症状**：`plugins doctor` 报 `Plugin X manifest missing`。

**修复**：

```bash
# 1. 重装
npx --yes ruflo@latest plugins install <X> --force

# 2. 验证
npx --yes ruflo@latest plugins doctor --verbose 2>&1 | tail -20
```

---

## 8. Swarm 跑飞

### 8.1 症状

- Swarm 跑了 10 分钟没进度
- Agents 互相 deadlock
- Memory 命名空间爆炸（> 1000 keys）

### 8.2 修复

```bash
# 1. 看 swarm 状态
npx --yes ruflo@latest swarm status --no-color 2>&1 | tail -30

# 2. 终止卡住的 agent
npx --yes ruflo@latest agent kill --all --reason "stuck > 5min"

# 3. 重置共识状态
npx --yes ruflo@latest swarm consensus reset

# 4. 减少 max agents
npx --yes ruflo@latest swarm config set --max-agents 4  # 从 8 降到 4

# 5. 重新启动（更小）
npx --yes ruflo@latest swarm init \
  --topology hierarchical \
  --strategy specialized \
  --consensus raft \
  --max-agents 4
```

详见 [ch06 · Anti-Drift 默认](./06-swarm-coordination.md)。

---

## 9. 紧急修复流程（5 分钟复活）

当一切都不工作时，按这个顺序执行：

```bash
# 1. 杀进程
pkill -f "ruflo" || true
pkill -f "claude" || true
sleep 2

# 2. 清缓存（不删配置）
rm -rf /tmp/ruflo-* ~/.cache/ruflo/ .claude-flow/cache/ 2>/dev/null

# 3. 重跑 init（幂等）
cd /path/to/project
npx --yes ruflo@latest init --non-interactive --skip-prompts 2>&1 | tail -10

# 4. 跑 doctor --fix
npx --yes ruflo@latest doctor --fix --no-color 2>&1 | tail -10

# 5. 跑 verify
npx --yes ruflo@latest verify --no-color 2>&1 | tail -5

# 6. 验证 MCP 注册
cat .mcp.json | jq .

# 7. 重启 Claude Code

# 8. 在 Claude Code 里跑 `/mcp__ruflo__mcp_status` 确认 314 个工具都在
```

如果还不行：

```bash
# 终极方案：完全重装
rm -rf .claude .claude-flow .mcp.json CLAUDE.md AGENTS.md
npx --yes ruflo@latest init --non-interactive --skip-prompts
npx --yes ruflo@latest doctor --fix
npx --yes ruflo@latest verify
```

---

## 10. 调试技巧汇总

### 10.1 看完整日志

```bash
# 启动时加 --verbose
npx --yes ruflo@latest init --verbose 2>&1 | tee /tmp/init.log

# MCP server 日志
npx --yes ruflo@latest mcp start --log-level debug \
  --log-file ~/.ruflo/logs/mcp.log

# Tail 实时
tail -f ~/.ruflo/logs/mcp.log
```

### 10.2 复现最小用例

```bash
# 沙箱内复现
bash sandbox/setup.sh debug
cd /tmp/ruflo-sandbox-debug
# 跑出问题的命令
npx --yes ruflo@latest <failing-command> --verbose
```

### 10.3 抓网络包

```bash
# 看 MCP stdio 流量
strace -e trace=read,write -f npx ruflo@latest mcp start 2>&1 | tail -50
# 或 macOS：
sudo dtrace -n 'syscall::read*:return { arg0 > 0 } { trace(arg0); }' -p $(pgrep -f ruflo)
```

### 10.4 启用调试模式

```bash
export RUFLO_DEBUG=1
export DEBUG=ruflo:*
export NODE_OPTIONS="--inspect-brk=0.0.0.0:9229"

npx --yes ruflo@latest mcp start
# Chrome → chrome://inspect → 进入调试
```

---

## 11. 错误码速查表

| 错误码 | 含义 | 详见 |
|--------|------|------|
| `EADDRINUSE` | 端口被占 | §3.2.A |
| `EPIPE` | stdio 关闭 | §3.2.B |
| `INVALID_JSON_RPC` | 协议错误 | §3.2.C |
| `CERT_EXPIRED` | mTLS 证书过期 | §4.2.A |
| `TRUST_INSUFFICIENT` | 信任不够 | §4.2.B |
| `BUDGET_EXCEEDED` | 预算熔断 | §4.2.C |
| `SCHEMA_MISMATCH` | 内存 schema 旧 | §6.1 |
| `PLUGIN_CONFLICT` | 插件 hook 冲突 | §7.2 |
| `PLUGIN_INCOMPATIBLE` | 插件版本不兼容 | §7.3 |
| `PLUGIN_MANIFEST_MISSING` | 插件清单缺失 | §7.4 |
| `SWARM_DEADLOCK` | swarm 死锁 | §8 |
| `NODE_VERSION_LOW` | Node 太老 | §1.1 |
| `MCP_UNREACHABLE` | MCP server 起不来 | §3 |
| `HNSW_CORRUPTION` | HNSW 损坏 | §1.11 |
| `WITNESS_INVALID` | 签名不通过 | §1.21 |

---

## 12. 获取帮助（升级路径）

按这个顺序尝试：

1. **本章** —— 90% 问题有现成方案
2. **doctor --fix** —— 60% 问题自动修
3. **`ruflo status`** —— 看全局状态
4. **GitHub Issues**：<https://github.com/ruvnet/ruflo/issues>
   - 标签：`docs-drift`（文档不对）、`bug`（BUG）、`needs-triage`（待分类）
5. **Discord**：<https://discord.gg/ruflo>
6. **邮件支持**：`support@ruvnet.org`（付费用户）

提 issue 时务必附上：

```bash
# 收集诊断信息
npx --yes ruflo@latest doctor --no-color > /tmp/doctor.log 2>&1
npx --yes ruflo@latest verify --no-color > /tmp/verify.log 2>&1
npx --yes ruflo@latest status --no-color > /tmp/status.log 2>&1
node --version > /tmp/env.log 2>&1
npm --version >> /tmp/env.log 2>&1
os=$(uname -a) && echo "$os" >> /tmp/env.log

# 打包
tar czf ruflo-debug-$(date +%Y%m%d).tgz /tmp/*.log

# 把 ruflo-debug-XXX.tgz 附到 issue
```

---

## 13. 小结

### 关键要点

- **26 项 doctor 检查** 是第一道防线，60% 问题 `doctor --fix` 即可
- 7 类常见错误：doctor / hooks / MCP / 联邦 / 性能 / 数据 / 插件
- **性能抖动三剑客**：CPU（top）/ 内存（heap dump）/ 磁盘（du -sh）
- **数据迁移两步走**：备份 → `init upgrade --add-missing`
- **紧急修复 5 分钟**：杀进程 → 清缓存 → 重跑 init → doctor --fix → verify

### 术语锚点

- doctor 26 项 → [ch02](./02-install-and-init.md)
- Hooks (17) → [ch11](./11-hooks-and-workers.md)
- MCP server → [ch04](./04-architecture-deep-dive.md)
- Federation → [ch09](./09-federation.md)
- mTLS / Trust Ladder → [ch09](./09-federation.md)
- Witness → [ch10](./10-security-and-aidefence.md)
- Plugin (33) → [ch12](./12-plugin-ecosystem.md)

### 下一步

👉 进入 [第 19 章 引用与版本快照](./19-references.md)，看官方文档索引 + ADR 全表 + 版本兼容矩阵。

### 参考链接

- 官方 Troubleshooting：<https://github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md#troubleshooting>
- Doctor 源码：`v3/@claude-flow/cli/src/commands/doctor.ts`
- Doctor 检查注册表：`v3/@claude-flow/cli/src/doctor/checks/*.ts`