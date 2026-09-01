import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from langchain_core.messages import HumanMessage

from app.core.application_graph_service import (
    application_graph,
)


THREAD_ID = "application-test-001"


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
        print("\nAPPLICATION DRAFT:\n")

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


def run_turn(user_input: str):
    config = {
        "configurable": {
            "thread_id": THREAD_ID,
        }
    }

    snapshot = application_graph.get_state(config)

    if snapshot.values:
        messages = (
            snapshot.values["messages"]
            + [HumanMessage(content=user_input)]
        )

        state = {
            **snapshot.values,
            "messages": messages,
            "user_input": user_input,
        }
    else:
        state = {
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

    return application_graph.invoke(
        state,
        config=config,
    )


def main():
    print("\nTURN 1")
    print("=" * 60)

    turn_1 = (
        "I need to write an application to my college "
        "asking for three days leave because I am sick."
    )

    result = run_turn(turn_1)

    print_result(result)

    print("\n\nTURN 2")
    print("=" * 60)

    turn_2 = (
        "My name is Harsh Tiwari. "
        "I need leave from 10 September to 12 September."
    )

    result = run_turn(turn_2)

    print_result(result)


if __name__ == "__main__":
    main()