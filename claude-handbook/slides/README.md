# Claude Code CLI Handbook 分享演示

本目录提供基于仓库 00–14 章制作的自包含 HTML 演示文稿，面向资深工程师，建议分享时长为 35–45 分钟。

- 主文件：[claude-code-cli-handbook-overview.html](claude-code-cli-handbook-overview.html)
- 内容规模：24 页主 deck + 4 页附录
- 内容基线：Claude Code 2.1.214、macOS 15.7.7、核验 2026-07-20
- 事实来源：仓库唯一事实台账 [SOURCES.md](../SOURCES.md)

## 打开方式

从仓库根目录执行：

```bash
open slides/claude-code-cli-handbook-overview.html
```

也可以直接把 HTML 文件拖入现代浏览器。文件内联了 CSS、JavaScript 与图形，不依赖 CDN、远程字体或 npm 构建，可离线打开。

## 操作

| 操作 | 快捷键 |
|------|--------|
| 上一页 / 下一页 | `←` / `→`、`PageUp` / `PageDown` |
| 下一页 | `Space` |
| 首页 / 末页 | `Home` / `End` |
| 切换深浅主题 | `T` |
| 进入或退出全屏 | `F` |
| 打印或导出 PDF | `P` |

页面 URL 使用 `#slide-N` 深链，例如 `#slide-15` 直接打开 Hooks 页。图表 mark 支持鼠标 hover 和键盘 focus；“查看数据表”提供不依赖颜色或 tooltip 的等价数据。

## 打印与 PDF

在 Chrome 中打开后使用打印功能，并启用“背景图形”。演示使用 16:9 打印页面，每个 slide 独占一页；交互控件、tooltip 与对话框不会进入打印结果。

也可以从命令行生成 PDF：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --disable-gpu \
  --print-to-pdf="$TMPDIR/claude-code-handbook-slides.pdf" \
  "file://$PWD/slides/claude-code-cli-handbook-overview.html"
```

PDF 是临时验收产物，不纳入仓库。

## 内容与引用规则

- 所有版本敏感命令、flag、默认值、路径、限制和 feature gate 都链接到 [SOURCES.md](../SOURCES.md) 中已有的 `CC-xxx`。
- “条件性”结论在同页标明订阅、认证、安装渠道、实验状态或组织策略条件。
- 演示文稿不是第二份事实台账；事实变化时先更新 `SOURCES.md`，再更新 deck。
- 演示范围与根 [README.md](../README.md) 一致，不把 Windows、Linux、WSL、Agent SDK、Anthropic API、Desktop、Web 或 IDE 当作主线。
- 不在演示中放入真实用户配置、凭证、绝对主目录、session transcript、agent 状态 JSON 或 debug log。

## 视觉与无障碍

- 使用中性的 light/dark surfaces、固定 categorical 顺序和单色 ordinal ramp，不宣称是 Claude 官方品牌视觉。
- 状态色始终配图标和文字；正文文本不使用 series color。
- 图表使用直接标签、legend、键盘 focus、tooltip 和等价数据表，不依赖颜色单独传达身份。
- `prefers-reduced-motion` 下关闭非必要动画。
- 每页使用语义化 section；图表和流程均提供可读标题、描述或 HTML 等价结构。

## 发布前验证

### 1. 检查事实引用

```bash
python3 - <<'PY'
from pathlib import Path
import re

html = Path("slides/claude-code-cli-handbook-overview.html").read_text()
sources = Path("SOURCES.md").read_text()
used = sorted(set(re.findall(r"CC-\d+", html)))
missing = [fact_id for fact_id in used if f"### {fact_id}" not in sources]
print(f"引用 {len(used)} 个事实 ID")
print("缺失：", missing)
PY
```

### 2. 检查 HTML、链接与敏感内容

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import re

path = Path("slides/claude-code-cli-handbook-overview.html")
text = path.read_text()
HTMLParser().feed(text)

links = re.findall(r'href="([^"#][^"]*)"', text)
missing = []
for href in links:
    target = (path.parent / href.split("#", 1)[0]).resolve()
    if not target.exists():
        missing.append(href)

assert not missing, missing
assert "/Users/" not in text
assert not re.search(r"sk-ant-|ghp_|xox[abp]-", text, re.I)
print("HTML 解析、相对链接和敏感模式检查通过")
PY
```

### 3. 验证调色板

使用 dataviz skill 的 `scripts/validate_palette.js`，分别验证：

```bash
node "$DATAVIZ_SKILL_DIR/scripts/validate_palette.js" \
  "#2a78d6,#008300,#e87ba4,#eda100,#1baf7a,#eb6834,#4a3aa7,#e34948" \
  --mode light

node "$DATAVIZ_SKILL_DIR/scripts/validate_palette.js" \
  "#3987e5,#008300,#d55181,#c98500,#199e70,#d95926,#9085e9,#e66767" \
  --mode dark

node "$DATAVIZ_SKILL_DIR/scripts/validate_palette.js" \
  "#86b6ef,#5598e7,#2a78d6,#1c5cab,#104281" \
  --ordinal --mode light
```

浅色 categorical 中对比度低于 3:1 的 series 仍须保留直接标签或等价数据表；不能把 validator 的 `WARN` 当作可忽略项。

### 4. 渲染抽检

至少检查以下页面：

- `#slide-1`：封面
- `#slide-4`：学习路线
- `#slide-6`：事实等级图表和数据表
- `#slide-12`：Permission × Sandbox 矩阵
- `#slide-16`：MCP 矩阵
- `#slide-18`：并行概念密集页
- `#slide-21`：版本门槛时间线
- `#slide-24`：主 deck 末页
- `#slide-28`：引用索引

分别在 1920×1080、1280×720 和 light/dark 主题下确认无裁切、重叠、横向溢出或标签碰撞。

### 5. 仓库检查

```bash
git diff --check
git status --short
pre-commit run --all-files
```

如果当前仓库没有可用的 pre-commit 配置，应如实报告，不要为本演示额外引入无关构建配置。
