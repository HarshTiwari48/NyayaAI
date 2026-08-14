from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
)

from langchain_core.messages import HumanMessage

from app.core.graph_service import graph
from app.core.state_factory import create_initial_state
from app.rag.loader import load_pdf

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
    thread_id: str,
):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    snapshot = graph.get_state(config)

    state = create_initial_state(request.query)

    if snapshot.values:
        state["messages"] = (
            snapshot.values["messages"]
            + [HumanMessage(content=request.query)]
        )

    result = graph.invoke(
        state,
        config=config,
    )

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
    query: str = Form(...),
    thread_id: str = Form(...),
    file: UploadFile = File(...),
):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    snapshot = graph.get_state(config)

    state = create_initial_state(query)

    if snapshot.values:
        state["messages"] = (
            snapshot.values["messages"]
            + [HumanMessage(content=query)]
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pages = load_pdf(file_path)

    state["user_documents"] = pages

    result = graph.invoke(
        state,
        config=config,
    )

    file_path.unlink(missing_ok=True)

    return AnalyzeResponse(
        answer=result["answer"],
        facts=result["facts"],
        legal_issues=result["legal_issues"],
        verified=result["verified"],
    )