from pathlib import Path

from app.rag.chunker import chunk_sections
from app.rag.embeddings import get_embedding_model
from app.rag.loader import load_pdf
from app.rag.parser import parse_statute
from app.rag.vector_store import create_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BNS_PATH = PROJECT_ROOT / "Data" / "statutes" / "BNS.pdf"
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


def main() -> None:
    pages = load_pdf(BNS_PATH)

    sections = parse_statute(
        pages,
        act="Bharatiya Nyaya Sanhita, 2023",
        act_code="BNS",
    )

    chunks = chunk_sections(sections)

    print(
        f"Loaded {len(pages)} pages → "
        f"{len(sections)} sections → "
        f"{len(chunks)} chunks"
    )

    embedding_model = get_embedding_model()

    create_vector_store(
        documents=chunks,
        embedding_model=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    print(f"Indexed {len(chunks)} chunks successfully.")


if __name__ == "__main__":
    main()