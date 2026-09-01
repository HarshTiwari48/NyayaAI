from app.graph.application_state import ApplicationState


def route_after_collection(
    state: ApplicationState,
) -> str:
    if state.get("is_complete", False):
        return "generate"

    return "follow_up"