#!/usr/bin/env bash
# sandbox/verify-chapter.sh — 统一章节断言入口
#
# 设计：每个章节的 hands-on 都在沙箱内跑命令，期望产出 stdout/stderr。
# 本脚本包装「运行 → 抓输出 → 比对期望」三段式，并在控制台打印 PASS/FAIL。
#
# 用法：
#   bash sandbox/verify-chapter.sh <chapter-number>
# 例：
#   bash sandbox/verify-chapter.sh 2
#   bash sandbox/verify-chapter.sh all   # 跑全章节（耗时长）

set -uo pipefail

CHAPTER="${1:-all}"
HANDBOOK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUFLO_SRC="/Users/digoal/new/ruflo"

# macOS 没有 timeout 命令，做个轻量包装
_timeout() {
  local secs="$1"; shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "$secs" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$secs" "$@"
  else
    # 后台跑 + sleep + kill
    "$@" &
    local pid=$!
    ( sleep "$secs" && kill -9 "$pid" 2>/dev/null ) &
    local watchdog=$!
    wait "$pid"
    local rc=$?
    kill -9 "$watchdog" 2>/dev/null || true
    return "$rc"
  fi
}

# 加载该章节专属断言
declare -a ASSERT_NAMES=()
declare -a ASSERT_FUNCS=()

PASS=0
FAIL=0

note() { printf "\033[1;34m▸\033[0m %s\n" "$*"; }
ok()   { printf "\033[1;32m✓\033[0m %s\n" "$*"; PASS=$((PASS+1)); }
bad()  { printf "\033[1;31m✗\033[0m %s\n" "$*"; FAIL=$((FAIL+1)); }

# 工具：判断 ruflo 是否能跑（npx 首次启动可能耗时 1-3 分钟）
ruflo_ok() {
  _timeout 240 npx --yes ruflo@latest --version >/dev/null 2>&1
}

# === 通用断言（任何章节都先跑） ===
note "通用断言：ruflo CLI 可用"
if ruflo_ok; then
  ok "ruflo --version 通过"
  RUFLO_VER="$(_timeout 240 npx --yes ruflo@latest --version 2>&1 | head -1)"
  note "  → 当前版本: $RUFLO_VER"
else
  bad "ruflo --version 失败；请检查网络或代理"
  note "  → 可执行: npm config get registry"
  note "  → 备选：本地源码 build (cd /Users/digoal/new/ruflo/v3/@claude-flow/cli && npm run build)"
  exit 1
fi

note "通用断言：ruflo 源码可达"
if [[ -d "$RUFLO_SRC/v3/@claude-flow/cli" ]]; then
  ok "$RUFLO_SRC 存在 v3 monorepo"
  COMMIT="$(git -C "$RUFLO_SRC" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  note "  → 当前 commit: $COMMIT"
else
  bad "找不到 ruflo 源码 $RUFLO_SRC；请确认路径"
  exit 1
fi

# === assert 函数（章节脚本可调用） ===
# 用法：assert "描述" <期望退出码> <命令...>
assert() {
  local desc="$1"
  local expect="${2:-0}"
  shift 2 || true
  if "$@" >/tmp/sbx-out.log 2>&1; then
    local actual=0
  else
    local actual=$?
  fi
  if [[ "$actual" -eq "$expect" ]]; then
    ok "Chapter $CHAPTER: $desc"
  else
    bad "Chapter $CHAPTER: $desc（实际 exit $actual，期望 $expect）"
    tail -8 /tmp/sbx-out.log | sed 's/^/    /'
  fi
}

# === 章节特定断言 ===
load_chapter_assertions() {
  local ch="$1"
  local fn_file="$HANDBOOK_ROOT/sandbox/asserts/ch${ch}.sh"
  if [[ -f "$fn_file" ]]; then
    note "加载章节断言: $fn_file"
    # shellcheck source=/dev/null
    source "$fn_file"
  else
    note "章节 $ch 没有专属断言（$fn_file 不存在）"
  fi
}

case "$CHAPTER" in
  0|all) load_chapter_assertions "0" ;;
  1|all) load_chapter_assertions "1" ;;
  2|all) load_chapter_assertions "2" ;;
  3|all) load_chapter_assertions "3" ;;
  *)     load_chapter_assertions "$CHAPTER" ;;
esac

echo ""
echo "════════════════════════════════════════"
printf "\033[1m结果：PASS=%d  FAIL=%d\033[0m\n" "$PASS" "$FAIL"
if [[ "$FAIL" -eq 0 ]]; then
  ok "Chapter $CHAPTER: 全部通过"
  exit 0
else
  bad "Chapter $CHAPTER: $FAIL 个断言失败"
  exit 1
fi