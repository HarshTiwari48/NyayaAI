from typing import Literal
from pydantic import BaseModel, Field

ResearchSource = Literal["statutes", "judgments", "user_documents"]

class ResearchPlan(BaseModel):
    statute_queries: list[str] = Field(
        default_factory=list,
        description="Queries for finding relevant provisions in Indian statutes.",
    )

    judgment_queries: list[str] = Field(
        default_factory=list,
        description="Queries for finding relevant Indian judicial precedents.",
    )

    use_user_documents: bool = Field(
        default=False,
        description="Whether documents uploaded by the user should be researched.",
    )