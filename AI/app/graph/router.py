from app.graph.state import AgentState


def route_after_analysis(state: AgentState) -> str:
    print("\n===== ROUTER =====")
    print(
        "needs_legal_research =",
        state.get("needs_legal_research", False),
    )
    print("==================\n")

    if state.get("needs_legal_research", False):
        return "planner"

    return "generator"


def route_after_verification(
    state: AgentState,
) -> str:

    print("\n===== VERIFICATION ROUTER =====")
    print("verified =", state.get("verified", False))
    print("retry_count =", state.get("retry_count", 0))
    print("================================\n")

    if state.get("verified", False):
        return "end"

    if state.get("retry_count", 0) >= 1:
        return "end"

    return "retry" 