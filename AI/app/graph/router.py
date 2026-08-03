from app.graph.state import AgentState


def route_after_verification(
    state: AgentState,
) -> str:

    if state["verified"]:
        return "end"

    if state["retry_count"] >= 1:
        return "end"

    return "retry"