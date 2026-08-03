from app.core.graph_service import graph
from app.core.state_factory import create_initial_state
from fastapi import (
    APIRouter,
    File,
    UploadFile,
)
from app.core.state_factory import create_initial_state

from app.rag.loader import load_pdf

from pathlib import Path


from api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
)

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze(
    request: AnalyzeRequest,
):

    state = create_initial_state(request.query)

    result = graph.invoke(state)

    return AnalyzeResponse(
        answer=result["answer"],
        facts=result["facts"],
        legal_issues=result["legal_issues"],
        verified=result["verified"],
    )

@router.post(
    "/analyze-with-document",
    response_model=AnalyzeResponse,
)
async def analyze_document(
    query: str,
    file: UploadFile = File(...),
):

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pages = load_pdf(file_path)
    print("PAGES LOADED:", len(pages))

    state = create_initial_state(query)

    state["user_documents"] = pages
    print("STATE USER DOCS:", len(state["user_documents"]))

    print(state["user_documents"][0].page_content[:300])
    result = graph.invoke(state)
    file_path.unlink(missing_ok=True)

    return AnalyzeResponse(
        answer=result["answer"],
        facts=result["facts"],
        legal_issues=result["legal_issues"],
        verified=result["verified"],
    )