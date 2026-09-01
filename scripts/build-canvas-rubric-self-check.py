#!/usr/bin/env python3
"""Build the grader-facing AURA Forge rubric self-check PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/capstone/submission/canvas/06_AURA_Forge_Rubric_Self_Check.md"
OUTPUT = SOURCE.with_suffix(".pdf")

NAVY = colors.HexColor("#0B1220")
BLUE = colors.HexColor("#2563EB")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
BORDER = colors.HexColor("#CBD5E1")
PALE = colors.HexColor("#EAF2FF")


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=20, leading=23, textColor=colors.white),
        "sub": ParagraphStyle("sub", parent=base["Normal"], fontSize=8.7, leading=11, textColor=colors.HexColor("#DCE7F7")),
        "score": ParagraphStyle("score", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=24, textColor=BLUE, alignment=1),
        "score_label": ParagraphStyle("score_label", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.3, leading=8.5, textColor=MUTED, alignment=1),
        "section": ParagraphStyle("section", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=6, spaceAfter=5),
        "head": ParagraphStyle("head", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.2, leading=8.6, textColor=colors.white),
        "cell": ParagraphStyle("cell", parent=base["Normal"], fontSize=7.1, leading=9.1, textColor=SLATE),
        "cell_score": ParagraphStyle("cell_score", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.2, leading=9.4, textColor=BLUE, alignment=1),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontSize=7.4, leading=9.2, leftIndent=9, firstLineIndent=-6, textColor=SLATE, spaceAfter=1),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontSize=7.5, leading=9.6, textColor=SLATE, spaceAfter=2),
        "callout": ParagraphStyle("callout", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY, borderColor=BLUE, borderWidth=1, borderPadding=6, backColor=PALE, spaceBefore=4),
    }


def _rows() -> list[tuple[str, str, str, str]]:
    rows = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and line[2:3].isdigit():
            parts = [part.strip() for part in line.strip().strip("|").split("|")]
            rows.append((parts[0], parts[1], parts[2], parts[3]))
    if len(rows) != 13:
        raise ValueError(f"Expected 13 rubric rows, found {len(rows)}")
    return rows


def _header(styles: dict[str, ParagraphStyle]) -> Table:
    table = Table(
        [[[Paragraph("AURA Forge Rubric Self-Check", styles["title"]), Paragraph("Official LaunchCode 13-criterion rubric · corrected non-video revision · 2026-09-01", styles["sub"])], [Paragraph("48 / 52", styles["score"]), Paragraph("DEFENSIBLE SELF-ASSESSMENT", styles["score_label"])]]],
        colWidths=[5.7 * inch, 1.25 * inch],
        rowHeights=[0.72 * inch],
    )
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 16), ("RIGHTPADDING", (1, 0), (1, 0), 10), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return table


def _rubric_table(items: list[tuple[str, str, str, str]], styles: dict[str, ParagraphStyle]) -> Table:
    data = [[Paragraph("#", styles["head"]), Paragraph("Official criterion", styles["head"]), Paragraph("Score", styles["head"]), Paragraph("Defensible evidence summary", styles["head"])]]
    for number, name, score, evidence in items:
        data.append([Paragraph(number, styles["cell"]), Paragraph(name, styles["cell"]), Paragraph(score, styles["cell_score"]), Paragraph(evidence, styles["cell"])])
    table = Table(data, colWidths=[0.28 * inch, 1.56 * inch, 0.48 * inch, 4.62 * inch], repeatRows=1)
    commands = [("BACKGROUND", (0, 0), (-1, 0), BLUE), ("GRID", (0, 0), (-1, -1), 0.45, BORDER), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for index in range(2, len(data), 2):
        commands.append(("BACKGROUND", (0, index), (-1, index), colors.HexColor("#F8FAFC")))
    table.setStyle(TableStyle(commands))
    return table


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.line(doc.leftMargin, 0.42 * inch, letter[0] - doc.rightMargin, 0.42 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.8)
    canvas.drawString(doc.leftMargin, 0.26 * inch, "Source of truth: docs/capstone/final-rubric-audit.md")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.26 * inch, f"Page {doc.page}")
    canvas.restoreState()


def _invariant_canvas(*args, **kwargs) -> Canvas:
    kwargs["invariant"] = 1
    return Canvas(*args, **kwargs)


def build(local_tests: int, offline_tests: int) -> None:
    styles = _styles()
    rows = _rows()
    document = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=0.38 * inch, rightMargin=0.38 * inch, topMargin=0.32 * inch, bottomMargin=0.52 * inch, title="AURA Forge Rubric Self-Check", author="Muhammad Imran")
    story = [_header(styles), Spacer(1, 7), Paragraph("Score calculation: 52 − 1 (criterion 2) − 1 (criterion 4) − 1 (criterion 9) − 1 (criterion 11) = 48. This is a self-assessment, not a Canvas regrade.", styles["callout"]), Paragraph("Criteria 1–7", styles["section"]), _rubric_table(rows[:7], styles), PageBreak(), _header(styles), Spacer(1, 7), Paragraph("Criteria 8–13", styles["section"]), _rubric_table(rows[7:], styles), Spacer(1, 5), Paragraph("Current verification", styles["section"]), Paragraph(f"Full local evaluation suite: {local_tests} passed · Offline network-disabled container: {offline_tests} passed · Pipeline integrity: PASS · Local path-reference scan: PASS · Video unchanged.", styles["body"]), Paragraph("Required human actions before resubmission", styles["section"])]
    for text in ("Approve, commit, and push this revision to capstone/aura-forge.", "Wait for fresh GitHub CI and use that run as current evidence.", "Change or share the private repository so a logged-out grader can access the exact branch."):
        story.append(Paragraph("• " + text, styles["bullet"]))
    story.append(Paragraph("Main blocker: GitHub reports Muhammad7839/FitGPT-Agentic-Engineering as PRIVATE. After repository access, fresh CI, and a walkthrough at or below 10 minutes are verified, submit the exact link through Canvas/LaunchCode and confirm the revised submission is visible.", styles["callout"]))
    document.build(story, onFirstPage=_footer, onLaterPages=_footer, canvasmaker=_invariant_canvas)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-tests", type=int, required=True)
    parser.add_argument("--offline-tests", type=int, required=True)
    args = parser.parse_args()
    build(args.local_tests, args.offline_tests)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
