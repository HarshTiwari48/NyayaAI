from app.graph.graph import build_graph
from app.services.llm import get_llm


def main() -> None:
    llm = get_llm()
    graph = build_graph(llm)

    result = graph.invoke(
        {
            "query": (
                "A person told me he would sell me a laptop, "
                "I transferred him the money and then he disappeared."
            ),
            "case_summary": "",
            "facts": [],
            "legal_issues": [],
            "research_queries": [],
            "research_sources": [],
            "evidence": [],
            "answer": "",
            "verified": False,
            "retry_count": 0,
        }
    )

    print("\nCASE SUMMARY")
    print(result["case_summary"])

    print("\nFACTS")
    for fact in result["facts"]:
        print("-", fact)

    print("\nLEGAL ISSUES")
    for issue in result["legal_issues"]:
        print("-", issue)


if __name__ == "__main__":
    main()