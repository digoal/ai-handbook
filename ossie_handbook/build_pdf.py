#!/usr/bin/env python3
"""Generate handbook.pdf via ReportLab + STHeiti (TTC font)."""
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "handbook.pdf"

# Register STHeiti (Mac system font with full Chinese coverage)
FONT_PATHS = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/Library/Fonts/STHeiti Medium.ttc",
]
font_name = None
for fp in FONT_PATHS:
    if Path(fp).exists():
        try:
            pdfmetrics.registerFont(TTFont("Heiti", fp))
            font_name = "Heiti"
            break
        except Exception:
            continue

if font_name is None:
    print("ERROR: STHeiti font not found", file=sys.stderr)
    sys.exit(1)

styles = getSampleStyleSheet()
zh_style = ParagraphStyle("zh", parent=styles["BodyText"], fontName=font_name, fontSize=10, leading=16)
zh_h1 = ParagraphStyle("h1", parent=zh_style, fontSize=18, leading=24, spaceBefore=12, spaceAfter=8)
zh_h2 = ParagraphStyle("h2", parent=zh_style, fontSize=14, leading=20, spaceBefore=10, spaceAfter=6)
zh_h3 = ParagraphStyle("h3", parent=zh_style, fontSize=12, leading=18, spaceBefore=8, spaceAfter=4)
zh_code = ParagraphStyle("code", parent=zh_style, fontName="Courier", fontSize=8, leading=10, leftIndent=8)

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
story = []

md_files = sorted(SRC.glob("*.md"))
print(f"Building PDF from {len(md_files)} MD files...")

for md in md_files:
    print(f"  + {md.name}")
    text = md.read_text(encoding="utf-8")
    in_code = False
    code_buf = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_buf), zh_code))
                code_buf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        # skip license header / abstract blockquote line markup
        line_clean = line.replace("**", "").replace("`", "'").replace(">", "")
        # strip ALL angle-bracket content (HTML, Mermaid pseudo, ReportLab internal)
        import re as _re
        line_clean = _re.sub(r"<[^>]+>", "", line_clean)
        # escape ampersand (confuses ReportLab entity parser)
        line_clean = line_clean.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if line_clean.startswith("# "):
            story.append(Paragraph(line_clean[2:].strip(), zh_h1))
        elif line_clean.startswith("## "):
            story.append(Paragraph(line_clean[3:].strip(), zh_h2))
        elif line_clean.startswith("### "):
            story.append(Paragraph(line_clean[4:].strip(), zh_h3))
        elif line_clean.startswith("|") or line_clean.startswith("---"):
            continue  # skip tables/separators in PDF
        elif line_clean.strip() == "":
            story.append(Spacer(1, 4))
        else:
            story.append(Preformatted(line_clean[:200], zh_style))
    story.append(PageBreak())

doc.build(story)
print(f"DONE: {OUT} ({OUT.stat().st_size:,} bytes)")