from app.graph.state import AgentState
from app.services.judgement_service import retrieve_judgment_evidence


def judgment_research_node(state: AgentState) -> dict:
    evidence = []
    seen = set()

    # Avoid making an API search for every planner query
    queries = state["judgment_queries"][:2]

    for query in queries:
        documents = retrieve_judgment_evidence(
            query=query,
            case_limit=2,
            passage_limit=3,
        )

        for document in documents:
            key = (
                document.metadata.get("document_id"),
                document.page_content,
            )

            if key not in seen:
                seen.add(key)
                evidence.append(document)

    
    return {"evidence": evidence}