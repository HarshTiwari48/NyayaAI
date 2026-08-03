from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router




app = FastAPI(
    title="NyayaAI",
    version="1.0.0",
)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)