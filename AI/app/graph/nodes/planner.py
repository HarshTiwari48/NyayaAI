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

Given an analyzed case, decide what legal research is required.

Available research sources:
- statutes
- judgments
- user_documents

Create focused research queries rather than answering the case yourself.

Use only sources that are actually relevant.
Do not provide legal conclusions.
""",
        ),
        (
    "human",
    """
Case summary:
{case_summary}

Facts:
{facts}

Potential legal issues:
{legal_issues}

Previous verification feedback:
{verification_feedback}

Research attempt:
{retry_count}

Create a research plan based on the case.

If this is a retry, use the verification feedback to identify what evidence
was missing or insufficient and create improved research queries.
Do not simply repeat the previous research queries.
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
                "retry_count": state["retry_count"],
            }
        )

        return {
            "research_queries": plan.research_queries,
            "research_sources": plan.research_sources,
        }

    return planner_node