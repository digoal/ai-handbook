# Cognee 记忆工程 · 发布流水线 Makefile
#
# 一键:`make all` = extract → svg → chapter-svg → epub → pdf → html
#
# 中间产物可清理:`make clean` 删 dist 与 assets/diagrams/{*.mmd,*.svg}
#
# 重要:
#   - mmdc 需要 Chrome headless shell(已在 ~/.cache/puppeteer/)。
#   - Pandoc 直接渲染 mermaid 不稳,所以 chapter-svg 阶段把
#     chapters/*.md 里的 ```mermaid 块替换为 ![](assets/diagrams/*.svg) 引用。
#   - PDF 用 Chrome headless --print-to-pdf,绕开 LaTeX 依赖。
#
# 全部命令已加 `env -u HTTP_PROXY -u HTTPS_PROXY ...`,避免本地 npm/proxy 干扰。

ROOT       := $(abspath .)
DIAG_DIR   := $(ROOT)/assets/diagrams
DIST_DIR   := $(ROOT)/dist
CHAPTERS   := $(ROOT)/chapters

# Chrome headless shell —— 用于 mmdc 与 PDF 打印
CHROME_HEADLESS := $(HOME)/.cache/puppeteer/chrome-headless-shell/mac_arm-150.0.7871.24/chrome-headless-shell-mac-arm64/chrome-headless-shell

# 让 mmdc / pandoc 不走本地代理
ENV := env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy

MMDC := $(ENV) mmdc
PANDOC := $(ENV) pandoc
PYTHON := $(ENV) python3

# === Phony targets ============================================================
.PHONY: all extract svg chapter-svg epub pdf html smoke clean verify

# 用 bash 支持 process substitution (zsh/macOS 默认 sh 不支持)
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

# === 1) Extract ===============================================================
# 从 chapters/**/*.md 中抽取 ```mermaid 块到 assets/diagrams/chNN-NN-slug.mmd
extract:
	@echo "==> [1/5] Extract mermaid blocks from chapters/"
	@$(PYTHON) shared-context/extract_mermaid.py

