from pydantic import BaseModel, Field

class CaseAnalysis(BaseModel):
    case_summary: str = Field(
        description="A concise summary of the user's situation."
    )

    facts: list[str] = Field(
        description="Material facts explicitly stated by the user."
    )

    legal_issues: list[str] = Field(
        description="Potential legal issues that may require research."
    )