from pathlib import Path
from uuid import uuid4

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
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
    Generate a PDF file from an application draft.

    Returns:
        Path to the generated PDF.
    """

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

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    styles = getSampleStyleSheet()

    normal_style = styles["Normal"]
    normal_style.alignment = TA_LEFT
    normal_style.spaceAfter = 12

    subject_style = styles["Heading2"]
    subject_style.alignment = TA_LEFT
    subject_style.spaceAfter = 18

    story = []

    # ---------------------------------------------
    # RECIPIENT
    # ---------------------------------------------

    if draft.recipient:
        story.append(
            Paragraph(
                draft.recipient,
                normal_style,
            )
        )

    if draft.organization:
        story.append(
            Paragraph(
                draft.organization,
                normal_style,
            )
        )

    story.append(
        Spacer(1, 18)
    )

    # ---------------------------------------------
    # SUBJECT
    # ---------------------------------------------

    story.append(
        Paragraph(
            f"<b>Subject: {draft.subject}</b>",
            subject_style,
        )
    )

    # ---------------------------------------------
    # SALUTATION
    # ---------------------------------------------

    story.append(
        Paragraph(
            draft.salutation,
            normal_style,
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # ---------------------------------------------
    # BODY
    # ---------------------------------------------

    for paragraph in draft.body:
        story.append(
            Paragraph(
                paragraph,
                normal_style,
            )
        )

        story.append(
            Spacer(1, 12)
        )

    # ---------------------------------------------
    # CLOSING
    # ---------------------------------------------

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            draft.closing,
            normal_style,
        )
    )

    # ---------------------------------------------
    # SENDER
    # ---------------------------------------------

    if draft.sender_name:
        story.append(
            Spacer(1, 24)
        )

        story.append(
            Paragraph(
                draft.sender_name,
                normal_style,
            )
        )

    if draft.sender_details:
        story.append(
            Paragraph(
                draft.sender_details,
                normal_style,
            )
        )

    # ---------------------------------------------
    # BUILD PDF
    # ---------------------------------------------

    document.build(story)

    return file_path