from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from app.graph.nodes.analyzer import create_analyzer_node
from app.graph.state import AgentState


def planner_node(state: AgentState) -> dict:
    return {
        "research_queries": [state["query"]],
        "research_sources": ["statutes"],
    }


def build_graph(llm: BaseChatModel):
    builder = StateGraph(AgentState)

    builder.add_node(
        "analyzer",
        create_analyzer_node(llm),
    )

    builder.add_node("planner", planner_node)

    builder.add_edge(START, "analyzer")
    builder.add_edge("analyzer", "planner")
    builder.add_edge("planner", END)

    return builder.compile()