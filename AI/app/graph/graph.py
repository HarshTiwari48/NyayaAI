from langchain_chroma import Chroma
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from app.graph.nodes.analyzer import create_analyzer_node
from app.graph.nodes.planner import create_planner_node
from app.graph.nodes.statute_research import create_statute_research_node
from app.graph.nodes.judgment_research import judgment_research_node
from app.graph.nodes.user_document_research import (
    user_document_research_node,
)
from app.graph.nodes.generator import create_generator_node
from app.graph.nodes.verifier import create_verifier_node

from app.graph.router import (route_after_verification,
                              route_after_analysis,)
from app.graph.state import AgentState

from langgraph.checkpoint.base import BaseCheckpointSaver


def retry_node(state: AgentState):
    return {
        "retry_count": state["retry_count"] + 1,
    }


def build_graph(
    llm: BaseChatModel,
    vector_store: Chroma,
    checkpointer: BaseCheckpointSaver | None = None,
):
    builder = StateGraph(AgentState)

    builder.add_node(
        "analyzer",
        create_analyzer_node(llm),
    )

    builder.add_node(
        "planner",
        create_planner_node(llm),
    )

    builder.add_node(
        "statute_research",
        create_statute_research_node(vector_store),
    )

    builder.add_node(
        "judgment_research",
        judgment_research_node,
    )

    builder.add_node(
        "user_document_research",
        user_document_research_node,
    )

    builder.add_node(
        "generator",
        create_generator_node(llm),
    )

    builder.add_node(
        "verifier",
        create_verifier_node(llm),
    )

    builder.add_node(
        "retry",
        retry_node,
    )

    builder.add_edge(START, "analyzer")
    builder.add_conditional_edges(
        "analyzer",
        route_after_analysis,
        {
            "planner": "planner",
            "generator": "generator",
        },
    )
    

    # ------------------------
    # FAN OUT
    # ------------------------

    builder.add_edge(
        "planner",
        "statute_research",
    )

    builder.add_edge(
        "planner",
        "judgment_research",
    )

    builder.add_edge(
        "planner",
        "user_document_research",
    )

    # ------------------------
    # FAN IN
    # ------------------------

    builder.add_edge(
        "statute_research",
        "generator",
    )

    builder.add_edge(
        "judgment_research",
        "generator",
    )

    builder.add_edge(
        "user_document_research",
        "generator",
    )

    builder.add_edge(
        "generator",
        "verifier",
    )

    builder.add_conditional_edges(
        "verifier",
        route_after_verification,
        {
            "retry": "retry",
            "end": END,
        },
    )

    builder.add_edge(
        "retry",
        "planner",
    )

    return builder.compile(
        checkpointer=checkpointer,
    )