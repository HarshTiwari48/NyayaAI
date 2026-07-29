from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.rag.retriever import retrieve_documents


SYSTEM_PROMPT = """
You are NyayaAI, an Indian legal information assistant.

Answer the user's question using only the provided legal context.

Rules:
- Do not invent legal provisions.
- Do not claim a section says something unless supported by the context.
- If the provided context is insufficient, say that the available sources
  are insufficient to answer reliably.
- Clearly distinguish legal information from legal advice.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """
Legal context:

{context}

User question:
{question}
""",
        ),
    ]
)


def format_context(documents: list[Document]) -> str:
    parts: list[str] = []

    for document in documents:
        act = document.metadata.get("act_code", "Unknown")
        section = document.metadata.get("section", "Unknown")

        parts.append(
            f"[{act} Section {section}]\n"
            f"{document.page_content}"
        )

    return "\n\n---\n\n".join(parts)


def answer_question(
    *,
    question: str,
    vector_store,
    llm: BaseChatModel,
) -> dict:

    documents = retrieve_documents(
        vector_store=vector_store,
        query=question,
        k=5,
    )

    context = format_context(documents)

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    sources = [
        {
            "act": document.metadata.get("act_code"),
            "section": document.metadata.get("section"),
            "chunk_index": document.metadata.get("chunk_index"),
        }
        for document in documents
    ]

    return {
        "answer": response.content,
        "sources": sources,
    }