from typing import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated

from app.schemas.application import ApplicationInformation


class ApplicationState(TypedDict):
    # Conversation
    messages: Annotated[list[BaseMessage], add_messages]
    user_input: str

    # Collected information
    application_info: ApplicationInformation | None

    # Information collection
    missing_fields: list[str]
    is_complete: bool
    follow_up_question: str | None

    # Final document
    application_draft: dict | None