from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import AgentState
from app.schemas.research import ResearchPlan


PLANNER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the research planner for an Indian legal research system.

Based on the case analysis, create focused research queries for
relevant Indian statutory provisions.

Statute queries:
- Generate concise legal concepts.
- Prefer Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS),
  and Bharatiya Sakshya Adhiniyam (BSA).
- Avoid referring to the repealed Indian Penal Code (IPC) unless the user
  explicitly asks about historical law.
- Do not write "search", "check", or "review".
- Focus on the actual legal issues raised by the user.

Set use_user_documents to true only when documents supplied by the user
could materially help answer the question.

Do not invent facts that are absent from the case.
""",
        ),
        (
            "human",
            """
Case summary:
{case_summary}

Facts:
{facts}

Legal issues:
{legal_issues}

Previous verification feedback:
{verification_feedback}
""",
        ),
    ]
)


def create_planner_node(llm: BaseChatModel):
    structured_llm = llm.with_structured_output(ResearchPlan)
    chain = PLANNER_PROMPT | structured_llm

    def planner_node(state: AgentState) -> dict:
        plan = chain.invoke(
            {
                "case_summary": state["case_summary"],
                "facts": state["facts"],
                "legal_issues": state["legal_issues"],
                "verification_feedback": state["verification_feedback"],
            }
        )

        return {
            "statute_queries": plan.statute_queries,
            "use_user_documents": plan.use_user_documents,
        }

    return planner_node