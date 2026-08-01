from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    answer: str