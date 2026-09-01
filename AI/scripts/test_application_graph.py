import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


from langchain_core.messages import HumanMessage

from app.rag.groq import get_groq_model
from app.graph.application_graph import (
    build_application_graph,
)


def print_result(result: dict):
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print("\nIs complete:")
    print(result.get("is_complete"))

    print("\nMissing fields:")
    print(result.get("missing_fields"))

    if result.get("follow_up_question"):
        print("\nFOLLOW-UP QUESTION:")
        print(result["follow_up_question"])

    if result.get("application_draft"):
        print("\nAPPLICATION DRAFT:")
        print()

        draft = result["application_draft"]

        print("Recipient:")
        print(draft.get("recipient"))

        print("\nOrganization:")
        print(draft.get("organization"))

        print("\nSubject:")
        print(draft.get("subject"))

        print("\nSalutation:")
        print(draft.get("salutation"))

        print("\nBody:")
        for paragraph in draft.get("body", []):
            print(paragraph)
            print()

        print("Closing:")
        print(draft.get("closing"))

        print("\nSender:")
        print(draft.get("sender_name"))

        print("\nSender details:")
        print(draft.get("sender_details"))


def main():
    llm = get_groq_model()

    graph = build_application_graph(llm)

    user_input = (
        "I need to write an application to my college "
        "asking for three days leave because I am sick."
    )

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_input": user_input,
            "application_info": None,
            "missing_fields": [],
            "is_complete": False,
            "follow_up_question": None,
            "application_draft": None,
        }
    )

    print_result(result)


if __name__ == "__main__":
    main()