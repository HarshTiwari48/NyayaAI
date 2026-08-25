from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    statute_queries: list[str] = Field(
        default_factory=list,
        description="Queries for finding relevant provisions in Indian statutes.",
    )

    use_user_documents: bool = Field(
        default=False,
        description="Whether documents uploaded by the user should be researched.",
    )