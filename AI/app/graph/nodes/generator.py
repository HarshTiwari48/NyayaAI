from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import AgentState
from app.services.rag_service import format_context


GENERATOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are NyayaAI, an Indian legal information assistant.

Answer the user's question using only the supplied legal evidence.

Rules:
- Do not invent statutes, sections, facts, or punishments.
- Ignore evidence that is unrelated to the user's question.
- Cite statutory claims using the format [BNS Section 318].
- If the evidence is insufficient, clearly say so.
- Explain the answer in clear language.
- Provide legal information, not personalized legal advice.
""",
        ),
        (
            "human",
            """
User question:
{query}

Case summary:
{case_summary}

Legal evidence:
{evidence}
""",
        ),
    ]
)


def create_generator_node(llm: BaseChatModel):
    chain = GENERATOR_PROMPT | llm

    def generator_node(state: AgentState) -> dict:

        unique = {}

        for document in state["evidence"]:
            key = (
                document.metadata.get("source_type"),
                document.metadata.get("act_code"),
                document.metadata.get("section"),
                document.metadata.get("document_id"),
                document.page_content[:100],
            )

            unique[key] = document

        evidence = list(unique.values())

        user_docs = []
        statutes = []
        judgments = []

        for doc in evidence:

            source = doc.metadata.get("source_type")

            if source == "user_document":
                user_docs.append(doc)

            elif source == "judgment":
                judgments.append(doc)
            else: # statute
                statutes.append(doc)

        evidence = (
            user_docs[:3]
            + statutes[:3]
            + judgments[:3]
        )
        print("\n========== GENERATOR ==========")
        print("User Docs:", len(user_docs))
        print("Statutes:", len(statutes))
        print("Judgments:", len(judgments))
        print("===============================\n")

        context = format_context(evidence)
        print(context[:2500])

        response = chain.invoke(
            {
                "query": state["query"],
                "case_summary": state["case_summary"],
                "evidence": context,
            }
        )
        

        return {
            "answer": response.content,
        }

    return generator_node