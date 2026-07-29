from typing import Literal
from pydantic import BaseModel, Field

ResearchSource = Literal["statutes", "judgments", "user_documents"]

class ResearchPlan(BaseModel):
    research_queries: list[str] = Field(
        description="Focused legal research queries needed to answer the case"
    )

    research_sources: list[ResearchSource] = Field(
        description="Sources that should be searched for evidence."
    )