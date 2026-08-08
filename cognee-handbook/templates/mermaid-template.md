# Mermaid 渲染配置

```json
{
  "theme": "neutral",
  "themeVariables": {
    "background": "#FAFAFA",
    "primaryColor": "#3B82F6",
    "primaryTextColor": "#FFFFFF",
    "primaryBorderColor": "#1E40AF",
    "secondaryColor": "#10B981",
    "tertiaryColor": "#F59E0B",
    "lineColor": "#6B7280",
    "textColor": "#1F2937",
    "fontFamily": "PingFang SC, Microsoft YaHei, system-ui",
    "fontSize": "14px"
  },
  "flowchart": {
    "curve": "basis",
    "nodeSpacing": 50,
    "rankSpacing": 60
  },
  "sequence": {
    "actorMargin": 80,
    "messageMargin": 40
  }
}
```

## 安装 mmdc

```bash
npm install -g @mermaid-js/mermaid-cli
# 或者
pnpm add -g @mermaid-js/mermaid-cli
```

## 渲染命令

```bash
mmdc -i chapters/part-XX-.../chapter-XX-diagram.mmd \
     -o assets/diagrams/chXX-diagram-name.svg \
     -b transparent \
     -t neutral \
     --configFile templates/mermaid-config.json
```

## 内联 mermaid(直接在 markdown 中)

```mermaid
%% title: Ch01 — 流程示意
graph LR
    A[开始] --> B[处理]
    B --> C[结束]
```

GitBook / mdbook / Hugo / Obsidian 等大多数现代 markdown 渲染器都支持内联 mermaid。