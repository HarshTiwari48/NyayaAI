from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from app.graph.application_state import ApplicationState


FOLLOW_UP_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are helping collect information needed to write an application.

Ask the user for the missing information.

Rules:
- Ask naturally and conversationally.
- Ask only for information that is actually missing.
- Do not ask unnecessary questions.
- If multiple pieces of information are missing, combine them
  into one clear question when possible.
- Do not mention internal field names.
- Do not generate the application yet.
""",
        ),
        (
            "human",
            """
The user wants to write an application.

Purpose:
{purpose}

Missing information:
{missing_fields}
""",
        ),
    ]
)


def create_application_follow_up_node(
    llm: BaseChatModel,
):
    chain = FOLLOW_UP_PROMPT | llm

    def application_follow_up_node(
        state: ApplicationState,
    ) -> dict:
        application_info = state["application_info"]

        response = chain.invoke(
            {
                "purpose": application_info.purpose,
                "missing_fields": ", ".join(
                    state["missing_fields"]
                ),
            }
        )

        question = response.content

        return {
            "follow_up_question": question,
            "messages": [
                AIMessage(content=question)
            ],
        }

    return application_follow_up_node