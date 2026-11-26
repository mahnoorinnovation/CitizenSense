from pathlib import Path
import re
import mistune

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether
)

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "CitizenSense_Final_Report_Complete.md"
OUTPUT = BASE / "CitizenSense_Final_Report_Updated.pdf"

if not SOURCE.exists():
    raise FileNotFoundError(f"Report not found: {SOURCE}")

if OUTPUT.exists():
    raise FileExistsError(
        f"PDF already exists: {OUTPUT}\n"
        "Existing PDF preserved. Rename it manually before rebuilding."
    )

markdown = SOURCE.read_text(encoding="utf-8")
renderer = mistune.create_markdown(renderer="ast", plugins=["table", "strikethrough"])
tokens = renderer(markdown)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=21, leading=27,
    alignment=TA_CENTER, textColor=colors.HexColor("#17365D"),
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name="H1Custom", parent=styles["Heading1"],
    fontSize=16, leading=20, textColor=colors.HexColor("#17365D"),
    spaceBefore=14, spaceAfter=8, keepWithNext=True
))
styles.add(ParagraphStyle(
    name="H2Custom", parent=styles["Heading2"],
    fontSize=12, leading=15, textColor=colors.HexColor("#24527A"),
    spaceBefore=10, spaceAfter=6, keepWithNext=True
))
styles.add(ParagraphStyle(
    name="H3Custom", parent=styles["Heading3"],
    fontSize=10, leading=13, textColor=colors.HexColor("#333333"),
    spaceBefore=8, spaceAfter=4, keepWithNext=True
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"],
    fontSize=8.5, leading=12, spaceAfter=6,
    splitLongWords=1, allowWidows=0, allowOrphans=0
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"],
    fontSize=7, leading=9, splitLongWords=1
))
styles.add(ParagraphStyle(
    name="BulletCustom", parent=styles["BodyText"],
    fontSize=8.5, leading=11, leftIndent=14,
    firstLineIndent=-8, spaceAfter=3
))
styles.add(ParagraphStyle(
    name="CodeCustom", parent=styles["Code"],
    fontName="Courier", fontSize=7, leading=9,
    backColor=colors.HexColor("#F1F3F5"),
    borderPadding=5, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="TableCell", parent=styles["BodyText"],
    fontSize=6.3, leading=8, splitLongWords=1
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["BodyText"],
    fontName="Helvetica-Bold", fontSize=6.5,
    leading=8, textColor=colors.white
))

story = []
image_count = 0
table_count = 0

def safe_text(value):
    value = str(value or "")
    value = value.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\u2022", "-")
    return value

def inline_text(children):
    result = ""
    for child in children or []:
        kind = child.get("type")
        raw = safe_text(child.get("raw", ""))
        if kind == "text":
            result += raw
        elif kind == "codespan":
            result += "<font name='Courier' size='7'>" + raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</font>"
        elif kind == "strong":
            result += "<b>" + inline_text(child.get("children")) + "</b>"
        elif kind == "emphasis":
            result += "<i>" + inline_text(child.get("children")) + "</i>"
        elif kind == "strikethrough":
            result += "<strike>" + inline_text(child.get("children")) + "</strike>"
        elif kind == "link":
            label = inline_text(child.get("children"))
            url = safe_text(child.get("attrs", {}).get("url", ""))
            result += f"<link href='{url}' color='#1769AA'>{label}</link>" if url.startswith(("http://", "https://")) else label
        elif kind == "image":
            result += safe_text(child.get("attrs", {}).get("alt", "Image"))
        elif kind == "inline_html":
            result += raw
        elif child.get("children"):
            result += inline_text(child["children"])
    return result

def add_image(url):
    global image_count
    raw = safe_text(url)
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    candidate = (BASE / raw).resolve()
    if not candidate.exists():
        candidate = (BASE.parent / raw).resolve()
    if not candidate.exists() or not candidate.is_file():
        story.append(Paragraph(f"[Image unavailable: {raw}]", styles["SmallCustom"]))
        return
    try:
        from PIL import Image as PILImage
        with PILImage.open(candidate) as im:
            width_px, height_px = im.size
        max_w, max_h = 165 * mm, 105 * mm
        scale = min(max_w / width_px, max_h / height_px, 1)
        pic = Image(str(candidate), width=width_px * scale, height=height_px * scale)
        pic.hAlign = "CENTER"
        story.append(Spacer(1, 4))
        story.append(pic)
        story.append(Spacer(1, 7))
        image_count += 1
    except Exception as exc:
        story.append(Paragraph(f"[Could not display image: {candidate.name}]", styles["SmallCustom"]))
        print(f"Image warning: {candidate}: {exc}")

