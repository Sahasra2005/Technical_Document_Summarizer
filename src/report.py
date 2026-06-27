from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os

# Register Unicode font
font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))

def generate_pdf(summary_sections, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SectionHeader",
                              fontName="DejaVuSans",
                              fontSize=14,
                              spaceAfter=10,
                              textColor=colors.darkblue,
                              leading=16))
    styles.add(ParagraphStyle(name="SummaryText",
                              fontName="DejaVuSans",
                              fontSize=11,
                              leading=14))

    story = []

    # Title
    story.append(Paragraph("Document Summary", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    # Sectioned summaries
    for title, summary in summary_sections:
        story.append(Paragraph(title, styles["SectionHeader"]))
        story.append(Paragraph(summary, styles["SummaryText"]))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
