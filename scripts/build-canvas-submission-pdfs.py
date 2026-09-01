#!/usr/bin/env python3
"""Build the text-first Canvas PDF packet from current Markdown evidence."""

from __future__ import annotations

import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
CANVAS_DIR = ROOT / "docs/capstone/submission/canvas"
NAVY = colors.HexColor("#0B1220")
BLUE = colors.HexColor("#2563EB")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
BORDER = colors.HexColor("#CBD5E1")

PACKAGES: dict[str, tuple[str, list[str]]] = {
    "01_AURA_Forge_Architecture_Writeup.pdf": (
        "AURA Forge Architecture Write-Up",
        [
            "docs/capstone/final-architecture.md",
            "docs/capstone/retrieval-tool-evidence.md",
            "docs/capstone/reproducibility-runbook.md",
        ],
    ),
    "02_AURA_Forge_Impact_and_Tool_Evolution.pdf": (
        "AURA Forge Impact and Tool-Evolution Report",
        [
            "docs/capstone/control-vs-aura-impact.md",
            "docs/capstone/tool-evolution-drill.md",
            "docs/capstone/reliability-controls.md",
        ],
    ),
    "03_AURA_Forge_Stakeholder_One_Pager.pdf": (
        "AURA Forge Stakeholder One-Pager",
        ["docs/capstone/stakeholder-one-pager.md"],
    ),
    "04_AURA_Forge_Ops_Runbook.pdf": (
        "AURA Forge Ops-Ready Runbook",
        [
            "docs/capstone/monitoring-incident-runbook.md",
            "docs/capstone/reliability-controls.md",
            "docs/capstone/reproducibility-runbook.md",
        ],
    ),
    "05_AURA_Forge_ADR_Package.pdf": (
        "AURA Forge ADR Package",
        [str(path.relative_to(ROOT)) for path in sorted((ROOT / "docs/adr").glob("*.md"))],
    ),
}


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("packet_title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=19, leading=23, textColor=colors.white),
        "subtitle": ParagraphStyle("packet_subtitle", parent=base["Normal"], fontSize=8.5, leading=11, textColor=colors.HexColor("#DCE7F7")),
        "h1": ParagraphStyle("md_h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY, spaceBefore=4, spaceAfter=7),
        "h2": ParagraphStyle("md_h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4),
        "h3": ParagraphStyle("md_h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=BLUE, spaceBefore=6, spaceAfter=3),
        "body": ParagraphStyle("md_body", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=10.6, textColor=SLATE, spaceAfter=4),
        "bullet": ParagraphStyle("md_bullet", parent=base["BodyText"], fontSize=7.8, leading=10.2, textColor=SLATE, leftIndent=12, firstLineIndent=-8, spaceAfter=2),
        "code": ParagraphStyle("md_code", parent=base["Code"], fontName="Courier", fontSize=6.8, leading=8.5, textColor=NAVY, backColor=colors.HexColor("#F1F5F9"), borderPadding=5, spaceAfter=5),
        "table_head": ParagraphStyle("md_table_head", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=6.7, leading=8, textColor=colors.white),
        "table_cell": ParagraphStyle("md_table_cell", parent=base["Normal"], fontSize=6.5, leading=8.1, textColor=SLATE),
        "source": ParagraphStyle("source", parent=base["Normal"], fontSize=7, leading=9, textColor=MUTED, spaceBefore=4, spaceAfter=4),
    }


def plain_inline(text: str) -> str:
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    return escape(text.strip())


def table_flowable(lines: list[str], style_map: dict[str, ParagraphStyle]) -> Table:
    rows = [[plain_inline(cell) for cell in line.strip().strip("|").split("|")] for line in lines]
    if len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in rows[1]):
        rows.pop(1)
    width = 7.0 * inch
    column_count = len(rows[0])
    weights = []
    for index in range(column_count):
        weights.append(max(8, min(42, max(len(row[index]) if index < len(row) else 0 for row in rows))))
    total = sum(weights)
    column_widths = [width * weight / total for weight in weights]
    data = []
    for row_index, row in enumerate(rows):
        paragraph_style = style_map["table_head"] if row_index == 0 else style_map["table_cell"]
        data.append([Paragraph(cell, paragraph_style) for cell in row])
    table = Table(data, colWidths=column_widths, repeatRows=1, hAlign="LEFT")
    commands = [("BACKGROUND", (0, 0), (-1, 0), BLUE), ("GRID", (0, 0), (-1, -1), 0.4, BORDER), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for row_index in range(2, len(data), 2):
        commands.append(("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#F8FAFC")))
    table.setStyle(TableStyle(commands))
    return table


def markdown_story(path: Path, style_map: dict[str, ParagraphStyle]) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    story = [Paragraph(plain_inline(lines[0].lstrip("# ") if lines else path.stem), style_map["h1"]), Paragraph(f"Source: {path.relative_to(ROOT)}", style_map["source"])]
    index = 1
    paragraph: list[str] = []

    def flush() -> None:
        nonlocal paragraph
        if paragraph:
            story.append(Paragraph(plain_inline(" ".join(part.strip() for part in paragraph)), style_map["body"]))
            paragraph = []

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush()
            index += 1
            continue
        if stripped.startswith("```"):
            flush()
            code = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            story.append(Preformatted("\n".join(code), style_map["code"]))
            index += 1
            continue
        if stripped.startswith("|") and index + 1 < len(lines) and lines[index + 1].strip().startswith("|"):
            flush()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(table_flowable(table_lines, style_map))
            story.append(Spacer(1, 4))
            continue
        if stripped.startswith("### "):
            flush(); story.append(Paragraph(plain_inline(stripped[4:]), style_map["h3"])); index += 1; continue
        if stripped.startswith("## "):
            flush(); story.append(Paragraph(plain_inline(stripped[3:]), style_map["h2"])); index += 1; continue
        if stripped.startswith("# "):
            flush(); story.append(Paragraph(plain_inline(stripped[2:]), style_map["h1"])); index += 1; continue
        bullet = re.match(r"^(?:[-*]|\d+\.)\s+(.*)$", stripped)
        if bullet:
            flush(); story.append(Paragraph("• " + plain_inline(bullet.group(1)), style_map["bullet"])); index += 1; continue
        if stripped == "---":
            flush(); story.append(Spacer(1, 4)); index += 1; continue
        paragraph.append(stripped)
        index += 1
    flush()
    return story


def header(title: str, source_count: int, style_map: dict[str, ParagraphStyle]) -> Table:
    table = Table([[[Paragraph(plain_inline(title), style_map["title"]), Paragraph(f"Current evidence packet · {source_count} tracked Markdown source(s) · 2026-09-01", style_map["subtitle"])]]], colWidths=[7.0 * inch], rowHeights=[0.68 * inch])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 16), ("RIGHTPADDING", (0, 0), (-1, -1), 12)]))
    return table


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.line(doc.leftMargin, 0.42 * inch, letter[0] - doc.rightMargin, 0.42 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.8)
    canvas.drawString(doc.leftMargin, 0.26 * inch, "AURA Forge Canvas Submission Package")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.26 * inch, f"Page {doc.page}")
    canvas.restoreState()


def invariant_canvas(*args, **kwargs) -> Canvas:
    kwargs["invariant"] = 1
    return Canvas(*args, **kwargs)


def build_package(filename: str, title: str, sources: list[str]) -> None:
    style_map = styles()
    output = CANVAS_DIR / filename
    document = SimpleDocTemplate(str(output), pagesize=letter, leftMargin=0.45 * inch, rightMargin=0.45 * inch, topMargin=0.32 * inch, bottomMargin=0.52 * inch, title=title, author="Muhammad Imran")
    story = [header(title, len(sources), style_map), Spacer(1, 8)]
    for source_index, source in enumerate(sources):
        if source_index:
            story.append(PageBreak())
            story.append(header(title, len(sources), style_map))
            story.append(Spacer(1, 8))
        story.extend(markdown_story(ROOT / source, style_map))
    document.build(story, onFirstPage=footer, onLaterPages=footer, canvasmaker=invariant_canvas)
    print(output)


def main() -> int:
    for filename, (title, sources) in PACKAGES.items():
        build_package(filename, title, sources)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
