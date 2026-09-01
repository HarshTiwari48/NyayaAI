from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from app.graph.application_state import ApplicationState
from app.graph.application_router import route_after_collection

from app.graph.nodes.application_collector import (
    create_application_collector_node,
)
from app.graph.nodes.application_follow_up import (
    create_application_follow_up_node,
)
from app.graph.nodes.application_generator import (
    create_application_generator_node,
)


def build_application_graph(
    llm: BaseChatModel,
    checkpointer: BaseCheckpointSaver | None = None,
):
    builder = StateGraph(ApplicationState)

    # --------------------------------------------------
    # NODES
    # --------------------------------------------------

    builder.add_node(
        "collector",
        create_application_collector_node(llm),
    )

    builder.add_node(
        "follow_up",
        create_application_follow_up_node(llm),
    )

    builder.add_node(
        "generator",
        create_application_generator_node(llm),
    )

    # --------------------------------------------------
    # START → COLLECTOR
    # --------------------------------------------------

    builder.add_edge(
        START,
        "collector",
    )

    # --------------------------------------------------
    # COLLECTOR → FOLLOW-UP OR GENERATOR
    # --------------------------------------------------

    builder.add_conditional_edges(
        "collector",
        route_after_collection,
        {
            "follow_up": "follow_up",
            "generate": "generator",
        },
    )

    # --------------------------------------------------
    # FOLLOW-UP → END
    # --------------------------------------------------

    builder.add_edge(
        "follow_up",
        END,
    )

    # --------------------------------------------------
    # GENERATOR → END
    # --------------------------------------------------

    builder.add_edge(
        "generator",
        END,
    )

    return builder.compile(
        checkpointer=checkpointer,
    )