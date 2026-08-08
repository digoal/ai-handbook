# Ruflo 手册沙箱（Sandbox）

本目录提供两种沙箱方案，供不同环境用户选用：

| 方案 | 适用场景 | 启动命令 |
|------|---------|----------|
| **本地模式** `setup.sh` | 主机无 Docker / 想轻量验证 | `bash sandbox/setup.sh` |
| **Docker 模式** `Dockerfile` | 主机有 Docker daemon | `docker build -t ruflo-sandbox sandbox/ && docker run --rm -it -v $(pwd):/handbook ruflo-sandbox` |

两种方案共用 `verify-chapter.sh` 断言模板与 `sandbox/fixtures/demo-repo/` 演示仓库。

## 工作区结构

沙箱初始化后会在 `/tmp/ruflo-sandbox-default/` 产生：

```
/tmp/ruflo-sandbox-default/
├── src/                 # demo-repo 副本（含 TS / Python / Markdown 文件）
├── .mcp.json             # mock LLM 配置
├── CLAUDE.md             # ruflo init 生成
├── .claude/              # hooks / settings / skills
├── .claude-flow/         # memory / config
├── bin/                  # 自定义脚本
├── logs/                 # 沙箱内日志
├── bootstrap.sh          # 一键 init + 装 5 个核心插件
└── verify-chapter.sh     # 章节断言（通用部分）
```

## 章节断言文件位置

每个章节的专属断言放在 `sandbox/asserts/ch{N}.sh`，由 `verify-chapter.sh` 自动 source。

```
sandbox/asserts/
├── ch0.sh    # 通用（CLI 可用 / 源码可达）
├── ch2.sh    # 第 2 章专属（init 可重入、doctor --fix 幂等）
├── ch3.sh    # 第 3 章专属（hooks 自动触发）
└── ...
```

每个 `ch{N}.sh` 文件用 `assert "<描述>" <exit_code> <命令...>` 注册断言：

```bash
# sandbox/asserts/ch2.sh
assert "init --non-interactive 可重入" 0 bash -c '
  cd /tmp/ruflo-sandbox-default
  timeout 120 npx --yes ruflo@latest init --non-interactive 2>&1 | grep -q "already initialized\|initialized successfully"
'

assert "doctor --fix 幂等" 0 bash -c '
  timeout 60 npx --yes ruflo@latest doctor --fix --no-color 2>&1 | grep -qE "(fixed|up to date)"
'
```

## 版本快照

每章在 `verify-chapter.sh` 跑通时记录：

```
✓ 通用断言：ruflo CLI 可用
  → 当前版本: ruflo v3.32.9
✓ 通用断言：ruflo 源码可达
  → 当前 commit: 26c35b59
▸ Chapter 2: init --non-interactive 可重入
  ✓ PASS (exit 0)
▸ Chapter 2: doctor --fix 幂等
  ✓ PASS (exit 0)

════════════════════════════════════════
结果：PASS=4  FAIL=0
✓ Chapter 2: 全部通过
```

如果 `ruflo --version` 与某章 `LAST_VERIFIED_AGAINST` 字段不一致，需在该章顶部加 `[⚠ 待同步]` 横条。

## 网络隔离

沙箱默认**只允许**访问：

- `registry.npmjs.org` / `cdn.jsdelivr.net`（拉 ruflo / pnpm 包）
- `api.anthropic.com`（如设置了 ANTHROPIC_API_KEY；默认不开）

不调用真 LLM 时，所有 hands-on 都能跑通。需要在沙箱里调用 Claude/GPT 时：

```bash
# 在沙箱 .mcp.json 里加 key
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_FLOW_API_KEY="$ANTHROPIC_API_KEY"
```

## 数据清理

```bash
rm -rf /tmp/ruflo-sandbox-default
docker rmi ruflo-sandbox   # 仅 Docker 模式
```

## 故障排查

| 现象 | 可能原因 | 解决 |
|------|---------|------|
| `npx ruflo@latest --version` 超时 | 网络封锁 npm | `npm config set registry https://registry.npmmirror.com` |
| `ruflo init` 卡在 prompt | 没传 `--non-interactive` | 加 `--skip-prompts --non-interactive` |
| `doctor` 报 `LLM_API_KEY missing` | 沙箱无 LLM key | 预期红，标 `[EXPECTED]`；或注入 mock provider |
| hooks 不触发 | init 没跑完 | `bash sandbox/setup.sh` 重新跑 |