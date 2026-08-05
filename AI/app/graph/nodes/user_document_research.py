from app.graph.state import AgentState
from app.rag.user_document_retriever import (
    retrieve_user_document_passages,
)


def user_document_research_node(state: AgentState) -> dict:

    if not state["use_user_documents"]:
        return {"evidence": []}

    documents = state["user_documents"]

    if not documents:
        return {"evidence": []}

    queries = [state["query"]]

    evidence = []
    seen = set()

    for query in queries[:2]:
        results = retrieve_user_document_passages(
            query=query,
            documents=documents,
            k=3,
        )
        print("QUERY:", query)
        print("RESULTS:", len(results))

        for document in results:
            key = document.page_content
            print(document.page_content[:150])

            if key not in seen:
                seen.add(key)
                evidence.append(document)

    return {
        "evidence": evidence,
    }