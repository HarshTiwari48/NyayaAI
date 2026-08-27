from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from app.graph.graph import build_graph
from app.rag.groq import get_groq_model
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import load_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_STORE_PATH = PROJECT_ROOT / "vector_store"


CHECKPOINT_DB = PROJECT_ROOT / "checkpoints.db"


embedding_model = get_embedding_model()

vector_store = load_vector_store(
    embedding_model=embedding_model,
    persist_directory=VECTOR_STORE_PATH,
)

print("\n========== VECTOR STORE DEBUG ==========")
print("Vector store path:", VECTOR_STORE_PATH.resolve())
print(
    "Document count:",
    vector_store._collection.count()
)
print("========================================\n")

from collections import Counter

all_data = vector_store.get(
    include=["metadatas"],
)

act_counts = Counter(
    metadata.get("act_code", "UNKNOWN")
    for metadata in all_data["metadatas"]
)

print("\n========== VECTOR STORE CONTENTS ==========")

for act_code, count in act_counts.items():
    print(f"{act_code}: {count}")

print("===========================================\n")

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