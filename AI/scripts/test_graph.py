from app.graph.graph import build_graph
from app.services.llm import get_llm

from pathlib import Path

from app.graph.graph import build_graph
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store
from app.services.llm import get_llm


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


def main() -> None:
    embedding_model = get_embedding_model()

    vector_store = load_vector_store(
            embedding_model=embedding_model,
            persist_directory=VECTOR_STORE_PATH,
        )

    llm = get_llm()
    graph = build_graph(
            llm=llm,
            vector_store=vector_store,
        )
    
    

    result = graph.invoke(
        {
            "query": (
                "A person scammed me with a laptop, "
                "I transferred him the money and then he disappeared. I never got the laptop"
            ),
            "case_summary": "",
            "facts": [],
            "legal_issues": [],
            "research_queries": [],
            "research_sources": [],
            "evidence": [],
            "answer": "",
            "verified": False,
            "retry_count": 0,
        }
    )

    print("\nCASE SUMMARY")
    print(result["case_summary"])

    print("\nFACTS")
    for fact in result["facts"]:
        print("-", fact)

    print("\nLEGAL ISSUES")
    for issue in result["legal_issues"]:
        print("-", issue)

    print("\nRESEARCH QUERIES")
    for query in result["research_queries"]:
        print("-", query)

    print("\nRESEARCH SOURCES")
    for source in result["research_sources"]:
        print("-", source)

    print("\nEVIDENCE")

    for document in result["evidence"]:
        print(
            f"{document.metadata['act_code']} "
            f"Section {document.metadata['section']} "
            f"| Chunk {document.metadata['chunk_index']}"
        )
    print("\nANSWER")
    print(result["answer"])


if __name__ == "__main__":
    main()