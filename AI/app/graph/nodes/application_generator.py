from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.graph.application_state import ApplicationState
from app.schemas.application import ApplicationDraft


APPLICATION_GENERATOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional application-writing assistant.

Generate a clear, formal, and appropriately worded application
based only on the information provided.

Rules:
- Do not invent personal information.
- Do not invent names, dates, addresses, or other facts.
- Preserve all important facts provided in the application details.
- Do not replace specific facts with vague statements.
  For example, if the user says they are sick, do not change it
  to "personal reasons".
- Include relevant dates, durations, reasons, and other important
  details when they are provided.
- If optional sender information is unavailable, leave it null.
- Use placeholders only when genuinely necessary.
- Keep the language appropriate for the recipient and situation.
- The subject should be concise and professional.
- The body should contain well-structured paragraphs.
- Do not add unnecessary legal language.
- Generate only the application structure requested.
""",
        ),
        (
            "human",
            """
Application information:

Purpose:
{purpose}

Recipient:
{recipient}

Organization:
{organization}

Sender name:
{sender_name}

Sender details:
{sender_details}

Important details:
{details}
""",
        ),
    ]
)


def create_application_generator_node(
    llm: BaseChatModel,
):
    structured_llm = llm.with_structured_output(
        ApplicationDraft
    )

    chain = (
        APPLICATION_GENERATOR_PROMPT
        | structured_llm
    )

    def application_generator_node(
        state: ApplicationState,
    ) -> dict:
        info = state["application_info"]

        if not info:
            raise ValueError(
                "Application information is missing."
            )

        draft = chain.invoke(
            {
                "purpose": info["purpose"],
                "recipient": (
                    info["recipient"] or "Not specified"
                ),
                "organization": (
                    info["organization"] or "Not specified"
                ),
                "sender_name": (
                    info["sender_name"] or "Not specified"
                ),
                "sender_details": (
                    info["sender_details"]
                    or "Not specified"
                ),
                "details": "\n".join(
                    f"- {detail}"
                    for detail in info["details"]
                )
                or "None",
            }
        )

        return {
            "application_draft": draft.model_dump(),
            "follow_up_question": None,
        }

    return application_generator_node