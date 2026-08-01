from fastapi import APIRouter
from app.services.graph_service import graph


from api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
)

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze(
    request: AnalyzeRequest,
):

    return AnalyzeResponse(
        answer=f"You asked: {request.query}"
    )