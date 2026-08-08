# Examples · 7 仓真实 benchmark 汇总

> CodeGraph Handbook Ch09 配套真实跑分报告。每个子目录是当前 commit + cg 1.5.0 的实测数据。

## 汇总表

| 仓库 | 目录 | commit | 索引(nodes/edges) | 探针 sym / files / tokens~ / time | Ch09 引用 | 状态 |
|------|------|--------|------------------|-----------------------------------|----------|------|
| microsoft/vscode | [vscode-extension-host](vscode-extension-host/README.md) | `74dc74c` | 17,951 / 56,312 | 45 / 3 / 5,393 / 0.31 s | 1 / 1 / 1,638 / 0.15 s | ⚠ |
| excalidraw/excalidraw | [excalidraw-canvas](excalidraw-canvas/README.md) | `b2e81e3` | 9,852 / 43,698 | 74 / 1 / 6,320 / 0.28 s | 1 / 1 / 1,433 / 0.14 s | ⚠ |
| django/django | [django-orm](django-orm/README.md) | `957d0ce` | 2,816 / 7,110 | 83 / 2 / 4,802 / 0.20 s | 0 / 0 / 42 / 0.14 s | ⚠ |
| tokio-rs/tokio | [tokio-runtime](tokio-runtime/README.md) | `6a05877` | 2,601 / 7,800 | 78 / 5 / 3,974 / 0.20 s | 0 / 0 / 41 / 0.14 s | ⚠ |
| square/okhttp | [okhttp-interceptors](okhttp-interceptors/README.md) | `e005148` | 19,115 / 50,520 | 55 / 4 / 5,021 / 0.34 s | 1 / 1 / 885 / 0.14 s | ⚠ |
| gin-gonic/gin | [gin-middleware](gin-middleware/README.md) | `34dac20` | 1,504 / 5,208 | 82 / 3 / 2,418 / 0.19 s | 82 / 3 / 2,603 / 0.17 s | ✓ |
| Alamofire/Alamofire | [alamofire-request](alamofire-request/README.md) | `903c53c` | 2,052 / 4,285 | 61 / 3 / 3,383 / 0.19 s | 0 / 0 / 40 / 0.14 s | ⚠ |

**符号说明**:
- `⚠` 探针数字与 Ch09 章节引用数字差异显著 — 子目录 README 给出真实数据 + 差异说明
- `✓` 探针数字与 Ch09 引用一致

## Ch09 章节 vs 真实探针 差异

Ch09 §9.3.1–9.3.7 引用的"实测"数字(1/1/1638/0.15s 等)来自早期探针版本;`examples/<dir>/README.md` 提供当前 commit + cg 1.5.0 的真实数字。差异主要来源:

1. **commit 时差**:Ch09 引用多基于 2025-07 前后 commit,本次复现是 2026-07 HEAD,代码可能多了几层
2. **响应范围**:当前 `codegraph_explore` 默认回 5-10 个 symbols + 3-4 个文件 + blast radius,旧探针可能只回 1 个入口符号
3. **sparse-checkout 范围**:本次按"框架核心目录"做 sparse,而旧探针可能全收

## 索引规模与 git 操作

每个子目录 README 包含:
- 仓库地址 + commit SHA
- 完整 clone + sparse-checkout 命令
- `codegraph init` 的真实输出
- 2 次 `codegraph explore` 的真实响应(前 50 行)
- 单位换算:symbols/files/tokens≈(响应字节/4)/time
- 与 README 自报数据(89/69/60%)的差异说明

## 复现命令(通用)

```bash
# 1. 在隔离目录浅克隆
mkdir -p /tmp/eval-repos/<name> && cd /tmp/eval-repos/<name>
git clone --depth=1 --filter=blob:none --sparse <repo-url>
cd <repo>
git sparse-checkout set <relevant-paths>

# 2. 建索引
codegraph init

# 3. 预热 daemon
codegraph explore "warmup query"  # 不计入测试

# 4. 跑 2 次原 question
codegraph explore "<original README question>" --max-files 12
codegraph explore "<original README question>" --max-files 12

# 5. 统计
echo "lines: $(wc -l < output)"        # 行数
echo "bytes: $(wc -c < output)"        # 字节数
echo "tokens~: $(wc -c < output | awk '{print int($1/4)}')"  # 字节/4 估算
```

## 验收检查

- [x] 7 仓真实 README 全部写入(vscode / excalidraw / django / tokio / okhttp / gin / alamofire)
- [x] validation-log 同步追加 7 行
- [x] Ch09 引用路径全部修正为带后缀长名
- [x] Ch09 9.4.1 复现性声明段已加
- [x] 7 个早期 stub README 已清理
- [x] examples/README.md 汇总表完整
