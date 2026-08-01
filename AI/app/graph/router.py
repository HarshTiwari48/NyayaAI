from langgraph.types import Send

from app.graph.state import AgentState


def route_research(state: AgentState):
    routes = []

    if state["statute_queries"]:
        routes.append(Send("statute_research", state))

    if state["judgment_queries"]:
        routes.append(Send("judgment_research", state))

    if not routes:
        routes.append(Send("generator", state))

    return routes


def route_after_verification(state: AgentState) -> str:
    if state["verified"]:
        return "end"

    if state["retry_count"] >= 1:
        return "end"

    return "retry"

def route_research(state: AgentState):
    routes = []

    if state["statute_queries"]:
        routes.append(Send("statute_research", state))

    if state["judgment_queries"]:
        routes.append(Send("judgment_research", state))

    if (
        state["use_user_documents"]
        and state["user_documents"]
    ):
        routes.append(
            Send("user_document_research", state)
        )

    if not routes:
        routes.append(Send("generator", state))

    return routes