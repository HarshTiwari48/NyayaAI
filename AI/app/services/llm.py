from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm() -> BaseChatModel:
    return ChatOllama(
        model="qwen3:0.6B",
        temperature=0,
        )
