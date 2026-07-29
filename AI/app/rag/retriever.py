from langchain_core.documents import Document
from langchain_chroma import Chroma


def retrieve_documents(
        vector_store: Chroma,
        query: str,
        k: int = 5, 
) -> list[Document]:
    return vector_store.similarity_search(
        query=query, 
        k=k
        )