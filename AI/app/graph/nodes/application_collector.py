from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.application_state import ApplicationState
from app.schemas.application import ApplicationInformation


COLLECTOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an information collection component for an application-writing system.

Your job is to analyze the user's request and the conversation so far.

Determine:
- What application the user wants to write.
- Information already provided by the user.
- Important information that is still missing.

Do not invent personal details.

An application can be addressed to many different people or organizations,
including schools, colleges, companies, government offices, landlords,
or other authorities.

Only require information that is genuinely necessary to create a useful
application.

Do not require unnecessary details.

The user's name and sender details are optional because they can be
left as placeholders in the final application if necessary.
""",
        ),
        (
            "human",
            """
Conversation:

{messages}

Current user input:

{user_input}
""",
        ),
    ]
)


class CollectionResult(ApplicationInformation):
    missing_fields: list[str]
    is_complete: bool


def create_application_collector_node(
    llm: BaseChatModel,
):
    structured_llm = llm.with_structured_output(
        CollectionResult
    )

    chain = COLLECTOR_PROMPT | structured_llm

    def application_collector_node(
        state: ApplicationState,
    ) -> dict:
        history = "\n".join(
            f"{message.type.upper()}: {message.content}"
            for message in state["messages"]
        )

        result = chain.invoke(
            {
                "messages": history,
                "user_input": state["user_input"],
            }
        )

        application_info = ApplicationInformation(
            purpose=result.purpose,
            recipient=result.recipient,
            organization=result.organization,
            sender_name=result.sender_name,
            sender_details=result.sender_details,
            additional_details=result.additional_details,
        )

        return {
            "application_info": application_info,
            "missing_fields": result.missing_fields,
            "is_complete": result.is_complete,
        }

    return application_collector_node