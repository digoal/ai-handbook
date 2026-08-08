#!/usr/bin/env bash
# sandbox/entrypoint.sh — Docker 沙箱入口
# 默认行为：跑一次 smoke test 后进入 bash

set -e

cd /handbook

echo "════════════════════════════════════════"
echo " Ruflo Handbook Sandbox"
echo " Node:    $(node --version)"
echo " npm:     $(npm --version)"
echo " ruflo:   $(ruflo --version 2>&1 || echo 'not yet installed')"
echo " Workdir: $(pwd)"
echo "════════════════════════════════════════"

# 自动跑一次 verify 模板（章节 0 = 通用）
if [[ -f /handbook/sandbox/verify-chapter.sh ]]; then
  echo ""
  echo "→ 跑 sandbox/verify-chapter.sh（默认 = chapter=0 仅检查 CLI 可用）"
  bash /handbook/sandbox/verify-chapter.sh 0 || true
fi

echo ""
echo "进入 bash。可执行："
echo "  cd /handbook && bash sandbox/verify-chapter.sh 2"
echo "  ruflo doctor"
echo "  ruflo status"
exec "$@"