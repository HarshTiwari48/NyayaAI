from langchain_chroma import Chroma

from app.graph.state import AgentState
from app.rag.retriever import retrieve_documents



def create_statute_research_node(vector_store: Chroma):

    def statute_research_node(state: AgentState) -> dict:
        evidence = []
        seen = set()

        if not state["statute_queries"]:
            return {"evidence": []}

        for query in state["statute_queries"][:2]:
            documents = retrieve_documents(
                vector_store=vector_store,
                query=query,
                k=2,
            )

            for document in documents:
                key = (
                    document.metadata.get("act_code"),
                    document.metadata.get("section"),
                    document.metadata.get("chunk_index"),
                )

                if key not in seen:
                    seen.add(key)
                    evidence.append(document)

        return {"evidence": evidence}

    return statute_research_node