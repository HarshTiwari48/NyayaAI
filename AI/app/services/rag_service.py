from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.rag.retriever import retrieve_documents


SYSTEM_PROMPT = """
You are NyayaAI, an Indian legal information assistant.

Answer the user's question using only the provided legal context.

Rules:
- If a USER DOCUMENT is provided, treat it as the primary source of facts.
- Use statutes and judgments only to interpret or explain the facts in the user document.
- Do not invent legal provisions.
- Do not claim a section says something unless supported by the context.
- If the provided context is insufficient, clearly say so.
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
    if not documents:
        return "No legal evidence available."

    priority = {
        "user_document": 0,
        "statute": 1,
        "judgment": 2,
    }

    documents = sorted(
        documents,
        key=lambda d: priority.get(
            d.metadata.get("source_type"),
            99,
        ),
    )

    parts: list[str] = []

    for document in documents:

        source_type = document.metadata.get("source_type")

        if source_type == "user_document":

            parts.append(
                "[USER DOCUMENT]\n"
                f"{document.page_content}"
            )

        elif source_type == "judgment":

            parts.append(
                f"[JUDGMENT]\n"
                f"Case: {document.metadata.get('case_name', 'Unknown')}\n"
                f"Date: {document.metadata.get('date', '')}\n\n"
                f"{document.page_content}"
            )

        else:

            parts.append(
                f"[{document.metadata.get('act_code', 'Unknown')} "
                f"Section {document.metadata.get('section', 'Unknown')}]\n"
                f"{document.page_content}"
            )

    return "\n\n-----------------------------\n\n".join(parts)


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