from pydantic import BaseModel, Field


class ApplicationInformation(BaseModel):
    purpose: str = Field(
        description="The purpose of the application"
    )

    recipient: str | None = Field(
        default=None,
        description="Person or authority receiving the application",
    )

    organization: str | None = Field(
        default=None,
        description=(
            "School, college, office, government department, "
            "or other organization"
        ),
    )

    sender_name: str | None = Field(
        default=None,
        description="Name of the person writing the application",
    )

    sender_details: str | None = Field(
        default=None,
        description=(
            "Relevant details such as class, department, "
            "designation, address, or contact information"
        ),
    )

    details: list[str] = Field(
        default_factory=list,
        description=(
            "Important facts and details provided by the user "
            "that should be included in the application. "
            "For example: reason, dates, duration, incident "
            "details, request details, or other relevant facts."
        ),
    )


class ApplicationDraft(BaseModel):
    recipient: str

    organization: str | None = None

    subject: str

    salutation: str

    body: list[str]

    closing: str

    sender_name: str | None = None

    sender_details: str | None = None