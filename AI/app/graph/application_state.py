from typing import Any, Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ApplicationState(TypedDict):
    # Conversation
    messages: Annotated[list[BaseMessage], add_messages]
    user_input: str

    # Collected information
    application_info: dict[str, Any] | None

    # Information collection
    missing_fields: list[str]
    is_complete: bool
    follow_up_question: str | None

    # Final document
    application_draft: dict | None