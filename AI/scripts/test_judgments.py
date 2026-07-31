from app.services.judgement_service import (
    retrieve_judgment_evidence,
)


def main() -> None:
    query = "online fraud cheating"

    evidence = retrieve_judgment_evidence(query)

    print(f"\nRetrieved passages: {len(evidence)}")

    for i, document in enumerate(evidence, start=1):
        print(
            f"\n{i}. {document.metadata['case_name']}"
        )

        print(
            "Score:",
            round(
                document.metadata["similarity_score"],
                4,
            ),
        )

        print(document.page_content[:400])


if __name__ == "__main__":
    main()