def render_table(token):
    global table_count
    rows = []
    for child in token.get("children", []):
        if child.get("type") == "table_head":
            cells = child.get("children", [])
            rows.append([Paragraph(inline_text(c.get("children")), styles["TableHead"]) for c in cells])
        elif child.get("type") == "table_body":
            for row in child.get("children", []):
                cells = row.get("children", [])
                rows.append([Paragraph(inline_text(c.get("children")), styles["TableCell"]) for c in cells])

    if not rows:
        return

    ncols = max(len(r) for r in rows)
    for row in rows:
        while len(row) < ncols:
            row.append(Paragraph("", styles["TableCell"]))

    # Wide tables are placed on a landscape page to keep columns readable.
    if ncols >= 6:
        story.append(PageBreak())
        widths = [257 * mm / ncols] * ncols
        page_size = landscape(A4)
    else:
        widths = [178 * mm / ncols] * ncols
        page_size = A4

    tbl = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24476B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D2DC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6F9")]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 8))
    table_count += 1

def walk(items):
    for token in items:
        kind = token.get("type")

        if kind == "heading":
            level = token.get("attrs", {}).get("level", 2)
            text_value = inline_text(token.get("children"))
            if level == 1:
                story.append(Paragraph(text_value, styles["ReportTitle"]))
            elif level == 2:
                story.append(Paragraph(text_value, styles["H1Custom"]))
            elif level == 3:
                story.append(Paragraph(text_value, styles["H2Custom"]))
            else:
                story.append(Paragraph(text_value, styles["H3Custom"]))

        elif kind == "paragraph":
            children = token.get("children", [])
            images = [c for c in children if c.get("type") == "image"]
            if images and len(children) == 1:
                add_image(images[0].get("attrs", {}).get("url", ""))
            else:
                content = inline_text(children).strip()
                if content:
                    story.append(Paragraph(content, styles["BodyCustom"]))

        elif kind in ("list",):
            ordered = token.get("attrs", {}).get("ordered", False)
            start = token.get("attrs", {}).get("start", 1) or 1
            for index, item in enumerate(token.get("children", [])):
                prefix = f"{start + index}." if ordered else "•"
                content = inline_text(item.get("children"))
                story.append(Paragraph(f"{prefix} {content}", styles["BulletCustom"]))

        elif kind == "table":
            render_table(token)

        elif kind == "block_code":
            code = safe_text(token.get("raw", ""))
            code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(code.replace("\n", "<br/>"), styles["CodeCustom"]))

        elif kind == "block_quote":
            content = inline_text(token.get("children"))
            if content:
                story.append(Paragraph(f"<i>{content}</i>", styles["BodyCustom"]))

        elif kind == "thematic_break":
            story.append(Spacer(1, 6))

        elif token.get("children"):
            walk(token["children"])

walk(tokens)

def footer(canvas, doc):
    canvas.saveState()
    w, h = doc.pagesize
    canvas.setStrokeColor(colors.HexColor("#D7DEE7"))
    canvas.line(18 * mm, 14 * mm, w - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#65758B"))
    canvas.drawString(18 * mm, 9 * mm, "CitizenSense | Final Project Report")
    canvas.drawRightString(w - 18 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=16 * mm, leftMargin=16 * mm,
    topMargin=17 * mm, bottomMargin=21 * mm,
    title="CitizenSense - Complete Final Report",
    author="CitizenSense Project Team"
)

doc.build(story, onFirstPage=footer, onLaterPages=footer)

print("PDF created successfully:", OUTPUT)
print("Source Markdown preserved:", SOURCE.exists())
print("Images included:", image_count)
print("Tables included:", table_count)
print("PDF size:", OUTPUT.stat().st_size, "bytes")

