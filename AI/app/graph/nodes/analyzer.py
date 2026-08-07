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

If an uploaded document is provided, use it as the primary source of facts.

Extract:
1. A concise case summary.
2. Material facts explicitly provided.
3. Potential legal issues requiring research.
4. needs_legal_research.

Set needs_legal_research to:

True:
- Questions requiring statutes.
- Questions requiring case law.
- Questions requiring legal analysis.
- Questions about rights, offences, procedures or legal consequences.
- Summarizing or explaining uploaded legal documents.

False:
- Greetings.
- Small talk.
- Memory questions (e.g. "What is my name?")
- Questions about previous conversation.
- Questions answerable purely from the conversation without researching law.

Do not invent missing facts.
Do not provide legal advice.
Do not decide the final answer.
""",
        ),
        (
            "human",
            """
User query:
{query}

Uploaded document:
{document}
""",
        ),
    ]
)


def create_analyzer_node(llm: BaseChatModel):
    structured_llm = llm.with_structured_output(CaseAnalysis)

    chain = ANALYZER_PROMPT | structured_llm

    def analyzer_node(state: AgentState) -> dict:
        print("\n========== ANALYZER ==========")
        print("Messages in state:", len(state["messages"]))

        for msg in state["messages"]:
            print(type(msg).__name__, ":", msg.content[:100])

        

        document_text = ""
        conversation = []
        for message in state["messages"]:
            role = "User"

            if message.type == "ai":
                role = "Assistant"

            conversation.append(
                f"{role}: {message.content}"
            )

        conversation_text = "\n".join(conversation)

            

        if state["user_documents"]:
            document_text = "\n\n".join(
                doc.page_content
                for doc in state["user_documents"][:3]
            )

        analysis = chain.invoke(
            {
                "query": conversation_text,
                "document": document_text,
            }
        )

        

        return {
            "case_summary": analysis.case_summary,
            "facts": analysis.facts,
            "legal_issues": analysis.legal_issues,
            "needs_legal_research": analysis.needs_legal_research,
        }   
        
    

    return analyzer_node