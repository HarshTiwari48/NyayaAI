from pathlib import Path
from uuid import uuid4
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.schemas.application import ApplicationDraft


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_DOCUMENTS_DIR = (
    PROJECT_ROOT / "generated_documents"
)


def generate_application_pdf(
    draft: ApplicationDraft | dict,
) -> Path:
    """
    Generate a professionally formatted PDF
    from an application draft.

    Returns:
        Path to the generated PDF.
    """

    # --------------------------------------------------
    # NORMALIZE INPUT
    # --------------------------------------------------

    if isinstance(draft, dict):
        draft = ApplicationDraft(**draft)

    GENERATED_DOCUMENTS_DIR.mkdir(
        exist_ok=True
    )

    file_name = (
        f"application_{uuid4().hex}.pdf"
    )

    file_path = (
        GENERATED_DOCUMENTS_DIR / file_name
    )

    # --------------------------------------------------
    # PDF DOCUMENT
    # --------------------------------------------------

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        title="Application",
        author="NyayaAI",
    )

    styles = getSampleStyleSheet()

    # --------------------------------------------------
    # CUSTOM STYLES
    # --------------------------------------------------

    recipient_style = ParagraphStyle(
        name="Recipient",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=2,
    )

    subject_style = ParagraphStyle(
        name="Subject",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=20,
    )

    salutation_style = ParagraphStyle(
        name="Salutation",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=16,
    )

    body_style = ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=17,
        alignment=TA_LEFT,
        spaceAfter=14,
        firstLineIndent=0,
    )

    closing_style = ParagraphStyle(
        name="Closing",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
    )

    sender_style = ParagraphStyle(
        name="Sender",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=2,
    )

    sender_details_style = ParagraphStyle(
        name="SenderDetails",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#333333"),
    )

    story = []

    # --------------------------------------------------
    # RECIPIENT BLOCK
    # --------------------------------------------------

    if draft.recipient:
        story.append(
            Paragraph(
                f"<b>To,</b><br/>{escape(draft.recipient)}",
                recipient_style,
            )
        )

    if draft.organization:
        story.append(
            Paragraph(
                escape(draft.organization),
                recipient_style,
            )
        )

    story.append(
        Spacer(1, 18)
    )

    # --------------------------------------------------
    # SUBJECT
    # --------------------------------------------------

    story.append(
        Paragraph(
            f"Subject: {escape(draft.subject)}",
            subject_style,
        )
    )

    # --------------------------------------------------
    # SALUTATION
    # --------------------------------------------------

    story.append(
        Paragraph(
            escape(draft.salutation),
            salutation_style,
        )
    )

    # --------------------------------------------------
    # BODY
    # --------------------------------------------------

    for paragraph in draft.body:
        if paragraph.strip():
            story.append(
                Paragraph(
                    escape(paragraph),
                    body_style,
                )
            )

    # --------------------------------------------------
    # CLOSING
    # --------------------------------------------------

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            escape(draft.closing),
            closing_style,
        )
    )

    # --------------------------------------------------
    # SIGNATURE / SENDER
    # --------------------------------------------------

    if draft.sender_name:
        story.append(
            Spacer(1, 24)
        )

        story.append(
            Paragraph(
                escape(draft.sender_name),
                sender_style,
            )
        )

    if draft.sender_details:
        story.append(
            Paragraph(
                escape(draft.sender_details),
                sender_details_style,
            )
        )

    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------

    document.build(story)

    return file_path