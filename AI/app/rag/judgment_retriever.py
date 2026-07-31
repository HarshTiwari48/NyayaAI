import numpy as np

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.embeddings import get_embedding_model


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)


def chunk_judgments(
    documents: list[Document],
) -> list[Document]:
    return splitter.split_documents(documents)


def retrieve_judgment_passages(
    query: str,
    documents: list[Document],
    k: int = 5,
) -> list[Document]:

    chunks = chunk_judgments(documents)

    if not chunks:
        return []

    embedding_model = get_embedding_model()

    query_embedding = np.array(
        embedding_model.embed_query(query)
    )

    chunk_embeddings = np.array(
        embedding_model.embed_documents(
            [chunk.page_content for chunk in chunks]
        )
    )

    # Cosine similarity
    query_norm = np.linalg.norm(query_embedding)
    chunk_norms = np.linalg.norm(
        chunk_embeddings,
        axis=1,
    )

    scores = (
        chunk_embeddings @ query_embedding
    ) / (chunk_norms * query_norm + 1e-10)

    ranked_indices = np.argsort(scores)[::-1]

    results = []
    case_counts = {}

    MAX_PER_CASE = 2
    MIN_SCORE = 0.35

    for index in ranked_indices:
        score = float(scores[index])

        if score < MIN_SCORE:
            break

        chunk = chunks[index]
        case_id = chunk.metadata.get("document_id")

        count = case_counts.get(case_id, 0)

        if count >= MAX_PER_CASE:
            continue

        chunk.metadata["similarity_score"] = score

        results.append(chunk)
        case_counts[case_id] = count + 1

        if len(results) >= k:
            break

    return results