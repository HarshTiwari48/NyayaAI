from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from app.graph.state import AgentState
from app.services.rag_service import format_context


GENERATOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are NyayaAI, an Indian legal information assistant.

Use the recent conversation only for conversational context and
understanding references to earlier messages.

Answer the current user's question using the supplied legal evidence.

Evidence priority:
1. USER DOCUMENT
2. Statutes (BNS, BNSS, BSA)
3. Judgments

Rules:
- Treat the uploaded USER DOCUMENT as the primary source of facts.
- Never replace, modify, or contradict facts from the uploaded document
  using retrieved legal documents.
- Use statutes to explain the law that applies to the facts.
- Use judgments only to support or interpret the applicable law.
- Ignore unrelated evidence.
- Do not invent statutes, sections, punishments, or facts.
- Cite statutory claims using the format [BNS Section 318].
- If the available evidence is insufficient, clearly say so.
- Explain everything in clear language.
- Provide legal information, not personalized legal advice.
""",
        ),
        (
            "human",
            """
Recent conversation:
{messages}

Current user question:
{query}

Case summary:
{case_summary}

Facts:
{facts}

Legal issues:
{legal_issues}

Evidence:
{evidence}
""",
        ),
    ]
)


def create_generator_node(llm: BaseChatModel):
    chain = GENERATOR_PROMPT | llm

    def generator_node(state: AgentState) -> dict:

        # -----------------------------------------------------
        # DEDUPLICATE EVIDENCE
        # -----------------------------------------------------

        unique = {}

        for document in state["evidence"]:
            key = (
                document.metadata.get("source_type"),
                document.metadata.get("act_code"),
                document.metadata.get("section"),
                document.metadata.get("document_id"),
                document.metadata.get("chunk_index"),
                document.page_content[:100],
            )

            unique[key] = document

        evidence = list(unique.values())

        # -----------------------------------------------------
        # PRIORITIZE EVIDENCE
        # -----------------------------------------------------

        user_docs = []
        statutes = []
        judgments = []

        for document in evidence:
            source = document.metadata.get("source_type")

            if source == "user_document":
                user_docs.append(document)

            elif source == "judgment":
                judgments.append(document)

            else:
                statutes.append(document)

        evidence = (
            user_docs[:3]
            + statutes[:3]
            + judgments[:3]
        )

        context = format_context(evidence)

        # -----------------------------------------------------
        # RECENT CONVERSATION ONLY
        # -----------------------------------------------------

        recent_messages = state["messages"][-6:]

        history = "\n".join(
            f"{msg.type.upper()}: {msg.content}"
            for msg in recent_messages
        )

        response = chain.invoke(
            {
                "messages": history,
                "query": state["query"],
                "case_summary": state["case_summary"],
                "facts": "\n".join(state["facts"]),
                "legal_issues": "\n".join(state["legal_issues"]),
                "evidence": context,
            }
        )

        return {
            "answer": response.content,
            "messages": [
                AIMessage(content=response.content)
            ],
        }

    return generator_node