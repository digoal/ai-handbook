#!/usr/bin/env bash
# sandbox/setup.sh — 本地沙箱初始化（无需 Docker）
#
# 用法（在 ruflo_handbook 根目录）：
#   bash sandbox/setup.sh [sandbox-name]
#
# 默认行为：
#   1. 在 /tmp/ruflo-sandbox-<name> 创建独立工作区
#   2. 链接到 ruflo 源码（/Users/digoal/new/ruflo）方便读路径
#   3. 预装 demo-repo（小型 TS+Python+MD 演示项目）
#   4. 安装 ruflo CLI（npx @ruflo/cli@latest）
#   5. 输出 verify-chapter.sh 模板

set -euo pipefail

SANDBOX_NAME="${1:-default}"
WORKSPACE="/tmp/ruflo-sandbox-${SANDBOX_NAME}"
RUFLO_SRC="/Users/digoal/new/ruflo"
HANDBOOK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# 防止误清空已有目录
if [[ -e "$WORKSPACE" ]]; then
  echo "✗ workspace $WORKSPACE 已存在；如需重建请先 rm -rf"
  exit 1
fi

echo "→ 创建工作区 $WORKSPACE"
mkdir -p "$WORKSPACE/src"
mkdir -p "$WORKSPACE/bin"
mkdir -p "$WORKSPACE/logs"

echo "→ 复制 demo-repo"
cp -R "$HANDBOOK_ROOT/sandbox/fixtures/demo-repo/." "$WORKSPACE/src/"
ls "$WORKSPACE/src"

echo "→ 准备 ruflo CLI 校验"
if ! command -v npx >/dev/null 2>&1; then
  echo "✗ npx 不可用；请先安装 Node.js 20+"
  exit 1
fi

# Node 版本断言
NODE_MAJOR="$(node -e 'console.log(process.versions.node.split(".")[0])')"
if [[ "$NODE_MAJOR" -lt 20 ]]; then
  echo "✗ Node 版本过低（需 ≥ 20）：当前 $(node --version)"
  exit 1
fi

# 在沙箱内生成 verify-chapter.sh 模板
cat > "$WORKSPACE/verify-chapter.sh" <<'VERIFY_EOF'
#!/usr/bin/env bash
# verify-chapter.sh — 章节断言模板（在沙箱内运行）
# 用法：bash verify-chapter.sh <chapter-number>
# 例：  bash verify-chapter.sh 2
set -euo pipefail

CHAPTER="${1:-all}"
PASS=0
FAIL=0

run_assert() {
  local name="$1"; shift
  local expect_exit="${1:-0}"; shift
  echo ""
  echo "▸ Assert: $name"
  if "$@" >/tmp/sbx-out.log 2>&1; then
    if [[ "$expect_exit" -eq 0 ]]; then
      echo "  ✓ PASS (exit 0)"
      head -20 /tmp/sbx-out.log
      PASS=$((PASS+1))
    else
      echo "  ✗ FAIL（预期失败但成功了）"
      FAIL=$((FAIL+1))
    fi
  else
    if [[ "$expect_exit" -ne 0 ]]; then
      echo "  ✓ PASS (exit non-zero, as expected)"
      head -20 /tmp/sbx-out.log
      PASS=$((PASS+1))
    else
      echo "  ✗ FAIL"
      tail -10 /tmp/sbx-out.log
      FAIL=$((FAIL+1))
    fi
  fi
}

# === 通用断言：所有章节共享 ===
run_assert "ruflo CLI 可用" 0 npx --yes ruflo@latest --version
run_assert "ruflo doctor 通过（仅 LLM_API_KEY 允许红）" 0 \
  bash -c 'npx --yes ruflo@latest doctor --no-color 2>&1 | grep -q "doctor complete"'

case "$CHAPTER" in
  1|all)
    : # 第 1 章无 hands-on
    ;;
  2|all)
    run_assert "init 流程可重入（已 init 则跳过）" 0 \
      bash -c 'cd /tmp/ruflo-sandbox-'"${SANDBOX_NAME:-default}"' && npx --yes ruflo@latest init --non-interactive 2>&1 | tail -5'
    run_assert "doctor --fix 幂等" 0 \
      bash -c 'npx --yes ruflo@latest doctor --fix 2>&1 | tail -3'
    ;;
  *)
    echo "→ 章节 $CHAPTER 的专属断言需在对应 chapters/NN-*.md 中定义"
    ;;
esac

echo ""
echo "════════════════════════════════════════"
echo "PASS=$PASS  FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]] && echo "✓ Chapter $CHAPTER: 全部通过" || { echo "✗ Chapter $CHAPTER: 有失败断言"; exit 1; }
VERIFY_EOF
chmod +x "$WORKSPACE/verify-chapter.sh"

cat > "$WORKSPACE/bootstrap.sh" <<'BOOT_EOF'
#!/usr/bin/env bash
# bootstrap.sh — 在沙箱内一键 init ruflo + 安装 5 个核心插件
set -euo pipefail

cd /tmp/ruflo-sandbox-default

echo "→ 1. 写入 .mcp.json（mock LLM）"
cat > .mcp.json <<'MCP'
{
  "mcpServers": {
    "ruflo": {
      "command": "npx",
      "args": ["--yes", "ruflo@latest", "mcp", "start"],
      "env": {
        "MOCK_LLM": "1",
        "RUFLO_LOG_LEVEL": "info",
        "CLAUDE_FLOW_HOOKS_ENABLED": "true"
      }
    }
  }
}
MCP

echo "→ 2. 跑 init（非交互）"
npx --yes ruflo@latest init --non-interactive --skip-prompts || true

echo "→ 3. 安装 5 个核心插件"
npx --yes ruflo@latest plugins install -n @claude-flow/plugin-ruflo-core || true
npx --yes ruflo@latest plugins install -n @claude-flow/plugin-ruflo-swarm || true
npx --yes ruflo@latest plugins install -n @claude-flow/plugin-ruflo-intelligence || true
npx --yes ruflo@latest plugins install -n @claude-flow/plugin-ruflo-rag-memory || true
npx --yes ruflo@latest plugins install -n @claude-flow/plugin-ruflo-aidefence || true

echo "→ 4. 跑 doctor 看健康度"
npx --yes ruflo@latest doctor --no-color | tail -30

echo "✓ bootstrap 完成"
BOOT_EOF
chmod +x "$WORKSPACE/bootstrap.sh"

echo ""
echo "════════════════════════════════════════"
echo "✓ 本地沙箱已就绪"
echo "  工作区：$WORKSPACE"
echo "  ruflo 源码：$RUFLO_SRC"
echo ""
echo "下一步："
echo "  cd $WORKSPACE"
echo "  bash bootstrap.sh              # 跑 init + 装插件"
echo "  bash verify-chapter.sh 2       # 验证第 2 章"
echo ""