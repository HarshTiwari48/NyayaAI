from typing import Literal

from app.graph.state import AgentState


def route_research(
    state: AgentState,
) -> Literal["statute_research", "generator"]:

    if "statutes" in state["research_sources"]:
        return "statute_research"

    return "generator"