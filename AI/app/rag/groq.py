import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def get_groq_model() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0,
    )