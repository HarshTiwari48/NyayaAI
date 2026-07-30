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

    TEST_QUERIES = [
    "What is the punishment for cheating?",
    "When can a person get bail in a non-bailable offence?",
    "Are electronic or digital records admissible as evidence?",
]


    for query in TEST_QUERIES:
        print(f"\n{'=' * 70}")
        print(f"QUERY: {query}")
        print("=" * 70)

        results = vector_store.similarity_search_with_score(
            query,
            k=5,
        )

        for i, (document, score) in enumerate(results, start=1):
            print(
                f"{i}. "
                f"{document.metadata['act_code']} "
                f"Section {document.metadata['section']} "
                f"| Chunk {document.metadata['chunk_index']} "
                f"| Score: {score:.4f}"
            )

            print(document.page_content[:250])
            print("-" * 60)


if __name__ == "__main__":
    main()