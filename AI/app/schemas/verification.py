from pydantic import BaseModel, Field


class VerificationResult(BaseModel):
    verified: bool = Field(
        description=(
            "True only if the answer is supported by the supplied evidence "
            "and does not contain unsupported legal claims."
        )
    )

    feedback: str = Field(
        description=(
            "Explain what is unsupported, missing, or incorrect. "
            "If verified, briefly state why."
        )
    )