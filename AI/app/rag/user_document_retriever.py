import numpy as np

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.embeddings import get_embedding_model


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
)


def retrieve_user_document_passages(
    query: str,
    documents: list[Document],
    k: int = 5,
) -> list[Document]:

    if not documents:
        return []

    chunks = splitter.split_documents(documents)

    embedding_model = get_embedding_model()

    query_embedding = np.array(
        embedding_model.embed_query(query)
    )

    chunk_embeddings = np.array(
        embedding_model.embed_documents(
            [chunk.page_content for chunk in chunks]
        )
    )

    query_norm = np.linalg.norm(query_embedding)
    chunk_norms = np.linalg.norm(
        chunk_embeddings,
        axis=1,
    )

    scores = (
        chunk_embeddings @ query_embedding
    ) / (chunk_norms * query_norm + 1e-10)

    top_indices = np.argsort(scores)[::-1][:k]

    results = []

    for index in top_indices:
        chunk = chunks[index]

        chunk.metadata["source_type"] = "user_document"
        chunk.metadata["similarity_score"] = float(scores[index])

        results.append(chunk)

    return results