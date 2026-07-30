from pathlib import Path

from app.rag.chunker import chunk_sections
from app.rag.embeddings import get_embedding_model
from app.rag.loader import load_pdf
from app.rag.parser import parse_statute
from app.rag.vector_store import create_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]

STATUTES_PATH = PROJECT_ROOT / "Data" / "statutes"
VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"


STATUTES = [
    {
        "file": "BNS.pdf",
        "act": "Bharatiya Nyaya Sanhita, 2023",
        "act_code": "BNS",
    },
    {
        "file": "BNSS.pdf",
        "act": "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "act_code": "BNSS",
    },
    {
        "file": "BSA.pdf",
        "act": "Bharatiya Sakshya Adhiniyam, 2023",
        "act_code": "BSA",
    },
]


def main() -> None:
    all_chunks = []

    for statute in STATUTES:
        pdf_path = STATUTES_PATH / statute["file"]

        pages = load_pdf(pdf_path)

        sections = parse_statute(
            pages,
            act=statute["act"],
            act_code=statute["act_code"],
        )

        chunks = chunk_sections(sections)
        all_chunks.extend(chunks)

        print(
            f"{statute['act_code']}: "
            f"{len(pages)} pages → "
            f"{len(sections)} sections → "
            f"{len(chunks)} chunks"
        )

    print(f"\nTotal chunks: {len(all_chunks)}")

    embedding_model = get_embedding_model()

    create_vector_store(
        documents=all_chunks,
        embedding_model=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    print(f"Indexed {len(all_chunks)} chunks successfully.")


if __name__ == "__main__":
    main()