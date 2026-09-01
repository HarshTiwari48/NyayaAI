from app.graph.application_graph import (
    build_application_graph,
)
from app.rag.groq import get_groq_model

from app.core.graph_service import checkpointer


llm = get_groq_model()


application_graph = build_application_graph(
    llm=llm,
    checkpointer=checkpointer,
)