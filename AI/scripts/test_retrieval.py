from pathlib import Path

from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store
from app.rag.retriever import retrieve_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


def main() -> None:
    embedding_model = get_embedding_model()

    vector_store = load_vector_store(
        embedding_model=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    TEST_QUERIES = [
        "BNS Section 325",
        "What does BNS Section 325 state?",
        "What is the punishment for killing a dog?",
        "What is the punishment for killing an animal?",
        "What is the punishment for theft?",
        "What is the punishment for cheating?",
        "What law deals with causing death by negligence?",
        "What are the rules regarding electronic evidence?",
    ]

    for query in TEST_QUERIES:
        print(f"\n{'=' * 70}")
        print(f"QUERY: {query}")
        print("=" * 70)

        results = retrieve_documents(
            vector_store=vector_store,
            query=query,
            k=5,
        )

        for i, document in enumerate(results, start=1):
            print(
                f"{i}. "
                f"{document.metadata.get('act_code')} "
                f"Section {document.metadata.get('section')} "
                f"| Chunk {document.metadata.get('chunk_index')}"
            )

            print(document.page_content[:250])
            print("-" * 60)


if __name__ == "__main__":
    main()