# === 2) SVG ===================================================================
# 把每个 .mmd 渲染为 .svg。 如果没有 .mmd(因为 chapters/ 已经是 SVG 版本),
# 这个 target 跳过,直接进入下一阶段。
svg: extract
	@echo "==> [2/5] Render mermaid → SVG (mmdc)"
	@mkdir -p $(DIAG_DIR)
	@shopt -s nullglob; mmds=($(DIAG_DIR)/*.mmd); \
	  if [ $${#mmds[@]} -eq 0 ]; then \
	    echo "     (no .mmd found, skipping — chapters already use SVG refs)"; \
	  else \
	    for mmd in "$${mmds[@]}"; do \
	      out="$${mmd%.mmd}.svg"; \
	      echo "     $$out"; \
	      $(MMDC) -i "$$mmd" -o "$$out" \
	             -b transparent \
	             -t neutral \
	             --configFile templates/mermaid-config.json \
	             --puppeteerConfigFile <(echo '{"executablePath":"$(CHROME_HEADLESS)","args":["--no-sandbox"]}'); \
	    done; \
	  fi

# === 3) Chapter SVG replacement ===============================================
# 把 chapters/*.md 中的 ```mermaid 块替换为 ![](../../assets/diagrams/*.svg) 引用
# (路径以章节文件为基准上溯两级到仓库根,这是 pandoc 解析 <img> 默认行为必须的)
# 原内联版本已备份到 chapters-inline-mermaid.bak/(运行本目录前已存在)
chapter-svg: svg
	@echo "==> [3/5] Replace inline mermaid with SVG refs in chapters/"
	@$(PYTHON) shared-context/mermaid_to_svg.py

# 通用 --resource-path 选项:让 Pandoc 在多 part/ 目录上溯时也能找到 SVG 与图
# (来自 M13 SVG 路径审计:cognee-handbook 的 chapter markdown 位于
# chapters/part-XX/ 深度 2,SVG 在仓库根 assets/diagrams/,所以默认 base 是错的)
PANDOC_RP := --resource-path=. --resource-path=chapters/part-01-foundation --resource-path=chapters/part-02-architecture --resource-path=chapters/part-03-api --resource-path=chapters/part-04-integrations --resource-path=chapters/part-05-production

# === 4) EPUB ==================================================================
epub: chapter-svg
	@echo "==> [4/5] Build EPUB via Pandoc"
	@mkdir -p $(DIST_DIR)
	@cd $(ROOT) && $(PANDOC) -o $(DIST_DIR)/cognee-handbook.epub \
	  $(PANDOC_RP) \
	  --from=markdown+raw_html --embed-resources --standalone \
	  --toc --toc-depth=3 \
	  --metadata title="Cognee 记忆工程" \
	  --metadata lang=zh-CN \
	  --metadata author="Cognee Handbook Authors" \
	  SUMMARY.md chapters/part-*/chapter-*.md

# === 5) PDF (Chrome headless --print-to-pdf,绕开 LaTeX) =======================
pdf: chapter-svg
	@echo "==> [5a/6] Build HTML for Chrome"
	@mkdir -p $(DIST_DIR)
	@cd $(ROOT) && $(PANDOC) -o $(DIST_DIR)/cognee-handbook-for-pdf.html \
	  $(PANDOC_RP) \
	  --from=markdown+raw_html --embed-resources --standalone \
	  --toc --toc-depth=3 \
	  --metadata title="Cognee 记忆工程" \
	  --metadata lang=zh-CN \
	  SUMMARY.md chapters/part-*/chapter-*.md
	@echo "==> [5b/6] Print to PDF via Chrome headless"
	@$(CHROME_HEADLESS) --no-sandbox --headless --disable-gpu \
	  --print-to-pdf=$(DIST_DIR)/cognee-handbook.pdf \
	  --no-pdf-header-footer \
	  "file://$(DIST_DIR)/cognee-handbook-for-pdf.html"
	@echo "==> PDF generated. Tail with: pdftotext -enc UTF-8 dist/cognee-handbook.pdf - | head"

# === 6) HTML (self-contained) =================================================
html: chapter-svg
	@echo "==> [6/6] Build self-contained HTML via Pandoc"
	@mkdir -p $(DIST_DIR)
	@cd $(ROOT) && $(PANDOC) -o $(DIST_DIR)/cognee-handbook.html \
	  $(PANDOC_RP) \
	  --from=markdown+raw_html --embed-resources --standalone \
	  --toc --toc-depth=3 \
	  --metadata title="Cognee 记忆工程" \
	  --metadata lang=zh-CN \
	  SUMMARY.md chapters/part-*/chapter-*.md

# === Smoke test ===============================================================
# 跑 code-review/smoke-test.py —— 验证 30 章 API 用法 vs cognee v1.4.0 实际实现
# 无 OPENAI_API_KEY 时多数测试会 SKIP,但 import + 签名 + 枚举层面的检查仍能跑
# 安装提示(首次跑需要):
#   env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
#     uv pip install --system -e <COGNEE_REPO>
smoke:
	@echo "==> Smoke test: cognee v1.4.0 API surface"
	@cd $(ROOT) && $(PYTHON) -m pytest code-review/smoke-test.py -v

# === Verify ===================================================================
# 不重新构建,只检查产物是否符合预期
verify:
	@echo "==> Inline mermaid blocks (should be 0):"
	@grep -rc '^```mermaid$$' $(CHAPTERS)/part-*/chapter-*.md 2>/dev/null | awk -F: '$$2>0' || true
	@echo "==> SVG refs count (should be >= 38):"
	@grep -rEho '(?:\.\./)?(?:\.\./)?assets/diagrams/[^)"]*\.svg' $(CHAPTERS)/part-*/chapter-*.md | sort -u | wc -l
	@echo "==> dist/ artifacts:"
	@ls -lh $(DIST_DIR)/cognee-handbook.* 2>/dev/null || echo "  (no dist artifacts)"

# === Clean ====================================================================
clean:
	@echo "==> Clean dist + diagram intermediates"
	@rm -rf $(DIST_DIR)/cognee-handbook.epub $(DIST_DIR)/cognee-handbook.html \
	        $(DIST_DIR)/cognee-handbook.pdf $(DIST_DIR)/cognee-handbook-for-pdf.html
	@rm -f $(DIAG_DIR)/*.mmd $(DIAG_DIR)/*.svg
	@echo "Done. Run 'make all' to rebuild."

# === All ======================================================================
all: extract svg chapter-svg epub pdf html
	@echo ""
	@echo "==> Done. Artifacts:"
	@ls -lh $(DIST_DIR)/cognee-handbook.* 2>/dev/null