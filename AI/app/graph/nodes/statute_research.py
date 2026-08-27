from langchain_chroma import Chroma

from app.graph.state import AgentState
from app.rag.retriever import retrieve_documents


def create_statute_research_node(vector_store: Chroma):

    def statute_research_node(state: AgentState) -> dict:
        evidence = []
        seen = set()

        # Use the user's actual question as the primary
        # statute retrieval query.
        query = state["query"]

        print("\n========== STATUTE RETRIEVAL ==========")
        print("Original user query:", query)

        documents = retrieve_documents(
            vector_store=vector_store,
            query=query,
            k=5,
        )

        print("\nRetrieved:")

        for document in documents:
            print(
                f"{document.metadata.get('act_code')} "
                f"Section {document.metadata.get('section')} "
                f"| Chunk {document.metadata.get('chunk_index')}"
            )

            key = (
                document.metadata.get("act_code"),
                document.metadata.get("section"),
                document.metadata.get("chunk_index"),
            )

            if key not in seen:
                seen.add(key)
                evidence.append(document)

        print("=======================================\n")

        return {"evidence": evidence}

    return statute_research_node