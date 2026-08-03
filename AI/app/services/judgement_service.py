import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.documents import Document

from app.rag.judgment_retriever import retrieve_judgment_passages

load_dotenv()

BASE_URL = "https://api.indiankanoon.org"


def clean_judgment_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    return soup.get_text(
        separator="\n",
        strip=True,
    )


def search_judgment_documents(
    query: str,
    limit: int = 3,
) -> list[Document]:

    search_result = search_judgments(query)
    results = search_result.get("docs", [])

    documents = []

    for result in results[:limit]:
        document_id = result.get("tid")

        if not document_id:
            continue

        judgment = get_judgment(document_id)

        if not judgment:
            continue

        text = clean_judgment_html(
            judgment.get("doc", "")
        )

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source_type": "judgment",
                    "document_id": document_id,
                    "case_name": judgment.get("title", ""),
                    "date": judgment.get("publishdate", ""),
                    "source": judgment.get("docsource", ""),
                },
            )
        )

    return documents


def get_judgment(document_id: int) -> dict:
    api_key = os.getenv("INDIAN_KANOON_API_KEY")

    if not api_key:
        raise ValueError("INDIAN_KANOON_API_KEY is not configured.")

    try:
        response = requests.post(
            f"{BASE_URL}/doc/{document_id}/",
            headers={
                "Authorization": f"Token {api_key}",
            },
            timeout=15,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Failed to fetch judgment {document_id}: {e}")
        return {}


def search_judgments(
    query: str,
    page_num: int = 0,
) -> dict:

    api_key = os.getenv("INDIAN_KANOON_API_KEY")

    if not api_key:
        raise ValueError("INDIAN_KANOON_API_KEY is not configured.")

    try:
        response = requests.post(
            f"{BASE_URL}/search/",
            headers={
                "Authorization": f"Token {api_key}",
            },
            data={
                "formInput": query,
                "pagenum": page_num,
            },
            timeout=15,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Indian Kanoon search failed: {e}")
        return {"docs": []}


def retrieve_judgment_evidence(
    query: str,
    case_limit: int = 3,
    passage_limit: int = 5,
) -> list[Document]:

    judgments = search_judgment_documents(
        query=query,
        limit=case_limit,
    )

    if not judgments:
        return []

    return retrieve_judgment_passages(
        query=query,
        documents=judgments,
        k=passage_limit,
    )
