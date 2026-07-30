import os

import requests
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://api.indiankanoon.org"


def search_judgments(query: str, page_num: int = 0) -> dict:
    api_key = os.getenv("INDIAN_KANOON_API_KEY")

    if not api_key:
        raise ValueError("INDIAN_KANOON_API_KEY is not configured.")

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