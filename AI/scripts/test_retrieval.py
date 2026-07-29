from pathlib import Path

from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


def main() -> None:
    embedding_model = get_embedding_model()

    vector_store = load_vector_store(
        embedding_model=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    query = "What is the punishment for cheating?"

    results = vector_store.similarity_search_with_score(
        query=query,
        k=5,
    )

    print(f"\nQuery: {query}\n")

    for index, (document, score) in enumerate(results, start=1):
        print(
            f"{index}. "
            f"{document.metadata['act_code']} "
            f"Section {document.metadata['section']} "
            f"| Chunk {document.metadata['chunk_index']} "
            f"| Score: {score:.4f}"
        )

        print(document.page_content[:250])
        print("-" * 60)


if __name__ == "__main__":
    main()