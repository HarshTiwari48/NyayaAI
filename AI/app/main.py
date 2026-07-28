from fastapi import FastAPI

app = FastAPI(
    title="NyayaAI AI Service",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "nyaya-ai"
    }