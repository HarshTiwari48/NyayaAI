from pathlib import Path

from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store
from app.services.llm import get_llm
from app.services.rag_service import answer_question


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


def main() -> None:
    embedding_model = get_embedding_model()

    vector_store = load_vector_store(
        embedding_model=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    llm = get_llm()

    question = "What is the punishment for cheating?"

    result = answer_question(
        question=question,
        vector_store=vector_store,
        llm=llm,
    )

    print("\nQUESTION")
    print(question)

    print("\nANSWER")
    print(result["answer"])

    print("\nRETRIEVED SOURCES")

    for source in result["sources"]:
        print(
            f"{source['act']} Section {source['section']} "
            f"(chunk {source['chunk_index']})"
        )


if __name__ == "__main__":
    main()