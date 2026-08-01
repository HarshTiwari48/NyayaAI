from pathlib import Path

from app.rag.loader import load_pdf
from app.rag.user_document_retriever import (
    retrieve_user_document_passages,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Temporary test using an existing PDF.
TEST_PDF = PROJECT_ROOT / "Data" / "statutes" / "BNS.pdf"


def main() -> None:
    documents = load_pdf(TEST_PDF)

    results = retrieve_user_document_passages(
        query="cheating someone by dishonestly taking their money",
        documents=documents,
        k=5,
    )

    print(f"Retrieved: {len(results)}")

    for i, document in enumerate(results, start=1):
        print(
            f"\n{i}. Score: "
            f"{document.metadata['similarity_score']:.4f}"
        )
        print(document.page_content[:300])


if __name__ == "__main__":
    main()