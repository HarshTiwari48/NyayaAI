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

    needs_legal_research: bool = Field(
        description=(
            "True if answering the user's request requires legal research "
            "(statutes or judgments). False for normal conversation, "
            "memory questions, greetings, or general chat."
        )
    )