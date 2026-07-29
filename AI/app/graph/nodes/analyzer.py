from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import AgentState
from app.schemas.analysis import CaseAnalysis


ANALYZER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the case analysis component of an Indian legal research system.

Analyze the user's situation before legal research begins.

Extract:
1. A concise case summary.
2. Material facts explicitly provided by the user.
3. Potential legal issues that require research.

Do not invent missing facts.
Do not provide legal advice.
Do not decide the final answer.
""",
        ),
        ("human", "{query}"),
    ]
)


def create_analyzer_node(llm: BaseChatModel):
    structured_llm = llm.with_structured_output(CaseAnalysis)

    chain = ANALYZER_PROMPT | structured_llm

    def analyzer_node(state: AgentState) -> dict:
        analysis = chain.invoke(
            {
                "query": state["query"],
            }
        )

        return {
            "case_summary": analysis.case_summary,
            "facts": analysis.facts,
            "legal_issues": analysis.legal_issues,
        }

    return analyzer_node