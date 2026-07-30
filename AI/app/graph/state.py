from typing import TypedDict
from langchain_core.documents import Document

class AgentState(TypedDict):
    # Input
    query: str

    # Analyzer output
    case_summary: str
    facts: list[str]
    legal_issues: list[str]

    # Planner output
    research_queries: list[str]
    research_sources: list[str]

    # Research output
    evidence: list[Document]

    # Generation
    answer: str

    # Verification
    verified: bool
    verification_feedback: str
    retry_count: int