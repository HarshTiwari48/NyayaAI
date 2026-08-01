from app.graph.state import AgentState
from app.rag.user_document_retriever import (
    retrieve_user_document_passages,
)


def user_document_research_node(state: AgentState) -> dict:
    documents = state["user_documents"]

    if not documents:
        return {"evidence": []}

    queries = state["statute_queries"] + state["judgment_queries"]

    # Fallback for document-focused questions where planner
    # doesn't request statute/judgment research.
    if not queries:
        queries = [state["query"]]

    evidence = []
    seen = set()

    for query in queries[:2]:
        results = retrieve_user_document_passages(
            query=query,
            documents=documents,
            k=3,
        )

        for document in results:
            key = document.page_content

            if key not in seen:
                seen.add(key)
                evidence.append(document)

    return {"evidence": evidence}