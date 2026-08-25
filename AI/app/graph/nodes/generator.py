from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import AgentState
from app.services.rag_service import format_context
from langchain_core.messages import AIMessage


GENERATOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
    "system",
    """
You are NyayaAI, an Indian legal information assistant.
The conversation history is the source of conversational context.

If the current question depends on previous messages (for example "What is my name?", "What were we discussing?", "Is there a bail option in this?"), use the conversation history to determine the topic before answering.

Do not say you don't know previous messages if they are present in the conversation history.

Use retrieved legal evidence only for legal reasoning, not for remembering the conversation.

Answer the user's question using only the supplied evidence.

Evidence priority (highest to lowest):
1. USER DOCUMENT (uploaded by the user)
2. Statutes (BNS, BNSS, BSA)


Rules:
- Treat the uploaded USER DOCUMENT as the primary source of facts.
- Never replace, modify, or contradict facts from the uploaded document using retrieved legal documents.
- Use statutes only to explain the law that applies to the facts in the uploaded document.
- If the user asks to summarize, explain, or extract information from the uploaded document, focus almost entirely on the USER DOCUMENT. Mention statutes or judgments only if they directly help answer the user's question.
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
Conversation history:
{messages}

Current user question:
{query}

Case summary:
{case_summary}

The evidence below is ordered by priority.

Priority 1:
USER DOCUMENT

Priority 2:
Relevant Statutes

Priority 3:
Relevant Judgments

Evidence:
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
        

        for doc in evidence:

            source = doc.metadata.get("source_type")

            if source == "user_document":
                user_docs.append(doc)

            
            else: # statute
                statutes.append(doc)

        evidence = (
            user_docs[:3]
            + statutes[:3]
        )
        

        context = format_context(evidence)
        

        history = "\n".join(
            f"{msg.type.upper()}: {msg.content}" 
            for msg in state["messages"]
        )

        response = chain.invoke(
            {
                "messages": history,
                "query": state["query"],
                "case_summary": state["case_summary"],
                "evidence": context,
            }
        )
        

        return {
            "answer": response.content,
            "messages": [AIMessage(content=response.content)],
        }

    return generator_node