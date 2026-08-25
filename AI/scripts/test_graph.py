from pathlib import Path

from app.graph.graph import build_graph
from app.rag.groq import get_groq_model
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store
from app.rag.loader import load_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


def main() -> None:
    # ------------------------
    # Load models
    # ------------------------

    embedding_model = get_embedding_model()

    vector_store = load_vector_store(
        embedding_model=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    llm = get_groq_model()

    graph = build_graph(
        llm=llm,
        vector_store=vector_store,
    )

    # ------------------------
    # Test document
    # ------------------------

    test_document_path = (
        PROJECT_ROOT / "Data" / "statutes" / "BNS.pdf"
    )

    user_documents = load_pdf(test_document_path)

    # ------------------------
    # Run graph
    # ------------------------

    result = graph.invoke(
        {
            "query": (
                "According to the document I uploaded, "
                "what does it say about cheating?"
            ),

            "messages": [],

            "case_summary": "",
            "facts": [],
            "legal_issues": [],
            "needs_legal_research": True,

            "statute_queries": [],

            "use_user_documents": True,
            "user_documents": user_documents,

            "evidence": [],

            "answer": "",

            "verified": False,
            "verification_feedback": "",
        }
    )

    # ------------------------
    # Print analysis
    # ------------------------

    print("\nCASE SUMMARY")
    print(result["case_summary"])

    print("\nFACTS")
    for fact in result["facts"]:
        print("-", fact)

    print("\nLEGAL ISSUES")
    for issue in result["legal_issues"]:
        print("-", issue)

    # ------------------------
    # Print planner output
    # ------------------------

    print("\nSTATUTE QUERIES")
    for query in result["statute_queries"]:
        print("-", query)

    print("\nUSE USER DOCUMENTS")
    print(result["use_user_documents"])

    # ------------------------
    # Print evidence
    # ------------------------

    print("\nEVIDENCE")

    for document in result["evidence"]:
        source_type = document.metadata.get("source_type")

        if source_type == "statute":
            print(
                f"{document.metadata.get('act_code', '')} "
                f"Section {document.metadata.get('section', '')} "
                f"| Chunk {document.metadata.get('chunk_index', '')}"
            )

        elif source_type == "user_document":
            print(
                "User Document | "
                f"Score: "
                f"{document.metadata.get('similarity_score', 0):.4f}"
            )

        else:
            print(
                f"Unknown source type: {source_type}"
            )

    # ------------------------
    # Verification
    # ------------------------

    print("\nVERIFICATION")
    print("Verified:", result["verified"])
    print("Feedback:", result["verification_feedback"])

    # ------------------------
    # Answer
    # ------------------------

    print("\nANSWER")
    print(result["answer"])


if __name__ == "__main__":
    main()