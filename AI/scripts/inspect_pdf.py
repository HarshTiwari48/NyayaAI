from pathlib import Path

from app.rag.loader import load_pdf
from app.rag.parser import parse_statute
from app.rag.chunker import chunk_sections


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BNS_PATH = PROJECT_ROOT / "Data" / "statutes" / "BNS.pdf"


# Load PDF
pages = load_pdf(BNS_PATH)

# Convert PDF pages into legal sections
sections = parse_statute(
    pages,
    act="Bharatiya Nyaya Sanhita, 2023",
    act_code="BNS",
)

# Split large sections into smaller chunks
chunks = chunk_sections(sections)


print(f"PDF pages: {len(pages)}")
print(f"Sections: {len(sections)}")
print(f"Chunks: {len(chunks)}")


# Inspect chunking of a large section
section_number = "318"

section_chunks = [
    chunk
    for chunk in chunks
    if chunk.metadata["section"] == section_number
]

print(f"\nSection {section_number} chunks: {len(section_chunks)}")

for chunk in section_chunks:
    print(
        f"Section {chunk.metadata['section']} | "
        f"Chunk {chunk.metadata['chunk_index']} | "
        f"Characters: {len(chunk.page_content)}"
    )
