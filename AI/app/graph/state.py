from typing import TypedDict
import operator
from typing import Annotated

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # Input
    query: str
    messages: Annotated[list[BaseMessage], add_messages]

    # Analyzer output
    case_summary: str
    facts: list[str]
    legal_issues: list[str]
    needs_legal_research: bool

    # Planner output
    statute_queries: list[str]
    use_user_documents: bool

    # Research output
    user_documents: list[Document]
    evidence: Annotated[list[Document], operator.add]

    # Generation
    answer: str

    # Verification
    verified: bool
    verification_feedback: str