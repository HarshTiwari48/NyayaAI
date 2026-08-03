from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    answer: str
    facts: List[str]
    legal_issues: List[str]
    verified: bool

