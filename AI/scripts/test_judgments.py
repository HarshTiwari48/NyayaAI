from app.services.judgement_service import search_judgments


def main() -> None:
    result = search_judgments(
        "online fraud cheating"
    )

    print("Total results:", result.get("found"))

    docs = result.get("docs", [])

    for doc in docs[:5]:
        print(
            doc.get("title"),
            "| ID:",
            doc.get("tid"),
        )


if __name__ == "__main__":
    main()