from typing import TypedDict
import operator
from typing import Annotated

from langchain_core.documents import Document

class AgentState(TypedDict):
    # Input
    query: str

    # Analyzer output
    case_summary: str
    facts: list[str]
    legal_issues: list[str]

    # Planner output
    statute_queries: list[str]
    judgment_queries: list[str]
    use_user_documents: bool
    
    # Research output
    evidence: Annotated[list[Document], operator.add]

    # Generation
    answer: str

    # Verification
    verified: bool
    verification_feedback: str
    retry_count: int