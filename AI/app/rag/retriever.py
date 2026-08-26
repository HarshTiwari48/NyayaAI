import re

from langchain_core.documents import Document
from langchain_chroma import Chroma


SECTION_QUERY_PATTERN = re.compile(
    r"\b(?P<act>BNS|BNSS|BSA)\s*(?:section|sec\.?)?\s*(?P<section>\d{1,3})\b",
    re.IGNORECASE,
)


def _extract_section_reference(
    query: str,
) -> tuple[str, str] | None:
    match = SECTION_QUERY_PATTERN.search(query)

    if not match:
        return None

    act_code = match.group("act").upper()
    section = match.group("section")

    return act_code, section


def retrieve_documents(
    vector_store: Chroma,
    query: str,
    k: int = 2,
) -> list[Document]:

    section_reference = _extract_section_reference(query)

    # ---------------------------------------------------------
    # EXACT SECTION LOOKUP
    # ---------------------------------------------------------

    if section_reference:
        act_code, section = section_reference

        documents = vector_store.similarity_search(
            query=query,
            k=k,
            filter={
                "$and": [
                    {"act_code": act_code},
                    {"section": section},
                ]
            },
        )

        if documents:
            return documents

    # ---------------------------------------------------------
    # NORMAL SEMANTIC RETRIEVAL
    # ---------------------------------------------------------

    return vector_store.similarity_search(
        query=query,
        k=k,
    )