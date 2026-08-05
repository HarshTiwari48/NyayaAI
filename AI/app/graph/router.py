from app.graph.state import AgentState

def route_after_analysis(state: AgentState) -> str:
    print("\n===== ROUTER =====")
    print("needs_legal_research =", state["needs_legal_research"])
    print("==================\n")

    if state["needs_legal_research"]:
        return "planner"

    return "generator"


def route_after_verification(
    state: AgentState,
) -> str:

    if state["verified"]:
        return "end"

    if state["retry_count"] >= 1:
        return "end"

    return "retry"