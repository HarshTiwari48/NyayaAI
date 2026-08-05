from langchain_core.messages import HumanMessage

from app.graph.state import AgentState


def create_initial_state(query: str) -> AgentState:
    return {
        "messages": [
            HumanMessage(content=query),
        ],
        "query": query,
        "case_summary": "",
        "facts": [],
        "legal_issues": [],
        "needs_legal_research": True,
        "statute_queries": [],
        "judgment_queries": [],
        "use_user_documents": False,
        "evidence": [],
        "user_documents": [],
        "answer": "",
        "verified": False,
        "verification_feedback": "",
        "retry_count": 0,
    }