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
- Important information that is still genuinely needed to write
  a useful application.

Do not invent personal details.

An application can be addressed to many different people or organizations,
including schools, colleges, companies, government offices, landlords,
or other authorities.

IMPORTANT RULES:

- Do NOT require a fixed set of fields for every application.
- Determine required information based on the specific purpose
  of the application.
- Ask only for information that is necessary to clearly communicate
  the request, complaint, explanation, or purpose.
- Do NOT require optional administrative details such as student ID,
  roll number, course, class, contact information, supporting documents,
  or sender details unless they are genuinely necessary for the
  particular application.
- The recipient and organization may be represented with reasonable
  placeholders in the final application if the user does not provide them.
- The sender's name and details may also be left as placeholders.
- Do not mark the application incomplete merely because optional
  identifying information is missing.

Mark the application as complete when the purpose and the important
situation-specific details are sufficiently clear to write a useful
application.

For example:
- For a leave application, the reason and leave duration/dates are
  generally the important details.
- For a complaint, the incident or problem being complained about
  should be clear.
- For a request, what the user is requesting and any important
  circumstances should be clear.

Do not ask for information that the user has already provided in
the conversation.
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

        application_info = {
            "purpose": result.purpose,
            "recipient": result.recipient,
            "organization": result.organization,
            "sender_name": result.sender_name,
            "sender_details": result.sender_details,
            "additional_details": result.additional_details,
        }

        return {
            "application_info": application_info,
            "missing_fields": result.missing_fields,
            "is_complete": result.is_complete,
        }

    return application_collector_node