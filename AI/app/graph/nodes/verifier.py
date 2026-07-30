from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import AgentState
from app.schemas.verification import VerificationResult
from app.services.rag_service import format_context


VERIFIER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the verification component of an Indian legal research system.

Check whether the generated answer is supported by the supplied legal evidence.

Verify that:
- Legal claims are supported by the evidence.
- Cited sections actually appear in the evidence.
- The answer does not invent facts, provisions, or punishments.
- The answer addresses the user's question.

If important evidence is missing or a claim is unsupported,
mark the answer as not verified and explain what needs further research.
""",
        ),
        (
            "human",
            """
User question:
{query}

Evidence:
{evidence}

Generated answer:
{answer}
""",
        ),
    ]
)


def create_verifier_node(llm: BaseChatModel):
    structured_llm = llm.with_structured_output(VerificationResult)
    chain = VERIFIER_PROMPT | structured_llm

    def verifier_node(state: AgentState) -> dict:
        result = chain.invoke(
            {
                "query": state["query"],
                "evidence": format_context(state["evidence"]),
                "answer": state["answer"],
            }
        )

        return {
            "verified": result.verified,
            "verification_feedback": result.feedback,
        }

    return verifier_node