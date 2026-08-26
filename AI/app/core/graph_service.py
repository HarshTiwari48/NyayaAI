from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from app.graph.graph import build_graph
from app.rag.groq import get_groq_model
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_STORE_PATH = PROJECT_ROOT / "AI" / "vector_store"

CHECKPOINT_DB = PROJECT_ROOT / "checkpoints.db"


embedding_model = get_embedding_model()

vector_store = load_vector_store(
    embedding_model=embedding_model,
    persist_directory=VECTOR_STORE_PATH,
)

llm = get_groq_model()


checkpointer_cm = SqliteSaver.from_conn_string(
    str(CHECKPOINT_DB)
)

checkpointer = checkpointer_cm.__enter__()


graph = build_graph(
    llm=llm,
    vector_store=vector_store,
    checkpointer=checkpointer,
)