from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

COLLECTION_NAME = "nyaya-statutes"

def create_vector_store(
        documents: list[Document],
        embedding_model: Embeddings,
        persist_directory: Path,
) -> Chroma:
    if not documents:
        raise ValueError("Cannot create a vector store with no documents.")

    persist_directory.mkdir(parents=True, exist_ok=True)

    return Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(persist_directory),
    )

def load_vector_store(
    embedding_model: Embeddings,
    persist_directory: Path,
) -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(persist_directory),
    )