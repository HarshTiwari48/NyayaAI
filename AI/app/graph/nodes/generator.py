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
        context = format_context(state["evidence"])

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